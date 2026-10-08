"""E-075 PR-3 (CUL-420): the trade-level claim-test family (tools/claim_tests.py).

On these TRADES (selector `trade {where: [...]}`), the trade's net return or the
market's move after its exit (outcomes trade_net_return, post_exit_return) is
different from the OTHER trades (baseline other_trades), as mean_diff or
hit_rate. A trade is one LIFO lot of trades.json. GATED: everything is refused
unless check_spec / check_claim / measure_variant get trade_tests=True, with
exactly the pre-PR-3 refusal, and nothing in the pipeline passes it yet.

Covers: the interim exit classifier (E-074 PHASE_A 4.2: flip, same-sign
reduction, to_zero, same_sign_flat, end_of_window ONLY at the window's last bar
and not on its last calendar day, unknown), hand-computed numbers on a
synthetic lot set (long and short, partial reductions sharing an entry bar,
flips, the window's last bar), the all-costs basis and its fallback, the
per-window values, check_spec / check_claim accept and refuse, lookahead
(rewriting every row after a trade's exit leaves its entry-time fields, and its
exit descriptors, unchanged; rewriting rows after exit + h leaves
post_exit_return(h) unchanged), the old spec hashes (real saved specs of
run_070/071/074, whose saved claim_check.yaml hashes these are) and flag-off
identity (the refusal messages, the unchanged block lists and CLAIM_TESTS.md, no
prompt wiring). Synthetic data only (2020 dates); no market data is read.
"""
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "tools"))

import claim_card as cc  # noqa: E402
import claim_measure as cm  # noqa: E402
import claim_tests as ct  # noqa: E402

T0 = 1577836800          # 2020-01-01 00:00 UTC (a Wednesday)
HOUR = 3600
GUIDE = SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design" / "CLAIM_TESTS.md"
TRADE_GUIDE = SR_ROOT / "workflow_artifacts" / "skills" / "hypothesis-design" / "CLAIM_TESTS_TRADE.md"
N = 30                   # bars 0..29: 2020-01-01 00:00 .. 2020-01-02 05:00; Jan 2 holds bars 24..29
CLOSE = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 111, 110, 112, 114, 113,
         115, 117, 116, 118, 120, 119, 121, 123, 122, 124, 126, 125, 127, 129, 128]
assert len(CLOSE) == N


def stamp(i, iso=True):
    t = np.datetime64(T0 + i * HOUR, "s").astype(str)          # 2020-01-01T00:00:00
    return t if iso else t.replace("T", " ")


def bars(close=None, forecast=None, regime=None, label="w0"):
    c = np.array(CLOSE if close is None else close, dtype=float)
    ts = T0 + np.arange(len(c), dtype=np.int64) * HOUR
    fc = np.arange(len(c), dtype=float) - 10.0 if forecast is None else np.asarray(forecast, float)
    rg = (np.array(["trending" if i % 2 else "chop" for i in range(len(c))], dtype=object)
          if regime is None else np.asarray(regime, dtype=object))
    return ct.Window("SYN", label, ts, c, fc, rg, HOUR)


def trade(tid, side, e, x, ef, net_pct, regime="trending", exit_time=None):
    return {"trade_id": tid, "side": side, "entry_time": stamp(e),
            "exit_time": exit_time or stamp(x), "exit_forecast": ef, "entry_regime": regime,
            "net_profit_loss_percent": net_pct}


# Hand-built lots (entry bar, exit bar, exit_forecast, post-exit allocation set below).
TRADES = [
    trade("t0", "LONG", 2, 5, -3.0, 1.0),                        # flip (bar 5)
    trade("t1", "LONG", 3, 5, -3.0, -0.5),                       # flip, same exit bar as t0
    trade("t2", "LONG", 3, 8, 2.0, 2.0),                         # reduction; shares entry bar 3 with t1
    trade("t3", "SHORT", 10, 12, 4.0, 3.0),                      # SHORT + positive forecast = flip
    trade("t4", "SHORT", 11, 15, -2.0, -1.0, regime="mean_reversion"),   # reduction (short stays short)
    trade("t5", "LONG", 16, 20, 0.0, 0.5),                       # to_zero
    trade("t6", "LONG", 17, 22, 5.0, 1.5),                       # same_sign_flat
    trade("t7", "LONG", 18, 29, -1.0, 4.0),                      # exit on the LAST bar -> end_of_window
    trade("t8", "LONG", 20, 26, 3.0, 2.5),                       # last calendar day, NOT last bar: reduction
    trade("t9", "LONG", 21, 27, -2.0, 2.0),                      # last calendar day, NOT last bar: flip
    trade("t10", "LONG", 4, 9, 2.0, 0.0, exit_time="2020-01-03T00:00:00"),   # exit bar not a row
    trade("t11", "LONG", 5, 13, None, 1.0),                      # no exit_forecast
]
POST = {8: 0.3, 15: -0.4, 22: 0.0, 26: 0.2, 13: 0.5}            # postRebalance_current_allocation by bar
FLIPS = {"t0", "t1", "t3", "t9"}
EXPECTED_CAUSE = ["flip", "flip", "reduction", "flip", "reduction", "to_zero", "same_sign_flat",
                  "end_of_window", "reduction", "flip", "unknown", "unknown"]


def post_alloc(overrides=None):
    a = np.full(N, 0.1)
    for i, v in {**POST, **(overrides or {})}.items():
        a[i] = v
    return a


def twin(w=None, trades=None, post=None, costs=None):
    return ct.build_trade_window(bars() if w is None else w, TRADES if trades is None else trades,
                                 post_alloc() if post is None else post, costs)


def spec(where, outcome=None, statistic="mean_diff", direction="greater", floor=None, **kw):
    return ct.TestSpec.from_dict({
        "selector": {"kind": "trade", "where": where},
        "outcome": outcome or {"kind": "trade_net_return"},
        "baseline": {"kind": "other_trades"}, "statistic": statistic,
        "direction": direction, "floor": floor or {"min_events": 1}, **kw})


def eq(field, value):
    return {"field": field, "op": "==", "value": value}


# ---------------------------------------------------------------------------
# 1. The interim exit classifier
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("side,ef,post,found,last,want", [
    (1, -3.0, 0.1, True, False, "flip"),                  # long, forecast turned negative
    (-1, 4.0, -0.1, True, False, "flip"),                 # short, forecast turned positive
    (1, 2.0, 0.3, True, False, "reduction"),              # long, still long after the bar
    (-1, -2.0, -0.4, True, False, "reduction"),           # short, still short after the bar
    (1, 0.0, 0.3, True, False, "to_zero"),                # forecast exactly 0
    (-1, 0.0, -0.3, True, False, "to_zero"),
    (1, 5.0, 0.0, True, False, "same_sign_flat"),         # same sign, flat after
    (-1, -5.0, 0.0, True, False, "same_sign_flat"),
    (1, 5.0, 4e-7, True, False, "same_sign_flat"),        # dust at the 6-decimal level is flat
    (1, -1.0, 0.1, True, True, "end_of_window"),          # the last bar wins, even over a flip
    (1, 3.0, 0.2, True, False, "reduction"),              # a last-CALENDAR-day bar that is not the last bar
    (1, None, 0.3, True, False, "unknown"),               # no exit_forecast
    (1, float("nan"), 0.3, True, False, "unknown"),
    (1, 2.0, None, True, False, "unknown"),               # no allocation after the bar
    (1, 2.0, float("nan"), True, False, "unknown"),
    (1, 2.0, -0.3, True, False, "unknown"),               # same-sign forecast but short after: odd
    (1, -3.0, 0.1, False, False, "unknown"),              # no exit row in bars.csv
    (1, -3.0, 0.1, False, True, "unknown"),
])
def test_classify_exit_cases(side, ef, post, found, last, want):
    assert ct.classify_exit(side, ef, post, found, last) == want


def test_classifier_on_the_lot_set_includes_last_day_but_not_last_bar():
    tw = twin()
    assert list(tw.exit_cause) == EXPECTED_CAUSE
    # bars 24..29 are 2020-01-02, the window's last calendar day. run_protocol's date test would
    # call every exit there end_of_window; only the exit ON bar 29 is.
    assert stamp(26)[:10] == stamp(29)[:10] == "2020-01-02"
    assert tw.exit_cause[8] == "reduction" and tw.exit_cause[9] == "flip"
    assert tw.exit_cause[7] == "end_of_window"
    assert list(tw.exit_idx[:3]) == [5, 5, 8] and tw.exit_idx[10] == -1


def test_classifier_last_bar_is_by_timestamp():
    w = bars(close=CLOSE[:27], forecast=np.arange(27) - 10.0)
    tw = ct.build_trade_window(w, [TRADES[8], TRADES[9]], post_alloc()[:27])
    assert tw.exit_cause[0] == "end_of_window"          # t8 exits on bar 26 = the last row now
    assert tw.exit_cause[1] == "unknown"                # t9's exit bar 27 is not a row


def test_unknown_side_fails_loud():
    bad = dict(TRADES[0], side="BOTH")
    with pytest.raises(ValueError, match="side"):
        ct.build_trade_window(bars(), [bad], post_alloc())


# ---------------------------------------------------------------------------
# 2. The loader fields
# ---------------------------------------------------------------------------

def test_fields_of_the_lot_set():
    tw = twin()
    assert tw.n == 12
    assert list(tw.side[:5]) == ["long", "long", "long", "short", "short"]
    # holding_bars = exit stamp - entry stamp, in bars
    hb, _ = ct._trade_field(tw, "holding_bars")
    assert list(hb[:9]) == [3, 2, 5, 2, 4, 4, 5, 11, 6]
    # entry_hour / entry_weekday from the entry stamp: bar 2 = 02:00 Wed (Mon=0 -> 2)
    h, _ = ct._trade_field(tw, "entry_hour")
    d, _ = ct._trade_field(tw, "entry_weekday")
    assert list(h[:3]) == [2, 3, 3] and h[8] == 20
    assert set(d) == {2}                      # every entry is on 2020-01-01, a Wednesday
    # entry_forecast = the entry bar's forecast (bar index - 10); regime from the trade
    ef, ok = ct._trade_field(tw, "entry_forecast")
    assert list(ef[:3]) == [-8.0, -7.0, -7.0] and ok.all()
    assert tw.regime_at_entry[0] == "trending"
    # the trade's own entry regime, not the bars' label at some other row (bar 15 says "trending")
    assert tw.regime_at_entry[4] == "mean_reversion" and bars().regime[15] == "trending"
    m, _ = ct.sel_trade(tw, {"where": [eq("regime_at_entry", "mean_reversion")]})
    assert list(np.nonzero(m)[0]) == [4]
    assert math.isclose(tw.net_return[0], 0.01) and tw.basis == "net_of_fees_and_slippage"


def test_all_costs_basis_when_every_lot_has_it_else_fallback():
    costs = [{"trade_id": t["trade_id"], "gross_return_before_costs": 2.0, "cost_paid_all": 30.0}
             for t in TRADES]
    tw = twin(costs=costs)
    # gross 2.0 % minus 30 bps (0.30 %) = 1.70 % = 0.017
    assert tw.basis == "all_costs" and np.allclose(tw.net_return, 0.017)
    partial = [dict(c) for c in costs]
    partial[3]["cost_paid_all"] = None                     # one lot lacks it -> the whole window falls back
    assert twin(costs=partial).basis == "net_of_fees_and_slippage"
    short = costs[:-1]                                     # not one-to-one -> fallback
    assert twin(costs=short).basis == "net_of_fees_and_slippage"
    wrong_ids = [dict(c, trade_id="x" + c["trade_id"]) for c in costs]
    assert twin(costs=wrong_ids).basis == "net_of_fees_and_slippage"
    assert math.isclose(twin(costs=short).net_return[0], 0.01)


# ---------------------------------------------------------------------------
# 3. Hand-computed numbers
# ---------------------------------------------------------------------------

def test_selector_where_is_an_and_and_missing_fields_leave_both_groups():
    tw = twin()
    m, v = ct.sel_trade(tw, {"where": [eq("exit_cause", "flip")]})
    assert [i for i in range(12) if m[i]] == [0, 1, 3, 9] and v.all()
    m, v = ct.sel_trade(tw, {"where": [eq("exit_cause", "flip"), eq("side", "long")]})
    assert [i for i in range(12) if m[i]] == [0, 1, 9]
    m, v = ct.sel_trade(tw, {"where": [{"field": "holding_bars", "op": ">=", "value": 5}]})
    # holding bars: t2 5, t6 5, t7 11, t8 6, t9 6, t10 (exit stamp 2020-01-03) 68, t11 8
    assert list(np.nonzero(m)[0]) == [2, 6, 7, 8, 9, 10, 11]
    m, v = ct.sel_trade(tw, {"where": [{"field": "exit_cause", "op": "in",
                                        "value": ["to_zero", "same_sign_flat"]}]})
    assert list(np.nonzero(m)[0]) == [5, 6]
    m, v = ct.sel_trade(tw, {"where": [{"field": "exit_cause", "op": "!=", "value": "flip"}]})
    assert list(np.nonzero(m)[0]) == [2, 4, 5, 6, 7, 8, 10, 11]
    # a lot without an entry-bar row has no entry_forecast: neither selected nor in the baseline
    tw2 = twin(trades=[dict(TRADES[0], entry_time="2020-01-05T00:00:00")])
    m, v = ct.sel_trade(tw2, {"where": [{"field": "entry_forecast", "op": "<", "value": 0}]})
    assert not v[0] and not m[0]


def test_a_trade_with_a_missing_field_is_in_neither_group_by_hand():
    """where entry_forecast < 0: t0 (entry bar 2, forecast -8, net .01) is selected; t3 (bar 10,
    forecast 0, net .03) is the baseline; a lot entering outside the bars (net .5) has no
    entry_forecast and is in neither: mean_diff = .01 - .03."""
    ghost = dict(TRADES[1], trade_id="ghost", entry_time="2020-01-05T00:00:00", net_profit_loss_percent=50.0)
    tw = twin(trades=[TRADES[0], TRADES[3], ghost])
    _, out_h, _, _ = ct.effect_sizes([tw], spec([{"field": "entry_forecast", "op": "<", "value": 0}]))
    assert out_h[0]["value"] == pytest.approx(-0.02) and out_h[0]["n_events"] == 1


def test_mean_diff_trade_net_return_by_hand():
    """flips: t0 .01, t1 -.005, t3 .03, t9 .02 -> mean .01375.
    others: t2 .02, t4 -.01, t5 .005, t6 .015, t7 .04, t8 .025, t10 .0, t11 .01 -> sum .105 / 8 = .013125."""
    per, out_h, horizons, _ = ct.effect_sizes([twin()], spec([eq("exit_cause", "flip")]))
    assert horizons == [0]
    h = out_h[0]
    assert h["value"] == pytest.approx(0.01375 - 0.013125) and h["oriented"] == pytest.approx(0.000625)
    assert h["n_events"] == 4 and h["n_windows_with_events"] == 1
    assert h["per_window"] == {"SYN/w0": {"value": pytest.approx(0.000625),
                                          "oriented": pytest.approx(0.000625),
                                          "basis": "net_of_fees_and_slippage"}}
    assert h["bases"] == ["net_of_fees_and_slippage"]
    # direction less flips the oriented sign only
    _, out_l, _, _ = ct.effect_sizes([twin()], spec([eq("exit_cause", "flip")], direction="less"))
    assert out_l[0]["value"] == pytest.approx(0.000625) and out_l[0]["oriented"] == pytest.approx(-0.000625)


def test_hit_rate_trade_net_return_by_hand():
    """selected = shorts (t3 +3.0, t4 -1.0): 1 of 2 win = .5. others: wins are net > 0:
    t0 t2 t5 t6 t7 t8 t9 t11 win; t1 loses; t10 (net 0.0) is not > 0 -> 8 of 10 = .8."""
    _, out_h, _, _ = ct.effect_sizes([twin()], spec([eq("side", "short")], statistic="hit_rate"))
    assert out_h[0]["value"] == pytest.approx(0.5 - 0.8)
    assert out_h[0]["n_events"] == 2


def test_post_exit_return_by_hand_signed_by_side_and_nan_at_the_window_end():
    tw = twin()
    y2 = ct.trade_outcome(tw, "post_exit_return", 2)
    assert y2[0] == pytest.approx(CLOSE[7] / CLOSE[5] - 1)               # t0 long, exit 5: 108/104 - 1
    assert y2[0] == pytest.approx(0.038461538)
    assert y2[3] == pytest.approx(-(CLOSE[14] / CLOSE[12] - 1))          # t3 short, exit 12: -(113/112 - 1)
    assert y2[3] == pytest.approx(-0.008928571)
    assert y2[8] == pytest.approx(CLOSE[28] / CLOSE[26] - 1)             # t8 exit 26 -> bar 28
    assert y2[8] == pytest.approx(0.032)
    assert np.isnan(y2[7])                                               # t7 exits on the last bar: no future
    assert np.isnan(y2[10])                                              # exit bar is not a row
    assert np.isnan(ct.trade_outcome(tw, "post_exit_return", 4)[8])      # 26 + 4 = 30: no such bar
    # a mean_diff over flips vs the rest at h=2 (hand values for the four flips)
    # t1 exits at bar 5 too (same exit bar and side as t0): the same market move, the same value,
    # counted ONCE (review fix): the four flips are three events
    assert y2[1] == y2[0]
    flips = [0, 3, 9]
    _, out_h, horizons, _ = ct.effect_sizes([tw], spec([eq("exit_cause", "flip")],
                                                       {"kind": "post_exit_return", "horizons": [2]}))
    assert horizons == [2]
    sel = [y2[i] for i in flips]
    rest = [y2[i] for i in range(12) if i not in (0, 1, 3, 9) and np.isfinite(y2[i])]
    assert out_h[2]["value"] == pytest.approx(np.mean(sel) - np.mean(rest))
    assert out_h[2]["n_events"] == 3


def test_two_windows_give_per_window_values_and_pooled_numbers():
    w1 = twin()
    w2 = ct.build_trade_window(bars(label="w1"), TRADES[:4], post_alloc())
    _, out_h, _, _ = ct.effect_sizes([w1, w2], spec([eq("exit_cause", "flip")]))
    h = out_h[0]
    assert set(h["per_window"]) == {"SYN/w0", "SYN/w1"}
    # w1: flips t0 .01, t1 -.005, t3 .03 -> .0116667; others t2 .02 -> diff -.0083333
    assert h["per_window"]["SYN/w1"]["value"] == pytest.approx((0.01 - 0.005 + 0.03) / 3 - 0.02)
    # pooled: 7 flips (.01 -.005 .03 .02 | .01 -.005 .03) vs 9 others (8 from w0 = .105, plus t2 .02)
    sel = [0.01, -0.005, 0.03, 0.02, 0.01, -0.005, 0.03]
    oth = [0.02, -0.01, 0.005, 0.015, 0.04, 0.025, 0.0, 0.01, 0.02]
    assert h["value"] == pytest.approx(np.mean(sel) - np.mean(oth))
    assert h["n_events"] == 7 and h["n_windows_with_events"] == 2


def test_partial_reductions_that_overlap_are_one_stretch_in_the_block_count():
    """t0 [2,5], t1 [3,5] and t2 [3,8] overlap: one stretch of trades, not two entry bars."""
    sp = spec([{"field": "entry_hour", "op": "in", "value": [2, 3]}], floor={"min_blocks": 1})
    _, out_h, _, _ = ct.effect_sizes([twin()], sp)
    assert out_h[0]["n_events"] == 3                     # t0, t1, t2
    assert out_h[0]["n_blocks"] == 1                     # one overlapping stretch [2, 8]


def test_eras_split_by_entry_date_and_no_events_is_all_nan():
    eras = [{"era_id": "e1", "range": ["2020-01-01", "2020-12-31"]}]
    _, out_h, _, _ = ct.effect_sizes([twin()], spec([eq("exit_cause", "flip")]), eras)
    assert set(out_h[0]["per_era"]) == {"e1"} and out_h[0]["n_eras_with_events"] == 1
    _, none, _, _ = ct.effect_sizes([twin()], spec([eq("exit_cause", "same_sign_flat"),
                                                    eq("side", "short")]))
    assert none[0]["n_events"] == 0 and none[0]["value"] is None


def test_window_without_trades_is_measurable():
    empty = ct.build_trade_window(bars(), [], post_alloc())
    empty_w = ct.build_trade_window(bars(label="w1"), [], post_alloc())
    _, out_h, _, _ = ct.effect_sizes([empty_w, twin()], spec([eq("exit_cause", "flip")]))
    assert out_h[0]["per_window"]["SYN/w1"] == {"value": None, "oriented": None, "basis": None}
    assert out_h[0]["per_window"]["SYN/w0"]["value"] == pytest.approx(0.000625)
    assert out_h[0]["n_events"] == 4 and out_h[0]["n_windows_with_events"] == 1
    assert empty.n == 0


# ---------------------------------------------------------------------------
# 4. check_spec / check_claim: accept and refuse
# ---------------------------------------------------------------------------

GOOD_CLAIM_TEST = {
    "name": "flip_exits_pay",
    "selector": {"kind": "trade", "where": [eq("exit_cause", "flip")]},
    "outcome": {"kind": "trade_net_return"}, "baseline": {"kind": "other_trades"},
    "statistic": "mean_diff", "direction": "greater", "floor": {"min_events": 50}}


def claim(*tests, kind="conditional_behaviour"):
    return {"statement": "s", "kind": kind, "tests": list(tests), "pass_if": "p",
            "fail_if": "f", "rationale": "r"}


def test_check_spec_accepts_the_family_only_with_trade_tests():
    sp = spec([eq("exit_cause", "flip")])
    assert ct.check_spec(sp, trade_tests=True) == []
    assert ct.check_spec(spec([eq("side", "long")], {"kind": "post_exit_return", "horizons": [1, 6]},
                              statistic="hit_rate"), trade_tests=True) == []
    # default: exactly the pre-PR-3 refusals
    assert ct.check_spec(sp) == [
        "selector: unknown selector {'kind': 'trade', 'where': [{'field': 'exit_cause', 'op': '==', "
        "'value': 'flip'}]}; known: ['all', 'calendar', 'event', 'quantile', 'regime', 'regime_change']",
        "outcome: unknown {'kind': 'trade_net_return'}; known: ['fwd_max_drawdown', 'fwd_return', "
        "'fwd_volatility', 'trend_ends']",
        "baseline: unknown {'kind': 'other_trades'}; known: ['complement', 'other_selector', 'placebo']"]


def test_check_claim_accepts_and_refuses():
    ok = cc.check_claim(claim(GOOD_CLAIM_TEST), trade_tests=True)
    assert ok.errors == [] and ok.tests[0]["name"] == "flip_exits_pay"
    assert ok.tests[0]["verdict_possible"] is False and ok.tests[0]["reason"] == cc.TRADE_REASON
    assert ok.tests[0]["spec_hash"] == ct.spec_hash(ct.TestSpec.from_dict(
        {k: v for k, v in GOOD_CLAIM_TEST.items() if k != "name"}))
    off = cc.check_claim(claim(GOOD_CLAIM_TEST))
    assert off.errors and "unknown selector" in off.errors[0] and off.tests == []
    # check_claim's default argument is the old behaviour
    assert off.errors == cc.check_claim(claim(GOOD_CLAIM_TEST), trade_tests=False).errors


def _errs(**changes):
    t = json.loads(json.dumps(GOOD_CLAIM_TEST))
    t.update(changes)
    return cc.check_claim(claim(t), trade_tests=True).errors


@pytest.mark.parametrize("change,needle", [
    ({"selector": {"kind": "trade", "where": [eq("mae", 1.0)]}}, "not a trade field"),
    ({"selector": {"kind": "trade", "where": [eq("exit_forecast", 1.0)]}}, "not a trade field"),
    ({"selector": {"kind": "trade", "where": [eq("post_exit_return", 1.0)]}}, "not a trade field"),
    ({"selector": {"kind": "trade", "where": [{"field": "exit_cause", "op": ">", "value": "flip"}]}},
     "op for exit_cause"),
    ({"selector": {"kind": "trade", "where": [eq("exit_cause", "stop_loss")]}}, "not one of"),
    ({"selector": {"kind": "trade", "where": [eq("side", "LONG")]}}, "not one of"),
    ({"selector": {"kind": "trade", "where": [eq("entry_hour", 24)]}}, "0..23"),
    ({"selector": {"kind": "trade", "where": [eq("entry_weekday", 7)]}}, "0..6"),
    ({"selector": {"kind": "trade", "where": [eq("entry_hour", "9")]}}, "must be a number"),
    ({"selector": {"kind": "trade", "where": [{"field": "entry_hour", "op": "in", "value": []}]}},
     "non-empty list"),
    ({"selector": {"kind": "trade", "where": []}}, "1 to 4 clauses"),
    ({"selector": {"kind": "trade", "where": [eq("side", "long")] * 5}}, "1 to 4 clauses"),
    ({"selector": {"kind": "trade"}}, "exactly {kind: trade, where"),
    ({"selector": {"kind": "trade", "where": [eq("side", "long")], "bars": 3}}, "exactly {kind: trade, where"),
    ({"selector": {"kind": "trade", "where": [{"field": "side", "op": "==", "value": "long",
                                               "extra": 1}]}}, "exactly {field, op, value}"),
    ({"outcome": {"kind": "fwd_return", "horizons": [1]}}, "needs one of"),
    ({"outcome": {"kind": "trade_net_return", "horizons": [1]}}, "no horizons"),
    ({"outcome": {"kind": "post_exit_return"}}, "non-empty list"),
    ({"outcome": {"kind": "post_exit_return", "horizons": [0]}}, "ints >= 1"),
    ({"outcome": {"kind": "post_exit_return", "horizons": [1, 1]}}, "distinct"),
    ({"outcome": {"kind": "post_exit_return", "horizons": [1], "x": 1}}, "only `horizons`"),
    ({"baseline": {"kind": "complement"}}, "other_trades"),
    ({"baseline": None}, "other_trades"),
    ({"statistic": "rank_ic"}, "mean_diff"),
    ({"statistic": "decay_curve"}, "mean_diff"),
    ({"direction": "up"}, "direction"),
    ({"floor": {}}, "floor"),
])
def test_check_claim_refuses(change, needle):
    errs = _errs(**change)
    assert errs and any(needle in e for e in errs), errs


def test_trade_outcomes_and_baseline_need_the_trade_selector():
    bar_sel = ct.TestSpec.from_dict({
        "selector": {"kind": "all"}, "outcome": {"kind": "trade_net_return"},
        "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": "greater",
        "floor": {"min_events": 1}})
    assert "need a selector of kind 'trade'" in ct.check_spec(bar_sel, trade_tests=True)[0]
    bar_sel2 = ct.TestSpec.from_dict({
        "selector": {"kind": "all"}, "outcome": {"kind": "fwd_return", "horizons": [1]},
        "baseline": {"kind": "other_trades"}, "statistic": "mean_diff", "direction": "greater",
        "floor": {"min_events": 1}})
    assert "need a selector of kind 'trade'" in ct.check_spec(bar_sel2, trade_tests=True)[0]
    # a plain bar test is checked exactly as before when trade_tests is on
    plain = ct.TestSpec.from_dict({
        "selector": {"kind": "event", "field": "forecast", "op": ">=", "value": 12},
        "outcome": {"kind": "fwd_return", "horizons": [1]}, "baseline": {"kind": "complement"},
        "statistic": "mean_diff", "direction": "greater", "floor": {"min_events": 10}})
    assert ct.check_spec(plain, trade_tests=True) == ct.check_spec(plain) == []


def test_the_verdict_path_still_refuses_trade_specs():
    with pytest.raises(ValueError, match="invalid spec"):
        ct.run_test([bars()], spec([eq("exit_cause", "flip")]))


def test_spec_hash_of_a_trade_spec_is_stable_and_sensitive():
    a = spec([eq("exit_cause", "flip"), eq("side", "long")])
    b = ct.TestSpec.from_dict({"floor": {"min_events": 1}, "direction": "greater",
                               "statistic": "mean_diff", "baseline": {"kind": "other_trades"},
                               "outcome": {"kind": "trade_net_return"},
                               "selector": {"where": [{"value": "flip", "op": "==", "field": "exit_cause"},
                                                      {"value": "long", "op": "==", "field": "side"}],
                                            "kind": "trade"}})
    assert ct.spec_hash(a) == ct.spec_hash(b)                     # key order does not matter
    assert ct.spec_hash(a) != ct.spec_hash(spec([eq("exit_cause", "flip")]))
    c = spec([eq("exit_cause", "flip")], {"kind": "post_exit_return", "horizons": [6, 1]})
    d = spec([eq("exit_cause", "flip")], {"kind": "post_exit_return", "horizons": [1, 6]})
    assert ct.spec_hash(c) == ct.spec_hash(d)                     # horizons are sorted


# ---------------------------------------------------------------------------
# 5. Lookahead
# ---------------------------------------------------------------------------

def _rewrite_after(w, post, row):
    """A copy of the window and allocation with every row AFTER `row` rewritten
    (close, forecast, regime, allocation); timestamps unchanged."""
    close, fc, rg, pa = w.close.copy(), w.forecast.copy(), w.regime.copy(), post.copy()
    rng = np.random.default_rng(7)
    k = slice(row + 1, None)
    close[k] = rng.uniform(50, 500, len(close[k]))
    fc[k] = rng.uniform(-20, 20, len(fc[k]))
    rg[k] = "garbage"
    pa[k] = rng.uniform(-1, 1, len(pa[k]))
    return ct.Window(w.symbol, w.window, w.ts, close, fc, rg, w.step), pa


ENTRY_FIELDS = ("side", "entry_hour", "entry_weekday", "regime_at_entry", "entry_forecast")


@pytest.mark.parametrize("k", range(10))
def test_rewriting_every_row_after_a_trades_exit_leaves_its_fields_unchanged(k):
    w, pa = bars(), post_alloc()
    exit_row = int((ct._parse_ts([TRADES[k]["exit_time"]])[0] - T0) // HOUR)
    w2, pa2 = _rewrite_after(w, pa, exit_row)
    keep = [t for t in TRADES if t["trade_id"] == TRADES[k]["trade_id"]]      # other trades are dropped too
    a = ct.build_trade_window(w, TRADES, pa)
    b = ct.build_trade_window(w2, keep, pa2)
    i = 0                                                                     # the kept trade in b
    for f in ENTRY_FIELDS + ("exit_cause", "holding_bars"):
        va, _ = ct._trade_field(a, f)
        vb, _ = ct._trade_field(b, f)
        assert va[k] == vb[i] or (math.isnan(va[k]) and math.isnan(vb[i])), f
    assert a.net_return[k] == b.net_return[i]
    # and a selector on the entry-time fields picks the same trade
    where = [eq("side", TRADES[k]["side"].lower()), {"field": "entry_forecast", "op": "<=", "value": 100}]
    assert ct.sel_trade(a, {"where": where})[0][k] == ct.sel_trade(b, {"where": where})[0][i]


def test_the_check_is_not_vacuous_a_row_before_the_exit_does_change_the_fields():
    w, pa = bars(), post_alloc()
    # trade t2: entry 3, exit 8. Rewriting the EXIT row's allocation changes its cause; rewriting
    # the ENTRY row's forecast changes entry_forecast.
    a = ct.build_trade_window(w, TRADES, pa)
    pa_x = pa.copy()
    pa_x[8] = 0.0
    assert ct.build_trade_window(w, TRADES, pa_x).exit_cause[2] == "same_sign_flat" != a.exit_cause[2]
    fc = w.forecast.copy()
    fc[3] = 99.0
    w_e = ct.Window(w.symbol, w.window, w.ts, w.close, fc, w.regime, w.step)
    assert ct.build_trade_window(w_e, TRADES, pa).entry_forecast[2] == 99.0 != a.entry_forecast[2]


@pytest.mark.parametrize("h", [1, 2, 3, 5])
def test_rewriting_rows_after_exit_plus_h_leaves_post_exit_return_unchanged(h):
    w, pa = bars(), post_alloc()
    a = ct.build_trade_window(w, TRADES, pa)
    ya = ct.trade_outcome(a, "post_exit_return", h)
    checked = 0
    for k, t in enumerate(TRADES):
        e = a.exit_idx[k]
        if e < 0 or e + h >= N:
            continue
        w2, pa2 = _rewrite_after(w, pa, int(e) + h)
        b = ct.build_trade_window(w2, [t], pa2)
        assert ct.trade_outcome(b, "post_exit_return", h)[0] == ya[k], (k, h)
        # sensitivity: rewriting the row AT exit + h does change it
        c2 = w.close.copy()
        c2[e + h] *= 1.5
        wc = ct.Window(w.symbol, w.window, w.ts, c2, w.forecast, w.regime, w.step)
        assert ct.trade_outcome(ct.build_trade_window(wc, [t], pa), "post_exit_return", h)[0] != ya[k]
        checked += 1
    assert checked >= 8


def test_post_exit_return_is_timestamp_matched_inside_the_window():
    """A missing bar at exit + h gives NaN, not the next row (nothing is chained)."""
    keep = [i for i in range(N) if i != 7]
    ts = T0 + np.array(keep, dtype=np.int64) * HOUR
    w = ct.Window("SYN", "w0", ts, np.array([CLOSE[i] for i in keep], float),
                  np.zeros(len(keep)), np.array(["x"] * len(keep), dtype=object), HOUR)
    tw = ct.build_trade_window(w, [TRADES[0]], np.full(len(keep), 0.1))
    assert np.isnan(ct.trade_outcome(tw, "post_exit_return", 2)[0])      # exit 5, bar 7 is gone
    assert ct.trade_outcome(tw, "post_exit_return", 1)[0] == pytest.approx(106 / 104 - 1)


# ---------------------------------------------------------------------------
# 6. Old spec hashes and flag-off identity
# ---------------------------------------------------------------------------

# Real saved specs: runs 070, 071 and 074's hypothesis cards, whose saved claim_check.yaml
# carries exactly these hashes (read from the main checkout's strategy-research/runs/).
PINNED = [
    ("run_070 high_close_shock_reversion",
     {"baseline": {"kind": "complement"}, "consistency": {"min_same_sign": 3, "unit": "window"},
      "direction": "less", "floor": {"min_events": 50, "min_windows": 4},
      "outcome": {"horizons": [1, 2, 4, 6, 12], "kind": "fwd_return"},
      "selector": {"field": "close", "kind": "quantile", "lookback": 100, "q": 0.1, "side": "top"},
      "statistic": "decay_curve"},
     "c688b1863f8cb3ff4d3a3bb05e0c15d5b885d27a65d3b805ad1990263fa83a99"),
    ("run_070 low_close_shock_reversion",
     {"baseline": {"kind": "complement"}, "consistency": {"min_same_sign": 3, "unit": "window"},
      "direction": "greater", "floor": {"min_events": 50, "min_windows": 4},
      "outcome": {"horizons": [1, 2, 4, 6, 12], "kind": "fwd_return"},
      "selector": {"field": "close", "kind": "quantile", "lookback": 100, "q": 0.1, "side": "bottom"},
      "statistic": "decay_curve"},
     "859161e14578a12522d303685d6abad3614c0a94d27555c235ff660e2a850211"),
    ("run_071 continuation_by_conviction",
     {"baseline": {"kind": "complement"}, "consistency": {"min_same_sign": 3, "unit": "window"},
      "direction": "greater", "floor": {"min_events": 40, "min_windows": 3},
      "outcome": {"horizons": [1, 2, 3, 4], "kind": "fwd_return"},
      "selector": {"field": "forecast", "kind": "event", "op": ">=", "value": 12},
      "statistic": "mean_diff"},
     "75ac6399c191d394244e5d81c9dd08995c04a38a6da4717bbe406fdd09cd3a29"),
    ("run_074 shock_reversal_rank_ic",
     {"baseline": None, "direction": "greater", "floor": {"min_windows": 4},
      "outcome": {"horizons": [1, 2, 3, 4], "kind": "fwd_return"},
      "selector": {"kind": "all"}, "statistic": "rank_ic"},
     "f084b07ea82d1cae3caffbba2d318ea0c91c206bff5cc4578ebc6ead526d8521"),
]


@pytest.mark.parametrize("name,d,want", PINNED, ids=[p[0] for p in PINNED])
def test_old_spec_hashes_are_unchanged(name, d, want):
    sp = ct.TestSpec.from_dict(d)
    assert ct.spec_hash(sp) == want
    assert ct.check_spec(sp) == [] and ct.check_spec(sp, trade_tests=True) == []
    # and through the claim card, with and without the gate
    for gate in (False, True):
        res = cc.check_claim(claim(dict(d, name="t")), trade_tests=gate)
        assert res.errors == [] and res.tests[0]["spec_hash"] == want


def test_block_lists_and_the_old_guide_are_unchanged():
    assert sorted(ct.SELECTORS) == ["all", "calendar", "event", "quantile", "regime", "regime_change"]
    assert sorted(ct.OUTCOMES) == ["fwd_max_drawdown", "fwd_return", "fwd_volatility", "trend_ends"]
    assert sorted(ct.BASELINES) == ["complement", "other_selector", "placebo"]
    assert sorted(ct.STATISTICS) == ["decay_curve", "hit_rate", "mean_diff", "rank_ic"]
    assert ct.BAR_T_FIELDS == ("forecast", "close", "past_return")
    text = GUIDE.read_text(encoding="utf-8")
    for token in ("trade_net_return", "post_exit_return", "other_trades", "exit_cause",
                  "CLAIM_TESTS_TRADE"):
        assert token not in text, token


def test_no_prompt_or_stage_wires_the_trade_guide_or_the_trade_gate():
    """No prompt reads the new guide yet, and the pipeline passes trade_tests=True only
    under orchestrator.analyst.enabled (E-075 PR-5a, D-091; this test pinned "nowhere"
    before, changed deliberately there): every orchestrator literal sits in an
    `if _analyst_enabled()` conditional, and the flag is off by default."""
    import re as _re
    tools_allowed = ("claim_tests.py", "claim_card.py", "claim_measure.py", "analyst_queries.py",
                     # D-091: they take a trade_tests keyword, passed only under the flag
                     "reader_findings.py", "explore_confirm.py", "decide_next.py",
                     "fold_confirm.py")
    for rel in ("workflow", "tools"):
        for p in (SR_ROOT / rel).glob("*.py"):
            src = p.read_text(encoding="utf-8")
            if p.name != "claim_tests.py":            # its own header names the guide
                assert "CLAIM_TESTS_TRADE" not in src, p
            if rel == "tools" and p.name not in tools_allowed:
                assert "trade_tests" not in src, p
            if rel == "workflow" and p.name not in ("run_phase1_research.py", "run_campaign.py"):
                assert "trade_tests" not in src, p
            if rel == "workflow":
                code = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
                lits = _re.findall(r'\{"trade_tests": True\}( if \w*\.?_analyst_enabled\(\))?', code)
                in_doc = src.count('{"trade_tests": True}, so a claim may use the')
                assert sum(1 for g in lits if not g) == in_doc, p     # only a docstring mention
    cfg = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert cfg["orchestrator"]["analyst"]["enabled"] is False


def test_the_trade_guide_lists_exactly_the_engine_fields_causes_and_blocks():
    text = TRADE_GUIDE.read_text(encoding="utf-8")
    rows = set(re.findall(r"^\| `([a-z_]+)`", text, flags=re.M))
    fields = set(ct.TRADE_FIELDS)
    assert fields <= rows, sorted(fields - rows)
    for name in ct.TRADE_OUTCOMES + ct.TRADE_STATISTICS + ct.TRADE_BASELINES:
        assert f"`{name}`" in text, name
    # the ops the guide names are the ones the engine accepts
    for op in ct.TRADE_OPS:
        assert f"`{op}`" in text, op
    for cause in ct.EXIT_CAUSES:
        assert f"`{cause}`" in text, cause
    for name in ("trade", "other_trades"):
        assert f"`{name}`" in text
    assert set(ct.TRADE_ENTRY_FIELDS) | set(ct.TRADE_EXIT_FIELDS) == set(ct.TRADE_FIELDS)
    for f in ("mae", "mfe"):
        assert f not in ct.TRADE_FIELDS


def test_the_readers_data_dictionary_subset_is_unchanged_by_the_new_note():
    import data_dictionary as dd
    full = dd.FULL_DOC.read_text(encoding="utf-8")
    assert "Trade-level claim tests (E-075 PR-3" in full
    assert dd.reader_subset(full) == dd.READERS_DOC.read_text(encoding="utf-8")
    assert "E-075 PR-3" not in dd.READERS_DOC.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# 7. The loader and claim_measure, on a synthetic run directory
# ---------------------------------------------------------------------------

def _write_run(root: Path, trades=TRADES, diag=None, vid="base", with_trades_file=True):
    w = bars()
    pa = post_alloc()
    res = root / "variants" / vid / "results" / "RID1"
    res.mkdir(parents=True)
    lines = ["timestamp,open,high,low,close,forecast,regime,postRebalance_current_allocation"]
    for i in range(N):
        lines.append(f"{stamp(i, False)},{w.close[i]},{w.close[i]},{w.close[i]},{w.close[i]},"
                     f"{w.forecast[i]},{w.regime[i]},{pa[i]}")
    (res / "bars.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if with_trades_file:
        (res / "trades.json").write_text(json.dumps(trades), encoding="utf-8")
    art = root / "artifacts" / "variants" / vid
    art.mkdir(parents=True)
    (art / "protocol_result.yaml").write_text(yaml.safe_dump(
        {"results": [{"run_id": "RID1", "symbol": "SYN", "window": "w0"}]}), encoding="utf-8")
    if diag is not None:
        (root / "variants" / vid / "trade_diagnostics.json").write_text(
            json.dumps({"trades": diag}), encoding="utf-8")
    return root


def test_loader_reads_trades_bars_and_the_all_costs_basis(tmp_path):
    run = _write_run(tmp_path / "r1")
    [tw] = ct.load_variant_trade_windows(run, "base")
    assert tw.label == "SYN/w0" and tw.n == 12 and list(tw.exit_cause) == EXPECTED_CAUSE
    assert tw.basis == "net_of_fees_and_slippage" and tw.net_return[0] == pytest.approx(0.01)
    diag = [{"trade_id": t["trade_id"], "window": "w0", "gross_return_before_costs": 2.0,
             "cost_paid_all": 30.0} for t in TRADES]
    [tw2] = ct.load_variant_trade_windows(_write_run(tmp_path / "r2", diag=diag), "base")
    assert tw2.basis == "all_costs" and np.allclose(tw2.net_return, 0.017)
    # a diagnostics file for another window label is not used
    other = [dict(d, window="elsewhere") for d in diag]
    [tw3] = ct.load_variant_trade_windows(_write_run(tmp_path / "r3", diag=other), "base")
    assert tw3.basis == "net_of_fees_and_slippage"


def test_loader_fails_loud_when_trades_json_is_missing(tmp_path):
    run = _write_run(tmp_path / "r4", with_trades_file=False)
    with pytest.raises(FileNotFoundError, match="trades.json"):
        ct.load_variant_trade_windows(run, "base")


def test_claim_measure_measures_trade_tests_only_when_asked(tmp_path):
    run = _write_run(tmp_path / "r5")
    tests = [dict(GOOD_CLAIM_TEST, name="flip_net"),
             dict(GOOD_CLAIM_TEST, name="flip_post", outcome={"kind": "post_exit_return",
                                                              "horizons": [1, 2]}),
             {"name": "bar_all", "selector": {"kind": "all"},
              "outcome": {"kind": "fwd_return", "horizons": [1]}, "baseline": {"kind": "placebo"},
              "statistic": "mean_diff", "direction": "greater", "floor": {"min_events": 5}}]
    doc = cm.measure_variant(run, "base", tests, None, "2025-01-01", trade_tests=True)
    r = doc["tests"]
    assert r["flip_net"]["status"] == cm.MEASURED and r["flip_post"]["status"] == cm.MEASURED
    assert r["bar_all"]["status"] == cm.MEASURED
    h = r["flip_net"]["horizons"][0]
    assert h["value"] == pytest.approx(0.000625) and h["n_events"] == 4
    assert h["per_window"]["SYN/w0"]["oriented"] == pytest.approx(0.000625)
    assert h["windows_with_claimed_sign"] == 1 and h["windows_with_a_value"] == 1
    assert set(r["flip_post"]["horizons"]) == {1, 2}
    assert "selected trades" in r["flip_net"]["description"][0]
    assert r["flip_net"]["spec_hash"] == cm.test_spec(tests[0], True)[1]
    # default: the trade tests are not measurable (invalid), the bar test is unaffected
    off = cm.measure_variant(run, "base", tests, None, "2025-01-01")
    assert off["tests"]["flip_net"]["status"] == cm.NOT_MEASURED
    assert "unknown selector" in off["tests"]["flip_net"]["detail"]
    assert off["tests"]["bar_all"]["status"] == cm.MEASURED
    assert off["tests"]["bar_all"]["horizons"] == r["bar_all"]["horizons"]
    with pytest.raises(ValueError, match="unknown selector"):
        cm.test_spec(tests[0])


def test_claim_measure_reports_no_trades_and_a_missing_trades_file(tmp_path):
    run = _write_run(tmp_path / "r6")
    none = dict(GOOD_CLAIM_TEST, name="none",
                selector={"kind": "trade", "where": [eq("exit_cause", "flip"), eq("side", "short"),
                                                     eq("regime_at_entry", "nowhere")]})
    doc = cm.measure_variant(run, "base", [none], None, "2025-01-01", trade_tests=True)
    assert doc["tests"]["none"]["status"] == cm.NO_EVENTS
    assert doc["tests"]["none"]["reason"] == "the selector matched no trades"
    run2 = _write_run(tmp_path / "r7", with_trades_file=False)
    doc2 = cm.measure_variant(run2, "base", [GOOD_CLAIM_TEST], None, "2025-01-01", trade_tests=True)
    assert doc2["tests"][GOOD_CLAIM_TEST["name"]]["status"] == cm.NOT_MEASURED
    assert "trades.json" in doc2["tests"][GOOD_CLAIM_TEST["name"]]["detail"]


# ---------------------------------------------------------------------------
# 8. Review fixes (PR #352)
# ---------------------------------------------------------------------------

def test_this_pr_is_d086_and_decision_ids_are_unique():
    """Open PR #351 (E-077 PR-1) already uses D-085: this PR's row is D-086."""
    log = (SR_ROOT / "engineering" / "DECISION_LOG.md").read_text(encoding="utf-8")
    ids = re.findall(r"^\| (D-\d+) \|", log, flags=re.M)
    assert len(ids) == len(set(ids))
    rows = [ln for ln in log.splitlines() if ln.startswith("| D-086 |")]
    assert len(rows) == 1 and "trade-level claim-test family" in rows[0]
    assert "Numbered D-086" in rows[0] and "D-085" in rows[0]
    assert not [ln for ln in log.splitlines()
                if ln.startswith("| D-085 |") and "trade-level claim-test family" in ln]


def _flips_measure(trades, outcome=None, where=None, windows=None, floor=None):
    sp = spec(where or [eq("side", "long")], outcome, floor=floor or {"min_events": 1})
    return ct.effect_sizes(windows or [twin(trades=trades)], sp)[1]


# --- 2. n_blocks / n_events count independent samples

def test_trade_net_return_blocks_are_stretches_of_overlapping_trades():
    """t0..t9 minus none: [2,5] [3,5] [3,8] | [10,12] [11,15] | [16,20] [17,22] [18,29] [20,26]
    [21,27] -> 3 stretches (the old entry-bar count was 9 distinct entry bars)."""
    where = [{"field": "exit_cause", "op": "!=", "value": "unknown"}]
    out = _flips_measure(None, where=where)
    assert out[0]["n_events"] == 10 and out[0]["n_blocks"] == 3


def test_touching_trades_are_one_stretch_and_a_gap_of_one_bar_is_two():
    a = trade("a", "LONG", 2, 5, 2.0, 1.0)
    b = trade("b", "LONG", 5, 8, 2.0, 1.0)            # enters on a's exit stamp: overlap
    c = trade("c", "LONG", 9, 12, 2.0, 1.0)           # enters one bar after b's exit: a new stretch
    assert _flips_measure([a, b, c])[0]["n_blocks"] == 2
    assert _flips_measure([a, c])[0]["n_blocks"] == 2
    assert _flips_measure([a, b])[0]["n_blocks"] == 1
    # input order is irrelevant
    assert _flips_measure([c, b, a])[0]["n_blocks"] == 2
    # a long trade that contains two short ones is one stretch (the stretch ends at the LATEST exit)
    outer, inner1, inner2 = (trade("o", "LONG", 2, 10, 2.0, 1.0), trade("i1", "LONG", 3, 4, 2.0, 1.0),
                             trade("i2", "LONG", 6, 8, 2.0, 1.0))
    assert _flips_measure([outer, inner1, inner2])[0]["n_blocks"] == 1


def test_stretches_are_counted_per_window_and_summed():
    a, c = trade("a", "LONG", 2, 5, 2.0, 1.0), trade("c", "LONG", 9, 12, 2.0, 1.0)
    w0, w1 = twin(trades=[a, c]), ct.build_trade_window(bars(label="w1"), [a, c], post_alloc())
    out = _flips_measure(None, windows=[w0, w1])
    assert out[0]["n_blocks"] == 4 and out[0]["n_events"] == 4


def test_post_exit_blocks_are_counted_on_exit_bars():
    """t1 [3,5] and t2 [3,8] share an entry bar and exit on bars 5 and 8: two exit-bar blocks
    (the old entry-bar count gave one)."""
    out = _flips_measure(None, outcome={"kind": "post_exit_return", "horizons": [1]},
                         where=[eq("entry_hour", 3)])
    assert out[1]["n_events"] == 2 and out[1]["n_blocks"] == 2


def test_post_exit_lots_closing_on_one_bar_on_one_side_are_one_event():
    """t0 and t1 both close LONG on bar 5 (the same close-to-close move): selected, they are one event."""
    sel = [{"field": "entry_hour", "op": "in", "value": [2, 3]}]            # t0, t1, t2
    out = _flips_measure(None, outcome={"kind": "post_exit_return", "horizons": [1]}, where=sel)
    assert out[1]["n_events"] == 2                                          # bar 5 once, bar 8
    y = ct.trade_outcome(twin(), "post_exit_return", 1)
    assert y[0] == y[1]
    others = [y[i] for i in range(12) if i not in (0, 1, 2) and np.isfinite(y[i])]
    assert out[1]["value"] == pytest.approx(np.mean([y[0], y[2]]) - np.mean(others))


def test_post_exit_dedup_applies_inside_the_baseline_too_and_keeps_the_two_sides_apart():
    s_ = trade("S", "SHORT", 8, 12, 2.0, 1.0)
    l1, l2 = trade("L1", "LONG", 2, 5, 2.0, 1.0), trade("L2", "LONG", 3, 5, 2.0, 1.0)
    l3 = trade("L3", "LONG", 4, 8, 2.0, 1.0)
    out = _flips_measure([s_, l1, l2, l3], outcome={"kind": "post_exit_return", "horizons": [1]},
                         where=[eq("side", "short")])
    y5, y8 = CLOSE[6] / CLOSE[5] - 1, CLOSE[9] / CLOSE[8] - 1
    ys = -(CLOSE[13] / CLOSE[12] - 1)
    assert out[1]["value"] == pytest.approx(ys - (y5 + y8) / 2)            # not (2*y5 + y8) / 3
    # the same exit bar on the other side is a different value: both stay
    a = trade("a", "LONG", 2, 5, -3.0, 1.0)                                # flip, long
    b = trade("b", "SHORT", 3, 5, 3.0, 1.0)                                # flip, short
    out2 = _flips_measure([a, b], outcome={"kind": "post_exit_return", "horizons": [1]},
                          where=[eq("exit_cause", "flip")])
    assert out2[1]["n_events"] == 2
    # two windows are never merged
    w0, w1 = twin(trades=[a]), ct.build_trade_window(bars(label="w1"), [a], post_alloc())
    out3 = _flips_measure(None, outcome={"kind": "post_exit_return", "horizons": [1]},
                          where=[eq("exit_cause", "flip")], windows=[w0, w1])
    assert out3[1]["n_events"] == 2


def test_trade_net_return_keeps_every_lot_as_an_event():
    """Lots sharing an exit bar have their own net returns: no deduplication for trade_net_return."""
    out = _flips_measure(None, where=[eq("exit_cause", "flip")])
    assert out[0]["n_events"] == 4


# --- 3. spec_hash does not depend on clause order

def _hspec(where):
    return spec(where)


def test_spec_hash_ignores_the_order_of_where_clauses_and_in_lists():
    a, b = eq("side", "long"), eq("exit_cause", "flip")
    assert ct.spec_hash(_hspec([a, b])) == ct.spec_hash(_hspec([b, a]))
    c3 = {"field": "entry_hour", "op": "in", "value": [3, 4, 9]}
    c3b = {"field": "entry_hour", "op": "in", "value": [9, 3, 4]}
    assert ct.spec_hash(_hspec([c3])) == ct.spec_hash(_hspec([c3b]))
    d1 = {"field": "exit_cause", "op": "in", "value": ["to_zero", "flip"]}
    d2 = {"field": "exit_cause", "op": "in", "value": ["flip", "to_zero"]}
    assert ct.spec_hash(_hspec([a, d1, c3])) == ct.spec_hash(_hspec([c3b, d2, a]))
    # still sensitive to the content
    assert ct.spec_hash(_hspec([a, b])) != ct.spec_hash(_hspec([a, eq("exit_cause", "to_zero")]))
    assert ct.spec_hash(_hspec([c3])) != ct.spec_hash(_hspec([{"field": "entry_hour", "op": "in",
                                                                 "value": [3, 4, 10]}]))
    assert ct.spec_hash(_hspec([a])) != ct.spec_hash(_hspec([{"field": "side", "op": "!=", "value": "long"}]))
    # the hash through the claim card agrees
    t1 = dict(GOOD_CLAIM_TEST, selector={"kind": "trade", "where": [a, b]})
    t2 = dict(GOOD_CLAIM_TEST, selector={"kind": "trade", "where": [b, a]})
    r1, r2 = (cc.check_claim(claim(t), trade_tests=True) for t in (t1, t2))
    assert r1.errors == r2.errors == [] and r1.tests[0]["spec_hash"] == r2.tests[0]["spec_hash"]


def test_a_repeated_where_clause_is_refused():
    a = eq("side", "long")
    errs = ct.check_spec(_hspec([a, eq("exit_cause", "flip"), dict(a)]), trade_tests=True)
    assert len(errs) == 1 and "where[2]" in errs[0] and "repeats where[0]" in errs[0]
    d1 = {"field": "entry_hour", "op": "in", "value": [3, 4]}
    d2 = {"field": "entry_hour", "op": "in", "value": [4, 3]}       # the same clause, another order
    assert any("repeats" in e for e in ct.check_spec(_hspec([d1, d2]), trade_tests=True))
    # different value or op is not a repeat
    assert ct.check_spec(_hspec([a, eq("side", "short")]), trade_tests=True) == []
    assert ct.check_spec(_hspec([{"field": "entry_hour", "op": ">=", "value": 3},
                                 {"field": "entry_hour", "op": "<=", "value": 3}]), trade_tests=True) == []
    res = cc.check_claim(claim(dict(GOOD_CLAIM_TEST, selector={"kind": "trade", "where": [a, dict(a)]})),
                         trade_tests=True)
    assert res.errors and "repeats" in res.errors[0] and res.tests == []


# --- 4. a trade test has no verdict

def test_trade_tests_are_effect_size_only_and_bar_tests_are_unchanged():
    bar = {"name": "bar_ev", "selector": {"kind": "event", "field": "forecast", "op": ">=", "value": 12},
           "outcome": {"kind": "fwd_return", "horizons": [1]}, "baseline": {"kind": "complement"},
           "statistic": "mean_diff", "direction": "greater", "floor": {"min_events": 10}}
    res = cc.check_claim(claim(GOOD_CLAIM_TEST, bar), trade_tests=True)
    assert res.errors == []
    by = {t["name"]: t for t in res.tests}
    assert by["flip_exits_pay"]["verdict_possible"] is False
    assert by["flip_exits_pay"]["reason"] == cc.TRADE_REASON
    assert by["bar_ev"]["verdict_possible"] is True and "reason" not in by["bar_ev"]
    # nothing about a bar test changes with the gate off
    off = cc.check_claim(claim(bar))
    assert off.tests == [{"name": "bar_ev", "spec_hash": by["bar_ev"]["spec_hash"],
                          "verdict_possible": True}]
    # the pipeline's note for such a test is the "effect-size only" line
    src = (SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8")
    assert 'if not t["verdict_possible"]:' in src and "is effect-size only: {t['reason']}" in src


# --- 5. the return basis is recorded, and bases are not pooled

ALL_COSTS = [{"trade_id": t["trade_id"], "gross_return_before_costs": 2.0, "cost_paid_all": 30.0}
             for t in TRADES]


def test_basis_is_recorded_per_window_and_pooled():
    w0 = twin(costs=ALL_COSTS)
    w1 = ct.build_trade_window(bars(label="w1"), TRADES, post_alloc(), ALL_COSTS)
    out = _flips_measure(None, where=[eq("exit_cause", "flip")], windows=[w0, w1])
    assert out[0]["bases"] == ["all_costs"]
    assert {k: v["basis"] for k, v in out[0]["per_window"].items()} == {"SYN/w0": "all_costs",
                                                                       "SYN/w1": "all_costs"}
    out2 = _flips_measure(None, where=[eq("exit_cause", "flip")])
    assert out2[0]["bases"] == ["net_of_fees_and_slippage"]


def test_windows_with_different_bases_are_not_pooled():
    w0 = twin(costs=ALL_COSTS)                                              # all_costs
    w1 = ct.build_trade_window(bars(label="w1"), TRADES, post_alloc())      # fallback
    sp = spec([eq("exit_cause", "flip")])
    with pytest.raises(ct.MixedReturnBasis, match="all_costs.*net_of_fees_and_slippage"):
        ct.effect_sizes([w0, w1], sp)
    # through claim_measure: not_measured, with its own reason and the windows' bases
    res = cm.measure_test([w0, w1], dict(GOOD_CLAIM_TEST), None, True)
    assert res["status"] == cm.NOT_MEASURED and res["reason"] == cm.MIXED_BASES == "mixed_return_basis"
    assert "SYN/w0" in res["detail"] and "SYN/w1" in res["detail"] and "horizons" not in res
    # a window without trades has no basis and conflicts with nothing
    empty = ct.build_trade_window(bars(label="w2"), [], post_alloc())
    out = ct.effect_sizes([w0, empty], sp)[1]
    assert out[0]["bases"] == ["all_costs"] and out[0]["per_window"]["SYN/w2"]["basis"] is None
    # post_exit_return does not use the return basis: mixed windows are fine, nothing recorded
    pe = spec([eq("exit_cause", "flip")], {"kind": "post_exit_return", "horizons": [1]})
    out_pe = ct.effect_sizes([w0, w1], pe)[1]
    assert "bases" not in out_pe[1] and "basis" not in out_pe[1]["per_window"]["SYN/w0"]


def test_claim_measure_carries_the_basis_into_its_rows():
    res = cm.measure_test([twin(costs=ALL_COSTS)], dict(GOOD_CLAIM_TEST), None, True)
    assert res["status"] == cm.MEASURED
    assert res["horizons"][0]["bases"] == ["all_costs"]
    assert res["horizons"][0]["per_window"]["SYN/w0"]["basis"] == "all_costs"
