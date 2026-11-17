"""Chart files of a backtest record: the two small files the run viewer draws a backtest from (operator, 2026-11-17).

  python chart_files.py RECORD            writes RECORD/chart_bars.csv.gz and RECORD/chart_trades.csv.gz
  python chart_files.py --backfill        writes them for every committed backtest that is worth a chart and has its
                                          windows' files on disk; prints the counts

chart_bars.csv.gz: coin, window, timestamp, close, forecast, position, value: one row per bar of every window
(position = postRebalance_current_allocation, value = postRebalance_total_value; 6 significant digits, forecast 2
decimals). chart_trades.csv.gz: coin, window, entry_time, exit_time, direction, entry_price, exit_price,
realized_return (the trade's net return in percent, after fees). Written beside run.md, where git keeps them (the
windows' own files stay local: 04_backtest/.gitignore).

Worth a chart (the same rule for new backtests and for the backfill): confirmed by step 5, or profitable enough by
step 6. `run_idea` writes them after step 6 for such a backtest.

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


def write(record):
    """Write the record's two chart files; return (bars, trades) counts. A record without windows' files writes none."""
    record = Path(record)
    bars, trades = ["coin,window,timestamp,close,forecast,position,value"], [
        "coin,window,entry_time,exit_time,direction,entry_price,exit_price,realized_return"]
    files = sorted(record.glob("*/w*/bars.csv.gz"), key=lambda p: (p.parts[-3], int(p.parent.name[1:])))
    if not files:
        return 0, 0
    for f in files:
        coin, w = f.parts[-3], f.parent.name
        d = pd.read_csv(f, usecols=BAR_COLS)
        for t, c, fc, p, v in d.itertuples(index=False):
            bars.append(f"{coin},{w},{t},{g6(c)},{'' if fc != fc else f'{float(fc):.2f}'},{g6(p)},{g6(v)}")
        tj = f.parent / "trades.json.gz"
        for x in (json.loads(gzip.decompress(tj.read_bytes())) if tj.exists() else []):
            trades.append(f"{coin},{w},{x.get('entry_time')},{x.get('exit_time')},{x.get('side')},"
                          f"{g6(x.get('entry_price'))},{g6(x.get('exit_price'))},{g6(x.get('net_profit_loss_percent'))}")
    (record / "chart_bars.csv.gz").write_bytes(_gz("\n".join(bars) + "\n"))
    (record / "chart_trades.csv.gz").write_bytes(_gz("\n".join(trades) + "\n"))
    return len(bars) - 1, len(trades) - 1


def worth_a_chart(verdict, check):
    """Confirmed by step 5, or profitable enough by step 6 (their result.json files; a missing file says nothing)."""
    st = json.loads(Path(verdict).read_text()).get("status") if Path(verdict).exists() else None
    pr = json.loads(Path(check).read_text()).get("status") if Path(check).exists() else None
    return st == "confirmed" or pr == "profitable enough"


def backfill(root=STEPS):
    done, no_files, size = [], [], 0
    for v in sorted(root.glob("05_verification/*_run/verdicts/*/result.json")):
        run, rid = v.parts[-4], v.parent.name
        if not worth_a_chart(v, root / "06_profitability" / run / "checks" / rid / "result.json"):
            continue
        rec = root / "04_backtest" / run / "backtests" / rid
        nb, nt = write(rec)
        if nb:
            done.append(rid)
            size += sum((rec / n).stat().st_size for n in ("chart_bars.csv.gz", "chart_trades.csv.gz"))
        else:
            no_files.append(f"{run}/{rid}")
    print(f"chart files written: {len(done)} backtests, {size / 1024 / 1024:.1f} MB; worth a chart but no windows' "
          f"files on disk: {len(no_files)}")
    for x in no_files:
        print(f"  no files: {x}")
    return done, no_files


def main():
    a = argparse.ArgumentParser()
    a.add_argument("record", type=Path, nargs="?")
    a.add_argument("--backfill", action="store_true")
    args = a.parse_args()
    if args.backfill:
        backfill()
    elif args.record:
        nb, nt = write(args.record)
        print(f"chart files: {nb} bars, {nt} trades" if nb else "chart files: no windows' files in the record")
    else:
        sys.exit("give a record, or --backfill")


if __name__ == "__main__":
    main()
