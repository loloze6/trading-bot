"""E-075 PR-4 (CUL-422, D-088): the analyst's query engine and memory view.

tools/analyst_queries.py -- six fixed functions over ONE saved run's own bars and
trades -- and tools/analyst_memory_view.py -- earlier claims with numbers for
confirmed ones only. Pure modules: nothing imports them, no flag, no SDK.

Covers: conditional_effect equals claim_tests.effect_sizes (and claim_measure's
measurement of the `test` block it returns) for every selector x outcome x
baseline x statistic the bar slots allow and for the trade family; by=window /
by=coin cells; the comparison counts; refusals (unknown / never-offered /
outcome-only / label columns, a variant or window id that would leave the run,
a run under local_data, the holdout start, the group / horizon / size caps, the
comparison budget) all LOGGED; the log entry is on disk before the result is
returned and survives a function that raises after logging; ids are sequential
across engines; no path under local_data is ever opened (open() patched);
event_study's before half cannot change with later bars; the data dictionary
parser; the memory view on a fixture shaped like run_074's memory (no exploratory
effect, no window count, numbers for a confirmed claim). Synthetic data only
(2020 dates); no market data, no model call.
"""
import ast
import builtins
import copy
import io
import itertools
import json
import re
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "tools"))

import analyst_memory_view as amv  # noqa: E402
import analyst_queries as aq  # noqa: E402
import claim_measure as cm  # noqa: E402
import claim_tests as ct  # noqa: E402

T0 = 1577836800            # 2020-01-01 00:00 UTC
HOUR = 3600
N = 130
HOLDOUT = "2021-01-01"
# (window run id, symbol, window label, start offset in hours, seed)
WINDOWS = [("R1", "AAA", "w0", 0, 11), ("R2", "AAA", "w1", 24 * 31, 12), ("R3", "BBB", "w0", 0, 13)]
HOLDS = [9, 3, 5, 7, 2, 4, 3, 5]       # hold 9 appears once per window
EXIT_FC = [-3.0, 2.0, 0.0, 4.0, -1.0, 3.0, -2.0, 5.0]


def stamp(t, iso=False):
    s = np.datetime64(int(t), "s").astype(str)
    return s if iso else s.replace("T", " ")


def make_closes():
    out = {}
    for _rid, sym, win, off, seed in WINDOWS:
        rng = np.random.default_rng(seed)
        out[(sym, win)] = 100.0 * np.exp(np.cumsum(0.004 * rng.standard_normal(N)))
    return out


def make_run(root: Path, closes=None, vid="base", trades=True, extra_results=None):
    """A synthetic run directory: 3 hourly windows (two coins), bars.csv with
    dictionary-named columns, trades.json with 8 lots a window."""
    closes = closes or make_closes()
    root = Path(root)
    results = []
    for rid, sym, win, off, seed in WINDOWS:
        rng = np.random.default_rng(seed + 100)
        c = closes[(sym, win)]
        ts = T0 + off * HOUR + np.arange(N) * HOUR
        fc = 6.0 * rng.standard_normal(N)
        regime = np.where(np.arange(N) % 3 == 0, "trending", "chop")
        post = np.zeros(N)
        tr = []
        for k, hold in enumerate(HOLDS):
            e, x = 5 + 15 * k, 5 + 15 * k + hold
            side = "LONG" if k % 2 == 0 else "SHORT"
            sign = 1 if side == "LONG" else -1
            ef = sign * EXIT_FC[k]
            post[x] = sign * 0.3
            tr.append({"trade_id": f"{rid}-{k}", "side": side, "entry_time": stamp(ts[e], True),
                       "exit_time": stamp(ts[x], True), "exit_forecast": ef,
                       "entry_regime": str(regime[e]),
                       "net_profit_loss_percent": float(rng.uniform(-2, 2))})
        res = root / "variants" / vid / "results" / rid
        res.mkdir(parents=True)
        cols = ("timestamp,open,high,low,close,volume,fear_greed,forecast,confidence,regime,"
                "total_portfolio_value,previous_allocation,allocation_change,approved_rebalance,"
                "postRebalance_current_allocation,balances.USDT.free,"
                "debug_info.components.c1.post_pipeline_value,debug_info.error,mystery_col")
        lines = [cols]
        for i in range(N):
            lines.append(",".join(str(v) for v in (
                stamp(ts[i]), c[i], c[i] * 1.002, c[i] * 0.998, c[i], 10 + (i % 7), 40 + (i % 5),
                fc[i], 0.0, regime[i], 1000 + i, 0.1 * (i % 3), 0.05 * ((i % 5) - 2),
                "True" if i % 2 else "False", post[i], 777.0, fc[i] / 2,
                "Strategy not ready" if i < 3 else "", 1.5)))
        (res / "bars.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
        if trades:
            (res / "trades.json").write_text(json.dumps(tr), encoding="utf-8")
        results.append({"run_id": rid, "symbol": sym, "window": win})
    art = root / "artifacts" / "variants" / vid
    art.mkdir(parents=True)
    (art / "protocol_result.yaml").write_text(
        yaml.safe_dump({"results": results + list(extra_results or [])}), encoding="utf-8")
    return root


@pytest.fixture()
def run(tmp_path):
    return make_run(tmp_path / "run_001")


def engine(run, tmp_path=None, **kw):
    kw.setdefault("holdout_start", HOLDOUT)
    kw.setdefault("comparison_budget", 10 ** 9)
    kw.setdefault("log_path", Path(run).parent / (Path(run).name + "_log.yaml"))
    return aq.QueryEngine(run, **kw)


def log_of(eng):
    return eng.log.entries()


# ---------------------------------------------------------------------------
# 1. The data dictionary: the closed vocabulary of columns
# ---------------------------------------------------------------------------

def test_the_dictionary_parses_and_assigns_roles():
    rows = aq.load_bars_dictionary()
    assert len(rows) > 40
    assert all(r["role"] == aq.ROLE_OF_WHEN[r["when"]] for r in rows)
    get = lambda c: aq.dictionary_row(rows, c)                                  # noqa: E731
    assert get("close")["role"] == "feature"
    assert get("postRebalance_current_allocation")["role"] == "feature"          # fill
    assert get("confidence")["role"] == "label"                                  # meta
    assert get("balances.USDT.free")["role"] == "never"                          # end (A1)
    assert get("debug_info.components.any_id.post_pipeline_value")["role"] == "feature"
    assert get("not_a_column") is None
    assert get("balances.USDT") is None                       # a placeholder does not match a prefix


# ---------------------------------------------------------------------------
# 2. conditional_effect == claim_tests.effect_sizes (== claim_measure.measure_test)
# ---------------------------------------------------------------------------

BAR_SELECTORS = [
    {"kind": "all"},
    {"kind": "event", "field": "forecast", "op": ">=", "value": 4.0},
    {"kind": "event", "field": "close", "op": "<=", "value": 100.0},
    {"kind": "event", "field": "past_return", "bars": 5, "op": "<=", "value": -0.002},
    {"kind": "event", "field": "trailing_vol", "bars": 6, "op": ">=", "value": 0.004},
    {"kind": "regime", "value": "trending"},
    {"kind": "regime_change", "to": "trending"},
    {"kind": "calendar", "hours": [3, 4, 5]},
    {"kind": "quantile", "field": "forecast", "side": "top", "q": 0.2, "lookback": 24},
    {"kind": "quantile", "field": "trailing_vol", "bars": 6, "side": "top", "q": 0.3,
     "lookback": 24},
]
OUTCOMES = {"fwd_return": [1, 3], "fwd_volatility": [2, 4], "fwd_max_drawdown": [1, 2],
            "trend_ends": [2, 3]}
BASELINES = [{"kind": "complement"}, {"kind": "placebo"},
             {"kind": "other_selector", "selector": {"kind": "calendar", "hours": [10, 11]}}]


def _bar_combos():
    for outcome, stat, base in itertools.product(OUTCOMES, ("mean_diff", "hit_rate", "decay_curve"),
                                                 BASELINES):
        yield outcome, stat, base
    for outcome in OUTCOMES:
        yield outcome, "rank_ic", None


def _same(res, windows, test, trade=False):
    """The engine's numbers are the claim engine's, to the 8 digits it prints."""
    assert res["status"] == "ok", res.get("reason")
    spec = ct.TestSpec.from_dict({k: v for k, v in test.items() if k != "name"})
    per, out_h, hz, _ = ct.effect_sizes(windows, spec)
    got = res["result"]
    assert got["spec_hash"] == ct.spec_hash(spec)
    assert set(got["horizons"]) == {("trade" if (trade and h == 0) else str(h)) for h in hz}
    for h in hz:
        c = got["horizons"]["trade" if (trade and h == 0) else str(h)]
        o = out_h[h]
        k, n = cm._claimed(o["per_window"].values())
        assert c["effect"] == aq.r8(o["value"])
        assert c["oriented"] == aq.r8(o["oriented"])
        assert c["n_events"] == o["n_events"]
        assert c["n_windows_with_events"] == o["n_windows_with_events"]
        assert c["n_blocks"] == o["n_blocks"]
        assert (c["windows_claimed_sign"], c["windows_with_value"]) == (k, n)
    return spec


def _measure_the_block(res, windows, spec, trade=False):
    """The `test` block the engine returns, measured by claim_measure, gives the same
    numbers (only for blocks claim_card accepts today: trailing_vol is gated)."""
    block = res["result"]["test"]
    if not res["result"]["compiles_as_claim"]:
        return False
    m = cm.measure_test(windows, block, None, trade_tests=trade)
    for h, row in m["horizons"].items():
        c = res["result"]["horizons"]["trade" if (trade and h == 0) else str(h)]
        assert c["effect"] == aq.r8(row["value"])
        assert c["n_events"] == row["n_events"]
    return True


@pytest.mark.parametrize("selector", BAR_SELECTORS, ids=lambda s: s["kind"] + str(s.get("field", "")))
def test_bar_conditional_effect_equals_effect_sizes_for_every_slot_combination(selector, run):
    eng = engine(run)
    windows = ct.load_variant_bars(run, "base")
    compiled = 0
    for outcome, stat, base in _bar_combos():
        test = {"selector": selector, "outcome": {"kind": outcome, "horizons": OUTCOMES[outcome]},
                "baseline": base, "statistic": stat, "direction": "greater",
                "floor": {"min_events": 1}}
        res = eng.conditional_effect(selector, OUTCOMES[outcome], outcome, base, stat, "greater")
        spec = _same(res, windows, test)
        compiled += _measure_the_block(res, windows, spec)
    gated = selector.get("field") == "trailing_vol"
    assert (compiled == 0) if gated else (compiled > 0)
    assert len(log_of(eng)) == len(list(_bar_combos()))


@pytest.mark.parametrize("direction", ["greater", "less"])
def test_the_direction_is_passed_through(direction, run):
    eng = engine(run)
    windows = ct.load_variant_bars(run, "base")
    sel = {"kind": "event", "field": "forecast", "op": ">=", "value": 2.0}
    test = {"selector": sel, "outcome": {"kind": "fwd_return", "horizons": [1, 2]},
            "baseline": {"kind": "complement"}, "statistic": "mean_diff", "direction": direction,
            "floor": {"min_events": 1}}
    _same(eng.conditional_effect(sel, [1, 2], direction=direction), windows, test)


TRADE_WHERES = [
    [{"field": "exit_cause", "op": "==", "value": "flip"}],
    [{"field": "side", "op": "==", "value": "long"}],
    [{"field": "holding_bars", "op": ">=", "value": 5}],
    [{"field": "entry_hour", "op": "in", "value": [5, 20, 35 % 24]}],
    [{"field": "entry_forecast", "op": ">", "value": 0}, {"field": "side", "op": "==", "value": "long"}],
    [{"field": "regime_at_entry", "op": "!=", "value": "chop"}],
    [{"field": "entry_weekday", "op": "<=", "value": 2}],
]


@pytest.mark.parametrize("where", TRADE_WHERES, ids=lambda w: w[0]["field"] + str(len(w)))
def test_trade_conditional_effect_equals_effect_sizes(where, run):
    eng = engine(run)
    twins = ct.load_variant_trade_windows(run, "base")
    sel = {"kind": "trade", "where": where}
    n_ok = 0
    for outcome, hz in (("trade_net_return", None), ("post_exit_return", [1, 3])):
        for stat, direction in itertools.product(("mean_diff", "hit_rate"), ("greater", "less")):
            o = {"kind": outcome} if hz is None else {"kind": outcome, "horizons": hz}
            test = {"selector": sel, "outcome": o, "baseline": {"kind": "other_trades"},
                    "statistic": stat, "direction": direction, "floor": {"min_events": 1}}
            res = eng.conditional_effect(sel, hz, outcome, None, stat, direction)
            spec = _same(res, twins, test, trade=True)
            assert res["result"]["unit"] == "trades"
            assert _measure_the_block(res, twins, spec, trade=True)
            n_ok += 1
    assert n_ok == 8


def test_by_window_and_by_coin_cells_are_the_engines(run):
    eng = engine(run)
    windows = ct.load_variant_bars(run, "base")
    sel = {"kind": "event", "field": "forecast", "op": ">=", "value": 3.0}
    spec = ct.TestSpec.from_dict({"selector": sel,
                                  "outcome": {"kind": "fwd_return", "horizons": [1, 2]},
                                  "baseline": {"kind": "complement"}, "statistic": "mean_diff",
                                  "direction": "greater", "floor": {"min_events": 1}})
    per, out_h, _hz, _ = ct.effect_sizes(windows, spec)
    res = eng.conditional_effect(sel, [1, 2], by="window")["result"]
    assert set(res["groups"]) == {"AAA/w0", "AAA/w1", "BBB/w0"}
    for lab, cells in res["groups"].items():
        for h in (1, 2):
            assert cells[str(h)]["effect"] == aq.r8(out_h[h]["per_window"][lab]["value"])
            p = next(p for p in per if p["w"].label == lab)
            assert cells[str(h)]["n_events"] == int((p["mask"] & np.isfinite(p["ys"][h])).sum())
    res = eng.conditional_effect(sel, [1, 2], by="coin")["result"]
    assert set(res["groups"]) == {"AAA", "BBB"}
    for sym, cells in res["groups"].items():
        for h in (1, 2):
            want = cm._per_coin(per, spec, h)[sym]
            assert cells[str(h)] == {"effect": aq.r8(want["value"]),
                                     "oriented": aq.r8(want["oriented"]),
                                     "n_events": want["n_events"]}
    # the trade family by window
    tsel = {"kind": "trade", "where": [{"field": "side", "op": "==", "value": "long"}]}
    res = eng.conditional_effect(tsel, by="window")["result"]
    assert set(res["groups"]) == {"AAA/w0", "AAA/w1", "BBB/w0"}
    assert set(res["groups"]["AAA/w0"]) == {"trade"}


def test_conditional_effect_default_slots(run):
    eng = engine(run)
    r = eng.conditional_effect({"kind": "all"}, [1])
    assert r["result"]["outcome"] == "fwd_return"
    assert r["result"]["test"]["baseline"] == {"kind": "complement"}
    r = eng.conditional_effect({"kind": "all"}, [1], statistic="rank_ic")
    assert r["status"] == "ok" and r["result"]["test"]["baseline"] is None
    r = eng.conditional_effect({"kind": "trade", "where": TRADE_WHERES[0]})
    assert r["result"]["test"]["baseline"] == {"kind": "other_trades"}
    assert r["result"]["test"]["outcome"] == {"kind": "trade_net_return"}


# ---------------------------------------------------------------------------
# 3. Comparisons are counted
# ---------------------------------------------------------------------------

def test_comparisons_are_counted_per_horizon_and_group(run):
    eng = engine(run)
    sel = {"kind": "event", "field": "forecast", "op": ">=", "value": 3.0}
    r = eng.conditional_effect(sel, [1, 2])
    assert (r["n_comparisons"], r["cumulative_comparisons"]) == (2, 2)
    r = eng.conditional_effect(sel, [1, 2, 3], by="window")          # 3 horizons x 3 windows
    assert (r["n_comparisons"], r["cumulative_comparisons"]) == (9, 11)
    r = eng.conditional_effect(sel, [1, 2], by="coin")               # 2 horizons x 2 coins
    assert (r["n_comparisons"], r["cumulative_comparisons"]) == (4, 15)
    assert eng.describe("close", by="window")["n_comparisons"] == 0
    assert eng.distribution("close")["n_comparisons"] == 0
    assert eng.list_columns()["n_comparisons"] == 0
    # trade_slice: groups x outcome aggregates that are not a count
    aggs = [{"field": "trade_net_return", "stat": "mean"},
            {"field": "post_exit_return", "stat": "share_positive", "h": 2},
            {"field": "trade_net_return", "stat": "count"},          # a count relates nothing
            {"field": "holding_bars", "stat": "median"}]            # not an outcome
    r = eng.trade_slice([], aggs, by="direction")                    # 2 groups x 2
    assert (r["n_comparisons"], r["cumulative_comparisons"]) == (4, 19)
    r = eng.trade_slice([], [{"field": "entry_forecast", "stat": "mean"}], by="window")
    assert r["n_comparisons"] == 0
    # event_study: the "after" checkpoints
    r = eng.event_study([], 6, 12)                                   # after: 1, 2, 3, 6, 12
    assert (r["n_comparisons"], r["cumulative_comparisons"]) == (5, 24)
    r = eng.event_study([], 24, 1)
    assert (r["n_comparisons"], r["cumulative_comparisons"]) == (1, 25)
    log = log_of(eng)
    assert [q["cumulative_comparisons"] for q in log if q["n_comparisons"]] == [2, 11, 15, 19, 24, 25]
    assert log[-1]["cumulative_comparisons"] == sum(q["n_comparisons"] for q in log)


def test_the_comparison_budget_refuses_outcome_calls_only(run):
    eng = engine(run, comparison_budget=3)
    sel = {"kind": "event", "field": "forecast", "op": ">=", "value": 3.0}
    assert eng.conditional_effect(sel, [1, 2])["status"] == "ok"        # 2 of 3
    r = eng.conditional_effect(sel, [1, 2])                             # would be 4 of 3
    assert r["status"] == "refused" and "comparison budget spent" in r["reason"]
    assert r["n_comparisons"] == 0 and r["cumulative_comparisons"] == 2
    assert eng.conditional_effect(sel, [1])["status"] == "ok"           # 3 of 3
    assert eng.conditional_effect(sel, [1])["status"] == "refused"
    assert eng.describe("close")["status"] == "ok"                      # features stay free
    assert eng.trade_slice([], [{"field": "holding_bars", "stat": "mean"}])["status"] == "ok"
    assert eng.event_study([], 3, 3)["status"] == "refused"             # needs 3 more


# ---------------------------------------------------------------------------
# 4. describe / distribution / trade_slice / event_study
# ---------------------------------------------------------------------------

def test_describe_matches_numpy_and_groups(run):
    eng = engine(run)
    windows = ct.load_variant_bars(run, "base")
    close = np.concatenate([w.close for w in windows])
    g = eng.describe("close")["result"]["groups"]["all"]
    assert g["n"] == len(close) and g["nan_share"] == 0.0
    assert g["mean"] == aq.r8(close.mean()) and g["std"] == aq.r8(close.std(ddof=1))
    assert g["p50"] == aq.r8(np.percentile(close, 50))
    by_w = eng.describe("close", by="window")["result"]["groups"]
    assert list(by_w) == ["AAA/w0", "AAA/w1", "BBB/w0"]
    assert by_w["AAA/w1"]["mean"] == aq.r8(windows[1].close.mean())
    assert set(eng.describe("close", by="coin")["result"]["groups"]) == {"AAA", "BBB"}
    assert set(eng.describe("close", by="regime")["result"]["groups"]) == {"trending", "chop"}
    assert list(eng.describe("close", by="weekday")["result"]["groups"]) == list(aq._WEEKDAYS)
    hrs = eng.describe("close", by="hour")["result"]["groups"]
    assert list(hrs) == ["00-03", "04-07", "08-11", "12-15", "16-19", "20-23"]
    # a column with NaNs (empty cells) reports its NaN share
    d = eng.describe("debug_info.error")
    assert d["status"] == "refused"                                      # no numeric value at all
    # booleans are numbers
    assert eng.describe("approved_rebalance")["result"]["groups"]["all"]["mean"] == 0.5


def test_derived_columns_are_the_claim_engines_fields(run):
    eng = engine(run)
    windows = ct.load_variant_bars(run, "base")
    pr = np.concatenate([ct.past_return(w, 5) for w in windows])
    g = eng.describe("past_return_5")["result"]["groups"]["all"]
    fin = pr[np.isfinite(pr)]
    assert g["n"] == len(pr) and g["mean"] == aq.r8(fin.mean())
    assert g["nan_share"] == aq.r8(1 - len(fin) / len(pr))
    assert eng.describe("trailing_vol_6")["status"] == "ok"
    for bad in ("past_return_0", "trailing_vol_1", "past_return_99999", "past_return_x"):
        assert eng.describe(bad)["status"] == "refused"


def test_distribution_counts_sum_to_the_finite_values(run):
    eng = engine(run)
    r = eng.distribution("forecast", by="coin", bins=8)["result"]
    assert len(r["bin_edges"]) == 9
    windows = ct.load_variant_bars(run, "base")
    n_aaa = sum(len(w.ts) for w in windows if w.symbol == "AAA")
    assert sum(r["groups"]["AAA"]) == n_aaa
    for bad in (1, 21, "10", True, None):
        assert eng.distribution("forecast", bins=bad)["status"] == "refused"


def test_trade_slice_hand_numbers(run):
    eng = engine(run)
    twins = ct.load_variant_trade_windows(run, "base")
    flt = [{"field": "exit_cause", "op": "==", "value": "flip"}]
    res = eng.trade_slice(flt, [{"field": "trade_net_return", "stat": "mean"},
                                {"field": "trade_net_return", "stat": "share_positive"},
                                {"field": "post_exit_return", "stat": "median", "h": 2},
                                {"field": "holding_bars", "stat": "count"}], by=None)["result"]
    sel = [t.exit_cause == "flip" for t in twins]
    net = np.concatenate([t.net_return[m] for t, m in zip(twins, sel)])
    pe = np.concatenate([ct.trade_outcome(t, "post_exit_return", 2)[m] for t, m in zip(twins, sel)])
    cell = res["groups"]["all"]
    assert cell["n_trades"] == int(net.size)
    assert cell["trade_net_return_mean"] == aq.r8(np.nanmean(net))
    assert cell["trade_net_return_share_positive"] == aq.r8((net[np.isfinite(net)] > 0).mean())
    assert cell["post_exit_return_h2_median"] == aq.r8(np.median(pe[np.isfinite(pe)]))
    assert cell["holding_bars_count"] == int(net.size)
    assert res["return_basis"] == ["net_of_fees_and_slippage"]
    by = eng.trade_slice([], [{"field": "trade_net_return", "stat": "count"}],
                         by="direction")["result"]["groups"]
    assert by["long"]["n_trades"] + by["short"]["n_trades"] == 3 * len(HOLDS)
    for b in ("regime_at_entry", "weekday", "hour", "window"):
        assert eng.trade_slice([], [{"field": "holding_bars", "stat": "mean"}], by=b)["status"] == "ok"


def _event_expected(run_closes, k_before, k_after, hold):
    """Independent numpy: the trades with this hold, signed by side, from the entry close."""
    before = {p: [] for p in (1, 2, 3, 6, 12, 24)}
    after = {p: [] for p in before}
    for _rid, sym, win, _off, _seed in WINDOWS:
        c = run_closes[(sym, win)]
        for k, h in enumerate(HOLDS):
            if h != hold:
                continue
            e, sign = 5 + 15 * k, (1 if k % 2 == 0 else -1)
            for p in before:
                if p <= k_before and e - p >= 0:
                    before[p].append(sign * (c[e] / c[e - p] - 1))
                if p <= k_after and e + p < N:
                    after[p].append(sign * (c[e + p] / c[e] - 1))
    return before, after


def test_event_study_hand_numbers_and_no_lookahead_in_the_before_half(tmp_path):
    closes = make_closes()
    a = make_run(tmp_path / "a", closes)
    flt = [{"field": "holding_bars", "op": "==", "value": 9}]
    res = engine(a).event_study(flt, 12, 6)
    assert res["n_comparisons"] == 4                                    # after: 1, 2, 3, 6
    out = res["result"]
    before, after = _event_expected(closes, 12, 6, 9)
    assert out["n_trades"] == 3
    mean = lambda v: aq.r8(np.mean(v)) if v else None                           # noqa: E731
    for p, vals in before.items():
        if p <= 12:
            assert out["before"][str(p)] == {"n": len(vals), "mean": mean(vals)}
    for p, vals in after.items():
        if p <= 6:
            assert out["after"][str(p)] == {"n": len(vals), "mean": mean(vals)}
    assert out["before"]["3"]["n"] == 3 and out["before"]["12"] == {"n": 0, "mean": None}
    assert set(out["before"]) == {"1", "2", "3", "6", "12"} and set(out["after"]) == {"1", "2", "3", "6"}
    assert "OUTCOME" in out["note"]
    # rewrite every close AFTER each entry bar: the before half cannot move, the after half does
    mutated = {key: c.copy() for key, c in closes.items()}
    for key, c in mutated.items():
        for k in range(len(HOLDS)):
            e = 5 + 15 * k
            c[e + 1:e + 16] *= 1.37
    b = make_run(tmp_path / "b", mutated)
    out2 = engine(b).event_study(flt, 12, 6)["result"]
    assert out2["before"] == out["before"]
    assert out2["after"] != out["after"]
    for bad in (0, 25, -1, "3", True):
        assert engine(a).event_study(flt, bad, 3)["status"] == "refused"
        assert engine(a).event_study(flt, 3, bad)["status"] == "refused"


def test_trade_filters_are_the_claim_engines(run):
    eng = engine(run)
    agg = [{"field": "holding_bars", "stat": "mean"}]
    # exit-time descriptors and entry-time fields only; nothing else
    for bad in ([{"field": "profitable_net", "op": "==", "value": True}],
                [{"field": "mae", "op": ">", "value": 0}],
                [{"field": "exit_cause", "op": "==", "value": "stop_loss"}],
                [{"field": "side", "op": "~", "value": "long"}],
                [{"field": "side", "op": "==", "value": "long"}] * 2,
                [{"field": "side", "op": "==", "value": "long"}] * 5, "side == long",
                [{"field": "entry_hour", "op": "==", "value": 99}]):
        assert eng.trade_slice(bad, agg)["status"] == "refused", bad
        assert eng.event_study(bad, 3, 3)["status"] == "refused", bad
    for bad in ([], [{"field": "mae", "stat": "mean"}], [{"field": "post_exit_return", "stat": "mean"}],
                [{"field": "holding_bars", "stat": "mean", "h": 2}],
                [{"field": "holding_bars", "stat": "p99"}], "x", [{"field": "holding_bars"}],
                [{"field": "holding_bars", "stat": "mean"}] * 5):
        assert eng.trade_slice([], bad)["status"] == "refused", bad


def test_list_columns_is_closed_and_fits_the_cap(run):
    r = engine(run).list_columns()
    assert r["status"] == "ok"
    out = r["result"]
    names = {c.split(" | ")[0] for c in out["bar_columns"]}
    assert {"close", "forecast", "volume", "debug_info.components.c1.post_pipeline_value"} <= names
    assert "balances.USDT.free" not in names and "confidence" not in names
    assert "mystery_col" in out["not_offered"]["not_in_dictionary"]
    assert "balances.USDT.free" in out["not_offered"]["never"]
    assert "confidence" in out["not_offered"]["label"]
    assert out["cadence"] == "hourly" and out["caps"]["groups"] == aq.MAX_GROUPS
    assert len(aq._canon_json(out)) <= aq.MAX_RESULT_CHARS
    assert set(out["trade_fields"]["exit_time"]) == {"exit_cause", "holding_bars"}


# ---------------------------------------------------------------------------
# 5. Refusals are logged
# ---------------------------------------------------------------------------

def _last(eng):
    return log_of(eng)[-1]


def test_every_kind_of_refusal_is_returned_and_logged(run, monkeypatch):
    eng = engine(run)
    refusals = [
        ("describe", dict(column="no_such_column"), "not a column"),
        ("describe", dict(column="mystery_col"), "not in the data dictionary"),
        ("describe", dict(column="balances.USDT.free"), "never offered"),
        ("describe", dict(column="confidence"), "label"),
        ("describe", dict(column="close", by="decade"), "by="),
        ("describe", dict(column=["close"]), "column"),
        ("describe", dict(column="close", variant="../other"), "not a variant"),
        ("describe", dict(column="close", variant="nope"), "not a graded variant"),
        ("distribution", dict(column="close", bins=1), "bins"),
        ("conditional_effect", dict(condition="all", horizons=[1]), "selector mapping"),
        ("conditional_effect", dict(condition={"kind": "event", "field": "volume", "op": ">",
                                              "value": 1}, horizons=[1]), "bar-t field"),
        ("conditional_effect", dict(condition={"kind": "event", "field": "forecast", "op": ">",
                                              "value": 1}, horizons=[1], outcome="fwd_close"),
         "outcome"),
        ("conditional_effect", dict(condition={"kind": "all"}, horizons=[0]), "horizons"),
        ("conditional_effect", dict(condition={"kind": "all"}, horizons=None), "horizons"),
        ("conditional_effect", dict(condition={"kind": "all"}, horizons=list(range(1, 8))),
         "cap"),
        ("conditional_effect", dict(condition={"kind": "all"}, horizons=[1], by="regime"), "by="),
        ("conditional_effect", dict(condition={"kind": "all"}, horizons=[1], statistic="sharpe"),
         "statistic"),
        ("conditional_effect", dict(condition={"kind": "trade", "where": [
            {"field": "mae", "op": ">", "value": 0}]}), "not a trade field"),
        ("conditional_effect", dict(condition={"kind": "all"}, horizons=[1],
                                    outcome="trade_net_return"), "trade"),
        ("conditional_effect", dict(condition={"kind": "all"}, horizons=[1],
                                    baseline={"kind": "other_trades"}), "baseline"),
        ("trade_slice", dict(filter=[], agg=[{"field": "mae", "stat": "mean"}]), "agg"),
        ("event_study", dict(trade_filter=[], bars_before=0, bars_after=1), "bars_before"),
    ]
    for i, (fn, kw, needle) in enumerate(refusals, 1):
        res = getattr(eng, fn)(**kw)
        assert res["status"] == "refused", (fn, kw, res)
        assert needle in res["reason"], (fn, res["reason"])
        assert res["n_comparisons"] == 0 and res["query_id"] == f"q{i}"
        entry = _last(eng)
        assert entry["id"] == f"q{i}" and entry["status"] == "refused"
        assert entry["function"] == fn and entry["reason"] == res["reason"]
        assert entry["n_comparisons"] == 0 and "result" not in entry
    assert len(log_of(eng)) == len(refusals)
    assert log_of(eng)[-1]["cumulative_comparisons"] == 0


def test_an_outcome_only_column_is_refused(run):
    eng = engine(run)
    eng._dictionary = [dict(r, when="after", role="outcome") if r["field"] == "volume" else r
                       for r in aq.load_bars_dictionary()]
    res = eng.describe("volume")
    assert res["status"] == "refused" and "outcome-only" in res["reason"]
    assert eng.describe("close")["status"] == "ok"


def test_a_window_id_that_leaves_the_run_is_refused_and_logged(tmp_path):
    root = make_run(tmp_path / "run_x", extra_results=[
        {"run_id": "../../outside", "symbol": "AAA", "window": "w9"}])
    eng = engine(root)
    res = eng.describe("close")
    assert res["status"] == "refused" and "not a plain name" in res["reason"]
    assert _last(eng)["status"] == "refused"
    for i, rid in enumerate(("..", "a/b", "a\\b", "/abs", "C:\\x", ".hidden/..")):
        root = make_run(tmp_path / f"run_{i}", extra_results=[
            {"run_id": rid, "symbol": "AAA", "window": "w9"}])
        assert engine(root).describe("close")["status"] == "refused", rid


def test_a_run_under_local_data_or_the_sealed_store_is_refused(tmp_path):
    for part in ("local_data", "holdout_sealed"):
        root = make_run(tmp_path / part / "run_1")
        with pytest.raises(ValueError, match=part):
            aq.QueryEngine(root, holdout_start=HOLDOUT)
    with pytest.raises(ValueError, match="does not exist"):
        aq.QueryEngine(tmp_path / "missing")


def test_a_bar_at_or_after_the_holdout_start_is_refused(run):
    eng = engine(run, holdout_start="2020-01-05")
    res = eng.conditional_effect({"kind": "all"}, [1])
    assert res["status"] == "refused" and "holdout" in res["reason"]
    assert eng.list_columns()["status"] == "refused"
    assert engine(run, holdout_start="2020-03-01").describe("close")["status"] == "ok"


def test_an_unreadable_holdout_policy_refuses_every_data_call(run, monkeypatch):
    import holdout_policy as hp

    def boom(*a, **k):
        raise hp.HoldoutPolicyError("no policy")
    monkeypatch.setattr(hp, "load_holdout_range", boom)
    eng = aq.QueryEngine(run, log_path=run.parent / "l.yaml")
    res = eng.describe("close")
    assert res["status"] == "refused" and "holdout start" in res["reason"]


def test_the_default_holdout_start_comes_from_the_policy(run):
    eng = aq.QueryEngine(run, log_path=run.parent / "p.yaml")
    assert eng.describe("close")["status"] == "ok"
    assert eng._holdout_start and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", eng._holdout_start)


def test_missing_trades_is_a_logged_refusal_not_a_crash(tmp_path):
    root = make_run(tmp_path / "notrades", trades=False)
    eng = engine(root)
    assert eng.describe("close")["status"] == "ok"
    res = eng.trade_slice([], [{"field": "holding_bars", "stat": "mean"}])
    assert res["status"] == "refused" and "trades cannot be read" in res["reason"]


def test_caps_on_groups_horizons_and_size_refuse_and_log(run, monkeypatch):
    eng = engine(run)
    monkeypatch.setattr(aq, "MAX_GROUPS", 2)
    for call in (lambda: eng.describe("close", by="window"),
                 lambda: eng.distribution("close", by="window"),
                 lambda: eng.conditional_effect({"kind": "all"}, [1], by="window"),
                 lambda: eng.trade_slice([], [{"field": "holding_bars", "stat": "mean"}],
                                         by="window")):
        res = call()
        assert res["status"] == "refused" and "cap of 2" in res["reason"]
    assert eng.describe("close", by="coin")["status"] == "ok"             # 2 groups fit
    monkeypatch.setattr(aq, "MAX_GROUPS", 12)
    monkeypatch.setattr(aq, "MAX_HORIZONS", 2)
    res = eng.conditional_effect({"kind": "all"}, [1, 2, 3])
    assert res["status"] == "refused" and "cap of 2" in res["reason"]
    monkeypatch.setattr(aq, "MAX_HORIZONS", 6)
    n = len(log_of(eng))
    monkeypatch.setattr(aq, "MAX_RESULT_CHARS", 150)
    res = eng.describe("close", by="window")
    assert res["status"] == "refused" and "over the 150 cap" in res["reason"]
    assert res["n_comparisons"] == 0
    assert len(log_of(eng)) == n + 1 and _last(eng)["status"] == "refused"
    # an oversized outcome result counts nothing
    res = eng.conditional_effect({"kind": "all"}, [1, 2, 3], by="window")
    assert res["status"] == "refused" and res["cumulative_comparisons"] == 0


def test_a_group_label_of_the_hour_split_is_a_four_hour_bucket_and_daily_runs_refuse_it(tmp_path):
    root = make_run(tmp_path / "ok")
    assert engine(root).describe("close", by="hour")["status"] == "ok"
    # a daily run: re-stamp the bars one day apart
    d = tmp_path / "daily"
    make_run(d)
    for p in (d / "variants" / "base" / "results").glob("*/bars.csv"):
        lines = p.read_text(encoding="utf-8").splitlines()
        out = [lines[0]]
        for i, ln in enumerate(lines[1:]):
            _ts, rest = ln.split(",", 1)
            out.append(f"{stamp(T0 + i * 86400)},{rest}")
        p.write_text("\n".join(out) + "\n", encoding="utf-8")
    for p in (d / "variants" / "base" / "results").glob("*/trades.json"):
        p.unlink()
        (p.parent / "trades.json").write_text("[]", encoding="utf-8")
    eng = engine(d)
    res = eng.describe("close", by="hour")
    assert res["status"] == "refused" and "hourly" in res["reason"]
    assert eng.describe("close", by="weekday")["status"] == "ok"


# ---------------------------------------------------------------------------
# 6. The log: written BEFORE the result is returned
# ---------------------------------------------------------------------------

def test_the_log_entry_exists_before_the_result_is_built(run, monkeypatch):
    eng = engine(run)
    seen = {}
    real = aq.QueryEngine._package

    def spy(self, logged, result):
        # the last step before returning: the entry must already be in the file
        on_disk = aq.QueryLog(self.log.path).entries()
        seen["ids"] = [q["id"] for q in on_disk]
        seen["logged"] = logged["id"]
        return real(self, logged, result)
    monkeypatch.setattr(aq.QueryEngine, "_package", spy)
    res = eng.describe("close")
    assert seen["ids"] == ["q1"] and seen["logged"] == "q1" and res["query_id"] == "q1"
    eng.conditional_effect({"kind": "all"}, [1])
    assert seen["ids"] == ["q1", "q2"]
    eng.describe("nope")                                   # a refusal is logged first too
    assert seen["ids"] == ["q1", "q2", "q3"]


def test_a_function_that_raises_after_logging_still_leaves_the_entry(run, monkeypatch):
    eng = engine(run)
    real = aq.QueryLog.append

    def append_then_die(self, entry):
        out = real(self, entry)
        raise RuntimeError("died right after the log write")
    monkeypatch.setattr(aq.QueryLog, "append", append_then_die)
    with pytest.raises(RuntimeError, match="died right after"):
        eng.conditional_effect({"kind": "all"}, [1, 2])
    monkeypatch.setattr(aq.QueryLog, "append", real)
    entries = aq.QueryLog(eng.log.path).entries()
    assert [q["id"] for q in entries] == ["q1"]
    assert entries[0]["status"] == "ok" and entries[0]["n_comparisons"] == 2
    assert entries[0]["function"] == "conditional_effect"
    assert entries[0]["params"]["horizons"] == [1, 2]


def test_an_unexpected_error_is_logged_and_raised(run, monkeypatch):
    eng = engine(run)

    def broken(self, *a, **k):
        raise ZeroDivisionError("boom")
    monkeypatch.setattr(aq.QueryEngine, "_describe", broken)
    with pytest.raises(ZeroDivisionError):
        eng.describe("close")
    e = _last(eng)
    assert e["status"] == "error" and "ZeroDivisionError: boom" in e["reason"]
    assert e["n_comparisons"] == 0


def test_the_entry_carries_params_digest_result_and_hash(run):
    eng = engine(run)
    sel = {"kind": "event", "field": "forecast", "op": ">=", "value": 3.0}
    res = eng.conditional_effect(sel, [2, 1])
    e = _last(eng)
    assert e["params"]["condition"] == sel and e["params"]["horizons"] == [2, 1]
    assert e["status"] == "ok" and e["result"] == res["result"]
    assert re.fullmatch(r"[0-9a-f]{64}", e["result_sha256"])
    assert e["result_sha256"] == __import__("hashlib").sha256(
        aq._canon_json(res["result"]).encode()).hexdigest()
    assert e["digest"] and len(e["digest"]) < 200
    assert e["n_comparisons"] == 2 and e["cumulative_comparisons"] == 2
    doc = yaml.safe_load(eng.log.path.read_text(encoding="utf-8"))
    assert doc["schema_version"] == 1 and doc["queries"][0]["id"] == "q1"


def test_ids_and_the_running_total_continue_across_engines(run):
    log = run.parent / "shared.yaml"
    a = aq.QueryEngine(run, log_path=log, holdout_start=HOLDOUT, comparison_budget=5)
    a.conditional_effect({"kind": "all"}, [1, 2, 3])
    b = aq.QueryEngine(run, log_path=log, holdout_start=HOLDOUT, comparison_budget=5)
    r = b.describe("close")
    assert r["query_id"] == "q2" and r["cumulative_comparisons"] == 3
    assert b.conditional_effect({"kind": "all"}, [1, 2, 3])["status"] == "refused"   # 3 + 3 > 5
    assert b.conditional_effect({"kind": "all"}, [1, 2])["cumulative_comparisons"] == 5


def test_the_default_log_is_in_the_run_artifacts(tmp_path):
    root = make_run(tmp_path / "r")
    eng = aq.QueryEngine(root, holdout_start=HOLDOUT)
    eng.describe("close")
    assert (root / "artifacts" / "analyst_queries.yaml").exists()
    assert aq.LOG_REL == "artifacts/analyst_queries.yaml"


def test_unserialisable_parameters_are_refused_and_logged(run):
    eng = engine(run)
    res = eng.conditional_effect({"kind": "all", "x": object()}, [1])
    assert res["status"] == "refused" and "plain JSON" in res["reason"]
    assert _last(eng)["status"] == "refused"


# ---------------------------------------------------------------------------
# 7. What the tools can read
# ---------------------------------------------------------------------------

@pytest.fixture()
def open_spy(monkeypatch):
    opened = []
    real_open, real_io_open = builtins.open, io.open

    def watch(real):
        def wrapped(file, *a, **k):
            if isinstance(file, (str, bytes, Path)) or hasattr(file, "__fspath__"):
                name = str(file)
                opened.append(name)
                if "local_data" in name.replace("\\", "/").split("/") or "holdout_sealed" in name:
                    raise AssertionError(f"a protected path was opened: {name}")
            return real(file, *a, **k)
        return wrapped
    monkeypatch.setattr(builtins, "open", watch(real_open))
    monkeypatch.setattr(io, "open", watch(real_io_open))
    return opened


def test_the_cache_and_sealed_stores_are_never_opened(run, open_spy):
    eng = aq.QueryEngine(run, log_path=run.parent / "spy.yaml")     # the holdout start from the policy
    sel = {"kind": "event", "field": "forecast", "op": ">=", "value": 3.0}
    calls = [eng.list_columns(), eng.describe("close", by="window"), eng.distribution("volume"),
             eng.conditional_effect(sel, [1, 2], by="coin"),
             eng.conditional_effect({"kind": "trade", "where": TRADE_WHERES[0]}),
             eng.trade_slice([], [{"field": "trade_net_return", "stat": "mean"}], by="direction"),
             eng.event_study([], 6, 6)]
    assert [c["status"] for c in calls] == ["ok"] * 7
    assert open_spy
    root = str(run.resolve()).lower()
    allowed = (root, str(Path(run.parent).resolve()).lower(),
               str((SR_ROOT / "docs").resolve()).lower(),
               str((SR_ROOT / "config").resolve()).lower())
    data_files = [n for n in open_spy if n.lower().endswith((".csv", ".json", ".yaml", ".md"))]
    assert any(n.endswith("bars.csv") for n in data_files)
    assert any(n.endswith("trades.json") for n in data_files)
    for name in data_files:
        low = str(Path(name).resolve()).lower()
        assert any(low.startswith(a) for a in allowed), name
    for name in open_spy:                   # claim_tests gets no cache: no warm-up file exists
        assert "local_data" not in name and "holdout_sealed" not in name


def test_the_loader_gets_no_cache_resolver(run, monkeypatch):
    seen = []
    real = ct.load_variant_bars

    def spy(run_dir, vid, cache_path_for=None):
        seen.append(cache_path_for)
        return real(run_dir, vid, cache_path_for)
    monkeypatch.setattr(ct, "load_variant_bars", spy)
    engine(run).describe("close")
    assert seen == [None]


def test_the_module_imports_no_sdk_and_nothing_imports_it():
    src = (SR_ROOT / "tools" / "analyst_queries.py").read_text(encoding="utf-8")
    src2 = (SR_ROOT / "tools" / "analyst_memory_view.py").read_text(encoding="utf-8")
    for text in (src, src2):
        assert not re.search(r"^\s*(import|from)\s+(claude_agent_sdk|anthropic|google\.genai)",
                             text, re.M)
        assert "os.environ" not in text and "subprocess" not in text
    users = []
    for p in list((SR_ROOT / "tools").glob("*.py")) + list((SR_ROOT / "workflow").glob("*.py")):
        if p.name in ("analyst_queries.py", "analyst_memory_view.py"):
            continue
        if re.search(r"analyst_queries|analyst_memory_view", p.read_text(encoding="utf-8")):
            users.append(p.name)
    # E-075 PR-5 (D-092) wires them (this pinned "nothing yet" before, changed deliberately):
    # analyst_session names the log directory; the orchestrator imports both modules only
    # inside their lazy loaders, which only the analyst stage (its flag) calls
    assert sorted(users) == ["analyst_session.py", "run_phase1_research.py"]
    tree = ast.parse((SR_ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8"))
    loaders = {}
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef):
            for n in ast.walk(fn):
                if isinstance(n, ast.Import) and n.names[0].name in ("analyst_queries",
                                                                     "analyst_memory_view"):
                    loaders[n.names[0].name] = fn.name
    assert loaders == {"analyst_queries": "_analyst_queries_module",
                       "analyst_memory_view": "_analyst_memory_view_module"}
    top = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    assert not any(a.name.startswith("analyst_") for n in top for a in n.names)


def test_the_modules_name_no_sealed_date():
    for name in ("analyst_queries.py", "analyst_memory_view.py"):
        text = (SR_ROOT / "tools" / name).read_text(encoding="utf-8")
        assert not re.search(r"2026-0[1-6]", text)


# ---------------------------------------------------------------------------
# 8. The memory view
# ---------------------------------------------------------------------------

RUN074_STATEMENT = ("The shock_reversal forecast at period=2 predicts zero forward returns "
                    "(median forecast_return_corr=-0.0057, not significant), indicating "
                    "smoothing reduces oscillation but cannot create an edge from a noisy signal.")


def _run074_memory():
    horizons = {str(h): {"effect": 0.0542876 + h / 1e4, "n_events": 17512 - h,
                         "windows_claimed_sign": 6, "windows_with_value": 6} for h in (1, 2, 3, 4)}
    test = {"name": "shock_reversal_rank_ic",
            "spec_hash": "f084b07ea82d1cae3caffbba2d318ea0c91c206bff5cc4578ebc6ead526d8521",
            "statistic": "rank_ic", "direction": "greater", "outcome": "fwd_return",
            "horizons": horizons, "effect": 0.0542876,            # decoys: results on the test row
            "spec": {"selector": {"kind": "all"},
                     "outcome": {"kind": "fwd_return", "horizons": [1, 2, 3, 4]},
                     "baseline": None, "statistic": "rank_ic", "direction": "greater",
                     "floor": {"min_windows": 4}}}
    finding = {
        "finding_id": "F-run_074-1", "label": "measured, not proven", "status": "measured",
        "reason": None, "statement": RUN074_STATEMENT, "kind": "direction_forecast",
        "tests": [test], "scope": {"timeframe": "1h"},
        "result": {"per_variant": {"base": {"status": "measured", "tests": {
            "shock_reversal_rank_ic": {"status": "measured", "horizons": horizons}}}}}}
    return {"runs": {
        "run_074": {"run_id": "run_074", "finding": finding},
        "run_073": {"run_id": "run_073", "fold": "A", "finding": {
            "finding_id": "F-run_073-1", "status": "measured", "kind": "event_behaviour",
            "statement": "After a 3% fall in 24 hours the next 24 hours return 0.4% more.",
            "tests": [], "result": {}}},
        "run_070": {"run_id": "run_070"}}}                       # no finding: not a claim


def _fold_rows():
    """Fold rows exactly as fold_confirm.confirm_on_fold builds them (the fields the view
    reads), for explore_confirm.record_fold_confirmation to write."""
    row_confirmed = {
        "finding_id": "trade_efficiency-run_074-2", "source_run": "run_074", "run_id": "run_080",
        "basis": "child_run", "fold": "B", "kind": "event_behaviour", "status": "confirmed",
        "statement": "After a 3% fall in 24 hours the next 24 hours return more by 12 bps.",
        "fold_observed": "A", "spec_hashes": ["aaa"],
        "tests": {"t1": {"spec_hash": "aaa", "status": "confirmed", "horizons": {
            "24": {"effect": 0.0012, "windows_claimed_sign": 5, "windows_with_value": 6}}}},
        "effect": {"t1": {"24": 0.0012}}, "agreement": {"t1": {"24": "5 of 6"}}}
    row_failed = {
        "finding_id": "forecast_power-run_074-1", "source_run": "run_074", "run_id": "run_081",
        "basis": "child_run", "fold": "B", "kind": "direction_forecast", "status": "not_confirmed",
        "statement": "A forecast above 8 predicts a 0.31% return at h=6.",
        "reason": "the noise rule fails: h=6: pooled held, windows 3 of 6",
        "spec_hashes": ["bbb"],
        "tests": {"t1": {"spec_hash": "bbb", "status": "not_confirmed", "horizons": {
            "6": {"effect": 0.0031, "windows_claimed_sign": 3, "windows_with_value": 6}}}},
        "effect": {"t1": {"6": 0.0031}}, "agreement": {"t1": {"6": "3 of 6"}}}
    row_short = {"finding_id": "x-run_073-1", "source_run": "run_073", "run_id": "run_082",
                 "basis": "child_run", "fold": "C", "status": "not_measurable",
                 "kind": "conversion", "statement": "Rebalances smaller than 0.3 lose 14 bps.",
                 "reason": "fewer than 4 windows with a value (windows with a value) 2"}
    row_nc = {"finding_id": "x-run_073-2", "source_run": "run_073", "run_id": "run_083",
              "basis": "child_run", "fold": "B", "status": "not_comparable",
              "kind": "conversion", "statement": "Claim 7 about 12 bars."}
    return [row_confirmed, row_failed, row_short, row_nc]


def _e072_rows():
    """E-072 `findings` rows (never confirmed on a fold)."""
    row_legacy_pending = {"finding_id": "old-run_070-1", "source_run": "run_070",
                          "status": "pending", "confirmation_sign_retained": "pending",
                          "kind": "event_behaviour", "statement": "Legacy 5% claim.",
                          "finding_spec_hashes": ["ccc"]}
    row_legacy_measured = {"finding_id": "old-run_070-2", "source_run": "run_070",
                           "status": "measured", "confirmation_sign_retained": True,
                           "kind": "event_behaviour", "statement": "Legacy 9% held claim.",
                           "tests": {"t": {"status": "measured", "horizons": {
                               "1": {"effect": 0.9, "windows_claimed_sign": 6,
                                     "windows_with_value": 6}}}}}
    return {r["finding_id"]: r for r in (row_legacy_pending, row_legacy_measured)}


def _write_ledger(root: Path, fold_rows=None, e072=None) -> dict:
    """campaign_record/confirmations.yaml as the real writers leave it: E-072 rows under
    `findings`, then each fold row through explore_confirm.record_fold_confirmation (which
    files it under `fold_confirmations`). Returns the loaded ledger."""
    import explore_confirm as ec
    path = root / ec.LEDGER_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({"schema_version": 1, "findings": dict(e072 or {}),
                                    "looks": []}), encoding="utf-8")
    for row in fold_rows or []:
        ec.record_fold_confirmation(root, copy.deepcopy(row))
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _ledger(tmp_path):
    return _write_ledger(tmp_path, _fold_rows(), _e072_rows())


def _walk(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk(k)
            yield from _walk(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _walk(v)
    else:
        yield obj


def test_the_memory_view_of_run_074_shows_no_exploratory_effect_and_no_window_count():
    view = amv.build_memory_view(_run074_memory(), {})
    c = next(c for c in view["claims"] if c["claim_id"] == "F-run_074-1")
    assert c["status"] == "pending" and c["kind"] == "direction_forecast"
    assert c["fold_observed"] is None and c["fold_confirmed"] is None
    assert "confirmed" not in c
    blob = json.dumps(view)
    for leaked in ("0.0542876", "0.0543", "17512", "-0.0057", "0.0057", "6/6", "6 of 6",
                   "windows_claimed_sign", "windows_with_value", "largest_effect", "by_variant",
                   "measured, not proven"):
        assert leaked not in blob, leaked
    assert not re.search(r"\b\d+\s*/\s*\d+\b|\b\d+ of \d+\b", blob)
    # the claim's words survive, its number literals do not, its mechanical spec is readable
    assert "shock_reversal forecast at period=<n> predicts zero forward returns" in c["statement"]
    assert c["tests"][0]["selector"] == {"kind": "all"} and c["tests"][0]["statistic"] == "rank_ic"
    assert c["tests"][0]["spec_hash"].startswith("f084b07e")
    # every field of every claim, and of every test row, is one of the allowed ones
    for cl in view["claims"]:
        for t in cl["tests"]:
            assert set(t) <= {"name", "spec_hash", "selector", "outcome", "baseline",
                              "statistic", "direction"}, t
        assert set(cl) <= {"claim_id", "source_run", "statement", "kind", "fold_observed",
                           "fold_confirmed", "status", "tests", "confirmed"}
    # a claim of a run with a fold carries it; a claim with no test cannot be confirmed
    c3 = next(c for c in view["claims"] if c["claim_id"] == "F-run_073-1")
    assert c3["fold_observed"] == "A" and c3["status"] == "not_measurable"
    assert "3% fall" not in c3["statement"] and "<n>" in c3["statement"]
    assert [c["claim_id"] for c in view["claims"]] == ["F-run_073-1", "F-run_074-1"]   # run order


def test_the_memory_view_with_the_ledger_numbers_only_for_confirmed_claims(tmp_path):
    ledger = _ledger(tmp_path)
    assert set(ledger["fold_confirmations"]) == {
        "trade_efficiency-run_074-2@run_080", "forecast_power-run_074-1@run_081",
        "x-run_073-1@run_082", "x-run_073-2@run_083"}           # where the real writer files them
    view = amv.build_memory_view(_run074_memory(), ledger)
    by = {c["claim_id"]: c for c in view["claims"]}
    conf = by["trade_efficiency-run_074-2"]
    assert conf["status"] == "confirmed" and conf["fold_confirmed"] == ["B"]
    assert conf["fold_observed"] == "A"
    assert conf["confirmed"] == [{"fold": "B", "effect": {"t1": {"24": 0.0012}},
                                  "agreement": {"t1": {"24": "5 of 6"}}}]
    assert conf["folds"] == [{"fold": "B", "run_id": "run_080", "status": "confirmed"}]
    # D-090: a confirmed claim's statement is masked too (its numbers are the exploratory ones)
    assert "12 bps" not in conf["statement"] and "<n>" in conf["statement"]
    # the others: a status and a fold, never a number
    assert by["forecast_power-run_074-1"]["status"] == "not_confirmed"
    assert by["forecast_power-run_074-1"]["fold_confirmed"] is None
    assert by["x-run_073-1"]["status"] == "not_measurable"
    assert by["x-run_073-2"]["status"] == "not_measurable"                # not_comparable
    assert by["old-run_070-1"]["status"] == "pending"
    assert by["old-run_070-2"]["status"] == "pending"                     # an in-run sign is no confirmation
    assert by["old-run_070-1"]["tests"] == [{"spec_hash": "ccc"}]
    assert view["by_status"] == {"confirmed": 1, "not_confirmed": 1, "not_measurable": 3,
                                 "pending": 3}
    assert view["n_claims"] == 8
    rest = {k: v for k, v in by.items() if k != "trade_efficiency-run_074-2"}
    blob = json.dumps(rest) + json.dumps(conf["statement"])
    for leaked in ("0.0031", "3 of 6", "0.9", "windows", "reason", "noise rule", "14 bps",
                   "0.31%", "0.3 lose", "5%", "9%", "12 bars", "12 bps", "3%"):
        assert leaked not in blob, leaked
    nums = [x for x in _walk(rest) if isinstance(x, float)]
    assert nums == []
    # the confirmed numbers can also come from the row's per-test horizons
    rows = _fold_rows()
    del rows[0]["effect"], rows[0]["agreement"]
    c = next(c for c in amv.build_memory_view({}, _write_ledger(tmp_path / "b", rows))["claims"]
             if c["claim_id"] == "trade_efficiency-run_074-2")
    assert c["confirmed"][0]["effect"] == {"t1": {"24": 0.0012}}
    assert c["confirmed"][0]["agreement"] == {"t1": {"24": "5 of 6"}}


def _same_claim_on(fold, run_id, status, effect=0.0012):
    row = copy.deepcopy(_fold_rows()[0])
    row.update(fold=fold, run_id=run_id, status=status, effect={"t1": {"24": effect}})
    return row


@pytest.mark.parametrize("order", [(0, 1), (1, 0)])
def test_a_claim_measured_on_two_folds_gets_one_status_from_the_statuses(tmp_path, order):
    """Operator, 2026-10-08 (D-090): confirmed on one fold and refuted on another reads
    `confirmed`, whatever the key order (run_100 sorts before run_99 as text); the
    refutation stays recorded in `folds`, and only the confirming fold's numbers show."""
    rows = [_same_claim_on("B", "run_99", "confirmed"),
            _same_claim_on("C", "run_100", "not_confirmed", effect=-0.003)]
    ledger = _write_ledger(tmp_path, [rows[i] for i in order])
    (c,) = amv.build_memory_view({}, ledger)["claims"]
    assert c["status"] == "confirmed" and c["fold_confirmed"] == ["B"]
    assert [x["fold"] for x in c["confirmed"]] == ["B"]
    assert -0.003 not in [x for x in _walk(c) if isinstance(x, float)]
    assert c["folds"] == [{"fold": "B", "run_id": "run_99", "status": "confirmed"},
                          {"fold": "C", "run_id": "run_100", "status": "not_confirmed"}]
    # refuted with nothing confirmed: not_confirmed, and no number
    (c,) = amv.build_memory_view({}, _write_ledger(tmp_path / "r", [rows[1]]))["claims"]
    assert c["status"] == "not_confirmed" and "confirmed" not in c
    assert not [x for x in _walk(c) if isinstance(x, float)]


def test_confirmed_on_one_fold_and_not_measurable_on_another_is_confirmed(tmp_path):
    rows = [_same_claim_on("C", "run_100", "not_measurable"),
            _same_claim_on("B", "run_99", "confirmed")]
    (c,) = amv.build_memory_view({}, _write_ledger(tmp_path, rows))["claims"]
    assert c["status"] == "confirmed" and c["fold_confirmed"] == ["B"]
    assert [x["fold"] for x in c["confirmed"]] == ["B"]
    # confirmed on two folds: both rows' numbers, one entry per fold
    rows = [_same_claim_on("B", "run_99", "confirmed"),
            _same_claim_on("C", "run_100", "confirmed", effect=0.002)]
    (c,) = amv.build_memory_view({}, _write_ledger(tmp_path / "two", rows))["claims"]
    assert c["fold_confirmed"] == ["B", "C"]
    assert [x["effect"]["t1"]["24"] for x in c["confirmed"]] == [0.0012, 0.002]


def test_a_fold_row_replaces_the_e072_row_and_the_memory_claim_of_the_same_id(tmp_path):
    memory = _run074_memory()
    row = dict(_same_claim_on("B", "run_080", "not_confirmed"), finding_id="F-run_074-1",
               statement=RUN074_STATEMENT)
    e072 = {"F-run_074-1": {"finding_id": "F-run_074-1", "status": "pending",
                            "statement": RUN074_STATEMENT}}
    view = amv.build_memory_view(memory, _write_ledger(tmp_path, [row], e072))
    c = next(c for c in view["claims"] if c["claim_id"] == "F-run_074-1")
    assert c["status"] == "not_confirmed"
    assert "-0.0057" not in c["statement"]
    assert sum(1 for x in view["claims"] if x["claim_id"] == "F-run_074-1") == 1


def test_the_view_of_nothing_is_empty_and_the_loader_reads_the_two_files(tmp_path):
    assert amv.build_memory_view({}, None)["claims"] == []
    assert amv.load_memory_view(tmp_path)["n_claims"] == 0
    rec = tmp_path / "campaign_record"
    rec.mkdir()
    (rec / "campaign_memory.yaml").write_text(yaml.safe_dump(_run074_memory()), encoding="utf-8")
    _write_ledger(tmp_path, _fold_rows(), _e072_rows())
    view = amv.load_memory_view(tmp_path)
    assert view["n_claims"] == 8 and view["by_status"]["confirmed"] == 1
    assert amv.MEMORY_REL == "campaign_record/campaign_memory.yaml"
    assert amv.LEDGER_REL == "campaign_record/confirmations.yaml"


def test_the_real_confirmations_row_shape_of_e072_is_read_without_error():
    """A row exactly as explore_confirm.confirm_findings writes it today."""
    import explore_confirm as ec
    row = {"finding_id": "trade_efficiency-run_073-1", "category": "trade_efficiency",
           "source_run": "run_073", "kind": "event_behaviour", "statement": "S 3 bps.",
           "proposer_saw": [], "confirmation_set": "set", "bar": ec.HONEST_BAR,
           "route": ec.IN_RUN, "status": ec.MEASURED, "confirmation_sign_retained": True,
           "finding_spec_hashes": ["h1"], "tests": {"t": {"horizons": {
               "1": {"effect": 0.01, "windows_claimed_sign": 3, "windows_with_value": 3}}}}}
    view = amv.build_memory_view({}, {"findings": {row["finding_id"]: row}})
    c = view["claims"][0]
    assert c["status"] == "pending" and "confirmed" not in c
    assert json.dumps(c).count("0.01") == 0


# ---------------------------------------------------------------------------
# 9. Post-merge review fixes (D-090)
# ---------------------------------------------------------------------------

def test_a_grouping_by_hour_weekday_or_regime_is_counted_whatever_the_column(run):
    """past_return_1 at bar t+1 is fwd_return h=1 at bar t, and the bucket means of a price
    level differ by the move between the buckets: a mean by hour IS a calendar effect, so
    describe / distribution count one per group by hour, weekday or regime (D-090)."""
    eng = engine(run)
    for col, by in (("past_return_1", "hour"), ("close", "hour"), ("close", "weekday"),
                    ("forecast", "regime"), ("total_portfolio_value", "hour")):
        r = eng.describe(col, by=by)
        groups = len(r["result"]["groups"])
        assert groups >= 1 and r["n_comparisons"] == groups, (col, by)
    r = eng.distribution("trailing_vol_24", by="weekday", bins=4)
    assert r["n_comparisons"] == len(r["result"]["groups"])
    # no grouping, or a grouping by window or coin, stays free
    assert eng.describe("past_return_1", by="window")["n_comparisons"] == 0
    assert eng.describe("close", by="coin")["n_comparisons"] == 0
    assert eng.describe("past_return_1")["n_comparisons"] == 0
    assert eng.distribution("forecast")["n_comparisons"] == 0


def test_the_calendar_count_is_charged_before_any_number(run):
    eng = engine(run, comparison_budget=2)
    r = eng.describe("past_return_1", by="hour")
    assert r["status"] == "refused" and "comparison budget spent" in r["reason"]
    assert "result" not in r and log_of(eng)[-1]["status"] == "refused"


@pytest.mark.parametrize("bad", [float("inf"), float("-inf"), float("nan")])
def test_a_non_finite_parameter_is_refused_and_logged(run, bad):
    eng = engine(run)
    r = eng.conditional_effect({"kind": "event", "field": "forecast", "op": ">=", "value": bad},
                               [1])
    assert r["status"] == "refused" and "finite" in r["reason"]
    assert r["n_comparisons"] == 0 and log_of(eng)[-1]["status"] == "refused"


def test_a_negative_count_in_the_log_gives_no_budget_back(run):
    eng = engine(run, comparison_budget=3)
    sel = {"kind": "event", "field": "forecast", "op": ">=", "value": 3.0}
    assert eng.conditional_effect(sel, [1, 2, 3])["status"] == "ok"            # 3 of 3
    doc = yaml.safe_load(eng.log.path.read_text(encoding="utf-8"))
    doc["queries"].append({"id": "q2", "function": "describe", "status": "ok",
                           "n_comparisons": -1000})
    eng.log.path.write_text(yaml.safe_dump(doc), encoding="utf-8")
    r = eng.conditional_effect(sel, [1])
    assert r["status"] == "refused" and "comparison budget spent" in r["reason"]


def test_event_study_counts_only_checkpoints_with_a_value(tmp_path):
    closes = make_closes()
    for c in closes.values():
        for k in range(len(HOLDS)):
            c[5 + 15 * k + 1] = np.nan                     # the close one bar after each entry
    a = make_run(tmp_path / "a", closes)
    out = engine(a).event_study([], 3, 3)["result"]
    assert out["after"]["1"] == {"n": 0, "mean": None}
    assert out["after"]["2"]["n"] > 0 and out["after"]["2"]["mean"] is not None


def test_a_fold_row_without_words_keeps_the_words_of_the_claim_it_replaces(tmp_path):
    bare = dict(_same_claim_on("A", "run_90", "not_measurable"), statement=None, kind=None)
    worded = _same_claim_on("B", "run_91", "not_confirmed")
    e072 = {worded["finding_id"]: {"finding_id": worded["finding_id"], "status": "pending",
                                   "statement": "E-072 words", "kind": "event_behaviour"}}
    (c,) = amv.build_memory_view({}, _write_ledger(tmp_path, [bare, worded], e072))["claims"]
    assert c["statement"].startswith("After a <n> fall") and c["kind"] == "event_behaviour"
    (c,) = amv.build_memory_view({}, _write_ledger(tmp_path / "b", [bare], e072))["claims"]
    assert c["statement"] == "E-<n> words" and c["kind"] == "event_behaviour"


def test_free_text_outside_the_statement_carries_no_number(tmp_path):
    row = dict(_same_claim_on("B", "run_91", "not_confirmed"), kind="edge of 0.31% at h=6",
               statement="x2 h24 5of6 Sharpe1.2 1_000 Q4 R2 kept words")
    (c,) = amv.build_memory_view({}, _write_ledger(tmp_path, [row]))["claims"]
    assert c["kind"] is None                                # not a claim kind: not shown
    assert not re.search(r"\d", c["statement"]) and "kept words" in c["statement"]
    memory = _run074_memory()
    memory["runs"]["run_074"]["finding"]["tests"][0]["name"] = "fc_gt_8_gives_0.31pct_h6"
    view = amv.build_memory_view(memory, {})
    assert "0.31" not in json.dumps(view) and "fc_gt_8" not in json.dumps(view)


def test_an_unknown_fold_status_is_not_measurable_everywhere(tmp_path):
    row = _same_claim_on("B", "run_91", "weird")
    (c,) = amv.build_memory_view({}, _write_ledger(tmp_path, [row]))["claims"]
    assert c["status"] == "not_measurable" and c["folds"][0]["status"] == "not_measurable"


def test_a_numpy_nan_parameter_is_refused_too():
    assert aq._nonfinite({"a": [np.float32("nan")]}) and aq._nonfinite(np.float64("inf"))
    assert not aq._nonfinite({"a": [1.0, 2, "x", None]})


def test_a_group_without_a_value_is_not_charged(run):
    eng = engine(run)
    vals = eng._column_values("base", "close")
    vals[0][:] = np.nan                    # window w0 of AAA: no close (the cached column)
    r = eng.describe("close", by="hour")
    groups = r["result"]["groups"]
    with_value = sum(1 for g in groups.values() if g["mean"] is not None)
    assert r["n_comparisons"] == with_value
    eng._cols[("base", "close")] = [np.full_like(v, np.nan) for v in vals]
    r = eng.describe("close", by="weekday")
    assert r["n_comparisons"] == 0 and all(g["mean"] is None for g in r["result"]["groups"].values())


def test_fold_observed_comes_from_the_first_row_that_has_it(tmp_path):
    bare = dict(_same_claim_on("A", "run_90", "not_measurable"), statement=None, kind=None)
    bare.pop("fold_observed")
    worded = _same_claim_on("B", "run_91", "not_confirmed")
    (c,) = amv.build_memory_view({}, _write_ledger(tmp_path, [bare, worded]))["claims"]
    assert c["fold_observed"] == "A" and worded["fold_observed"] == "A"
