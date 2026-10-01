"""
D-055 (operator, 2026-10-01): how the knowledge base turns findings into bans.

A finding is information by default. It is a ban (listed in
exhausted_mechanisms, and able to pause a run through
_check_kb_reactivation_conformance) only when it is `exhausted: true` AND
either evidence_count >= 3 or all three operator-approval fields are set.
A word in exhausted_basis prose -- the old A5.1 rule matched the substring
"analytic", even inside "analytically-explained" -- never makes a ban.
"""
import sys
from pathlib import Path

import pytest
import yaml

SR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR / "workflow"))
sys.path.insert(0, str(SR / "tools"))

import record_schema  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

APPROVED = {"veto_basis": "three clean reruns, same sign", "veto_approved_by": "operator",
            "veto_approved_on": "2026-10-01"}
WITHDRAWN = ("keltner_mean_reversion_no_edge", "keltner_breakout_inverted",
             "keltner_scoremode_no_edge", "rsi_mean_reversion_no_edge",
             "rsi_momentum_trending_cost_drag")


def _finding(**kw):
    f = {"id": "f", "hypothesis_id": "H_X", "outcome": "no_edge_observed",
         "evidence_count": 1, "exhausted": True, "reactivation_condition": None}
    f.update(kw)
    return f


def _view(*findings):
    kb = {"findings": list(findings)}
    rpr._recompute_kb_views(kb)
    return kb["exhausted_mechanisms"]


@pytest.mark.parametrize("basis", [
    "analytic", "Analytic: cost_drag=273% ...", "non-analytic result",
    "Empirical: real, analytically-explained regime-gate artefact"])
@pytest.mark.parametrize("ec", [1, 2])
def test_the_word_analytic_alone_never_makes_a_ban(basis, ec):
    f = _finding(exhausted_basis=basis, evidence_count=ec)
    assert rpr._kb_veto_reason(f) is None
    assert _view(f) == []


def test_an_approved_structured_veto_is_a_ban():
    f = _finding(**APPROVED)
    assert rpr._kb_veto_reason(f) == "approved"
    [entry] = _view(f)
    assert entry["id"] == "f" and entry["veto_reason"] == "approved"
    assert entry["hypothesis_ids"] == ["H_X"]


@pytest.mark.parametrize("missing", list(APPROVED))
def test_an_incomplete_approval_is_not_a_ban(missing):
    fields = dict(APPROVED)
    fields[missing] = "  "
    assert rpr._kb_veto_reason(_finding(**fields)) is None
    fields.pop(missing)
    assert rpr._kb_veto_reason(_finding(**fields)) is None


def test_three_post_backtest_results_make_a_ban():
    assert rpr._kb_veto_reason(_finding(evidence_count=3)) == "evidence_count"
    assert rpr._kb_veto_reason(_finding(evidence_count=2)) is None


def test_a_finding_that_is_not_exhausted_is_never_a_ban():
    assert rpr._kb_veto_reason(_finding(exhausted=False, evidence_count=5, **APPROVED)) is None


def test_the_approval_fields_pass_the_closed_kb_schema():
    record_schema.validate_kb_finding(_finding(**APPROVED), "test")


def test_the_reactivation_check_follows_the_same_rule():
    question = {"research_goal": "retest H_X on 4h"}
    below_bar = _finding(exhausted_basis="Analytic: one run", evidence_count=2)
    assert rpr._check_kb_reactivation_conformance(question, {"findings": [below_bar]}) == []
    banned = _finding(evidence_count=3)
    [v] = rpr._check_kb_reactivation_conformance(question, {"findings": [banned]})
    assert "H_X" in v and "ban" in v
    # a consumed reactivation condition still blocks (operator-written, pre-registered)
    consumed = _finding(exhausted=False, reactivation_consumed_by="run_050")
    assert len(rpr._check_kb_reactivation_conformance(question, {"findings": [consumed]})) == 1


def test_live_kb_the_five_bans_are_withdrawn_not_deleted():
    kb = yaml.safe_load((SR / "campaign_record" / "campaign_knowledge_base.yaml").read_text(encoding="utf-8"))
    by_id = {f["id"]: f for f in kb["findings"]}
    for fid in WITHDRAWN:
        f = by_id[fid]
        assert f["exhausted"] is False, fid
        assert f["policy_consequence"].startswith("WITHDRAWN 2026-10-01 (D-055)"), fid
        assert f["readjudication_20261001"].startswith("D-055"), fid
        assert f["exhausted_basis"], fid  # history kept
    banned = [e["id"] for e in kb["exhausted_mechanisms"]]
    assert not set(WITHDRAWN) & set(banned)
    # the stored view is what the rule produces from the stored findings
    rebuilt = {"findings": kb["findings"]}
    rpr._recompute_kb_views(rebuilt)
    assert rebuilt["exhausted_mechanisms"] == kb["exhausted_mechanisms"]
    assert rebuilt["coverage_matrix"] == kb["coverage_matrix"]


def test_an_integral_float_count_is_accepted():
    assert rpr._kb_veto_reason(_finding(evidence_count=3.0)) == "evidence_count"


@pytest.mark.parametrize("bad", ["3", 2.5, True, None])
def test_a_mistyped_evidence_count_fails_loud(bad):
    with pytest.raises(ValueError, match="evidence_count must be an integer"):
        rpr._kb_veto_reason(_finding(evidence_count=bad))
