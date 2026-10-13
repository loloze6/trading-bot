"""CUL-431 (D-107): tools/curve_cost_ratio.py, the curve-based gross / cost ratio.

Synthetic accounts check the arithmetic, the lot-net vs equity-change guard and
the agreement with the whole-test chain on junction days. The run_081 tests read
the operator's run folder (untracked runtime files) and skip where it is absent;
set CUL431_RUN_DIR to point at it from a worktree.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "tools"))

import curve_cost_ratio as ccr  # noqa: E402
import portfolio_daily as pdv1  # noqa: E402
import portfolio_whole_test as pw  # noqa: E402

FEE = 5e-4   # 5 bps per side (Kraken futures, cost_model.json)
SLIP = 2.5e-4


def _lot(side, q, ref_in, ref_out, t_in, t_out, trade_id="L"):
    """A trades.json record priced as the engine prices it (mock fill at the
    close moved by SLIP against the trade; commissions as metrics.py)."""
    if side == "LONG":
        p_in, p_out = ref_in * (1 + SLIP), ref_out * (1 - SLIP)
        c_in, c_out = q * p_in * FEE / (1 - FEE), q * p_out * FEE
        pnl = q * (p_out - p_in)
    else:
        p_in, p_out = ref_in * (1 - SLIP), ref_out * (1 + SLIP)
        c_in, c_out = q * p_in * FEE, q * p_out * FEE / (1 - FEE)
        pnl = q * (p_in - p_out)
    return {"trade_id": trade_id, "side": side, "matched_quantity": q,
            "entry_price": p_in, "exit_price": p_out, "entry_time": t_in, "exit_time": t_out,
            "total_commission": c_in + c_out, "net_profit_loss_absolute": pnl - c_in - c_out}


# ---------------------------------------------------------------------------
# arithmetic
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("side", ["LONG", "SHORT"])
def test_gross_is_the_move_at_bar_closes(side):
    lots = [_lot(side, 2.0, 100.0, 110.0, "2022-01-02", "2022-01-04", "a"),
            _lot(side, 1.0, 110.0, 95.0, "2022-01-04", "2022-01-05", "b")]
    closes = {"2022-01-02": 100.0, "2022-01-04": 110.0, "2022-01-05": 95.0}
    net = sum(x["net_profit_loss_absolute"] for x in lots)
    a = ccr.account_costs(lots, 1000.0, 1000.0 + net, closes, [False, True])
    sign = 1 if side == "LONG" else -1
    move = sign * (2.0 * (110 - 100) + 1.0 * (95 - 110))
    assert a["gross"] == pytest.approx(move, abs=1e-9)
    assert a["fees"] == pytest.approx(sum(x["total_commission"] for x in lots), abs=1e-12)
    assert a["slippage"] > 0
    f_b, s_b = ccr.lot_costs(lots[1], 110.0, 95.0)
    assert a["window_end_costs"] == pytest.approx(f_b + s_b, abs=1e-12)
    assert a["n_lots"] == 2


def test_ratio_sums_points_over_accounts_without_min():
    accts = [{"start": 1000.0, "equity_change": 50.0, "gross": 60.0, "costs": 10.0,
              "window_end_costs": 4.0, "n_lots": 3},
             {"start": 500.0, "equity_change": -10.0, "gross": -5.0, "costs": 5.0,
              "window_end_costs": 0.0, "n_lots": 2}]
    out = ccr.curve_gross_to_cost(accts)
    # points: gross 6 + (-1) = 5, costs 1 + 1 = 2, window-end 0.4
    assert out["gross_points"] == pytest.approx(5.0)
    assert out["cost_points"] == pytest.approx(2.0)
    assert out["ratio"] == pytest.approx(2.5)
    assert out["net_points"] == pytest.approx(5.0 - 2.0)
    assert out["window_end_cost_share"] == pytest.approx(0.2)
    assert (out["n_accounts"], out["n_lots"]) == (2, 5)


def test_not_evaluable_without_accounts_or_costs():
    with pytest.raises(pdv1.PortfolioNotEvaluable):
        ccr.curve_gross_to_cost([])
    with pytest.raises(pdv1.PortfolioNotEvaluable):
        ccr.curve_gross_to_cost([{"start": 1000.0, "equity_change": 0.0, "gross": 0.0,
                                  "costs": 0.0, "window_end_costs": 0.0, "n_lots": 0}])


# ---------------------------------------------------------------------------
# the guard: lot costs are summed only when lot net P&L == equity change
# ---------------------------------------------------------------------------

def test_guard_refuses_lots_that_do_not_sum_to_the_equity_change():
    lot = _lot("LONG", 1.0, 100.0, 120.0, "2022-01-02", "2022-01-03")
    closes = {"2022-01-02": 100.0, "2022-01-03": 120.0}
    end = 1000.0 + lot["net_profit_loss_absolute"]
    ccr.account_costs([lot], 1000.0, end, closes, [True])          # exact: accepted
    ccr.account_costs([lot], 1000.0, end + 1e-7, closes, [True])   # float noise: accepted
    with pytest.raises(ValueError, match="equity change"):
        ccr.account_costs([lot], 1000.0, end + 1e-3, closes, [True])
    with pytest.raises(ValueError, match="equity change"):
        ccr.account_costs([], 1000.0, end, closes, [])               # a missing lot


def test_guard_refuses_missing_close_bad_side_and_flag_count():
    lot = _lot("LONG", 1.0, 100.0, 120.0, "2022-01-02", "2022-01-03")
    end = 1000.0 + lot["net_profit_loss_absolute"]
    with pytest.raises(ValueError, match="no bar close"):
        ccr.account_costs([lot], 1000.0, end, {"2022-01-02": 100.0}, [False])
    with pytest.raises(ValueError, match="flags"):
        ccr.account_costs([lot], 1000.0, end, {"2022-01-02": 100.0, "2022-01-03": 120.0}, [])
    with pytest.raises(ValueError, match="side"):
        ccr.lot_costs({**lot, "side": "FLAT"}, 100.0, 120.0)
    with pytest.raises(ValueError, match="finite"):
        ccr.lot_costs({**lot, "total_commission": float("nan")}, 100.0, 120.0)


# ---------------------------------------------------------------------------
# a synthetic run folder: loader, and agreement with the whole-test chain
# ---------------------------------------------------------------------------

_COLS = ["timestamp", "close", "regime", "total_portfolio_value", "postRebalance_total_value"]


def _write_account(root, run_id, days, closes, equity_pre_first, equity_post, lots):
    d = root / "results" / run_id
    d.mkdir(parents=True)
    with open(d / "portfolio_states.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(_COLS)
        for i, day in enumerate(days):
            pre = equity_pre_first if i == 0 else equity_post[i - 1]
            w.writerow([day.isoformat(), closes[i], "unknown", pre, equity_post[i]])
    (d / "trades.json").write_text(json.dumps(lots), encoding="utf-8")


def _synthetic_run(tmp_path):
    """Two coins x two 5-day windows. AAA w1: a lot from day 2 to the window end;
    BBB w2: a lot entered on the window's FIRST day (a day-1 fill)."""
    w1 = [date(2022, 1, 1) + timedelta(days=i) for i in range(5)]
    w2 = [date(2022, 1, 6) + timedelta(days=i) for i in range(5)]
    px = [100.0, 102.0, 101.0, 106.0, 108.0]
    results, diag = [], []

    def flat(sym, win, days, rid):
        _write_account(tmp_path, rid, days, px, 1000.0, [1000.0] * 5, [])
        results.append({"symbol": sym, "window": win, "run_id": rid})

    # AAA w1: buy 5 at day-2 close, held to day 5 (window end)
    lot = _lot("LONG", 5.0, px[1], px[4], w1[1].isoformat(), w1[4].isoformat(), "aaa1")
    cash_after_buy = 1000.0 - 5.0 * lot["entry_price"] * (1 + FEE / (1 - FEE))
    eq = [1000.0] + [cash_after_buy + 5.0 * p for p in px[1:4]] \
        + [1000.0 + lot["net_profit_loss_absolute"]]
    _write_account(tmp_path, "r_aaa_w1", w1, px, 1000.0, eq, [lot])
    results.append({"symbol": "AAA", "window": "w1", "run_id": "r_aaa_w1"})
    diag.append({**lot, "symbol": "AAA", "window": "w1", "exit_reason": "end_of_window"})
    flat("BBB", "w1", w1, "r_bbb_w1")
    flat("AAA", "w2", w2, "r_aaa_w2")
    # BBB w2: buy 4 at the FIRST day's close, sold at day 4 (signal)
    lot2 = _lot("LONG", 4.0, px[0], px[3], w2[0].isoformat(), w2[3].isoformat(), "bbb2")
    cash2 = 1000.0 - 4.0 * lot2["entry_price"] * (1 + FEE / (1 - FEE))
    end2 = 1000.0 + lot2["net_profit_loss_absolute"]
    eq2 = [cash2 + 4.0 * p for p in px[0:3]] + [end2, end2]
    _write_account(tmp_path, "r_bbb_w2", w2, px, 1000.0, eq2, [lot2])
    results.append({"symbol": "BBB", "window": "w2", "run_id": "r_bbb_w2"})
    diag.append({**lot2, "symbol": "BBB", "window": "w2", "exit_reason": "signal_flip"})
    (tmp_path / "artifacts").mkdir()
    (tmp_path / "artifacts" / "protocol_result.yaml").write_text(
        yaml.safe_dump({"results": results}), encoding="utf-8")
    (tmp_path / "trade_diagnostics.json").write_text(json.dumps({"trades": diag}),
                                                     encoding="utf-8")
    bounds = {"w1": (w1[0], w1[-1]), "w2": (w2[0], w2[-1])}
    return results, bounds


def _chain(run_dir, results, bounds):
    windows, coins = pdv1.load_windows(run_dir, {"results": results})
    return pw.chain_windows(windows, coins, bounds)


def _junction_check(run_dir, accounts, chain, tol):
    """Equity only, not costs: this ties the curve figure's equity change to the
    chain's equity; cost correctness rests on the lot-net == equity-change guard
    and the slippage test. Per chained window: the chain's level ratio from its join day to its end
    day vs the equal-weight mean of (equity change / start). They agree when no
    coin trades on the window's first day; with a day-1 fill the chain anchors
    at that day's close AFTER the fill, so it leaves that fill's costs out, and
    the gap is exactly mean(V_end / V_anchor) - mean(V_end / V_start)."""
    levels = dict(chain["daily_levels"])
    nets = ccr.window_net_returns(accounts)
    checked = {"agree": 0, "day1_gap": 0}
    for seg in chain["segments"]:
        win = seg["window"]
        chain_ret = levels[seg["end_day"]] / levels[seg["join_day"]] - 1
        accts = {s: a for (s, w), a in accounts.items() if w == win}
        anchors = {}
        for s in accts:
            path = pdv1.find_window_equity_file(run_dir, _run_id(run_dir, s, win))
            anchors[s] = pdv1.window_daily_closes(path)[seg["anchor"]]
        expected_gap = sum((a["start"] + a["equity_change"]) * (1 / anchors[s] - 1 / a["start"])
                           for s, a in accts.items()) / len(accts)
        assert chain_ret - nets[win] == pytest.approx(expected_gap, abs=tol), win
        if all(abs(anchors[s] - a["start"]) <= 1e-9 for s, a in accts.items()):
            assert chain_ret == pytest.approx(nets[win], abs=tol), win
            checked["agree"] += 1
        else:
            assert abs(chain_ret - nets[win]) > tol, win
            checked["day1_gap"] += 1
    return checked


def _run_id(run_dir, sym, win):
    pr = yaml.safe_load((Path(run_dir) / "artifacts" / "protocol_result.yaml").read_text(encoding="utf-8"))
    return next(r["run_id"] for r in pr["results"] if r["symbol"] == sym and str(r["window"]) == win)


def test_loader_on_a_synthetic_run(tmp_path):
    _synthetic_run(tmp_path)
    accounts = ccr.load_run_accounts(tmp_path)
    assert len(accounts) == 4
    a = accounts[("AAA", "w1")]
    assert a["gross"] == pytest.approx(5.0 * (108.0 - 102.0), abs=1e-9)
    assert a["window_end_costs"] == pytest.approx(a["costs"], abs=1e-12)
    b = accounts[("BBB", "w2")]
    assert b["gross"] == pytest.approx(4.0 * (106.0 - 100.0), abs=1e-9)
    assert b["window_end_costs"] == 0.0
    out = ccr.curve_gross_to_cost(list(accounts.values()))
    assert out["ratio"] == pytest.approx((a["gross"] + b["gross"]) / (a["costs"] + b["costs"]))


def test_loader_refuses_mismatched_diagnostics(tmp_path):
    _synthetic_run(tmp_path)
    p = tmp_path / "trade_diagnostics.json"
    d = json.loads(p.read_text())
    d["trades"][0]["trade_id"] = "other"
    p.write_text(json.dumps(d))
    with pytest.raises(ValueError, match="lots differ"):
        ccr.load_run_accounts(tmp_path)


def test_agrees_with_the_whole_test_chain_on_junction_days(tmp_path):
    results, bounds = _synthetic_run(tmp_path)
    accounts = ccr.load_run_accounts(tmp_path)
    chain = _chain(tmp_path, results, bounds)
    # w1: no first-day fill -> agree; w2: BBB fills on day 1 -> the known gap
    assert _junction_check(tmp_path, accounts, chain, 1e-12) == {"agree": 1, "day1_gap": 1}


# ---------------------------------------------------------------------------
# not wired: no stage or tool imports it (a pure tool, so no flag)
# ---------------------------------------------------------------------------

def test_not_imported_by_any_stage_or_tool():
    pat = re.compile(r"^\s*(from|import)\s+curve_cost_ratio\b|import_module\(\s*['\"]curve_cost_ratio",
                     re.M)
    hits = [p for d in ("workflow", "tools") for p in (SR_ROOT / d).rglob("*.py")
            if p.name != "curve_cost_ratio.py" and pat.search(p.read_text(encoding="utf-8",
                                                                          errors="replace"))]
    assert hits == []


# ---------------------------------------------------------------------------
# run_081 (the operator's run folder; skipped where absent)
# ---------------------------------------------------------------------------

RUN_081 = Path(os.environ.get("CUL431_RUN_DIR", SR_ROOT / "runs" / "run_081"))
needs_run_081 = pytest.mark.skipif(not (RUN_081 / "trade_diagnostics.json").exists(),
                                   reason="run_081's folder is a local runtime artefact")


@needs_run_081
def test_run_081_every_account_lot_net_equals_equity_change():
    # load_run_accounts raises on any account whose lots' net P&L differs
    accounts = ccr.load_run_accounts(RUN_081)
    assert len(accounts) == 48
    out = ccr.curve_gross_to_cost(list(accounts.values()))
    assert out["n_lots"] == 257
    assert out["ratio"] == pytest.approx(5.6123, abs=1e-4)
    assert out["window_end_cost_share"] == pytest.approx(0.1226, abs=1e-4)


@needs_run_081
def test_run_081_slippage_matches_the_diagnostics_bps():
    """Per lot, the currency slippage over each leg's notional is exactly the
    configured slippage on both legs (manifest cost_model), and within 0.2 bps
    of the run's own STORED slippage_paid (run_protocol._all_costs_fields), which was
    written before D-117 from bars.csv closes rounded to 6 decimals (DOGE near 0.06: up to
    ~0.08 bps per leg; run_081 max 0.107). Since D-117 new diagnostics read full-precision
    closes (tests/test_d117_slippage_precision.py)."""
    diag = json.loads((RUN_081 / "trade_diagnostics.json").read_text(encoding="utf-8"))["trades"]
    pr = yaml.safe_load((RUN_081 / "artifacts" / "protocol_result.yaml").read_text(encoding="utf-8"))
    n = 0
    for r in pr["results"]:
        path = pdv1.find_window_equity_file(RUN_081, r["run_id"])
        cm = json.loads((path.parent / "manifest.json").read_text(encoding="utf-8"))["config"]["cost_model"]
        slip_bps = cm["slippage_bps"].get(r["symbol"], cm["slippage_bps"]["default"])
        with open(path, encoding="utf-8", newline="") as f:
            closes = {ccr._ts(row["timestamp"]): float(row["close"]) for row in csv.DictReader(f)}
        lots = json.loads((path.parent / "trades.json").read_text(encoding="utf-8"))
        recs = [d for d in diag if d["symbol"] == r["symbol"] and str(d["window"]) == str(r["window"])]
        for lot, rec in zip(lots, recs):
            r_in, r_out = closes[ccr._ts(lot["entry_time"])], closes[ccr._ts(lot["exit_time"])]
            sign = 1 if lot["side"] == "LONG" else -1   # a short sells to enter, buys to exit
            leg_bps = sign * ((lot["entry_price"] - r_in) / r_in
                              + (r_out - lot["exit_price"]) / r_out) * 1e4
            assert leg_bps == pytest.approx(2 * slip_bps, abs=1e-6)
            assert leg_bps == pytest.approx(rec["slippage_paid"], abs=0.2)
            n += 1
    assert n == 257


@needs_run_081
def test_run_081_agrees_with_the_whole_test_chain_on_junction_days():
    pr = yaml.safe_load((RUN_081 / "artifacts" / "protocol_result.yaml").read_text(encoding="utf-8"))
    proto = RUN_081.parent.parent / pr["protocol_file"].replace("\\", "/")
    bounds = {str(k): v for k, v in pw.load_protocol_window_bounds(proto).items()}
    accounts = ccr.load_run_accounts(RUN_081)
    chain = _chain(RUN_081, pr["results"], {w: bounds[w] for w in
                                            {str(r["window"]) for r in pr["results"]}})
    # 2022-01 and 2023-09 have no first-day fill; the other four do
    assert _junction_check(RUN_081, accounts, chain, 1e-9) == {"agree": 2, "day1_gap": 4}
