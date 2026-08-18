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
    """A run dir carrying only the artifacts the gate reads."""
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    if brief is not None:
        (artifacts / "research_brief.yaml").write_text(
            yaml.safe_dump(brief), encoding="utf-8")
    return tmp_path


@pytest.mark.parametrize("brief,label", [
    ({"research_only": True}, "explicitly research-only"),
    ({}, "key absent (the shape all 57 live briefs have)"),
    (None, "no research_brief.yaml at all"),
    ({"research_only": None}, "explicit null"),
    ({"research_only": "false"}, "string 'false', not the boolean"),
    ({"research_only": 0}, "falsy 0 -- must not satisfy an `is False` check"),
])
def test_gate_refuses_unless_tradable_is_affirmed(tmp_path, brief, label):
    """Every non-affirmative shape terminates the run instead of proceeding."""
    assert r1._route_holdout_evaluation(
        _run_dir(tmp_path, brief), "run_test") == "completed_rejected", label


def test_gate_lets_an_affirmatively_tradable_brief_through(tmp_path):
    """research_only False must NOT be refused by gate 0.

    It proceeds to the later gates and, with no promotion_audit.yaml and no
    holdout_result.yaml present, lands on the human pause -- proving gate 0
    let it past rather than that everything returns the same verdict.
    """
    run_dir = _run_dir(tmp_path, {"research_only": False})
    # The downstream gate reads one of promotion_audit / verdict_interpretation;
    # supply the latter so this test exercises gate 0's pass-through rather than
    # tripping over an unrelated missing artifact.
    (run_dir / "artifacts" / "verdict_interpretation.yaml").write_text(
        yaml.safe_dump({"hypothesis_id": "run_test"}), encoding="utf-8")
    assert r1._route_holdout_evaluation(run_dir, "run_test") == "human_pause"


def test_refusal_precedes_the_backtest_instruction(tmp_path, capsys):
    """The refusal must fire BEFORE the pause that tells a human to run the
    holdout backtest.

    This is the whole point of placing gate 0 first rather than merely ahead
    of the holdout_consumed_by write: the pause branch prints "Run the holdout
    backtest on this range", and a human following that instruction opens the
    sealed data. Looking is spending, so a refusal printed after that text
    would be a refusal after the fact.
    """
    r1._route_holdout_evaluation(_run_dir(tmp_path, {"research_only": True}), "run_test")
    out = capsys.readouterr().out
    assert "HOLDOUT REFUSED" in out
    assert "Run the holdout backtest" not in out


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
