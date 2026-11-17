"""Chart files of a backtest record: the two small files the run viewer draws a backtest from (operator, 2026-11-17).

  python chart_files.py RECORD [--local]  writes RECORD/chart_bars.csv.gz and RECORD/chart_trades.csv.gz (with --local:
                                          chart_bars.local.csv.gz and chart_trades.local.csv.gz)
  python chart_files.py --backfill        writes them for every backtest that has its windows' files on disk, under the
                                          name its worth gives; prints the counts

chart_bars.csv.gz: coin, window, timestamp, close, forecast, position, value: one row per bar of every window
(position = postRebalance_current_allocation, value = postRebalance_total_value; 6 significant digits, forecast 2
decimals). chart_trades.csv.gz: coin, window, entry_time, exit_time, direction, entry_price, exit_price,
realized_return (the trade's net return in percent, after fees). Written beside run.md.

Every backtest gets its chart files (operator, 2026-11-17: on the PC, size does not matter); their name says whether git
keeps them. A backtest worth a chart (confirmed by step 5, or profitable enough by step 6) gets chart_bars.csv.gz and
chart_trades.csv.gz, committed; any other gets chart_bars.local.csv.gz and chart_trades.local.csv.gz, which git ignores
(04_backtest/.gitignore): they stay on the disk where the run happened. `run_idea` writes them after step 6; the viewer
reads the committed name first, then the local one.

Why this cannot leak: display files written after the backtest, from its own output; no step reads them.
"""
import argparse, gzip, json, sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[1]
BAR_COLS = ["timestamp", "close", "forecast", "postRebalance_current_allocation", "postRebalance_total_value"]


def g6(x):
    return "" if x is None or x != x else f"{float(x):.6g}"


def _gz(text):
    return gzip.compress(text.encode(), mtime=0)            # the same bytes for the same rows


NAMES = {False: ("chart_bars.csv.gz", "chart_trades.csv.gz"), True: ("chart_bars.local.csv.gz", "chart_trades.local.csv.gz")}


def write(record, local=False):
    """Write the record's two chart files, under the committed names or the local ones; remove the other names' files
    (a backtest has one pair). Return (bars, trades) counts. A record without windows' files writes none."""
    record = Path(record)
    bars, trades = ["coin,window,timestamp,close,forecast,position,value"], [
        "coin,window,entry_time,exit_time,direction,entry_price,exit_price,realized_return"]
    files = sorted(record.glob("*/w*/bars.csv.gz"), key=lambda p: (p.parts[-3], int(p.parent.name[1:])))
    if not files:
        return 0, 0
    for f in files:
        coin, w = f.parts[-3], f.parent.name
        d = pd.read_csv(f, usecols=BAR_COLS)[BAR_COLS]       # usecols keeps the file's own order: put them in ours
        for t, c, fc, p, v in d.itertuples(index=False):
            bars.append(f"{coin},{w},{t},{g6(c)},{'' if fc != fc else f'{float(fc):.2f}'},{g6(p)},{g6(v)}")
        tj = f.parent / "trades.json.gz"
        for x in (json.loads(gzip.decompress(tj.read_bytes())) if tj.exists() else []):
            trades.append(f"{coin},{w},{x.get('entry_time')},{x.get('exit_time')},{x.get('side')},"
                          f"{g6(x.get('entry_price'))},{g6(x.get('exit_price'))},{g6(x.get('net_profit_loss_percent'))}")
    nb, nt = NAMES[local]
    (record / nb).write_bytes(_gz("\n".join(bars) + "\n"))
    (record / nt).write_bytes(_gz("\n".join(trades) + "\n"))
    for other in NAMES[not local]:
        (record / other).unlink(missing_ok=True)
    return len(bars) - 1, len(trades) - 1


def worth_a_chart(verdict, check):
    """Confirmed by step 5, or profitable enough by step 6 (their result.json files; a missing file says nothing)."""
    st = json.loads(Path(verdict).read_text()).get("status") if Path(verdict).exists() else None
    pr = json.loads(Path(check).read_text()).get("status") if Path(check).exists() else None
    return st == "confirmed" or pr == "profitable enough"


def backfill(root=STEPS):
    counts, no_files = {False: [0, 0], True: [0, 0]}, []
    for v in sorted(root.glob("05_verification/*_run/verdicts/*/result.json")):
        run, rid = v.parts[-4], v.parent.name
        local = not worth_a_chart(v, root / "06_profitability" / run / "checks" / rid / "result.json")
        rec = root / "04_backtest" / run / "backtests" / rid
        nb, nt = write(rec, local)
        if nb:
            counts[local][0] += 1
            counts[local][1] += sum((rec / n).stat().st_size for n in NAMES[local])
        else:
            no_files.append(f"{run}/{rid}")
    for local, label in ((False, "committed (worth a chart)"), (True, "local only")):
        print(f"chart files, {label}: {counts[local][0]} backtests, {counts[local][1] / 1024 / 1024:.1f} MB")
    print(f"backtests without their windows' files on disk: {len(no_files)}")
    return counts, no_files


def main():
    a = argparse.ArgumentParser()
    a.add_argument("record", type=Path, nargs="?")
    a.add_argument("--backfill", action="store_true")
    a.add_argument("--local", action="store_true", help="the local names (a backtest not worth a chart)")
    args = a.parse_args()
    if args.backfill:
        backfill()
    elif args.record:
        nb, nt = write(args.record, args.local)
        print(f"chart files: {nb} bars, {nt} trades" if nb else "chart files: no windows' files in the record")
    else:
        sys.exit("give a record, or --backfill")


if __name__ == "__main__":
    main()
