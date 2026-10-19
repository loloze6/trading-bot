"""PR-C (2026-10-19): claim tests gain the selector all_of, the bar-t fields
abs_forecast and forecast_sign_change, and the trade outcomes trade_gross_return
and trade_cost_share (tools/claim_tests.py). Core checks only; synthetic data
(2020 dates), no market data is read.
"""
import math
import sys
from pathlib import Path

import numpy as np

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "tools"))

import claim_card as cc  # noqa: E402
import claim_tests as ct  # noqa: E402

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


def test_trade_gross_return_and_cost_share_on_both_bases():
    trades = [_trade("a", 1, 3, 2.0, 1.8), _trade("b", 4, 6, -1.0, -1.2),
              _trade("c", 7, 9, 0.0, -0.2)]
    post = np.zeros(12)
    tw = ct.build_trade_window(_bars(), trades, post)
    assert tw.basis == "net_of_fees_and_slippage"
    assert np.allclose(ct.trade_outcome(tw, "trade_gross_return", 0), [0.02, -0.01, 0.0])
    share = ct.trade_outcome(tw, "trade_cost_share", 0)
    assert np.allclose(share[:2], [0.002 / 0.02, 0.002 / 0.01]) and math.isnan(share[2])
    costs = [{"trade_id": t["trade_id"], "gross_return_before_costs": g, "cost_paid_all": c}
             for t, g, c in zip(trades, (2.5, -1.0, 0.4), (30.0, 25.0, 40.0))]
    tw2 = ct.build_trade_window(_bars(), trades, post, costs)
    assert tw2.basis == "all_costs"
    g2 = ct.trade_outcome(tw2, "trade_gross_return", 0)
    n2 = ct.trade_outcome(tw2, "trade_net_return", 0)
    assert np.allclose(g2, [0.025, -0.01, 0.004])
    assert np.allclose(g2 - n2, [0.003, 0.0025, 0.004])                     # net = gross - cost
    assert np.allclose(ct.trade_outcome(tw2, "trade_cost_share", 0), [0.12, 0.25, 1.0])


def test_own_outcomes_take_no_horizons_and_measure_at_horizon_zero():
    sel = {"kind": "trade", "where": [{"field": "side", "op": "==", "value": "long"}]}
    for kind in ("trade_gross_return", "trade_cost_share"):
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
