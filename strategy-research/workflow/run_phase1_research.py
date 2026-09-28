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
import contextlib
import os
import re
import asyncio
import tempfile
import time
import subprocess
import json
import sys
import shutil
import math
import statistics
import hashlib
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock
from google import genai
from google.genai import types

# CUL-213: the ~130 emoji status prints below crash on a Windows cp1252 console
# (UnicodeEncodeError) the moment stdout is redirected/piped/logged — exactly an
# unattended campaign run. Degrade unencodable glyphs to '?' rather than raising.
# Same fix as setup_run.py (CUL-12). Guarded: pytest's captured stdout has no
# .reconfigure, and a stream may reject it (OSError) — never crash a context the
# raw prints already survived. getattr because typeshed types sys.stdout as
# TextIO, which does not declare reconfigure (present on the real TextIOWrapper
# since 3.7).
_reconfigure = getattr(sys.stdout, "reconfigure", None)
if _reconfigure is not None:
    with contextlib.suppress(OSError):
        _reconfigure(errors="replace")

# CUL-11: opt-in workflow-artifact schema validation (warn-by-default, exception-proof).
# Reuses the shared tools/ helper so save_yaml/load_yaml validate against
# workflow_artifacts/schemas/{stem}.schema.json when one exists.
_tools_dir = str(Path(__file__).resolve().parent.parent / "tools")
if _tools_dir not in sys.path:
    sys.path.insert(0, _tools_dir)
try:
    from workflow_artifact_validation import validate_workflow_artifact
except Exception:  # helper unimportable -> validation is a no-op, never break the pipeline

    def validate_workflow_artifact(path, data):  # type: ignore[misc]
        return


ROOT = Path(".")
CAMPAIGN_STATE_PATH = ROOT / "campaign_record" / "campaign_state.yaml"

# E-054 Layer 2 (2026-09-11): data-availability gate. Originally shipped
# off-by-default via an env var. delivery_plan_v26.md s:0.4 item 14
# (2026-09-20) flipped this to ON by default -- see
# _data_availability_gate_enabled() below for the flag itself and why it is
# the one exception to this file's usual off-by-default convention.
# backtest_specification routes through the new "data_availability_gate"
# tool stage first (see its STAGE_CONFIGS entry and run_tool_worker branch
# below) before protocol_execution ever runs, unless explicitly disabled in
# config/campaign_config.yaml.


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
        "skill": "hypothesis-design",
    },
    # E-056 Slice 3b (config-direct authoring, orchestrator.config_direct_authoring.enabled):
    # registered UNCONDITIONALLY (same pattern as data_availability_gate's own addition --
    # strategy-research/CLAUDE.md's stage-count note documents this convention) but only
    # ROUTED to when the flag is on -- see run_loop's hypothesis_generation override. Sits
    # between hypothesis_generation and innovation_expansion in this flow: it authors the BASE
    # config innovation_expansion then patches into variants, reversing backtest-engineering's
    # old post-expansion position.
    "strategy_config_authoring": {
        "handoff": "hypothesis_to_strategy_config_authoring.yaml",
        "default_next": "innovation_expansion",
        "skill": "strategy-config-authoring",
    },
    "innovation_expansion": {
        "handoff": "hypothesis_to_innovation_expansion.yaml",
        # "required_outputs": [
        #     ARTIFACTS / "expanded_hypothesis_card.yaml",
        #     ARTIFACTS / "innovation_notes.yaml",
        # ],
        "default_next": "validation",
        "skill": "innovation-expansion",
    },
    "validation": {
        "handoff": "innovation_expansion_to_validation.yaml",
        # "required_outputs": [
        #     ARTIFACTS / "validation_protocol.yaml",
        #     ARTIFACTS / "validation_decision.yaml",
        # ],
        # E-039 S4 (2026-09-12): "refinement_planner" retired as a separate
        # stage -- this same call now also produces refinement_notes.yaml
        # (an additive, conditional deliverable) when its own verdict is
        # "refine", instead of handing off to a second LLM stage to do that.
        "default_next": "dynamic_routing", # Validation decides the next step
        "skill": "quant-validation",
    },
    "backtest_specification": {
        "handoff": "validation_to_backtest_specification.yaml",
        "default_next": "dynamic_routing",
        "skill": "backtest-engineering",
    },
    # E-054 Layer 2 (2026-09-11): pre-backtest data-availability gate (tool,
    # no LLM). ON by default -- see _data_availability_gate_enabled() below;
    # the entry exists in the registry unconditionally (Decision A: a real
    # pipeline stage, not an inline check) and is ROUTED to unless explicitly
    # disabled in config/campaign_config.yaml (delivery_plan_v26.md s:0.4
    # item 14, 2026-09-20).
    "data_availability_gate": {
        "handoff": "backtest_spec_to_data_availability_gate.yaml",
        "default_next": "dynamic_routing",
    },
    "protocol_execution": {
        "handoff": "backtest_spec_to_protocol_execution.yaml",
        "default_next": "verdict_interpreter",
    },
    "verdict_interpreter": {
        "handoff": "protocol_to_verdict_interpreter.yaml",
        "default_next": "dynamic_routing",
        "skill": "verdict-interpreter",
    },
    # E-046a Slice 5b-ii-B (orchestrator.specialist_readers.enabled, off by default):
    # registered UNCONDITIONALLY (same convention as strategy_config_authoring above) but
    # only ROUTED to when the flag is on -- see run_loop's protocol_execution override.
    # Runs the five reader skills (workflow_artifacts/skills/readers/<category>-reader/)
    # one after another; each writes artifacts/proposals/<category>.yaml. No "skill" key:
    # this stage is 1:5, not 1:1, so it never goes through _SKILL_MAP -- see
    # _run_specialist_readers. Under the flag verdict_interpreter above is unreached (not
    # deleted), and the post-run route comes from the grid (idea_status.yaml), never from
    # the readers' proposals -- see determine_post_specialist_readers_route.
    "specialist_readers": {
        "handoff": "protocol_to_specialist_readers.yaml",
        "default_next": "dynamic_routing",
    },
    # E-058 S2a (orchestrator.regroup_record.enabled, off by default; requires
    # specialist_readers): registered UNCONDITIONALLY, same convention as
    # specialist_readers above, but only ROUTED to when the flag is on -- then it sits
    # between specialist_readers and determine_post_specialist_readers_route ("memory
    # before decision", roadmap card H). A tool stage, no LLM and no "skill" key: it
    # writes one entry per run to campaign_record/campaign_memory.yaml
    # (tools/campaign_memory.py) and writes no trial rows -- see _run_regroup_record_stage.
    "regroup_record": {
        "handoff": "specialist_readers_to_regroup_record.yaml",
        "default_next": "dynamic_routing",
    },
    "campaign_review": {
        "handoff": "campaign_review.yaml",
        "default_next": "dynamic_routing",
        "skill": "campaign-review",
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
    except yaml.YAMLError:
        # Second pass: iterative repair (handles LLM colon/multi-doc errors)
        repaired = _repair_yaml(content, source=Path(path).name)
        docs = list(yaml.safe_load_all(repaired))
    result = docs[0] if docs else None
    # CUL-11: opt-in read-side schema check — catches drift in LLM-authored artifacts
    # (which have no Python writer) when the orchestrator reads them back.
    if result is not None:
        validate_workflow_artifact(path, result)
    return result

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
    # CUL-11: opt-in write-side schema check. Warn-by-default (no-op if no schema for
    # path.stem); under WORKFLOW_ARTIFACT_VALIDATION=raise a violation blocks the write.
    validate_workflow_artifact(path, data)
    _atomic_write_bytes(path, _yaml_file_bytes(data))


def _yaml_file_bytes(data) -> bytes:
    """The exact bytes save_yaml has always written: yaml.safe_dump as a
    text-mode file writes it (newline=None: "\\n" -> os.linesep, UTF-8)."""
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    return text.replace("\n", os.linesep).encode("utf-8")


_ANY_BYTES = object()


def _atomic_write_bytes(path: Path, data: bytes, *, durable: bool = False,
                        expect=_ANY_BYTES) -> bool:
    """Temp file in the destination's own directory, then os.replace (atomic
    on POSIX and Windows): readers see the old or the new content, never a
    partial one, and a failure at any point leaves the original in place.

    durable=True (CUL-331, the holdout consume marker) also fsyncs the temp
    file before the replace, copies the existing file's mode onto it (mkstemp
    creates 0600), and on POSIX fsyncs the directory after the replace so the
    rename itself survives a crash (skipped on Windows, where a directory
    cannot be opened for fsync).

    expect: when given, the replace happens only if the file's current bytes
    (None = no file) still equal it; otherwise the temp file is removed and
    False is returned, for the caller to re-read and re-apply. True once
    written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            if durable:
                f.flush()
                os.fsync(f.fileno())
        if durable and path.exists():
            with contextlib.suppress(OSError):
                shutil.copymode(path, tmp_name)
        if expect is not _ANY_BYTES:
            current = path.read_bytes() if path.exists() else None
            if current != expect:
                os.unlink(tmp_name)
                return False
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
    if durable and os.name != "nt":
        with contextlib.suppress(OSError):
            dir_fd = os.open(str(path.parent), os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
    return True

def update_state(path: Path, **kwargs):
    # NOT `or {}`, tried and reverted 2026-08-18. Verified by execution, since two
    # earlier attempts to describe this path from reading were both wrong:
    #   * load_yaml on an empty-but-present pipeline_state.yaml returns None, and the
    #     subscript below then raises TypeError. (Confirmed directly.)
    #   * run_loop reads the same file unguarded at its top and uses it immediately,
    #     so on that path it fails there first, before entering its own try — the
    #     exception escapes run_loop and process_once either way and leaves the queue
    #     entry `in_progress`. That outcome is verified; do not re-describe the route
    #     without re-running it.
    # Defaulting to {} looks like the fix and is worse: this function then writes
    # `audit_log: {}`, which zeroes _compute_weighted_budget_usage and silently hands
    # the run its full weighted token budget again — a loud crash traded for a
    # flattering, invisible one. The escape is real but pre-existing and shared by
    # every caller; it wants its own fix (atomic writes on the save side) rather than
    # a default here that launders corrupt state into plausible state.
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

# Stage -> SKILL.md directory mapping. Module-level (not nested in
# run_claude_worker) so _build_stage_prompt can share it without duplication.
_SKILL_MAP = {
    "hypothesis_generation": "hypothesis-design",
    "strategy_config_authoring": "strategy-config-authoring",  # E-056 Slice 3b, config-direct-authoring flow only
    "innovation_expansion": "innovation-expansion",
    "validation": "quant-validation",
    "backtest_specification": "backtest-engineering",
    "verdict_interpreter": "verdict-interpreter",
    "campaign_review": "campaign-review",
}


def _build_stage_prompt(stage_name: str, handoff: dict, path: Path,
                         retry_context: str | None = None,
                         skill_file_name: str | None = None) -> str:
    """Pure function: assembles the exact prompt text run_claude_worker sends
    to the model. Extracted (2026-08-23, E-032 S2a) so tests can assert on
    the fully-assembled prompt -- including the exclusion-digest
    required_input's flag-off/flag-on byte-identity proof -- WITHOUT
    invoking the agent SDK / spending any tokens. No behavior change: this
    is the same code that used to live inline in run_claude_worker, moved
    verbatim.

    `skill_file_name` (E-046a Slice 5b-ii-B): an explicit skill directory
    under workflow_artifacts/skills/, used instead of the _SKILL_MAP lookup.
    Only the specialist_readers stage passes it (one stage, five skills --
    _SKILL_MAP is strictly 1:1). Omitted by every other caller, so their
    prompts are unchanged."""
    if skill_file_name is None:
        skill_file_name = _SKILL_MAP.get(stage_name)
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
        else:
            # E-032 S2b: an optional_input that never resolves used to vanish with
            # zero trace -- exactly how research_brief_to_hypothesis.yaml's
            # campaign_knowledge_base.yaml entry stayed silently broken for the
            # pipeline's whole life (a stale path from before the E-002 restructure,
            # 8f162fa6, moved several top-level artifacts under campaign_record/ --
            # see EPIC.md's S2a review and this story's Log entry). Diagnostic only:
            # this print does not touch context_blocks/full_prompt, so it cannot
            # change what a stage receives -- a correctly-configured, normally-absent
            # optional input (e.g. artifacts/refinement_notes.yaml outside a
            # refinement loop) still triggers it and that is expected/benign; the
            # value is catching a path that is ALWAYS missing, run after run.
            print(f"⚠️ WARNING: optional_input never resolved, stage continues "
                  f"without it: {req['path']} (stage={stage_name})")

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

    return full_prompt


# The model every Claude stage runs on (run_claude_worker and, E-046a 5b-ii-B,
# run_reader_worker) -- one constant so the two paths cannot drift.
_CLAUDE_WORKER_MODEL = "claude-haiku-4-5"

# CUL-336: see _stage_agent_options.
_STAGE_AGENT_CWD = Path(tempfile.gettempdir()) / "strategy_research_stage_agent_cwd"
_DISABLE_AUTO_MEMORY_ENV = "CLAUDE_CODE_DISABLE_AUTO_MEMORY"


def _stage_agent_options() -> ClaudeAgentOptions:
    """CUL-336 (2026-09-27): the options every Claude stage agent runs with.
    run_claude_worker and _invoke_reader_llm both call this, and it is the
    only ClaudeAgentOptions(...) construction in this module
    (tests/test_cul336_closed_book_stages.py pins both), so the two paths
    cannot drift.

    Closed-book: the agent sees only its prompt (skill + handoff + the
    handoff's input files pasted as text) and can open nothing itself. Read
    from the installed claude_agent_sdk==0.2.82, not assumed:
      - tools=[] -> `--tools ""`: no built-in tool exists. Before CUL-336 only
        allowed_tools=[] was passed, which sends no flag at all (it lists the
        tools that run WITHOUT ASKING; it does not limit which tools exist),
        so every stage had the CLI's default tool set, and a run_060
        validation agent Read two config files on its own
        (engineering/roadmap/E-035/S1_FINDINGS.md section 1.2).
      - setting_sources=[] -> `--setting-sources=`: no user/project/local
        settings file loads, so no machine's permission allow rules apply and
        no CLAUDE.md is loaded (the SDK loads CLAUDE.md only with "project").
      - strict_mcp_config=True -> `--strict-mcp-config`: no MCP server from
        any config file. MCP tools are not built-in tools, so tools=[] alone
        does not remove them; 4 of the 5 retained SDK stage transcripts list
        claude.ai Slack tools among the agent's deferred tools.
      - env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 (merged by the SDK on top of
        the inherited environment, not replacing it): the bundled CLI
        (2.1.142) loads the auto-memory MEMORY.md behind its own gate, which
        reads this env var, the settings key autoMemoryEnabled (absent once
        no settings file loads, so the default -- ON -- applies) and feature
        flags; it is NOT behind --setting-sources the way project CLAUDE.md
        files are. Its path is keyed on the git root of the cwd, so a stage
        launched from strategy-research/ would load the operator's own
        session memory for this repository.
      - cwd=_STAGE_AGENT_CWD, a neutral empty directory in the system temp
        dir, outside any repository: no git root, so no repo-keyed memory,
        and nothing to find even if a file tool ever came back. Nothing in a
        stage depends on the agent's cwd -- the prompt (skill, handoff,
        inputs) is assembled in this process from this process's own cwd.
        One fixed directory rather than one per call: the CLI files each
        session's transcript under ~/.claude/projects/<cwd key>/, and a
        fresh directory per call would scatter one folder per stage call.
      - max_turns is left unset on purpose: with no tool there is no
        tool-result round trip, so a stage is one turn by construction, and
        the audit log's num_turns shows it. A cap would only add a new
        failure mode (the CLI's max-turns error result) on top of that.
      - allowed_tools is left at its default ([]): it never removed a tool
        (tools=[] does) and passing it changes no CLI argument.
    A fresh object per call: ClaudeAgentOptions is a mutable dataclass.
    What a stage needs to read reaches it through its handoff (see
    _apply_closed_book_inputs), never through a tool."""
    _STAGE_AGENT_CWD.mkdir(parents=True, exist_ok=True)
    return ClaudeAgentOptions(
        model=_CLAUDE_WORKER_MODEL,
        tools=[],  # the option that removes tools: --tools ""
        setting_sources=[],
        strict_mcp_config=True,
        env={_DISABLE_AUTO_MEMORY_ENV: "1"},
        cwd=str(_STAGE_AGENT_CWD),
    )


def _usage_token_record(usage: dict) -> dict:
    """The audit_log `tokens` block for one SDK `usage` dict: raw counts, total,
    and the F4c weighted units the budget breaker sums. Shared by
    run_claude_worker and run_reader_worker (E-046a 5b-ii-B)."""
    usage = usage or {}
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    cache_read = usage.get("cache_read_input_tokens", 0)
    cache_creation = usage.get("cache_creation_input_tokens", 0)
    return {
        "input": input_tokens,
        "output": output_tokens,
        "cache_read": cache_read,
        "cache_creation": cache_creation,
        "total": input_tokens + output_tokens + cache_read + cache_creation,
        "weighted": round(_weighted_token_units(
            input_tokens, output_tokens, cache_read, cache_creation), 1),
    }


async def run_claude_worker(stage_name: str, handoff: str, path: Path, retry_context: str | None = None):

    print(f"\n🧠 [AGENT INVOKED] Waking up specialist for: {stage_name}"
          + (" (YAML-repair retry)" if retry_context else ""))

    full_prompt = _build_stage_prompt(stage_name, handoff, path, retry_context=retry_context)

    # --- PRE-FLIGHT SAFETY RADAR ---
    start_time = time.time()
    # check_context_limits(stage_name, full_prompt, max_window=150000)

    # 5. Invoke the Agent and Stream the Response (with strict tool constraints to enforce handoff rules)
    print("⏳ Waiting for Claude CLI response...")
    agent_output = ""
    exact_usage = {}
    total_cost = 0.0
    num_turns = None

    # CUL-336: closed-book -- no tools, no settings files, no MCP servers
    # (see _stage_agent_options). The handoff's inputs are the only context.
    async for message in query(
        prompt=full_prompt,
        options=_stage_agent_options()
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

    # F4c (2026-07-05, run_047 budget investigation): the SDK's `usage` on the
    # final ResultMessage is CUMULATIVE FOR THE SESSION (see claude_agent_sdk
    # types.py: "Cumulative API usage for the session"), i.e. across every
    # internal turn (`num_turns`) the model took to produce this stage's
    # deliverable — not a single-call snapshot. A stage that needed several
    # internal turns will show a much larger token count than its final
    # deliverable's file size would suggest; num_turns is what makes that
    # attributable at a glance instead of looking like unexplained bloat.
    # (E-046a 5b-ii-B: extracted into _usage_token_record, shared with
    # run_reader_worker so both paths weight tokens identically.)
    _tok = _usage_token_record(exact_usage)
    input_tokens, output_tokens = _tok["input"], _tok["output"]
    cache_read, cache_creation = _tok["cache_read"], _tok["cache_creation"]
    total_tokens, weighted_units = _tok["total"], _tok["weighted"]

    print(f"⏱️ Finished in {execution_time}s")
    print(f"💰 Cost Estimate: ${total_cost:.4f} | Tokens: {total_tokens:,} (Cache Read: {cache_read:,}) "
          f"| Weighted: {weighted_units:,} | Turns: {num_turns}")

    # 4. Save to the central audit ledger
    # E-030 S1.5 Piece 2 (RUNBOOK.md section 4.5's known crash-resume overwrite):
    # keyed on injected_context["stage_attempt"] (per-stage entry count, independent
    # of the refinement-budget cycle), not the OLD "refinement_attempt" key -- see
    # run_loop's own comment at the increment site for why the two happen to
    # coincide on the non-crash path and diverge only on a genuine crash-resume.
    attempt_num = handoff.get('injected_context', {}).get('stage_attempt', '0')
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
    skill_file_name = STAGE_CONFIGS[stage_name].get("skill")
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
    # E-030 S1.5 Piece 2 (RUNBOOK.md section 4.5's known crash-resume overwrite):
    # keyed on injected_context["stage_attempt"] (per-stage entry count, independent
    # of the refinement-budget cycle), not the OLD "refinement_attempt" key -- see
    # run_loop's own comment at the increment site for why the two happen to
    # coincide on the non-crash path and diverge only on a genuine crash-resume.
    attempt_num = handoff.get('injected_context', {}).get('stage_attempt', '0')
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
            # E-039 S4 (2026-09-12): third entry is conditional -- present
            # only when this call's own verdict is "refine" (refinement_planner
            # retired as a separate stage; this same response now produces its
            # plan directly). A 2-block approve/reject response is unaffected:
            # the block-matching loop below only consumes as many names as
            # blocks actually exist.
            "validation": ["validation_protocol.yaml", "validation_decision.yaml", "refinement_notes.yaml"],
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

def _validation_protocol_args(validation_path: Path) -> list:
    """E-061 C1.3 (review A2): the validation-protocol arguments of a
    run_protocol.py call. Config-direct authoring never writes
    validation_protocol.yaml: under it the `--validation-protocol <path>` pair
    is passed only when the file exists, else `--diagnostics-only` (the
    diagnostics block with no rule set and no verdict, G14). Passing the missing
    path used to spend every window's data and then fail the variant. Flag off:
    the pair is always passed, exactly as before (the legacy flow's handoff
    requires the file); `--diagnostics-only` never is."""
    if validation_path.exists() or not _config_direct_authoring_enabled():
        return ["--validation-protocol", str(validation_path)]
    return ["--diagnostics-only"]


def _legacy_verdict_args() -> list:
    """C5.6 (D-043) review fix 2: `--legacy-verdict-retired` when a protocol's
    promotion block decides nothing (_promotion_retired_enabled:
    config_direct_authoring AND verdict_routing_retired) -- run_protocol.py
    then records its legacy top-level verdict as null and reads no promotion
    block. Otherwise nothing is added: run_protocol.py computes that verdict
    from the protocol's block, and refuses a missing/empty/partial block
    before any backtest."""
    return ["--legacy-verdict-retired"] if _promotion_retired_enabled() else []


import protocol_refusal as _protocol_refusal  # noqa: E402  (tools/: one definition)
import holdout_policy as _holdout_policy  # noqa: E402  (tools/: CUL-339, the ONE strict holdout_range parser)


class _RefusedBeforeAnyBacktest(RuntimeError):
    """run_protocol.py refused before any window ran: no data touched, no trial row."""


def _window_results(out_dir: Path) -> set:
    """The window result dirs run_protocol.py has written under `out_dir`/results."""
    results = Path(out_dir) / "results"
    return {p.name for p in results.iterdir()} if results.is_dir() else set()


def _refused_before_any_backtest(result, windows_before: set, out_dir: Path) -> bool:
    """E-061 C1.3: run_protocol.py refused before any window ran (e.g. an unusable
    validation protocol) -- no market data was touched, so no trial row. All
    three are required: exit EXIT_NO_DATA_TOUCHED, the token opening the FIRST
    line of stderr, and no window result written under `out_dir` by this call.
    Anything else is a real (data-touching) failure and keeps its
    failed-backtest trial row."""
    return (result.returncode == _protocol_refusal.EXIT_NO_DATA_TOUCHED
            and _protocol_refusal.stderr_declares_no_data_touched(
                getattr(result, "stderr", None))
            and not (_window_results(out_dir) - windows_before))


async def run_tool_worker(stage_name: str, run_id: str):
    """Executes a deterministic tool stage. No LLM call. No token cost."""
    RUN_DIR = ROOT / "runs" / run_id
    ARTIFACTS = RUN_DIR / "artifacts"
    TBOT_PYTHON = _resolve_tbot_python()

    # E-046a Slice 5b-ii-B (code-review fix 1): under specialist_readers every
    # grid/report/proposal artifact must come from THIS protocol_execution
    # attempt. A re-run (the RUNBOOK's recovery path) would otherwise route on
    # the previous attempt's idea_status.yaml and skip readers whose stale
    # proposals already exist. Flag off: nothing is deleted.
    _sr_on = stage_name == "protocol_execution" and _specialist_readers_enabled()
    if _sr_on:
        _clear_specialist_readers_artifacts(RUN_DIR)
    # Branch 3 on every backtest (code review 2026-09-24): the per-variant profit
    # evaluation must come from THIS attempt too -- a stale one from a previous
    # attempt would otherwise be recorded / routed on. Flag off: nothing deleted.
    if stage_name == "protocol_execution" and _profit_bars_every_backtest_enabled():
        _stale_pbe = ARTIFACTS / _PROFIT_BARS_EVALUATION_FILE
        if _stale_pbe.exists():
            _stale_pbe.unlink()
            print(f"🧹 [branch 3] protocol_execution re-run: cleared previous attempt's "
                  f"{_PROFIT_BARS_EVALUATION_FILE}")

    if stage_name == "data_availability_gate" and _variant_loop_enabled():
        # E-033.1 Slice 4b (delivery_plan_v26.md Slice 4, sub-slice 2 of 2:
        # "data gate + conformance + grid/promotion wiring"). Per the
        # operator's 2026-09-22 decision (S1_FINDINGS.md "Decision" section):
        # every workflow control runs independently PER VARIANT -- each
        # validated variant in artifacts/variants/index.yaml gets its OWN
        # data_availability_gate.py call, its OWN refine/decline outcome,
        # its OWN not_tested marking -- never one shared gate result applied
        # to all three. Mirrors Slice 4a's own protocol_execution per-variant
        # loop (continue-on-error, per-variant output dirs under
        # RUN_DIR/variants/<variant_id>/): a crash or a decline on ONE
        # variant must not stop the others from being gated.
        index_path = ARTIFACTS / "variants" / "index.yaml"
        index_doc = load_yaml(index_path) or {}
        variants_idx = index_doc.get("variants", {})
        validated = {vid: v for vid, v in variants_idx.items() if v.get("status") == "validated"}
        if not validated:
            # Same defensive rationale as protocol_execution's own per-variant
            # loop (S1_FINDINGS.md §3a code-review note): routing already
            # refuses to reach this stage with zero validated variants, but
            # this branch must never silently trust that -- raise loudly
            # instead of iterating over nothing. Checked BEFORE resolving the
            # protocol path (mirrors protocol_execution's own ordering) so a
            # zero-variant race/staleness case fails on ITS OWN message, not
            # on an unrelated protocol-resolution error.
            raise RuntimeError(
                f"run_tool_worker(data_availability_gate): no validated variants found in "
                f"{index_path} for {run_id} -- refusing to run an empty gate loop."
            )

        protocol_path = _resolve_protocol_path(RUN_DIR, run_id)
        data_requests: list = []
        for variant_id in sorted(validated):
            vinfo = validated[variant_id]
            _config_path_val = vinfo.get("config_path")
            if not _config_path_val:
                reason = (f"variant '{variant_id}' is 'validated' in index.yaml but has no "
                          "'config_path' -- refusing to guess a path")
                variants_idx[variant_id] = {**vinfo, "status": "not_tested", "reason": reason}
                data_requests.append({"variant_id": variant_id, "outcome": "error", "reason": reason})
                print(f"⚠️  data_availability_gate: variant '{variant_id}' has no config_path "
                      "in index.yaml; continuing with remaining variants.")
                continue

            variant_config_path = RUN_DIR / _config_path_val
            variant_out_dir = RUN_DIR / "variants" / variant_id / "data_availability"
            cmd = [
                str(TBOT_PYTHON), str(ROOT / "tools" / "data_availability_gate.py"),
                str(variant_config_path), str(protocol_path),
                "--run-id", run_id,
                "--out-dir", str(variant_out_dir),
            ]
            print(f"🗂️  data_availability_gate: variant '{variant_id}'...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            # Exit codes (data_availability_gate.py's own convention):
            # 0=validate, 2=decline, 3=refine. A non-{0,2,3} code is a
            # genuine crash of the tool itself -- unlike the flag-off
            # single-gate branch below (which still raises loud, since a
            # tool crash there has no sibling variant to fall back to), a
            # per-variant crash here is recorded as this variant's own
            # not_tested outcome and the loop continues, same isolation
            # principle as protocol_execution's own per-variant loop.
            if result.returncode not in (0, 2, 3):
                reason = f"data_availability_gate.py crashed (exit {result.returncode}): {result.stderr}"
                variants_idx[variant_id] = {**vinfo, "status": "not_tested", "reason": reason}
                data_requests.append({"variant_id": variant_id, "outcome": "error", "reason": reason})
                print(f"⚠️  data_availability_gate: variant '{variant_id}' tool crashed "
                      f"(exit {result.returncode}); marking not_tested, continuing with "
                      "remaining variants.")
                continue

            gate_path = variant_out_dir / "data_availability_gate.yaml"
            if not gate_path.exists():
                reason = f"data_availability_gate.yaml not found after gate run for variant '{variant_id}'"
                variants_idx[variant_id] = {**vinfo, "status": "not_tested", "reason": reason}
                data_requests.append({"variant_id": variant_id, "outcome": "error", "reason": reason})
                print(f"⚠️  data_availability_gate: variant '{variant_id}' produced no "
                      "data_availability_gate.yaml; marking not_tested, continuing with "
                      "remaining variants.")
                continue

            variant_artifacts_dir = ARTIFACTS / "variants" / variant_id
            variant_artifacts_dir.mkdir(parents=True, exist_ok=True)
            # CODE-REVIEW FIX (2026-09-22): shutil is already imported at
            # module scope -- no need for a redundant local import repeated
            # once per validated variant per run.
            shutil.copy(gate_path, variant_artifacts_dir / "data_availability_gate.yaml")
            gate_result = load_yaml(variant_artifacts_dir / "data_availability_gate.yaml") or {}
            outcome = gate_result.get("outcome", "unknown")
            print(f"✅ data_availability_gate: variant '{variant_id}' outcome: {outcome.upper()}")

            if outcome == "validate":
                pass  # variants_idx[variant_id] left untouched (stays
                      # "validated") -- this variant proceeds to protocol_execution.
            else:
                # CODE-REVIEW FIX (2026-09-22): previously only "refine" and
                # "decline" were handled here, so an "unknown" (or any other
                # malformed/missing) outcome silently fell through and left
                # the variant as "validated" -- proceeding to a real
                # backtest despite the gate never actually validating the
                # data. This is the opposite of the sibling flag-off routing
                # branch (`gate.get("outcome", "decline")` -- fails CLOSED
                # on a missing key) and of this codebase's own "fail loud,
                # not flattering" rule. Any outcome that isn't the literal
                # string "validate" now marks the variant not_tested.
                reasons = gate_result.get("reasons", [])
                reason = f"data_availability_gate outcome={outcome}: " + "; ".join(reasons[:10])
                variants_idx[variant_id] = {**vinfo, "status": "not_tested", "reason": reason}
                data_requests.append({
                    "variant_id": variant_id, "outcome": outcome,
                    "reason": reason, "reasons": reasons,
                })

        save_yaml(index_path, {"variants": variants_idx})
        if data_requests:
            # campaign_record/data_requests.yaml -- new file, no existing
            # precedent (S1_FINDINGS.md §8); shape mirrors the sibling
            # campaign_record/component_requests.yaml written by Slice 3b's
            # own backtest_specification branch above (:1797-1803): a flat,
            # append-only "requests" list, each row stamped with run_id and
            # stage so multiple runs/stages can share one file.
            # Slice 6c S2c review fix 7: under verdict_routing_retired a parked
            # run re-runs this gate on --unpark; no duplicate rows then.
            _append_data_requests(run_id, data_requests,
                                  **({"dedupe": True} if _verdict_routing_retired_enabled() else {}))

        remaining = sum(1 for v in variants_idx.values() if v.get("status") == "validated")
        print(f"✅ data_availability_gate (variant loop): {remaining}/{len(validated)} "
              f"variant(s) remain validated after gating")

    elif stage_name == "data_availability_gate":
        # E-054 Layer 2: real per-window/per-feed data-touch check, BEFORE the
        # (much more expensive) protocol_execution stage ever runs. Uses the
        # SAME shared resolver protocol_execution uses below, so it checks
        # the literal protocol that will execute — never a hypothesis-level
        # declared timeframe (E-054 Phase 1 characterization's Q3 finding:
        # those can silently diverge).
        config_path = ARTIFACTS / "candidate_strategy_config.json"
        protocol_path = _resolve_protocol_path(RUN_DIR, run_id)

        out_dir = RUN_DIR / "data_availability"
        cmd = [
            str(TBOT_PYTHON), str(ROOT / "tools" / "data_availability_gate.py"),
            str(config_path), str(protocol_path),
            "--run-id", run_id,
            "--out-dir", str(out_dir),
        ]
        print("🗂️  Running E-054 data-availability gate (Layer 2)...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        # Exit codes (data_availability_gate.py's own convention):
        # 0=validate, 2=decline, 3=refine. A non-{0,2,3} code is a genuine
        # crash of the tool itself, not a real outcome — raise loud rather
        # than silently treating a bug in the gate as a data verdict.
        if result.returncode not in (0, 2, 3):
            raise RuntimeError(f"data_availability_gate.py crashed (exit {result.returncode}):\n{result.stderr}")

        gate_path = out_dir / "data_availability_gate.yaml"
        if not gate_path.exists():
            raise FileNotFoundError("data_availability_gate.yaml not found after gate run")

        import shutil as _dag_shutil
        _dag_shutil.copy(gate_path, ARTIFACTS / "data_availability_gate.yaml")
        gate_result = load_yaml(ARTIFACTS / "data_availability_gate.yaml") or {}
        print(f"✅ E-054 Layer 2 outcome: {gate_result.get('outcome', 'unknown').upper()}")

    elif stage_name == "protocol_execution" and _variant_loop_enabled():
        # E-033.1 Slice 4a (delivery_plan_v26.md Slice 4, sub-slice 1 of 2:
        # "loop restructure + trial accounting"). Runs tools/run_protocol.py
        # once per VALIDATED variant in artifacts/variants/index.yaml (S1_
        # FINDINGS.md §3a), instead of the flag-off branch's single
        # candidate_strategy_config.json below -- using the SAME resolved
        # protocol path for every variant (§7: confirmed variant-
        # independent). Each variant gets its own trial_id
        # (f"{run_id}:{variant_id}", Decision A) and its own
        # protocol_result.yaml under artifacts/variants/<variant_id>/.
        #
        # Decision B (this slice's dispatch, 2026-09-22): the singular
        # artifacts/protocol_result.yaml is ALSO still written, as an exact
        # copy of the 'base' variant's own result -- several existing
        # readers (run_loop's OWN protocol_execution conformance branch,
        # build_reports.py, verdict-interpreter/SKILL.md) still expect that
        # singular file to exist. This is an explicit, temporary bridge, not
        # a permanent per-variant design -- 4b (data gate + conformance +
        # grid/promotion wiring) revisits it once those consumers get real
        # per-variant treatment.
        #
        # Deliberately NOT built here (S1_FINDINGS.md's own 4a/4b split,
        # this slice's own scope limit): the per-variant data-availability-
        # gate loop, the conformance-check per-variant restructure (run_loop's
        # OWN separate elif branch, not this one), and _write_promotion_
        # audit's relationship to per-variant results. Also not per-variant
        # here (out of this slice's stated build list): pass_rule_evaluation.yaml
        # (C7) and category reports stay computed once, from the base
        # variant's summary only, exactly mirroring the flag-off branch's
        # shape -- only the grid (S1_FINDINGS.md §5/item 8) genuinely needs
        # every variant's result, since cross-variant comparison is its
        # entire purpose.
        index = load_yaml(ARTIFACTS / "variants" / "index.yaml") or {}
        variants_idx = index.get("variants", {})
        validated = {vid: v for vid, v in variants_idx.items() if v.get("status") == "validated"}
        if not validated:
            # Self-adversarial review item: the routing function
            # (_route_post_config_direct_backtest_specification) already
            # refuses to reach this stage with zero validated variants, but
            # this branch must never silently trust that and iterate over
            # nothing (a race/staleness case, e.g. index.yaml edited by hand
            # between routing and this stage running) -- raise loudly
            # instead of a silent no-op empty loop.
            raise RuntimeError(
                f"run_tool_worker(protocol_execution): no validated variants found in "
                f"{ARTIFACTS / 'variants' / 'index.yaml'} for {run_id} -- refusing to "
                "run an empty backtest loop."
            )

        protocol_path = _resolve_protocol_path(RUN_DIR, run_id)
        validation_path = ARTIFACTS / "validation_protocol.yaml"
        legacy_verdict_args = _legacy_verdict_args()  # C5.6: read once, every variant
        base_variant_id = _json_pointer_module().base_variant_id(validated)  # "base", else sorted()[0]

        per_variant_summaries: dict = {}
        base_summary = None
        refused_variants: dict = {}  # E-061 C1.3: variant_id -> reason (no trial row)
        # E-061 C2 S2a (D-015): variant_id -> reason for every validated variant
        # that produced no graded result (the `continue` branches below), prefixed
        # `refused:` (no data touched, no trial row) or `backtest_failed:` (a spent
        # look). The grid carries it as top-level failed_variants -- never a column
        # -- and the idea is then at best inconclusive. Trial rows are unchanged
        # (each failure branch still records its own). Each reason is also
        # persisted as index.yaml `failed_attempt`, so a later attempt of this run
        # (resume / retry of protocol_execution) still counts the variant unless
        # it re-runs it successfully -- otherwise a refused variant (not_tested
        # after attempt 1, never re-run) would silently drop out of the idea.
        _vce_prefixes = _verdict_criteria_evaluator_module()
        failed_variants: dict = {}
        carried_failures = {vid: v["failed_attempt"] for vid, v in variants_idx.items()
                            if isinstance(v, dict) and v.get("failed_attempt")}

        def _variant_failed(vid: str, why: str, *, refused: bool = False) -> None:
            prefix = (_vce_prefixes.FAILED_VARIANT_REFUSED if refused
                      else _vce_prefixes.FAILED_VARIANT_BACKTEST_FAILED)
            failed_variants[vid] = f"{prefix} {why}"

        for variant_id in sorted(validated):
            vinfo = validated[variant_id]
            trial_id = f"{run_id}:{variant_id}"
            # CODE-REVIEW FIX (2026-09-22): every other failure mode in this
            # loop (non-zero exit, missing summary, parse error, trial-write
            # failure) is wrapped and recorded via _record_failed_backtest_trial
            # before continuing -- this dict access was not, so a validated
            # index.yaml entry missing 'config_path' (e.g. a race/staleness
            # edit between routing and this stage running) raised an
            # uncaught KeyError with ZERO trial-ledger accounting for that
            # variant's attempted look, breaking the same H4-core invariant
            # this branch otherwise enforces everywhere else.
            _config_path_val = vinfo.get("config_path")
            if not _config_path_val:
                try:
                    _record_failed_backtest_trial(
                        run_id, RUN_DIR / "artifacts" / "variants" / variant_id,
                        f"variant '{variant_id}' is 'validated' in index.yaml but has no "
                        "'config_path' -- refusing to guess a path", trial_id=trial_id)
                except Exception as _rec_err:
                    print(f"⚠️  H4: could not record failed-backtest trial for {trial_id}: {_rec_err}")
                print(f"⚠️  protocol_execution: variant '{variant_id}' has no config_path in "
                      "index.yaml; continuing with remaining variants.")
                _variant_failed(variant_id, "validated in index.yaml but has no config_path")
                continue
            variant_config_path = RUN_DIR / _config_path_val
            variant_artifacts_dir = ARTIFACTS / "variants" / variant_id
            variant_artifacts_dir.mkdir(parents=True, exist_ok=True)
            variant_run_dir = RUN_DIR / "variants" / variant_id
            variant_run_dir.mkdir(parents=True, exist_ok=True)

            cmd = [
                str(TBOT_PYTHON), str(ROOT / "tools" / "run_protocol.py"),
                str(variant_config_path), str(protocol_path),
                *_validation_protocol_args(validation_path),
                *legacy_verdict_args,
                "--out-dir", str(variant_run_dir),
            ]
            print(f"--- protocol_execution: variant '{variant_id}' ---")
            _windows_before = _window_results(variant_run_dir)
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            if _refused_before_any_backtest(result, _windows_before, variant_run_dir):
                # E-061 C1.3: refused before any window ran -- an engineering
                # failure, no data touched, so NO trial row. This variant is
                # marked not_tested (written to index.yaml after the loop) and
                # the loop continues with the others.
                _first = (result.stderr or "").strip().splitlines()[0]
                refused_variants[variant_id] = (
                    f"run_protocol.py refused before any backtest (no data touched): {_first}")
                print(f"⚠️  protocol_execution: variant '{variant_id}' refused before any "
                      f"backtest (no data touched, no trial row); continuing with remaining "
                      f"variants.\n{result.stderr}")
                _variant_failed(variant_id, refused_variants[variant_id], refused=True)
                continue
            if result.returncode != 0:
                # Self-adversarial review item: variant 2 of 3 failing must
                # not stop variant 3 from running, and must not disturb
                # variant 1's already-recorded trial -- continue the loop,
                # same H4-core "record the spent look" pattern as the
                # flag-off branch below, just per-variant.
                try:
                    _record_failed_backtest_trial(
                        run_id, variant_config_path,
                        f"run_protocol.py non-zero exit ({result.returncode}) for variant "
                        f"'{variant_id}'", trial_id=trial_id)
                except Exception as _rec_err:
                    print(f"⚠️  H4: could not record failed-backtest trial for {trial_id}: {_rec_err}")
                print(f"⚠️  protocol_execution: variant '{variant_id}' failed (run_protocol.py "
                      f"exit {result.returncode}); continuing with remaining variants.")
                _variant_failed(variant_id, f"run_protocol.py non-zero exit ({result.returncode})")
                continue

            summary_path = variant_run_dir / "protocol_summary.json"
            if not summary_path.exists():
                try:
                    _record_failed_backtest_trial(
                        run_id, variant_config_path,
                        f"protocol_summary.json missing after protocol run for variant "
                        f"'{variant_id}'", trial_id=trial_id)
                except Exception as _rec_err:
                    print(f"⚠️  H4: could not record failed-backtest trial for {trial_id}: {_rec_err}")
                print(f"⚠️  protocol_execution: variant '{variant_id}' produced no "
                      "protocol_summary.json; continuing with remaining variants.")
                _variant_failed(variant_id, "protocol_summary.json missing after the protocol run")
                continue

            try:
                with open(summary_path, encoding="utf-8") as f:
                    summary = json.load(f)
                save_yaml(variant_artifacts_dir / "protocol_result.yaml", summary)
            except Exception as _win_err:
                try:
                    _record_failed_backtest_trial(
                        run_id, variant_config_path,
                        f"post-success window raised {type(_win_err).__name__} for variant "
                        f"'{variant_id}' (protocol_summary.json parse)", trial_id=trial_id)
                except Exception as _rec_err:
                    print(f"⚠️  H4: could not record failed-backtest trial for {trial_id}: {_rec_err}")
                print(f"⚠️  protocol_execution: variant '{variant_id}' failed parsing its "
                      f"summary ({type(_win_err).__name__}); continuing with remaining variants.")
                _variant_failed(variant_id, f"protocol_summary.json parse raised "
                                            f"{type(_win_err).__name__}")
                continue

            try:
                _record_backtest_trial(run_id, summary, variant_config_path, trial_id=trial_id)
            except Exception as _write_err:
                try:
                    _record_failed_backtest_trial(
                        run_id, variant_config_path,
                        f"backtest completed but the trial write raised "
                        f"{type(_write_err).__name__} for variant '{variant_id}'",
                        trial_id=trial_id)
                except Exception as _rec_err:
                    print(f"⚠️  G1: backtest completed but the ledger is unwritable for "
                          f"{trial_id} -- both the trial write ({type(_write_err).__name__}) "
                          f"and its recovery row ({type(_rec_err).__name__}) failed.")
                print(f"⚠️  protocol_execution: variant '{variant_id}' backtest completed but "
                      "its trial row could not be written; continuing with remaining variants.")
                _variant_failed(variant_id, f"the backtest completed but its trial write raised "
                                            f"{type(_write_err).__name__}")
                continue

            if variant_id == base_variant_id:
                # Decision B bridge -- singular file mirrors the base variant exactly.
                # E-061 C2 S2a: only once base's trial row is written -- a base whose
                # trial write failed is a failed variant, and its result must never
                # feed the singular file, C7 or the category reports.
                save_yaml(ARTIFACTS / "protocol_result.yaml", summary)
                base_summary = summary
            per_variant_summaries[variant_id] = summary
            top_verdict = summary.get("verdict", "unknown")
            print(f"✅ Variant '{variant_id}' protocol complete. Verdict: {top_verdict}")

        # E-061 C2 S2a (D-015): a variant refused / failed on an EARLIER attempt of
        # this run stays counted unless this attempt re-ran it successfully.
        for _vid, _reason in carried_failures.items():
            if _vid not in per_variant_summaries and _vid not in failed_variants:
                failed_variants[_vid] = _reason
        if refused_variants or failed_variants or carried_failures:
            # E-061 C1.3: record the refusals (no data touched, no trial row).
            for _vid, _reason in refused_variants.items():
                variants_idx[_vid] = {**variants_idx[_vid], "status": "not_tested",
                                      "reason": _reason}
            # E-061 C2 S2a: persist this attempt's failures; clear a carried one
            # whose variant this attempt re-ran successfully.
            for _vid in per_variant_summaries:
                variants_idx[_vid].pop("failed_attempt", None)
            for _vid, _reason in failed_variants.items():
                variants_idx[_vid] = {**variants_idx[_vid], "failed_attempt": _reason}
            save_yaml(ARTIFACTS / "variants" / "index.yaml", {"variants": variants_idx})
        # E-061 C2 S2a (card D): every other variant of the idea with no graded
        # result in THIS attempt -- skipped as an exact REPEAT, declined by the data
        # gate, refused by 5a. Unanimity is judged within one run, so the idea is
        # then at best inconclusive (earlier graded results live in the memory).
        untested_variants = {
            _vid: str((_v or {}).get("reason") or f"index status {(_v or {}).get('status')!r}")
            for _vid, _v in variants_idx.items()
            if _vid not in per_variant_summaries and _vid not in failed_variants}

        if not per_variant_summaries:
            raise RuntimeError(
                f"run_tool_worker(protocol_execution): all {len(validated)} validated "
                f"variant(s) failed for {run_id} -- no variant produced a successful "
                "backtest trial. See per-variant artifacts/variants/<variant_id>/ for detail."
            )

        # C7 pass-rule evaluation + E-046a category reports: computed ONCE,
        # from the base variant's summary only (or the first succeeded
        # variant if base itself failed) -- mirrors the flag-off branch's
        # single-result shape exactly, written to the same singular
        # artifacts/ paths. Not per-variant here; see this branch's own
        # header comment. E-061 C2 S2a: "succeeded" = graded, i.e. its trial row
        # was written (base_summary is set only then); a failed variant's result,
        # base's included, never feeds these artifacts. per_variant_summaries is
        # never empty here (all-failed raised above), so a representative exists.
        _rep_vid = base_variant_id if base_summary is not None else next(iter(per_variant_summaries))
        _rep_summary = per_variant_summaries[_rep_vid]
        if base_summary is None:
            # CODE-REVIEW FIX (2026-09-22): Decision B's bridge file
            # (artifacts/protocol_result.yaml, singular) was previously only
            # written inside the per-variant loop's own base-success branch
            # -- if base failed while a sibling variant succeeded, the
            # bridge file was never written at all, breaking every existing
            # singular-file reader this decision exists to keep working
            # (run_loop's conformance branch, build_reports.py, verdict-
            # interpreter/SKILL.md). Write it here from the same
            # already-computed representative summary the C7 step below
            # uses, so the bridge file always exists whenever ANY variant
            # succeeded, not only when base specifically did.
            save_yaml(ARTIFACTS / "protocol_result.yaml", _rep_summary)
        _tools_path = str(Path(__file__).parent.parent / "tools")
        if _tools_path not in sys.path:
            sys.path.insert(0, _tools_path)
        import verdict_criteria_evaluator as _vce
        _pre_reg_path = ARTIFACTS / "pre_registration.yaml"
        _pre_reg_for_eval = load_yaml(_pre_reg_path) if _pre_reg_path.exists() else {}
        _brief_path = ARTIFACTS / "research_brief.yaml"
        _brief_for_eval = (load_yaml(_brief_path) if _brief_path.exists() else {}) or {}
        # CODE-REVIEW FIX (2026-09-22): this block used to run completely
        # unguarded, unlike the grid/reports blocks right below it in this
        # same branch. By this point every succeeded variant's trial has
        # ALREADY been recorded (inside the per-variant loop above) -- a
        # crash here previously left N clean trial rows with
        # pass_rule_evaluation.yaml (a REQUIRED input for verdict_interpreter)
        # permanently missing and no signal that anything went wrong. Same
        # isolation pattern as the grid/reports blocks: log loudly, never
        # re-raise, never touch the already-recorded trials -- a bug in this
        # write is not evidence the backtest(s) failed.
        try:
            _pass_rule_eval = _vce.evaluate_pass_rule_criteria(
                _rep_summary, _pre_reg_for_eval or {}, _brief_for_eval)
            _pass_rule_eval["evaluated_at"] = datetime.now(timezone.utc).isoformat()
            _pass_rule_eval["evaluator_version"] = 2
            save_yaml(ARTIFACTS / "pass_rule_evaluation.yaml", _pass_rule_eval)
            _pre_reg_result = _pass_rule_eval.get("result")
            print(f"✅ [C7] pass_rule_evaluation.yaml written ({_rep_vid!r} variant): "
                  f"result={_pre_reg_result}")
        except Exception as _c7_err:
            print(f"⚠️  [C7] pass_rule_evaluation.yaml raised {type(_c7_err).__name__}: "
                  f"{_c7_err} -- at least one variant's backtest already succeeded and is "
                  "already recorded as a trial; pass_rule_evaluation.yaml is simply not "
                  "written this run. Not re-raised: a C7 bug must never misrecord an "
                  "already-successful trial as failed, but note this artifact is a "
                  "REQUIRED input for verdict_interpreter -- this run cannot proceed "
                  "past that stage until it exists.")

        # E-046b S2 (the grid). Dispatch step 5 / S1_FINDINGS.md §5 & §8: the
        # grid now receives a real N-column {variant_id: protocol_result}
        # dict built from every variant that actually succeeded, instead of
        # the flag-off branch's single-entry {run_id: summary}. Same gating
        # (menu-shaped pass_rule, _grid_evaluation_enabled()) and the same
        # never-turn-a-success-into-a-failure isolation as the flag-off
        # branch below.
        _sr_errors: list = []  # E-046a 5b-ii-B: grid/report failures, fatal only under specialist_readers
        if _grid_evaluation_enabled():
            try:
                _pass_rule_for_grid = _vce._find_pass_rule(_pre_reg_for_eval or {})
                if _vce._is_menu_shaped_pass_rule(_pass_rule_for_grid):
                    _menu_path = ROOT / "config" / "criterion_menu.yaml"
                    _menu = load_yaml(_menu_path) if _menu_path.exists() else {}
                    # E-061 C2 S2a (D-015, card D): the variants of this idea with
                    # no graded column in this attempt. Passed only when non-empty,
                    # so a run where every variant was graded writes a
                    # byte-identical grid.
                    _failed_kw = {**({"failed_variants": failed_variants} if failed_variants else {}),
                                  **({"untested_variants": untested_variants}
                                     if untested_variants else {})}
                    # E-060 S2: under composition_runs the grid reads copies carrying
                    # the residual IC; off, it reads per_variant_summaries unchanged.
                    if _composition_runs_enabled():
                        _grid_inputs, _grid_pre_reg = _residual_ic_grid_inputs(
                            per_variant_summaries, RUN_DIR, protocol_path, TBOT_PYTHON,
                            _pre_reg_for_eval or {})
                        # E-060 S3b: a composition run's profit_bars cells are
                        # graded by branch 3's own function (guess 9).
                        _grid_result = _vce.evaluate_grid(
                            _grid_inputs, _grid_pre_reg, _brief_for_eval, _menu,
                            composition_runs=True,
                            **({"profit_bars_grader": _profit_bars_grid_grader(RUN_DIR, run_id)}
                               if _composition_mode(RUN_DIR) else {}),
                            **_failed_kw)
                    else:
                        _grid_result = _vce.evaluate_grid(
                            per_variant_summaries, _pre_reg_for_eval or {}, _brief_for_eval, _menu,
                            **_failed_kw)
                    _grid_result["evaluated_at"] = datetime.now(timezone.utc).isoformat()
                    save_yaml(ARTIFACTS / "grid_evaluation.yaml", _grid_result)
                    _idea_status_artifact = _build_idea_status_artifact(_grid_result, run_id)
                    save_yaml(ARTIFACTS / "idea_status.yaml", _idea_status_artifact)
                    print(f"✅ [E-046b] grid_evaluation.yaml written across "
                          f"{sorted(per_variant_summaries)}: result={_grid_result.get('result')} "
                          f"idea_status={_grid_result.get('idea_status')}"
                          + (f" (failed, not graded: {sorted(failed_variants)})"
                             if failed_variants else "")
                          + (f" (untested this run: {sorted(untested_variants)})"
                             if untested_variants else ""))
                elif _sr_on:
                    _sr_errors.append("pre_registration.yaml's pass_rule is not menu-shaped -- no grid")
            except Exception as _grid_err:
                print(f"⚠️  [E-046b] grid evaluation raised {type(_grid_err).__name__}: "
                      f"{_grid_err} -- at least one variant's backtest already succeeded; "
                      "grid_evaluation.yaml/idea_status.yaml are simply not written this run.")
                if _sr_on:
                    _sr_errors.append(f"grid evaluation raised {type(_grid_err).__name__}: {_grid_err}")

        if _category_reports_enabled():
            try:
                if _sr_on:
                    _refresh_regime_detector_report_for_readers(run_id, RUN_DIR)
                _br_tools_path = str(Path(__file__).parent.parent / "tools")
                if _br_tools_path not in sys.path:
                    sys.path.insert(0, _br_tools_path)
                import build_reports as _br
                _reports = _br.build_reports(RUN_DIR, write=True)
                print(f"✅ [E-046a] artifacts/reports/*.yaml written: {sorted(_reports.keys())}")
            except Exception as _reports_err:
                print(f"⚠️  [E-046a] category report build raised {type(_reports_err).__name__}: "
                      f"{_reports_err} -- at least one variant's backtest already succeeded; "
                      "artifacts/reports/*.yaml are simply not written this run.")
                if _sr_on:
                    _sr_errors.append(f"category reports raised {type(_reports_err).__name__}: "
                                      f"{_reports_err}")

        print(f"✅ protocol_execution (variant loop): {len(per_variant_summaries)}/"
              f"{len(validated)} variant(s) succeeded: {sorted(per_variant_summaries)}")
        # Raised only now, after every variant's trial row is already recorded, so
        # a grid/report failure never misrecords a successful backtest as failed.
        _raise_specialist_readers_prereq_errors(_sr_errors)

    elif stage_name == "protocol_execution":
        config_path     = ARTIFACTS / "candidate_strategy_config.json"
        # K3/§9 Q4: consolidated resolver (also used by the E-054 data-
        # availability gate above, and formerly by the removed
        # signal_prescreen stage, E-039 step 5).
        protocol_path = _resolve_protocol_path(RUN_DIR, run_id)
        validation_path = ARTIFACTS / "validation_protocol.yaml"

        cmd = [
            str(TBOT_PYTHON), str(ROOT / "tools" / "run_protocol.py"),
            str(config_path), str(protocol_path),
            *_validation_protocol_args(validation_path),
            *_legacy_verdict_args(),
            "--out-dir", str(RUN_DIR),
        ]
        _windows_before = _window_results(RUN_DIR)
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if _refused_before_any_backtest(result, _windows_before, RUN_DIR):
            # E-061 C1.3: an engineering failure, no data touched -> no trial row.
            raise _RefusedBeforeAnyBacktest(
                f"run_protocol.py refused the candidate config before any backtest (no data "
                f"touched, no trial row recorded):\n{result.stderr}")
        if result.returncode != 0:
            # H4-core (issue #28): this data-touching backtest raised before
            # _record_backtest_trial (:1134) — record the spent look so N counts it.
            # Wrapped so a recording failure only logs; the original error still raises.
            try:
                _record_failed_backtest_trial(
                    run_id, config_path,
                    f"run_protocol.py non-zero exit ({result.returncode})")
            except Exception as _rec_err:
                print(f"⚠️  H4: could not record failed-backtest trial for {run_id}: {_rec_err}")
            raise RuntimeError(f"run_protocol.py failed:\n{result.stderr}")

        summary_path = RUN_DIR / "protocol_summary.json"
        if not summary_path.exists():
            # H4-core (issue #28): same as above for the missing-summary failure.
            try:
                _record_failed_backtest_trial(
                    run_id, config_path,
                    "protocol_summary.json missing after protocol run")
            except Exception as _rec_err:
                print(f"⚠️  H4: could not record failed-backtest trial for {run_id}: {_rec_err}")
            raise FileNotFoundError("protocol_summary.json not found after protocol run")

        # H4-core (E-025 B1, issue #28): the subprocess exited 0 AND wrote
        # protocol_summary.json -- the backtest really ran and market data was really
        # spent -- but this post-success window (json.load, save_yaml, the C7 pass-rule
        # eval) can still raise BEFORE _record_backtest_trial below (a truncated/corrupt
        # summary at json.load; a non-numeric structured pass-rule metric inside
        # evaluate_pass_rule_criteria). The two failure branches above (:1140/:1153) each
        # record a backtest_failed row before re-raising; this window had none, so a raise
        # here left NO trial row while the look had already touched data -- N under-counted.
        # Record the spent look, then RE-RAISE the original error unchanged: this is an
        # accounting add, not an exception swallow -- the loud halt that escalates to a
        # human must survive. Recording is itself wrapped so its own failure only logs.
        _sr_errors: list = []  # E-046a 5b-ii-B: grid/report failures, fatal only under specialist_readers
        try:
            with open(summary_path, encoding="utf-8") as f:
                summary = json.load(f)
            save_yaml(ARTIFACTS / "protocol_result.yaml", summary)
            # The kill decision is the TOP-LEVEL `verdict` (measured: 'kill' in 18/39 real
            # protocol_summary.json). hypothesis_verdict.verdict is 'refine'/None but NEVER
            # 'kill' (0/39), so the old line — which printed only that field — showed 'refine'
            # for a killed run, the one word an operator reads to see what the run decided. Show
            # the top-level verdict prominently, keeping the hypothesis_verdict detail alongside.
            hv = (summary.get("hypothesis_verdict") or {}).get("verdict", "unknown")
            top_verdict = summary.get("verdict", "unknown")
            print(f"✅ Protocol complete. Verdict: {top_verdict} "
                  f"(hypothesis_verdict detail: {hv})")

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

            # E-046b S2 (the grid, engineering_roadmap.html card C). ADDITIVE:
            # fires only when the flag is on AND pre_registration's pass_rule is
            # menu-shaped (criteria carry source/reducer fields) -- everything
            # above (evaluate_pass_rule_criteria's call, pass_rule_evaluation.yaml's
            # own write) is completely untouched either way. A single-variant
            # (this run's own) 1-column grid, per S1_FINDINGS.md §7 / delivery_plan_v26.md
            # slice 2: "a grid with one column is still a grid."
            #
            # CODE-REVIEW FIX (2026-09-20): this block used to sit inside the SAME
            # try/except as pass_rule_evaluation.yaml's write, above. A backtest
            # that completed successfully (pass_rule_evaluation.yaml already on
            # disk) would get misrecorded as a FAILED trial by the outer handler's
            # _record_failed_backtest_trial call if grid evaluation itself raised
            # -- e.g. a menu criterion declaring floor.min_n_eff (deliberately
            # NotImplementedError, see _check_floor) or an idea_status the routing
            # table doesn't recognize. Grid evaluation is a purely additive,
            # informational artifact; a bug in it is not evidence the backtest
            # failed, and must never overwrite an already-successful trial's
            # ledger entry. Isolated in its own try/except that logs loudly and
            # re-raises NOTHING, so a grid bug can never turn a real success into
            # a recorded failure.
            if _grid_evaluation_enabled():
                try:
                    _pass_rule_for_grid = _vce._find_pass_rule(_pre_reg_for_eval or {})
                    if _vce._is_menu_shaped_pass_rule(_pass_rule_for_grid):
                        _menu_path = ROOT / "config" / "criterion_menu.yaml"
                        _menu = load_yaml(_menu_path) if _menu_path.exists() else {}
                        _grid_result = _vce.evaluate_grid(
                            {run_id: summary}, _pre_reg_for_eval or {}, _brief_for_eval, _menu)
                        _grid_result["evaluated_at"] = datetime.now(timezone.utc).isoformat()
                        save_yaml(ARTIFACTS / "grid_evaluation.yaml", _grid_result)
                        _idea_status_artifact = _build_idea_status_artifact(_grid_result, run_id)
                        save_yaml(ARTIFACTS / "idea_status.yaml", _idea_status_artifact)
                        print(f"✅ [E-046b] grid_evaluation.yaml written: result="
                              f"{_grid_result.get('result')} idea_status="
                              f"{_grid_result.get('idea_status')}")
                    elif _sr_on:
                        _sr_errors.append("pre_registration.yaml's pass_rule is not menu-shaped "
                                          "-- no grid")
                except Exception as _grid_err:
                    print(f"⚠️  [E-046b] grid evaluation raised "
                          f"{type(_grid_err).__name__}: {_grid_err} -- the backtest itself "
                          "already succeeded and pass_rule_evaluation.yaml is already written; "
                          "grid_evaluation.yaml/idea_status.yaml are simply not written this "
                          "run. Not re-raised: a grid bug must never misrecord a successful "
                          "trial as failed.")
                    if _sr_on:
                        _sr_errors.append(f"grid evaluation raised {type(_grid_err).__name__}: "
                                          f"{_grid_err}")

            # E-046a Slice 5a (delivery_plan_v26.md, "Slice 5 -- Reports and
            # readers"). ADDITIVE, called AFTER the grid block above, same
            # isolation pattern: category reports are a pure re-projection of
            # artifacts that already exist once the backtest above succeeded
            # (protocol_result.yaml/summary, trade_diagnostics.json,
            # bars.csv, and the campaign-level regime_detector_report.yaml),
            # so a bug in report-building must never turn an already-
            # successful trial into a recorded failure -- its own try/except,
            # logs loudly, never re-raises.
            if _category_reports_enabled():
                try:
                    if _sr_on:
                        _refresh_regime_detector_report_for_readers(run_id, RUN_DIR)
                    _br_tools_path = str(Path(__file__).parent.parent / "tools")
                    if _br_tools_path not in sys.path:
                        sys.path.insert(0, _br_tools_path)
                    import build_reports as _br
                    _reports = _br.build_reports(RUN_DIR, write=True)
                    print(f"✅ [E-046a] artifacts/reports/*.yaml written: "
                          f"{sorted(_reports.keys())}")
                except Exception as _reports_err:
                    print(f"⚠️  [E-046a] category report build raised "
                          f"{type(_reports_err).__name__}: {_reports_err} -- the "
                          "backtest itself already succeeded; artifacts/reports/*.yaml "
                          "are simply not written this run. Not re-raised, same "
                          "reasoning as the grid-evaluation block above.")
                    if _sr_on:
                        _sr_errors.append(f"category reports raised "
                                          f"{type(_reports_err).__name__}: {_reports_err}")
        except Exception as _win_err:
            try:
                _record_failed_backtest_trial(
                    run_id, config_path,
                    f"post-success window raised {type(_win_err).__name__} "
                    "(protocol_summary.json parse or pass-rule evaluation) "
                    "after successful protocol run")
            except Exception as _rec_err:
                print(f"⚠️  H4: could not record failed-backtest trial for {run_id}: {_rec_err}")
            raise

        # A6.2: record full-backtest trial in campaign_state.trial_sharpes.
        # G1 (E-025, issue #28): the LAST unwrapped writer on the data-touching path —
        # its three sibling _record_failed_backtest_trial calls — the non-zero-exit branch, the
        # missing-summary branch, and the post-success-window guard — each wrap the recorder in
        # try/except.
        # The backtest COMPLETED here (data spent, a real median Sharpe in `summary`), so a
        # raise inside _record_backtest_trial (a config that vanished from the artifacts dir
        # at _compute_forecast_hash; a corrupt/unreadable ledger at load_campaign_state; a
        # disk/permission failure at _save_campaign_state) would leave NO trial row while the
        # look had already touched market data — N under-counting a spent look, exactly the
        # H4/B1 defect one stage later. Record a distinct-reason recovery row so N still counts
        # it, then RE-RAISE the original unchanged: an accounting add, never a swallow (the loud
        # halt that escalates to a human must survive). The recovery writer itself calls
        # load_campaign_state/_save_campaign_state, so when the LEDGER is the failure the recovery
        # also fails — degrade to a loud log and re-raise the ORIGINAL error, never mask it with
        # the recovery's own.
        try:
            _record_backtest_trial(run_id, summary, config_path)
        except Exception as _write_err:
            try:
                _record_failed_backtest_trial(
                    run_id, config_path,
                    f"backtest completed but the trial write raised "
                    f"{type(_write_err).__name__} (ledger/hash write failure after a "
                    "successful backtest)")
            except Exception as _rec_err:
                print(f"⚠️  G1: backtest completed but the ledger is unwritable for {run_id} — "
                      f"both the trial write ({type(_write_err).__name__}) and its recovery row "
                      f"({type(_rec_err).__name__}) failed; re-raising the original.")
            raise

        # E-046a 5b-ii-B: raised only after the trial row above is recorded, so a
        # grid/report failure under specialist_readers fails the stage without
        # misrecording a successful backtest as failed. Flag off: _sr_errors is empty.
        _raise_specialist_readers_prereq_errors(_sr_errors)

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

    elif stage_name == "backtest_specification":
        # E-056 Slice 3b (config-direct authoring, orchestrator.config_direct_authoring.enabled):
        # tool-only replacement for the LLM-authored backtest_specification stage. By the time
        # this branch runs, strategy_config_authoring (1b, now BEFORE innovation_expansion in this
        # flow) already wrote the BASE config into artifacts/backtest_spec.yaml, and
        # innovation_expansion (Step 2, rewritten this slice) already wrote
        # artifacts/variant_patches.yaml -- base + design patch + asset patch, each
        # {variant_id, patch: [{path, value}], rationale}. This branch applies each variant's
        # patch to the base config, validates the result (validate_config.py, which includes V12
        # component-existence automatically), checks the manifest's declared paths resolve,
        # and writes one strategy_config.json
        # per variant, plus a 'base' variant copy at candidate_strategy_config.json so the
        # EXISTING data_availability_gate/protocol_execution tool branches above (both
        # unmodified) can run against it exactly as they always have.
        base_spec_path = ARTIFACTS / "backtest_spec.yaml"
        base_spec = load_yaml(base_spec_path) if base_spec_path.exists() else None
        if not base_spec or base_spec.get("status") != "spec_ready" or not base_spec.get("config"):
            raise RuntimeError(
                "run_tool_worker(backtest_specification): artifacts/backtest_spec.yaml is "
                "missing, not spec_ready, or has no 'config' -- strategy_config_authoring must "
                "complete successfully (status: spec_ready) before this tool stage can run."
            )
        base_config = base_spec["config"]

        patches_path = ARTIFACTS / "variant_patches.yaml"
        patches_doc = load_yaml(patches_path) if patches_path.exists() else None
        if not patches_doc or not patches_doc.get("variants"):
            raise RuntimeError(
                "run_tool_worker(backtest_specification): artifacts/variant_patches.yaml is "
                "missing or has no 'variants' -- innovation_expansion must write it before this "
                "tool stage can run."
            )

        # E-056 1b block manifest (STRATEGY_DESIGN_GUIDE.md §7c, built): 1b writes
        # artifacts/block_manifest.yaml next to the config. Checked here, against the base
        # config, with tools/block_manifest.py -- the exact check tools/block_registry.py
        # runs later -- so a manifest this stage accepts is one the registry accepts.
        # Missing, unparseable, malformed or unresolved: fail loud before any variant is
        # built (this branch only runs under orchestrator.config_direct_authoring).
        # E-060 S3b: a composition run has no block manifest -- its composition
        # manifest is checked instead (every block present, gated and pinned as
        # its source, the scheme's weights), on the base and on every variant.
        _comp_run = _composition_mode(RUN_DIR)
        if _comp_run:
            _comp_cand = _composition_candidate(RUN_DIR)
            comp_manifest = _load_composition_manifest(RUN_DIR, _comp_cand)
            if load_yaml(ARTIFACTS / _COMPOSITION_MANIFEST_FILE) != comp_manifest:
                raise RuntimeError(
                    f"run_tool_worker(backtest_specification): artifacts/"
                    f"{_COMPOSITION_MANIFEST_FILE} is not the brief's composition manifest")
            # an R1 composition's base IS the code-written base: every variant
            # must then hash to its code-written file (a reader patch's may not)
            _comp_strict = (base_config is not None and _canonical_json_sha256(base_config)
                            == comp_manifest["variants"]["base"]["config_sha256"])
            _comp_registry = _load_block_registry_doc()  # once for every variant (fix 8)
            _check_composition_variant(ARTIFACTS, "base", base_config, comp_manifest, _comp_strict,
                                       _comp_registry)
        else:
            _bm = _block_manifest_module()
            manifest_path = ARTIFACTS / _bm.MANIFEST_FILENAME
            manifest = _bm.load_manifest_file(manifest_path, error_cls=RuntimeError)
            if manifest is None:
                raise RuntimeError(
                    "run_tool_worker(backtest_specification): artifacts/block_manifest.yaml is "
                    "missing -- strategy_config_authoring must write it next to the base config "
                    "(STRATEGY_DESIGN_GUIDE.md §7c) when its status is spec_ready."
                )
            _bm.check_manifest(manifest, base_config, where=str(manifest_path),
                               error_cls=RuntimeError)
        # E-059 S2a: a decide_next patch candidate's config must be 1b's verbatim
        # pass-through copy (no-op for every other brief -- see the function).
        _check_pass_through_config_hash(ARTIFACTS)

        variants_dir = ARTIFACTS / "variants"
        variants_dir.mkdir(parents=True, exist_ok=True)
        index = {}
        component_requests = []

        for variant in patches_doc["variants"]:
            variant_id = variant.get("variant_id") if isinstance(variant, dict) else None
            if variant_id in index:
                # CODE-REVIEW FIX (self-adversarial pass, E-056 Slice 3b): a duplicate
                # variant_id would otherwise silently overwrite the first entry's result
                # in `index` below -- the exact "silently wrong rather than loudly wrong"
                # failure mode this slice's own dispatch asked to be checked for.
                raise RuntimeError(
                    f"run_tool_worker(backtest_specification): duplicate variant_id "
                    f"'{variant_id}' in artifacts/variant_patches.yaml -- each variant_id "
                    "must be unique, the second entry would silently overwrite the first's "
                    "recorded result."
                )
            if not variant_id:
                raise RuntimeError(
                    "run_tool_worker(backtest_specification): a variant_patches.yaml entry is "
                    f"missing 'variant_id' (entry: {variant!r})"
                )
            # CODE-REVIEW FIX (2026-09-21): variant_id is LLM-authored
            # (innovation-expansion's output) and gets used below as a bare
            # filesystem path segment (variants_dir / variant_id). Without a
            # shape check, a path-separator or ".." in variant_id (an
            # authoring slip, e.g. "design/v2", or worse) would let
            # variant_dir resolve outside artifacts/variants/ entirely --
            # pathlib's `/` operator also treats an absolute right-hand
            # operand specially, replacing the base path altogether. Refuse
            # anything that isn't a safe bare identifier before it's ever
            # used to construct a write path.
            if not re.fullmatch(r"[A-Za-z0-9_-]+", variant_id):
                raise RuntimeError(
                    f"run_tool_worker(backtest_specification): variant_id {variant_id!r} is "
                    "not a safe bare identifier (letters, digits, '_', '-' only) -- refusing "
                    "to use it as a filesystem path segment."
                )

            try:
                variant_config = _apply_json_pointer_patch(base_config, variant.get("patch") or [])
            except PatchApplicationError as e:
                reason = f"patch application failed: {e}"
                index[variant_id] = {"status": "not_tested", "reason": reason}
                component_requests.append({"variant_id": variant_id, "reason": reason})
                print(f"⚠️  [E-056 Slice3b] variant '{variant_id}' NOT TESTED: {reason}")
                continue

            if _comp_run:
                # E-060 S3b: code-written patches -- a mismatch is an engineering
                # fault and raises (never a quietly not_tested variant).
                _check_composition_variant(ARTIFACTS, variant_id, variant_config, comp_manifest,
                                           _comp_strict, _comp_registry)
                missing_paths = []
            else:
                # A variant patch can still remove a BLOCK path; that variant no longer
                # holds the idea, so it is not tested. Scaffolding may change per variant
                # (the base config's scaffolding was checked above).
                missing_paths = _check_manifest_paths(variant_config, manifest)
            if missing_paths:
                reason = f"manifest paths unresolved: {missing_paths}"
                index[variant_id] = {"status": "not_tested", "reason": reason}
                component_requests.append({"variant_id": variant_id, "reason": reason})
                print(f"⚠️  [E-056 Slice3b] variant '{variant_id}' NOT TESTED: {reason}")
                continue

            variant_dir = variants_dir / variant_id
            variant_dir.mkdir(parents=True, exist_ok=True)
            variant_config_path = variant_dir / "strategy_config.json"
            with open(variant_config_path, "w", encoding="utf-8") as f:
                json.dump(variant_config, f, indent=2)

            validator = Path("..") / "trading-bot" / "tools" / "validate_config.py"
            result = subprocess.run(
                [str(TBOT_PYTHON), str(validator), str(variant_config_path)],
                capture_output=True, text=True,
            )
            if result.returncode != 0:
                report = (result.stdout + result.stderr).strip()
                (variant_dir / "spec_validation_report.txt").write_text(report, encoding="utf-8")
                reason = "validate_config.py violations"
                index[variant_id] = {
                    "status": "not_tested", "reason": reason,
                    "config_path": str(variant_config_path.relative_to(RUN_DIR)),
                    "report": report,
                }
                component_requests.append({"variant_id": variant_id, "reason": reason, "report": report})
                print(f"⚠️  [E-056 Slice3b] variant '{variant_id}' NOT TESTED: {reason}")
                continue

            index[variant_id] = {
                "status": "validated",
                "config_path": str(variant_config_path.relative_to(RUN_DIR)),
            }
            if variant_id == "base":
                with open(ARTIFACTS / "candidate_strategy_config.json", "w", encoding="utf-8") as f:
                    json.dump(variant_config, f, indent=2)

        # E-059 S2a: re-checked on the base variant actually written above.
        _check_pass_through_config_hash(ARTIFACTS)
        save_yaml(variants_dir / "index.yaml", {"variants": index})
        if component_requests:
            # Slice 6c S2b review fix 8: one locked, atomic appender shared with
            # campaign review's escalate_component (same {requests: [...]} file).
            _crr.append_component_requests(
                ROOT / _crr.COMPONENT_REQUESTS_REL,
                [{"run_id": run_id, "stage": "backtest_specification", **req}
                 for req in component_requests],
                # Slice 6c S2c review fix 7: a parked run re-runs this stage on
                # --unpark; under the flag the same request is not appended twice.
                **({"key": _crr.request_key} if _verdict_routing_retired_enabled() else {}))

        validated_count = sum(1 for v in index.values() if v["status"] == "validated")
        print(f"✅ [E-056 Slice3b] backtest_specification (config-direct authoring): "
              f"{validated_count}/{len(index)} variants validated")

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
    "backtest_specification",
    "verdict_interpreter",
    "campaign_review",
    # CODE-REVIEW FIX (2026-09-21, E-056 Slice 3b): under
    # orchestrator.config_direct_authoring.enabled, strategy_config_authoring
    # -- not backtest_specification -- is the LLM stage that compiles the
    # hypothesis into a binding strategy config. B7 exists specifically
    # because a compiling-type stage deciding without ever reading
    # pre_registration.yaml caused real incidents (see this constant's own
    # comment block above); omitting the new stage here would silently
    # reopen exactly that gap for the config-direct-authoring flow.
    # backtest_specification stays in this set too, since flag-off it is
    # still the LLM-authoring stage exactly as before.
    "strategy_config_authoring",
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


# CUL-336 (2026-09-27): files a stage's own SKILL.md tells it to read that no
# handoff delivered. While stage agents had the CLI's default tools they could
# open such files themselves (measured once: a run_060 validation agent Read
# config/cost_model.yaml); closed-book (_stage_agent_options) they see only
# what the prompt carries, so the files are unioned into the handoff here, the
# same deterministic way as B7. Entries: (path relative to the run dir, kind,
# reason); a path starting with "@" is resolved at call time
# (_CLOSED_BOOK_DYNAMIC_PATHS). Kinds:
#   required        tracked reference files -- a missing one is a broken
#                   checkout and _build_stage_prompt raises.
#   optional        run artifacts that exist on some paths only.
#   refine_only     optional, and added only when this run is already in a
#                   validation refine loop (artifacts/refinement_notes.yaml
#                   exists) -- the only refine signal code has before the
#                   stage decides; keeps the skill's minimal-context rule on a
#                   first pass.
#   after_backtest  required when artifacts/protocol_result.yaml records a
#                   completed backtest (a non-empty results list), else
#                   optional.
# Deliberately NOT here: campaign_data_policy.yaml for validation (its skill
# says not to read it directly; the one field it fed, sample_split_design.
# walk_forward_range, has no code reader), and trade_diagnostics.json's
# per-trade list (up to ~480 KB measured, runs/run_059) -- verdict_interpreter
# gets only its summary block, which is all its skill reads
# (_write_trade_diagnostics_summary).
_TRADE_DIAGNOSTICS_SUMMARY_REL = "artifacts/trade_diagnostics_summary.yaml"
_CLOSED_BOOK_QUANT_FUNDAMENTALS = (
    "../../workflow_artifacts/skills/quant-fundamentals/SKILL.md", "required",
    "CUL-336: this stage's skill says to read quant-fundamentals before applying its rules "
    "or proposing a config change; it is authoritative over a conflicting skill rule.",
)
_CLOSED_BOOK_STAGE_INPUTS = {
    "innovation_expansion": (
        ("../../config/coin_universe.yaml", "required",
         "CUL-336: skill required input (Improvement 06 asset-generalizability check -- "
         "candidate symbols from a different category than the base instrument)."),
    ),
    "validation": (
        ("../../config/cost_model.yaml", "required",
         "CUL-336: skill Improvement 09 -- populate cost_feasibility from round_trip_cost_bps; "
         "the single source of truth for cost numbers (implausible blocks approval)."),
        ("artifacts/innovation_notes.yaml", "refine_only",
         "CUL-336: skill input, needed only on a refine verdict (context for the plan); given "
         "because this run is already in a refine loop."),
        ("../../docs/DATA_AVAILABILITY.md", "refine_only",
         "CUL-336: skill input, for a refine blocker about data/timeframe availability; given "
         "because this run is already in a refine loop."),
    ),
    "backtest_specification": (
        ("artifacts/innovation_notes.yaml", "optional",
         "CUL-336: skill required input (Improvement 02 asset_diversity_audit candidate symbols)."),
        ("../../docs/DATA_AVAILABILITY.md", "optional",
         "CUL-336: forced-read whenever timeframe/symbol/venue differs from a prior config."),
        ("artifacts/findings_carryover.yaml", "optional",
         "CUL-336: if present, the parameter_bracket midpoint is mandatory for that dimension."),
        ("artifacts/run_context.yaml", "optional",
         "CUL-336: if present, run_type drives the skill's Replication guard."),
        _CLOSED_BOOK_QUANT_FUNDAMENTALS,
    ),
    "strategy_config_authoring": (_CLOSED_BOOK_QUANT_FUNDAMENTALS,),
    "verdict_interpreter": (
        ("artifacts/pass_rule_evaluation.yaml", "after_backtest",
         "CUL-336: skill REQUIRED input (K2) -- when result is PASS or FAIL, hypothesis_verdict/"
         "lineage_routing are copy-through. Required once protocol_result.yaml records a "
         "completed backtest."),
        ("../../config/coin_universe.yaml", "required",
         "CUL-336: skill input (E-026 asset stability gate; escalation target selection)."),
        ("@campaign_state", "optional",
         "CUL-336: skill input -- cross-run altitude history (altitude decision logic, circuit "
         "breaker). The old ../../campaign_state.yaml path never resolved after the E-002 move."),
        (_TRADE_DIAGNOSTICS_SUMMARY_REL, "optional",
         "CUL-336: the summary block of this run's trade_diagnostics.json (STEP 03 trade "
         "attribution, fee_reduction_metrics). Written by code from that file; the per-trade "
         "list is left out (size)."),
        _CLOSED_BOOK_QUANT_FUNDAMENTALS,
    ),
    "campaign_review": (_CLOSED_BOOK_QUANT_FUNDAMENTALS,),
}


def _closed_book_dynamic_path(token: str) -> str:
    """Paths that follow a module-level location (patched in tests)."""
    if token == "@campaign_state":
        return _rel_to_run(CAMPAIGN_STATE_PATH)
    raise ValueError(f"unknown closed-book path token {token!r}")


def _completed_backtest(run_dir: Path) -> bool:
    """True when artifacts/protocol_result.yaml exists and records at least
    one backtest result -- the file is written only after a backtest ran."""
    path = run_dir / "artifacts" / "protocol_result.yaml"
    if not path.exists():
        return False
    doc = load_yaml(path)
    return isinstance(doc, dict) and bool(doc.get("results"))


def _write_trade_diagnostics_summary(run_dir: Path) -> None:
    """verdict_interpreter's skill reads only the `summary` block of
    trade_diagnostics.json (written by tools/run_protocol.py into the run dir,
    where tools/build_reports.py also looks for it). The full file carries
    every trade -- 481,835 bytes on runs/run_059 -- so only the summary is
    put in front of the model, written into the run so the run keeps exactly
    what the model was shown. Absent file: nothing written (optional input).
    A present but malformed file raises."""
    src = run_dir / "trade_diagnostics.json"
    if not src.exists():
        return
    with open(src, encoding="utf-8") as f:
        doc = json.load(f)
    if not isinstance(doc, dict) or "summary" not in doc:
        raise ValueError(f"{src} has no top-level 'summary' block")
    save_yaml(run_dir / _TRADE_DIAGNOSTICS_SUMMARY_REL, {
        "source": "trade_diagnostics.json (summary block only; per-trade list omitted)",
        "summary": doc["summary"],
    })


def _apply_closed_book_inputs(stage_name: str, handoff: dict, run_dir: Path) -> None:
    """Union _CLOSED_BOOK_STAGE_INPUTS[stage_name] into the handoff's
    required_inputs/optional_inputs. A path already named keeps its entry,
    except that required wins: a path in both lists ends up required only.
    Always on: part of CUL-336's declared default change, no flag."""
    entries = _CLOSED_BOOK_STAGE_INPUTS.get(stage_name)
    if not entries:
        return
    if stage_name == "verdict_interpreter":
        _write_trade_diagnostics_summary(run_dir)
    required = handoff.setdefault("required_inputs", [])
    optional = handoff.setdefault("optional_inputs", [])
    in_refine_loop = (run_dir / "artifacts" / "refinement_notes.yaml").exists()
    backtest_done = _completed_backtest(run_dir)
    for path, kind, reason in entries:
        if path.startswith("@"):
            path = _closed_book_dynamic_path(path)
        if kind == "refine_only":
            if not in_refine_loop:
                continue
            kind = "optional"
        elif kind == "after_backtest":
            kind = "required" if backtest_done else "optional"
        target = required if kind == "required" else optional
        if path in {r["path"] for r in required} or path in {r["path"] for r in target}:
            continue
        target.append({"path": path, "reason": reason})
    required_paths = {r["path"] for r in required}
    optional[:] = [r for r in optional if r["path"] not in required_paths]


# E-032 S2a: the exclusion digest as a required_input on the two stages that
# invent content. See engineering/roadmap/E-032/EPIC.md's 2026-08-23 review
# entry -- "E-032 is primarily an INPUT problem, not a disposition problem."
# hypothesis_generation/innovation_expansion structurally cannot see
# campaign history today (neither stage's handoff template lists
# campaign_state.yaml, the KB, or the scoreboard; the ONE nominal reference,
# research_brief_to_hypothesis.yaml's optional campaign_knowledge_base.yaml
# entry, points at a path -- "../../campaign_knowledge_base.yaml" -- that
# does not exist; the real file lives under campaign_record/, so that
# optional_input has always silently no-op'd). This union puts what was
# already tried in front of the model, gated by config/campaign_config.yaml's
# orchestrator.exclusion_digest_input.enabled (same shape as E-030 S2a's
# halt_policy.quarantine_enabled -- see run_campaign._quarantine_enabled();
# switched ON 2026-09-02 by E-041).
#
# E-036 S2a (2026-09-27, S1_FINDINGS_SLICE8.md operator decision 3): when
# campaign_record/campaign_memory.yaml exists, the input is
# artifacts/tried_ideas.yaml -- a per-run snapshot derived at prompt time by
# tools/campaign_memory.tried_ideas (idea hypothesis_id, coins, timeframe, the
# grid's idea_status; no family grouping; at most TRIED_IDEAS_MAX_ROWS rows, so
# the prompt stays bounded) -- and the legacy digest is NOT also fed. When it
# does not exist (orchestrator.regroup_record off, today's default), the input
# is the legacy campaign_record/exclusion_digest.yaml exactly as before this
# story (same path, same reason text, same missing-file skip): the default
# prompt input is byte-identical (tests/test_exclusion_digest_input.py pins it).
_EXCLUSION_DIGEST_INPUT_STAGES = {"hypothesis_generation", "innovation_expansion"}
_EXCLUSION_DIGEST_RELATIVE_PATH = "../../campaign_record/exclusion_digest.yaml"
_EXCLUSION_DIGEST_REASON = (
    "E-032 S2a: family-scoped (family, instrument, timeframe) triples "
    "already tried, freshly derived from run artifacts -- NOT "
    "campaign_state.yaml's stale, family-blind instruments_tried/"
    "timeframes_tried lists. Prefer a candidate whose family is absent "
    "here, or whose (instrument, timeframe) triple is absent under its "
    "family, over a same-family tweak when both are viable. This is "
    "raw material, not a binding gate -- the anti_adjacency_gate tool "
    "stage makes the mechanical refusal decision downstream."
)
_TRIED_IDEAS_RELATIVE_PATH = "artifacts/tried_ideas.yaml"
_TRIED_IDEAS_REASON = (
    "E-036 S2a: what was already tried -- one row per run recorded in "
    "campaign_record/campaign_memory.yaml: the idea (hypothesis_id), its coins, the "
    "timeframe it ran on, and the grid's idea_status (validated / refuted / "
    "inconclusive). No family grouping: an idea's identity is its hypothesis_id, and "
    "the same idea on other coins or another timeframe is a variant of it. Prefer an "
    "idea, or a coin/timeframe, not listed here over re-proposing a listed one "
    "unchanged. This is raw material, not a binding gate -- the exact-match check at "
    "5a refuses an exact repeat (same config, coins, timeframe and protocol windows) "
    "downstream."
)


# E-061 C1.4 / C1.5: the run-level halt flags run_campaign sets on a classified
# pause (stage_exception, protocol_promotion_unratified, launch_exception); every
# un-pause path clears them (_stale_run_halt_flags). One source for both modules.
RUN_HALT_FLAGS = ("stage_exception", "protocol_promotion_unratified", "launch_exception")


def _orchestrator_config(cfg: dict | None = None) -> dict:
    """E-061 C1.5 (third-round review fix 10): the parsed config/campaign_config.yaml
    a flag reader works on -- `cfg` when the caller already parsed it (run_campaign's
    launch pre-flight parses it ONCE and calls every real reader with it), else
    read here ({} when the file is absent, so each reader's own default holds).
    """
    if cfg is not None:
        return cfg
    path = ROOT / "config" / "campaign_config.yaml"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _flag_dep(reader, cfg: dict | None) -> bool:
    """A prerequisite flag read by a flag reader: on the same parsed config when one
    was passed, else exactly as before (no argument -- so a reader replaced in a
    test by a zero-argument stub still works on the runtime path)."""
    return reader() if cfg is None else reader(cfg)


# E-046b S2 (the grid, engineering_roadmap.html card C). Off-by-default flag,
# same shape as _exclusion_digest_input_enabled() below. See
# config/campaign_config.yaml's orchestrator.grid_evaluation.enabled comment
# for the full rationale.
def _grid_evaluation_enabled(cfg: dict | None = None) -> bool:
    """False (no behavior change) when the key, the section, or the file is
    absent -- same silence-is-never-a-green-light rule as
    _exclusion_digest_input_enabled() below. While false, the
    protocol_execution branch's existing evaluate_pass_rule_criteria() call
    and its pass_rule_evaluation.yaml write are completely untouched, and
    artifacts/grid_evaluation.yaml / artifacts/idea_status.yaml are never
    written."""
    cfg = _orchestrator_config(cfg)
    return _strict_orchestrator_flag("grid_evaluation", cfg=cfg)  # E-061 C1.5: strict


# E-046a Slice 5a (delivery_plan_v26.md, "Slice 5 -- Reports and readers").
# Off-by-default flag, same shape as _grid_evaluation_enabled() above. See
# config/campaign_config.yaml's orchestrator.category_reports.enabled
# comment for the full rationale.
def _category_reports_enabled(cfg: dict | None = None) -> bool:
    """False (no behavior change) when the key, the section, or the file is
    absent -- same silence-is-never-a-green-light rule as
    _grid_evaluation_enabled() above. While false, nothing under
    artifacts/reports/ is ever written and every other artifact the
    protocol_execution branch produces is untouched."""
    cfg = _orchestrator_config(cfg)
    return _strict_orchestrator_flag("category_reports", cfg=cfg)  # E-061 C1.5: strict


# delivery_plan_v26.md 0.2 (item 2) -- config/profitability_bars.yaml and the
# branch-3 stop. Off-by-default flag, same shape as _grid_evaluation_enabled()
# above. See config/campaign_config.yaml's orchestrator.profit_bars_file.enabled
# comment for the full rationale.
def _profit_bars_file_enabled(cfg: dict | None = None) -> bool:
    """False (no behavior change) when the key, the section, or the file is
    absent -- same silence-is-never-a-green-light rule as
    _grid_evaluation_enabled() above. While false, _dispatch_verdict_route's
    promote branch is untouched: _write_promotion_audit runs and the branch
    unconditionally returns "holdout_evaluation", exactly as before this
    feature existed -- artifacts/profit_bars_evaluation.yaml is never written
    and config/profitability_bars.yaml is never read."""
    cfg = _orchestrator_config(cfg)
    return _strict_orchestrator_flag("profit_bars_file", cfg=cfg)  # E-061 C1.5: strict


# Branch 3 on every backtest (operator-approved 2026-09-24; delivery_plan_v26.md
# target row "8 · profit bars ... one file, every backtest, stop rule"). See
# config/campaign_config.yaml's orchestrator.profit_bars_every_backtest.enabled.
def _profit_bars_every_backtest_enabled(cfg: dict | None = None) -> bool:
    """False when the key, the section or the config file is absent. A non-bool
    value raises. Requires orchestrator.profit_bars_file.enabled AND
    orchestrator.regroup_record.enabled (hence specialist_readers): raises,
    loudly, if this flag is on without them. run_loop resolves it once, in its
    pre-flight, so a misconfiguration fails the run before any spend.

    While false: nothing new is read or written, and the promote-path check
    (_dispatch_verdict_route -> _evaluate_profit_bars) runs exactly as before.
    While true: _evaluate_profit_bars_every_backtest grades every tested variant
    of the attempt right after protocol_execution (never pausing there);
    regroup_record records the per-variant results in the campaign memory; the
    route after it raises profit_bars_reached (_profit_bars_stop_route). The
    promote path skips its own evaluation only for a run holding that
    every_backtest evaluation (see the coexistence note in
    _dispatch_verdict_route)."""
    cfg = _orchestrator_config(cfg)
    pbe_cfg = ((cfg.get("orchestrator") or {}).get("profit_bars_every_backtest") or {})
    value = pbe_cfg.get("enabled", False)
    if not isinstance(value, bool):
        raise ValueError(
            f"orchestrator.profit_bars_every_backtest.enabled={value!r} is not a real "
            f"boolean (got {type(value).__name__}) -- write an unquoted `true` or `false` "
            f"in config/campaign_config.yaml, not a quoted string or null."
        )
    if value and not _flag_dep(_profit_bars_file_enabled, cfg):
        raise ValueError(
            "orchestrator.profit_bars_every_backtest.enabled=true requires "
            "orchestrator.profit_bars_file.enabled=true as well -- the per-backtest check "
            "grades every variant against config/profitability_bars.yaml, which is only "
            "read under that flag. Enable both, or neither."
        )
    if value and not _flag_dep(_regroup_record_enabled, cfg):
        # Code review 2026-09-24 (order judge -> learn -> profit check -> regroup +
        # record -> decide): the stop is raised in the route AFTER regroup_record,
        # which itself requires specialist_readers (and grid_evaluation +
        # category_reports) -- _regroup_record_enabled raises on those.
        raise ValueError(
            "orchestrator.profit_bars_every_backtest.enabled=true requires "
            "orchestrator.regroup_record.enabled=true as well (and therefore "
            "specialist_readers, grid_evaluation and category_reports) -- the profit "
            "result is recorded in the campaign memory by regroup_record and the "
            "profit_bars_reached stop is raised in the route after it."
        )
    return value


# Required fields and their expected types for config/profitability_bars.yaml.
# Kept as a module-level constant so the schema is visible in one place and the
# loader below (and its tests) can iterate it instead of repeating field names.
_PROFITABILITY_BARS_SCHEMA = {
    "sharpe_min":                 (int, float),
    "max_drawdown_pct_max":       (int, float),
    "avg_daily_return_min":       (int, float),
    "trade_count_min":            (int,),
    "deflated_sharpe_threshold":  (int, float),
    "target_instrument_set":      (list,),
    "ratified_by":                (str, type(None)),
    "ratified_at":                (str, type(None)),
}


class ProfitabilityBarsSchemaError(ValueError):
    """Raised by _load_profitability_bars on any missing or wrong-typed field --
    deliberately loud (a silently-defaulted threshold would make branch-3 pass/fail
    verdicts meaningless without anyone knowing the config was malformed)."""


def _load_profitability_bars(path: Path | None = None) -> dict:
    """Load and schema-validate config/profitability_bars.yaml. Raises
    ProfitabilityBarsSchemaError loudly on any missing field, wrong type, or an
    unparseable/empty file -- never silently defaults a threshold. `path` is
    overridable for tests; defaults to ROOT / "config" / "profitability_bars.yaml"."""
    bars_path = path if path is not None else (ROOT / "config" / "profitability_bars.yaml")
    if not bars_path.exists():
        raise ProfitabilityBarsSchemaError(f"{bars_path} does not exist.")
    with open(bars_path, encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    if not isinstance(doc, dict):
        raise ProfitabilityBarsSchemaError(
            f"{bars_path} did not parse to a mapping (got {type(doc).__name__})."
        )

    missing = [k for k in _PROFITABILITY_BARS_SCHEMA if k not in doc]
    if missing:
        raise ProfitabilityBarsSchemaError(
            f"{bars_path} is missing required field(s): {sorted(missing)}."
        )

    wrong_type = []
    for key, expected_types in _PROFITABILITY_BARS_SCHEMA.items():
        value = doc[key]
        # bool is a subclass of int in Python -- explicitly reject it for the
        # numeric fields so `sharpe_min: true` doesn't silently pass as 1.
        if isinstance(value, bool) and bool not in expected_types:
            wrong_type.append(f"{key} (got bool {value!r}, expected {expected_types})")
        elif not isinstance(value, expected_types):
            wrong_type.append(f"{key} (got {type(value).__name__}, expected {expected_types})")
    if wrong_type:
        raise ProfitabilityBarsSchemaError(
            f"{bars_path} has wrong-typed field(s): {'; '.join(wrong_type)}."
        )

    if not doc["target_instrument_set"]:
        raise ProfitabilityBarsSchemaError(
            f"{bars_path}'s target_instrument_set is empty -- must list at least one symbol."
        )

    return doc


# E-054 Layer 2 "on by default" (delivery_plan_v26.md s:0.4 item 14,
# 2026-09-20). Replaces the old _E054_GATE_ENABLED env var
# (E054_DATA_AVAILABILITY_GATE=1). Same config-loading shape as
# _grid_evaluation_enabled() above -- but the DEFAULT is inverted.
def _data_availability_gate_enabled(cfg: dict | None = None) -> bool:
    """True (gate runs) when the key, the section, or the config file itself
    is missing -- the ONE flag in this module that defaults ON instead of
    off. Every other flag here (_grid_evaluation_enabled,
    _exclusion_digest_input_enabled, _stale_input_path_fix_enabled, ...)
    follows "silence is never a green light" and defaults False on a
    missing key/section/file. This flag is the deliberate exception: E-054
    Layer 2 is complete and tested (shipped 2026-09-11), and the operator's
    own brief (delivery_plan_v26.md s:0.4 item 14) requires this control to
    run for every hypothesis by default, not opt-in. An explicit
    `orchestrator.data_availability_gate.enabled: false` in
    config/campaign_config.yaml still disables it and reproduces, byte for
    byte, the behavior of the old unset E054_DATA_AVAILABILITY_GATE env var
    (backtest_specification -> protocol_execution, data_availability_gate
    stage never routed to) -- see
    tests/test_e054_stage_wiring.py's explicit-off case."""
    cfg = _orchestrator_config(cfg)
    dag_cfg = ((cfg.get("orchestrator") or {}).get("data_availability_gate") or {})
    value = dag_cfg.get("enabled", True)
    # CODE-REVIEW FIX (2026-09-21): bool(value) silently mis-coerces two real
    # config-authoring mistakes -- a quoted "false" string (bool("false") is
    # True, so the gate stays ON when the author believed they'd disabled
    # it) and an explicit `enabled:` / `enabled: null` (bool(None) is False,
    # silently disabling this file's ONE inverted-default, deliberately-ON
    # flag instead of the "missing key" case the docstring above actually
    # promises True for). Because this is that one exception, a coercion
    # mistake here is uniquely dangerous in a direction the sibling
    # off-by-default flags (e.g. _grid_evaluation_enabled) don't share.
    # Fail loud on anything that isn't a real YAML bool rather than guess.
    if not isinstance(value, bool):
        raise ValueError(
            f"orchestrator.data_availability_gate.enabled={value!r} is not a real "
            f"boolean (got {type(value).__name__}) -- write an unquoted `true` or "
            f"`false` in config/campaign_config.yaml, not a quoted string or null. "
            f"Refusing to guess on the one flag in this file that defaults ON."
        )
    return value


# E-046b S2 routing (delivery_plan_v26.md slice 2, "until slice 6c"):
# validated -> promote, refuted -> kill/terminate, inconclusive -> human_pause
# (reason: inconclusive_grid). (result, hypothesis_verdict, lineage_routing).
_GRID_IDEA_STATUS_ROUTING = {
    "validated":    ("PASS", "promote", None),
    "refuted":      ("FAIL", "kill", "terminate"),
    "inconclusive": ("INCONCLUSIVE", "human_pause", "inconclusive_grid"),
}


def _build_idea_status_artifact(grid_result: dict, run_id: str) -> dict:
    """Written in the SAME shape pass_rule_evaluation.yaml uses when it
    carries a binding verdict (result / hypothesis_verdict / lineage_routing)
    so a LATER slice can pass this artifact as _resolve_verdict_fields()'s
    own `pre_eval` argument exactly like pass_rule_evaluation.yaml already
    is -- that function only binds when result is 'PASS' or 'FAIL', so only
    validated/refuted are mechanically binding through it; inconclusive
    deliberately does NOT bind (a human decides, not a formula), which is
    why its own `result` here is 'INCONCLUSIVE', not 'PASS'/'FAIL'.

    THIS SLICE DOES NOT WIRE THIS ARTIFACT INTO ANY _resolve_verdict_fields
    CALL SITE -- no existing routing behavior changes when this function
    runs. That repointing is slice 6c's own scope (S1_FINDINGS.md §6)."""
    idea_status = grid_result.get("idea_status")
    routing = _GRID_IDEA_STATUS_ROUTING.get(idea_status)
    if routing is None:
        raise ValueError(f"grid_result idea_status={idea_status!r} is not one of "
                          f"{sorted(_GRID_IDEA_STATUS_ROUTING)} -- evaluate_grid's own contract "
                          f"was violated")
    result, hypothesis_verdict, lineage_routing = routing
    return {
        "run_id": run_id,
        "idea_status": idea_status,
        "result": result,
        "hypothesis_verdict": hypothesis_verdict,
        "lineage_routing": lineage_routing,
        "grid_evaluation_ref": f"runs/{run_id}/artifacts/grid_evaluation.yaml",
        "reason": grid_result.get("reason"),
    }


def _exclusion_digest_input_enabled(cfg: dict | None = None) -> bool:
    """False (no behavior change) when the key, the section, or the file is
    absent -- silence is never a green light, mirroring
    run_campaign._quarantine_enabled()'s own rule verbatim. Reads via ROOT
    (not a source-file-relative path) for the same reason that function
    does: so the test sandbox (tests/conftest.py's autouse guard patches
    ROOT) can seed its own value without touching the real repository."""
    cfg = _orchestrator_config(cfg)
    return _strict_orchestrator_flag("exclusion_digest_input", cfg=cfg)  # E-061 C1.5: strict


def _apply_exclusion_digest_input(stage_name: str, handoff: dict, run_dir: Path) -> None:
    """Union "what was already tried" into handoff['optional_inputs'] for the
    two generating stages, ONLY when the flag is on -- deduplicated, same
    skip-gracefully-on-absence discipline as _apply_b7_mandatory_inputs.
    optional_inputs (not required_inputs): a missing input must never crash a
    stage that predates this feature.

    Which input (E-036 S2a):
      * campaign_record/campaign_memory.yaml exists -> artifacts/tried_ideas.yaml,
        derived here (tools/campaign_memory.tried_ideas) and written into the
        run before the stage reads it, so the run keeps exactly what the
        model was shown. The legacy digest is NOT also fed. A malformed
        memory raises (CampaignMemoryError), never silently skipped.
      * no memory file -> campaign_record/exclusion_digest.yaml, exactly as
        before E-036 S2a (same path, same reason, skipped when the file is
        missing): byte-identical default prompt input.

    Flag OFF: this function is a no-op -- the handoff dict is never mutated
    and nothing is written, so _build_stage_prompt's assembled prompt text is
    byte-identical to before this function existed
    (tests/test_exclusion_digest_input.py)."""
    if stage_name not in _EXCLUSION_DIGEST_INPUT_STAGES:
        return
    if not _exclusion_digest_input_enabled():
        return
    memory_path = ROOT / "campaign_record" / "campaign_memory.yaml"
    if memory_path.exists():
        import campaign_memory as _cm_mod  # tools/ sibling (tools/ is on sys.path, module top)
        view = _cm_mod.tried_ideas(_cm_mod.load_memory(memory_path), root=ROOT)
        save_yaml(run_dir / _TRIED_IDEAS_RELATIVE_PATH, view)
        path, reason = _TRIED_IDEAS_RELATIVE_PATH, _TRIED_IDEAS_REASON
    elif (run_dir / _EXCLUSION_DIGEST_RELATIVE_PATH).exists():
        path, reason = _EXCLUSION_DIGEST_RELATIVE_PATH, _EXCLUSION_DIGEST_REASON
    else:
        return
    optional = handoff.setdefault("optional_inputs", [])
    if path in {req["path"] for req in optional}:
        return
    optional.append({"path": path, "reason": reason})


# E-032 S2b: two of hypothesis_generation's OWN declared optional_inputs
# (research_brief_to_hypothesis.yaml) point at paths that have never resolved,
# for the same reason and since the same commit -- the E-002 restructure
# (8f162fa6, 2026-08-06) moved campaign_knowledge_base.yaml and
# feed_wishlist.yaml from the strategy-research/ root into campaign_record/,
# and the "../../<name>.yaml" references in this one template were never
# repointed. Both are OPTIONAL, so run_claude_worker's context-gathering loop
# has always treated the miss as silent absence (no error) -- this is the
# specific instance of the general defect the new warning above now surfaces.
#
# A same-day scan of every "../../..." path across workflow_artifacts/templates/
# handoffs/*.yaml found this is not isolated to hypothesis_generation:
# campaign_review.yaml has the identical stale-path bug on TWO REQUIRED
# inputs (../../campaign_state.yaml, ../../campaign_knowledge_base.yaml --
# both belong under campaign_record/), and protocol_to_verdict_interpreter.yaml
# has it on one optional input (../../coin_universe.yaml, belongs under
# config/). Those three are NOT fixed here: campaign_review's inputs being
# required means a fix there is a behavior-enabling change to a stage that is
# currently guaranteed to crash if ever triggered live (S1: its own output is
# orphaned, next: [] -- no run has actually invoked it since before the
# restructure, per runs/run_054 predating 8f162fa6), and
# verdict_interpreter is outside E-032's two generating stages entirely. Both
# are a distinct pre-existing bug in stages this epic does not own; fixing
# them belongs to whoever owns campaign_review/verdict_interpreter next, not
# to this story. [CUL-336, 2026-09-27: the verdict_interpreter template entry
# was removed; _apply_closed_book_inputs now supplies config/coin_universe.yaml
# and campaign_record/campaign_state.yaml to that stage. campaign_review's two
# required stale paths are still as described here.] (A structurally identical but separate defect exists in
# run_gemini_worker's own, un-refactored copy of the context-gathering loop:
# it has no `else` at all, so it silently skips even a MISSING REQUIRED input
# instead of raising. Not touched here either -- assigned_engine is "claude"
# on every template this repo currently ships, so that path is dead code in
# practice, and fixing an unexercised alternate engine is its own story.)
#
# Restoring either path changes what hypothesis_generation actually reads --
# real KB/wishlist content it has never seen -- so, per the same discipline
# S2a used for the exclusion digest, this is gated off by default and proven
# byte-identical at flag-off via _build_stage_prompt
# (tests/test_stale_input_path_fix.py).
_STALE_INPUT_PATH_FIXES = {
    "hypothesis_generation": {
        "../../campaign_knowledge_base.yaml": "../../campaign_record/campaign_knowledge_base.yaml",
        "../../feed_wishlist.yaml": "../../campaign_record/feed_wishlist.yaml",
    },
}


def _stale_input_path_fix_enabled(cfg: dict | None = None) -> bool:
    """False when the key, the section, or the config file is absent -- same
    silence-is-never-a-green-light rule as _exclusion_digest_input_enabled()
    and run_campaign._quarantine_enabled(). Reads via ROOT so the test
    sandbox (tests/conftest.py's autouse guard) can seed its own value."""
    cfg = _orchestrator_config(cfg)
    return _strict_orchestrator_flag("stale_input_path_fix", cfg=cfg)  # E-061 C1.5: strict


def _apply_stale_input_path_fix(stage_name: str, handoff: dict) -> None:
    """Rewrite any optional_inputs path that matches a known-stale entry in
    _STALE_INPUT_PATH_FIXES to its correct, post-E-002-restructure location --
    IN PLACE, and ONLY when the flag is on. Never touches required_inputs
    (none of the known stale paths on the two generating stages are
    required -- campaign_review's required-input instances are deliberately
    out of scope, see the comment above) and never adds an entry the template
    does not already declare, so this corrects exactly the known-broken
    paths rather than becoming a general path-repair pass.

    Flag OFF (the default): no-op -- the handoff dict is never mutated, so
    _build_stage_prompt's assembled prompt is byte-identical to before this
    function existed (tests/test_stale_input_path_fix.py, same acceptance
    bar as _apply_exclusion_digest_input)."""
    fixes = _STALE_INPUT_PATH_FIXES.get(stage_name)
    if not fixes:
        return
    if not _stale_input_path_fix_enabled():
        return
    for req in handoff.get("optional_inputs", []):
        corrected = fixes.get(req.get("path"))
        if corrected:
            req["path"] = corrected


# ---------------------------------------------------------------------------
# E-056 Slice 3b (config-direct authoring). OFF BY DEFAULT, same shape as
# every other orchestrator.<name>.enabled flag above (silence is never a
# green light). When on:
#   - hypothesis_generation routes to the new strategy_config_authoring stage
#     instead of straight to innovation_expansion (see run_loop).
#   - hypothesis_generation and innovation_expansion each receive one new
#     file-presence signal in required_inputs (see _apply_config_direct_
#     authoring_context below) -- the LLM cannot read this config flag
#     directly, so its effect on a skill's own behavior is always signaled
#     by which files are present in context, the same convention
#     _apply_exclusion_digest_input/_apply_stale_input_path_fix already use.
#   - innovation_expansion's ADMIT routing target becomes backtest_specification
#     instead of validation (validation becomes naturally unreached, not
#     deleted -- see run_loop's innovation_expansion branch).
#   - backtest_specification joins async_invoke_agent's tool_stages set,
#     becoming a deterministic run_tool_worker branch instead of an LLM call.
# ---------------------------------------------------------------------------

_CONFIG_DIRECT_AUTHORING_CONTEXT_STAGES = {"hypothesis_generation", "innovation_expansion"}


def _config_direct_authoring_enabled(cfg: dict | None = None) -> bool:
    """False (no behavior change) when the key, the section, or the config
    file is absent -- same silence-is-never-a-green-light rule as
    _exclusion_digest_input_enabled()/_stale_input_path_fix_enabled() above
    (this is NOT the one inverted-default flag in this file -- that is
    _data_availability_gate_enabled() alone; see its own docstring for why
    it's the deliberate exception)."""
    cfg = _orchestrator_config(cfg)
    cda_cfg = ((cfg.get("orchestrator") or {}).get("config_direct_authoring") or {})
    value = cda_cfg.get("enabled", False)
    # CODE-REVIEW FIX (2026-09-21): bool(value) silently mis-coerces a quoted
    # "false" string (bool("false") is True) -- the exact trap
    # _data_availability_gate_enabled() in this same file was already
    # patched to fail loudly on instead of guessing. This flag is
    # off_incomplete and unproven against a real LLM pass; a config-authoring
    # slip that reads as truthy would silently activate the whole reshaped
    # pipeline (new stage routing, tool-only backtest_specification, the
    # validation stage skip). Fail loud on anything that isn't a real bool.
    if not isinstance(value, bool):
        raise ValueError(
            f"orchestrator.config_direct_authoring.enabled={value!r} is not a real "
            f"boolean (got {type(value).__name__}) -- write an unquoted `true` or "
            f"`false` in config/campaign_config.yaml, not a quoted string or null."
        )
    return value


def _variant_loop_enabled(cfg: dict | None = None) -> bool:
    """E-033.1 Slice 4a (delivery_plan_v26.md Slice 4, sub-slice 1 of 2: "loop
    restructure + trial accounting"). False (no behavior change) when the
    key, the section, or the config file is absent -- same silence-is-never-
    a-green-light rule as _config_direct_authoring_enabled() above (this is
    NOT the one inverted-default flag in this file -- that is
    _data_availability_gate_enabled() alone; see its own docstring for why
    it's the deliberate exception).

    Structurally requires config_direct_authoring to be on too:
    artifacts/variants/index.yaml (the file run_tool_worker's protocol_execution
    per-variant loop reads under this flag) is ONLY EVER written by
    config-direct authoring's own tool-only backtest_specification branch
    (E-056 Slice 3b) -- with that flag off, the file structurally cannot
    exist. Raises loudly (not a silent no-op) if variant_loop.enabled=true
    is set while config_direct_authoring.enabled is false or absent --
    S1_FINDINGS.md §9 flagged this exact hard-dependency as a real invalid-
    config state, not a redundant flag."""
    cfg = _orchestrator_config(cfg)
    vl_cfg = ((cfg.get("orchestrator") or {}).get("variant_loop") or {})
    value = vl_cfg.get("enabled", False)
    # Same "fail loud on anything that isn't a real bool" rule
    # _config_direct_authoring_enabled() above already established for this
    # module -- a quoted "false" string must never silently read truthy.
    if not isinstance(value, bool):
        raise ValueError(
            f"orchestrator.variant_loop.enabled={value!r} is not a real "
            f"boolean (got {type(value).__name__}) -- write an unquoted `true` or "
            f"`false` in config/campaign_config.yaml, not a quoted string or null."
        )
    if value and not _flag_dep(_config_direct_authoring_enabled, cfg):
        raise ValueError(
            "orchestrator.variant_loop.enabled=true requires "
            "orchestrator.config_direct_authoring.enabled=true as well -- "
            "artifacts/variants/index.yaml (which the variant loop reads) is only "
            "ever written by config-direct authoring's own tool-only "
            "backtest_specification branch (E-056 Slice 3b); with config-direct "
            "authoring off, that file structurally cannot exist. Enable both "
            "flags together, not variant_loop alone."
        )
    return value


# ---------------------------------------------------------------------------
# E-046a Slice 5b-ii-B -- the specialist_readers stage and the interim route
# from the grid (delivery_plan_v26.md slices 2 and 5; S1_FINDINGS_5B_II.md
# §2-§4 and its REALIGNMENT section). OFF BY DEFAULT. When on:
#   - protocol_execution routes to specialist_readers instead of
#     verdict_interpreter (verdict_interpreter stays registered, unreached --
#     the validation/config-direct-authoring precedent, not a deletion).
#   - specialist_readers runs the five reader skills one after another. Each
#     sees ONLY its own artifacts/reports/<category>.yaml plus
#     artifacts/grid_evaluation.yaml and writes artifacts/proposals/
#     <category>.yaml through run_reader_worker, which owns that explicit
#     output path (run_claude_worker's shared filename regex is untouched).
#   - the route after the stage comes from the grid ONLY: a component-error
#     check on protocol_result.yaml first (an engineering fault makes the grid
#     meaningless), then idea_status.yaml through the existing binding path
#     (_resolve_verdict_fields -> _dispatch_verdict_route). The proposals'
#     scores are never read here -- they rank the next candidate in the later
#     decide-next step (slice 6b), and nothing else.
# Nothing here reintroduces refine/pivot/escalate routing, the per-family
# circuit breaker, hypothesis_family, or continuation children (all retired
# in slice 6c): the route is only ever promote, kill/terminate or a pause.
# ---------------------------------------------------------------------------

def _specialist_readers_enabled(cfg: dict | None = None) -> bool:
    """False (no behavior change) when the key, the section, or the config
    file is absent -- same silence-is-never-a-green-light rule as
    _config_direct_authoring_enabled(). A non-bool value raises (a quoted
    "false" must never read truthy). Structurally requires
    orchestrator.grid_evaluation.enabled (the route reads idea_status.yaml,
    which only the grid writes) and orchestrator.category_reports.enabled
    (each reader reads its artifacts/reports/<category>.yaml, which only the
    report builder writes): raises, loudly, if this flag is on while either
    is off -- with either off the stage could only fail later, after spend,
    or route on a guess."""
    cfg = _orchestrator_config(cfg)
    sr_cfg = ((cfg.get("orchestrator") or {}).get("specialist_readers") or {})
    value = sr_cfg.get("enabled", False)
    if not isinstance(value, bool):
        raise ValueError(
            f"orchestrator.specialist_readers.enabled={value!r} is not a real "
            f"boolean (got {type(value).__name__}) -- write an unquoted `true` or "
            f"`false` in config/campaign_config.yaml, not a quoted string or null."
        )
    if value:
        missing = [name for name, on in (
                       ("grid_evaluation", _flag_dep(_grid_evaluation_enabled, cfg)),
                       ("category_reports", _flag_dep(_category_reports_enabled, cfg)))
                   if not on]
        if missing:
            raise ValueError(
                "orchestrator.specialist_readers.enabled=true requires "
                + " and ".join(f"orchestrator.{m}.enabled=true" for m in missing)
                + " as well -- the readers read artifacts/reports/<category>.yaml "
                "(written only under category_reports) and the route reads "
                "artifacts/idea_status.yaml (written only under grid_evaluation). "
                "Enable all three together."
            )
    return value


_SPECIALIST_READERS_HANDOFF = "protocol_to_specialist_readers.yaml"
_READER_OUTPUT_BLOCK_RE = re.compile(r"```ya?ml[^\n]*\n(.*?)```", re.DOTALL)

# Artifacts that must come from the CURRENT protocol_execution attempt under
# specialist_readers (code-review fix 1). Cleared at protocol_execution entry.
_SPECIALIST_READERS_RUN_SCOPED_FILES = ("idea_status.yaml", "grid_evaluation.yaml")
_SPECIALIST_READERS_RUN_SCOPED_DIRS = ("reports", "proposals")


def _clear_specialist_readers_artifacts(run_dir: Path) -> None:
    """Delete idea_status.yaml, grid_evaluation.yaml, reports/ and proposals/
    (plus stale reader debug dumps) so a protocol_execution re-run can never
    route on, or skip readers because of, a previous attempt's output. Called
    only under the flag, at protocol_execution entry."""
    arts = run_dir / "artifacts"
    removed = []
    for name in _SPECIALIST_READERS_RUN_SCOPED_FILES:
        if (arts / name).exists():
            (arts / name).unlink()
            removed.append(name)
    for name in _SPECIALIST_READERS_RUN_SCOPED_DIRS:
        if (arts / name).exists():
            shutil.rmtree(arts / name)
            removed.append(f"{name}/")
    for dbg in arts.glob("debug_specialist_readers_*_raw_output.txt") if arts.exists() else []:
        dbg.unlink()
        removed.append(dbg.name)
    if removed:
        print(f"🧹 [E-046a] protocol_execution re-run: cleared previous attempt's {removed}")


def _raise_specialist_readers_prereq_errors(errors: list) -> None:
    """Under specialist_readers the grid and the reports are prerequisites, not
    optional extras: a failure in either fails protocol_execution (after its
    trial rows are recorded) instead of being logged and swallowed."""
    if errors:
        raise RuntimeError(
            "orchestrator.specialist_readers.enabled requires the grid and the category "
            "reports, and protocol_execution could not produce them: " + "; ".join(errors))


def _refresh_regime_detector_report_for_readers(run_id: str, run_dir: Path) -> None:
    """_ensure_regime_detector_report used to run only from the
    verdict_interpreter branch, which is unreached under the flag. Run it
    before build_reports so regime_power.yaml is built from a fresh detector
    report; if one cannot be produced, fail rather than build from a stale or
    missing one."""
    if _ensure_regime_detector_report(run_id, run_dir) is None:
        raise RuntimeError("regime_detector_report.yaml could not be produced or refreshed "
                           "(see the message above) -- refusing to build regime_power.yaml "
                           "from a stale or missing detector report")


def _check_specialist_readers_preflight(run_dir: Path) -> None:
    """Before any spend under the flag: pre_registration.yaml must carry a
    menu-shaped pass_rule, or the grid is never evaluated and the run would
    only fail after a full backtest and a trial row."""
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import verdict_criteria_evaluator as _vce
    path = run_dir / "artifacts" / "pre_registration.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} is missing -- orchestrator.specialist_readers.enabled routes only from "
            f"the grid, which needs a pre-registered, menu-shaped pass_rule.")
    if not _vce._is_menu_shaped_pass_rule(_vce._find_pass_rule(load_yaml(path) or {})):
        raise ValueError(
            f"{path}: pass_rule is not menu-shaped (no criterion carries source/reducer) -- "
            f"the grid cannot evaluate it, so under orchestrator.specialist_readers.enabled "
            f"this run could only fail after its backtest. Refusing before any spend.")


def _reader_categories() -> list:
    """The five categories, from tools/build_reports.py::REPORT_CATEGORIES --
    one source of truth shared with the report builder (Slice 5a)."""
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import build_reports as _br
    return list(_br.REPORT_CATEGORIES)


def _reader_proposals_module():
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import reader_proposals as _rp
    return _rp


def _reader_skill_dir(category: str) -> str:
    """Skill directory under workflow_artifacts/skills/ for one category."""
    return f"readers/{category}-reader"


def _ensure_specialist_readers_handoff(run_id: str, run_dir: Path) -> Path:
    """Write the stage-level handoff run_loop loads for specialist_readers,
    once. Created lazily at stage entry (not in _create_remaining_handoffs),
    so flag-off runs never get this file. Its only required input is
    protocol_result.yaml -- the component-error check runs before any
    reader, and each reader's own inputs are checked per reader."""
    handoff_path = run_dir / "handoffs" / _SPECIALIST_READERS_HANDOFF
    if not handoff_path.exists():
        save_yaml(handoff_path, {
            "handoff_version": 1, "run_id": run_id,
            "from_stage": "protocol_execution", "to_stage": "specialist_readers",
            "assigned_engine": "claude",
            "objective": (
                "E-046a: run the five specialist readers, one after another. Each "
                "reads only its own artifacts/reports/<category>.yaml plus "
                "artifacts/grid_evaluation.yaml and proposes evidence-grounded "
                "changes to artifacts/proposals/<category>.yaml. Readers never "
                "decide or route; the route comes from artifacts/idea_status.yaml."
            ),
            "required_inputs": [
                {"path": "artifacts/protocol_result.yaml",
                 "reason": "component-error check, before any reader runs"},
            ],
            "deliverables": [f"proposals/{c}.yaml" for c in _reader_categories()],
        })
    return handoff_path


def _protocol_component_errors(run_dir: Path) -> list:
    """Every results[*] entry whose component_errors.count > 0, in
    artifacts/protocol_result.yaml and (variant loop) in each
    artifacts/variants/<id>/protocol_result.yaml -- the grid reads every
    variant, so an error in any of them makes it meaningless. Missing
    protocol_result.yaml, or a present but malformed component_errors block,
    raises: an unreadable error count is not a zero one. An absent/null
    block (component_errors off for that window) counts as none.

    The body lives in tools/campaign_memory.protocol_component_errors (E-036
    S2b: shared with tools/replay_repeat_gate.py); this orchestrator reads the
    files with its own load_yaml, exactly as before."""
    return _campaign_memory_module().protocol_component_errors(run_dir, load=load_yaml)


def _load_idea_status(run_dir: Path, run_id: str) -> dict:
    """artifacts/idea_status.yaml, validated -- raises on anything that is not
    exactly what _build_idea_status_artifact writes for this run. The route
    under specialist_readers is never guessed: a missing, unparseable, stale
    (other run_id) or internally inconsistent file stops the run."""
    path = run_dir / "artifacts" / "idea_status.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} is missing -- under orchestrator.specialist_readers.enabled the "
            f"route comes only from the grid. It is written by protocol_execution when "
            f"grid_evaluation is on AND the pass_rule is menu-shaped; check that run's "
            f"protocol_execution log for a grid-evaluation warning. Refusing to guess a route.")
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"{path}: unparseable YAML ({exc})") from exc
    if not isinstance(doc, dict):
        raise ValueError(f"{path}: expected a mapping, got {type(doc).__name__}")
    status = doc.get("idea_status")
    expected = _GRID_IDEA_STATUS_ROUTING.get(status)
    if expected is None:
        raise ValueError(f"{path}: idea_status={status!r} is not one of "
                         f"{sorted(_GRID_IDEA_STATUS_ROUTING)}")
    found = (doc.get("result"), doc.get("hypothesis_verdict"), doc.get("lineage_routing"))
    if found != expected:
        raise ValueError(f"{path}: (result, hypothesis_verdict, lineage_routing)={found} "
                         f"disagrees with idea_status={status!r}'s fixed mapping {expected}")
    if doc.get("run_id") != run_id:
        raise ValueError(f"{path}: run_id={doc.get('run_id')!r} is not this run ({run_id!r}) "
                         f"-- a copied or stale grid result")
    return doc


def _idea_hypothesis_id(run_dir: Path) -> str:
    """The idea's identity under specialist_readers: hypothesis_card.yaml's
    hypothesis_id (written by hypothesis_generation; verdict_interpretation.yaml
    only ever restated it). Raises when absent -- falling back to the run_id
    would let one hypothesis spend the single-use holdout twice under two run
    ids."""
    card = load_yaml(run_dir / "artifacts" / "hypothesis_card.yaml") or {}
    hyp_id = card.get("hypothesis_id")
    if not isinstance(hyp_id, str) or not hyp_id.strip():
        raise ValueError(f"{run_dir / 'artifacts' / 'hypothesis_card.yaml'} has no hypothesis_id "
                         f"-- cannot identify the idea for promotion/holdout accounting")
    return hyp_id


def _reader_handoff(category: str, run_id: str, stage_attempt) -> dict:
    """The per-reader handoff, built in memory. Its only inputs are this
    category's report and the grid -- deliberately none of the stage-wide
    unions (B7 pre-registration, exclusion digest, config-direct context):
    each reader's SKILL.md scopes it to exactly these two files."""
    return {
        "handoff_version": 1, "run_id": run_id,
        "from_stage": "protocol_execution", "to_stage": "specialist_readers",
        "reader_category": category,
        "assigned_engine": "claude",
        "objective": (f"Read artifacts/reports/{category}.yaml (and artifacts/grid_evaluation.yaml) "
                      f"and propose zero or more evidence-grounded changes. Output a single YAML "
                      f"list (`[]` for none) -- it is written to "
                      f"artifacts/proposals/{category}.yaml."),
        "required_inputs": [
            {"path": f"artifacts/reports/{category}.yaml", "reason": f"the {category} report"},
            {"path": "artifacts/grid_evaluation.yaml", "reason": "the grid's per-criterion result"},
        ],
        "deliverables": [f"proposals/{category}.yaml"],
        "injected_context": {"stage_attempt": str(stage_attempt),
                             "feed_names": _reader_feed_vocabulary()},
    }


FEED_WISHLIST_REL = "campaign_record/feed_wishlist.yaml"


def _reader_feed_vocabulary() -> dict:
    """E-035 S2c: the canonical names a reader's `requires_feed.feed` must use
    when one fits, so readers do not invent synonyms:
      wired         -- FEED_REGISTRY keys (usable today);
      reserved      -- RESERVED_FEED_REGISTRY keys (need a data-policy designation);
      wishlist_only -- feed_name entries of campaign_record/feed_wishlist.yaml
                       not in either registry (named, never built).
    Built for every reader call, so it never raises: an unreadable registry
    or wishlist is reported in the dict (and printed) instead -- a campaign
    whose readers never ask for a feed must not stop on the registry's
    syntax. The router (_route_reader_feed_requests) reads the registry again
    and fails loud when a proposal does carry requires_feed."""
    import decide_next as _dn  # tools/ sibling (on sys.path, module top)
    out = {"rule": ("Set requires_feed.feed to one of these names when one fits; coin a new "
                    "lowercase snake_case name only when none does, never a synonym of a "
                    "listed one. wishlist_only names are wishlist entries, not wired feeds.")}
    try:
        reg = _dn.load_feed_registry(_TRADING_BOT_ROOT)
        out["wired"], out["reserved"] = reg["wired"], reg["reserved"]
    except _dn.DecideNextError as exc:
        print(f"⚠️ WARNING: reader feed names: feed registry unreadable: {exc}")
        reg = {"wired": [], "reserved": []}
        out["registry_error"] = str(exc)
    wishlist = []
    path = ROOT / FEED_WISHLIST_REL
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
        for item in (doc or {}).get("wishlist") or []:
            name = item.get("feed_name") if isinstance(item, dict) else None
            if isinstance(name, str) and name not in wishlist:
                wishlist.append(name)
    except (OSError, yaml.YAMLError, AttributeError) as exc:
        print(f"⚠️ WARNING: reader feed names: {FEED_WISHLIST_REL} unreadable: {exc}")
        out["wishlist_error"] = str(exc)
    known = set(reg["wired"]) | set(reg["reserved"])
    out["wishlist_only"] = sorted(n for n in wishlist if n not in known)
    return out


async def _invoke_reader_llm(prompt: str) -> tuple:
    """One reader's LLM call. Returns (text, meta). Split out so tests can
    replace the model without touching prompt building, parsing or writing.
    Same options helper as run_claude_worker (_stage_agent_options, CUL-336)."""
    agent_output = ""
    usage, total_cost, num_turns = {}, 0.0, None
    async for message in query(prompt=prompt, options=_stage_agent_options()):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    agent_output += block.text
        if hasattr(message, "total_cost_usd"):
            usage = getattr(message, "usage", {}) or {}
            total_cost = getattr(message, "total_cost_usd", 0.0)
            num_turns = getattr(message, "num_turns", None)
    return agent_output, {"usage": usage, "cost_usd": total_cost, "num_turns": num_turns}


class _ReaderBudgetExceeded(RuntimeError):
    """Raised inside the reader loop when the run's weighted token budget is
    already spent. run_loop turns it into the same terminal
    rejected_budget_exceeded outcome as its own loop-top budget check."""


def _check_reader_budget(run_dir: Path, category: str) -> None:
    state = load_yaml(run_dir / "pipeline_state.yaml") or {}
    used, _ = _compute_weighted_budget_usage(state.get("audit_log", {}))
    budget = _load_token_budget()
    if used > budget:
        raise _ReaderBudgetExceeded(
            f"Weighted token budget exceeded before the {category} reader "
            f"({used:,.0f} > {budget:,.0f}).")


def _validate_reader_output(text: str, category: str, run_dir: Path):
    """Parse one reader response and validate it for its category in a scratch
    directory. Returns (body, None) when valid, (None, error message) when not.
    Never touches artifacts/proposals/."""
    blocks = _READER_OUTPUT_BLOCK_RE.findall(text or "")
    if len(blocks) != 1:
        return None, (f"{category} reader returned {len(blocks)} fenced YAML block(s); "
                      f"exactly one is required.")
    body = blocks[0].strip() + "\n"
    rp = _reader_proposals_module()
    scratch = Path(tempfile.mkdtemp(prefix=f".reader_{category}_", dir=str(run_dir / "artifacts")))
    try:
        (scratch / f"{category}.yaml").write_text(body, encoding="utf-8")
        rp.load_proposals(scratch, [category])
    except rp.ProposalError as exc:
        return None, str(exc).replace(str(scratch), "proposals")
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return body, None


def run_reader_worker(category: str, run_id: str, run_dir: Path, stage_attempt=0) -> Path:
    """Run ONE reader skill and write its output to the explicit path
    artifacts/proposals/<category>.yaml (S1_FINDINGS_5B_II.md §2 option (a):
    this function owns the path; any filename the model writes in its fenced
    block is ignored). The output is validated for this category
    (reader_proposals) BEFORE it reaches the final path, via a temp file and
    os.replace, so a bad output can never sit at the final path and block a
    resume. An invalid output gets exactly one retry with the validation
    error appended to the prompt (same bound as _invoke_agent_with_yaml_retry);
    if that also fails, the raw output is saved as
    debug_specialist_readers_<category>_raw_output.txt and this raises."""
    handoff = _reader_handoff(category, run_id, stage_attempt)
    base_prompt = _build_stage_prompt("specialist_readers", handoff, run_dir,
                                      skill_file_name=_reader_skill_dir(category))
    prompt = base_prompt
    dest = run_dir / "artifacts" / "proposals" / f"{category}.yaml"
    for attempt in range(2):
        if attempt:
            _check_reader_budget(run_dir, category)
        print(f"\n🧠 [READER INVOKED] {category} ({_reader_skill_dir(category)})"
              + (" (validation retry)" if attempt else ""))
        start = time.time()
        text, meta = asyncio.run(_invoke_reader_llm(prompt))
        key = f"specialist_readers_{category}_attempt_{stage_attempt}" + (f"_retry{attempt}" if attempt else "")
        update_state(path=run_dir, audit_log={key: {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine": "claude-agent-sdk",
            "execution_time_seconds": round(time.time() - start, 2),
            "cost_usd": meta.get("cost_usd", 0.0),
            "num_turns": meta.get("num_turns"),
            "tokens": _usage_token_record(meta.get("usage") or {}),
        }})
        body, error = _validate_reader_output(text, category, run_dir)
        if error is None:
            dest.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp_name = tempfile.mkstemp(prefix=f".{category}.", suffix=".tmp", dir=str(dest.parent))
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(body)
                os.replace(tmp_name, dest)
            except BaseException:
                with contextlib.suppress(OSError):
                    os.unlink(tmp_name)
                raise
            print(f"✅ [READER COMPLETE] {category} -> {dest.relative_to(run_dir).as_posix()}")
            return dest
        if attempt == 0:
            print(f"⚠️  {category} reader output invalid -- retrying once with the error: {error}")
            prompt = base_prompt + (
                "\n\n    YOUR PREVIOUS OUTPUT FAILED VALIDATION:\n    " + error +
                "\n\n    Fix exactly this and output ONE fenced ```yaml block holding a YAML "
                "list of proposals (`[]` for none).\n")
    debug_path = run_dir / "artifacts" / f"debug_specialist_readers_{category}_raw_output.txt"
    debug_path.write_text(text or "", encoding="utf-8")
    raise _reader_proposals_module().ProposalError(
        f"{category} reader output invalid after one retry: {error} "
        f"Raw output saved to {debug_path}.")


def _run_specialist_readers(run_id: str, run_dir: Path, stage_attempt=0) -> dict:
    """The per-category loop (S1_FINDINGS_5B_II.md §3 shape (a)). Sequential:
    the orchestrator has no fan-out. A category whose proposals file already
    exists is re-validated, not re-run -- safe because protocol_execution
    clears artifacts/proposals/ on every attempt under this flag, so an
    existing file can only come from this same attempt's earlier, validated
    reader call. The budget is checked before every reader (five calls share
    one stage). Returns the validated proposals: nothing in this module
    routes the run on them; the stage body only copies their requires_feed
    requests into data_requests.yaml (E-035 S2c)."""
    categories = _reader_categories()
    rp = _reader_proposals_module()
    proposals_dir = run_dir / "artifacts" / "proposals"
    for category in categories:
        dest = proposals_dir / f"{category}.yaml"
        if dest.exists():
            rp.load_proposals(proposals_dir, categories)
            print(f"⏭️  proposals/{category}.yaml already present and valid -- reader not re-run.")
            continue
        _check_reader_budget(run_dir, category)
        run_reader_worker(category, run_id, run_dir, stage_attempt)
        rp.load_proposals(proposals_dir, categories)
    missing = [c for c in categories if not (proposals_dir / f"{c}.yaml").exists()]
    if missing:
        raise FileNotFoundError(f"specialist_readers finished without proposals for {missing}")
    return rp.load_proposals(proposals_dir, categories)


def _check_retune_firewall(run_dir: Path) -> None:
    """A2.2 retune firewall, relocated from the verdict_interpreter branch to
    specialist_readers stage entry (before any reader call, and on every
    resume)."""
    aud_path = run_dir / "artifacts" / "regime_audit_decision.yaml"
    if not aud_path.exists():
        return
    violations = _validate_retune_firewall(load_yaml(aud_path) or {})
    if violations:
        raise RuntimeError(
            "RETUNE FIREWALL VIOLATION — regime_audit_decision.yaml "
            "references forbidden strategy metrics:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )


def _run_specialist_readers_stage(run_id: str, run_dir: Path, stage_attempt=0) -> None:
    """Stage body. Engineering errors first: when protocol_result.yaml reports
    component errors the readers are not run at all (the grid they read is
    meaningless and determine_post_specialist_readers_route pauses). Then
    idea_status.yaml and the retune firewall are checked BEFORE any reader
    spends a call."""
    if not _specialist_readers_enabled():
        raise RuntimeError("specialist_readers reached with orchestrator.specialist_readers.enabled "
                           "off -- reset pending_stage to verdict_interpreter or enable the flag.")
    if _protocol_component_errors(run_dir):
        print("⏭️  specialist_readers: component errors in protocol_result.yaml -- readers not "
              "run (the grid is meaningless); the route pauses for a human.")
        return
    _load_idea_status(run_dir, run_id)
    _check_retune_firewall(run_dir)
    proposals = _run_specialist_readers(run_id, run_dir, stage_attempt)
    # E-035 S2c: each feed the validated proposals ask for and do not have
    # becomes a data_requests.yaml row (idempotent per run and feed; nothing
    # written when no proposal carries requires_feed).
    n_feed = _route_reader_feed_requests(run_id, proposals)
    if n_feed:
        print(f"📥 specialist_readers: {n_feed} feed request(s) offered to "
              f"campaign_record/data_requests.yaml (stage {READER_FEED_REQUEST_STAGE}).")


def determine_post_specialist_readers_route(path: Path, run_id: str, *,
                                           component_errors: list | None = None,
                                           idea: dict | None = None,
                                           routing_retired: bool = False) -> str:
    """The interim route under orchestrator.specialist_readers.enabled
    (delivery_plan_v26.md slice 2: "until slice 6c"). Reads ONLY
    protocol_result.yaml and idea_status.yaml -- never proposals/*.yaml and
    never verdict_interpretation.yaml.
      1. any component error -> human_pause (component_execution_error_flagged)
      2. idea_status validated -> promote (holdout path, unchanged)
         idea_status refuted   -> kill / terminate
         idea_status inconclusive -> human_pause (inconclusive_grid)
    Validated/refuted go through the existing binding path:
    _resolve_verdict_fields(pre_eval=idea_status) -> _dispatch_verdict_route.
    No circuit breaker, no refine/pivot/escalate, no hypothesis_family: the
    `interp` handed on is empty because there is no LLM narrative under this
    flag, and neither function reads it on the promote / kill+terminate paths
    except _route_kill's legacy altitude_history family field, left empty.

    `component_errors` / `idea` (E-058 S2a): passed by run_loop when the
    regroup_record stage already computed them this iteration; None (every
    other caller, and the flag-off path) computes them here as before.

    `routing_retired` (slice 6c S2a): passed True by run_loop only under
    orchestrator.verdict_routing_retired.enabled (resolved in its pre-flight).
    The component-error pause is unchanged; after it the run ends
    completed_<idea_status> (_route_retired_idea_status) -- no inconclusive
    pause, no _resolve_verdict_fields, no _dispatch_verdict_route."""
    if not _specialist_readers_enabled():
        raise RuntimeError("determine_post_specialist_readers_route called with "
                           "orchestrator.specialist_readers.enabled off")
    errors = component_errors if component_errors is not None else _protocol_component_errors(path)
    if errors:
        print("\n⚠️  component_execution_error: a strategy component raised during the "
              "backtest -- an engineering fault, not a research finding. The grid is "
              "meaningless on this run; pausing before any route.")
        for e in errors[:10]:
            print(f"   - {e}")
        update_state(path=path, status="paused_for_human",
                     flags={"component_execution_error_flagged": True})
        return "human_pause"

    if idea is None:
        idea = _load_idea_status(path, run_id)
    if routing_retired:
        return _route_retired_idea_status(path, run_id, idea)
    status = idea["idea_status"]
    if status == "inconclusive":
        print(f"\n⏸️  inconclusive_grid: the grid could not decide this idea "
              f"(reason: {idea.get('reason')!r}). A human decides -- see "
              f"artifacts/grid_evaluation.yaml.")
        update_state(path=path, status="paused_for_human", flags={"inconclusive_grid": True})
        return "human_pause"

    hypothesis_verdict, lineage_routing = _resolve_verdict_fields({}, "", "", pre_eval=idea)
    print(f"\n🧮 Route from the grid: idea_status={status} -> "
          f"{hypothesis_verdict}/{lineage_routing}")
    return _dispatch_verdict_route(path, run_id, {}, load_campaign_state(),
                                   hypothesis_verdict, lineage_routing)


# ---------------------------------------------------------------------------
# E-058 S2a -- the regroup_record stage and the campaign memory
# (delivery_plan_v26.md slice 6a, first half; engineering/roadmap/E-058/
# S1_FINDINGS.md §2-§3 and its operator decision). OFF BY DEFAULT. When on:
#   specialist_readers -> regroup_record -> determine_post_specialist_readers_route
# (unchanged route, only later in time: "memory before decision", card H).
# regroup_record writes ONE entry per run to campaign_record/campaign_memory.yaml
# (replaced on re-run) through tools/campaign_memory.py. It decides nothing:
# the entry's idea_status is copied from the grid's idea_status.yaml, reader
# proposals are only referenced (ids + count, never scores), and it writes NO
# trial rows (protocol_execution already recorded them; the memory only reads
# their ids). No refine/pivot/escalate, circuit breaker, hypothesis_family,
# altitude or continuation field is read or written (retired in slice 6c).
# E-058 S2b adds, under the same flag: the block registry
# (tools/block_registry.py, validated + manifest only, append-only), one
# grid-based KB entry per non-fault run (tools/grid_kb_writer.py,
# legacy_schema: false, never merged into a legacy entry), the near-miss
# scoreboard rebuild, and campaign-review's memory input.
# ---------------------------------------------------------------------------

_REGROUP_RECORD_HANDOFF = "specialist_readers_to_regroup_record.yaml"


def _regroup_record_enabled(cfg: dict | None = None) -> bool:
    """False when the key, the section or the config file is absent. A
    non-bool value raises. Requires orchestrator.specialist_readers.enabled
    (itself requiring grid_evaluation + category_reports): raises, loudly, if
    this flag is on without it -- without the readers flag the stage is never
    routed to and there is no idea_status route to record before."""
    cfg = _orchestrator_config(cfg)
    rr_cfg = ((cfg.get("orchestrator") or {}).get("regroup_record") or {})
    value = rr_cfg.get("enabled", False)
    if not isinstance(value, bool):
        raise ValueError(
            f"orchestrator.regroup_record.enabled={value!r} is not a real boolean "
            f"(got {type(value).__name__}) -- write an unquoted `true` or `false` in "
            f"config/campaign_config.yaml, not a quoted string or null."
        )
    if value and not _flag_dep(_specialist_readers_enabled, cfg):
        raise ValueError(
            "orchestrator.regroup_record.enabled=true requires "
            "orchestrator.specialist_readers.enabled=true as well -- regroup_record runs "
            "only after the specialist_readers stage and records the grid's idea_status "
            "before its route. Enable both (with grid_evaluation and category_reports)."
        )
    return value


def _decide_next_enabled(cfg: dict | None = None) -> bool:
    """E-059 S2a (delivery_plan_v26.md slice 6b; S1_FINDINGS_6B.md §9 and its
    operator decision). False when the key, the section or the config file is
    absent. A non-bool value raises. Requires, loudly:
      * orchestrator.regroup_record.enabled (itself requiring
        specialist_readers, grid_evaluation, category_reports) -- decide_next
        reads campaign_record/campaign_memory.yaml and the reader proposals it
        references, which exist only under those flags;
      * orchestrator.config_direct_authoring.enabled -- operator decision 2:
        every proposal-sourced candidate enters step 1a, which writes its
        criteria from config/criterion_menu.yaml, and 1a only sees that menu
        (IMPROVEMENT 07/08 of hypothesis-design) and 1b only honours a
        pass-through config under this flag. Without it a candidate could only
        fail pre-flight for want of a menu-shaped pass_rule.
    Read by run_campaign.process_once (as orch._decide_next_enabled()), once per
    step."""
    cfg = _orchestrator_config(cfg)
    dn_cfg = ((cfg.get("orchestrator") or {}).get("decide_next") or {})
    value = dn_cfg.get("enabled", False)
    if not isinstance(value, bool):
        raise ValueError(
            f"orchestrator.decide_next.enabled={value!r} is not a real boolean "
            f"(got {type(value).__name__}) -- write an unquoted `true` or `false` in "
            f"config/campaign_config.yaml, not a quoted string or null."
        )
    if value:
        missing = [name for name, on in (
                       ("regroup_record", _flag_dep(_regroup_record_enabled, cfg)),
                                         ("config_direct_authoring",
                                          _flag_dep(_config_direct_authoring_enabled, cfg)))
                   if not on]
        if missing:
            raise ValueError(
                "orchestrator.decide_next.enabled=true requires "
                + " and ".join(f"orchestrator.{m}.enabled=true" for m in missing)
                + " as well -- decide_next reads the campaign memory and reader proposals "
                "(regroup_record, hence specialist_readers, grid_evaluation, category_reports), "
                "and every picked candidate writes its criteria at step 1a from the criterion "
                "menu (config_direct_authoring). Enable them together."
            )
    return value


# ---------------------------------------------------------------------------
# E-059 S3 / slice 6c S2a -- verdict routing retired (delivery_plan_v26.md slice
# 6c; engineering/roadmap/E-059/S1_FINDINGS_6C.md and its operator decision of
# 2026-09-25). OFF BY DEFAULT. When on, the route after regroup_record ends the
# run at completed_<idea_status> (validated / refuted / inconclusive): the idea
# status comes only from the grid, and the next run is chosen only by
# decide_next (run_campaign's DONE branch). Refine, pivot, escalate, kill, the
# circuit breaker, the escalation/timeframe protocols and continuation_child are
# unreachable; their code stays for flag-off runs, marked
# `# legacy routing (v26 card G)`. Nothing routes to holdout_evaluation: the
# holdout is reached only through the branch-3 profit_bars_reached stop plus an
# operator unlock (slice 6c S2d, _holdout_unlock_route below).
# ---------------------------------------------------------------------------

# The three run endings under the flag, one per grid idea_status. Pinned in
# every outcome list by tests/test_e059_6c_s2a_route_retirement.py.
RETIRED_ROUTING_TERMINALS = ("completed_validated", "completed_refuted",
                             "completed_inconclusive")


def _strict_orchestrator_flag(name: str, requires: tuple = (), why: str = "", *,
                              cfg: dict | None = None, default: bool = False) -> bool:
    """Generic strict reader for orchestrator.<name>.enabled (slice 6c S2a code
    review, item 10). `default` (False) when the key, the section or the config
    file is absent; a non-bool value raises; when true, every (dep_name,
    dep_reader) in `requires` must read true, else it raises naming each missing
    dependency (`why` is appended to that error). Each dep_reader enforces its
    own chain. Used by _verdict_routing_retired_enabled and
    _composition_runs_enabled.

    E-061 C1.5 (A8): also THE one strict check of the seven readers that used
    plain bool(). Every reader takes an optional parsed `cfg`
    (_orchestrator_config), which run_campaign's launch pre-flight passes to all
    of them after parsing the config once -- one check, one message, no copy of
    the rules outside the readers."""
    if cfg is None:
        path = ROOT / "config" / "campaign_config.yaml"
        if not path.exists():
            return default
        with open(path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    value = ((cfg.get("orchestrator") or {}).get(name) or {}).get("enabled", default)
    if not isinstance(value, bool):
        raise ValueError(
            f"orchestrator.{name}.enabled={value!r} is not a real boolean "
            f"(got {type(value).__name__}) -- write an unquoted `true` or `false` in "
            f"config/campaign_config.yaml, not a quoted string or null."
        )
    if value:
        missing = [dep for dep, reader in requires if not reader()]
        if missing:
            raise ValueError(
                f"orchestrator.{name}.enabled=true requires "
                + " and ".join(f"orchestrator.{m}.enabled=true" for m in missing)
                + (f" as well -- {why}" if why else " as well.")
            )
    return value


def _verdict_routing_retired_enabled(cfg: dict | None = None) -> bool:
    """False when the key, the section or the config file is absent. A non-bool
    value raises. Requires, loudly:
      * orchestrator.decide_next.enabled (itself requiring regroup_record,
        specialist_readers, grid_evaluation, category_reports and
        config_direct_authoring) -- once routing is gone, only decide-next
        picks the next run;
      * orchestrator.profit_bars_every_backtest.enabled (itself requiring
        profit_bars_file) -- the promote-path profit-bars check lives inside
        the retired _dispatch_verdict_route, so without the per-backtest check
        no run would ever be graded against the bars (S1_FINDINGS_6C.md §4).
    Read ONCE per run, in run_loop's pre-flight (that value is passed to every
    decision inside the run), and once per step in run_campaign.process_once."""
    return _strict_orchestrator_flag(
        "verdict_routing_retired", cfg=cfg,
        requires=(("decide_next", lambda: _flag_dep(_decide_next_enabled, cfg)),
                  ("profit_bars_every_backtest",
                   lambda: _flag_dep(_profit_bars_every_backtest_enabled, cfg))),
        why=("with verdict routing retired, only decide_next picks the next run, and only "
             "the per-backtest profit-bars check grades a run against "
             "config/profitability_bars.yaml. Enable them together."))


# ---------------------------------------------------------------------------
# E-060 S2 -- composition runs, part 1: the residual-IC criterion, the
# composite cache and the registry's timeframe / residual-IC fields
# (delivery_plan_v26.md slice 7 item 7.1; engineering/roadmap/E-060/
# S1_FINDINGS.md guesses 4-8 and the operator decision of 2026-09-26).
# OFF BY DEFAULT. When on:
#   * step 1a's pass_rule gets the code-added `residual_ic` criterion
#     (config/criterion_menu.yaml code_added_criteria) for every
#     forecast-block idea (_with_residual_ic_criterion);
#   * protocol_execution (variant loop) computes each variant's residual IC
#     against the current composite (tools/composite_cache.py,
#     tools/residual_ic.py), writes artifacts/residual_ic.yaml and injects it
#     into the grid's copy of the variant's protocol result
#     (hypothesis_verdict.diagnostics.residual_ic) -- the saved
#     protocol_result.yaml files and the trial rows are untouched;
#   * regroup_record's registry entry records the block's timeframe, its
#     timeframe category, residual_ic and correlation_to_composite.
# The composite is not a trial, not graded, and never reaches the holdout.
# Off: nothing new is read or written.
# ---------------------------------------------------------------------------

_RESIDUAL_IC_CRITERION_ID = "residual_ic"
_RESIDUAL_IC_ARTIFACT = "residual_ic.yaml"
# code_added_criteria keys that describe the entry rather than define the criterion.
_CODE_CRITERION_META_KEYS = ("basis", "card_overridable", "requires_flag", "ratified")


def _composition_runs_enabled(cfg: dict | None = None) -> bool:
    """False when the key, the section or the config file is absent. A non-bool
    value raises. Requires, loudly (S1_FINDINGS.md "Flag design"):
      * orchestrator.decide_next.enabled (hence regroup_record,
        specialist_readers, grid_evaluation, category_reports,
        config_direct_authoring) -- the criterion is written at 1a from the
        menu, and the registry is written by regroup_record;
      * orchestrator.variant_loop.enabled -- the residual IC is computed per
        variant inside the variant loop's protocol_execution;
      * orchestrator.profit_bars_every_backtest.enabled (hence
        profit_bars_file) and orchestrator.verdict_routing_retired.enabled --
        without the latter a composition run could reach refine/pivot
        routing, which must never be fed."""
    return _strict_orchestrator_flag(
        "composition_runs", cfg=cfg,
        requires=(("decide_next", lambda: _flag_dep(_decide_next_enabled, cfg)),
                  ("variant_loop", lambda: _flag_dep(_variant_loop_enabled, cfg)),
                  ("profit_bars_every_backtest",
                   lambda: _flag_dep(_profit_bars_every_backtest_enabled, cfg)),
                  ("verdict_routing_retired",
                   lambda: _flag_dep(_verdict_routing_retired_enabled, cfg))),
        why=("the residual-IC criterion is written at 1a from the criterion menu, computed "
             "per variant in the variant loop, recorded by regroup_record, and a composition "
             "run must never reach retired refine/pivot routing. Enable them together."))


def _residual_ic_menu_entry(menu: dict) -> dict:
    """config/criterion_menu.yaml's code_added_criteria `residual_ic` entry,
    stripped of its descriptive keys. Raises when it is missing (E-060 S3b
    review fix 10: one reader, _code_added_criterion)."""
    return _code_added_criterion(menu, _RESIDUAL_IC_CRITERION_ID)


def _residual_ic_exempt_reason(run_dir: Path) -> str | None:
    """Why this run's idea is NOT a forecast-block idea (guess 6: the
    criterion is required for every forecast block, not for composition runs
    or regime blocks). None = required."""
    path = Path(run_dir) / "artifacts" / "research_brief.yaml"
    brief = (load_yaml(path) if path.exists() else {}) or {}
    cand = brief.get("candidate") if isinstance(brief, dict) else None
    cand = cand if isinstance(cand, dict) else {}
    source = cand.get("source") if isinstance(cand.get("source"), dict) else {}
    if "composition" in (brief.get("origin"), source.get("origin")) or brief.get("composition") \
            or isinstance(cand.get("composition"), dict):
        # E-060 S3b: candidate.composition also marks a reader patch on a
        # composite (7.5) -- itself a composition run.
        return "composition run"
    proposal = source.get("proposal") if isinstance(source.get("proposal"), dict) else {}
    kinds = {((proposal.get("block") or {}) if isinstance(proposal.get("block"), dict) else {}).get("kind"),
             (((cand.get("manifest") or {}).get("block") or {})
              if isinstance(cand.get("manifest"), dict) else {}).get("kind")}
    if "regime" in kinds:
        return "regime block"
    # Code review fix 6: a 1a-authored brief carries no candidate block. Once
    # they exist, the hypothesis card (a block kind field, if 1a wrote one) and
    # 1b's block_manifest.yaml (the authoritative kind) decide -- so at grid
    # time a regime-detector idea from an ordinary brief is exempt too.
    arts = Path(run_dir) / "artifacts"
    for name, pick in (("hypothesis_card.yaml",
                        lambda d: d.get("block_kind") or ((d.get("block") or {})
                                                          if isinstance(d.get("block"), dict)
                                                          else {}).get("kind")),
                       ("block_manifest.yaml",
                        lambda d: ((d.get("block") or {}) if isinstance(d.get("block"), dict)
                                   else {}).get("kind"))):
        p = arts / name
        doc = (load_yaml(p) if p.exists() else {}) or {}
        if isinstance(doc, dict) and pick(doc) == "regime":
            return "regime block"
    return None


def _with_residual_ic_criterion(pass_rule: dict, menu: dict) -> dict:
    """pass_rule with the code's `residual_ic` criterion appended (any
    criterion already carrying that id is replaced: code, not 1a, sets it)."""
    crit = _residual_ic_menu_entry(menu)
    others = [c for c in (pass_rule.get("criteria") or [])
              if not (isinstance(c, dict) and c.get("id") == _RESIDUAL_IC_CRITERION_ID)]
    return {**pass_rule, "criteria": others + [crit]}


def _ensure_residual_ic_in_pre_registration(run_dir: Path) -> bool:
    """For a run whose pass_rule step 1a wrote directly (a research brief, not
    a decide-next candidate): the same append as _write_pass_rule_from_card,
    on pre_registration.yaml, wherever its pass_rule sits. Caller checks the
    flag. No-op (False) for an exempt idea or a pass_rule the grid cannot read
    (not menu-shaped -- no grid is written for it anyway)."""
    if _residual_ic_exempt_reason(run_dir):
        return False
    path = Path(run_dir) / "artifacts" / "pre_registration.yaml"
    if not path.exists():
        return False
    pre_reg = load_yaml(path) or {}
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import verdict_criteria_evaluator as _vce
    pass_rule = _vce._find_pass_rule(pre_reg)
    if not _vce._is_menu_shaped_pass_rule(pass_rule):
        print(f"⚠️  [E-060] {path}: pass_rule is not menu-shaped -- residual_ic not added "
              f"(no grid is written for this run)")
        return False
    menu_path = ROOT / "config" / "criterion_menu.yaml"
    menu = (load_yaml(menu_path) if menu_path.exists() else {}) or {}
    new_rule = _with_residual_ic_criterion(pass_rule, menu)
    if new_rule == pass_rule:
        return False
    if pre_reg.get("pass_rule") is not None:
        pre_reg["pass_rule"] = new_rule
    else:
        pre_reg["machine_constraints"]["pass_rule"] = new_rule
    save_yaml(path, pre_reg)
    print(f"✅ [E-060] pre_registration.yaml: code-added criterion residual_ic appended")
    return True


def _residual_ic_grid_inputs(per_variant_summaries: dict, run_dir: Path, protocol_path,
                             python_exe, pre_registration: dict) -> tuple:
    """(grid inputs, grid pre_registration). Each variant's residual IC
    against the current composite, written to artifacts/residual_ic.yaml, and
    returned as DEEP COPIES of the variant summaries carrying
    hypothesis_verdict.diagnostics.residual_ic -- the grid's inputs only. The
    saved protocol_result.yaml files and trial rows are not touched. The
    composite computation writes no trial row.
    An exempt idea (regime block -- now detectable from 1b's manifest -- or a
    composition run): nothing is computed and no subprocess runs;
    residual_ic.yaml records `skipped` + the timeframe, and the grid reads a
    copy of the pre-registration without the residual_ic criterion (loudly)."""
    import copy
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import composite_cache as _cc
    import verdict_criteria_evaluator as _vce
    run_dir = Path(run_dir)
    exempt = _residual_ic_exempt_reason(run_dir)
    doc = _cc.residual_ic_by_variant(
        per_variant_summaries,
        {vid: run_dir / "variants" / vid / "results" for vid in per_variant_summaries},
        root=ROOT, protocol_path=Path(protocol_path),
        registry_path=_block_registry_path(),
        compositions_path=ROOT / "campaign_record" / "compositions.yaml",
        holdout_range=_load_holdout_range(), breach_cls=HoldoutBoundaryBreach,
        exempt_reason=exempt, python_exe=python_exe)
    save_yaml(run_dir / "artifacts" / _RESIDUAL_IC_ARTIFACT, doc)
    if exempt:
        grid_pre = copy.deepcopy(pre_registration)
        rule = _vce._find_pass_rule(grid_pre)
        if isinstance(rule, dict) and isinstance(rule.get("criteria"), list):
            dropped = [c for c in rule["criteria"]
                       if isinstance(c, dict) and c.get("id") == _RESIDUAL_IC_CRITERION_ID]
            rule["criteria"] = [c for c in rule["criteria"] if c not in dropped]
            if dropped:
                print(f"⚠️  [E-060] {run_dir.name}: {exempt} -- residual_ic is not graded for "
                      f"this idea (removed from the grid's copy of the pass_rule)")
        print(f"✅ [E-060] residual_ic.yaml written: skipped ({exempt})")
        return per_variant_summaries, grid_pre
    out = {}
    for vid, summary in per_variant_summaries.items():
        s = copy.deepcopy(summary)
        hv = s.get("hypothesis_verdict")
        if not isinstance(hv, dict):
            hv = s["hypothesis_verdict"] = {}
        diag = hv.get("diagnostics")
        if not isinstance(diag, dict):
            diag = hv["diagnostics"] = {}
        diag[_RESIDUAL_IC_CRITERION_ID] = copy.deepcopy(doc["variants"][vid])
        out[vid] = s
    print(f"✅ [E-060] residual_ic.yaml written (composite={doc['composite']['kind']}, "
          f"timeframe={doc['timeframe']}): "
          f"{ {v: d.get('value') for v, d in doc['variants'].items()} }")
    return out, pre_registration


# ---------------------------------------------------------------------------
# E-060 S3b -- composition runs, part 2: composition mode (delivery_plan_v26.md
# slice 7 items 7.2, 7.3, 7.5; engineering/roadmap/E-060/S1_FINDINGS.md guesses
# 9-12 and the operator decisions of 2026-09-26). Only under
# orchestrator.composition_runs.enabled, and only for a run whose
# research_brief.yaml carries `candidate.composition` -- an R1 composition
# (tools/decide_next.composition_brief) or a reader patch on one (7.5). Such a
# run authors NOTHING with an LLM:
#   * step 1a passes the candidate through: a code-written card and the
#     pass_rule [profit_bars] (config/criterion_menu.yaml code_added_criteria);
#   * step 1b copies the code-written base config (sha-checked) and the
#     composition manifest (sha-checked) -- no block_manifest.yaml;
#   * step 2 writes variant_patches.yaml from the manifest's schemes;
#   * 5a checks every variant against the manifest (tools/composition.
#     check_composition_config) instead of a block manifest;
#   * the grid grades the profit_bars criterion with branch 3's own grading
#     function; branch 3 labels the variants `composite`;
#   * regroup_record never registers a composite as a block.
# Everything else (the data gate, the backtests and their trial rows, the
# readers, the memory, decide-next, the branch-3 stop and the operator-only
# holdout unlock) is the ordinary path. Off: nothing here runs.
# ---------------------------------------------------------------------------

_COMPOSITION_CODE_STAGES = ("hypothesis_generation", "strategy_config_authoring",
                            "innovation_expansion")
_PROFIT_BARS_CRITERION_ID = "profit_bars"
import composition_names as _composition_names  # noqa: E402  (tools/: one definition)
_COMPOSITION_MANIFEST_FILE = _composition_names.MANIFEST_FILENAME


def _composition_module():
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import composition as _comp
    return _comp


def _load_block_registry_doc() -> dict:
    """campaign_record/block_registry.yaml (read only; malformed raises)."""
    _composition_module()  # puts tools/ on sys.path
    import block_registry as _br
    return _br.load_registry(_block_registry_path())


def _composition_candidate(run_dir: Path) -> dict | None:
    """research_brief.yaml's `candidate` when it carries a `composition`
    block, else None. Read only."""
    path = Path(run_dir) / "artifacts" / "research_brief.yaml"
    if not path.exists():
        return None
    brief = load_yaml(path) or {}
    cand = brief.get("candidate") if isinstance(brief, dict) else None
    if isinstance(cand, dict) and isinstance(cand.get("composition"), dict):
        return cand
    return None


def _composition_mode(run_dir: Path) -> bool:
    """True for a composition run under the flag. A composition brief with the
    flag off raises: it must never fall through to the LLM stages."""
    if _composition_candidate(run_dir) is None:
        return False
    if not _composition_runs_enabled():
        raise ValueError(f"{Path(run_dir).name}: research_brief.yaml carries candidate.composition "
                         f"but orchestrator.composition_runs is off -- a composition brief is never "
                         f"authored by the LLM stages. Switch the flag back on, or mark the entry "
                         f"superseded.")
    return True


def _code_added_criterion(menu: dict, cid: str) -> dict:
    import copy
    for entry in (menu or {}).get("code_added_criteria") or []:
        if isinstance(entry, dict) and entry.get("id") == cid:
            return {k: copy.deepcopy(v) for k, v in entry.items()
                    if k not in _CODE_CRITERION_META_KEYS}
    raise ValueError(f"config/criterion_menu.yaml has no code_added_criteria entry {cid!r} -- "
                     f"orchestrator.composition_runs.enabled requires it (E-060 S3b)")


def _load_composition_manifest(run_dir: Path, cand: dict) -> dict:
    """The candidate's composition manifest from its manifest_ref, checked
    against the brief: canonical sha256 (manifest_sha256), registry_hash and
    timeframe. Raises on any difference."""
    comp = cand["composition"]
    ref = comp.get("manifest_ref")
    path = ROOT / str(ref)
    _composition_module()._cc._refuse_sealed(path)
    if not ref or not path.exists():
        raise FileNotFoundError(f"{Path(run_dir).name}: composition manifest {path} is missing")
    manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    got = _canonical_json_sha256(manifest)
    if got != comp.get("manifest_sha256"):
        raise RuntimeError(f"{path}: canonical sha256 {got} differs from the brief's "
                           f"manifest_sha256 {comp.get('manifest_sha256')} -- changed after R1 wrote it")
    for key in ("registry_hash", "timeframe"):
        if manifest.get(key) != comp.get(key):
            raise RuntimeError(f"{path}: {key}={manifest.get(key)!r} is not the brief's "
                               f"{comp.get(key)!r}")
    return manifest


def _composition_pass_through_1a(run_dir: Path, run_id: str, sr_flag: bool) -> None:
    """Step 1a in composition mode (IMPROVEMENT 09 of hypothesis-design, done
    by code): the card is the candidate passed through, and the pass_rule is
    the profit bars (guess 9) -- never picked by an LLM, never inherited.
    Writes hypothesis_card.yaml and pre_registration.yaml's pass_rule, runs
    the K3 lint and (flag on) the specialist_readers pre-flight. Raises before
    any spend."""
    cand = _composition_candidate(run_dir)
    source = cand.get("source") if isinstance(cand.get("source"), dict) else {}
    hyp = source.get("hypothesis_id")
    if not isinstance(hyp, str) or not hyp.strip():
        raise ValueError(f"{run_id}: research_brief.yaml candidate.source has no hypothesis_id")
    manifest = _load_composition_manifest(run_dir, cand)
    comp = cand["composition"]
    arts = Path(run_dir) / "artifacts"
    card = {
        "hypothesis_id": hyp,
        "thesis": (f"The validated forecast blocks {comp['block_ids']} on {manifest['timeframe']}, "
                   f"combined as validated, clear the campaign's profit bars together."),
        "timeframe": manifest["timeframe"],
        "pass_through": True,
        "source": (f"code (E-060 S3b composition pass-through, no LLM): "
                   f"{source.get('origin')} candidate, manifest {comp['manifest_ref']}"),
        "composition": {"registry_hash": manifest["registry_hash"],
                        "registry_revision": manifest.get("registry_revision"),
                        "timeframe": manifest["timeframe"],
                        "timeframe_category": manifest["timeframe_category"],
                        "block_ids": [b["block_id"] for b in manifest["blocks"]],
                        "manifest_ref": comp["manifest_ref"]},
        "criteria": [{"id": _PROFIT_BARS_CRITERION_ID}],
    }
    save_yaml(arts / "hypothesis_card.yaml", card)
    menu_path = ROOT / "config" / "criterion_menu.yaml"
    menu = (load_yaml(menu_path) if menu_path.exists() else {}) or {}
    pass_rule = {"criteria": [_code_added_criterion(menu, _PROFIT_BARS_CRITERION_ID)]}
    pre_path = arts / "pre_registration.yaml"
    if not pre_path.exists():
        raise FileNotFoundError(f"{pre_path} is missing for a composition run -- it is written at "
                                f"materialization (run_campaign._materialize_run).")
    pre_reg = load_yaml(pre_path) or {}
    violations = _lint_machine_constraints_protocol_selection(
        pre_reg.get("machine_constraints") or {}, pass_rule)
    if violations:
        raise ValueError(f"{run_id}: the composition pass_rule failed the K3 protocol-selection "
                         f"lint:\n" + "\n".join(f"  - {v}" for v in violations))
    pre_reg["pass_rule"] = pass_rule
    pre_reg["pass_rule_source_ref"] = "config/criterion_menu.yaml#code_added_criteria/profit_bars"
    save_yaml(pre_path, pre_reg)
    print(f"✅ [E-060 S3b] composition 1a pass-through: card {hyp} written by code, "
          f"pass_rule = [profit_bars] (no LLM call)")
    if sr_flag:
        _check_specialist_readers_preflight(run_dir)


def _composition_base_config(run_dir: Path, cand: dict) -> dict:
    """The run's base config, verified against candidate.source.
    expected_config_sha256: candidate.config (a reader patch, 7.5) or the
    code-written file at source.base_config_ref (an R1 composition)."""
    source = cand.get("source") if isinstance(cand.get("source"), dict) else {}
    expected = source.get("expected_config_sha256")
    if not expected:
        raise RuntimeError(f"{Path(run_dir).name}: candidate.source has no expected_config_sha256")
    if isinstance(cand.get("config"), dict):
        config = cand["config"]
    else:
        path = ROOT / str(source.get("base_config_ref"))
        _composition_module()._cc._refuse_sealed(path)
        if not path.exists():
            raise FileNotFoundError(f"composition base config {path} is missing")
        config = json.loads(path.read_text(encoding="utf-8"))
    got = _canonical_json_sha256(config)
    if got != expected:
        raise RuntimeError(f"composition base config sha256 {got} differs from the brief's "
                           f"expected_config_sha256 {expected}")
    return config


def _composition_1b(run_dir: Path, run_id: str) -> None:
    """Step 1b in composition mode: no authoring. Copies the verified base
    config into backtest_spec.yaml (spec_ready), the verified manifest into
    artifacts/composition_manifest.yaml, writes decision.yaml, and checks the
    base config against the manifest (equal weights) before anything else
    runs. Writes no block_manifest.yaml (a composite is never a block)."""
    import copy
    cand = _composition_candidate(run_dir)
    manifest = _load_composition_manifest(run_dir, cand)
    config = _composition_base_config(run_dir, cand)
    _composition_module().check_composition_config(config, manifest, "base", root=ROOT,
                                                   registry_doc=_load_block_registry_doc())
    arts = Path(run_dir) / "artifacts"
    hyp = (load_yaml(arts / "hypothesis_card.yaml") or {}).get("hypothesis_id")
    save_yaml(arts / _COMPOSITION_MANIFEST_FILE, copy.deepcopy(manifest))
    save_yaml(arts / "backtest_spec.yaml", {
        "hypothesis_id": hyp, "status": "spec_ready", "config": copy.deepcopy(config),
        "config_rationale": [{"hypothesis_claim": "composition of validated blocks",
                              "config_choice": "code-written by tools/composition.py (E-060 S3b); "
                                               "passed through unchanged, no LLM"}]})
    save_yaml(arts / "decision.yaml", {
        "hypothesis_id": hyp, "stage": "strategy_config_authoring", "status": "spec_ready",
        "rationale": "E-060 S3b composition mode: the code-written base config and composition "
                     "manifest were passed through (sha-checked); nothing authored"})
    print(f"✅ [E-060 S3b] composition 1b: base config + composition manifest passed through "
          f"(no LLM call)")


def _composition_variant_patches(run_dir: Path) -> None:
    """Step 2 in composition mode: variant_patches.yaml from the manifest's
    three schemes (guess 12) -- code, not the innovation-expansion LLM."""
    arts = Path(run_dir) / "artifacts"
    manifest = load_yaml(arts / _COMPOSITION_MANIFEST_FILE)
    save_yaml(arts / "variant_patches.yaml",
              _composition_module().variant_patches_from_manifest(manifest))
    print("✅ [E-060 S3b] composition variants: variant_patches.yaml written by code "
          "(base / vol_scaled / ic_weighted -- weights only)")


def _run_composition_code_stage(stage: str, run_id: str, run_dir: Path, sr_flag: bool) -> None:
    if stage == "hypothesis_generation":
        _composition_pass_through_1a(run_dir, run_id, sr_flag)
    elif stage == "strategy_config_authoring":
        _composition_1b(run_dir, run_id)
    elif stage == "innovation_expansion":
        _composition_variant_patches(run_dir)
    else:  # pragma: no cover -- guarded by _COMPOSITION_CODE_STAGES
        raise ValueError(f"no composition code stage {stage!r}")


def _check_composition_variant(artifacts: Path, variant_id: str, variant_config: dict,
                               manifest: dict, strict_sha: bool, registry_doc: dict) -> None:
    """5a for one composition variant: check_composition_config against the
    variant's scheme, and -- for an R1 composition (strict_sha: its base is
    the code-written base) -- the variant config's canonical sha256 must equal
    the code-written file's. Raises (fail loud: the patches are code-written,
    a mismatch is an engineering fault, never a not_tested variant).
    `registry_doc`: loaded ONCE by the caller for every variant (review fix 8)."""
    _composition_module().check_composition_config(variant_config, manifest, variant_id,
                                                   root=ROOT, registry_doc=registry_doc)
    if strict_sha:
        want = manifest["variants"][variant_id]["config_sha256"]
        got = _canonical_json_sha256(variant_config)
        if got != want:
            raise RuntimeError(f"composition variant {variant_id!r}: config sha256 {got} is not the "
                               f"code-written {want} ({manifest['variants'][variant_id]['config_ref']})")


def _profit_bars_grid_grader(run_dir: Path, run_id: str):
    """The grid's profit_bars grader (guess 9): variant_id -> branch 3's own
    grading of artifacts/variants/<id>/protocol_result.yaml
    (_grade_profit_bars_protocol_result, same bars file, same DSR context,
    same equal-weight portfolio), through the SAME tested-candidate helper
    branch 3 uses (_profit_bars_tested_candidate): a variant whose trial row
    is invalidated_artifact is INVALIDATED -- never graded, never passing
    (review fix 4). Each answer also carries the variant's weight schedule
    from artifacts/composition_manifest.yaml (review fix 5: which windows used
    estimated weights, which equal). Reads only; writes nothing."""
    bars = _load_profitability_bars()
    dsr_ctx = _promotion_dsr_context()
    invalidated = _invalidated_trial_ids()
    kind = "composite" if _composition_mode(Path(run_dir)) else "variant"
    man_path = Path(run_dir) / "artifacts" / _COMPOSITION_MANIFEST_FILE
    manifest = (load_yaml(man_path) if man_path.exists() else None) or {}

    def grade(variant_id: str) -> dict:
        cand = _profit_bars_tested_candidate(
            Path(run_dir), variant_id, f"{run_id}:{variant_id}",
            f"artifacts/variants/{variant_id}/protocol_result.yaml", kind, invalidated)
        sched = ((manifest.get("variants") or {}).get(variant_id) or {}).get("weight_schedule")
        extra = {"weight_schedule": sched} if sched is not None else {}
        if cand["protocol_result"] is None:
            return {"result": cand["result"], "bars": [], "reasons": [cand["reason"]], **extra}
        results, overall, reasons = _grade_profit_bars_protocol_result(
            Path(run_dir), cand["protocol_result"], cand["protocol_result_ref"], bars, dsr_ctx)
        return {"result": overall, "bars": results, "reasons": reasons, **extra}
    return grade


# ---------------------------------------------------------------------------
# Slice 6c S2c -- parked states (S1_FINDINGS_6C.md §6 and guesses 7-9), under
# orchestrator.verdict_routing_retired.enabled only. A run that waits on a
# missing component or on missing data does not pause the campaign: the
# parkable sites below write pipeline_state.yaml `parked` (plus the usual
# status paused_for_human) and stop the run; run_campaign.process_once reads
# the marker, marks the queue entry paused:waiting_for_<kind>, and decide-next
# picks the next run. run_campaign --unpark clears the marker. Nothing here is
# reached with the flag off, and no new sticky flag or pause row exists: the
# marker is read by process_once, never by _classify_human_pause.
# ---------------------------------------------------------------------------

PARKED_KEY = "parked"
PARK_KINDS = ("component", "data")
# The trading-bot checkout (same anchor as run_campaign._TRADING_BOT_ROOT): where
# decide_next.component_class_status reads strategies/strategy_components.py.
_TRADING_BOT_ROOT = Path(__file__).resolve().parent.parent.parent / "trading-bot"
# validate_config.py's V12 "cannot load" line. The loader's own message follows
# (strategies/registry._load_class); only its getattr failure -- "module '<m>'
# has no attribute '<Class>'" -- proves the module imported and the class is
# absent. An ImportError inside the module, a module typo, a dotless path, or
# a V12 "missing required 'class' key" is an engineering/config error.
_V12_CANNOT_LOAD_RE = re.compile(r"^VIOLATION V12 \S+\.class: cannot load '([^']+)': (.*)$")
# data_availability_gate.py's reasons for a shortfall no fetch can close
# (review fix 5): a reserved feed (a data-POLICY decline) and an unbuilt feed.
_UNFETCHABLE_AUX_REASON_MARKERS = ("is a RESERVED feed", "is not a known feed")


def _v12_missing_classes(report) -> list:
    """The class paths a validate_config.py report cannot load, when EVERY
    non-empty line of the report is a V12 cannot-load whose class is genuinely
    missing: the loader says the module has no such attribute (so the module
    imported) AND decide_next.component_class_status reads it 'missing' (a
    well-formed path in the component module, which exists and parses, and does
    not define it). [] otherwise -- another V-code, a missing 'class' key, an
    ImportError, a typo, a crash: design/engineering errors, never parked
    (guess 7; slice 6c S2c review fix 2)."""
    import decide_next as _dn  # tools/ sibling (on sys.path, module top)
    lines = [ln.strip() for ln in str(report or "").splitlines() if ln.strip()]
    classes = []
    for ln in lines:
        m = _V12_CANNOT_LOAD_RE.match(ln)
        if not m:
            return []
        class_path, detail = m.group(1), m.group(2)
        module, _, name = class_path.rpartition(".")
        if (f"module '{module}' has no attribute '{name}'" not in detail
                or _dn.component_class_status(_TRADING_BOT_ROOT, class_path) != "missing"):
            return []
        classes.append(class_path)
    return sorted(set(classes))


def _gate_shortfall_fetchable(gate: dict) -> bool:
    """Slice 6c S2c review fix 5: True only when a data_availability_gate.yaml
    DECLINE is a shortfall a fetch can close -- every non-validating price
    window was checked for real (Layer 2, not a Layer 1 venue/listing/timeframe
    impossibility), returned short WITHOUT raising (a SealedDataError or any
    other fetch error never parks), and lies wholly outside the sealed holdout
    range; every non-validating aux feed likewise, and is neither reserved nor
    unbuilt. A gate `refine`, an unreadable policy, or anything unknown: False
    (the previous, terminal behaviour)."""
    if not isinstance(gate, dict) or gate.get("outcome") != "decline":
        return False
    try:
        seal_start, seal_end = _load_holdout_range()
    except Exception:
        return False
    bad = [r for r in (gate.get("windows") or []) if isinstance(r, dict)
           and r.get("outcome") != "validate"]
    bad_aux = [r for r in (gate.get("aux_feeds") or []) if isinstance(r, dict)
               and r.get("outcome") != "validate"]
    if not (bad or bad_aux):
        return False
    for r in bad + bad_aux:
        if r.get("fetch_error") or any(isinstance(p, dict) and p.get("fetch_error")
                                       for p in (r.get("per_symbol") or {}).values()):
            return False
        if any(m in str(r.get("reason") or "") for m in _UNFETCHABLE_AUX_REASON_MARKERS):
            return False
        start, end = str(r.get("start") or "")[:10], str(r.get("end") or "")[:10]
        if len(start) != 10 or len(end) != 10 or not (end < seal_start or start > seal_end):
            return False
    for r in bad:
        if r.get("layer") != 2:
            return False
    return True


# E-036 S2a: the exact-match gate's skip reason prefix (_gate_config_direct_variants).
_REPEAT_REASON_PREFIX = "repeat:"


def _is_repeat_skip(v) -> bool:
    """True for an index.yaml entry the exact-match gate skipped as a repeat
    (not_tested, reason "repeat: ..."). Never a data or engineering problem:
    the data gate's shortfall check and _variant_park_kind leave it out."""
    return (isinstance(v, dict) and v.get("status") == "not_tested"
            and str(v.get("reason") or "").startswith(_REPEAT_REASON_PREFIX))


def _variant_park_kind(variants: dict, artifacts_dir=None) -> tuple:
    """(kind, classes) for the not_tested variants of artifacts/variants/index.yaml:
    'component' when each one is a genuinely missing class (5a,
    _v12_missing_classes) or a fetchable data decline and at least one is a
    class -- a mix parks as component, the data gate re-runs on unpark anyway;
    'data' when each one is a fetchable data decline (its own
    artifacts/variants/<id>/data_availability_gate.yaml, _gate_shortfall_fetchable);
    (None, []) when any other reason is present (a patch failure, unresolved
    manifest paths, another V-code, a gate crash, a gate refine, an
    unfetchable decline -- which stay what they are today) or none is not_tested.
    E-036 S2a: a repeat skip (_is_repeat_skip) is ignored -- it counts as
    neither class, data nor other."""
    classes, data, other = set(), 0, 0
    for vid, v in (variants or {}).items():
        if not isinstance(v, dict) or v.get("status") != "not_tested" or _is_repeat_skip(v):
            continue
        reason = str(v.get("reason") or "")
        found = (_v12_missing_classes(v.get("report"))
                 if reason == "validate_config.py violations" else [])
        gate_path = (Path(artifacts_dir) / "variants" / str(vid) / "data_availability_gate.yaml"
                     if artifacts_dir is not None else None)
        if found:
            classes.update(found)
        elif (reason.startswith("data_availability_gate outcome=decline:")
              and gate_path is not None and gate_path.is_file()
              and _gate_shortfall_fetchable(load_yaml(gate_path) or {})):
            data += 1
        else:
            other += 1
    if other or not (classes or data):
        return None, []
    return ("component" if classes else "data"), sorted(classes)


def _append_data_requests(run_id: str, requests: list, *, dedupe: bool = False,
                          stage: str = "data_availability_gate", key=None) -> None:
    """campaign_record/data_requests.yaml, a flat append-only {requests: [...]}
    list, each row stamped with run_id and `stage` (default
    data_availability_gate; E-035 S2c's reader router passes
    specialist_reader). dedupe=False: the per-variant gate's writer, moved here
    unchanged (E-033.1 Slice 4b) -- flag-off byte-identical. dedupe=True (under
    orchestrator.verdict_routing_retired, slice 6c S2c review fix 7; always for
    the reader router): the locked, idempotent appender shared with
    component_requests.yaml, so a park/unpark cycle re-running the gate (or a
    re-run of the readers stage) adds no duplicate row. `key` is the row
    identity (default campaign_review_retired.request_key, the gate's; the
    reader router passes feed_request_key)."""
    requests_path = ROOT / "campaign_record" / "data_requests.yaml"
    rows = [{"run_id": run_id, "stage": stage, **req} for req in requests]
    if dedupe:
        _crr.append_requests(requests_path, rows, key=key or _crr.request_key)
        return
    requests_path.parent.mkdir(parents=True, exist_ok=True)
    existing = (load_yaml(requests_path) or {}) if requests_path.exists() else {}
    existing_requests = existing.get("requests", [])
    existing_requests.extend(rows)
    save_yaml(requests_path, {"requests": existing_requests})


# E-035 S2c (delivery_plan_v26.md slice 8.2): the feed-acquisition lane's intake.
READER_FEED_REQUEST_STAGE = "specialist_reader"


# What a reader feed-request row asks a human for, by the gate's own
# classification (decide_next.feed_status): a reserved feed needs a
# campaign_data_policy.yaml designation; an unknown one must be built.
READER_FEED_REQUEST_KINDS = {"reserved": "designation", "unknown": "acquisition"}


def _reader_feed_request_rows(proposals: dict, feed_set: dict) -> list:
    """The data_requests.yaml rows (without run_id/stage) for the validated
    proposals carrying `requires_feed`: ONE row per feed, in first-seen order
    (category order, then file order):
      {feed, request: designation|acquisition,
       proposals: [{category, proposal_id, reason}, ...],
       reason: '<requires_feed|requires_feed_reserved>:<feed> -- ...'}
    A feed already WIRED (a FEED_REGISTRY key, not reserved) gets no row:
    there is nothing to acquire -- whether it covers the run's venue, symbols
    and windows is the data-availability gate's check at step 3."""
    import decide_next as _dn  # tools/ sibling (on sys.path, module top)
    by_feed: dict = {}
    for category, items in proposals.items():
        for p in items or []:
            rf = p.get("requires_feed")
            if rf is not None:
                by_feed.setdefault(rf["feed"], []).append(
                    {"category": category, "proposal_id": p["proposal_id"], "reason": rf["reason"]})
    rows = []
    for feed, asks in by_feed.items():
        status = _dn.feed_status(feed, feed_set)
        if status not in READER_FEED_REQUEST_KINDS:  # wired
            continue
        request = READER_FEED_REQUEST_KINDS[status]
        prefix = "requires_feed_reserved" if status == "reserved" else "requires_feed"
        rows.append({"feed": feed, "request": request, "proposals": asks,
                     "reason": f"{prefix}:{feed} -- {request} asked by {len(asks)} reader "
                               f"proposal(s): {', '.join(a['proposal_id'] for a in asks)}"})
    return rows


def _route_reader_feed_requests(run_id: str, proposals: dict, *, feed_registry=None) -> int:
    """After specialist_readers validates the proposals: append one row per
    feed they ask for and do not have to campaign_record/data_requests.yaml
    through the locked, idempotent appender, keyed on (run, stage, feed)
    (campaign_review_retired.feed_request_key) -- a resume or a re-attempt
    that asks for the same feed again, whatever its wording or proposal_id,
    adds nothing. The feed registry is read (decide_next.load_feed_registry,
    or the `feed_registry` document passed in) only when some proposal
    carries requires_feed, and then fails loud when unreadable. Writes
    nothing -- the file is not even created -- when no proposal carries it or
    every feed asked for is already wired. Proposes only: it never changes
    the idea's status, the route or the queue (decide_next gates the
    candidate). Returns the number of rows offered."""
    if not any(p.get("requires_feed") is not None
               for items in proposals.values() for p in items or []):
        return 0
    if feed_registry is None:
        import decide_next as _dn  # tools/ sibling (on sys.path, module top)
        feed_registry = _dn.load_feed_registry(_TRADING_BOT_ROOT)
    rows = _reader_feed_request_rows(proposals, feed_registry)
    if rows:
        _append_data_requests(run_id, rows, dedupe=True, stage=READER_FEED_REQUEST_STAGE,
                              key=_crr.feed_request_key)
    return len(rows)


def _park_run(run_dir: Path, *, kind: str, stage: str, reason: str, request_refs: list,
              resume_stage: str, classes=()) -> str:
    """Writes the parked marker and status paused_for_human; returns
    "human_pause" so every caller stops the run exactly as a pause does
    (pending_stage stays the parking stage). resume_stage is where --unpark
    restarts the SAME run (guess 8). The marker is replaced, never merged."""
    if kind not in PARK_KINDS:
        raise ValueError(f"_park_run: unknown park kind {kind!r}")
    marker = {
        "kind": kind, "stage": stage, "reason": str(reason),
        "request_refs": list(request_refs), "resume_stage": resume_stage,
        "classes": list(classes),
        "parked_at": datetime.now(timezone.utc).isoformat(),
    }
    update_state(path=run_dir, **{PARKED_KEY: None})  # update_state merges dicts
    update_state(path=run_dir, status="paused_for_human", **{PARKED_KEY: marker})
    print(f"\n🅿️  PARKED (waiting_for_{kind}) at {stage}: {reason}. Requests: "
          f"{list(request_refs)}. The campaign continues; unpark with run_campaign.py "
          f"--unpark <entry_id> once the {kind} exists (docs/RUNBOOK.md §4).")
    return "human_pause"


def _record_run_in_campaign_state(run_id: str, diag: dict) -> None:
    """The campaign_state bookkeeping kept once the retired machinery is gone
    (shared by _route_retired_idea_status and _route_kill's readers-flag
    branch): the run in `runs` and ONE `diagnostics_log` row per run_id, both
    idempotent -- a re-run of the route (e.g. after a resume) replaces the
    run's row in place instead of appending a duplicate. Nothing else: no
    altitude_history, failed_families or continuation field, no trial row."""
    state = load_campaign_state()
    state.setdefault("runs", [])
    if run_id not in state["runs"]:
        state["runs"].append(run_id)
    log = state.setdefault("diagnostics_log", [])
    row = {"run": run_id, **diag}
    idx = next((i for i, r in enumerate(log) if isinstance(r, dict) and r.get("run") == run_id),
               None)
    if idx is None:
        log.append(row)
    else:
        log[idx] = row
    _save_campaign_state(state)


def _route_retired_idea_status(path: Path, run_id: str, idea: dict) -> str:
    """The route after regroup_record under verdict_routing_retired (called by
    determine_post_specialist_readers_route AFTER its component-error pause):
    completed_<idea_status>, whatever the status. No pause (inconclusive no
    longer pauses, S1 guess 2), no child run, no continuation_child, no
    campaign-state field of the retired machinery, no route to the holdout.
    The bookkeeping later readers rely on is kept for every status
    (_record_run_in_campaign_state). Trial accounting is untouched (it lives
    in protocol_execution)."""
    status = idea.get("idea_status") if isinstance(idea, dict) else None
    terminal = f"completed_{status}"
    if terminal not in RETIRED_ROUTING_TERMINALS:
        raise ValueError(f"verdict_routing_retired: idea_status {status!r} for {run_id} is not "
                         f"validated/refuted/inconclusive -- refusing to route.")
    _record_run_in_campaign_state(run_id, _extract_diagnostics(path))
    print(f"\n🧮 Route from the grid (verdict routing retired): idea_status={status} -> "
          f"{terminal}. The next run is chosen by decide_next; nothing routes to the holdout.")
    return terminal


# Slice 6c S2a code review (item 7): run_loop's refusals under the flag pause
# with these sticky flags (classified by run_campaign._classify_human_pause;
# RUNBOOK §3 rows of the same names), never a generic failure.
HOLDOUT_REFUSED_FLAG = "holdout_refused_under_retired_routing"
CAMPAIGN_REVIEW_REFUSED_FLAG = "campaign_review_refused_under_retired_routing"


def _holdout_hypothesis_id(run_dir: Path, run_id: str) -> tuple:
    """(hypothesis_id, passes_deflated_threshold), derived exactly as
    _route_holdout_evaluation derives them -- shared, so the spent-holdout
    record under verdict_routing_retired names the id the single-use check
    keys on."""
    artifacts = run_dir / "artifacts"
    audit_path = artifacts / "promotion_audit.yaml"
    if audit_path.exists():
        audit = load_yaml(audit_path) or {}
        return audit.get("hypothesis_id", run_id), audit.get("passes_deflated_threshold")
    if _specialist_readers_enabled():
        # E-046a Slice 5b-ii-B: no verdict_interpretation.yaml under this flag --
        # same re-point as _write_promotion_audit (hypothesis_card.yaml).
        return _idea_hypothesis_id(run_dir), None
    interp = load_yaml(artifacts / "verdict_interpretation.yaml") or {}
    return interp.get("hypothesis_id", run_id), None


def _mark_holdout_consumed(policy: dict, consumed: list, hyp_id: str) -> None:
    """Step 4 of _route_holdout_evaluation: record the single-use spend in
    campaign_data_policy.yaml holdout_consumed_by.

    CUL-331: the ONLY writer of the tracked policy file. The legacy gate calls
    it directly; the verdict_routing_retired record paths (_record_spent_holdout
    and the S2d unlock) reach it through _mark_holdout_consumed_if_absent. It
    runs AFTER the seal is spent, so it must never refuse. Recording the
    marker is mandatory; keeping the file's comments is best effort.

      * Under the policy lock (_policy_lock), the file is re-read and the
        marker applied to what is on disk NOW: the list becomes the on-disk
        list plus any of `consumed` + [hyp_id] not already in it. Another
        writer's entry is never dropped, and an id already there is never
        written twice.
      * In-place edit when _edit_consumed_in_place can do it and its strict
        parse-back check passes: only the holdout_consumed_by value changes.
        Every other byte stays as it was, comments included.
      * Otherwise (a shape the editor does not handle, a file only
        load_yaml's repair can parse, a non-list value) -> master's behaviour:
        the whole parsed policy plus the marker is rewritten, exactly as
        save_yaml writes it, with a loud WARNING that comments were lost.
      * The write is atomic and durable (_atomic_write_bytes). If the file's
        bytes change between the read and the replace, it is re-read and the
        marker re-applied."""
    new_consumed = _write_consumed_marker(_DATA_POLICY_PATH, policy, consumed, hyp_id)
    policy["holdout_consumed_by"] = new_consumed
    print(f"⚙️  A6.1: {hyp_id} marked in holdout_consumed_by (single-use consumed).")


_CONSUMED_KEY = "holdout_consumed_by"
_POLICY_LOCK_FILENAME = ".campaign_data_policy.yaml.lock"
_MARKER_WRITE_ATTEMPTS = 5
# A top-level (column-0, unquoted) `holdout_consumed_by:` key line. Comment
# lines that merely mention the key start with '#' and never match.
_CONSUMED_KEY_LINE = re.compile(r"holdout_consumed_by[ \t]*:(?=[ \t\r\n]|$)")
# One line of a block sequence: `- item` (any indent, including none).
_BLOCK_ITEM_LINE = re.compile(r"([ \t]*)-(?=[ \t\r\n]|$)")
_COMMENT_OR_BLANK_LINE = re.compile(r"[ \t]*(#.*)?[\r\n]*$")


def _consumed_list(value) -> list:
    """holdout_consumed_by, normalised to a list: None -> [], a list as is,
    a scalar string -> [it] (never iterated as characters). Any other type
    -> [str(value)], so the old value stays visible and nothing is erased."""
    if value is None:
        return []
    if isinstance(value, list):
        return list(value)
    if isinstance(value, str):
        return [value]
    return [str(value)]


@contextlib.contextmanager
def _policy_lock():
    """The policy writer's lock, the same O_EXCL lock-file primitive the
    campaign-memory and KB writers use (campaign_memory._file_lock). If the
    lock cannot be taken, the write goes ahead unlocked with a WARNING, as
    master's writer (which took no lock) always did: the marker is mandatory."""
    lock_path = _DATA_POLICY_PATH.parent / _POLICY_LOCK_FILENAME
    with contextlib.ExitStack() as stack:
        try:
            stack.enter_context(_campaign_memory_module()._file_lock(
                lock_path, "campaign_data_policy.yaml"))
        except Exception as exc:
            print(f"⚠️  WARNING (CUL-331): could not lock {lock_path} ({exc}); recording the "
                  f"holdout consume marker unlocked, as before this lock existed.")
        yield


def _flow_yaml(value) -> str:
    return yaml.safe_dump(value, default_flow_style=True, width=float("inf"),
                          allow_unicode=True).strip()


def _flow_scalar(value) -> str:
    return _flow_yaml([value])[1:-1]  # a flow-safe scalar is block-safe too


def _split_line_ending(line: str) -> tuple:
    body = line.rstrip("\r\n")
    return body, line[len(body):]


def _split_trailing_comment(value: str):
    """(value, comment) for the text after `key:`, or None if it does not
    parse. The comment starts at the first whitespace+'#' whose cut parses to
    the same value, so a '#' inside a quoted scalar is never taken for one."""
    try:
        full = yaml.safe_load(f"k:{value}")
    except yaml.YAMLError:
        return None
    for m in re.finditer(r"[ \t]+#", value):
        try:
            if yaml.safe_load(f"k:{value[:m.start()]}") == full:
                return value[:m.start()], value[m.start():]
        except yaml.YAMLError:
            continue
    return value, ""


def _edit_consumed_in_place(text: str, doc: dict, new_list: list):
    """CUL-331: `text` with holdout_consumed_by set to new_list, and every
    other byte unchanged, or None when this edit cannot do that (the caller
    then falls back to a full rewrite). new_list is the old list plus extras.

      * block list: one `- id` line per extra after the last item, at its
        indent; comment and blank lines between the key and the items, or
        between items, are kept;
      * single-line flow list: `, id` inserted before the closing bracket;
        the existing ids, their quoting and spacing are left alone;
      * empty / null / scalar string value: the value becomes a flow list;
      * key absent: `holdout_consumed_by: [ids]` appended at the end.
    A trailing comment on the key line and all line endings are kept. The
    result must parse to exactly {**doc, holdout_consumed_by: new_list},
    same keys in the same order, else None."""
    old_list = _consumed_list(doc.get(_CONSUMED_KEY))
    extras = new_list[len(old_list):]
    if new_list[:len(old_list)] != old_list or not extras:
        return None
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=True)
    key_idx = [i for i, line in enumerate(lines) if _CONSUMED_KEY_LINE.match(line)]
    if len(key_idx) > 1 or (not key_idx and _CONSUMED_KEY in doc):
        return None
    if not key_idx:
        if lines and not lines[-1].endswith(("\n", "\r")):
            lines[-1] += newline
        lines.append(f"{_CONSUMED_KEY}: {_flow_yaml(new_list)}{newline}")
    else:
        i = key_idx[0]
        items = []
        for j in range(i + 1, len(lines)):
            if _BLOCK_ITEM_LINE.match(lines[j]):
                items.append(j)
            elif not _COMMENT_OR_BLANK_LINE.fullmatch(lines[j]):
                break
        body, ending = _split_line_ending(lines[i])
        prefix = body[:_CONSUMED_KEY_LINE.match(body).end()]
        split = _split_trailing_comment(body[len(prefix):])
        if split is None:
            return None
        value, comment = split
        stripped = value.strip()
        if items:
            if stripped:
                return None
            last = items[-1]
            indent = _BLOCK_ITEM_LINE.match(lines[last]).group(1)
            last_body, last_ending = _split_line_ending(lines[last])
            lines[last] = last_body + (last_ending or newline)
            added = [f"{indent}- {_flow_scalar(x)}" for x in extras]
            lines.insert(last + 1, newline.join(added) + last_ending)
        elif stripped.startswith("[") and stripped.endswith("]"):
            open_, close = value.index("["), value.rindex("]")
            inner = value[open_ + 1:close]
            rendered = ", ".join(_flow_scalar(x) for x in extras)
            keep = len(inner.rstrip())
            inner = (inner[:keep] + ", " + rendered + inner[keep:]) if inner.strip() \
                else (inner + rendered)
            lines[i] = prefix + value[:open_ + 1] + inner + value[close:] + comment + ending
        else:
            lead = value[:len(value) - len(value.lstrip())] or " "
            trail = value[len(value.rstrip()):]
            lines[i] = prefix + lead + _flow_yaml(new_list) + trail + comment + ending
    new_text = "".join(lines)
    expected = {**doc, _CONSUMED_KEY: new_list}
    try:
        new_doc = yaml.safe_load(new_text)
    except yaml.YAMLError:
        return None
    if not isinstance(new_doc, dict) or new_doc != expected or list(new_doc) != list(expected):
        return None
    return new_text


def _parse_policy_text(text: str):
    """(doc, strict): the policy parsed strictly, else through load_yaml's
    repair pass (strict False), else (None, False)."""
    try:
        doc = yaml.safe_load(text)
        if doc is None or isinstance(doc, dict):
            return (doc or {}), True
    except yaml.YAMLError:
        pass
    try:
        docs = list(yaml.safe_load_all(_repair_yaml(text, source=_DATA_POLICY_PATH.name)))
    except yaml.YAMLError:
        return None, False
    doc = docs[0] if docs else None
    return (doc if isinstance(doc, dict) else None), False


def _consume_marker_bytes(raw: bytes | None, policy: dict, consumed: list, hyp_id: str):
    """(bytes to write or None when already recorded, the new list) for the
    policy file whose current bytes are `raw` (None = no file)."""
    text = None if raw is None else raw.decode("utf-8")
    doc, strict = _parse_policy_text(text) if text is not None else (None, False)
    base = doc if doc is not None else dict(policy)  # unparseable: master's view
    old_value = base.get(_CONSUMED_KEY)
    new_list = _consumed_list(old_value)
    for x in _consumed_list(consumed) + [hyp_id]:
        if x not in new_list:
            new_list.append(x)
    if doc is not None and new_list == _consumed_list(old_value) and (
            old_value is None or isinstance(old_value, (list, str))):
        return None, new_list
    if strict and (old_value is None or isinstance(old_value, (list, str))):
        new_text = _edit_consumed_in_place(text, doc, new_list)
        if new_text is not None:
            return new_text.encode("utf-8"), new_list
    if old_value is not None and not isinstance(old_value, (list, str)):
        print(f"⚠️  WARNING (CUL-331): campaign_data_policy.yaml {_CONSUMED_KEY} was a "
              f"{type(old_value).__name__}, not a list: kept as {_consumed_list(old_value)!r} "
              f"at the head of the new list.")
    if raw is not None:
        print(f"⚠️  WARNING (CUL-331): campaign_data_policy.yaml could not be edited in place; "
              f"it was REWRITTEN whole to record the holdout consume marker for {hyp_id}, and "
              f"its comments were LOST. Restore them from git by hand, keeping the "
              f"{_CONSUMED_KEY} value now on disk.")
    rewritten = {**base, _CONSUMED_KEY: new_list}
    validate_workflow_artifact(_DATA_POLICY_PATH, rewritten)  # save_yaml parity
    return _yaml_file_bytes(rewritten), new_list


def _write_consumed_marker(path: Path, policy: dict, consumed: list, hyp_id: str) -> list:
    """The consume-marker write (see _mark_holdout_consumed); returns the
    list now on disk. The bytes read are compared with the file again just
    before os.replace; a change in between means re-read and re-apply. The
    last attempt writes regardless, as master's writer always did."""
    with _policy_lock():
        for attempt in range(_MARKER_WRITE_ATTEMPTS):
            raw = path.read_bytes() if path.exists() else None
            data, new_list = _consume_marker_bytes(raw, policy, consumed, hyp_id)
            if data is None:
                print(f"⚙️  A6.1: {hyp_id} was already in holdout_consumed_by on disk.")
                return new_list
            last = attempt == _MARKER_WRITE_ATTEMPTS - 1
            if _atomic_write_bytes(path, data, durable=True, expect=_ANY_BYTES if last else raw):
                return new_list
            print(f"⚠️  campaign_data_policy.yaml changed while recording {hyp_id}; "
                  f"re-reading and re-applying the marker.")
    raise AssertionError("unreachable: the last attempt always writes")


def _load_data_policy() -> dict:
    return (load_yaml(_DATA_POLICY_PATH) or {}) if _DATA_POLICY_PATH.exists() else {}


def _holdout_already_spent(hyp_id: str, policy: dict | None = None) -> bool:
    """The single-use check (A6.1), in one place: is hyp_id in
    campaign_data_policy.yaml holdout_consumed_by?"""
    policy = _load_data_policy() if policy is None else policy
    return hyp_id in _consumed_list(policy.get("holdout_consumed_by"))  # exact, never substring


def _mark_holdout_consumed_if_absent(hyp_id: str) -> bool:
    """The consume marker, written only when absent (so a crash before or
    after the write ends with exactly one entry). True when written now."""
    policy = _load_data_policy()
    if _holdout_already_spent(hyp_id, policy):
        print(f"⚙️  A6.1: {hyp_id} already in holdout_consumed_by -- the spend is on record.")
        return False
    _mark_holdout_consumed(policy, policy.get("holdout_consumed_by") or [], hyp_id)
    return True


def _holdout_result_terminal(status: str) -> str | None:
    """The gate's step-4 mapping: pass -> completed_promoted, fail ->
    completed_rejected, anything else -> None (a human decides)."""
    return {"pass": "completed_promoted", "fail": "completed_rejected"}.get(status)


# Slice 6c S2d review fix 3: a holdout_result.yaml with no valid operator
# unlock is recorded as consumed, then always pauses -- never a promotion.
HOLDOUT_SPENT_WITHOUT_UNLOCK_FLAG = "holdout_spent_without_unlock"
# pipeline_state.yaml key: the per-run consume intent, written BEFORE the marker
# (S2d; also by the S2a record path, review fix 1 needs it to account the spend).
HOLDOUT_CONSUME_RECORD_KEY = "holdout_consume_record"


def _write_consume_intent(run_dir: Path, run_id: str, hyp_id: str, **extra) -> dict:
    """Persists the run's consume intent (hypothesis_id, the result's sha256,
    whether the hypothesis had ALREADY consumed the holdout before this run)
    before the marker is written. Written once: an existing intent is kept."""
    state = load_yaml(run_dir / "pipeline_state.yaml") or {}
    if state.get(HOLDOUT_CONSUME_RECORD_KEY):
        return state[HOLDOUT_CONSUME_RECORD_KEY]
    hr_path = run_dir / "artifacts" / "holdout_result.yaml"
    intent = {"hypothesis_id": hyp_id, "run_id": run_id,
              "consumed_before": _holdout_already_spent(hyp_id),
              "holdout_result_sha256": hashlib.sha256(hr_path.read_bytes()).hexdigest(),
              "recorded_at": datetime.now(timezone.utc).isoformat(), **extra}
    update_state(path=run_dir, **{HOLDOUT_CONSUME_RECORD_KEY: intent})
    return intent


def _record_spent_holdout(run_dir: Path, run_id: str) -> str:
    """Slice 6c S2a code review (item 1), tightened by S2d review fixes 3 and 8.
    Under verdict_routing_retired, a run found at holdout_evaluation WITH
    artifacts/holdout_result.yaml and WITHOUT a valid operator unlock has spent
    the seal by hand. The spend is recorded first (the consume intent, then the
    marker if absent), and the run then ALWAYS pauses as
    holdout_spent_without_unlock: no unlock, no promotion. hypothesis_id comes
    only from hypothesis_card.yaml, never a promotion_audit.yaml."""
    hyp_id = _idea_hypothesis_id(run_dir)
    _write_consume_intent(run_dir, run_id, hyp_id, unlock=None)
    _mark_holdout_consumed_if_absent(hyp_id)
    hr = load_yaml(run_dir / "artifacts" / "holdout_result.yaml") or {}
    status = str(hr.get("status", "")).lower()
    print(f"\n🛑 verdict_routing_retired: the holdout spent by hand for {hyp_id} is recorded "
          f"(status={status!r}), but no operator unlock authorised it -- never promoted. "
          f"See docs/RUNBOOK.md §3 ({HOLDOUT_SPENT_WITHOUT_UNLOCK_FLAG}).")
    update_state(path=run_dir, flags={HOLDOUT_SPENT_WITHOUT_UNLOCK_FLAG: True})
    return "human_pause"


# ---------------------------------------------------------------------------
# Slice 6c S2d -- the holdout unlock (S1_FINDINGS_6C.md guess 1 and the
# operator decision of 2026-09-25), under orchestrator.verdict_routing_retired
# only. The holdout is reached ONLY through branch 3: a backtest passed every
# profit bar -> the profit_bars_reached stop -> the operator resumes with
# artifacts/holdout_decision.yaml. The grid's idea_status plays no part: a
# validated idea never reaches the holdout by itself, and a refuted or
# inconclusive idea whose variant passed the bars may still be spent on.
#   * spend    -> holdout_evaluation for the named variant; refused unless this
#                 run's evaluation records PASS for it under the current
#                 bars file (by sha256), its deflated Sharpe still
#                 clears the bar on the CURRENT trial ledger, the operator
#                 attests the trial ledgers are merged, no other run holds an
#                 unfinished spend of the one physical seal, and the hypothesis
#                 has not consumed the holdout.
#   * continue -> the holdout is untouched, the choice is recorded, the run
#                 ends completed_<idea_status> and decide-next runs.
# Once holdout_result.yaml exists the spend is RECORDED FIRST (consume intent,
# then the marker if absent); only then can a check change the ending (an
# unbound or relabelled result, a second spend, the research_only hold) --
# never skip the record. Code review fixes 1-10 (tests in
# tests/test_e059_6c_s2d_review_fixes.py).
# ---------------------------------------------------------------------------

HOLDOUT_DECISION_FILE = "holdout_decision.yaml"
HOLDOUT_DECISIONS = ("spend", "continue")
# The operator file's closed schema: a key outside these two tuples is refused
# (a typo such as `varient_id` must never read as "no variant named").
HOLDOUT_DECISION_REQUIRED_KEYS = ("decision", "run_id", "profit_bars_stop_evaluation",
                                  "ratified_by", "ratified_at")
# variant_id and trial_ledgers_merged: true are required for spend.
HOLDOUT_DECISION_OPTIONAL_KEYS = ("variant_id", "trial_ledgers_merged", "note")
# What holdout_result.yaml must state, besides `status`, to bind it to the unlock.
HOLDOUT_RESULT_BINDING_KEYS = ("variant_id", "trial_id", "decision_sha256")
# pipeline_state.yaml keys, written only under the flag.
HOLDOUT_DECISION_RECORD_KEY = "holdout_decision_record"
HOLDOUT_UNLOCK_REFUSAL_KEY = "holdout_unlock_refusal"
HOLDOUT_RELABEL_KEY = "holdout_result_relabel_attempts"
# The evaluation's record of the whole bars file (review fix 7).
BARS_FILE_SHA_FIELD = "bars_file_sha256"
# Sticky pause flags (run_campaign._classify_human_pause; RUNBOOK §3 rows).
HOLDOUT_UNLOCK_REFUSED_FLAG = "holdout_unlock_refused"
HOLDOUT_AWAITING_RESULT_FLAG = "holdout_unlocked_awaiting_result"
HOLDOUT_RESULT_INCONCLUSIVE_FLAG = "holdout_unlocked_result_inconclusive"
HOLDOUT_RESULT_UNBOUND_FLAG = "holdout_result_unbound"
HOLDOUT_RESULT_RELABELLED_FLAG = "holdout_result_relabelled"
# Every refusal code; each has its own RUNBOOK §3 row (pinned by the tests).
HOLDOUT_UNLOCK_REFUSALS = (
    "decision_missing",        # no holdout_decision.yaml
    "decision_malformed",      # unparseable, not a mapping, or outside the schema
    "decision_wrong_run",      # run_id names another run
    "decision_stale",          # written for another profit_bars_reached stop
    "decision_changed",        # edited after it unlocked the spend, before the backtest
    "variant_not_passing",     # the named variant is not PASS in this run's evaluation
    "bars_changed",            # the evaluation was graded under another bars file
    "holdout_already_consumed",  # the hypothesis is in holdout_consumed_by
    "seal_spend_pending",      # another run or writer holds an unfinished spend
    "ledgers_not_merged",      # spend without trial_ledgers_merged: true
    "dsr_fails_current_ledger",  # deflated Sharpe does not clear the bar on today's ledger
)


class HoldoutUnlockRefused(Exception):
    """A spend or continue that must not proceed. `code` is one of
    HOLDOUT_UNLOCK_REFUSALS."""

    def __init__(self, code: str, detail: str):
        if code not in HOLDOUT_UNLOCK_REFUSALS:
            raise ValueError(f"unknown holdout-unlock refusal code {code!r}")
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _holdout_decision_path(run_dir: Path) -> Path:
    return run_dir / "artifacts" / HOLDOUT_DECISION_FILE


def _is_ratified(value) -> bool:
    """A non-blank string (the decision file's run_id / stop / ratified_by /
    variant_id). None, "", "   " or a non-string are refused."""
    return isinstance(value, str) and bool(value.strip())


def _bars_file_path() -> Path:
    return ROOT / "config" / "profitability_bars.yaml"


def _bars_file_sha256() -> str | None:
    path = _bars_file_path()
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def _read_holdout_decision(run_dir: Path) -> tuple:
    """(doc, sha256) of the operator file, schema-checked. Parsed with plain
    yaml.safe_load -- never load_yaml's repair pass, which could turn a broken
    operator file into a plausible one."""
    from datetime import date as _date
    path = _holdout_decision_path(run_dir)
    if not path.is_file():
        raise HoldoutUnlockRefused("decision_missing", f"{path} does not exist")
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    try:
        doc = yaml.safe_load(raw.decode("utf-8"))
    except (yaml.YAMLError, UnicodeDecodeError) as e:
        raise HoldoutUnlockRefused("decision_malformed", f"{path} does not parse: {e}")
    if not isinstance(doc, dict):
        raise HoldoutUnlockRefused("decision_malformed",
                                   f"{path} is not a mapping (got {type(doc).__name__})")
    allowed = HOLDOUT_DECISION_REQUIRED_KEYS + HOLDOUT_DECISION_OPTIONAL_KEYS
    unknown = sorted(str(k) for k in doc if k not in allowed)
    missing = [k for k in HOLDOUT_DECISION_REQUIRED_KEYS if k not in doc]
    if unknown or missing:
        raise HoldoutUnlockRefused(
            "decision_malformed", f"{path}: unknown key(s) {unknown}, missing key(s) {missing}; "
            f"allowed: {list(allowed)}")
    problems = []
    if doc["decision"] not in HOLDOUT_DECISIONS:
        problems.append(f"decision={doc['decision']!r} is not one of {list(HOLDOUT_DECISIONS)}")
    for key in ("run_id", "profit_bars_stop_evaluation", "ratified_by"):
        if not _is_ratified(doc[key]):
            problems.append(f"{key} must be a non-empty (quoted) string, got {doc[key]!r}")
    ratified_at = doc["ratified_at"]
    if isinstance(ratified_at, str):
        try:
            datetime.fromisoformat(ratified_at.strip())
        except ValueError:
            problems.append(f"ratified_at={ratified_at!r} is not an ISO date or datetime")
    elif not isinstance(ratified_at, (_date, datetime)):
        problems.append(f"ratified_at must be an ISO date or datetime, got {ratified_at!r}")
    variant = doc.get("variant_id")
    if doc["decision"] == "spend" and not _is_ratified(variant):
        problems.append("variant_id (the passing backtest) is required for decision: spend")
    elif variant is not None and not _is_ratified(variant):
        problems.append(f"variant_id must be a non-empty string or absent, got {variant!r}")
    merged = doc.get("trial_ledgers_merged")
    if merged is not None and not isinstance(merged, bool):
        problems.append(f"trial_ledgers_merged must be an unquoted true/false, got {merged!r}")
    if doc.get("note") is not None and not isinstance(doc["note"], str):
        problems.append("note must be a string")
    if problems:
        raise HoldoutUnlockRefused("decision_malformed", f"{path}: " + "; ".join(problems))
    return doc, sha


def _evaluation_under_current_bars(ev: dict) -> dict:
    """Refuses unless the bars file in place now is byte-for-byte the file the
    evaluation was graded under (its whole-file sha256, review fix 7), so the
    bars cannot change under a PASS unnoticed. Bars ratification is the
    operator's manual check, not enforced here (operator decision 2026-09-26,
    replacing review fix 6). Returns the loaded bars."""
    try:
        bars = _load_profitability_bars()
    except ProfitabilityBarsSchemaError as e:
        raise HoldoutUnlockRefused("bars_changed", f"the current bars file does not load: {e}")
    graded, now = ev.get(BARS_FILE_SHA_FIELD), _bars_file_sha256()
    if not graded or graded != now:
        raise HoldoutUnlockRefused(
            "bars_changed", f"the evaluation was graded under bars file sha256 {graded!r}; the "
            f"file in place now is {now!r}")
    return bars


def _dsr_on_current_ledger(run_dir: Path, variant: str, entry: dict, bars: dict,
                           ev: dict) -> dict:
    """Review fix 8: the variant's deflated Sharpe, recomputed NOW on the
    current campaign trial ledger with the promotion audit's own evaluator
    (_promotion_dsr_context), must still clear deflated_sharpe_threshold. N only
    grows, so a figure graded earlier on fewer trials is never trusted alone."""
    basis = (ev.get("dsr_basis") or {}).get("n_dsr_total")
    if entry.get("trial_id") in _invalidated_trial_ids():
        raise HoldoutUnlockRefused("dsr_fails_current_ledger",
                                   f"trial {entry.get('trial_id')!r} is now invalidated_artifact")
    rel = entry.get("protocol_result_ref")
    try:
        pr = load_yaml(run_dir / rel) if rel else None
        if not isinstance(pr, dict):
            raise ValueError(f"no readable protocol_result at {rel!r}")
        ctx = _promotion_dsr_context()
        dsr = ctx["dsr_candidate"](pr)[4].get("deflated_sharpe_ratio")
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise HoldoutUnlockRefused("dsr_fails_current_ledger",
                                   f"the deflated Sharpe cannot be reproduced: {e}")
    threshold = bars["deflated_sharpe_threshold"]
    if not isinstance(dsr, (int, float)) or not math.isfinite(dsr) or dsr < threshold:
        raise HoldoutUnlockRefused(
            "dsr_fails_current_ledger", f"variant {variant!r}: deflated Sharpe on the current "
            f"ledger is {dsr!r} (threshold {threshold}; ledger N now {ctx['n_dsr_total']}, at "
            f"grading {basis})")
    return {"deflated_sharpe_ratio": dsr, "n_dsr_total": ctx["n_dsr_total"],
            "n_trials": ctx["n_trials"], "n_dsr_total_at_grading": basis}


_FINISHED_PREFIXES = ("completed", "rejected", "failed_validation")


def _other_pending_spends(run_id: str) -> list:
    """Review fix 1 -- one physical seal, one pending spend. Every OTHER run
    whose pipeline_state.yaml holds a spend decision or a consume record and
    has not finished (any hypothesis), plus every hypothesis in the tracked
    campaign_data_policy.yaml holdout_consumed_by that no finished run here
    accounts for (the other writer's spend, or a hand spend, which may still be
    in flight). Fail closed: an unreadable state counts as pending."""
    pending, finished_ids = [], set()
    for sp in sorted((ROOT / "runs").glob("*/pipeline_state.yaml")):
        rid = sp.parent.name
        try:
            st = load_yaml(sp) or {}
        except Exception as e:
            if rid != run_id:
                pending.append(f"{rid} (pipeline_state.yaml unreadable: {e})")
            continue
        consume = st.get(HOLDOUT_CONSUME_RECORD_KEY)
        spend = st.get(HOLDOUT_DECISION_RECORD_KEY)
        done = str(st.get("pending_stage") or "").startswith(_FINISHED_PREFIXES)
        if done and isinstance(consume, dict):
            finished_ids.add(consume.get("hypothesis_id"))
        if rid == run_id or done:
            continue
        if consume or (isinstance(spend, dict) and spend.get("decision") == "spend"):
            pending.append(f"{rid} ({'consume record' if consume else 'spend decision'}, "
                           f"pending_stage={st.get('pending_stage')!r})")
    unaccounted = [h for h in _consumed_list(_load_data_policy().get("holdout_consumed_by"))
                   if h not in finished_ids]
    if unaccounted:
        pending.append(f"campaign_data_policy.yaml holdout_consumed_by {unaccounted} (no finished "
                       f"run in this checkout accounts for them: another writer's or a hand spend)")
    return pending


def _profit_stop_raised(run_dir: Path, run_id: str, state: dict | None = None) -> dict | None:
    """Review fix 10: this run's every_backtest evaluation when the
    profit_bars_reached stop was raised for it (a passing variant, and the
    run's recorded stop names its generated_at); else None."""
    if state is None:
        state = load_yaml(run_dir / "pipeline_state.yaml") or {}
    ev = _load_every_backtest_evaluation(run_dir, run_id)
    if (ev is None or not ev.get("passing") or not state.get("profit_bars_stop_evaluation")
            or state.get("profit_bars_stop_evaluation") != ev.get("generated_at")):
        return None
    return ev


def _validate_holdout_decision(run_dir: Path, run_id: str, state: dict) -> dict:
    """The operator's decision checked against THIS run and THIS stop; for a
    spend, every precondition of the operator decision of 2026-09-25 and of
    code-review fixes 1, 6-9. Read-only. Returns the record to store
    (HOLDOUT_DECISION_RECORD_KEY); raises HoldoutUnlockRefused otherwise."""
    doc, sha = _read_holdout_decision(run_dir)
    if doc["run_id"] != run_id:
        raise HoldoutUnlockRefused("decision_wrong_run",
                                   f"run_id={doc['run_id']!r}, but this run is {run_id!r}")
    ev = _profit_stop_raised(run_dir, run_id, state)
    stop = state.get("profit_bars_stop_evaluation")
    if ev is None:
        raise HoldoutUnlockRefused(
            "decision_stale", f"this run has no raised profit_bars_reached stop matching its "
            f"current evaluation (pipeline_state profit_bars_stop_evaluation={stop!r})")
    if doc["profit_bars_stop_evaluation"] != stop:
        raise HoldoutUnlockRefused(
            "decision_stale", f"profit_bars_stop_evaluation={doc['profit_bars_stop_evaluation']!r} "
            f"names another stop; this run's stop is {stop!r}")
    variant = doc.get("variant_id")
    record = {
        "decision": doc["decision"], "run_id": run_id,
        "profit_bars_stop_evaluation": stop, "variant_id": variant,
        "ratified_by": doc["ratified_by"], "ratified_at": str(doc["ratified_at"]),
        "note": doc.get("note"), "decision_sha256": sha,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    entry = None
    if variant is not None:
        entry = (ev.get("variants") or {}).get(variant)
        bar_rows = (entry or {}).get("bars") or []
        if (variant not in (ev.get("passing") or []) or not isinstance(entry, dict)
                or entry.get("result") != "PASS" or not bar_rows
                or any(not isinstance(r, dict) or r.get("result") != "PASS" for r in bar_rows)):
            raise HoldoutUnlockRefused(
                "variant_not_passing", f"variant {variant!r} is not PASS on every bar in this "
                f"run's profit_bars_evaluation.yaml (passing: {ev.get('passing')})")
        record.update(trial_id=entry.get("trial_id"),
                      protocol_result_ref=entry.get("protocol_result_ref"))
    if doc["decision"] == "spend":
        if doc.get("trial_ledgers_merged") is not True:
            raise HoldoutUnlockRefused(
                "ledgers_not_merged", "a spend needs `trial_ledgers_merged: true`, the "
                "operator's attestation that both writers' trial ledgers are merged (no "
                "holdout touch until they are)")
        bars = _evaluation_under_current_bars(ev)
        hyp_id = _idea_hypothesis_id(run_dir)  # never a promotion_audit.yaml (fix 8)
        if _holdout_already_spent(hyp_id):
            raise HoldoutUnlockRefused(
                "holdout_already_consumed", f"{hyp_id} is already in campaign_data_policy.yaml "
                f"holdout_consumed_by -- the holdout is single-use per hypothesis (A6.1)")
        others = _other_pending_spends(run_id)
        if others:
            raise HoldoutUnlockRefused(
                "seal_spend_pending", "the holdout is one physical seal and another spend is "
                "unfinished: " + "; ".join(others))
        record["dsr_recheck"] = _dsr_on_current_ledger(run_dir, variant, entry, bars, ev)
        record["hypothesis_id"] = hyp_id
        record["trial_ledgers_merged"] = True
    return record


def _refuse_holdout_unlock(run_dir: Path, refusal: HoldoutUnlockRefused) -> str:
    """The classified pause for a refused decision. Nothing is spent; any
    earlier decision record is dropped, so a stale spend can never survive a
    refusal. pending_stage is left where it was."""
    print(f"\n🛑 HOLDOUT UNLOCK REFUSED ({refusal.code}): {refusal.detail}. Nothing was spent. "
          f"See docs/RUNBOOK.md §3 ({HOLDOUT_UNLOCK_REFUSED_FLAG} / {refusal.code}).")
    update_state(path=run_dir, **{HOLDOUT_DECISION_RECORD_KEY: None})
    update_state(path=run_dir, status="paused_for_human",
                 flags={HOLDOUT_UNLOCK_REFUSED_FLAG: True},
                 **{HOLDOUT_UNLOCK_REFUSAL_KEY: {
                     "code": refusal.code, "detail": refusal.detail,
                     "at": datetime.now(timezone.utc).isoformat()}})
    return "human_pause"


def _clear_sticky_flags(run_dir: Path, *flags: str) -> None:
    """Clears the named flags only when set (update_state merges `flags`, so a
    flag left true would mask a later, different pause)."""
    state = load_yaml(run_dir / "pipeline_state.yaml") or {}
    set_flags = {f: False for f in flags if (state.get("flags") or {}).get(f)}
    if set_flags:
        update_state(path=run_dir, flags=set_flags)


def _holdout_unlock_route(run_dir: Path, run_id: str) -> str | None:
    """Called by run_loop after regroup_record, under the flag, when the
    profit-bars stop route returned None. None when the stop was NOT raised for
    this run's current evaluation (no passing variant: any holdout_decision.yaml
    is ignored, and a validated idea goes on to completed_validated like any
    other). Otherwise this is the resume from profit_bars_reached:
      already spent (a consume record or holdout_result.yaml) -> "holdout_evaluation"
                  (the record step; no decision can route around it);
      spend    -> "holdout_evaluation" (the run is still recorded in
                  campaign_state.runs, as the retired route would);
      continue -> None (the retired route follows: completed_<idea_status>);
      refused  -> "human_pause" (holdout_unlock_refused)."""
    state = load_yaml(run_dir / "pipeline_state.yaml") or {}
    if _profit_stop_raised(run_dir, run_id, state) is None:
        if _holdout_decision_path(run_dir).exists():
            print(f"⚙️  holdout unlock: {HOLDOUT_DECISION_FILE} ignored -- no profit_bars_reached "
                  f"stop was raised for this run's evaluation; the holdout is reached only "
                  f"from that stop.")
        return None
    if state.get(HOLDOUT_CONSUME_RECORD_KEY) or (run_dir / "artifacts" / "holdout_result.yaml").exists():
        print(f"⚠️  holdout unlock: {run_id} already spent the holdout (a consume record or "
              f"holdout_result.yaml is present) -- routing to holdout_evaluation to record it; "
              f"{HOLDOUT_DECISION_FILE} is not consulted.")
        return "holdout_evaluation"
    try:
        record = _validate_holdout_decision(run_dir, run_id, state)
    except HoldoutUnlockRefused as refusal:
        return _refuse_holdout_unlock(run_dir, refusal)
    update_state(path=run_dir, **{HOLDOUT_DECISION_RECORD_KEY: None,
                                  HOLDOUT_UNLOCK_REFUSAL_KEY: None})
    update_state(path=run_dir, **{HOLDOUT_DECISION_RECORD_KEY: record})
    _clear_sticky_flags(run_dir, HOLDOUT_UNLOCK_REFUSED_FLAG, HOLDOUT_AWAITING_RESULT_FLAG)
    if record["decision"] == "continue":
        print(f"\n📒 holdout decision: continue (ratified by {record['ratified_by']} at "
              f"{record['ratified_at']}). The holdout is untouched; the run ends "
              f"completed_<idea_status> and decide-next picks the next run.")
        return None
    _record_run_in_campaign_state(run_id, _extract_diagnostics(run_dir))
    print(f"\n🔓 holdout decision: SPEND on variant {record['variant_id']!r} (trial "
          f"{record.get('trial_id')!r}, {record.get('protocol_result_ref')}), hypothesis "
          f"{record['hypothesis_id']}, ratified by {record['ratified_by']} at "
          f"{record['ratified_at']}. Routing to holdout_evaluation.")
    return "holdout_evaluation"


def _spend_unlock_for(state: dict, run_id: str) -> dict | None:
    """The spend record that lets holdout_evaluation run under the flag, or
    None: it must name this run, say spend, and be bound to the run's current
    profit_bars_reached stop."""
    rec = state.get(HOLDOUT_DECISION_RECORD_KEY)
    if (isinstance(rec, dict) and rec.get("decision") == "spend" and rec.get("run_id") == run_id
            and rec.get("profit_bars_stop_evaluation")
            and rec.get("profit_bars_stop_evaluation") == state.get("profit_bars_stop_evaluation")):
        return rec
    return None


def _spent_holdout_ending(run_dir: Path, run_id: str, intent: dict, unlock: dict) -> str:
    """The ending of an unlocked spend whose record is ALREADY made (intent +
    marker). Every check here changes only the ending, never the record:
    a second spend -> completed_rejected; a relabelled result (fix 5) or one
    not bound to the unlock (fix 4) -> a classified pause; the research_only
    hold; then the gate's pass/fail mapping, an unknown status pausing."""
    hyp_id = intent.get("hypothesis_id")
    if intent.get("consumed_before"):
        print(f"\n🛑 HOLDOUT REFUSED: {hyp_id} had already consumed the single holdout "
              f"evaluation before this run -- a second holdout attempt is forbidden (A6.1). "
              f"This run's spend is on record.")
        return "completed_rejected"
    hr_path = run_dir / "artifacts" / "holdout_result.yaml"
    raw = hr_path.read_bytes()
    now_sha = hashlib.sha256(raw).hexdigest()
    if now_sha != intent.get("holdout_result_sha256"):
        attempts = list((load_yaml(run_dir / "pipeline_state.yaml") or {}).get(HOLDOUT_RELABEL_KEY)
                        or [])
        attempts.append({"holdout_result_sha256": now_sha,
                         "content": raw.decode("utf-8", errors="replace")[:2000],
                         "at": datetime.now(timezone.utc).isoformat()})
        update_state(path=run_dir, flags={HOLDOUT_RESULT_RELABELLED_FLAG: True},
                     **{HOLDOUT_RELABEL_KEY: attempts})
        print(f"\n🛑 holdout_result.yaml changed after the spend was recorded (sha256 "
              f"{intent.get('holdout_result_sha256')} -> {now_sha}). The attempt is recorded; the "
              f"result stays as first recorded. See docs/RUNBOOK.md §3 "
              f"({HOLDOUT_RESULT_RELABELLED_FLAG}).")
        return "human_pause"
    hr = yaml.safe_load(raw.decode("utf-8", errors="replace")) if raw else None
    hr = hr if isinstance(hr, dict) else {}
    expected = {"variant_id": unlock.get("variant_id"), "trial_id": unlock.get("trial_id"),
                "decision_sha256": unlock.get("decision_sha256")}
    mismatched = {k: (hr.get(k), v) for k, v in expected.items() if hr.get(k) != v}
    card_hyp = _idea_hypothesis_id(run_dir)
    if mismatched or card_hyp != unlock.get("hypothesis_id") or hyp_id != unlock.get("hypothesis_id"):
        update_state(path=run_dir, flags={HOLDOUT_RESULT_UNBOUND_FLAG: True})
        print(f"\n🛑 holdout_result.yaml is not bound to the unlock: mismatched "
              f"{ {k: {'result': a, 'unlock': b} for k, (a, b) in mismatched.items()} }, "
              f"hypothesis card {card_hyp!r} / recorded {hyp_id!r} / unlock "
              f"{unlock.get('hypothesis_id')!r}. The spend is on record; never promoted. "
              f"See docs/RUNBOOK.md §3 ({HOLDOUT_RESULT_UNBOUND_FLAG}).")
        return "human_pause"
    if _research_only_hold(run_dir, run_id):
        return "human_pause"
    status = str(hr.get("status", "")).lower()
    terminal = _holdout_result_terminal(status)
    if terminal is None:
        update_state(path=run_dir, flags={HOLDOUT_RESULT_INCONCLUSIVE_FLAG: True})
        print(f"\n⏸️  HOLDOUT INCONCLUSIVE for {hyp_id} (status={status!r}); the spend is on "
              f"record. See docs/RUNBOOK.md §3 ({HOLDOUT_RESULT_INCONCLUSIVE_FLAG}).")
        return "human_pause"
    print(f"\n{'🏆' if terminal == 'completed_promoted' else '🛑'} holdout_result status="
          f"{status} for {hyp_id} (variant {unlock.get('variant_id')!r}) -> {terminal}.")
    return terminal


def _unlocked_holdout_evaluation(run_dir: Path, run_id: str, state: dict) -> str:
    """holdout_evaluation under the flag, after an operator spend unlocked it.
      * no holdout_result.yaml yet (nothing spent): the decision is re-checked
        from disk (never trusted from state alone; edited since -> refused),
        including the pending-spend, ledger and DSR checks; then the
        research_only hold; then a pause for the manual backtest
        (holdout_unlocked_awaiting_result).
      * holdout_result.yaml present (the seal is spent): RECORD FIRST -- the
        consume intent, then the marker if absent -- and only then
        _spent_holdout_ending decides the ending. No precondition can refuse
        before the record (review fix 2). A crash anywhere after the intent
        resumes here and only finishes the record."""
    unlock = _spend_unlock_for(state, run_id)
    consume = state.get(HOLDOUT_CONSUME_RECORD_KEY)
    if unlock is None:
        raise ValueError(f"{run_id}: holdout_evaluation reached without this run's spend unlock")
    hr_path = run_dir / "artifacts" / "holdout_result.yaml"
    if not consume and not hr_path.exists():
        try:
            fresh = _validate_holdout_decision(run_dir, run_id, state)
        except HoldoutUnlockRefused as refusal:
            return _refuse_holdout_unlock(run_dir, refusal)
        if (fresh["decision"] != "spend" or fresh["decision_sha256"] != unlock["decision_sha256"]
                or fresh.get("variant_id") != unlock.get("variant_id")):
            return _refuse_holdout_unlock(run_dir, HoldoutUnlockRefused(
                "decision_changed", f"{HOLDOUT_DECISION_FILE} changed after it unlocked the spend "
                f"(recorded sha256 {unlock['decision_sha256']}, now {fresh['decision_sha256']})"))
        if _research_only_hold(run_dir, run_id):
            return "human_pause"
        holdout_range = _load_data_policy().get("holdout_range", [])
        print(f"\n⏸️  HOLDOUT: holdout_result.yaml not yet present for {unlock['hypothesis_id']}. "
              f"Run the holdout backtest by hand for variant {unlock['variant_id']!r} ONLY "
              f"(trial {unlock.get('trial_id')!r}) on the range {holdout_range}, write "
              f"holdout_result.yaml with status, variant_id, trial_id and decision_sha256 "
              f"{unlock['decision_sha256']}, then resume.")
        update_state(path=run_dir, flags={HOLDOUT_AWAITING_RESULT_FLAG: True})
        return "human_pause"
    if not hr_path.exists():
        raise FileNotFoundError(f"{hr_path} is missing, but {run_id} recorded a holdout spend "
                                f"against it -- restore it (never delete a spent result)")
    _clear_sticky_flags(run_dir, HOLDOUT_AWAITING_RESULT_FLAG, HOLDOUT_RESULT_INCONCLUSIVE_FLAG)
    intent = consume or _write_consume_intent(
        run_dir, run_id, unlock["hypothesis_id"], unlock={
            k: unlock.get(k) for k in ("variant_id", "trial_id", "protocol_result_ref",
                                       "decision_sha256")})
    if intent.get("run_id") != run_id or not intent.get("hypothesis_id"):
        raise ValueError(f"{HOLDOUT_CONSUME_RECORD_KEY} on {run_id} is not this run's: {intent!r}")
    _mark_holdout_consumed_if_absent(intent["hypothesis_id"])
    return _spent_holdout_ending(run_dir, run_id, intent, unlock)


def holdout_decision_resume_blocker(run_dir: Path, run_id: str) -> str | None:
    """For run_campaign.resume_paused_entry (the profit_bars_reached and
    holdout_unlock_refused pauses, flag on): the refusal a resume would meet,
    or None. Read-only; run_loop checks again, authoritatively."""
    state = load_yaml(run_dir / "pipeline_state.yaml") or {}
    if _profit_stop_raised(run_dir, run_id, state) is None:
        return None
    if state.get(HOLDOUT_CONSUME_RECORD_KEY) or (run_dir / "artifacts" / "holdout_result.yaml").exists():
        return None  # already spent: run_loop routes to the record step (_holdout_unlock_route)
    try:
        _validate_holdout_decision(run_dir, run_id, state)
    except HoldoutUnlockRefused as refusal:
        return f"{HOLDOUT_UNLOCK_REFUSED_FLAG} ({refusal.code}): {refusal.detail}"
    return None


# ---------------------------------------------------------------------------
# E-059 S3 / slice 6c S2b -- campaign review under verdict_routing_retired
# (S1_FINDINGS_6C.md §5 and guesses 3-6; operator decision of 2026-09-25: build
# on the S1 defaults; code-review fixes 1-10). Reached only when run_loop's
# pre-flight read the flag on.
#   * Cadence (guess 3, review fixes 2+4): a review is due when at least
#     review_every_n_runs (campaign_state.yaml, default 6) runs recorded in
#     campaign_record/campaign_memory.yaml without an engineering_fault are
#     not yet covered by a COMPLETED review (campaign_record/
#     campaign_review_log.yaml). Only a completed review resets the count, so
#     a missed one carries forward and none fires twice on the same runs.
#     Never the retired failed_families list. Evaluated in run_loop after the
#     grid route, so the component-error pause and the profit-bars stop come first.
#   * continue / escalate_* (guess 4): recorded, never routed; they return
#     before any verdict_interpretation.yaml could be read.
#   * reframe (guess 6, review fix 1): a candidate brief whose criteria are
#     written at step 1a (criteria_from: hypothesis_generation, operator
#     decision 2 of 6b) with the source run's protocol pin; process_once
#     registers it as a `ready` queue entry (origin campaign_review) BEFORE
#     decide-next, which alone picks the next run.
#   * terminate (guess 5): a real stop -- a classified pause
#     (campaign_review_terminate, RUNBOOK §3), recorded in the append-only
#     campaign_decision.yaml history; an operator's continue-anyway resume
#     records an override there, then the run ends and decide-next runs.
# The run's ending is always completed_<idea_status>, re-read from the grid's
# idea_status.yaml: a review never changes an idea's status.
# ---------------------------------------------------------------------------

import campaign_review_retired as _crr  # tools/ sibling (on sys.path, module top)

# pipeline_state.yaml keys, written only under the flag.
CAMPAIGN_REVIEW_TRIGGER_KEY = "campaign_review_trigger"
CAMPAIGN_REVIEW_REFRAME_KEY = "campaign_review_reframe_brief"
CAMPAIGN_REVIEW_TERMINATE_KEY = "campaign_review_terminate_review"
# The terminate stop's sticky flag; one definition, shared with run_campaign.
CAMPAIGN_REVIEW_TERMINATE_FLAG = _crr.CAMPAIGN_REVIEW_TERMINATE_FLAG
# The queue origin of a reframe's entry (tools/record_schema.py _ORIGIN_VALUES).
CAMPAIGN_REVIEW_ORIGIN = "campaign_review"
# The flag-gated skill note, injected as a required input (never in SKILL.md,
# so the flag-off prompt is unchanged).
_RETIRED_REVIEW_GUIDANCE = "../../workflow_artifacts/skills/campaign-review/RETIRED_ROUTING.md"
# The code-written digest of the campaign memory the review reads (review fix 10).
CAMPAIGN_REVIEW_DIGEST_FILE = "campaign_review_digest.yaml"
REFRAME_BRIEF_REQUIRED_KEYS = _crr.REFRAME_BRIEF_REQUIRED_KEYS
_REVIEW_RECORDED_ONLY = ("continue", "escalate_instrument", "escalate_component")


def _rel_to_run(path: Path) -> str:
    """A ROOT-relative path as a run's handoff input ("../../<rel>")."""
    return "../../" + Path(path).relative_to(ROOT).as_posix()


def _review_log_path() -> Path:
    return ROOT / _crr.REVIEW_LOG_REL


def _review_cadence() -> int:
    n = (load_campaign_state() or {}).get("review_every_n_runs", 6)
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError(f"campaign_state.yaml review_every_n_runs={n!r} is not a positive "
                         f"integer -- refusing to guess the campaign-review cadence.")
    return n


def _retired_review_trigger(run_id: str) -> dict | None:
    """The trigger record when at least review_every_n_runs counted runs are
    not yet covered by a completed review, else None. The run itself must be a
    counted memory entry: regroup_record records it before this is called, so
    its absence is an integrity failure (raises), never a silent "no review"."""
    memory_path = _campaign_memory_path()
    runs = _campaign_memory_module().load_memory(memory_path).get("runs") or {}
    entry = runs.get(run_id)
    if not isinstance(entry, dict) or entry.get("engineering_fault"):
        raise ValueError(
            f"campaign review trigger: {run_id} has no recorded entry without an "
            f"engineering_fault in {memory_path} -- regroup_record records every run before "
            f"this point. Refusing to count runs without it.")
    n = _review_cadence()
    since = _crr.runs_since_last_review(runs, _crr.load_review_log(_review_log_path()))
    if len(since) < n:
        return None
    return {"rule": "runs_since_last_completed_review", "review_every_n_runs": n,
            "runs_since_last_review": len(since), "since_runs": since,
            "memory": memory_path.relative_to(ROOT).as_posix()}


def _idea_status_counts(entries) -> dict:
    counts: dict = {}
    for e in entries:
        key = e.get("idea_status") or f"engineering_fault:{e.get('engineering_fault')}"
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def _write_review_digest(run_dir: Path, trigger: dict) -> Path:
    """Review fix 10: what the review reads instead of the whole memory --
    every run since the last completed review in full, and aggregate counts
    for the earlier ones. Written by code, never by the model."""
    runs = _campaign_memory_module().load_memory(_campaign_memory_path()).get("runs") or {}
    since = set(trigger["since_runs"])
    earlier = [e for rid, e in sorted(runs.items()) if rid not in since]
    log = _crr.load_review_log(_review_log_path())
    last = (log.get("completed") or [None])[-1]
    digest = {
        "schema_version": 1,
        "written_by": "run_phase1_research._write_review_digest (E-059 slice 6c S2b)",
        "review_every_n_runs": trigger["review_every_n_runs"],
        "last_completed_review": ({k: last.get(k) for k in ("run_id", "recommendation",
                                                            "completed_at")}
                                  if isinstance(last, dict) else None),
        "runs_since_last_review": {rid: runs[rid] for rid in sorted(since) if rid in runs},
        "earlier_runs": {"count": len(earlier),
                         "idea_status_counts": _idea_status_counts(earlier)},
        "all_runs_idea_status_counts": _idea_status_counts(runs.values()),
    }
    path = run_dir / "artifacts" / CAMPAIGN_REVIEW_DIGEST_FILE
    save_yaml(path, digest)
    return path


def _write_retired_review_handoff(run_dir: Path, run_id: str) -> Path:
    """The campaign_review handoff under the flag. Written in full (not the
    legacy template: its campaign_state/KB paths predate the campaign_record/
    move and would fail ensure_files, and campaign_state.yaml carries the
    retired fields). Required: the run's digest of the memory and its brief.
    The KB is OPTIONAL (review fix 10): absent, the reason says so and the
    stage still runs. The skill note is added at invoke time
    (_apply_retired_routing_review_context). verdict_interpretation.yaml is
    never an input."""
    kb_reason = ("A5.1-5.3: the KB of tested mechanisms, power-parked findings and exhausted "
                 "cells. Read before any recommendation.")
    if not _KB_PATH.exists():
        kb_reason = ("ABSENT when this review was triggered: the campaign has no knowledge "
                     "base yet. Answer each KB GATE question with 'no KB yet' -- do not invent "
                     "KB content.")
    handoff = {
        "handoff_version": 1,
        "run_id": run_id,
        "from_stage": "regroup_record",
        "to_stage": "campaign_review",
        "assigned_engine": "claude",
        "objective": (
            "Step back from single runs and assess the whole campaign from its memory digest. "
            "Recommend continue, reframe, escalate_instrument, escalate_component or "
            "terminate; under orchestrator.verdict_routing_retired only reframe (a new "
            "brief in the queue) and terminate (a stop for the operator) act."),
        "primary_input_artifact": f"artifacts/{CAMPAIGN_REVIEW_DIGEST_FILE}",
        "required_inputs": [
            {"path": f"artifacts/{CAMPAIGN_REVIEW_DIGEST_FILE}",
             "reason": "the campaign memory, digested by code: every run since the last "
                       "completed review in full (idea_status from the grid only, grid counts, "
                       "registry, proposals), aggregate counts for the earlier runs."},
            {"path": "artifacts/research_brief.yaml",
             "reason": "this run's research question, to compare with the campaign's direction"},
        ],
        "optional_inputs": [{"path": _rel_to_run(_KB_PATH), "reason": kb_reason}],
        "deliverables": ["campaign_review.yaml"],
        "constraints": [
            "Cite runs from the digest by run_id and idea_status; never restate or override "
            "an idea_status.",
            "If recommendation is reframe, next_research_question must be a complete "
            "research_brief (see the note in your inputs).",
            "KB GATE -- answer the three KB questions of the skill (untested cells, exhausted "
            "cells forbidden, combination candidates) in campaign_review.yaml.",
        ],
    }
    path = run_dir / "handoffs" / STAGE_CONFIGS["campaign_review"]["handoff"]
    save_yaml(path, handoff)
    return path


def _retired_review_route(run_dir: Path, run_id: str, terminal: str) -> str:
    """run_loop, after the grid route under the flag: `terminal` unless a
    review is due, then "campaign_review" -- with its digest and handoff
    written and the trigger recorded on pipeline_state.yaml (the marker
    run_loop's campaign_review guards and the context helpers read)."""
    trigger = _retired_review_trigger(run_id)
    if trigger is None:
        return terminal
    trigger["idea_status_terminal"] = terminal
    _write_review_digest(run_dir, trigger)
    _write_retired_review_handoff(run_dir, run_id)
    update_state(path=run_dir, **{CAMPAIGN_REVIEW_TRIGGER_KEY: trigger})
    print(f"\n🔭 CAMPAIGN REVIEW TRIGGERED (verdict routing retired): "
          f"{trigger['runs_since_last_review']} recorded runs since the last completed review "
          f"(cadence {trigger['review_every_n_runs']}).")
    return "campaign_review"


def _retired_review_marked(run_dir: Path) -> bool:
    state_path = Path(run_dir) / "pipeline_state.yaml"
    state = (load_yaml(state_path) or {}) if state_path.exists() else {}
    return bool(state.get(CAMPAIGN_REVIEW_TRIGGER_KEY))


def _apply_retired_routing_review_context(stage_name: str, handoff: dict, run_dir: Path) -> None:
    """campaign_review of a run whose review was triggered under the flag AND
    with the flag still on (review fix 3): add the skill note
    RETIRED_ROUTING.md as a required input. The marker is checked first, so
    every flag-off run (no marker) returns before any flag read and the
    handoff is never mutated: the prompt is byte-identical."""
    if stage_name != "campaign_review" or not _retired_review_marked(run_dir):
        return
    if not _verdict_routing_retired_enabled():
        return
    required = handoff.setdefault("required_inputs", [])
    if any(req.get("path") == _RETIRED_REVIEW_GUIDANCE for req in required):
        return
    required.append({"path": _RETIRED_REVIEW_GUIDANCE,
                     "reason": "E-059 slice 6c S2b: verdict routing is retired -- what each "
                               "recommendation does now, and what to cite. It replaces the "
                               "skill's escalation-era terminate guard."})


def _review_idea_terminal(run_dir: Path, run_id: str) -> str:
    """completed_<idea_status>, re-read from the grid's idea_status.yaml
    (validated by _load_idea_status): a review never changes an idea's status."""
    terminal = f"completed_{_load_idea_status(run_dir, run_id)['idea_status']}"
    if terminal not in RETIRED_ROUTING_TERMINALS:
        raise ValueError(f"campaign review ({run_id}): {terminal!r} is not a retired-routing ending")
    return terminal


def _record_review_component_request(run_id: str, review: dict) -> None:
    """escalate_component (guess 4): the rationale goes where card J says the
    operator looks, campaign_record/component_requests.yaml, as
    {run_id, stage: campaign_review, variant_id: null, reason} -- through the
    shared locked writer. Once per run."""
    _crr.append_component_requests(
        ROOT / _crr.COMPONENT_REQUESTS_REL,
        [{"run_id": run_id, "stage": "campaign_review", "variant_id": None,
          "reason": str(review.get("recommendation_rationale") or "no rationale provided")}],
        unless=lambda r: r.get("run_id") == run_id and r.get("stage") == "campaign_review")


def _source_protocol_pin(run_dir: Path, run_id: str) -> dict:
    """Review fix 1: the reframe's protocol pin, from the source run's own
    pre_registration.yaml machine_constraints (protocol_ref [+ its content
    hash], or a generated protocol spec). None found: raise -- a reframe
    brief with no protocol would not launch."""
    pre_path = run_dir / "artifacts" / "pre_registration.yaml"
    pre = (load_yaml(pre_path) or {}) if pre_path.exists() else {}
    mc = (pre.get("machine_constraints") or {}) if isinstance(pre, dict) else {}
    if mc.get("protocol_ref"):
        return {k: mc[k] for k in ("protocol_ref", "protocol_ref_content_hash") if mc.get(k)}
    if mc.get("protocol"):
        return {"protocol": mc["protocol"]}
    raise ValueError(f"campaign review ({run_id}): {pre_path} has no machine_constraints "
                     f"protocol_ref or protocol -- the reframe brief has no protocol to pin. "
                     f"Refusing to write a brief that could not launch.")


def _write_reframe_brief(run_dir: Path, run_id: str, nrq: dict) -> str:
    """Guess 6 + review fix 1: campaign_record/candidate_briefs/<run_id>__reframe.md,
    a frontmatter brief from next_research_question. A required key it lacks
    is filled from this run's research_brief.yaml (named in the prose); one
    still missing stops the run loudly. The orchestrator adds
    `criteria_from: hypothesis_generation` (criteria fitted to the new idea at
    step 1a, from the menu -- operator decision 2 of 6b) and
    `machine_constraints` = the source run's protocol pin. The review may not
    set criteria, a protocol or a `candidate` block itself (refused).
    Idempotent for the same text; a different text over an existing file
    raises (briefs are never overwritten). Returns the ROOT-relative path."""
    evaluation = nrq.get("evaluation")
    owned = [k for k in ("candidate", "criteria_from", "machine_constraints") if k in nrq]
    if isinstance(evaluation, dict) and "pass_rule" in evaluation:
        owned.append("evaluation.pass_rule")
    if owned:
        raise ValueError(f"campaign review ({run_id}): next_research_question sets {owned} -- the "
                         f"orchestrator writes those (criteria at step 1a, the source run's "
                         f"protocol pin). Refusing to write the brief.")
    brief = dict(nrq)
    src_path = run_dir / "artifacts" / "research_brief.yaml"
    src = (load_yaml(src_path) or {}) if src_path.exists() else {}
    filled = []
    for key in REFRAME_BRIEF_REQUIRED_KEYS:
        if not brief.get(key) and isinstance(src, dict) and src.get(key):
            brief[key] = src[key]
            filled.append(key)
    missing = [k for k in REFRAME_BRIEF_REQUIRED_KEYS if not brief.get(k)]
    if missing:
        raise ValueError(
            f"campaign review ({run_id}): the reframe's next_research_question lacks {missing}, "
            f"and {src_path} does not supply them -- refusing to register an incomplete brief. "
            f"Complete next_research_question in artifacts/campaign_review.yaml and resume.")
    brief["criteria_from"] = PASS_RULE_PENDING_AT_1A
    brief["machine_constraints"] = _source_protocol_pin(run_dir, run_id)
    rel = f"{_decide_next_tools().CANDIDATE_BRIEFS_DIR}/{run_id}__reframe.md"
    text = ("---\n" + yaml.safe_dump(brief, sort_keys=False, allow_unicode=True) + "---\n\n"
            f"# Reframe from campaign review ({run_id})\n\n"
            f"Written by the orchestrator from runs/{run_id}/artifacts/campaign_review.yaml "
            f"(recommendation: reframe; E-059 slice 6c S2b). Registered as a `ready` queue "
            f"entry with origin campaign_review; decide-next picks the next run. Its criteria "
            f"are written at step 1a from config/criterion_menu.yaml (criteria_from); its "
            f"protocol pin is {run_id}'s.\n"
            + (f"\nFilled from runs/{run_id}/artifacts/research_brief.yaml: {', '.join(filled)}.\n"
               if filled else ""))
    path = ROOT / rel
    if path.exists():
        if path.read_text(encoding="utf-8") == text:
            return rel
        raise RuntimeError(f"campaign review ({run_id}): {path} already exists with other "
                           f"content -- briefs are never overwritten. Move it aside and resume.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return rel


def _review_sha(run_dir: Path) -> str:
    return hashlib.sha256((run_dir / "artifacts" / "campaign_review.yaml").read_bytes()).hexdigest()


def _route_retired_campaign_terminate(run_dir: Path, run_id: str, review: dict,
                                      terminal: str) -> str:
    """Guess 5 + review fix 7: terminate really stops. A `terminate` event is
    appended to campaign_decision.yaml's history (runs_attempted and idea
    status counts from the campaign memory; no families_tried or
    altitude_justification); then a pause with its own flag. Nothing in
    campaign_state.yaml is written (its `space_empty` has no reader).
    `CAMPAIGN_REVIEW_TERMINATE_KEY` records the review's hash: the operator's
    continue-anyway resume of the same review appends an `override_continue`
    event and ends the run at `terminal` (decide-next then runs)."""
    review_sha = _review_sha(run_dir)
    decision_path = ROOT / _crr.DECISION_REL
    state = load_yaml(run_dir / "pipeline_state.yaml") or {}
    if state.get(CAMPAIGN_REVIEW_TERMINATE_KEY) == review_sha:
        _crr.append_decision_event(decision_path, {
            "event": "override_continue", "run_id": run_id, "review_sha256": review_sha,
            "note": "the operator cleared the campaign_review_terminate stop and resumed; "
                    "the campaign continues (decide-next picks the next run)"})
        print(f"⚙️  campaign_review_terminate was already raised for this review; the operator "
              f"resumed -> override recorded in campaign_decision.yaml -> {terminal}.")
        return terminal
    runs = _campaign_memory_module().load_memory(_campaign_memory_path()).get("runs") or {}
    campaign = load_campaign_state() or {}
    _crr.append_decision_event(decision_path, {
        "event": "terminate", "run_id": run_id, "review_sha256": review_sha,
        "campaign_id": campaign.get("campaign_id", "default"),
        "source": "campaign_review (orchestrator.verdict_routing_retired; E-059 slice 6c S2b)",
        "rationale": review.get("primary_failure_mode")
                     or review.get("recommendation_rationale", "no rationale provided"),
        "runs_attempted": sorted(runs),
        "idea_status_counts": _idea_status_counts(runs.values()),
        "instruments_tried": campaign.get("instruments_tried", []),
        "components_built": campaign.get("components_built", []),
    })
    print(f"\n🛑 CAMPAIGN REVIEW: terminate -> the campaign stops here "
          f"({CAMPAIGN_REVIEW_TERMINATE_FLAG}; recorded in campaign_decision.yaml). See "
          f"docs/RUNBOOK.md §3.")
    update_state(path=run_dir, status="paused_for_human",
                 flags={CAMPAIGN_REVIEW_TERMINATE_FLAG: True},
                 **{CAMPAIGN_REVIEW_TERMINATE_KEY: review_sha})
    return "human_pause"


def _complete_retired_review(run_dir: Path, run_id: str, rec: str) -> None:
    """Review fixes 2+4: the one place a review COMPLETES -- it covers the
    runs its trigger counted, so only now does the cadence count reset."""
    state = load_yaml(run_dir / "pipeline_state.yaml") or {}
    trigger = state.get(CAMPAIGN_REVIEW_TRIGGER_KEY)
    if not isinstance(trigger, dict) or not isinstance(trigger.get("since_runs"), list):
        raise ValueError(f"campaign review ({run_id}): pipeline_state.yaml carries no "
                         f"{CAMPAIGN_REVIEW_TRIGGER_KEY} with since_runs -- refusing to mark a "
                         f"review complete without knowing which runs it covered.")
    _crr.record_completed_review(_review_log_path(), run_id=run_id,
                                 review_sha256=_review_sha(run_dir),
                                 covered=trigger["since_runs"], recommendation=rec)


def _route_retired_campaign_review(run_dir: Path, run_id: str) -> str:
    """determine_post_campaign_review_route's branch under the flag (called
    first, before that function loads anything). Every recommendation ends in
    completed_<idea_status> except terminate (a pause until the operator
    overrides it) and a reframe refused by the A5.4 KB-reactivation check (a
    pause, as flag-off). A review is recorded as completed only when the route
    ends the run. continue and escalate_* are recorded, not routed, and return
    before any verdict_interpretation.yaml could be read; a continue's
    next_research_question is ignored. Never picks the next run, never
    scaffolds a run, never writes a continuation or a campaign_state field."""
    review = load_yaml(run_dir / "artifacts" / "campaign_review.yaml")
    if not isinstance(review, dict):
        raise ValueError(f"{run_dir / 'artifacts' / 'campaign_review.yaml'} is not a mapping")
    rec = str(review.get("recommendation") or "").strip().lower()
    terminal = _review_idea_terminal(run_dir, run_id)
    if rec in _REVIEW_RECORDED_ONLY:
        print(f"\n🔭 campaign_review: {rec} recorded, not routed (v26 card G) -> {terminal}.")
        if rec == "continue" and review.get("next_research_question"):
            print("   next_research_question on a continue is ignored (only a reframe adds a brief).")
        if rec == "escalate_component":
            _record_review_component_request(run_id, review)
            print("   rationale appended to campaign_record/component_requests.yaml.")
        _complete_retired_review(run_dir, run_id, rec)
        return terminal
    if rec == "reframe":
        nrq = review.get("next_research_question")
        if isinstance(nrq, str):
            nrq = yaml.safe_load(nrq)
        if not isinstance(nrq, dict) or not nrq:
            raise ValueError(f"campaign review ({run_id}): reframe without a next_research_question "
                             f"mapping -- refusing to drop the reframe silently.")
        # A5.4 (F09): the same KB-reactivation gate as flag-off, before any write.
        kb = load_yaml(_KB_PATH) if _KB_PATH.exists() else {}
        violations = _check_kb_reactivation_conformance(nrq, kb or {})
        if violations:
            print("\n🛑 [A5.4] KB-REACTIVATION CONFORMANCE VIOLATION — this reframe targets an "
                  "already-closed KB entry:")
            for v in violations:
                print(f"   - {v}")
            update_state(path=run_dir, status="paused_for_human",
                         flags={"kb_reactivation_violation": True},
                         kb_reactivation_violations=violations)
            return "human_pause"
        rel = _write_reframe_brief(run_dir, run_id, nrq)
        update_state(path=run_dir, **{CAMPAIGN_REVIEW_REFRAME_KEY: rel})
        _complete_retired_review(run_dir, run_id, rec)
        print(f"\n🔄 campaign_review: reframe -> {rel} (registered in the queue at DONE; "
              f"decide-next picks the next run) -> {terminal}.")
        return terminal
    if rec == "terminate":
        out = _route_retired_campaign_terminate(run_dir, run_id, review, terminal)
        if out == terminal:
            _complete_retired_review(run_dir, run_id, rec)
        return out
    raise ValueError(f"Unknown campaign_review recommendation: {rec}")


# ---------------------------------------------------------------------------
# E-059 S2a, operator decision 2 (S1_FINDINGS_6B.md, 2026-09-24): criteria of a
# proposal-sourced candidate are written at step 1a, never inherited from the
# source run. A candidate is recognised by its research_brief.yaml carrying
# `candidate.criteria_from: hypothesis_generation` (permanent, written by
# tools/decide_next.py). run_campaign._materialize_run writes its
# pre_registration.yaml with `pass_rule: null` and
# `pass_rule_pending: hypothesis_generation`; while that marker is set and the
# run sits at hypothesis_generation, run_loop DEFERS the specialist_readers
# pre-flight. EVERY time 1a completes for a candidate,
# _write_pass_rule_from_card rebuilds the pass_rule from the CURRENT card
# (idempotent: a re-run of 1a rewrites it), lints it and runs the pre-flight --
# before 1b, 2 or any backtest. The marker is cleared only once pending_stage
# has advanced past hypothesis_generation (_clear_pass_rule_pending). A brief
# without the candidate block is untouched (byte-identical).
# ---------------------------------------------------------------------------

PASS_RULE_PENDING_KEY = "pass_rule_pending"
PASS_RULE_PENDING_AT_1A = "hypothesis_generation"
# criterion_menu.yaml keys that describe an entry rather than define a criterion.
_MENU_META_KEYS = ("basis", "card_overridable")
_DECIDE_NEXT_GUIDANCE = "../../workflow_artifacts/skills/hypothesis-design/DECIDE_NEXT_CANDIDATES.md"


def _decide_next_candidate(run_dir: Path) -> dict | None:
    """research_brief.yaml's `candidate` block when it is a decide-next
    candidate (criteria written at 1a), else None."""
    path = Path(run_dir) / "artifacts" / "research_brief.yaml"
    if not path.exists():
        return None
    brief = load_yaml(path) or {}
    cand = brief.get("candidate") if isinstance(brief, dict) else None
    if isinstance(cand, dict) and cand.get("criteria_from") == PASS_RULE_PENDING_AT_1A:
        return cand
    return None


def _brief_criteria_from_1a(run_dir: Path) -> bool:
    """Slice 6c S2b review fix 1: research_brief.yaml's BRIEF-LEVEL
    `criteria_from: hypothesis_generation` (a campaign-review reframe brief):
    the idea's criteria are written at step 1a, like a decide-next candidate's,
    but with no candidate block. No such key on any other brief."""
    path = Path(run_dir) / "artifacts" / "research_brief.yaml"
    if not path.exists():
        return False
    brief = load_yaml(path) or {}
    return isinstance(brief, dict) and brief.get("criteria_from") == PASS_RULE_PENDING_AT_1A


def _pass_rule_pending_at_1a(run_dir: Path) -> bool:
    """True when this run's pre_registration.yaml still carries the pending
    marker (set at materialization, cleared once the run is past 1a)."""
    path = Path(run_dir) / "artifacts" / "pre_registration.yaml"
    if not path.exists():
        return False
    doc = load_yaml(path) or {}
    return isinstance(doc, dict) and doc.get(PASS_RULE_PENDING_KEY) == PASS_RULE_PENDING_AT_1A


def _specialist_readers_preflight_deferred(run_dir: Path, pending_stage: str) -> bool:
    """The start-of-run_loop pre-flight is deferred only while the run has not
    yet passed step 1a AND its pass_rule is pending at 1a. A run past 1a that
    still carries the marker is not deferred: the check then runs, loudly."""
    return pending_stage == PASS_RULE_PENDING_AT_1A and _pass_rule_pending_at_1a(run_dir)


def _clear_pass_rule_pending(run_dir: Path, pending_stage: str) -> bool:
    """Drop the pending marker once pending_stage has advanced past
    hypothesis_generation. No-op (no write) when the marker is absent."""
    if pending_stage == PASS_RULE_PENDING_AT_1A or not _pass_rule_pending_at_1a(run_dir):
        return False
    path = Path(run_dir) / "artifacts" / "pre_registration.yaml"
    doc = load_yaml(path) or {}
    doc.pop(PASS_RULE_PENDING_KEY, None)
    save_yaml(path, doc)
    return True


def _pass_rule_from_card(card: dict, menu: dict, where: str) -> dict:
    """{criteria: [...]} from a card's id-only criteria, resolved with the
    grid's own merge (verdict_criteria_evaluator.resolve_criteria_against_menu).
    A card item may carry only `id` plus the fields its menu entry lists under
    `card_overridable`; anything else (a stray key, an override of metric /
    comparator / threshold / null_handling the menu does not allow, a
    threshold override on a scale_free: false entry, or a floor override that
    lowers/drops the menu's sample floor -- verdict_criteria_evaluator.
    menu_criterion_overrides_violations, C5.1) raises."""
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import verdict_criteria_evaluator as _vce
    raw = card.get("criteria")
    if not isinstance(raw, list) or not raw:
        raise ValueError(
            f"{where} has no `criteria` list, but this run is a decide-next candidate "
            f"(research_brief.yaml candidate.criteria_from: {PASS_RULE_PENDING_AT_1A}) -- step 1a "
            f"must write the idea's criteria from config/criterion_menu.yaml. Refusing before 1b.")
    menu_by_id = {e["id"]: e for e in ((menu or {}).get("criteria") or [])
                  if isinstance(e, dict) and e.get("id")}
    for i, c in enumerate(raw):
        cid = c.get("id") if isinstance(c, dict) else None
        if cid not in menu_by_id:
            raise ValueError(f"{where}: criteria[{i}] id={cid!r} is not a live entry of "
                             f"config/criterion_menu.yaml ({sorted(menu_by_id)}) -- 1a picks from the "
                             f"menu only.")
        violations = _vce.menu_criterion_overrides_violations(c, menu_by_id[cid])
        if violations:
            raise ValueError(f"{where}: criteria[{i}] ({cid}) " + "; ".join(violations)
                             + ". Refusing before 1b.")
    resolved = _vce.resolve_criteria_against_menu(raw, menu)
    for crit in resolved:
        for key in _MENU_META_KEYS:
            crit.pop(key, None)
    return {"criteria": resolved}


def _write_pass_rule_from_card(run_dir: Path, run_id: str, sr_flag: bool) -> bool:
    """After EVERY completion of hypothesis_generation (1a) for a decide-next
    candidate: rebuild pre_registration.yaml's pass_rule from the CURRENT
    hypothesis_card.yaml (_pass_rule_from_card), re-check the card's
    hypothesis_id against candidate.source.hypothesis_id, run the registration
    lint that applies to this shape (K3 protocol selection / window_set_ref),
    write it, then run the specialist_readers pre-flight when that flag is on.
    The pending marker is left in place (cleared once the run advances).
    Returns False (a no-op) for any other run. Raises before any spend."""
    run_dir = Path(run_dir)
    cand = _decide_next_candidate(run_dir)
    # Slice 6c S2b review fix 1: a campaign-review reframe brief carries
    # criteria_from at brief level (no candidate block, no source id to match).
    if cand is None and not _brief_criteria_from_1a(run_dir):
        return False
    arts = run_dir / "artifacts"
    card_path = arts / "hypothesis_card.yaml"
    card = (load_yaml(card_path) if card_path.exists() else {}) or {}
    expected_hid = (((cand.get("source") or {}) if isinstance(cand.get("source"), dict)
                     else {}).get("hypothesis_id") if cand is not None else None)
    if cand is not None and (not expected_hid or card.get("hypothesis_id") != expected_hid):
        raise ValueError(
            f"{card_path}: hypothesis_id={card.get('hypothesis_id')!r} is not the candidate's "
            f"{expected_hid!r} (research_brief.yaml candidate.source.hypothesis_id; operator "
            f"decision 1: a reader patch is a NEW idea with that id). Refusing before 1b.")
    menu_path = ROOT / "config" / "criterion_menu.yaml"
    menu = (load_yaml(menu_path) if menu_path.exists() else {}) or {}
    pass_rule = _pass_rule_from_card(card, menu, str(card_path))
    # E-060 S2 (guess 6): code, not 1a, adds residual_ic for a forecast-block idea.
    if _composition_runs_enabled() and not _residual_ic_exempt_reason(run_dir):
        pass_rule = _with_residual_ic_criterion(pass_rule, menu)
    pre_reg_path = arts / "pre_registration.yaml"
    if not pre_reg_path.exists():
        raise FileNotFoundError(f"{pre_reg_path} is missing for a decide-next candidate -- it is "
                                f"written at materialization (run_campaign._materialize_run).")
    pre_reg = load_yaml(pre_reg_path) or {}
    violations = _lint_machine_constraints_protocol_selection(
        pre_reg.get("machine_constraints") or {}, pass_rule)
    if violations:
        raise ValueError(f"{run_id}: the pass_rule built from 1a's criteria failed the K3 "
                         f"protocol-selection lint:\n" + "\n".join(f"  - {v}" for v in violations))
    pre_reg["pass_rule"] = pass_rule
    pre_reg["pass_rule_source_ref"] = f"runs/{run_id}/artifacts/hypothesis_card.yaml#criteria"
    save_yaml(pre_reg_path, pre_reg)
    print(f"✅ [E-059] pre_registration.yaml pass_rule written from 1a's criteria "
          f"{[c['id'] for c in pass_rule['criteria']]} (not inherited from any source run)")
    if sr_flag:
        _check_specialist_readers_preflight(run_dir)
    return True


def _apply_decide_next_context(stage_name: str, handoff: dict, run_dir: Path) -> None:
    """hypothesis_generation of a decide-next candidate, under
    orchestrator.decide_next.enabled only: add the addendum
    workflow_artifacts/skills/hypothesis-design/DECIDE_NEXT_CANDIDATES.md as a
    required input (the exception to IMPROVEMENT 08's four-field rule). Flag
    off, another stage, or a brief that is not a candidate: no-op -- the
    handoff is never mutated, so the 1a prompt is byte-identical."""
    if stage_name != "hypothesis_generation" or not _decide_next_enabled():
        return
    if _decide_next_candidate(run_dir) is None:
        return
    required = handoff.setdefault("required_inputs", [])
    if any(req.get("path") == _DECIDE_NEXT_GUIDANCE for req in required):
        return
    required.append({"path": _DECIDE_NEXT_GUIDANCE,
                     "reason": "E-059 S2a: this brief is a decide-next candidate -- author its "
                               "card and criteria per this addendum (an exception to "
                               "IMPROVEMENT 08)."})


def _canonical_json_sha256(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


def _check_pass_through_config_hash(artifacts: Path) -> None:
    """E-059 S2a, the 5a pass-through check (S1_FINDINGS_6B.md §3.3). A
    decide_next patch candidate's research_brief.yaml carries
    candidate.source.expected_config_sha256 and expected_manifest_sha256: the
    canonical-JSON hashes (the _compute_forecast_hash rule) of the config
    decide_next resolved and of the source block manifest. 1b copies both
    through by prompt; this checks the copies -- backtest_spec.yaml's config,
    once written variants/base/strategy_config.json, and block_manifest.yaml --
    and stops loudly on any difference, before any backtest. No expected hash
    (every brief not written by decide_next, and new_block candidates): no-op."""
    brief_path = Path(artifacts) / "research_brief.yaml"
    if not brief_path.exists():
        return
    brief = load_yaml(brief_path) or {}
    source = ((brief.get("candidate") or {}) if isinstance(brief, dict) else {}).get("source") or {}
    if not isinstance(source, dict):
        return
    expected_cfg = source.get("expected_config_sha256")
    expected_man = source.get("expected_manifest_sha256")
    if not expected_cfg and not expected_man:
        return
    bad = {}
    if expected_cfg:
        spec = load_yaml(Path(artifacts) / "backtest_spec.yaml") or {}
        got = {"backtest_spec.yaml config": _canonical_json_sha256(spec.get("config"))}
        base_cfg = Path(artifacts) / "variants" / "base" / "strategy_config.json"
        if base_cfg.exists():
            got["variants/base/strategy_config.json"] = _compute_forecast_hash(base_cfg)
        bad.update({k: v for k, v in got.items() if v != expected_cfg})
    if expected_man:
        man_path = Path(artifacts) / "block_manifest.yaml"
        man = load_yaml(man_path) if man_path.exists() else None
        got_man = _canonical_json_sha256(man) if man is not None else None
        if got_man != expected_man:
            bad["block_manifest.yaml"] = got_man
    if bad:
        raise RuntimeError(
            f"run_tool_worker(backtest_specification): pass-through mismatch -- decide_next "
            f"expected config sha256 {expected_cfg} and manifest sha256 {expected_man} "
            f"(research_brief.yaml candidate.source) but got {bad}. Stage 1b did not copy the "
            f"candidate's config/manifest through verbatim; refusing before any backtest.")


# ---------------------------------------------------------------------------
# E-059 S2b -- briefs (card M) and brief exhaustion, under
# orchestrator.decide_next.enabled only (S1_FINDINGS_6B.md §4.3, §6 and the
# operator decision of 2026-09-24: 4, 7, 9).
#
# run_campaign.process_once writes artifacts/brief_hypotheses_context.yaml when
# it launches a brief run under the flag (an operator brief or an R2 request --
# never a decide-next reader candidate). Its presence is what makes step 1a
# get the BRIEF_HYPOTHESES.md addendum, which lets 1a:
#   * write several cards (hypothesis_card_<n>.yaml) plus
#     artifacts/extra_card_scores.yaml -- the three anchored 0-3 scores
#     (rubric brief-card-v1) per card, used ONLY to rank the extra cards;
#   * or write no card and artifacts/brief_status.yaml
#     {brief_status: exhausted, reason} -> terminal completed_brief_exhausted.
# Under the flag the multi-card split scaffolds no sibling run and writes no
# campaign_state.hypothesis_splits row: cards 2..k are copied to
# campaign_record/queued_cards/<run_id>/ and listed with their scores in
# artifacts/queued_hypotheses.yaml, which process_once enqueues through
# register_hypothesis (status queued, origin brief, card_ref). Flag off: every
# function below is a no-op and the 1a prompt is byte-identical.
# ---------------------------------------------------------------------------

BRIEF_CONTEXT_FILE = "brief_hypotheses_context.yaml"
EXTRA_CARD_SCORES_FILE = "extra_card_scores.yaml"
BRIEF_STATUS_FILE = "brief_status.yaml"
BRIEF_EXHAUSTED_STAGE = "completed_brief_exhausted"
# Code-review fix 1: every card 1a wrote repeats one this brief already produced.
NO_NEW_HYPOTHESIS_STAGE = "completed_no_new_hypothesis"
_BRIEF_HYPOTHESES_GUIDANCE = "../../workflow_artifacts/skills/hypothesis-design/BRIEF_HYPOTHESES.md"


def _decide_next_tools():
    """tools/decide_next.py, imported lazily (tools/ is on sys.path: module top)."""
    import decide_next as _dn
    return _dn


def _brief_run_context(run_dir: Path) -> dict | None:
    """artifacts/brief_hypotheses_context.yaml of a brief run under
    orchestrator.decide_next.enabled, else None. The file is checked FIRST, so
    a flag-off run (which never has it) reads no config."""
    path = Path(run_dir) / "artifacts" / BRIEF_CONTEXT_FILE
    if not path.exists() or not _decide_next_enabled():
        return None
    doc = load_yaml(path)
    return doc if isinstance(doc, dict) else {}


def _already_produced(ctx: dict) -> set:
    return {h for h in (ctx.get("already_produced") or []) if isinstance(h, str)}


def _apply_brief_hypotheses_context(stage_name: str, handoff: dict, run_dir: Path) -> None:
    """hypothesis_generation of a brief run under orchestrator.decide_next.enabled:
    add the BRIEF_HYPOTHESES.md addendum and artifacts/brief_hypotheses_context.yaml
    (the hypothesis ids already produced from this brief) as required inputs.
    Flag off, another stage, no context file, or a decide-next reader candidate:
    no-op -- the handoff is never mutated, so the 1a prompt is byte-identical."""
    if stage_name != "hypothesis_generation":
        return
    if _brief_run_context(run_dir) is None or _decide_next_candidate(run_dir) is not None:
        return
    required = handoff.setdefault("required_inputs", [])
    existing = {req.get("path") for req in required}
    for path, reason in (
            (_BRIEF_HYPOTHESES_GUIDANCE,
             "E-059 S2b: this run authors hypotheses from a brief -- extra cards are scored "
             "for ranking, and an exhausted brief is reported per this addendum."),
            (f"artifacts/{BRIEF_CONTEXT_FILE}",
             "E-059 S2b: the hypotheses already produced from this brief -- do not repeat them.")):
        if path not in existing:
            required.append({"path": path, "reason": reason})


def _queue_extra_hypothesis_cards(run_id: str, run_dir: Path, cards: list) -> bool:
    """The flag-on branch of the multi-card split (S1 §6, decisions 4 and 9).
    Every check runs BEFORE anything is copied or written (code-review fix 2):
    an exhausted signal next to the cards (contradiction), a decide-next
    reader candidate (its brief is ONE proposed idea), a legacy brief (no
    brief context: no addendum, so no scores -- fix 9), a card with no
    hypothesis_id, a score item naming no card file (fix 8), a missing or
    malformed score or a rubric other than brief-card-v1 (fix 5), or cards of
    an earlier attempt already enqueued. All raise: the run fails before 1b.

    Code-review fix 1: a card repeating a hypothesis this brief already
    produced (or another card of this output) is REJECTED -- recorded, never
    kept or queued. The first new card becomes this run's hypothesis_card.yaml;
    the other new ones are copied to campaign_record/queued_cards/<run_id>/ and
    listed with their scores in artifacts/queued_hypotheses.yaml for
    run_campaign.process_once to enqueue. If every card repeats, card 1 is kept
    and _brief_card_is_repeat ends the run completed_no_new_hypothesis.
    No sibling run, no hypothesis_splits row."""
    dn = _decide_next_tools()
    artifacts = Path(run_dir) / "artifacts"
    if (artifacts / BRIEF_STATUS_FILE).exists():
        raise ValueError(f"{artifacts / BRIEF_STATUS_FILE} says the brief is exhausted, but step 1a "
                         f"also wrote {len(cards)} hypothesis cards -- contradictory output, "
                         f"refusing to pick one.")
    if _decide_next_candidate(run_dir) is not None:
        raise ValueError(
            f"{run_id}: step 1a wrote {len(cards)} cards for a decide-next reader candidate, whose "
            f"brief is one proposed idea (hypothesis_id fixed by candidate.source). Refusing to "
            f"queue the extras.")
    ctx = _brief_run_context(run_dir)
    if ctx is None:
        raise ValueError(
            f"{run_id}: step 1a wrote {len(cards)} cards, but this run has no "
            f"artifacts/{BRIEF_CONTEXT_FILE} (a legacy brief, operator decision 7): it never got "
            f"the scoring addendum, so its extra cards cannot be ranked. Register the brief anew "
            f"with the flag on (brief_status: open).")
    queued_path = artifacts / dn.QUEUED_HYPOTHESES_FILE
    prior = load_yaml(queued_path) if queued_path.exists() else None
    if isinstance(prior, dict) and prior.get("enqueued"):
        raise ValueError(
            f"{queued_path} says the extra cards of an earlier 1a attempt are already in the queue; "
            f"refusing to overwrite them. Mark those `<entry>__h<n>` queue entries superseded "
            f"and delete this file by hand before resuming.")
    scores_path = artifacts / EXTRA_CARD_SCORES_FILE
    raw = load_yaml(scores_path) if scores_path.exists() else None
    items = raw.get("cards") if isinstance(raw, dict) else None
    if not isinstance(items, list):
        raise ValueError(
            f"{scores_path} is missing or has no `cards` list, but step 1a wrote {len(cards)} "
            f"hypothesis cards: every extra card needs its anchored scores (rubric "
            f"{dn.BRIEF_CARD_RUBRIC}, BRIEF_HYPOTHESES.md) to be ranked.")
    names = {c.name for c in cards}
    by_card = {}
    for i, item in enumerate(items):
        name = item.get("card") if isinstance(item, dict) else None
        if not isinstance(name, str) or name in by_card:
            raise ValueError(f"{scores_path}: cards[{i}] has a missing or duplicate `card` name")
        if name not in names:
            raise ValueError(f"{scores_path}: cards[{i}] scores {name!r}, which is not one of the "
                             f"cards step 1a wrote ({sorted(names)})")
        by_card[name] = item
    seen = set(_already_produced(ctx))
    new_cards, rejected = [], []
    for card in cards:
        doc = load_yaml(card) or {}
        hid = doc.get("hypothesis_id") if isinstance(doc, dict) else None
        if not isinstance(hid, str) or not hid.strip():
            raise ValueError(f"{card}: no hypothesis_id -- every card must name its idea")
        hid = hid.strip()
        if hid in seen:
            rejected.append({"card": card.name, "hypothesis_id": hid,
                             "reason": "already produced from this brief"})
            continue
        seen.add(hid)
        new_cards.append((card, hid))
    kept = new_cards[0][0] if new_cards else cards[0]
    records = []
    for n, (card, hid) in enumerate(new_cards[1:], start=2):
        if card.name not in by_card:
            raise ValueError(f"{scores_path}: no scores for {card.name}")
        try:
            scores = dn.validate_card_scores(by_card[card.name], f"{scores_path} {card.name}")
        except dn.DecideNextError as exc:
            raise ValueError(str(exc)) from exc
        records.append({"n": n, "source_card": card.name,
                        "card_ref": f"{dn.QUEUED_CARDS_DIR}/{run_id}/{card.name}",
                        "hypothesis_id": hid, **_card_scores_as_item(scores)})
    # Every check passed: now write (the kept card, then the queued copies).
    dest = ROOT / dn.QUEUED_CARDS_DIR / run_id
    shutil.copy(kept, artifacts / "hypothesis_card.yaml")
    if dest.exists():
        shutil.rmtree(dest)  # a re-run of 1a whose cards were never enqueued (checked above)
    if records:
        dest.mkdir(parents=True)
        for card, _ in new_cards[1:]:
            shutil.copy(card, dest / card.name)
    save_yaml(queued_path, {"schema_version": 1, "run_id": run_id, "kept_card": kept.name,
                            "enqueued": False, "cards": records, "rejected": rejected})
    print(f"\n[E-059] hypothesis_generation produced {len(cards)} cards: {run_id} keeps "
          f"{kept.name}; {len(records)} new extra card(s) saved for the queue, {len(rejected)} "
          f"rejected as already produced. No sibling run scaffolded.")
    return True


def _card_scores_as_item(scores: dict) -> dict:
    """decide_next.validate_card_scores' flat dict back to the file shape
    {scores: {...}, model_id, rubric_version}."""
    keys = _decide_next_tools()._rp.SCORE_KEYS
    return {"scores": {k: scores[k] for k in keys},
            "model_id": scores["model_id"], "rubric_version": scores["rubric_version"]}


def _brief_single_card_check(run_dir: Path) -> None:
    """Code-review fix 8. A brief run (flag on, context present) that wrote
    hypothesis_card.yaml must not ALSO leave hypothesis_card_<n>.yaml or
    extra_card_scores.yaml: that output is ambiguous (one card or several?),
    so it raises. No-op otherwise (flag off: nothing read)."""
    if _brief_run_context(run_dir) is None:
        return
    artifacts = Path(run_dir) / "artifacts"
    stray = sorted(p.name for p in artifacts.glob("hypothesis_card_*.yaml"))
    if (artifacts / EXTRA_CARD_SCORES_FILE).exists():
        stray.append(EXTRA_CARD_SCORES_FILE)
    if (artifacts / "hypothesis_card.yaml").exists() and stray:
        raise ValueError(f"{artifacts}: step 1a wrote hypothesis_card.yaml AND {stray} -- "
                         f"ambiguous output (one card or several?), refusing to pick.")


def _brief_card_is_repeat(run_dir: Path) -> bool:
    """Code-review fix 1. True when this brief run's hypothesis_card.yaml
    repeats a hypothesis_id the brief already produced (context
    `already_produced`): the card is rejected, recorded in
    artifacts/brief_repeat.yaml, and run_loop ends the run
    completed_no_new_hypothesis before 1b. False for any other run (flag off:
    nothing read)."""
    ctx = _brief_run_context(run_dir)
    if ctx is None:
        return False
    artifacts = Path(run_dir) / "artifacts"
    card_path = artifacts / "hypothesis_card.yaml"
    card = load_yaml(card_path) if card_path.exists() else None
    hid = card.get("hypothesis_id") if isinstance(card, dict) else None
    if not (isinstance(hid, str) and hid.strip() in _already_produced(ctx)):
        return False
    save_yaml(artifacts / "brief_repeat.yaml", {
        "hypothesis_id": hid.strip(), "reason": "already produced from this brief",
        "run_end": NO_NEW_HYPOTHESIS_STAGE})
    print(f"[E-059] step 1a repeated {hid.strip()!r}, already produced from this brief -- "
          f"card rejected, run ends {NO_NEW_HYPOTHESIS_STAGE} (no spend beyond 1a).")
    return True


def _brief_exhausted_signal(run_dir: Path) -> bool:
    """True when step 1a reported the brief exhausted: artifacts/brief_status.yaml
    {brief_status: exhausted, reason: <text>}, written for a brief run (its
    context file present) under orchestrator.decide_next.enabled, with NO card.
    No file, or the flag off: False, reads nothing else (flag-off byte-identity).
    Raises on a malformed file, a file on a run that is not a brief run, or an
    exhausted signal next to a card (a contradiction, never silently resolved)."""
    artifacts = Path(run_dir) / "artifacts"
    path = artifacts / BRIEF_STATUS_FILE
    if not path.exists() or not _decide_next_enabled():
        return False
    doc = load_yaml(path)
    if not (isinstance(doc, dict) and doc.get("brief_status") == "exhausted"
            and isinstance(doc.get("reason"), str) and doc["reason"].strip()):
        raise ValueError(f"{path} must be {{brief_status: exhausted, reason: <text>}}; got {doc!r}")
    if not (artifacts / BRIEF_CONTEXT_FILE).exists() or _decide_next_candidate(run_dir) is not None:
        raise ValueError(f"{path}: only a brief run (artifacts/{BRIEF_CONTEXT_FILE} present, not a "
                         f"decide-next reader candidate) may report its brief exhausted.")
    if (artifacts / "hypothesis_card.yaml").exists() or list(artifacts.glob("hypothesis_card_*.yaml")):
        raise ValueError(f"{path} says the brief is exhausted, but step 1a also wrote a hypothesis "
                         f"card -- contradictory output, refusing to pick one.")
    return True


def _campaign_memory_path() -> Path:
    """Resolved from ROOT at call time, so the test sandbox's ROOT covers it."""
    return ROOT / "campaign_record" / "campaign_memory.yaml"


def _campaign_memory_module():
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import campaign_memory as _cm
    return _cm


def _verdict_criteria_evaluator_module():
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import verdict_criteria_evaluator as _vce
    return _vce


def _ensure_regroup_record_handoff(run_id: str, run_dir: Path) -> Path:
    """Stage-level handoff, written lazily at stage entry (flag-off runs never
    get this file), like _ensure_specialist_readers_handoff."""
    handoff_path = run_dir / "handoffs" / _REGROUP_RECORD_HANDOFF
    if not handoff_path.exists():
        save_yaml(handoff_path, {
            "handoff_version": 1, "run_id": run_id,
            "from_stage": "specialist_readers", "to_stage": "regroup_record",
            "assigned_engine": "tool",
            "objective": (
                "E-058: record this run in campaign_record/campaign_memory.yaml (one "
                "entry per run_id, replaced on re-run) before the grid's route is taken. "
                "Decides nothing; writes no trial rows."
            ),
            "required_inputs": [
                {"path": "artifacts/protocol_result.yaml", "reason": "component-error check"},
                {"path": "artifacts/idea_status.yaml", "reason": "the grid's idea status"},
                {"path": "artifacts/grid_evaluation.yaml", "reason": "the grid's cells"},
                {"path": "artifacts/hypothesis_card.yaml", "reason": "the idea's hypothesis_id"},
            ],
            "deliverables": [],
        })
    return handoff_path


def _run_regroup_record_stage(run_id: str, run_dir: Path,
                              profit_bars_evaluated: bool = False) -> dict:
    """Stage body. Reached only from run_loop, which already refuses this
    stage when the flag is off (no second flag check here).

    Component errors and idea_status.yaml are computed ONCE here and returned
    ({"entry", "component_errors", "idea"}) so run_loop hands them to
    determine_post_specialist_readers_route instead of recomputing them.

    Component-error run: a minimal fault-only entry (build_fault_entry), which
    parses none of the run's grid / variant / proposal artifacts. If even that
    cannot be recorded, the failure is logged loudly and swallowed: the
    component_execution_error pause that follows must still fire.
    Otherwise: idea_status.yaml validated exactly as the route validates it,
    then the full entry. campaign_state.trial_sharpes is only READ."""
    errors = _protocol_component_errors(run_dir)
    idea = None if errors else _load_idea_status(run_dir, run_id)
    cm = _campaign_memory_module()
    import block_registry as _br  # tools/ sibling, on sys.path via _campaign_memory_module
    import grid_kb_writer as _kbw
    memory_path = _campaign_memory_path()
    if errors:
        entry = None
        step = "the campaign memory (campaign_record/campaign_memory.yaml)"
        try:
            # E-058 S2b review fix 1: the fault-only memory entry is written
            # FIRST; a fault run never registers a block or writes a KB entry.
            fault = cm.build_fault_entry(run_dir, run_id, errors)
            cm.upsert_memory(memory_path, fault)
            entry = fault
            print(f"📒 [E-058] campaign memory: {run_id} recorded as engineering_fault="
                  f"{entry['engineering_fault']} -> {memory_path}")
            # Then: an earlier VALIDATED pass of this same run may have left a
            # block (append-only) or a grid KB entry. Code never removes them;
            # stop loudly so a person decides. The pause below still fires.
            step = "the stale-record check (block_registry.yaml / campaign_knowledge_base.yaml)"
            stale = []
            reg_path = _block_registry_path()
            blocks = _br.blocks_for_run(reg_path, run_id)
            if blocks:
                stale.append(f"{reg_path} still holds block(s) {blocks} registered by an earlier "
                             f"validated pass of {run_id}")
            kb_id = _kbw.entry_id_for_run(_KB_PATH, run_id)
            if kb_id:
                stale.append(f"{_KB_PATH} still holds grid entry {kb_id!r} from an earlier pass "
                             f"of {run_id}")
            if stale:
                raise RuntimeError(
                    "; ".join(stale) + ". This re-run is an engineering fault, so those records "
                    "no longer describe it -- the block registry is append-only and code never "
                    "edits either file: a person decides whether to remove them.")
        except Exception as e:
            print(f"❌ [E-058] regroup_record ({run_id}, component_execution_error): {step} "
                  f"failed -- {type(e).__name__}: {e}. The run still pauses for the component "
                  f"errors; resolve this and resume.")
    else:
        entry = cm.build_memory_entry(
            run_dir, run_id,
            trial_sharpes=(load_campaign_state() or {}).get("trial_sharpes") or [],
            categories=_reader_categories(),
            protocol_root=ROOT,
            # Branch 3 on every backtest: the per-variant profit-bars results
            # (written after protocol_execution) fill `profit_bars`; flag off
            # keeps null + "not evaluated before regroup".
            profit_bars_evaluated=profit_bars_evaluated,
        )
        # E-058 S2b, in this order so a failure leaves nothing half-recorded
        # that a re-run cannot redo: registry (append-only; conflict raises
        # BEFORE the memory entry is replaced), KB entry (replaced on re-run),
        # memory entry (replaced on re-run), then the scoreboard (derived).
        _comp_on = _composition_runs_enabled()
        entry["registry"] = _br.record_run(
            _block_registry_path(), run_dir, entry, root=ROOT, composition_runs=_comp_on,
            # E-060 S3b (guess 11): a composition run never registers a block.
            **({"composition_run": True} if _comp_on and _composition_mode(run_dir) else {}))
        entry["kb_entry_id"] = _kbw.write_kb_entry(
            _KB_PATH, _kbw.build_kb_entry(entry), root=ROOT, recompute_views=_recompute_kb_views)
        cm.upsert_memory(memory_path, entry)
        print(f"📒 [E-058] campaign memory: {run_id} recorded "
              f"(idea_status={entry['idea_status']}) -> {memory_path}")
        _write_near_miss_scoreboard()
    return {"entry": entry, "component_errors": errors, "idea": idea}


def _block_registry_path() -> Path:
    """Resolved from ROOT at call time, so the test sandbox's ROOT covers it."""
    return ROOT / "campaign_record" / "block_registry.yaml"


def _near_miss_scoreboard_dir() -> Path:
    """The scoreboard's tracked home (E-018), resolved from ROOT at call time --
    never near_miss_scoreboard.STRATEGY_RESEARCH_ROOT, which the sandbox does
    not cover (S1_FINDINGS.md §1.4)."""
    return ROOT / "engineering" / "roadmap" / "E-018" / "artifacts"


def _write_near_miss_scoreboard() -> None:
    """E-058 S2b: the scoreboard's documented hook. Idea-generation raw
    material only; nothing on the route reads it (firewall, by review). It
    decides nothing, so it can NEVER fail the stage (review fix 3): any
    error is logged loudly and the stage continues to the route."""
    try:
        import near_miss_scoreboard as _nms  # tools/ sibling
        rows = _nms.build_scoreboard(ROOT / "runs")
        yaml_path, _ = _nms.write_scoreboard(rows, _near_miss_scoreboard_dir())
        print(f"🗒️  [E-058] near-miss scoreboard rebuilt ({len(rows)} run dirs) -> {yaml_path}")
    except Exception as e:
        print(f"❌ [E-058] near-miss scoreboard NOT rebuilt ({type(e).__name__}: {e}). It is a "
              f"firewalled view that decides nothing; the run continues to its route. Rebuild by "
              f"hand with tools/near_miss_scoreboard.py once fixed.")


# E-058 S2b: campaign-review's memory input, added only under the flag. Not in
# the handoff template's required_inputs, because ensure_files would then fail
# every flag-off run, which has no memory file (S1_FINDINGS.md §6).
_REGROUP_RECORD_CONTEXT_STAGES = {"campaign_review"}


def _apply_regroup_record_context(stage_name: str, handoff: dict, run_dir: Path) -> None:
    """Flag OFF (the default): no-op, the handoff dict is never touched, so
    the assembled prompt is byte-identical. Flag on: campaign_review gets
    campaign_record/campaign_memory.yaml as a required input -- only when the
    file exists (review fix 8), so a campaign with no recorded run yet cannot
    fail the stage with FileNotFoundError."""
    if stage_name not in _REGROUP_RECORD_CONTEXT_STAGES:
        return
    if not _regroup_record_enabled():
        return
    # Slice 6c S2b review fix 10: a review started by the verdict_routing_retired
    # trigger reads the code-written digest of the memory instead of the whole
    # file (its handoff names it). Only such runs carry the marker.
    if _retired_review_marked(run_dir):
        return
    path = "../../campaign_record/campaign_memory.yaml"
    if not (Path(run_dir) / path).exists():
        print("ℹ️  [E-058] campaign_review: no campaign_record/campaign_memory.yaml yet -- "
              "not added as an input.")
        return
    required = handoff.setdefault("required_inputs", [])
    if any(req.get("path") == path for req in required):
        return
    required.append({
        "path": path,
        "reason": ("E-058: the per-run campaign memory (orchestrator.regroup_record.enabled) -- "
                   "the complete per-run list under this flag (campaign_state.yaml runs is "
                   "incomplete under it). For every run you discuss, cite its idea_status "
                   "(validated|refuted|inconclusive -- the idea's status comes ONLY from the "
                   "grid; never restate or override it), grid.counts, registry (block_ids or "
                   "skipped reason) and proposals (refs/ids/count only; reader scores decide "
                   "nothing here). An entry with engineering_fault is a broken run, not a "
                   "finding. Runs before the flag are absent; their history is "
                   "campaign_knowledge_base.yaml, where an entry without legacy_schema: false "
                   "is legacy."),
    })


def _apply_config_direct_authoring_context(stage_name: str, handoff: dict, run_dir: Path) -> None:
    """Union the config-direct-authoring flow's file-presence signals into
    required_inputs for the two stages whose SKILL.md prose branches on
    them (hypothesis-design IMPROVEMENT 07/08, innovation-expansion
    IMPROVEMENT 07) -- config/criterion_menu.yaml + config/cost_model.yaml
    for hypothesis_generation, artifacts/backtest_spec.yaml (strategy_config_
    authoring's own output, written before innovation_expansion runs in this
    flow) for innovation_expansion. Required, not optional: unlike the
    exclusion digest (raw material a stage may or may not find), these files
    are the entire point of the flow's own new skill sections when the flag
    is on -- a stage silently proceeding without them would defeat IMPROVEMENT
    07/08 rather than degrade gracefully.

    Flag OFF (the default): no-op -- the handoff dict is never mutated, so
    _build_stage_prompt's assembled prompt is byte-identical to before this
    function existed, same acceptance bar as every other _apply_* helper in
    this module."""
    if stage_name not in _CONFIG_DIRECT_AUTHORING_CONTEXT_STAGES:
        return
    if not _config_direct_authoring_enabled():
        return
    required = handoff.setdefault("required_inputs", [])
    existing_paths = {req["path"] for req in required}

    def _add(path: str, reason: str) -> None:
        if path in existing_paths:
            return
        required.append({"path": path, "reason": reason})
        existing_paths.add(path)

    if stage_name == "hypothesis_generation":
        _add(
            "../../config/criterion_menu.yaml",
            "E-056 Slice 3b IMPROVEMENT 07: pre-register pass/fail criteria here, at 1a, "
            "picked from this menu's live entries only.",
        )
        _add(
            "../../config/cost_model.yaml",
            "E-056 Slice 3b IMPROVEMENT 07: populate cost_feasibility from round_trip_cost_bps "
            "here (relocated from quant-validation, which this flow does not invoke).",
        )
    elif stage_name == "innovation_expansion":
        _add(
            "artifacts/backtest_spec.yaml",
            "E-056 Slice 3b IMPROVEMENT 07: strategy_config_authoring's base config -- "
            "variant_patches.yaml's patches are diffs against this file's 'config' field.",
        )
        # E-061 C1.2: variant_patches.yaml is a deliverable of step 2 in this flow
        # (in memory only -- the run's handoff file is never rewritten with it).
        deliverables = handoff.setdefault("deliverables", [])
        for extra in _config_direct_step2_deliverables(stage_name):
            if extra not in deliverables:
                deliverables.append(extra)


# ---------------------------------------------------------------------------
# E-032 S2c's anti-adjacency retry (orchestrator.anti_adjacency_retry,
# _anti_adjacency_retry_enabled, _route_post_innovation_expansion's gate call and
# _apply_anti_adjacency_retry_context) was RETIRED by E-036 S2a (2026-09-27,
# engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md §1 and its operator decision):
# it fired before backtest_specification had produced any config, so an exact
# repeat was structurally unreachable there -- the flag never had a working
# REPEAT effect and was off. The exact-match check lives at 5a
# (_route_post_variant_selection / _gate_config_direct_variants below).
# ---------------------------------------------------------------------------


# E-034 S2: record which expanded_variants menu entry backtest_specification
# actually chose, and persist the discards. See engineering/roadmap/E-034/
# artifacts/s1_selection_record.md Task 3 for the full design and the
# 2026-08-24 S1-review Log entry in EPIC.md for why this is NOT built as a
# "required" field on backtest_spec.schema.json alone: no schema under
# workflow_artifacts/schemas/ is loaded or validated by any code, anywhere
# (grep-verified) -- a schema-only "required" is decorative. The actual
# guarantee is this code seam: it raises if selected_variant_id is missing
# or does not match anything in the menu, independent of the schema file.
def _derive_variant_id(variant, index: int) -> str:
    """Stable identifier for one expanded_hypothesis_card.yaml
    expanded_variants[] entry. Used identically everywhere a variant needs
    an ID -- this function is the single source of the S1 Task 3 derivation
    rule, reused by both record-writing here and (per S1's note) S3's future
    gate-matching code; do not re-implement it a second time.

    Priority, per S1's measurement of the real 138-variant corpus:
    1. dict with a truthy 'variant_id' key (92% of the 74 dict-shaped
       variants) -- use it verbatim.
    2. dict without 'variant_id' but with 'id'/'name'/'variant_name'/'label'
       (covers the remaining 8%, and any variant shape) -- use the first of
       these present, in that priority order.
    3. bare string (64/138 in the corpus), or a dict with none of the above
       keys (0/74 measured, but handled rather than crashing) -- a short
       deterministic hash of the item's own content, prefixed with its
       positional index so it stays stable across re-reads of the same file
       and distinct even if two bare-string variants share text.
    """
    if isinstance(variant, dict):
        variant_id = variant.get("variant_id")
        if variant_id:
            return str(variant_id)
        for key in ("id", "name", "variant_name", "label"):
            value = variant.get(key)
            if value:
                return str(value)
        content = yaml.safe_dump(variant, sort_keys=True)
    else:
        content = str(variant)
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()[:8]
    return f"str_{index}_{digest}"


def _variant_selection_record_enabled(cfg: dict | None = None) -> bool:
    """False when the key, the section, or the config file is absent -- same
    silence-is-never-a-green-light rule as every other orchestrator.<name>.
    enabled flag in this module (_exclusion_digest_input_enabled,
    _stale_input_path_fix_enabled, _variant_anti_adjacency_gate_enabled). Reads via
    ROOT so the test sandbox (tests/conftest.py's autouse guard) can seed its
    own value without touching the real repository."""
    cfg = _orchestrator_config(cfg)
    return _strict_orchestrator_flag("variant_selection_record", cfg=cfg)  # E-061 C1.5: strict


_INSTRUMENT_SINGLE_ASSET_KEYS = ("asset", "symbol", "instrument", "target_market")


def _coerce_scalar_instrument(value, run_dir: Path):
    """E-034 S3 review fix (2026-08-25, MEASURED not theoretical): hypothesis_
    card.yaml's target_market is declared a string by hypothesis_card.schema.
    json, but the real corpus does not honor that -- of 46 sampled cards, 34
    are plain strings, 10 carry a LIST (['BTCUSDT', 'ETHUSDT']), 2 carry a
    DICT ({'asset': 'BTCUSDT', ...}). All three used to flow straight into
    variant_selection.yaml's 'instrument' field, where (until E-036 S2a
    replaced the family digest with the exact-match key) the gate's
    per-instrument digest lookup silently compared a non-string-non-list
    False against every digest triple -- Layer-2 matching quietly never
    fired for roughly a fifth of the corpus's shape, with no error anywhere. Exactly the class of silent-wrong-answer bug this
    project has spent this whole session finding and refusing to leave in
    place.

    A dict naming a single asset under one of the common keys is a real,
    unambiguous answer -- resolve it to that string. A list of distinct
    string symbols is REAL, LEGITIMATE multi-symbol data (the funding-rate
    mean-reversion family genuinely targets BOTH BTCUSDT and ETHUSDT
    identically) -- returned as-is, list[str], for the caller to check EVERY
    named instrument rather than forcing a false single answer: silently
    picking element 0 would look plausible and be wrong for every candidate
    testing the OTHER symbol in that same list. Only a shape with no
    resolvable single-or-multi string answer (empty list, non-string list
    items, a dict with none of the known keys) fails loud."""
    if value is None or isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in _INSTRUMENT_SINGLE_ASSET_KEYS:
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate:
                return candidate
        raise RuntimeError(
            f"[E-034 S3] {run_dir.name}: hypothesis_card.yaml's target_market "
            f"is a dict with none of {_INSTRUMENT_SINGLE_ASSET_KEYS} as a "
            f"string value ({value!r}) -- cannot resolve an instrument for "
            f"the anti-adjacency gate. Add one of those keys, or teach this "
            f"resolver the shape actually in use."
        )
    if isinstance(value, list) and value and all(isinstance(v, str) and v for v in value):
        return list(value)
    raise RuntimeError(
        f"[E-034 S3] {run_dir.name}: target_market resolved to "
        f"{value!r} -- neither a single instrument string, a resolvable "
        f"single-asset dict, nor a clean list of instrument strings. "
        f"Cannot evaluate the anti-adjacency gate against this shape."
    )


def _record_variant_selection(run_dir: Path) -> None:
    """Deterministic post-processing, invoked right after
    backtest_specification's output has been confirmed spec_ready (same
    stage-output-enrichment lifecycle point _apply_b7_mandatory_inputs and
    friends hook into, except those run BEFORE a stage; this one runs AFTER).

    Flag OFF (default): returns immediately -- no file is read beyond the
    flag check, no artifact is written, run_loop's behavior is byte-identical
    to before this function existed.

    Flag ON: loads backtest_spec.yaml.selected_variant_id (RAISES if absent
    -- this is the actual enforcement the unread schema cannot provide),
    matches it against expanded_hypothesis_card.yaml's expanded_variants menu
    using _derive_variant_id (RAISES if it matches nothing -- a hallucinated
    or malformed ID must halt the run, not produce a silently-broken record),
    then writes artifacts/variant_selection.yaml (the chosen variant, copied
    verbatim, plus resolved instrument/timeframe and the LLM's own rationale
    relocated to a place code can find it) and
    artifacts/variants_not_pursued.yaml (every other menu entry, verbatim,
    none dropped, none duplicated, the selected one excluded).
    """
    if not _variant_selection_record_enabled():
        return

    artifacts = run_dir / "artifacts"
    backtest_spec = load_yaml(artifacts / "backtest_spec.yaml") or {}
    selected_variant_id = backtest_spec.get("selected_variant_id")
    if not selected_variant_id:
        raise RuntimeError(
            f"[E-034 S2] {run_dir.name}: backtest_spec.yaml is missing "
            f"'selected_variant_id'. backtest-engineering/SKILL.md requires "
            f"the stage to name the exact expanded_variants entry it used. "
            f"Refusing to proceed without it -- this is the fail-loud code-"
            f"seam enforcement; the schema field alone is not checked by "
            f"anything (see EPIC.md's 2026-08-24 S1-review entry)."
        )
    selected_variant_id = str(selected_variant_id)

    expanded_card = load_yaml(artifacts / "expanded_hypothesis_card.yaml") or {}
    variants = expanded_card.get("expanded_variants") or []
    derived_ids = [_derive_variant_id(v, i) for i, v in enumerate(variants)]

    matched_index = None
    for idx, vid in enumerate(derived_ids):
        if vid == selected_variant_id:
            matched_index = idx
            break
    if matched_index is None:
        raise RuntimeError(
            f"[E-034 S2] {run_dir.name}: backtest_spec.yaml's "
            f"selected_variant_id={selected_variant_id!r} does not match any "
            f"entry in expanded_hypothesis_card.yaml's expanded_variants "
            f"(derived menu IDs: {derived_ids}). Refusing to write a "
            f"selection record pointing at a hallucinated or malformed ID."
        )

    matched_variant = variants[matched_index]
    hypothesis_card = load_yaml(artifacts / "hypothesis_card.yaml") or {}

    variant_instrument = None
    variant_timeframe = None
    if isinstance(matched_variant, dict):
        variant_instrument = (matched_variant.get("target_market")
                               or matched_variant.get("target_markets")
                               or matched_variant.get("instrument"))
        variant_timeframe = (matched_variant.get("timeframe")
                              or matched_variant.get("timeframe_expanded")
                              or matched_variant.get("timeframe_original"))
    resolved_instrument = _coerce_scalar_instrument(
        variant_instrument if variant_instrument else hypothesis_card.get("target_market"),
        run_dir,
    )
    resolved_timeframe = variant_timeframe if variant_timeframe else hypothesis_card.get("timeframe")

    decision = load_yaml(artifacts / "decision.yaml") if (artifacts / "decision.yaml").exists() else {}
    chosen_rationale = backtest_spec.get("config_rationale") or (decision or {}).get("rationale")

    run_id = run_dir.name
    hypothesis_id = expanded_card.get("base_hypothesis_id") or hypothesis_card.get("hypothesis_id")

    save_yaml(artifacts / "variant_selection.yaml", {
        "run_id": run_id,
        "hypothesis_id": hypothesis_id,
        "selected_variant_id": selected_variant_id,
        "variant_definition": matched_variant,
        "instrument": resolved_instrument,
        "timeframe": resolved_timeframe,
        "chosen_rationale": chosen_rationale,
    })

    not_pursued = []
    for idx, (vid, variant) in enumerate(zip(derived_ids, variants)):
        if idx == matched_index:
            continue
        entry = {
            "variant_id": vid,
            "run_id": run_id,
            "hypothesis_id": hypothesis_id,
            "variant_definition": variant,
        }
        lost_reason = None
        if isinstance(variant, dict):
            lost_reason = variant.get("lost_reason") or variant.get("why_it_lost")
        if lost_reason:
            entry["lost_reason"] = lost_reason
        not_pursued.append(entry)
    save_yaml(artifacts / "variants_not_pursued.yaml", {"variants_not_pursued": not_pursued})


# ---------------------------------------------------------------------------
# E-034 S3 / E-036 S2a -- the 5a exact-match repeat check
# (orchestrator.variant_anti_adjacency_gate.enabled, off by default).
#
# Redesigned by E-036 S2a (delivery_plan_v26.md slice 8.1;
# engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md + operator decision
# 2026-09-27): the gate is the binary exact-match check of tools/novelty.py
# (the key decide_next already binds on), looked up in
# campaign_record/campaign_memory.yaml -- no family digest, no NEIGHBOUR, no
# composition fingerprint. It is the backstop for every queue origin
# (operator, external, queued_card, reader, brief): decide_next checks only the
# candidates it mints, this checks the config a backtest is about to run.
#
# Two call sites, one per 5a flow:
#   * _route_post_variant_selection -- the legacy LLM backtest_specification
#     flow, after candidate_strategy_config.json is written (the file the
#     trial row's forecast_hash is computed from).
#   * _gate_config_direct_variants -- the config-direct tool-stage 5a
#     (orchestrator.config_direct_authoring, which decide_next requires),
#     one check per variant that protocol_execution would run.
# ---------------------------------------------------------------------------

def _variant_anti_adjacency_gate_enabled(cfg: dict | None = None) -> bool:
    """False (no behavior change) when the key, the section, or the config
    file is absent -- same silence-is-never-a-green-light rule as the other
    orchestrator.<name>.enabled flags in this module
    (_exclusion_digest_input_enabled, _stale_input_path_fix_enabled,
    _variant_selection_record_enabled)."""
    cfg = _orchestrator_config(cfg)
    return _strict_orchestrator_flag("variant_anti_adjacency_gate", cfg=cfg)  # E-061 C1.5: strict


_CAMPAIGN_MEMORY_REL = "campaign_record/campaign_memory.yaml"


def _repeat_gate_context(run_dir: Path, run_id: str) -> dict:
    """Everything the exact-match check needs that is the same for every
    variant of one run, from the SAME sources campaign_memory.yaml's entries
    are built from:
      * memory -- campaign_record/campaign_memory.yaml (tools/campaign_memory.
        load_memory). Absent: a fresh campaign's legitimate empty memory when
        orchestrator.regroup_record is on; a misconfiguration (raise) when it
        is off -- nothing would ever write the memory this gate reads, so
        every check would silently ADMIT.
      * protocol_ref -- the protocol this run will execute
        (_resolve_protocol_path, the resolver protocol_execution and the data
        gate use), made relative to ROOT by campaign_memory.protocol_ref_of,
        the rule regroup_record applies to protocol_result.yaml's
        protocol_file.
      * symbols -- that protocol's `symbols` (what tools/run_protocol.py
        iterates; campaign_memory measures them back from its results).
      * specs -- novelty.protocol_specs over the memory (an unreadable memory
        protocol degrades to an unresolved key, listed in
        `protocol_warnings`), plus this run's protocol read STRICTLY (fail
        loud: the candidate's key must never be unresolved).
      * index -- novelty.match_index, built once per run (this run excluded).
      * layer1_advisory -- the KB's advisory verdict, computed once per run
        (it depends only on the run's hypothesis_id and the protocol's
        timeframe)."""
    import anti_adjacency_gate as _aag  # tools/ sibling (tools/ is on sys.path)
    import campaign_memory as _cm_mod
    import novelty as _nov
    memory_path = ROOT / _CAMPAIGN_MEMORY_REL
    memory_present = memory_path.exists()
    if not memory_present and not _regroup_record_enabled():
        raise RuntimeError(
            f"[E-036 S2a] {run_dir.name}: orchestrator.variant_anti_adjacency_gate.enabled is "
            f"true but {_CAMPAIGN_MEMORY_REL} does not exist and "
            f"orchestrator.regroup_record.enabled is off -- nothing writes the memory this "
            f"gate reads, so every variant would silently ADMIT. Turn on regroup_record "
            f"(and its prerequisites) first.")
    memory = _cm_mod.load_memory(memory_path)
    protocol_path = _resolve_protocol_path(run_dir, run_id)
    protocol_ref = _cm_mod.protocol_ref_of(str(protocol_path), ROOT)
    proto = _nov.load_protocol(ROOT, protocol_ref)  # strict: raises NoveltyError
    symbols = proto.get("symbols")
    if not (isinstance(symbols, list) and symbols and all(isinstance(s, str) and s for s in symbols)):
        raise RuntimeError(
            f"[E-036 S2a] {run_dir.name}: protocol {protocol_ref} has no usable `symbols` list "
            f"({symbols!r}) -- cannot build the exact-match key.")
    card_path = run_dir / "artifacts" / "hypothesis_card.yaml"
    card = (load_yaml(card_path) or {}) if card_path.exists() else {}
    card = card if isinstance(card, dict) else {}
    kb_path = ROOT / "campaign_record" / "campaign_knowledge_base.yaml"
    kb = (load_yaml(kb_path) or {}) if kb_path.exists() else None
    warnings: list = []
    specs = _nov.protocol_specs(ROOT, memory, warnings=warnings)
    cand_spec = _nov.protocol_spec(ROOT, protocol_ref, strict=True)
    specs[_nov.normalize_ref(protocol_ref)] = cand_spec
    return {
        "aag": _aag,
        "memory_present": memory_present,
        "protocol_ref": protocol_ref,
        "protocol_warnings": warnings,
        "symbols": sorted(set(symbols)),
        "specs": specs,
        "index": _nov.match_index(memory, specs, exclude_run_id=run_id),
        "hypothesis_id": card.get("hypothesis_id"),
        "card_timeframe": card.get("timeframe"),
        "layer1_advisory": _aag.layer1_advisory(card.get("hypothesis_id"), cand_spec["timeframe"],
                                                kb, ROOT / "runs"),
    }


def _check_variant_repeat(ctx: dict, config_path: Path, run_id: str) -> dict:
    """One variant's gate result (a plain dict): the key from the config file
    the backtest will run, hashed by _compute_forecast_hash -- the function
    its trial row's forecast_hash comes from -- and the shared context."""
    import campaign_memory as _cm_mod  # tools/ sibling: the path-relativising rule
    import novelty as _nov  # tools/ sibling: the recorded key shape (key_dict)
    aag = ctx["aag"]
    forecast_hash = _compute_forecast_hash(Path(config_path))
    key = aag.candidate_key(forecast_hash, ctx["symbols"], ctx["protocol_ref"], ctx["specs"],
                            card_timeframe=ctx["card_timeframe"])
    result = aag.layer2_digest_check(key, ctx["index"])
    result["layer1_advisory"] = ctx["layer1_advisory"]
    return {**dict(result),
            "key": _nov.key_dict(key),
            "config_ref": _cm_mod.protocol_ref_of(str(config_path), ROOT)}


def _route_post_variant_selection(run_dir: Path, run_id: str) -> str | None:
    """E-034 S3, redesigned by E-036 S2a. The legacy (LLM
    backtest_specification) flow's 5a exact-match check, called by run_loop
    right AFTER artifacts/candidate_strategy_config.json is written (the file
    protocol_execution runs and hashes into the trial row) and before
    validate_config.py.

    Flag OFF (default): returns None immediately -- nothing is read, no
    artifact or state field is written; run_loop is byte-identical.

    Flag ON: requires orchestrator.variant_selection_record.enabled (fail
    loud, unchanged from E-034 S3: the result records variant_selection.yaml's
    selected_variant_id). Checks candidate_strategy_config.json's key against
    campaign_memory.yaml (_repeat_gate_context, _check_variant_repeat) and
    writes artifacts/variant_anti_adjacency_result.yaml.
      - NOVEL -> None (run_loop's next_stage untouched).
      - REPEAT -> status=paused_for_human,
        flags.variant_anti_adjacency_gate_refused=True, returns 'human_pause'
        (E-034 S3's escalate-on-first-refusal policy, unchanged: two LLM
        stages are already spent; a person picks another variant).
    Layer 1 (KB) is recorded as `layer1_advisory` and never pauses."""
    if not _variant_anti_adjacency_gate_enabled():
        return None

    if not _variant_selection_record_enabled():
        raise RuntimeError(
            "[E-034 S3] orchestrator.variant_anti_adjacency_gate.enabled is "
            "true but orchestrator.variant_selection_record.enabled is "
            "false. This gate reads artifacts/variant_selection.yaml, which "
            "only _record_variant_selection() (gated by that other flag) "
            "ever writes -- enabling this gate without its producer is a "
            "misconfiguration, not a legitimate 'nothing to gate yet' "
            "state. Turn on orchestrator.variant_selection_record.enabled "
            "first."
        )

    artifacts = run_dir / "artifacts"
    selection_path = artifacts / "variant_selection.yaml"
    if not selection_path.exists():
        raise RuntimeError(
            f"[E-034 S3] {run_dir.name}: variant_anti_adjacency_gate is "
            f"enabled but {selection_path} does not exist. This function "
            f"must only be called right after _record_variant_selection() "
            f"has succeeded -- a caller-ordering bug, not a degenerate-"
            f"input case to route around."
        )
    config_path = artifacts / "candidate_strategy_config.json"
    if not config_path.exists():
        raise RuntimeError(
            f"[E-036 S2a] {run_dir.name}: variant_anti_adjacency_gate is enabled but "
            f"{config_path} does not exist -- this function must only be called right "
            f"after run_loop writes it (a caller-ordering bug).")
    selection = load_yaml(selection_path) or {}

    ctx = _repeat_gate_context(run_dir, run_id)
    result = _check_variant_repeat(ctx, config_path, run_id)
    save_yaml(artifacts / "variant_anti_adjacency_result.yaml", {
        **result,
        "selected_variant_id": selection.get("selected_variant_id"),
        "hypothesis_id": selection.get("hypothesis_id") or ctx["hypothesis_id"],
        "protocol_ref": ctx["protocol_ref"],
        "memory_present": ctx["memory_present"],
        "protocol_warnings": ctx["protocol_warnings"],
    })

    if result["route"] == "admit":
        print(f"✅ [E-036 S2a] exact-match gate ADMIT for {run_id}: {result.get('reasons')}")
        return None

    reason_text = "; ".join(result.get("reasons", []))
    update_state(
        path=run_dir,
        status="paused_for_human",
        flags={"variant_anti_adjacency_gate_refused": True},
        variant_anti_adjacency_gate={
            "route": "refuse", "layer": result.get("layer"), "reason": reason_text,
        },
    )
    print(f"\n⏸️  PIPELINE PAUSED: the exact-match gate REFUSEd {run_id}'s chosen "
          f"variant as a REPEAT: {reason_text}. Escalating (no auto-retry: validation "
          f"and backtest_specification are already spent) -- see "
          f"artifacts/variant_anti_adjacency_result.yaml and variants_not_pursued.yaml.")
    return "human_pause"


def _gate_config_direct_variants(run_dir: Path, run_id: str) -> str | None:
    """E-036 S2a: the config-direct tool-stage 5a exact-match check, called
    at the top of _route_post_config_direct_backtest_specification, after
    run_tool_worker has written artifacts/variants/index.yaml.

    Flag OFF (default): returns None immediately -- nothing is read or
    written; the route is byte-identical. A composition run (E-060
    _composition_mode) is never gated either: a composite is not a new idea
    (S3b design, the same reason its step 2 has no novelty gate).

    Flag ON: checks every variant protocol_execution would run -- every
    `validated` one under orchestrator.variant_loop, else `base` only --
    against campaign_memory.yaml, each keyed on the file whose hash its trial
    row would carry (variant loop: its config_path; otherwise
    candidate_strategy_config.json, which protocol_execution runs).
      * A REPEAT variant is skipped: marked `not_tested` in index.yaml with
        reason "repeat: ..." naming the matching memory run:variant (the same
        skip the per-variant data gate uses). protocol_execution runs only
        `validated` variants, so a skipped repeat gets no trial row and no
        grid column; campaign memory records it as not_tested with that
        reason. The others proceed. A repeat skip is never a data or
        engineering problem (_is_repeat_skip): the variant loop's ">= 3
        remaining" check counts only non-repeat variants (so when repeats
        alone shrink the set, every remaining non-repeat variant proceeds)
        and _variant_park_kind ignores repeat skips.
      * EVERY checked variant a repeat: returns completed_no_new_hypothesis
        (NO_NEW_HYPOTHESIS_STAGE) -- the existing non-verdict terminal
        ending for "this run has nothing new to test" (registered in
        verdict_criteria_evaluator._NON_VERDICT_OUTCOMES), reused rather than
        a new state. No backtest, no trial row, no grid.
      * Nothing checked (no validated variant): None -- the route's own
        existing handling applies.
    The per-variant results go to artifacts/variant_anti_adjacency_result.yaml.
    Layer 1 (KB) is recorded per variant as `layer1_advisory`, never a skip."""
    if not _variant_anti_adjacency_gate_enabled():
        return None
    if _composition_mode(run_dir):
        return None
    artifacts = run_dir / "artifacts"
    index_path = artifacts / "variants" / "index.yaml"
    index_doc = load_yaml(index_path) or {}
    variants = index_doc.get("variants") or {}
    loop_on = _variant_loop_enabled()
    checked = sorted(vid for vid, v in variants.items()
                     if isinstance(v, dict) and v.get("status") == "validated"
                     and (loop_on or vid == "base"))
    if not checked:
        return None

    ctx = _repeat_gate_context(run_dir, run_id)
    results, repeats = {}, []
    for vid in checked:
        info = variants[vid]
        if loop_on:
            if not info.get("config_path"):
                raise RuntimeError(f"[E-036 S2a] {run_id}: variant {vid!r} is validated in "
                                   f"{index_path} but has no config_path -- refusing to guess.")
            config_path = run_dir / info["config_path"]
        else:
            config_path = artifacts / "candidate_strategy_config.json"
        res = _check_variant_repeat(ctx, config_path, run_id)
        results[vid] = res
        if res["route"] == "refuse":
            refs = [f"{m['run_id']}:{m['variant_id']}" for m in res["matched"]]
            variants[vid] = {**info, "status": "not_tested",
                             "reason": (f"{_REPEAT_REASON_PREFIX} exact match of tested "
                                        f"variant(s) {refs} in {_CAMPAIGN_MEMORY_REL}")}
            repeats.append(vid)
            print(f"⏭️  [E-036 S2a] variant '{vid}' is an exact REPEAT of {refs} -- skipped "
                  f"(not_tested, no backtest, no trial row).")
    all_repeat = len(repeats) == len(checked)
    save_yaml(artifacts / "variant_anti_adjacency_result.yaml", {
        "run_id": run_id,
        "flow": "config_direct",
        "protocol_ref": ctx["protocol_ref"],
        "memory_present": ctx["memory_present"],
        "protocol_warnings": ctx["protocol_warnings"],
        "checked": checked,
        "repeats": repeats,
        "run_end": NO_NEW_HYPOTHESIS_STAGE if all_repeat else None,
        "variants": results,
    })
    if repeats:
        save_yaml(index_path, {**index_doc, "variants": variants})
    if all_repeat:
        print(f"\n🔁 [E-036 S2a] every variant {run_id} would test is an exact repeat of a "
              f"tested one -- run ends {NO_NEW_HYPOTHESIS_STAGE} (no backtest, no trial row).")
        return NO_NEW_HYPOTHESIS_STAGE
    return None


async def async_invoke_agent(stage_name: str, run_id: str, retry_context: str | None = None):
    tool_stages = {"protocol_execution", "data_availability_gate"}
    # E-056 Slice 3b: backtest_specification joins the tool stages ONLY when
    # config-direct authoring is on -- flag off, it still routes through the
    # engine=="claude" LLM path below exactly as before this slice existed.
    if _config_direct_authoring_enabled():
        tool_stages = tool_stages | {"backtest_specification"}
    if stage_name in tool_stages:
        await run_tool_worker(stage_name, run_id)
        return

    RUN_DIR = ROOT / "runs" / run_id
    HANDOFFS = RUN_DIR / "handoffs"
    config = STAGE_CONFIGS[stage_name]
    handoff_path = HANDOFFS / config["handoff"]
    # E-061 C1.2 review fix 8: under config-direct, verdict_interpreter's own handoff.
    handoff_path = (_config_direct_handoff_path(stage_name, run_id, RUN_DIR, rebuild=False)
                    or handoff_path)

    # 1. Load the live handoff file
    handoff = load_yaml(handoff_path)

    # B7: deterministic mandatory-inputs union (see helper docstring above).
    _apply_b7_mandatory_inputs(stage_name, handoff, RUN_DIR)

    # CUL-336: closed-book stages get the files their skills tell them to read (see helper docstring above).
    _apply_closed_book_inputs(stage_name, handoff, RUN_DIR)

    # E-032 S2a: exclusion-digest union, off by default (see helper docstring above).
    _apply_exclusion_digest_input(stage_name, handoff, RUN_DIR)

    # E-032 S2b: repoint known-stale optional_input paths, off by default (see helper docstring above).
    _apply_stale_input_path_fix(stage_name, handoff)

    # E-056 Slice 3b: criterion-menu/cost-model/base-config file-presence signals, off by default (see helper docstring above).
    _apply_config_direct_authoring_context(stage_name, handoff, RUN_DIR)

    # E-059 S2a: the decide-next candidate addendum, off by default (see helper docstring above).
    _apply_decide_next_context(stage_name, handoff, RUN_DIR)

    # E-059 S2b: the brief-hypotheses addendum, off by default (see helper docstring above).
    _apply_brief_hypotheses_context(stage_name, handoff, RUN_DIR)

    # E-058 S2b: campaign-review's memory input, off by default (see helper docstring above).
    _apply_regroup_record_context(stage_name, handoff, RUN_DIR)

    # E-059 slice 6c S2b: campaign-review's retired-routing note, only for a review
    # the flag's trigger started (see helper docstring above).
    _apply_retired_routing_review_context(stage_name, handoff, RUN_DIR)

    # E-056 1b block manifest: stale-manifest removal + manifest-retry context,
    # strategy_config_authoring under config_direct_authoring only (see helper docstrings).
    _clear_stale_block_manifest(stage_name, RUN_DIR)
    _apply_block_manifest_retry_context(stage_name, handoff, RUN_DIR)

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

def determine_post_validation_route(path: Path):
    """Once validation is complete, read the decision from validation_decision artifact and route accordingly:
    - If "approve": proceed to Phase 2 development of backtest
    - If "refine": read the SAME call's refinement_notes.yaml and route per
      determine_post_refinement_route (unless max refinements reached, then reject)
    - If "reject": mark as completed and rejected

    E-039 S4 (2026-09-12): "refinement_planner" retired as a separate stage --
    a "refine" verdict used to hand off to it as a second LLM call; now the
    validation call itself produces refinement_notes.yaml in the same
    response (an additive, conditional deliverable), and this function reads
    it directly instead of a later stage doing so.
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

        # A8.6 (a-priori power pre-flight) removed 2026-09-11, E-039: the
        # epic's whole premise is "always backtest" -- a hypothesis is no
        # longer killed on an estimated activation rate before a real
        # backtest ever runs. Replaced by E-054's data-availability gate
        # (a real structural/data check, not a statistical-power guess) and
        # CUL-264's post-backtest route (a REAL measured go/no-go once the
        # backtest has actually produced numbers). This is a DECLARED
        # behavior change, not bit-identity-preserving: hypotheses that
        # would previously have been blocked here now proceed to
        # backtest_specification unconditionally.
        return "backtest_specification"
    
    elif status == "refine":
        if refinements_used >= max_refinements:
            print(f"🛑 Refinement limit reached ({max_refinements}). Rejecting hypothesis.")
            return "completed_rejected"
        # Increment the refinement counter (previously done by the dispatch
        # loop's own "refinement_planner" branch, now folded in here since
        # that stage no longer exists separately).
        update_state(path=path, counters={"refinements_used": refinements_used + 1})
        return determine_post_refinement_route(path)
    
    elif status == "reject":
        return "completed_rejected"
    
    else:
        raise ValueError(f"Unknown validation status: {status}")

def _create_remaining_handoffs(run_id: str, run_dir: Path):
    """Write data_availability_gate, protocol_execution, and
    verdict_interpreter handoffs."""
    handoffs = run_dir / "handoffs"
    dag_path = handoffs / "backtest_spec_to_data_availability_gate.yaml"
    pe_path = handoffs / "backtest_spec_to_protocol_execution.yaml"
    vi_path = handoffs / "protocol_to_verdict_interpreter.yaml"

    # E-054 Layer 2: data_availability_gate handoff. Written unconditionally
    # (harmless when _data_availability_gate_enabled() is False — nothing
    # ever routes to this stage in that case) so toggling the flag either
    # way needs no separate backfill step for runs already past
    # backtest_specification.
    if not dag_path.exists():
        save_yaml(dag_path, {
            "handoff_version": 1, "run_id": run_id,
            "from_stage": "backtest_specification", "to_stage": "data_availability_gate",
            "assigned_engine": "tool",
            "objective": (
                "E-054 Layer 2: check whether the data this variant needs (price for "
                "every declared symbol, every declared aux feed) can actually be "
                "assembled for the resolved protocol's windows, before spending a "
                "full walk-forward run on it. Outcome: validate / refine / decline."
            ),
            "required_inputs": [
                {"path": "artifacts/candidate_strategy_config.json",
                 "reason": "declared symbols and aux_feeds to check"},
            ],
            "deliverables": ["data_availability_gate.yaml"],
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

    # legacy routing (v26 card G) -- retired in slice 6c. Still written under
    # orchestrator.specialist_readers.enabled (inert: that flag makes
    # verdict_interpreter unreached, and its deliverables list is bookkeeping
    # only), exactly like the data_availability_gate handoff above when that
    # gate is off.
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
                # CUL-336: was ../../campaign_state.yaml, which never resolved
                # after the E-002 move under campaign_record/.
                {"path": _rel_to_run(CAMPAIGN_STATE_PATH),
                 "reason": "cross-run altitude history; drives circuit-breaker altitude decisions"},
                {"path": "../../engineering/roadmap/E-018/artifacts/near_miss_scoreboard.yaml",
                 "reason": "E-018 (2026-09-13): ranked table of past near-miss root causes -- "
                           "informs root_cause/proposed_brief/findings_carryover only, never "
                           "hypothesis_verdict/lineage_routing (see verdict-interpreter/SKILL.md's "
                           "Near-miss scoreboard section). Given unconditionally, with no guard "
                           "tied to whether THIS run has a registered pass_rule -- optional only "
                           "in the ordinary missing-file sense every other optional_input here has "
                           "(e.g. the file not yet regenerated), same as campaign_state.yaml above."},
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


# ---------------------------------------------------------------------------
# E-061 C1.2 (review A1): the handoff contract under config-direct authoring.
# The legacy handoffs of 5a and protocol_execution (templates copied by
# setup_run) require artifacts/validation_protocol.yaml, which only the
# validation stage writes -- and config-direct never reaches that stage; the
# data-gate handoff was written only by _create_remaining_handoffs, on the
# legacy 5a branch. So under orchestrator.config_direct_authoring.enabled
# these three stages load their OWN handoff, written by code at stage entry
# (like the specialist_readers / regroup_record handoffs), naming the inputs
# the config-direct tool branches of run_tool_worker actually read and the
# files they always write. Flag off: never consulted, never written -- the
# legacy handoffs are loaded exactly as before.
# Review fix 8: verdict_interpreter too (reached under config-direct only with
# specialist_readers off, outside the target flag set): its legacy handoff
# requires validation_protocol.yaml as well.
# ---------------------------------------------------------------------------
_CONFIG_DIRECT_HANDOFFS = {
    "backtest_specification": "config_direct_backtest_specification.yaml",
    "data_availability_gate": "config_direct_data_availability_gate.yaml",
    "protocol_execution": "config_direct_protocol_execution.yaml",
    "verdict_interpreter": "config_direct_verdict_interpreter.yaml",
}
_VARIANT_INDEX_REL = "variants/index.yaml"
_VALIDATION_PROTOCOL_REL = "artifacts/validation_protocol.yaml"
_HANDOFF_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "workflow_artifacts" / \
    "templates" / "handoffs"
# Review round 3 (fixes 4/5): a stage's config-direct outputs are cleared at the
# start of each attempt -- moved under RUN_DIR/.previous_attempts/ -- and must
# exist after it, so a previous attempt's file can never satisfy the check. No
# clock involved.
_PREVIOUS_ATTEMPTS_DIR = ".previous_attempts"


def _config_direct_handoff_doc(stage_name: str, run_id: str, variant_loop: bool) -> dict:
    """The config-direct handoff of one of _CONFIG_DIRECT_HANDOFFS' stages. The
    outputs a stage must produce in THIS attempt (incl. the per-variant gate
    files) are cleared at its entry and checked after it
    (_clear_config_direct_attempt_outputs / _check_config_direct_attempt_outputs)."""
    if stage_name == "verdict_interpreter":
        # The legacy template, minus the validation protocol nothing writes.
        doc = load_yaml(_HANDOFF_TEMPLATES_DIR / STAGE_CONFIGS[stage_name]["handoff"]) or {}
        doc["run_id"] = run_id
        doc["required_inputs"] = [x for x in doc.get("required_inputs") or []
                                  if x.get("path") != _VALIDATION_PROTOCOL_REL]
        doc["config_direct_authoring"] = True
        return doc
    index_input = {"path": f"artifacts/{_VARIANT_INDEX_REL}",
                   "reason": "the variants 5a validated; this stage runs once per validated variant"}
    candidate_input = {"path": "artifacts/candidate_strategy_config.json",
                       "reason": "the base variant's config (written by 5a; no variant loop)"}
    doc = {"handoff_version": 1, "run_id": run_id, "assigned_engine": "tool",
           "config_direct_authoring": True}
    if stage_name == "backtest_specification":
        doc.update({
            "from_stage": "innovation_expansion", "to_stage": "backtest_specification",
            "objective": (
                "E-056 config-direct authoring (tool, no LLM): apply each variant's patch in "
                "artifacts/variant_patches.yaml to the base config in artifacts/backtest_spec.yaml, "
                "validate every variant (validate_config.py) and write "
                "artifacts/variants/<variant_id>/strategy_config.json plus "
                "artifacts/variants/index.yaml."),
            "required_inputs": [
                {"path": "artifacts/backtest_spec.yaml",
                 "reason": "strategy_config_authoring's base config (status spec_ready)"},
                {"path": "artifacts/variant_patches.yaml",
                 "reason": "innovation_expansion's variants: patches against the base config"},
            ],
            "deliverables": [_VARIANT_INDEX_REL],
        })
    elif stage_name == "data_availability_gate":
        doc.update({
            "from_stage": "backtest_specification", "to_stage": "data_availability_gate",
            "objective": (
                "E-054 Layer 2 under config-direct authoring: check that the data each "
                "validated variant needs can be assembled for the resolved protocol's windows, "
                "before any backtest. Outcome per variant: validate / refine / decline."),
        })
        if variant_loop:
            doc.update({
                "required_inputs": [index_input],
                "deliverables": [_VARIANT_INDEX_REL],
                "per_variant_outputs": ["variants/<variant_id>/data_availability_gate.yaml"],
            })
        else:
            doc.update({"required_inputs": [candidate_input],
                        "deliverables": ["data_availability_gate.yaml"]})
    elif stage_name == "protocol_execution":
        doc.update({
            "from_stage": "backtest_specification", "to_stage": "protocol_execution",
            "objective": (
                "Run the full walk-forward protocol against each validated variant's config. "
                "Config-direct authoring writes no validation_protocol.yaml: run_protocol.py "
                "runs with --diagnostics-only (the diagnostics block, no rule set)."),
            "required_inputs": [index_input if variant_loop else candidate_input],
            "deliverables": ["protocol_result.yaml"],
        })
        if variant_loop:
            doc["per_variant_outputs"] = ["variants/<variant_id>/protocol_result.yaml"]
    else:
        raise ValueError(f"no config-direct handoff for stage {stage_name!r}")
    return doc


def _config_direct_handoff_path(stage_name: str, run_id: str, run_dir: Path, *,
                                rebuild: bool) -> Path | None:
    """The ONE place deciding whether `stage_name` loads a config-direct handoff:
    None when it does not (flag off, or a stage with no config-direct handoff),
    else its path, the file ensured. `rebuild=True` (run_loop, at every stage
    entry) rewrites it from the current flags, so a flag change or a park/unpark
    never loads a stale shape (review fix 6); `rebuild=False` (async_invoke_agent,
    after run_loop injected its context) only creates it when missing. Flag-off
    runs never get these files."""
    if stage_name not in _CONFIG_DIRECT_HANDOFFS or not _config_direct_authoring_enabled():
        return None
    handoff_path = run_dir / "handoffs" / _CONFIG_DIRECT_HANDOFFS[stage_name]
    if rebuild or not handoff_path.exists():
        save_yaml(handoff_path,
                  _config_direct_handoff_doc(stage_name, run_id, _variant_loop_enabled()))
    return handoff_path


def _config_direct_step2_deliverables(stage_name: str) -> list:
    """E-061 C1.2: under config-direct authoring step 2 (innovation_expansion)
    must also write variant_patches.yaml -- 5a reads nothing else. Returned for
    run_loop's in-memory deliverable check and added (in memory) to the prompt's
    handoff by _apply_config_direct_authoring_context; never persisted into the
    run's handoff file (review fix 7), so a flag-off resume never requires it.
    Flag off / any other stage: []."""
    if stage_name != "innovation_expansion" or not _config_direct_authoring_enabled():
        return []
    return ["variant_patches.yaml"]


def _config_direct_attempt_outputs(stage_name: str, run_dir: Path) -> list:
    """The files (relative to artifacts/) a config-direct stage must write in each
    attempt: step 2 variant_patches.yaml; 5a variants/index.yaml; the variant-loop
    data gate every variants/<vid>/data_availability_gate.yaml (its index is an
    INPUT, rewritten in place, so it is not cleared). Flag off / other stages: []."""
    if stage_name not in ("innovation_expansion", "backtest_specification",
                          "data_availability_gate"):
        return []
    if not _config_direct_authoring_enabled():
        return []
    arts = run_dir / "artifacts"
    if stage_name == "innovation_expansion":
        return ["variant_patches.yaml"]
    if stage_name == "backtest_specification":
        return [_VARIANT_INDEX_REL]
    if not _variant_loop_enabled():
        return []
    return sorted(p.relative_to(arts).as_posix()
                  for p in (arts / "variants").glob("*/data_availability_gate.yaml"))


def _clear_config_direct_attempt_outputs(stage_name: str, run_dir: Path, attempt: int) -> None:
    """Move this stage's previous outputs (_config_direct_attempt_outputs) to
    RUN_DIR/.previous_attempts/<stage>_attempt_<n>/, before the attempt runs, so
    only what THIS attempt writes can satisfy _check_config_direct_attempt_outputs.
    Kept, not deleted: a previous LLM-written variant_patches.yaml is evidence."""
    arts = run_dir / "artifacts"
    dest_root = run_dir / _PREVIOUS_ATTEMPTS_DIR / f"{stage_name}_attempt_{attempt}"
    for rel in _config_direct_attempt_outputs(stage_name, run_dir):
        src = arts / rel
        if src.exists():
            dest = dest_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                dest.unlink()
            shutil.move(str(src), str(dest))


def _check_config_direct_attempt_outputs(stage_name: str, run_dir: Path) -> None:
    """After the attempt: step 2 / 5a -- their output exists (it was cleared at
    entry, so this attempt wrote it); the variant-loop gate -- the gate file of
    every variant still validated after the gate (one whose gate crashed is
    marked not_tested by the loop and is not required; a gate that wrote nothing
    fails). Raises RuntimeError naming each missing file. Flag off: no-op."""
    if stage_name not in ("innovation_expansion", "backtest_specification",
                          "data_availability_gate"):
        return
    if not _config_direct_authoring_enabled():
        return
    arts = run_dir / "artifacts"
    if stage_name == "innovation_expansion":
        required = ["variant_patches.yaml"]
    elif stage_name == "backtest_specification":
        required = [_VARIANT_INDEX_REL]
    elif _variant_loop_enabled():
        index = (load_yaml(arts / _VARIANT_INDEX_REL)
                 if (arts / _VARIANT_INDEX_REL).exists() else None) or {}
        required = [f"variants/{vid}/data_availability_gate.yaml"
                    for vid, v in sorted((index.get("variants") or {}).items())
                    if isinstance(v, dict) and v.get("status") == "validated"]
    else:
        return
    missing = [str(arts / rel) for rel in required if not (arts / rel).exists()]
    if missing:
        raise RuntimeError(f"{stage_name} (config-direct): this attempt did not write "
                           f"{missing}")


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


def _inject_post_backtest_route_into_handoff(handoff_path: Path, protocol_result: dict | None,
                                              run_id: str):
    """
    E-039 step 3 / CUL-264 (2026-09-11): surface the real, measured
    post-backtest go/no-go route as CONTEXT for verdict_interpreter --
    NEVER a gate on whether it runs. Jeremy's explicit decision (CUL-264,
    2026-09-11): every backtest still gets an LLM pass; a mechanical
    kill/refine route is informational, exactly like forecast_return_corr
    or cost_drag_pct, never a bypass. Mirrors
    _inject_regime_context_into_handoff's exact pattern (summary field +
    a constraint telling the model how to use it).

    No-ops cleanly when absent: a prescreen-kill run that never reached a
    real backtest has no protocol_result.yaml at all, and post_backtest_route
    only exists once build_core has actually run on real trade/window data
    (CUL-264/272, trading-bot/reporting/run_artifact.py::build_core) --
    prefers the REAL-cost route (post_backtest_route_real, CUL-272) over the
    estimated one when both are present, since real numbers supersede an
    estimate once they exist.
    """
    if not handoff_path.exists() or not protocol_result:
        return

    results = protocol_result.get("results") or []
    routes = []
    for r in results:
        core = r.get("core") or {}
        route = core.get("post_backtest_route_real") or core.get("post_backtest_route")
        if not route:
            continue
        routes.append({
            "window": r.get("window_label") or r.get("label"),
            "symbol": r.get("symbol"),
            "route": route,
            "rationale": (core.get("post_backtest_route_real_rationale")
                          or core.get("post_backtest_route_rationale")),
        })
    if not routes:
        return

    handoff = load_yaml(handoff_path) or {}
    handoff["post_backtest_routes"] = routes

    constraints = handoff.setdefault("constraints", [])
    note = (
        "E-039/CUL-264 POST-BACKTEST ROUTE — INFORMATIONAL ONLY, NEVER A GATE: "
        "post_backtest_routes above is a REAL, measured go/no-go computed from "
        "this run's actual backtest (real trades where available, CUL-272; "
        "otherwise a real correlation/cost estimate, CUL-264) — not a guess "
        "and not the removed A8.6 pre-flight. Treat it as supporting evidence "
        "alongside every other diagnostic, exactly like forecast_return_corr "
        "or cost_drag_pct. Do NOT auto-adopt a kill_*/refine_* label as your "
        "verdict without independently examining the evidence, and do NOT "
        "skip your own analysis because a route says kill or refine. A route "
        "of inconclusive_insufficient_data means the sample was too small to "
        "trust the route's own math — treat it as informationless, not as a "
        "kill signal itself."
    )
    if note not in constraints:
        constraints.append(note)

    save_yaml(handoff_path, handoff)
    print(f"✅ Post-backtest route context injected into verdict_interpreter handoff: "
          f"{[r['route'] for r in routes]}")


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

    CUL-339: parsed by tools/holdout_policy.py, the ONE strict parser. Stricter
    than before on exactly the shapes the old `str(...)` let through: both ends
    must be strict YYYY-MM-DD days (no timestamp, tz offset or other format),
    end >= start, and an unparseable YAML file is a HoldoutBoundaryBreach too
    (it used to escape as yaml.YAMLError).
    """
    p = Path(policy_path) if policy_path else _DATA_POLICY_PATH
    try:
        return _holdout_policy.load_holdout_range(p)
    except _holdout_policy.HoldoutPolicyError as exc:
        raise HoldoutBoundaryBreach(
            f"{exc}. Refusing to generate windows against an unknown seal."
        ) from exc


def _generated_protocol_holdout_block(proto_constraint: dict) -> dict:
    """CUL-339 review fix: the `holdout` block a generated protocol carries --
    always the policy's holdout_range. A pre-registered override
    (machine_constraints.protocol.holdout) is accepted only when it names
    exactly that range (strict days); any disagreement is refused HERE, at
    generation, instead of being written and only refused later by
    `run_protocol.py --holdout`. An explicit null is treated as absent. Shared
    by generation and run_campaign._expected_generated_protocol so both raise
    at the same place."""
    policy_start, policy_end = _load_holdout_range()
    override = proto_constraint.get("holdout")
    if override is not None:
        agrees = (isinstance(override, dict)
                  and set(override) <= {"start", "end"}
                  and _holdout_policy.iso_day(override.get("start")) == policy_start
                  and _holdout_policy.iso_day(override.get("end")) == policy_end)
        if not agrees:
            raise HoldoutBoundaryBreach(
                f"machine_constraints.protocol.holdout {override!r} disagrees with "
                f"campaign_data_policy.yaml holdout_range [{policy_start}, {policy_end}]. "
                f"The holdout range has ONE home (the policy); remove the override.")
    return {"start": policy_start, "end": policy_end}


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


def _ensure_protocol_from_constraints(run_dir: Path, run_id: str, constraints: dict, *,
                                      promotion_retired=False) -> Path | None:
    """
    Idempotent: generates runs/{run_id}'s dedicated protocol JSON + run_context.yaml
    override from machine_constraints.protocol, if present and not already done.
    Returns the generated protocol path, or None if no protocol constraint exists.

    C5.6 `promotion_retired` (see _generated_protocol_promotion): a bool, or a
    zero-argument reader called only when a protocol is actually generated
    (run_loop passes _promotion_retired_enabled, so an already-generated run
    reads no config here). The default False is the flag-off generator,
    exactly as before: no config read, G7 first.
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
    # function whose windows have to be checked against it. CUL-339: an
    # override that disagrees with the policy is refused at generation.
    protocol_obj = {
        "symbols": symbols,
        "timeframe": timeframe,
        "windows": windows,
        "holdout": _generated_protocol_holdout_block(proto_constraint),
        # C5.6 (D-043): G7 unless the promotion block is retired, then no key.
        **_generated_protocol_promotion(
            proto_constraint, run_id,
            promotion_retired=(promotion_retired() if callable(promotion_retired)
                               else promotion_retired)),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(protocol_obj, f, indent=2)
    print(f"✅ [F4d] Generated protocol from pre-registered machine_constraints: {out_path}"
          f" ({len(windows)} windows, {start} -> {end})")

    # run_type MUST be "forced_diagnostic" — protocol_execution's (and the
    # E-054 data-availability gate's) shared protocol-resolution logic only
    # consults run_context's `protocol` key under that exact run_type;
    # otherwise it silently falls back to campaign_state.last_escalation.
    # protocol_path (STALE campaign-wide state
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


def _promotion_retired_enabled(cfg: dict | None = None) -> bool:
    """C5.6 (D-043): True when a protocol's `promotion` block decides nothing --
    orchestrator.config_direct_authoring.enabled AND
    orchestrator.verdict_routing_retired.enabled. Under both, the legacy
    verdict_interpreter route and tools/run_protocol.py's top-level
    promote/kill/refine verdict are retired (the grid and the profit bars
    decide), so G7 is skipped, a generated protocol carries no block and
    run_protocol.py is told not to compute that verdict. config_direct alone
    is NOT enough: with verdict routing still live G7 stays required.

    Not a flag of its own -- the conjunction of two flag readers, each read
    strictly (verdict_routing_retired only when config_direct_authoring is on).
    run_campaign's pre-flight derives the same value from its single parsed
    reading (run_campaign._promotion_retired_from) instead of calling this."""
    return (_flag_dep(_config_direct_authoring_enabled, cfg)
            and _flag_dep(_verdict_routing_retired_enabled, cfg))


def _generated_protocol_promotion(proto_constraint: dict, run_id: str, *,
                                  promotion_retired: bool) -> dict:
    """C5.6 (D-043): the `promotion` entry of a generated protocol, as a dict to
    splice into it. The ONE place both the generator
    (_ensure_protocol_from_constraints) and run_campaign's pre-flight
    (_expected_generated_protocol) decide it, so the two cannot drift.
    Reads no config: `promotion_retired` is the caller's own reading of
    _promotion_retired_enabled (review fixes 5/6).

    promotion_retired False (flag off, or config_direct_authoring with verdict
    routing still live): {"promotion": <block>} through G7
    (_require_pre_registered_promotion), which refuses a brief with none --
    exactly as before, with no I/O before G7.

    promotion_retired True: nothing reads a protocol's promotion block, so the
    generated protocol carries NO `promotion` key -- whatever the brief
    pre-registered is dropped (never copied, never substituted); registration
    already refused an abolished generic or present-but-empty block, and any
    other block is ignored with a logged note."""
    if promotion_retired:
        if "promotion" in proto_constraint:
            print(f"ℹ️  [C5.6] {run_id}: machine_constraints.protocol.promotion is ignored and "
                  f"not copied into the generated protocol -- under config_direct_authoring + "
                  f"verdict_routing_retired nothing reads it (D-043).")
        return {}
    return {"promotion": _require_pre_registered_promotion(proto_constraint, run_id)}



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

    # _path_basename_any_os, not Path(ref).name (CUL-186 follow-up, 2026-09-03):
    # this is the same machine_constraints.protocol_ref field
    # _check_prescreen_conformance was fixed for below -- a Windows-recorded ref
    # ("protocols\baseline_v1.json") mis-parses as one long name on POSIX,
    # ref_path then never exists, and this function raises FileNotFoundError on
    # a protocol that is genuinely present. Missed in the original pass because
    # this call site is in a different function entirely; caught on code review.
    bare_name = _path_basename_any_os(ref)
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
    two previously-duplicated copies inside run_tool_worker's protocol_execution
    branch and the removed signal_prescreen branch (E-039 step 5). Four branch
    classes: replication_diagnostic;
    protocol-GENERATED forced_diagnostic; protocol_ref-PINNED (its own
    distinguishable run_type, A3); and the claim-checked last_escalation fallback
    (B10, §4) -- which now HARD-FAILS instead of silently reusing stale
    campaign-wide state, unless this run is that escalation's own claimed consumer.

    C7-EXT-R (D-3): every exit passes through _assert_promotion_ratified, so an
    unratified generic promotion block is refused wherever the protocol came
    from -- generated, pinned, defaulted or inherited. The audit's point was that
    guarding only the generator left the artifacts and the defaults untouched.

    E-054 Layer 2 (2026-09-11): the decision logic itself now lives in
    tools/protocol_resolution.py::resolve_protocol_path, so the data-availability
    gate can resolve the SAME protocol a run will actually execute against
    without duplicating this 4-branch logic (see that module's docstring for
    why it can't just import this file directly). This function is now a thin
    delegator that supplies the orchestrator's own globals/side-effects
    (ROOT, load_campaign_state(), update_state's flag write) -- behavior is
    unchanged, proven by the existing test_k3_protocol_pinning.py suite.
    """
    from protocol_resolution import (
        resolve_protocol_path as _shared_resolve_protocol_path,
        UngatedProtocolError as _SharedUngatedProtocolError,
    )

    def _on_stale_escalation():
        update_state(path=run_dir, flags={"stale_escalation_unclaimed": True})

    # Log-line fidelity only (never a second copy of the DECISION): re-derive
    # which branch is about to fire purely to pick the right pre-existing
    # print, using the exact same cheap read the shared resolver does anyway.
    _run_ctx_path = run_dir / "artifacts" / "run_context.yaml"
    _run_ctx = (load_yaml(_run_ctx_path) or {}) if _run_ctx_path.exists() else {}
    _run_type = _run_ctx.get("run_type", "")
    if _run_type == "replication_diagnostic":
        print("🔁 replication_diagnostic run — ignoring last_escalation, using baseline_v1.json")
    elif _run_type == "forced_diagnostic" and _run_ctx.get("protocol"):
        print(f"🔬 forced_diagnostic run — using protocol: {_run_ctx['protocol']}")
    elif _run_type == "protocol_ref_pinned" and _run_ctx.get("protocol"):
        print(f"📌 [B3] protocol_ref_pinned run — using pinned protocol: {_run_ctx['protocol']}")

    try:
        result = _shared_resolve_protocol_path(
            run_dir=run_dir,
            run_id=run_id,
            protocols_root=ROOT / "protocols",
            campaign_state=load_campaign_state(),
            on_stale_escalation=_on_stale_escalation,
        )
        if _run_type not in ("replication_diagnostic", "forced_diagnostic", "protocol_ref_pinned"):
            print(f"⚠️  [B10] Using campaign_state.last_escalation.protocol_path "
                  f"({result}) -- this run ({run_id}) is its claimed "
                  f"consumer. Fragile: prefer machine_constraints.protocol_ref on "
                  f"this run's own pre_registration.yaml instead.")
        return result
    except _SharedUngatedProtocolError as e:
        # Re-wrap as THIS module's own UngatedProtocolError so existing
        # `except UngatedProtocolError` call sites (if any are ever added
        # here) and isinstance checks against rpr.UngatedProtocolError keep
        # working -- the shared module deliberately declares its own class
        # rather than importing this file (see its docstring).
        raise UngatedProtocolError(str(e)) from e


def _path_basename_any_os(path_str: str) -> str:
    """E037-11/CUL-186: pathlib.Path(...).name only recognizes the HOST OS's own
    separator -- a Windows-written protocol_version ("protocols\\x.json", the
    real shape run_060 recorded) mis-parses as one long name on POSIX (and a
    POSIX-written "protocols/x.json" would, symmetrically, mis-parse on
    Windows if it ever contained a literal backslash in the filename itself,
    though that direction hasn't been observed). This treats both '/' and '\\'
    as separators regardless of host OS, so the comparison below is stable
    across the dual-writer (Windows + macOS) model. Byte-identical to
    Path(...).name for any already-well-formed same-OS path.
    """
    return str(path_str).replace("\\", "/").rsplit("/", 1)[-1]


def _check_protocol_execution_conformance(protocol_result: dict, constraints: dict, protocol_obj: dict) -> list:
    """
    Compares a completed protocol_execution's ACTUALS against what was
    pre-registered in machine_constraints. Returns a list of violation
    strings (empty = conforms).

    RELOCATED 2026-09-12 (E-039 step 5) from the removed signal_prescreen
    stage's own _check_prescreen_conformance -- the underlying risk this
    guards against does not disappear once prescreen is removed:
    protocol_execution resolves its own protocol via the same
    _resolve_protocol_path() machinery prescreen used, and A4's/Q1's
    REGISTRATION-time guards still cannot catch a runtime override that
    changes AFTER that resolution already happened (a stale run_context.yaml,
    or a hand-edited pre_registration.yaml mid-run -- the real F4d/run_047
    incident this check exists because of). Same mechanism, new source data:
    `protocol_result.get("protocol_file")` (run_protocol.py's own CLI-arg
    record, the direct analog of prescreen_result.yaml's "protocol_version")
    and `protocol_result.get("episode_blocked_significance_by_symbol")`
    (CUL-265, exposed 2026-09-12 specifically so this check has something
    real to read -- previously computed only transiently for the
    prescreen/backtest cross-check, never persisted).
    """
    violations = []

    expected_sig = constraints.get("significance_methodology")
    if expected_sig == "episode_blocked_a851a":
        # Per-symbol now (CUL-265): protocol_execution computes A8.5.1a
        # significance separately per symbol, unlike prescreen's single
        # pooled-across-everything value. A violation on ANY symbol is a
        # real conformance failure -- silently passing because ONE symbol
        # happened to conform would hide the others.
        _tools_path = str(Path(__file__).parent.parent / "tools")
        if _tools_path not in sys.path:
            sys.path.insert(0, _tools_path)
        import episode_significance as _es
        by_symbol = protocol_result.get("episode_blocked_significance_by_symbol") or {}
        if not by_symbol:
            violations.append(
                "pre-registered machine_constraints.significance_methodology="
                "episode_blocked_a851a, but protocol_result carries no "
                "episode_blocked_significance_by_symbol at all -- the A8.5.1a "
                "path was not computed for this run"
            )
        for symbol, actual_sig in by_symbol.items():
            if not _es.is_a851a_method(actual_sig):
                violations.append(
                    f"{symbol}: episode_blocked_significance_method={actual_sig!r} is not "
                    f"an A8.5.1a outcome ({sorted(_es.VALID_METHODS)} or "
                    f"block_<n>_dense_fallback) -- pre-registered "
                    f"machine_constraints.significance_methodology=episode_blocked_a851a "
                    f"was not honored"
                )
    elif expected_sig:
        # No per-run analog exists yet for a non-A8.5.1a named methodology
        # constraint on the backtest side -- flag as unconfirmable rather
        # than silently passing or inventing a comparison.
        violations.append(
            f"pre-registered machine_constraints.significance_methodology="
            f"{expected_sig!r}, but protocol_execution has no equivalent "
            f"recorded field to confirm it against (only episode_blocked_a851a "
            f"is currently checkable here)"
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
    # both REGISTRATION-time checks; neither catches an executed run that
    # silently ran against a DIFFERENT file than the one pinned (e.g. a stale
    # run_context.yaml override, or a hand-edited pre_registration.yaml that
    # changed protocol_ref after protocol_execution already ran once).
    # run_protocol.py's own protocol_result.yaml/protocol_summary.json records
    # the executed protocol's identity under "protocol_file" -- the raw CLI
    # protocol_path argument (an absolute or ROOT-relative path string),
    # confirmed by reading tools/run_protocol.py directly. Compared here by
    # BARE FILENAME (matching A1's own bare-filename convention for
    # run_context.yaml's "protocol" key), never by full path, since the two
    # are constructed differently (CLI arg vs. ROOT-relative ref). Basename
    # extraction goes through _path_basename_any_os, not Path(...).name
    # (E037-11/CUL-186, fixed 2026-09-03): a path recorded on Windows
    # ("protocols\\x.json", the real shape run_060 recorded) mis-parses as
    # one long name on POSIX, producing a spurious violation the first time
    # an artifact crosses machines.
    protocol_ref = constraints.get("protocol_ref")
    if protocol_ref:
        executed_identity = protocol_result.get("protocol_file")
        pinned_name = _path_basename_any_os(protocol_ref)
        if executed_identity:
            executed_name = _path_basename_any_os(executed_identity)
            if executed_name != pinned_name:
                violations.append(
                    f"protocol_execution ran protocol {executed_name!r} != pre-registered "
                    f"machine_constraints.protocol_ref bare filename {pinned_name!r} "
                    f"(protocol_result.protocol_file={executed_identity!r})"
                )

        # Optional, stronger guarantee (§5): if the brief also pinned a content
        # hash, recompute it over the ACTUAL executed protocol_obj (already
        # loaded by this function's own call site) and compare. Duplicates
        # _compute_protocol_content_hash's small formula rather than calling
        # it directly -- that function takes a Path and re-reads the file
        # from disk; protocol_obj here is already the parsed executed
        # content, and this function's authorized write set is
        # _check_protocol_execution_conformance only (K3 rider scope).
        expected_hash = constraints.get("protocol_ref_content_hash")
        if expected_hash and protocol_obj:
            _stripped = {k: v for k, v in protocol_obj.items()
                         if k not in ("protocol_version", "protocol_content_hash")}
            _canonical = json.dumps(_stripped, sort_keys=True)
            actual_hash = "sha256:" + hashlib.sha256(_canonical.encode("utf-8")).hexdigest()
            if actual_hash != expected_hash:
                violations.append(
                    f"protocol_execution's executed protocol content hash {actual_hash!r} != "
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

    # C5.1 (D-013): a menu-referencing criterion (carries `id`, no
    # `metric_basis`) is checked by verdict_criteria_evaluator.
    # lint_menu_shaped_pass_rule instead -- this loop's checks assume the
    # legacy K2/C7 schema (metric_basis mandatory, comparator always
    # present), which several menu reducers (e.g. sign_consistent_by_era)
    # never carry, and would otherwise false-positive on them.
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import verdict_criteria_evaluator as _vce
    # C7/C8: every criterion states its metric, comparator, and metric_basis
    # (bar_level/episode_level -- never fragment_level, per the standing
    # metric-basis rule); a per-symbol (sparse-eligible) criterion also needs
    # a null_handling policy or the only possible runtime outcome is SPEC_ERROR.
    for criterion in criteria:
        if _vce.is_menu_referencing_criterion(criterion):
            continue
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


def _mark_trial_invalidated(trial_id: str, reason: str):
    """F8b-pattern: flag a previously-recorded trial as invalidated_artifact — it
    contacted real data but tested the wrong thing (conformance violation), so it
    must be excluded from promotion/deflate-sharpe accounting like run_044's
    bug-artifact precedent, not silently deleted.

    RESTORED 2026-09-12 (E-039 step 5): briefly deleted during the
    signal_prescreen removal on the mistaken assumption its only caller was
    the (now relocated) prescreen conformance gate -- run_campaign.py's own
    `_apply_trial_accounting` (E-030 S2a quarantine handling) calls this
    directly for `component_execution_error` halts, entirely independent of
    prescreen. Caught by running the real test suite, not by re-reading the
    diff.

    RENAMED param 2026-09-22 (E-033.1 Slice 4a, Decision A): was `run_id`,
    now `trial_id` -- purely a rename, the comparison and every call shape
    is unchanged. Under the compound `f"{run_id}:{variant_id}"` trial_id
    shape (see _record_backtest_trial), a conformance violation on ONE
    variant's protocol run must invalidate ONLY that variant's trial row,
    never the whole run's variant family -- so this function now takes the
    exact trial_id to invalidate rather than deriving one from a bare
    run_id.

    UPDATED 2026-09-22 (Slice 4b): run_loop now has TWO call sites for this
    function -- the flag-off `protocol_execution` elif-branch still passes a
    bare run_id (correct and unaffected: it is not a per-variant loop, so
    run_id IS the trial_id there), and the new `protocol_execution and
    _variant_loop_enabled()` elif-branch passes the compound
    `f"{run_id}:{variant_id}"` per variant, finishing what this docstring
    previously described as still owed to 4b."""
    state = load_campaign_state()
    marked = False
    for t in state.get("trial_sharpes", []):
        if t.get("trial_id") == trial_id and not t.get("invalidated_artifact"):
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

    # E-059 S2b: under orchestrator.decide_next.enabled the extra cards go to the
    # queue (queued, card_ref) instead of sibling runs. Flag off: unchanged below.
    if _decide_next_enabled():
        return _queue_extra_hypothesis_cards(run_id, run_dir, cards)

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


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
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


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
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


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
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


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
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


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
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


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
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
    if _specialist_readers_enabled():
        # E-046a 5b-ii-B (code-review fix 8): under the flag the kill feeds none of
        # the retired machinery (v26 card G, slice 6c) -- no altitude_history row
        # (family-keyed), no failed_families, no continuation_* writes. Only the
        # run list and the diagnostics log are kept; trial accounting is untouched
        # (it lives in protocol_execution, not here). Shared with slice 6c's
        # route (_record_run_in_campaign_state; one diagnostics row per run).
        _record_run_in_campaign_state(run_id, diag)
        return "completed_rejected"
    # legacy routing (v26 card G) -- retired in slice 6c.
    update_campaign_state_after_run(run_id, "hypothesis", "",
                                     interp.get("hypothesis_family", ""), "kill", diag)
    # K4 symmetry: record the (null) continuation explicitly, same site A1's
    # other routing functions use -- this lineage has no child.
    update_state(path=path, continuation_child=None, continuation_created_by="_route_kill")
    return "completed_rejected"


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
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



def _record_backtest_trial(run_id: str, summary: dict, config_path: Path, trial_id: str | None = None):
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

    `trial_id` param added 2026-09-22 (E-033.1 Slice 4a): optional, defaults to
    None -- when omitted (every call site outside the new per-variant loop),
    behavior is byte-identical to before, since the effective trial_id falls
    back to the bare `run_id`. The new per-variant protocol_execution loop
    (run_tool_worker, under orchestrator.variant_loop.enabled) passes
    `trial_id=f"{run_id}:{variant_id}"` explicitly, per Decision A.
    """
    effective_trial_id = trial_id if trial_id is not None else run_id
    state  = load_campaign_state()
    trials = state.setdefault("trial_sharpes", [])

    if any(t.get("trial_id") == effective_trial_id and t.get("source") == "backtest" for t in trials):
        print(f"⏭️  A6.2/H3: backtest trial for {effective_trial_id} already recorded — skipping duplicate.")
        return

    hv    = summary.get("hypothesis_verdict") or {}
    diag  = hv.get("diagnostics") or {}
    pss   = summary.get("per_symbol_summary") or {}

    # Aggregate Sharpe across symbols. NOTE: per_symbol_summary entries never
    # carried a "trade_count" key (run_protocol.py:1316-1321 -- only
    # median_sharpe/max_abs_drawdown_pct/min_trade_count/zero_trade_slot_pct),
    # so n_trades read as 0 on every backtest row (measured live: 34 recorded
    # backtest trials, all n_trades=0). min_trade_count is a per-symbol FLOOR
    # (the minimum across that symbol's windows), not a total, and summing it
    # would still be a large undercount (measured on run_021: 735 vs the true
    # 8701). The real total-trade-count data is the raw per-window "results"
    # list (run_protocol.py:1389), which summary already carries.
    sharpes = [v.get("median_sharpe") for v in pss.values() if v.get("median_sharpe") is not None]
    results_list  = summary.get("results") or []
    n_trades      = sum((r.get("core") or {}).get("trade_count", 0) for r in results_list)
    median_sharpe = round(statistics.median(sharpes), 4) if sharpes else None

    # CUL-15 red-team fix: the SAME {mean, se, t_stat, n} dict shape CUL-193
    # fixed at _write_promotion_audit reaches this sibling call site too, and it
    # was still storing the whole dict in a ledger field every other declaration
    # types `float | None` (deflate_sharpe.py:788, and this function's own
    # docstring above). Nothing reads that field arithmetically TODAY, which is
    # why it never crashed -- but deflate_sharpe.compute_promotion_audit divides
    # by exactly this quantity (`expectancy_bps / expectancy_se`), and handed the
    # dict it raises "unsupported operand type(s) for /: 'dict' and 'float'".
    # The trial ledger is what counts N for the deflated Sharpe, so storing a
    # dict where a number belongs corrupts the accounting record itself. The
    # prescreen-stub path (:4866) still writes a bare None, so both shapes must
    # be handled -- same unwrap as :5330.
    _exp_block   = diag.get("per_trade_expectancy_bps")
    if isinstance(_exp_block, dict):
        expectancy = _exp_block.get("mean")
    else:
        expectancy = _exp_block if isinstance(_exp_block, (int, float)) else None
    below_floor  = diag.get("below_floor_pct", 0.0) or 0.0

    # A6.2 extension: sparse-trading strategies use expectancy, not Sharpe
    if below_floor > 50.0:
        statistic_valid = "expectancy"
    elif median_sharpe is not None:
        statistic_valid = "sharpe"
    else:
        statistic_valid = "neither"

    trial_entry = {
        "trial_id":        effective_trial_id,
        "source":          "backtest",
        "sharpe":          median_sharpe,
        "expectancy_bps":  expectancy,
        "n_trades":        n_trades,
        "statistic_valid": statistic_valid,
        "below_floor_pct": below_floor,
        "forecast_hash":   _compute_forecast_hash(config_path),
    }
    # CUL-233: carry an explicit reproduces_trial back-reference into the ledger
    # row so deduplicate_trials can collapse a re-execution onto its original in
    # the DSR N. Additive: added only when the summary declares it (a byte-
    # identical re-execution of an earlier trial); absent -> key absent -> the row
    # is byte-identical to before. No current pipeline stage sets it -- the field
    # is written today by the H-series driver into run artifacts (see
    # FORK_CHANGES) -- so this is dormant plumbing for the merged-ledger loader.
    reproduces_trial = summary.get("reproduces_trial") or diag.get("reproduces_trial")
    if reproduces_trial is not None:
        trial_entry["reproduces_trial"] = reproduces_trial
    trials.append(trial_entry)
    _save_campaign_state(state)
    print(f"⚙️  A6.2: backtest trial recorded (sharpe={median_sharpe}, "
          f"n_trades={n_trades}, statistic_valid={statistic_valid})")


def _record_failed_backtest_trial(run_id: str, config_path: Path, reason: str, trial_id: str | None = None):
    """
    `trial_id` param added 2026-09-22 (E-033.1 Slice 4a): optional, defaults
    to None -- when omitted (every call site outside the new per-variant
    loop), behavior is byte-identical to before, since the effective
    trial_id falls back to the bare `run_id`. The new per-variant
    protocol_execution loop (run_tool_worker, under
    orchestrator.variant_loop.enabled) passes
    `trial_id=f"{run_id}:{variant_id}"` explicitly, per Decision A -- same
    shape as _record_backtest_trial's own new parameter above.

    H4-core (E-025, 2026-08-16, issue #28): record a data-touching backtest that
    RAISED before _record_backtest_trial could run, so the spent look still moves the
    deflated-Sharpe count. Without this, a backtest that crashed on a non-zero exit
    (protocol_execution :1089) or a missing summary (:1093) left NO trial row at all —
    N silently under-counted a look that had already touched market data. Purely
    additive: appends one distinct-source row, never mutates or drops an existing one.

    source == "backtest_failed" (NOT "backtest"): _record_backtest_trial's
    (trial_id, "backtest") idempotency guard (:3056) and deflate_sharpe's read-side
    check_no_duplicate_trial_ids both key on (trial_id, source). A distinct source keeps
    a later SUCCESSFUL retry's real "backtest" row from being suppressed and does not
    collide with either guard.

    statistic_valid == "failed" lands in deflate_sharpe.load_sharpe_trials's
    "statistic_neither" exclusion bucket (deflate_sharpe.py:212-214, no crash) — so a
    failed row is EXCLUDED from today's DSR N (that exclusion is H1, Jeremy's decision)
    while total_hypotheses_tested / total_variants_tested count it immediately. The
    label conflation with a genuine "neither" is conscious.

    Idempotency guard keyed on (trial_id, source) — the SAME key as _record_backtest_trial's
    success guard (:3056) and deflate_sharpe's read-side check_no_duplicate_trial_ids (:121).
    A second "backtest_failed" row for the same run_id is suppressed regardless of config, so
    this writer can never produce a ledger the read-side check rejects. A run_id is one trial
    slot; a genuine changed-config retry is a NEW run_NNN (different trial_id) and records on
    its own key. A same-run_id re-invoke with an edited config is the artificial manual case —
    recording it once as "this trial's backtest failed" is the correct contract. forecast_hash
    is still carried on the row (provenance + read-time dedup); only the guard key excludes it.

    Conservative by design: recording at the :1089 non-zero-exit site OVER-counts N — a
    non-zero exit includes pre-data failures (config parse, bad args), not only
    data-touching crashes. Over-counting N is the anti-flattering direction (a larger
    trial count only deflates a candidate Sharpe further), so the conservative choice is
    the honest one.
    """
    effective_trial_id = trial_id if trial_id is not None else run_id
    try:
        forecast_hash = _compute_forecast_hash(config_path)
    except Exception:
        # The config may BE what is broken — a hashless row is legal and always kept
        # unique in deflate_sharpe.deduplicate_trials (:88-90). Never mask the original
        # failure by raising out of the hash step.
        forecast_hash = None

    state  = load_campaign_state()
    trials = state.setdefault("trial_sharpes", [])

    if any(t.get("trial_id") == effective_trial_id and t.get("source") == "backtest_failed" for t in trials):
        print(f"⏭️  H4: failed-backtest trial for {effective_trial_id} already recorded — skipping duplicate.")
        return

    trials.append({
        "trial_id":        effective_trial_id,
        "source":          "backtest_failed",
        "sharpe":          None,
        "expectancy_bps":  None,
        "n_trades":        0,
        "statistic_valid": "failed",
        "forecast_hash":   forecast_hash,
        "error":           reason,
    })
    _save_campaign_state(state)
    print(f"⚙️  H4: failed-backtest trial recorded (run={run_id}, reason={reason})")


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
        # E-058 S2b review fix 2: a grid entry (legacy_schema: false, written
        # by tools/grid_kb_writer.py) is one run's record, never a legacy
        # entry to merge into or to close by F09.
        if f.get("legacy_schema") is False:
            continue
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

    E-058 S2b review fix 2: the read-modify-write runs under the same
    campaign_record/.campaign_knowledge_base.lock the grid KB writer takes,
    so the two writers cannot lose each other's entries. The lock file is
    removed on release; the KB bytes written are unchanged.
    """
    if not _KB_PATH.exists():
        print(f"⚠️  A5.1: campaign_knowledge_base.yaml not found — skipping KB update")
        return
    cm = _campaign_memory_module()
    import grid_kb_writer as _kbw  # tools/ sibling, on sys.path via _campaign_memory_module
    with cm._file_lock(_KB_PATH.parent / _kbw.KB_LOCK_FILENAME, "the campaign knowledge base"):
        _write_kb_findings_entry_locked(path, run_id, interp)


def _write_kb_findings_entry_locked(path: Path, run_id: str, interp: dict):
    """_write_kb_findings_entry's body, unchanged, run under the KB lock."""
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


def _verify_verdict_outputs(run_dir: Path, mechanical_lineage_routing: str | None = None) -> list:
    """
    Check that verdict_interpreter produced the right artifacts for its declared status.
    Always reads verdict_interpretation.yaml fresh — never uses caller-modified status,
    EXCEPT for `mechanical_lineage_routing` (E-018, 2026-09-13): when a run's
    pass_rule_evaluation.yaml is binding, the ACTUAL route is that file's
    lineage_routing, not whatever verdict_interpreter itself restated (the two
    can now genuinely disagree -- see _resolve_verdict_fields). Checking the
    artifact's own, possibly-disagreeing field here would verify the WRONG
    shape (e.g. checking for pivot's required files when the real route is
    refine), so callers pass the mechanically-resolved value explicitly in
    that case. None (the default) preserves the original discipline exactly:
    derive from the artifact itself, for every run without a binding pass rule.
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
    status = mechanical_lineage_routing or interp.get("lineage_routing")
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


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
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


def _reproduces_collapses_inline(rec: dict, reproduces_by_key: dict) -> bool:
    """Resolve rec's reproduces_trial chain WITHIN its source (CUL-233).

    True when it terminates at an original present in the input (collapse, counts
    once); False when the chain leaves the input (absent reference -> keep the
    row, never silently dropped). Raises on self-reference or a cycle. A chain
    (A->B->C) resolves transitively and collapses onto the terminal original.
    Independent transcription of deflate_sharpe.py::
    _reproduces_collapses_onto_present_original -- the two lockstep DSR paths must
    agree (test_dedup_predicate_lockstep / test_cul233_reproduces_dedup)."""
    source = rec.get("source")
    origin_id = rec.get("trial_id")
    target_id = rec.get("reproduces_trial")
    if target_id == origin_id:
        raise ValueError(
            f"reproduces_trial self-reference: trial {origin_id!r} names itself "
            f"(CUL-233)."
        )
    seen: set = {(origin_id, source)}
    while True:
        key = (target_id, source)
        if key in seen:
            raise ValueError(
                f"reproduces_trial cycle detected starting at {origin_id!r} "
                f"(revisited {target_id!r}, same source) -- refused (CUL-233)."
            )
        if key not in reproduces_by_key:
            return False
        seen.add(key)
        next_target = reproduces_by_key[key]
        if next_target is None:
            return True
        target_id = next_target


def _dedupe_trials(valid_trials: list) -> tuple[list, int]:
    """Deduplicate campaign trial rows by (forecast_hash, source), honouring
    reproduces_trial (CUL-233). Returns (deduped_trials, n_dedup_removed).

    This is the PIPELINE's own, independent implementation of the same rule as
    deflate_sharpe.py::deduplicate_trials -- deliberately duplicated (the
    mirrored-paths house pattern: two implementations that a lockstep test proves
    agree, so drift is caught rather than hidden by sharing). A run's prescreen
    and backtest rows share a forecast_hash but differ by source, so source is in
    the key; a reproduces_trial row collapses (transitively, within source) onto
    the terminal original present in the input, independent of hash. #57: `is
    None`, NOT truthiness -- a falsy-but-present hash ("" or 0) is a real hash."""
    reproduces_by_key: dict = {}
    for t in valid_trials:
        reproduces_by_key[(t.get("trial_id"), t.get("source"))] = t.get("reproduces_trial")

    seen_keys: set = set()
    deduped_trials = []
    n_dedup_removed = 0
    for t in valid_trials:
        if t.get("reproduces_trial") is not None and _reproduces_collapses_inline(
            t, reproduces_by_key
        ):
            n_dedup_removed += 1
            continue
        fh = t.get("forecast_hash")
        if fh is None:
            deduped_trials.append(t)
            continue
        key = (fh, t.get("source"))
        if key in seen_keys:
            n_dedup_removed += 1
        else:
            seen_keys.add(key)
            deduped_trials.append(t)
    return deduped_trials, n_dedup_removed


def _promotion_dsr_context() -> dict:
    """The campaign-wide trial-ledger statistics and the per-candidate
    Deflated-Sharpe evaluator that _write_promotion_audit applies to each
    candidate protocol_result.

    EXTRACTED VERBATIM 2026-09-24 (branch 3, profit bars on every backtest)
    from _write_promotion_audit's own body so the per-backtest profit-bars
    check (_evaluate_profit_bars_every_backtest) grades each variant's
    Sharpe/DSR with the SAME math and the SAME ledger basis as the promotion
    audit, instead of a second copy that could drift (this module's lockstep
    history: #40/#43, #56, #57). Nothing is written here; the ledger is only
    read. Returns {dsr_candidate, campaign, n_dsr_total, n_trials, excluded,
    total_tested, DSR_THRESHOLD}; dsr_candidate(pr) returns (raw_median_sr,
    is_sparse, passes_deflated, e_max_sr, dsr_result) for ONE
    protocol_result dict, exactly as before the extraction."""
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

    # A6.4: deduplicate by (forecast_hash, source) -- #36 -- honouring
    # reproduces_trial -- CUL-233. This path's own (independent) implementation
    # lives in module-level _dedupe_trials, which deflate_sharpe.py::
    # deduplicate_trials must mirror exactly (the mirrored-paths lockstep, pinned
    # by test_dedup_predicate_lockstep + test_cul233_reproduces_dedup). Extracted
    # to a named function so the lockstep test can execute this real code, not a
    # transcription of it (CUL-233 F3).
    deduped_trials, n_dedup_removed = _dedupe_trials(valid_trials)

    # A6.2: compute over statistic_valid='sharpe' only
    #
    # Bucketing bug fix (2026-08-16, issue #28, adjacent to H1): the previous version
    # special-cased "expectancy" and "neither" and let anything else (including H4's
    # "failed" backtest_failed rows) fall through into "no_sharpe_value" once sharpe
    # was found to be None. deflate_sharpe.py::load_sharpe_trials -- the canonical
    # implementation these two are supposed to mirror exactly -- instead treats
    # "sharpe" as the one recognized value and buckets EVERYTHING else (including
    # "failed") as "statistic_neither". Restructured to match that if/elif/else shape
    # exactly, so any future statistic_valid value lands in the same bucket in both
    # implementations without needing a new special case here. Does not change
    # n_dsr_total, n_trials, or the DSR value -- only which diagnostic bucket a
    # non-sharpe row is reported under in excluded_trial_counts.
    excluded = {"statistic_expectancy": 0, "statistic_neither": 0, "no_sharpe_value": 0,
                "non_finite_sharpe": 0,
                "dedup_removed": n_dedup_removed, "invalidated_artifact": n_invalidated}
    sharpe_values = []
    for t in deduped_trials:
        sv = t.get("statistic_valid")
        if sv == "sharpe":
            s = t.get("sharpe")
            if s is None:
                excluded["no_sharpe_value"] += 1
            elif not math.isfinite(float(s)):
                # CUL-31: a NaN/inf sharpe (contract-legitimate merged row, e.g. a
                # killed-run placeholder) must be excluded with a visible counter --
                # a single non-finite value silently corrupts mu_sr/sigma_sr/dsr
                # (NaN < 1e-10 is False, so the zero-variance guard does not catch it).
                # Lockstep with deflate_sharpe.load_sharpe_trials. Does not shrink
                # n_dsr_total (len(deduped_trials)): N stays honest.
                excluded["non_finite_sharpe"] += 1
            else:
                sharpe_values.append(float(s))
        elif sv == "expectancy":
            excluded["statistic_expectancy"] += 1
        else:
            excluded["statistic_neither"] += 1

    n_trials = len(sharpe_values)
    total_tested = len(valid_trials)  # F8b: excludes invalidated_artifact trials
    # H1 fix (2026-08-16, issue #28): the multiple-testing correction's N -- every real
    # attempt, kills and expectancy-only trials included -- is a different quantity
    # from n_trials (the real-Sharpe-VALUE sample used to estimate mu_sr/sigma_sr).
    # Deliberately len(deduped_trials), matching deflate_sharpe.py's
    # total_hypotheses_tested exactly (post-dedup, post-invalidated-exclusion) -- NOT
    # total_tested (pre-dedup) or len(campaign.runs) (a third, separate basis).
    # COUNT-DIV fix (2026-08-17): this value is now also the one exposed in the
    # output audit dict as "total_hypotheses_tested" -- see below.
    n_dsr_total = len(deduped_trials)
    # Defensive, mirrors deflate_sharpe.py::compute_dsr's same check: n_dsr_total must
    # be >= n_trials by construction (sharpe_values is a filtered subset of
    # deduped_trials), so this should never fire -- but a silent violation would
    # understate the correction, the flattering direction, so fail loud rather than
    # let it pass quietly if the two ever drift apart.
    if n_dsr_total < n_trials:
        raise ValueError(
            f"n_dsr_total={n_dsr_total} is smaller than n_trials (real Sharpe values)="
            f"{n_trials} -- every real Sharpe value is itself a counted attempt, so the "
            f"honest total can never be less than the real-valued sample it's estimated "
            f"from. This indicates deduped_trials and sharpe_values have diverged."
        )

    # --- Deflated Sharpe computation, per candidate protocol_result -------
    # EXTRACTED 2026-09-22 (Slice 4b) from what was previously this
    # function's own inline body, verbatim -- only the candidate's own
    # per_symbol_summary/hypothesis_verdict.diagnostics (pss/hv_diag/
    # raw_median_sr/is_sparse/expectancy_bps/expectancy_se) are now read from
    # a `pr` PARAMETER instead of a single module-level load, so the exact
    # same math can run once per variant (flag-on) or once for the singular
    # bridge file (flag-off) without duplicating the formula. Every shared
    # campaign-wide quantity it closes over (deduped_trials/sharpe_values/
    # n_dsr_total/n_trials/excluded/total_tested/EULER_GAMMA/DSR_THRESHOLD/
    # _phi/_phi_inv) is unchanged and computed exactly once above, regardless
    # of how many candidates are evaluated against it.
    def _dsr_candidate(pr: dict):
        """Returns (raw_median_sr, is_sparse, passes_deflated, e_max_sr,
        dsr_result) for ONE protocol_result dict -- the same 5 quantities
        this function's pre-4b body computed for the singular candidate."""
        pss     = pr.get("per_symbol_summary") or {}
        hv_diag = (pr.get("hypothesis_verdict") or {}).get("diagnostics") or {}

        sharpes_raw   = [v.get("median_sharpe") for v in pss.values() if v.get("median_sharpe") is not None]
        raw_median_sr = round(statistics.median(sharpes_raw), 4) if sharpes_raw else None
        below_floor   = hv_diag.get("below_floor_pct", 0.0) or 0.0
        is_sparse     = below_floor > 50.0
        # CUL-193: per_trade_expectancy_bps is a {mean, se, t_stat, n} dict on the
        # real trade-diagnostics path (run_protocol.py's A3.4 summary, injected into
        # protocol_result.yaml's hypothesis_verdict.diagnostics verbatim) -- the SE
        # this function needs was already being computed and stored upstream; this
        # site was simply reading the whole dict as if it were the bare mean. The
        # stub path (prescreen-kill, :4866) still writes a bare None here, so both
        # shapes must be handled.
        _exp_block = hv_diag.get("per_trade_expectancy_bps")
        if isinstance(_exp_block, dict):
            expectancy_bps = _exp_block.get("mean")
            expectancy_se  = _exp_block.get("se")
        else:
            expectancy_bps = _exp_block if isinstance(_exp_block, (int, float)) else None
            expectancy_se  = None

        dsr_result: dict = {}
        passes_deflated = None
        # promotion_threshold_raw is E_max_SR (raw Sharpe space); None outside the
        # happy path, matching deflate_sharpe.compute_promotion_audit exactly. The
        # Sharpe branch below reassigns this to the computed e_max_sr.
        e_max_sr = None

        if is_sparse:
            # Sparse path: expectancy t-stat. CUL-193: mirrors
            # tools/deflate_sharpe.py::compute_promotion_audit's sparse branch
            # exactly -- same formula, same t > 2.0 practical threshold (not the
            # strict Bonferroni value, which is reported in the note only), same
            # None-not-False indeterminate convention (CUL-163: a candidate whose
            # t-stat cannot be computed was never actually evaluated, so it must
            # not collapse to a terminal FAIL). Lockstep is required by CUL-193's
            # own acceptance criteria -- both implementations must agree on the
            # sparse verdict for the same inputs.
            n_trades = sum(t.get("n_trades", 0) for t in deduped_trials if t.get("statistic_valid") == "expectancy")
            t_stat = None
            if expectancy_bps is not None and expectancy_se is not None and expectancy_se > 0:
                t_stat = expectancy_bps / expectancy_se
            passes_deflated = None if t_stat is None else (t_stat > 2.0)
            _strict_bonferroni_t = (
                f"{_phi_inv(1.0 - 0.05 / max(total_tested, 1)):.2f}" if total_tested >= 1 else "N/A"
            )
            dsr_result = {
                "deflated_sharpe_ratio":   None,
                "expected_max_sharpe":     None,
                "trial_sharpe_variance":   None,
                "correction_method":       "expectancy_t_stat_bonferroni",
                "expectancy_promotion": {
                    "t_stat":          round(t_stat, 4) if t_stat is not None else None,
                    "passes":          passes_deflated,
                    "bonferroni_note": (
                        f"Strict Bonferroni threshold with N={total_tested} trials would be "
                        f"t > {_strict_bonferroni_t}. Using conservative t > 2.0 as practical threshold."
                    ),
                },
            }
        elif n_dsr_total < 2:
            dsr_result = {
                "deflated_sharpe_ratio": None,
                "expected_max_sharpe":   None,
                "trial_sharpe_variance": None,
                "correction_method":     "bailey_lopezdeprado_2014",
                "dsr_error":             f"Insufficient trials: need >= 2, got {n_dsr_total}",
            }
            passes_deflated = False
        elif n_trials < 2:
            # H1: N (n_dsr_total) can be >= 2 while too few of those trials produced a real
            # Sharpe value to estimate the distribution's variance -- a large N does not
            # fix an unmeasurable variance. Distinct error from the n_dsr_total<2 case above.
            dsr_result = {
                "deflated_sharpe_ratio": None,
                "expected_max_sharpe":   None,
                "trial_sharpe_variance": None,
                "correction_method":     "bailey_lopezdeprado_2014",
                "dsr_error":             (
                    f"N={n_dsr_total} trials recorded (multiple-testing count is honest), "
                    f"but only {n_trials} produced a real Sharpe value -- need >= 2 real "
                    f"Sharpe values to estimate the trial distribution's variance. A large "
                    f"N does not fix an unmeasurable variance."
                ),
            }
            passes_deflated = False
        else:
            mu_sr    = statistics.mean(sharpe_values)
            # #56: POPULATION variance (n denominator), matching
            # deflate_sharpe.py's reasoned choice. This site used
            # statistics.stdev -- the SAMPLE form, n-1 denominator, with no
            # rationale attached -- so the two lockstep paths returned different
            # sigma_sr, hence different E_max_SR and different DSR, for identical
            # trial Sharpes. The pipeline always reported the LARGER sigma, by
            # sqrt(n/(n-1)): ~5.4% at n=10, ~1% at n=50.
            # The population form is the intended one: it estimates the SHAPE of
            # the Sharpe-generating process from the values actually observed,
            # independent of how many total attempts N counts.
            # Second drift of this class after correction_method (#40/#43), third
            # counting the dedup predicate (#57).
            var_sr   = sum((v - mu_sr) ** 2 for v in sharpe_values) / len(sharpe_values)
            sigma_sr = math.sqrt(var_sr)

            if sigma_sr < 1e-10:
                dsr_result = {
                    "deflated_sharpe_ratio": None,
                    "expected_max_sharpe":   None,
                    "trial_sharpe_variance": round(var_sr, 6),
                    "correction_method":     "bailey_lopezdeprado_2014",
                    "dsr_error":             "Zero trial Sharpe variance — all trials identical; DSR undefined.",
                }
                passes_deflated = False
            else:
                # H1: N is the honest multiple-testing total (n_dsr_total), NOT n_trials
                # (the real-Sharpe-value sample size) -- mu_sr/sigma_sr above already used
                # n_trials correctly (statistics.mean/stdev sample size), this is only the
                # expected-max-Sharpe benchmark's exponent.
                N = n_dsr_total
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
                    "correction_method":     "bailey_lopezdeprado_2014",
                }

        return raw_median_sr, is_sparse, passes_deflated, e_max_sr, dsr_result
    return {
        "dsr_candidate": _dsr_candidate,
        "campaign":      campaign,
        "n_dsr_total":   n_dsr_total,
        "n_trials":      n_trials,
        "excluded":      excluded,
        "total_tested":  total_tested,
        "DSR_THRESHOLD": DSR_THRESHOLD,
    }


def _write_promotion_audit(run_dir: Path, run_id: str):
    """
    A6.2: Write promotion_audit.yaml before holdout_evaluation.
    Compute Deflated Sharpe over statistic_valid='sharpe' trials from campaign_state.
    For sparse-trading candidates (statistic_valid='expectancy'), record expectancy t-stat.

    RESTRUCTURED 2026-09-22 (E-033.1 Slice 4b, build item 9 / S1_FINDINGS.md §6.5,
    per the operator's 2026-09-22 "Decision" section, Branch 3): under
    orchestrator.variant_loop.enabled, this function now evaluates EVERY
    variant's own protocol_result.yaml (RUN_DIR/artifacts/variants/<variant_id>/
    protocol_result.yaml, written per-variant by Slice 4a's protocol_execution
    loop) independently, instead of the singular bridge-file
    artifacts/protocol_result.yaml alone -- an existential quantifier across
    variants: the overall promotion result PASSES if AT LEAST ONE variant's
    own DSR/expectancy verdict passes. The per-candidate math itself
    (_dsr_candidate below) is verbatim the original single-result computation,
    extracted unchanged so the campaign-wide trial-ledger statistics
    (deduped_trials/sharpe_values/n_dsr_total/n_trials/excluded/total_tested --
    these are the SAME across every variant, since the multiple-testing
    correction's distribution is estimated from the whole campaign's trial
    ledger, not per-variant) are computed exactly once regardless of which
    protocol_result(s) they're evaluated against. Flag-off path below is
    untouched code, reached unconditionally when
    orchestrator.variant_loop.enabled is off/absent -- byte-identical
    promotion_audit.yaml to every pre-4b run (save_yaml uses sort_keys=False,
    so the dict's insertion order was preserved exactly, not just its keys).
    """
    # --- Load verdict interpretation for hypothesis_id ---
    if _specialist_readers_enabled():
        # E-046a Slice 5b-ii-B: verdict_interpretation.yaml is never written under
        # this flag; the idea's id comes from hypothesis_card.yaml (which the old
        # stage only restated). Raises rather than falling back to run_id.
        hyp_id = _idea_hypothesis_id(run_dir)
    else:
        interp      = load_yaml(run_dir / "artifacts" / "verdict_interpretation.yaml") or {}
        hyp_id      = interp.get("hypothesis_id", run_id)

    # Branch 3 (2026-09-24): the ledger statistics and _dsr_candidate were
    # extracted verbatim into _promotion_dsr_context() -- same values, same
    # order of evaluation after hyp_id, so promotion_audit.yaml is unchanged.
    _dsr_ctx        = _promotion_dsr_context()
    campaign        = _dsr_ctx["campaign"]
    n_dsr_total     = _dsr_ctx["n_dsr_total"]
    n_trials        = _dsr_ctx["n_trials"]
    excluded        = _dsr_ctx["excluded"]
    total_tested    = _dsr_ctx["total_tested"]
    DSR_THRESHOLD   = _dsr_ctx["DSR_THRESHOLD"]
    _dsr_candidate  = _dsr_ctx["dsr_candidate"]

    if _variant_loop_enabled():
        # Slice 4b (E-033.1), per the operator's 2026-09-22 Decision section
        # (Branch 3): every variant's own protocol_result.yaml is evaluated
        # independently; the overall promotion result PASSES if AT LEAST ONE
        # variant clears the DSR/expectancy bar -- an existential quantifier,
        # not a single/base-only result. Deliberately NOT touching
        # _evaluate_profit_bars (a separate function, out of this slice's
        # stated build list) -- it still reads THIS function's top-level
        # fields, which remain present and now represent the winning (or,
        # absent a winner, the most-informative) variant.
        variants_dir = run_dir / "artifacts" / "variants"
        variant_results: dict = {}
        if variants_dir.exists():
            for vdir in sorted(p for p in variants_dir.iterdir() if p.is_dir()):
                vpr_path = vdir / "protocol_result.yaml"
                if vpr_path.exists():
                    variant_results[vdir.name] = load_yaml(vpr_path) or {}
        if not variant_results:
            # No per-variant protocol_result.yaml exists at all (e.g. every
            # variant's backtest failed before writing one -- protocol_execution
            # itself already raises if NO variant succeeded, S1_FINDINGS.md
            # §3a, so this is a defensive fallback, not the expected path).
            # Fall back to the singular bridge file so this function still
            # produces an audit rather than an empty per_variant block.
            _pr_path = run_dir / "artifacts" / "protocol_result.yaml"
            variant_results = {"base": load_yaml(_pr_path) if _pr_path.exists() else {}}

        per_variant: dict = {}
        for vid, pr in sorted(variant_results.items()):
            v_raw_median_sr, v_is_sparse, v_passes, v_e_max_sr, v_dsr_result = _dsr_candidate(pr)
            per_variant[vid] = {
                "raw_median_sharpe":         v_raw_median_sr,
                "is_sparse_trading":         v_is_sparse,
                "passes_deflated_threshold": v_passes,
                "promotion_threshold_raw":   v_e_max_sr,
                **v_dsr_result,
            }

        # Existential OR: True beats None (indeterminate) beats False. A
        # variant reading None (e.g. a sparse candidate whose expectancy SE
        # could not be computed) must never be conflated with a hard False --
        # only report an overall False when EVERY variant's own passes value
        # is False.
        passing = sorted(vid for vid, f in per_variant.items() if f["passes_deflated_threshold"] is True)
        indeterminate = sorted(vid for vid, f in per_variant.items() if f["passes_deflated_threshold"] is None)
        if passing:
            passes_deflated = True
            # CODE-REVIEW FIX (2026-09-22): previously picked the
            # alphabetically-first passing variant_id, so a weaker passing
            # candidate (e.g. DSR barely over threshold) could be reported
            # as `promoted_variant` over a stronger one (e.g. DSR well
            # above threshold) purely by name ordering. Rank by the
            # variant's own deflated_sharpe_ratio, highest first; a
            # variant lacking that key (the sparse/expectancy-only path)
            # sorts last rather than crashing, since it has no comparable
            # DSR figure to rank on. Ties (including all-missing) fall back
            # to alphabetical for determinism.
            def _evidence_strength(vid: str) -> float:
                f = per_variant[vid]
                dsr = f.get("deflated_sharpe_ratio")
                if dsr is not None:
                    return dsr
                # Sparse/expectancy-valid candidates never have a DSR figure
                # -- fall back to the expectancy t-stat as the comparable
                # "how far past the promotion bar" evidence strength for
                # that pathway.
                t_stat = (f.get("expectancy_promotion") or {}).get("t_stat")
                return t_stat if t_stat is not None else float("-inf")
            rep_vid = max(
                passing,
                key=lambda vid: (_evidence_strength(vid), -passing.index(vid)),
            )
        elif indeterminate:
            passes_deflated = None
            rep_vid = indeterminate[0]
        else:
            passes_deflated = False
            rep_vid = sorted(per_variant)[0]
        rep = per_variant[rep_vid]

        audit = {
            "hypothesis_id":                hyp_id,
            "generated_at":                 datetime.now(timezone.utc).isoformat(),
            "raw_median_sharpe":             rep["raw_median_sharpe"],
            "total_hypotheses_tested":       n_dsr_total,
            "total_campaign_runs":           len(campaign.get("runs", [])),
            "total_variants_tested":         total_tested,
            "n_trials_used":                 n_trials,
            "is_sparse_trading":             rep["is_sparse_trading"],
            "passes_deflated_threshold":     passes_deflated,
            "promoted_variant":              rep_vid if passes_deflated else None,
            "promotion_threshold_raw":       rep["promotion_threshold_raw"],
            "promotion_threshold_deflated":  DSR_THRESHOLD,
            "excluded_trial_counts":         excluded,
            "deflated_sharpe_ratio":         rep.get("deflated_sharpe_ratio"),
            "expected_max_sharpe":           rep.get("expected_max_sharpe"),
            "trial_sharpe_variance":         rep.get("trial_sharpe_variance"),
            "correction_method":             rep.get("correction_method"),
            **({"dsr_error": rep["dsr_error"]} if "dsr_error" in rep else {}),
            **({"expectancy_promotion": rep["expectancy_promotion"]} if "expectancy_promotion" in rep else {}),
            # per_variant: {variant_id: {raw_median_sharpe, is_sparse_trading,
            # passes_deflated_threshold, promotion_threshold_raw,
            # deflated_sharpe_ratio, expected_max_sharpe, trial_sharpe_variance,
            # correction_method, dsr_error?, expectancy_promotion?}} -- the new
            # design surface this build item introduces (S1_FINDINGS.md §6.5
            # had no precedent to follow).
            "per_variant": per_variant,
        }
    else:
        # Flag-off: byte-identical to pre-4b -- exactly one candidate, the
        # singular bridge-file protocol_result.yaml, exactly as before Slice
        # 4/4b existed. Same dict key insertion order as the pre-4b body
        # (save_yaml writes with sort_keys=False).
        pr_path = run_dir / "artifacts" / "protocol_result.yaml"
        pr = load_yaml(pr_path) if pr_path.exists() else {}
        raw_median_sr, is_sparse, passes_deflated, e_max_sr, dsr_result = _dsr_candidate(pr)

        audit = {
            "hypothesis_id":              hyp_id,
            "generated_at":               datetime.now(timezone.utc).isoformat(),
            "raw_median_sharpe":          raw_median_sr,
            # COUNT-DIV fix (2026-08-17): promotion_audit.schema.json declares
            # total_hypotheses_tested as "Total deduplicated trial records in
            # campaign_state.trial_sharpes at audit time (N in BLP 2014)" -- i.e.
            # n_dsr_total, matching deflate_sharpe.py's own total_hypotheses_tested
            # exactly. This field previously held len(campaign["runs"]) -- an
            # unrelated data structure (the campaign's run-id list, not
            # trial_sharpes), an outright schema violation, not just a naming
            # ambiguity. n_dsr_total is what the DSR math above actually uses
            # (:4270) but was never exposed in the output before this fix.
            "total_hypotheses_tested":    n_dsr_total,
            # The displaced metric keeps its own honest name rather than being
            # dropped -- a legitimate, different count (this campaign's total run
            # attempts, not the trial-ledger's deduplicated DSR-N).
            "total_campaign_runs":        len(campaign.get("runs", [])),
            "total_variants_tested":      total_tested,
            "n_trials_used":              n_trials,
            "is_sparse_trading":          is_sparse,
            "passes_deflated_threshold":  passes_deflated,
            "promotion_threshold_raw":    e_max_sr,
            "promotion_threshold_deflated": DSR_THRESHOLD,
            "excluded_trial_counts":      excluded,
            **dsr_result,
        }

    audit_path = run_dir / "artifacts" / "promotion_audit.yaml"
    save_yaml(audit_path, audit)
    _final_passes = audit["passes_deflated_threshold"]
    status_str = "PASS" if _final_passes else ("INDETERMINATE" if _final_passes is None else "FAIL")
    print(f"⚙️  A6.2: promotion_audit.yaml written (DSR={audit.get('deflated_sharpe_ratio')}, "
          f"n_trials={n_trials}, passes={status_str})")


def _grade_profit_bars(bars: dict, *, sharpe, sharpe_note: str, dsr, dsr_note: str,
                       pss: dict, portfolio: dict | None = None) -> tuple:
    """Grade ONE candidate against every bar in a loaded profitability_bars.yaml
    doc. Returns (results, overall, reasons): results is the ordered list of
    {name, threshold, actual, result, note} bar rows, overall is "PASS" only when
    EVERY bar reads PASS (a NOT_EVALUABLE bar blocks it), reasons lists every
    non-PASS bar. `sharpe`/`dsr` come from the caller's own source (the promote
    path: promotion_audit.yaml; the per-backtest path: _promotion_dsr_context's
    evaluator on the variant's own protocol_result) and `*_note` names it. `pss`
    is that candidate's protocol_result per_symbol_summary.

    `portfolio` is None for every flag-off caller: the rows are then exactly what
    they were before branch 3 (worst-coin drawdown, NOT_EVALUABLE avg daily
    return, no `basis` key). Under orchestrator.profit_bars_every_backtest the
    caller passes _portfolio_profit_metrics(...): max_drawdown_pct_max and
    avg_daily_return_min are then judged on the equal-weight portfolio of all
    tested coins (operator decision 2026-09-24), and every row records the
    definition that produced its `actual` in a `basis` key.

    Extracted verbatim 2026-09-24 from _evaluate_profit_bars (branch 3) -- see
    that function's docstring for the flag-off worst-symbol aggregation choice."""
    results = []

    def _bar(name: str, threshold, actual, comparator: str, note: str = "", basis: str = "",
             not_evaluable_reason: str | None = None):
        if actual is None:
            outcome = "NOT_EVALUABLE"
        elif comparator == ">=":
            outcome = "PASS" if actual >= threshold else "FAIL"
        elif comparator == "<=":
            outcome = "PASS" if actual <= threshold else "FAIL"
        else:
            raise ValueError(f"_evaluate_profit_bars: unknown comparator {comparator!r}")
        entry = {"name": name, "threshold": threshold, "actual": actual, "result": outcome}
        if portfolio is not None:  # flag on only: flag-off rows stay byte-identical
            entry["basis"] = basis
            if actual is None and not_evaluable_reason:
                # A structured field (and a line in `reasons`), never only the note.
                entry["not_evaluable_reason"] = not_evaluable_reason
        if note:
            entry["note"] = note
        results.append(entry)

    _bar("sharpe_min", bars["sharpe_min"], sharpe, ">=", note=sharpe_note,
         basis="median_of_coin_median_sharpes")

    _bar(
        "deflated_sharpe_threshold", bars["deflated_sharpe_threshold"], dsr, ">=",
        note=dsr_note, basis="deflated_sharpe_on_campaign_trial_ledger",
    )

    if portfolio is None:
        symbol_drawdowns = [v.get("max_abs_drawdown_pct") for v in pss.values()
                             if v.get("max_abs_drawdown_pct") is not None]
        worst_drawdown = max(symbol_drawdowns) if symbol_drawdowns else None
        _bar(
            "max_drawdown_pct_max", bars["max_drawdown_pct_max"], worst_drawdown, "<=",
            note="protocol_result.yaml.per_symbol_summary[*].max_abs_drawdown_pct, worst symbol",
        )
    else:
        _bar("max_drawdown_pct_max", bars["max_drawdown_pct_max"],
             portfolio["max_drawdown_pct"][0], "<=", note=portfolio["max_drawdown_pct"][1],
             basis=_BASIS_PORTFOLIO_WORST_WINDOW,
             not_evaluable_reason=portfolio.get("not_evaluable_reason"))

    symbol_trade_counts = [v.get("min_trade_count") for v in pss.values()
                            if v.get("min_trade_count") is not None]
    worst_trade_count = min(symbol_trade_counts) if symbol_trade_counts else None
    _bar(
        "trade_count_min", bars["trade_count_min"], worst_trade_count, ">=",
        note="protocol_result.yaml.per_symbol_summary[*].min_trade_count, worst symbol",
        basis=_BASIS_WORST_COIN,
    )

    # avg_daily_return_min: with `portfolio` omitted (every flag-off caller) this
    # reads NOT_EVALUABLE exactly as before -- protocol_result.yaml has no
    # mean-daily-return field. Under orchestrator.profit_bars_every_backtest the
    # caller passes _portfolio_profit_metrics(...), derived from the per-window
    # equity files (definition in its docstring).
    if portfolio is None:
        _bar(
            "avg_daily_return_min", bars["avg_daily_return_min"], None, ">=",
            note="no source: protocol_result.yaml and metrics.json's bar_equity block "
                 "(off-by-default) neither one carries a mean-daily-return figure",
        )
    else:
        _bar("avg_daily_return_min", bars["avg_daily_return_min"],
             portfolio["avg_daily_return"][0], ">=", note=portfolio["avg_daily_return"][1],
             basis=_BASIS_PORTFOLIO,
             not_evaluable_reason=portfolio.get("not_evaluable_reason"))

    outcomes = {r["result"] for r in results}
    overall = "PASS" if outcomes == {"PASS"} else "FAIL"
    reasons = [
        f"{r['name']}: {r['result']} (threshold={r['threshold']!r}, actual={r['actual']!r})"
        + (f" -- {r['not_evaluable_reason']}" if r.get("not_evaluable_reason") else "")
        for r in results if r["result"] != "PASS"
    ]

    return results, overall, reasons


def _evaluate_profit_bars(run_dir: Path, run_id: str, portfolio_basis: bool = False) -> dict:
    """delivery_plan_v26.md 0.2 (item 2) -- the branch-3 stop. Sibling to
    _write_promotion_audit, called right after it (same run_dir) so this function
    can read promotion_audit.yaml's own just-written numbers rather than
    re-deriving them. Evaluates every bar in config/profitability_bars.yaml against
    the real numbers already present in promotion_audit.yaml / protocol_result.yaml
    for this run -- NOT against protocol_result.yaml's raw candidate numbers
    directly for the Sharpe/DSR bars (promotion_audit.yaml is the one place those
    are already reconciled: dedup, invalidated-trial exclusion, the sparse-vs-DSR
    branch). Writes artifacts/profit_bars_evaluation.yaml and returns the same dict.

    Each bar reads NOT_EVALUABLE, not a silent PASS or a crash, when its
    underlying metric genuinely is not present anywhere in this run's artifacts
    (see per-bar comments in _grade_profit_bars -- avg_daily_return_min always does
    with portfolio_basis off, since nothing else in this pipeline computes a mean
    daily return).

    portfolio_basis=True is passed only under orchestrator.profit_bars_every_backtest
    (and only for a run without its own every_backtest evaluation): drawdown and avg
    daily return are then judged on the equal-weight portfolio of all coins
    (_portfolio_profit_metrics) and every row carries `basis`. The paragraph below
    describes the flag-off (portfolio_basis=False) behavior, which is unchanged.

    Aggregation choice for the two per-symbol_summary-sourced bars
    (max_drawdown_pct_max, trade_count_min): per_symbol_summary carries one
    value per symbol, not a single campaign-wide number, and profitability_bars.yaml
    declares one threshold. Deliberately conservative in the fail-loud direction:
    max_drawdown_pct_max compares against the WORST (highest) per-symbol drawdown,
    trade_count_min compares against the WORST (lowest) per-symbol trade count --
    a bar that would fail on any one traded symbol reads FAIL, not PASS-on-average.
    """
    bars = _load_profitability_bars()

    audit_path = run_dir / "artifacts" / "promotion_audit.yaml"
    audit = load_yaml(audit_path) if audit_path.exists() else {}
    pr_path = run_dir / "artifacts" / "protocol_result.yaml"
    pr = load_yaml(pr_path) if pr_path.exists() else {}
    pss = pr.get("per_symbol_summary") or {}

    # Branch 3 (2026-09-24): the bar-by-bar grading moved verbatim into
    # _grade_profit_bars so the per-backtest check grades every variant with the
    # same comparators, aggregation and NOT_EVALUABLE rules. Same notes, same
    # order, same output as before.
    results, overall, reasons = _grade_profit_bars(
        bars,
        sharpe=audit.get("raw_median_sharpe"),
        sharpe_note="promotion_audit.yaml.raw_median_sharpe",
        dsr=audit.get("deflated_sharpe_ratio"),
        dsr_note="promotion_audit.yaml.deflated_sharpe_ratio (None on the sparse-trading or "
                 "insufficient-trials path, where no DSR is computed at all)",
        pss=pss,
        # Only under orchestrator.profit_bars_every_backtest (the caller passes
        # portfolio_basis=True): the same equal-weight portfolio computation as the
        # per-backtest check (drawdown and avg daily return), with `basis` on every
        # row. Flag off: omitted -- worst-symbol drawdown and NOT_EVALUABLE avg
        # daily return, byte-identical to before.
        portfolio=(_portfolio_profit_metrics(run_dir, pr) if portfolio_basis else None),
    )

    evaluation = {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "bars": results,
        "result": overall,
        "reasons": reasons,
    }
    save_yaml(run_dir / "artifacts" / "profit_bars_evaluation.yaml", evaluation)
    print(f"⚙️  0.2: profit_bars_evaluation.yaml written (result={overall})")
    return evaluation


# --- Branch 3 on every backtest (orchestrator.profit_bars_every_backtest.enabled) ---
#
# Why here and not on the promote path: the promote path is reached only by an
# idea the walk-forward verdict route promotes, so only grid-validated ideas were
# ever checked against the bars. Branch 3 is independent of the grid (branch 1)
# and the readers (branch 2): every tested variant of THIS protocol_execution
# attempt is graded right after protocol_execution, and a variant may reach the
# bars while the idea itself is not validated.
#
# Order (code review 2026-09-24): judge (grid, in protocol_execution) -> learn
# (specialist_readers) -> profit check (graded right after protocol_execution,
# recorded, never paused there) -> regroup + record (campaign memory carries the
# per-variant results) -> decide (the route after regroup_record raises the
# profit_bars_reached stop BEFORE the grid route, see _profit_bars_stop_route).
# A resume re-enters regroup_record, never protocol_execution: the backtests are
# never re-run by a resume.
#
# Hard alignment rule (do not relax): this check reads protocol results, the
# per-window equity files and the trial ledger; it writes only
# artifacts/profit_bars_evaluation.yaml and (later, in the route) the pause flag.
# It writes no trial row (slice 4 owns them), never touches idea_status.yaml /
# grid_evaluation.yaml, and feeds nothing retired (refine/pivot/escalate/kill,
# the circuit breaker, hypothesis_family, altitude_history, continuation
# children).

_PROFIT_BARS_EVALUATION_FILE = "profit_bars_evaluation.yaml"


def _profit_bars_scope_every_backtest() -> str:
    """The one scope constant, owned by tools/campaign_memory.py (its reader)."""
    return _campaign_memory_module().PROFIT_BARS_SCOPE_EVERY_BACKTEST


def _invalidated_trial_ids() -> set:
    """trial_ids carrying invalidated_artifact (a conformance violation marks
    the row; _mark_trial_invalidated). Read only."""
    rows = (load_campaign_state() or {}).get("trial_sharpes") or []
    return {r.get("trial_id") for r in rows if isinstance(r, dict) and r.get("invalidated_artifact")}


def _backtest_failed_trial_ids() -> set:
    """trial_ids carrying a `backtest_failed` row (a spent look whose backtest
    produced no graded result). Read only."""
    rows = (load_campaign_state() or {}).get("trial_sharpes") or []
    return {r.get("trial_id") for r in rows
            if isinstance(r, dict) and r.get("source") == "backtest_failed"}


def _profit_bars_tested_candidate(run_dir: Path, cid: str, trial_id: str, rel: str, kind: str,
                                  invalidated: set) -> dict:
    """ONE tested backtest as branch 3 grades it: {kind, trial_id,
    protocol_result_ref, protocol_result, result, reason}. A trial row marked
    invalidated_artifact (conformance violation) is INVALIDATED -- never graded,
    never passing. Shared by branch 3 (_profit_bars_backtest_candidates) and
    the composition grid's profit_bars grader (_profit_bars_grid_grader), so
    the two cannot disagree (E-060 S3b review fix 4)."""
    if trial_id in invalidated:
        return {"kind": kind, "trial_id": trial_id, "protocol_result_ref": None,
                "protocol_result": None, "result": "INVALIDATED",
                "reason": f"trial {trial_id!r} is invalidated_artifact (conformance "
                          f"violation): not graded, never passing"}
    if not (run_dir / rel).exists():
        raise FileNotFoundError(
            f"profit bars (every backtest): grid column {cid!r} has no {run_dir / rel}.")
    pr = load_yaml(run_dir / rel)
    if not isinstance(pr, dict):
        raise ValueError(f"profit bars (every backtest): {rel} is not a mapping "
                         f"({type(pr).__name__}).")
    return {"kind": kind, "trial_id": trial_id, "protocol_result_ref": rel,
            "protocol_result": pr, "result": None, "reason": None}


def _profit_bars_backtest_candidates(run_dir: Path, run_id: str) -> dict:
    """The backtests THIS protocol_execution attempt produced, keyed as the grid
    keys its columns: {candidate_id: {kind, trial_id, protocol_result_ref,
    protocol_result, result, reason}}; `result` is None for a gradeable
    candidate, else "NOT_TESTED" or "INVALIDATED".

    The tested set is the columns of this attempt's grid_evaluation.yaml (the
    flag requires specialist_readers, which deletes the previous attempt's grid at
    protocol_execution entry, and fails protocol_execution when no grid is
    written) -- never "which protocol_result.yaml files exist on disk", which can
    hold a stale file from an earlier attempt whose backtest failed this time.
      * variant loop on: one entry per artifacts/variants/index.yaml variant. A
        grid column is tested (its own artifacts/variants/<id>/protocol_result.yaml
        must exist); a variant in the grid's failed_variants (E-061 C2 S2a,
        D-015; never a column) is NOT_TESTED -- a `backtest_failed:` one with
        its backtest_failed trial_id, a `refused:` one with none; a validated
        variant without a column (a grid written before S2a) failed its
        backtest; any other index status was not tested.
      * variant loop off: the grid's single column, run_id, graded from
        artifacts/protocol_result.yaml.
    A tested candidate whose trial row is invalidated_artifact (conformance
    violation) is INVALIDATED: never graded, never passing.

    SLICE 7 SEAM (composition, not built here): a composite's backtest is a
    second candidate kind. Add it here as {kind: "composite", ...} from wherever
    slice 7 writes its protocol result; _evaluate_profit_bars_every_backtest
    grades every candidate the same way, and the any-candidate-passes stop rule
    already covers it.

    Raises (fail loud) on a missing/malformed grid, a grid column outside the
    index, a tested column without its result file, or a result that is not a
    mapping."""
    arts = run_dir / "artifacts"
    grid_path = arts / "grid_evaluation.yaml"
    if not grid_path.exists():
        raise FileNotFoundError(
            f"profit bars (every backtest): {grid_path} is missing -- the tested variants of "
            f"this attempt are the grid's columns, and protocol_execution writes the grid "
            f"under specialist_readers.")
    grid_doc = load_yaml(grid_path) or {}
    columns = grid_doc.get("variants")
    if not isinstance(columns, list) or not columns:
        raise ValueError(f"profit bars (every backtest): {grid_path} has no variant columns.")
    # E-061 C2 S2a (D-015): a failed variant is never a column; it is NOT_TESTED
    # here, so it can never be graded or pass the bars (its result file may be
    # missing, or a stale one from an earlier attempt). The evaluator's own
    # validator: a present but malformed failed_variants raises.
    _vce = _verdict_criteria_evaluator_module()
    try:
        failed = _vce.grid_failed_variants(grid_doc)
    except ValueError as exc:
        raise ValueError(f"profit bars (every backtest): {grid_path}: {exc}") from exc
    # D-021: the grid's idea status is NOT a holdout precondition -- the graded
    # survivors of an inconclusive (or refuted) idea are still graded here, on purpose.
    invalidated = _invalidated_trial_ids()
    # E-060 S3b (the slice-7 seam below): a composition run's variants ARE the
    # composite backtests -- same grading, same stop rule, label `composite`.
    kind = "composite" if _composition_mode(run_dir) else "variant"
    out: dict = {}

    def _tested(cid: str, trial_id: str, rel: str) -> dict:
        return _profit_bars_tested_candidate(run_dir, cid, trial_id, rel, kind, invalidated)

    if _variant_loop_enabled():
        index_path = arts / "variants" / "index.yaml"
        variants = (load_yaml(index_path) or {}).get("variants") if index_path.exists() else None
        if not isinstance(variants, dict) or not variants:
            raise ValueError(f"profit bars (every backtest): {index_path} lists no variants.")
        unknown = [c for c in list(columns) + list(failed) if c not in variants]
        if unknown:
            raise ValueError(f"profit bars (every backtest): grid column(s) / failed variant(s) "
                             f"{unknown} are not in {index_path}.")
        failed_rows = _backtest_failed_trial_ids() if failed else set()
        for vid in sorted(variants):
            info = variants[vid] if isinstance(variants[vid], dict) else {}
            if vid in failed:
                # A crashed variant carries its real backtest_failed trial_id; a
                # refused one touched no data and has no trial row (null).
                refused = failed[vid].startswith(_vce.FAILED_VARIANT_REFUSED)
                tid = f"{run_id}:{vid}"
                out[vid] = {"kind": kind,
                            "trial_id": None if refused or tid not in failed_rows else tid,
                            "protocol_result_ref": None,
                            "protocol_result": None, "result": "NOT_TESTED",
                            "reason": (f"refused before any backtest, no data touched "
                                       f"({failed[vid]}): never graded, never passing"
                                       if refused else
                                       f"backtest failed ({failed[vid]}): never graded, "
                                       f"never passing")}
            elif vid in columns:
                out[vid] = _tested(vid, f"{run_id}:{vid}",
                                   f"artifacts/variants/{vid}/protocol_result.yaml")
            elif info.get("status") == "validated":
                out[vid] = {"kind": kind, "trial_id": None, "protocol_result_ref": None,
                            "protocol_result": None, "result": "NOT_TESTED",
                            "reason": "validated, but no grid column on this attempt "
                                      "(its backtest failed)"}
            else:
                out[vid] = {"kind": kind, "trial_id": None, "protocol_result_ref": None,
                            "protocol_result": None, "result": "NOT_TESTED",
                            "reason": f"not tested (index status {info.get('status')!r}): "
                                      f"{info.get('reason')}"}
    else:
        if columns != [run_id] or failed:
            raise ValueError(f"profit bars (every backtest): variant loop off, so the grid must "
                             f"have the single, graded column {run_id!r}; got {columns} "
                             f"(failed_variants {failed!r}).")
        out[run_id] = _tested(run_id, run_id, "artifacts/protocol_result.yaml")
    return out


# E-060 S3b code review fix 9: the equal-weight portfolio's readers live in
# tools/portfolio_daily.py (one definition, shared with the composition's
# stand-alone block returns). The old names stay as aliases.
import portfolio_daily as _pd  # noqa: E402  (tools/ is on sys.path, module top)
_find_window_equity_file = _pd.find_window_equity_file
_window_equity_bars = _pd.window_equity_bars
_daily_closes = _pd.daily_closes
_window_daily_closes = _pd.window_daily_closes


# basis values recorded on each bar row of a flag-on evaluation, so the artifact
# says which definition produced `actual` (see config/profitability_bars.yaml).
_BASIS_PORTFOLIO = "portfolio_equal_weight"
_BASIS_PORTFOLIO_WORST_WINDOW = "portfolio_equal_weight_worst_window"
_BASIS_WORST_COIN = "worst_coin"

PORTFOLIO_MIN_COMMON_DAY_COVERAGE = _pd.PORTFOLIO_MIN_COMMON_DAY_COVERAGE  # one definition


def _portfolio_profit_metrics(run_dir: Path, pr: dict) -> dict:
    """avg_daily_return_min and max_drawdown_pct_max actual values for ONE backtest
    candidate, judged on the portfolio you would actually trade: every tested coin
    together, equally weighted (operator decision 2026-09-24). Returns
    {"avg_daily_return": (value or None, note),
     "max_drawdown_pct": (value or None, note),
     "not_evaluable_reason": None, or why both values are None}.

    DEFINITION (mirrored in config/profitability_bars.yaml's header):
      * source: every (coin, window) backtest in protocol_result.results, via its
        portfolio_states.csv, column postRebalance_total_value (equity after each
        bar's rebalance), warm-up bars (regime NOT_READY) dropped;
      * daily close: the last bar of each UTC calendar day;
      * COMMON DAYS, per window: the UTC days on which every coin of that window
        has a daily close (the intersection). A day missing for any coin is
        dropped for all coins (never filled, never 0.0). The common days must
        cover at least PORTFOLIO_MIN_COMMON_DAY_COVERAGE of the union of the
        coins' days, and there must be at least 2 of them, in EVERY window;
      * normalization: each coin is divided by its daily close on the FIRST COMMON
        DAY of the window (so each coin is 1.0 there); portfolio value = the
        arithmetic MEAN of the coins' normalized values (1/N of the capital in each
        coin at that close, no re-weighting between coins afterwards);
      * daily return: SIMPLE return V_d / V_(d-1) - 1 of the portfolio's daily
        closes, counted only between two common days that are CONSECUTIVE calendar
        days of the same window. A step across a gap (a dropped or missing day) is
        a multi-day return and is NOT counted; the chain restarts after the gap.
        Windows are separate periods that each restart from a fresh balance;
      * avg daily return = the ARITHMETIC mean of those daily returns, pooled across
        all windows (a fraction per day; not geometric, not annualised);
      * max drawdown, on BARS (so intraday drops count): per window, the portfolio
        curve over the COMMON BARS (timestamps at which every coin has a bar), from
        the first-common-day close onwards, each coin normalized as above; the
        largest peak-to-trough fall 100 * (1 - V_t / max_{s<=t} V_s) (a positive
        percent); actual = the LARGEST such WINDOW drawdown. This is the worst
        WINDOW of the combined portfolio, not the worst coin.
    Both values None (NOT_EVALUABLE, reason in `not_evaluable_reason`) when results
    is empty, any window's portfolio_states.csv is missing, the coin set differs
    between windows (run_protocol writes every coin in every window, so a mismatch
    means broken data), any window has fewer than 2 common days, is below the
    coverage floor, or has no common bar from its first-common-day close onwards,
    or no daily return is left after the gap rule. A malformed results entry or a
    duplicate (coin, window) raises. Windows are visited in results order and
    coins sorted as strings, so mixed label types cannot raise."""
    def _none(why: str) -> dict:
        reason = f"equal-weight portfolio NOT_EVALUABLE: {why}"
        return {"avg_daily_return": (None, reason), "max_drawdown_pct": (None, reason),
                "not_evaluable_reason": reason}

    # E-060 S3b code review fix 9: the readers, the common days and the daily
    # returns come from tools/portfolio_daily.py (shared with the composition);
    # same order of checks, same messages.
    try:
        windows, coins = _pd.load_windows(run_dir, pr)
    except _pd.PortfolioNotEvaluable as exc:
        return _none(str(exc))

    returns: list = []
    window_dd: dict = {}
    n_union = n_common = n_gap_steps = n_bars = 0
    for win, by_coin in windows.items():
        try:
            wc = _pd.window_common_curve(win, by_coin, coins)
        except _pd.PortfolioNotEvaluable as exc:
            return _none(str(exc))
        daily, union, common, anchor = wc["daily"], wc["union"], wc["common"], wc["anchor"]
        n_union += len(union)
        n_common += len(common)
        rets, gaps = _pd.consecutive_daily_returns(common, wc["curve"])
        returns.extend(r for _d, r in rets)
        n_gap_steps += gaps
        # Drawdown on the bar-level curve, from the first-common-day close onwards.
        start_ts = max(daily[c][common[0]][0] for c in coins)
        common_bars = sorted(t for t in set.intersection(*(set(by_coin[c]) for c in coins))
                             if t >= start_ts)
        if not common_bars:
            return _none(f"window {win!r} has no bar, from its first-common-day close "
                         f"onwards, at which every coin has a value")
        n_bars += len(common_bars)
        peak, dd = None, 0.0
        for t in common_bars:
            v = sum(by_coin[c][t] / anchor[c] for c in coins) / len(coins)
            peak = v if peak is None else max(peak, v)
            dd = max(dd, 1.0 - v / peak)
        window_dd[win] = dd * 100.0
    if not returns:
        return _none("no two common days are consecutive calendar days, so there is no "
                     "daily return")
    worst_window = max(window_dd, key=lambda w: window_dd[w])
    base = (f"equal-weight portfolio of {len(coins)} coin(s) {coins}, each normalized to 1.0 "
            f"at its close on the first common day of each window (postRebalance_total_value, "
            f"post-warmup), over {len(window_dd)} window(s); days: {n_union} in the union of "
            f"the coins' days = {n_common} common + {n_union - n_common} dropped by the "
            f"intersection (coverage floor {PORTFOLIO_MIN_COMMON_DAY_COVERAGE} per window); "
            f"{n_common} common = {len(window_dd)} first day(s) + {len(returns)} daily "
            f"return(s) + {n_gap_steps} multi-day step(s) across a gap, not counted")
    return {
        "avg_daily_return": (round(sum(returns) / len(returns), 8), (
            f"arithmetic mean of the portfolio's {len(returns)} daily simple return(s) "
            f"(last bar per UTC day, consecutive common days only), pooled across windows; "
            f"{base}")),
        "max_drawdown_pct": (round(window_dd[worst_window], 6), (
            f"largest peak-to-trough drawdown of the combined portfolio on its {n_bars} "
            f"common bar(s), within one window (worst WINDOW {worst_window!r}, not the worst "
            f"coin); {base}")),
        "not_evaluable_reason": None,
    }


def _grade_profit_bars_protocol_result(run_dir: Path, pr: dict, pr_ref: str, bars: dict,
                                       dsr_ctx: dict) -> tuple:
    """Branch 3's grading of ONE tested backtest (a variant, or a composite's
    variant): Sharpe and DSR from the promotion audit's evaluator on its own
    protocol_result, trade count from its per_symbol_summary, drawdown and avg
    daily return from its equal-weight portfolio -- (results, overall,
    reasons) from _grade_profit_bars. Extracted verbatim (E-060 S3b) so the
    grid's profit_bars cell of a composition run calls the SAME function
    (_profit_bars_grid_grader): the two cannot disagree on the same inputs."""
    raw_median_sr, _sparse, _passes, _e_max, dsr_result = dsr_ctx["dsr_candidate"](pr)
    return _grade_profit_bars(
        bars,
        sharpe=raw_median_sr,
        sharpe_note=(f"{pr_ref}: median of per_symbol_summary[*]"
                     f".median_sharpe (the promotion audit's raw_median_sharpe rule)"),
        dsr=dsr_result.get("deflated_sharpe_ratio"),
        dsr_note=(f"{pr_ref}: deflated Sharpe on the campaign trial "
                  f"ledger (the promotion audit's rule; None on the sparse-trading or "
                  f"insufficient-trials path, where no DSR is computed at all)"),
        pss=pr.get("per_symbol_summary") or {},
        portfolio=_portfolio_profit_metrics(run_dir, pr),
    )


def _evaluate_profit_bars_every_backtest(run_dir: Path, run_id: str, *,
                                         record_bars_sha: bool = False) -> dict:
    """Grade every tested variant of THIS attempt (see
    _profit_bars_backtest_candidates) against every bar in
    config/profitability_bars.yaml; write artifacts/profit_bars_evaluation.yaml
    (per-variant shape, scope every_backtest) and return it. Never pauses: the
    profit_bars_reached stop is raised later, in the route after regroup_record.

    Numbers per variant: Sharpe and DSR from _promotion_dsr_context's evaluator on
    that variant's own protocol_result (the promotion audit's own math and ledger
    basis, read after this attempt's trial rows were written and after the
    conformance check invalidated any non-conforming one); trade count from its own
    per_symbol_summary (minimum per coin); drawdown and avg daily return from the
    equal-weight portfolio of all its coins, built from its own per-window equity
    files (_portfolio_profit_metrics). Every bar row records its `basis`.

    result is PASS when ANY graded variant passes every bar; `passing` names them.
    A malformed or missing bars file raises ProfitabilityBarsSchemaError before
    anything is graded or written (fail loud; never a defaulted threshold).
    record_bars_sha (verdict_routing_retired only): also record the whole bars
    file's sha256 (BARS_FILE_SHA_FIELD)."""
    bars_sha = _bars_file_sha256() if record_bars_sha else None
    bars = _load_profitability_bars()
    if record_bars_sha and _bars_file_sha256() != bars_sha:
        raise ProfitabilityBarsSchemaError("config/profitability_bars.yaml changed while it was "
                                           "being loaded -- grade again.")
    candidates = _profit_bars_backtest_candidates(run_dir, run_id)
    dsr_ctx = _promotion_dsr_context()

    variants: dict = {}
    for cid, cand in candidates.items():
        entry = {"kind": cand["kind"], "trial_id": cand["trial_id"],
                 "protocol_result_ref": cand["protocol_result_ref"]}
        if cand["protocol_result"] is None:
            variants[cid] = {**entry, "result": cand["result"], "reason": cand["reason"],
                             "bars": [], "reasons": []}
            continue
        results, overall, reasons = _grade_profit_bars_protocol_result(
            run_dir, cand["protocol_result"], cand["protocol_result_ref"], bars, dsr_ctx)
        variants[cid] = {**entry, "result": overall, "reason": None,
                         "bars": results, "reasons": reasons}

    passing = sorted(cid for cid, v in variants.items() if v["result"] == "PASS")
    overall = "PASS" if passing else "FAIL"
    evaluation = {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": _profit_bars_scope_every_backtest(),
        "bars_ratified_by": bars["ratified_by"],
        "bars_ratified_at": bars["ratified_at"],
        "dsr_basis": {"n_dsr_total": dsr_ctx["n_dsr_total"], "n_trials": dsr_ctx["n_trials"]},
        # Per-variant shape. Composites (slice 7) would add their own graded
        # entries -- see _profit_bars_backtest_candidates' seam note.
        "variants": variants,
        "passing": passing,
        "result": overall,
    }
    if record_bars_sha:
        # Slice 6c S2d review fix 7 (verdict_routing_retired only, so every
        # other caller's file is unchanged): the whole bars file this was graded
        # under, compared byte-for-byte at spend time.
        evaluation[BARS_FILE_SHA_FIELD] = bars_sha
    save_yaml(run_dir / "artifacts" / _PROFIT_BARS_EVALUATION_FILE, evaluation)
    graded = sum(1 for v in variants.values() if v["bars"])
    print(f"⚙️  branch 3: profit_bars_evaluation.yaml written, {graded} graded variant(s) of "
          f"{len(variants)} (result={overall}, passing={passing}) -- recorded; any stop is "
          f"raised after regroup_record")
    return evaluation


def _load_every_backtest_evaluation(run_dir: Path, run_id: str) -> dict | None:
    """This run's per-backtest evaluation, or None when absent or not
    scope=every_backtest for this run_id (e.g. a promote-path file)."""
    path = run_dir / "artifacts" / _PROFIT_BARS_EVALUATION_FILE
    if not path.exists():
        return None
    doc = load_yaml(path)
    if (not isinstance(doc, dict) or doc.get("scope") != _profit_bars_scope_every_backtest()
            or doc.get("run_id") != run_id):
        return None
    return doc


def _profit_bars_stop_route(run_dir: Path, run_id: str) -> str | None:
    """The decide step's branch-3 stop, called by run_loop after regroup_record
    (so the memory already holds the per-variant results) and BEFORE the grid
    route: "human_pause" when this attempt's evaluation has a passing variant and
    this exact evaluation has not already stopped the run; else None (the grid
    route follows, unchanged).

    Same mechanics as the inconclusive_grid pause: status paused_for_human, the
    existing flag profit_bars_reached, pending_stage left at regroup_record (past
    protocol_execution). `profit_bars_stop_evaluation` records the evaluation's
    generated_at: a resume re-enters regroup_record and this route, which then
    sees the stop was already raised for this evaluation and continues into the
    grid route -- forward, never re-running the backtests and never re-pausing on
    the same numbers. A new protocol_execution attempt writes a new evaluation and
    can stop again. Never changes idea_status."""
    ev = _load_every_backtest_evaluation(run_dir, run_id)
    if ev is None:
        raise FileNotFoundError(
            f"profit bars (every backtest): {run_dir / 'artifacts' / _PROFIT_BARS_EVALUATION_FILE} "
            f"is missing or not this run's every_backtest evaluation -- it is written right "
            f"after protocol_execution under the flag.")
    passing = ev.get("passing") or []
    if not passing:
        return None
    state = load_yaml(run_dir / "pipeline_state.yaml") or {}
    if state.get("profit_bars_stop_evaluation") == ev.get("generated_at"):
        print(f"⚙️  branch 3: profit_bars_reached was already raised for this evaluation "
              f"({ev.get('generated_at')}); continuing into the grid route.")
        return None
    idea = load_yaml(run_dir / "artifacts" / "idea_status.yaml") or {}
    print(f"\n🛑 PROFIT BARS REACHED: variant(s) {passing} passed every bar in "
          f"config/profitability_bars.yaml. The grid's idea_status is "
          f"{idea.get('idea_status')!r} (unchanged -- it comes only from the grid). "
          f"Pausing for the operator (branch-3 stop).")
    update_state(path=run_dir, status="paused_for_human", flags={"profit_bars_reached": True},
                 profit_bars_stop_evaluation=ev.get("generated_at"))
    return "human_pause"


def _research_only_hold(run_dir: Path, run_id: str) -> bool:
    """Step 2b of _route_holdout_evaluation (E-015 S3), extracted verbatim by
    slice 6c S2d review fix 10 so the unlocked path under
    orchestrator.verdict_routing_retired runs the SAME hold. True when held
    (status paused_for_human, flags.research_only_unverified); False when the
    brief declares research_only: false (any stale hold flag is cleared).
    See the gate's step-2b comment for why it is affirmative."""
    _brief_path = run_dir / "artifacts" / "research_brief.yaml"
    brief = (load_yaml(_brief_path) or {}) if _brief_path.exists() else {}
    if brief.get("research_only") is not False:
        declared = brief.get("research_only", "<absent>")
        print(f"\n⏸️  HOLDOUT HELD: {run_id}'s research_brief.yaml does not affirmatively "
              f"declare the strategy tradable (research_only={declared!r}; a value of False "
              f"is required to proceed).")
        print(f"   The holdout is single-use and terminal, so it is spent only on a "
              f"strategy we could actually trade.")
        print(f"   DO NOT run the holdout backtest to resolve this — looking is spending, "
              f"and this run has not earned the look yet.")
        print(f"   Resolve by declaring tradability, then resume. A FRESH-LAUNCH run gets "
              f"this automatically from run_campaign.py's _materialize_run, which resolves "
              f"venue+product against config/venue_tradability.yaml. A REFINE/REFRAME "
              f"DESCENDANT inherits neither the key nor the venue fields and has no "
              f"automated path (research_only is resolved only at fresh launch), so a "
              f"human must check this run's venue+product against venue_tradability.yaml "
              f"and, only if it is genuinely tradable, record venue, product AND "
              f"research_only: false on this run's research_brief.yaml. Setting the flag "
              f"without doing that check is the bypass this gate exists to prevent.")
        # human_pause, NOT completed_rejected. The two terminal refusals below are
        # genuinely unrecoverable (DSR too low; holdout already consumed). This one is a
        # fixable declaration gap, and because research_only is not propagated by the
        # refine path (setup_next_run copies an LLM-authored proposed_brief.yaml) or the
        # reframe path (_safe_write_new_research_brief), a legitimately tradable
        # descendant lands here as a matter of course; completed_rejected would write
        # status="rejected", which resume_pipeline refuses to resume, killing a good run
        # over missing paperwork.
        #
        # The flag is LOAD-BEARING, not decoration. Without it _classify_human_pause
        # sees promotion_audit.yaml present + holdout_result.yaml absent and returns
        # `provisional_promote_awaiting_holdout`, whose RUNBOOK row instructs the
        # operator to "Run the holdout backtest ... by hand" — i.e. a bare human_pause
        # here would route the operator into spending the seal, which is strictly worse
        # than the terminal reject it replaced. The flag gives this its own classifier
        # bucket and its own RUNBOOK row (see run_campaign._classify_human_pause).
        #
        # Campaign-level consequence, stated rather than assumed: a classified pause
        # halts the campaign (process_once returns False) where completed_rejected would
        # have marked the entry done and advanced the queue. That is the intended
        # behaviour for a state needing a human decision, and it is the same shape every
        # other classified pause already has.
        update_state(path=run_dir, status="paused_for_human",
                     flags={"research_only_unverified": True})
        return True

    # Passed: clear any hold left from a previous attempt. The flag is sticky
    # (update_state merges rather than replaces), so without this the operator who
    # does exactly what the RUNBOOK row says — declare tradability, resume — gets
    # gate 2b passing while the stale flag still classifies the NEXT, legitimate
    # `provisional_promote_awaiting_holdout` pause as `research_only_unverified`.
    # That pause is then unresolvable by construction: its RUNBOOK row says not to
    # run the holdout backtest, while the run's own stdout says to run it, and no
    # action clears the flag. Deadlock, and precisely on the recovery path this
    # whole hold exists to keep open.
    # `or {}` matches the other four loads in this function: an empty-but-present
    # pipeline_state.yaml yields None, and .get on it would raise AttributeError —
    # surfacing as a misleading unhandled_exception instead of the hold.
    _sp = run_dir / "pipeline_state.yaml"
    _state = (load_yaml(_sp) or {}) if _sp.exists() else {}
    if (_state.get("flags") or {}).get("research_only_unverified"):
        update_state(path=run_dir, flags={"research_only_unverified": False})
        print(f"✅ {run_id}: tradability now declared — research_only hold cleared.")
    return False


def _route_holdout_evaluation(run_dir: Path, run_id: str) -> str:
    """
    Improvement 06: single-use holdout gate. Steps are listed in EXECUTION order;
    the order is load-bearing, so keep this list and the code in step.
    1.  Check promotion_audit.yaml — if passes_deflated_threshold is False, terminal reject.
    2.  Check campaign_data_policy.yaml — refuse if hypothesis_id already consumed.
    2b. Hold unless the brief affirmatively declares the strategy tradable (E-015 S3).
        Below 1 and 2 because both are terminal rejects that never touch the seal;
        above 3 and 4 because those are the acts it exists to prevent.
    3.  If holdout_result.yaml is absent, pause for human (holdout backtest must be
        run externally).
    4.  Mark the holdout consumed, then evaluate holdout_result.yaml's status.

    Slice 6c S2d review fix 10: the single-use check (_holdout_already_spent)
    and the research_only hold (_research_only_hold) are shared with the
    unlocked path under orchestrator.verdict_routing_retired, which never calls
    this function. Behaviour unchanged.
    """
    ARTIFACTS = run_dir / "artifacts"

    # Load hypothesis_id from promotion_audit or verdict_interpretation
    # (_holdout_hypothesis_id, shared with _record_spent_holdout).
    hyp_id, passes = _holdout_hypothesis_id(run_dir, run_id)

    # 1. Deflated Sharpe gate (if not sparse / not indeterminate)
    if passes is False:
        print(f"\n🛑 HOLDOUT BLOCKED: promotion_audit.yaml passes_deflated_threshold=False "
              f"for {hyp_id}. DSR too low — trial count and Sharpe distribution do not support promotion.")
        return "completed_rejected"

    # 2. Single-use enforcement
    policy = load_yaml(_DATA_POLICY_PATH) or {} if _DATA_POLICY_PATH.exists() else {}
    consumed = policy.get("holdout_consumed_by") or []
    if _holdout_already_spent(hyp_id, policy):
        print(f"\n🛑 HOLDOUT REFUSED: {hyp_id} has already consumed the single holdout evaluation "
              f"(found in campaign_data_policy.yaml holdout_consumed_by). "
              f"Second holdout attempt is mechanically forbidden per A6.1.")
        return "completed_rejected"

    # --- 2b. research_only / venue gate (E-015 S3) -------------------------------
    # POSITION: deliberately below steps 1-2 and above step 3. It must precede step
    # 3, whose message tells a human to go run the holdout backtest, and step 4,
    # which marks the seal consumed — those are the acts this gate exists to stop.
    # It must NOT precede steps 1-2: both return completed_rejected, which is
    # terminal and already safe, and holding above them would halt the whole
    # campaign (a classified pause makes process_once return False) for a run that
    # step 1 was going to reject anyway — trading a clean terminal reject for a
    # paperwork pause that resolves into the same rejection.
    # Until now research_only was written by run_campaign.py's _materialize_run and
    # read by nothing, so it protected nothing: a brief for a product we cannot
    # legally trade could reach the holdout and inform a live-money decision on
    # research-only evidence.
    #
    # AFFIRMATIVE check, not a negative one. `research_only is True` alone would be
    # decorative: measured 2026-08-18, 0 of 57 briefs in the tree carry the key at
    # all, and it is written by only one of the three research_brief.yaml writers,
    # so it does not survive a refine or a reframe. Requiring research_only is False
    # makes a missing/undeclared brief refuse instead of sail through, which matches
    # venue_tradability.yaml's own rule that silence must never resolve to a green
    # light — and needs no propagation machinery to be correct for child runs.
    #
    # Safe to make fail-closed: holdout_consumed_by is empty and no run has ever
    # reached this gate (measured, same date), so there is no legacy corpus this
    # blocks. The first run it stops is fixed by declaring venue/product on the
    # brief, which is exactly what this epic's registration rule asks for.
    #
    # On the upper bound of that position: ahead of step 3's human_pause, not merely
    # ahead of step 4's holdout_consumed_by write. Step 3 instructs a human to go run
    # the holdout backtest, and in this project's doctrine looking is spending, so
    # holding after that instruction has been printed would be holding after the fact.
    # load_yaml raises FileNotFoundError rather than returning None, and a run dir
    # with no research_brief.yaml at all must refuse like any other undeclared brief
    # — not crash out of the router with a traceback.
    if _research_only_hold(run_dir, run_id):
        return "human_pause"

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
    _mark_holdout_consumed(policy, consumed, hyp_id)

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


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
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
# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
_LEGACY_STATUS_TO_VERDICT_ROUTING = {
    "promote":  ("promote", None),
    "kill":     ("kill", "terminate"),
    "refine":   ("refine", "refine"),
    "pivot":    ("kill", "pivot"),
    "escalate": ("kill", "escalate"),
}

# E-018 (2026-09-13): inverse of the map above, keyed by the (hypothesis_verdict,
# lineage_routing) pair -- every pair in _LEGACY_STATUS_TO_VERDICT_ROUTING is
# distinct, so this is a clean one-to-one lookup. Used to translate a BINDING
# pass_rule_evaluation.yaml's mechanical (hv, lr) pair into the legacy single-enum
# "status" the circuit breaker itself operates on, so the breaker's family-history
# governance applies consistently whether the pair came from the mechanical
# evaluator or (pre-K2) the stage's own restated status.
_VERDICT_ROUTING_TO_LEGACY_STATUS = {v: k for k, v in _LEGACY_STATUS_TO_VERDICT_ROUTING.items()}


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
def _resolve_verdict_fields(interp: dict, original_status: str, breaker_status: str,
                             pre_eval: dict | None = None) -> tuple:
    """
    A8 (K2 kernel): resolves the (hypothesis_verdict, lineage_routing) pair a
    caller should route on, for one verdict_interpretation.yaml.

    E-018 (2026-09-13): when `pre_eval` (pass_rule_evaluation.yaml) carries a
    BINDING verdict (result PASS/FAIL, not a `discretion: stage` branch), its
    own hypothesis_verdict/lineage_routing are used DIRECTLY as the route --
    routing no longer depends on the stage's own restated copy being correct.
    This is what makes it safe to also give verdict_interpreter the near-miss
    scoreboard as an input: for any run with a registered, binding pass rule,
    the stage no longer holds the pen on the actual promote/kill decision, only
    on the qualitative fields (root_cause, findings_carryover, proposed_brief).
    `_check_pass_rule_evaluation_conformance` (below) still compares the
    stage's own restated pair against this one, but only to LOG a mismatch as
    an LLM-comprehension signal -- it no longer blocks routing (see caller).

    Falls back to the artifact's OWN hypothesis_verdict/lineage_routing fields
    (the A8 schema) when `pre_eval` is absent or not binding, and further falls
    back to deriving both from the legacy single-enum `status` field for a
    not-yet-migrated (pre-K2) artifact -- both fallback paths unchanged from
    before this function took `pre_eval`.

    `original_status` / `breaker_status` are the status string BEFORE and
    AFTER _apply_circuit_breaker ran (callers already compute both, deriving
    them from `pre_eval` when binding -- see determine_post_verdict_route). If
    the breaker fired (they differ), its forced value overrides
    `lineage_routing` ONLY -- the breaker's job is "route differently" (e.g.
    force pivot after repeated same-dimension refines), never "re-decide
    whether the mechanism itself is dead". A declared `hypothesis_verdict`
    (mechanical or artifact-own) survives a breaker override; only
    `lineage_routing` is replaced.
    """
    breaker_fired = breaker_status != original_status

    if pre_eval and pre_eval.get("result") in ("PASS", "FAIL") and pre_eval.get("discretion") != "stage":
        mech_hv = pre_eval.get("hypothesis_verdict")
        mech_lr = pre_eval.get("lineage_routing")
        if mech_hv is not None or mech_lr is not None:
            if breaker_fired:
                mapped = _LEGACY_STATUS_TO_VERDICT_ROUTING.get(breaker_status)
                if mapped is None:
                    raise ValueError(f"Unknown circuit-breaker-forced status: '{breaker_status}'")
                mapped_hv, mapped_lr = mapped
                return (mech_hv or mapped_hv), mapped_lr
            return mech_hv, mech_lr

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


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
def _dispatch_verdict_route(path: Path, run_id: str, interp: dict, campaign: dict,
                             hypothesis_verdict: str, lineage_routing: str | None,
                             routing_retired: bool = False) -> str:
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
    # Slice 6c S2a: the ONE refusal of the legacy routing, keyed on run_loop's
    # own pre-flight reading of orchestrator.verdict_routing_retired.enabled
    # (passed down as routing_retired; never re-read inside a run).
    if routing_retired:
        raise RuntimeError(
            "_dispatch_verdict_route is legacy verdict routing (v26 card G), retired under "
            "orchestrator.verdict_routing_retired.enabled -- it must not run. Under the flag "
            "the run ends completed_<idea_status> after regroup_record and decide_next picks "
            "the next run.")
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

        # delivery_plan_v26.md 0.2 (item 2) -- the branch-3 stop. ADDITIVE and
        # isolated in its own try/except, same posture as the E-046b grid-evaluation
        # block above (code-review fix 2026-09-20): a bug here must never turn an
        # already-successful _write_promotion_audit call into a misclassified
        # failure -- promotion_audit.yaml is already on disk by this point either
        # way, so on any exception this falls back to the pre-existing unconditional
        # "holdout_evaluation" route rather than raising.
        #
        # Coexistence with branch 3 on every backtest (code review 2026-09-24):
        # the promote-path check is skipped ONLY when THIS run already holds its
        # own scope=every_backtest evaluation (written right after
        # protocol_execution, graded on every variant with the same Sharpe/DSR
        # math, and the one that raises profit_bars_reached in the route after
        # regroup_record). A second evaluation would overwrite that per-variant
        # artifact with a single-candidate one, and a second pause on the same
        # numbers would re-stop a run the operator already released. Any other
        # case (flag off, or flag on but no such artifact, e.g. a run that
        # reached protocol_execution before the flag was on) runs the check as
        # before; with the flag on it grades avg_daily_return_min and
        # max_drawdown_pct_max on the equal-weight portfolio built from the
        # per-window equity files. The flag is read ONCE, inside the try, so even
        # a malformed flag value falls back to the unconditional holdout route.
        if _profit_bars_file_enabled():
            try:
                _pbe_on = _profit_bars_every_backtest_enabled()
                if _pbe_on and _load_every_backtest_evaluation(path, run_id) is not None:
                    print("⚙️  0.2: promote-path profit-bars check skipped -- this run's "
                          "artifacts/profit_bars_evaluation.yaml (scope every_backtest) already "
                          "graded every variant after protocol_execution.")
                    return "holdout_evaluation"
                profit_bars_result = (_evaluate_profit_bars(path, run_id, portfolio_basis=True)
                                      if _pbe_on else _evaluate_profit_bars(path, run_id))
                if profit_bars_result.get("result") == "PASS":
                    print("\n🛑 PROFIT BARS REACHED: every bar in config/profitability_bars.yaml "
                          "passed. Pausing for human regroup before the single-use holdout gate "
                          "(branch-3 stop, delivery_plan_v26.md 0.2).")
                    update_state(path=path, status="paused_for_human",
                                 flags={"profit_bars_reached": True})
                    return "human_pause"
            except Exception as _profit_bars_err:
                print(f"⚠️  [0.2] profit-bars evaluation raised "
                      f"{type(_profit_bars_err).__name__}: {_profit_bars_err} -- "
                      "promotion_audit.yaml is already written; routing to "
                      "holdout_evaluation as if the flag were off. Not re-raised: a "
                      "profit-bars bug must never block or misclassify a real promote.")

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


# legacy routing (v26 card G) -- not called under orchestrator.verdict_routing_retired
# (slice 6c S2a); kept for flag-off runs.
def determine_post_verdict_route(path: Path, run_id: str, routing_retired: bool = False):
    interp = load_yaml(path / "artifacts" / "verdict_interpretation.yaml")
    # `status` is the new altitude-aware field; fall back to `protocol_verdict` for old runs
    status = (interp.get("status") or interp.get("protocol_verdict") or "").strip().lower()
    campaign = load_campaign_state()

    # E-018 (2026-09-13): when pass_rule_evaluation.yaml carries a BINDING verdict,
    # its mechanical (hypothesis_verdict, lineage_routing) pair -- not the stage's
    # own restated `status` -- is what actually drives routing (see
    # _resolve_verdict_fields). The circuit breaker's family-history governance
    # must see that SAME mechanical status as its input, not the LLM's copy, so
    # translate it here via the inverse map before the breaker runs.
    pre_eval_path = path / "artifacts" / "pass_rule_evaluation.yaml"
    pre_eval = load_yaml(pre_eval_path) if pre_eval_path.exists() else {}
    pre_eval_binding = bool(pre_eval) and pre_eval.get("result") in ("PASS", "FAIL") \
        and pre_eval.get("discretion") != "stage"
    if pre_eval_binding:
        _mech_pair = (pre_eval.get("hypothesis_verdict"), pre_eval.get("lineage_routing"))
        _mech_status = _VERDICT_ROUTING_TO_LEGACY_STATUS.get(_mech_pair)
        if _mech_status is not None:
            status = _mech_status

    # F6 (2026-07-04): an engineering-failure diagnosis can NEVER be overridden into a
    # scientific verdict by the circuit breaker (or by anything else). Checked before
    # any breaker logic runs, using the LLM's own root_cause -- covers the case
    # where verdict_interpreter itself reaches an engineering diagnosis after a
    # full backtest (the signal_prescreen stage this once also guarded against
    # is removed, E-039 step 5).
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

    # Phase 1.4 (docs/CAMPAIGN_PROGRAM.md) / E-016 (2026-09-10 redesign): a
    # cost-dominated kill must answer "is there a cheap, timing-only variant
    # of this SAME signal worth trying?" (trade less often, combine nearby
    # trades, exit later, enter earlier); if yes, register the cheap variant
    # as a new idea. The earlier 5-option infra-level enum (maker-only
    # execution, lower-frequency variant, different product, venue tier,
    # batching) is superseded -- those are Jeremy's decisions to make
    # deliberately and holistically, not per-strategy pipeline suggestions
    # (see verdict_interpretation.schema.json's candidate_system enum and
    # workflow_artifacts/skills/verdict-interpreter/SKILL.md's IMPROVEMENT 10).
    # Unlike component_execution_error/regime_misattribution above, this does
    # not pause the pipeline -- it's a completeness gap in the autopsy, not
    # evidence the verdict itself is untrustworthy (regime_attribution, this
    # schema's only other "mandatory" root_cause-adjacent field, has no
    # code-side pause either -- it's enforced only at the prompt/skill level,
    # with no post-hoc check anywhere in this file). A print-level nudge,
    # mirroring the warning style (not the routing behavior) of the
    # component_execution_error/regime_misattribution blocks above, rather
    # than silently passing.
    if root_cause.get("mechanism_failure") == "signal_real_but_subscale_vs_costs" \
            and not root_cause.get("fee_reduction_assessment"):
        print("\n⚠️  Phase 1.4: root_cause.mechanism_failure = signal_real_but_subscale_vs_costs "
              "but root_cause.fee_reduction_assessment is missing.")
        print("   Mandatory: is there a cheap, timing-only variant of this same signal worth "
              "trying (trade_less_often, combine_nearby_trades, exit_later, enter_earlier)? "
              "If yes, register the cheap variant as a new idea and name it in "
              "fee_reduction_assessment.registered_as.")
    # --- end mechanism_failure routing ---

    # A8 (K2 kernel): resolve the two-field pair (preferring a BINDING
    # pass_rule_evaluation.yaml's mechanical pair, then the artifact's own
    # hypothesis_verdict/lineage_routing; legacy-status fallback + circuit-breaker
    # interaction documented in _resolve_verdict_fields).
    hypothesis_verdict, lineage_routing = _resolve_verdict_fields(
        interp, original_status, status, pre_eval=pre_eval if pre_eval_binding else None
    )

    # E-018 (2026-09-13): C7 downgraded from BLOCKING to INFORMATIONAL, and now
    # compares the STAGE'S OWN restated hypothesis_verdict/lineage_routing
    # (interp's own fields) against pass_rule_evaluation.yaml -- NOT the
    # already-resolved `hypothesis_verdict`/`lineage_routing` above, which when
    # pre_eval was binding now simply ARE the mechanical pair (comparing them
    # to themselves would find nothing). Called UNCONDITIONALLY, even when the
    # stage declared no hypothesis_verdict at all (`_own_hv is None`) --
    # _check_pass_rule_evaluation_conformance's own early-returns already
    # handle "pre_eval not binding" safely, and a binding pre_eval can only
    # arise from a K2-era (2026-07-13+) pre_registration.yaml, which is
    # exactly the era where verdict_interpreter's SKILL.md instructs the LLM
    # to declare these fields via B4 copy-through -- so an unexpected `None`
    # here on a binding run is itself the most useful signal this check can
    # produce (the LLM ignored the copy-through instruction entirely), not a
    # case to silently skip. A mismatch can no longer mean "routing might be
    # wrong" (routing already used the mechanical pair directly) -- it only
    # means the stage's own restated copy was wrong or absent, an
    # LLM-comprehension signal worth recording, not a reason to halt the
    # pipeline.
    _own_hv, _own_lr = interp.get("hypothesis_verdict"), interp.get("lineage_routing")
    _prc_violations = _check_pass_rule_evaluation_conformance(path, _own_hv, _own_lr)
    if _prc_violations:
        print("\n⚠️  [C7] Stage's own restated verdict disagreed with the binding "
              "pass_rule_evaluation.yaml (informational only -- routing already used "
              "the mechanical verdict directly):")
        for v in _prc_violations:
            print(f"   - {v}")
        update_state(path=path, flags={"pass_rule_evaluation_disagreement": True},
                     pass_rule_evaluation_violations=_prc_violations)

    # Short-circuit ordering UNCHANGED from pre-K2 behavior: promote and a
    # terminal kill (lineage_routing == "terminate") bypass carryover
    # generation / KB write / output verification / campaign-review-trigger,
    # exactly as the old status=="promote"/"kill" branches did.
    if hypothesis_verdict == "promote" or lineage_routing == "terminate":
        return _dispatch_verdict_route(path, run_id, interp, campaign, hypothesis_verdict, lineage_routing,
                                       routing_retired=routing_retired)

    # Auto-generate findings_carryover if missing (catches both normal and resume paths)
    _auto_generate_findings_carryover(path, interp, lineage_routing)

    # A5.1-5.3: update campaign KB with this run's verdict
    _write_kb_findings_entry(path, run_id, interp)

    # Verify verdict outputs before scaffolding the next run (not applied to terminal routes).
    # E-018: pass the MECHANICALLY-resolved lineage_routing when pre_eval was
    # binding, so this checks the artifacts the actual route requires rather
    # than whatever the stage's own (possibly-disagreeing) restatement says.
    violations = _verify_verdict_outputs(
        path, mechanical_lineage_routing=lineage_routing if pre_eval_binding else None
    )
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

    return _dispatch_verdict_route(path, run_id, interp, campaign, hypothesis_verdict, lineage_routing,
                                   routing_retired=routing_retired)


# legacy routing (v26 card G) -- under orchestrator.verdict_routing_retired only its
# first line runs (slice 6c S2b: _route_retired_campaign_review); the rest is flag-off only.
def determine_post_campaign_review_route(path: Path, run_id: str, routing_retired: bool = False) -> str:
    # Slice 6c S2b: run_loop passes its pre-flight reading of the flag. The
    # branch returns before anything below is loaded (verdict_interpretation.yaml
    # included) -- no legacy route, circuit breaker or child run.
    if routing_retired:
        return _route_retired_campaign_review(path, run_id)
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

        # E-018 (2026-09-13): same binding-pre_eval status override as
        # determine_post_verdict_route (R1 -- one shared rule, not a divergent copy).
        pre_eval_path = path / "artifacts" / "pass_rule_evaluation.yaml"
        pre_eval = load_yaml(pre_eval_path) if pre_eval_path.exists() else {}
        pre_eval_binding = bool(pre_eval) and pre_eval.get("result") in ("PASS", "FAIL") \
            and pre_eval.get("discretion") != "stage"
        if pre_eval_binding:
            _mech_pair = (pre_eval.get("hypothesis_verdict"), pre_eval.get("lineage_routing"))
            _mech_status = _VERDICT_ROUTING_TO_LEGACY_STATUS.get(_mech_pair)
            if _mech_status is not None:
                status = _mech_status

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
        hypothesis_verdict, lineage_routing = _resolve_verdict_fields(
            interp, original_status, status, pre_eval=pre_eval if pre_eval_binding else None
        )

        # C7: same informational (non-blocking) disagreement check as
        # determine_post_verdict_route (R1 -- one shared conformance rule, not a
        # divergent second copy) -- compares the STAGE'S OWN restated pair,
        # not the already-resolved one, called unconditionally. See E-018
        # (2026-09-13) note there for why an unexpected `None` hv/lr is itself
        # a signal worth checking, not a case to skip.
        _own_hv, _own_lr = interp.get("hypothesis_verdict"), interp.get("lineage_routing")
        _prc_violations = _check_pass_rule_evaluation_conformance(path, _own_hv, _own_lr)
        if _prc_violations:
            print("\n⚠️  [C7] Stage's own restated verdict disagreed with the binding "
                  "pass_rule_evaluation.yaml (informational only -- routing already used "
                  "the mechanical verdict directly):")
            for v in _prc_violations:
                print(f"   - {v}")
            update_state(path=path, flags={"pass_rule_evaluation_disagreement": True},
                         pass_rule_evaluation_violations=_prc_violations)

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


# E-056 1b block manifest (code-review fix 1): 1b's manifest is checked right
# after 1b, before innovation_expansion spends an LLM call on patches. One
# re-try of 1b carries the error; a second bad manifest fails the run.
_BLOCK_MANIFEST_RETRY_MAX = 1
_BLOCK_MANIFEST_RETRY_STATE_KEY = "block_manifest_retry"


def _block_manifest_error(path: Path):
    """None when artifacts/block_manifest.yaml exists and passes
    tools/block_manifest.check_manifest against the config in
    artifacts/backtest_spec.yaml (the same check 5a and the registry run);
    otherwise the error text."""
    _bm = _block_manifest_module()
    manifest_path = path / "artifacts" / _bm.MANIFEST_FILENAME
    spec_path = path / "artifacts" / "backtest_spec.yaml"
    try:
        spec = load_yaml(spec_path) if spec_path.exists() else None
        config = spec.get("config") if isinstance(spec, dict) else None
        if not isinstance(config, dict):
            return f"{spec_path} has no 'config' mapping to check the manifest against"
        manifest = _bm.load_manifest_file(manifest_path)
        if manifest is None:
            return (f"{manifest_path} is missing -- a spec_ready config needs its block manifest "
                    f"(STRATEGY_DESIGN_GUIDE.md §7c)")
        _bm.check_manifest(manifest, config, where=str(manifest_path))
    except _bm.BlockManifestError as exc:
        return str(exc)
    return None


def _route_block_manifest_check(path: Path) -> str:
    """spec_ready from 1b: innovation_expansion when the manifest is valid;
    otherwise back to strategy_config_authoring ONCE with the error (carried by
    _apply_block_manifest_retry_context); a second failure raises."""
    error = _block_manifest_error(path)
    state = load_yaml(path / "pipeline_state.yaml") or {}
    attempts = (state.get(_BLOCK_MANIFEST_RETRY_STATE_KEY) or {}).get("attempts", 0)
    if error is None:
        if attempts:
            update_state(path=path, **{_BLOCK_MANIFEST_RETRY_STATE_KEY: {"attempts": 0, "last_error": None}})
        return "innovation_expansion"
    if attempts >= _BLOCK_MANIFEST_RETRY_MAX:
        raise RuntimeError(
            f"strategy_config_authoring: block_manifest.yaml still invalid after "
            f"{attempts} retry -- {error}")
    update_state(path=path, **{_BLOCK_MANIFEST_RETRY_STATE_KEY: {
        "attempts": attempts + 1, "last_error": error}})
    print(f"🔁 [E-056 1b] block_manifest.yaml invalid -- retrying strategy_config_authoring "
          f"once with the error: {error}")
    return "strategy_config_authoring"


def _apply_block_manifest_retry_context(stage_name: str, handoff: dict, run_dir: Path) -> None:
    """Under config_direct_authoring, on a manifest retry of
    strategy_config_authoring, put the previous manifest error into that
    stage's handoff. Flag off, another stage, or no retry pending: no-op."""
    if stage_name != "strategy_config_authoring" or not _config_direct_authoring_enabled():
        return
    state_path = run_dir / "pipeline_state.yaml"
    state = (load_yaml(state_path) or {}) if state_path.exists() else {}
    retry = state.get(_BLOCK_MANIFEST_RETRY_STATE_KEY) or {}
    if not retry.get("attempts") or not retry.get("last_error"):
        return
    handoff.setdefault("injected_context", {})
    handoff["injected_context"]["block_manifest_error"] = (
        f"Retry {retry['attempts']}/{_BLOCK_MANIFEST_RETRY_MAX}. Your previous "
        f"block_manifest.yaml was rejected: {retry['last_error']}. Re-emit backtest_spec.yaml, "
        f"decision.yaml and a corrected block_manifest.yaml (STRATEGY_DESIGN_GUIDE.md §7c).")


def _clear_stale_block_manifest(stage_name: str, run_dir: Path) -> None:
    """Under config_direct_authoring, delete artifacts/block_manifest.yaml as
    strategy_config_authoring starts, so a 1b pass never inherits an earlier
    pass's (or idea's) manifest. Flag off or another stage: no-op."""
    if stage_name != "strategy_config_authoring" or not _config_direct_authoring_enabled():
        return
    stale = run_dir / "artifacts" / _block_manifest_module().MANIFEST_FILENAME
    if stale.exists():
        stale.unlink()
        print(f"[E-056 1b] removed stale {stale} before strategy_config_authoring")


def determine_post_strategy_config_authoring_route(path: Path, *, routing_retired: bool = False):
    """Routing for the new strategy_config_authoring stage (E-056 Slice 3b,
    config-direct authoring). Mirrors determine_post_spec_route's shape
    exactly -- same decision.yaml contract (status spec_ready|component_gap)
    -- but the success target is innovation_expansion, not protocol_execution:
    strategy_config_authoring runs BEFORE innovation_expansion in this flow
    (it authors the BASE config that innovation_expansion patches into
    variants), where backtest-engineering used to run AFTER it and pick one
    variant from an already-expanded menu.

    Slice 6c S2c: with routing_retired (run_loop passes it only when
    orchestrator.verdict_routing_retired is on), component_gap parks the run
    (waiting_for_component) instead of pausing the campaign; the rationale is
    appended to campaign_record/component_requests.yaml."""
    KNOWN_STATUSES = {"spec_ready", "component_gap"}
    decision = load_yaml(path / "artifacts" / "decision.yaml")
    status = decision.get("status", "").strip().lower()
    if status == "spec_ready":
        return _route_block_manifest_check(path)
    if status == "component_gap" and routing_retired:
        run_id = path.name
        reason = str(decision.get("rationale") or "component_gap (no rationale given)")
        _crr.append_component_requests(
            ROOT / _crr.COMPONENT_REQUESTS_REL,
            [{"run_id": run_id, "stage": "strategy_config_authoring", "variant_id": None,
              "reason": reason, "blocking_issues": decision.get("blocking_issues") or []}],
            unless=lambda r: (r.get("run_id") == run_id
                              and r.get("stage") == "strategy_config_authoring"
                              and r.get("reason") == reason))
        return _park_run(path, kind="component", stage="strategy_config_authoring",
                         reason=f"component_gap: {reason}",
                         request_refs=[f"runs/{run_id}/artifacts/decision.yaml",
                                       _crr.COMPONENT_REQUESTS_REL],
                         resume_stage="strategy_config_authoring")
    if status == "component_gap":
        update_state(path=path, status="paused_for_human")
        print("\n⏸️ COMPONENT GAP: hypothesis needs an engine piece that does not exist. "
              "See artifacts/decision.yaml; extend the engine per STRATEGY_EXTENDING.md, then resume.")
        return "human_pause"
    if status not in KNOWN_STATUSES:
        update_state(path=path, status="paused_for_human")
        print(f"\n⏸️ UNEXPECTED STATUS '{status}' from strategy_config_authoring — "
              f"SKILL.md may need a new status case, or this run had bad inputs. "
              f"Rationale: {decision.get('rationale', '<none>')}")
        return "human_pause"


# E-059 S2a: moved to tools/json_pointer.py (behaviour-preserving) so
# tools/decide_next.py applies a reader patch with the same semantics without
# importing this module. Re-exported under its old name: every
# `except PatchApplicationError` / `rpr.PatchApplicationError` keeps working.
# tools/ is already on sys.path (module top).
from json_pointer import PatchApplicationError  # noqa: E402


def _json_pointer_module():
    """tools/json_pointer.py (E-058 S2b), imported lazily like the other
    tools/ siblings."""
    _tools = str(Path(__file__).parent.parent / "tools")
    if _tools not in sys.path:
        sys.path.insert(0, _tools)
    import json_pointer as _jp
    return _jp


def _block_manifest_module():
    """tools/block_manifest.py (E-056 1b block manifest): the one implementation
    of the STRATEGY_DESIGN_GUIDE.md §7c contract, shared with
    tools/block_registry.py. Imported lazily like the other tools/ siblings."""
    _json_pointer_module()  # puts tools/ on sys.path
    import block_manifest as _bm
    return _bm


def _split_json_pointer(path: str) -> list:
    """RFC 6901 tokenization: '/' splits, '~1' -> '/' and '~0' -> '~' unescaped
    per segment. Raises PatchApplicationError on anything that isn't a
    non-empty string starting with '/'. Implementation: tools/json_pointer.py."""
    return _json_pointer_module().split_json_pointer(path, PatchApplicationError)


def _apply_json_pointer_patch(base_config: dict, patch: list) -> dict:
    """Apply a list of {path, value} JSON-Pointer (RFC 6901) set-operations to
    a DEEP COPY of base_config. Raises PatchApplicationError on any patch that
    cannot be applied cleanly. Implementation (moved, behaviour-preserving,
    E-059 S2a): tools/json_pointer.apply_json_pointer_patch, whose docstring
    states the exact set semantics."""
    return _json_pointer_module().apply_json_pointer_patch(base_config, patch)


def _json_pointer_exists(config, path: str) -> bool:
    """True iff the RFC 6901 pointer 'path' resolves inside config. Never
    raises -- an invalid pointer simply does not exist. Shared with
    tools/block_registry.py via tools/json_pointer.py (E-058 S2b)."""
    return _json_pointer_module().json_pointer_exists(config, path)


def _check_manifest_paths(variant_config: dict, manifest: dict) -> list:
    """Returns the manifest-declared block.config_paths (STRATEGY_DESIGN_GUIDE.md
    §7c) that do NOT resolve in variant_config; [] when the manifest has no
    block.config_paths list at all. Block paths only -- a variant may change
    scaffolding. The whole manifest is checked against the base config first,
    by tools/block_manifest.check_manifest (after 1b, and again in the
    backtest_specification tool stage). Implementation: tools/json_pointer.py."""
    return _json_pointer_module().manifest_missing_paths(variant_config, manifest)


def _route_post_config_direct_backtest_specification(run_dir: Path, *,
                                                     routing_retired: bool = False) -> str:
    """Routing for the config-direct-authoring flow's tool-only
    backtest_specification stage. By the time run_loop reaches this branch,
    run_tool_worker's own "backtest_specification" branch (below) has already
    applied variant_patches.yaml's patches to strategy_config_authoring's
    base config, validated each variant, and written
    artifacts/variants/index.yaml. Mirrors determine_post_spec_route's shape
    (spec_ready -> data_availability_gate/protocol_execution, component_gap
    -> human_pause) but reads the per-variant index instead of a single
    decision.yaml, since config-direct authoring produces N pursued variants
    per run, not one selected variant -- see S2_FINDINGS.md §7 on why
    _record_variant_selection's single-selected-variant model does not apply
    here.

    Slice 6c S2c: with routing_retired (passed by run_loop only when
    orchestrator.verdict_routing_retired is on), a "nothing validated" outcome
    whose blocking variants all failed ONLY on V12 cannot-load (a missing
    class) parks the run (waiting_for_component); any other failure stays the
    pause below."""
    # E-036 S2a: the 5a exact-match check, off by default (see
    # _gate_config_direct_variants). Flag off: None, nothing read. A repeat
    # variant is marked not_tested in index.yaml BEFORE it is read below; every
    # checked variant a repeat ends the run completed_no_new_hypothesis.
    _repeat_end = _gate_config_direct_variants(run_dir, run_dir.name)
    if _repeat_end is not None:
        return _repeat_end
    index = load_yaml(run_dir / "artifacts" / "variants" / "index.yaml") or {}
    variants = index.get("variants", {})
    if routing_retired:
        # The variants that block: every variant in the variant loop (none is
        # validated when this fires), only `base` otherwise.
        blocking = (variants if _variant_loop_enabled()
                    else ({"base": variants["base"]} if "base" in variants else {}))
        nothing_validated = not any(v.get("status") == "validated" for v in blocking.values())
        kind, classes = (_variant_park_kind(blocking, run_dir / "artifacts")
                          if nothing_validated else (None, []))
        if kind == "component":
            return _park_run(
                run_dir, kind="component", stage="backtest_specification",
                reason=f"no variant passed validation; missing class(es): {classes}",
                request_refs=[_crr.COMPONENT_REQUESTS_REL,
                              f"runs/{run_dir.name}/artifacts/variants/index.yaml"],
                resume_stage="backtest_specification", classes=classes)
    if _variant_loop_enabled():
        # E-033.1 Slice 4a: config-direct authoring produces N pursued
        # variants per run, not one selected variant -- widen the "is there
        # anything to test" check from "is base validated" to "is at least
        # one variant validated". No per-variant GATING decision here (that's
        # 4b's job, S1_FINDINGS.md §8) -- this only decides whether to
        # proceed at all.
        if not any(v.get("status") == "validated" for v in variants.values()):
            update_state(path=run_dir, status="paused_for_human")
            print(
                "\n⏸️ CONFIG-DIRECT AUTHORING: no variant passed validation. See "
                "artifacts/variants/index.yaml and "
                "campaign_record/component_requests.yaml."
            )
            return "human_pause"
    else:
        base = variants.get("base")
        if base is None or base.get("status") != "validated":
            update_state(path=run_dir, status="paused_for_human")
            print(
                "\n⏸️ CONFIG-DIRECT AUTHORING: the 'base' variant is missing or failed "
                "validation. See artifacts/variants/index.yaml and "
                "campaign_record/component_requests.yaml."
            )
            return "human_pause"
    if _data_availability_gate_enabled():
        return "data_availability_gate"
    return "protocol_execution"


def determine_post_spec_route(path: Path):
    KNOWN_STATUSES = {"spec_ready", "component_gap"}
    decision = load_yaml(path / "artifacts" / "decision.yaml")
    status = decision.get("status", "").strip().lower()
    if status == "spec_ready":
        # E-039 step 5 (2026-09-12): signal_prescreen removed -- "always
        # backtest" (E-039's own premise). A spec-ready hypothesis now goes
        # straight to protocol_execution; the E-054 data-availability gate
        # (routed to separately, when enabled) still runs first if that flag
        # is on -- see the backtest_specification branch in run_loop.
        return "protocol_execution"
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

def _stale_run_halt_flags(state: dict) -> dict:
    """E-061 C1.4 (fourth-round review fix 2): {flag: False} for each
    RUN_HALT_FLAGS entry still set on this state -- every un-pause path
    (run_campaign's --resume and --unpark, resume_pipeline) clears them, so a
    flag from an earlier halt never outranks a later, real classification.
    Empty when none is set (the state is then written exactly as before)."""
    flags = (state or {}).get("flags") or {}
    return {name: False for name in RUN_HALT_FLAGS if flags.get(name)}


def resume_pipeline(run_id: str):
    RUN_DIR = ROOT / "runs" / run_id
    state = load_yaml(RUN_DIR / "pipeline_state.yaml")
    if state.get("status") != "paused_for_human":
        print("Pipeline is not paused. Nothing to resume.")
        return

    resolution_path = RUN_DIR / "artifacts" / "human_resolution.yaml"
    ensure_files([resolution_path])

    resolution = load_yaml(resolution_path)
    _stale = _stale_run_halt_flags(state)  # E-061: an un-pause clears the halt flags
    if resolution.get("status") == "resolved_proceed":
        print("✅ Human resolution verified. Resuming pipeline...")
        # Inject the human's paths directly into the state so the next agent can see them
        update_state(
            path=RUN_DIR,
            status="active",
            current_stage="human_resolution",
            pending_stage="backtest_specification", # Move to Phase 2
            injected_human_context=resolution.get("injected_context"),
            **({"flags": _stale} if _stale else {})
        )
        run_loop(run_id)
    else:
        print("❌ Human marked issue as unresolvable. Ending run.")
        update_state(path=RUN_DIR, status="rejected", pending_stage="completed_rejected",
                     **({"flags": _stale} if _stale else {}))

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
        # C5.6: the flags are read only if a protocol is actually generated now.
        _ensure_protocol_from_constraints(RUN_DIR, run_id, _machine_constraints,
                                          promotion_retired=_promotion_retired_enabled)
        _ensure_protocol_ref_pinned(RUN_DIR, run_id, _machine_constraints)

    # E-046a Slice 5b-ii-B: resolve the specialist_readers flag ONCE per run_loop,
    # up front, inside a try (code-review fix 9): a flag set on without its
    # grid_evaluation/category_reports dependencies, or a non-menu-shaped
    # pass_rule under the flag (fix 6), stops the run with status=failed before
    # any stage spends anything, instead of escaping run_loop.
    _TERMINAL_AT_START = ("completed", "rejected", "human_pause", "failed_validation")
    _pending_at_start = state.get("pending_stage") or ""
    try:
        _sr_flag = _specialist_readers_enabled()
        if _sr_flag and _pending_at_start and not _pending_at_start.startswith(_TERMINAL_AT_START):
            # E-059 S2a (operator decision 2): a decide_next candidate's pass_rule
            # is written by 1a, so the check runs right after 1a instead
            # (_write_pass_rule_from_card), still before any backtest.
            if not _specialist_readers_preflight_deferred(RUN_DIR, _pending_at_start):
                _check_specialist_readers_preflight(RUN_DIR)
    except Exception as e:
        print(f"❌ specialist_readers pre-flight failed: {e}")
        update_state(path=RUN_DIR, status="failed", last_error=str(e))
        return
    # E-058 S2a: the regroup_record flag, resolved ONCE the same way (its
    # dependency on specialist_readers fails the run here, before any spend).
    # A run already at a terminal stage is skipped, like the specialist_readers
    # pre-flight: it will not reach any stage, so a misconfiguration must not
    # overwrite its finished status with "failed".
    _rr_flag = False
    try:
        if _pending_at_start and not _pending_at_start.startswith(_TERMINAL_AT_START):
            _rr_flag = _regroup_record_enabled()
    except Exception as e:
        print(f"❌ regroup_record pre-flight failed: {e}")
        update_state(path=RUN_DIR, status="failed", last_error=str(e))
        return
    # Branch 3 on every backtest: resolved ONCE the same way, so its dependency on
    # profit_bars_file (or a non-bool value) fails the run here, before any spend.
    _pbe_flag = False
    try:
        if _pending_at_start and not _pending_at_start.startswith(_TERMINAL_AT_START):
            _pbe_flag = _profit_bars_every_backtest_enabled()
    except Exception as e:
        print(f"❌ profit_bars_every_backtest pre-flight failed: {e}")
        update_state(path=RUN_DIR, status="failed", last_error=str(e))
        return
    # Slice 6c S2a: verdict routing retired, resolved ONCE the same way (its
    # dependencies on decide_next and profit_bars_every_backtest, or a non-bool
    # value, fail the run here, before any spend).
    _vrr_flag = False
    try:
        if _pending_at_start and not _pending_at_start.startswith(_TERMINAL_AT_START):
            _vrr_flag = _verdict_routing_retired_enabled()
    except Exception as e:
        print(f"❌ verdict_routing_retired pre-flight failed: {e}")
        update_state(path=RUN_DIR, status="failed", last_error=str(e))
        return
    # Slice 6c S2c: a parked run is restarted only through run_campaign.py
    # --unpark, which clears the marker after its checks. A run still carrying
    # the marker here was restarted by hand: stop loudly before any spend, so a
    # stale marker can never make a LATER, unrelated pause read as a park.
    if _vrr_flag and state.get(PARKED_KEY):
        _msg = (f"{run_id} is parked ({PARKED_KEY}: waiting_for_"
                f"{(state.get(PARKED_KEY) or {}).get('kind')}) but was restarted without "
                f"run_campaign.py --unpark. Restore status paused_for_human and the queue "
                f"entry's paused:waiting_for_<kind>, then --unpark (docs/RUNBOOK.md §4); or set "
                f"{PARKED_KEY}: null by hand, which skips the unpark checks.")
        print(f"❌ {_msg}")
        update_state(path=RUN_DIR, status="failed", last_error=_msg)
        return

    while True:
        current_stage = state.get("pending_stage")
         
        TERMINAL_PREFIXES = ("completed", "rejected", "human_pause", "failed_validation")
        if not current_stage or current_stage.startswith(TERMINAL_PREFIXES):
            print(f"🏁 Pipeline finished. Final state: {current_stage}")
            break

        # --- TOKEN CIRCUIT BREAKER (F4c: weighted units, not raw token sum) ---
        budget = _load_token_budget()
        total_weighted_used, stage_breakdown = _compute_weighted_budget_usage(state.get("audit_log", {}))

        # E-058 S2a: regroup_record is exempt. It is a zero-cost tool stage
        # carrying the grid route that flag-off runs take in the SAME iteration
        # as specialist_readers (after this check); stopping it here would leave
        # a run with no memory entry and no route. The next stage is checked as
        # usual. Every other stage: unchanged.
        if total_weighted_used > budget and current_stage != "regroup_record":
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
        # E-061 C1.2: under config-direct authoring 5a / the data gate /
        # protocol_execution / verdict_interpreter load their own handoff,
        # rebuilt here from the current flags at every entry.
        handoff_path = (_config_direct_handoff_path(current_stage, run_id, RUN_DIR, rebuild=True)
                        or handoff_path)
        if current_stage == "specialist_readers":
            # E-046a Slice 5b-ii-B: created lazily at stage entry, so flag-off
            # runs never get this file.
            _ensure_specialist_readers_handoff(run_id, RUN_DIR)
        elif current_stage == "regroup_record":
            # E-058 S2a: a run routed here while the flag was on, resumed with it
            # off, stops loudly instead of skipping the record or guessing a route.
            if not _rr_flag:
                _msg = ("regroup_record is unreached with orchestrator.regroup_record.enabled "
                        "off -- this run was routed here while the flag was on. Reset "
                        "pending_stage to specialist_readers (or switch the flag on) and resume.")
                print(f"❌ {_msg}")
                update_state(path=RUN_DIR, status="failed", last_error=_msg)
                break
            _ensure_regroup_record_handoff(run_id, RUN_DIR)
        elif current_stage == "holdout_evaluation" and _vrr_flag:
            # Slice 6c S2a: under the flag nothing routes here, and the operator
            # decision of 2026-09-25 allows the holdout ONLY through the branch-3
            # profit_bars_reached stop plus an operator unlock (S2d below).
            # Code review item 1: a run found here WITH holdout_result.yaml
            # already spent the seal by hand -- only the record step runs
            # (_record_spent_holdout), so the spend is never left unrecorded.
            # Without it: a classified pause (HOLDOUT_REFUSED_FLAG), no gate runs.
            if _spend_unlock_for(state, run_id):
                # Slice 6c S2d: the operator's spend, bound to this run's stop,
                # unlocked it (_unlocked_holdout_evaluation: re-check, then the
                # manual backtest; once a result exists, record first). Without
                # a valid unlock a result is only recorded, never promoted
                # (_record_spent_holdout, review fix 3).
                try:
                    _terminal = _unlocked_holdout_evaluation(RUN_DIR, run_id, state)
                except Exception as e:
                    print(f"❌ Error in the unlocked holdout_evaluation: {e}")
                    update_state(path=RUN_DIR, status="failed", last_error=str(e))
                    break
                if _terminal == "human_pause":
                    update_state(path=RUN_DIR, status="paused_for_human")
                    break
                update_state(path=RUN_DIR,
                             status="active" if _terminal != "completed_rejected" else "rejected",
                             completed_stages=(state.get("completed_stages") or [])
                             + ["holdout_evaluation"],
                             current_stage="holdout_evaluation", pending_stage=_terminal)
                state = load_yaml(STATE_FILE)
                continue
            if (ARTIFACTS / "holdout_result.yaml").exists():
                try:
                    _terminal = _record_spent_holdout(RUN_DIR, run_id)
                except Exception as e:
                    print(f"❌ Error recording the spent holdout: {e}")
                    update_state(path=RUN_DIR, status="failed", last_error=str(e))
                    break
                if _terminal == "human_pause":
                    update_state(path=RUN_DIR, status="paused_for_human")
                    break
                update_state(path=RUN_DIR,
                             status="active" if _terminal != "completed_rejected" else "rejected",
                             completed_stages=(state.get("completed_stages") or [])
                             + ["holdout_evaluation"],
                             current_stage="holdout_evaluation", pending_stage=_terminal)
                state = load_yaml(STATE_FILE)
                continue
            print("⏸️  holdout_evaluation is refused under orchestrator.verdict_routing_retired."
                  "enabled: the holdout is reached only through the profit_bars_reached stop "
                  f"plus an operator spend in artifacts/{HOLDOUT_DECISION_FILE} (slice 6c S2d), "
                  "and this run carries no such unlock. Nothing was spent. "
                  f"See docs/RUNBOOK.md §3 ({HOLDOUT_REFUSED_FLAG}).")
            update_state(path=RUN_DIR, status="paused_for_human",
                         flags={HOLDOUT_REFUSED_FLAG: True})
            break
        elif (current_stage == "campaign_review" and not _vrr_flag
              and state.get(CAMPAIGN_REVIEW_TRIGGER_KEY)):
            # Slice 6c S2b review fix 3, mirroring the regroup_record guard: a
            # review the flag's trigger started, resumed with the flag off, stops
            # loudly -- the legacy route must never act on it. Flag-off runs never
            # carry the marker, so they never reach this branch.
            _msg = ("campaign_review was triggered under orchestrator.verdict_routing_retired."
                    "enabled (pipeline_state.yaml carries campaign_review_trigger), but the flag "
                    "is now off -- the legacy route must not act on it. Switch the flag back on "
                    "and resume (RUNBOOK §3, campaign_review_terminate row).")
            print(f"❌ {_msg}")
            update_state(path=RUN_DIR, status="failed", last_error=_msg)
            break
        elif (current_stage == "campaign_review" and _vrr_flag
              and not state.get(CAMPAIGN_REVIEW_TRIGGER_KEY)):
            # Slice 6c S2a guard, relaxed in slice 6c S2b (the one refusal for this
            # stage): a review the memory-count trigger started under the flag
            # (_retired_review_route) carries CAMPAIGN_REVIEW_TRIGGER_KEY and runs.
            # Any other run found here -- a legacy review left over from before the
            # flag -- pauses BEFORE the LLM call, so it spends nothing.
            print("⏸️  campaign_review was reached without the memory-count trigger under "
                  "orchestrator.verdict_routing_retired.enabled (a legacy review); its route is "
                  "legacy verdict routing (v26 card G). "
                  f"See docs/RUNBOOK.md §3 ({CAMPAIGN_REVIEW_REFUSED_FLAG}).")
            update_state(path=RUN_DIR, status="paused_for_human",
                         flags={CAMPAIGN_REVIEW_REFUSED_FLAG: True})
            break



        # 1. Verify required inputs exist before invoking the agent
        handoff_data = load_yaml(handoff_path)
        required_input_paths = [RUN_DIR / x["path"] for x in handoff_data.get("required_inputs", [])]
        ensure_files(required_input_paths)

        # 2. Update state to running
        # E-030 S1.5 Piece 2: stage_attempts[current_stage] counts literal entries of
        # THIS stage, independent of counters.refinements_used (the refinement-BUDGET
        # gate -- RUNBOOK.md section 4.5 explicitly forbids hand-bumping that counter
        # to fix the audit-log overwrite below, since it would falsely consume real
        # refinement budget). Read BEFORE incrementing so the value used for THIS
        # attempt's audit-log key matches today's behavior on first entry (0, same as
        # refinements_used's own default) and every normal (non-crash) refinement
        # cycle re-entry (both counters increment by exactly 1 per legitimate re-entry,
        # so the two stay numerically identical on the tested, non-crash path -- they
        # diverge only on a genuine crash-resume, where refinements_used stays put but
        # this counter still advances, giving the re-attempt its own key instead of
        # overwriting the first attempt's audit_log entry).
        _stage_attempts = dict(state.get("stage_attempts") or {})
        _this_stage_attempt = _stage_attempts.get(current_stage, 0)
        _stage_attempts[current_stage] = _this_stage_attempt + 1
        state["stage_attempts"] = _stage_attempts
        update_state(path=RUN_DIR, current_stage=current_stage, status="running",
                     stage_attempts=_stage_attempts)

        _brief_exhausted = False  # E-059 S2b: set only by hypothesis_generation below
        _brief_no_new = False  # E-059 S2b review fix 1: likewise
        try:
            # E-046a Slice 5b-ii-B: under the flag verdict_interpreter is never
            # invoked. A run already routed there before the flag was switched on
            # stops here instead of spending the LLM call.
            if current_stage == "verdict_interpreter" and _sr_flag:
                raise RuntimeError(
                    "verdict_interpreter is unreached under "
                    "orchestrator.specialist_readers.enabled -- this run was routed here "
                    "before the flag was switched on. Reset pending_stage to "
                    "specialist_readers (or switch the flag off) and resume.")

            # 3. Inject dynamic state directly into the run's existing handoff file
            handoff_data["run_id"] = state.get("run_id", run_id)

            # Create or overwrite the injected_context block with the latest dynamic info from the state (like counters or human context)
            handoff_data["injected_context"] = {
                # E-030 S1.5 Piece 2: per-stage entry counter, NOT the refinement-cycle
                # counter below -- see the increment comment above for why they
                # coincide on the non-crash path. Consumed only by the two audit_log
                # key-building sites (run_claude_worker/run_gemini_worker); nothing
                # else reads this key.
                "stage_attempt": str(_this_stage_attempt),
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
                    # E-061 C1.2: the handoff this stage loads (config-direct: its own).
                    _vi_handoff = handoff_path
                    _inject_regime_context_into_handoff(_vi_handoff, _regime_rpt, _regime_aud, run_id)

                    # E-039 step 3 (2026-09-11): surface the real post-backtest
                    # route as context, never a gate -- see the function's own
                    # docstring. No-ops when protocol_result.yaml is absent
                    # (a prescreen-kill run that never reached a real backtest).
                    _protocol_result_path = RUN_DIR / "artifacts" / "protocol_result.yaml"
                    _protocol_result = (load_yaml(_protocol_result_path)
                                        if _protocol_result_path.exists() else None)
                    _inject_post_backtest_route_into_handoff(_vi_handoff, _protocol_result, run_id)

            # Invoke the Agent (F4b: one bounded YAML-repair retry on failure)
            expected_outputs = [RUN_DIR / "artifacts" / x for x in handoff_data.get("deliverables", [])]
            # E-061 C1.2: step 2's config-direct deliverable, checked in memory only.
            expected_outputs += [RUN_DIR / "artifacts" / x
                                 for x in _config_direct_step2_deliverables(current_stage)
                                 if x not in handoff_data.get("deliverables", [])]
            # E-061 C1.2: clear this stage's config-direct outputs, so only what this
            # attempt writes can satisfy the check after it. Flag off: no-op.
            _clear_config_direct_attempt_outputs(current_stage, RUN_DIR, _this_stage_attempt)
            # E-060 S3b: a composition run's 1a / 1b / step 2 are code, never an
            # LLM call (only under orchestrator.composition_runs; raises when a
            # composition brief meets the flag off).
            _comp_mode = (current_stage in _COMPOSITION_CODE_STAGES
                          and _composition_mode(RUN_DIR))
            if current_stage == "specialist_readers":
                # E-046a Slice 5b-ii-B: five reader calls, each through
                # run_reader_worker (explicit output path), never through
                # _invoke_agent_with_yaml_retry/_SKILL_MAP.
                _run_specialist_readers_stage(run_id, RUN_DIR, _this_stage_attempt)
            elif current_stage == "regroup_record":
                # E-058 S2a: tool stage, no LLM call, no _SKILL_MAP entry. Its
                # component-error / idea_status checks are reused by the route below.
                _rr_checks = _run_regroup_record_stage(run_id, RUN_DIR,
                                                       profit_bars_evaluated=_pbe_flag)
            elif _comp_mode:
                _run_composition_code_stage(current_stage, run_id, RUN_DIR, _sr_flag)
            elif not _skip_agent:
                if current_stage == "hypothesis_generation":
                    _split = False
                    try:
                        _invoke_agent_with_yaml_retry(current_stage, run_id, RUN_DIR, expected_outputs, state)
                    except FileNotFoundError:
                        if _handle_hypothesis_generation_multi_card_split(run_id, RUN_DIR):
                            _split = True
                        # E-059 S2b: no card + brief_status.yaml exhausted (flag on,
                        # brief run only) is a valid 1a outcome. Flag off: False, raise.
                        elif _brief_exhausted_signal(RUN_DIR):
                            _brief_exhausted = True
                        else:
                            raise
                    if not _brief_exhausted:
                        # E-059 S2b: an exhausted signal next to a card raises; so does
                        # an ambiguous single-card output (review fix 8). Both no-ops
                        # without a brief context / with the flag off.
                        _brief_exhausted_signal(RUN_DIR)
                        if not _split:
                            _brief_single_card_check(RUN_DIR)
                        # E-059 S2b review fix 1: a card this brief already produced
                        # ends the run before 1b (no-op for any other run).
                        _brief_no_new = _brief_card_is_repeat(RUN_DIR)
                        if not _brief_no_new:
                            # E-059 S2a (operator decision 2): no-op unless pre_registration.yaml
                            # is pending at 1a; raises (-> status failed) before any spend.
                            if (not _write_pass_rule_from_card(RUN_DIR, run_id, _sr_flag)
                                    and _composition_runs_enabled()):
                                # E-060 S2: a pass_rule 1a wrote itself gets the same
                                # code-added residual_ic, still before any spend.
                                _ensure_residual_ic_in_pre_registration(RUN_DIR)
                else:
                    _invoke_agent_with_yaml_retry(current_stage, run_id, RUN_DIR, expected_outputs, state)
            else:
                ensure_files(expected_outputs)
            # E-061 C1.2: the config-direct outputs this attempt had to write (step 2,
            # 5a, the variant-loop gate). Flag off / other stages: no-op.
            _check_config_direct_attempt_outputs(current_stage, RUN_DIR)

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

            # E-056 Slice 3b: config-direct authoring inserts strategy_config_authoring
            # between hypothesis_generation and innovation_expansion. Flag off: next_stage
            # stays config["default_next"] ('innovation_expansion'), untouched. A separate
            # `if`, not folded into the elif chain below, since current_stage can never be
            # both "hypothesis_generation" and "validation"/etc. at once.
            if current_stage == "hypothesis_generation" and _config_direct_authoring_enabled():
                next_stage = "strategy_config_authoring"
            # E-059 S2b: 1a reported the brief exhausted and wrote no card -> terminal.
            if current_stage == "hypothesis_generation" and _brief_exhausted:
                next_stage = BRIEF_EXHAUSTED_STAGE
            elif current_stage == "hypothesis_generation" and _brief_no_new:
                next_stage = NO_NEW_HYPOTHESIS_STAGE

            # E-046a Slice 5b-ii-B: under specialist_readers, protocol_execution's
            # default_next (verdict_interpreter) is redirected -- verdict_interpreter
            # becomes unreached, not deleted (same pattern as validation under
            # config-direct authoring). The protocol_execution branches below can
            # still override this with human_pause on a conformance violation.
            if current_stage == "protocol_execution" and _sr_flag:
                next_stage = "specialist_readers"

            if current_stage == "validation":
                next_stage = determine_post_validation_route(RUN_DIR) # Used to trigger state of refinement until (Artifact State is validated OR max refinement reached OR rejected)
                # E-039 S4: a "refine" verdict can now itself resolve to
                # "human_pause" (determine_post_refinement_route, folded in
                # above) -- same break-and-stop as every other human-in-the-
                # loop pause below, since "refinement_planner" no longer
                # exists as its own stage to catch this.
                if next_stage == "human_pause":
                    break # Break the while loop to stop the script cleanly

            elif current_stage == "strategy_config_authoring" and _comp_mode:
                # E-060 S3b: no block manifest to check (a composite is never a
                # block); the base config was checked against the composition
                # manifest inside the code stage.
                next_stage = "innovation_expansion"

            elif current_stage == "strategy_config_authoring":
                # E-056 Slice 3b: only reached when config_direct_authoring is on --
                # nothing routes here otherwise (see the override above and
                # STAGE_CONFIGS's own registration comment).
                # Slice 6c S2c: the kwarg only when on, so the flag-off call is unchanged.
                next_stage = determine_post_strategy_config_authoring_route(
                    RUN_DIR, **({"routing_retired": True} if _vrr_flag else {}))
                if next_stage == "human_pause":
                    break

            elif current_stage == "innovation_expansion" and _comp_mode:
                # E-060 S3b: the variants are code-written; no novelty gate (a
                # composite is not a new idea) -- straight to the tool-only 5a.
                next_stage = "backtest_specification"

            elif current_stage == "innovation_expansion":
                # E-036 S2a retired E-032 S2c's anti-adjacency retry here (it fired
                # before any config existed; see the retirement note above
                # _record_variant_selection): next_stage stays config["default_next"]
                # ('validation'), exactly what the flag-off route returned.
                # E-056 Slice 3b: under config-direct authoring, the validation stage
                # becomes naturally unreached (not deleted) -- redirect straight to the
                # tool-only backtest_specification stage instead.
                if next_stage == "validation" and _config_direct_authoring_enabled():
                    next_stage = "backtest_specification"

            elif current_stage == "backtest_specification" and _config_direct_authoring_enabled():
                # E-056 Slice 3b: tool-only path. run_tool_worker's own
                # "backtest_specification" branch (via async_invoke_agent's tool_stages,
                # see above) already applied variant_patches.yaml's patches, validated
                # each variant, and wrote artifacts/variants/index.yaml -- this only
                # decides where to route next.
                next_stage = _route_post_config_direct_backtest_specification(
                    RUN_DIR, **({"routing_retired": True} if _vrr_flag else {}))
                if next_stage == "human_pause":
                    break

            elif current_stage == "backtest_specification":
                next_stage = determine_post_spec_route(RUN_DIR)
                if next_stage == "protocol_execution":
                    # E-034 S2: record which expanded_variants menu entry was
                    # chosen (and persist the discards), off by default (see
                    # _record_variant_selection's own docstring). Runs only on
                    # the spec_ready path -- component_gap means no
                    # config/variant was actually implemented, so there is
                    # nothing to record.
                    _record_variant_selection(RUN_DIR)
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
                    # E-034 S3 / E-036 S2a: the exact-match repeat check on the
                    # CHOSEN VARIANT, off by default (see
                    # _route_post_variant_selection's own docstring). Called
                    # after the file above is written -- it is the config
                    # protocol_execution runs and hashes into the trial row
                    # (F4d's injection included) -- and before any
                    # config-schema work. Flag off: returns None immediately.
                    _variant_gate_next = _route_post_variant_selection(RUN_DIR, run_id)
                    if _variant_gate_next == "human_pause":
                        next_stage = "human_pause"
                        break
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
                        # Create handoff files for the remaining pipeline stages
                        _create_remaining_handoffs(run_id, RUN_DIR)
                        # E-054 Layer 2 (on by default -- see
                        # _data_availability_gate_enabled()): route through
                        # the data-availability gate FIRST. Explicit
                        # config-off leaves next_stage exactly what
                        # determine_post_spec_route returned above
                        # (protocol_execution), byte-identical to every
                        # pre-E-054 run and to the old unset-env-var default.
                        if _data_availability_gate_enabled():
                            next_stage = "data_availability_gate"
                        # CODE-REVIEW FIX (2026-09-21): this message used to
                        # print unconditionally, before the gate-routing check
                        # above existed, and named protocol_execution as the
                        # advance target even on the now-common path where
                        # next_stage was just set to data_availability_gate
                        # instead -- misleading anyone reading the log/console
                        # to understand what actually runs next.
                        print(f"✅ config schema-valid; advancing to {next_stage}")
                elif next_stage == "human_pause":
                    break

            elif current_stage == "data_availability_gate" and _variant_loop_enabled():
                # E-033.1 Slice 4b: route on how many variants remain
                # "validated" in artifacts/variants/index.yaml AFTER
                # run_tool_worker's per-variant data_availability_gate loop
                # has already marked any refine/decline variant not_tested
                # (that loop's own campaign_record/data_requests.yaml has the
                # per-variant detail). Per the operator's 2026-09-22 decision
                # (S1_FINDINGS.md "Decision" section) and the S1 §8
                # idea_status-collision note: fewer than 3 remaining variants
                # is a PRECONDITION failure that happens before the grid ever
                # runs -- it must NOT write to idea_status (that field
                # already means something different: the criteria-grid's own
                # validated/refuted/inconclusive rollup, written by
                # _build_idea_status_artifact AFTER backtests complete, a
                # later and unrelated stage). Uses a distinct flag,
                # pipeline_state.flags.variant_gate_insufficient, with its
                # own _classify_human_pause/_PAUSE_FLAG_TO_REASON entries in
                # run_campaign.py.
                index = load_yaml(ARTIFACTS / "variants" / "index.yaml") or {}
                variants_idx = index.get("variants", {})
                remaining = [vid for vid, v in variants_idx.items() if v.get("status") == "validated"]
                # E-036 S2a: variants the exact-match gate skipped as repeats
                # are not a shortfall. Only non-repeat variants count: when
                # repeats alone shrink the set below 3, every remaining
                # non-repeat variant proceeds; a data decline among them still
                # pauses/parks exactly as before. No repeat skip: min_needed
                # stays 3 (byte-identical).
                _n_repeat = sum(1 for v in variants_idx.values() if _is_repeat_skip(v))
                _min_needed = max(1, min(3, len(variants_idx) - _n_repeat)) if _n_repeat else 3
                # Slice 6c S2c: under verdict_routing_retired, a shortfall whose
                # not_tested variants all wait on data (or a missing class) parks
                # the run; --unpark restarts it at backtest_specification, which
                # rebuilds index.yaml before the gate runs again. No sticky flag.
                _park_kind, _park_classes = ((_variant_park_kind(variants_idx, ARTIFACTS)
                                              if _vrr_flag and len(remaining) < _min_needed
                                              else (None, [])))
                if _park_kind:
                    _refs = ["campaign_record/data_requests.yaml",
                             f"runs/{run_id}/artifacts/variants/index.yaml"]
                    if _park_kind == "component":
                        _refs.insert(0, _crr.COMPONENT_REQUESTS_REL)
                    next_stage = _park_run(
                        RUN_DIR, kind=_park_kind, stage="data_availability_gate",
                        reason=(f"only {len(remaining)}/{len(variants_idx)} variant(s) remain "
                                f"validated after the per-variant data-availability gate "
                                f"(need >= {_min_needed})"
                                + (f"; missing class(es): {_park_classes}"
                                   if _park_classes else "")),
                        request_refs=_refs, resume_stage="backtest_specification",
                        classes=_park_classes)
                    break
                if len(remaining) < _min_needed:
                    print(f"⏸️  PIPELINE PAUSED: only {len(remaining)}/{len(variants_idx)} "
                          "variant(s) remain validated after the per-variant "
                          f"data-availability gate (need >= {_min_needed}). See "
                          "artifacts/variants/index.yaml and "
                          "campaign_record/data_requests.yaml.")
                    update_state(path=RUN_DIR, status="paused_for_human",
                                 flags={"variant_gate_insufficient": True})
                    next_stage = "human_pause"
                    break
                print(f"✅ data_availability_gate (variant loop): {len(remaining)}/"
                      f"{len(variants_idx)} variant(s) remain validated — advancing to "
                      "protocol_execution.")
                next_stage = "protocol_execution"

            elif current_stage == "data_availability_gate":
                # E-054 Layer 2: route on validate/refine/decline. This branch
                # only runs when _data_availability_gate_enabled() routed
                # here in the first place -- see the backtest_specification
                # branch above.
                gate = load_yaml(ARTIFACTS / "data_availability_gate.yaml") or {}
                gate_outcome = gate.get("outcome", "decline")
                if _vrr_flag and _gate_shortfall_fetchable(gate):
                    # Slice 6c S2c (guess 7, card J; review fix 5): a decline whose
                    # shortfall a fetch can close parks the run (waiting_for_data)
                    # instead of rejecting it; the gate re-runs on --unpark. A
                    # refine, and a decline no fetch can close (sealed window,
                    # reserved or unbuilt feed, before listing, a fetch error),
                    # keep the previous behaviour below.
                    _reasons = list(gate.get("reasons") or [])
                    _append_data_requests(run_id, [{
                        "variant_id": None, "outcome": gate["outcome"],
                        "reason": (f"data_availability_gate outcome={gate['outcome']}: "
                                   + "; ".join(str(r) for r in _reasons[:10])),
                        "reasons": _reasons}], dedupe=True)
                    next_stage = _park_run(
                        RUN_DIR, kind="data", stage="data_availability_gate",
                        reason=(f"data_availability_gate outcome={gate['outcome']}: "
                                + "; ".join(str(r) for r in _reasons[:3])),
                        request_refs=[f"runs/{run_id}/artifacts/data_availability_gate.yaml",
                                      "campaign_record/data_requests.yaml"],
                        resume_stage="data_availability_gate")
                    break
                if gate_outcome == "validate":
                    print("✅ E-054 Layer 2: VALIDATE — advancing to protocol_execution.")
                    next_stage = "protocol_execution"
                elif gate_outcome == "refine":
                    # Mirrors this orchestrator's own documented HITL design
                    # ("Path C: Data Block" in the module docstring) -- a
                    # partial data problem is exactly what that pause path
                    # was built for: a human decides how to narrow the
                    # variant (drop a window, drop a feed), not the pipeline.
                    print("⏸️  PIPELINE PAUSED: E-054 Layer 2 says REFINE — "
                          "some data is only partially available. Review "
                          "artifacts/data_availability_gate.yaml, narrow the "
                          "variant (drop the listed window(s)/feed), then "
                          "write artifacts/human_resolution.yaml and resume.")
                    for reason in gate.get("reasons", [])[:10]:
                        print(f"   - {reason}")
                    update_state(path=RUN_DIR, status="paused_for_human")
                    next_stage = "human_pause"
                    break
                else:  # decline
                    print(f"🛑 E-054 Layer 2: DECLINE — required data does not exist. "
                          f"Rejecting hypothesis without spending a real backtest.")
                    for reason in gate.get("reasons", [])[:10]:
                        print(f"   - {reason}")
                    next_stage = "completed_rejected"

            elif current_stage == "protocol_execution" and _variant_loop_enabled():
                # E-033.1 Slice 4b (S1_FINDINGS.md §3b): the per-variant
                # conformance loop -- a SEPARATE restructure from Slice 4a's
                # own protocol_execution backtest loop (run_tool_worker, a
                # different function/branch entirely; this one is run_loop's
                # own elif branch, one level up). Reads each variant's OWN
                # artifacts/variants/<variant_id>/protocol_result.yaml
                # (written by Slice 4a's loop), calls the UNCHANGED, pure
                # _check_protocol_execution_conformance once per variant, and
                # on a violation invalidates ONLY that variant's own trial
                # row via its compound trial_id (f"{run_id}:{variant_id}",
                # Slice 4a's Decision A) -- per the operator's per-variant-
                # control decision, a violation on one variant must not
                # affect sibling variants' trial rows.
                # _mark_trial_invalidated's own signature was already
                # renamed run_id->trial_id in Slice 4a (Decision A) precisely
                # for this call site, which 4a's own final report flagged as
                # intentionally left unmigrated (still passing a bare
                # run_id) for 4b to finish -- this is that finish.
                _constraints = _load_machine_constraints(RUN_DIR)
                _all_violations: dict = {}
                if _constraints:
                    _variants_dir = ARTIFACTS / "variants"
                    if _variants_dir.exists():
                        for _vdir in sorted(p for p in _variants_dir.iterdir() if p.is_dir()):
                            _vpr_path = _vdir / "protocol_result.yaml"
                            if not _vpr_path.exists():
                                continue
                            _variant_id = _vdir.name
                            _pr = load_yaml(_vpr_path) or {}
                            _protocol_obj = {}
                            _protocol_path_str = _pr.get("protocol_file")
                            if _protocol_path_str:
                                _candidate = Path(_protocol_path_str)
                                if not _candidate.is_absolute():
                                    _candidate = ROOT / _candidate
                                if _candidate.exists():
                                    with open(_candidate, encoding="utf-8") as f:
                                        _protocol_obj = json.load(f)
                            _violations = _check_protocol_execution_conformance(_pr, _constraints, _protocol_obj)
                            if _violations:
                                _trial_id = f"{run_id}:{_variant_id}"
                                print(f"\n🛑 [F4d] PRE-REGISTRATION CONFORMANCE VIOLATION — variant "
                                      f"'{_variant_id}' did NOT test what was pre-registered:")
                                for v in _violations:
                                    print(f"   - {v}")
                                _mark_trial_invalidated(_trial_id, "; ".join(_violations))
                                _all_violations[_variant_id] = _violations
                if _all_violations:
                    update_state(path=RUN_DIR, status="paused_for_human",
                                 flags={"conformance_violation": True},
                                 conformance_violations=_all_violations)
                    next_stage = "human_pause"

            elif current_stage == "protocol_execution":
                # E-039 step 5 (2026-09-12): pre-registration conformance gate,
                # relocated from the removed signal_prescreen stage's own
                # F4d check (see _check_protocol_execution_conformance's
                # docstring for why this risk doesn't disappear along with
                # prescreen). default_next ("verdict_interpreter") is left
                # untouched on conformance -- this branch only ever PAUSES on
                # a real violation, never advances early.
                _pr_path = ARTIFACTS / "protocol_result.yaml"
                _constraints = _load_machine_constraints(RUN_DIR)
                if _constraints and _pr_path.exists():
                    _pr = load_yaml(_pr_path) or {}
                    _protocol_obj = {}
                    _protocol_path_str = _pr.get("protocol_file")
                    if _protocol_path_str:
                        _candidate = Path(_protocol_path_str)
                        if not _candidate.is_absolute():
                            _candidate = ROOT / _candidate
                        if _candidate.exists():
                            with open(_candidate, encoding="utf-8") as f:
                                _protocol_obj = json.load(f)
                    _violations = _check_protocol_execution_conformance(_pr, _constraints, _protocol_obj)
                    if _violations:
                        print("\n🛑 [F4d] PRE-REGISTRATION CONFORMANCE VIOLATION — protocol_execution did "
                              "NOT test what was pre-registered:")
                        for v in _violations:
                            print(f"   - {v}")
                        _mark_trial_invalidated(run_id, "; ".join(_violations))
                        update_state(path=RUN_DIR, status="paused_for_human",
                                     flags={"conformance_violation": True},
                                     conformance_violations=_violations)
                        next_stage = "human_pause"

            elif current_stage == "verdict_interpreter":
                _interp = load_yaml(ARTIFACTS / "verdict_interpretation.yaml")
                _auto_generate_findings_carryover(RUN_DIR, _interp)
                # Slice 6c S2a: the pre-flight's flag reading is passed down (the
                # kwarg only when on, so the flag-off call is unchanged).
                next_stage = determine_post_verdict_route(
                    RUN_DIR, run_id, **({"routing_retired": True} if _vrr_flag else {}))
                # CODE-REVIEW FIX (2026-09-21): the profit-bars stop
                # (determine_post_verdict_route -> _dispatch_verdict_route's
                # promote branch) can now return "human_pause" here, something
                # this branch never produced before. Every OTHER stage that can
                # return "human_pause" (backtest_specification, data_availability_
                # gate, holdout_evaluation) already breaks immediately so step 6
                # below never overwrites the just-set paused_for_human status
                # back to "active" -- this branch was missing that guard, which
                # would have silently un-paused a genuinely halted run and left
                # resume_pipeline's status check refusing to resume it.
                if next_stage == "human_pause":
                    update_state(path=RUN_DIR, status="paused_for_human")
                    break

            elif current_stage == "specialist_readers":
                if _rr_flag:
                    # E-058 S2a: record before deciding -- the same route runs
                    # after regroup_record instead of here.
                    next_stage = "regroup_record"
                else:
                    # E-046a Slice 5b-ii-B: the route comes from the grid only
                    # (component-error check, then idea_status.yaml). The readers'
                    # proposals play no part in it.
                    next_stage = determine_post_specialist_readers_route(RUN_DIR, run_id)
                    if next_stage == "human_pause":
                        update_state(path=RUN_DIR, status="paused_for_human")
                        break

            elif current_stage == "regroup_record":
                # E-058 S2a: the unchanged grid route, after the memory is written,
                # on the checks the stage already made this iteration.
                # Branch 3 on every backtest: the decide step first raises the
                # profit_bars_reached stop when a variant passed every bar (the
                # memory already records it). A component-error run skips it: its
                # own pause below wins. None -> the grid route, unchanged.
                next_stage = None
                if _pbe_flag and not _rr_checks["component_errors"]:
                    next_stage = _profit_bars_stop_route(RUN_DIR, run_id)
                    # Slice 6c S2d: the resume from that stop reads the operator's
                    # holdout_decision.yaml -- spend -> holdout_evaluation,
                    # continue -> None (the route below), else a refusal pause.
                    if next_stage is None and _vrr_flag:
                        next_stage = _holdout_unlock_route(RUN_DIR, run_id)
                # Slice 6c S2a: under verdict_routing_retired the grid route ends
                # the run at completed_<idea_status> (never a pause except the
                # component-error one, never the holdout).
                if next_stage is None:
                    next_stage = determine_post_specialist_readers_route(
                        RUN_DIR, run_id, component_errors=_rr_checks["component_errors"],
                        idea=_rr_checks["idea"], routing_retired=_vrr_flag)
                if next_stage == "human_pause":
                    update_state(path=RUN_DIR, status="paused_for_human")
                    break
                # Slice 6c S2b: the memory-count campaign-review trigger, after the
                # component-error pause, the profit-bars stop and the grid route.
                # (An operator spend -> holdout_evaluation is not a terminal: no
                # review this run; the cadence carries it forward.)
                if _vrr_flag and next_stage in RETIRED_ROUTING_TERMINALS:
                    next_stage = _retired_review_route(RUN_DIR, run_id, next_stage)

            elif current_stage == "campaign_review" and _vrr_flag:
                # Slice 6c S2b: the flag branch (reframe -> a queued brief,
                # terminate -> a stop, continue/escalate_* -> recorded only). A pause
                # keeps pending_stage at campaign_review.
                next_stage = determine_post_campaign_review_route(RUN_DIR, run_id,
                                                                  routing_retired=True)
                if next_stage == "human_pause":
                    update_state(path=RUN_DIR, status="paused_for_human")
                    break

            elif current_stage == "campaign_review":
                next_stage = determine_post_campaign_review_route(RUN_DIR, run_id)

            elif current_stage == "holdout_evaluation":
                # Improvement 06: tool stage — no LLM. Single-use holdout enforcement + DSR gate.
                next_stage = _route_holdout_evaluation(RUN_DIR, run_id)
                if next_stage == "human_pause":
                    update_state(path=RUN_DIR, status="paused_for_human")
                    break

            # Branch 3 on every backtest (orchestrator.profit_bars_every_backtest.
            # enabled, off by default): after either protocol_execution branch above
            # (so after its conformance check, which may have invalidated a
            # variant's trial row), grade every tested variant of this attempt and
            # write profit_bars_evaluation.yaml. It NEVER changes next_stage and
            # never pauses here: protocol_execution completes normally; the stop is
            # raised in the route after regroup_record (_profit_bars_stop_route).
            if current_stage == "protocol_execution" and _pbe_flag:
                _evaluate_profit_bars_every_backtest(
                    RUN_DIR, run_id, **({"record_bars_sha": True} if _vrr_flag else {}))

            # 6. Mark completed and stage next phase
            completed = state.get("completed_stages", [])
            completed.append(current_stage)

            # Slice 6c S2a: the three retired-routing endings are finished runs
            # ("completed"); they are produced only under the flag, so every
            # flag-off run keeps the status it had before.
            update_state(path=RUN_DIR,
                status=("completed" if next_stage in RETIRED_ROUTING_TERMINALS
                        else "active" if next_stage != "completed_rejected" else "rejected"),
                completed_stages=completed,
                current_stage=current_stage,
                pending_stage=next_stage
            )
            # E-059 S2a: a decide-next candidate's pending-at-1a marker is dropped
            # only once the run has moved past hypothesis_generation (no-op otherwise).
            if current_stage == "hypothesis_generation":
                _clear_pass_rule_pending(RUN_DIR, next_stage)

            # Reload state for the next while loop iteration
            state = load_yaml(STATE_FILE)

        except _ReaderBudgetExceeded as e:
            # E-046a 5b-ii-B (code-review fix 7): same terminal outcome as the
            # loop-top weighted-budget check above, not a generic failure.
            print(f"🛑 RUN TERMINATED: {e}")
            update_state(path=RUN_DIR, status="rejected_budget_exceeded")
            break

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