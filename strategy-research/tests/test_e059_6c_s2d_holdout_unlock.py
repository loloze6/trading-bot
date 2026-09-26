"""
E-059 S3 / slice 6c S2d -- the holdout unlock (orchestrator.verdict_routing_retired
.enabled, off by default). Spec: engineering/roadmap/E-059/S1_FINDINGS_6C.md,
guess 1 and the operator decision of 2026-09-25: the holdout is reached ONLY
through branch 3 (a backtest passes every profit bar -> the profit_bars_reached
stop -> the operator resumes with artifacts/holdout_decision.yaml). The grid's
idea_status is never a precondition and never leads there by itself.

All synthetic: no LLM, no backtest, no sealed data. The "holdout backtest" is a
hand-written holdout_result.yaml fixture; the data policy is a sandbox file with
placeholder range strings (conftest redirects _DATA_POLICY_PATH).
  1. Flag off: byte-identical, whatever holdout_decision.yaml says.
  2. spend: the happy path through every existing holdout guard, the variant
     recorded, the marker written once.
  3. Refusals: each code, as a classified pause that spends nothing.
  4. Branch 1 never reaches the holdout: a validated idea with no profit stop.
  5. continue -> completed_<idea_status> -> decide-next.
  6. The consume marker across crash/resume: exactly once, right outcome.
  7. --resume refuses early; drift (RUNBOOK rows, pause table, docs, codes).
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import record_schema as rs  # noqa: E402

from test_e058_s2a_regroup_record import RUN_ID, _set_orchestrator  # noqa: E402
from test_profit_bars_every_backtest import (  # noqa: E402
    _VALID_BARS, _write_bars, _single_run, _state)
from test_e059_6c_s2a_route_retirement import (  # noqa: E402
    PREREQS, RETIRED_ON, FLAT_ON, _MUST_NOT_RUN, _forbid)
from test_halt_quarantine_policy import (  # noqa: E402
    _save_queue_entries, _entry,
    campaign_root,  # noqa: F401  (fixture)
)
from test_e059_s2a_decide_next import _write_flags, _patch, _stage_flag_on_source  # noqa: E402

HYP = "H-MEM-1"  # _seed's hypothesis_card.yaml
RATIFIED = {**_VALID_BARS, "ratified_by": "operator", "ratified_at": "2020-01-01"}
# Everything that must never run on these paths, except the holdout gate itself.
_NOT_THE_GATE = tuple(n for n in _MUST_NOT_RUN if n != "_route_holdout_evaluation")


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _policy(consumed=()) -> None:
    rpr.save_yaml(rpr._DATA_POLICY_PATH, {"holdout_range": ["range-start", "range-end"],
                                          "holdout_consumed_by": list(consumed)})


def _consumed() -> list:
    return rpr.load_yaml(rpr._DATA_POLICY_PATH).get("holdout_consumed_by") or []


def _stopped_run(idea_status="validated", good=True, orchestrator=RETIRED_ON,
                 bars=RATIFIED, tradable=True) -> Path:
    """A run at regroup_record whose every_backtest evaluation is graded by the
    real evaluator under `bars`; run_loop is run once, so a passing variant
    raises the profit_bars_reached stop."""
    _set_orchestrator(orchestrator)
    _write_bars(bars)
    run_dir = _single_run(good, idea_status=idea_status)
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    brief = {"research_only": False} if tradable else {}
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", brief)
    _policy()
    rpr.run_loop(RUN_ID)
    return run_dir


def _decision(run_dir, decision="spend", **over) -> Path:
    doc = {"decision": decision, "run_id": RUN_ID,
           "profit_bars_stop_evaluation": _state(run_dir).get("profit_bars_stop_evaluation"),
           "variant_id": RUN_ID, "ratified_by": "operator", "ratified_at": "2020-01-01"}
    doc.update(over)
    doc = {k: v for k, v in doc.items() if v is not _DROP}
    path = run_dir / "artifacts" / rpr.HOLDOUT_DECISION_FILE
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


_DROP = object()


def _resume(run_dir, *flags) -> None:
    """RUNBOOK §4: status active and the pause's flags cleared, then run_loop."""
    rpr.update_state(path=run_dir, status="active", last_error=None,
                     flags={f: False for f in ("profit_bars_reached",) + flags})
    rpr.run_loop(RUN_ID)


def _strip(state: dict) -> dict:
    return {k: v for k, v in state.items() if k not in ("updated_at", "last_updated")}


# ---------------------------------------------------------------------------
# 1. Flag off: byte-identical
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status,expected", [("refuted", "completed_rejected"),
                                                  ("validated", "holdout_evaluation")])
def test_flag_off_resume_ignores_the_decision_file(monkeypatch, idea_status, expected):
    """Flag off (absent and explicit false): the resume from the stop follows
    the legacy route exactly as without the file -- no new state key, no new
    flag, the data policy untouched by S2d."""
    # the legacy validated route continues into holdout_evaluation: stop there
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "holdout_evaluation",
                        {**rpr.STAGE_CONFIGS["holdout_evaluation"], "handoff": "missing.yaml"})
    seen = []
    for cfg in (PREREQS, {**PREREQS, "verdict_routing_retired": {"enabled": False}}):
        for with_file in (False, True):
            run_dir = _stopped_run(idea_status, orchestrator=cfg)
            assert _state(run_dir)["flags"] == {"profit_bars_reached": True}
            if with_file:
                _decision(run_dir, "spend")
            policy_before = rpr._DATA_POLICY_PATH.read_bytes()
            if expected == "holdout_evaluation":
                with pytest.raises(FileNotFoundError):
                    _resume(run_dir)
            else:
                _resume(run_dir)
            state = _state(run_dir)
            assert state["pending_stage"] == expected
            for key in (rpr.HOLDOUT_DECISION_RECORD_KEY, rpr.HOLDOUT_CONSUME_RECORD_KEY,
                        rpr.HOLDOUT_UNLOCK_REFUSAL_KEY):
                assert key not in state
            assert rpr._DATA_POLICY_PATH.read_bytes() == policy_before
            state.pop("profit_bars_stop_evaluation")
            seen.append(_strip(state))
    assert all(s == seen[0] for s in seen[1:])


def test_flag_off_holdout_gate_signature_is_unchanged(monkeypatch):
    """The legacy gate called as every flag-off caller calls it (no
    before_consume) writes the marker exactly as before."""
    _set_orchestrator(PREREQS)
    run_dir = _stopped_run("validated", orchestrator=PREREQS)
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": "pass"})
    assert rpr._route_holdout_evaluation(run_dir, RUN_ID) == "completed_promoted"
    assert _consumed() == [HYP]
    assert rpr.HOLDOUT_CONSUME_RECORD_KEY not in _state(run_dir)


# ---------------------------------------------------------------------------
# 2. spend: the happy path
# ---------------------------------------------------------------------------

def test_spend_happy_path_every_guard_then_recorded_once(monkeypatch):
    run_dir = _stopped_run("validated")
    _forbid(monkeypatch, _NOT_THE_GATE)
    gate_calls = []
    real_gate = rpr._route_holdout_evaluation

    def _gate(*a, **k):
        gate_calls.append(k.get("before_consume") is not None)
        return real_gate(*a, **k)
    monkeypatch.setattr(rpr, "_route_holdout_evaluation", _gate)
    _decision(run_dir, "spend", note="the one we pre-registered")

    # resume: unlocked -> holdout_evaluation -> the gate pauses for the manual backtest
    _resume(run_dir)
    state = _state(run_dir)
    assert state["status"] == "paused_for_human" and state["pending_stage"] == "holdout_evaluation"
    assert state["flags"][rpr.HOLDOUT_AWAITING_RESULT_FLAG] is True
    assert camp._classify_human_pause(run_dir, state) == rpr.HOLDOUT_AWAITING_RESULT_FLAG
    rec = state[rpr.HOLDOUT_DECISION_RECORD_KEY]
    assert rec["decision"] == "spend" and rec["variant_id"] == RUN_ID
    assert rec["trial_id"] == RUN_ID and rec["hypothesis_id"] == HYP
    assert rec["protocol_result_ref"].endswith("protocol_result.yaml")
    assert rec["ratified_by"] == "operator" and rec["note"] == "the one we pre-registered"
    assert _consumed() == []  # nothing spent yet
    assert "regroup_record" in state["completed_stages"]
    assert rpr.load_campaign_state()["runs"] == [RUN_ID]  # bookkeeping kept

    # the operator runs the holdout backtest by hand and writes the result
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": "pass"})
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    state = _state(run_dir)
    assert state["pending_stage"] == "completed_promoted"
    assert state["completed_stages"][-1] == "holdout_evaluation"
    assert _consumed() == [HYP]
    consume = state[rpr.HOLDOUT_CONSUME_RECORD_KEY]
    assert consume["hypothesis_id"] == HYP and consume["variant_id"] == RUN_ID
    assert consume["decision_sha256"] == rec["decision_sha256"]
    assert gate_calls == [True, True]  # the existing gate, both passes

    # a stray re-entry never writes the marker again
    rpr.update_state(path=run_dir, status="active", pending_stage="holdout_evaluation")
    rpr.run_loop(RUN_ID)
    assert _consumed() == [HYP]
    assert _state(run_dir)["pending_stage"] == "completed_promoted"


def test_spend_on_a_refuted_idea_reaches_the_gate(monkeypatch):
    """Grid validation is NOT a precondition (operator decision): a refuted
    idea whose variant passed every bar may be spent on."""
    run_dir = _stopped_run("refuted")
    _forbid(monkeypatch, _NOT_THE_GATE)
    _decision(run_dir, "spend")
    _resume(run_dir)
    assert _state(run_dir)[rpr.HOLDOUT_DECISION_RECORD_KEY]["decision"] == "spend"
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": "fail"})
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    state = _state(run_dir)
    assert state[rpr.HOLDOUT_CONSUME_RECORD_KEY]["variant_id"] == RUN_ID
    assert state["pending_stage"] == "completed_rejected" and state["status"] == "rejected"
    assert _consumed() == [HYP]


def test_spend_still_meets_the_research_only_hold(monkeypatch):
    """The existing guards run unchanged: an undeclared brief holds before
    anyone is told to run the holdout."""
    run_dir = _stopped_run("validated", tradable=False)
    _forbid(monkeypatch, _NOT_THE_GATE)
    _decision(run_dir, "spend")
    _resume(run_dir)
    state = _state(run_dir)
    assert state["pending_stage"] == "holdout_evaluation"
    assert camp._classify_human_pause(run_dir, state) == "research_only_unverified"
    assert not state["flags"].get(rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    assert _consumed() == []


def test_inconclusive_holdout_result_pauses_classified_then_finishes(monkeypatch):
    run_dir = _stopped_run("validated")
    _decision(run_dir, "spend")
    _resume(run_dir)
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": "unclear"})
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    state = _state(run_dir)
    assert state["pending_stage"] == "holdout_evaluation" and state["status"] == "paused_for_human"
    assert camp._classify_human_pause(run_dir, state) == rpr.HOLDOUT_RESULT_INCONCLUSIVE_FLAG
    assert _consumed() == [HYP]  # spent and recorded, like the legacy gate
    # the operator corrects the result: only the record step runs, no second write
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": "pass"})
    _resume(run_dir, rpr.HOLDOUT_RESULT_INCONCLUSIVE_FLAG)
    assert _state(run_dir)["pending_stage"] == "completed_promoted"
    assert _consumed() == [HYP]


# ---------------------------------------------------------------------------
# 3. Refusals: a classified pause, nothing spent, the gate never entered
# ---------------------------------------------------------------------------

def _stale(run_dir):
    _decision(run_dir, profit_bars_stop_evaluation="another-stop")


def _unratified_after(run_dir):
    _write_bars({**RATIFIED, "ratified_by": None, "ratified_at": None})
    _decision(run_dir)


def _threshold_moved(run_dir):
    _write_bars({**RATIFIED, "sharpe_min": 0.4})
    _decision(run_dir)


_REFUSALS = {
    "missing": ("decision_missing", lambda d: None),
    "unparseable": ("decision_malformed", lambda d: (d / "artifacts" / rpr.HOLDOUT_DECISION_FILE)
                    .write_text("decision: [spend\n", encoding="utf-8")),
    "not_a_mapping": ("decision_malformed", lambda d: (d / "artifacts" / rpr.HOLDOUT_DECISION_FILE)
                      .write_text("- spend\n", encoding="utf-8")),
    "unknown_key": ("decision_malformed", lambda d: _decision(d, varient_id="x")),
    "bad_decision": ("decision_malformed", lambda d: _decision(d, "maybe")),
    "no_ratified_by": ("decision_malformed", lambda d: _decision(d, ratified_by=_DROP)),
    "bad_ratified_at": ("decision_malformed", lambda d: _decision(d, ratified_at="yesterday")),
    "spend_without_variant": ("decision_malformed", lambda d: _decision(d, variant_id=_DROP)),
    "wrong_run": ("decision_wrong_run", lambda d: _decision(d, run_id="run_999")),
    "stale": ("decision_stale", _stale),
    "no_pass": ("variant_not_passing", lambda d: _decision(d, variant_id="not-a-variant")),
    "already_consumed": ("holdout_already_consumed",
                         lambda d: (_policy([HYP]), _decision(d))),
    "bars_unratified": ("bars_unratified", _unratified_after),
    "bars_changed": ("bars_changed", _threshold_moved),
}


@pytest.mark.parametrize("case", sorted(_REFUSALS))
def test_refused_resume_spends_nothing(monkeypatch, case):
    code, write = _REFUSALS[case]
    run_dir = _stopped_run("validated")
    _forbid(monkeypatch)  # the holdout gate included
    write(run_dir)
    policy_before = rpr._DATA_POLICY_PATH.read_bytes()
    _resume(run_dir)
    state = _state(run_dir)
    assert state["status"] == "paused_for_human" and state["pending_stage"] == "regroup_record"
    assert state["flags"][rpr.HOLDOUT_UNLOCK_REFUSED_FLAG] is True
    assert state[rpr.HOLDOUT_UNLOCK_REFUSAL_KEY]["code"] == code
    assert rpr.HOLDOUT_DECISION_RECORD_KEY not in state or \
        state[rpr.HOLDOUT_DECISION_RECORD_KEY] is None
    assert camp._classify_human_pause(run_dir, state) == rpr.HOLDOUT_UNLOCK_REFUSED_FLAG
    reason, detail = camp._hard_pause_reason(run_dir, state)
    assert reason == rpr.HOLDOUT_UNLOCK_REFUSED_FLAG and detail.startswith(f"{code}: ")
    assert rpr._DATA_POLICY_PATH.read_bytes() == policy_before
    assert "holdout_evaluation" not in (state.get("completed_stages") or [])


def test_refusal_on_an_unratified_evaluation_even_when_the_file_is_ratified_later(monkeypatch):
    """Graded under placeholder bars, ratified afterwards: the ratification
    differs from the evaluation's -> bars_changed (never spent on numbers
    graded before the bars were an operator decision)."""
    run_dir = _stopped_run("validated", bars={**RATIFIED, "ratified_by": None,
                                              "ratified_at": None})
    _forbid(monkeypatch)
    _write_bars(RATIFIED)
    _decision(run_dir)
    _resume(run_dir)
    assert _state(run_dir)[rpr.HOLDOUT_UNLOCK_REFUSAL_KEY]["code"] == "bars_changed"


def test_fixed_decision_after_a_refusal_proceeds(monkeypatch):
    run_dir = _stopped_run("validated")
    _decision(run_dir, run_id="run_999")
    _resume(run_dir)
    assert _state(run_dir)[rpr.HOLDOUT_UNLOCK_REFUSAL_KEY]["code"] == "decision_wrong_run"
    _decision(run_dir, "continue")
    _resume(run_dir, rpr.HOLDOUT_UNLOCK_REFUSED_FLAG)
    state = _state(run_dir)
    assert state["pending_stage"] == "completed_validated"
    assert state.get(rpr.HOLDOUT_UNLOCK_REFUSAL_KEY) is None
    assert not state["flags"].get(rpr.HOLDOUT_UNLOCK_REFUSED_FLAG)


def test_decision_edited_after_the_unlock_is_refused_before_the_backtest(monkeypatch):
    run_dir = _stopped_run("validated")
    _decision(run_dir, "spend")
    _resume(run_dir)
    assert _state(run_dir)["flags"][rpr.HOLDOUT_AWAITING_RESULT_FLAG] is True
    _decision(run_dir, "spend", note="edited")
    _forbid(monkeypatch)
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    state = _state(run_dir)
    assert state["pending_stage"] == "holdout_evaluation"
    assert state[rpr.HOLDOUT_UNLOCK_REFUSAL_KEY]["code"] == "decision_changed"
    assert state.get(rpr.HOLDOUT_DECISION_RECORD_KEY) is None
    assert _consumed() == []
    # with the record dropped, a plain resume is the S2a refusal, never the gate
    _resume(run_dir, rpr.HOLDOUT_UNLOCK_REFUSED_FLAG)
    assert camp._classify_human_pause(run_dir, _state(run_dir)) == \
        "holdout_refused_under_retired_routing"
    assert _consumed() == []


def test_a_hand_written_unlock_for_another_stop_is_refused(monkeypatch):
    """A decision record not bound to the run's current stop never unlocks
    the gate: the S2a refusal applies."""
    run_dir = _stopped_run("validated")
    _forbid(monkeypatch)
    rpr.update_state(path=run_dir, status="active", pending_stage="holdout_evaluation",
                     **{rpr.HOLDOUT_DECISION_RECORD_KEY: {
                         "decision": "spend", "run_id": RUN_ID,
                         "profit_bars_stop_evaluation": "another-stop",
                         "variant_id": RUN_ID, "decision_sha256": "x"}})
    rpr.run_loop(RUN_ID)
    assert camp._classify_human_pause(run_dir, _state(run_dir)) == \
        "holdout_refused_under_retired_routing"
    assert _consumed() == []


# ---------------------------------------------------------------------------
# 4. Branch 1 never reaches the holdout
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status", ["validated", "refuted", "inconclusive"])
def test_no_profit_stop_never_reaches_the_holdout_even_with_a_spend_file(monkeypatch,
                                                                         idea_status):
    run_dir = _stopped_run(idea_status, good=False)  # no variant passes: no stop
    state = _state(run_dir)
    assert state["pending_stage"] == f"completed_{idea_status}"
    assert "profit_bars_reached" not in (state.get("flags") or {})
    # an operator file slipped in, and a re-run of the route: still no holdout
    _decision(run_dir, "spend", profit_bars_stop_evaluation="whatever")
    _forbid(monkeypatch)
    rpr.update_state(path=run_dir, status="active", pending_stage="regroup_record")
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["pending_stage"] == f"completed_{idea_status}"
    assert "holdout_evaluation" not in (state.get("completed_stages") or [])
    assert rpr.HOLDOUT_DECISION_RECORD_KEY not in state
    assert _consumed() == []


# ---------------------------------------------------------------------------
# 5. continue -> decide-next
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status", ["validated", "refuted", "inconclusive"])
def test_continue_records_the_choice_and_ends_completed(monkeypatch, idea_status):
    run_dir = _stopped_run(idea_status)
    _forbid(monkeypatch)
    _decision(run_dir, "continue", variant_id=_DROP)
    _resume(run_dir)
    state = _state(run_dir)
    assert state["pending_stage"] == f"completed_{idea_status}" and state["status"] == "completed"
    rec = state[rpr.HOLDOUT_DECISION_RECORD_KEY]
    assert rec["decision"] == "continue" and rec["variant_id"] is None
    assert "hypothesis_id" not in rec
    assert _consumed() == []
    assert rpr.HOLDOUT_CONSUME_RECORD_KEY not in state


@pytest.mark.parametrize("terminal", ["completed_validated", "completed_promoted",
                                      "completed_rejected"])
def test_the_run_after_the_decision_is_chosen_by_decide_next(campaign_root, monkeypatch,
                                                            terminal):
    """continue ends completed_<idea_status>; a spend ends at the gate's own
    terminal. Either way the DONE branch runs decide-next (a decision record,
    a minted entry), no child run."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    root = campaign_root["root"]
    run_dir = _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1", conf=3)],
                                    idea_status="validated")
    _write_flags(root, **FLAT_ON)
    rpr.update_state(path=run_dir, status="completed" if terminal == "completed_validated"
                     else "rejected" if terminal == "completed_rejected" else "active",
                     pending_stage=terminal)
    dirs_before = {p.name for p in campaign_root["runs_dir"].iterdir()}
    assert camp.process_once() is True
    done, new = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    assert done["status"] == "done" and done["outcome"] == "validated"
    assert new["status"] == "ready"
    assert (run_dir / "artifacts" / "decision_record.yaml").exists()
    assert {p.name for p in campaign_root["runs_dir"].iterdir()} == dirs_before


# ---------------------------------------------------------------------------
# 6. The consume marker: exactly once across crash/resume
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("crash", ["before_marker", "after_marker"])
def test_consume_marker_written_exactly_once_across_a_crash(monkeypatch, crash):
    run_dir = _stopped_run("validated")
    _policy(["H-OTHER"])
    _decision(run_dir, "spend")
    _resume(run_dir)  # awaiting the manual backtest
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": "pass"})
    real_mark = rpr._mark_holdout_consumed

    def _crashing(policy, consumed, hyp_id):
        if crash == "after_marker":
            real_mark(policy, consumed, hyp_id)
        raise RuntimeError("simulated crash")
    monkeypatch.setattr(rpr, "_mark_holdout_consumed", _crashing)
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    state = _state(run_dir)
    assert state["status"] == "failed" and state["pending_stage"] == "holdout_evaluation"
    assert state[rpr.HOLDOUT_CONSUME_RECORD_KEY]["hypothesis_id"] == HYP  # intent first
    assert _consumed() == (["H-OTHER", HYP] if crash == "after_marker" else ["H-OTHER"])

    monkeypatch.setattr(rpr, "_mark_holdout_consumed", real_mark)
    _forbid(monkeypatch, ("_route_holdout_evaluation",))  # the finish only, never the gate
    _resume(run_dir)
    state = _state(run_dir)
    # never skipped, never doubled, and the result is not misread as a second spend
    assert _consumed() == ["H-OTHER", HYP]
    assert state["pending_stage"] == "completed_promoted"


def test_back_out_before_the_backtest_spends_nothing(monkeypatch):
    """RUNBOOK (holdout_unlocked_awaiting_result): continue for the same stop,
    pending_stage regroup_record -> completed_<idea_status>, nothing spent."""
    run_dir = _stopped_run("validated")
    _decision(run_dir, "spend")
    _resume(run_dir)
    _decision(run_dir, "continue")
    _forbid(monkeypatch)
    rpr.update_state(path=run_dir, pending_stage="regroup_record")
    _resume(run_dir)
    state = _state(run_dir)
    assert state["pending_stage"] == "completed_validated"
    assert state[rpr.HOLDOUT_DECISION_RECORD_KEY]["decision"] == "continue"
    assert not state["flags"].get(rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    assert _consumed() == []


@pytest.mark.parametrize("spent", ["consume_record", "result_file"])
def test_back_out_after_the_seal_is_spent_still_records_it_once(monkeypatch, spent):
    """A `continue` written after the holdout ran can never skip the marker:
    the route goes to the record step whatever the file says."""
    run_dir = _stopped_run("validated")
    _decision(run_dir, "spend")
    _resume(run_dir)
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": "fail"})
    if spent == "consume_record":  # crash between the intent and the marker
        real_mark = rpr._mark_holdout_consumed
        monkeypatch.setattr(rpr, "_mark_holdout_consumed",
                            lambda *a: (_ for _ in ()).throw(RuntimeError("crash")))
        _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
        assert _state(run_dir)[rpr.HOLDOUT_CONSUME_RECORD_KEY]
        monkeypatch.setattr(rpr, "_mark_holdout_consumed", real_mark)
    assert _consumed() == []
    _decision(run_dir, "continue")
    rpr.update_state(path=run_dir, pending_stage="regroup_record")
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    state = _state(run_dir)
    assert _consumed() == [HYP]
    assert state["pending_stage"] == "completed_rejected"


def test_a_second_run_of_the_same_hypothesis_cannot_spend_again(monkeypatch):
    run_dir = _stopped_run("validated")
    _decision(run_dir, "spend")
    _resume(run_dir)
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": "pass"})
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    assert _state(run_dir)["pending_stage"] == "completed_promoted"
    assert _consumed() == [HYP]
    # the same hypothesis stops again (a new attempt): the spend is refused
    rpr.update_state(path=run_dir, pending_stage="regroup_record", status="active",
                     profit_bars_stop_evaluation=None,
                     **{rpr.HOLDOUT_CONSUME_RECORD_KEY: None,
                        rpr.HOLDOUT_DECISION_RECORD_KEY: None})
    (run_dir / "artifacts" / "holdout_result.yaml").unlink()
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)  # a new evaluation
    rpr.run_loop(RUN_ID)
    assert _state(run_dir)["flags"]["profit_bars_reached"] is True
    _decision(run_dir, "spend")
    _forbid(monkeypatch)
    _resume(run_dir)
    assert _state(run_dir)[rpr.HOLDOUT_UNLOCK_REFUSAL_KEY]["code"] == "holdout_already_consumed"
    assert _consumed() == [HYP]


# ---------------------------------------------------------------------------
# 7. --resume refuses early; drift
# ---------------------------------------------------------------------------

def test_resume_cli_refuses_without_a_valid_decision(campaign_root):
    run_dir = _stopped_run("validated")
    _write_flags(campaign_root["root"], **FLAT_ON)
    _set_orchestrator(RETIRED_ON)
    _save_queue_entries(campaign_root["queue_path"],
                        [{**_entry(RUN_ID), "status": "paused:profit_bars_reached"}])
    rpr.update_state(path=run_dir, status="active", flags={"profit_bars_reached": False})
    queue = camp._load_queue()
    assert camp.resume_paused_entry(queue) is False
    assert camp._load_queue()["queue"][0]["status"] == "paused:profit_bars_reached"
    _decision(run_dir, "continue")
    queue = camp._load_queue()
    assert camp.resume_paused_entry(queue) is True
    assert camp._load_queue()["queue"][0]["status"] == "in_progress"


def test_resume_cli_flag_off_does_not_read_the_decision(campaign_root, monkeypatch):
    run_dir = _stopped_run("validated", orchestrator=PREREQS)
    _set_orchestrator(PREREQS)
    monkeypatch.setattr(rpr, "holdout_decision_resume_blocker",
                        lambda *a: (_ for _ in ()).throw(AssertionError("read flag-off")))
    _save_queue_entries(campaign_root["queue_path"],
                        [{**_entry(RUN_ID), "status": "paused:profit_bars_reached"}])
    rpr.update_state(path=run_dir, status="active", flags={"profit_bars_reached": False})
    assert camp.resume_paused_entry(camp._load_queue()) is True


_NEW_FLAGS = ("HOLDOUT_UNLOCK_REFUSED_FLAG", "HOLDOUT_AWAITING_RESULT_FLAG",
              "HOLDOUT_RESULT_INCONCLUSIVE_FLAG")


@pytest.mark.parametrize("const", _NEW_FLAGS)
def test_new_pause_flags_mirror_the_table_and_have_rows(const):
    flag = getattr(rpr, const)
    assert dict(camp._PAUSE_FLAG_TO_REASON)[flag] == flag
    assert camp._classify_human_pause(Path("."), {"flags": {flag: True}}) == flag
    # a stale profit_bars_reached never masks it
    assert camp._classify_human_pause(
        Path("."), {"flags": {flag: True, "profit_bars_reached": True}}) == flag
    runbook = (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    assert f"| `{flag}`" in runbook
    assert f"'{flag}': False" in runbook  # §4's reset list
    rs.validate_queue_entry({"id": "x", "status": f"paused:{flag}"})


@pytest.mark.parametrize("code", rpr.HOLDOUT_UNLOCK_REFUSALS)
def test_every_refusal_code_has_a_runbook_row(code):
    runbook = (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    assert f"| `{rpr.HOLDOUT_UNLOCK_REFUSED_FLAG}` (`{code}`) |" in runbook


def test_refusal_codes_match_the_codes_the_code_raises():
    """Every HoldoutUnlockRefused("<code>", ...) literal in the orchestrator is
    a registered code, and every registered code is raised somewhere."""
    tree = ast.parse((_SR / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8"))
    raised = {n.args[0].value for n in ast.walk(tree)
              if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "HoldoutUnlockRefused"
              and n.args and isinstance(n.args[0], ast.Constant)}
    assert raised == set(rpr.HOLDOUT_UNLOCK_REFUSALS)


def test_schema_documented_and_no_not_built_leftovers():
    runbook = (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    row = next(ln for ln in runbook.splitlines() if ln.startswith("| `profit_bars_reached` |"))
    assert rpr.HOLDOUT_DECISION_FILE in row
    for key in rpr.HOLDOUT_DECISION_REQUIRED_KEYS + rpr.HOLDOUT_DECISION_OPTIONAL_KEYS:
        assert f"`{key}`" in row, key
    for decision in rpr.HOLDOUT_DECISIONS:
        assert f"`{decision}`" in row
    guide = (_SR / "docs" / "USER_GUIDE.md").read_text(encoding="utf-8")
    assert rpr.HOLDOUT_DECISION_FILE in guide
    reg = yaml.safe_load((_SR / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    entry = next(f for f in reg["flags"] if f["name"] == "verdict_routing_retired")
    assert "S2d" in entry["criterion"] and "holdout_decision.yaml" in entry["criterion"]
    assert "S2d (the holdout unlock)" not in entry["blocked_on"]
    for rel in ("docs/RUNBOOK.md", "docs/USER_GUIDE.md", "DOC_INDEX.md",
                "config/campaign_config.yaml", "workflow/run_phase1_research.py"):
        text = (_SR / rel).read_text(encoding="utf-8")
        assert "S2d, not built" not in text and "S2d), not built" not in text, rel
        assert "slice 6c S2d, not built" not in text, rel


def test_decision_keys_do_not_collide_with_pipeline_state_keys():
    """The new pipeline_state keys and flags are new names (dispatch template
    §3 N+3): none is written anywhere else in the workflow or tools."""
    names = [rpr.HOLDOUT_DECISION_RECORD_KEY, rpr.HOLDOUT_CONSUME_RECORD_KEY,
             rpr.HOLDOUT_UNLOCK_REFUSAL_KEY] + [getattr(rpr, c) for c in _NEW_FLAGS]
    for path in list((_SR / "workflow").glob("*.py")) + list((_SR / "tools").glob("*.py")):
        if path.name == "run_phase1_research.py":
            continue
        text = path.read_text(encoding="utf-8")
        for name in names:
            assert f'"{name}"' not in text, (path.name, name)
