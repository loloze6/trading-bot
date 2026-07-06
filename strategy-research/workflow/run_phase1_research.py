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
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from google import genai
from google.genai import types

ROOT = Path(".")
CAMPAIGN_STATE_PATH = ROOT / "campaign_state.yaml"

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

def record_escalation(target: str, detail: str, protocol_path: str = None):
    """Record a search-space escalation."""
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
        state["last_escalation"] = {"target": target, "detail": detail, "protocol_path": protocol_path}
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
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

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
        asyncio.run(async_invoke_agent(current_stage, run_id, retry_context=retry_ctx))
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

    skill_path = Path(".") / "skills" / skill_file_name / "SKILL.md"
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

    # 4. Construct the strict prompt (Combining Persona + Instructions)
    full_prompt = f"""
    PERSONA AND RULES:
    {system_prompt}
    
    YOUR HANDOFF INSTRUCTIONS:
    {yaml.dump(handoff, sort_keys=False)}
    
    YOUR PROVIDED CONTEXT FILES:
    {chr(10).join(context_blocks)}
    
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



# Initialize the Native Client
# It automatically picks up the GEMINI_API_KEY environment variable
client = genai.Client()

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
    skill_path = Path(".") / "skills" / skill_file_name / "SKILL.md"
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

    full_prompt = f"""
    YOUR HANDOFF INSTRUCTIONS:
    {yaml.dump(handoff, sort_keys=False)}

    YOUR PROVIDED CONTEXT FILES:
    {chr(10).join(context_blocks)}

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
    response = await client.aio.models.generate_content(
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
    TBOT_PYTHON = Path("..") / "venv" / "Scripts" / "python.exe"

    if stage_name == "signal_prescreen":
        # Improvement 08+09: signal prescreen — cheap IC + cost gate before full backtest.
        config_path = ARTIFACTS / "candidate_strategy_config.json"

        # Protocol selection mirrors protocol_execution logic
        run_ctx_path = ARTIFACTS / "run_context.yaml"
        run_ctx = (load_yaml(run_ctx_path) or {}) if run_ctx_path.exists() else {}
        run_type = run_ctx.get("run_type", "")
        if run_type == "replication_diagnostic":
            protocol_path = ROOT / "protocols" / "baseline_v1.json"
        elif run_type == "forced_diagnostic":
            proto_name = run_ctx.get("protocol", "baseline_v1.json")
            protocol_path = ROOT / "protocols" / proto_name
        else:
            campaign = load_campaign_state()
            last_escalation = campaign.get("last_escalation") or {}
            protocol_path_str = last_escalation.get("protocol_path")
            protocol_path = Path(protocol_path_str) if protocol_path_str else ROOT / "protocols" / "baseline_v1.json"

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
            _record_prescreen_trial(run_id, ps)
        else:
            print(f"⏭️  A6.2: trial for {run_id} already recorded — skipping duplicate.")

    elif stage_name == "protocol_execution":
        config_path     = ARTIFACTS / "candidate_strategy_config.json"
        # Protocol selection: replication_diagnostic → baseline_v1.json;
        # forced_diagnostic → protocol named in run_context.yaml; else → campaign escalation path.
        run_ctx_path = ARTIFACTS / "run_context.yaml"
        run_ctx = (load_yaml(run_ctx_path) or {}) if run_ctx_path.exists() else {}
        run_type = run_ctx.get("run_type", "")
        if run_type == "replication_diagnostic":
            print("🔁 replication_diagnostic run — ignoring last_escalation, using baseline_v1.json")
            protocol_path = ROOT / "protocols" / "baseline_v1.json"
        elif run_type == "forced_diagnostic":
            proto_name = run_ctx.get("protocol", "baseline_v1.json")
            protocol_path = ROOT / "protocols" / proto_name
            print(f"🔬 forced_diagnostic run — using protocol: {proto_name}")
        else:
            campaign = load_campaign_state()
            last_escalation = campaign.get("last_escalation") or {}
            protocol_path_str = last_escalation.get("protocol_path")
            protocol_path = Path(protocol_path_str) if protocol_path_str else ROOT / "protocols" / "baseline_v1.json"
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

        # A6.2: record full-backtest trial in campaign_state.trial_sharpes
        _record_backtest_trial(run_id, summary)

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
    status = decision.get("status").strip().lower()

    state = load_yaml(path / "pipeline_state.yaml")
    refinements_used = state.get("counters", {}).get("refinements_used", 0)
    max_refinements = state.get("governance", {}).get("max_refinements_after_validation", 2)

    if status in ("approve", "conditional_approve"):
        if status == "conditional_approve":
            conditions = decision.get("conditions", [])
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

        TBOT_PYTHON = Path("..") / "venv" / "Scripts" / "python.exe"
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


def _generate_monthly_windows(start: str, end: str) -> list:
    """[start, end) chunked into calendar-month windows, matching baseline_v1.json's
    schema: [{"label": "YYYY-MM", "test": {"start": ..., "end": ...}}, ...]."""
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
    protocol_obj = {
        "symbols": symbols,
        "timeframe": timeframe,
        "windows": windows,
        "holdout": proto_constraint.get("holdout", {"start": "2026-01-01", "end": None}),
        "promotion": proto_constraint.get("promotion", {
            "median_sharpe_gt": 0, "max_abs_drawdown_pct_lt": 30,
            "min_trade_count_gte": 20, "kill_median_sharpe_lt": -1,
        }),
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


def _next_instrument_from_universe(campaign: dict) -> dict:
    """
    Given current campaign state, return the next instrument to try from coin_universe.yaml.
    Returns: {symbol, category, timeframe} or None if all tried.
    """
    import yaml
    universe_path = ROOT / "coin_universe.yaml"
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
    universe = yaml.safe_load((ROOT / "coin_universe.yaml").read_text(encoding="utf-8"))
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
    return "completed_refined"


def _route_pivot(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    family = interp.get("hypothesis_family", "")
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
        record_escalation("instrument", next_inst["symbol"], protocol_path=str(proto_path))
        diag = _extract_diagnostics(path)
        update_campaign_state_after_run(run_id, "search_space", "instrument", "", "escalate", diag)
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
        record_escalation("timeframe", next_tf, protocol_path=str(proto_path))
        diag = _extract_diagnostics(path)
        update_campaign_state_after_run(run_id, "search_space", "timeframe", "", "escalate", diag)
        return "completed_escalated"

    elif target == "new_component":
        print("\n⏸️ ESCALATE → new component required. Pausing for human authoring.")
        update_state(path=path, status="paused_for_human")
        return "human_pause"

    else:
        raise ValueError(f"_route_escalate: unknown escalation target '{target}'")


def _route_kill(path: Path, run_id: str, interp: dict, campaign: dict) -> str:
    print("\n🛑 KILL: space exhausted or question answered negatively.")
    decision = {
        "campaign_id": campaign.get("campaign_id", "default"),
        "terminal_run": run_id,
        "decision": "kill",
        "rationale": interp.get("primary_failure_mode", "no rationale provided"),
        "altitude_justification": interp.get("altitude_justification", ""),
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


def _record_prescreen_trial(run_id: str, ps: dict):
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
    }
    trials.append(trial_entry)
    _save_campaign_state(state)
    print(f"⚙️  A6.2: prescreen trial recorded in campaign_state.trial_sharpes "
          f"(route={route}, statistic_valid=neither)")


def _record_backtest_trial(run_id: str, summary: dict):
    """
    A6.2: record a completed full-backtest as a trial in campaign_state.trial_sharpes.
    Appends {trial_id, source, sharpe, expectancy_bps, n_trades, statistic_valid}.
    Sparse-trading strategies (A3.4): statistic_valid='expectancy' when median Sharpe
    is null/unreliable; 'sharpe' otherwise.
    """
    state  = load_campaign_state()
    trials = state.setdefault("trial_sharpes", [])

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
    }
    trials.append(trial_entry)
    _save_campaign_state(state)
    print(f"⚙️  A6.2: backtest trial recorded (sharpe={median_sharpe}, "
          f"n_trades={n_trades}, statistic_valid={statistic_valid})")


# ---------------------------------------------------------------------------
# Improvement 05 — AC1/AC2: KB auto-write and derived views
# ---------------------------------------------------------------------------

_KB_PATH = ROOT / "campaign_knowledge_base.yaml"

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
    verdict_label = (interp.get("verdict_label") or interp.get("disposition") or "").lower()
    outcome = _VERDICT_TO_OUTCOME.get(verdict_label, "inconclusive")

    existing = _find_kb_entry(findings, hyp_id)

    if existing:
        runs = existing.setdefault("evidence_runs", [])
        if run_id_str not in runs:
            runs.append(run_id_str)
            existing["evidence_count"] = len(runs)
        print(f"⚙️  A5.1: KB entry for {hyp_id} updated "
              f"(evidence_count={existing['evidence_count']}, run={run_id_str})")
    else:
        ps = interp.get("prescreen_result_summary", {})
        power = interp.get("power_disposition")
        stub = {
            "id": f"{hyp_id.lower().replace('-', '_').replace('/', '_')}_auto",
            "hypothesis_id": hyp_id,
            "evidence_runs": [run_id_str] if run_id_str else [],
            "evidence_count": 1 if run_id_str else 0,
            "outcome": outcome,
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
    block_size = 24  # 1h bars per episode

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


def _auto_generate_findings_carryover(path: Path, interp: dict):
    """
    Constructs findings_carryover.yaml from verdict_interpretation.yaml when the LLM
    omitted it. Called after verdict_interpreter completes, before _verify_verdict_outputs.
    Safe to call unconditionally — skips if the file already exists.
    """
    carryover_path = path / "artifacts" / "findings_carryover.yaml"
    if carryover_path.exists():
        return

    status = (interp.get("status") or "").strip().lower()
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

    # Derive status from the artifact itself, not from any caller-supplied value.
    status = (interp.get("status") or interp.get("protocol_verdict") or "").strip().lower()

    # Universal checks (all statuses)
    if not interp.get("altitude_justification"):
        violations.append("verdict_interpretation.yaml missing altitude_justification")
    if not status:
        violations.append("verdict_interpretation.yaml missing status field")

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
    # --- end mechanism_failure routing ---

    if status == "promote":
        update_state(path=path, flags={"walk_forward_passed": True})
        print("\n🎯 PROVISIONAL PROMOTE: walk-forward passed. Writing promotion_audit and routing to holdout_evaluation.")
        _write_promotion_audit(path, run_id)
        return "holdout_evaluation"

    if status == "kill":
        return _route_kill(path, run_id, interp, campaign)

    # Auto-generate findings_carryover if missing (catches both normal and resume paths)
    _auto_generate_findings_carryover(path, interp)

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
            template = ROOT / "templates" / "handoffs" / "campaign_review.yaml"
            cr_data = load_yaml(template)
            cr_data["run_id"] = run_id
            save_yaml(cr_handoff, cr_data)
        return "campaign_review"

    if status == "refine":
        return _route_refine(path, run_id, interp, campaign)

    if status == "pivot":
        return _route_pivot(path, run_id, interp, campaign)

    if status == "escalate":
        return _route_escalate(path, run_id, interp, campaign)

    raise ValueError(f"Unknown verdict status: '{status}'")


def determine_post_campaign_review_route(path: Path, run_id: str) -> str:
    review = load_yaml(path / "artifacts" / "campaign_review.yaml")
    rec = review.get("recommendation", "").strip().lower()

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
        # then route — but do NOT call _should_trigger_campaign_review again.
        status = _apply_circuit_breaker(status, interp, campaign)
        if status == "refine":
            return _route_refine(path, run_id, interp, campaign)
        if status == "pivot":
            return _route_pivot(path, run_id, interp, campaign)
        if status == "escalate":
            return _route_escalate(path, run_id, interp, campaign)
        if status == "promote":
            return "completed_promoted"
        if status == "kill":
            return _route_kill(path, run_id, interp, campaign)
        raise ValueError(f"continue: unknown verdict status {status}")

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
        return _route_kill(path, run_id, review, load_campaign_state())

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
        _ensure_protocol_from_constraints(RUN_DIR, run_id, _machine_constraints)

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
                            _record_prescreen_trial(run_id, _ps_data)
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
                        _record_prescreen_trial(run_id, _a86_ps_data)

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
                    TBOT_PYTHON = Path("..") / "venv" / "Scripts" / "python.exe"
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