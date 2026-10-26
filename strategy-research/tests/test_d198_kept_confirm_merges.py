"""
D-198: the kept explore/confirm and in-run merge code, restored after the reader-only test
files went.

From origin/master's test_e072_explore_confirm.py (tools/explore_confirm.py is kept: the fold
confirmation and the analyst's memory view use it, and the ledger functions) and the merge half
of test_e073_citations_dedup.py (reader_findings.side_finding_merges and decide_next's
merge collapse are kept).

Dropped as tests of deleted code: the readers stage, the exploration copies the readers were
given, the reader prompts and handoffs, the readers' skip rules, the citation value check and
its retry, and the explore_confirm flag routing in the stage. The stage-level tests that
measured findings through the stage now call the explore_confirm functions in the same
sequence the deleted `_record_confirmations` used (`_confirm_stage` below). No LLM, no backtest.
"""
import copy
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import reader_proposals as rp  # noqa: E402
import reader_findings as rf  # noqa: E402
import decide_next as dn  # noqa: E402
import explore_confirm as ec  # noqa: E402
import claim_measure as cmeas  # noqa: E402

from _reader_test_helpers import (  # noqa: E402,F401
    EC_ON, RUN_ID, _block_claim, _child_run, _claim, _confirmation, _ec_run, _eras_holdout,
    _inputs, _memory_entry, _pure_claim, _reading, _save, _scores, _sides, _src, _write,
    _stub_tbot_python)


def _split(run_dir: Path, run_id: str = RUN_ID) -> dict:
    """What protocol_execution did at entry under the flag: the pre-registered split."""
    return ec.ensure_split(run_dir / "artifacts", run_id,
                           extra_files=[run_dir / "protocol.json"])


def _confirm_stage(run_dir: Path, run_id: str, readings: dict, merges=None) -> list:
    """The deleted `_record_confirmations`, on the kept explore_confirm functions: each side
    finding measured on the confirmation windows (or pending), a pending finding this run was
    built from resolved under the ledger lock, the run's confirmation.yaml written."""
    arts = run_dir / "artifacts"
    split = ec.load_split(arts)
    eras, holdout_start = _eras_holdout()
    records = ec.confirm_findings(run_dir, run_id, readings, split, base_variant="base",
                                  eras=eras, holdout_start=holdout_start,
                                  **({"merges": merges} if merges is not None else {}))
    source = ec.source_finding_id(arts)

    def _resolve(findings: dict) -> list:
        pending = ec.pending_for(findings, source, run_id)
        if pending is None:
            return []
        return [ec.resolve_pending(run_dir, run_id, pending, split, base_variant="base",
                                   eras=eras, holdout_start=holdout_start)]
    written = ec.record(rpr.ROOT, run_id, records, resolve=_resolve if source else None)
    rpr.save_yaml(arts / ec.CONFIRMATION_ARTIFACT, {
        "schema_version": ec.SCHEMA_VERSION, "run_id": run_id, "note": ec.LEDGER_NOTE,
        "bar": ec.HONEST_BAR, "exploration": ec.labels(split["exploration"]),
        "confirmation": ec.labels(split["confirmation"]),
        "side_findings": written[:len(records)], "resolved_pending": written[len(records):]})
    return written


def _readings_of(sides: dict, run_id: str = RUN_ID) -> dict:
    return {cat: _reading(cat, run_id=run_id, sides=sides.get(cat, []))
            for cat in rpr.READER_CATEGORIES}


# ---------------------------------------------------------------------------
# explore_confirm: routes, sign rule, ledger
# ---------------------------------------------------------------------------

def test_routes_of_side_findings():
    assert ec.finding_route({"claim": _pure_claim()})[0] == ec.IN_RUN
    assert ec.finding_route({"claim": _block_claim()})[0] == ec.PENDING
    regime = {**_block_claim(), "kind": "regime_classifier"}
    assert ec.finding_route({"claim": regime})[0] == ec.PENDING
    reads_forecast = copy.deepcopy(_pure_claim())
    reads_forecast["tests"][0]["selector"] = {"kind": "event", "field": "forecast",
                                              "op": ">", "value": 0.0}
    change = [{"component_id": "c", "field": "params.p", "before": 1, "after": 2}]
    assert ec.finding_route({"claim": reads_forecast})[0] == ec.IN_RUN
    assert ec.finding_route({"claim": reads_forecast, "config_change": change})[0] == ec.PENDING
    assert ec.finding_route({"claim": _pure_claim(), "config_change": change})[0] == ec.IN_RUN
    none = {**_pure_claim(), "tests": "none", "missing_block": "x"}
    assert ec.finding_route({"claim": none})[0] == ec.NOT_MEASURABLE


def test_sign_rule():
    def r(*oriented, status=cmeas.MEASURED):
        return {"status": status, "horizons": {i + 1: {"oriented": o}
                                               for i, o in enumerate(oriented)}}
    assert ec.test_sign(r(0.1, 0.2))[0] is True
    assert ec.test_sign(r(0.1, None))[0] is True
    assert ec.test_sign(r(0.1, -0.2))[0] is False
    assert ec.test_sign(r(0.0))[0] is False
    assert ec.test_sign(r(None))[0] is False
    assert ec.test_sign(r(status=cmeas.NO_EVENTS))[0] is False
    assert ec.test_sign({"status": cmeas.NOT_MEASURED, "reason": "error"})[0] is None
    assert ec.finding_sign({"a": r(0.1), "b": r(-0.1)})[0] is False
    assert ec.finding_sign({"a": r(0.1), "b": {"status": "not_measured"}})[0] is None
    assert ec.finding_sign({"a": r(0.1), "b": r(0.3)})[0] is True



def test_readings_without_side_findings_and_an_absent_ledger_load(tmp_path):
    assert ec.load_ledger(tmp_path) == {}
    assert ec.side_finding_items({"profitability": _reading("profitability", sides=[]),
                                  "regime_power": {"schema_version": 3,
                                                   "reading_id": f"regime_power-{RUN_ID}",
                                                   "skipped": {"rule": "r", "reason": "x"}}}) == []
    assert ec.source_finding_id(tmp_path) is None



def test_a_rerun_never_removes_a_finding_another_run_measured(tmp_path):
    ec.record(tmp_path, "run_1", [{"finding_id": "a", "source_run": "run_1",
                                   "confirmation_sign_retained": True,
                                   "measured_in_run": "run_2"}])
    ec.record(tmp_path, "run_1", [])
    assert "a" in ec.load_ledger(tmp_path)["findings"]



def test_a_rerun_replaces_only_a_pending_or_same_run_record(tmp_path):
    def rec(**kw):
        return {"finding_id": "f", "source_run": "run_1", "finding_spec_hashes": ["h"], **kw}
    ec.record(tmp_path, "run_1", [rec(confirmation_sign_retained=ec.PENDING)])
    ec.record(tmp_path, "run_1", [rec(confirmation_sign_retained=True, measured_in_run="run_1")])
    assert ec.load_ledger(tmp_path)["findings"]["f"]["confirmation_sign_retained"] is True
    ec.record(tmp_path, "run_1", [rec(confirmation_sign_retained=False, measured_in_run="run_1")])
    assert ec.load_ledger(tmp_path)["findings"]["f"]["confirmation_sign_retained"] is False
    # pending again (a block claim), then resolved by run_2: a re-run of run_1
    # may not replace that
    ec.record(tmp_path, "run_1", [rec(confirmation_sign_retained=ec.PENDING)])
    ec.record(tmp_path, "run_2", [rec(confirmation_sign_retained=True, measured_in_run="run_2")])
    assert ec.load_ledger(tmp_path)["findings"]["f"]["measured_in_run"] == "run_2"
    written = ec.record(tmp_path, "run_1", [rec(confirmation_sign_retained=ec.PENDING)])
    doc = ec.load_ledger(tmp_path)
    assert doc["findings"]["f"]["measured_in_run"] == "run_2"
    assert doc["superseded"][-1]["run_id"] == "run_1" and "run_2" in written[0]["ledger"]


# --- finding 3: a malformed ledger never breaks the campaign summary ----------

@pytest.mark.parametrize("doc", [[1, 2], {"by_set": []}, {"by_set": ["x"]},
                                 {"findings": ["x"]}, "just a string"])
def test_a_malformed_ledger_gives_one_unreadable_line(doc, tmp_path):
    _save(tmp_path / ec.LEDGER_REL, doc)
    lines = ec.summary_lines(tmp_path)
    assert lines[-1].startswith(f"- {ec.LEDGER_REL} is unreadable")
    assert len([x for x in lines if x.strip()]) == 2                 # the title and that line


def test_a_wellformed_ledger_without_by_set_still_summarises(tmp_path):
    _save(tmp_path / ec.LEDGER_REL, {"findings": {"f": {"confirmation_sign_retained": True}}})
    assert any("Side findings: 1 (held 1" in x for x in ec.summary_lines(tmp_path))


# ---------------------------------------------------------------------------
# explore_confirm: a pending finding resolved by the run built from it
# ---------------------------------------------------------------------------

def _seed_pending(monkeypatch) -> dict:
    """run_990 proposes a block claim (pending); returns its ledger record."""
    run_dir = _ec_run(monkeypatch)
    _split(run_dir)
    _confirm_stage(run_dir, RUN_ID, _readings_of(_sides()))
    return ec.load_ledger(rpr.ROOT)["findings"][f"forecast_power-{RUN_ID}-1"]


def test_a_resume_after_resolution_keeps_resolved_pending(monkeypatch):
    _seed_pending(monkeypatch)
    child = _child_run(monkeypatch, "run_991")
    _split(child, "run_991")
    none = _readings_of({}, "run_991")
    _confirm_stage(child, "run_991", none)
    first = ec.load_ledger(rpr.ROOT)
    _confirm_stage(child, "run_991", none)                        # a resume
    doc = _confirmation(child)
    assert [r["finding_id"] for r in doc["resolved_pending"]] == [f"forecast_power-{RUN_ID}-1"]
    again = ec.load_ledger(rpr.ROOT)
    rec = again["findings"][f"forecast_power-{RUN_ID}-1"]
    assert rec["measured_in_run"] == "run_991" and rec["status"] == ec.MEASURED
    assert [a["run_id"] for a in rec["attempts"]] == ["run_991"]     # replaced, not appended
    assert again["by_set"] == first["by_set"]                        # no look counted twice
    assert rec["confirmation_sign_retained"] == \
        first["findings"][f"forecast_power-{RUN_ID}-1"]["confirmation_sign_retained"]
    assert rec["pending_state"]["confirmation_sign_retained"] == ec.PENDING


def test_the_pending_lookup_reads_the_ledger_under_its_lock(monkeypatch):
    """The lookup reads the findings ec.record hands it under the lock -- not
    an unlocked load_ledger copy (here a stale, empty view)."""
    _seed_pending(monkeypatch)
    child = _child_run(monkeypatch, "run_991")
    _split(child, "run_991")
    monkeypatch.setattr(ec, "load_ledger", lambda root: {})
    _confirm_stage(child, "run_991", _readings_of({}, "run_991"))
    assert _confirmation(child)["resolved_pending"][0]["measured_in_run"] == "run_991"


# ---------------------------------------------------------------------------
# In-run merges (reader_findings.side_finding_merges, explore_confirm, decide_next)
# ---------------------------------------------------------------------------

def _side(cat, n=1, claim=None, change=None, scores=2, run_id=RUN_ID) -> dict:
    s = {"proposal_id": f"{cat}-{run_id}-{n}", "claim": claim or _pure_claim(),
         "evidence": ["exploration only"], "scores": _scores(scores)}
    if change is not None:
        s["config_change"] = change
    return s


def _readings(sides: dict, run_id=RUN_ID) -> dict:
    return {cat: _reading(cat, run_id=run_id, sides=s) for cat, s in sides.items()}


CHANGE = [{"component_id": "shock_reversal", "field": "params.period", "before": 1, "after": 2}]


def test_the_same_tests_from_two_readers_merge_into_one_listing_both():
    groups = rf.side_finding_merges(_readings({
        "trade_efficiency": [_side("trade_efficiency")],
        "forecast_power": [_side("forecast_power")]}))
    [g] = groups
    assert g["finding_id"] == f"forecast_power-{RUN_ID}-1"          # categories sorted
    assert g["finding_ids"] == [f"forecast_power-{RUN_ID}-1", f"trade_efficiency-{RUN_ID}-1"]
    assert g["sources"] == [{"category": "forecast_power", "finding_id": g["finding_ids"][0]},
                            {"category": "trade_efficiency", "finding_id": g["finding_ids"][1]}]
    assert len(g["spec_hashes"]) == 1 and g["config_change"] is None


def test_what_is_not_merged():
    other = copy.deepcopy(_pure_claim())
    other["tests"].append({**copy.deepcopy(other["tests"][0]), "name": "second",
                           "outcome": {"kind": "fwd_return", "horizons": [2]}})
    none = {**_pure_claim(), "tests": "none", "missing_block": "m"}
    assert rf.side_finding_merges(_readings({            # different config change
        "trade_efficiency": [_side("trade_efficiency", change=CHANGE)],
        "forecast_power": [_side("forecast_power")]})) == []
    assert rf.side_finding_merges(_readings({            # a partial overlap
        "trade_efficiency": [_side("trade_efficiency", claim=other)],
        "forecast_power": [_side("forecast_power")]})) == []
    assert rf.side_finding_merges(_readings({            # tests: none
        "trade_efficiency": [_side("trade_efficiency", claim=none)],
        "forecast_power": [_side("forecast_power", claim=none)]})) == []
    same_change = rf.side_finding_merges(_readings({     # the same change: merged
        "trade_efficiency": [_side("trade_efficiency", change=CHANGE)],
        "forecast_power": [_side("forecast_power", change=copy.deepcopy(CHANGE))]}))
    assert len(same_change) == 1 and same_change[0]["config_change"] == CHANGE


def test_a_statement_or_score_difference_does_not_prevent_a_merge():
    words = {**_pure_claim(), "statement": "Other words, same test.", "rationale": "x"}
    groups = rf.side_finding_merges(_readings({
        "trade_efficiency": [_side("trade_efficiency", claim=words, scores=3)],
        "forecast_power": [_side("forecast_power", scores=1)],
        "profitability": [_side("profitability", scores=0)]}))
    assert len(groups) == 1 and len(groups[0]["sources"]) == 3


def _two_readers_same_test():
    return {"trade_efficiency": [_side("trade_efficiency")],
            "forecast_power": [_side("forecast_power")]}



def _merges_of(run_dir: Path, readings: dict) -> dict:
    """The kept `_record_side_finding_merges`: reads artifacts/proposals/, writes
    side_finding_merges.yaml, returns the merge index."""
    for cat, doc in readings.items():
        _write(run_dir / "artifacts" / "proposals" / f"{cat}.yaml", doc)
    return rpr._record_side_finding_merges(RUN_ID, run_dir)


def test_a_merged_finding_is_measured_and_counted_once(monkeypatch):
    run_dir = _ec_run(monkeypatch, flags=EC_ON, conf_sign=1.0)
    _split(run_dir)
    readings = _readings(_two_readers_same_test())
    merges = _merges_of(run_dir, readings)
    doc = yaml.safe_load((run_dir / "artifacts" / rf.MERGES_ARTIFACT).read_text(encoding="utf-8"))
    assert doc["note"] == rf.MERGE_NOT_AGREEMENT and len(doc["merged"]) == 1
    primary, dup = doc["merged"][0]["finding_ids"]
    _confirm_stage(run_dir, RUN_ID, readings, merges)
    [rec] = _confirmation(run_dir)["side_findings"]
    assert rec["finding_id"] == primary and rec["merged_finding_ids"] == [dup]
    assert [s["finding_id"] for s in rec["sources"]] == [primary, dup]
    assert rec["merge_note"] == rf.MERGE_NOT_AGREEMENT
    assert rec["confirmation_sign_retained"] is True
    ledger = ec.load_ledger(rpr.ROOT)
    assert set(ledger["findings"]) == {primary}
    key = ec.set_key(ec.load_split(run_dir / "artifacts")["confirmation"])
    assert ledger["by_set"] == {key: {"n_looks": 1, "n_comparisons": 1}}
    assert [ln for ln in ec.summary_lines(rpr.ROOT) if "Side findings:" in ln][0].startswith(
        "- Side findings: 1 (held 1,")
    # a resumed confirmation measures and counts nothing again
    _confirm_stage(run_dir, RUN_ID, readings, merges)
    assert ec.load_ledger(rpr.ROOT)["by_set"] == {key: {"n_looks": 1, "n_comparisons": 1}}


def test_a_run_built_from_the_duplicate_resolves_the_primary():
    findings = {"forecast_power-run_990-1": {
        "finding_id": "forecast_power-run_990-1", "confirmation_sign_retained": ec.PENDING,
        "merged_finding_ids": ["trade_efficiency-run_990-1"]}}
    assert ec.pending_for(findings, "trade_efficiency-run_990-1", "run_991") \
        is findings["forecast_power-run_990-1"]
    assert ec.pending_for(findings, "profitability-run_990-1", "run_991") is None
    assert ec.pending_for(findings, "forecast_power-run_990-1", "run_991") \
        is findings["forecast_power-run_990-1"]


# decide-next ---------------------------------------------------------------
def _dn_side(cat, scores=2) -> dict:
    return {"proposal_id": f"{cat}-run_070-1", "kind": rp.SIDE_FINDING, "claim": _claim(),
            "evidence": ["e"], "scores": _scores(scores), "model_id": "m",
            "rubric_version": f"{cat}-reading-v1"}


def _merged_src(a, b) -> dict:
    src = _src([{"category": "forecast_power", "proposal": a},
                {"category": "trade_efficiency", "proposal": b}])
    ids = [a["proposal_id"], b["proposal_id"]]
    doc = rf.merges_doc("run_070", [{"finding_id": ids[0], "finding_ids": ids,
                                     "sources": [{"category": "forecast_power",
                                                  "finding_id": ids[0]},
                                                 {"category": "trade_efficiency",
                                                  "finding_id": ids[1]}],
                                     "spec_hashes": ["h"], "config_change": None}])
    src["side_finding_merges"] = rf.merge_index(doc)
    return src


def _decide(src) -> dict:
    inputs = _inputs(memory={"runs": {"run_070": _memory_entry()}}, runs={"run_070": src})
    return dn.decide(inputs, now="2026-10-08T00:00:00Z",
                     trigger={"after_run": "run_070", "after_entry": "E", "idea_status": "refuted"})


def test_a_merged_pair_is_one_candidate_with_the_primarys_scores():
    a, b = _dn_side("forecast_power", scores=1), _dn_side("trade_efficiency", scores=3)
    rec = _decide(_merged_src(a, b))
    [cand] = rec["candidates"]
    assert cand["candidate_id"] == "forecast_power-run_070-1" and cand["rank"] == 1
    assert cand["scores"]["confidence_real"] == 1          # never the higher of the two
    assert cand["merged_sources"] == [
        "runs/run_070/artifacts/proposals/forecast_power.yaml#forecast_power-run_070-1",
        "runs/run_070/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_070-1"]
    assert cand["merge_note"] == dn.MERGE_NOTE and cand["collapsed_sources"] == []
    assert "_merge" not in cand
    # without the merge file the existing collapse keeps the higher score (unchanged)
    src = _merged_src(a, b)
    del src["side_finding_merges"]
    [plain] = _decide(src)["candidates"]
    assert plain["candidate_id"] == "trade_efficiency-run_070-1" and "merged_sources" not in plain


def test_a_duplicate_whose_primary_is_ineligible_stays_its_own_candidate():
    a = {**_dn_side("forecast_power"), "claim": {**_claim(), "tests": "none",
                                                 "missing_block": "m"}}
    b = _dn_side("trade_efficiency")
    rec = _decide(_merged_src(a, b))
    elig = [c for c in rec["candidates"] if c["eligible"]]
    assert [c["candidate_id"] for c in elig] == ["trade_efficiency-run_070-1"]
    assert "merged_sources" not in elig[0]



def test_load_inputs_reads_the_merge_file_only_when_it_exists(tmp_path):
    """D-198: only the merge file is read; an old run's citation_checks/ is not."""
    arts = tmp_path / "artifacts"
    arts.mkdir()
    assert dn._observable_inputs(arts) == {}
    rpr.save_yaml(arts / rf.MERGES_ARTIFACT, rf.merges_doc("run_070", []))
    (arts / "citation_checks").mkdir()
    rpr.save_yaml(arts / "citation_checks" / "trade_efficiency.yaml",
                  {"items": {"trade_efficiency-run_070-1": {"bad": [{"path": "p"}]}}})
    assert dn._observable_inputs(arts) == {"side_finding_merges": {}}


def test_flag_off_confirm_findings_is_unchanged_without_merges(monkeypatch):
    run_dir = _ec_run(monkeypatch, flags=EC_ON, conf_sign=1.0)
    split = _split(run_dir)
    readings = _readings(_two_readers_same_test())
    eras, holdout = _eras_holdout()
    kw = dict(base_variant="base", eras=eras, holdout_start=holdout)
    assert ec.confirm_findings(run_dir, RUN_ID, readings, split, **kw) \
        == ec.confirm_findings(run_dir, RUN_ID, readings, split, merges=None, **kw) \
        == ec.confirm_findings(run_dir, RUN_ID, readings, split, merges={}, **kw)


def test_the_same_tests_under_two_claim_kinds_are_not_merged():
    """finding_route routes by kind (a block kind PENDING, a pure kind
    IN_RUN), so the kind is part of the merge key."""
    import claim_card as cc
    block_kind = {**_pure_claim(), "kind": "direction_forecast"}
    assert not cc.check_claim(block_kind).errors
    assert ec.finding_route({"claim": block_kind})[0] != ec.finding_route(
        {"claim": _pure_claim()})[0]
    assert rf.side_finding_merges(_readings({
        "trade_efficiency": [_side("trade_efficiency", claim=block_kind)],
        "forecast_power": [_side("forecast_power")]})) == []
    assert len(rf.side_finding_merges(_readings({
        "trade_efficiency": [_side("trade_efficiency", claim=copy.deepcopy(block_kind))],
        "forecast_power": [_side("forecast_power", claim=block_kind)]}))) == 1
