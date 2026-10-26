"""
D-194 -- decide-next ranks on confidence_real desc, then cost.backtests asc;
distance_to_profitable and mechanism_plausibility are retired.

Proven here, synthetic inputs only (no LLM, no backtest, no trial row):
  * the order: confidence_real desc, then cost asc (unknown cost last), then
    candidate_id asc;
  * a tie on BOTH keys: the lowest candidate_id is picked, `picked.tie_with`
    lists the others (ascending) and the why text names them;
  * no tie: no `tie_with` key at all, and the why text says nothing of a tie;
  * records written before D-194 (scores carrying the two retired fields) still
    load and validate: reader proposals, queued-card scores, the proposal and
    decision-record schemas;
  * nothing new writes either field: candidates, the decision record, the
    analyst's side finding, the rendered docs the readers and step 1a get.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import decide_next as dn  # noqa: E402
import reader_proposals as rp  # noqa: E402

from test_e059_s2a_decide_next import (  # noqa: E402
    _patch, _inputs, _one_source, _decide, _src, _memory_entry, _by_id,
)

RETIRED = ("distance_to_profitable", "mechanism_plausibility")
SCHEMAS = _SR / "workflow_artifacts" / "schemas"


def _ranked(rec):
    return [c["candidate_id"] for c in rec["candidates"] if c["rank"]]


def _cand(cid, conf, backtests):
    return {"candidate_id": cid, "scores": {"confidence_real": conf},
            "cost": {"backtests": backtests}}


# ---------------------------------------------------------------------------
# The order
# ---------------------------------------------------------------------------

def test_rank_key_is_confidence_desc_then_cost_asc_then_id():
    cands = [_cand("c", 1, 1), _cand("b", 3, 20), _cand("a", 3, 5), _cand("d", 3, None),
             _cand("e", 2, 1)]
    assert [c["candidate_id"] for c in sorted(cands, key=dn.rank_key)] == [
        "a", "b", "d", "e", "c"]


def test_the_retired_fields_do_not_rank():
    # a high distance / mechanism value on the lower-confidence candidate changes nothing
    lo = _cand("a", 1, 4)
    lo["scores"].update(distance_to_profitable=3, mechanism_plausibility=3)
    hi = _cand("b", 2, 4)
    hi["scores"].update(distance_to_profitable=0, mechanism_plausibility=0)
    assert sorted([lo, hi], key=dn.rank_key)[0] is hi


def test_decide_ranks_on_confidence_then_cost():
    a = _src([_patch("profitability-run_061-1", conf=2)])
    b = _src([_patch("profitability-run_062-1", after=0.9, conf=2)])
    c = _src([_patch("profitability-run_063-1", after=0.95, conf=3)])
    inputs = _inputs(
        {"run_061": a, "run_062": b, "run_063": c},
        {"run_061": _memory_entry("run_061", n_windows=11, proposal_ids=["profitability-run_061-1"]),
         "run_062": _memory_entry("run_062", n_windows=4, protocol_ref="p4",
                                  proposal_ids=["profitability-run_062-1"]),
         "run_063": _memory_entry("run_063", n_windows=20, protocol_ref="p20",
                                  proposal_ids=["profitability-run_063-1"])})
    rec = _decide(inputs)
    # run_063 has the highest confidence despite the dearest cost; 062 beats 061 on cost
    assert _ranked(rec) == ["profitability-run_063-1", "profitability-run_062-1",
                            "profitability-run_061-1"]
    assert rec["picked"]["candidate_id"] == "profitability-run_063-1"
    assert "tie_with" not in rec["picked"]


# ---------------------------------------------------------------------------
# The declared tie
# ---------------------------------------------------------------------------

def test_tie_on_both_keys_picks_lowest_id_and_declares_the_others():
    props = [_patch("profitability-run_061-3", after=0.8, conf=2),
             _patch("profitability-run_061-1", after=0.6, conf=2),
             _patch("profitability-run_061-2", after=0.7, conf=2),
             _patch("profitability-run_061-4", after=0.9, conf=1)]
    rec = _decide(_one_source(props))
    picked = rec["picked"]
    assert picked["candidate_id"] == "profitability-run_061-1"
    assert picked["tie_with"] == ["profitability-run_061-2", "profitability-run_061-3"]
    for other in picked["tie_with"]:
        assert other in picked["why"]
    assert "profitability-run_061-4" not in picked["tie_with"]   # lower confidence: not tied
    assert "profitability-run_061-4" not in picked["why"]


def test_same_confidence_but_different_cost_is_not_a_tie():
    a = _src([_patch("profitability-run_061-1", conf=2)])
    b = _src([_patch("profitability-run_062-1", after=0.9, conf=2)])
    inputs = _inputs({"run_061": a, "run_062": b},
                     {"run_061": _memory_entry("run_061", n_windows=11,
                                               proposal_ids=["profitability-run_061-1"]),
                      "run_062": _memory_entry("run_062", n_windows=4, protocol_ref="p4",
                                               proposal_ids=["profitability-run_062-1"])})
    rec = _decide(inputs)
    assert rec["picked"]["candidate_id"] == "profitability-run_062-1"
    assert "tie_with" not in rec["picked"]
    assert "tied" not in rec["picked"]["why"]


def test_no_tie_writes_no_tie_with_key_and_no_tie_text():
    rec = _decide(_one_source([_patch("profitability-run_061-1", after=0.6, conf=3),
                               _patch("profitability-run_061-2", after=0.7, conf=1)]))
    assert rec["picked"]["candidate_id"] == "profitability-run_061-1"
    assert "tie_with" not in rec["picked"]
    assert "tied" not in rec["picked"]["why"]
    assert "tie_with" not in json.dumps(rec)


def test_a_lone_candidate_has_no_tie():
    rec = _decide(_one_source([_patch("profitability-run_061-1")]))
    assert "tie_with" not in rec["picked"]


def test_unknown_cost_ties_with_unknown_cost():
    top, same, cheaper_conf = _cand("b", 2, None), _cand("a", 2, None), _cand("c", 1, None)
    ranked = sorted([top, same, cheaper_conf], key=dn.rank_key)
    assert ranked[0] is same
    assert dn._tied_with(ranked[0], ranked) == ["b"]


# ---------------------------------------------------------------------------
# Old records still load
# ---------------------------------------------------------------------------

def test_check_scores_accepts_old_and_new_shape():
    rp.check_scores({"confidence_real": 2}, "w")
    rp.check_scores({"confidence_real": 2, "distance_to_profitable": 1,
                     "mechanism_plausibility": 3}, "w")


@pytest.mark.parametrize("bad", [
    {}, {"distance_to_profitable": 1}, {"confidence_real": 4},
    {"confidence_real": 1, "mechanism_plausibility": 9},
    {"confidence_real": 1, "something_else": 1}, None,
])
def test_check_scores_still_refuses_malformed(bad):
    with pytest.raises(rp.ProposalError):
        rp.check_scores(bad, "w")


def test_an_old_proposal_loads_and_its_candidate_drops_the_retired_fields():
    old = _patch("profitability-run_061-1", conf=2, dist=3, mech=3)
    assert set(old["scores"]) == {"confidence_real", *RETIRED}
    rec = _decide(_one_source([old]))
    cand = _by_id(rec)["profitability-run_061-1"]
    assert cand["scores"]["confidence_real"] == 2
    for name in RETIRED:
        assert name not in cand["scores"]


def test_old_and_new_card_scores_validate_and_return_only_confidence():
    old = {"scores": {"confidence_real": 1, "distance_to_profitable": 2,
                      "mechanism_plausibility": 3},
           "model_id": "m", "rubric_version": dn.BRIEF_CARD_RUBRIC}
    new = {"scores": {"confidence_real": 1}, "model_id": "m", "rubric_version": dn.BRIEF_CARD_RUBRIC}
    for item in (old, new):
        out = dn.validate_card_scores(item, "w")
        assert out == {"confidence_real": 1, "model_id": "m",
                       "rubric_version": dn.BRIEF_CARD_RUBRIC}
    bad = copy.deepcopy(new)
    del bad["scores"]["confidence_real"]
    with pytest.raises(dn.DecideNextError):
        dn.validate_card_scores(bad, "w")


def _validator(name):
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    return jsonschema, schema


def test_decision_record_schema_accepts_old_and_new_candidates_and_tie_with():
    jsonschema, schema = _validator("decision_record.schema.json")
    rec = _decide(_one_source([_patch("profitability-run_061-1", after=0.6, conf=2),
                               _patch("profitability-run_061-2", after=0.7, conf=2)]))
    assert rec["picked"]["tie_with"] == ["profitability-run_061-2"]
    cand_ref = {"$defs": schema["$defs"], "$ref": "#/$defs/candidate"}
    new_cand = copy.deepcopy(rec["candidates"][0])
    jsonschema.validate(new_cand, cand_ref)
    old_cand = copy.deepcopy(new_cand)
    old_cand["scores"].update(distance_to_profitable=1, mechanism_plausibility=2)
    jsonschema.validate(old_cand, cand_ref)                            # a pre-D-194 record
    picked_ref = {"$defs": schema["$defs"], **schema["properties"]["picked"]}
    jsonschema.validate(rec["picked"], picked_ref)
    no_tie = {k: v for k, v in rec["picked"].items() if k != "tie_with"}
    jsonschema.validate(no_tie, picked_ref)                            # the key stays optional
    bad = dict(rec["picked"], tie_with="profitability-run_061-2")      # a string, not a list
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, picked_ref)


# ---------------------------------------------------------------------------
# Nothing new writes the retired fields
# ---------------------------------------------------------------------------

def test_no_new_decision_record_carries_either_field():
    # the inputs are OLD (they carry both fields); the record written from them must not
    old = [_patch("profitability-run_061-1", after=0.6, conf=2, dist=3, mech=3),
           _patch("profitability-run_061-2", after=0.7, conf=1, dist=2, mech=2)]
    text = json.dumps(_decide(_one_source(old)))
    for name in RETIRED:
        assert name not in text


def test_the_constants_are_gone_from_the_ranking_and_analyst_code():
    for rel in ("tools/decide_next.py", "tools/analyst_session.py"):
        text = (_SR / rel).read_text(encoding="utf-8")
        for name in RETIRED:
            assert name not in text, f"{rel} still names {name}"
    assert "FIXED_SCORE" not in (_SR / "tools" / "analyst_session.py").read_text(encoding="utf-8")
    assert rp.SCORE_KEYS == ("confidence_real",)


@pytest.mark.parametrize("rel", [
    "workflow_artifacts/skills/hypothesis-design/BRIEF_HYPOTHESES.md",
])
def test_the_prompts_that_ask_for_scores_no_longer_ask_for_the_retired_ones(rel):
    text = (_SR / rel).read_text(encoding="utf-8")
    for name in RETIRED:
        assert name not in text, f"{rel} still names {name}"
    assert "confidence_real" in text


def test_step_1a_is_no_longer_handed_the_block_registry():
    src = (_SR / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    start = src.index("def _apply_brief_hypotheses_context")
    body = src[start:src.index("\ndef ", start + 10)]
    assert "block_registry" not in body and "distance_to" not in body

