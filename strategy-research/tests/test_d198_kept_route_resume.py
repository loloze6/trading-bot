"""
D-198, review round 1: the grid failure at protocol_execution (master's fix 1, grid part) and the
route-only resume.

  * a pause at the route leaves the route-only sentinel (`specialist_readers`, the deleted
    stage's name) as pending_stage, so a resume of a run over its token budget takes the route
    instead of being terminated at the loop top (master exempted the route after the analyst);
  * the route-only resume makes the route's entry checks (a valid idea_status.yaml, the retune
    firewall) as master did on every stage entry.
No LLM.
"""
import asyncio
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import analyst_session as asm  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402
from _reader_test_helpers import (  # noqa: E402,F401
    RUN_ID, _seed_run, _set_orchestrator, _stub_tbot_python, _write_menu_pre_registration)

ALL_ON = {"grid_evaluation": {"enabled": True}}


# ---------------------------------------------------------------------------
# master's fix 1, grid part: a failed grid fails protocol_execution
# ---------------------------------------------------------------------------

def _protocol_execution_run(run_id: str, menu_shaped: bool) -> Path:
    root = rpr.ROOT
    _write_protocol(root, f"{run_id}.json")
    run_dir = _minimal_run(root, run_id)
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{}", encoding="utf-8")
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": f"protocols/{run_id}.json"})
    if menu_shaped:
        _write_menu_pre_registration(run_dir)
    return run_dir


def _fake_protocol_subprocess(monkeypatch):
    def _run(cmd, *args, **kwargs):
        out_dir = Path(cmd[cmd.index("--out-dir") + 1])
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "protocol_summary.json").write_text(
            rpr.json.dumps({"config_sha256": "x", "protocol_file": "p", "results": [],
                            "per_symbol_summary": {}, "verdict": "kill"}), encoding="utf-8")

        class _Ok:
            returncode, stdout, stderr = 0, "", ""
        return _Ok()
    monkeypatch.setattr(rpr.subprocess, "run", _run)


def _stub_grid(monkeypatch, grid_raises=False):
    import verdict_criteria_evaluator as vce

    def _grid(results, pre_reg, brief, menu):
        if grid_raises:
            raise RuntimeError("grid bug")
        return {"result": "FAIL", "idea_status": "refuted", "reason": "fresh"}
    monkeypatch.setattr(vce, "evaluate_grid", _grid)
    monkeypatch.setattr(vce, "evaluate_pass_rule_criteria",
                        lambda *a, **k: {"result": "legacy_not_evaluable"})
    monkeypatch.setattr(rpr, "_ensure_regime_detector_report",
                        lambda run_id, run_dir: {"per_symbol_per_timeframe": []})


@pytest.mark.parametrize("grid_raises,menu_shaped", [(True, True), (False, False)])
def test_fix1_grid_failure_fails_stage_after_trial_recorded(monkeypatch, grid_raises,
                                                            menu_shaped):
    """The grid is a prerequisite of the route -- a failure (a raising grid, or a non-menu pass
    rule) fails protocol_execution after its trial rows are recorded. (Master's version also
    stubbed the report builder; it is deleted.)"""
    _set_orchestrator(ALL_ON)
    run_dir = _protocol_execution_run("run_951", menu_shaped=menu_shaped)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "idea_status.yaml",
                  rpr._build_idea_status_artifact({"idea_status": "validated"}, run_dir.name))
    rpr.save_yaml(arts / "grid_evaluation.yaml", {"stale": True})
    _fake_protocol_subprocess(monkeypatch)
    _stub_grid(monkeypatch, grid_raises=grid_raises)
    with pytest.raises(RuntimeError, match="could not produce it"):
        asyncio.run(rpr.run_tool_worker("protocol_execution", "run_951"))
    if grid_raises or not menu_shaped:
        assert not (arts / "idea_status.yaml").exists()     # the stale one is not left to route on
    # the backtest's trial row is a normal success row, not a failure row
    trials = rpr.load_campaign_state().get("trial_sharpes", [])
    assert [t["trial_id"] for t in trials] == ["run_951"]
    assert "backtest_failed" not in str(trials[0])


# ---------------------------------------------------------------------------
# the route-only resume
# ---------------------------------------------------------------------------

def _fake_lens_worker(called):
    def worker(lens, run_id, run_dir, stage_attempt=0):
        called.append(lens)
        rpr._write_skipped_reading(asm.LENS_CATEGORY[lens], run_id, run_dir,
                                   {"rule": "output_refused_after_retry", "reason": "stub"})
    return worker


def _set_idea_status(run_dir: Path, idea_status: str) -> None:
    rpr.save_yaml(run_dir / "artifacts" / "idea_status.yaml",
                  rpr._build_idea_status_artifact({"idea_status": idea_status, "reason": "r"},
                                                  RUN_ID))


def _over_budget(monkeypatch) -> None:
    monkeypatch.setattr(rpr, "_load_token_budget", lambda: 1)
    monkeypatch.setattr(rpr, "_compute_weighted_budget_usage", lambda log: (10**9, []))


def test_a_pause_at_the_route_after_the_analyst_resumes_into_the_route_even_over_budget(
        monkeypatch):
    """regroup_record off, analyst + grid on: the route pauses in the analyst's iteration. The
    run must resume into the route (master exempted it from the loop-top budget check as
    `specialist_readers` after the analyst), not be terminated as over budget, and the lenses
    are not run again."""
    _set_orchestrator(ALL_ON)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    run_dir = _seed_run(pending="analyst", idea_status="inconclusive")
    called = []
    monkeypatch.setattr(rpr, "run_analyst_worker", _fake_lens_worker(called))
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert len(called) == 2 and state["status"] == "paused_for_human"
    assert state["pending_stage"] == rpr.LEGACY_READERS_STAGE
    # the operator rules; the run resumes over budget: it routes, it is not terminated
    _set_idea_status(run_dir, "refuted")
    rpr.update_state(path=run_dir, status="active")
    _over_budget(monkeypatch)
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "rejected" and state["pending_stage"] == "completed_rejected"
    assert len(called) == 2                                  # no lens was re-run


def test_a_stage_that_spends_is_still_budget_checked_before_the_analyst(monkeypatch):
    """The exemption is the route-only resume's alone: a run entering the analyst stage over
    budget is still terminated before any lens call."""
    _set_orchestrator(ALL_ON)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    run_dir = _seed_run(pending="analyst", idea_status="refuted")
    called = []
    monkeypatch.setattr(rpr, "run_analyst_worker", _fake_lens_worker(called))
    _over_budget(monkeypatch)
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "rejected_budget_exceeded" and called == []


def test_the_route_only_resume_makes_the_retune_firewall_check():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(pending=rpr.LEGACY_READERS_STAGE, idea_status="refuted")
    rpr.save_yaml(run_dir / "artifacts" / "regime_audit_decision.yaml",
                  {"recommended_action": "raise the period because the sharpe is low"})
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "failed" and "RETUNE FIREWALL VIOLATION" in state["last_error"]
    assert state["pending_stage"] == rpr.LEGACY_READERS_STAGE     # never routed


def test_the_route_only_resume_checks_idea_status_before_routing():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(pending=rpr.LEGACY_READERS_STAGE, idea_status="refuted")
    doc = rpr.load_yaml(run_dir / "artifacts" / "idea_status.yaml")
    doc["run_id"] = "run_001"                                      # stale
    rpr.save_yaml(run_dir / "artifacts" / "idea_status.yaml", doc)
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "failed" and "stale" in state["last_error"]


def test_the_route_only_resume_with_component_errors_pauses_without_the_entry_checks():
    """A run with component errors is paused by the route itself; the firewall file is not
    consulted (the stage body skipped everything for such a run on master too)."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(pending=rpr.LEGACY_READERS_STAGE, idea_status="refuted", errors_count=2)
    rpr.save_yaml(run_dir / "artifacts" / "regime_audit_decision.yaml",
                  {"recommended_action": "raise the period because the sharpe is low"})
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human"
    assert state["flags"] == {"component_execution_error_flagged": True}
