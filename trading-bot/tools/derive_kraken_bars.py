"""Derive longer Kraken bars (local_data/kraken_<PAIR>_4h.csv) from the cached hourly ones (kraken_<PAIR>_1h.csv).

A data tool (local_data/README.md, "Coverage"): it reads the local hourly files only (never an exchange, never
local_data/holdout_sealed/), writes one file per pair beside them, and records in local_data/coverage.yaml the days
the new file covers (those of the hourly file it came from).

A bar of N hours is the block of N consecutive hours that starts at a UTC hour divisible by N (4h: 00, 04, 08, 12,
16, 20 UTC; 24h: the UTC day), built from the hourly bars inside the block:
    open = the first hour's open, high = the highest high, low = the lowest low, close = the last hour's close,
    volume = the sum of the volumes, number_of_trades = the sum of the trade counts,
    quote_asset_volume = volume x close (the convention of the archive files, tools/ingest_kraken_archive.py),
    timestamp = the block's start (the hourly files' convention: a bar is stamped with its opening time),
    close_time = the block's end less one millisecond.
A block with no hourly bar (no trade in N hours) has no row, as Kraken leaves out the hours without a trade. A block
past the hourly file's covered days is not written.

  python tools/derive_kraken_bars.py [--hours 4] [--pairs BTCUSD ETHUSD] [--dry-run]
  python tools/derive_kraken_bars.py --compare-daily      # the proof: 24h blocks against the Kraken daily files

Why this can't leak: every derived bar is stamped with its opening time and holds only the hours inside it, so a
bar's close is known at its close_time, the same as a Kraken 4h bar; the engine hands each bar's decision the rows up
to that bar. The tool reads no data the hourly files do not hold and writes nothing past their covered days.
"""
import argparse, csv, datetime as dt, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data import coverage  # noqa: E402  (the days each file was fetched for)

DATA = Path(__file__).resolve().parents[1] / "local_data"
HEADER = ["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
          "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]
FMT = "%Y-%m-%d %H:%M:%S"


def block_start(ts, hours):
    """The start of the UTC block of `hours` hours holding the hour `ts` (a naive UTC datetime)."""
    return ts.replace(hour=ts.hour - ts.hour % hours, minute=0, second=0, microsecond=0)


def aggregate(rows, hours, last_day=None):
    """Rows of the hourly file (lists, in time order, without the header) -> rows of the `hours`-hour file.
    Blocks starting after `last_day` (a date, the last covered day) are dropped."""
    out, cur, group = [], None, []

    def flush():
        if not group:
            return
        highs = [float(r[2]) for r in group]
        lows = [float(r[3]) for r in group]
        vol = sum(float(r[5]) for r in group)
        close = group[-1][4]
        end = cur + dt.timedelta(hours=hours) - dt.timedelta(milliseconds=1)
        out.append([cur.strftime("%Y-%m-%d") if hours == 24 else cur.strftime(FMT),
                    group[0][1], group[highs.index(max(highs))][2], group[lows.index(min(lows))][3], close,
                    repr(vol), end.strftime(FMT) + ".999", repr(vol * float(close)),
                    str(sum(int(r[8] or 0) for r in group)), "", "", "0"])

    for r in rows:
        start = block_start(dt.datetime.strptime(r[0][:19], FMT), hours)
        if last_day is not None and start.date() > last_day:
            break
        if start != cur:
            flush()
            cur, group = start, []
        group.append(r)
    flush()
    return out


def read(path):
    rows = list(csv.reader(path.open(encoding="utf-8", newline="")))
    if rows[0] != HEADER:
        raise ValueError(f"{path.name}: unexpected header {rows[0]}")
    body = rows[1:]
    stamps = [r[0] for r in body]
    if stamps != sorted(stamps) or len(set(stamps)) != len(stamps):
        raise ValueError(f"{path.name}: timestamps not strictly increasing")
    return body


def covered_last_day(data_dir, name):
    """The last day of the hourly file's coverage (one range from its start, as the archive files have), or None."""
    spans = coverage.ranges(coverage.load(data_dir).get(name))
    if len(spans) != 1:
        raise ValueError(f"{name}: coverage has {len(spans)} ranges, expected one")
    return spans[0]


def derive(src, hours, data_dir=DATA, dry_run=False):
    """Writes kraken_<PAIR>_<hours>h.csv from kraken_<PAIR>_1h.csv and records its coverage. Returns a summary line."""
    start, last_day = covered_last_day(data_dir, src.name)
    rows = aggregate(read(src), hours, last_day)
    name = src.name.replace("_1h.csv", f"_{hours}h.csv")
    if not dry_run:
        dest = Path(data_dir) / name
        tmp = dest.with_suffix(".csv.tmp")
        with tmp.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(HEADER)
            w.writerows(rows)
        tmp.replace(dest)
        if coverage.ranges(coverage.load(data_dir).get(name)) != [(start, last_day)]:   # a rerun records nothing new
            coverage.record(data_dir, name, start, last_day,
                            f"derived from {src.name} by tools/derive_kraken_bars.py ({hours}-hour UTC blocks)")
    return f"{name}: {len(rows)} bars from {rows[0][0]} to {rows[-1][0]}" if rows else f"{name}: no bars"


def compare_daily(data_dir=DATA, pairs=None):
    """The proof: 24-hour blocks of each hourly file against the Kraken daily file, on the days both have.
    Prints, per pair and in total: days compared, days only in one, and the days whose fields differ."""
    tot = {"days": 0, "only_derived": 0, "only_daily": 0, "ohlc_differ": 0, "volume_differ": 0, "trades_differ": 0}
    for src in sorted(Path(data_dir).glob("kraken_*_1h.csv")):
        pair = src.name.split("_")[1]
        if pairs and pair not in pairs:
            continue
        daily_path = src.with_name(f"kraken_{pair}_1d.csv")
        if not daily_path.exists():
            continue
        derived = {r[0]: r for r in aggregate(read(src), 24, covered_last_day(data_dir, src.name)[1])}
        daily = {r[0]: r for r in read(daily_path) if r[0] <= max(derived)}
        both = sorted(set(derived) & set(daily))
        c = {"days": len(both), "only_derived": len(set(derived) - set(daily)),
             "only_daily": len(set(daily) - set(derived)), "ohlc_differ": 0, "volume_differ": 0, "trades_differ": 0}
        for d in both:
            a, b = derived[d], daily[d]
            if any(float(x) != float(y) for x, y in zip(a[1:5], b[1:5])):
                c["ohlc_differ"] += 1
            if abs(float(a[5]) - float(b[5])) > 1e-9 * max(1.0, abs(float(b[5]))):
                c["volume_differ"] += 1
            if int(a[8]) != int(b[8] or 0):
                c["trades_differ"] += 1
        for k in tot:
            tot[k] += c[k]
        print(pair, " ".join(f"{k}={v}" for k, v in c.items()))
    print("TOTAL", " ".join(f"{k}={v}" for k, v in tot.items()))
    return tot


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--hours", type=int, default=4, help="the bar's length in hours (a divisor of 24)")
    a.add_argument("--pairs", nargs="*", help="e.g. BTCUSD ETHUSD (default: every kraken_*_1h.csv)")
    a.add_argument("--dry-run", action="store_true")
    a.add_argument("--compare-daily", action="store_true", help="the proof against the daily files; writes nothing")
    args = a.parse_args()
    if args.compare_daily:
        compare_daily(pairs=args.pairs)
        return
    if args.hours < 2 or 24 % args.hours:
        sys.exit("--hours must divide 24 and be at least 2")
    for src in sorted(DATA.glob("kraken_*_1h.csv")):
        if not args.pairs or src.name.split("_")[1] in args.pairs:
            print(derive(src, args.hours, dry_run=args.dry_run))


if __name__ == "__main__":
    sys.exit(main())
