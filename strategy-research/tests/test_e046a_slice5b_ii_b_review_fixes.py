"""
E-046a Slice 5b-ii-B -- regression tests for the code-review fixes on 1079c96b
(one or more per item; each fails on 1079c96b). Items 3 and 5 are covered in
test_e046a_slice5b_ii_b_readers_stage.py (reader-output and firewall tests).
Sandboxing: tests/conftest.py's autouse _sandbox_by_default. No LLM, no
real subprocess.
"""
import asyncio
import re
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import reader_proposals  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import (  # noqa: E402
    ALL_ON, RUN_ID, _seed_run, _set_orchestrator, _write_menu_pre_registration,
)

FLAG_OFF_DEPS_ON = {"grid_evaluation": {"enabled": True}, "category_reports": {"enabled": True}}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


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


def _seed_stale(run_dir: Path) -> None:
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "idea_status.yaml",
                  rpr._build_idea_status_artifact({"idea_status": "validated"}, run_dir.name))
    rpr.save_yaml(arts / "grid_evaluation.yaml", {"stale": True})
    rpr.save_yaml(arts / "reports" / "profitability.yaml", {"stale": True})
    (arts / "proposals").mkdir(parents=True, exist_ok=True)
    (arts / "proposals" / "profitability.yaml").write_text("[]", encoding="utf-8")


def _stub_grid_and_reports(monkeypatch, grid_raises=False, reports_raise=False, order=None):
    import verdict_criteria_evaluator as vce
    import build_reports as br

    def _grid(results, pre_reg, brief, menu):
        if grid_raises:
            raise RuntimeError("grid bug")
        return {"result": "FAIL", "idea_status": "refuted", "reason": "fresh"}
    monkeypatch.setattr(vce, "evaluate_grid", _grid)
    monkeypatch.setattr(vce, "evaluate_pass_rule_criteria",
                        lambda *a, **k: {"result": "legacy_not_evaluable"})

    def _reports(run_dir, write=True):
        if order is not None:
            order.append("build_reports")
        if reports_raise:
            raise RuntimeError("reports bug")
        return {}
    monkeypatch.setattr(br, "build_reports", _reports)

    def _regime(run_id, run_dir):
        if order is not None:
            order.append("regime_report")
        return {"per_symbol_per_timeframe": []}
    monkeypatch.setattr(rpr, "_ensure_regime_detector_report", _regime)


# --- 1. stale artifacts / swallowed prerequisites ---------------------------

def test_fix1_protocol_execution_clears_stale_artifacts_and_rewrites_fresh(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _protocol_execution_run("run_950", menu_shaped=True)
    _seed_stale(run_dir)
    _fake_protocol_subprocess(monkeypatch)
    _stub_grid_and_reports(monkeypatch)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_950"))
    arts = run_dir / "artifacts"
    assert rpr.load_yaml(arts / "idea_status.yaml")["idea_status"] == "refuted"
    assert "stale" not in rpr.load_yaml(arts / "grid_evaluation.yaml")
    assert not (arts / "reports" / "profitability.yaml").exists()
    assert not (arts / "proposals").exists()


@pytest.mark.parametrize("grid_raises,reports_raise,menu_shaped", [
    (True, False, True), (False, True, True), (False, False, False)])
def test_fix1_grid_or_report_failure_fails_stage_after_trial_recorded(
        monkeypatch, grid_raises, reports_raise, menu_shaped):
    _set_orchestrator(ALL_ON)
    run_dir = _protocol_execution_run("run_951", menu_shaped=menu_shaped)
    _seed_stale(run_dir)
    _fake_protocol_subprocess(monkeypatch)
    _stub_grid_and_reports(monkeypatch, grid_raises=grid_raises, reports_raise=reports_raise)
    with pytest.raises(RuntimeError, match="could not produce them"):
        asyncio.run(rpr.run_tool_worker("protocol_execution", "run_951"))
    arts = run_dir / "artifacts"
    assert not (arts / "proposals").exists()
    if grid_raises or not menu_shaped:
        assert not (arts / "idea_status.yaml").exists()
    # the backtest's trial row is a normal success row, not a failure row
    trials = rpr.load_campaign_state().get("trial_sharpes", [])
    assert [t["trial_id"] for t in trials] == ["run_951"]
    assert "backtest_failed" not in str(trials[0])


def test_fix1_flag_off_deletes_nothing_and_swallows_as_before(monkeypatch):
    _set_orchestrator(FLAG_OFF_DEPS_ON)
    run_dir = _protocol_execution_run("run_952", menu_shaped=True)
    _seed_stale(run_dir)
    _fake_protocol_subprocess(monkeypatch)
    _stub_grid_and_reports(monkeypatch, grid_raises=True, reports_raise=True)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_952"))  # no raise
    arts = run_dir / "artifacts"
    assert (arts / "proposals" / "profitability.yaml").exists()
    assert rpr.load_yaml(arts / "grid_evaluation.yaml") == {"stale": True}


# --- 2. killed_run_gate fixture ---------------------------------------------

def test_fix2_killed_run_gate_pipeline_proof_holds_with_flag_on(monkeypatch):
    import killed_run_gate as kg
    _set_orchestrator(ALL_ON)
    # the gate reassigns rpr.CAMPAIGN_STATE_PATH itself; restore it on teardown
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", rpr.CAMPAIGN_STATE_PATH)
    result = kg.proof_killed_row_counts_in_pipeline_N()
    assert result["passed"], result


# --- 4. no campaign-level regime detector report before the reports ----------
# CUL-381 replaced fix 4's refresh: the readers' reports are built from this
# run's own output only, so the campaign-level detector report is neither
# refreshed nor required, and a missing one cannot fail the stage.

def test_fix4_cul381_no_regime_report_refresh_under_flag(monkeypatch):
    _set_orchestrator(ALL_ON)
    _protocol_execution_run("run_953", menu_shaped=True)
    _fake_protocol_subprocess(monkeypatch)
    order = []
    _stub_grid_and_reports(monkeypatch, order=order)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_953"))
    assert order == ["build_reports"]
    assert not hasattr(rpr, "_refresh_regime_detector_report_for_readers")


def test_fix4_cul381_detector_report_has_one_caller_the_legacy_verdict_interpreter():
    """Static pin over BOTH report-building sites (single-run and variant loop):
    the campaign-level detector report is produced only by the legacy
    verdict_interpreter branch, which the reader flag never reaches."""
    src = Path(rpr.__file__).read_text(encoding="utf-8")
    calls = [m.start() for m in re.finditer(r"(?<!def )_ensure_regime_detector_report\(", src)]
    assert len(calls) == 1, len(calls)
    # ...and that call sits inside the legacy `verdict_interpreter` branch
    branch = src.index('            if current_stage == "verdict_interpreter":')
    next_branch = src.index('            elif current_stage == "regroup_record":', branch)
    assert branch < calls[0] < next_branch
    injects = [m.start() for m in
               re.finditer(r"(?<!def )_inject_regime_context_into_handoff\(", src)]
    assert len(injects) == 1 and branch < injects[0] < next_branch


def test_fix4_flag_off_does_not_refresh_regime_report(monkeypatch):
    _set_orchestrator(FLAG_OFF_DEPS_ON)
    _protocol_execution_run("run_954", menu_shaped=True)
    _fake_protocol_subprocess(monkeypatch)
    order = []
    _stub_grid_and_reports(monkeypatch, order=order)
    asyncio.run(rpr.run_tool_worker("protocol_execution", "run_954"))
    assert order == ["build_reports"]


# --- 6. pre-flight on the pass_rule ------------------------------------------

def test_fix6_preflight_rejects_non_menu_or_missing_pass_rule_before_any_spend(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(pending="hypothesis_generation")
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml",
                  {"pass_rule": "median sharpe > 0.5 (legacy prose)"})
    invoked = []
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", lambda *a, **k: invoked.append(a[0]))
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert invoked == []
    assert state["status"] == "failed" and "not menu-shaped" in state["last_error"]
    (run_dir / "artifacts" / "pre_registration.yaml").unlink()
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert invoked == [] and "pre_registration.yaml is missing" in state["last_error"]


def test_fix6_no_preflight_flag_off(monkeypatch):
    _set_orchestrator(FLAG_OFF_DEPS_ON)
    run_dir = _seed_run(pending="hypothesis_generation")
    (run_dir / "artifacts" / "pre_registration.yaml").unlink()
    invoked = []

    def _stop(stage, *a, **k):
        invoked.append(stage)
        raise KeyError("stop")
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", _stop)
    rpr.save_yaml(run_dir / "handoffs" / "research_brief_to_hypothesis.yaml",
                  {"required_inputs": [], "deliverables": []})
    rpr.run_loop(RUN_ID)
    assert invoked == ["hypothesis_generation"]


# --- 7. budget inside the reader loop ----------------------------------------

def test_fix7_budget_inside_reader_loop_is_rejected_budget_exceeded(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run(idea_status="refuted")
    calls = []

    async def _expensive(prompt):
        calls.append(prompt)
        return "```yaml\n[]\n```", {"usage": {"output_tokens": 10**9}, "cost_usd": 0.0,
                                     "num_turns": 1}
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _expensive)
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert len(calls) == 1
    assert state["status"] == "rejected_budget_exceeded"
    assert state["pending_stage"] == "specialist_readers"


# --- 8. _route_kill feeds no retired machinery under the flag -----------------

def test_fix8_flag_on_kill_writes_no_family_or_continuation_state():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="refuted")
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "completed_rejected"
    campaign = rpr.load_campaign_state()
    assert RUN_ID in campaign["runs"]
    assert [d["run"] for d in campaign["diagnostics_log"]] == [RUN_ID]
    assert not campaign.get("altitude_history")
    assert not campaign.get("failed_families")
    assert not campaign.get("recent_parameter_dimensions_by_family")
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert not any(k.startswith("continuation") for k in state)


def test_fix8_flag_off_kill_unchanged():
    _set_orchestrator(None)
    run_dir = _seed_run(idea_status=None)
    assert rpr._route_kill(run_dir, RUN_ID, {"hypothesis_family": "F"}, {}) == "completed_rejected"
    assert rpr.load_campaign_state()["altitude_history"][-1]["family"] == "F"
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["continuation_created_by"] == "_route_kill"


# --- 9. flag reads ------------------------------------------------------------

def test_fix9_extract_run_numbers_degrades_on_bad_flag():
    run_dir = _seed_run(idea_status="validated")
    _set_orchestrator({"specialist_readers": {"enabled": "yes"}})
    assert "idea_status" not in camp._extract_run_numbers(run_dir)


def test_fix9_bad_flag_sets_failed_not_escape(monkeypatch):
    _set_orchestrator({"specialist_readers": {"enabled": "yes"}})
    run_dir = _seed_run(pending="hypothesis_generation")
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "failed" and "not a real boolean" in state["last_error"]


# --- 10. one model constant, one token helper ---------------------------------

def test_fix10_reader_uses_shared_model_and_token_helper(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    monkeypatch.setattr(rpr, "_CLAUDE_WORKER_MODEL", "sentinel-model")
    seen = []

    class _Opts:
        def __init__(self, model, **_closed_book):  # CUL-336: + tools/setting_sources/...
            seen.append(model)

    async def _query(prompt, options):
        yield type("R", (), {"total_cost_usd": 0.0, "num_turns": 1,
                             "usage": {"input_tokens": 3, "cache_read_input_tokens": 7}})()
    monkeypatch.setattr(rpr, "ClaudeAgentOptions", _Opts)
    monkeypatch.setattr(rpr, "query", _query)
    # no text -> no fenced block, twice; CUL-380: recorded as dropped, no raise
    rpr.run_reader_worker("profitability", RUN_ID, run_dir)
    assert seen == ["sentinel-model", "sentinel-model"]
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    assert audit["specialist_readers_profitability_attempt_0"]["tokens"] == \
        rpr._usage_token_record({"input_tokens": 3, "cache_read_input_tokens": 7})
    assert not hasattr(rpr, "_READER_MODEL")


def test_fix10_claude_worker_audit_tokens_unchanged(monkeypatch, tmp_path):
    """run_claude_worker's audit_log tokens block is byte-identical after the
    helper extraction (same keys, same order, same weighted value)."""
    rec = rpr._usage_token_record({"input_tokens": 100, "output_tokens": 20,
                                   "cache_read_input_tokens": 1000,
                                   "cache_creation_input_tokens": 8})
    assert list(rec) == ["input", "output", "cache_read", "cache_creation", "total", "weighted"]
    assert rec["total"] == 1128
    assert rec["weighted"] == round(100 * 1.0 + 20 * 5.0 + 1000 * 0.1 + 8 * 1.25, 1)
