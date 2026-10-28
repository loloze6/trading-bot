"""PR-B (analyst tools, 2026-10-19): the economics of one variant, per (coin, window) --
ONE definition, shared by the analyst's `window_economics` query
(QueryEngine.window_economics, the analyst's query engine) and the per-variant
`window_economics` object stored beside `forecast_shape` in
artifacts/profit_bars_evaluation.yaml (workflow/run_phase1_research.py, under
orchestrator.analyst.enabled). Each caller resolves its own window folders (with
its own path checks) and hands over each window's `core` block from
protocol_result.yaml (`results[i]["core"]`); this module reads the `bars.csv`,
`trades.json` and `metrics.json` of the folders it is given. A pure module: no SDK, no
network, writes nothing.

Operator ruling 2026-10-19 (item 4): READ the run's own figures, do not recompute them.
Per window, trades / gross / net / fees / cost drag / average trade duration are the
`core` block's (trading-bot/reporting/run_artifact.py build_core), turnover is
metrics.json's `bar_equity.turnover` (run_artifact.py build_bar_equity); a percent of the
window's starting equity is a conversion of the read dollars, nothing else. Only
direction_changes, mean and max absolute allocation and median_holding_bars are computed.

Per (coin, window) cell, keyed `<symbol>/<window>`; `total` pools every cell
-------------------------------------------------------------------------
READ (a window whose figure is absent -- no `core` block, an older run, no metrics.json --
carries None for it; nothing is recomputed in its place):
  trades                 core.trade_count (count of completed LIFO lots)
  gross_pct              100 * core.gross_pnl / V0   (core.gross_pnl: dollars, before commission)
  fees_pct               100 * core.fees_paid / V0   (dollars)
  net_pct                100 * core.net_pnl / V0     (dollars, after commission)
                         V0 = total_portfolio_value of the window's first bars.csv row, the
                         account at the window's start; a dollar figure divided once by V0.
  cost_drag_pct          core.cost_drag_pct verbatim ((gross - net) / |gross| * 100 as the run
                         computed it; None when the run's gross was 0)
  avg_trade_duration_bars  core.avg_trade_duration_bars verbatim (mean trade duration / median
                         bar spacing, in bars)
  turnover               metrics.json bar_equity.turnover verbatim (the sum of |executed
                         allocation change| per ready bar; allocation units)
COMPUTED from the window's own files:
  n_bars               the bars bars.csv has with regime != NOT_READY (stripped, upper case) --
                       the rows build_bar_equity counts
  direction_changes    sign flips of postRebalance_current_allocation; |a| <= FLAT_EPS is
                       flat and has no sign; a flat stretch is skipped, so long -> flat
                       -> short counts 1 and long -> flat -> long counts 0
  mean_abs_allocation  mean of |postRebalance_current_allocation|
  max_abs_allocation   max of |postRebalance_current_allocation|
  median_holding_bars  median of duration_minutes * 60 / step over the lots of trades.json;
                       step = the median spacing of the window's bars.csv timestamps; None
                       without lots
DERIVED from the cell's own figures above (D-168, 2026-10-21; None when an input is None):
  fees_pct_annualised  fees_pct x 365 / n_bars (percent of the starting account per 365 bars
                       of the window)
  gross_per_lot_pct    gross_pct / trades (mean over the window's lots, percent of the starting
                       account; None without lots)
  fees_per_lot_pct     fees_pct / trades (the same, for fees)
  turnover_annualised  turnover x 365 / n_bars
  cost_drag_pct        reported only when abs(gross_pct) >= 5 x fees_pct; otherwise None and
                       cost_drag_note = "cost_drag_pct not reported: |gross| under 5x fees (D-168)"
                       (cost_drag_note is None otherwise; a cell with no gross or no fees figure
                       cannot be judged and keeps the read cost_drag_pct)
`total`: trades, turnover, direction_changes and the three *_pct summed over the cells (each
window is its own account) -- None when any cell's figure is None; cost_drag_pct from the
SUMMED READ DOLLARS, (sum gross - sum net) / |sum gross| * 100 (the run's own formula on
the summed dollars; None when the sum is 0 or any cell lacks a figure);
avg_trade_duration_bars the mean of the cells' averages weighted by their trade_count (the
pooled mean; windows without trades have no average and no weight); mean_abs_allocation
over all bars pooled; max over all; median_holding_bars over all lots pooled. The derived
fields of `total` are the same formulas on the total's figures (summed percents, summed trades
and turnover, pooled bars), and its cost_drag_pct passes the same 5 x fees_pct test on the
summed percents.

Why not the per-lot percent fields: profit_loss_percent / net_profit_loss_percent /
total_commission_percent (trading-bot/performance/metrics.py CompletedTrade.to_dict) are
returns on the LOT's own entry notional, and the lots of one window range from about 2%
to 200% of the account (one saved run); the run's dollar totals are the reconciled basis.
They stay per-lot fields of the analyst's trade_slice (trade_gross_return, trade_cost_pct),
where a lot is the unit.

Why this cannot leak: post-run accounting. It reads only the run's own protocol_result core
block and the bars.csv, trades.json and metrics.json of the given window folders, after the
backtest wrote them; no figure is an input to any bar's decision, and nothing outside the
given window folders is opened.
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

from claim_tests import FLAT_EPS  # noqa: E402  (one definition of "flat")

BAR_COLUMNS = ("timestamp", "regime", "total_portfolio_value",
               "postRebalance_current_allocation", "previous_allocation")
TRADE_FIELDS = ("duration_minutes",)
CELL_KEYS = ("n_bars", "trades", "turnover", "direction_changes", "mean_abs_allocation",
             "max_abs_allocation", "gross_pct", "fees_pct", "net_pct", "cost_drag_pct",
             "avg_trade_duration_bars", "median_holding_bars",
             "fees_pct_annualised", "gross_per_lot_pct", "fees_per_lot_pct",
             "turnover_annualised", "cost_drag_note")
#: D-168: bars per "year" of the annualised figures (365 bars of the window, as the operator
#: wrote it; a year on a daily timeframe)
ANNUALISE_BARS = 365
#: D-168: cost_drag_pct is reported only when abs(gross_pct) >= COST_DRAG_MIN_GROSS_X x fees_pct
COST_DRAG_MIN_GROSS_X = 5
COST_DRAG_NOTE = "cost_drag_pct not reported: |gross| under 5x fees (D-168)"


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


def result_cores(protocol_result) -> dict:
    """{str(run_id): core} of every protocol_result `results[]` entry that has a run_id; the
    core is the entry's `core` block (a dict), or None when absent / not a mapping. Keyed by
    run_id so a caller pairs a window folder (variants/<vid>/results/<run_id>/) with its own
    core whatever the order of the entries."""
    out = {}
    for entry in (protocol_result or {}).get("results") or []:
        if not isinstance(entry, dict) or not entry.get("run_id"):
            continue
        core = entry.get("core")
        out[str(entry["run_id"])] = core if isinstance(core, dict) else None
    return out


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


def _num(src, key: str, where: str):
    """src[key] as a float; None when src is not a mapping or the key is absent / None
    (the figure was not recorded); ValueError when it is present but not a finite number."""
    if not isinstance(src, dict):
        return None
    v = src.get(key)
    if v is None:
        return None
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(f"{where}: {key} is not a finite number ({v!r})")
    return float(v)


def _read_turnover(folder: Path):
    """metrics.json bar_equity.turnover of the window folder, verbatim; None when the file or
    the bar_equity block / its turnover is absent (a run made without bar_equity)."""
    path = folder / "metrics.json"
    if not path.is_file():
        return None
    doc = json.loads(path.read_text(encoding="utf-8"))
    be = doc.get("bar_equity") if isinstance(doc, dict) else None
    return _num(be, "turnover", f"{path}: bar_equity")


def _read_core(core, v0: float, where: str) -> dict:
    """The figures a window reads from its protocol_result `core` block: dollars (for the
    total) and the cell's read fields. A missing block or key is None throughout."""
    gross, fees, net = (_num(core, k, where) for k in ("gross_pnl", "fees_paid", "net_pnl"))
    pct = (lambda d: None if d is None else 100.0 * d / v0)
    n = _num(core, "trade_count", where)
    return {"gross_usd": gross, "fees_usd": fees, "net_usd": net,
            "gross": pct(gross), "fees": pct(fees), "net": pct(net),
            "trades": None if n is None else int(n),
            "cost_drag": _num(core, "cost_drag_pct", where),
            "avg_dur": _num(core, "avg_trade_duration_bars", where)}


def _per_bars(value, n_bars: int):
    """value per ANNUALISE_BARS bars of the window (None when the value or the bars are None / 0)."""
    return None if value is None or not n_bars else value * ANNUALISE_BARS / n_bars


def _per_lot(value, trades):
    """The mean over the window's lots of a figure summed over them (None without a figure or lots)."""
    return None if value is None or not trades else value / trades


def _cost_drag_gate(read: dict):
    """(cost_drag value, note): the read cost drag only when abs(gross_pct) >= 5 x fees_pct,
    else None with COST_DRAG_NOTE. A window with no gross or no fees figure cannot be judged and
    keeps what the run recorded, unchanged."""
    gross, fees = read["gross"], read["fees"]
    if gross is None or fees is None or abs(gross) >= COST_DRAG_MIN_GROSS_X * fees:
        return read["cost_drag"], None
    return None, COST_DRAG_NOTE


def _cell(alloc: np.ndarray, n_flips: int, read: dict, turnover, holding: list) -> dict:
    a = np.abs(alloc)
    cost_drag, cost_drag_note = _cost_drag_gate(read)
    return {
        "n_bars": int(len(alloc)),
        "trades": read["trades"],
        "turnover": _r8(turnover),
        "direction_changes": int(n_flips),
        "mean_abs_allocation": _r8(a.mean()) if len(a) else None,
        "max_abs_allocation": _r8(a.max()) if len(a) else None,
        "gross_pct": _r8(read["gross"]),
        "fees_pct": _r8(read["fees"]),
        "net_pct": _r8(read["net"]),
        "cost_drag_pct": _r8(cost_drag),
        "avg_trade_duration_bars": _r8(read["avg_dur"]),
        "median_holding_bars": _r8(np.median(holding)) if holding else None,
        "fees_pct_annualised": _r8(_per_bars(read["fees"], len(alloc))),
        "gross_per_lot_pct": _r8(_per_lot(read["gross"], read["trades"])),
        "fees_per_lot_pct": _r8(_per_lot(read["fees"], read["trades"])),
        "turnover_annualised": _r8(_per_bars(turnover, len(alloc))),
        "cost_drag_note": cost_drag_note,
    }


def _sum_or_none(values):
    """The sum of the values, or None when any is None."""
    return None if any(v is None for v in values) else sum(values)


def _total_read(reads: list, turnovers: list) -> dict:
    """The `total` cell's read fields from the cells' read figures (see the module docstring)."""
    gross_usd, net_usd = _sum_or_none([r["gross_usd"] for r in reads]), \
        _sum_or_none([r["net_usd"] for r in reads])
    cost_drag = None
    if gross_usd is not None and net_usd is not None and gross_usd != 0:
        cost_drag = (gross_usd - net_usd) / abs(gross_usd) * 100
    trades = _sum_or_none([r["trades"] for r in reads])
    avg_dur = None
    if trades:
        weighted = [(r["trades"], r["avg_dur"]) for r in reads if r["trades"]]
        if all(d is not None for _n, d in weighted):
            avg_dur = sum(n * d for n, d in weighted) / sum(n for n, _d in weighted)
    return {"trades": trades,
            "gross": _sum_or_none([r["gross"] for r in reads]),
            "fees": _sum_or_none([r["fees"] for r in reads]),
            "net": _sum_or_none([r["net"] for r in reads]),
            "cost_drag": cost_drag, "avg_dur": avg_dur,
            "turnover": _sum_or_none(turnovers)}


def window_economics(windows) -> dict:
    """{"windows": {"<symbol>/<window>": cell}, "total": cell} (fields: module docstring).

    `windows`: an iterable of (symbol, window label, folder, core), the folder holding that
    (coin, window) backtest's bars.csv, trades.json and metrics.json, and core the window's
    `results[i]["core"]` block of protocol_result.yaml (None when it has none: the read
    figures are then None). Raises ValueError (or OSError) on a missing bars.csv or
    trades.json, a missing column, a non-numeric duration or core figure, a NaN allocation
    among the ready bars, a non-positive starting account, two windows with one label, or no
    window at all."""
    out: dict = {}
    allocs, holds, reads, turnovers = [], [], [], []
    flips_total = 0
    for symbol, window, folder, core in windows:
        label = f"{symbol}/{window}"
        if label in out:
            raise ValueError(f"window {label!r} given twice")
        folder = Path(folder)
        ready, step, v0 = _read_bars(folder / "bars.csv")
        trades = _read_trades(folder / "trades.json")
        alloc = ready["postRebalance_current_allocation"].to_numpy(dtype=float)
        flips = direction_changes(alloc)
        read = _read_core(core, v0, f"{label}: core")
        turn = _read_turnover(folder)
        holding = [t["duration_minutes"] * 60.0 / step for t in trades]
        out[label] = _cell(alloc, flips, read, turn, holding)
        allocs.append(alloc)
        holds += holding
        reads.append(read)
        turnovers.append(turn)
        flips_total += flips
    if not out:
        raise ValueError("no window to read")
    tot = _total_read(reads, turnovers)
    return {"windows": out,
            "total": _cell(np.concatenate(allocs), flips_total, tot, tot["turnover"], holds)}
