"""
D-198: the kept grid route, restored after the readers' stage tests went, plus the two
route-only resume fixes of review round 1.

From origin/master's test_e046a_slice5b_ii_b_readers_stage.py (section 5-7: the route from the
grid) and test_e046a_slice5b_ii_b_review_fixes.py (fix 1 grid part, fix 6, fix 8). The route
(`determine_post_specialist_readers_route`) is keyed on orchestrator.grid_evaluation.enabled now
(the deleted specialist_readers flag used to switch it). Dropped as tests of deleted code: the
reader loop, fail-loud reader output, the stage body, report refresh and the flag helper.

New (review round 1):
  * a pause at the route leaves the route-only sentinel (`specialist_readers`), so a resume of a
    run over its token budget takes the route instead of being terminated at the loop top
    (master exempted the route after the analyst);
  * the route-only resume makes the route's entry checks (valid idea_status.yaml, the retune
    firewall), as master did on every stage entry.
No LLM.
"""
import asyncio
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import reader_proposals  # noqa: E402
import analyst_session as asm  # noqa: E402

from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402
from test_e033_slice4b_gate_conformance_promotion import _minimal_run_at, _noop_invoke  # noqa: E402
from _reader_test_helpers import (  # noqa: E402,F401
    RUN_ID, _proposal, _protocol_result, _seed_run, _set_orchestrator, _stub_tbot_python,
    _write_menu_pre_registration)

# D-198: the route flag is the grid's (the deleted specialist_readers flag used to require it)
ALL_ON = {"grid_evaluation": {"enabled": True}}
REPORT_CATEGORIES = list(rpr.READER_CATEGORIES)


# ---------------------------------------------------------------------------
# The route from the grid
# ---------------------------------------------------------------------------

def test_validated_routes_to_promote(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="validated")
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "holdout_evaluation"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["flags"]["walk_forward_passed"] is True
    audit = rpr.load_yaml(run_dir / "artifacts" / "promotion_audit.yaml")
    assert audit["hypothesis_id"] == "H-TEST-1"  # from hypothesis_card.yaml, not run_id
    assert not (run_dir / "artifacts" / "verdict_interpretation.yaml").exists()


def test_promote_without_hypothesis_id_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="validated")
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", {"title": "no id"})
    with pytest.raises(ValueError, match="hypothesis_id"):
        rpr.determine_post_specialist_readers_route(run_dir, RUN_ID)


def test_refuted_routes_to_kill_terminate(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="refuted")
    dispatched = []
    real = rpr._dispatch_verdict_route

    def _spy(path, run_id, interp, campaign, hv, lr):
        dispatched.append((interp, hv, lr))
        return real(path, run_id, interp, campaign, hv, lr)
    monkeypatch.setattr(rpr, "_dispatch_verdict_route", _spy)
    breaker = []
    monkeypatch.setattr(rpr, "_apply_circuit_breaker", lambda *a: breaker.append(a))
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "completed_rejected"
    assert dispatched == [({}, "kill", "terminate")]
    assert breaker == []
    # code-review fix 8: no continuation_* bookkeeping under the flag
    assert "continuation_child" not in rpr.load_yaml(run_dir / "pipeline_state.yaml")


def test_inconclusive_pauses_with_inconclusive_grid():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="inconclusive")
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "human_pause"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human"
    assert state["flags"] == {"inconclusive_grid": True}
    assert camp._classify_human_pause(run_dir, state) == "inconclusive_grid"
    assert dict(camp._PAUSE_FLAG_TO_REASON)["inconclusive_grid"] == "inconclusive_grid"


@pytest.mark.parametrize("idea_status", ["validated", "refuted", "inconclusive", None])
def test_component_errors_pause_first(idea_status):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status=idea_status, errors_count=3)
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "human_pause"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["flags"] == {"component_execution_error_flagged": True}
    assert not (run_dir / "artifacts" / "promotion_audit.yaml").exists()
    assert camp._classify_human_pause(run_dir, state) == "component_execution_error"


def test_component_errors_in_a_variant_count_too():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="validated")
    rpr.save_yaml(run_dir / "artifacts" / "variants" / "v2" / "protocol_result.yaml", _protocol_result(1))
    errors = rpr._protocol_component_errors(run_dir)
    assert len(errors) == 1 and "variants/v2/protocol_result.yaml" in errors[0]


def test_component_errors_zero_or_null_do_not_pause():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(errors_count=0)
    assert rpr._protocol_component_errors(run_dir) == []


@pytest.mark.parametrize("block", [{"count": "3"}, {"samples": []}, "x", {"count": True}])
def test_malformed_component_errors_fail_loud(block):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run()
    pr = _protocol_result()
    pr["results"][0]["component_errors"] = block
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", pr)
    with pytest.raises(ValueError, match="malformed"):
        rpr.determine_post_specialist_readers_route(run_dir, RUN_ID)


def test_missing_idea_status_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status=None)
    with pytest.raises(FileNotFoundError, match="Refusing to guess"):
        rpr.determine_post_specialist_readers_route(run_dir, RUN_ID)
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml").get("flags") == {}


@pytest.mark.parametrize("mutate,match", [
    (lambda d: d.update(idea_status="maybe"), "not one of"),
    (lambda d: d.update(result="PASS"), "disagrees"),
    (lambda d: d.update(lineage_routing="pivot"), "disagrees"),
    (lambda d: d.update(run_id="run_001"), "stale"),
])
def test_malformed_idea_status_fails_loud(mutate, match):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="refuted")
    doc = rpr.load_yaml(run_dir / "artifacts" / "idea_status.yaml")
    mutate(doc)
    rpr.save_yaml(run_dir / "artifacts" / "idea_status.yaml", doc)
    with pytest.raises(ValueError, match=match):
        rpr.determine_post_specialist_readers_route(run_dir, RUN_ID)


def test_unparseable_idea_status_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status=None)
    (run_dir / "artifacts" / "idea_status.yaml").write_text("idea_status: [unclosed\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unparseable"):
        rpr.determine_post_specialist_readers_route(run_dir, RUN_ID)



# 6. Reader scores cannot change the route
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status,expected", [
    ("validated", "holdout_evaluation"), ("refuted", "completed_rejected"), ("inconclusive", "human_pause")])
def test_reader_scores_cannot_change_the_route(monkeypatch, idea_status, expected):
    _set_orchestrator(ALL_ON)
    routes = []
    for i, (n_props, score) in enumerate([(0, 0), (3, 0), (3, 3)]):
        run_id = f"run_99{i}"
        run_dir = _seed_run(run_id=run_id, idea_status=idea_status)
        pdir = run_dir / "artifacts" / "proposals"
        pdir.mkdir(parents=True)
        for c in REPORT_CATEGORIES:
            rpr.save_yaml(pdir / f"{c}.yaml", [_proposal(c, run_id, n, score) for n in range(1, n_props + 1)])
        reader_proposals.load_proposals(pdir, REPORT_CATEGORIES)  # the fixtures are valid proposals
        routes.append(rpr.determine_post_specialist_readers_route(run_dir, run_id))
    assert routes == [expected] * 3


def test_route_never_reads_proposals(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(idea_status="refuted")

    def _boom(*a, **k):
        raise AssertionError("the route must not read proposals")
    monkeypatch.setattr(reader_proposals, "load_proposals", _boom)
    monkeypatch.setattr(rpr, "_reader_proposals_module", _boom)
    real_load = rpr.load_yaml

    def _guarded_load(path):
        assert "proposals" not in Path(path).parts, path
        assert Path(path).name != "verdict_interpretation.yaml", path
        return real_load(path)
    monkeypatch.setattr(rpr, "load_yaml", _guarded_load)
    assert rpr.determine_post_specialist_readers_route(run_dir, RUN_ID) == "completed_rejected"


# ---------------------------------------------------------------------------
# verdict_interpreter is never invoked on the grid route
# ---------------------------------------------------------------------------

def test_full_loop_under_flag_never_invokes_verdict_interpreter(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    _seed_run(pending="protocol_execution", idea_status="refuted")
    rpr._ensure_protocol_ref_pinned(run_dir, RUN_ID, {"protocol_ref": f"protocols/{RUN_ID}_pinned.json"})
    rpr.save_yaml(run_dir / "handoffs" / "backtest_spec_to_protocol_execution.yaml",
                  {"required_inputs": [], "deliverables": []})
    stages = []

    async def _record(stage_name, run_id, retry_context=None):
        stages.append(stage_name)
    monkeypatch.setattr(rpr, "async_invoke_agent", _record)

    rpr.run_loop(RUN_ID)

    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert stages == ["protocol_execution"]
    # D-198: no readers stage; the route is taken in the iteration of protocol_execution
    assert state["completed_stages"][-1] == "protocol_execution"
    assert "specialist_readers" not in state["completed_stages"]
    assert state["pending_stage"] == "completed_rejected"
    assert "verdict_interpreter" not in state["completed_stages"]
    assert not (run_dir / "artifacts" / "verdict_interpretation.yaml").exists()


def test_pending_verdict_interpreter_under_flag_stops_without_invoking(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_run(pending="verdict_interpreter")
    rpr.save_yaml(run_dir / "handoffs" / "protocol_to_verdict_interpreter.yaml",
                  {"required_inputs": [], "deliverables": []})
    invoked = []
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", lambda *a, **k: invoked.append(a[0]))
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert invoked == []
    assert state["status"] == "failed" and "unreached" in state["last_error"]


# ---------------------------------------------------------------------------
# From the review-fixes file: fix 8 (kill) and fix 6 (pre-flight)
# ---------------------------------------------------------------------------

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

