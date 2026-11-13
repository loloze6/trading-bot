"""Step 6: profitability check. Reads one backtest record and applies the rule (rule.yaml) to the book the backtest
traded, after the backtest's own costs. It calculates only: no trade is rebuilt, no cost is computed, nothing is
measured on the prices beyond holding the same coins. No model call.

  python check_profitability.py path/to/04_backtest/backtests/<record>
Option: --checks-dir (default: ../checks next to this folder).

Definitions (the same for every backtest):
- The book of one coin in one window: the backtest's value after each rebalance and its fees
  (`postRebalance_total_value`), read at the last bar of each UTC day. Its daily returns stay inside the window.
- The backtest's book: every coin together, equal weight: on each day of a window, the mean of the daily returns of
  the coins that have that day. Holding: the same, from the coins' closing prices.
- Sharpe: mean over standard deviation of all the daily returns of all windows, times sqrt(365).
- Calmar: the annualised return of all the daily returns chained in window order, divided by the deepest fall of
  that chained curve. No fall and a positive return passes.
- Leave one window out: the Sharpe without the days of one window (the same window number for every coin, so the
  same period); the lowest over all windows.
- Trades per bar: the backtest's trades, without those closed on a window's last bar (a forced close), divided by
  the number of bars, every coin and window together.
"""
import argparse, gzip, json, math, os, re, sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[1]
MEASURES = [  # (rule key, label, comparison)
    ("sharpe_min", "Sharpe", "above"),
    ("sharpe_vs_hold_min", "Sharpe minus holding's Sharpe", "above"),
    ("avg_daily_return_min", "Mean daily return", "at least"),
    ("leave_one_window_out_sharpe_min", "Lowest Sharpe, one window left out", "above"),
    ("calmar_min", "Calmar", "above"),
    ("trade_frequency_min", "Trades per bar", "at least"),
]


def write_atomic(path, text):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def sharpe(r):
    r = np.asarray(r, float)
    if len(r) < 2 or r.std(ddof=1) == 0:
        return 0.0
    return float(r.mean() / r.std(ddof=1) * math.sqrt(365))


def daily(series, ts):
    """Daily returns from a per-bar series: its value at the last bar of each UTC day, returns between days."""
    s = pd.Series(series.to_numpy(float), index=pd.to_datetime(ts, utc=True))
    closes = s.groupby(s.index.normalize()).last()
    return closes.pct_change().dropna()


def load(record):
    """Per window: the equal-weight daily returns of the book and of holding; and the trade and bar counts."""
    book, hold, trades, bars, coins = {}, {}, 0, 0, []
    for coin in sorted(p for p in record.iterdir() if p.is_dir()):
        wins = sorted(coin.glob("w*/bars.csv.gz"), key=lambda p: int(p.parent.name[1:]))
        if not wins:
            continue
        coins.append(coin.name)
        for f in wins:
            w = int(f.parent.name[1:])
            d = pd.read_csv(f, usecols=["timestamp", "close", "postRebalance_total_value"])
            book.setdefault(w, []).append(daily(d["postRebalance_total_value"], d["timestamp"]).rename(coin.name))
            hold.setdefault(w, []).append(daily(d["close"], d["timestamp"]).rename(coin.name))
            bars += len(d)
            last = pd.to_datetime(d["timestamp"].iloc[-1])
            with gzip.open(f.parent / "trades.json.gz", "rt") as g:
                t = json.load(g)
            trades += sum(1 for x in t if pd.to_datetime(x["exit_time"]) != last)   # a close on the last bar is forced
    eq = lambda parts: {w: pd.concat(v, axis=1, sort=True).mean(axis=1) for w, v in parts.items()}
    return eq(book), eq(hold), trades, bars, coins


def check(record, rule, target_vol=None):
    book, hold, trades, bars, coins = load(record)
    windows = sorted(book)
    r = np.concatenate([book[w].to_numpy() for w in windows])
    if target_vol:   # overnight test: one common risk level (the book's daily returns scaled to a yearly volatility)
        vol = r.std(ddof=1) * math.sqrt(365)
        if vol > 0:
            r = r * (target_vol / vol)
            book = {w: book[w] * (target_vol / vol) for w in windows}
    h = np.concatenate([hold[w].to_numpy() for w in windows])
    curve = np.cumprod(1 + r)
    years = len(r) / 365
    ann = curve[-1] ** (1 / years) - 1 if years > 0 and curve[-1] > 0 else -1.0
    fall = float(np.max(1 - curve / np.maximum.accumulate(np.concatenate([[1.0], curve]))[1:]))
    calmar = math.inf if fall == 0 and ann > 0 else (ann / fall if fall > 0 else 0.0)
    loo = {w: sharpe(np.concatenate([book[x].to_numpy() for x in windows if x != w])) for w in windows}
    v = {
        "sharpe_min": sharpe(r),
        "sharpe_vs_hold_min": sharpe(r) - sharpe(h),
        "avg_daily_return_min": float(r.mean()),
        "leave_one_window_out_sharpe_min": min(loo.values()),
        "calmar_min": calmar,
        "trade_frequency_min": trades / bars if bars else 0.0,
    }
    rows = []
    for key, label, cmp in MEASURES:
        ok = v[key] > rule[key] if cmp == "above" else v[key] >= rule[key]
        rows.append({"measure": key, "label": label, "value": v[key], "threshold": rule[key], "comparison": cmp, "passed": bool(ok)})
    facts = {"coins": coins, "windows": len(windows), "days": int(len(r)), "years": round(years, 2), "bars": bars,
             "trades": trades, "holding_sharpe": sharpe(h), "annualised_return": float(ann), "deepest_fall": fall,
             "worst_window_left_out": f"w{min(loo, key=loo.get)}"}
    return rows, facts


def fmt(x):
    if isinstance(x, float):
        return "inf" if math.isinf(x) else f"{x:.4g}"
    return str(x)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("record", type=Path, help="one backtest record folder")
    a.add_argument("--checks-dir", type=Path, default=HERE.parent / "checks")
    a.add_argument("--target-vol", type=float, default=None, help="overnight test: scale the book to this yearly volatility first (for example 0.2)")
    args = a.parse_args()

    record = args.record.resolve()
    rid = record.name
    rule = yaml.safe_load((HERE / "rule.yaml").read_text())
    out_dir = args.checks_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / "INDEX.md"

    def index_line(line):
        lines = [l for l in (index_path.read_text().splitlines() if index_path.exists() else []) if not l.startswith(rid + ":")]
        write_atomic(index_path, "".join(l + "\n" for l in sorted(lines + [line])))

    if not list(record.glob("*/w*/bars.csv.gz")):
        index_line(f"{rid}: not checked: the record holds no window that ran")
        print(f"{rid}: not checked (no window ran)")
        return
    data = next((l[len("- Data: "):] for l in (record / "run.md").read_text().splitlines() if l.startswith("- Data: ")), "") \
        if (record / "run.md").exists() else ""

    rows, facts = check(record, rule, args.target_vol)
    ok = all(x["passed"] for x in rows)
    decided = "every measure passed" if ok else "failed: " + "; ".join(x["label"] for x in rows if not x["passed"])
    status = "profitable enough" if ok else "not profitable enough"
    d = out_dir / rid
    d.mkdir(parents=True, exist_ok=True)
    write_atomic(d / "result.json", json.dumps({"status": status, "measures": rows, "decided_by": decided},
                                               indent=2, default=str) + "\n")
    lines = ["---", f"backtest: {rid}", f"data: {data}", f"status: {status}", "---",
             "| Measure | Value | Rule | Passed |", "|---|---|---|---|"]
    lines += [f"| {x['label']} | {fmt(x['value'])} | {x['comparison']} {fmt(x['threshold'])} | {'yes' if x['passed'] else 'no'} |" for x in rows]
    lines += ["", f"- Decided by: {decided}",
              f"Record: `steps_cards/{os.path.relpath(record, STEPS)}`", "Rule: `steps_cards/06_profitability/helper/rule.yaml`"]
    write_atomic(d / "check.md", "\n".join(lines) + "\n")
    summary = "; ".join(f"{x['label']} {fmt(x['value'])}" for x in rows[:2] + rows[4:5])
    index_line(f"{rid}: {status} [{summary}]")
    print(f"{rid}: {status} ({decided})")


if __name__ == "__main__":
    main()
