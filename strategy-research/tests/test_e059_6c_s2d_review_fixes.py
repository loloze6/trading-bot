"""
E-059 slice 6c S2d -- code-review fixes (review of f251a779..f3a82d55). Every
test here fails on f3a82d55. Synthetic only: no LLM, no backtest, no sealed
data (the "holdout result" is a hand-written fixture; conftest sandboxes the
data policy).
  1. One physical seal, one pending spend (other runs, and unaccounted ids in
     the tracked campaign_data_policy.yaml).
  2. Record first: a result is recorded before any check can change the ending.
  3. No unlock, no promotion.
  4. The result is bound to the unlock (variant, trial, decision sha, hypothesis).
  5. No relabelling of a recorded result.
  6. Operator decision 2026-09-26 (replaces the review's fix 6): bars
     ratification is not enforced in code.
  7. The whole bars file's sha256.
  8. DSR re-checked on the current ledger; hypothesis_id from the card only.
  9. trial_ledgers_merged: true for a spend.
 10. The seal checks exist once.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402

from test_e058_s2a_regroup_record import RUN_ID  # noqa: E402
from test_profit_bars_every_backtest import _VALID_BARS, _write_bars, _state  # noqa: E402
from test_e059_6c_s2a_route_retirement import _forbid  # noqa: E402
from test_e059_6c_s2d_holdout_unlock import (  # noqa: E402
    HYP, _stopped_run, _decision, _result, _resume, _policy, _consumed, _DROP)


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _refusal(run_dir):
    return (_state(run_dir).get(rpr.HOLDOUT_UNLOCK_REFUSAL_KEY) or {}).get("code")


def _other_run(name, **state):
    d = rpr.ROOT / "runs" / name
    d.mkdir(parents=True, exist_ok=True)
    rpr.save_yaml(d / "pipeline_state.yaml", {"run_id": name, **state})


def _awaiting(idea_status="validated"):
    run_dir = _stopped_run(idea_status)
    _decision(run_dir, "spend")
    _resume(run_dir)
    assert _state(run_dir)["flags"][rpr.HOLDOUT_AWAITING_RESULT_FLAG] is True
    return run_dir


# 1 ---------------------------------------------------------------------------

@pytest.mark.parametrize("other", [
    {"pending_stage": "holdout_evaluation",
     "holdout_decision_record": {"decision": "spend", "run_id": "run_777"}},
    {"pending_stage": "holdout_evaluation", "status": "failed",
     "holdout_consume_record": {"hypothesis_id": "H-X", "run_id": "run_777"}},
])
def test_another_runs_unfinished_spend_blocks_the_unlock(monkeypatch, other):
    run_dir = _stopped_run("validated")
    _other_run("run_777", **other)
    _forbid(monkeypatch)
    _decision(run_dir, "spend")
    _resume(run_dir)
    assert _refusal(run_dir) == "seal_spend_pending"
    assert _consumed() == []


def test_a_finished_spend_of_another_hypothesis_does_not_block(monkeypatch):
    run_dir = _stopped_run("validated")
    _other_run("run_777", pending_stage="completed_rejected",
               holdout_consume_record={"hypothesis_id": "H-X", "run_id": "run_777"})
    _policy(["H-X"])
    _decision(run_dir, "spend")
    _resume(run_dir)
    assert _state(run_dir)["flags"][rpr.HOLDOUT_AWAITING_RESULT_FLAG] is True


def test_an_unaccounted_policy_entry_blocks_the_unlock(monkeypatch):
    """The dual-writer case: an id in the tracked holdout_consumed_by that no
    finished run here accounts for (another writer's spend) blocks a spend."""
    run_dir = _stopped_run("validated")
    _policy(["H-FROM-THE-OTHER-WRITER"])
    _forbid(monkeypatch)
    _decision(run_dir, "spend")
    _resume(run_dir)
    assert _refusal(run_dir) == "seal_spend_pending"


def test_the_pre_result_recheck_also_sees_a_new_pending_spend(monkeypatch):
    run_dir = _awaiting()
    _other_run("run_777", pending_stage="holdout_evaluation",
               holdout_decision_record={"decision": "spend", "run_id": "run_777"})
    _forbid(monkeypatch)
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    assert _refusal(run_dir) == "seal_spend_pending"
    assert _state(run_dir)["pending_stage"] == "holdout_evaluation"


# 2 ---------------------------------------------------------------------------

def test_record_first_a_hold_after_the_backtest_never_skips_the_marker(monkeypatch):
    run_dir = _awaiting()
    _result(run_dir, "pass")
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", {})  # undeclared since
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    state = _state(run_dir)
    assert _consumed() == [HYP]  # recorded before the hold
    assert state[rpr.HOLDOUT_CONSUME_RECORD_KEY]["hypothesis_id"] == HYP
    assert camp._classify_human_pause(run_dir, state) == "research_only_unverified"


def test_record_first_a_result_that_appears_after_a_refusal_is_still_recorded(monkeypatch):
    """The decision is refused, then a result exists anyway (the backtest ran
    by hand): the resume records it -- no refusal can come first."""
    run_dir = _stopped_run("validated")
    _decision(run_dir, "spend", run_id="run_999")
    _resume(run_dir)
    assert _refusal(run_dir) == "decision_wrong_run"
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": "pass"})
    _resume(run_dir, rpr.HOLDOUT_UNLOCK_REFUSED_FLAG)
    assert _consumed() == [HYP]
    assert camp._classify_human_pause(run_dir, _state(run_dir)) == \
        rpr.HOLDOUT_SPENT_WITHOUT_UNLOCK_FLAG


# 3 ---------------------------------------------------------------------------

@pytest.mark.parametrize("status", ["pass", "fail"])
def test_a_result_without_an_unlock_is_recorded_and_never_promoted(monkeypatch, status):
    run_dir = _stopped_run("validated")
    rpr.save_yaml(run_dir / "artifacts" / "holdout_result.yaml", {"status": status})
    _forbid(monkeypatch)
    rpr.update_state(path=run_dir, status="active", pending_stage="holdout_evaluation")
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["pending_stage"] == "holdout_evaluation" and state["status"] == "paused_for_human"
    assert camp._classify_human_pause(run_dir, state) == rpr.HOLDOUT_SPENT_WITHOUT_UNLOCK_FLAG
    assert _consumed() == [HYP]


# 4 ---------------------------------------------------------------------------

@pytest.mark.parametrize("damage", [{"variant_id": _DROP}, {"trial_id": "other-trial"},
                                    {"decision_sha256": "0" * 64}])
def test_an_unbound_result_is_recorded_then_paused(monkeypatch, damage):
    run_dir = _awaiting()
    _result(run_dir, "pass", **damage)
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    state = _state(run_dir)
    assert _consumed() == [HYP]
    assert state["pending_stage"] == "holdout_evaluation"
    assert camp._classify_human_pause(run_dir, state) == rpr.HOLDOUT_RESULT_UNBOUND_FLAG


def test_a_changed_hypothesis_card_is_unbound(monkeypatch):
    run_dir = _awaiting()
    _result(run_dir, "pass")
    rpr.save_yaml(run_dir / "artifacts" / "hypothesis_card.yaml", {"hypothesis_id": "H-ELSE"})
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    assert _consumed() == [HYP]  # the unlock's hypothesis is the one recorded
    assert camp._classify_human_pause(run_dir, _state(run_dir)) == rpr.HOLDOUT_RESULT_UNBOUND_FLAG


# 5 ---------------------------------------------------------------------------

def test_a_result_rewritten_after_the_record_is_refused(monkeypatch):
    run_dir = _awaiting()
    _result(run_dir, "fail")
    real = rpr._spent_holdout_ending
    monkeypatch.setattr(rpr, "_spent_holdout_ending",
                        lambda *a: (_ for _ in ()).throw(RuntimeError("crash after the record")))
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    assert _consumed() == [HYP] and _state(run_dir)["status"] == "failed"
    monkeypatch.setattr(rpr, "_spent_holdout_ending", real)
    _result(run_dir, "pass")  # the relabel
    _resume(run_dir)
    state = _state(run_dir)
    assert state["pending_stage"] == "holdout_evaluation"
    assert camp._classify_human_pause(run_dir, state) == rpr.HOLDOUT_RESULT_RELABELLED_FLAG
    assert "status: pass" in state[rpr.HOLDOUT_RELABEL_KEY][0]["content"]
    assert _consumed() == [HYP]


# 6 ---------------------------------------------------------------------------

def test_unratified_bars_do_not_block_a_spend(monkeypatch):
    """Operator decision 2026-09-26: ratification is the operator's manual
    check, never enforced in code; the stop carries no ratification mark."""
    run_dir = _stopped_run("validated", bars={**_VALID_BARS})  # ratified_by/at null
    assert not any("unratified" in str(k) for k in _state(run_dir))
    _decision(run_dir, "spend")
    _resume(run_dir)
    assert _state(run_dir)["flags"][rpr.HOLDOUT_AWAITING_RESULT_FLAG] is True
    assert "bars_unratified" not in rpr.HOLDOUT_UNLOCK_REFUSALS


# 7 ---------------------------------------------------------------------------

def test_any_byte_change_to_the_bars_file_refuses_the_spend(monkeypatch):
    run_dir = _stopped_run("validated")
    path = rpr.ROOT / "config" / "profitability_bars.yaml"
    path.write_text(path.read_text(encoding="utf-8") + "# edited after grading\n",
                    encoding="utf-8")
    _forbid(monkeypatch)
    _decision(run_dir, "spend")
    _resume(run_dir)
    assert _refusal(run_dir) == "bars_changed"


def test_the_evaluation_records_the_bars_sha_only_under_the_flag():
    run_dir = _stopped_run("validated")
    ev = rpr._load_every_backtest_evaluation(run_dir, RUN_ID)
    assert ev[rpr.BARS_FILE_SHA_FIELD] == rpr._bars_file_sha256()
    ev_off = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    assert rpr.BARS_FILE_SHA_FIELD not in ev_off


# 8 ---------------------------------------------------------------------------

def test_dsr_is_rechecked_on_the_current_ledger(monkeypatch):
    run_dir = _stopped_run("validated")
    state = rpr.load_campaign_state()
    state["trial_sharpes"].extend(
        {"trial_id": f"run_{500 + i}", "source": "backtest", "statistic_valid": "sharpe",
         "sharpe": 1.3 + 0.01 * (i % 20), "forecast_hash": f"fh-grown-{i}"} for i in range(200))
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)
    _forbid(monkeypatch)
    _decision(run_dir, "spend")
    _resume(run_dir)
    assert _refusal(run_dir) == "dsr_fails_current_ledger"


def test_the_spend_record_carries_the_dsr_recheck():
    run_dir = _awaiting()
    rec = _state(run_dir)[rpr.HOLDOUT_DECISION_RECORD_KEY]
    assert rec["dsr_recheck"]["deflated_sharpe_ratio"] >= _VALID_BARS["deflated_sharpe_threshold"]


def test_a_stale_promotion_audit_never_names_the_hypothesis(monkeypatch):
    run_dir = _stopped_run("validated")
    rpr.save_yaml(run_dir / "artifacts" / "promotion_audit.yaml",
                  {"hypothesis_id": "H-STALE", "passes_deflated_threshold": False})
    _decision(run_dir, "spend")
    _resume(run_dir)
    assert _state(run_dir)[rpr.HOLDOUT_DECISION_RECORD_KEY]["hypothesis_id"] == HYP
    _result(run_dir, "pass")
    _resume(run_dir, rpr.HOLDOUT_AWAITING_RESULT_FLAG)
    assert _consumed() == [HYP]
    assert _state(run_dir)["pending_stage"] == "completed_promoted"


# 9 ---------------------------------------------------------------------------

@pytest.mark.parametrize("value", [_DROP, False])
def test_a_spend_needs_the_ledgers_merged_attestation(monkeypatch, value):
    run_dir = _stopped_run("validated")
    _forbid(monkeypatch)
    _decision(run_dir, "spend", trial_ledgers_merged=value)
    _resume(run_dir)
    assert _refusal(run_dir) == "ledgers_not_merged"


def test_continue_needs_no_attestation(monkeypatch):
    run_dir = _stopped_run("validated")
    _decision(run_dir, "continue")
    _resume(run_dir)
    assert _state(run_dir)["pending_stage"] == "completed_validated"


# 10 --------------------------------------------------------------------------

def test_the_seal_checks_exist_once():
    src = (_SR / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    # the single-use membership test lives only in _holdout_already_spent
    assert src.count('in _consumed_list(policy.get("holdout_consumed_by"))') == 1
    assert src.count("hyp_id in consumed") == 0
    for name in ("_profit_stop_raised", "_holdout_already_spent",
                 "_mark_holdout_consumed_if_absent", "_holdout_result_terminal"):
        assert callable(getattr(rpr, name)), name
    import inspect
    assert "_mark_holdout_consumed_if_absent" in inspect.getsource(rpr._record_spent_holdout)
    for fn in (rpr._holdout_unlock_route, rpr.holdout_decision_resume_blocker):
        assert "_profit_stop_raised" in inspect.getsource(fn)
