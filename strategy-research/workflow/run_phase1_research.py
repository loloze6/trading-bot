"""
=============================================================================
PHASE 1 ORCHESTRATOR: HYPOTHESIS & VALIDATION STATE MACHINE
=============================================================================
This script runs a file-driven, autonomous state machine that generates and 
ruthlessly validates quantitative trading hypotheses BEFORE any backtest code 
is written.

THE AGENTS (DIVISION OF LABOR):
1. Hypothesis Design    : Invents the core thesis (The Concept).
2. Innovation Expansion : Designs specific, testable variants (The Blueprints).
3. Quant Validation     : The Gatekeeper. Finds lookahead bias, overfitting, 
                          or missing data. (Outputs: Approve, Refine, or Reject).
4. Refinement Planner   : Translates "Refine" rejections into concrete action 
                          plans to fix the strategy or flag missing data.

THE ROUTING LOGIC:
- ✅ Path A (Approval)  : Validation -> [Approve] -> Moves to Phase 2 (Code).
- 🔄 Path B (Logic Fix) : Validation -> [Refine] -> Refinement Planner -> 
                          Loops back to Innovation Expansion to redraw the 
                          variants using the new plan.
- ⏸️ Path C (Data Block): Validation -> [Refine] -> Refinement Planner detects 
                          missing data -> Pipeline PAUSES for human audit.

THE HUMAN-IN-THE-LOOP (HITL) RESUME:
If paused for a data audit, the human downloads the data, writes 
`human_resolution.yaml`, and runs this script with `--resume`. 
Crucially, the pipeline resumes back to QUANT VALIDATION (not Phase 2), 
forcing the agent to officially review the human's data before approving.

SAFETY GUARDRAILS:
Controlled by `pipeline_state.yaml`. If the `refinements_used` counter hits
`max_refinements_after_validation`, the loop terminates to prevent infinite 
AI hallucination cycles.
=============================================================================
"""


from pathlib import Path
import yaml
from datetime import datetime, timezone
import argparse
import os
import re
import asyncio
import tempfile
import time
import subprocess
import json
import sys
import shutil
import statistics
import hashlib
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from google import genai
from google.genai import types

ROOT = Path(".")
CAMPAIGN_STATE_PATH = ROOT / "campaign_record" / "campaign_state.yaml"


def _resolve_tbot_python() -> Path:
    """Path to the trading-bot venv interpreter, relative to the CWD the script runs from.

    Windows layout is tried first so an upstream checkout resolves to exactly the
    interpreter it always has. A candidate must be a regular file AND executable:
    this repo has upstream's Windows venv committed, so venv/Scripts/python.exe
    exists on macOS too but cannot run there, and a bare directory would pass the
    executable check on its own because directories are searchable. No usable
    candidate raises rather than falling back to sys.executable — a silently wrong
    interpreter is the worst outcome here.
    """
    candidates = (
        Path("..") / "venv" / "Scripts" / "python.exe",
        Path("..") / ".venv" / "bin" / "python",
    )
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    raise RuntimeError(
        "No runnable trading-bot interpreter. Tried, relative to the current "
        f"directory {Path.cwd()}: " + ", ".join(str(c) for c in candidates)
    )


# Dynamic Stage Configurations
STAGE_CONFIGS = {
    "hypothesis_generation": {
        "handoff": "research_brief_to_hypothesis.yaml",
        # "required_outputs": [ARTIFACTS / "hypothesis_card.yaml"],
        "default_next": "innovation_expansion",
    },
    "innovation_expansion": {
        "handoff": "hypothesis_to_innovation_expansion.yaml",
        # "required_outputs": [
        #     ARTIFACTS / "expanded_hypothesis_card.yaml",
        #     ARTIFACTS / "innovation_notes.yaml",
        # ],
        "default_next": "validation",
    },
    "validation": {
        "handoff": "innovation_expansion_to_validation.yaml",
        # "required_outputs": [
        #     ARTIFACTS / "validation_protocol.yaml",
        #     ARTIFACTS / "validation_decision.yaml",
        # ],
        "default_next": "dynamic_routing", # Validation decides the next step
    },
    "refinement_planner": {
        "handoff": "validation_to_refinement.yaml",
        # "required_outputs": [ARTIFACTS / "refinement_notes.yaml"],
        "default_next": "innovation_expansion", # Route back to innovation after planning
    },
    "backtest_specification": {
        "handoff": "validation_to_backtest_specification.yaml",
        "default_next": "dynamic_routing",
    },
    # Improvement 08+09: prescreen stage (tool, no LLM)
    "signal_prescreen": {
        "handoff": "backtest_spec_to_signal_prescreen.yaml",
        "default_next": "dynamic_routing",
    },
    "protocol_execution": {
        "handoff": "backtest_spec_to_protocol_execution.yaml",
        "default_next": "verdict_interpreter",
    },
    "verdict_interpreter": {
        "handoff": "protocol_to_verdict_interpreter.yaml",
        "default_next": "dynamic_routing",
    },
    "campaign_review": {
        "handoff": "campaign_review.yaml",
        "default_next": "dynamic_routing",
    },
    # Improvement 06: holdout evaluation (tool stage, no LLM — single-use per hypothesis_id)
    "holdout_evaluation": {
        "handoff": "holdout_evaluation.yaml",
        "default_next": "dynamic_routing",
    },
}

# ---------------------------------------------------------------------------
# Campaign state (B3) — cross-run memory spanning all runs of one research question
# ---------------------------------------------------------------------------

def load_campaign_state() -> dict:
    """Load campaign_state.yaml, creating a blank one if absent."""
    if not CAMPAIGN_STATE_PATH.exists():
        return {
            "campaign_id":               "default",
            "research_question":         "",
            "runs":                      [],
            "altitude_history":          [],
            "recent_parameter_dimensions_by_family": {},
            "failed_families":           [],
            "instruments_tried":         [],
            "components_built":          [],
            "timeframes_tried":          ["1h"],
            "diagnostics_log":           [],
            "status":                    "active",
        }
    return load_yaml(CAMPAIGN_STATE_PATH)

def _save_campaign_state(state: dict):
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_yaml(CAMPAIGN_STATE_PATH, state)

def update_campaign_state_after_run(run_id: str, altitude: str, dimension: str,
                                     family: str, outcome: str, diagnostics: dict):
    """Append one run's outcome to campaign history and update derived fields."""
    state = load_campaign_state()
    state.setdefault("runs", [])
    if run_id not in state["runs"]:
        state["runs"].append(run_id)

    state.setdefault("altitude_history", [])
    state["altitude_history"].append({
        "run": run_id, "altitude": altitude,
        "dimension": dimension, "family": family, "outcome": outcome,
    })

    # F6 (2026-07-04): scoped PER hypothesis family — a global list let stale
    # dimension history from one family (e.g. Keltner-era 'regime_filter_er_threshold')
    # force an unrelated family's first refine attempt straight to pivot (run_044,
    # 2026-07-04). See _apply_circuit_breaker().
    if altitude == "parameter" and dimension:
        dims_by_family = state.setdefault("recent_parameter_dimensions_by_family", {})
        dims = dims_by_family.setdefault(family, [])
        if dimension not in dims:
            dims.append(dimension)

    state.setdefault("diagnostics_log", [])
    state["diagnostics_log"].append({"run": run_id, **diagnostics})

    _save_campaign_state(state)

def record_pivot(family: str):
    """Record a failed hypothesis family and reset ITS parameter-dimension counter
    only (F6, 2026-07-04) — other families' dimension history must survive untouched."""
    state = load_campaign_state()
    state.setdefault("failed_families", [])
    if family:
        state["failed_families"].append(family)
    state.setdefault("recent_parameter_dimensions_by_family", {})[family] = []
    _save_campaign_state(state)

def record_escalation(target: str, detail: str, protocol_path: str = None, claimed_by_run: str = None):
    """
    Record a search-space escalation.

    K3 (B10, §4): claimed_by_run/claimed_at mark the ONE run this escalation's
    last_escalation.protocol_path fallback is legitimate for -- mirroring the KB's
    own reactivation_consumed_by pattern. Set at the SAME call that sets
    last_escalation (this function already knows next_run_id at its call sites in
    _route_escalate), so the claim is never a separate, racy write.
    """
    state = load_campaign_state()
    if target == "instrument":
        state.setdefault("instruments_tried", [])
        if detail and detail not in state["instruments_tried"]:
            state["instruments_tried"].append(detail)
    elif target == "timeframe":
        state.setdefault("timeframes_tried", [])
        if detail and detail not in state["timeframes_tried"]:
            state["timeframes_tried"].append(detail)
    elif target == "new_component":
        state.setdefault("components_built", [])
        if detail and detail not in state["components_built"]:
            state["components_built"].append(detail)
    if protocol_path:
        last_escalation = {"target": target, "detail": detail, "protocol_path": protocol_path}
        if claimed_by_run:
            last_escalation["claimed_by_run"] = claimed_by_run
            last_escalation["claimed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        state["last_escalation"] = last_escalation
    _save_campaign_state(state)


def _mark_campaign_status(status: str):
    """Set the top-level status field in campaign_state."""
    state = load_campaign_state()
    state["status"] = status
    _save_campaign_state(state)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _quote_yaml_line(line: str) -> str:
    """Quote the value portion of a single YAML line that is causing a parse error."""
    import re
    stripped = line.lstrip()
    indent = len(line) - len(stripped)
    # List item scalar
    if stripped.startswith("- "):
        value = stripped[2:]
        if value and not value[0] in ('"', "'", "|", ">", "{", "["):
            q = value.replace('"', "'")
            return " " * indent + '- "' + q + '"'
    # Mapping value
    m = re.match(r'^(\s*)([\w _\-./]+):\s+(.+)$', line)
    if m:
        pre, key, value = m.groups()
        if value and not value[0] in ('"', "'", "|", ">", "{", "[", "~"):
            q = value.replace('"', "'")
            return pre + key + ': "' + q + '"'
    return line


def _is_list_item_start(stripped: str) -> bool:
    return stripped.startswith("- ")


def _is_mapping_start(stripped: str) -> bool:
    return bool(re.match(r'^[\w _\-./]+:\s', stripped)) or stripped.endswith(":")


def _repair_multiline_list_item(lines: list, line_idx: int):
    """
    F4b (2026-07-05, run_047): _quote_yaml_line only recognizes a colon on the
    SAME physical line as a `- ` marker or a `key:` mapping. It cannot repair a
    colon on a WRAPPED CONTINUATION line of a multi-line plain-scalar list item —
    e.g.:
        - 1h bar granularity is sufficient to capture post-settlement impulse
          (empirical lag: 0-2 bars from prior runs).
    where the second physical line has no `- ` or `key:` prefix of its own, so
    the single-line heuristic can't tell how to quote it and gives up
    ("unrepairable"), even though this is exactly the same class of LLM mistake
    F4 was built to catch — just spread across two lines instead of one.

    This walks backward from the failing continuation line to find the `- `
    marker it belongs to, walks forward to collect every subsequent
    continuation line (indented further than the marker, no `- `/`key:` of its
    own), folds them into ONE flattened plain-scalar value (per YAML's own
    line-folding rule: consecutive non-blank continuation lines join with a
    single space), and replaces the whole physical-line range with a single
    quoted line.

    Returns a NEW lines list (length may shrink) on success, or None if
    line_idx is not a continuation line this function can handle.
    """
    stripped = lines[line_idx].lstrip()
    if _is_list_item_start(stripped) or _is_mapping_start(stripped):
        return None  # not a continuation line — _quote_yaml_line already tried this shape

    indent = len(lines[line_idx]) - len(stripped)

    # Walk backward for the `- ` marker this line continues.
    start_idx = None
    i = line_idx - 1
    while i >= 0:
        li = lines[i]
        li_stripped = li.lstrip()
        if not li_stripped:
            break  # blank line — not part of the same scalar
        li_indent = len(li) - len(li_stripped)
        if _is_list_item_start(li_stripped) and li_indent < indent:
            start_idx = i
            break
        if li_indent <= indent and not _is_list_item_start(li_stripped) and not _is_mapping_start(li_stripped):
            i -= 1
            continue  # another continuation line at/below our indent — keep walking
        break  # hit something else (a key:, a deeper/shallower structure) — give up
    if start_idx is None:
        return None

    marker_indent = len(lines[start_idx]) - len(lines[start_idx].lstrip())

    # Walk forward from start_idx+1 collecting every continuation line (indented
    # deeper than the marker, no `- `/`key:` of its own) — may extend past
    # line_idx if the same logical scalar wraps further.
    end_idx = start_idx
    j = start_idx + 1
    while j < len(lines):
        lj = lines[j]
        lj_stripped = lj.lstrip()
        if not lj_stripped:
            break
        lj_indent = len(lj) - len(lj_stripped)
        if lj_indent > marker_indent and not _is_list_item_start(lj_stripped) and not _is_mapping_start(lj_stripped):
            end_idx = j
            j += 1
            continue
        break
    if end_idx <= start_idx:
        return None  # nothing to fold — not actually a wrapped continuation

    marker_value = lines[start_idx].lstrip()[2:]  # strip "- "
    continuation_values = [lines[k].strip() for k in range(start_idx + 1, end_idx + 1)]
    merged = " ".join([marker_value] + continuation_values)
    quoted = merged.replace('"', "'")
    new_line = " " * marker_indent + '- "' + quoted + '"'

    return lines[:start_idx] + [new_line] + lines[end_idx + 1:]


def _repair_yaml(content: str, source: str = "") -> str:
    """
    Iteratively repair LLM-generated YAML by using the parser's own error marks
    to find the exact failing line, quoting its value, and retrying.
    Handles both list-item colons and inline string colons.
    Logs each repair so silent fixes are auditable.
    """
    attempt = content
    for _ in range(30):
        try:
            list(yaml.safe_load_all(attempt))
            return attempt  # parsed successfully
        except yaml.YAMLError as e:
            mark = getattr(e, "problem_mark", None) or getattr(e, "context_mark", None)
            if mark is None:
                break
            line_idx = mark.line
            lines = attempt.split("\n")
            if line_idx >= len(lines):
                break
            original = lines[line_idx]
            fixed_line = _quote_yaml_line(original)
            if fixed_line != original:
                tag = f" [{source}]" if source else ""
                print(f"[YAML-REPAIR]{tag} line {line_idx + 1} quoted"
                      f"\n    was: {original[:120]}"
                      f"\n    now: {fixed_line[:120]}")
                lines[line_idx] = fixed_line
                attempt = "\n".join(lines)
                continue
            # F4b: single-line quoting made no change — try folding a wrapped
            # multi-line list-item continuation (see _repair_multiline_list_item).
            new_lines = _repair_multiline_list_item(lines, line_idx)
            if new_lines is not None:
                tag = f" [{source}]" if source else ""
                print(f"[YAML-REPAIR]{tag} line {line_idx + 1} folded a wrapped "
                      f"multi-line list item and quoted it"
                      f"\n    was: {original[:120]}")
                attempt = "\n".join(new_lines)
                continue
            break  # no change possible — give up
    return attempt


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    # First pass: standard parse (handles well-formed YAML)
    try:
        docs = list(yaml.safe_load_all(content))
        return docs[0] if docs else None
    except yaml.YAMLError:
        pass
    # Second pass: iterative repair (handles LLM colon/multi-doc errors)
    repaired = _repair_yaml(content, source=Path(path).name)
    docs = list(yaml.safe_load_all(repaired))
    return docs[0] if docs else None

def save_yaml(path: Path, data):
    """
    R4 (K4 kernel, 2026-07-13): writes via temp-file-then-os.replace in the
    destination's own directory, not a direct open(path, "w"). os.replace()
    is atomic on both POSIX and Windows (MoveFileEx w/ MOVEFILE_REPLACE_EXISTING) --
    a crash mid-write can no longer leave a partially-written/truncated
    pipeline_state.yaml (or any other file this function writes) in place;
    readers always see either the old complete content or the new complete
    content, never a partial one.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise

def update_state(path: Path, **kwargs):
    state = load_yaml(path / "pipeline_state.yaml")
    for key, value in kwargs.items():
        if isinstance(value, dict) and key in state and isinstance(state[key], dict):
            state[key].update(value) # Merge nested dicts (like counters)
        else:
            state[key] = value

    if "audit_log" not in state:
        state["audit_log"] = {}

    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_yaml(path / "pipeline_state.yaml", state)

class UnrepairableYAMLError(ValueError):
    """F4b: carries the offending path/content/parse-error so a caller can build
    a useful retry-with-context prompt, while remaining a plain ValueError for
    any existing `except ValueError` handling."""
    def __init__(self, path: Path, raw_content: str, parse_error: Exception):
        self.path = path
        self.raw_content = raw_content
        self.parse_error = parse_error
        super().__init__(f"YAML parse error in {path.name} (unrepairable): {parse_error}")


def ensure_files(paths):
    """
    F4 (P1a shakedown, 2026-07-04): previously did a bare `yaml.safe_load()` with no
    repair path, unlike `load_yaml()` (used for handoffs/state), which retries via
    `_repair_yaml()` (auto-quotes an unquoted-colon value using the parser's own error
    mark). This meant the EXACT failure mode every skill file explicitly warns about
    ("any string containing a colon MUST be quoted... violation halts the pipeline")
    crashed unrepaired specifically when it landed in a stage's own deliverable output
    (checked here, right after the LLM call) rather than in a handoff/state file —
    which is what happened to run_044's `expanded_hypothesis_card.yaml`
    (`library_category: structural_rate (composite: structural_rate + volatility ...)`).
    Now routes through the same repair path, and — unlike `load_yaml()`, which only
    repairs in-memory — persists the repaired content back to the file, since this
    function specifically validates freshly-produced stage deliverables that nothing
    else has had a chance to read yet.
    """
    missing = [str(p) for p in paths if not Path(p).exists()]
    if missing:
        raise FileNotFoundError(f"Missing files: {missing}")
    for p in paths:
        p = Path(p)
        if p.suffix in ('.yaml', '.yml'):
            content = p.read_text(encoding='utf-8')
            try:
                list(yaml.safe_load_all(content))
                continue
            except yaml.YAMLError:
                pass
            repaired = _repair_yaml(content, source=p.name)
            try:
                list(yaml.safe_load_all(repaired))
            except yaml.YAMLError as e:
                raise UnrepairableYAMLError(p, content, e)
            if repaired != content:
                p.write_text(repaired, encoding='utf-8')
                print(f"[YAML-REPAIR] {p.name} auto-repaired and written back to disk.")

def _build_yaml_retry_context(err: "UnrepairableYAMLError") -> str:
    """F4b: turn an UnrepairableYAMLError into a prompt-ready context block —
    the parse error plus a line-numbered window around the failing mark, so the
    retried LLM call can see exactly what it did wrong."""
    lines = err.raw_content.split("\n")
    mark = getattr(err.parse_error, "problem_mark", None) or getattr(err.parse_error, "context_mark", None)
    center = mark.line if mark is not None else 0
    lo = max(0, center - 3)
    hi = min(len(lines), center + 4)
    window = "\n".join(f"{i + 1}: {lines[i]}" for i in range(lo, hi))
    return (
        f"File: {err.path.name}\n"
        f"Parse error: {err.parse_error}\n"
        f"Lines around the failure (this file's own line numbers):\n{window}\n"
        f"Root cause is almost always an unquoted colon (:) inside a plain-text "
        f"value, INCLUDING one on a wrapped continuation line of a multi-line "
        f"list item. Quote the whole value, or keep it on one physical line."
    )



# SDK result-misclassification rider (2026-07-16, run_054+run_058 prior art;
# claude_agent_sdk==0.2.82 installed in this venv, verified against its own
# source this session, not assumed): the SDK's query loop
# (_internal/query.py) can raise a bare Exception whose message is the
# literal, self-contradictory string below. Root cause, read directly out of
# the installed package: when the CLI's result message carries
# `is_error=True` with an EMPTY `errors` list, the SDK falls back to that
# turn's own `subtype` field as the error text (_internal/query.py, the
# `if message.get("is_error"): ... self._last_error_result_text = ...`
# block, ~lines 302-307 in this install); if that `subtype` happens to be
# the literal string "success" -- an SDK-internal inconsistency
# (is_error=True paired with subtype="success"), not anything this
# orchestrator or the agent's own output did wrong -- a later ProcessError's
# message gets replaced with this exact nonsensical text (same file, the
# `except Exception as e: ... if isinstance(e, ProcessError) and
# self._last_error_result_text is not None: error_text = f"Claude Code
# returned an error result: {self._last_error_result_text}"` block, ~lines
# 326-342). There is no structured exception type upstream distinguishing
# this from a real failure -- bare Exception + EXACT string match is
# deliberate here, not a shortcut: a future reader must NOT broaden this
# into a general except-Exception catch-all, since that would also swallow
# real agent/CLI failures that happen to share the generic "Claude Code
# returned an error result: ..." prefix with a genuine, different subtype.
_SDK_ERROR_RESULT_SUCCESS_MSG = "Claude Code returned an error result: success"


def _invoke_agent_with_yaml_retry(current_stage: str, run_id: str, run_dir: Path, expected_outputs: list, state: dict):
    """
    F4b (2026-07-05, run_047): invoke the agent for `current_stage`; if its
    deliverable is unrepairable YAML, retry the SAME stage exactly ONCE with the
    parse error + offending lines appended to the prompt (see
    _build_yaml_retry_context). If the retry's output ALSO fails parse+repair,
    re-raise — fails to human, unchanged from pre-F4b behavior. Every retry is
    logged to pipeline_state.yaml's `yaml_retry_count` so a chronically-sloppy
    stage is visible across runs, not just in this run's console log.
    """
    retry_ctx = None
    for attempt in range(2):
        for sdk_attempt in range(2):
            try:
                asyncio.run(async_invoke_agent(current_stage, run_id, retry_context=retry_ctx))
                break
            except Exception as sdk_err:
                if sdk_attempt == 0 and str(sdk_err) == _SDK_ERROR_RESULT_SUCCESS_MSG:
                    print(f"⚠️ [SDK-RETRY] {current_stage}: claude_agent_sdk 0.2.82 "
                          f"result-misclassification defect (is_error=True/subtype="
                          f"'success' contradiction) — re-invoking once, prompt unchanged.")
                    continue
                raise  # any other message, or a second occurrence — unchanged
        try:
            ensure_files(expected_outputs)
            return
        except UnrepairableYAMLError as err:
            if attempt == 0:
                retry_count = state.get("yaml_retry_count", 0) + 1
                update_state(path=run_dir, yaml_retry_count=retry_count)
                print(f"⚠️ [F4b] {current_stage}: unrepairable YAML on first attempt — "
                      f"retrying once with error context appended "
                      f"(yaml_retry_count={retry_count}).\n    {err}")
                retry_ctx = _build_yaml_retry_context(err)
                continue
            raise  # retry ALSO failed — fail to human as before, unchanged


# F4c (2026-07-05, run_047 budget investigation): relative cost weights per
# token class, matching Anthropic's published per-token pricing ratios (output
# ~5x input; cache_read ~0.1x input — a 90% discount; cache_creation ~1.25x
# input — a 25% write premium). A raw token SUM treats a cheap cache-read
# token identically to an expensive fresh-output token, which let a single
# validation call's 836,461 cache_read tokens (heavily-discounted reuse, not
# fresh cost) dominate the old budget check as if it were 836,461 equally
# expensive tokens. Weighted units approximate the ACTUAL relative dollar cost
# of what was consumed.
_TOKEN_WEIGHT_INPUT = 1.0
_TOKEN_WEIGHT_OUTPUT = 5.0
_TOKEN_WEIGHT_CACHE_READ = 0.1
_TOKEN_WEIGHT_CACHE_CREATION = 1.25


def _weighted_token_units(input_tokens: int, output_tokens: int, cache_read: int, cache_creation: int) -> float:
    return (
        input_tokens * _TOKEN_WEIGHT_INPUT
        + output_tokens * _TOKEN_WEIGHT_OUTPUT
        + cache_read * _TOKEN_WEIGHT_CACHE_READ
        + cache_creation * _TOKEN_WEIGHT_CACHE_CREATION
    )


def _compute_weighted_budget_usage(audit_log: dict) -> tuple:
    """
    F4c: sum weighted token units across every audit_log entry. Returns
    (total_weighted, [(stage_attempt_name, weighted_units), ...]).
    Handles both F4c-era entries (which already carry a `weighted` field) and
    pre-F4c entries (derives it from the raw components) so old runs' logs
    still compute a sensible number without a migration step.
    """
    total_weighted = 0.0
    stage_breakdown = []
    for name, entry in audit_log.items():
        tokens = entry.get("tokens")
        if isinstance(tokens, dict):
            if "weighted" in tokens:
                w = tokens["weighted"]
            else:
                w = _weighted_token_units(
                    tokens.get("input", 0), tokens.get("output", 0),
                    tokens.get("cache_read", 0), tokens.get("cache_creation", 0),
                )
        else:
            w = entry.get("total_estimated_tokens", 0)  # manual estimator path
        total_weighted += w
        stage_breakdown.append((name, w))
    return total_weighted, stage_breakdown


def _load_token_budget() -> float:
    """
    F4c: unlike every other campaign_config.yaml constant in this file (declared
    parity only, enforced by test_campaign_config_sync.py — see that file's
    module docstring), this ONE constant is read at runtime by explicit request:
    the token budget is an operational knob campaign operators need to tune
    per-run-shape without a code change, not a fixed statistical/architectural
    constant like block_size_1h.
    """
    p = Path(__file__).parent.parent / "config" / "campaign_config.yaml"
    default = 300000.0
    if not p.exists():
        return default
    with open(p, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return float(cfg.get("orchestrator", {}).get("token_budget_per_run_weighted_units", default))


def estimate_tokens(text: str) -> int:
    """Provides a rough token estimation (1 token ≈ 4 chars)."""
    return len(str(text)) // 4

# def check_context_limits(stage_name: str, full_prompt: str, max_window: int = 100000):
#     """Monitors the payload size and warns/halts if nearing limits."""
#     estimated_tokens = estimate_tokens(full_prompt)
#     # print(f"📊 [METRICS] {stage_name} Payload: ~{estimated_tokens:,} tokens")
    
#     if estimated_tokens > max_window * 0.8:
#         print("⚠️ WARNING: Context window is at 80% capacity. Risk of model degradation.")
#     if estimated_tokens > max_window:
#         raise ValueError(f"CRITICAL: Context window exceeded ({estimated_tokens:,} > {max_window:,}). Pipeline halted.")
        
#     return estimated_tokens

async def run_claude_worker(stage_name: str, handoff: str, path: Path, retry_context: str | None = None):

    print(f"\n🧠 [AGENT INVOKED] Waking up specialist for: {stage_name}"
          + (" (YAML-repair retry)" if retry_context else ""))
    
    
    # 2. Map the stage to the correct SKILL definition
    skill_map = {
        "hypothesis_generation": "hypothesis-design",
        "innovation_expansion": "innovation-expansion",
        "validation": "quant-validation",
        "refinement_planner": "refinement-planner",
        "backtest_specification": "backtest-engineering",
        "verdict_interpreter": "verdict-interpreter",
        "campaign_review": "campaign-review",
    }

    skill_file_name = skill_map.get(stage_name)
    if not skill_file_name:
        raise ValueError(f"No SKILL file mapped for stage: {stage_name}")

    skill_path = Path(".") / "workflow_artifacts" / "skills" / skill_file_name / "SKILL.md"
    with open(skill_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 3. Gather Context
    context_blocks = []
    inputs_to_read = handoff.get("required_inputs", []) + handoff.get("optional_inputs", [])
    
    for req in inputs_to_read:
        filepath = path / req["path"]
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            context_blocks.append(f"--- CONTENT OF {req['path']} ---\n{content}\n")
        elif req in handoff.get("required_inputs", []):
            raise FileNotFoundError(f"Agent strictly requires {filepath}, but it is missing.")

    b7_deference_block = (
        f"\n    {_B7_DEFERENCE_SENTENCE}\n"
        if stage_name in _B7_MANDATORY_INPUT_STAGES else ""
    )

    # 4. Construct the strict prompt (Combining Persona + Instructions)
    full_prompt = f"""
    PERSONA AND RULES:
    {system_prompt}

    YOUR HANDOFF INSTRUCTIONS:
    {yaml.dump(handoff, sort_keys=False)}

    YOUR PROVIDED CONTEXT FILES:
    {chr(10).join(context_blocks)}
    {b7_deference_block}
    INSTRUCTIONS FOR OUTPUT:
    Fulfill the objective defined in the handoff. You must generate the exact deliverables requested.
    Output ONLY valid YAML blocks for your deliverables. Do not output conversational filler.

    YAML FORMATTING RULES (violations will crash the pipeline):
    - Any string value containing a colon (:) MUST be wrapped in double quotes.
    - Example bad:  description: Split into windows (0.0-0.15, 0.15-0.25, 0.25+) to verify costs
    - Example good: description: "Split into windows (0.0-0.15, 0.15-0.25, 0.25+) to verify costs"
    - When in doubt, quote the entire value.
    - F4b: keep each list item ("- ...") on a SINGLE physical line. Do NOT wrap a
      long list item onto a second indented line — a colon appearing on that
      wrapped continuation line is just as fatal as one on the first line, and
      is harder to auto-repair. If a value is long, either keep it on one line
      or use a block scalar (- >) rather than manual line-wrapping.

    You MUST use this exact format for each deliverable so my script can parse it:

    ```yaml
    # filename.yaml
    <your yaml content here>
    ```
    """

    if retry_context:
        full_prompt += f"""

    YOUR PREVIOUS ATTEMPT FAILED TO PARSE AS YAML:
    {retry_context}

    Fix the exact issue described above and regenerate ALL deliverables from
    scratch, following the YAML FORMATTING RULES precisely this time.
    """

    # --- PRE-FLIGHT SAFETY RADAR ---
    start_time = time.time()
    # check_context_limits(stage_name, full_prompt, max_window=150000)

    # 5. Invoke the Agent and Stream the Response (with strict tool constraints to enforce handoff rules)
    print("⏳ Waiting for Claude CLI response...")
    agent_output = ""
    exact_usage = {}
    total_cost = 0.0
    num_turns = None

    # We pass an empty allowed_tools list to prevent it from wandering off
    # and strictly enforce our handoff file constraints.
    async for message in query(
        prompt=full_prompt,
        options=ClaudeAgentOptions(model= "claude-haiku-4-5",allowed_tools=[])
    ):
        # Accumulate text content from assistant messages
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    agent_output += block.text
        # --- Optional: NATIVE COST TRACKING ---
        if hasattr(message, "total_cost_usd"):
            exact_usage = getattr(message, "usage", {})
            total_cost = getattr(message, "total_cost_usd", 0.0)
            num_turns = getattr(message, "num_turns", None)

    # --- OPTIONAL METRICS POST-FLIGHT CALCULATION ---
    execution_time = round(time.time() - start_time, 2)

    input_tokens = exact_usage.get("input_tokens", 0)
    output_tokens = exact_usage.get("output_tokens", 0)
    cache_read = exact_usage.get("cache_read_input_tokens", 0)
    cache_creation = exact_usage.get("cache_creation_input_tokens", 0)
    total_tokens = input_tokens + output_tokens + cache_read + cache_creation
    # F4c (2026-07-05, run_047 budget investigation): the SDK's `usage` on the
    # final ResultMessage is CUMULATIVE FOR THE SESSION (see claude_agent_sdk
    # types.py: "Cumulative API usage for the session"), i.e. across every
    # internal turn (`num_turns`) the model took to produce this stage's
    # deliverable — not a single-call snapshot. A stage that needed several
    # internal turns will show a much larger token count than its final
    # deliverable's file size would suggest; num_turns is what makes that
    # attributable at a glance instead of looking like unexplained bloat.
    weighted_units = round(_weighted_token_units(
        input_tokens, output_tokens, cache_read, cache_creation
    ), 1)

    print(f"⏱️ Finished in {execution_time}s")
    print(f"💰 Cost Estimate: ${total_cost:.4f} | Tokens: {total_tokens:,} (Cache Read: {cache_read:,}) "
          f"| Weighted: {weighted_units:,} | Turns: {num_turns}")

    # 4. Save to the central audit ledger
    attempt_num = handoff.get('injected_context', {}).get('refinement_attempt', '0')
    log_entry = {
        f"{stage_name}_attempt_{attempt_num}": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine": "claude-agent-sdk",
            "execution_time_seconds": execution_time,
            "cost_usd": total_cost,
            "num_turns": num_turns,
            "tokens": {
                "input": input_tokens,
                "output": output_tokens,
                "cache_read": cache_read,
                "cache_creation": cache_creation,
                "total": total_tokens,
                "weighted": weighted_units,
            }
        }
    }
    update_state(path=path, audit_log=log_entry)


    # 6. Parse and Save the Deliverables
    pattern = r"```yaml\s*#\s*([a-zA-Z0-9_.]+\.yaml)\s*(.*?)```"
    matches = re.findall(pattern, agent_output, re.DOTALL)
    
    if not matches:
        print("⚠️ Warning: Could not parse standard YAML blocks. Saving raw output for debug.")
        debug_path = path / "artifacts" / f"debug_{stage_name}_raw_output.txt"
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(agent_output)
        return

    saved_files = []
    for filename, yaml_content in matches:
        dest_path = path / "artifacts" / filename.strip()
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(yaml_content.strip())
        saved_files.append(filename.strip())
        
    print(f"✅ [AGENT COMPLETE] Successfully wrote deliverables: {', '.join(saved_files)}")



# Initialize the Native Client lazily, so importing this module does not
# construct it or require GEMINI_API_KEY. Construction still auto-reads
# GEMINI_API_KEY from the environment on first use, as before.
_client = None


def _get_client():
    global _client
    if _client is None:
        _client = genai.Client()
    return _client

async def run_gemini_worker(stage_name: str, handoff: dict, run_dir: Path):
    print(f"\n✨ [GEMINI INVOKED] Waking up Native Gemini API for: {stage_name}")
    
    # 2. Map the stage to the correct SKILL definition
    skill_map = {
        "hypothesis_generation": "hypothesis-design",
        "innovation_expansion": "innovation-expansion",
        "validation": "quant-validation",
        "refinement_planner": "refinement-planner",
        "backtest_specification": "backtest-engineering",
        "verdict_interpreter": "verdict-interpreter",
        "campaign_review": "campaign-review",
    }

    skill_file_name = skill_map.get(stage_name)
    if not skill_file_name:
        raise ValueError(f"No SKILL file mapped for Gemini stage: {stage_name}")
        
    # --- FIX 3: Point to the 'skills' directory ---
    skill_path = Path(".") / "workflow_artifacts" / "skills" / skill_file_name / "SKILL.md"
    with open(skill_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 2. Gather Context
    context_blocks = []
    inputs_to_read = handoff.get("required_inputs", []) + handoff.get("optional_inputs", [])
    
    for req in inputs_to_read:
        filepath = run_dir / req["path"]
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            context_blocks.append(f"--- CONTENT OF {req['path']} ---\n{content}\n")

    b7_deference_block = (
        f"\n    {_B7_DEFERENCE_SENTENCE}\n"
        if stage_name in _B7_MANDATORY_INPUT_STAGES else ""
    )

    full_prompt = f"""
    YOUR HANDOFF INSTRUCTIONS:
    {yaml.dump(handoff, sort_keys=False)}

    YOUR PROVIDED CONTEXT FILES:
    {chr(10).join(context_blocks)}
    {b7_deference_block}
    YAML FORMATTING RULES (violations will crash the pipeline):
    - Any string value containing a colon (:) MUST be wrapped in double quotes.
    - Example bad:  description: Split into windows (0.0-0.15, 0.15-0.25, 0.25+) to verify costs
    - Example good: description: "Split into windows (0.0-0.15, 0.15-0.25, 0.25+) to verify costs"
    - When in doubt, quote the entire value.
    """

    # --- PRE-FLIGHT SAFETY RADAR ---
    start_time = time.time()
    # Gemini has a massive context window, but we still protect our budget
    # estimated_prompt_tokens = check_context_limits(stage_name, full_prompt, max_window=200000)

    print("⏳ Waiting for Gemini API response...")
    
    # --- FIX 1 & 2: Use the async '.aio' client and correct model name ---
    response = await _get_client().aio.models.generate_content(
        model='gemini-2.5-flash-lite',
        contents=full_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2, # Keep the quant bot logical and deterministic
            max_output_tokens=4000, # <-- LAYER 3 HARD LIMIT
            safety_settings=[
                {
                    "category": types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
                {
                    "category": types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    "threshold": types.HarmBlockThreshold.BLOCK_NONE,
                },
            ]
        ),
        
    )
    
    agent_output = response.text

    # --- METRICS POST-FLIGHT CALCULATION ---
    execution_time = round(time.time() - start_time, 2)
    
    # Extract perfect Native Token tracking from the response object
    exact_input_tokens = response.usage_metadata.prompt_token_count
    exact_output_tokens = response.usage_metadata.candidates_token_count
    total_tokens = exact_input_tokens + exact_output_tokens

    print(f"⏱️ Finished in {execution_time}s | Output: {exact_output_tokens:,} tokens")

    # 4. Save to the central audit ledger
    attempt_num = handoff.get('injected_context', {}).get('refinement_attempt', '0')
    log_entry = {
        f"{stage_name}_attempt_{attempt_num}": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine": "gemini-native-api",
            "execution_time_seconds": execution_time,
            "tokens": {
                "input": exact_input_tokens,
                "output": exact_output_tokens,
                "total": total_tokens
            }
        }
    }
    update_state(path=run_dir, audit_log=log_entry)

    # 5. Simple Stage-Based Saving
    blocks = re.sub(r'^[a-zA-Z0-9_\-.]+\.yaml\s*\n', '', agent_output.strip())
    yaml_blocks = re.findall(r"```yaml\s*(.*?)\s*```", blocks, re.DOTALL)
    
    if yaml_blocks:
        # Define exactly what files each stage is supposed to emit in order
        stage_outputs = {
            "hypothesis_generation": ["hypothesis_card.yaml"],
            "innovation_expansion": ["expanded_hypothesis_card.yaml", "innovation_notes.yaml"],
            "validation": ["validation_protocol.yaml", "validation_decision.yaml"],
            "refinement_planner": ["refinement_notes.yaml"]
        }
        
        expected_files = stage_outputs.get(stage_name, [f"{stage_name}_output.yaml"])
        saved_files = []
        
        # Match each extracted block to its expected filename
        for i, block_content in enumerate(yaml_blocks):
            if i < len(expected_files):
                filename = expected_files[i]
            else:
                filename = f"{stage_name}_extra_{i}.yaml"
                
            dest_path = run_dir / "artifacts" / filename
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(block_content.strip())
            saved_files.append(filename)
            
        print(f"✅ [WORKER COMPLETE] Successfully wrote deliverables: {', '.join(saved_files)}")
    else:
        print(f"⚠️ Warning: No yaml blocks found in output. Saving raw debug file.")
        debug_path = run_dir / "artifacts" / f"debug_{stage_name}_raw_output.txt"
        with open(debug_path, "w", encoding="utf-8") as f:
            f.write(agent_output)

async def run_tool_worker(stage_name: str, run_id: str):
    """Executes a deterministic tool stage. No LLM call. No token cost."""
    RUN_DIR = ROOT / "runs" / run_id
    ARTIFACTS = RUN_DIR / "artifacts"
    TBOT_PYTHON = _resolve_tbot_python()

    if stage_name == "signal_prescreen":
        # Improvement 08+09: signal prescreen — cheap IC + cost gate before full backtest.
        config_path = ARTIFACTS / "candidate_strategy_config.json"

        # K3/§9 Q4: consolidated resolver, replaces the previously-duplicated
        # inline protocol-selection logic (also present in protocol_execution below).
        protocol_path = _resolve_protocol_path(RUN_DIR, run_id)

        out_dir = RUN_DIR / "prescreen"
        cmd = [
            str(TBOT_PYTHON), str(ROOT / "tools" / "prescreen_signal.py"),
            str(config_path), str(protocol_path),
            "--run-id", run_id,
            "--out-dir", str(out_dir),
        ]
        print("🔬 Running signal prescreen (Improvement 08+09)...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            raise RuntimeError(f"prescreen_signal.py failed:\n{result.stderr}")

        prescreen_path = out_dir / "prescreen_result.yaml"
        if not prescreen_path.exists():
            raise FileNotFoundError("prescreen_result.yaml not found after prescreen run")

        # Copy to artifacts so verdict_interpreter can read it
        import shutil as _ps_shutil
        _ps_shutil.copy(prescreen_path, ARTIFACTS / "prescreen_result.yaml")

        ps = load_yaml(ARTIFACTS / "prescreen_result.yaml")
        route = ps.get("route", "unknown")
        print(f"✅ Prescreen complete. Route: {route} | "
              f"IC={ps.get('ic_spearman_pooled')} | "
              f"cost_pass={ps.get('cost_check', {}).get('pass')}")

        # A6.2: record prescreen as a trial in campaign_state (even kills count as trials)
        # statistic_valid = "neither" for kills (no backtest Sharpe available)
        # F3 idempotency hardening (2026-07-04): the two A8.6 bypass call sites in
        # run_loop already guard this with an existing-trial_id check; this, the normal
        # (non-bypass) call site, did not. Not live-triggered by the run_043 resume
        # (which restarts past this stage), but a resume that ever re-entered
        # signal_prescreen would otherwise double-record. Matching the same guard here.
        _campaign_for_guard = load_campaign_state()
        if not any(t.get("trial_id") == run_id for t in _campaign_for_guard.get("trial_sharpes", [])):
            _record_prescreen_trial(run_id, ps, config_path)
        else:
            print(f"⏭️  A6.2: trial for {run_id} already recorded — skipping duplicate.")

    elif stage_name == "protocol_execution":
        config_path     = ARTIFACTS / "candidate_strategy_config.json"
        # K3/§9 Q4: consolidated resolver, replaces the previously-duplicated
        # inline protocol-selection logic (also present in signal_prescreen above).
        protocol_path = _resolve_protocol_path(RUN_DIR, run_id)
        validation_path = ARTIFACTS / "validation_protocol.yaml"

        cmd = [
            str(TBOT_PYTHON), str(ROOT / "tools" / "run_protocol.py"),
            str(config_path), str(protocol_path),
            "--validation-protocol", str(validation_path),
            "--out-dir", str(RUN_DIR),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            raise RuntimeError(f"run_protocol.py failed:\n{result.stderr}")

        summary_path = RUN_DIR / "protocol_summary.json"
        if not summary_path.exists():
            raise FileNotFoundError("protocol_summary.json not found after protocol run")

        with open(summary_path, encoding="utf-8") as f:
            summary = json.load(f)
        save_yaml(ARTIFACTS / "protocol_result.yaml", summary)
        hv = (summary.get("hypothesis_verdict") or {}).get("verdict", "unknown")
        print(f"✅ Protocol complete. Hypothesis verdict: {hv}")

        # C7 (K2 kernel, 2026-07-13): machine-checkable pass-rule evaluation --
        # replaces evaluate_against_decision_rules (tools/run_protocol.py's own
        # prose-criteria parser) as the DECISION authority; that function's
        # output remains informational only from here on (see design note
        # section 6). Writes pass_rule_evaluation.yaml, a REQUIRED input for
        # the verdict_interpreter stage (workflow_artifacts/skills/verdict-interpreter/SKILL.md).
        # R3 (K2 Phase B operator ruling): evaluate_pass_rule_criteria() never
        # raises on a legacy (string-shaped or absent) pass_rule -- it returns
        # 'legacy_not_evaluable', and the LLM stage's own judgment applies
        # exactly as it did before K2 (every run's pre_registration.yaml
        # before this kernel, including run_057's own, is this legacy shape).
        _tools_path = str(Path(__file__).parent.parent / "tools")
        if _tools_path not in sys.path:
            sys.path.insert(0, _tools_path)
        import verdict_criteria_evaluator as _vce
        _pre_reg_path = ARTIFACTS / "pre_registration.yaml"
        _pre_reg_for_eval = load_yaml(_pre_reg_path) if _pre_reg_path.exists() else {}
        # C7-EXT (2026-07-22): the brief is now an evaluator input -- G1 needs
        # product/timeframe/rebalance to decide whether funding must be modeled.
        _brief_path = ARTIFACTS / "research_brief.yaml"
        _brief_for_eval = (load_yaml(_brief_path) if _brief_path.exists() else {}) or {}
        _pass_rule_eval = _vce.evaluate_pass_rule_criteria(
            summary, _pre_reg_for_eval or {}, _brief_for_eval)
        _pass_rule_eval["evaluated_at"] = datetime.now(timezone.utc).isoformat()
        _pass_rule_eval["evaluator_version"] = 2  # C7-EXT: G1-G5 preconditions
        save_yaml(ARTIFACTS / "pass_rule_evaluation.yaml", _pass_rule_eval)
        _pre_reg_result = _pass_rule_eval.get("result")
        print(f"✅ [C7] pass_rule_evaluation.yaml written: result={_pre_reg_result}"
              + (f" verdict={_pass_rule_eval.get('hypothesis_verdict')}/"
                 f"{_pass_rule_eval.get('lineage_routing')}"
                 if _pre_reg_result in ("PASS", "FAIL") else ""))

        # A6.2: record full-backtest trial in campaign_state.trial_sharpes
        _record_backtest_trial(run_id, summary, config_path)

        # Verify Phase A diagnostics are present
        result_data = load_yaml(ARTIFACTS / "protocol_result.yaml")
        hv_block = result_data.get("hypothesis_verdict") or {}
        diagnostics = hv_block.get("diagnostics") or {}
        missing = [f for f in ["median_gross_pnl", "median_forecast_return_corr",
                                "median_cost_drag_pct"] if diagnostics.get(f) is None]
        if missing:
            print(f"⚠️ WARNING: diagnostics block missing fields: {missing}")
            print("   Phase A metrics unavailable — verdict_interpreter will have reduced signal.")
            print("   Check run_artifact.py build_core and ensure trading-bot venv has scipy.")
        else:
            print(f"✅ Diagnostics verified: corr={diagnostics['median_forecast_return_corr']:.3f}, "
                  f"cost_drag={diagnostics['median_cost_drag_pct']:.1f}%, "
                  f"gross_pnl={diagnostics['median_gross_pnl']:.2f}")
    else:
        raise ValueError(f"No tool implementation for stage: {stage_name}")


# B7: stages at/after the validation gate must see the pre-registered
# pass_rule and original brief regardless of what a given run's handoff
# happens to list -- engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md B7 (three
# in-the-wild occurrences of a stage deciding without ever reading
# pre_registration.yaml, most recently run_058's validation_decision.yaml
# misdescribing the very registration it vetoed). This is a deterministic
# union, not stage discretion: each path is added to required_inputs only
# when the file actually exists on disk for the run (missing files are
# skipped, never force-required), so the union degrades gracefully on
# older runs that predate pre_registration.yaml/user_brief_verbatim.yaml.
_B7_MANDATORY_INPUT_PATHS = (
    "artifacts/pre_registration.yaml",
    "artifacts/user_brief_verbatim.yaml",
)
_B7_MANDATORY_INPUT_STAGES = {
    "validation",
    "refinement_planner",
    "backtest_specification",
    "verdict_interpreter",
    "campaign_review",
}
_B7_DEFERENCE_SENTENCE = (
    "B7: pre-registered artifacts (pre_registration.yaml / "
    "user_brief_verbatim.yaml, if provided above) outrank any "
    "stage-generated card on any conflict -- defer to them."
)


def _apply_b7_mandatory_inputs(stage_name: str, handoff: dict, run_dir: Path) -> None:
    """Union B7's mandatory pre-registration inputs into handoff['required_inputs']
    for validation and every downstream LLM stage, deduplicated, skipping any
    path that does not exist on disk for this run."""
    if stage_name not in _B7_MANDATORY_INPUT_STAGES:
        return
    required = handoff.setdefault("required_inputs", [])
    existing_paths = {req["path"] for req in required}
    for mandatory_path in _B7_MANDATORY_INPUT_PATHS:
        if mandatory_path in existing_paths:
            continue
        if not (run_dir / mandatory_path).exists():
            continue
        required.append({
            "path": mandatory_path,
            "reason": "B7 mandatory input: pre-registered pass_rule/brief outrank stage-generated cards on any conflict.",
        })
        existing_paths.add(mandatory_path)


async def async_invoke_agent(stage_name: str, run_id: str, retry_context: str | None = None):
    tool_stages = {"protocol_execution", "signal_prescreen"}
    if stage_name in tool_stages:
        await run_tool_worker(stage_name, run_id)
        return

    RUN_DIR = ROOT / "runs" / run_id
    HANDOFFS = RUN_DIR / "handoffs"
    config = STAGE_CONFIGS[stage_name]
    handoff_path = HANDOFFS / config["handoff"]

    # 1. Load the live handoff file
    handoff = load_yaml(handoff_path)

    # B7: deterministic mandatory-inputs union (see helper docstring above).
    _apply_b7_mandatory_inputs(stage_name, handoff, RUN_DIR)

    # Select engine from handoff file, default to Claude if not specified
    engine = handoff.get("assigned_engine", "claude")

    if engine == "claude":
        # Fires the Claude Agent SDK worker
        return await run_claude_worker(stage_name, handoff, RUN_DIR, retry_context=retry_context)
    elif engine == "gemini":
        # Fires the Gemini API worker
        return await run_gemini_worker(stage_name, handoff, RUN_DIR)

def determine_post_refinement_route(path: Path):
    """Checks if refinement requires a human pause or loops back to innovation."""
    refinement_path = path / "artifacts" / "refinement_notes.yaml"
    refinement = load_yaml(refinement_path)
    
    # Check the flag from the Refinement Planner
    implementation_allowed = refinement.get("decision", {}).get("implementation_allowed", True)
    
    if not implementation_allowed:
        print("\n⏸️ PIPELINE PAUSED: Human Intervention Required.")
        print("Please review artifacts/refinement_notes.yaml.")
        print("When complete, create artifacts/human_resolution.yaml and run with --resume.")
        update_state(path=path, status="paused_for_human")
        return "human_pause" # Halts the while loop
    
    return "innovation_expansion" # Otherwise, loop back for another try

def _create_a86_validation_bypass_handoffs(run_id: str, run_dir: Path):
    """
    A8.6 Fix 2: create minimal handoffs for the power-gate bypass path.
    Used when A8.6 blocks at the validation gate (before backtest_specification runs).
    Creates signal_prescreen and verdict_interpreter handoffs with only the artifacts
    that actually exist (prescreen_result.yaml, hypothesis_card.yaml).
    """
    handoffs = run_dir / "handoffs"
    handoffs.mkdir(exist_ok=True)

    # Overwrite signal_prescreen handoff with a minimal version that has no missing inputs
    sp_path = handoffs / "backtest_spec_to_signal_prescreen.yaml"
    save_yaml(sp_path, {
        "handoff_version": 1, "run_id": run_id,
        "from_stage": "validation", "to_stage": "signal_prescreen",
        "assigned_engine": "tool",
        "objective": (
            "A8.6 power gate triggered at validation — prescreen_result.yaml already written. "
            "No prescreen tool runs; prescreen stage is a pass-through."
        ),
        "required_inputs": [
            {"path": "artifacts/prescreen_result.yaml",
             "reason": "A8.6 power gate output — written at validation stage"},
        ],
        "deliverables": [],
    })

    # Create verdict_interpreter handoff for the A8.6 path
    vi_path = handoffs / "protocol_to_verdict_interpreter.yaml"
    if not vi_path.exists():
        save_yaml(vi_path, {
            "handoff_version": 1, "run_id": run_id,
            "from_stage": "signal_prescreen", "to_stage": "verdict_interpreter",
            "assigned_engine": "claude",
            "objective": (
                "Interpret A8.6 power gate result. Hypothesis was blocked before component build. "
                "Produce verdict_interpretation.yaml with parked disposition and data requirement."
            ),
            "required_inputs": [
                {"path": "artifacts/prescreen_result.yaml",
                 "reason": "A8.6 power check result — no IC computed; power metrics are the evidence"},
                {"path": "artifacts/hypothesis_card.yaml",
                 "reason": "hypothesis parameters for reactivation_condition"},
            ],
            "deliverables": ["verdict_interpretation.yaml"],
            "constraints": [
                (
                    "A8.6 POWER GATE: This hypothesis was blocked before prescreen. "
                    "Use verdict_label: insufficient_power_a_priori. "
                    "disposition: parked. do_not_add_to_failed_families: true. "
                    "reactivation_trigger: the data_requirement from prescreen_result.yaml.a86_power_check. "
                    "trial_count: 0 (no IC computed, no trial spent). "
                    "sharpe: null, n_trades: 0, statistic_valid: neither."
                ),
            ],
        })


def determine_post_validation_route(path: Path):
    """Once validation is complete, read the decision from validation_decision artifact and route accordingly:
    - If "approve": proceed to Phase 2 development of backtest
    - If "refine": route to refinement planner (unless max refinements reached, then reject)
    - If "reject": mark as completed and rejected
    """
    decision_path = path / "artifacts" / "validation_decision.yaml"
    decision = load_yaml(decision_path)
    # F4f (2026-07-06, run_053): the quant-validation skill's real output for a
    # multi-variant family validation (5 MACD variants) used `family_status`
    # instead of the schema-canonical top-level `status` (schemas/validation_decision.
    # schema.json requires status/rationale/blocking_issues; family_status is not
    # even a schema-valid key). Fall back rather than crash with an opaque
    # AttributeError on None — but still fail loudly (not silently proceed) if
    # neither key is present, since that means the file is genuinely malformed.
    status = decision.get("status") or decision.get("family_status")
    if status is None:
        raise ValueError(
            f"{decision_path} has neither 'status' nor 'family_status' — cannot "
            f"determine route. Keys present: {list(decision.keys())}"
        )
    status = status.strip().lower()

    state = load_yaml(path / "pipeline_state.yaml")
    refinements_used = state.get("counters", {}).get("refinements_used", 0)
    max_refinements = state.get("governance", {}).get("max_refinements_after_validation", 2)

    if status in ("approve", "conditional_approve"):
        if status == "conditional_approve":
            # Family-schema output has no top-level `conditions` — aggregate
            # per-variant conditions instead (see the status fallback above).
            conditions = decision.get("conditions")
            if conditions is None:
                conditions = [
                    c for v in decision.get("variant_decisions", []) for c in v.get("conditions", [])
                ]
            print(f"\n⚠️  CONDITIONAL APPROVAL — conditions to respect in backtest config:")
            for c in conditions:
                print(f"   - {c}")
        update_state(path=path, flags={"validation_approved": True})

        # A8.6 Fix 2: deterministic power stop before component build
        _a86 = _run_a86_power_check(path / "artifacts")
        if _a86["verdict"] == "insufficient_power_a_priori":
            run_id = path.name
            print(f"\n⚡ A8.6: Power gate blocked at validation — no component will be built.")
            print(f"   min_detectable_ic={_a86['min_detectable_ic']:.4f} > "
                  f"plausible_ic_upper={_a86['plausible_ic_upper']}")
            print(f"   expected_n_eff={_a86['expected_n_eff']:.1f} "
                  f"(active_n={_a86['expected_active_n']:.0f}, "
                  f"n_eff_symbols={_a86.get('n_eff_symbols', 'n/a')}, rho={_a86.get('rho_bar')})")
            print(f"   Data requirement: {_a86.get('data_requirement')}")
            save_yaml(path / "artifacts" / "prescreen_result.yaml", {
                "run_id": run_id,
                "route": "insufficient_power_a_priori",
                "a86_power_check": _a86,
                "stage_blocked_at": "validation",
                "note": "A8.6 power gate: no component built, no trial spent.",
            })
            _create_a86_validation_bypass_handoffs(run_id, path)
            return "signal_prescreen"

        return "backtest_specification"
    
    elif status == "refine":
        if refinements_used >= max_refinements:
            print(f"🛑 Refinement limit reached ({max_refinements}). Rejecting hypothesis.")
            return "completed_rejected"
        return "refinement_planner"
    
    elif status == "reject":
        return "completed_rejected"
    
    else:
        raise ValueError(f"Unknown validation status: {status}")

def _create_remaining_handoffs(run_id: str, run_dir: Path):
    """Write signal_prescreen, protocol_execution, and verdict_interpreter handoffs."""
    handoffs = run_dir / "handoffs"
    sp_path = handoffs / "backtest_spec_to_signal_prescreen.yaml"
    pe_path = handoffs / "backtest_spec_to_protocol_execution.yaml"
    vi_path = handoffs / "protocol_to_verdict_interpreter.yaml"

    # Improvement 08+09: signal_prescreen handoff
    if not sp_path.exists():
        save_yaml(sp_path, {
            "handoff_version": 1, "run_id": run_id,
            "from_stage": "backtest_specification", "to_stage": "signal_prescreen",
            "assigned_engine": "tool",
            "objective": (
                "Run signal prescreen — cheap IC + cost gate before full walk-forward. "
                "Compute pooled IC, block-adjusted significance, turnover proxy, and "
                "cost_check from config/cost_model.yaml. Route: proceed_to_backtest "
                "(both IC and cost pass) or kill/refine (skip backtest)."
            ),
            "required_inputs": [
                {"path": "artifacts/candidate_strategy_config.json",
                 "reason": "strategy config to prescreen"},
                {"path": "../../config/cost_model.yaml",
                 "reason": "Layer 2 cost hurdle parameters"},
                {"path": "../../config/campaign_data_policy.yaml",
                 "reason": "holdout range guard — prescreen must not read holdout data"},
            ],
            "deliverables": ["prescreen_result.yaml"],
            "constraints": [
                "A8.1: no standalone IC pass — cost_check is always required.",
                "A2.3: ic_by_regime is suspended; report ungated IC only.",
                "A6.2: prescreen kills must be recorded as trials in campaign_state.",
                "Holdout data must not be used in prescreen windows.",
            ],
        })

    if not pe_path.exists():
        save_yaml(pe_path, {
            "handoff_version": 1, "run_id": run_id,
            "from_stage": "backtest_specification", "to_stage": "protocol_execution",
            "assigned_engine": "tool",
            "objective": "Run the full walk-forward protocol against the emitted config, "
                         "evaluated against this hypothesis's specific validation criteria.",
            "required_inputs": [
                {"path": "artifacts/candidate_strategy_config.json",
                 "reason": "the config to backtest"},
                {"path": "artifacts/validation_protocol.yaml",
                 "reason": "hypothesis-specific success criteria for verdict evaluation"},
            ],
            "deliverables": ["protocol_result.yaml"],
        })

    if not vi_path.exists():
        save_yaml(vi_path, {
            "handoff_version": 1, "run_id": run_id,
            "from_stage": "protocol_execution", "to_stage": "verdict_interpreter",
            "assigned_engine": "claude",
            "objective": "Interpret backtest findings against hypothesis-specific criteria. "
                         "Choose the correct altitude (refine/pivot/escalate/kill/promote) "
                         "based on diagnostics and campaign history. Produce the matching artifact.",
            "required_inputs": [
                {"path": "artifacts/protocol_result.yaml",
                 "reason": "backtest findings, hypothesis verdict, and diagnostics block"},
                {"path": "artifacts/validation_protocol.yaml",
                 "reason": "original success criteria and failure modes to interpret against"},
                {"path": "artifacts/backtest_spec.yaml",
                 "reason": "maps config choices to hypothesis claims for failure attribution"},
                {"path": "artifacts/research_brief.yaml",
                 "reason": "original research question and constraints"},
            ],
            "optional_inputs": [
                {"path": "../../campaign_state.yaml",
                 "reason": "cross-run altitude history; drives circuit-breaker altitude decisions"},
            ],
            "deliverables": ["verdict_interpretation.yaml"],
            "constraints": [
                "Change at most one hypothesis dimension in proposed_brief.yaml (refine case).",
                "Do not recommend components absent from STRATEGY_CONFIG_REFERENCE.md.",
                "Accept protocol_result.yaml numbers as truth — do not re-evaluate.",
                "Populate altitude_justification with the specific diagnostic value used.",
                "Do not emit both proposed_brief.yaml AND escalation_request.yaml.",
            ],
            "stop_conditions": [
                "All evaluable approve criteria pass → status: promote, emit research_decision.yaml.",
                "Two or more reject criteria confirmed → status: kill, emit research_decision.yaml.",
            ],
        })


def _ensure_regime_detector_report(run_id: str, run_dir: Path) -> dict | None:
    """
    Improvement 02: ensure regime_detector_report.yaml exists and is < 30 days old.
    If stale or absent, runs validate_regime_detector.py deterministically.
    Returns the loaded report dict, or None if it could not be produced.
    """
    import datetime as _dt
    report_path = ROOT / "regime_detector_report.yaml"
    stale = True
    if report_path.exists():
        try:
            rpt = load_yaml(report_path)
            evaluated_at = rpt.get("evaluated_at", "")
            if evaluated_at:
                age = datetime.now(timezone.utc) - datetime.fromisoformat(evaluated_at)
                if age.days < 30:
                    stale = False
        except Exception:
            pass

    if stale:
        config_path = run_dir / "artifacts" / "candidate_strategy_config.json"
        if not config_path.exists():
            print("⚠️  regime_detector_report: candidate_strategy_config.json not found — skipping.")
            return None

        TBOT_PYTHON = _resolve_tbot_python()
        cmd = [
            str(TBOT_PYTHON),
            str(ROOT / "tools" / "validate_regime_detector.py"),
            "--config", str(config_path),
        ]
        print("🔍 Running regime detector validation (Improvement 02)...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️  validate_regime_detector.py failed:\n{result.stderr}")
            return None

    if report_path.exists():
        return load_yaml(report_path)
    return None


_RETUNE_FORBIDDEN_TERMS = {
    "pnl", "sharpe", "ic", "backtest", "cost_drag",
    "forecast_return_corr", "per_trade", "expectancy",
}

def _validate_retune_firewall(regime_audit: dict) -> list:
    """
    A2.2 retune firewall: regime_audit_decision.yaml must not cite strategy metrics
    in recommended_action. Returns a list of violation strings (empty = clean).
    """
    violations = []
    recommended = (regime_audit.get("recommended_action") or "").lower()
    for term in _RETUNE_FORBIDDEN_TERMS:
        if term in recommended:
            violations.append(
                f"Retune firewall: '{term}' in recommended_action — "
                "detector retunes must use detector-intrinsic criteria only."
            )
    return violations


def _inject_regime_context_into_handoff(handoff_path: Path, regime_report: dict,
                                         regime_audit: dict | None, run_id: str):
    """
    Improvement 02: update the verdict_interpreter handoff to include regime detector
    confidence and the A2.1 ungated-escape flag. Adds optional_inputs and a constraint.
    """
    if not handoff_path.exists() or regime_report is None:
        return

    handoff = load_yaml(handoff_path) or {}

    # Add regime_detector_report as optional input
    opt = handoff.setdefault("optional_inputs", [])
    paths_present = {x.get("path") for x in opt}
    if "../../regime_detector_report.yaml" not in paths_present:
        opt.append({
            "path": "../../regime_detector_report.yaml",
            "reason": "Improvement 02: detector confidence per symbol/timeframe; "
                      "required before any regime-attribution conclusion",
        })

    # Summarise confidence per entry for the skill
    conf_summary = {
        f'{e["symbol"]}_{e["timeframe"]}': e["confidence"]
        for e in regime_report.get("per_symbol_per_timeframe", [])
    }
    handoff["regime_detector_confidence"] = conf_summary

    # A2.1 ungated escape
    if regime_audit:
        handoff["ungated_escape_eligible"] = regime_audit.get("ungated_escape_eligible", False)
        handoff["ungated_escape_rationale"] = regime_audit.get("ungated_escape_rationale", "")

    # Add the mechanical constraint
    constraints = handoff.setdefault("constraints", [])
    detector_block = (
        "IMPROVEMENT 02 — REGIME ATTRIBUTION GATE: "
        "Do NOT conclude regime_attribution.conclusion = signal_bad_everywhere "
        "while detector_confidence != high for the tested symbol/timeframe, "
        "UNLESS ungated_escape_eligible is true (see handoff field). "
        "If detector_confidence is low/medium and ungated escape is not available, "
        "set conclusion = inconclusive_low_detector_confidence and route to regime_auditor."
    )
    if detector_block not in constraints:
        constraints.append(detector_block)

    save_yaml(handoff_path, handoff)
    print(f"✅ Regime context injected into verdict_interpreter handoff: {conf_summary}")


_BLANK_BRIEF_PLACEHOLDER = "# TODO: Paste your research brief configuration here."


def _safe_write_new_research_brief(next_run_id: str, nrq: dict):
    """
    F8 (2026-07-04): only ever write research_brief.yaml for a run that doesn't have
    one yet, or still has the untouched setup_run.py placeholder. Refuses to silently
    overwrite a real brief — this is the second half of what a run-ID collision
    looked like in practice (a campaign_review reframe overwriting an unrelated,
    already-in-progress run's actual research question). Call this AFTER
    _scaffold_next_run(next_run_id) has already succeeded (which itself now refuses
    to scaffold over a non-fresh run) — this is a second, independent check on the
    specific file being written, not a replacement for that one.
    """
    brief_path = ROOT / "runs" / next_run_id / "artifacts" / "research_brief.yaml"
    if brief_path.exists():
        existing_text = brief_path.read_text(encoding="utf-8").strip()
        if existing_text != _BLANK_BRIEF_PLACEHOLDER:
            raise RuntimeError(
                f"REFUSING TO OVERWRITE: {brief_path} already has real content. This is "
                f"very likely a run-ID collision (F8) — '{next_run_id}' was computed as "
                f"a supposedly-free ID but already holds a different research brief. "
                f"Fix the caller's ID allocation; do not delete this file to work around it."
            )
    save_yaml(brief_path, nrq)


def _scaffold_next_run(next_run_id: str):
    """Scaffold next run directory only — no brief copy.

    F8 (2026-07-04): checks the subprocess result — setup_run.py now raises (nonzero
    exit) if next_run_id already has real progress (see setup_run.py
    _is_fresh_or_absent). Previously this return code was never checked, so a
    collision silently "succeeded" from the caller's point of view while quietly
    clobbering the colliding run's pipeline_state.yaml.
    """
    result = subprocess.run([sys.executable, str(ROOT / "workflow" / "setup_run.py"), next_run_id])
    if result.returncode != 0:
        raise RuntimeError(
            f"setup_run.py failed for '{next_run_id}' (see output above) — most likely "
            f"a run-ID collision (F8): the computed ID was already in use by a run with "
            f"real progress."
        )


def setup_next_run(current_run_path: Path, next_run_id: str):
    """Scaffold next run and copy proposed_brief as its research_brief. Refine path only."""
    _scaffold_next_run(next_run_id)
    proposed  = current_run_path / "artifacts" / "proposed_brief.yaml"
    next_brief = ROOT / "runs" / next_run_id / "artifacts" / "research_brief.yaml"
    shutil.copy(proposed, next_brief)
    print(f"✅ {next_run_id} scaffolded with proposed brief from {current_run_path.name}")


# ---------------------------------------------------------------------------
# F4d (2026-07-05, run_047 conformance gap): machine-readable pre-registration
# constraints. run_047 pre-registered "use the extended 2019-2025 range" and
# "MANDATORY A8.5.1a" purely in prose (research_brief.yaml / pre_registration.yaml
# free text). Nothing mechanically enforced either — signal_prescreen silently
# defaulted to protocols/baseline_v1.json (the existing 2024-only protocol), and
# backtest_specification's LLM stage silently dropped the significance_methodology
# field despite an explicit skill-file instruction to carry it through. The result
# looked like a completed, verdict-bearing run but never tested what was
# pre-registered. machine_constraints closes this: anything the brief mandates
# that a machine CAN check goes in pre_registration.yaml's machine_constraints
# block, the orchestrator derives the protocol/config directly from it (removing
# the hand-built-override step as a manual task), and a conformance check gates
# entry to verdict_interpreter — a mismatch is an engineering failure, never a
# scientific result, exactly like F5c's no_signal_artifact.
# ---------------------------------------------------------------------------

def _load_machine_constraints(run_dir: Path) -> dict | None:
    pr_path = run_dir / "artifacts" / "pre_registration.yaml"
    if not pr_path.exists():
        return None
    pr = load_yaml(pr_path) or {}
    return pr.get("machine_constraints")


class HoldoutBoundaryBreach(ValueError):
    """
    A generated month tile would materialise bars inside the sealed holdout
    range (campaign_data_policy.yaml:holdout_range).

    Raised, never clamped-and-continued. A silently truncated sweep is a sweep
    whose reported coverage no longer matches what was pre-registered, and the
    caller has no way to notice. Fail loudly and let a human decide whether the
    request or the seal was wrong.
    """


def _load_holdout_range(policy_path=None) -> tuple:
    """
    (start, end) of holdout_range, read from campaign_data_policy.yaml.

    Deny by default: a missing, unreadable or malformed policy raises rather
    than returning "no holdout to worry about". The date is never hardcoded
    here — the seal has exactly one home, and a second copy in the generator is
    a second thing to forget to move.

    `_DATA_POLICY_PATH` is the pre-existing module global (defined further
    down, alongside the holdout_consumed_by writer); tests/conftest.py
    redirects it into a per-test sandbox, so it is deliberately read at call
    time rather than captured here.
    """
    p = Path(policy_path) if policy_path else _DATA_POLICY_PATH
    try:
        policy = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except OSError as exc:
        raise HoldoutBoundaryBreach(
            f"cannot read the campaign data policy at {p}: {exc}. Refusing to "
            "generate windows without knowing where the holdout starts."
        ) from exc
    hr = policy.get("holdout_range")
    if not isinstance(hr, (list, tuple)) or len(hr) != 2 or not all(hr):
        raise HoldoutBoundaryBreach(
            f"{p} has no usable holdout_range (got {hr!r}). Refusing to generate "
            "windows against an unknown seal."
        )
    return str(hr[0]), str(hr[1])


def _assert_windows_clear_of_holdout(windows: list, holdout_start: str,
                                     holdout_end: str) -> None:
    """
    Refuse any window whose bars would land at or after `holdout_start`.

    THE OFF-BY-ONE THIS EXISTS TO KILL
    ----------------------------------
    `test.end` looks exclusive — the generator emits the FIRST OF THE NEXT
    MONTH and the next window starts on the same date. It is not exclusive at
    the engine. `run_protocol` hands `end` straight to `launcher.run_backtest`,
    which passes it to `load_data(end_date=end)`, and that yields every bar of
    the end DAY, through 23:00. So a tile written as
    [month M day 1, month M+1 day 1) actually materialises
    [month M day 1 00:00, month M+1 day 1 23:00] -- for a 1h timeframe, 768
    bars, 24 of them in the following month.

    That 24-bar overspill sits on every tile of every monthly sweep and is
    harmless on all but the last one. It stopped being harmless exactly once:
    the final tile of the 2025 sweep spilled into day 1 of the sealed holdout
    and spent those bars
    (campaign_data_policy.yaml:holdout_contaminated_runs). The generator had no
    clamp, so a sweep extended by one more month would breach again by
    construction.

    Comparison is on YYYY-MM-DD strings, which is chronological for this format
    and is the same shape run_protocol's own boundary assert uses.
    """
    for w in windows:
        label = w.get("label", "?")
        for edge in ("start", "end"):
            value = str(w["test"][edge])[:10]
            if value >= holdout_start:
                raise HoldoutBoundaryBreach(
                    f"window {label!r} has test.{edge}={value}, at or past "
                    f"holdout_start={holdout_start} (holdout_range "
                    f"{holdout_start}..{holdout_end}). `end` is INCLUSIVE-BY-DAY at "
                    f"the engine, so end={value} materialises that whole day's bars "
                    f"inside the sealed window. Move the sweep's end date before "
                    f"{holdout_start}; this generator will not truncate it for you."
                )


def _generate_monthly_windows(start: str, end: str, holdout_range=None) -> list:
    """[start, end) chunked into calendar-month windows, matching baseline_v1.json's
    schema: [{"label": "YYYY-MM", "test": {"start": ..., "end": ...}}, ...].

    Raises HoldoutBoundaryBreach if any generated tile would reach the sealed
    holdout — see `_assert_windows_clear_of_holdout` for why `end` is not the
    exclusive bound it looks like. `holdout_range` overrides the policy file
    (tests only)."""
    from datetime import date as _date
    y, m = int(start[:4]), int(start[5:7])
    end_y, end_m = int(end[:4]), int(end[5:7])
    windows = []
    while (y, m) < (end_y, end_m) or (y == end_y and m == end_m and end[8:10] != "01"):
        if (y, m) > (end_y, end_m):
            break
        window_start = f"{y:04d}-{m:02d}-01"
        if m == 12:
            ny, nm = y + 1, 1
        else:
            ny, nm = y, m + 1
        window_end = f"{ny:04d}-{nm:02d}-01"
        if window_end > end:
            window_end = end
        windows.append({"label": f"{y:04d}-{m:02d}", "test": {"start": window_start, "end": window_end}})
        if window_end >= end:
            break
        y, m = ny, nm

    hs, he = holdout_range if holdout_range else _load_holdout_range()
    _assert_windows_clear_of_holdout(windows, hs, he)
    return windows


def _ensure_protocol_from_constraints(run_dir: Path, run_id: str, constraints: dict) -> Path | None:
    """
    Idempotent: generates runs/{run_id}'s dedicated protocol JSON + run_context.yaml
    override from machine_constraints.protocol, if present and not already done.
    Returns the generated protocol path, or None if no protocol constraint exists.
    """
    proto_constraint = constraints.get("protocol")
    if not proto_constraint:
        return None

    protocols_dir = ROOT / "protocols"
    protocols_dir.mkdir(parents=True, exist_ok=True)
    out_path = protocols_dir / f"{run_id}_generated.json"

    run_ctx_path = run_dir / "artifacts" / "run_context.yaml"
    if out_path.exists() and run_ctx_path.exists():
        return out_path  # already generated this run — do not regenerate/clobber

    symbols = proto_constraint["symbols"]
    timeframe = proto_constraint.get("timeframe", "1h")
    per_symbol_start = proto_constraint.get("per_symbol_start") or {}
    start = min(per_symbol_start.values()) if per_symbol_start else proto_constraint["start"]
    end = proto_constraint["end"]

    windows = _generate_monthly_windows(start, end)
    # The seal has ONE home. Defaulting to a literal here was a second copy of
    # holdout_range that nothing kept in sync with the policy file, in the very
    # function whose windows have to be checked against it.
    policy_start, policy_end = _load_holdout_range()
    protocol_obj = {
        "symbols": symbols,
        "timeframe": timeframe,
        "windows": windows,
        "holdout": proto_constraint.get(
            "holdout", {"start": policy_start, "end": policy_end}
        ),
        "promotion": _require_pre_registered_promotion(proto_constraint, run_id),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(protocol_obj, f, indent=2)
    print(f"✅ [F4d] Generated protocol from pre-registered machine_constraints: {out_path}"
          f" ({len(windows)} windows, {start} -> {end})")

    # run_type MUST be "forced_diagnostic" — both signal_prescreen's and
    # protocol_execution's protocol-resolution logic only consult run_context's
    # `protocol` key under that exact run_type; otherwise they silently fall back
    # to campaign_state.last_escalation.protocol_path (STALE campaign-wide state
    # from a previous, unrelated run's escalation — this is exactly what happened
    # to run_050's first attempt: it picked up run_047's leftover
    # escalation_tf_15m.json because this run_type key was missing).
    run_ctx = {"run_type": "forced_diagnostic", "protocol": out_path.name}
    run_ctx_path.parent.mkdir(parents=True, exist_ok=True)
    save_yaml(run_ctx_path, run_ctx)
    print(f"✅ [F4d] Wrote run_context.yaml override: run_type=forced_diagnostic, protocol={out_path.name}")
    return out_path


class UngatedProtocolError(ValueError):
    """G7 (C7-EXT): a protocol was materialized from a brief whose
    machine_constraints carry no pre-registered `promotion` block.

    C7-EXT-R (D-3) widens this to protocol SELECTION as well as generation."""


# C7-EXT-R / D-3. The exact block G7 abolished, kept in ONE place so "is this
# the abolished default?" is a single comparison rather than four scattered
# literals. Any protocol file whose promotion block equals this did not get it
# from a brief -- it got it from the code default, by copy or by generation.
_GENERIC_PROMOTION = {
    "median_sharpe_gt": 0,
    "max_abs_drawdown_pct_lt": 30,
    "min_trade_count_gte": 20,
    "kill_median_sharpe_lt": -1,
}


def promotion_is_generic(promotion) -> bool:
    """True when a promotion block is byte-equal to the abolished code default."""
    return isinstance(promotion, dict) and dict(promotion) == _GENERIC_PROMOTION


def _assert_promotion_ratified(protocol_path: Path) -> None:
    """
    C7-EXT-R / D-3. G7 alone was half a fix, and the audit said so plainly:
    guarding the GENERATOR while leaving the generated artifacts and the default
    selection in place changes nothing for a run that simply loads one.

    The abolished block is still committed and live in several protocol files
    (baseline_v1/v2, the escalation_* set, and the run_0NN_generated ones
    materialized before G7 existed). `_resolve_protocol_path` could hand any of
    them to a run, and the resulting verdict would once again be computed against
    thresholds no brief ever froze.

    (test_d3_generic_classifier_agrees_with_independent_derivation_and_all_are_unratified
    checks that every committed protocol the classifier calls generic is recorded
    unratified, by agreement with an independent re-derivation rather than a file
    count -- so the guard cannot silently drift as the protocol set changes.)

    So the check moves to the point of USE. A protocol carrying the generic block
    is refused unless the file explicitly ratifies it, via:

        "promotion_provenance": {"ratified_by": "<brief or operator ruling>",
                                 "ratified_at": "<date>"}

    Ratification is cheap and reversible -- it is a claim that a human looked at
    these four numbers and adopted them for this protocol on purpose. That is the
    entire difference between a pre-registered threshold and a leftover default,
    and it is exactly the difference the campaign could not previously express.
    """
    try:
        with open(protocol_path, "r", encoding="utf-8") as fh:
            protocol_obj = json.load(fh)
    except (OSError, ValueError):
        return  # existence/parse failures are other checks' business, not this one
    if not isinstance(protocol_obj, dict):
        return

    promotion = protocol_obj.get("promotion")
    if not promotion_is_generic(promotion):
        return

    provenance = protocol_obj.get("promotion_provenance") or {}
    if isinstance(provenance, dict) and provenance.get("ratified_by"):
        return

    raise UngatedProtocolError(
        f"[G7/D-3] {protocol_path.name} carries the abolished generic promotion "
        f"block {_GENERIC_PROMOTION} with no `promotion_provenance.ratified_by`. "
        f"These four numbers came from a code default, not from any brief -- they "
        f"are the same unregistered '30% DD bar' the XS_momentum verdict was "
        f"argued against. Refusing to run a verdict-bearing protocol against them. "
        f"Either pre-register real thresholds for this hypothesis, or add "
        f"promotion_provenance: {{ratified_by, ratified_at}} to {protocol_path.name} "
        f"to state on the record that these values were adopted deliberately."
    )


def _require_pre_registered_promotion(proto_constraint: dict, run_id: str) -> dict:
    """
    G7 (C7-EXT, 2026-07-22). This function replaces a silent default.

    It used to read:

        "promotion": proto_constraint.get("promotion", {
            "median_sharpe_gt": 0, "max_abs_drawdown_pct_lt": 30,
            "min_trade_count_gte": 20, "kill_median_sharpe_lt": -1,
        }),

    -- i.e. a brief that pre-registered NO thresholds silently acquired four
    generic ones, and every downstream artifact then read as though the
    campaign had registered them in advance. That is the exact C7 symptom
    ("protocol_result.yaml issued verdict: refine from generic code
    thresholds (min_trades>=20, drawdown caps)"), left live in the tree after
    C7 was recorded CLOSED. It is also the provenance of the "30% DD bar" that
    XS_momentum's post-hoc verdict was argued against -- a number no brief
    ever froze.

    Failing loudly is the point: a missing pass rule is a registration defect
    to be fixed in the brief, never a gap for code to paper over.
    """
    promotion = proto_constraint.get("promotion")
    if not promotion:
        raise UngatedProtocolError(
            f"[G7] run {run_id}: machine_constraints.protocol has no pre-registered "
            f"`promotion` block. Refusing to substitute generic thresholds -- a "
            f"protocol materialized from defaults is structurally ungated, and any "
            f"verdict computed against it would misrepresent invented thresholds as "
            f"pre-registered ones. Add an explicit `promotion` block (B11 total "
            f"mapping) to the brief's machine_constraints, then re-run."
        )
    return promotion


def _compute_protocol_content_hash(path: Path) -> str:
    """
    K3/§5: structural hash (tolerant of key reordering from hand edits), computed
    over the file's own JSON body MINUS its own protocol_version/protocol_content_hash
    stamp fields (avoids a circular hash-of-a-hash problem).
    """
    obj = json.loads(path.read_text(encoding="utf-8"))
    obj.pop("protocol_version", None)
    obj.pop("protocol_content_hash", None)
    canonical = json.dumps(obj, sort_keys=True)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _lint_machine_constraints_protocol_selection(constraints: dict, pass_rule: dict | None = None) -> list:
    """
    K3/§3+§9(Q1): materialization-time lint for machine_constraints.protocol_ref.
    Returns a list of violation strings (empty = conforms). Called from
    run_campaign.py's _materialize_run/_materialize_refinement_run, alongside
    the existing B11 lint call — same site, not a new mechanism.
    """
    violations = []
    proto = constraints.get("protocol")
    ref = constraints.get("protocol_ref")

    if proto and ref:
        violations.append(
            f"machine_constraints carries BOTH protocol={proto!r} (generate) AND "
            f"protocol_ref={ref!r} (pin) — these are mutually exclusive; a brief "
            f"must choose exactly one protocol-selection mechanism."
        )
        return violations  # incoherent pair — no point checking ref shape further

    if ref is not None:
        if not isinstance(ref, str) or not ref.strip():
            violations.append(
                f"machine_constraints.protocol_ref={ref!r} must be a non-empty string."
            )
        else:
            ref_path = Path(ref)
            if ref_path.parent != Path("protocols"):
                violations.append(
                    f"machine_constraints.protocol_ref={ref!r} must resolve FLAT under "
                    f"'protocols/' (e.g. 'protocols/name.json') — nested subdirectories "
                    f"or paths outside protocols/ are rejected (K3/§9 A1.2)."
                )
            # Q1: pass_rule.window_set_ref naming a DIFFERENT file is a HARD REJECT,
            # not the WARNING originally proposed in §3. A legacy (string-shaped)
            # pass_rule has no window_set_ref to compare -- not linted here, same
            # scope limitation _lint_pass_rule_total_mapping's own docstring names.
            window_set_ref = pass_rule.get("window_set_ref") if isinstance(pass_rule, dict) else None
            if window_set_ref and window_set_ref != ref:
                violations.append(
                    f"machine_constraints.protocol_ref={ref!r} and "
                    f"pass_rule.window_set_ref={window_set_ref!r} name DIFFERENT files "
                    f"— incoherent pre-registration (K3/§9 Q1 hard reject)."
                )

    return violations


def _ensure_protocol_ref_pinned(run_dir: Path, run_id: str, constraints: dict) -> Path | None:
    """
    K3 (B3): pins an EXISTING, named protocol file via machine_constraints.protocol_ref
    -- never generates/regenerates windows (that remains _ensure_protocol_from_constraints's
    job, gated on the DIFFERENT `protocol` key). Idempotent across repeated run_loop()
    entries into the same run.

    A1 fix (K3/§9): writes the BARE FILENAME into run_context.yaml's "protocol" key
    (not the ROOT-relative protocol_ref value) so the existing
    `ROOT / "protocols" / proto_name` consumer construction keeps working unmodified
    -- the original Phase A draft wrote the full ref and doubled the path.
    A3 fix (K3/§9): uses a NEW, dedicated run_type ("protocol_ref_pinned") rather than
    reusing "forced_diagnostic", so a pinned run is mechanically distinguishable from a
    generated one at the run_context.yaml level.
    """
    ref = constraints.get("protocol_ref")
    if not ref:
        return None

    bare_name = Path(ref).name
    ref_path = ROOT / "protocols" / bare_name
    run_ctx_path = run_dir / "artifacts" / "run_context.yaml"

    if run_ctx_path.exists():
        existing = load_yaml(run_ctx_path) or {}
        if existing.get("run_type") == "protocol_ref_pinned" and existing.get("protocol") == bare_name:
            return ref_path  # already pinned this run — idempotent, no re-write

    if not ref_path.exists():
        raise FileNotFoundError(
            f"machine_constraints.protocol_ref={ref!r} does not exist at {ref_path} -- "
            f"a pinned ref must name an EXISTING protocol file (this is the whole point "
            f"of pinning: never silently generate a substitute)."
        )

    # §5 version-stamping: optional content-hash guard against in-place edits.
    expected_hash = constraints.get("protocol_ref_content_hash")
    if expected_hash:
        actual_hash = _compute_protocol_content_hash(ref_path)
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"[B3] machine_constraints.protocol_ref={ref!r}'s content hash "
                f"{actual_hash!r} != pre-registered {expected_hash!r} -- the pinned "
                f"file's CONTENT changed since this brief was registered (e.g. windows "
                f"silently redefined in place). Refusing to execute against a file that "
                f"no longer matches what was pre-registered."
            )

    run_ctx_path.parent.mkdir(parents=True, exist_ok=True)
    save_yaml(run_ctx_path, {
        "run_type": "protocol_ref_pinned",
        "protocol": bare_name,
        "protocol_ref_pinned": True,
    })
    print(f"📌 [B3] Wrote run_context.yaml pin: run_type=protocol_ref_pinned, protocol={bare_name}")
    return ref_path


def _resolve_protocol_path(run_dir: Path, run_id: str) -> Path:
    """
    K3 (B3+B10, §9 Q4): the ONE shared protocol-selection resolver, replacing the
    two previously-duplicated copies inside run_tool_worker's signal_prescreen/
    protocol_execution branches. Four branch classes: replication_diagnostic;
    protocol-GENERATED forced_diagnostic; protocol_ref-PINNED (its own
    distinguishable run_type, A3); and the claim-checked last_escalation fallback
    (B10, §4) -- which now HARD-FAILS instead of silently reusing stale
    campaign-wide state, unless this run is that escalation's own claimed consumer.

    C7-EXT-R (D-3): every exit passes through _assert_promotion_ratified, so an
    unratified generic promotion block is refused wherever the protocol came
    from -- generated, pinned, defaulted or inherited. The audit's point was that
    guarding only the generator left the artifacts and the defaults untouched.
    """
    artifacts = run_dir / "artifacts"
    run_ctx_path = artifacts / "run_context.yaml"
    run_ctx = (load_yaml(run_ctx_path) or {}) if run_ctx_path.exists() else {}
    run_type = run_ctx.get("run_type", "")

    def _selected(path: Path) -> Path:
        _assert_promotion_ratified(path)
        return path

    if run_type == "replication_diagnostic":
        print("🔁 replication_diagnostic run — ignoring last_escalation, using baseline_v1.json")
        return _selected(ROOT / "protocols" / "baseline_v1.json")

    if run_type == "forced_diagnostic":
        # C7-EXT-R/D-3: the implicit "baseline_v1.json" default is gone. A
        # forced_diagnostic that forgot to name its protocol was silently handed
        # the generic-threshold baseline -- the same silent-default class of
        # defect G7 was opened to abolish, one layer further out.
        proto_name = run_ctx.get("protocol")
        if not proto_name:
            raise UngatedProtocolError(
                f"[G7/D-3] run {run_id}: run_context.yaml declares "
                f"run_type=forced_diagnostic but names no `protocol`. Refusing to "
                f"default to baseline_v1.json -- a diagnostic that does not say what "
                f"it is running against silently inherits generic thresholds. Name "
                f"the protocol explicitly in run_context.yaml."
            )
        print(f"🔬 forced_diagnostic run — using protocol: {proto_name}")
        return _selected(ROOT / "protocols" / proto_name)

    if run_type == "protocol_ref_pinned":
        proto_name = run_ctx.get("protocol")
        if not proto_name:
            raise RuntimeError(
                f"[K3] run_context.yaml declares run_type=protocol_ref_pinned but has no "
                f"'protocol' key -- malformed pin state for {run_id}."
            )
        print(f"📌 [B3] protocol_ref_pinned run — using pinned protocol: {proto_name}")
        return _selected(ROOT / "protocols" / proto_name)

    # B10 fallback: campaign-wide last_escalation, claim-checked (§4).
    campaign = load_campaign_state()
    last_escalation = campaign.get("last_escalation") or {}
    claimed_by = last_escalation.get("claimed_by_run")
    protocol_path_str = last_escalation.get("protocol_path")
    if protocol_path_str and claimed_by == run_id:
        # This run IS the escalation's own designated next run -- the fallback is
        # correct FOR THIS ONE RUN, not stale reuse. Still printed loudly (never
        # silent) and still exactly one hop -- claimed_by is not transitively
        # inherited by any further lineage continuation from this run.
        print(f"⚠️  [B10] Using campaign_state.last_escalation.protocol_path "
              f"({protocol_path_str}) -- this run ({run_id}) is its claimed "
              f"consumer. Fragile: prefer machine_constraints.protocol_ref on "
              f"this run's own pre_registration.yaml instead.")
        return _selected(Path(protocol_path_str))

    update_state(path=run_dir, flags={"stale_escalation_unclaimed": True})
    raise RuntimeError(
        f"[B10] No run_context.yaml override and no machine_constraints.protocol_ref "
        f"for {run_id}, and campaign_state.last_escalation "
        f"(protocol_path={protocol_path_str!r}) is either empty or claimed by a "
        f"different run ({claimed_by!r}) -- refusing to silently run against stale, "
        f"unrelated campaign-wide state. Pin this run's protocol explicitly via "
        f"machine_constraints.protocol_ref in pre_registration.yaml."
    )


def _check_prescreen_conformance(prescreen_result: dict, constraints: dict, protocol_obj: dict) -> list:
    """
    Compares a completed prescreen's ACTUALS against what was pre-registered in
    machine_constraints. Returns a list of violation strings (empty = conforms).
    """
    violations = []

    expected_sig = constraints.get("significance_methodology")
    if expected_sig == "episode_blocked_a851a":
        # F4d fix (caught before shipping, via test-writing): significance_methodology_used
        # names the SPECIFIC outcome (episode_block_bootstrap / episode_bootstrap_insufficient_n
        # / block_24_dense_fallback — episode_significance.VALID_METHODS), not the family
        # name. A literal-equality check would have wrongly flagged the legitimate
        # density-fallback and insufficient-episode outcomes (both correct per A8.5.1a's
        # own spec rules 3/4) as violations. The real thing to detect is "the
        # significance_methodology config flag was absent/ignored and the OLD default
        # (block_24_fisher_z, prescreen_signal.py's own default label) ran instead."
        _tools_path = str(Path(__file__).parent.parent / "tools")
        if _tools_path not in sys.path:
            sys.path.insert(0, _tools_path)
        import episode_significance as _es
        actual_sig = prescreen_result.get("significance_methodology_used")
        if actual_sig not in _es.VALID_METHODS:
            violations.append(
                f"significance_methodology_used={actual_sig!r} is not an A8.5.1a outcome "
                f"({sorted(_es.VALID_METHODS)}) — pre-registered "
                f"machine_constraints.significance_methodology=episode_blocked_a851a was not honored"
            )
    elif expected_sig:
        actual_sig = prescreen_result.get("significance_methodology_used")
        if actual_sig != expected_sig:
            violations.append(
                f"significance_methodology_used={actual_sig!r} != pre-registered "
                f"machine_constraints.significance_methodology={expected_sig!r}"
            )

    proto_constraint = constraints.get("protocol")
    if proto_constraint:
        expected_symbols = set(proto_constraint.get("symbols", []))
        actual_symbols = set(protocol_obj.get("symbols", []))
        if expected_symbols and expected_symbols != actual_symbols:
            violations.append(
                f"protocol symbols {sorted(actual_symbols)} != pre-registered {sorted(expected_symbols)}"
            )

        actual_windows = protocol_obj.get("windows", [])
        actual_start = min((w["test"]["start"] for w in actual_windows), default=None)
        actual_end = max((w["test"]["end"] for w in actual_windows), default=None)

        per_symbol_start = proto_constraint.get("per_symbol_start")
        expected_start = min(per_symbol_start.values()) if per_symbol_start else proto_constraint.get("start")
        expected_end = proto_constraint.get("end")

        if expected_start and actual_start and actual_start > expected_start:
            violations.append(
                f"protocol windows start at {actual_start}, pre-registered range requires "
                f"starting by {expected_start} (the backward-extension range was not used)"
            )
        if expected_end and actual_end and actual_end < expected_end:
            violations.append(
                f"protocol windows end at {actual_end}, pre-registered range requires "
                f"coverage through {expected_end} (the backward-extension range was not used)"
            )

    # K3 rider (2026-07-15, operator ruling on Phase B deviation 1): protocol_ref
    # post-hoc conformance -- A4's runtime guard and Q1's materialization lint are
    # both REGISTRATION-time checks; neither catches an executed prescreen that
    # silently ran against a DIFFERENT file than the one pinned (e.g. a stale
    # run_context.yaml override, or a hand-edited pre_registration.yaml that
    # changed protocol_ref after signal_prescreen already ran once). tools/
    # prescreen_signal.py's own prescreen_result.yaml records the executed
    # protocol's identity under the (confusingly named, pre-existing, unrelated
    # to K3) "protocol_version" field -- protocol.get("_version", protocol_path):
    # no real protocol JSON in this repo carries a literal "_version" key. Two
    # files (baseline_v2.json, ts_trend_daily_v1.json) DO carry a "protocol_version"
    # key, but this is a PRE-EXISTING, hand-set label that predates K3 entirely
    # (git history: commits 410512a/d9fc4e7, both before K3) -- a coincidental
    # collision with K3's own §5 stamp FIELD NAME, not K3's own data: stamp_protocol.py
    # always writes protocol_version PAIRED with protocol_content_hash, and neither
    # of these two files carries that hash (audit finding, 2026-07-15, corrected
    # from this comment's own earlier, wrong provenance claim). Either way -- hand
    # label or K3 stamp -- neither is the underscored "_version" key
    # prescreen_signal.py's own `.get("_version", ...)` looks for, so this field
    # is, in practice, always the raw CLI protocol_path argument (an absolute or
    # ROOT-relative path string) -- confirmed by reading tools/prescreen_signal.py
    # and every protocols/*.json file, not assumed. Compared here by BARE FILENAME
    # (matching A1's own bare-filename convention for run_context.yaml's "protocol"
    # key), never by full path, since the two are constructed differently (CLI arg
    # vs. ROOT-relative ref).
    protocol_ref = constraints.get("protocol_ref")
    if protocol_ref:
        executed_identity = prescreen_result.get("protocol_version")
        pinned_name = Path(protocol_ref).name
        if executed_identity:
            executed_name = Path(executed_identity).name
            if executed_name != pinned_name:
                violations.append(
                    f"prescreen executed protocol {executed_name!r} != pre-registered "
                    f"machine_constraints.protocol_ref bare filename {pinned_name!r} "
                    f"(prescreen_result.protocol_version={executed_identity!r})"
                )

        # Optional, stronger guarantee (§5): if the brief also pinned a content
        # hash, recompute it over the ACTUAL executed protocol_obj (already
        # loaded by determine_post_prescreen_route's own call site) and compare.
        # Duplicates _compute_protocol_content_hash's small formula rather than
        # calling it directly -- that function takes a Path and re-reads the
        # file from disk; protocol_obj here is already the parsed executed
        # content, and this function's authorized write set is
        # _check_prescreen_conformance only (K3 rider scope).
        expected_hash = constraints.get("protocol_ref_content_hash")
        if expected_hash and protocol_obj:
            _stripped = {k: v for k, v in protocol_obj.items()
                         if k not in ("protocol_version", "protocol_content_hash")}
            _canonical = json.dumps(_stripped, sort_keys=True)
            actual_hash = "sha256:" + hashlib.sha256(_canonical.encode("utf-8")).hexdigest()
            if actual_hash != expected_hash:
                violations.append(
                    f"prescreen executed protocol's content hash {actual_hash!r} != "
                    f"pre-registered machine_constraints.protocol_ref_content_hash "
                    f"{expected_hash!r} -- the executed file's CONTENT differs from "
                    f"what was pre-registered"
                )

    return violations


_VALID_HYPOTHESIS_VERDICTS = ("kill", "refine", "promote")
_VALID_LINEAGE_ROUTINGS = ("terminate", "refine", "pivot", "escalate")
_VALID_CRITERION_COMPARATORS = (">=", ">", "<=", "<", "==")


def _lint_pass_rule_total_mapping(pre_registration: dict) -> tuple:
    """
    B11 (K2 kernel, 2026-07-13): materialization-time lint over
    pre_registration.yaml's structured pass_rule.outcomes -- every branch
    must carry an explicit {hypothesis_verdict, lineage_routing} pair, or an
    explicit 'discretion: stage' opt-in ("routing at stage discretion" as an
    opt-in phrase, per B11's own fix text -- never the absence of a pair,
    which is what today's "verdict routing decides kill vs pivot" free-text
    amounts to, exactly run_057's own incident).

    Returns (violations, warnings) -- a non-empty `violations` list means the
    brief is REJECTED at materialization (never reaches
    runs/<id>/artifacts/pre_registration.yaml, mirroring
    _parse_brief_frontmatter's/_parse_refinement_brief_yaml's own
    required-field ValueError style, applied here as a caller-facing
    contract instead of a raised exception so callers can log every
    violation at once). `warnings` never blocks materialization.

    A legacy (string-shaped, or altogether absent) pass_rule is NOT linted
    here -- R3's legacy_not_evaluable path (tools/verdict_criteria_evaluator.py)
    handles it at evaluation time instead; this lint only applies to briefs
    that opt INTO the structured schema.
    """
    violations = []
    warnings = []

    pass_rule = pre_registration.get("pass_rule")
    if pass_rule is None or isinstance(pass_rule, str):
        return violations, warnings  # legacy shape -- nothing to lint

    if not isinstance(pass_rule, dict):
        violations.append(f"pass_rule is neither a string nor a dict (got {type(pass_rule).__name__})")
        return violations, warnings

    criteria = pass_rule.get("criteria") or []
    outcomes = pass_rule.get("outcomes") or []

    if not outcomes:
        violations.append("pass_rule is dict-shaped but has no outcomes -- a structured "
                           "pass rule must enumerate every branch's verdict+routing mapping")

    seen_branches = set()
    for outcome in outcomes:
        branch = outcome.get("branch")
        if not branch:
            violations.append(f"outcomes entry {outcome!r} is missing its 'branch' name")
            continue
        seen_branches.add(branch)
        discretion = outcome.get("discretion")
        if discretion == "stage":
            continue  # explicit opt-in -- no pair required
        if discretion is not None:
            violations.append(f"branch {branch!r}: discretion={discretion!r} is not a "
                               f"recognized opt-in value (only 'stage' is)")
            continue
        hv = outcome.get("hypothesis_verdict")
        lr = outcome.get("lineage_routing")
        if hv not in _VALID_HYPOTHESIS_VERDICTS:
            violations.append(f"branch {branch!r}: hypothesis_verdict={hv!r} is missing or "
                               f"not one of {_VALID_HYPOTHESIS_VERDICTS} (no discretion opt-in present)")
        if hv == "promote":
            if lr is not None:
                violations.append(f"branch {branch!r}: hypothesis_verdict=promote must have "
                                   f"lineage_routing=null (promote never routes); got {lr!r}")
        else:
            if lr not in _VALID_LINEAGE_ROUTINGS:
                violations.append(f"branch {branch!r}: lineage_routing={lr!r} is missing or "
                                   f"not one of {_VALID_LINEAGE_ROUTINGS} (no discretion opt-in present)")

    # C7/C8: every criterion states its metric, comparator, and metric_basis
    # (bar_level/episode_level -- never fragment_level, per the standing
    # metric-basis rule); a per-symbol (sparse-eligible) criterion also needs
    # a null_handling policy or the only possible runtime outcome is SPEC_ERROR.
    for criterion in criteria:
        cid = criterion.get("id", "<unnamed>")
        if not criterion.get("metric"):
            violations.append(f"criterion {cid!r}: missing 'metric'")
        if criterion.get("comparator") not in _VALID_CRITERION_COMPARATORS:
            violations.append(f"criterion {cid!r}: missing or invalid 'comparator'")
        if not criterion.get("metric_basis"):
            violations.append(f"criterion {cid!r}: missing 'metric_basis' (bar_level / "
                               f"episode_level -- fragment_level is itself inadmissible for "
                               f"a verdict, per the standing metric-basis rule)")
        if criterion.get("per_symbol_threshold") and not criterion.get("null_handling"):
            violations.append(f"criterion {cid!r}: has per_symbol_threshold (a per-symbol, "
                               f"sparse-eligible statistic) but no null_handling policy -- "
                               f"A3.4 requires stating what a null aggregate means here")

    # A1 (K2 Phase B operator amendment): WARN (never reject) when multiple
    # FAIL-<id> branches carry DIFFERING verdict pairs -- id-order resolution
    # at evaluation time silently picks the first failing criterion's branch
    # unless the brief's author is told about the ordering now, at registration.
    fail_branches = [o for o in outcomes if str(o.get("branch", "")).startswith("FAIL-")]
    if len(fail_branches) > 1:
        pairs = {(o.get("hypothesis_verdict"), o.get("lineage_routing")) for o in fail_branches}
        if len(pairs) > 1:
            warnings.append(
                f"multiple FAIL branches ({[o.get('branch') for o in fail_branches]}) carry "
                f"DIFFERING hypothesis_verdict/lineage_routing pairs -- criteria id-order at "
                f"evaluation time will silently pick the FIRST failing criterion's branch; "
                f"confirm this ordering is intentional"
            )

    # Best-effort, never blocks: does pass_rule.statement's own prose mention
    # every branch label registered in outcomes? (Prose branch-labeling is
    # inherently fuzzier than the structured outcomes list, hence WARNING only.)
    statement = str(pass_rule.get("statement") or "")
    if statement:
        for branch in seen_branches:
            label = branch[len("FAIL-"):] if branch.startswith("FAIL-") else branch
            if branch.lower() not in statement.lower() and label.lower() not in statement.lower():
                warnings.append(f"branch {branch!r} is registered in outcomes but its label "
                                 f"was not found in pass_rule.statement's own prose -- "
                                 f"cross-check the human-readable rule still matches")

    return violations, warnings


def _check_kb_reactivation_conformance(next_research_question: dict, kb: dict) -> list:
    """
    A5.4 (2026-07-06, F09/run_053 postmortem): before honoring ANY reframe/reactivation
    recommendation from campaign_review, verify it does not target a KB finding whose
    reactivation_condition has already been consumed (reactivation_consumed_by set) or
    that is flatly exhausted with no open reactivation_condition. Mirrors
    _check_prescreen_conformance (F4d) in spirit — a violation here means the campaign
    is about to spend a real trial re-testing an already-answered question, exactly
    what happened live: run_053's campaign_review recommended reframing into
    reactivating both H-041-A and H-041-C, both of which run_050/run_048 (P1b) had
    already closed — but neither KB entry had been written back with the closing
    verdict (see _write_kb_findings_entry's F09 hook, which now prevents this from
    recurring going forward; this gate is the second, independent line of defense that
    also catches a STALE KB entry a human hasn't gotten around to correcting yet).

    Detection is text-based (hypothesis_id mentioned in the proposed research
    question's prose) — next_research_question is free-form LLM prose, not a
    structured pointer to a KB entry, the same class of match already used for
    wishlist-trigger detection in workflow/run_campaign.py._check_wishlist_trigger.
    Returns a list of violation strings (empty = conforms).
    """
    if not next_research_question:
        return []
    text_parts = []
    for key in ("research_goal", "existing_context", "constraints"):
        val = next_research_question.get(key)
        if not val:
            continue
        text_parts.append(val if isinstance(val, str) else " ".join(str(v) for v in val))
    text = " ".join(text_parts).lower()
    if not text:
        return []

    violations = []
    for f in (kb.get("findings") or []):
        # R4/C9 (K2 kernel, 2026-07-13) bug fix: this KB's `findings` schema is
        # NOT uniform -- 9 of 15 findings use a singular `hypothesis_id`, but 5
        # (including all three Keltner findings, the exact family this ledger
        # item's own C9 symptom names) use a plural `hypothesis_ids` list
        # instead, and one has neither. Reading only `f.get("hypothesis_id")`
        # (as this function did before this fix) silently returns None for
        # every multi-hypothesis finding, so this gate could NEVER catch a
        # reactivation/re-proposal of any of them, regardless of text content
        # -- verified by direct parse of campaign_knowledge_base.yaml, not
        # assumed (see engineering/improvements/done/design_and_docs/K2_verdict_machinery_design_20260713.md
        # section 7). Normalize both shapes to a list and match on any member.
        hyp_ids = f.get("hypothesis_ids") or ([f["hypothesis_id"]] if f.get("hypothesis_id") else [])
        hyp_id = next((h for h in hyp_ids if h and h.lower() in text), None)
        if not hyp_id:
            continue
        consumed_by = f.get("reactivation_consumed_by")
        if consumed_by:
            violations.append(
                f"next_research_question references {hyp_id} (finding {f.get('id')!r}), "
                f"whose reactivation_condition was already consumed by {consumed_by} "
                f"(outcome={f.get('outcome')}). A genuinely different formulation is a "
                f"new hypothesis registration, not a reactivation of this entry."
            )
        elif f.get("exhausted") and not f.get("reactivation_condition"):
            violations.append(
                f"next_research_question references {hyp_id} (finding {f.get('id')!r}), "
                f"which is exhausted (outcome={f.get('outcome')}) with no open "
                f"reactivation_condition."
            )
    return violations


def _mark_trial_invalidated(run_id: str, reason: str):
    """F8b-pattern: flag a previously-recorded trial as invalidated_artifact — it
    contacted real data but tested the wrong thing (conformance violation), so it
    must be excluded from promotion/deflate-sharpe accounting like run_044's
    bug-artifact precedent, not silently deleted."""
    state = load_campaign_state()
    marked = False
    for t in state.get("trial_sharpes", []):
        if t.get("trial_id") == run_id and not t.get("invalidated_artifact"):
            t["invalidated_artifact"] = True
            t["invalidation_reason"] = reason
            marked = True
    if marked:
        _save_campaign_state(state)
    return marked


def _next_run_id(run_id: str) -> str:
    """
    Allocate the next GLOBALLY-unique run ID.

    F8 (2026-07-04): the previous version just incremented the CURRENT run's own
    number ("run_043" -> "run_044") and assumed that slot was free. It collided
    TWICE in the same session: run_043's reframe computed "run_044" while an
    unrelated, independently-launched run_044 was already mid-pipeline (silently
    overwriting its pipeline_state.yaml and research_brief.yaml); the recovery
    then hit the identical defect a second time when run_044's own reframe computed
    "run_045", which by then held the first collision's recovered content.

    Fix: scan BOTH runs/ on disk and campaign_state.yaml's `runs` list for the true
    maximum in-use number under this prefix, and allocate strictly above it — not
    "current + 1". setup_run.py additionally refuses to overwrite a non-fresh run
    (defense in depth, independent of this function being correct).
    """
    parts = run_id.rsplit("_", 1)
    if not (len(parts) == 2 and parts[1].isdigit()):
        # Non-numeric run_id (unexpected in practice) — fall back to a suffix,
        # still verified against collisions below.
        prefix, width = run_id, None
        base_candidate = f"{run_id}_next"
    else:
        prefix, width = parts[0], len(parts[1])
        base_candidate = None

    runs_dir = ROOT / "runs"
    existing_numbers = set()
    if width is not None:
        pattern = re.compile(rf"^{re.escape(prefix)}_(\d+)$")
        if runs_dir.exists():
            for p in runs_dir.iterdir():
                if p.is_dir():
                    m = pattern.match(p.name)
                    if m:
                        existing_numbers.add(int(m.group(1)))
        campaign = load_campaign_state()
        for rid in campaign.get("runs", []):
            m = pattern.match(rid)
            if m:
                existing_numbers.add(int(m.group(1)))
        existing_numbers.add(int(parts[1]))  # the calling run itself always counts

        next_num = max(existing_numbers) + 1
        candidate = f"{prefix}_{next_num:0{width}d}"
        if (runs_dir / candidate).exists():
            # Should be unreachable given the scan above; never hand back an
            # occupied slot regardless.
            raise RuntimeError(
                f"_next_run_id computed '{candidate}' but it already exists on disk — "
                f"refusing to return an occupied run ID."
            )
        return candidate

    candidate = base_candidate
    suffix_n = 2
    while (runs_dir / candidate).exists():
        candidate = f"{base_candidate}{suffix_n}"
        suffix_n += 1
    return candidate


def _handle_hypothesis_generation_multi_card_split(run_id: str, run_dir: Path) -> bool:
    """
    Architecture rule (2026-07-06, run_054 postmortem): ONE hypothesis per run.
    hypothesis_generation's handoff always expects a single hypothesis_card.yaml —
    ensure_files()'s contract is NOT changed to accept multiple; every downstream
    stage assumes one card. If the LLM instead writes MULTIPLE
    hypothesis_card_*.yaml files (because next_research_question's research_goal
    named more than one mechanism to test — exactly what happened for run_054,
    reframed from run_053 into testing BOTH H-041-A and H-041-C at once), that is
    not a failure to raise on: split it. The first card becomes THIS run's
    hypothesis_card.yaml (so it proceeds completely normally — no change to any
    downstream stage or to ensure_files); every additional card is handed to a
    freshly-scaffolded sibling run, already past hypothesis_generation, and the
    split is recorded in campaign_state.yaml's hypothesis_splits so a multi-run
    wrapper (workflow/run_campaign.py) can tell a split sibling apart from a
    reframe/escalate continuation (same brief lineage) and create a SEPARATE queue
    entry for it instead.

    Called from run_loop only when ensure_files() raised FileNotFoundError for
    hypothesis_generation's expected hypothesis_card.yaml. Returns True if a split
    was performed (caller treats the stage as having succeeded); False if this
    isn't actually a multi-card situation (caller re-raises the original error
    unchanged — a genuinely missing, non-multi-card deliverable is still a real
    failure).
    """
    artifacts = run_dir / "artifacts"
    expected = artifacts / "hypothesis_card.yaml"
    if expected.exists():
        return False  # not actually missing — some other deliverable was the problem

    cards = sorted(artifacts.glob("hypothesis_card_*.yaml"))
    if len(cards) < 2:
        return False  # genuinely missing, not a multi-card split — let the caller raise

    print(f"\n🔀 ARCHITECTURE RULE (one hypothesis per run): hypothesis_generation produced "
          f"{len(cards)} hypothesis cards instead of one ({[c.name for c in cards]}). "
          f"Splitting: this run keeps the first card; a sibling run is scaffolded per "
          f"additional card.")

    first, rest = cards[0], cards[1:]
    shutil.copy(first, expected)
    print(f"   {run_id} keeps {first.name} as hypothesis_card.yaml")

    research_brief_src = artifacts / "research_brief.yaml"
    children = []
    for card in rest:
        child_id = _next_run_id(run_id)
        _scaffold_next_run(child_id)
        child_dir = ROOT / "runs" / child_id
        child_artifacts = child_dir / "artifacts"
        if research_brief_src.exists():
            shutil.copy(research_brief_src, child_artifacts / "research_brief.yaml")
        shutil.copy(card, child_artifacts / "hypothesis_card.yaml")
        # Skip straight to innovation_expansion — this card is already a completed
        # hypothesis_generation deliverable, not a fresh one to regenerate.
        update_state(path=child_dir, pending_stage="innovation_expansion",
                     current_stage="hypothesis_generation",
                     completed_stages=["hypothesis_generation"], status="active")
        children.append(child_id)
        print(f"   {child_id} scaffolded from {card.name}")

    state = load_campaign_state()
    splits = state.setdefault("hypothesis_splits", [])
    splits.append({"parent_run": run_id, "children": children,
                    "reason": "hypothesis_generation produced multiple hypothesis cards"})
    _save_campaign_state(state)

    return True


def _next_instrument_from_universe(campaign: dict) -> dict:
    """
    Given current campaign state, return the next instrument to try from coin_universe.yaml.
    Returns: {symbol, category, timeframe} or None if all tried.
    """
    import yaml
    universe_path = ROOT / "config" / "coin_universe.yaml"
    if not universe_path.exists():
        return None

    universe = yaml.safe_load(universe_path.read_text(encoding="utf-8"))
    tried = set(campaign.get("instruments_tried", []))
    raw_tf = campaign.get("timeframes_tried", ["1h"])[-1]
    # Guard: timeframes_tried may contain prose strings if a corruption occurred.
    # Extract the first clean timeframe identifier; default to "1h" if none found.
    import re as _re
    _tf_match = _re.search(r'\b(1m|5m|15m|30m|1h|2h|4h|6h|12h|1d|3d|1w)\b', raw_tf)
    current_tf = _tf_match.group(1) if _tf_match else "1h"

    # Walk escalation_order by priority
    for step in sorted(universe["escalation_order"]["sequence"],
                       key=lambda x: x["priority"]):
        cat_name = step["category"]
        cat = universe["categories"].get(cat_name, {})
        for coin in cat.get("coins", []):
            symbol = coin["symbol"]
            if symbol not in tried:
                return {
                    "symbol": symbol,
                    "category": cat_name,
                    "timeframe": current_tf,
                    "strategy_affinity": cat.get("strategy_affinity", []),
                    "data_cached": coin.get("data_cached", False),
                }
    return None   # all instruments exhausted


def _next_timeframe_from_universe(campaign: dict):
    """Return the next timeframe to try, or None if all tried."""
    import yaml
    universe = yaml.safe_load((ROOT / "config" / "coin_universe.yaml").read_text(encoding="utf-8"))
    tried = set(campaign.get("timeframes_tried", ["1h"]))
    for step in universe["timeframe_escalation"]["sequence"]:
        if step["timeframe"] not in tried:
            return step["timeframe"]
    return None


def _create_escalation_protocol(symbol: str, timeframe: str) -> Path:
    """
    Create a new protocol file for the escalated instrument.
    Does NOT modify baseline_v1.json -- creates a new file in protocols/.
    Returns the path to the new protocol file.
    """
    import json
    baseline_path = ROOT / "protocols" / "baseline_v1.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    escalation = dict(baseline)
    escalation["symbols"] = [symbol]
    escalation["timeframe"] = timeframe
    escalation["_escalation_note"] = (
        f"Auto-generated for instrument escalation to {symbol}. "
        f"Derived from baseline_v1.json. Do not edit manually."
    )
    proto_name = f"escalation_{symbol.lower()}_{timeframe}.json"
    proto_path = ROOT / "protocols" / proto_name
    proto_path.write_text(json.dumps(escalation, indent=2), encoding="utf-8")
    print(f"✅ Created escalation protocol: {proto_path.name}")
    return proto_path


def _create_timeframe_protocol(timeframe: str) -> Path:
    """Create a new protocol file for a timeframe escalation."""
    import json
    baseline_path = ROOT / "protocols" / "baseline_v1.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    escalation = dict(baseline)
    escalation["timeframe"] = timeframe
    escalation["_escalation_note"] = (
        f"Auto-generated for timeframe escalation to {timeframe}. "
        f"Derived from baseline_v1.json."
    )
    proto_name = f"escalation_tf_{timeframe.replace('/', '_')}.json"
    proto_path = ROOT / "protocols" / proto_name
    proto_path.write_text(json.dumps(escalation, indent=2), encoding="utf-8")
    return proto_path


def _route_refine(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    proposed = path / "artifacts" / "proposed_brief.yaml"
    if not proposed.exists():
        print("\n⏸️ REFINE verdict but no proposed_brief.yaml found. Human review needed.")
        return "human_pause"
    state = load_yaml(path / "pipeline_state.yaml")
    used  = state.get("counters", {}).get("refinements_used", 0)
    max_r = state.get("governance", {}).get("max_refinements_after_validation", 2)
    if used >= max_r:
        print(f"\n🛑 Refinement budget exhausted ({used}/{max_r}). Killing hypothesis.")
        return "completed_rejected"
    # C9 rider (K2 kernel, 2026-07-13): KB exhaustion + reactivation-conformance
    # check BEFORE scaffolding -- proposed_brief.yaml is the LLM-authored
    # proposal this route is about to install as the child's own
    # research_brief.yaml; a forbidden/exhausted family here must pause, not
    # scaffold, exactly the gap this ledger item names (Keltner re-proposal).
    # Reuses _check_kb_reactivation_conformance directly -- proposed_brief.yaml
    # is itself a research_brief.yaml-shaped document (same schema as the
    # input brief, per workflow_artifacts/skills/verdict-interpreter/SKILL.md), so it already
    # carries the research_goal/existing_context/constraints fields that
    # function's text-matching expects; no separate wrapper needed.
    proposed_content = load_yaml(proposed) or {}
    _kb = load_yaml(_KB_PATH) if _KB_PATH.exists() else {}
    _kb_violations = _check_kb_reactivation_conformance(proposed_content, _kb or {})
    if _kb_violations:
        print("\n🛑 [C9] KB-EXHAUSTION CHECK — refine proposal targets an "
              "already-closed/exhausted family:")
        for v in _kb_violations:
            print(f"   - {v}")
        update_state(path=path, status="paused_for_human",
                     flags={"kb_reactivation_violation": True},
                     kb_reactivation_violations=_kb_violations)
        return "human_pause"

    next_id = _next_run_id(run_id)
    print(f"\n🔄 REFINE (altitude 1): setting up {next_id} with proposed brief.")
    setup_next_run(path, next_id)
    # Copy findings_carryover.yaml (enables directional memory / parameter_bracket)
    carryover_src = path / "artifacts" / "findings_carryover.yaml"
    if carryover_src.exists():
        carryover_dst = ROOT / "runs" / next_id / "artifacts" / "findings_carryover.yaml"
        import shutil as _shutil
        _shutil.copy(carryover_src, carryover_dst)
        print(f"  findings_carryover.yaml copied to {next_id}")
    # Record in campaign state
    dim = interp.get("proposed_change_dimension", "")
    fam = interp.get("hypothesis_family", "")
    diag = _extract_diagnostics(path)
    update_campaign_state_after_run(run_id, "parameter", dim, fam, "no_improvement", diag)
    # A1 (K4 kernel): persist continuation intent on THIS run's own state,
    # after the child scaffold is known-good (see design note section 5 for
    # the ordering rationale) -- process_once() reads this back instead of
    # diffing runs/ across separate process invocations.
    update_state(path=path, continuation_child=next_id, continuation_created_by="_route_refine")
    return "completed_refined"


def _route_pivot(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    family = interp.get("hypothesis_family", "")

    # C9 rider (K2 kernel, 2026-07-13): _route_pivot does NOT read or write
    # proposed_brief.yaml (verified this phase -- the next run's brief is
    # produced by a LATER, separate hypothesis_generation stage, using
    # findings_carryover.yaml as input). The forward-looking content that
    # could name a forbidden/exhausted family AT PIVOT TIME is
    # verdict_interpretation.yaml's own prose (primary_failure_mode,
    # config_to_failure_map, root_cause) and findings_carryover.yaml's
    # what_not_to_try/notes -- both already written by the time this function
    # runs. Checking here is strictly earlier/cheaper than waiting for
    # hypothesis_generation to formalize a forbidden family into a wasted
    # scaffold (see design note section 7 for why this differs from a
    # literal "before writing proposed_brief.yaml" reading of the ledger).
    _pivot_text_parts = [
        family,
        str(interp.get("primary_failure_mode") or ""),
        str(interp.get("config_to_failure_map") or ""),
        str((interp.get("root_cause") or {}).get("supporting_evidence") or ""),
    ]
    _carryover_for_gate = path / "artifacts" / "findings_carryover.yaml"
    if _carryover_for_gate.exists():
        _co = load_yaml(_carryover_for_gate) or {}
        _pivot_text_parts.append(str(_co.get("what_not_to_try") or ""))
        _pivot_text_parts.append(str(_co.get("notes") or ""))
    _pivot_text = " ".join(p for p in _pivot_text_parts if p)
    _kb = load_yaml(_KB_PATH) if _KB_PATH.exists() else {}
    _kb_violations = _check_kb_reactivation_conformance({"research_goal": _pivot_text}, _kb or {})
    if _kb_violations:
        print("\n🛑 [C9] KB-EXHAUSTION CHECK — pivot direction targets an "
              "already-closed/exhausted family:")
        for v in _kb_violations:
            print(f"   - {v}")
        update_state(path=path, status="paused_for_human",
                     flags={"kb_reactivation_violation": True},
                     kb_reactivation_violations=_kb_violations)
        return "human_pause"

    next_id = _next_run_id(run_id)
    print(f"\n🔀 PIVOT (altitude 2): hypothesis family '{family}' exhausted. "
          f"Setting up {next_id} for fresh hypothesis generation.")
    # Scaffold directory only — no proposed_brief to copy. The next run's brief
    # is produced by hypothesis_generation using findings_carryover.yaml as input.
    subprocess.run([sys.executable, str(ROOT / "workflow" / "setup_run.py"), next_id])
    # Copy findings_carryover.yaml if the LLM produced it
    carryover_src = path / "artifacts" / "findings_carryover.yaml"
    if carryover_src.exists():
        carryover_dst = ROOT / "runs" / next_id / "artifacts" / "findings_carryover.yaml"
        import shutil as _shutil
        _shutil.copy(carryover_src, carryover_dst)
        print(f"  findings_carryover.yaml copied to {next_id}")
    record_pivot(family)
    diag = _extract_diagnostics(path)
    update_campaign_state_after_run(run_id, "hypothesis", "", family, "pivot", diag)
    # A1 (K4 kernel): see _route_refine's identical comment above.
    update_state(path=path, continuation_child=next_id, continuation_created_by="_route_pivot")
    return "completed_refined"


def _route_escalate(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    esc_path = path / "artifacts" / "escalation_request.yaml"
    # When the circuit breaker forces escalate (overriding an LLM pivot verdict),
    # no escalation_request.yaml is produced. Default to instrument escalation —
    # that is the canonical meaning of "hypothesis family exhausted".
    if not esc_path.exists():
        print("\n📊 ESCALATE (circuit-breaker forced) → defaulting to instrument escalation.")
        target = "instrument"
    else:
        escalation = load_yaml(esc_path)
        target = escalation.get("target", "instrument")

    campaign = load_campaign_state()

    if target == "instrument":
        next_inst = _next_instrument_from_universe(campaign)
        if next_inst is None:
            # All instruments exhausted. Do NOT return "campaign_review" (loop risk if we
            # arrived here FROM campaign_review). Mark the campaign space_empty and terminate.
            print("⚠️ All instruments in coin_universe.yaml tried. Marking campaign space_empty.")
            _mark_campaign_status("space_empty")
            return "completed_rejected"
        print(f"\n📊 ESCALATE → {next_inst['symbol']} ({next_inst['category']}, {next_inst['timeframe']})")
        if not next_inst["data_cached"]:
            print(f"   ⚠️ Data not cached for {next_inst['symbol']} — will fetch on first run.")
        proto_path = _create_escalation_protocol(next_inst["symbol"], next_inst["timeframe"])
        next_run_id = _next_run_id(run_id)
        _scaffold_next_run(next_run_id)
        # Carry the current methodology brief into the next run (not proposed_brief.yaml).
        src_brief = path / "artifacts" / "research_brief.yaml"
        if src_brief.exists():
            shutil.copy(src_brief, ROOT / "runs" / next_run_id / "artifacts" / "research_brief.yaml")
        # Write run_context.yaml so hypothesis_generation knows the escalation target.
        # research_brief.yaml carries the hypothesis methodology; run_context overrides asset.
        next_run_ctx = ROOT / "runs" / next_run_id / "artifacts" / "run_context.yaml"
        save_yaml(next_run_ctx, {
            "escalation_type": "instrument",
            "target_symbol": next_inst["symbol"],
            "target_timeframe": next_inst["timeframe"],
            "escalation_reason": "hypothesis_family_exhausted",
            "source_run": run_id,
            "note": (
                "This run is an instrument escalation. research_brief.yaml carries the "
                "hypothesis methodology from the previous run. Override the asset target to "
                f"{next_inst['symbol']} — do NOT use the asset listed in research_brief.yaml. "
                f"All stages must target {next_inst['symbol']} at {next_inst['timeframe']} timeframe."
            ),
        })
        record_escalation("instrument", next_inst["symbol"], protocol_path=str(proto_path), claimed_by_run=next_run_id)
        diag = _extract_diagnostics(path)
        update_campaign_state_after_run(run_id, "search_space", "instrument", "", "escalate", diag)
        # A1 (K4 kernel): see _route_refine's identical comment above.
        update_state(path=path, continuation_child=next_run_id, continuation_created_by="_route_escalate")
        return "completed_escalated"

    elif target == "timeframe":
        next_tf = _next_timeframe_from_universe(campaign)
        if next_tf is None:
            print("⚠️ All timeframes tried. Marking campaign space_empty.")
            _mark_campaign_status("space_empty")
            return "completed_rejected"
        print(f"\n⏱ ESCALATE → timeframe {next_tf}")
        proto_path = _create_timeframe_protocol(next_tf)
        next_run_id = _next_run_id(run_id)
        _scaffold_next_run(next_run_id)
        # Carry the current methodology brief into the next run (not proposed_brief.yaml).
        src_brief = path / "artifacts" / "research_brief.yaml"
        if src_brief.exists():
            shutil.copy(src_brief, ROOT / "runs" / next_run_id / "artifacts" / "research_brief.yaml")
        record_escalation("timeframe", next_tf, protocol_path=str(proto_path), claimed_by_run=next_run_id)
        diag = _extract_diagnostics(path)
        update_campaign_state_after_run(run_id, "search_space", "timeframe", "", "escalate", diag)
        # A1 (K4 kernel): see _route_refine's identical comment above.
        update_state(path=path, continuation_child=next_run_id, continuation_created_by="_route_escalate")
        return "completed_escalated"

    elif target == "new_component":
        print("\n⏸️ ESCALATE → new component required. Pausing for human authoring.")
        update_state(path=path, status="paused_for_human")
        return "human_pause"

    else:
        raise ValueError(f"_route_escalate: unknown escalation target '{target}'")


def _route_kill(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    """
    A9 (K2 kernel, 2026-07-13): PER-HYPOTHESIS termination only. Prior to
    this split, this function ALSO wrote a campaign-wide campaign_decision.yaml
    and set campaign_state.status = "space_empty" unconditionally -- killing
    ONE gate variant would have declared the whole campaign's search space
    exhausted (the writeback agent caught this live on run_057's own
    lineage-close and applied the terminal state by hand, bypassing this
    router entirely). That campaign-wide write now lives ONLY in
    _route_campaign_terminate, invoked exclusively from
    determine_post_campaign_review_route()'s own, already-existing
    `rec == "terminate"` branch -- an EXPLICIT campaign-review decision, never
    inferred from a single hypothesis's kill verdict.
    """
    print("\n🛑 KILL: hypothesis dead (mechanism falsified / no edge / question answered negatively).")
    diag = _extract_diagnostics(path)
    update_campaign_state_after_run(run_id, "hypothesis", "",
                                     interp.get("hypothesis_family", ""), "kill", diag)
    # K4 symmetry: record the (null) continuation explicitly, same site A1's
    # other routing functions use -- this lineage has no child.
    update_state(path=path, continuation_child=None, continuation_created_by="_route_kill")
    return "completed_rejected"


def _route_campaign_terminate(path: Path, run_id: str, interp_or_review: dict, campaign: dict) -> str:
    """
    A9 (K2 kernel): campaign-WIDE termination -- the search space itself is
    declared exhausted, not just one hypothesis. This is the campaign-decision.yaml
    + campaign_state.status="space_empty" write _route_kill used to perform
    unconditionally; it now only runs from determine_post_campaign_review_route()'s
    `rec == "terminate"` branch, an explicit campaign_review recommendation
    (campaign-review scope, per A9's own fix text), never from a single
    hypothesis's own kill verdict.
    """
    print("\n🛑 CAMPAIGN TERMINATE: campaign_review recommends the search space is exhausted.")
    decision = {
        "campaign_id": campaign.get("campaign_id", "default"),
        "terminal_run": run_id,
        "decision": "kill",
        "rationale": interp_or_review.get("primary_failure_mode")
                     or interp_or_review.get("recommendation_rationale", "no rationale provided"),
        "altitude_justification": interp_or_review.get("altitude_justification", ""),
        "runs_attempted": campaign.get("runs", []),
        "families_tried": campaign.get("failed_families", []),
        "instruments_tried": campaign.get("instruments_tried", []),
        "components_built": campaign.get("components_built", []),
        "utc": datetime.now(timezone.utc).isoformat(),
    }
    save_yaml(ROOT / "campaign_decision.yaml", decision)
    print(f"  → Campaign decision written to campaign_decision.yaml")
    state = load_campaign_state()
    state["status"] = "space_empty"
    _save_campaign_state(state)
    return "completed_rejected"


def _extract_diagnostics(path: Path) -> dict:
    """Pull diagnostics from protocol_result.yaml for campaign logging."""
    try:
        pr = load_yaml(path / "artifacts" / "protocol_result.yaml")
        diag = (pr.get("hypothesis_verdict") or {}).get("diagnostics", {})
        return {
            "forecast_return_corr":      diag.get("median_forecast_return_corr"),
            "cost_drag_pct":             diag.get("median_cost_drag_pct"),
            "win_rate_vs_sharpe":        diag.get("win_rate_vs_sharpe"),
            "avg_trade_duration_bars":   diag.get("median_avg_trade_duration_bars"),
        }
    except Exception:
        return {}


def _compute_forecast_hash(config_path: Path) -> str:
    """
    E-025 S1 (2026-08-16, issue #28): fingerprint of the exact strategy config a trial
    tested, so cross-writer dedup (A6.4, deflate_sharpe.py::deduplicate_trials) can
    recognize when two trials -- possibly from different machines under the dual-writer
    protocol -- tested the same idea. Canonical JSON (sorted keys, no whitespace
    variance) so semantically-identical configs hash identically regardless of key
    order or formatting.

    Fails loud on a missing config rather than returning None/a placeholder: by the
    time either trial-recording function calls this, the same config file has already
    been read by the prescreen/backtest subprocess this trial's result came from, so
    its absence here means something is structurally wrong with the run's artifacts,
    not a normal degraded case worth silently tolerating (mandatory per E-025's
    2026-08-16 decision: forecast_hash on every new trial, both writers).
    """
    if not config_path.exists():
        raise FileNotFoundError(
            f"forecast_hash requires {config_path}, which does not exist. This trial's "
            f"own prescreen/backtest step already had to read this file to produce a "
            f"result -- its absence now means the artifacts directory is in an "
            f"unexpected state, not a normal case to silently skip hashing for."
        )
    canonical = json.dumps(json.loads(config_path.read_text(encoding="utf-8")), sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _record_prescreen_trial(run_id: str, ps: dict, config_path: Path):
    """
    A6.2: record a prescreen run as a trial in campaign_state.trial_sharpes.
    Prescreen kills count as trials (statistic_valid='neither', sharpe=null, n_trades=0).
    Prescreen passes that advance to backtest will have their full Sharpe recorded
    after protocol_execution completes.
    """
    state = load_campaign_state()
    trials = state.setdefault("trial_sharpes", [])
    route  = ps.get("route", "unknown")
    trial_entry = {
        "trial_id":        run_id,
        "source":          "prescreen",
        "route":           route,
        "sharpe":          None,
        "expectancy_bps":  None,
        "n_trades":        0,
        "statistic_valid": "neither",  # no backtest ran
        "ic_pooled":       ps.get("ic_spearman_pooled"),
        "cost_pass":       ps.get("cost_check", {}).get("pass"),
        "forecast_hash":   _compute_forecast_hash(config_path),
    }
    trials.append(trial_entry)
    _save_campaign_state(state)
    print(f"⚙️  A6.2: prescreen trial recorded in campaign_state.trial_sharpes "
          f"(route={route}, statistic_valid=neither)")


def _record_backtest_trial(run_id: str, summary: dict, config_path: Path):
    """
    A6.2: record a completed full-backtest as a trial in campaign_state.trial_sharpes.
    Appends {trial_id, source, sharpe, expectancy_bps, n_trades, statistic_valid}.
    Sparse-trading strategies (A3.4): statistic_valid='expectancy' when median Sharpe
    is null/unreliable; 'sharpe' otherwise.

    H3 fix (2026-08-16, issue #28): idempotency guard keyed on (trial_id, source) --
    NOT trial_id alone. A prescreen row for this same run_id was already recorded
    earlier in the run's lifecycle (see _record_prescreen_trial above), so a
    trial_id-only guard would wrongly treat that as "already recorded" and silently
    drop this legitimate backtest row. The guard here only suppresses a second
    "backtest"-source row for the same trial_id, which is the actual re-entry case
    (protocol_execution re-run via resume/retry) -- measured live in the committed
    ledger before this fix: run_054 and run_059 were each recorded 3x.
    """
    state  = load_campaign_state()
    trials = state.setdefault("trial_sharpes", [])

    if any(t.get("trial_id") == run_id and t.get("source") == "backtest" for t in trials):
        print(f"⏭️  A6.2/H3: backtest trial for {run_id} already recorded — skipping duplicate.")
        return

    hv    = summary.get("hypothesis_verdict") or {}
    diag  = hv.get("diagnostics") or {}
    pss   = summary.get("per_symbol_summary") or {}

    # Aggregate Sharpe and trade count across symbols
    sharpes     = [v.get("median_sharpe") for v in pss.values() if v.get("median_sharpe") is not None]
    trade_counts = [v.get("trade_count") or 0 for v in pss.values()]
    n_trades    = sum(trade_counts)
    median_sharpe = round(statistics.median(sharpes), 4) if sharpes else None

    expectancy   = diag.get("per_trade_expectancy_bps")
    below_floor  = diag.get("below_floor_pct", 0.0) or 0.0

    # A6.2 extension: sparse-trading strategies use expectancy, not Sharpe
    if below_floor > 50.0:
        statistic_valid = "expectancy"
    elif median_sharpe is not None:
        statistic_valid = "sharpe"
    else:
        statistic_valid = "neither"

    trial_entry = {
        "trial_id":        run_id,
        "source":          "backtest",
        "sharpe":          median_sharpe,
        "expectancy_bps":  expectancy,
        "n_trades":        n_trades,
        "statistic_valid": statistic_valid,
        "below_floor_pct": below_floor,
        "forecast_hash":   _compute_forecast_hash(config_path),
    }
    trials.append(trial_entry)
    _save_campaign_state(state)
    print(f"⚙️  A6.2: backtest trial recorded (sharpe={median_sharpe}, "
          f"n_trades={n_trades}, statistic_valid={statistic_valid})")


# ---------------------------------------------------------------------------
# Improvement 05 — AC1/AC2: KB auto-write and derived views
# ---------------------------------------------------------------------------

_KB_PATH = ROOT / "campaign_record" / "campaign_knowledge_base.yaml"

_VERDICT_TO_OUTCOME = {
    "insufficient_sample_inconclusive": "inconclusive",
    "parked_insufficient_sample": "inconclusive",
    "insufficient_power_a_priori": "inconclusive",
    "no_edge_observed": "no_edge_observed",
    "kill_no_ic": "no_edge_observed",
    "kill_cost_drag": "no_edge_observed",
    "signal_inversion": "no_edge_observed",
    "blocked_feed_unavailable": "blocked_feed_unavailable",
    "unusable_for_this_symbol_timeframe": "unusable_for_this_symbol_timeframe",
}


def _verdict_provenance_stamp(run_id_str: str) -> dict:
    """
    G6 / C7-EXT-R (D-4). Returns the provenance fields a KB record must carry,
    determined by what is ACTUALLY ON DISK for this run -- never asserted.

    Before this, _write_kb_findings_entry wrote a bare `outcome` with no
    provenance and no verdict_status, and then called the G6 validator on the
    result. That only passed because the validator did not look at `outcome`.
    With the validator repaired, the writer has to be able to satisfy it, and the
    only honest way to do that is to check:

      - runs/<id>/artifacts/pass_rule_evaluation.yaml exists AND resolved a
        binding PASS/FAIL  ->  verdict_status: gated, plus the citation;
      - anything else -> verdict_status: ungated. Not a demotion of the finding;
        a statement that the campaign's mechanical gate did not adjudicate it.
        Most runs legitimately land here (a prescreen kill never reaches a
        pass rule at all), and the record simply says so now.
    """
    if not run_id_str:
        return {"verdict_status": "ungated"}

    ref = f"runs/{run_id_str}/artifacts/pass_rule_evaluation.yaml"
    _tools_path = str(Path(__file__).parent.parent / "tools")
    if _tools_path not in sys.path:
        sys.path.insert(0, _tools_path)
    import verdict_criteria_evaluator as _vce

    ok, _detail = _vce.resolve_evaluation_ref(
        ref, {"evidence_runs": [run_id_str]}, root=ROOT)
    if ok:
        return {"verdict_status": "gated", "pass_rule_evaluation_ref": ref}
    return {"verdict_status": "ungated"}


def _find_kb_entry(findings: list, hyp_id: str) -> dict | None:
    for f in findings:
        if f.get("hypothesis_id") == hyp_id:
            return f
        if hyp_id in f.get("hypothesis_ids", []):
            return f
    return None


def _recompute_kb_views(kb: dict):
    """
    AC2: Recompute derived views after every KB write.
    - coverage_matrix: {edge_source_category: [{hypothesis_id, outcome, evidence_count}]}
    - exhausted_mechanisms: entries satisfying A5.1 threshold (ec>=3 OR analytic basis)
    """
    findings = kb.get("findings", [])

    coverage: dict = {}
    for f in findings:
        cat = f.get("edge_source_category") or "unclassified"
        outcome = f.get("outcome", "unknown")
        hyp_ids = (
            [f["hypothesis_id"]] if f.get("hypothesis_id")
            else f.get("hypothesis_ids", [])
        )
        for hyp_id in hyp_ids:
            coverage.setdefault(cat, []).append({
                "hypothesis_id": hyp_id,
                "finding_id": f.get("id"),
                "outcome": outcome,
                "evidence_count": f.get("evidence_count", 0),
            })
    kb["coverage_matrix"] = coverage

    exhausted = []
    for f in findings:
        if not f.get("exhausted"):
            continue
        ec = f.get("evidence_count", 0)
        basis = (f.get("exhausted_basis") or "").lower()
        is_analytic = "analytic" in basis
        if ec >= 3 or is_analytic:
            exhausted.append({
                "id": f.get("id"),
                "mechanism": f.get("mechanism"),
                "outcome": f.get("outcome"),
                "evidence_count": ec,
                "basis": "analytic" if is_analytic else "empirical",
            })
        else:
            print(f"⚠️  A5.1: KB entry '{f.get('id')}' has exhausted=true but "
                  f"evidence_count={ec} with no analytic basis — omitted from exhausted_mechanisms view")
    kb["exhausted_mechanisms"] = exhausted


def _write_kb_findings_entry(path: Path, run_id: str, interp: dict):
    """
    AC1 (A5.1-5.3): After every verdict, update or create a findings entry in
    campaign_knowledge_base.yaml. If the hypothesis_id already has an entry, increment
    evidence_count and append run_id. If not, create a minimal stub from verdict fields.
    Always calls _recompute_kb_views() before saving.
    """
    if not _KB_PATH.exists():
        print(f"⚠️  A5.1: campaign_knowledge_base.yaml not found — skipping KB update")
        return

    kb = load_yaml(_KB_PATH) or {}
    findings = kb.setdefault("findings", [])

    hyp_id = interp.get("hypothesis_id", "")
    if not hyp_id:
        print("⚠️  A5.1: verdict_interpretation.yaml missing hypothesis_id — skipping KB update")
        return

    run_id_str = str(interp.get("run_id") or run_id)
    # F10 (2026-07-06, run_053): verdict_interpreter's REAL output for this run used
    # neither verdict_label nor disposition — it wrote protocol_verdict: "kill" (generic,
    # not in _VERDICT_TO_OUTCOME) alongside prescreen_evidence.route: "kill_no_ic" (the
    # specific code that IS in the map). The old two-key lookup silently fell back to the
    # "inconclusive" default, writing a genuine no_edge_observed null into the KB as
    # merely "inconclusive" — the same class of schema drift as the validation stage's
    # family_status incident (F08). prescreen_evidence.route is checked before
    # protocol_verdict because it carries the specific outcome code; protocol_verdict is
    # last-resort (generic "kill"/"promote"/etc. wording that mostly won't match anyway,
    # but is still better than empty string).
    verdict_label = (
        interp.get("verdict_label")
        or interp.get("disposition")
        or (interp.get("prescreen_evidence") or {}).get("route")
        or interp.get("protocol_verdict")
        or ""
    ).lower()
    outcome = _VERDICT_TO_OUTCOME.get(verdict_label, "inconclusive")

    # G6 / C7-EXT-R (D-4): stamp this run's OWN provenance onto whatever we write.
    # The audit's sharpest finding was that this writer emitted a bare `outcome`
    # with neither a pass_rule_evaluation_ref nor a verdict_status -- so the
    # orchestrator's own output could not have satisfied the gate it then ran.
    # Every KB record now states which it is, computed from what is on disk:
    # cite the evaluator's artifact if the evaluator actually ran, else declare
    # the record ungated and keep the measurements.
    _pre_stamp = _verdict_provenance_stamp(run_id_str)

    existing = _find_kb_entry(findings, hyp_id)

    if existing:
        runs = existing.setdefault("evidence_runs", [])
        if run_id_str not in runs:
            runs.append(run_id_str)
            existing["evidence_count"] = len(runs)
        print(f"⚙️  A5.1: KB entry for {hyp_id} updated "
              f"(evidence_count={existing['evidence_count']}, run={run_id_str})")

        # F09 (2026-07-06, run_053 postmortem): a run that consumes an OPEN
        # reactivation_condition must close it here — otherwise the KB entry stays
        # stale (still describing the pre-reactivation outcome/underpowered state,
        # with reactivation_condition still inviting another attempt) even after a
        # corrected, adequately-powered re-run genuinely answers the question. This
        # exact gap let run_053's campaign_review propose reactivating H-041-A/H-041-C
        # on 2026-07-06 — run_050/run_048 (P1b) had already closed both, but neither
        # KB entry was ever written back with the new verdict, so reactivation_condition
        # was still non-null when campaign_review read it. Fixed here at the write
        # path (not just by hand-correcting the two stale entries — see
        # campaign_knowledge_base.yaml git history), so it cannot recur silently for
        # a future reactivation. Only fires when the new verdict is NOT itself another
        # inconclusive/underpowered result (re-parking an open condition is fine —
        # only a genuinely definitive new verdict should close it).
        if existing.get("reactivation_condition") and not existing.get("reactivation_consumed_by"):
            is_still_open = outcome == "inconclusive" or "insufficient" in verdict_label
            if not is_still_open:
                existing["reactivation_consumed_by"] = run_id_str
                existing["reactivation_condition"] = None
                existing["outcome"] = outcome
                # G6/D-4: provenance travels with the outcome. Drop any stale
                # citation first -- an entry re-adjudicated by an ungated run
                # must not keep a previous run's evaluation pointing at it.
                existing.pop("pass_rule_evaluation_ref", None)
                existing.update(_pre_stamp)
                existing["outcome_reason"] = verdict_label
                ps = interp.get("prescreen_result_summary", {})
                if ps:
                    existing["signal_property"] = {
                        k: ps.get(k) for k in ("ic_active_bars", "p_value", "n_eff", "n_episodes")
                        if ps.get(k) is not None
                    }
                power = interp.get("power_disposition")
                if power:
                    existing["power_disposition"] = power
                existing["exhausted"] = True
                existing["exhausted_basis"] = (
                    f"Empirical ({run_id_str}): reactivation_condition consumed with a "
                    f"definitive verdict ({verdict_label}). Auto-closed by "
                    f"_write_kb_findings_entry (F09) — REVIEW FOR ACCURACY, especially if "
                    f"the result is nuanced (e.g. era-conditional instability, a flipped "
                    f"sign, or anything a plain outcome enum can't capture); a stub close "
                    f"is a starting point for the human-authored narrative, not a substitute."
                )
                print(f"🔒 F09: reactivation_condition for {hyp_id} consumed by {run_id_str} "
                      f"— KB entry closed (outcome={outcome}). Review exhausted_basis for "
                      f"accuracy if the result is nuanced.")
    else:
        ps = interp.get("prescreen_result_summary", {})
        power = interp.get("power_disposition")
        stub = {
            "id": f"{hyp_id.lower().replace('-', '_').replace('/', '_')}_auto",
            "hypothesis_id": hyp_id,
            "evidence_runs": [run_id_str] if run_id_str else [],
            "evidence_count": 1 if run_id_str else 0,
            "outcome": outcome,
            **_pre_stamp,  # G6/D-4: provenance travels with the outcome
            "outcome_reason": verdict_label,
            "protocol_version": interp.get("protocol_version", "baseline_v2"),
            "detector_version": "not_applicable",
            "power_disposition": power if power else (
                "underpowered" if "insufficient_sample" in verdict_label else "not_applicable"
            ),
            "exhausted": False,
            "exhausted_basis": None,
            "reactivation_condition": interp.get("reactivation_trigger"),
        }
        if ps:
            stub["signal_property"] = {
                k: ps.get(k) for k in ("ic_active_bars", "p_value", "n_eff") if ps.get(k) is not None
            }
        findings.append(stub)
        print(f"⚙️  A5.1: KB stub entry created for {hyp_id} (outcome={outcome}, run={run_id_str})")

    # G6 (C7-EXT): every finding must clear verdict-provenance before the KB is
    # saved -- not just the one this call touched. The KB is the campaign's
    # memory; a verdict written into it without evaluator provenance becomes
    # indistinguishable, later, from one that earned its way there. Validating
    # the whole list also means a hand-edited entry cannot slip in behind a
    # legitimate write.
    _tools_path = str(Path(__file__).parent.parent / "tools")
    if _tools_path not in sys.path:
        sys.path.insert(0, _tools_path)
    import verdict_criteria_evaluator as _vce
    for f_entry in findings:
        if isinstance(f_entry, dict):
            # C7-EXT-R/D-4: `root` is what lets the evaluator RESOLVE a cited
            # pass_rule_evaluation_ref rather than accept any truthy string.
            _vce.validate_verdict_provenance(
                f_entry, entry_ref=f"KB finding {f_entry.get('id')!r}", root=ROOT)

    _recompute_kb_views(kb)
    save_yaml(_KB_PATH, kb)


# ---------------------------------------------------------------------------
# A8.6: A-priori power pre-flight (inline of power_check.py logic)
# ---------------------------------------------------------------------------

def _load_rho_bar() -> float:
    """Load measured ρ̄ from campaign_config.yaml. Falls back to 0.82 if unavailable."""
    cfg_path = ROOT / "config" / "campaign_config.yaml"
    try:
        cfg = load_yaml(cfg_path) or {}
        return float(cfg.get("symbol_correlation", {}).get("btc_eth_return_correlation_1h", 0.82))
    except Exception:
        return 0.82


# ---------------------------------------------------------------------------
# Soft patch (b) — P1a shakedown, 2026-07-04: LLM-vs-machine power discrepancy log.
#
# hypothesis_card.schema.json's power_parameters block only requires the INPUTS
# (activation_rate, plausible_ic_upper, n_bars, n_symbols, is_market_wide) — it has no
# fields for a derived n_eff/min_detectable_ic/verdict. In practice the LLM writes its
# own self-computed conclusion anyway, free-form, usually embedded in prose
# (a_priori_calculation / power_notes). Fixture: run_044 (2026-07-04) declared
# is_market_wide=false (correctly — funding rate is per-symbol, not a shared index) but
# then applied a rho-based discount anyway in its own prose
# ("n_eff_symbols ≈ sqrt(2) / (1 + 0.82) ≈ 1.1") — contradicting its own flag AND using
# a formula that isn't even n/(1+(n-1)*rho) (the real one). Its self-reported
# n_eff≈100.4 came in materially lower than the machine's actual n_eff=182.5 at the same
# inputs. This was never caught because the run crashed one stage earlier (YAML parse
# error) before _run_a86_power_check ever ran on it. This log exists so a human can spot
# this class of self-contradiction even when the run never reaches the point that would
# have machine-verified it.
# ---------------------------------------------------------------------------

_POWER_DISCREPANCY_LOG_PATH = ROOT / "power_check_discrepancy_log.yaml"


def _extract_llm_reported_power(card: dict) -> dict:
    """
    Best-effort extraction of the LLM's OWN self-computed power numbers from
    hypothesis_card.yaml. Returns only whatever it can find — missing keys are absent,
    not zero or None-filled, so callers can distinguish "not reported" from "reported
    as zero."
    """
    params = card.get("power_parameters", {}) or {}
    out = {}

    if isinstance(params.get("n_symbols_effective"), (int, float)):
        out["n_symbols_effective"] = float(params["n_symbols_effective"])

    prose = " ".join(
        str(params.get(k, "")) for k in ("a_priori_calculation", "power_notes", "power_note")
    )

    _NUM = r"(\d+\.\d+|\d+)"
    m = re.search(r"expected_n_eff\s*=?\s*[^=]*?=\s*" + _NUM, prose)
    if not m:
        m = re.search(r"\bn_eff\s*[≈=]\s*" + _NUM, prose)
    if m:
        out["expected_n_eff"] = float(m.group(1))

    m = re.search(r"min_detectable_ic\s*=?\s*[^=]*?[≈=]\s*" + _NUM, prose)
    if m:
        out["min_detectable_ic"] = float(m.group(1))

    for key in ("verdict", "power_verdict"):
        if key in params and isinstance(params[key], str):
            out["power_verdict"] = params[key]
            break

    return out


def _log_power_check_discrepancy(run_id: str, hyp_id: str, machine: dict, llm_reported: dict,
                                  discrepancies: list):
    """Append one entry to the running discrepancy log. Never raises — this is an
    observability aid, not a gate; a logging bug must not block the pipeline."""
    try:
        existing = load_yaml(_POWER_DISCREPANCY_LOG_PATH) if _POWER_DISCREPANCY_LOG_PATH.exists() else None
        log = existing or {"entries": []}
        log.setdefault("entries", []).append({
            "run_id": run_id,
            "hypothesis_id": hyp_id,
            "logged_at": datetime.now(timezone.utc).isoformat(),
            "machine_computed": machine,
            "llm_reported": llm_reported,
            "discrepancies": discrepancies,
        })
        save_yaml(_POWER_DISCREPANCY_LOG_PATH, log)
        print(f"⚠️  A8.6 discrepancy log: {len(discrepancies)} field(s) diverged for "
              f"{hyp_id} ({run_id}) — see {_POWER_DISCREPANCY_LOG_PATH.name}")
    except Exception as e:
        print(f"⚠️  Could not write power_check_discrepancy_log.yaml: {e}")


def _compare_llm_vs_machine_power(run_id: str, hyp_id: str, machine: dict, card: dict,
                                   rel_tol: float = 0.20):
    """Compare the machine-computed A8.6 result against whatever the LLM self-reported.
    Logs (does not gate) any field that diverges by more than rel_tol (relative) or any
    outright contradiction (is_market_wide=false but a correlation discount applied)."""
    llm_reported = _extract_llm_reported_power(card)
    if not llm_reported:
        return  # LLM reported nothing derived — nothing to compare

    discrepancies = []

    params = card.get("power_parameters", {}) or {}
    is_market_wide = bool(params.get("is_market_wide", False))
    if not is_market_wide and llm_reported.get("n_symbols_effective") not in (None,) \
            and abs(llm_reported["n_symbols_effective"] - float(params.get("n_symbols", 2))) > 1e-6:
        discrepancies.append(
            f"is_market_wide=false but n_symbols_effective={llm_reported['n_symbols_effective']} "
            f"!= n_symbols={params.get('n_symbols', 2)} — a correlation discount was applied "
            f"despite the signal being declared per-symbol, not a shared index. Per "
            f"_run_a86_power_check, no discount should apply here."
        )

    for field in ("expected_n_eff", "min_detectable_ic"):
        llm_val = llm_reported.get(field)
        machine_val = machine.get(field)
        if llm_val is None or machine_val is None:
            continue
        denom = max(abs(machine_val), 1e-9)
        if abs(llm_val - machine_val) / denom > rel_tol:
            discrepancies.append(
                f"{field}: LLM self-reported {llm_val} vs machine-computed {machine_val} "
                f"(>{rel_tol:.0%} relative difference)"
            )

    if llm_reported.get("power_verdict") and machine.get("verdict"):
        llm_says_adequate = "adequate" in llm_reported["power_verdict"].lower() or \
            "sufficient" in llm_reported["power_verdict"].lower()
        machine_says_adequate = machine["verdict"] == "power_adequate"
        if llm_says_adequate != machine_says_adequate:
            discrepancies.append(
                f"power_verdict: LLM said '{llm_reported['power_verdict']}' "
                f"(adequate={llm_says_adequate}) vs machine verdict='{machine['verdict']}' "
                f"(adequate={machine_says_adequate})"
            )

    if discrepancies:
        _log_power_check_discrepancy(run_id, hyp_id, machine, llm_reported, discrepancies)


# 2026-07-07: A8.6 block_size, timeframe-aware (mirrors prescreen_signal.py's
# _BLOCK_SIZE_1H/_BLOCK_SIZE_1D — both must be updated together, same as the
# power_check.py/prescreen_signal.py mirroring this docstring already calls out).
_A86_BLOCK_SIZE_BY_TIMEFRAME = {"1h": 24, "1d": 1}


def _run_a86_power_check(artifacts: Path) -> dict:
    """
    A8.6: compute expected statistical power from hypothesis_card.yaml power_parameters.
    Returns result dict with 'verdict' key: power_adequate | insufficient_power_a_priori | skip.
    Mirrors power_check.py logic identically — both must be updated together.

    Correlation correction (A8.6 amendment): n_eff_symbols = n / (1 + (n-1)*rho_bar).
    sqrt(n) heuristic is NOT used; it materially overstates power for correlated symbols.
    """
    import math as _math
    card_path = artifacts / "hypothesis_card.yaml"
    if not card_path.exists():
        return {"verdict": "skip", "reason": "hypothesis_card.yaml not found"}

    card = load_yaml(card_path) or {}
    params = card.get("power_parameters", {})
    if not params:
        return {"verdict": "skip", "reason": "no power_parameters block"}

    activation_rate = params.get("activation_rate")
    plausible_ic_upper = params.get("plausible_ic_upper")
    if activation_rate is None or plausible_ic_upper is None:
        return {"verdict": "skip", "reason": "power_parameters incomplete (activation_rate or plausible_ic_upper is null)"}

    n_bars = params.get("n_bars", 17520)
    n_symbols = params.get("n_symbols", 2)
    is_market_wide = params.get("is_market_wide", False)
    # 2026-07-07: block_size must match the run's actual timeframe — this was
    # hardcoded to 24 (1h bars/day) with no dispatch at all, silently treating
    # a daily-bar hypothesis's power_parameters.n_bars as if they were hourly
    # (n_eff off by a full 24x). Read timeframe from research_brief.yaml (the
    # standard schema field every run already carries); default "1h" preserves
    # every prior run's exact behavior when the field is absent.
    brief_path = artifacts / "research_brief.yaml"
    timeframe = (load_yaml(brief_path) or {}).get("timeframe", "1h") if brief_path.exists() else "1h"
    block_size = _A86_BLOCK_SIZE_BY_TIMEFRAME.get(timeframe, 24)

    if is_market_wide:
        rho = _load_rho_bar()
        n_sym_eff = n_symbols / (1.0 + (n_symbols - 1) * rho)
    else:
        rho = 0.0
        n_sym_eff = float(n_symbols)

    active_n = activation_rate * n_bars * n_sym_eff
    n_eff = active_n / block_size
    mde = 1.0 / _math.sqrt(max(n_eff - 3.0, 1.0))

    verdict = "insufficient_power_a_priori" if mde > plausible_ic_upper else "power_adequate"
    result = {
        "verdict": verdict,
        "expected_active_n": round(active_n, 1),
        "expected_n_eff": round(n_eff, 2),
        "min_detectable_ic": round(mde, 4),
        "plausible_ic_upper": plausible_ic_upper,
        "n_eff_symbols": round(n_sym_eff, 3),
        "rho_bar": round(rho, 4) if is_market_wide else None,
        "is_market_wide": is_market_wide,
        "data_requirement": params.get("data_requirement") if verdict == "insufficient_power_a_priori" else None,
    }

    # Soft patch (b): log (never gate on) any LLM-vs-machine power discrepancy.
    _compare_llm_vs_machine_power(
        run_id=artifacts.parent.name, hyp_id=card.get("hypothesis_id", "unknown"),
        machine=result, card=card,
    )

    return result


def _create_protocol_result_from_prescreen(path: Path, ps: dict):
    """
    When a prescreen kills (route=kill_* or refine_*), create a minimal
    protocol_result.yaml from prescreen evidence so verdict_interpreter
    can run its standard artifact-based flow.

    The stub carries IC and estimated cost_drag as the primary diagnostics.
    The verdict_interpreter skill reads prescreen_result.yaml (injected as
    optional input) for full prescreen context.
    """
    pr_path = path / "artifacts" / "protocol_result.yaml"
    if pr_path.exists():
        return  # don't overwrite an existing real result

    ic_pooled   = ps.get("ic_spearman_pooled")
    cost_pass   = ps.get("cost_check", {}).get("pass", False)
    ratio       = ps.get("cost_check", {}).get("edge_to_cost_ratio")
    route       = ps.get("route", "unknown")

    # Estimate cost_drag_pct from edge_to_cost_ratio:
    # if ratio = 0.5, edge covers 50% of cost → cost_drag ≈ 200% (cost > gross edge).
    # If ratio = 0, edge = 0 → cost_drag is undefined; use sentinel 999%.
    if ratio is not None and ratio > 0:
        estimated_cost_drag = round(100.0 / ratio, 1)
    elif ratio is not None and ratio == 0:
        estimated_cost_drag = 999.0
    else:
        estimated_cost_drag = None

    stub = {
        "source":           "prescreen_stub",
        "prescreen_route":  route,
        "hypothesis_verdict": {
            "verdict": "kill" if route.startswith("kill_") else "refine",
            "criteria_results": [],
            "verdict_reason": f"Prescreen gate: {ps.get('route_rationale', '')}",
            "diagnostics": {
                "median_forecast_return_corr":    ic_pooled,
                "median_cost_drag_pct":           estimated_cost_drag,
                "median_gross_pnl":               None,
                "median_avg_trade_duration_bars": None,
                "uninformative_regimes":          [],
                "win_rate_vs_sharpe":             "N/A (prescreen kill — no backtest)",
                "below_floor_pct":                100.0,  # no trades
                "per_trade_expectancy_bps":       None,
                "zero_trade_slot_pct":            100.0,
            },
        },
        "per_symbol_summary": {},
        "results":           [],
        "prescreen_kill_reason": ps.get("prescreen_kill_reason"),
    }
    save_yaml(pr_path, stub)
    print(f"⚙️  Created protocol_result.yaml stub from prescreen evidence "
          f"(route={route}, IC={ic_pooled})")


def determine_post_prescreen_route(path: Path) -> str:
    """
    Route after signal_prescreen based on prescreen_result.yaml.

    A8.1: proceed_to_backtest requires both ic_significance AND cost_check.pass.
    Kill/refine routes skip the full backtest and go directly to verdict_interpreter
    (with a stub protocol_result.yaml created from prescreen evidence).
    """
    ps_path = path / "artifacts" / "prescreen_result.yaml"
    if not ps_path.exists():
        print("⚠️  prescreen_result.yaml missing — skipping prescreen gate, continuing to backtest.")
        return "protocol_execution"

    ps    = load_yaml(ps_path)

    # F4d (2026-07-05, run_047): pre-registration conformance gate. A prescreen
    # that silently used the wrong protocol range or dropped a MANDATORY
    # significance methodology tested something other than what was
    # pre-registered — that is an engineering failure, not a scientific result,
    # regardless of what route the tool itself computed. Must never reach
    # verdict_interpreter (no KB write, no verdict) — same principle as F5c's
    # no_signal_artifact.
    constraints = _load_machine_constraints(path)
    if constraints:
        protocol_obj = {}
        protocol_path_str = ps.get("protocol_version")
        if protocol_path_str:
            candidate = Path(protocol_path_str)
            if not candidate.is_absolute():
                candidate = ROOT / candidate
            if candidate.exists():
                with open(candidate, encoding="utf-8") as f:
                    protocol_obj = json.load(f)
        violations = _check_prescreen_conformance(ps, constraints, protocol_obj)
        if violations:
            print("\n🛑 [F4d] PRE-REGISTRATION CONFORMANCE VIOLATION — this prescreen did "
                  "NOT test what was pre-registered:")
            for v in violations:
                print(f"   - {v}")
            run_id = path.name
            _mark_trial_invalidated(run_id, "; ".join(violations))
            update_state(path=path, status="paused_for_human",
                         flags={"conformance_violation": True},
                         conformance_violations=violations)
            return "human_pause"

    route = ps.get("route", "proceed_to_backtest")

    if route == "proceed_to_backtest":
        print(f"✅ Prescreen PASSED — advancing to protocol_execution.")
        return "protocol_execution"

    # F5c (2026-07-04): no_signal_artifact is an engineering failure (component never
    # emitted, or errored on every bar), NOT a scientific result. It must never reach
    # verdict_interpreter or get a KB write — that would treat a bug as a research
    # finding (see run_044, 2026-07-04, killed on this basis before F5 existed).
    # Pause for a human to fix the component/config; no trial is spent, no
    # findings_carryover is produced, no proposed_brief pivots the hypothesis away.
    if route == "no_signal_artifact":
        print(f"\n⏸️  ENGINEERING PAUSE (F5c): prescreen route=no_signal_artifact. "
              f"{ps.get('route_rationale', '')}")
        print(f"   component_error_count={ps.get('component_error_count', 0)} — "
              f"see component_error_sample in {ps_path.name}.")
        print("   This is NOT a kill/refine/pivot verdict. Fix the underlying component "
              "or config, then re-run signal_prescreen fresh (do not resume into "
              "verdict_interpreter — there is nothing for it to interpret).")
        update_state(path=path, status="paused_for_human",
                     flags={"no_signal_artifact_flagged": True})
        return "human_pause"

    # All other routes (kill_* or refine_*) skip the full backtest
    print(f"🔬 Prescreen gate triggered: {route}. "
          f"Creating stub protocol_result and routing to verdict_interpreter.")
    _create_protocol_result_from_prescreen(path, ps)
    return "verdict_interpreter"


def _inject_prescreen_context_into_verdict_handoff(handoff_path: Path, ps: dict):
    """
    When a prescreen kill routes directly to verdict_interpreter (no backtest ran),
    inject prescreen_result.yaml as a required input and add a constraint note
    so the skill knows to interpret prescreen evidence instead of backtest evidence.
    """
    if not handoff_path.exists():
        return

    handoff = load_yaml(handoff_path) or {}

    # Add prescreen_result as required input (backtest was skipped)
    req = handoff.setdefault("required_inputs", [])
    paths_present = {x.get("path") for x in req}
    if "artifacts/prescreen_result.yaml" not in paths_present:
        req.append({
            "path":   "artifacts/prescreen_result.yaml",
            "reason": "Prescreen killed this run — protocol_result.yaml is a stub. "
                      "Use prescreen_result.yaml as the primary evidence source.",
        })

    # Note for the skill
    constraints = handoff.setdefault("constraints", [])
    ps_note = (
        f"PRESCREEN KILL: This run was terminated by signal_prescreen "
        f"(route={ps.get('route')}, IC={ps.get('ic_spearman_pooled')}, "
        f"cost_pass={ps.get('cost_check', {}).get('pass')}). "
        f"protocol_result.yaml is a prescreen stub, NOT a full backtest result. "
        f"Base your verdict on prescreen_result.yaml evidence. "
        f"Apply the appropriate Diagnostic Rule from the prescreen route: "
        f"kill_no_ic → Rule 2 (weak signal); refine_inverted_ic → Rule 3 (signal inversion); "
        f"refine_cost_hurdle → Rule 1 (cost drag, raise threshold_filter); "
        f"kill_cost_hurdle → Rule 1 (cost drag, structural — kill); "
        f"insufficient_power_a_priori → A8.6 power gate: no IC computed, disposition=parked, "
        f"do_not_add_to_failed_families=true, verdict_label=insufficient_power_a_priori."
    )
    if ps_note not in constraints:
        constraints.append(ps_note)

    handoff["prescreen_route"] = ps.get("route")
    handoff["prescreen_ic"]    = ps.get("ic_spearman_pooled")
    save_yaml(handoff_path, handoff)
    print(f"✅ Prescreen context injected into verdict_interpreter handoff "
          f"(route={ps.get('route')})")


def _auto_generate_findings_carryover(path: Path, interp: dict, lineage_routing: str = None):
    """
    Constructs findings_carryover.yaml from verdict_interpretation.yaml when the LLM
    omitted it. Called after verdict_interpreter completes, before _verify_verdict_outputs.
    Safe to call unconditionally — skips if the file already exists.

    A8 (K2 kernel, 2026-07-13): branches on `lineage_routing` (what the NEXT
    run should avoid -- a routing question) rather than the legacy `status`
    enum. Callers that already resolved lineage_routing (e.g.
    determine_post_verdict_route) should pass it directly; if omitted, falls
    back to deriving it from the legacy `status` field for a not-yet-migrated
    call site.
    """
    carryover_path = path / "artifacts" / "findings_carryover.yaml"
    if carryover_path.exists():
        return

    if lineage_routing is None:
        legacy_status = (interp.get("status") or "").strip().lower()
        mapped = _LEGACY_STATUS_TO_VERDICT_ROUTING.get(legacy_status)
        lineage_routing = mapped[1] if mapped else legacy_status

    status = lineage_routing
    if status not in ("refine", "pivot", "escalate"):
        return

    altitude_just = interp.get("altitude_justification", "")

    # First sentence of altitude_justification → diagnostic_rule_applied
    first_sentence = altitude_just.split(". ")[0].strip() if altitude_just else "Rule unknown: no altitude_justification provided"

    def _extract_float(pattern: str, text: str):
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1).lstrip("+"))
            except ValueError:
                return None
        return None

    corr      = _extract_float(r'(?:forecast_return_corr|corr)=([+-]?[\d.]+)', altitude_just)
    cost_drag = _extract_float(r'cost_drag(?:_pct)?=([+-]?[\d.]+)', altitude_just)
    gross_pnl = _extract_float(r'gross_pnl=([+-]?[\d.]+)', altitude_just)

    what_failed = [
        c.get("criterion", str(c))
        for c in (interp.get("criteria_summary") or [])
        if str(c.get("result", "")).upper() == "FAIL"
    ]
    if not what_failed:
        what_failed = ["No explicit FAIL criteria found — see altitude_justification"]

    dim    = interp.get("proposed_change_dimension", "")
    family = interp.get("hypothesis_family", "")
    if status == "refine":
        what_not_to_try = [
            f"Do not change {dim} further without addressing the root cause cited in altitude_justification"
            if dim else "Do not repeat the same parameter dimension"
        ]
    elif status == "pivot":
        what_not_to_try = [
            f"Do not retry {family} hypothesis family — parameter space exhausted"
            if family else "Do not retry this hypothesis family"
        ]
    else:  # escalate
        what_not_to_try = [
            f"Do not apply {family} signal further on current instrument — regime/signal failure confirmed"
            if family else "Do not apply this signal on the current instrument"
        ]

    save_yaml(carryover_path, {
        "hypothesis_id":           interp.get("hypothesis_id", "unknown"),
        "what_failed":             what_failed,
        "diagnostic_rule_applied": first_sentence,
        "diagnostic_snapshot": {
            "forecast_return_corr": corr,
            "cost_drag_pct":        cost_drag,
            "gross_pnl":            gross_pnl,
        },
        "what_not_to_try": what_not_to_try,
        "next_altitude":   status,
    })
    print("⚙️ Auto-generated findings_carryover.yaml from verdict artifacts.")


def _verify_verdict_outputs(run_dir: Path) -> list:
    """
    Check that verdict_interpreter produced the right artifacts for its declared status.
    Always reads verdict_interpretation.yaml fresh — never uses caller-modified status.
    Returns a list of violation strings. Empty list = all checks pass.
    """
    violations = []
    ARTIFACTS = run_dir / "artifacts"
    interp = load_yaml(ARTIFACTS / "verdict_interpretation.yaml")

    # A8 (K2 kernel): derive lineage_routing from the artifact ITSELF, not from
    # any caller-supplied value (unchanged discipline from the pre-K2 status
    # field) -- which deliverable is required is a ROUTING question, prefer
    # the artifact's own lineage_routing field, falling back to the legacy
    # status field for a not-yet-migrated artifact.
    legacy_status = (interp.get("status") or interp.get("protocol_verdict") or "").strip().lower()
    status = interp.get("lineage_routing")
    if not status:
        mapped = _LEGACY_STATUS_TO_VERDICT_ROUTING.get(legacy_status)
        status = mapped[1] if mapped else legacy_status

    # Universal checks (all statuses)
    if not interp.get("altitude_justification"):
        violations.append("verdict_interpretation.yaml missing altitude_justification")
    if not status:
        violations.append("verdict_interpretation.yaml missing status/lineage_routing field")

    if status == "pivot":
        # pivot does NOT produce proposed_brief.yaml — the next run's brief is
        # generated fresh by hypothesis_generation using findings_carryover as input.
        # findings_carryover must exist and contain diagnostic_rule_applied
        carryover_path = ARTIFACTS / "findings_carryover.yaml"
        if not carryover_path.exists():
            violations.append("pivot: findings_carryover.yaml not produced")
        else:
            carryover = load_yaml(carryover_path)
            if not carryover.get("diagnostic_rule_applied"):
                violations.append(
                    "pivot: findings_carryover.yaml missing diagnostic_rule_applied field"
                )
            if not carryover.get("what_not_to_try"):
                violations.append(
                    "pivot: findings_carryover.yaml missing what_not_to_try field"
                )

    if status == "refine":
        proposed_path = ARTIFACTS / "proposed_brief.yaml"
        if not proposed_path.exists():
            violations.append("refine: proposed_brief.yaml not produced")
        else:
            dim = interp.get("proposed_change_dimension", "")
            family = interp.get("hypothesis_family", "")
            campaign = load_campaign_state()
            recent   = campaign.get("recent_parameter_dimensions_by_family", {}).get(family, [])
            if dim and dim in recent:
                violations.append(
                    f"refine: proposed_change_dimension '{dim}' was already tried for "
                    f"family '{family}' (in recent_parameter_dimensions_by_family: {recent}). "
                    f"Should have pivoted."
                )
            if not interp.get("proposed_change_dimension"):
                violations.append(
                    "refine: verdict_interpretation.yaml missing proposed_change_dimension"
                )

        # findings_carryover must exist for refine (cross-run directional memory)
        carryover_path = ARTIFACTS / "findings_carryover.yaml"
        if not carryover_path.exists():
            violations.append("refine: findings_carryover.yaml not produced")
        else:
            carryover = load_yaml(carryover_path)
            if not carryover.get("diagnostic_rule_applied"):
                violations.append(
                    "refine: findings_carryover.yaml missing diagnostic_rule_applied field"
                )
            if not carryover.get("what_not_to_try"):
                violations.append(
                    "refine: findings_carryover.yaml missing what_not_to_try field"
                )

    if status == "escalate":
        carryover_path = ARTIFACTS / "findings_carryover.yaml"
        if not carryover_path.exists():
            violations.append("escalate: findings_carryover.yaml not produced")
        else:
            carryover = load_yaml(carryover_path)
            if not carryover.get("diagnostic_rule_applied"):
                violations.append("escalate: findings_carryover.yaml missing diagnostic_rule_applied field")
            if not carryover.get("what_not_to_try"):
                violations.append("escalate: findings_carryover.yaml missing what_not_to_try field")
        escalation_path = ARTIFACTS / "escalation_request.yaml"
        if not escalation_path.exists():
            violations.append("escalate: escalation_request.yaml not produced")

    return violations


def _should_trigger_campaign_review(campaign: dict) -> bool:
    """
    Trigger campaign review when:
    - 2+ distinct hypothesis families have failed, OR
    - run count hits a multiple of review_every_n_runs (e.g. every 6 runs)
    Note: called AFTER the current run is recorded in campaign_state, so counts are current.

    F3 (P1a shakedown, 2026-07-04): campaign_state.yaml's failed_families is a MIXED
    list — the six historical entries (tagged 2026-07-02, Improvement 07) are dicts
    with {name, evidence_window, root_cause}; record_pivot() (still live) appends
    plain strings. `set(failed)` on a list containing dicts raises
    `TypeError: unhashable type: 'dict'` — this is what crashed run_043's second
    attempt (2026-07-04), the first live run to reach this function since the
    Improvement 07 retag (every prior non-kill/non-promote verdict was either
    pre-retag or backfilled manually, bypassing this code path). Extract the
    distinct family NAME from either shape instead of hashing the raw entry.
    """
    failed = campaign.get("failed_families", [])
    runs   = campaign.get("runs", [])
    review_n = campaign.get("review_every_n_runs", 6)
    distinct_names = {(f.get("name") if isinstance(f, dict) else f) for f in failed}
    families_trigger = len(distinct_names) >= 2   # distinct families, not total entries
    budget_trigger   = len(runs) > 0 and len(runs) % review_n == 0
    return families_trigger or budget_trigger


# ---------------------------------------------------------------------------
# Improvement 06 — promotion audit and holdout evaluation
# ---------------------------------------------------------------------------

_DATA_POLICY_PATH = ROOT / "config" / "campaign_data_policy.yaml"


def _write_promotion_audit(run_dir: Path, run_id: str):
    """
    A6.2: Write promotion_audit.yaml before holdout_evaluation.
    Compute Deflated Sharpe over statistic_valid='sharpe' trials from campaign_state.
    For sparse-trading candidates (statistic_valid='expectancy'), record expectancy t-stat.
    """
    import math as _math
    from statistics import NormalDist as _NDist

    _nd = _NDist(0, 1)

    def _phi(x: float) -> float:
        return _nd.cdf(x)

    def _phi_inv(p: float) -> float:
        p = max(1e-10, min(1 - 1e-10, p))
        return _nd.inv_cdf(p)

    EULER_GAMMA = 0.5772156649
    DSR_THRESHOLD = 0.95

    # --- Load verdict interpretation for hypothesis_id and candidate SR ---
    interp      = load_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml") or {}
    hyp_id      = interp.get("hypothesis_id", run_id)
    pr_path     = run_dir / "artifacts" / "protocol_result.yaml"
    pr          = load_yaml(pr_path) if pr_path.exists() else {}
    pss         = pr.get("per_symbol_summary") or {}
    hv_diag     = (pr.get("hypothesis_verdict") or {}).get("diagnostics") or {}

    sharpes_raw   = [v.get("median_sharpe") for v in pss.values() if v.get("median_sharpe") is not None]
    raw_median_sr = round(statistics.median(sharpes_raw), 4) if sharpes_raw else None
    below_floor   = hv_diag.get("below_floor_pct", 0.0) or 0.0
    is_sparse     = below_floor > 50.0
    expectancy_bps = hv_diag.get("per_trade_expectancy_bps")

    # --- Load and filter trial_sharpes from campaign_state ---
    campaign   = load_campaign_state()
    all_trials = campaign.get("trial_sharpes", [])

    # F8b (2026-07-04): exclude invalidated_artifact trials FIRST, before dedup or any
    # count. These represent zero actual hypothesis testing (e.g. run_044's
    # FundingRateMeanReversionComponent threshold=0 divide-by-zero, F5a) and must not
    # inflate the multiple-testing correction basis or the Sharpe trial distribution.
    # Mirrors tools/deflate_sharpe.py::exclude_invalidated_trials — this is a separate,
    # independent implementation (inline promotion path vs. standalone holdout tool)
    # and both must apply the exclusion identically.
    n_invalidated = sum(1 for t in all_trials if t.get("invalidated_artifact"))
    valid_trials = [t for t in all_trials if not t.get("invalidated_artifact")]

    # A6.4: deduplicate by forecast_hash
    seen_hashes: set = set()
    deduped_trials = []
    n_dedup_removed = 0
    for t in valid_trials:
        fh = t.get("forecast_hash")
        if fh and fh in seen_hashes:
            n_dedup_removed += 1
        else:
            if fh:
                seen_hashes.add(fh)
            deduped_trials.append(t)

    # A6.2: compute over statistic_valid='sharpe' only
    excluded = {"statistic_expectancy": 0, "statistic_neither": 0, "no_sharpe_value": 0,
                "dedup_removed": n_dedup_removed, "invalidated_artifact": n_invalidated}
    sharpe_values = []
    for t in deduped_trials:
        sv = t.get("statistic_valid")
        if sv == "expectancy":
            excluded["statistic_expectancy"] += 1
            continue
        if sv == "neither":
            excluded["statistic_neither"] += 1
            continue
        s = t.get("sharpe")
        if s is None:
            excluded["no_sharpe_value"] += 1
            continue
        sharpe_values.append(float(s))

    n_trials = len(sharpe_values)
    total_tested = len(valid_trials)  # F8b: excludes invalidated_artifact trials

    # --- Deflated Sharpe computation ---
    dsr_result: dict = {}
    passes_deflated = None

    if is_sparse:
        # Sparse path: expectancy t-stat
        n_trades = sum(t.get("n_trades", 0) for t in deduped_trials if t.get("statistic_valid") == "expectancy")
        exp_se   = None  # SE not yet stored in protocol_result; placeholder
        t_stat   = None
        if expectancy_bps is not None and n_trades > 1:
            # SE approximation: stdev of per-trade PnL / sqrt(n_trades).
            # We don't store this yet; flag as indeterminate.
            pass
        passes_deflated = None  # indeterminate without SE
        dsr_result = {
            "deflated_sharpe_ratio":   None,
            "expected_max_sharpe":     None,
            "trial_sharpe_variance":   None,
            "correction_method":       "expectancy_t_stat_bonferroni",
            "expectancy_promotion": {
                "t_stat":          t_stat,
                "passes":          passes_deflated,
                "bonferroni_note": (
                    f"Bonferroni-adjusted alpha = 0.05/{max(total_tested,1)} = {0.05/max(total_tested,1):.4f}; "
                    f"threshold t > 2.0 used as conservative approximation. "
                    f"Expectancy SE not yet stored in protocol_result — passes=null until SE is available."
                ),
            },
        }
    elif n_trials < 2:
        dsr_result = {
            "deflated_sharpe_ratio": None,
            "expected_max_sharpe":   None,
            "trial_sharpe_variance": None,
            "correction_method":     "baiey_lopez_prado_2014",
            "dsr_error":             f"Insufficient sharpe-valid trials for DSR (n={n_trials}, need ≥2)",
        }
        passes_deflated = False
    else:
        mu_sr    = statistics.mean(sharpe_values)
        sigma_sr = statistics.stdev(sharpe_values)
        var_sr   = sigma_sr ** 2

        if sigma_sr < 1e-10:
            dsr_result = {
                "deflated_sharpe_ratio": None,
                "expected_max_sharpe":   None,
                "trial_sharpe_variance": round(var_sr, 6),
                "correction_method":     "baiey_lopez_prado_2014",
                "dsr_error":             "Zero trial Sharpe variance — all trials identical; DSR undefined.",
            }
            passes_deflated = False
        else:
            N = n_trials
            z1 = _phi_inv(1.0 - 1.0 / N)
            z2 = _phi_inv(1.0 - 1.0 / (_math.e * N))
            z_exp_max = (1.0 - EULER_GAMMA) * z1 + EULER_GAMMA * z2
            e_max_sr  = mu_sr + sigma_sr * z_exp_max

            candidate = raw_median_sr if raw_median_sr is not None else 0.0
            z = (candidate - e_max_sr) / sigma_sr
            dsr = _phi(z)

            passes_deflated = dsr > DSR_THRESHOLD
            dsr_result = {
                "deflated_sharpe_ratio": round(dsr, 4),
                "expected_max_sharpe":   round(e_max_sr, 4),
                "trial_sharpe_variance": round(var_sr, 6),
                "correction_method":     "baiey_lopez_prado_2014",
            }

    audit = {
        "hypothesis_id":              hyp_id,
        "generated_at":               datetime.now(timezone.utc).isoformat(),
        "raw_median_sharpe":          raw_median_sr,
        "total_hypotheses_tested":    len(campaign.get("runs", [])),
        "total_variants_tested":      total_tested,
        "n_trials_used":              n_trials,
        "is_sparse_trading":          is_sparse,
        "passes_deflated_threshold":  passes_deflated,
        "promotion_threshold_raw":    0.0,
        "promotion_threshold_deflated": DSR_THRESHOLD,
        "excluded_trial_counts":      excluded,
        **dsr_result,
    }

    audit_path = run_dir / "artifacts" / "promotion_audit.yaml"
    save_yaml(audit_path, audit)
    status_str = "PASS" if passes_deflated else ("INDETERMINATE" if passes_deflated is None else "FAIL")
    print(f"⚙️  A6.2: promotion_audit.yaml written (DSR={dsr_result.get('deflated_sharpe_ratio')}, "
          f"n_trials={n_trials}, passes={status_str})")


def _route_holdout_evaluation(run_dir: Path, run_id: str) -> str:
    """
    Improvement 06: single-use holdout gate.
    1. Check campaign_data_policy.yaml — refuse if hypothesis_id already consumed.
    2. Check promotion_audit.yaml — if passes_deflated_threshold is False, terminal reject.
    3. Check holdout_result.yaml — if present and status is set, evaluate it.
    4. If holdout_result.yaml is absent, pause for human (holdout backtest must be run externally).
    """
    ARTIFACTS = run_dir / "artifacts"

    # Load hypothesis_id from promotion_audit or verdict_interpretation
    audit_path = ARTIFACTS / "promotion_audit.yaml"
    if audit_path.exists():
        audit = load_yaml(audit_path) or {}
        hyp_id = audit.get("hypothesis_id", run_id)
        passes = audit.get("passes_deflated_threshold")
    else:
        interp = load_yaml(ARTIFACTS / "verdict_interpretation.yaml") or {}
        hyp_id = interp.get("hypothesis_id", run_id)
        passes = None

    # 1. Deflated Sharpe gate (if not sparse / not indeterminate)
    if passes is False:
        print(f"\n🛑 HOLDOUT BLOCKED: promotion_audit.yaml passes_deflated_threshold=False "
              f"for {hyp_id}. DSR too low — trial count and Sharpe distribution do not support promotion.")
        return "completed_rejected"

    # 2. Single-use enforcement
    policy = load_yaml(_DATA_POLICY_PATH) or {} if _DATA_POLICY_PATH.exists() else {}
    consumed = policy.get("holdout_consumed_by", [])
    if hyp_id in consumed:
        print(f"\n🛑 HOLDOUT REFUSED: {hyp_id} has already consumed the single holdout evaluation "
              f"(found in campaign_data_policy.yaml holdout_consumed_by). "
              f"Second holdout attempt is mechanically forbidden per A6.1.")
        return "completed_rejected"

    # 3. Check if holdout_result.yaml is present
    hr_path = ARTIFACTS / "holdout_result.yaml"
    if not hr_path.exists():
        holdout_range = policy.get("holdout_range", [])
        print(f"\n⏸️  HOLDOUT: holdout_result.yaml not yet present for {hyp_id}.")
        print(f"   Holdout range: {holdout_range}")
        print(f"   Run the holdout backtest on this range, write holdout_result.yaml, "
              f"then resume the pipeline.")
        return "human_pause"

    hr = load_yaml(hr_path) or {}
    status = hr.get("status", "").lower()

    # 4. Mark holdout as consumed (regardless of pass/fail — single-use)
    policy["holdout_consumed_by"] = list(consumed) + [hyp_id]
    save_yaml(_DATA_POLICY_PATH, policy)
    print(f"⚙️  A6.1: {hyp_id} marked in holdout_consumed_by (single-use consumed).")

    if status == "pass":
        print(f"\n🏆 TERMINAL PROMOTE: holdout_result.yaml status=pass for {hyp_id}. "
              f"This is a confirmed edge (post-holdout, post-deflation).")
        return "completed_promoted"

    if status == "fail":
        print(f"\n🛑 TERMINAL REJECT: holdout_result.yaml status=fail for {hyp_id}. "
              f"Holdout failure is terminal per A6.1 — no further promotion path.")
        return "completed_rejected"

    # inconclusive
    print(f"\n⏸️  HOLDOUT INCONCLUSIVE for {hyp_id} (status={status}). Human review required.")
    return "human_pause"


def _family_names(failed_families: list) -> list:
    """
    F3/F6 (2026-07-04): failed_families is a MIXED list — dicts (post-Improvement-07
    retag, {name, evidence_window, root_cause}) or plain strings (record_pivot(), still
    live). `failed_families.count(family)` on the raw list never matches a dict entry
    against a string, so the escalate-circuit-breaker below was silently a no-op for
    every one of the six historical (dict-shaped) entries — the same class of bug F3
    fixed in _should_trigger_campaign_review, here too. Extract just the name.
    """
    return [(f.get("name") if isinstance(f, dict) else f) for f in failed_families]


def _apply_circuit_breaker(status: str, interp: dict, campaign: dict) -> str:
    """
    F6 (2026-07-04): circuit-breaker state is scoped PER hypothesis family. A global
    parameter-dimension list let stale history from one family force an unrelated
    family's very first refine attempt straight to pivot — exactly what happened to
    run_044 (FUNDING_RATE_CONTINUOUS_MEAN_REVERSION forced to pivot on its first-ever
    refine, using two 'regime_filter_er_threshold'/'er_threshold' entries left over
    from the long-closed Keltner/RSI-era families). Shared by
    determine_post_verdict_route and determine_post_campaign_review_route so both
    apply the identical fix.

    Callers MUST check for an engineering-failure diagnosis
    (root_cause.mechanism_failure == 'component_execution_error') and route to
    human_pause BEFORE calling this — that diagnosis is immune to the breaker
    entirely, not merely exempted from forcing pivot/escalate.
    """
    family = interp.get("hypothesis_family", "")

    if status == "refine":
        dim = interp.get("proposed_change_dimension", "")
        recent_dims = campaign.get("recent_parameter_dimensions_by_family", {}).get(family, [])
        if dim in recent_dims or len(recent_dims) >= 2:
            reason = (f"tried dimension '{dim}' before for family '{family}'" if dim in recent_dims
                      else f"2 parameter dimensions already tried for family '{family}' ({recent_dims})")
            print(f"⚠️  CIRCUIT BREAKER: parameter altitude exhausted ({reason}). Forcing pivot.")
            status = "pivot"

    if status == "pivot":
        failed_names = _family_names(campaign.get("failed_families", []))
        count = failed_names.count(family)
        if count >= 2:
            print(f"⚠️  CIRCUIT BREAKER: hypothesis family '{family}' exhausted "
                  f"(appeared {count}x in failed_families). Forcing escalate.")
            status = "escalate"

    return status


# A8 (K2 kernel, 2026-07-13): legacy single-enum status -> (hypothesis_verdict,
# lineage_routing) mapping, used ONLY when an artifact doesn't carry the new
# A8 fields directly (every pre-K2 run, or a circuit-breaker-forced override --
# see _resolve_verdict_fields). Preserves IDENTICAL routing to pre-K2 behavior;
# "pivot"/"escalate" map hypothesis_verdict to "kill" as the closest existing
# enum value (the legacy vocabulary never distinguished "mechanism dead" from
# "campaign routes elsewhere" -- this is a backward-compat approximation for
# OLD artifacts only, never used for a new-schema run).
_LEGACY_STATUS_TO_VERDICT_ROUTING = {
    "promote":  ("promote", None),
    "kill":     ("kill", "terminate"),
    "refine":   ("refine", "refine"),
    "pivot":    ("kill", "pivot"),
    "escalate": ("kill", "escalate"),
}


def _resolve_verdict_fields(interp: dict, original_status: str, breaker_status: str) -> tuple:
    """
    A8 (K2 kernel): resolves the (hypothesis_verdict, lineage_routing) pair a
    caller should route on, for one verdict_interpretation.yaml.

    Prefers the artifact's OWN hypothesis_verdict/lineage_routing fields (the
    new A8 schema) when present. Falls back to deriving both from the legacy
    single-enum `status` field for a not-yet-migrated (pre-K2) artifact.

    `original_status` / `breaker_status` are the status string BEFORE and
    AFTER _apply_circuit_breaker ran (callers already compute both). If the
    breaker fired (they differ), its forced value overrides `lineage_routing`
    ONLY -- the breaker's job is "route differently" (e.g. force pivot after
    repeated same-dimension refines), never "re-decide whether the mechanism
    itself is dead". An artifact-declared `hypothesis_verdict` survives a
    breaker override; only `lineage_routing` is replaced.
    """
    breaker_fired = breaker_status != original_status
    hv = interp.get("hypothesis_verdict")
    lr = interp.get("lineage_routing")

    if breaker_fired:
        mapped = _LEGACY_STATUS_TO_VERDICT_ROUTING.get(breaker_status)
        if mapped is None:
            raise ValueError(f"Unknown circuit-breaker-forced status: '{breaker_status}'")
        mapped_hv, mapped_lr = mapped
        return (hv or mapped_hv), mapped_lr

    if hv and (lr or hv == "promote"):
        return hv, lr

    mapped = _LEGACY_STATUS_TO_VERDICT_ROUTING.get(breaker_status)
    if mapped is None:
        raise ValueError(f"Unknown verdict status: '{breaker_status}'")
    return mapped


def _check_pass_rule_evaluation_conformance(path: Path, hypothesis_verdict: str,
                                             lineage_routing: str) -> list:
    """
    C7 (K2 kernel, 2026-07-13): if pass_rule_evaluation.yaml carries a BINDING
    verdict (result PASS/FAIL, with a concrete hypothesis_verdict/
    lineage_routing pair -- i.e. NOT legacy_not_evaluable/SPEC_ERROR, and NOT
    a `discretion: stage` branch), the verdict_interpreter stage's own
    resolved hypothesis_verdict/lineage_routing MUST match it exactly
    (copy-through, B4 discipline) -- a stage output that disagrees, either
    direction, is a conformance violation, never a silent overwrite (mirrors
    B8's semantic-conformance-gate precedent). Returns a list of violation
    strings (empty = conforms, or nothing binding to check against).
    """
    pre_path = path / "artifacts" / "pass_rule_evaluation.yaml"
    if not pre_path.exists():
        return []
    pre_eval = load_yaml(pre_path) or {}
    if pre_eval.get("result") not in ("PASS", "FAIL"):
        return []
    if pre_eval.get("discretion") == "stage":
        return []
    expected_hv = pre_eval.get("hypothesis_verdict")
    expected_lr = pre_eval.get("lineage_routing")
    if expected_hv is None and expected_lr is None:
        return []

    violations = []
    if expected_hv and hypothesis_verdict != expected_hv:
        violations.append(
            f"verdict_interpretation.yaml's hypothesis_verdict={hypothesis_verdict!r} "
            f"disagrees with pass_rule_evaluation.yaml's binding verdict {expected_hv!r} "
            f"(branch {pre_eval.get('statement_branch_matched')!r})"
        )
    if expected_lr and lineage_routing != expected_lr:
        violations.append(
            f"verdict_interpretation.yaml's lineage_routing={lineage_routing!r} disagrees "
            f"with pass_rule_evaluation.yaml's binding routing {expected_lr!r} "
            f"(branch {pre_eval.get('statement_branch_matched')!r})"
        )
    return violations


def _dispatch_verdict_route(path: Path, run_id: str, interp: dict, campaign: dict,
                             hypothesis_verdict: str, lineage_routing: str | None) -> str:
    """
    A8 (K2 kernel), R1 (operator ruling): the SINGLE verdict->route dispatcher,
    shared by determine_post_verdict_route and
    determine_post_campaign_review_route's continue-branch -- previously two
    independent copies of the same status->route if/elif chain (verified by
    reading both; see design note section 4 and the K2 Phase B deviations
    section for the ONE real behavioral divergence found between them,
    resolved during this consolidation).

    Callers own resolving `hypothesis_verdict`/`lineage_routing` (via
    _resolve_verdict_fields) and any pre-dispatch concerns (engineering-failure
    immunity, campaign-review-trigger check, KB-findings write, output
    verification) that only ONE of the two call sites needs -- this function
    is purely the verdict-shape -> route mapping, nothing else.

    K2 rider (2026-07-13): validates the resolved pair against the design's
    own §4 authority table BEFORE dispatching -- closes deviation 3 from the
    K2 Phase B report ("does not independently validate every pair for
    semantic coherence"). `_resolve_verdict_fields`'s pure-legacy fallback
    path (no artifact-declared hypothesis_verdict at all) always lands on
    one of these five pairs by construction, so a genuinely old-schema
    artifact is unaffected; only a NEW-schema artifact declaring an
    incoherent pair itself, or the breaker-fired branch mixing an
    artifact-declared hypothesis_verdict with a legacy-mapped
    lineage_routing (e.g. hv="refine" survives while the breaker forces
    lr="pivot"), can reach an invalid pair -- and must be caught here,
    never silently dispatched on lineage_routing alone.
    """
    valid_pairs = {
        ("kill", "terminate"), ("kill", "pivot"), ("kill", "escalate"),
        ("refine", "refine"), ("promote", None),
    }
    if (hypothesis_verdict, lineage_routing) not in valid_pairs:
        raise ValueError(
            f"Incoherent hypothesis_verdict/lineage_routing pair: "
            f"hypothesis_verdict={hypothesis_verdict!r}, lineage_routing={lineage_routing!r} "
            f"-- not one of the design's authority-table combinations "
            f"(kill+terminate, kill+pivot, kill+escalate, refine+refine, promote+null)."
        )

    if hypothesis_verdict == "promote":
        update_state(path=path, flags={"walk_forward_passed": True})
        print("\n🎯 PROVISIONAL PROMOTE: walk-forward passed. Writing promotion_audit and routing to holdout_evaluation.")
        _write_promotion_audit(path, run_id)
        return "holdout_evaluation"

    if lineage_routing == "pivot":
        return _route_pivot(path, run_id, interp, campaign)
    if lineage_routing == "escalate":
        return _route_escalate(path, run_id, interp, campaign)
    if lineage_routing == "refine":
        return _route_refine(path, run_id, interp, campaign)
    # lineage_routing == "terminate" (the only remaining possibility once
    # the valid_pairs check above has passed).
    return _route_kill(path, run_id, interp, campaign)


def determine_post_verdict_route(path: Path, run_id: str):
    interp = load_yaml(path / "artifacts" / "verdict_interpretation.yaml")
    # `status` is the new altitude-aware field; fall back to `protocol_verdict` for old runs
    status = (interp.get("status") or interp.get("protocol_verdict") or "").strip().lower()
    campaign = load_campaign_state()

    # F6 (2026-07-04): an engineering-failure diagnosis can NEVER be overridden into a
    # scientific verdict by the circuit breaker (or by anything else). Checked before
    # any breaker logic runs, using the LLM's own root_cause — not prescreen's
    # no_signal_artifact (F5c intercepts that earlier, at signal_prescreen, before
    # verdict_interpreter ever runs). This covers the case where verdict_interpreter
    # itself independently reaches an engineering diagnosis (e.g. after a full
    # backtest, not just a prescreen kill).
    root_cause = interp.get("root_cause") or {}
    if root_cause.get("mechanism_failure") == "component_execution_error":
        print("\n⚠️  F6: root_cause.mechanism_failure = component_execution_error — "
              "an engineering/component bug, not a research finding. The circuit "
              "breaker must not override this into refine/pivot/escalate/kill.")
        print(f"   supporting_evidence: {root_cause.get('supporting_evidence', '')}")
        print("   Fix the component/config, then re-run fresh. No trial or parameter-"
              "dimension slot is consumed; no family is marked failed.")
        update_state(path=path, status="paused_for_human",
                     flags={"component_execution_error_flagged": True})
        return "human_pause"

    original_status = status
    status = _apply_circuit_breaker(status, interp, campaign)

    # --- IMPROVEMENT 01: mechanism_failure routing (A1.01) ---
    # regime_misattribution must pause the pipeline before spawning any new run.
    # The instrumentation must be fixed (via regime-auditor) before the signal
    # can be re-evaluated. Per A2.3: if the auditor confirms detector is unusable,
    # the orchestrator switches to ungated-only generation.
    if root_cause.get("mechanism_failure") == "regime_misattribution":
        print("\n⚠️  IMPROVEMENT 01 — root_cause.mechanism_failure = regime_misattribution")
        print("   Regime attribution is an instrumentation problem, not a hypothesis failure.")
        print("   Pipeline paused: consult regime-auditor skill and regime_detector_report.yaml")
        print("   before spawning the next run. Per A2.3, if the detector remains unusable,")
        print("   switch to ungated-only hypothesis generation for this symbol/timeframe.")
        print("   When resolved, create artifacts/human_resolution.yaml and resume.")
        update_state(path=path, status="paused_for_human",
                     flags={"regime_misattribution_flagged": True})
        return "human_pause"

    # Phase 1.4 (docs/CAMPAIGN_PROGRAM.md): a cost-dominated kill must answer "is there
    # a system that reduces these fees?" (maker-only execution, lower-frequency
    # variant, different product, venue tier, batching); if yes, register the
    # cheap variant as a new idea. Unlike component_execution_error/
    # regime_misattribution above, this does not pause the pipeline -- it's a
    # completeness gap in the autopsy, not evidence the verdict itself is
    # untrustworthy (regime_attribution, this schema's only other "mandatory"
    # root_cause-adjacent field, has no code-side pause either -- it's enforced
    # only at the prompt/skill level, with no post-hoc check anywhere in this
    # file). A print-level nudge, mirroring the warning style (not the routing
    # behavior) of the component_execution_error/regime_misattribution blocks
    # above, rather than silently passing.
    if root_cause.get("mechanism_failure") == "signal_real_but_subscale_vs_costs" \
            and not root_cause.get("fee_reduction_assessment"):
        print("\n⚠️  Phase 1.4: root_cause.mechanism_failure = signal_real_but_subscale_vs_costs "
              "but root_cause.fee_reduction_assessment is missing.")
        print("   Mandatory: is there a system that reduces these fees (maker-only execution, "
              "lower-frequency variant, different product, venue tier, batching)? If yes, "
              "register the cheap variant as a new idea and name it in "
              "fee_reduction_assessment.registered_as.")
    # --- end mechanism_failure routing ---

    # A8 (K2 kernel): resolve the two-field pair (preferring the artifact's own
    # hypothesis_verdict/lineage_routing; legacy-status fallback + circuit-breaker
    # interaction documented in _resolve_verdict_fields).
    hypothesis_verdict, lineage_routing = _resolve_verdict_fields(interp, original_status, status)

    # C7: the stage's own verdict must not silently disagree with a BINDING
    # machine-authored pass_rule_evaluation.yaml verdict.
    _prc_violations = _check_pass_rule_evaluation_conformance(path, hypothesis_verdict, lineage_routing)
    if _prc_violations:
        print("\n🛑 [C7] STAGE OUTPUT DISAGREES WITH pass_rule_evaluation.yaml:")
        for v in _prc_violations:
            print(f"   - {v}")
        update_state(path=path, status="paused_for_human",
                     flags={"pass_rule_evaluation_disagreement": True},
                     pass_rule_evaluation_violations=_prc_violations)
        return "human_pause"

    # Short-circuit ordering UNCHANGED from pre-K2 behavior: promote and a
    # terminal kill (lineage_routing == "terminate") bypass carryover
    # generation / KB write / output verification / campaign-review-trigger,
    # exactly as the old status=="promote"/"kill" branches did.
    if hypothesis_verdict == "promote" or lineage_routing == "terminate":
        return _dispatch_verdict_route(path, run_id, interp, campaign, hypothesis_verdict, lineage_routing)

    # Auto-generate findings_carryover if missing (catches both normal and resume paths)
    _auto_generate_findings_carryover(path, interp, lineage_routing)

    # A5.1-5.3: update campaign KB with this run's verdict
    _write_kb_findings_entry(path, run_id, interp)

    # Verify verdict outputs before scaffolding the next run (not applied to terminal routes)
    violations = _verify_verdict_outputs(path)
    if violations:
        print(f"\n⚠️ VERDICT VERIFICATION FAILED ({len(violations)} issue(s)):")
        for v in violations:
            print(f"   - {v}")
        report_path = path / "artifacts" / "verdict_verification_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(violations))
        update_state(path=path, status="paused_for_human")
        print("Pipeline paused. Fix the violations above, then resume.")
        return "human_pause"

    if _should_trigger_campaign_review(load_campaign_state()):
        print(f"\n🔭 CAMPAIGN REVIEW TRIGGERED — stepping back to assess campaign direction.")
        # Ensure the run-specific handoff file exists (it's only in templates by default)
        cr_handoff = path / "handoffs" / "campaign_review.yaml"
        if not cr_handoff.exists():
            template = ROOT / "workflow_artifacts" / "templates" / "handoffs" / "campaign_review.yaml"
            cr_data = load_yaml(template)
            cr_data["run_id"] = run_id
            save_yaml(cr_handoff, cr_data)
        return "campaign_review"

    return _dispatch_verdict_route(path, run_id, interp, campaign, hypothesis_verdict, lineage_routing)


def determine_post_campaign_review_route(path: Path, run_id: str) -> str:
    review = load_yaml(path / "artifacts" / "campaign_review.yaml")
    rec = review.get("recommendation", "").strip().lower()

    # A5.4 (F09): KB-reactivation conformance gate. Any recommendation that carries a
    # next_research_question ("continue"+reframe or "reframe") is checked BEFORE
    # scaffolding a new run — a violation must not spend a trial re-testing an
    # already-answered, already-consumed reactivation. See
    # _check_kb_reactivation_conformance's docstring for the run_053 incident this
    # closes. No new run is scaffolded on a violation, same treatment as F4d's
    # prescreen conformance gate.
    _nrq_raw = review.get("next_research_question")
    if _nrq_raw and rec in ("continue", "reframe"):
        _nrq = _nrq_raw
        if isinstance(_nrq, str):
            _nrq = yaml.safe_load(_nrq)
        if isinstance(_nrq, dict) and _nrq:
            _kb = load_yaml(_KB_PATH) if _KB_PATH.exists() else {}
            _kb_violations = _check_kb_reactivation_conformance(_nrq, _kb or {})
            if _kb_violations:
                print("\n🛑 [A5.4] KB-REACTIVATION CONFORMANCE VIOLATION — this reframe "
                      "targets an already-closed KB entry:")
                for v in _kb_violations:
                    print(f"   - {v}")
                update_state(path=path, status="paused_for_human",
                             flags={"kb_reactivation_violation": True},
                             kb_reactivation_violations=_kb_violations)
                return "human_pause"

    if rec == "continue":
        # If campaign_review supplied next_research_question, honour it —
        # it overrides the verdict_interpreter's proposed_brief.yaml.
        nrq = review.get("next_research_question")
        if nrq and isinstance(nrq, dict) and len(nrq) > 0:
            import yaml as _yaml_nrq
            if isinstance(nrq, str):
                nrq = _yaml_nrq.safe_load(nrq)
            next_run_id = _next_run_id(run_id)
            _scaffold_next_run(next_run_id)
            _safe_write_new_research_brief(next_run_id, nrq)
            update_campaign_state_after_run(
                run_id=run_id, altitude="campaign", dimension="research_question",
                family="", outcome="reframed", diagnostics=_extract_diagnostics(path),
            )
            print(f"\n🔄 CAMPAIGN REVIEW (continue+reframe): next_research_question -> {next_run_id}")
            return "completed_reframed"

        # No next_research_question — true continue, defer to verdict_interpreter.
        print("\n🔭 CAMPAIGN REVIEW: continue current direction.")
        interp = load_yaml(path / "artifacts" / "verdict_interpretation.yaml")
        status = interp.get("status", "refine").strip().lower()
        campaign = load_campaign_state()

        # F6 (2026-07-04): same engineering-failure immunity as determine_post_verdict_route.
        root_cause = interp.get("root_cause") or {}
        if root_cause.get("mechanism_failure") == "component_execution_error":
            print("\n⚠️  F6: root_cause.mechanism_failure = component_execution_error — "
                  "an engineering/component bug. The circuit breaker (and campaign_review) "
                  "must not override this into refine/pivot/escalate/kill.")
            update_state(path=path, status="paused_for_human",
                         flags={"component_execution_error_flagged": True})
            return "human_pause"

        # Apply circuit-breaker overrides exactly as determine_post_verdict_route would,
        # then route via the SAME shared dispatcher (R1, K2 kernel) — but do NOT call
        # _should_trigger_campaign_review again.
        #
        # DEVIATION (K2 Phase B, found during implementation): this branch's OLD promote
        # handling was `return "completed_promoted"` directly — skipping
        # _write_promotion_audit and the holdout_evaluation gate entirely, unlike
        # determine_post_verdict_route's own promote handling. Nothing in this codebase
        # documents that divergence as intentional, and this campaign's own standing
        # doctrine treats holdout as a mandatory single-use gate every promote must pass
        # through. R1 rejects "two divergent copies"; consolidating onto the SAME
        # dispatcher necessarily picks ONE behavior, and the complete one (promotion_audit
        # + holdout_evaluation) is the only one consistent with that doctrine. Flagged
        # here and in the appended design-note section, not silently merged.
        original_status = status
        status = _apply_circuit_breaker(status, interp, campaign)
        hypothesis_verdict, lineage_routing = _resolve_verdict_fields(interp, original_status, status)

        # C7: same disagreement check as determine_post_verdict_route (R1 --
        # one shared conformance rule, not a divergent second copy).
        _prc_violations = _check_pass_rule_evaluation_conformance(path, hypothesis_verdict, lineage_routing)
        if _prc_violations:
            print("\n🛑 [C7] STAGE OUTPUT DISAGREES WITH pass_rule_evaluation.yaml:")
            for v in _prc_violations:
                print(f"   - {v}")
            update_state(path=path, status="paused_for_human",
                         flags={"pass_rule_evaluation_disagreement": True},
                         pass_rule_evaluation_violations=_prc_violations)
            return "human_pause"

        return _dispatch_verdict_route(path, run_id, interp, campaign, hypothesis_verdict, lineage_routing)

    if rec == "reframe":
        # Write the new research question as the next run's brief
        next_run_id = _next_run_id(run_id)
        _scaffold_next_run(next_run_id)
        nrq = review.get("next_research_question", {})
        if nrq:
            import yaml as _yaml
            if isinstance(nrq, str):
                nrq = _yaml.safe_load(nrq)
            _safe_write_new_research_brief(next_run_id, nrq)
        update_campaign_state_after_run(
            run_id=run_id,
            altitude="campaign",
            dimension="research_question",
            family="",
            outcome="reframed",
            diagnostics=_extract_diagnostics(path),
        )
        print(f"\n🔄 REFRAME: new research question for {next_run_id}")
        return "completed_reframed"

    if rec in ("escalate_instrument", "escalate_component"):
        # Route through the escalate helper directly (escalate is NOT a stage name).
        # Build a minimal interp dict carrying the escalation target so _route_escalate
        # knows whether to escalate instrument or component.
        interp = load_yaml(path / "artifacts" / "verdict_interpretation.yaml")
        target = "instrument" if rec == "escalate_instrument" else "new_component"
        # Ensure escalation_request.yaml exists with the right target for _route_escalate
        esc_path = path / "artifacts" / "escalation_request.yaml"
        if not esc_path.exists():
            save_yaml(esc_path, {"target": target,
                                 "reason": review.get("recommendation_rationale", "")})
        return _route_escalate(path, run_id, interp, load_campaign_state())

    if rec == "terminate":
        # A9 (K2 kernel): this is the campaign-review-EXPLICIT termination
        # decision the design note anticipated needing a new recommendation
        # value for -- on implementation, `rec == "terminate"` already existed
        # here (pre-K2) and already called the OLD, unsplit _route_kill (which
        # wrote campaign_decision.yaml + space_empty unconditionally). No new
        # recommendation value is needed: this existing "terminate" IS the
        # campaign-scope decision A9 wants isolated: it now calls
        # _route_campaign_terminate (the split-out campaign-wide half)
        # instead of the now-per-hypothesis-only _route_kill. See the
        # appended design-note section for why this differs from the
        # Phase A design (which proposed inventing "terminate_campaign").
        return _route_campaign_terminate(path, run_id, review, load_campaign_state())

    raise ValueError(f"Unknown campaign_review recommendation: {rec}")


def determine_post_spec_route(path: Path):
    KNOWN_STATUSES = {"spec_ready", "component_gap"}
    decision = load_yaml(path / "artifacts" / "decision.yaml")
    status = decision.get("status", "").strip().lower()
    if status == "spec_ready":
        # Improvement 08+09: route via signal_prescreen before full backtest
        return "signal_prescreen"
    if status == "component_gap":
        update_state(path=path, status="paused_for_human")
        print("\n⏸️ COMPONENT GAP: hypothesis needs an engine piece that does not exist. "
              "See artifacts/decision.yaml; extend the engine per STRATEGY_EXTENDING.md, then resume.")
        return "human_pause"
    if status not in KNOWN_STATUSES:
        update_state(path=path, status="paused_for_human")
        print(f"\n⏸️ UNEXPECTED STATUS '{status}' from backtest_specification — "
              f"SKILL.md may need a new status case, or this run had bad inputs. "
              f"Rationale: {decision.get('rationale', '<none>')}")
        return "human_pause"

def resume_pipeline(run_id: str):
    RUN_DIR = ROOT / "runs" / run_id
    state = load_yaml(RUN_DIR / "pipeline_state.yaml")
    if state.get("status") != "paused_for_human":
        print("Pipeline is not paused. Nothing to resume.")
        return

    resolution_path = RUN_DIR / "artifacts" / "human_resolution.yaml"
    ensure_files([resolution_path])
    
    resolution = load_yaml(resolution_path)
    if resolution.get("status") == "resolved_proceed":
        print("✅ Human resolution verified. Resuming pipeline...")
        # Inject the human's paths directly into the state so the next agent can see them
        update_state(
            path=RUN_DIR, 
            status="active",
            current_stage="human_resolution",
            pending_stage="backtest_specification", # Move to Phase 2
            injected_human_context=resolution.get("injected_context")
        )
        run_loop(run_id)
    else:
        print("❌ Human marked issue as unresolvable. Ending run.")
        update_state(path=RUN_DIR, status="rejected", pending_stage="completed_rejected")

def run_loop(run_id: str):
    """Main loop to run through the stages of Phase 1 with dynamic routing and state management.
    1- Load State from current run folder
    2- From the config (top of this file), determine the current pending stage its handoff file, required outputs, and default next stage
    3- Verify required handoff files exist before invoking the agent
    4- Run the Agent
    5- Validate required output artifacts were created
    6- Handle Dynamic Routing & Counters based on agent outputs and current state
        6.1 For validation, route to refinement if "refine", completed_rejected if "reject", or next phase if "approve"
        6.2 For refinement planner, increment a refinement counter and route back to innovation expansion
    7 -Mark completed and stage next phase
    
    """
    RUN_DIR = ROOT / "runs" / run_id
    ARTIFACTS = RUN_DIR / "artifacts"
    HANDOFFS = RUN_DIR / "handoffs"
    STATE_FILE = RUN_DIR / "pipeline_state.yaml" # Updated to your new state file
    state = load_yaml(STATE_FILE)

    # F4d: generate the protocol + run_context override from pre_registration.yaml's
    # machine_constraints, if present, BEFORE anything else runs. Idempotent.
    _machine_constraints = _load_machine_constraints(RUN_DIR)
    if _machine_constraints:
        # A4 (K3/§9): runtime mutual-exclusion guard, independent of the
        # materialization-time lint -- protects a hand-authored/hand-edited
        # pre_registration.yaml fed directly to this script (bypassing
        # run_campaign.py's materialization lint entirely, e.g. under --once/
        # direct-stage invocation).
        if _machine_constraints.get("protocol") and _machine_constraints.get("protocol_ref"):
            raise RuntimeError(
                f"[K3/A4] pre_registration.yaml's machine_constraints carries BOTH "
                f"protocol={_machine_constraints.get('protocol')!r} (generate) AND "
                f"protocol_ref={_machine_constraints.get('protocol_ref')!r} (pin) for "
                f"{run_id} -- mutually exclusive. This should have been caught by "
                f"run_campaign.py's materialization-time lint; a direct/hand-edited "
                f"invocation bypassed it. Refusing to silently pick one."
            )
        _ensure_protocol_from_constraints(RUN_DIR, run_id, _machine_constraints)
        _ensure_protocol_ref_pinned(RUN_DIR, run_id, _machine_constraints)

    while True:
        current_stage = state.get("pending_stage")
         
        TERMINAL_PREFIXES = ("completed", "rejected", "human_pause", "failed_validation")
        if not current_stage or current_stage.startswith(TERMINAL_PREFIXES):
            print(f"🏁 Pipeline finished. Final state: {current_stage}")
            break

        # --- TOKEN CIRCUIT BREAKER (F4c: weighted units, not raw token sum) ---
        budget = _load_token_budget()
        total_weighted_used, stage_breakdown = _compute_weighted_budget_usage(state.get("audit_log", {}))

        if total_weighted_used > budget:
            print(f"🛑 RUN TERMINATED: Weighted token budget exceeded "
                  f"({total_weighted_used:,.0f} > {budget:,.0f}).")
            print("   Per-stage weighted breakdown:")
            for name, w in stage_breakdown:
                print(f"     {name}: {w:,.0f}")
            update_state(path=RUN_DIR, status="rejected_budget_exceeded")
            break
        # ----------------------------------

        print(f"\n⚙️ Starting stage: {current_stage}")
        config = STAGE_CONFIGS[current_stage]
        #Each stage has Handodff YAML (inputs) / required output and default next stage
        handoff_path = HANDOFFS / config["handoff"]
        


        # 1. Verify required inputs exist before invoking the agent
        handoff_data = load_yaml(handoff_path)
        required_input_paths = [RUN_DIR / x["path"] for x in handoff_data.get("required_inputs", [])]
        ensure_files(required_input_paths)

        # 2. Update state to running
        update_state(path=RUN_DIR, current_stage=current_stage, status="running")

        try:
            # 3. Inject dynamic state directly into the run's existing handoff file
            handoff_data["run_id"] = state.get("run_id", run_id)
            
            # Create or overwrite the injected_context block with the latest dynamic info from the state (like counters or human context)
            handoff_data["injected_context"] = {
                "refinement_attempt": str(state.get("counters", {}).get("refinements_used", 0)),
                "human_data_paths_injected": "true" if state.get("injected_human_context") else "false"
            }
            if state.get("injected_human_context"): # If there is human context in the state, merge it into the injected_context for the agent to consume
                handoff_data["injected_context"].update(state.get("injected_human_context"))

            # Save it right back over the existing file
            save_yaml(handoff_path, handoff_data)

            # Skip agent invocation if artifact already exists and is valid YAML
            # (avoids re-running LLM when manually recovering from a parse error)
            _skip_agent = False
            if current_stage == "campaign_review":
                _cr_path = RUN_DIR / "artifacts" / "campaign_review.yaml"
                if _cr_path.exists():
                    try:
                        import yaml as _yaml_check
                        _yaml_check.safe_load(_cr_path.read_text(encoding="utf-8"))
                        _skip_agent = True
                        print(f"⏭️  campaign_review.yaml already valid — skipping LLM re-run.")
                    except Exception:
                        pass  # invalid YAML — re-run the agent

            # A8.6: a-priori power pre-flight — runs before the prescreen tool is invoked.
            # Also handles the validation-gate bypass case (prescreen_result.yaml already written).
            if current_stage == "signal_prescreen" and not _skip_agent:
                _ps_existing = ARTIFACTS / "prescreen_result.yaml"
                if _ps_existing.exists():
                    _ps_data = load_yaml(_ps_existing) or {}
                    if _ps_data.get("route") == "insufficient_power_a_priori":
                        print("⏭️  A8.6: prescreen_result.yaml already written (validation-gate bypass) — skipping prescreen tool.")
                        _skip_agent = True
                        # A6.2: run_tool_worker is skipped in this path; record trial here (idempotent guard)
                        _cs_check = load_campaign_state()
                        if not any(t.get("trial_id") == run_id for t in _cs_check.get("trial_sharpes", [])):
                            _record_prescreen_trial(run_id, _ps_data, ARTIFACTS / "candidate_strategy_config.json")
                if not _skip_agent:
                    _a86 = _run_a86_power_check(ARTIFACTS)
                    if _a86["verdict"] == "insufficient_power_a_priori":
                        print(f"\n⚡ A8.6: Insufficient a-priori power — skipping prescreen tool.")
                        print(f"   min_detectable_ic={_a86['min_detectable_ic']:.4f} > "
                              f"plausible_ic_upper={_a86['plausible_ic_upper']}")
                        print(f"   expected_n_eff={_a86['expected_n_eff']:.1f} "
                              f"(active_n={_a86['expected_active_n']:.0f}, "
                              f"n_eff_symbols={_a86.get('n_eff_symbols','n/a')}, rho={_a86.get('rho_bar')})")
                        print(f"   Data requirement: {_a86.get('data_requirement')}")
                        _a86_ps_data = {
                            "run_id": run_id,
                            "route": "insufficient_power_a_priori",
                            "a86_power_check": _a86,
                            "note": "A8.6 pre-flight: power insufficient before any prescreen IC computed.",
                        }
                        save_yaml(ARTIFACTS / "prescreen_result.yaml", _a86_ps_data)
                        _skip_agent = True
                        # A6.2: run_tool_worker is skipped in this path; record trial here
                        _record_prescreen_trial(run_id, _a86_ps_data, ARTIFACTS / "candidate_strategy_config.json")

            if current_stage == "verdict_interpreter":
                _vi_path = RUN_DIR / "artifacts" / "verdict_interpretation.yaml"
                if _vi_path.exists():
                    try:
                        import yaml as _yaml_check
                        _yaml_check.safe_load(_vi_path.read_text(encoding="utf-8"))
                        _skip_agent = True
                        print(f"⏭️  verdict_interpretation.yaml already valid — skipping LLM re-run.")
                    except Exception:
                        pass  # invalid YAML — re-run the agent

                # Improvement 02: ensure regime detector is fresh and inject context
                if not _skip_agent:
                    _regime_rpt = _ensure_regime_detector_report(run_id, RUN_DIR)
                    _regime_aud_path = RUN_DIR / "artifacts" / "regime_audit_decision.yaml"
                    _regime_aud = load_yaml(_regime_aud_path) if _regime_aud_path.exists() else None
                    # A2.2 retune firewall: audit output must not cite strategy metrics
                    if _regime_aud:
                        _fw_violations = _validate_retune_firewall(_regime_aud)
                        if _fw_violations:
                            raise RuntimeError(
                                "RETUNE FIREWALL VIOLATION — regime_audit_decision.yaml "
                                "references forbidden strategy metrics:\n"
                                + "\n".join(f"  - {v}" for v in _fw_violations)
                            )
                    _vi_handoff = RUN_DIR / "handoffs" / "protocol_to_verdict_interpreter.yaml"
                    _inject_regime_context_into_handoff(_vi_handoff, _regime_rpt, _regime_aud, run_id)

            # Invoke the Agent (F4b: one bounded YAML-repair retry on failure)
            expected_outputs = [RUN_DIR / "artifacts" / x for x in handoff_data.get("deliverables", [])]
            if not _skip_agent:
                if current_stage == "hypothesis_generation":
                    try:
                        _invoke_agent_with_yaml_retry(current_stage, run_id, RUN_DIR, expected_outputs, state)
                    except FileNotFoundError:
                        if not _handle_hypothesis_generation_multi_card_split(run_id, RUN_DIR):
                            raise
                else:
                    _invoke_agent_with_yaml_retry(current_stage, run_id, RUN_DIR, expected_outputs, state)
            else:
                ensure_files(expected_outputs)

            # 4b. For campaign_review: validate YAML is parseable (LLM often emits colons in list items)
            if current_stage == "campaign_review" and not _skip_agent:
                import yaml as _yaml_val
                _cr_out = RUN_DIR / "artifacts" / "campaign_review.yaml"
                try:
                    _yaml_val.safe_load(_cr_out.read_text(encoding="utf-8"))
                except Exception as _ye:
                    raise ValueError(
                        f"YAML parse error in campaign_review.yaml: {_ye}\n"
                        f"Fix the file manually and re-run to resume."
                    )

            # 5. Handle Dynamic Routing & Counters
            next_stage = config["default_next"]
            
            if current_stage == "validation":
                next_stage = determine_post_validation_route(RUN_DIR) # Used to trigger state of refinement until (Artifact State is validated OR max refinement reached OR rejected)
                
            elif current_stage == "refinement_planner":
                # Increment the refinement counter
                current_count = state.get("counters", {}).get("refinements_used", 0)
                update_state(path=RUN_DIR, counters={"refinements_used": current_count + 1})

                # Ask the new function where to go next
                next_stage = determine_post_refinement_route(RUN_DIR) #Checks if refinement requires a human pause or loops back to innovation.

                if next_stage == "human_pause":
                    break # Break the while loop to stop the script cleanly

            elif current_stage == "backtest_specification":
                next_stage = determine_post_spec_route(RUN_DIR)
                if next_stage in ("signal_prescreen", "protocol_execution"):
                    spec = load_yaml(ARTIFACTS / "backtest_spec.yaml")
                    config_obj = spec.get("config")
                    # F4d (2026-07-05, run_047): force-inject significance_methodology
                    # from pre-registered machine_constraints, regardless of whether the
                    # LLM stage remembered to carry it through from research_brief.yaml.
                    # run_047's backtest_specification silently dropped this field despite
                    # an explicit skill-file instruction — a pre-registered MANDATORY
                    # methodology must not be droppable by an LLM prompt-following miss.
                    if _machine_constraints and _machine_constraints.get("significance_methodology"):
                        config_obj["significance_methodology"] = _machine_constraints["significance_methodology"]
                    candidate_path = ARTIFACTS / "candidate_strategy_config.json"
                    with open(candidate_path, "w", encoding="utf-8") as f:
                        json.dump(config_obj, f, indent=2)
                    validator  = Path("..") / "trading-bot" / "tools" / "validate_config.py"
                    TBOT_PYTHON = _resolve_tbot_python()
                    result = subprocess.run(
                        [str(TBOT_PYTHON), str(validator), str(candidate_path)],
                        capture_output=True, text=True
                    )
                    if result.returncode != 0:
                        report = result.stdout + result.stderr
                        report_path = ARTIFACTS / "spec_validation_report.txt"
                        with open(report_path, "w", encoding="utf-8") as f:
                            f.write(report)
                        print("❌ Config schema violations found:")
                        print(report)
                        update_state(path=RUN_DIR, status="failed_validation")
                        next_stage = "failed_validation"
                    else:
                        print("✅ config schema-valid; advancing to signal_prescreen")
                        # Create handoff files for prescreen + remaining pipeline stages
                        _create_remaining_handoffs(run_id, RUN_DIR)
                elif next_stage == "human_pause":
                    break

            elif current_stage == "signal_prescreen":
                # Improvement 08+09: route based on prescreen_result.yaml
                next_stage = determine_post_prescreen_route(RUN_DIR)
                if next_stage == "verdict_interpreter":
                    # Prescreen kill — inject prescreen context into verdict handoff
                    ps = load_yaml(ARTIFACTS / "prescreen_result.yaml") or {}
                    _vi_handoff = RUN_DIR / "handoffs" / "protocol_to_verdict_interpreter.yaml"
                    _inject_prescreen_context_into_verdict_handoff(_vi_handoff, ps)
                    # Also inject regime context if available (Improvement 02)
                    _regime_rpt = _ensure_regime_detector_report(run_id, RUN_DIR)
                    _regime_aud_path = RUN_DIR / "artifacts" / "regime_audit_decision.yaml"
                    _regime_aud = load_yaml(_regime_aud_path) if _regime_aud_path.exists() else None
                    if _regime_aud:
                        _fw_violations = _validate_retune_firewall(_regime_aud)
                        if _fw_violations:
                            raise RuntimeError(
                                "RETUNE FIREWALL VIOLATION — regime_audit_decision.yaml "
                                "references forbidden strategy metrics:\n"
                                + "\n".join(f"  - {v}" for v in _fw_violations)
                            )
                    if _regime_rpt:
                        _inject_regime_context_into_handoff(_vi_handoff, _regime_rpt, _regime_aud, run_id)

            elif current_stage == "verdict_interpreter":
                _interp = load_yaml(ARTIFACTS / "verdict_interpretation.yaml")
                _auto_generate_findings_carryover(RUN_DIR, _interp)
                next_stage = determine_post_verdict_route(RUN_DIR, run_id)

            elif current_stage == "campaign_review":
                next_stage = determine_post_campaign_review_route(RUN_DIR, run_id)

            elif current_stage == "holdout_evaluation":
                # Improvement 06: tool stage — no LLM. Single-use holdout enforcement + DSR gate.
                next_stage = _route_holdout_evaluation(RUN_DIR, run_id)
                if next_stage == "human_pause":
                    update_state(path=RUN_DIR, status="paused_for_human")
                    break

            # 6. Mark completed and stage next phase
            completed = state.get("completed_stages", [])
            completed.append(current_stage)
            
            update_state(path=RUN_DIR, 
                status="active" if next_stage != "completed_rejected" else "rejected",
                completed_stages=completed,
                current_stage=current_stage,
                pending_stage=next_stage
            )
            
            # Reload state for the next while loop iteration
            state = load_yaml(STATE_FILE)

        except Exception as e:
            print(f"❌ Error in stage {current_stage}: {e}")
            update_state(path=RUN_DIR, status="failed", last_error=str(e))
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true", help="Resume from human pause")
    parser.add_argument("run_id", type=str, help="The ID for the new run (e.g., run_002)")
    args = parser.parse_args()

    if args.resume:
        resume_pipeline(args.run_id)
    else:
        run_loop(args.run_id)