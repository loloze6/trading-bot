"""
E-059 S3 / slice 6c S2a -- verdict routing retired
(orchestrator.verdict_routing_retired.enabled, off by default). Spec:
engineering/roadmap/E-059/S1_FINDINGS_6C.md §1, §4, §7, §8 (S2a) and its
operator decision of 2026-09-25 (the holdout only through the branch-3 stop plus
an operator unlock, S2d; guesses 2-13 on the S1 defaults).

All synthetic: no LLM, no backtest, no trial row, no holdout.
  1. The flag reader: absent/off, non-bool, both dependencies (decide_next,
     profit_bars_every_backtest), the run_loop pre-flight, the register.
  2. Outcome-list drift: the three completed_<idea_status> endings in every
     list; the halt reason in the RUNBOOK; the legacy marker on every retired
     function.
  3. Flag on, routing: each idea_status -> completed_<status>, status
     `completed`, no pause (inconclusive included), no retired function
     called, no child run, no continuation_child, no holdout; the profit-bars
     stop still fires and a resume ends completed_<status>.
  4. Flag on, process_once: the DONE branch writes the idea status and a
     decide-next record, no child run, the trial ledger untouched.
  5. Guards: legacy routers refuse under the flag; a run found at
     holdout_evaluation is refused; a legacy continuation halts process_once.
  6. Flag off: byte-identical route and process_once continuation.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import campaign_memory as cm  # noqa: E402
import record_schema as rs  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_e058_s2a_regroup_record import (  # noqa: E402
    RUN_ID, _seed, _set_orchestrator)
from test_profit_bars_every_backtest import (  # noqa: E402
    FULL_ON, _loop, _write_bars, _state, _pbe, _single_run)
from test_halt_quarantine_policy import (  # noqa: E402
    _save_queue_entries, _write_campaign_state, _write_fresh_scaffold, _entry,
    campaign_root,  # noqa: F401  (fixture)
)
from test_e059_s2a_decide_next import (  # noqa: E402
    _ALL_ON, _write_flags, _patch, _stage_flag_on_source)

# Every prerequisite of the 6c flag, on (dict-of-dicts shape for _set_orchestrator).
PREREQS = {**FULL_ON, "config_direct_authoring": {"enabled": True},
           "decide_next": {"enabled": True}}
RETIRED_ON = {**PREREQS, "verdict_routing_retired": {"enabled": True}}
# Flat shape for _write_flags (campaign_root sandbox).
FLAT_ON = {**_ALL_ON, "profit_bars_file": True, "profit_bars_every_backtest": True,
           "verdict_routing_retired": True}
STATUSES = ("validated", "refuted", "inconclusive")

# S1_FINDINGS_6C.md §1.2: every retired routing symbol.
LEGACY_FUNCTIONS = (
    "_dispatch_verdict_route", "determine_post_verdict_route", "_route_refine", "_route_pivot",
    "_route_escalate", "_route_kill", "_apply_circuit_breaker", "_create_escalation_protocol",
    "_create_timeframe_protocol", "_resolve_verdict_fields", "_should_trigger_campaign_review",
    "determine_post_campaign_review_route", "_route_campaign_terminate",
)
# Everything that could mint a child run or feed the retired machinery.
_MUST_NOT_RUN = LEGACY_FUNCTIONS + (
    "setup_next_run", "_scaffold_next_run", "record_pivot", "record_escalation",
    "update_campaign_state_after_run", "_mark_campaign_status", "_write_promotion_audit",
    "_route_holdout_evaluation", "_evaluate_profit_bars",
)


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _forbid(monkeypatch, names=_MUST_NOT_RUN):
    def _make(name):
        def _boom(*a, **k):
            raise AssertionError(f"{name} must not run under verdict_routing_retired")
        return _boom
    for n in names:
        monkeypatch.setattr(rpr, n, _make(n))


def _run_dirs() -> set:
    return {p.name for p in (rpr.ROOT / "runs").iterdir() if p.is_dir()}


def _graded_run(idea_status: str, good: bool, pending: str = "regroup_record") -> Path:
    """A run at `pending` whose every_backtest evaluation is on disk, graded by
    the real evaluator: good=True passes every bar (the branch-3 stop fires),
    good=False passes none."""
    _write_bars()
    run_dir = _single_run(good, idea_status=idea_status, pending=pending)
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    assert bool(ev["passing"]) is good
    return run_dir


# ---------------------------------------------------------------------------
# 1. The flag reader
# ---------------------------------------------------------------------------

def test_flag_false_when_absent():
    _set_orchestrator(None)
    assert rpr._verdict_routing_retired_enabled() is False
    _set_orchestrator(PREREQS)
    assert rpr._verdict_routing_retired_enabled() is False


@pytest.mark.parametrize("bad", ["true", None, 1])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**PREREQS, "verdict_routing_retired": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._verdict_routing_retired_enabled()


@pytest.mark.parametrize("missing", ["decide_next", "profit_bars_every_backtest"])
def test_flag_on_without_a_dependency_raises(missing):
    _set_orchestrator({**RETIRED_ON, missing: {"enabled": False}})
    with pytest.raises(ValueError, match=f"requires orchestrator.{missing}.enabled=true"):
        rpr._verdict_routing_retired_enabled()


def test_flag_on_with_every_dependency():
    _set_orchestrator(RETIRED_ON)
    assert rpr._verdict_routing_retired_enabled() is True


def test_run_loop_preflight_fails_before_any_stage(monkeypatch):
    _set_orchestrator({**RETIRED_ON, "profit_bars_every_backtest": {"enabled": False},
                       "profit_bars_file": {"enabled": False}})
    run_dir = _seed(pending="regroup_record")
    ran = []
    monkeypatch.setattr(rpr, "_run_regroup_record_stage", lambda *a, **k: ran.append(a))
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert ran == []
    assert state["status"] == "failed" and "verdict_routing_retired" in state["last_error"]
    assert state["pending_stage"] == "regroup_record"


def test_flag_is_off_in_the_real_config_and_registered():
    cfg = yaml.safe_load((_SR / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["verdict_routing_retired"]["enabled"] is False
    reg = yaml.safe_load((_SR / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    entry = next(f for f in reg["flags"] if f["name"] == "verdict_routing_retired")
    assert entry["state"] == "off_incomplete"
    assert entry["reader"] == "run_phase1_research._verdict_routing_retired_enabled"
    assert entry["config_key"] == "orchestrator.verdict_routing_retired.enabled"


# ---------------------------------------------------------------------------
# 2. Drift: outcome lists, halt reason, legacy markers
# ---------------------------------------------------------------------------

def test_terminals_are_one_per_grid_idea_status():
    assert rpr.RETIRED_ROUTING_TERMINALS == tuple(f"completed_{s}" for s in cm._IDEA_STATUSES)
    assert cm._IDEA_STATUSES == STATUSES


@pytest.mark.parametrize("terminal", ["completed_validated", "completed_refuted",
                                      "completed_inconclusive"])
def test_terminal_is_registered_in_every_outcome_list(terminal):
    # run_loop's terminal check and the queue runner treat it as finished
    assert terminal.startswith(("completed", "rejected", "human_pause", "failed_validation"))
    assert terminal not in rpr.STAGE_CONFIGS
    assert terminal not in camp._LINEAGE_CONTINUATION_STAGES
    if terminal == "completed_inconclusive":
        assert terminal in vce._NON_VERDICT_OUTCOMES
        assert not vce.outcome_is_verdict_bearing(terminal)
        vce.validate_verdict_provenance({"id": "x", "status": "done", "outcome": terminal},
                                        schema=rs.QUEUE_ENTRY_SCHEMA)
    else:  # a claim: it needs provenance, like completed_rejected
        assert terminal in vce._VERDICT_BEARING_OUTCOMES
        assert terminal not in vce._NON_VERDICT_OUTCOMES
        assert vce.outcome_is_verdict_bearing(terminal)
    for doc in ("RUNBOOK.md", "USER_GUIDE.md"):
        assert terminal in (_SR / "docs" / doc).read_text(encoding="utf-8"), doc


def test_legacy_continuation_halt_is_documented_and_schema_valid():
    reason = camp.LEGACY_CONTINUATION_HALT
    assert reason == "legacy_continuation_under_retired_routing"
    assert f"| `{reason}`" in (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    rs.validate_queue_entry({"id": "x", "status": f"paused:{reason}"})


def test_flag_documented_in_guide_runbook_and_index():
    key = "orchestrator.verdict_routing_retired.enabled"
    for rel in ("docs/RUNBOOK.md", "docs/USER_GUIDE.md", "DOC_INDEX.md", "CLAUDE.md"):
        assert key in (_SR / rel).read_text(encoding="utf-8"), rel


@pytest.mark.parametrize("name", LEGACY_FUNCTIONS + ("_LEGACY_STATUS_TO_VERDICT_ROUTING",))
def test_every_retired_symbol_carries_the_legacy_marker(name):
    lines = (_SR / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8").splitlines()
    idx = next(i for i, ln in enumerate(lines)
               if re.match(rf"^(def {name}\(|{name} = )", ln))
    above = "\n".join(lines[max(0, idx - 3):idx])
    assert "# legacy routing (v26 card G)" in above, name


# ---------------------------------------------------------------------------
# 3. Flag on: the route after regroup_record
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status", STATUSES)
def test_route_function_returns_completed_status_and_feeds_nothing(monkeypatch, idea_status):
    _set_orchestrator(RETIRED_ON)
    run_dir = _seed(idea_status=idea_status)
    before_state = (run_dir / "pipeline_state.yaml").read_bytes()
    before_dirs = _run_dirs()
    _forbid(monkeypatch)
    route = rpr.determine_post_specialist_readers_route(run_dir, RUN_ID, routing_retired=True)
    assert route == f"completed_{idea_status}"
    assert (run_dir / "pipeline_state.yaml").read_bytes() == before_state  # no pause, no flag
    assert _run_dirs() == before_dirs
    campaign = rpr.load_campaign_state()
    assert campaign["runs"] == [RUN_ID]
    assert [d["run"] for d in campaign["diagnostics_log"]] == [RUN_ID]
    # a second call duplicates neither the run nor its diagnostics row (a
    # resume re-enters the route; code review item 6)
    rpr.determine_post_specialist_readers_route(run_dir, RUN_ID, routing_retired=True)
    campaign = rpr.load_campaign_state()
    assert campaign["runs"] == [RUN_ID]
    assert [d["run"] for d in campaign["diagnostics_log"]] == [RUN_ID]


def test_route_function_component_errors_still_pause(monkeypatch):
    _set_orchestrator(RETIRED_ON)
    run_dir = _seed(errors_count=2)
    _forbid(monkeypatch)
    assert rpr.determine_post_specialist_readers_route(
        run_dir, RUN_ID, routing_retired=True) == "human_pause"
    assert _state(run_dir)["flags"] == {"component_execution_error_flagged": True}


def test_route_function_refuses_an_unknown_status():
    _set_orchestrator(RETIRED_ON)
    run_dir = _seed()
    with pytest.raises(ValueError, match="not validated/refuted/inconclusive"):
        rpr.determine_post_specialist_readers_route(
            run_dir, RUN_ID, idea={"idea_status": "promote"}, routing_retired=True)


@pytest.mark.parametrize("idea_status", STATUSES)
def test_run_loop_ends_completed_status_after_regroup_record(monkeypatch, idea_status):
    _set_orchestrator(RETIRED_ON)
    run_dir = _graded_run(idea_status, good=False)
    trials_before = rpr.CAMPAIGN_STATE_PATH.read_text(encoding="utf-8")
    before_dirs = _run_dirs()
    _forbid(monkeypatch)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["pending_stage"] == f"completed_{idea_status}"
    assert state["status"] == "completed"
    assert state["completed_stages"][-1] == "regroup_record"
    assert not (state.get("flags") or {})  # inconclusive no longer pauses
    assert "continuation_child" not in state and "continuation_created_by" not in state
    assert _run_dirs() == before_dirs  # no child run scaffolded
    assert "holdout_evaluation" not in state["completed_stages"]
    # trial rows untouched (only the run list / diagnostics are appended)
    before = yaml.safe_load(trials_before)["trial_sharpes"]
    assert rpr.load_campaign_state()["trial_sharpes"] == before
    assert not (run_dir / "artifacts" / "promotion_audit.yaml").exists()


def _continue_decision(run_dir: Path) -> None:
    """Slice 6c S2d: resuming from the stop needs the operator's
    holdout_decision.yaml; `continue` keeps the S2a ending."""
    stop = _state(run_dir)["profit_bars_stop_evaluation"]
    rpr.save_yaml(run_dir / "artifacts" / rpr.HOLDOUT_DECISION_FILE, {
        "decision": "continue", "run_id": RUN_ID, "profit_bars_stop_evaluation": stop,
        "ratified_by": "operator", "ratified_at": "2020-01-01"})


def test_profit_bars_stop_then_resume_ends_completed_validated(monkeypatch):
    """The branch-3 stop is unchanged; after the operator's resume with a
    `continue` decision (slice 6c S2d) the run ends completed_validated --
    never the holdout."""
    _set_orchestrator(RETIRED_ON)
    run_dir = _graded_run("validated", good=True)
    _forbid(monkeypatch)
    rpr.run_loop(RUN_ID)
    paused = _state(run_dir)
    assert paused["status"] == "paused_for_human" and paused["pending_stage"] == "regroup_record"
    assert paused["flags"] == {"profit_bars_reached": True}
    assert camp._classify_human_pause(run_dir, paused) == "profit_bars_reached"
    rpr.update_state(path=run_dir, status="active", flags={"profit_bars_reached": False})
    _continue_decision(run_dir)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["pending_stage"] == "completed_validated" and state["status"] == "completed"
    assert _run_dirs() == {RUN_ID}


def test_full_loop_from_protocol_execution_ends_completed(monkeypatch):
    """End to end through the real per-backtest evaluation and readers (mocked
    LLM): a refuted grid with passing bars stops, then resumes to completed."""
    _write_bars()
    run_dir, stages, _calls = _loop(monkeypatch, RETIRED_ON, good=True)
    assert stages == ["protocol_execution"]
    assert _state(run_dir)["flags"]["profit_bars_reached"] is True
    assert _pbe(run_dir)["passing"] == [RUN_ID]
    rpr.update_state(path=run_dir, status="active", flags={"profit_bars_reached": False})
    _continue_decision(run_dir)
    _forbid(monkeypatch)
    _run_dir, stages, calls = _loop(monkeypatch, RETIRED_ON, fresh=False)
    state = _state(run_dir)
    assert stages == [] and calls == []
    assert state["pending_stage"] == "completed_refuted" and state["status"] == "completed"


# ---------------------------------------------------------------------------
# 4. Flag on: process_once's DONE branch runs decide-next
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status", STATUSES)
def test_process_once_done_branch_decides_next(campaign_root, monkeypatch, idea_status):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    root = campaign_root["root"]
    run_dir = _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1", conf=3)],
                                    idea_status=idea_status)
    _write_flags(root, **FLAT_ON)
    rpr.update_state(path=run_dir, status="completed", pending_stage=f"completed_{idea_status}")
    ledger_before = campaign_root["campaign_state_path"].read_bytes()
    dirs_before = {p.name for p in campaign_root["runs_dir"].iterdir()}

    assert camp.process_once() is True
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    done, new = queue
    assert done["status"] == "done" and done["outcome"] == idea_status
    vce.validate_verdict_provenance(done, root=root, schema=rs.QUEUE_ENTRY_SCHEMA)
    assert new["status"] == "ready" and new["origin"] == "reader"
    assert (run_dir / "artifacts" / "decision_record.yaml").exists()
    assert {p.name for p in campaign_root["runs_dir"].iterdir()} == dirs_before
    assert campaign_root["campaign_state_path"].read_bytes() == ledger_before
    log = (root / "campaign_log.md").read_text(encoding="utf-8")
    assert f"DONE TEST_ENTRY (run_061) -> {idea_status}" in log
    assert "CONTINUE" not in log


# ---------------------------------------------------------------------------
# 5. Guards
# ---------------------------------------------------------------------------

def test_dispatch_refuses_on_the_passed_flag_only(monkeypatch):
    """Code review items 4 + 8: ONE refusal, in _dispatch_verdict_route, keyed on
    the flag run_loop resolved -- never a live re-read of the config."""
    _set_orchestrator(RETIRED_ON)
    run_dir = _seed()
    monkeypatch.setattr(rpr, "_verdict_routing_retired_enabled",
                        lambda: (_ for _ in ()).throw(AssertionError("re-read inside a run")))
    with pytest.raises(RuntimeError, match="legacy verdict routing"):
        rpr._dispatch_verdict_route(run_dir, RUN_ID, {}, {}, "promote", None,
                                    routing_retired=True)
    assert not (run_dir / "artifacts" / "promotion_audit.yaml").exists()


def test_single_refusal_site_per_entry_point():
    """Code review item 8: no guards on guards -- the old live-reading helper is
    gone, and neither determine_post_verdict_route nor
    determine_post_campaign_review_route carries a refusal of its own."""
    import inspect
    assert not hasattr(rpr, "_refuse_under_retired_routing")
    for fn in (rpr.determine_post_verdict_route, rpr.determine_post_campaign_review_route):
        src = inspect.getsource(fn)
        assert "_verdict_routing_retired_enabled" not in src, fn.__name__
        assert "legacy verdict routing" not in src, fn.__name__
    assert "legacy verdict routing" in inspect.getsource(rpr._dispatch_verdict_route)


def test_run_loop_reads_the_flag_once(monkeypatch):
    """Code review item 4: the pre-flight is the only reading inside a run."""
    _set_orchestrator(RETIRED_ON)
    run_dir = _graded_run("refuted", good=False)
    real, calls = rpr._verdict_routing_retired_enabled, []

    def _counted():
        calls.append(1)
        return real()
    monkeypatch.setattr(rpr, "_verdict_routing_retired_enabled", _counted)
    rpr.run_loop(RUN_ID)
    assert _state(run_dir)["pending_stage"] == "completed_refuted"
    assert len(calls) == 1


def test_holdout_without_result_pauses_classified_and_spends_nothing(monkeypatch):
    """Code review items 1 + 7: no holdout_result.yaml -> refused, as its own
    classified pause (never unhandled_exception, never the 'run the holdout'
    row even though promotion_audit.yaml exists)."""
    _set_orchestrator(RETIRED_ON)
    run_dir = _seed(idea_status="validated", pending="holdout_evaluation")
    rpr.save_yaml(run_dir / "artifacts" / "promotion_audit.yaml", {"hypothesis_id": "H-MEM-1"})
    policy = rpr._DATA_POLICY_PATH
    policy_before = policy.read_bytes() if policy.exists() else None
    _forbid(monkeypatch)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["status"] == "paused_for_human" and state["pending_stage"] == "holdout_evaluation"
    assert state["flags"] == {rpr.HOLDOUT_REFUSED_FLAG: True}
    assert camp._classify_human_pause(run_dir, state) == "holdout_refused_under_retired_routing"
    assert camp._hard_pause_reason(run_dir, state)[0] == "holdout_refused_under_retired_routing"
    assert (policy.read_bytes() if policy.exists() else None) == policy_before


@pytest.mark.parametrize("result,terminal", [("fail", "completed_rejected"),
                                             ("pass", "completed_promoted")])
def test_holdout_already_spent_is_recorded_then_the_run_ends(monkeypatch, result, terminal):
    """Code review item 1: holdout_result.yaml present = the seal was spent by
    hand. Only the consume record runs (once), then the run ends; no other
    holdout gate runs."""
    _set_orchestrator(RETIRED_ON)
    run_dir = _seed(idea_status="validated", pending="holdout_evaluation")
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": result})
    rpr.save_yaml(rpr._DATA_POLICY_PATH, {"holdout_range": ["a", "b"],
                                          "holdout_consumed_by": ["H-OTHER"]})
    _forbid(monkeypatch)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["pending_stage"] == terminal
    assert state["completed_stages"][-1] == "holdout_evaluation"
    policy = rpr.load_yaml(rpr._DATA_POLICY_PATH)
    assert policy["holdout_consumed_by"] == ["H-OTHER", "H-MEM-1"]
    assert policy["holdout_range"] == ["a", "b"]
    # recorded once: a second pass over the same run does not append again
    rpr.update_state(path=run_dir, pending_stage="holdout_evaluation", status="active")
    rpr.run_loop(RUN_ID)
    assert rpr.load_yaml(rpr._DATA_POLICY_PATH)["holdout_consumed_by"] == ["H-OTHER", "H-MEM-1"]


def test_campaign_review_stage_is_refused_before_any_llm_call(monkeypatch):
    _set_orchestrator(RETIRED_ON)
    run_dir = _seed(idea_status="refuted", pending="campaign_review")
    calls = []

    async def _record(stage_name, run_id, retry_context=None):
        calls.append(stage_name)
    monkeypatch.setattr(rpr, "async_invoke_agent", _record)
    monkeypatch.setattr(rpr, "_invoke_agent_with_yaml_retry", lambda *a, **k: calls.append(a))
    _forbid(monkeypatch)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert calls == []
    assert state["status"] == "paused_for_human" and state["pending_stage"] == "campaign_review"
    assert camp._classify_human_pause(run_dir, state) == \
        "campaign_review_refused_under_retired_routing"


@pytest.mark.parametrize("reason", ["holdout_refused_under_retired_routing",
                                    "campaign_review_refused_under_retired_routing",
                                    "refinement_brief_under_retired_routing",
                                    "idea_status_missing_at_done"])
def test_new_halt_reasons_have_runbook_rows(reason):
    assert f"| `{reason}`" in (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    rs.validate_queue_entry({"id": "x", "status": f"paused:{reason}"})


def test_refusal_flags_mirror_the_pause_table():
    table = dict(camp._PAUSE_FLAG_TO_REASON)
    for flag in (rpr.HOLDOUT_REFUSED_FLAG, rpr.CAMPAIGN_REVIEW_REFUSED_FLAG):
        assert table[flag] == flag == camp._classify_human_pause(Path("."), {"flags": {flag: True}})


def test_kill_route_readers_branch_uses_the_shared_bookkeeping(monkeypatch):
    """Code review item 9: one helper for the campaign_state bookkeeping."""
    _set_orchestrator(RETIRED_ON)
    run_dir = _seed()
    seen = []
    monkeypatch.setattr(rpr, "_record_run_in_campaign_state",
                        lambda run_id, diag: seen.append(run_id))
    assert rpr._route_kill(run_dir, RUN_ID, {}, {}) == "completed_rejected"
    assert rpr._route_retired_idea_status(run_dir, RUN_ID, {"idea_status": "refuted"}) == \
        "completed_refuted"
    assert seen == [RUN_ID, RUN_ID]


def test_generic_strict_flag_reader():
    """Code review item 10."""
    _set_orchestrator({"a": {"enabled": True}, "b": {"enabled": "yes"}})
    assert rpr._strict_orchestrator_flag("absent") is False
    assert rpr._strict_orchestrator_flag("a", requires=(("x", lambda: True),)) is True
    with pytest.raises(ValueError, match=r"requires orchestrator\.x\.enabled=true as well -- w"):
        rpr._strict_orchestrator_flag("a", requires=(("x", lambda: False),), why="w")
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._strict_orchestrator_flag("b")


def _legacy_continuation(campaign_root, flags):
    root = campaign_root["root"]
    _write_flags(root, **flags)
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_912", status="active",
                          pending_stage="completed_refined", continuation_child="run_913",
                          continuation_created_by="_route_refine")
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_913")
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_912")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_912"], trial_sharpes=[])


def test_legacy_continuation_halts_under_the_flag(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    _legacy_continuation(campaign_root, FLAT_ON)
    assert camp.process_once() is False
    entry = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert entry["status"] == "paused:legacy_continuation_under_retired_routing"
    assert entry["run_ids"] == ["run_912"]  # the child is not followed
    state = yaml.safe_load((campaign_root["runs_dir"] / "run_912" / "pipeline_state.yaml")
                           .read_text(encoding="utf-8"))
    assert state["halt_history"][-1]["reason"] == "legacy_continuation_under_retired_routing"
    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert "HALT — legacy_continuation_under_retired_routing" in log and "CONTINUE" not in log


@pytest.mark.parametrize("flags", [None, {**_ALL_ON, "profit_bars_file": True,
                                          "profit_bars_every_backtest": True,
                                          "verdict_routing_retired": False}])
def test_flag_off_legacy_continuation_is_followed_as_before(campaign_root, monkeypatch, flags):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    _legacy_continuation(campaign_root, flags or {})
    assert camp.process_once() is True
    entry = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert entry["status"] == "in_progress" and entry["run_ids"] == ["run_912", "run_913"]
    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert "CONTINUE TEST_ENTRY lineage run_912 -> run_913 (completed_refined)" in log


def _minted_child_entry(campaign_root, flags):
    """The realistic legacy case: the queue already followed run_913, which
    run_912's legacy refine minted; run_913 itself is mid-pipeline."""
    _write_flags(campaign_root["root"], **flags)
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_912", status="active",
                          pending_stage="completed_refined", continuation_child="run_913",
                          continuation_created_by="_route_refine")
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_913", status="active",
                          pending_stage="hypothesis_generation")
    entry = {**_entry("run_912"), "run_ids": ["run_912", "run_913"]}
    _save_queue_entries(campaign_root["queue_path"], [entry])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_912"], trial_sharpes=[])


def test_continue_action_on_a_legacy_minted_run_halts_before_run_loop(campaign_root, monkeypatch):
    """Code review item 2."""
    ran = []
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: ran.append(run_id))
    _minted_child_entry(campaign_root, FLAT_ON)
    assert camp.process_once() is False
    assert ran == []
    entry = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert entry["status"] == "paused:legacy_continuation_under_retired_routing"
    state = yaml.safe_load((campaign_root["runs_dir"] / "run_913" / "pipeline_state.yaml")
                           .read_text(encoding="utf-8"))
    assert state["halt_history"][-1]["reason"] == "legacy_continuation_under_retired_routing"
    assert "run_912's continuation_child is 'run_913'" in state["halt_history"][-1]["detail"]


def test_continue_action_flag_off_runs_the_minted_run_as_before(campaign_root, monkeypatch):
    ran = []
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: ran.append(run_id))
    _minted_child_entry(campaign_root, {})
    camp.process_once()
    assert ran == ["run_913"]


def test_resume_stays_blocked_until_the_legacy_continuation_is_resolved(campaign_root, monkeypatch):
    """Code review item 7: --resume re-checks the halt's own condition."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    _minted_child_entry(campaign_root, FLAT_ON)
    camp.process_once()
    queue = camp._load_queue()
    assert camp.resume_paused_entry(queue) is False
    assert queue["queue"][0]["status"] == "paused:legacy_continuation_under_retired_routing"
    # the operator drops the minted run from the lineage and clears the pointer
    rpr.update_state(path=campaign_root["runs_dir"] / "run_912", continuation_child=None,
                     continuation_created_by=None)
    queue["queue"][0]["run_ids"] = ["run_912"]
    rpr.update_state(path=campaign_root["runs_dir"] / "run_912", pending_stage="completed_rejected")
    camp._save_queue(queue)
    queue = camp._load_queue()
    assert camp.resume_paused_entry(queue) is True


def test_refinement_brief_action_halts_without_scaffolding(campaign_root, monkeypatch):
    """Code review item 3."""
    ran, scaffolded = [], []
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: ran.append(run_id))
    monkeypatch.setattr(camp, "setup_run", lambda run_id: scaffolded.append(run_id))
    _write_flags(campaign_root["root"], **FLAT_ON)
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_912", status="rejected",
                          pending_stage="completed_rejected")
    entry = {**_entry("run_912"), "refinement_brief_path": "briefs/refine.yaml"}
    _save_queue_entries(campaign_root["queue_path"], [entry])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_912"], trial_sharpes=[])
    assert camp.process_once() is False
    assert ran == [] and scaffolded == []
    queue = camp._load_queue()
    assert queue["queue"][0]["status"] == "paused:refinement_brief_under_retired_routing"
    assert queue["queue"][0]["run_ids"] == ["run_912"]
    assert camp.resume_paused_entry(queue) is False  # still carries the brief path


@pytest.mark.parametrize("damage", ["missing", "unreadable", "mismatch"])
def test_done_fails_closed_without_a_matching_idea_status(campaign_root, monkeypatch, damage):
    """Code review item 5: never recorded `ungated` under the flag."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    run_dir = _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")],
                                    idea_status="validated")
    _write_flags(campaign_root["root"], **FLAT_ON)
    rpr.update_state(path=run_dir, status="completed", pending_stage="completed_validated")
    ref = run_dir / "artifacts" / "idea_status.yaml"
    if damage == "missing":
        ref.unlink()
    elif damage == "unreadable":
        ref.write_text("idea_status: [unclosed\n", encoding="utf-8")
    else:
        ref.write_text(yaml.safe_dump({"idea_status": "refuted"}), encoding="utf-8")
    assert camp.process_once() is False
    entry = camp._load_queue()["queue"][0]
    assert entry["status"] == "paused:idea_status_missing_at_done"
    assert "verdict_status" not in entry and entry.get("outcome") is None
    assert not (run_dir / "artifacts" / "decision_record.yaml").exists()
    assert camp.resume_paused_entry(camp._load_queue()) is False


# ---------------------------------------------------------------------------
# 6. Flag off: the route is byte-identical
# ---------------------------------------------------------------------------

def _strip(state: dict) -> dict:
    return {k: v for k, v in state.items() if k not in ("updated_at", "last_updated")}


@pytest.mark.parametrize("idea_status,expected", [
    ("validated", "holdout_evaluation"), ("refuted", "completed_rejected"),
    ("inconclusive", "regroup_record")])
def test_flag_off_route_is_unchanged(monkeypatch, idea_status, expected):
    """Absent and explicit `false` give the same run state as each other and as
    the pre-6c route (validated -> holdout, refuted -> rejected, inconclusive
    -> the inconclusive_grid pause)."""
    # A validated route continues into holdout_evaluation; stop there without running it.
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "holdout_evaluation",
                        {**rpr.STAGE_CONFIGS["holdout_evaluation"], "handoff": "missing.yaml"})
    seen = []
    for cfg in (PREREQS, {**PREREQS, "verdict_routing_retired": {"enabled": False}}):
        _set_orchestrator(cfg)
        run_dir = _graded_run(idea_status, good=False)
        if idea_status == "validated":
            with pytest.raises(FileNotFoundError):
                rpr.run_loop(RUN_ID)
        else:
            rpr.run_loop(RUN_ID)
        state = _state(run_dir)
        assert state["pending_stage"] == expected
        assert "continuation_child" not in state
        seen.append(_strip(state))
    assert seen[0] == seen[1]
    if idea_status == "inconclusive":
        assert seen[0]["status"] == "paused_for_human"
        assert seen[0]["flags"] == {"inconclusive_grid": True}
