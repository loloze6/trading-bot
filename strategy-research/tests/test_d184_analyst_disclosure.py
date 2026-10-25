"""D-184 (direction 2026-10-24, PR-1; operator rule 2026-10-22, disclose, don't refuse).

Supersedes the refusal parts of D-178: (1) a floor-clearing result the answer leaves out is written
into the analyst record by code (`unreported_results`, each entry tagged `unreported_by_model`),
the answer is refused only when it cites no query; (2) `mechanism_query` may be any ok query of the
session; (3) after two refused attempts the record carries a top-level `status: refused`.

Real fixtures: the run_099 query logs (tests/fixtures/d178). No model call, no backtest.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import analyst_session as asm  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

from test_d178_analyst_method import (  # noqa: E402,F401
    _check, _claim_doc, _claim_entries, _haiku_nc, _log, _nc, _obs)
from test_e075_pr5_analyst import RUN_ID, _good_claim, _install, run  # noqa: E402,F401
from d178_legacy_fixture import d178_checks_off  # noqa: E402,F401


@pytest.fixture()
def _worker_flags(monkeypatch, d178_checks_off):
    """The worker tests run with the D-178 reader checks off (their stubbed answers predate
    them), exactly as tests/test_e075_pr5_analyst.py does."""
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_score_provenance_enabled", lambda *a: False)
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# (a) an unreported floor-clearing result is written into the record
# ---------------------------------------------------------------------------

def test_an_unreported_floor_clearing_result_is_written_into_the_record_with_six_fields_and_the_tag():
    e = _log("sonnet", "forecast")
    reading, rec, errors = _check(
        _nc(e, [_obs(e, "q12")], best_rejected={"statement": "A candidate.", "killed_by": "q9"}), e)
    assert errors == [] and reading is not None          # accepted
    assert asm.UNREPORTED_KEY == "unreported_results" and asm.UNREPORTED_TAG == "unreported_by_model"
    entries = {u["query"]: u for u in rec["unreported_results"]}
    assert "q7" in entries and "q12" not in entries
    u = entries["q7"]
    assert list(u) == ["query", "selector", "outcome", "statistic", "effect", "windows",
                       "unreported_by_model"]
    assert u["unreported_by_model"] is True
    test = e["q7"]["result"]["test"]
    assert (u["selector"], u["outcome"], u["statistic"]) == (
        test["selector"], test["outcome"], test["statistic"])
    for h, row in e["q7"]["result"]["horizons"].items():
        assert u["effect"][h] == row["effect"]
        assert u["windows"][h] == {k: row[k] for k in (
            "n_windows_with_events", "windows_claimed_sign", "windows_with_value")}
    # every entry of the list is a floor-clearing ok conditional_effect call, none twice
    ids = [x["query"] for x in rec["unreported_results"]]
    assert len(ids) == len(set(ids))
    assert all(asm.met_own_floor(e[q]) is True for q in ids)
    # the reading (what decide-next reads) is untouched by the disclosure
    assert "unreported_results" not in yaml.safe_dump(reading)


def test_the_disclosure_is_written_for_a_claim_answer_too():
    e = _log("sonnet", "forecast")
    reading, rec, errors = _check(_claim_doc(), e, claim=True)
    assert errors == [], errors
    assert "q7" in [u["query"] for u in rec["unreported_results"]]
    assert all(u["unreported_by_model"] is True for u in rec["unreported_results"])


def test_a_query_is_never_both_accounted_and_unreported():
    e = _log("sonnet", "forecast")
    _r, rec, errors = _check(
        _nc(e, [_obs(e, "q5", mechanism_query="q12"), _obs(e, "q15", mechanism_query="q12",
                                     floor_lowered_reason="r")]), e)
    assert errors == []
    listed = {u["query"] for u in rec["unreported_results"]}
    accounted = {"q9", "q5", "q15"}
    assert not (listed & accounted)
    # q11/q13 are the same finding as the accounted q15, q14 is not the same as q5 (direction)
    assert not ({"q11", "q13"} & listed) and "q14" in listed


# ---------------------------------------------------------------------------
# (b) an answer that cites no query is refused
# ---------------------------------------------------------------------------

def test_an_answer_that_cites_no_query_is_refused():
    e = _log("sonnet", "forecast")
    assert asm.completeness_errors(e, set())
    assert asm.completeness_errors(e, {None, "q99"})     # an id that is no ok query cites nothing
    failed = copy.deepcopy(e)
    failed["q40"] = {"id": "q40", "function": "describe", "status": "error", "result": None}
    assert asm.completeness_errors(failed, {"q40"})
    assert asm.completeness_errors(e, {"q1"}) == []      # any ok query of the session is a citation
    # the whole answer: a no_claim whose best_rejected cites a query that does not exist
    doc = _nc(e, [], best_rejected={"statement": "A candidate.", "killed_by": "q99"})
    del doc["no_claim"]["observations"]
    _r, _rec, errors = _check(doc, e)
    assert any("cites no query" in x for x in errors), errors


# ---------------------------------------------------------------------------
# (c) mechanism_query: any ok query of the session
# ---------------------------------------------------------------------------

def test_a_mechanism_query_earlier_than_the_observations_query_is_accepted():
    e = _log("sonnet", "forecast")
    # q5 is earlier than q12; q12 is the test itself; q15 is later: all ok queries of the session
    for mq in ("q5", "q12", "q15", "q1"):
        errs = asm.observation_errors([_obs(e, "q12", mechanism_query=mq)], e)
        assert not any("mechanism_query" in x for x in errs), (mq, errs)
    # whole answer, on the Haiku trade log: the test itself (q9) and an earlier query (q3)
    h = _log("haiku", "trade_efficiency")
    for mq in ("q9", "q3"):
        _r, rec, errors = _check(_haiku_nc(h, mechanism_query=mq), h, lens="trade_efficiency")
        assert errors == [], (mq, errors)
        assert rec["no_claim"]["observations"][0]["mechanism_query"] == mq


def test_an_unknown_or_failed_mechanism_query_is_still_refused_without_the_later_wording():
    e = _log("sonnet", "forecast")
    e["q40"] = {"id": "q40", "function": "describe", "status": "error", "result": None}
    for mq in ("q99", "q40", 12, "12", ""):
        errs = asm.observation_errors([_obs(e, "q12", mechanism_query=mq)], e)
        msgs = [x for x in errs if "mechanism_query" in x]
        assert msgs, (mq, errs)
        assert not any("LATER" in x or "later" in x for x in msgs), msgs


def test_a_missing_mechanism_query_and_stopped_by_is_still_refused():
    e = _log("sonnet", "forecast")
    o = _obs(e, "q12")
    del o["mechanism_query"]
    errs = asm.observation_errors([o], e)
    (msg,) = [x for x in errs if "needs `mechanism_query" in x]
    assert "after q12" not in msg and "LATER" not in msg
    # stopped_by instead: accepted; floors_met false: needs neither
    assert not any("mechanism_query" in x
                   for x in asm.observation_errors([dict(o, stopped_by="the tool limit")], e))
    assert not any("mechanism_query" in x
                   for x in asm.observation_errors([dict(o, floors_met=False)], e)
                   if "needs" in x)


# ---------------------------------------------------------------------------
# (d) a double refusal marks the record `status: refused`
# ---------------------------------------------------------------------------

def test_after_two_refused_attempts_the_record_carries_status_refused(
        run, monkeypatch, _worker_flags):
    async def script(call):
        return await _good_claim(call, cite_bad=True)    # refused on both attempts
    _install(monkeypatch, script)
    dest = rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    assert yaml.safe_load(dest.read_text(encoding="utf-8"))["skipped"]["rule"] \
        == "output_refused_after_retry"
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert [a["status"] for a in record["attempts"]] == ["refused", "refused"]
    assert record["status"] == "refused"
    # the attempts keep their own `status` keys: only the top level is new
    assert list(record).count("status") == 1


def test_an_accepted_record_has_no_top_level_status(run, monkeypatch, _worker_flags):
    _install(monkeypatch, _good_claim)
    rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert record["attempts"][-1]["status"] == "accepted" and "status" not in record
    # a refused first attempt followed by an accepted retry: still no top-level status
    n = {"calls": 0}

    async def script(call):
        n["calls"] += 1
        return await _good_claim(call, cite_bad=n["calls"] == 1)
    _install(monkeypatch, script)
    rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert [a["status"] for a in record["attempts"]] == ["refused", "accepted"]
    assert "status" not in record


def test_a_refused_attempts_disclosure_does_not_survive_into_the_final_record(
        run, monkeypatch, _worker_flags):
    """The record merges each attempt's `rec`; the disclosure of an earlier attempt must not
    stay beside a later attempt that has none."""
    calls = {"n": 0}
    disclosed = [{"query": "q1", asm.UNREPORTED_TAG: True}]

    def fake_check(text, **kw):
        calls["n"] += 1
        rec = {"lens": kw["lens"], "category": "trade_efficiency", "outcome": None}
        if calls["n"] == 1:
            rec[asm.UNREPORTED_KEY] = disclosed
        return None, rec, [f"refused {calls['n']}"]
    monkeypatch.setattr(asm, "check_answer", fake_check)

    async def script(call):
        return "no answer"
    _install(monkeypatch, script)
    rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    record = yaml.safe_load((run / asm.record_rel("trade_efficiency")).read_text(encoding="utf-8"))
    assert calls["n"] == 2 and record["status"] == "refused"
    assert asm.UNREPORTED_KEY not in record
