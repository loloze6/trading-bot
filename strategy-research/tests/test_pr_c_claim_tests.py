"""PR-C (2026-10-19): claim tests gain the selector all_of, the bar-t fields
abs_forecast and forecast_sign_change, and the trade outcome trade_gross_return
(tools/claim_tests.py). trade_cost_share was dropped as a claim outcome (operator ruling
2026-10-19, B2); the TradeWindow keeps its gross_return and cost columns. Core checks
only; synthetic data (2020 dates), no market data is read.
"""
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np
import pytest

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(SR_ROOT / "tools"))

import claim_card as cc  # noqa: E402
import claim_measure as cm  # noqa: E402
import claim_tests as ct  # noqa: E402
import test_e068_claim_tests as e68  # noqa: E402
import test_e075_pr3_trade_tests as pr3  # noqa: E402
import test_e075_pr4_queries as pr4  # noqa: E402

T0 = 1577836800          # 2020-01-01 00:00 UTC
HOUR = 3600


def window(forecast, close=None, ts_rows=None):
    n = len(forecast)
    rows = np.arange(n) if ts_rows is None else np.asarray(ts_rows)
    ts = T0 + rows.astype(np.int64) * HOUR
    c = np.linspace(100.0, 100.0 + n, n) if close is None else np.asarray(close, float)
    return ct.Window("SYN", "w0", ts, c, np.asarray(forecast, float),
                     np.array(["chop"] * n, dtype=object), HOUR)


def spec(selector, baseline=None):
    return ct.TestSpec.from_dict({
        "selector": selector, "outcome": {"kind": "fwd_return", "horizons": [1]},
        "baseline": baseline or {"kind": "complement"}, "statistic": "mean_diff",
        "direction": "greater", "floor": {"min_events": 1}})


EV_HI = {"kind": "event", "field": "abs_forecast", "op": ">=", "value": 5}
EV_FLIP = {"kind": "event", "field": "forecast_sign_change", "op": "==", "value": 1}


def test_bar_t_fields_values_and_nan_rules():
    # rows 0..5 present, row 6 missing (a gap), rows 7..8 present
    w = window([3.0, -2.0, 0.0, -4.0, 5.0, np.nan, 2.0, -1.0], ts_rows=[0, 1, 2, 3, 4, 5, 7, 8])
    assert np.allclose(ct.abs_forecast(w)[:5], [3.0, 2.0, 0.0, 4.0, 5.0])
    sc = ct.forecast_sign_change(w)
    assert math.isnan(sc[0])                       # the first bar has no t-1
    assert sc[1] == 1.0                            # + -> -
    assert sc[2] == 0.0 and sc[3] == 0.0           # - -> 0 and 0 -> -: a zero has no sign
    assert sc[4] == 1.0                            # - -> +
    assert math.isnan(sc[5])                       # forecast t is NaN
    assert math.isnan(sc[6])                       # bar ts - step missing (the gap)
    assert sc[7] == 1.0


def test_bar_t_fields_read_no_future_row():
    fc = [3.0, -2.0, 1.0, -4.0, 5.0, 6.0]
    w = window(fc)
    fut = window(fc[:3] + [99.0, -99.0, 0.0])      # rows after t = 2 rewritten
    for fn in (ct.abs_forecast, ct.forecast_sign_change):
        a, b = fn(w), fn(fut)
        assert np.array_equal(a[:3], b[:3], equal_nan=True)


def test_all_of_is_the_and_of_its_parts():
    w = window([6.0, -6.0, 2.0, -7.0, 8.0, 1.0])
    sel = {"kind": "all_of", "selectors": [EV_HI, EV_FLIP]}
    m1, v1 = ct.SELECTORS["event"](w, EV_HI)
    m2, v2 = ct.SELECTORS["event"](w, EV_FLIP)
    m, v = ct.SELECTORS["all_of"](w, sel)
    assert np.array_equal(m, m1 & m2) and np.array_equal(v, v1 & v2)
    assert ct.check_spec(spec(sel)) == []


def test_all_of_checks():
    def errs(sel):
        return ct.check_spec(spec(sel))
    assert errs({"kind": "all_of", "selectors": [EV_HI]})                       # one part
    assert errs({"kind": "all_of", "selectors": [EV_HI, EV_FLIP, EV_HI, EV_FLIP]})
    assert errs({"kind": "all_of", "selectors": [EV_HI, EV_HI]})                # a part twice
    assert errs({"kind": "all_of", "selectors": [EV_HI, {"kind": "all"}]})
    nested = {"kind": "all_of", "selectors": [EV_HI, EV_FLIP]}
    assert any("cannot be nested" in e
               for e in errs({"kind": "all_of", "selectors": [EV_HI, nested]}))
    assert errs({"kind": "all_of", "selectors": [EV_HI, EV_FLIP], "field": "close"})
    bad = dict(EV_HI, field="fwd_return")
    assert any(e.startswith("selector.selectors[1]: field")
               for e in errs({"kind": "all_of", "selectors": [EV_FLIP, bad]}))


def test_all_of_hash_ignores_part_order_and_claim_card_accepts_it():
    a = spec({"kind": "all_of", "selectors": [EV_HI, EV_FLIP]})
    b = spec({"kind": "all_of", "selectors": [EV_FLIP, dict(EV_HI, value=5.0)]})
    assert ct.spec_hash(a) == ct.spec_hash(b)
    regime = {"kind": "regime", "value": "chop"}
    test = {"name": "t", "selector": {"kind": "all_of", "selectors": [regime, EV_HI]},
            "outcome": {"kind": "fwd_return", "horizons": [1]},
            "baseline": {"kind": "complement"}, "statistic": "mean_diff",
            "direction": "greater", "floor": {"min_events": 1}}
    errors, h, possible = cc._check_test(test, "test")
    assert errors == [] and h and possible is False      # a regime part: effect size only


def _bars(n=12):
    return window(np.ones(n))


def _trade(tid, e, x, gross_pct, net_pct):
    st = lambda i: np.datetime64(T0 + i * HOUR, "s").astype(str)   # noqa: E731
    return {"trade_id": tid, "side": "LONG", "entry_time": st(e), "exit_time": st(x),
            "exit_forecast": 1.0, "profit_loss_percent": gross_pct,
            "net_profit_loss_percent": net_pct}


def test_trade_gross_return_and_the_cost_column_on_both_bases():
    trades = [_trade("a", 1, 3, 2.0, 1.8), _trade("b", 4, 6, -1.0, -1.2),
              _trade("c", 7, 9, 0.0, -0.2)]
    post = np.zeros(12)
    tw = ct.build_trade_window(_bars(), trades, post)
    assert tw.basis == "net_of_fees_and_slippage"
    assert np.allclose(ct.trade_outcome(tw, "trade_gross_return", 0), [0.02, -0.01, 0.0])
    assert np.allclose(tw.cost, [0.002, 0.002, 0.002])                      # the column stays (S1)
    costs = [{"trade_id": t["trade_id"], "gross_return_before_costs": g, "cost_paid_all": c}
             for t, g, c in zip(trades, (2.5, -1.0, 0.4), (30.0, 25.0, 40.0))]
    tw2 = ct.build_trade_window(_bars(), trades, post, costs)
    assert tw2.basis == "all_costs"
    g2 = ct.trade_outcome(tw2, "trade_gross_return", 0)
    n2 = ct.trade_outcome(tw2, "trade_net_return", 0)
    assert np.allclose(g2, [0.025, -0.01, 0.004])
    assert np.allclose(g2 - n2, [0.003, 0.0025, 0.004])                     # net = gross - cost
    assert np.allclose(tw2.cost, [0.003, 0.0025, 0.004])


def test_trade_cost_share_is_no_longer_a_trade_outcome(prun):
    """B2 (operator ruling 2026-10-19): trade_cost_share is refused as an unknown trade outcome
    by check_spec, check_claim and conditional_effect, and trade_outcome has no branch for it."""
    assert "trade_cost_share" not in ct.TRADE_OUTCOMES
    assert ct.TRADE_OWN_OUTCOMES == ("trade_net_return", "trade_gross_return")
    sel = {"kind": "trade", "where": [{"field": "side", "op": "==", "value": "long"}]}
    sp = ct.TestSpec.from_dict({"selector": sel, "outcome": {"kind": "trade_cost_share"},
                                "baseline": {"kind": "other_trades"}, "statistic": "mean_diff",
                                "direction": "greater", "floor": {"min_events": 1}})
    assert ct.check_spec(sp, trade_tests=True) == [
        "outcome: a trade test needs one of ['trade_net_return', 'post_exit_return', "
        "'trade_gross_return'], got {'kind': 'trade_cost_share'}"]
    block = dict(pr3.GOOD_CLAIM_TEST, outcome={"kind": "trade_cost_share"})
    checked = cc.check_claim(pr3.claim(block), trade_tests=True)
    assert checked.errors and checked.tests == []
    assert any("got {'kind': 'trade_cost_share'}" in e for e in checked.errors), checked.errors
    eng = pr4.engine(prun)
    res = eng.conditional_effect(sel, None, "trade_cost_share", None, "mean_diff", "greater")
    assert res["status"] == "refused" and res["n_comparisons"] == 0
    assert res["reason"] == (                     # the query builds the outcome with its horizons
        "outcome: a trade test needs one of ['trade_net_return', 'post_exit_return', "
        "'trade_gross_return'], got {'kind': 'trade_cost_share', 'horizons': None}")


def test_own_outcomes_take_no_horizons_and_measure_at_horizon_zero():
    sel = {"kind": "trade", "where": [{"field": "side", "op": "==", "value": "long"}]}
    for kind in ("trade_gross_return",):
        good = ct.TestSpec.from_dict({"selector": sel, "outcome": {"kind": kind},
                                      "baseline": {"kind": "other_trades"},
                                      "statistic": "mean_diff", "direction": "greater",
                                      "floor": {"min_events": 1}})
        assert ct.check_spec(good, trade_tests=True) == []
        assert ct._trade_horizons(good) == [0]
        bad = ct.TestSpec.from_dict({**{"selector": sel, "baseline": {"kind": "other_trades"},
                                        "statistic": "mean_diff", "direction": "greater",
                                        "floor": {"min_events": 1}},
                                     "outcome": {"kind": kind, "horizons": [1]}})
        assert any("no horizons" in e for e in ct.check_spec(bad, trade_tests=True))


# ===========================================================================
# Part 2 (docs commit): the full test list. Synthetic data only.
# ===========================================================================

PR2 = {"kind": "event", "field": "past_return", "bars": 2, "op": ">=", "value": 0.0}
ABS1 = {"kind": "event", "field": "abs_forecast", "op": ">=", "value": 1}
CAL_H3 = {"kind": "calendar", "hours": [3]}
CAL_WD5 = {"kind": "calendar", "weekdays": [5]}


def all_of(*parts):
    return {"kind": "all_of", "selectors": list(parts)}


def _w_nan():
    """10 hourly bars, a NaN forecast at bar 3 (so the sign change is NaN at 3 and 4)."""
    fc = [2.0, -3.0, 0.5, np.nan, -4.0, 5.0, -1.0, 0.0, 2.0, -2.0]
    close = [100, 101, 99, 98, 102, 103, 101, 104, 103, 105]
    return window(fc, close)


# ---------------------------------------------------------------------------
# 1. all_of
# ---------------------------------------------------------------------------

def test_all_of_is_the_and_of_masks_and_of_valids_with_nan_parts():
    w = _w_nan()
    for parts in ([PR2, EV_FLIP], [PR2, EV_FLIP, ABS1], [ABS1, EV_FLIP]):
        m, v = ct.SELECTORS["all_of"](w, all_of(*parts))
        ms, vs = zip(*(ct.SELECTORS[p["kind"]](w, p) for p in parts))
        assert np.array_equal(m, np.logical_and.reduce(ms))
        assert np.array_equal(v, np.logical_and.reduce(vs))
        assert not (m & ~v).any()                         # a selected bar is a defined bar
    m, v = ct.SELECTORS["all_of"](w, all_of(PR2, EV_FLIP))
    assert not v[:2].any()                                # past_return(2): two earlier bars needed
    assert not v[3] and not v[4]                          # forecast NaN at 3: change NaN at 3 and 4
    assert v[2] and v[5:].all()
    assert np.flatnonzero(m).tolist() == [5, 9]           # a flip on a bar that also rose over 2 bars
    # three parts: one more condition can only remove bars
    m3, v3 = ct.SELECTORS["all_of"](w, all_of(PR2, EV_FLIP, {"kind": "event", "field": "abs_forecast",
                                                              "op": ">=", "value": 3}))
    assert np.flatnonzero(m3).tolist() == [5] and np.array_equal(v3, v)


def test_all_of_as_an_other_selector_baseline():
    w = _w_nan()
    other = all_of(PR2, EV_FLIP)
    sel = {"kind": "event", "field": "abs_forecast", "op": ">=", "value": 3}
    base = {"kind": "other_selector", "selector": other}
    sp = spec(sel, base)
    assert ct.check_spec(sp) == []
    mask, valid = ct.SELECTORS["event"](w, sel)
    wts = ct.BASELINES["other_selector"](w, mask, valid, base, 1, None)
    m2, v2 = ct.SELECTORS["all_of"](w, other)
    assert np.array_equal(wts > 0, m2 & v2 & valid & ~mask)
    assert np.flatnonzero(wts).tolist() == [9]            # bar 5 is selected itself; bar 9 is not
    ct.effect_sizes([w], sp)                              # and it measures
    bad = spec(sel, {"kind": "other_selector", "selector": all_of(PR2)})
    assert any(e.startswith("baseline.selector: selectors must be a list of 2 to 3")
               for e in ct.check_spec(bad))


def test_all_of_calendar_period_and_the_placebo_shifts(monkeypatch):
    assert ct._calendar_period(all_of(CAL_WD5, EV_HI), HOUR) == 168
    assert ct._calendar_period(all_of(CAL_H3, EV_HI), HOUR) == 24
    assert ct._calendar_period(all_of(CAL_H3, CAL_WD5), HOUR) == 168     # a weekday part: a week
    assert ct._calendar_period(all_of(EV_HI, EV_FLIP), HOUR) is None     # no calendar part
    assert ct._calendar_period(all_of(CAL_WD5, EV_HI), 24 * HOUR) == 7
    seen = []
    real = ct._shift_offsets

    def spy(n, h_max, rng, size, period=None):
        k = real(n, h_max, rng, size, period)
        seen.append((period, k))
        return k

    monkeypatch.setattr(ct, "_shift_offsets", spy)
    w = window(np.where(np.arange(600) % 2 == 0, 6.0, -6.0))
    for parts, period in (((CAL_H3, EV_FLIP), 24), ((CAL_WD5, CAL_H3, EV_FLIP), 168)):
        seen.clear()
        sp = spec(all_of(*parts), {"kind": "placebo", "n_draws": 4})
        assert ct.check_spec(sp) == []
        ct.effect_sizes([w], sp)
        assert seen and all(p == period for p, _ in seen)
        assert all(not np.any(k % period == 0) for _, k in seen)          # no whole-period shift


@pytest.mark.parametrize("sel", [
    all_of(e68.EVENT, {"kind": "calendar", "weekdays": [5, 6]}),
    all_of({"kind": "event", "field": "abs_forecast", "op": ">=", "value": 5},
           {"kind": "quantile", "field": "close", "side": "bottom", "q": 0.1, "lookback": 20},
           e68.EVENT_HIGH),
    all_of({"kind": "event", "field": "forecast_sign_change", "op": "==", "value": 1},
           {"kind": "event", "field": "past_return", "bars": 3, "op": ">", "value": 0.0}),
], ids=["calendar", "three_parts", "sign_change_past_return"])
def test_all_of_never_reads_the_future(sel):
    """The same rewrite-the-future check as test_e068's LOOKAHEAD_SELECTORS, on all_of selectors
    that mix the old and the new fields (the plain ones live in that list too)."""
    w = e68.make_windows(22, n_windows=1)[0]
    mask, valid = ct.SELECTORS["all_of"](w, sel)
    rng = np.random.default_rng(23)
    for t in (40, 150, 233, len(w.ts) - 2):
        k = len(w.ts) - t - 1
        fut = ct.Window(w.symbol, w.window, w.ts.copy(), w.close.copy(), w.forecast.copy(),
                        w.regime.copy(), w.step)
        fut.close[t + 1:] = rng.uniform(1, 1000, k)
        fut.forecast[t + 1:] = rng.uniform(-20, 20, k)
        m2, v2 = ct.SELECTORS["all_of"](fut, sel)
        assert np.array_equal(mask[:t + 1], m2[:t + 1]), t
        assert np.array_equal(valid[:t + 1], v2[:t + 1]), t


def test_all_of_refusal_messages():
    def errs(sel, baseline=None):
        return ct.check_spec(spec(sel, baseline))
    shape = "selector: selectors must be a list of 2 to 3 bar selectors, all of which must hold"
    assert errs(all_of(EV_HI)) == [shape]                                  # one part
    assert errs(all_of(EV_HI, EV_FLIP, ABS1, PR2)) == [shape]              # four parts
    assert errs({"kind": "all_of", "selectors": "x"}) == [shape]           # not a list
    assert errs(all_of()) == [shape]
    exact = "selector: an all_of selector is exactly {kind: all_of, selectors: [...]}"
    assert errs({"kind": "all_of", "selectors": [EV_HI, EV_FLIP], "field": "close"}) == [exact]
    assert errs({"kind": "all_of"}) == [exact]
    assert errs(all_of(EV_HI, {"kind": "all"})) == [
        "selector.selectors[1]: `all` selects every bar; the AND is the other selector(s) alone"]
    assert errs(all_of(EV_HI, all_of(EV_FLIP, ABS1))) == [
        "selector.selectors[1]: all_of cannot be nested; list every condition in one all_of"]
    assert errs(all_of(EV_HI, EV_HI)) == [
        "selector.selectors[1]: repeats selectors[0]; write each condition once"]
    assert errs(all_of(EV_HI, dict(EV_HI, value=5.0))) == [                # 5 and 5.0 are one number
        "selector.selectors[1]: repeats selectors[0]; write each condition once"]
    assert errs(all_of(EV_HI, "x")) == [
        "selector.selectors[1]: unknown selector 'x'; known: ['all', 'all_of', 'calendar', "
        "'event', 'quantile', 'regime', 'regime_change']"]
    assert errs(all_of(EV_HI, 7)) and errs(all_of(EV_HI, None)) and errs(all_of(EV_HI, ["a"]))
    # a part is checked as a selector of its own, and named by its place
    bad = dict(EV_FLIP, field="fwd_return")
    assert errs(all_of(EV_HI, bad)) == [
        "selector.selectors[1]: field 'fwd_return' is not a bar-t field (allowed: "
        f"{list(ct.BAR_T_FIELDS)}); a selector may not read the future"]
    # as a baseline selector the same messages carry the baseline path
    base = {"kind": "other_selector", "selector": all_of(EV_HI, {"kind": "all"})}
    assert errs(EV_FLIP, base) == [
        "baseline.selector.selectors[1]: `all` selects every bar; the AND is the other "
        "selector(s) alone"]


def test_all_of_hash_ignores_part_order_also_inside_a_baseline():
    parts = [EV_HI, EV_FLIP, CAL_H3]
    hashes = {ct.spec_hash(spec(all_of(*p))) for p in itertools.permutations(parts)}
    assert len(hashes) == 1
    base_hashes = {ct.spec_hash(spec(EV_HI, {"kind": "other_selector", "selector": all_of(*p)}))
                   for p in itertools.permutations(parts)}
    assert len(base_hashes) == 1
    assert ct.spec_hash(spec(all_of(EV_HI, EV_FLIP))) != ct.spec_hash(spec(all_of(EV_HI, CAL_H3)))
    assert ct.spec_hash(spec(all_of(EV_HI, EV_FLIP))) != ct.spec_hash(spec(EV_HI))
    # the sub-selectors' own key order and 5 vs 5.0 do not matter either
    a = {"op": ">=", "kind": "event", "value": 5.0, "field": "abs_forecast"}
    assert ct.spec_hash(spec(all_of(EV_FLIP, a))) == ct.spec_hash(spec(all_of(EV_HI, EV_FLIP)))
    # a malformed all_of is hashed as it came and refused by check_spec, never raised on
    odd = {"kind": "all_of", "selectors": [EV_HI, "x"]}
    assert ct.spec_hash(spec(odd)) and ct.check_spec(spec(odd))


def test_a_value_past_float_range_in_a_part_is_refused_as_for_any_selector():
    huge = dict(EV_HI, value=10 ** 400)
    plain = spec(huge)
    nested = spec(all_of(huge, EV_FLIP))
    # check_spec itself does not raise on it (the duplicate test skips an unhashable part) ...
    assert ct.check_spec(nested) == ct.check_spec(plain) == []
    # ... and whatever the plain selector does downstream, the all_of does too
    with pytest.raises(OverflowError):
        ct.spec_hash(plain)
    with pytest.raises(OverflowError):
        ct.spec_hash(nested)
    # the same number twice: no crash while looking for the duplicate
    assert ct.check_spec(spec(all_of(huge, dict(huge)))) == []


# ---------------------------------------------------------------------------
# 2. conditional_effect with all_of == claim_measure
# ---------------------------------------------------------------------------

@pytest.fixture()
def prun(tmp_path):
    return pr4.make_run(tmp_path / "run_001")


ALL_OFS = [
    all_of({"kind": "event", "field": "abs_forecast", "op": ">=", "value": 4.0},
           {"kind": "calendar", "hours": [3, 4, 5, 6, 7, 8]}),
    all_of({"kind": "event", "field": "past_return", "bars": 3, "op": "<=", "value": 0.0},
           {"kind": "event", "field": "trailing_vol", "bars": 6, "op": ">=", "value": 0.002},
           {"kind": "event", "field": "abs_forecast", "op": ">=", "value": 2.0}),
    all_of({"kind": "event", "field": "forecast_sign_change", "op": "==", "value": 1},
           {"kind": "event", "field": "forecast", "op": ">=", "value": 0.0}),
    all_of({"kind": "regime", "value": "trending"},
           {"kind": "event", "field": "abs_forecast", "op": ">=", "value": 3.0}),
]


@pytest.mark.parametrize("sel", ALL_OFS, ids=["calendar", "three_parts", "sign_change", "regime"])
def test_conditional_effect_with_an_all_of_condition_equals_claim_measure(sel, prun):
    eng = pr4.engine(prun)
    windows = ct.load_variant_bars(prun, "base")
    has_regime = any(p["kind"] in ("regime", "regime_change") for p in sel["selectors"])
    n_calls = 0
    for base in ({"kind": "complement"}, {"kind": "placebo"},
                 {"kind": "other_selector", "selector": {"kind": "calendar", "hours": [10, 11]}}):
        test = {"selector": sel, "outcome": {"kind": "fwd_return", "horizons": [1, 3]},
                "baseline": base, "statistic": "mean_diff", "direction": "greater",
                "floor": {"min_events": 1}}
        res = eng.conditional_effect(sel, [1, 3], "fwd_return", base, "mean_diff", "greater")
        spec_ = pr4._same(res, windows, test)
        assert res["n_comparisons"] == 2                      # one per horizon, as for any selector
        assert res["result"]["compiles_as_claim"] is True and "claim_check" not in res["result"]
        assert pr4._measure_the_block(res, windows, spec_) is True
        # as a claim: accepted; a regime part leaves an effect size and no verdict
        claim = {"statement": "s", "kind": "conditional_behaviour", "tests": [res["result"]["test"]],
                 "pass_if": "p", "fail_if": "f", "rationale": "r"}
        checked = cc.check_claim(claim)
        assert checked.errors == []
        assert checked.tests[0]["verdict_possible"] is (not has_regime)
        n_calls += 1
    assert len(pr4.log_of(eng)) == n_calls


def test_a_regime_part_gets_no_verdict_from_run_test():
    sp = spec(all_of({"kind": "regime", "value": "chop"}, EV_HI))
    errs = ct.check_spec(sp)
    assert errs and all("cannot be graded under" in e for e in errs)
    assert errs[0].startswith("selector.selectors[0]: regime cannot be graded under")
    with pytest.raises(ValueError, match="cannot be graded"):
        ct.run_test([window(np.ones(40))], sp, calibrated=True)
    # an effect size is still measured (the claim-measure path)
    out = ct.effect_sizes([window(np.where(np.arange(40) % 2 == 0, 6.0, 1.0))], sp)
    assert out[1][1]["n_events"] >= 0


# ---------------------------------------------------------------------------
# 3. claim_card: signal columns and the verdict flag
# ---------------------------------------------------------------------------

def test_signal_columns_of_the_new_selectors():
    regime = {"kind": "regime", "value": "chop"}
    close_ev = {"kind": "event", "field": "close", "op": ">", "value": 1}

    def cols(selector, baseline=None, statistic="mean_diff"):
        return cc.signal_columns({"selector": selector, "baseline": baseline, "statistic": statistic})

    assert cols(EV_HI) == {"forecast"} and cols(EV_FLIP) == {"forecast"}          # the new fields
    assert cols({"kind": "quantile", "field": "abs_forecast", "side": "top", "q": 0.2,
                 "lookback": 10}) == {"forecast"}
    assert cols(all_of(EV_HI, CAL_H3)) == {"forecast"}
    assert cols(all_of(regime, EV_HI)) == {"regime", "forecast"}
    assert cols(all_of(close_ev, CAL_H3)) == set()
    assert cols(close_ev, {"kind": "other_selector", "selector": all_of(EV_FLIP, CAL_H3)}) == {"forecast"}
    assert cols(close_ev, {"kind": "other_selector", "selector": all_of(regime, CAL_H3)}) == {"regime"}
    assert cols(all_of(close_ev, CAL_H3), None, "rank_ic") == {"forecast"}
    assert cc.expected_block({"regime", "forecast"}) == "regime"


def test_a_regime_part_sets_verdict_possible_false_in_selector_and_baseline():
    def test(selector, baseline):
        return {"name": "t", "selector": selector, "outcome": {"kind": "fwd_return", "horizons": [1]},
                "baseline": baseline, "statistic": "mean_diff", "direction": "greater",
                "floor": {"min_events": 1}}
    regime = {"kind": "regime", "values": ["chop", "trend"]}
    cases = [
        (test(all_of(EV_HI, EV_FLIP), {"kind": "complement"}), True),
        (test(all_of(regime, EV_HI), {"kind": "complement"}), False),
        (test(EV_HI, {"kind": "other_selector", "selector": all_of(EV_FLIP, regime)}), False),
        (test(EV_HI, {"kind": "other_selector", "selector": all_of(EV_FLIP, CAL_H3)}), True),
        (test(all_of({"kind": "regime_change", "to": "chop"}, EV_FLIP), {"kind": "complement"}), False),
    ]
    for t, want in cases:
        errors, h, possible = cc._check_test(t, "test")
        assert errors == [] and h and possible is want, (t, errors)
    # a regime part is named by its path, so another refusal in the same test is not hidden
    t = test(all_of(regime, dict(EV_HI, op="~")), {"kind": "complement"})
    errors, _h, _p = cc._check_test(t, "test")
    assert errors and all("cannot be graded" not in e for e in errors)


# ---------------------------------------------------------------------------
# 4. abs_forecast and forecast_sign_change as selector fields
# ---------------------------------------------------------------------------

def _gap_window():
    fc = [3.0, -2.0, 0.0, -4.0, 5.0, np.nan, 2.0, -1.0, 6.0, -6.0]
    return window(fc, ts_rows=[0, 1, 2, 3, 4, 5, 7, 8, 9, 10])        # bar 6 is missing


def test_event_on_abs_forecast_and_forecast_sign_change():
    w = _gap_window()
    ev = lambda f, op, v: {"kind": "event", "field": f, "op": op, "value": v}      # noqa: E731
    m, v = ct.SELECTORS["event"](w, ev("abs_forecast", ">=", 5))
    assert v.tolist() == [True] * 5 + [False] + [True] * 4                  # NaN only at the NaN forecast
    assert np.flatnonzero(m).tolist() == [4, 8, 9]
    m, v = ct.SELECTORS["event"](w, ev("abs_forecast", "==", 0))
    assert np.flatnonzero(m).tolist() == [2] and v[2]                       # zero is a value
    m, v = ct.SELECTORS["event"](w, ev("forecast_sign_change", "==", 1))
    assert v.tolist() == [False, True, True, True, True, False, False, True, True, True]
    assert np.flatnonzero(m).tolist() == [1, 4, 7, 8, 9]    # -2 -> 0 and 0 -> -4 are not changes
    m, v = ct.SELECTORS["event"](w, ev("forecast_sign_change", "==", 0))
    assert np.flatnonzero(m).tolist() == [2, 3]
    assert not v[0] and not v[6]                             # first bar; the bar before is missing
    for sel in (ev("abs_forecast", ">", 1), ev("forecast_sign_change", ">=", 1)):
        assert ct.check_spec(spec(sel)) == []
        assert ct.check_spec(spec(dict(sel, bars=2))) == [
            "selector: `bars` is only allowed with field ['past_return', 'trailing_vol']"]


def test_quantile_on_abs_forecast_and_forecast_sign_change():
    w = _gap_window()
    sel = {"kind": "quantile", "field": "abs_forecast", "side": "top", "q": 0.5, "lookback": 3}
    m, v = ct.SELECTORS["quantile"](w, sel)
    # |forecast| = 3 2 0 4 5 nan 2 1 6 6: the trailing 3 bars must all be finite
    assert v.tolist() == [False, False, False, True, True, False, False, False, False, True]
    assert np.flatnonzero(m).tolist() == [3, 4, 9]
    assert ct.check_spec(spec(sel)) == []
    # N1 (operator ruling 2026-10-19): a 0/1 field is selected by an event, never a quantile
    msg = ('forecast_sign_change is 0 or 1: select it with {kind: event, field: '
           'forecast_sign_change, op: "==", value: 1}')
    sel2 = dict(sel, field="forecast_sign_change", side="bottom")
    assert ct.check_spec(spec(sel2)) == [f"selector: {msg}"]
    assert ct.check_spec(spec(all_of(EV_HI, sel2))) == [f"selector.selectors[1]: {msg}"]
    assert ct.check_spec(spec(EV_HI, {"kind": "other_selector", "selector": sel2})) == [
        f"baseline.selector: {msg}"]
    assert ct.check_spec(spec(EV_FLIP)) == []                    # the event form stays valid


def test_run_test_and_the_null_accept_the_new_fields():
    ws = e68.make_windows(5, n=200, n_windows=3)
    abs_ev = {"kind": "event", "field": "abs_forecast", "op": ">=", "value": 10}
    sels = [abs_ev, EV_FLIP,
            all_of(dict(abs_ev, value=8), {"kind": "calendar", "weekdays": [0, 1, 2, 3, 4]})]
    for sel in sels:
        sp = e68.spec(sel, floor={"min_events": 5})
        res = e68.rt(ws, sp)                                   # calibrated: the null is drawn
        assert res["status"] in ("supported", "refuted", "inconclusive"), res
        assert res["spec_hash"] == ct.spec_hash(sp)
    # the null window recomputes the forecast; the selectors read the recomputed one
    fw = ct.fake_window(ws[0], np.random.default_rng(1))
    m, v = ct.SELECTORS["event"](fw, abs_ev)
    assert np.array_equal(v, np.isfinite(fw.forecast))
    assert np.array_equal(m, v & (np.abs(np.nan_to_num(fw.forecast)) >= 10))
    sc, sv = ct.SELECTORS["event"](fw, EV_FLIP)
    assert np.array_equal(sc & sv, sc) and not sv[0]


def test_claim_tests_forecast_sign_change_is_the_analyst_derived_column(prun):
    """#491's derived column (analyst_queries) and the claim field are one definition: same
    bars, zeros, a NaN forecast and a missing stamp."""
    import analyst_queries as aq
    res = Path(prun) / "variants" / "base" / "results"
    for k, rid in enumerate(sorted(p.name for p in res.iterdir())):
        csv = res / rid / "bars.csv"
        lines = csv.read_text(encoding="utf-8").splitlines()
        head, rows = lines[0], lines[1:]
        col = head.split(",").index("forecast")
        pattern = [3.0, -2.0, 0.0, 4.0, -1.0, 0.0, 0.0, 5.0, -5.0, 2.0]
        out = []
        for i, line in enumerate(rows):
            cells = line.split(",")
            cells[col] = repr(pattern[i % 10] * (1 + k)) if i % 17 != 5 else "nan"
            out.append(",".join(cells))
        del out[40]                                           # one missing stamp
        csv.write_text("\n".join([head] + out) + "\n", encoding="utf-8")
    eng = pr4.engine(prun)
    windows = ct.load_variant_bars(prun, "base")
    for column, fn in (("forecast_sign_change", ct.forecast_sign_change),
                       ("abs_forecast", ct.abs_forecast)):
        got = eng._column_values("base", column)
        assert len(got) == len(windows) == 3
        for g, w in zip(got, windows):
            assert np.array_equal(np.asarray(g, float), fn(w), equal_nan=True)
    sc = ct.forecast_sign_change(windows[0])
    assert np.isnan(sc[0]) and np.isnan(sc[5]) and np.isnan(sc[40]) and sc[1] == 1.0
    assert aq.DERIVED_COLUMNS.count("forecast_sign_change") == 1


# ---------------------------------------------------------------------------
# 5. trade_gross_return (trade_cost_share dropped, B2; the cost column stays)
# ---------------------------------------------------------------------------

def _gross_trades(extra=0.2):
    """pr3.TRADES with profit_loss_percent = net + extra (so the commission is `extra` %)."""
    return [dict(t, profit_loss_percent=t["net_profit_loss_percent"] + extra) for t in pr3.TRADES]


def test_missing_source_fields_give_nan():
    tw = pr3.twin()                                            # these lots carry no profit_loss_percent
    assert np.isnan(ct.trade_outcome(tw, "trade_gross_return", 0)).all()
    assert np.isnan(tw.cost).all()
    assert np.isfinite(ct.trade_outcome(tw, "trade_net_return", 0)).all()
    # gross present, net missing: the cost is unknown too
    t = {k: v for k, v in pr3.TRADES[0].items() if k != "net_profit_loss_percent"}
    tw2 = ct.build_trade_window(pr3.bars(), [dict(t, profit_loss_percent=1.0)], pr3.post_alloc())
    assert ct.trade_outcome(tw2, "trade_gross_return", 0).tolist() == [0.01]
    assert np.isnan(tw2.cost).all()
    assert np.isnan(ct.trade_outcome(tw2, "trade_net_return", 0)).all()
    # an all_costs record that is complete for some lots only is not used at all (the basis stays)
    costs = [{"trade_id": "t0", "gross_return_before_costs": 2.0, "cost_paid_all": 30.0}]
    tw3 = pr3.twin(trades=_gross_trades(), costs=costs)
    assert tw3.basis == "net_of_fees_and_slippage"
    assert np.allclose(ct.trade_outcome(tw3, "trade_gross_return", 0),
                       [t["profit_loss_percent"] / 100 for t in _gross_trades()])


def test_net_is_gross_minus_the_cost_column_on_both_bases():
    trades = _gross_trades(0.2)
    trades[1] = dict(trades[1], profit_loss_percent=0.0, net_profit_loss_percent=-0.2)   # gross 0
    trades[4] = dict(trades[4], profit_loss_percent=-1.0, net_profit_loss_percent=-1.2)  # negative gross
    tw = pr3.twin(trades=trades)
    g, n = (ct.trade_outcome(tw, k, 0) for k in ("trade_gross_return", "trade_net_return"))
    assert g[1] == 0.0 and g[4] == pytest.approx(-0.01)
    assert np.allclose(tw.cost, 0.002) and np.allclose(g - n, tw.cost)
    costs = [{"trade_id": t["trade_id"], "gross_return_before_costs": g, "cost_paid_all": c}
             for t, g, c in zip(trades, [2.0, 0.0] + [1.0] * 10, [30.0, 10.0] + [20.0] * 10)]
    tw2 = pr3.twin(trades=trades, costs=costs)
    assert tw2.basis == "all_costs"
    g2, n2 = (ct.trade_outcome(tw2, k, 0) for k in ("trade_gross_return", "trade_net_return"))
    assert np.allclose(g2 - n2, [0.003, 0.001] + [0.002] * 10)           # net = gross - cost
    assert np.allclose(tw2.cost, [0.003, 0.001] + [0.002] * 10)


@pytest.mark.parametrize("kind", ["trade_gross_return"])
def test_mixed_bases_are_refused_for_the_gross_outcome(kind):
    w0 = pr3.twin(trades=_gross_trades(), costs=pr3.ALL_COSTS)                       # all_costs
    w1 = ct.build_trade_window(pr3.bars(label="w1"), _gross_trades(), pr3.post_alloc())  # fallback
    sp = pr3.spec([pr3.eq("exit_cause", "flip")], {"kind": kind})
    with pytest.raises(ct.MixedReturnBasis, match=f"{kind} over windows with different return bases"):
        ct.effect_sizes([w0, w1], sp)
    block = dict(pr3.GOOD_CLAIM_TEST, outcome={"kind": kind})
    res = cm.measure_test([w0, w1], block, None, True)
    assert res["status"] == cm.NOT_MEASURED and res["reason"] == cm.MIXED_BASES
    assert "SYN/w0" in res["detail"] and "SYN/w1" in res["detail"]
    # one basis in every window pools fine
    out = ct.effect_sizes([w0, ct.build_trade_window(pr3.bars(label="w1"), _gross_trades(),
                                                     pr3.post_alloc(), pr3.ALL_COSTS)], sp)[1]
    assert sorted(out) == [0] and out[0]["bases"] == ["all_costs"]


@pytest.mark.parametrize("kind", ["trade_gross_return"])
def test_per_window_basis_is_recorded_and_blocks_are_overlap_stretches(kind):
    w0 = pr3.twin(trades=_gross_trades())
    w1 = ct.build_trade_window(pr3.bars(label="w1"), _gross_trades(), pr3.post_alloc())
    where = [{"field": "exit_cause", "op": "!=", "value": "unknown"}]
    one = ct.effect_sizes([w0], pr3.spec(where, {"kind": kind}))[1]
    assert sorted(one) == [0]                                          # horizon 0: the lot's life
    assert one[0]["n_events"] == 10 and one[0]["n_blocks"] == 3        # stretches, not entry bars
    assert one[0]["bases"] == ["net_of_fees_and_slippage"]
    two = ct.effect_sizes([w0, w1], pr3.spec(where, {"kind": kind}))[1]
    assert two[0]["n_events"] == 20 and two[0]["n_blocks"] == 6
    assert {k: v["basis"] for k, v in two[0]["per_window"].items()} == {
        "SYN/w0": "net_of_fees_and_slippage", "SYN/w1": "net_of_fees_and_slippage"}
    # a window with no trades has no basis and conflicts with nothing
    empty = ct.build_trade_window(pr3.bars(label="w2"), [], pr3.post_alloc())
    out = ct.effect_sizes([w0, empty], pr3.spec(where, {"kind": kind}))[1]
    assert out[0]["per_window"]["SYN/w2"]["basis"] is None and out[0]["bases"] == [w0.basis]
    # lots with no figure to measure are not events
    nogross = ct.effect_sizes([pr3.twin()], pr3.spec(where, {"kind": kind}))[1]
    assert nogross[0]["n_events"] == 0 and nogross[0]["n_blocks"] == 0


def _with_gross(run, extra=0.3):
    for p in sorted(Path(run).glob("variants/base/results/*/trades.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        for x in data:
            x["profit_loss_percent"] = x["net_profit_loss_percent"] + extra
        p.write_text(json.dumps(data), encoding="utf-8")


@pytest.mark.parametrize("kind", ["trade_gross_return"])
def test_conditional_effect_and_claim_measure_on_the_trade_outcomes(kind, prun):
    _with_gross(prun)
    eng = pr4.engine(prun)
    twins = ct.load_variant_trade_windows(prun, "base")
    sel = {"kind": "trade", "where": [{"field": "side", "op": "==", "value": "long"}]}
    for stat in ("mean_diff", "hit_rate"):
        test = {"selector": sel, "outcome": {"kind": kind}, "baseline": {"kind": "other_trades"},
                "statistic": stat, "direction": "greater", "floor": {"min_events": 1}}
        res = eng.conditional_effect(sel, None, kind, None, stat, "greater")
        spec_ = pr4._same(res, twins, test, trade=True)
        assert res["result"]["unit"] == "trades" and list(res["result"]["horizons"]) == ["trade"]
        assert res["result"]["outcome"] == kind and res["n_comparisons"] == 1
        assert res["result"]["horizons"]["trade"]["n_events"] > 0
        assert res["result"]["compiles_as_claim"] is True
        assert pr4._measure_the_block(res, twins, spec_, trade=True) is True
        m = cm.measure_test(twins, res["result"]["test"], None, True)
        assert m["status"] == cm.MEASURED and sorted(m["horizons"]) == [0]
        assert m["horizons"][0]["bases"] == ["net_of_fees_and_slippage"]
        assert m["horizons"][0]["n_blocks"] == res["result"]["horizons"]["trade"]["n_blocks"]
        # a trade test has an effect size and no verdict
        claim = pr3.claim(res["result"]["test"])
        checked = cc.check_claim(claim, trade_tests=True)
        assert checked.errors == [] and checked.tests[0]["verdict_possible"] is False
    # horizons are refused, naming the outcome, charged nothing, and logged
    n_before = len(pr4.log_of(eng))
    bad = eng.conditional_effect(sel, [1, 2], kind)
    assert bad["status"] == "refused" and kind in pr4.log_of(eng)[-1]["reason"]
    assert bad["n_comparisons"] == 0 and len(pr4.log_of(eng)) == n_before + 1


def test_the_gross_figures_are_trades_json_over_one_hundred(prun):
    _with_gross(prun, 0.3)
    twins = ct.load_variant_trade_windows(prun, "base")
    for tw in twins:
        g = ct.trade_outcome(tw, "trade_gross_return", 0)
        n = ct.trade_outcome(tw, "trade_net_return", 0)
        assert np.allclose(g, n + 0.003)
        assert np.allclose(tw.cost, 0.003)


# ---------------------------------------------------------------------------
# 6. the default check_spec (no trade_tests) refuses the new outcomes as before PR-3
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("kind", ["trade_gross_return"])
def test_default_check_spec_and_check_claim_refuse_the_new_outcomes_as_before_pr3(kind):
    where = [{"field": "exit_cause", "op": "==", "value": "flip"}]
    sp = ct.TestSpec.from_dict({"selector": {"kind": "trade", "where": where},
                                "outcome": {"kind": kind}, "baseline": {"kind": "other_trades"},
                                "statistic": "mean_diff", "direction": "greater",
                                "floor": {"min_events": 1}})
    assert ct.check_spec(sp) == [
        "selector: unknown selector {'kind': 'trade', 'where': [{'field': 'exit_cause', 'op': '==', "
        "'value': 'flip'}]}; known: ['all', 'all_of', 'calendar', 'event', 'quantile', 'regime', "
        "'regime_change']",
        f"outcome: unknown {{'kind': '{kind}'}}; known: ['fwd_max_drawdown', 'fwd_return', "
        "'fwd_volatility', 'trend_ends']",
        "baseline: unknown {'kind': 'other_trades'}; known: ['complement', 'other_selector', 'placebo']"]
    assert ct.check_spec(sp, trade_tests=True) == []
    block = dict(pr3.GOOD_CLAIM_TEST, outcome={"kind": kind})
    off = cc.check_claim(pr3.claim(block))
    assert off.errors and off.tests == []
    assert cc.check_claim(pr3.claim(block), trade_tests=True).errors == []
    # a bar selector with a trade outcome: the gated family's own refusal, naming the new kinds
    mixed = ct.TestSpec.from_dict({"selector": {"kind": "all"}, "outcome": {"kind": kind},
                                   "baseline": {"kind": "other_trades"}, "statistic": "mean_diff",
                                   "direction": "greater", "floor": {"min_events": 1}})
    assert ct.check_spec(mixed, trade_tests=True) == [
        "selector: the trade outcomes ['trade_net_return', 'post_exit_return', 'trade_gross_return'] "
        "and the baseline ['other_trades'] need a selector of kind 'trade'"]
