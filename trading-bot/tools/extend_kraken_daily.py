"""Bring the cached Kraken daily bars (local_data/kraken_<COIN>USD_1d.csv) up to the last finished day.

Kraken's public OHLC endpoint (https://api.kraken.com/0/public/OHLC?pair=<PAIR>&interval=1440, no key) serves the
last 720 days. For each cached coin this appends the days after the cache's last row, up to yesterday (UTC), in the
cache's own row format. Rows already in the cache are never changed; on the days both have, the prices must be
equal or nothing is written for that coin. The days added are recorded in local_data/coverage.yaml (data/coverage.py),
which a backtest checks before reading.

  python tools/extend_kraken_daily.py [--until YYYY-MM-DD] [--dry-run]

Why this can't leak: only finished days are written (today's bar, still forming, is dropped; --until can only move
the last day earlier); the engine hands each bar's decision the rows up to that bar.
"""
import argparse, csv, datetime as dt, json, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data import coverage  # noqa: E402  (the days each file was fetched for)

DATA = Path(__file__).resolve().parents[1] / "local_data"
URL = "https://api.kraken.com/0/public/OHLC?pair={}&interval=1440"
PAIR = {"BTC": "XBT", "DOGE": "XDG"}          # Kraken's own names; the others use the usual ticker
PRICE = slice(1, 5)                           # open, high, low, close


def api_rows(coin):
    """{day: the cache's row} from Kraken's answer for this coin (COIN without USD)."""
    with urllib.request.urlopen(URL.format(PAIR.get(coin, coin) + "USD"), timeout=30) as r:
        ans = json.load(r)
    if ans["error"]:
        raise RuntimeError(f"{coin}: {ans['error']}")
    out = {}
    for t, o, h, l, c, _vwap, vol, n in next(v for k, v in ans["result"].items() if k != "last"):
        day = dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%d")
        out[day] = [day, repr(float(o)), repr(float(h)), repr(float(l)), repr(float(c)), repr(float(vol)),
                    day + " 23:59:59.999", repr(float(c) * float(vol)), str(n), "", "", "0"]
    return out


def extend(path, until, dry_run=False):
    rows = list(csv.reader(path.open(encoding="utf-8", newline="")))
    coin = path.stem.split("_")[1][:-3]
    new = api_rows(coin)
    have = {r[0]: r for r in rows[1:]}
    differ = [d for d in sorted(set(have) & set(new))
              if any(abs(float(a) / float(b) - 1) > 1e-9 for a, b in zip(have[d][PRICE], new[d][PRICE]))]
    if differ:
        return f"{coin}: not extended, {len(differ)} overlapping days differ in price (first {differ[0]})"
    last = rows[-1][0]
    add = [new[d] for d in sorted(new) if last < d <= until]
    gaps = [b for a, b in zip([last] + [r[0] for r in add], [r[0] for r in add])
            if (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days != 1]
    if add and not dry_run:
        with path.open("a", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(add)
        coverage.record(DATA, path.name, add[0][0], add[-1][0], "Kraken public OHLC API (tools/extend_kraken_daily.py)")
    span = f"{add[0][0]} to {add[-1][0]}" if add else "nothing to add"
    return (f"{coin}: {len(add)} days added ({span}); {len(set(have) & set(new))} overlapping days equal"
            + (f"; {len(gaps)} missing day(s) before {gaps[0]}" if gaps else ""))


def main():
    a = argparse.ArgumentParser()
    yesterday = (dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1)).isoformat()
    a.add_argument("--until", default=yesterday, help="the last day to add (at most yesterday, UTC)")
    a.add_argument("--dry-run", action="store_true")
    args = a.parse_args()
    until = min(args.until, yesterday)
    for path in sorted(DATA.glob("kraken_*USD_1d.csv")):
        print(extend(path, until, args.dry_run))
        time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
