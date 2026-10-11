"""
CUL-431 (D-107): a curve-based gross / cost ratio for pre-registration.

Why: the lot-based ratio (portfolio_whole_test.pooled_edge_to_cost_ratio, the
D-038 bar) is a plain mean per lot, unweighted by position size, and takes the
min of "all lots" and "lots without window-end closes". For a strategy whose
hold exceeds the 4-month window, the gains end as window-end closes, so that
min() removes the edge itself (run_081: -5.155 lot-based, about 3.9 at
position size; D-107).

Definition, per coin-window account, in currency divided by its starting
capital:
    gross = equity change + fees + slippage
    ratio = sum of gross / sum of (fees + slippage), over all accounts
The window-end closes' share of the costs is reported beside it, with no min().

Where the inputs come from (no output writes a fee per fill):
  * equity: the account's portfolio_states.csv, total_portfolio_value of its
    first row (the starting capital, before that bar's rebalance) and
    postRebalance_total_value of its last row;
  * fees: the engine's lot file trades.json (reporting/run_artifact.py
    write_trades_json), total_commission of each lot, in currency;
  * slippage: each lot's matched_quantity x the fill's adverse move from the
    bar close of the leg (the mock fill is close x (1 +/- slippage_bps),
    execution/execution_handler.py open_long_position / open_short_position);
    the close is read from the same portfolio_states.csv at the leg's
    timestamp (the run_protocol._all_costs_fields convention, in currency).
Summing lot costs per account is allowed only because the sum of the lots'
net P&L equals the account's equity change: account_costs checks it on every
account and raises otherwise (tested on all 48 accounts of run_081).

A pure tool: no stage imports it, so it needs no flag. It reads nothing under
local_data/: only a run directory's own result files.
"""
from __future__ import annotations

import csv
import json
import math
from datetime import datetime
from pathlib import Path

import yaml

from portfolio_daily import PortfolioNotEvaluable, find_window_equity_file

END_OF_WINDOW = "end_of_window"
# Relative tolerance of the lot-net vs equity-change identity: float rounding
# only (run_081's largest gap is 8.2e-13 on a 1000 start, ~1e-15 relative).
IDENTITY_REL_TOL = 1e-9


def _finite(value, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) \
            or not math.isfinite(float(value)):
        raise ValueError(f"{what} must be a finite number, got {value!r}")
    return float(value)


def _ts(value) -> datetime:
    return datetime.fromisoformat(str(value).strip().replace(" ", "T"))


def lot_costs(lot: dict, ref_in: float, ref_out: float) -> tuple:
    """(fees, slippage) of one lot in currency. lot: a trades.json record
    (side, matched_quantity, entry_price, exit_price, total_commission);
    ref_in / ref_out: the bar closes of its entry and exit legs."""
    side = lot.get("side")
    if side not in ("LONG", "SHORT"):
        raise ValueError(f"lot {lot.get('trade_id')!r} has side {side!r}")
    q = abs(_finite(lot.get("matched_quantity"), "matched_quantity"))
    p_in = _finite(lot.get("entry_price"), "entry_price")
    p_out = _finite(lot.get("exit_price"), "exit_price")
    fees = _finite(lot.get("total_commission"), "total_commission")
    r_in, r_out = _finite(ref_in, "entry close"), _finite(ref_out, "exit close")
    if r_in <= 0 or r_out <= 0:
        raise ValueError(f"lot {lot.get('trade_id')!r}: a leg's close is not positive")
    if side == "LONG":   # buy to enter, sell to exit
        slip = q * (p_in - r_in) + q * (r_out - p_out)
    else:                # sell to enter, buy to cover
        slip = q * (r_in - p_in) + q * (p_out - r_out)
    return fees, slip


def account_costs(lots: list, start_equity: float, end_equity: float, closes: dict,
                  window_end: list) -> dict:
    """One coin-window account, in currency: {start, equity_change, fees,
    slippage, costs, gross, window_end_costs, n_lots}.
    closes: {timestamp: bar close}; window_end: one bool per lot (its exit is a
    window-end forced close). Raises ValueError when the lots' net P&L does not
    sum to the equity change (the lot costs would then not be the account's)."""
    start = _finite(start_equity, "start equity")
    end = _finite(end_equity, "end equity")
    if start <= 0:
        raise ValueError(f"start equity must be positive, got {start!r}")
    if len(window_end) != len(lots):
        raise ValueError(f"{len(window_end)} window-end flags for {len(lots)} lots")
    by_ts = {_ts(k): _finite(v, f"close at {k}") for k, v in closes.items()}
    fees = slip = we = lot_net = 0.0
    for lot, is_we in zip(lots, window_end):
        t_in, t_out = _ts(lot.get("entry_time")), _ts(lot.get("exit_time"))
        if t_in not in by_ts or t_out not in by_ts:
            raise ValueError(f"lot {lot.get('trade_id')!r}: no bar close at its entry or exit")
        f, s = lot_costs(lot, by_ts[t_in], by_ts[t_out])
        fees += f
        slip += s
        if is_we:
            we += f + s
        lot_net += _finite(lot.get("net_profit_loss_absolute"), "net_profit_loss_absolute")
    change = end - start
    if abs(lot_net - change) > IDENTITY_REL_TOL * start:
        raise ValueError(f"lots' net P&L {lot_net!r} != equity change {change!r}: lot costs "
                         f"cannot be summed for this account")
    return {"start": start, "equity_change": change, "fees": fees, "slippage": slip,
            "costs": fees + slip, "gross": change + fees + slip, "window_end_costs": we,
            "n_lots": len(lots)}


def curve_gross_to_cost(accounts: list) -> dict:
    """The run's curve-based figure from account_costs results: {ratio,
    gross_points, cost_points, net_points, window_end_cost_share, n_accounts,
    n_lots}. *_points: percentage points of each account's starting capital,
    summed over the accounts. PortfolioNotEvaluable when there is no account or
    the costs sum to zero."""
    if not accounts:
        raise PortfolioNotEvaluable("curve cost ratio: no account")
    gross = cost = net = we = 0.0
    for a in accounts:
        gross += 100.0 * a["gross"] / a["start"]
        cost += 100.0 * a["costs"] / a["start"]
        net += 100.0 * a["equity_change"] / a["start"]
        we += 100.0 * a["window_end_costs"] / a["start"]
    if cost == 0:
        raise PortfolioNotEvaluable("curve cost ratio: the costs sum to zero")
    return {"ratio": gross / cost, "gross_points": gross, "cost_points": cost,
            "net_points": net, "window_end_cost_share": we / cost,
            "n_accounts": len(accounts), "n_lots": sum(a["n_lots"] for a in accounts)}


def load_run_accounts(run_dir: Path) -> dict:
    """{(symbol, window): account_costs result} for a run directory: windows
    from artifacts/protocol_result.yaml, lots from each window's trades.json,
    window-end flags from the run's trade_diagnostics.json (the run's own
    exit_reason, matched to trades.json by order and trade_id)."""
    run_dir = Path(run_dir)
    pr = yaml.safe_load((run_dir / "artifacts" / "protocol_result.yaml").read_text(encoding="utf-8"))
    diag = json.loads((run_dir / "trade_diagnostics.json").read_text(encoding="utf-8"))["trades"]
    reasons: dict = {}
    for rec in diag:
        reasons.setdefault((rec["symbol"], str(rec["window"])), []).append(rec)
    out = {}
    for r in pr.get("results") or []:
        sym, win = r["symbol"], str(r["window"])
        states = find_window_equity_file(run_dir, r["run_id"])
        if states is None:
            raise PortfolioNotEvaluable(f"no portfolio_states.csv for {sym} {win}")
        with open(states, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            raise PortfolioNotEvaluable(f"empty portfolio_states.csv for {sym} {win}")
        tpath = states.parent / "trades.json"
        lots = json.loads(tpath.read_text(encoding="utf-8")) if tpath.exists() else []
        recs = reasons.get((sym, win), [])
        if len(recs) != len(lots) or any(a.get("trade_id") != b.get("trade_id")
                                         for a, b in zip(lots, recs)):
            raise ValueError(f"{sym} {win}: trades.json and trade_diagnostics.json lots differ")
        out[(sym, win)] = account_costs(
            lots, float(rows[0]["total_portfolio_value"]),
            float(rows[-1]["postRebalance_total_value"]),
            {row["timestamp"]: float(row["close"]) for row in rows},
            [rec.get("exit_reason") == END_OF_WINDOW for rec in recs])
    if not out:
        raise PortfolioNotEvaluable("protocol_result has no per-window results")
    return out


def window_net_returns(accounts: dict) -> dict:
    """{window: equal-weight mean of (equity change / start)}, the per-window
    return the curve figure's equity implies (compared with the whole-test
    chain in the tests)."""
    by_win: dict = {}
    for (_sym, win), a in accounts.items():
        by_win.setdefault(win, []).append(a["equity_change"] / a["start"])
    return {w: sum(v) / len(v) for w, v in by_win.items()}
