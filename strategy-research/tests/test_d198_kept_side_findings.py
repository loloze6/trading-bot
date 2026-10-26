"""
D-198: the kept side-finding code, restored after the reader-only test files went.

These tests come from origin/master's test_e068_5_readers_v3.py. They cover code that is
still live after the five readers are deleted: the reading shape check (reader_proposals),
the side-finding review and test requests (reader_findings), and the decide_next candidate
rules (the analyst writes the same reading shape).

Dropped as tests of deleted code: the reader stage, prompts, handoffs, digest and skip rules,
the v2 SKILL bytes, the model-answer validation (`_validate_reader_output`), the reader
worker's review landing, and the pre-filled-claim step 1a notes. No LLM is called.
"""
import copy
import json
import re
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import reader_proposals as rp  # noqa: E402
import reader_findings as rf  # noqa: E402
import decide_next as dn  # noqa: E402
import claim_findings as cf  # noqa: E402

from _reader_test_helpers import (  # noqa: E402,F401
    FIX4, FIX5, RUN_ID, _claim, _inputs, _memory_entry, _patch, _reading, _scores, _side,
    _side_with_change, _src, _write)

HIGH_HASH = "c688b1863f8cb3ff4d3a3bb05e0c15d5b885d27a65d3b805ad1990263fa83a99"


# ---------------------------------------------------------------------------
# The reading shape
# ---------------------------------------------------------------------------

def test_a_legacy_reading_with_a_patch_still_loads_and_flattens(tmp_path):
    """Continuation 2: a v3 file written before the patch was removed (runs 070-074)."""
    doc = _reading(patch=_patch())
    _write(tmp_path / "trade_efficiency.yaml", doc)
    items = rp.load_proposals(tmp_path, ["trade_efficiency"])["trade_efficiency"]
    assert [(i["proposal_id"], i["kind"]) for i in items] == [
        (f"trade_efficiency-{RUN_ID}-1", "side_finding"), (f"trade_efficiency-{RUN_ID}-2", "patch")]
    assert all(i["model_id"] == "m" and i["rubric_version"] == "trade_efficiency-reading-v1"
               for i in items)
    assert items[1]["patch"] == _patch()["patch"]
    assert rp.load_readings(tmp_path, ["trade_efficiency"])["trade_efficiency"] == doc


_BAD = [
    ("verdict key", lambda d: d.update(supports=True), "undeclared field"),
    ("claim_status key", lambda d: d.update(claim_status="measured"), "undeclared field"),
    ("idea_status key", lambda d: d.update(idea_status="refuted"), "undeclared field"),
    ("no explanation", lambda d: d.pop("explanation"), "missing"),
    ("blank explanation", lambda d: d.update(explanation=" "), "explanation"),
    ("empty evidence", lambda d: d.update(evidence=[]), "evidence"),
    ("three side findings", lambda d: d.update(side_findings=[
        {"proposal_id": f"{d['reading_id']}-{n}", "claim": _claim(), "evidence": ["e"],
         "scores": _scores()} for n in (1, 2, 3)]), "at most 2"),
    ("bad id", lambda d: d["side_findings"][0].update(proposal_id="trade_efficiency-x-1"),
     "proposal_id"),
    ("claim not a mapping", lambda d: d["side_findings"][0].update(claim="x"), "claim block"),
    ("side verdict key", lambda d: d["side_findings"][0].update(refutes=True), "side finding"),
    ("bad score", lambda d: d["side_findings"][0]["scores"].update(confidence_real=4), "0..3"),
    ("patch item", lambda d: d.update(patch={**_patch(), "patch": [{"component_id": "a",
                                                                     "field": "f"}]}),
     "component_id, field, before, after"),
    ("duplicate id", lambda d: d.update(patch=_patch(n=1)), "duplicate"),
    ("wrong category", lambda d: d.update(reading_id=f"profitability-{RUN_ID}"), "reading_id"),
]


@pytest.mark.parametrize("label,mutate,match", _BAD, ids=[b[0] for b in _BAD])
def test_a_malformed_reading_is_refused(tmp_path, label, mutate, match):
    doc = _reading()
    mutate(doc)
    _write(tmp_path / "trade_efficiency.yaml", doc)
    with pytest.raises(rp.ProposalError, match=re.escape(match) if " " in match else match):
        rp.load_proposals(tmp_path, ["trade_efficiency"])


def test_skipped_is_written_by_code_only():
    doc = rf.skipped_reading("regime_power", RUN_ID, {"rule": rf.SKIP_REGIME_SCAFFOLDING,
                                                      "reason": "r"})
    rp.check_reading(doc, "regime_power", "w")              # code's file: accepted
    with pytest.raises(rp.ProposalError, match="written by code only"):
        rp.check_reading(doc, "regime_power", "w", from_model=True)
    bad = {**doc, "skipped": {"rule": "nothing_to_say", "reason": "r"}}
    with pytest.raises(rp.ProposalError, match="rule in"):
        rp.check_reading(bad, "regime_power", "w")


def test_v2_and_v3_files_load_side_by_side(tmp_path):
    shutil.copyfile(FIX5 / "trade_efficiency_v2.yaml", tmp_path / "trade_efficiency.yaml")
    shutil.copyfile(FIX5 / "regime_power_v2.yaml", tmp_path / "regime_power.yaml")
    _write(tmp_path / "profitability.yaml", _reading("profitability", run_id="run_070"))
    out = rp.load_proposals(tmp_path, ["trade_efficiency", "regime_power", "profitability"])
    assert out["trade_efficiency"][0]["proposal_id"] == "trade_efficiency-run_070-1"
    assert out["regime_power"][0]["kind"] == "new_block"
    assert out["profitability"][0]["kind"] == "side_finding"




def test_a_model_written_patch_is_refused_with_the_new_shape():
    """Continuation 2: the stand-alone patch is removed from what a reader writes."""
    with pytest.raises(rp.ProposalError, match="config_change"):
        rp.check_reading(_reading(patch=_patch()), "trade_efficiency", "w", from_model=True)
    with pytest.raises(rp.ProposalError, match="the stand-alone `patch` is removed"):
        rp.check_reading(_reading(patch=_patch()), "trade_efficiency", "w", from_model=True)
    rp.check_reading(_reading(), "trade_efficiency", "w", from_model=True)   # no patch: fine



@pytest.mark.parametrize("change,match", [
    ([], "non-empty list"), ("x", "non-empty list"),
    ([{"component_id": "a", "field": "f"}], "component_id, field, before, after")])
def test_a_malformed_config_change_is_refused(change, match):
    side = {**_side_with_change(), "config_change": change}
    with pytest.raises(rp.ProposalError, match=match):
        rp.check_reading(_reading(sides=[side]), "trade_efficiency", "w", from_model=True)



# ---------------------------------------------------------------------------
# Side findings: warnings, candidates
# ---------------------------------------------------------------------------

def test_review_of_a_side_finding():
    item = {"claim": _claim()}
    clean = rf.side_finding_review(item, prior={}, own=set(), run_id="r")
    assert clean["errors"] == [] and clean["warnings"] == [] and len(clean["spec_hashes"]) == 1
    h = clean["spec_hashes"][0]
    prior = {h: [{"run_id": "run_060", "status": "measured"}]}
    w = rf.side_finding_review(item, prior=prior, own=set(), run_id="r")["warnings"]
    assert w == [{"kind": rf.WARN_REPEAT, "spec_hash": h, "own_claim": False,
                  "runs": prior[h]}]
    w = rf.side_finding_review(item, prior=prior, own={h}, run_id="r")["warnings"]
    assert w[0]["own_claim"] is True and w[0]["runs"] == [{"run_id": "r", "status": None}]


def test_a_pure_finding_may_be_blind_a_block_claim_gets_a_warning():
    pure = rf.side_finding_review({"claim": _claim(kind="event_behaviour", field="close")},
                                  prior={}, own=set(), run_id="r")
    assert pure["errors"] == [] and pure["warnings"] == []
    block = rf.side_finding_review({"claim": _claim(kind="direction_forecast", field="close")},
                                   prior={}, own=set(), run_id="r")
    assert block["errors"] == [] and [w["kind"] for w in block["warnings"]] == [rf.WARN_BLIND]
    seeing = rf.side_finding_review({"claim": _claim(kind="direction_forecast",
                                                     field="forecast")},
                                    prior={}, own=set(), run_id="r")
    assert seeing["warnings"] == []


def test_tests_none_is_a_test_request():
    claim = {**_claim(), "tests": "none", "missing_block": "order book imbalance field"}
    review = rf.side_finding_review({"claim": claim}, prior={}, own=set(), run_id="r")
    assert review["tests_none"] and review["missing_block"] == "order book imbalance field"
    row = rf.test_request_row("run_070", "H-1", "trade_efficiency",
                              {"proposal_id": "trade_efficiency-run_070-1", "claim": claim},
                              review)
    assert row["hypothesis_id"] == "H-1__trade_efficiency-run_070-1"
    assert row["missing_block"] == "order book imbalance field"


# decide-next -------------------------------------------------------------

def test_a_side_finding_becomes_an_eligible_candidate():
    p = _side()
    cand = dn._candidate("run_070", _memory_entry(), _src([p]), "trade_efficiency", p,
                         _inputs(), {})
    assert cand["kind"] == "side_finding" and cand["eligible"] is True
    assert cand["gates"]["feasibility"]["result"] == "UNKNOWN"
    assert cand["gates"]["novelty"]["exact_match"] == "NOT_APPLICABLE"
    assert len(cand["gates"]["novelty"]["spec_hashes"]) == 1
    assert cand["hypothesis_id"] == "H-070__trade_efficiency-run_070-1"
    assert "warnings" not in cand


def test_a_repeated_test_is_a_warning_never_a_refusal():
    p = _side()
    h = rf.side_finding_review(p, prior={}, own=set(), run_id="x")["spec_hashes"][0]
    memory = {"runs": {"run_060": {cf.FINDING_KEY: {"status": "measured",
                                                    "tests": [{"spec_hash": h}]}}}}
    cand = dn._candidate("run_070", _memory_entry(), _src([p]), "trade_efficiency", p,
                         _inputs(memory), {})
    assert cand["eligible"] is True
    assert cand["warnings"] == [{"kind": rf.WARN_REPEAT, "spec_hash": h, "own_claim": False,
                                 "runs": [{"run_id": "run_060", "status": "measured"}]}]


def test_repeating_the_source_runs_own_claim_is_a_warning():
    card = yaml.safe_load((FIX4 / "artifacts" / "hypothesis_card.yaml").read_text(
        encoding="utf-8"))
    own_test = copy.deepcopy(card["claim"]["tests"][0])
    p = _side(claim=_claim(tests=[own_test]))
    cand = dn._candidate("run_070", _memory_entry(), _src([p]), "trade_efficiency", p,
                         _inputs(), {})
    assert cand["eligible"] is True
    assert cand["warnings"][0]["spec_hash"] == HIGH_HASH and cand["warnings"][0]["own_claim"]


@pytest.mark.parametrize("claim,reason", [
    ({**_claim(), "tests": "none", "missing_block": "m"}, "next_test_none"),
    ({**_claim(), "kind": "not_a_kind"}, "next_test_refused"),
    ({**_claim(), "kind": ["a", "list"]}, "next_test_refused"),   # review fix 5: no crash
    (_claim(kind="regime_classifier"), "regime_block_needs_composition"),
])
def test_ineligible_side_findings(claim, reason):
    p = _side(claim=claim)
    cand = dn._candidate("run_070", _memory_entry(), _src([p]), "trade_efficiency", p,
                         _inputs(), {})
    assert cand["eligible"] is False
    assert any(r.startswith(reason) for r in cand["gates"]["feasibility"]["reasons"])


def test_two_readers_with_the_same_tests_collapse():
    a, b = _side("trade_efficiency"), _side("profitability")
    b["scores"] = _scores(3)
    src = _src([a, b])
    cands = [dn._candidate("run_070", _memory_entry(), src, c, p, _inputs(), {})
             for c, p in (("trade_efficiency", a), ("profitability", b))]
    out = dn._collapse(cands)
    assert len(out) == 1 and out[0]["candidate_id"] == "profitability-run_070-1"


def test_a_decision_record_with_side_findings_matches_its_schema():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas"
                         / "decision_record.schema.json").read_text(encoding="utf-8"))
    card = yaml.safe_load((FIX4 / "artifacts" / "hypothesis_card.yaml").read_text(
        encoding="utf-8"))
    repeat = _side("trade_efficiency", 1, claim=_claim(tests=[copy.deepcopy(
        card["claim"]["tests"][0])]))
    blind = _side("forecast_power", 1, claim=_claim(kind="direction_forecast", field="close"))
    none = _side("profitability", 1, claim={**_claim(), "tests": "none", "missing_block": "m"})
    src = _src([{"category": c, "proposal": p} for c, p in
                (("trade_efficiency", repeat), ("forecast_power", blind), ("profitability", none))])
    inputs = _inputs(memory={"runs": {"run_070": _memory_entry()}}, runs={"run_070": src})
    record = dn.decide(inputs, now="2026-10-05T00:00:00Z",
                       trigger={"after_run": "run_070", "after_entry": "E068",
                                "idea_status": "refuted"})
    kinds = sorted((c["candidate_id"], c["eligible"], [w["kind"] for w in c.get("warnings", [])])
                   for c in record["candidates"])
    assert kinds == [("forecast_power-run_070-1", True, [rf.WARN_BLIND]),
                     ("profitability-run_070-1", False, []),
                     ("trade_efficiency-run_070-1", True, [rf.WARN_REPEAT])]
    errors = sorted(e.message for e in jsonschema.Draft202012Validator(schema).iter_errors(
        yaml.safe_load(yaml.safe_dump(record))))
    assert errors == []

