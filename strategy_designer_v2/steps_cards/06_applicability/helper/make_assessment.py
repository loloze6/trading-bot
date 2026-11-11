"""Applicability helper, step 6. Reads one idea's step 5 verdict and its backtest record, and applies the rule
(rule.yaml) to the book the backtest traded, after the backtest's own costs. It calculates only: no trade is rebuilt,
no cost is computed, nothing is measured on the prices beyond holding the coin. No model call.

  python make_assessment.py path/to/PLAN.md
Options: --records-root (default: ../../04_backtest/backtests), --verdicts-dir (default: ../../05_verification/verdicts),
--assessments-dir (default: ../assessments), --any-verdict (exercises only: assess an idea whose verdict is not
"confirmed"; the assessment says so).

Definitions (one for every idea):
- The book of one coin in one window: the backtest's value after each rebalance and its fees
  (`postRebalance_total_value`), read at the last bar of each UTC day. Its daily returns stay inside the window.
- The idea's book: every coin together, equal weight: on each day of a window, the mean of the daily returns of the
  coins that have that day. Holding: the same, from the coins' closing prices.
- Sharpe: mean over standard deviation of all the daily returns of all windows, times sqrt(365).
- Calmar: the annualised return of all the daily returns chained in window order, divided by the deepest fall of
  that chained curve. No fall and a positive return passes.
- Leave one window out: the Sharpe without the days of one window (the same window number for every coin, so the
  same period); the lowest over all windows.
- Trade frequency: the backtest's trades, without those closed on a window's last bar (a forced close), divided by
  the number of bars, every coin and window together.
"""
import argparse, gzip, json, math, os, re, sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[1]
BARS = [  # (rule key, label, comparison)
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


def header(text):
    m = re.match(r"\s*---\n(.*?)---\n", text, re.S)
    return {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)} if m else {}


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


def assess(record, rule):
    book, hold, trades, bars, coins = load(record)
    windows = sorted(book)
    r = np.concatenate([book[w].to_numpy() for w in windows])
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
    for key, label, cmp in BARS:
        ok = v[key] > rule[key] if cmp == "above" else v[key] >= rule[key]
        rows.append({"bar": key, "label": label, "value": v[key], "threshold": rule[key], "comparison": cmp, "passed": bool(ok)})
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
    a.add_argument("plan", type=Path)
    a.add_argument("--records-root", type=Path, default=STEPS / "04_backtest" / "backtests")
    a.add_argument("--verdicts-dir", type=Path, default=STEPS / "05_verification" / "verdicts")
    a.add_argument("--assessments-dir", type=Path, default=HERE.parent / "assessments")
    a.add_argument("--any-verdict", action="store_true", help="exercises only: assess whatever the verdict")
    args = a.parse_args()

    plan_path = args.plan.resolve()
    plan_id = plan_path.stem
    h = header(plan_path.read_text())
    rule = yaml.safe_load((HERE / "rule.yaml").read_text())
    out_dir = args.assessments_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / "INDEX.md"

    def index_line(line):
        lines = [l for l in (index_path.read_text().splitlines() if index_path.exists() else []) if not l.startswith(plan_id + ":")]
        write_atomic(index_path, "".join(l + "\n" for l in sorted(lines + [line])))

    vfile = args.verdicts_dir.resolve() / plan_id / "result.json"
    verdict = json.loads(vfile.read_text())["status"] if vfile.exists() else "none"
    record = args.records_root.resolve() / plan_id
    if verdict != "confirmed" and not args.any_verdict:
        index_line(f"{plan_id}: not assessed: the verdict is {verdict}")
        print(f"{plan_id}: not assessed (verdict {verdict})")
        return
    if not list(record.glob("*/w*/bars.csv.gz")):
        index_line(f"{plan_id}: not assessed: no backtest record")
        print(f"{plan_id}: not assessed (no backtest record)")
        return

    rows, facts = assess(record, rule)
    worth = all(x["passed"] for x in rows)
    failed = [x["label"] for x in rows if not x["passed"]]
    decided = "every bar of the rule passed" if worth else "failed: " + "; ".join(failed)
    status = "worth acting on" if worth else "not worth acting on"
    d = out_dir / plan_id
    d.mkdir(parents=True, exist_ok=True)
    write_atomic(d / "result.json", json.dumps({"status": status, "verdict": verdict, "bars": rows, "facts": facts,
                                                "decided_by": decided}, indent=2, default=str) + "\n")
    lines = ["---", f"plan: {plan_id}", f"idea: {h.get('idea', '')}", f"fit: {h.get('fit', 'not given')}",
             f"verdict: {verdict}" + ("" if verdict == "confirmed" else " (exercise: assessed although not confirmed)"),
             f"status: {status}", "---",
             "Acting on it: trading the idea on its own, as the backtest traded it, after the backtest's own costs.",
             "", "| Bar | Value | Rule | Passed |", "|---|---|---|---|"]
    lines += [f"| {x['label']} | {fmt(x['value'])} | {x['comparison']} {fmt(x['threshold'])} | {'yes' if x['passed'] else 'no'} |" for x in rows]
    lines += ["", f"- Decided by: {decided}",
              f"- Book: {', '.join(facts['coins'])}, equal weight; {facts['windows']} windows, {facts['days']} days "
              f"({facts['years']} years); {facts['trades']} trades on {facts['bars']} bars",
              f"- Holding's Sharpe: {fmt(facts['holding_sharpe'])}; annualised return: {fmt(facts['annualised_return'])}; "
              f"deepest fall: {fmt(facts['deepest_fall'])}; window whose removal lowers the Sharpe most: {facts['worst_window_left_out']}",
              f"Record: `steps_cards/{os.path.relpath(record, STEPS)}`", "Rule: `steps_cards/06_applicability/helper/rule.yaml`"]
    write_atomic(d / "assessment.md", "\n".join(lines) + "\n")
    summary = "; ".join(f"{x['label']} {fmt(x['value'])}" for x in rows[:2] + rows[4:5])
    index_line(f"{plan_id}: {status}{'' if verdict == 'confirmed' else ' (exercise, verdict ' + verdict + ')'} [{summary}]")
    print(f"{plan_id}: {status} ({decided})")


if __name__ == "__main__":
    main()
