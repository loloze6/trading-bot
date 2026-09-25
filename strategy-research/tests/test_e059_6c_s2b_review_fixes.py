"""
E-059 slice 6c S2b -- regression tests for the code-review fixes of
ca459e72..c0a035ee. Every test here fails on c0a035ee (the tools module
campaign_review_retired is imported inside the tests that need it, so the
others fail on their own assertions there rather than on collection).

  1. A reframe brief takes the pending-at-1a path (criteria_from at brief level
     + the source run's protocol pin): it launches, gets its criteria at 1a and
     never halts at the specialist_readers pre-flight.
  2+4. Cadence: runs since the last COMPLETED review; a missed review carries
     forward, a dropped count never fires twice; a budget stop at the review is
     a classified halt and the review stays pending.
  3. Flag flip: a triggered review resumed with the flag off fails loud; the
     note needs the flag; a reframe brief reaching DONE with the flag off halts.
  5. Registration failures at DONE are classified halts.
  6. campaign_review_terminate outranks the wishlist check.
  7. campaign_decision.yaml is an append-only history with an override entry.
  8. One locked writer for component_requests.yaml.
  9. One definition of the shared constants.
 10. The review reads a code-written digest; a missing KB is optional.
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402

from test_e058_s2a_regroup_record import RUN_ID, _seed, _set_orchestrator  # noqa: E402
from test_profit_bars_every_backtest import _state  # noqa: E402
from test_halt_quarantine_policy import (  # noqa: E402
    campaign_root, _write_fresh_scaffold)  # noqa: F401  (fixture)
from test_e059_s2a_decide_next import _write_flags  # noqa: E402
from test_e059_6c_s2a_route_retirement import RETIRED_ON, PREREQS, FLAT_ON, _forbid  # noqa: E402
from test_e059_6c_s2b_campaign_review import (  # noqa: E402
    _FORBIDDEN, _mem_entry, _write_memory, _prior_runs, _review_ready_run, _stub_review,
    _mark_triggered, _review_log, _finished_reframe_run)

_LOG_REL = "campaign_record/campaign_review_log.yaml"


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _write_log(covered: list) -> None:
    path = rpr.ROOT / _LOG_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({"schema_version": 1, "completed": [
        {"run_id": "run_x", "review_sha256": "s", "recommendation": "continue",
         "covered_runs": covered, "completed_at": "t"}]}), encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. A reframe launches and gets its criteria at 1a
# ---------------------------------------------------------------------------

def test_fix1_reframe_entry_launches_criteria_at_1a_never_the_preflight(campaign_root,
                                                                        monkeypatch):
    root = campaign_root["root"]
    real_loop = rpr.run_loop
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    _finished_reframe_run(campaign_root)
    assert camp.process_once() is True  # DONE: registered; decide-next picks it
    (root / "protocols").mkdir(exist_ok=True)
    (root / "protocols" / "p8.json").write_text("{}", encoding="utf-8")

    def _setup(run_id):
        run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], run_id)
        for stage, deliverable in (("hypothesis_generation", "hypothesis_card.yaml"),
                                   ("strategy_config_authoring", "backtest_spec.yaml")):
            rpr.save_yaml(run_dir / "handoffs" / rpr.STAGE_CONFIGS[stage]["handoff"],
                          {"required_inputs": [], "deliverables": [deliverable]})
    monkeypatch.setattr(camp, "setup_run", _setup)
    stages = []

    async def _agent(stage_name, run_id, retry_context=None):
        stages.append(stage_name)
        if stage_name != "hypothesis_generation":
            raise RuntimeError("stop-after-1a")
        rpr.save_yaml(root / "runs" / run_id / "artifacts" / "hypothesis_card.yaml",
                      {"hypothesis_id": "H-REFRAME", "thesis": "t",
                       "criteria": [{"id": "sign_consistent_by_era"}]})
    monkeypatch.setattr(rpr, "async_invoke_agent", _agent)
    monkeypatch.setattr(rpr, "run_loop", real_loop)

    assert camp.process_once() is False  # halts only on the stub's stop after 1a
    entry = next(e for e in camp._load_queue()["queue"] if e["id"] == "run_061__reframe")
    new_run = entry["run_ids"][-1]
    run_dir = campaign_root["runs_dir"] / new_run
    state = _state(run_dir)
    assert stages == ["hypothesis_generation", "strategy_config_authoring"]
    assert state["last_error"] == "stop-after-1a"  # never the pre-flight
    assert "hypothesis_generation" in state["completed_stages"]
    pre = rpr.load_yaml(run_dir / "artifacts" / "pre_registration.yaml")
    assert [c["id"] for c in pre["pass_rule"]["criteria"]] == ["sign_consistent_by_era"]
    assert pre["pass_rule_source_ref"] == f"runs/{new_run}/artifacts/hypothesis_card.yaml#criteria"
    assert pre["machine_constraints"] == {"protocol_ref": "protocols/p8.json"}
    rpr._check_specialist_readers_preflight(run_dir)  # passes


def test_fix1_brief_level_marker_in_materialize(campaign_root):
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_070")
    brief = {"strategy_domain": "c", "market_universe": "B", "timeframe": "1h",
             "research_goal": "g", "venue": "binance", "product": "perp",
             "criteria_from": "hypothesis_generation",
             "machine_constraints": {"protocol_ref": "protocols/p8.json"}}
    camp._materialize_run("run_070", brief)
    run_dir = campaign_root["runs_dir"] / "run_070"
    pre = rpr.load_yaml(run_dir / "artifacts" / "pre_registration.yaml")
    assert pre["pass_rule_pending"] == "hypothesis_generation" and pre["pass_rule"] is None
    assert rpr._specialist_readers_preflight_deferred(run_dir, "hypothesis_generation") is True


# ---------------------------------------------------------------------------
# 2 + 4. Cadence
# ---------------------------------------------------------------------------

def test_fix2_a_missed_review_carries_forward():
    """7 recorded runs, no review completed (the 6th's was lost): still due."""
    runs = _prior_runs(6, faults=0)
    runs[RUN_ID] = _mem_entry(RUN_ID)
    _write_memory(runs)
    trig = rpr._retired_review_trigger(RUN_ID)
    assert trig is not None and trig["runs_since_last_review"] == 7


def test_fix4_a_count_that_drops_never_fires_twice():
    """A review covered 6 runs; one of them later became a fault. The new run
    makes the total 6 again -- it must not fire a second review."""
    runs = _prior_runs(6, faults=0)
    covered = sorted(runs)
    runs[covered[-1]] = _mem_entry(covered[-1], fault="component_execution_error")
    runs[RUN_ID] = _mem_entry(RUN_ID)
    _write_memory(runs)
    _write_log(covered)
    assert rpr._retired_review_trigger(RUN_ID) is None


def test_fix2_budget_stop_at_review_is_classified_and_stays_pending(tmp_path):
    state = {"status": "rejected_budget_exceeded", "pending_stage": "campaign_review",
             rpr.CAMPAIGN_REVIEW_TRIGGER_KEY: {"since_runs": [RUN_ID]}}
    reason, detail = camp._hard_pause_reason(tmp_path, state)
    assert reason == "budget_breaker" and "still pending" in detail
    # the review never completed, so the next evaluation still counts every run
    runs = _prior_runs(5, faults=0)
    runs[RUN_ID] = _mem_entry(RUN_ID)
    _write_memory(runs)
    assert rpr._retired_review_trigger(RUN_ID)["runs_since_last_review"] == 6


def test_fix2_budget_status_without_the_marker_is_unchanged(tmp_path):
    """Flag-off byte-identity: without the marker the budget status reads as before."""
    assert camp._hard_pause_reason(tmp_path, {"status": "rejected_budget_exceeded",
                                              "pending_stage": "campaign_review"}) is None


# ---------------------------------------------------------------------------
# 3. Flag flip
# ---------------------------------------------------------------------------

def test_fix3_triggered_review_resumed_flag_off_fails_loud(monkeypatch):
    _set_orchestrator(PREREQS)
    run_dir = _seed(pending="campaign_review")
    _mark_triggered(run_dir)
    rpr.save_yaml(run_dir / "handoffs" / "campaign_review.yaml",
                  {"required_inputs": [], "deliverables": ["campaign_review.yaml"]})
    seen = []
    _stub_review(monkeypatch, {"recommendation": "continue"}, seen)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert seen == []
    assert state["status"] == "failed" and "verdict_routing_retired" in state["last_error"]
    assert state["pending_stage"] == "campaign_review"


def test_fix3_note_needs_the_flag_as_well_as_the_marker():
    run_dir = _seed()
    _mark_triggered(run_dir)
    handoff = {"required_inputs": []}
    _set_orchestrator(PREREQS)
    rpr._apply_retired_routing_review_context("campaign_review", handoff, run_dir)
    assert handoff == {"required_inputs": []}
    _set_orchestrator(RETIRED_ON)
    rpr._apply_retired_routing_review_context("campaign_review", handoff, run_dir)
    assert [r["path"] for r in handoff["required_inputs"]] == [rpr._RETIRED_REVIEW_GUIDANCE]


def test_fix3_reframe_brief_at_done_with_the_flag_off_halts(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    run_dir, rel = _finished_reframe_run(campaign_root)
    _write_flags(campaign_root["root"], **{**FLAT_ON, "verdict_routing_retired": False})
    assert camp.process_once() is False
    queue = camp._load_queue()["queue"]
    assert [e["id"] for e in queue] == ["TEST_ENTRY"]
    assert queue[0]["status"] == f"paused:{camp.REFRAME_HALT}"
    assert _state(run_dir)["halt_history"][-1]["reason"] == camp.REFRAME_HALT
    assert camp.resume_paused_entry(camp._load_queue()) is False  # still blocked
    _write_flags(campaign_root["root"], **FLAT_ON)  # flag back on: resumable
    assert camp.resume_paused_entry(camp._load_queue()) is True


# ---------------------------------------------------------------------------
# 5. Registration failures are classified halts
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("damage", ["collision", "missing_brief", "refused"])
def test_fix5_registration_failure_is_a_classified_halt(campaign_root, monkeypatch, damage):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    run_dir, rel = _finished_reframe_run(campaign_root)
    if damage == "collision":
        queue = camp._load_queue()
        queue["queue"].append({"id": "run_061__reframe", "brief_path": "other.md",
                               "status": "done", "outcome": "inconclusive", "priority": 5,
                               "notes": "n", "run_ids": []})
        camp._save_queue(queue)
    elif damage == "missing_brief":
        (campaign_root["root"] / rel).unlink()
    else:
        monkeypatch.setattr(camp, "register_hypothesis", lambda *a, **k: 1)
    assert camp.process_once() is False  # no raw exception
    entry = camp._load_queue()["queue"][0]
    assert entry["status"] == f"paused:{camp.REFRAME_HALT}"
    assert _state(run_dir)["halt_history"][-1]["reason"] == camp.REFRAME_HALT
    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert f"HALT — {camp.REFRAME_HALT}" in log
    assert f"| `{camp.REFRAME_HALT}`" in (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 6. terminate outranks the wishlist check
# ---------------------------------------------------------------------------

def test_fix6_terminate_outranks_the_wishlist_check(tmp_path, monkeypatch):
    (tmp_path / "artifacts").mkdir()
    (tmp_path / "artifacts" / "campaign_review.yaml").write_text(
        yaml.safe_dump({"recommendation": "reframe"}), encoding="utf-8")
    monkeypatch.setattr(camp, "_check_wishlist_trigger", lambda review: "fam")
    monkeypatch.setattr(camp, "evaluate_wishlist_predicate",
                        lambda name: {"result": "false", "detail": "d"})
    state = {"status": "paused_for_human", "pending_stage": "campaign_review",
             "flags": {rpr.CAMPAIGN_REVIEW_TERMINATE_FLAG: True},
             rpr.CAMPAIGN_REVIEW_TRIGGER_KEY: {"since_runs": []}}
    assert camp._hard_pause_reason(tmp_path, state)[0] == "campaign_review_terminate"


# ---------------------------------------------------------------------------
# 7. campaign_decision.yaml history
# ---------------------------------------------------------------------------

def test_fix7_decision_history_records_terminate_then_override():
    legacy = {"decision": "kill", "terminal_run": "run_001"}
    rpr.save_yaml(rpr.ROOT / "campaign_decision.yaml", legacy)
    run_dir = _seed(idea_status="refuted")
    _mark_triggered(run_dir)
    rpr.save_yaml(run_dir / "artifacts" / "campaign_review.yaml",
                  {"recommendation": "terminate", "recommendation_rationale": "spent"})
    assert rpr.determine_post_campaign_review_route(run_dir, RUN_ID, routing_retired=True) == \
        "human_pause"
    doc = rpr.load_yaml(rpr.ROOT / "campaign_decision.yaml")
    assert doc["legacy_decision"] == legacy
    assert [h["event"] for h in doc["history"]] == ["terminate"]
    assert doc["current"]["event"] == "terminate"
    sha = doc["history"][0]["review_sha256"]
    assert doc["history"][0]["run_id"] == RUN_ID and doc["history"][0]["utc"]
    # the operator's continue-anyway resume
    rpr.update_state(path=run_dir, status="active",
                     flags={rpr.CAMPAIGN_REVIEW_TERMINATE_FLAG: False})
    assert rpr.determine_post_campaign_review_route(run_dir, RUN_ID, routing_retired=True) == \
        "completed_refuted"
    doc = rpr.load_yaml(rpr.ROOT / "campaign_decision.yaml")
    assert [h["event"] for h in doc["history"]] == ["terminate", "override_continue"]
    assert doc["history"][1]["review_sha256"] == sha
    assert doc["current"]["event"] == "override_continue"
    # a re-entered route appends nothing (append-only, idempotent)
    rpr.determine_post_campaign_review_route(run_dir, RUN_ID, routing_retired=True)
    assert len(rpr.load_yaml(rpr.ROOT / "campaign_decision.yaml")["history"]) == 2


# ---------------------------------------------------------------------------
# 8 + 9. Shared writer and constants
# ---------------------------------------------------------------------------

def test_fix8_component_requests_share_one_locked_writer(monkeypatch):
    import campaign_review_retired as crr
    import campaign_memory as cm
    import campaign_lock
    src = inspect.getsource(rpr.run_tool_worker)
    assert "_crr.append_component_requests" in src
    assert '"campaign_record" / "component_requests.yaml"' not in src  # no second writer
    assert "_crr.append_component_requests" in inspect.getsource(
        rpr._record_review_component_request)
    path = rpr.ROOT / crr.COMPONENT_REQUESTS_REL
    assert crr.append_component_requests(path, [{"run_id": "a"}]) == 1
    assert crr.append_component_requests(path, [{"run_id": "a"}],
                                         unless=lambda r: r.get("run_id") == "a") == 0
    lock = path.parent / f".{path.stem}.lock"
    campaign_lock.acquire(lock)
    monkeypatch.setattr(cm, "MEMORY_LOCK_WAIT_SECONDS", 0.1)
    try:
        with pytest.raises(crr.CampaignReviewRecordError, match="still held"):
            crr.append_component_requests(path, [{"run_id": "b"}])
    finally:
        campaign_lock.release(lock)
    assert rpr.load_yaml(path) == {"requests": [{"run_id": "a"}]}


def test_fix9_one_definition_of_the_shared_constants():
    import campaign_review_retired as crr
    assert camp.crr is rpr._crr is crr
    assert rpr.REFRAME_BRIEF_REQUIRED_KEYS is crr.REFRAME_BRIEF_REQUIRED_KEYS
    assert rpr.CAMPAIGN_REVIEW_TERMINATE_FLAG is crr.CAMPAIGN_REVIEW_TERMINATE_FLAG
    assert "crr.REFRAME_BRIEF_REQUIRED_KEYS" in inspect.getsource(camp._parse_brief_frontmatter)
    assert "crr.CAMPAIGN_REVIEW_TERMINATE_FLAG" in inspect.getsource(camp._classify_human_pause)


# ---------------------------------------------------------------------------
# 10. A digest, and an optional KB
# ---------------------------------------------------------------------------

def test_fix10_review_reads_a_digest_not_the_whole_memory(monkeypatch):
    _set_orchestrator(RETIRED_ON)
    run_dir = _review_ready_run("refuted", prior=7)
    _write_log(["run_900", "run_901"])  # an earlier review covered two runs
    seen = []
    _stub_review(monkeypatch, {"recommendation": "continue"}, seen)
    _forbid(monkeypatch, _FORBIDDEN)
    rpr.run_loop(RUN_ID)
    (_, handoff), = seen
    paths = [r["path"] for r in handoff["required_inputs"]]
    assert f"artifacts/{rpr.CAMPAIGN_REVIEW_DIGEST_FILE}" in paths
    assert not any("campaign_memory" in p or "campaign_state" in p
                   or "verdict_interpretation" in p for p in paths)
    digest = rpr.load_yaml(run_dir / "artifacts" / rpr.CAMPAIGN_REVIEW_DIGEST_FILE)
    assert sorted(digest["runs_since_last_review"]) == \
        ["run_902", "run_903", "run_904", "run_905", "run_906", RUN_ID]
    assert digest["runs_since_last_review"][RUN_ID]["idea_status"] == "refuted"
    assert digest["earlier_runs"]["count"] == 4  # 2 covered + 2 faults
    assert digest["last_completed_review"]["run_id"] == "run_x"
    covered = _review_log()["completed"][-1]["covered_runs"]
    assert covered == sorted(digest["runs_since_last_review"])


def test_fix10_missing_kb_is_an_optional_input_with_a_note(monkeypatch):
    _set_orchestrator(RETIRED_ON)
    run_dir = _review_ready_run("refuted", kb=False)
    assert not rpr._KB_PATH.exists()
    seen = []
    _stub_review(monkeypatch, {"recommendation": "continue"}, seen)
    _forbid(monkeypatch, _FORBIDDEN)
    rpr.run_loop(RUN_ID)
    (_, handoff), = seen
    assert not any("knowledge_base" in r["path"] for r in handoff["required_inputs"])
    (kb,) = [r for r in handoff["optional_inputs"] if "knowledge_base" in r["path"]]
    assert kb["reason"].startswith("ABSENT")
    assert _state(run_dir)["pending_stage"] == "completed_refuted"
