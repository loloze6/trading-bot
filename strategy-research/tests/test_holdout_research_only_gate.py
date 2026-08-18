"""
E-015 S3: the holdout gate refuses a run whose brief does not affirmatively
declare the strategy tradable.

WHY THIS IS AN AFFIRMATIVE CHECK (research_only is False), not `research_only
is True` -> refuse. Measured on the live tree 2026-08-18, during S3's Phase A:

  * 0 of 57 research_brief.yaml files carried the research_only key at all;
  * it is written by exactly 1 of the 3 research_brief.yaml writers
    (run_campaign._materialize_run), so it does not survive a refine
    (setup_next_run copies an LLM-authored proposed_brief.yaml -- 0 of 27 of
    those carry it) or a campaign_review reframe.

A negative check would therefore have been decorative: it would have passed
every run that exists and every child of a flagged parent. The affirmative
form needs no propagation machinery to be correct for descendants, because a
child that inherits nothing inherits no permission either.

Fail-closed was safe to adopt outright: holdout_consumed_by was empty and no
run had ever reached this gate, so there is no legacy corpus being blocked.

The tests drive _route_holdout_evaluation() itself rather than a helper, so
they cover the real routing decision.
"""
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as r1  # noqa: E402


def _run_dir(tmp_path: Path, brief: dict | None) -> Path:
    """A run dir carrying the artifacts the gate reads.

    pipeline_state.yaml is always present, matching every real run: setup_run.py
    scaffolds it, and the router that calls this gate is itself driven from it.
    (If it were ever genuinely absent, update_state raises and the exception
    propagates out of the gate -- which still fails closed, since raising is not
    proceeding to the holdout, but it is not the shape production is ever in.)
    """
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    (tmp_path / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"run_id": "run_test", "flags": {}}), encoding="utf-8")
    if brief is not None:
        (artifacts / "research_brief.yaml").write_text(
            yaml.safe_dump(brief), encoding="utf-8")
    return tmp_path


_HELD = "HOLDOUT HELD"
# Pinned on the later branch's own distinctive, stable text rather than on the
# imperative sentence: "Run the holdout backtest" differs from the hold message's
# "run the holdout backtest" only by capitalisation, so a cosmetic recapitalisation
# of either message would break these tests with a false ordering failure.
_BACKTEST_INSTRUCTION = "holdout_result.yaml not yet present"


@pytest.mark.parametrize("brief,label", [
    ({"research_only": True}, "explicitly research-only"),
    ({}, "key absent (the shape all 57 live briefs have)"),
    (None, "no research_brief.yaml at all"),
    ({"research_only": None}, "explicit null"),
    ({"research_only": "false"}, "string 'false', not the boolean"),
    ({"research_only": 0}, "falsy 0 -- must not satisfy an `is False` check"),
])
def test_gate_holds_unless_tradable_is_affirmed(tmp_path, brief, label, capsys):
    """Every non-affirmative shape is held at gate 0 instead of proceeding.

    Asserted on the PRINTED VERDICT, not the return value: gate 0 and the
    legitimate no-holdout-result path both return "human_pause", so the return
    value alone cannot tell "held at the door" from "let through". The message
    is what distinguishes them, so the message is what this pins -- along with
    the absence of the backtest instruction (see the ordering test below).
    """
    result = r1._route_holdout_evaluation(_run_dir(tmp_path, brief), "run_test")
    out = capsys.readouterr().out
    assert _HELD in out, label
    assert _BACKTEST_INSTRUCTION not in out, label
    assert result == "human_pause", label


def test_gate_lets_an_affirmatively_tradable_brief_through(tmp_path, capsys):
    """research_only False must NOT be held by gate 0.

    It proceeds to the later gates and, with no holdout_result.yaml present,
    lands on the legitimate human pause that asks for the backtest. Pinned on
    the message rather than the return value, for the reason above: both land
    on "human_pause", and a gate 0 that wrongly held this run would still
    return the same string.
    """
    run_dir = _run_dir(tmp_path, {"research_only": False})
    # The downstream gate reads one of promotion_audit / verdict_interpretation;
    # supply the latter so this test exercises gate 0's pass-through rather than
    # tripping over an unrelated missing artifact.
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "run_test"}), encoding="utf-8")

    result = r1._route_holdout_evaluation(run_dir, "run_test")
    out = capsys.readouterr().out
    assert _HELD not in out
    assert _BACKTEST_INSTRUCTION in out
    assert result == "human_pause"


def test_hold_is_recoverable_not_terminal(tmp_path, capsys):
    """A held run must stay resumable.

    research_only is not propagated by the refine path (setup_next_run copies
    an LLM-authored proposed_brief.yaml) or the reframe path, so a genuinely
    tradable descendant of a correctly-materialized run lands here routinely.
    "completed_rejected" would write status="rejected", which resume_pipeline
    refuses to resume -- terminally killing a good run over missing paperwork.
    Pinned because the difference is one string and the protection is identical
    either way.
    """
    assert r1._route_holdout_evaluation(
        _run_dir(tmp_path, {"research_only": True}), "run_test") != "completed_rejected"


def test_hold_classifies_away_from_the_go_spend_the_seal_bucket(tmp_path):
    """The hold must NOT classify as provisional_promote_awaiting_holdout.

    This is the finding that makes the flag load-bearing rather than
    decorative. _classify_human_pause reaches that bucket whenever
    promotion_audit.yaml exists and holdout_result.yaml does not -- which is
    exactly the state of every run arriving at the holdout gate. Its RUNBOOK
    row instructs the operator to "Run the holdout backtest ... by hand", so a
    bare human_pause here would route a held run straight into spending the
    single-use seal: strictly worse than the terminal reject it replaced.

    Driven through the real classifier against a run dir in the true arriving
    shape (promotion_audit present, holdout_result absent), not a stub.
    """
    import importlib
    camp = importlib.import_module("run_campaign")

    run_dir = _run_dir(tmp_path, {"research_only": True})
    (run_dir / "artifacts" / "promotion_audit.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "run_test"}), encoding="utf-8")

    r1._route_holdout_evaluation(run_dir, "run_test")
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text())

    assert state["flags"]["research_only_unverified"] is True
    assert camp._classify_human_pause(run_dir, state) == "research_only_unverified"
    assert camp._classify_human_pause(run_dir, state) != "provisional_promote_awaiting_holdout"


def test_a_tradable_run_still_reaches_the_awaiting_holdout_bucket(tmp_path):
    """Control for the test above: the new classifier branch must not swallow
    the legitimate case. A run that DOES declare itself tradable still
    classifies as provisional_promote_awaiting_holdout, so the operator still
    gets told to run the holdout backtest when they have actually earned it.
    """
    import importlib
    camp = importlib.import_module("run_campaign")

    run_dir = _run_dir(tmp_path, {"research_only": False})
    (run_dir / "artifacts" / "promotion_audit.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "run_test"}), encoding="utf-8")

    r1._route_holdout_evaluation(run_dir, "run_test")
    state_path = run_dir / "pipeline_state.yaml"
    state = yaml.safe_load(state_path.read_text()) if state_path.exists() else {}

    assert not (state.get("flags") or {}).get("research_only_unverified")
    assert camp._classify_human_pause(run_dir, state) == "provisional_promote_awaiting_holdout"


def test_runbook_documents_the_new_pause_reason():
    """A classifier bucket with no RUNBOOK row leaves the operator with a
    reason string and no instructions -- and this particular one must actively
    contradict its neighbour's "go run the holdout backtest" guidance.
    """
    runbook = (Path(__file__).parent.parent / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    assert "| `research_only_unverified` |" in runbook
    assert "Do NOT run the holdout backtest to clear this" in runbook


def test_hold_precedes_the_backtest_instruction(tmp_path, capsys):
    """The hold must fire BEFORE the pause that tells a human to run the
    holdout backtest.

    This is the whole point of placing gate 0 first rather than merely ahead
    of the holdout_consumed_by write: the later pause prints "Run the holdout
    backtest on this range", and a human following that instruction opens the
    sealed data. Looking is spending, so a hold printed after that text would
    be a hold after the fact.
    """
    r1._route_holdout_evaluation(_run_dir(tmp_path, {"research_only": True}), "run_test")
    out = capsys.readouterr().out
    assert _HELD in out
    assert _BACKTEST_INSTRUCTION not in out


def test_refusal_does_not_consume_the_holdout(tmp_path, monkeypatch):
    """A refused run must not be marked as having spent its single holdout use.

    The seal is single-use and terminal; burning it on a run that was turned
    away at the door would be strictly worse than the gap this gate closes.
    Asserted by proving the policy file is never written at all.
    """
    policy = tmp_path / "campaign_data_policy.yaml"
    policy.write_text(yaml.safe_dump({"holdout_consumed_by": []}), encoding="utf-8")
    monkeypatch.setattr(r1, "_DATA_POLICY_PATH", policy)
    before = policy.read_bytes()

    r1._route_holdout_evaluation(_run_dir(tmp_path, {"research_only": True}), "run_test")

    assert policy.read_bytes() == before
    assert yaml.safe_load(policy.read_text())["holdout_consumed_by"] == []
