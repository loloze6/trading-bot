"""
E-032 S2c's anti-adjacency retry -- RETIRED by E-036 S2a (2026-09-27).

This file used to test orchestrator.anti_adjacency_retry: the gate call in
_route_post_innovation_expansion, its retry-4-times-then-escalate policy and
the refusal reason carried into the next hypothesis_generation prompt
(_apply_anti_adjacency_retry_context). The whole mechanism was removed, not
flipped: it fired before backtest_specification had produced any config, so
an exact repeat was structurally unreachable there and it never had a
working REPEAT effect (engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md §1,
§5 and the operator decision of 2026-09-27). The flag was off, so its
removal changes no default output.

Of its 23 test functions (25 collected), 21 are retired with it (their
subject -- the retry policy and its flag -- no longer exists) and 2 are
repointed below (noted in each). What remains proves the code path is gone,
that the innovation_expansion route is exactly what the flag-off code
returned, and that an old paused state still classifies. The exact-match
check now lives at 5a: tests/test_e036_s2a_exact_match_gate.py.
"""
import inspect
import sys
from pathlib import Path

import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))

import run_phase1_research as rpr  # noqa: E402


def test_retry_machinery_is_removed_from_the_orchestrator():
    for name in ("_anti_adjacency_retry_enabled", "_route_post_innovation_expansion",
                 "_apply_anti_adjacency_retry_context", "_ANTI_ADJACENCY_RETRY_MAX_ATTEMPTS"):
        assert not hasattr(rpr, name), name


def test_retry_flag_is_gone_from_config_and_register():
    cfg = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert "anti_adjacency_retry" not in cfg["orchestrator"]
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    assert "anti_adjacency_retry" not in {f["name"] for f in reg["flags"]}


def test_innovation_expansion_routes_to_default_next_with_no_gate_call():
    """What the flag-off route returned (STAGE_CONFIGS['innovation_expansion']
    ['default_next'], 'validation'), with the config-direct redirect
    untouched -- and no gate call or retry prompt hook left in run_loop /
    async_invoke_agent."""
    assert rpr.STAGE_CONFIGS["innovation_expansion"]["default_next"] == "validation"
    loop_src = inspect.getsource(rpr.run_loop)
    branch = loop_src[loop_src.index('elif current_stage == "innovation_expansion":'):]
    branch = branch[:branch.index("elif current_stage == \"backtest_specification\"")]
    assert "anti_adjacency" not in branch.replace("anti-adjacency", "")
    assert 'next_stage = "backtest_specification"' in branch
    assert "_apply_anti_adjacency_retry_context" not in inspect.getsource(rpr.async_invoke_agent)


def test_run_loop_ignores_a_leftover_retry_flag(monkeypatch):
    """Repointed from test_flag_off_run_loop_iteration_unchanged: a full
    run_loop iteration over innovation_expansion, now with a leftover
    `anti_adjacency_retry: {enabled: true}` in the config -- the stage
    advances to default_next, no gate result and no retry state are
    written."""
    root = rpr.ROOT
    (root / "config").mkdir(parents=True, exist_ok=True)
    (root / "config" / "campaign_config.yaml").write_text(yaml.safe_dump(
        {"orchestrator": {"anti_adjacency_retry": {"enabled": True}}}), encoding="utf-8")
    run_dir = root / "runs" / "run_914"
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "handoffs").mkdir(parents=True, exist_ok=True)
    (run_dir / "handoffs" / "hypothesis_to_innovation_expansion.yaml").write_text(
        yaml.safe_dump({"required_inputs": [], "deliverables": []}), encoding="utf-8")
    (run_dir / "pipeline_state.yaml").write_text(yaml.safe_dump({
        "run_id": "run_914", "status": "active", "pending_stage": "innovation_expansion",
        "completed_stages": [], "flags": {}, "audit_log": {},
        "counters": {"refinements_used": 0, "reruns_used": 0}}), encoding="utf-8")

    async def _noop_invoke(stage_name, run_id, retry_context=None):
        return
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    # default_next made terminal-shaped for this test only (same technique the
    # retired test used), so run_loop stops right after innovation_expansion.
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "innovation_expansion",
                        {**rpr.STAGE_CONFIGS["innovation_expansion"],
                         "default_next": "completed_rejected"})
    rpr.run_loop("run_914")
    final = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert final["pending_stage"] == "completed_rejected"
    assert "anti_adjacency_gate_retry" not in final
    assert not (run_dir / "artifacts" / "anti_adjacency_result.yaml").exists()


def test_a_pre_existing_exhausted_pause_still_classifies_as_itself():
    """Repointed from test_flag_on_escalation_classifies_via_existing_run_
    campaign_mechanism: nothing writes flags.anti_adjacency_gate_exhausted any
    more, but a pipeline_state.yaml written before the retirement must still
    classify as itself (run_campaign keeps that branch for exactly this)."""
    import run_campaign as camp
    run_dir = rpr.ROOT / "runs" / "run_924"
    run_dir.mkdir(parents=True, exist_ok=True)
    state = {"run_id": "run_924", "status": "paused_for_human", "pending_stage": "hypothesis_generation",
             "flags": {"anti_adjacency_gate_exhausted": True}, "audit_log": {}}
    assert camp._classify_human_pause(run_dir, state) == "anti_adjacency_gate_exhausted"
