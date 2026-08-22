"""
E-030 S1.5 Piece 2 (`tasks/todo.md`), 2026-08-22.

RUNBOOK.md section 4.5's known limitation: a crash-resume OVERWRITES the
stage's `attempt_N` audit-log entry instead of appending, because
`injected_context["refinement_attempt"]` was regenerated from
`counters.refinements_used` on every loop entry, and the audit key
(`f"{stage_name}_attempt_{attempt_num}"`) was built from that same value --
a same-`refinements_used` re-entry (crash-resume, `pending_stage` unchanged)
silently replaced the prior attempt's cost/timing record rather than adding
a new one. RUNBOOK explicitly forbids hand-bumping `refinements_used` to fix
this cosmetically (it's the refinement-BUDGET gate, not an attempt tally).

The fix adds a separate, independent counter -- `state["stage_attempts"]`,
a dict of `{stage_name: entry_count}`, incremented on every literal entry of
a stage regardless of why -- and threads it through as a NEW
`injected_context["stage_attempt"]` key (the OLD `refinement_attempt` key is
left untouched, still reflecting `refinements_used`, since nothing else was
found to read it). Two tests, matching the fix's two halves:

- test_stage_attempt_counter_survives_reentry_without_refinements_used_changing
  (producer side): drives `run_loop` through a synthetic stage TWICE without
  changing `counters.refinements_used` between calls -- simulating exactly
  the crash-resume condition RUNBOOK describes -- and asserts the counter
  advances (0, then 1) instead of staying pinned. `async_invoke_agent` is
  monkeypatched to a no-op (same boundary the existing SDK-retry tests in
  test_k3_protocol_pinning.py use), since this half only tests the
  PRODUCER (the counter + the value written into the handoff file), not the
  worker's consumption of it.

- test_run_claude_worker_keys_audit_log_on_stage_attempt_not_refinement_attempt
  (consumer side): calls `run_claude_worker` directly with a synthetic
  `injected_context` carrying a `stage_attempt` that DIFFERS from
  `refinement_attempt`, proving the audit_log key follows the new field, not
  the old one. `query` (the claude_agent_sdk entry point `run_claude_worker`
  calls) is monkeypatched to a zero-message async generator so the real
  function runs to the audit_log write without a network/SDK call.

Between them, both halves of the wire are exercised without mocking at the
SDK's internal message-streaming boundary, matching this suite's existing
convention (test_k3_protocol_pinning.py's SDK-retry tests monkeypatch at the
same `async_invoke_agent`/one-level-in boundary).
"""
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402


def _write_handoff(run_dir: Path, filename: str, deliverables=None):
    handoffs_dir = run_dir / "handoffs"
    handoffs_dir.mkdir(parents=True, exist_ok=True)
    data = {"required_inputs": [], "deliverables": deliverables or []}
    with open(handoffs_dir / filename, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def _read_state(run_dir: Path) -> dict:
    return yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))


def _read_handoff(run_dir: Path, filename: str) -> dict:
    return yaml.safe_load((run_dir / "handoffs" / filename).read_text(encoding="utf-8"))


def test_stage_attempt_counter_survives_reentry_without_refinements_used_changing(monkeypatch):
    root = rpr.ROOT  # already sandboxed to a per-test tmp_path by conftest's autouse fixture
    run_dir = root / "runs" / "run_800"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    _write_handoff(run_dir, "synth_handoff.yaml")

    # A synthetic stage, not one of the real routed ones -- default_next is a
    # TERMINAL_PREFIXES value so run_loop stops after exactly one stage per call,
    # without needing to satisfy the real routing graph's downstream stages.
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "synth_stage", {
        "handoff": "synth_handoff.yaml", "default_next": "completed_rejected",
    })

    async def _noop_invoke(stage_name, run_id, retry_context=None):
        return
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)

    state = {
        "run_id": "run_800", "status": "active", "pending_stage": "synth_stage",
        "completed_stages": [], "flags": {}, "audit_log": {},
        "counters": {"refinements_used": 0, "reruns_used": 0},
    }
    with open(run_dir / "pipeline_state.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, sort_keys=False)

    rpr.run_loop("run_800")

    state = _read_state(run_dir)
    assert state["pending_stage"] == "completed_rejected"
    assert state["stage_attempts"] == {"synth_stage": 1}
    handoff = _read_handoff(run_dir, "synth_handoff.yaml")
    assert handoff["injected_context"]["stage_attempt"] == "0", \
        "first entry must read 0, matching refinements_used's own default -- bit-identity for the non-crash path"

    # Simulate a crash-resume: a fresh process re-enters the SAME stage with
    # counters.refinements_used UNCHANGED -- exactly RUNBOOK section 4.5's
    # described condition, and exactly what the old refinement_attempt-keyed
    # audit_log would have overwritten.
    rpr.update_state(path=run_dir, pending_stage="synth_stage", status="active")

    rpr.run_loop("run_800")

    state = _read_state(run_dir)
    assert state["stage_attempts"] == {"synth_stage": 2}, \
        "counter must advance on re-entry even though refinements_used never changed"
    handoff = _read_handoff(run_dir, "synth_handoff.yaml")
    assert handoff["injected_context"]["stage_attempt"] == "1", \
        "second entry must get a DIFFERENT stage_attempt, or the audit_log key would collide and overwrite"
    # The old field is untouched -- still tracks refinements_used, still "0" both times.
    assert handoff["injected_context"]["refinement_attempt"] == "0"


def test_run_claude_worker_keys_audit_log_on_stage_attempt_not_refinement_attempt(monkeypatch):
    root = rpr.ROOT
    run_dir = root / "runs" / "run_801"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    with open(run_dir / "pipeline_state.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump({"status": "active", "audit_log": {}}, f, sort_keys=False)

    async def _empty_query(*args, **kwargs):
        return
        yield  # noqa -- makes this an async generator that yields zero messages
    monkeypatch.setattr(rpr, "query", _empty_query)

    handoff = {
        "required_inputs": [], "optional_inputs": [],
        # The two fields deliberately DIFFER, proving the audit_log key follows
        # stage_attempt (7), not the old refinement_attempt (0) -- if the fix
        # regressed to reading the old key, this assertion would catch it.
        "injected_context": {"stage_attempt": "7", "refinement_attempt": "0"},
    }

    import asyncio
    asyncio.run(rpr.run_claude_worker("hypothesis_generation", handoff, run_dir))

    state = _read_state(run_dir)
    assert "hypothesis_generation_attempt_7" in state["audit_log"], \
        f"expected key using stage_attempt=7, got keys: {list(state['audit_log'].keys())}"
    assert "hypothesis_generation_attempt_0" not in state["audit_log"], \
        "must not have keyed on the old refinement_attempt value"
