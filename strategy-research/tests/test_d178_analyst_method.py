"""D-178 / D-179 (operator item D, 2026-10-22): the analyst's method checks and texts, and its model.

Real fixtures: the query logs of run_099's analyst sessions (tests/fixtures/d178/<model>/<lens>.yaml,
copied from the lead's prepared files; Haiku 5.5 and Sonnet 5.5, forecast and trade_efficiency
lenses). No model call, no backtest.

  D1 floor_lowered (disclosure), D2 mechanism_query, D3 completeness, D4 tags (angle),
  D5 the three texts and the next_steps ledger, D6 the model value.
"""
from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import analyst_session as asm  # noqa: E402
import campaign_memory as cm  # noqa: E402
import claim_card as cc  # noqa: E402
import reader_proposals as rp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

import test_e075_pr4_queries as q4  # noqa: E402
from test_e075_pr5_analyst import _good_claim, _install, run, RUN_ID  # noqa: E402,F401
from d178_legacy_fixture import d178_checks_off  # noqa: E402,F401

FIX = SR_ROOT / "tests" / "fixtures" / "d178"


@pytest.fixture(autouse=True)
def _flags_d178(monkeypatch):
    """Analyst on (with folds), score provenance off; nothing reads the real config (the same
    four lines as test_e075_pr5_analyst._flags, without switching the D-178 checks off)."""
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_score_provenance_enabled", lambda *a: False)
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _log(model, lens):
    doc = yaml.safe_load((FIX / model / f"{lens}.yaml").read_text(encoding="utf-8"))
    return {q["id"]: q for q in doc["queries"]}


def _cite(entries, qid, path):
    node = entries[qid]["result"]
    for p in path.split("."):
        node = node[p]
    return f"{qid}:{path}={node}"


def _answer(doc):
    return "```yaml\n" + yaml.safe_dump(doc, sort_keys=False) + "```"


def _base_config():
    """The run_099 base strategy config (anchor_position's transforms[2] is a vol_target step)."""
    return json.loads((FIX / "run_099_strategy_config.json").read_text(encoding="utf-8"))


def _check(doc, entries, lens="forecast", claim=False, base_config=None):
    return asm.check_answer(
        _answer(doc), lens=lens, run_id="run_099", entries=entries,
        claim_check=(lambda c: cc.check_claim(c, folds=True, trade_tests=True)) if claim else None,
        holdout_start=q4.HOLDOUT, fold="A", model_id="m", base_config=base_config)


LEDGER = {"opposite_direction": "q8", "another_horizon": "not run: the floor",
          "all_bars_version": "q9", "mechanism": "not run: the tool limit"}


# ---------------------------------------------------------------------------
# the pieces on the real logs
# ---------------------------------------------------------------------------

def test_floor_lowered_info_on_the_sonnet_forecast_log():
    e = _log("sonnet", "forecast")
    # q5 (100 events, 4 windows) -> q7 (100, 3): the same selector and outcome, a lower floor
    assert asm.floor_lowered_info("q7", e) == {
        "from": {"min_events": 100, "min_windows": 4},
        "to": {"min_events": 100, "min_windows": 3}, "after": "q5"}
    # q10 (100, 4) -> q11 (50, 4)
    assert asm.floor_lowered_info("q11", e) == {
        "from": {"min_events": 100, "min_windows": 4},
        "to": {"min_events": 50, "min_windows": 4}, "after": "q10"}
    # the first run of a selector, and a call that is not a conditional_effect: nothing
    assert asm.floor_lowered_info("q5", e) is None and asm.floor_lowered_info("q8", e) is None
    assert asm.floor_lowered_info("q12", e) is None      # another selector (top, not bottom)


def test_the_text_of_a_lowered_floor():
    e = _log("sonnet", "forecast")
    assert rp.floor_lowered_text(asm.floor_lowered_info("q11", e)) == "on a lowered floor (100 to 50)"
    assert rp.floor_lowered_text(asm.floor_lowered_info("q7", e)) == "on a lowered floor (4 to 3)"
    both = {"from": {"min_events": 100, "min_windows": 4}, "to": {"min_events": 50, "min_windows": 3}}
    assert rp.floor_lowered_text(both) == "on a lowered floor (100/4 to 50/3)"


def test_met_own_floor_is_judged_at_any_horizon_on_the_units_the_result_reports():
    e = _log("sonnet", "forecast")
    assert asm.met_own_floor(e["q7"]) is True            # 396 and 378 events, 5 windows, floor 100/3
    assert asm.met_own_floor(e["q10"]) is False          # below its 100-event floor
    assert asm.met_own_floor(e["q8"]) is None            # not a conditional_effect
    cut = copy.deepcopy(e["q7"])
    cut["result"]["horizons"]["5"]["n_events"] = 10      # one horizon below, one above: still met
    assert asm.met_own_floor(cut) is True
    cut["result"]["horizons"]["10"]["n_events"] = 10
    assert asm.met_own_floor(cut) is False


# ---------------------------------------------------------------------------
# D1: floor_lowered (observation path, the real Sonnet forecast log)
# ---------------------------------------------------------------------------

def _obs(entries, qid, **over):
    o = {"statement": "Bars with the claimed condition were followed by lower returns.",
         "test": qid, "evidence": [_cite(entries, qid, "horizons.5.effect")],
         "floors_met": True, "mechanism_query": "q12"}
    o.update(over)
    return o


def _nc(entries, observations, **over):
    nc = {"reason": "Nothing more to test.",
          "best_rejected": {"statement": "A candidate.", "killed_by": "q9"},
          "observations": observations, "next_steps": dict(LEDGER)}
    nc.update(over)
    return {"outcome": "no_claim", "no_claim": nc, "evidence": [_cite(entries, "q9", "horizons.5.n_events")]}


@pytest.mark.parametrize("qid,after,floors,text", [
    ("q7", "q5", ({"min_events": 100, "min_windows": 4}, {"min_events": 100, "min_windows": 3}),
     "on a lowered floor (4 to 3)"),
    ("q11", "q10", ({"min_events": 100, "min_windows": 4}, {"min_events": 50, "min_windows": 4}),
     "on a lowered floor (100 to 50)"),
])
def test_an_observation_on_a_lowered_floor_needs_a_reason_and_records_the_disclosure(
        qid, after, floors, text):
    e = _log("sonnet", "forecast")
    # a missing reason is the one refusal
    _r, _rec, errors = _check(_nc(e, [_obs(e, qid)]), e)
    assert any(f"floor_lowered_reason is required" in x and after in x for x in errors), errors
    # a blank one too
    _r, _rec, errors = _check(_nc(e, [_obs(e, qid, floor_lowered_reason="  ")]), e)
    assert any("floor_lowered_reason is required" in x for x in errors)
    # with the reason the reader writes floor_lowered from the log
    _r, rec, errors = _check(_nc(e, [_obs(e, qid, floor_lowered_reason="Fewer bars qualify.")]), e)
    assert not any("floor_lowered_reason" in x for x in errors), errors
    (o,) = rec["no_claim"]["observations"]
    assert o["floor_lowered"] == {"from": floors[0], "to": floors[1], "after": after,
                                  "reason": "Fewer bars qualify."}
    assert "floor_lowered_reason" not in o
    assert rp.floor_lowered_text(o["floor_lowered"]) == text


def test_an_observation_whose_floor_was_not_lowered_carries_no_disclosure():
    e = _log("sonnet", "forecast")
    _r, rec, errors = _check(_nc(e, [_obs(e, "q12")]), e)
    (o,) = rec["no_claim"]["observations"]
    assert "floor_lowered" not in o and not any("floor_lowered" in x for x in errors)


# ---------------------------------------------------------------------------
# D3: completeness
# ---------------------------------------------------------------------------

def test_a_result_that_met_its_floor_and_is_written_nowhere_is_refused_naming_it():
    e = _log("sonnet", "forecast")
    # q7 (the forecast > 0 bars, by window) met its floor; nothing in this answer mentions it
    _r, _rec, errors = _check(
        _nc(e, [_obs(e, "q12")], best_rejected={"statement": "A candidate.", "killed_by": "q9"}), e)
    (msg,) = [x for x in errors if "appear nowhere in your answer" in x]
    assert "q7" in msg.split("cleared")[0]
    assert "q12" not in msg.split("cleared")[0]          # written, so not named


def test_completeness_counts_why_query_observations_killed_by_and_variants_of_a_written_test():
    e = _log("sonnet", "forecast")
    met = [q for q, x in e.items() if x["function"] == "conditional_effect"
           and asm.met_own_floor(x) is True]
    assert {"q5", "q6", "q7", "q11", "q12", "q13", "q14", "q15"} == set(met)
    assert asm.completeness_errors(e, set(met)) == []
    # q11/q13/q15 are one test (same selector, outcome, statistic, direction): writing q15
    # covers them; q7 and q14 are one test (direction less): writing q7 covers q14
    assert asm.completeness_errors(e, {"q15", "q12", "q5", "q6", "q7"}) == []
    (msg,) = asm.completeness_errors(e, {"q15", "q12", "q6"})
    assert all(q in msg.split("cleared")[0] for q in ("q5", "q7", "q14"))
    assert "q15" not in msg.split("cleared")[0] and "q13" not in msg.split("cleared")[0]
    # an unknown or non-string id in `accounted` is ignored, never raises
    assert asm.completeness_errors(e, {None, "q99", "q15"}) != []


def test_the_same_selector_in_the_opposite_direction_is_not_accounted_for():
    """Ruling 4: "accounted for" is selector + outcome + statistic + direction. q5 (forecast > 0,
    mean_diff, greater) and q7/q14 (the same, less) are two findings."""
    e = _log("sonnet", "forecast")
    (msg,) = asm.completeness_errors(e, {"q15", "q12", "q6", "q5"})
    named = msg.split("cleared")[0]
    assert "q7" in named and "q14" in named and "q5" not in named
    # the same direction at another floor/horizon is still the same finding
    assert asm.completeness_errors(e, {"q15", "q12", "q6", "q5", "q14"}) == []
    # through the whole answer: an observation on q5 does not cover q7
    _r, _rec, errors = _check(_nc(e, [_obs(e, "q5", mechanism_query="q12"),
                                      _obs(e, "q15", mechanism_query="q12")]), e)
    (msg,) = [x for x in errors if "appear nowhere in your answer" in x]
    assert "q7" in msg.split("cleared")[0]


# ---------------------------------------------------------------------------
# D2: mechanism_query (the real Haiku trade log: q9 is its last query)
# ---------------------------------------------------------------------------

def _haiku_nc(entries, **obs_over):
    obs = {"statement": "The forecast's rank correlation with forward returns is negative.",
           "test": "q9", "evidence": [_cite(entries, "q9", "horizons.5.effect"),
                                      _cite(entries, "q9", "horizons.5.n_events")],
           "floors_met": True}
    obs.update(obs_over)
    return {"outcome": "no_claim",
            "no_claim": {"reason": "No change follows yet.",
                         "best_rejected": {"statement": "A top-20% threshold.", "killed_by": "q7"},
                         # q6 (all bars, rank_ic, the OPPOSITE direction of q9) cleared its floors
                         # too, and is its own finding (ruling 4)
                         "observations": [obs, {
                             "statement": "The forecast's rank correlation with forward returns is positive.",
                             "test": "q6", "evidence": [_cite(entries, "q6", "horizons.5.effect")],
                             "floors_met": True, "stopped_by": "no query separates it"}],
                         "next_steps": {"opposite_direction": "q6", "another_horizon": "q9",
                                        "all_bars_version": "q9",
                                        "mechanism": "not run: the tool limit"}},
            "evidence": [_cite(entries, "q7", "horizons.20.n_events")]}


def test_the_haiku_trade_observation_with_no_later_query_is_refused():
    e = _log("haiku", "trade_efficiency")
    assert max(int(q[1:]) for q in e) == 9               # q9 is the last query of the session
    _r, _rec, errors = _check(_haiku_nc(e), e, lens="trade_efficiency")
    assert any("mechanism_query" in x and "q9" in x for x in errors), errors
    # a mechanism_query that is the test itself, or not a query of the session, is refused too
    for bad in ("q9", "q3", "q40", 9):
        _r, _rec, errors = _check(_haiku_nc(e, mechanism_query=bad), e, lens="trade_efficiency")
        assert any("mechanism_query" in x and "LATER" in x for x in errors), (bad, errors)


def test_a_later_query_or_a_named_tool_limit_satisfies_the_mechanism_rule():
    e = _log("haiku", "trade_efficiency")
    e["q10"] = {"id": "q10", "function": "describe", "status": "ok", "params": {},
                "result": {"column": "forecast"}}
    _r, rec, errors = _check(_haiku_nc(e, mechanism_query="q10"), e, lens="trade_efficiency")
    assert errors == [], errors
    assert rec["no_claim"]["observations"][0]["mechanism_query"] == "q10"
    e2 = _log("haiku", "trade_efficiency")
    _r, rec, errors = _check(_haiku_nc(e2, stopped_by="no tool measures the order book"), e2,
                             lens="trade_efficiency")
    assert errors == [], errors
    assert rec["no_claim"]["observations"][0]["stopped_by"] == "no tool measures the order book"
    # an observation that did not clear its floors needs neither
    _r, _rec, errors = _check(_haiku_nc(e2, floors_met=False), e2, lens="trade_efficiency")
    assert not any("mechanism_query" in x for x in errors)
    # a written mechanism_query is checked even when stopped_by is also written
    _r, _rec, errors = _check(_haiku_nc(e2, mechanism_query="q9", stopped_by="x"), e2,
                              lens="trade_efficiency")
    assert any("mechanism_query" in x for x in errors)


# ---------------------------------------------------------------------------
# D5: the next-steps ledger
# ---------------------------------------------------------------------------

def _ledger_errors(ns):
    e = _log("haiku", "trade_efficiency")
    doc = _haiku_nc(e, stopped_by="the tool limit")
    if ns is None:
        del doc["no_claim"]["next_steps"]
    else:
        doc["no_claim"]["next_steps"] = ns
    return [x for x in _check(doc, e, lens="trade_efficiency")[2] if "next_steps" in x]


GOOD = {"opposite_direction": "q6", "another_horizon": "q7", "all_bars_version": "q8",
        "mechanism": "not run: the tool limit"}


def test_the_ledger_is_required_with_four_lines_and_known_query_ids_only():
    assert _ledger_errors(GOOD) == []
    assert _ledger_errors(None)                                          # missing
    assert _ledger_errors({k: v for k, v in list(GOOD.items())[:3]})     # three lines
    assert _ledger_errors({**GOOD, "extra": "q1"})                       # five lines
    assert _ledger_errors({**GOOD, "mechanism": "q99"})                  # an id of no query here
    assert _ledger_errors({**GOOD, "mechanism": "the tool limit"})       # neither id nor "not run:"
    assert _ledger_errors({**GOOD, "mechanism": "not run:"})             # no reason after it
    assert _ledger_errors({**GOOD, "mechanism": None})
    assert _ledger_errors("q1")
    # the ledger judges nothing else: any known id, even a describe call, even the same twice
    assert _ledger_errors({k: "q1" for k in GOOD}) == []


def test_the_ledger_is_required_on_a_claim_too_and_kept_out_of_the_claim_card():
    e = _claim_entries()
    doc = _claim_doc()
    del doc["claim"]["next_steps"]
    assert any("claim.next_steps is required" in x for x in _check(doc, e, claim=True)[2])
    reading, rec, errors = _check(_claim_doc(), e, claim=True)
    assert errors == [], errors
    assert "next_steps" not in reading["side_findings"][0]["claim"]
    assert "floor_lowered_reasons" not in reading["side_findings"][0]["claim"]
    assert rec["next_steps"] == _claim_doc()["claim"]["next_steps"]


# ---------------------------------------------------------------------------
# D1 + D4 on the claim path (the Sonnet forecast claim, its own wording made neutral)
# ---------------------------------------------------------------------------

def _claim_entries():
    """The Sonnet forecast log without the unwritten results (q5, q6, q7, q9, q14), so a claim
    on q11/q13/q15 with why_query q12 leaves nothing unaccounted."""
    e = _log("sonnet", "forecast")
    for q in ("q5", "q6", "q7", "q9", "q14"):
        del e[q]
    return e


def _claim_doc():
    rec = yaml.safe_load((FIX / "sonnet" / "record_forecast.yaml").read_text(encoding="utf-8"))
    text = rec["attempts"][-1]["answer"]
    doc = yaml.safe_load(re.search(r"```yaml\n(.*?)```", text, re.S).group(1))
    c = doc["claim"]
    c["statement"] = ("On BTCUSD daily bars, when the past 20 days' volatility is in the bottom "
                      "30% of the trailing 60 bars, returns over the next 5 and 10 days are "
                      "higher than on other days.")
    c["rationale"] = ("A compressed-volatility regime tends to be a rising or quiet one. The "
                      "complement baseline cancels each window's drift.")
    c["next_steps"] = {"opposite_direction": "q12", "another_horizon": "not run: the floor",
                       "all_bars_version": "q8", "mechanism": "not run: the tool limit"}
    c["floor_lowered_reasons"] = {"low_vol_then_higher_returns": "Too few low-volatility bars."}
    doc["vehicle"] = [{"component_id": "anchor_position", "field": "transforms[2].params.window",
                       "before": 60, "after": 20}]
    return doc


def test_the_sonnet_claim_is_accepted_with_the_disclosure_written_from_the_log():
    e = _claim_entries()
    reading, rec, errors = _check(_claim_doc(), e, claim=True)
    assert errors == [], errors
    (side,) = reading["side_findings"]
    assert side["floor_lowered"] == {
        "test": "low_vol_then_higher_returns", "from": {"min_events": 100, "min_windows": 4},
        "to": {"min_events": 50, "min_windows": 4}, "after": "q10",
        "reason": "Too few low-volatility bars."}
    assert rec["floor_lowered"] == side["floor_lowered"]
    assert rp.floor_lowered_text(side["floor_lowered"]) == "on a lowered floor (100 to 50)"
    rp.check_reading(reading, "forecast_power", "reading", analyst=True, from_model=True,
                     envelope=True)


def test_a_claim_test_on_a_lowered_floor_without_a_reason_is_refused():
    e = _claim_entries()
    doc = _claim_doc()
    del doc["claim"]["floor_lowered_reasons"]
    errors = _check(doc, e, claim=True)[2]
    assert any("floor_lowered_reasons.low_vol_then_higher_returns is required" in x and "q10" in x
               for x in errors), errors


def test_the_unwritten_results_of_the_real_sonnet_log_refuse_the_claim_naming_q7():
    e = _log("sonnet", "forecast")
    errors = _check(_claim_doc(), e, claim=True)[2]
    (msg,) = [x for x in errors if "appear nowhere in your answer" in x]
    assert "q7" in msg.split("cleared")[0]


# ---------------------------------------------------------------------------
# D4: tags
# ---------------------------------------------------------------------------

_FORECAST_VEHICLE = [{"component_id": "anchor_position", "field": "params.period",
                      "before": 250, "after": 200}]
_SIZING_VEHICLE = [{"component_id": "anchor_position", "field": "transforms[2].params.window",
                    "before": 60, "after": 20}]


def test_a_selector_with_no_forecast_field_is_tagged_regime_by_code():
    e = _claim_entries()
    doc = _claim_doc()
    doc["vehicle"] = copy.deepcopy(_FORECAST_VEHICLE)
    reading, rec, errors = _check(doc, e, claim=True, base_config=_base_config())
    assert errors == [] and reading["side_findings"][0]["angle"] == "regime" and rec["angle"] == "regime"
    # observations: a trailing_vol selector -> regime; a forecast selector -> no tag
    ee = _log("sonnet", "forecast")
    _r, rec, _err = _check(_nc(ee, [_obs(ee, "q11", floor_lowered_reason="r"),
                                    _obs(ee, "q7", floor_lowered_reason="r")]), ee)
    tags = [o.get("angle") for o in rec["no_claim"]["observations"]]
    assert tags == ["regime", None]
    # by the letter of the ruling ("no forecast field in the selector"): a trade selector that
    # names none, and kind all, are regime selectors too
    trade = {"kind": "trade", "where": [{"field": "side", "op": "==", "value": "long"}]}
    assert asm.angle_of([trade]) == "regime" and asm.angle_of([{"kind": "all"}]) == "regime"
    assert asm.angle_of([{"kind": "event", "field": "past_return", "bars": 1, "op": ">=", "value": 0.01}]) == "regime"
    assert asm.angle_of([{"kind": "trade", "where": [
        {"field": "entry_forecast", "op": "<=", "value": -10}]}]) is None
    assert asm.angle_of([{"kind": "all_of", "clauses": [
        {"kind": "event", "field": "forecast", "op": ">", "value": 0},
        {"kind": "event", "field": "trailing_vol", "bars": 20, "op": ">", "value": 0.02}]}]) is None
    assert asm.angle_of([]) is None


def test_the_sonnet_forecast_claim_is_a_sizing_finding_by_its_vehicle_path_and_is_refused():
    """The real claim: vehicle anchor_position transforms[2].params.window 60 -> 20, where
    transforms[2] is the vol_target step of run_099's base config."""
    cfg = _base_config()
    assert cfg["strategies"]["regimes"]["unknown"]["components"][0]["transforms"][2]["op"] == "vol_target"
    e = _claim_entries()
    reading, rec, errors = _check(_claim_doc(), e, claim=True, base_config=cfg)
    assert any("sizing finding" in x and "never a claim with a vehicle" in x for x in errors), errors
    assert reading["side_findings"][0]["angle"] == "sizing" and rec["angle"] == "sizing"
    # without the base config the path cannot be resolved: nothing is guessed from words
    assert _check(_claim_doc(), e, claim=True)[2] == []


def test_words_in_the_prose_never_tag_a_claim_as_sizing():
    e = _claim_entries()
    doc = _claim_doc()
    doc["vehicle"] = copy.deepcopy(_FORECAST_VEHICLE)
    doc["claim"]["rationale"] = ("The base strategy's vol_target sizes inversely to volatility; "
                                 "the position is sized by it. Position sizing is not changed here.")
    doc["claim"]["statement"] += " A sized position, vol_target, sizing."
    reading, rec, errors = _check(doc, e, claim=True, base_config=_base_config())
    assert not any("sizing finding" in x for x in errors), errors
    assert reading["side_findings"][0].get("angle") != "sizing" and rec.get("angle") != "sizing"


def test_the_vehicle_paths_that_make_a_finding_a_sizing_finding():
    cfg = _base_config()
    assert asm.vehicle_is_sizing(_SIZING_VEHICLE, cfg) is True
    assert asm.vehicle_is_sizing([{"component_id": "anchor_position",
                                   "field": "transforms[2]", "before": {}, "after": {}}], cfg) is True
    assert asm.vehicle_is_sizing(_FORECAST_VEHICLE, cfg) is False
    assert asm.vehicle_is_sizing([{"component_id": "anchor_position", "field": "transforms[0].params.window",
                                   "before": 250, "after": 120}], cfg) is False           # standardise
    assert asm.vehicle_is_sizing(_SIZING_VEHICLE, None) is False
    # the sizing block
    assert asm.vehicle_is_sizing([{"component_id": "strategies.sizing", "field": "params.x",
                                   "before": 1, "after": 2}], None) is True
    assert asm.vehicle_is_sizing([{"component_id": "anything", "field": "strategies.sizing.target",
                                   "before": 1, "after": 2}], None) is True
    # a config vehicle: judged by what differs from the base at the sizing block / vol_target steps
    same = {"kind": "config", "config": copy.deepcopy(cfg)}
    assert asm.vehicle_is_sizing(same, cfg) is False
    cand = copy.deepcopy(cfg)
    cand["strategies"]["regimes"]["unknown"]["components"][0]["transforms"][2]["params"]["window"] = 20
    assert asm.vehicle_is_sizing({"kind": "config", "config": cand}, cfg) is True
    cand = copy.deepcopy(cfg)
    cand["strategies"]["sizing"] = {"kind": "fixed"}
    assert asm.vehicle_is_sizing({"kind": "config", "config": cand}, cfg) is True
    cand = copy.deepcopy(cfg)
    cand["strategies"]["regimes"]["unknown"]["components"][0]["params"]["period"] = 200
    assert asm.vehicle_is_sizing({"kind": "config", "config": cand}, cfg) is False
    # sizing wins over regime
    assert asm.angle_of([{"kind": "quantile", "field": "trailing_vol", "bars": 20, "side": "bottom",
                          "q": 0.3, "lookback": 60}], _SIZING_VEHICLE, cfg) == "sizing"


def test_a_sizing_finding_is_recorded_as_an_observation_tagged_sizing():
    cfg = _base_config()
    e = _log("sonnet", "forecast")
    obs = _obs(e, "q11", floor_lowered_reason="r", vehicle=copy.deepcopy(_SIZING_VEHICLE),
               statement="A shorter volatility window for the position size.")
    _r, rec, errors = _check(_nc(e, [obs, _obs(e, "q7", floor_lowered_reason="r")]), e, base_config=cfg)
    assert not any("observations[0]" in x for x in errors), errors
    assert rec["no_claim"]["observations"][0]["angle"] == "sizing"
    assert rec["no_claim"]["observations"][0]["vehicle"] == _SIZING_VEHICLE
    # a malformed observation vehicle is refused
    bad = _obs(e, "q11", floor_lowered_reason="r", vehicle=[{"component_id": "x"}])
    errors = _check(_nc(e, [bad]), e, base_config=cfg)[2]
    assert any("observations[0].vehicle" in x for x in errors), errors


# ---------------------------------------------------------------------------
# ruling 2: claims carry observations; D3 applies to claim and no_claim sessions
# ---------------------------------------------------------------------------

def _claim_with_observations(e):
    """A claim on q11/q13/q15 (why_query q12) over the FULL Sonnet log: q5, q6 and q7 cleared
    their floors too and are recorded as the claim's observations."""
    doc = _claim_doc()
    doc["vehicle"] = copy.deepcopy(_FORECAST_VEHICLE)
    doc["claim"]["observations"] = [
        _obs(e, "q5", floors_met=asm.floors_met_in_log(e["q5"]), mechanism_query="q12"),
        _obs(e, "q6", floors_met=asm.floors_met_in_log(e["q6"]), mechanism_query="q12"),
        _obs(e, "q7", floors_met=asm.floors_met_in_log(e["q7"]), mechanism_query="q12",
             floor_lowered_reason="Too few bars."),
    ]
    return doc


def test_a_claim_carries_observations_that_complete_the_account():
    e = _log("sonnet", "forecast")
    doc = _claim_with_observations(e)
    cfg = _base_config()
    # without the observations the claim is refused naming what is unaccounted
    bare = copy.deepcopy(doc)
    del bare["claim"]["observations"]
    errs = _check(bare, e, claim=True, base_config=cfg)[2]
    (msg,) = [x for x in errs if "appear nowhere in your answer" in x]
    assert all(q in msg.split("cleared")[0] for q in ("q5", "q6", "q7"))
    # with them: accepted, recorded in the record (masked, spec, floor_lowered), stripped
    # from the claim the claim card and the reading see
    reading, rec, errors = _check(doc, e, claim=True, base_config=cfg)
    assert errors == [], errors
    assert "observations" not in reading["side_findings"][0]["claim"]
    obs = rec["observations"]
    assert [o["test"] for o in obs] == ["q5", "q6", "q7"]
    assert all("spec" in o and "floor_lowered_reason" not in o for o in obs)
    assert obs[2]["floor_lowered"]["after"] == "q5" and obs[2]["floor_lowered"]["reason"] == "Too few bars."
    rp.check_reading(reading, "forecast_power", "reading", analyst=True, from_model=True,
                     envelope=True)


def test_a_claims_observations_follow_the_no_claim_rules():
    e = _log("sonnet", "forecast")
    cfg = _base_config()
    doc = _claim_with_observations(e)
    # the maximum is the same (3)
    over = copy.deepcopy(doc)
    over["claim"]["observations"].append(
        _obs(e, "q9", floors_met=asm.floors_met_in_log(e["q9"]), mechanism_query="q12"))
    errs = _check(over, e, claim=True, base_config=cfg)[2]
    assert any(x.startswith("claim.observations has 4 entries") for x in errs), errs
    # the same shape check, naming the claim
    bad = copy.deepcopy(doc)
    bad["claim"]["observations"][0]["surprise"] = 1
    errs = _check(bad, e, claim=True, base_config=cfg)[2]
    assert any(x.startswith("claim.observations[0] must have exactly the keys") for x in errs), errs
    # mechanism and floor-lowered rules apply
    bad = copy.deepcopy(doc)
    del bad["claim"]["observations"][0]["mechanism_query"]
    del bad["claim"]["observations"][2]["floor_lowered_reason"]
    errs = _check(bad, e, claim=True, base_config=cfg)[2]
    assert any("claim.observations[0]: q5 cleared its floors" in x for x in errs), errs
    assert any("claim.observations[2].floor_lowered_reason is required" in x for x in errs), errs
    # a non-list is refused
    bad = copy.deepcopy(doc)
    bad["claim"]["observations"] = "none"
    assert any("claim.observations must be a list" in x
               for x in _check(bad, e, claim=True, base_config=cfg)[2])


def test_campaign_memory_reads_a_claim_sessions_observations(tmp_path):
    e = _log("sonnet", "forecast")
    _r, rec, errors = _check(_claim_with_observations(e), e, claim=True, base_config=_base_config())
    assert errors == []
    rec["attempts"] = [{"status": "accepted", "outcome": "claim", "errors": []}]
    run_dir = tmp_path / "run_099"
    (run_dir / "artifacts" / "analyst").mkdir(parents=True)
    (run_dir / asm.record_rel("forecast")).write_text(yaml.safe_dump(rec), encoding="utf-8")
    rows = cm.analyst_observations(run_dir, "run_099")
    assert [r["test"] for r in rows] == ["q5", "q6", "q7"]


def test_the_mechanism_check_is_presence_only():
    """Ruling 3: any later query of the session satisfies mechanism_query; nothing judges
    whether it tests the mechanism."""
    e = _log("sonnet", "forecast")
    for later in ("q9", "q12", "q15"):
        errs = asm.observation_errors([_obs(e, "q7", mechanism_query=later,
                                            floor_lowered_reason="r")], e)
        assert not any("mechanism_query" in x for x in errs), (later, errs)


def test_decide_next_appends_the_floor_note_to_existing_notes():
    import decide_next as dn
    cand = {"notes": ["an earlier note"]}
    dn._append_notes(cand, "on a lowered floor (100 to 50)")
    assert cand["notes"] == ["an earlier note", "on a lowered floor (100 to 50)"]
    cand = {}
    dn._append_notes(cand, "on a lowered floor (100 to 50)")
    assert cand["notes"] == ["on a lowered floor (100 to 50)"]


# ---------------------------------------------------------------------------
# the tags in the reading, decide-next, the memory
# ---------------------------------------------------------------------------

def _reading():
    reading, _rec, errors = _check(_claim_doc(), _claim_entries(), claim=True)
    assert errors == []
    return reading


def test_check_reading_accepts_the_tags_for_the_analyst_only_and_checks_their_shape():
    reading = _reading()
    rp.check_reading(reading, "forecast_power", "r", analyst=True, from_model=True, envelope=True)
    with pytest.raises(rp.ProposalError, match="side finding is exactly"):
        rp.check_reading(reading, "forecast_power", "r", from_model=True, envelope=True)
    bad = copy.deepcopy(reading)
    bad["side_findings"][0]["angle"] = "momentum"
    with pytest.raises(rp.ProposalError, match="angle"):
        rp.check_reading(bad, "forecast_power", "r", analyst=True, from_model=True, envelope=True)
    bad = copy.deepcopy(reading)
    del bad["side_findings"][0]["floor_lowered"]["reason"]
    with pytest.raises(rp.ProposalError, match="floor_lowered"):
        rp.check_reading(bad, "forecast_power", "r", analyst=True, from_model=True, envelope=True)
    (item,) = rp.flatten_reading(reading)
    assert item["angle"] == "regime" and item["floor_lowered"]["after"] == "q10"


def test_decide_next_candidate_entry_shows_the_lowered_floor(run, monkeypatch, d178_checks_off):
    """The stubbed session of test_e075_pr5_analyst, with the disclosure code writes on the
    finding: the candidate entry carries it and its text."""
    _install(monkeypatch, _good_claim)
    dest = rpr.run_analyst_worker("trade_efficiency", RUN_ID, run)
    doc = yaml.safe_load(dest.read_text(encoding="utf-8"))
    doc["side_findings"][0]["floor_lowered"] = {
        "from": {"min_events": 100, "min_windows": 4}, "to": {"min_events": 50, "min_windows": 4},
        "after": "q1", "reason": "Too few bars."}
    doc["side_findings"][0]["angle"] = "regime"
    rp.check_reading(doc, "trade_efficiency", "file", strict_provenance=True, analyst=True)
    import test_e077_folds as tf
    (item,) = rp.flatten_reading(doc)
    inputs, _pid = tf._scenario(RUN_ID, "ROOT", {RUN_ID: tf.FOLD_A})
    inputs["runs"][RUN_ID]["proposals"] = [{"category": "trade_efficiency", "proposal": item}]
    inputs["trade_tests"] = True
    record = tf._decide(inputs, RUN_ID)
    cand = tf._cand(record, item["proposal_id"])
    assert cand["notes"] == ["on a lowered floor (100 to 50)"]
    assert cand["floor_lowered"]["after"] == "q1" and cand["angle"] == "regime"
    # a finding without the disclosure gets neither key
    del item["floor_lowered"], item["angle"]
    inputs["runs"][RUN_ID]["proposals"] = [{"category": "trade_efficiency", "proposal": item}]
    cand = tf._cand(tf._decide(inputs, RUN_ID), item["proposal_id"])
    assert "notes" not in cand and "floor_lowered" not in cand and "angle" not in cand


def test_campaign_memory_carries_the_observation_tags(tmp_path):
    e = _log("sonnet", "forecast")
    _r, rec, errors = _check(_nc(e, [_obs(e, "q11", floor_lowered_reason="Too few bars.")]), e)
    rec["attempts"] = [{"status": "accepted", "outcome": "no_claim", "errors": []}]
    rec["no_claim"]["observations"][0].pop("mechanism_query")
    run_dir = tmp_path / "run_099"
    (run_dir / "artifacts" / "analyst").mkdir(parents=True)
    (run_dir / asm.record_rel("forecast")).write_text(yaml.safe_dump(rec), encoding="utf-8")
    (row,) = cm.analyst_observations(run_dir, "run_099")
    assert row["angle"] == "regime" and row["floor_lowered"]["after"] == "q10"
    assert rp.floor_lowered_text(row["floor_lowered"]) == "on a lowered floor (100 to 50)"
    # a key outside the declared ones is still refused
    rec["no_claim"]["observations"][0]["surprise"] = 1
    (run_dir / asm.record_rel("forecast")).write_text(yaml.safe_dump(rec), encoding="utf-8")
    with pytest.raises(cm.CampaignMemoryError):
        cm.analyst_observations(run_dir, "run_099")


# ---------------------------------------------------------------------------
# D5 texts (the reader skill) and D6 the model
# ---------------------------------------------------------------------------

def _texts():
    """The three texts of the operator's direction, VERBATIM (tests/fixtures/d178/d5_texts_verbatim.md),
    whitespace-normalised."""
    raw = (FIX / "d5_texts_verbatim.md").read_text(encoding="utf-8")
    parts = re.split(r"^D5\([abc]\)[^\n]*\n", raw, flags=re.M)
    assert len(parts) == 4
    return [" ".join(p.split()) for p in parts[1:]]


def _skill(name="SKILL.md"):
    return " ".join((asm.SKILL_DIR / name).read_text(encoding="utf-8").split())


def test_the_three_texts_are_in_the_skill_verbatim_and_in_place():
    a, b, c = _texts()
    skill = _skill()
    for t in (a, b, c):
        assert t in skill
    # (a) replaced the selector-fit sentence; (b) sits right before the no-claim rule; (c) right
    # after the killed_by sentence
    assert "choose smaller ones" not in skill and "cannot clear the floors" not in skill
    assert skill.index(b) + len(b) + 1 == skill.index("A session may end in no claim only when")
    killed = "the only `killed_by` is a query of this session that measured a rival, named."
    assert skill.index(killed) + len(killed) + 1 == skill.index(c)
    assert skill.index(a) < skill.index("Write down the second query the mechanism predicts")
    for lens in ("forecast.md", "trade_efficiency.md"):
        assert "choose smaller ones" not in _skill(lens)


def test_the_skill_names_the_new_record_keys():
    skill = _skill()
    for key in ("next_steps", "mechanism_query", "stopped_by", "floor_lowered_reason",
                "floor_lowered_reasons", "opposite_direction", "another_horizon",
                "all_bars_version"):
        assert key in skill, key
    assert "A sizing finding is an observation, never a claim with a vehicle." in skill


def test_the_analyst_model_is_sonnet_5_5():
    cfg = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["analyst"]["model"] == "claude-sonnet-5-5"
    assert rpr._analyst_caps(cfg)["model"] == "claude-sonnet-5-5"
