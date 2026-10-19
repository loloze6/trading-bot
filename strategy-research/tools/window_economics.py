"""PR-B (analyst tools, 2026-10-19): the economics of one variant, per (coin, window) --
ONE definition, shared by the analyst's `window_economics` query
(QueryEngine.window_economics, the analyst's query engine) and the per-variant
`window_economics` object stored beside `forecast_shape` in
artifacts/profit_bars_evaluation.yaml (workflow/run_phase1_research.py, under
orchestrator.analyst.enabled). Each caller resolves its own window folders (with
its own path checks); this module only reads the `bars.csv` and `trades.json` of
the folders it is given. A pure module: no SDK, no network, writes nothing.

Per (coin, window) cell, keyed `<symbol>/<window>`; `total` pools every cell
-------------------------------------------------------------------------
Bar fields read the window's bars.csv rows with regime != NOT_READY (stripped,
upper case) -- the rows build_bar_equity (trading-bot/reporting/run_artifact.py)
counts, so `turnover` is metrics.json's bar_equity.turnover before its rounding.
  n_bars               the bars read
  turnover             performance.bar_equity.turnover(postRebalance_current_allocation,
                       previous_allocation): the sum of |executed allocation change| per
                       bar (the function run_artifact.py calls, not a copy)
  direction_changes    sign flips of postRebalance_current_allocation; |a| <= FLAT_EPS is
                       flat and has no sign; a flat stretch is skipped, so long -> flat
                       -> short counts 1 and long -> flat -> long counts 0
  mean_abs_allocation  mean of |postRebalance_current_allocation|
  max_abs_allocation   max of |postRebalance_current_allocation|
Trade fields read every lot of trades.json (one row per LIFO-matched lot):
  trades               the number of lots
  gross_pct            100 * sum(profit_loss_absolute) / V0
  fees_pct             100 * sum(total_commission) / V0
  net_pct              100 * sum(net_profit_loss_absolute) / V0  (= gross_pct - fees_pct)
                       V0 = total_portfolio_value of the window's first bars.csv row, the
                       account at the window's start. Dollars summed, then divided once:
                       net_pct is the window's realised account change from closed lots:
                       it equals 100 * (E_end - V0) / V0, E_end = the last bars.csv row's
                       postRebalance_total_value (the account after the window's last
                       action; NOT its total_portfolio_value, the pre-rebalance value of
                       that bar). run_097 base: equal to rounding. These are the
                       dollars of run_artifact.py's core gross_pnl / fees_paid / net_pnl
                       in percent of V0.
  cost_drag_pct        (gross_pct - net_pct) / |gross_pct| * 100 = fees / |gross| * 100;
                       None when gross is 0. run_artifact.py's core cost_drag_pct formula
                       (the same number on each window)
  median_holding_bars  median of duration_minutes * 60 / step over the lots; step = the
                       median spacing of the window's bars.csv timestamps; None without lots
`total`: counts, turnover and the three *_pct summed over the cells (each window is its own
account); mean_abs_allocation over all bars pooled; max over all; cost_drag_pct from the
summed *_pct; median_holding_bars over all lots pooled.

Why not the per-lot percent fields: profit_loss_percent / net_profit_loss_percent /
total_commission_percent (trading-bot/performance/metrics.py CompletedTrade.to_dict) are
returns on the LOT's own entry notional, and the lots of one window range from about 2%
to 200% of the account (run_097 base). An unweighted sum ignores size; a sum weighted by
the lot's share of the account at entry does not compound and did not reconcile (run_097
base 2024-01: +6.5 against an account change of -2.4). They stay per-lot fields of the
analyst's trade_slice (trade_gross_return, trade_cost_pct), where a lot is the unit.

Why this cannot leak: post-run accounting. It reads only the run's own bars.csv and
trades.json, after the backtest wrote them; no figure is an input to any bar's
decision, and nothing outside the given window folders is opened.
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))           # strategy-research/tools/
_TBOT = os.path.join(os.path.dirname(os.path.dirname(_HERE)), "trading-bot")
for _p in (_HERE, _TBOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from performance.bar_equity import turnover as _turnover  # noqa: E402
from claim_tests import FLAT_EPS  # noqa: E402  (one definition of "flat")

BAR_COLUMNS = ("timestamp", "regime", "total_portfolio_value",
               "postRebalance_current_allocation", "previous_allocation")
TRADE_FIELDS = ("profit_loss_absolute", "total_commission", "net_profit_loss_absolute",
                "duration_minutes")
CELL_KEYS = ("n_bars", "trades", "turnover", "direction_changes", "mean_abs_allocation",
             "max_abs_allocation", "gross_pct", "fees_pct", "net_pct", "cost_drag_pct",
             "median_holding_bars")


def _r8(v):
    """A number at 8 significant digits (None for None / non-finite)."""
    if v is None:
        return None
    f = float(v)
    return float(f"{f:.8g}") if math.isfinite(f) else None


def direction_changes(alloc) -> int:
    """Sign flips of an allocation series, flat (|a| <= FLAT_EPS) skipped: a bar
    counts when its sign differs from the last non-flat bar's sign."""
    last, n = 0, 0
    for a in np.asarray(alloc, dtype=float):
        s = 0 if abs(a) <= FLAT_EPS else (1 if a > 0 else -1)
        if s == 0:
            continue
        if last and s != last:
            n += 1
        last = s
    return n


def _read_bars(path: Path):
    """(ready rows sorted by time, step seconds, V0) of one bars.csv."""
    import pandas as pd
    df = pd.read_csv(path, usecols=lambda c: c in BAR_COLUMNS)
    missing = set(BAR_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing column(s) {sorted(missing)}")
    if len(df) < 2:
        raise ValueError(f"{path}: fewer than 2 bars")
    ts = pd.to_datetime(df["timestamp"], utc=True)
    secs = (ts - pd.Timestamp(0, tz="UTC")).dt.total_seconds().to_numpy()
    df = df.assign(_ts=secs).sort_values("_ts")
    step = float(np.median(np.diff(df["_ts"].to_numpy())))
    if not step > 0:
        raise ValueError(f"{path}: bar spacing is not positive")
    v0 = float(df["total_portfolio_value"].iloc[0])
    if not (math.isfinite(v0) and v0 > 0):
        raise ValueError(f"{path}: the first row's total_portfolio_value is not positive")
    ready = df[df["regime"].astype(str).str.strip().str.upper() != "NOT_READY"]
    if ready[["postRebalance_current_allocation", "previous_allocation"]].isna().any().any():
        raise ValueError(f"{path}: NaN allocation among the ready bars")
    return ready, step, v0


def _read_trades(path: Path) -> list:
    trades = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(trades, list):
        raise ValueError(f"{path}: not a list of trades")
    for i, t in enumerate(trades):
        if not isinstance(t, dict):
            raise ValueError(f"{path}: trade {i} is not a mapping")
        for k in TRADE_FIELDS:
            v = t.get(k)
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                raise ValueError(f"{path}: trade {i} has no numeric {k}")
    return trades


def _cell(alloc: np.ndarray, n_flips: int, turnover: float, n_trades: int,
          gross: float, fees: float, net: float, holding: list) -> dict:
    a = np.abs(alloc)
    return {
        "n_bars": int(len(alloc)),
        "trades": int(n_trades),
        "turnover": _r8(turnover),
        "direction_changes": int(n_flips),
        "mean_abs_allocation": _r8(a.mean()) if len(a) else None,
        "max_abs_allocation": _r8(a.max()) if len(a) else None,
        "gross_pct": _r8(gross),
        "fees_pct": _r8(fees),
        "net_pct": _r8(net),
        "cost_drag_pct": _r8((gross - net) / abs(gross) * 100) if gross != 0 else None,
        "median_holding_bars": _r8(np.median(holding)) if holding else None,
    }


def window_economics(windows) -> dict:
    """{"windows": {"<symbol>/<window>": cell}, "total": cell} (fields: module docstring).

    `windows`: an iterable of (symbol, window label, folder), the folder holding that
    (coin, window) backtest's bars.csv and trades.json. Raises ValueError (or OSError)
    on a missing file or column, a non-numeric trade field, a NaN allocation among the
    ready bars, a non-positive starting account, two windows with one label, or no
    window at all."""
    out: dict = {}
    allocs, holds = [], []
    tot = {"turnover": 0.0, "flips": 0, "trades": 0, "gross": 0.0, "fees": 0.0, "net": 0.0}
    for symbol, window, folder in windows:
        label = f"{symbol}/{window}"
        if label in out:
            raise ValueError(f"window {label!r} given twice")
        folder = Path(folder)
        ready, step, v0 = _read_bars(folder / "bars.csv")
        trades = _read_trades(folder / "trades.json")
        alloc = ready["postRebalance_current_allocation"].to_numpy(dtype=float)
        turn = _turnover(ready["postRebalance_current_allocation"], ready["previous_allocation"])
        flips = direction_changes(alloc)
        gross = 100.0 * sum(t["profit_loss_absolute"] for t in trades) / v0
        fees = 100.0 * sum(t["total_commission"] for t in trades) / v0
        net = 100.0 * sum(t["net_profit_loss_absolute"] for t in trades) / v0
        holding = [t["duration_minutes"] * 60.0 / step for t in trades]
        out[label] = _cell(alloc, flips, turn, len(trades), gross, fees, net, holding)
        allocs.append(alloc)
        holds += holding
        for k, v in (("turnover", turn), ("flips", flips), ("trades", len(trades)),
                     ("gross", gross), ("fees", fees), ("net", net)):
            tot[k] += v
    if not out:
        raise ValueError("no window to read")
    return {"windows": out,
            "total": _cell(np.concatenate(allocs), tot["flips"], tot["turnover"], tot["trades"],
                           tot["gross"], tot["fees"], tot["net"], holds)}
