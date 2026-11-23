"""Bring the cached Kraken hourly bars (local_data/kraken_<COIN>USD_1h.csv) up to a finished day.

Two Kraken sources, in this order, for the hours after the cache's last row:
  1. Kraken's quarterly OHLCVT archive (Kraken_OHLCVT_<YEAR>Q<N>.zip, the source of the cached history; listed on
     support.kraken.com, "Downloadable historical OHLCVT data"): only the coin's 60-minute member is read, by ranged
     requests, not the whole archive. Every published quarter after the cache's last day is used.
  2. After the last published quarter: Kraken's public trades (https://api.kraken.com/0/public/Trades, no key), made
     into hourly bars the way the archive makes them (open, high, low, close of the hour's trades, the volume summed,
     the trades counted, each trade id once; an hour without a trade has no row).
Before the trades are used for a coin, its archive's last day is rebuilt from the trades and must equal the archive
(every hour: prices equal, volume within 1e-9, trade count equal); otherwise nothing from the trades is written for
that coin. Rows already in the cache are never changed. Each added range is recorded in local_data/coverage.yaml
(data/coverage.py), which a backtest checks before reading.

  python tools/extend_kraken_hourly.py [--until YYYY-MM-DD] [--coins BTC,ETH,...] [--dry-run]
  --until: the last day to add (default: the last day of the daily files, at most yesterday UTC).

Why this can't leak: only finished days are written (--until is at most yesterday, UTC); a bar is stamped at its
hour's start and holds that hour's trades only; the engine hands each bar's decision the rows up to that bar.
"""
import argparse, csv, datetime as dt, decimal, io, json, sys, time, urllib.error, urllib.request, zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data import coverage  # noqa: E402  (the days each file was fetched for)

DATA = Path(__file__).resolve().parents[1] / "local_data"
ARCHIVE = "https://assets.kraken.com/marketing/institutions/Kraken_OHLCVT_{}Q{}.zip"
TRADES = "https://api.kraken.com/0/public/Trades?pair={}&since={}&count=1000"
HEADERS = {"User-Agent": "curl/8.5.0"}           # the asset host refuses Python's default client name
PAIR = {"BTC": "XBT", "DOGE": "XDG"}             # Kraken's own names; the others use the usual ticker
UTC = dt.timezone.utc


def get(url, headers=None, tries=8):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={**HEADERS, **(headers or {})}), timeout=120) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if isinstance(e, urllib.error.HTTPError) and e.code in (403, 404):
                raise
            time.sleep(min(60, 2 ** i))
    raise RuntimeError(f"no answer: {url}")


class Ranged(io.RawIOBase):
    """A remote file read by HTTP ranges, so zipfile reads one member without the whole archive."""
    def __init__(self, url):
        self.url, self.pos = url, 0
        req = urllib.request.Request(url, method="HEAD", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=60) as r:
            self.size = int(r.headers["Content-Length"])
    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos
    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else self.pos + off if whence == 1 else self.size + off
        return self.pos
    def read(self, n=-1):
        n = self.size - self.pos if n < 0 else min(n, self.size - self.pos)
        if n <= 0: return b""
        data = get(self.url, {"Range": f"bytes={self.pos}-{self.pos + n - 1}"}); self.pos += len(data)
        return data
    def readinto(self, b):
        d = self.read(len(b)); b[:len(d)] = d
        return len(d)


def quarters_after(day):
    """(year, quarter, first day, last day) of every published archive quarter starting after `day`."""
    y, q = day.year, (day.month - 1) // 3 + 1
    out = []
    while True:
        y, q = (y + 1, 1) if q == 4 else (y, q + 1)
        first = dt.date(y, 3 * q - 2, 1); last = (dt.date(y + (q == 4), 1 if q == 4 else 3 * q + 1, 1) - dt.timedelta(days=1))
        try:
            req = urllib.request.Request(ARCHIVE.format(y, q), method="HEAD", headers=HEADERS)
            urllib.request.urlopen(req, timeout=60).close()
        except urllib.error.HTTPError:
            return out
        out.append((y, q, first, last))


def row(t, o, h, l, c, vol, n):
    """The cache's row for the hour starting at unix second t."""
    s = dt.datetime.fromtimestamp(t, UTC)
    return [s.strftime("%Y-%m-%d %H:%M:%S"), repr(float(o)), repr(float(h)), repr(float(l)), repr(float(c)),
            repr(float(vol)), s.strftime("%Y-%m-%d %H:59:59.999"), repr(float(vol) * float(c)), str(int(n)), "", "", "0"]


def archive_bars(zf, coin):
    """{hour start (unix s): (o, h, l, c, volume, trades)} of the coin's 60-minute member."""
    raw = zf.read(f"{PAIR.get(coin, coin)}USD_60.csv").decode()
    return {int(r[0]): tuple(r[1:7]) for r in csv.reader(io.StringIO(raw)) if r}


def trade_bars(coin, start, end, log):
    """{hour start: (o, h, l, c, volume, trades)} from Kraken's public trades in [start, end) (unix s)."""
    bars, since, calls, last_id = {}, int(start * 1e9), 0, -1   # a page repeats the previous page's last trade: by id
    while True:
        ans = json.loads(get(TRADES.format(PAIR.get(coin, coin) + "USD", since))); calls += 1
        if ans["error"]:
            if any("Too many" in e or "Rate limit" in e for e in ans["error"]):
                time.sleep(5); continue
            raise RuntimeError(f"{coin}: {ans['error']}")
        trades = next(v for k, v in ans["result"].items() if k != "last")
        for p, v, t, *_rest in trades:
            tid = int(_rest[-1])
            if tid <= last_id: continue
            last_id = tid
            if not start <= t < end: continue
            h = int(t // 3600 * 3600); p = decimal.Decimal(p); v = decimal.Decimal(v)
            b = bars.get(h)
            bars[h] = [p, p, p, p, v, 1] if b is None else [b[0], max(b[1], p), min(b[2], p), p, b[4] + v, b[5] + 1]
        nxt = int(ans["result"]["last"])
        if not trades or trades[-1][2] >= end or nxt == since:
            break
        since = nxt
        if calls % 500 == 0:
            log(f"  {coin}: {calls} calls, up to {dt.datetime.fromtimestamp(trades[-1][2], UTC):%Y-%m-%d %H:%M}")
        time.sleep(0.5)
    return {h: tuple(b) for h, b in bars.items()}, calls


def same(a, b):
    """An archive bar and a bar made from trades: prices equal, volume within 1e-9, trade count equal."""
    return (all(decimal.Decimal(str(x)) == decimal.Decimal(str(y)) for x, y in zip(a[:4], b[:4]))
            and abs(float(a[4]) - float(b[4])) <= 1e-9 * max(1.0, abs(float(a[4]))) and int(a[5]) == int(b[5]))


def extend(path, until, quarters, dry_run, log):
    coin = path.stem.split("_")[1][:-3]
    last_t = int(dt.datetime.strptime(next(reversed(list(csv.reader(path.open(encoding="utf-8"))))) [0],
                                      "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC).timestamp())
    end_t = int(dt.datetime.combine(until + dt.timedelta(days=1), dt.time(), UTC).timestamp())
    add, ranges, last_arch = [], [], None
    for y, q, first, last in quarters:
        if first > until: break
        bars = archive_bars(zipfile.ZipFile(Ranged(ARCHIVE.format(y, q))), coin)
        hi = min(last, until)
        keep = sorted(t for t in bars if last_t < t < int(dt.datetime.combine(hi + dt.timedelta(days=1), dt.time(), UTC).timestamp()))
        add += [row(t, *bars[t]) for t in keep]; ranges.append((first, hi, f"Kraken OHLCVT archive {y}Q{q} (tools/extend_kraken_hourly.py)"))
        last_arch = (last, bars)
    msg = [f"{coin}: archive {len(add)} hours"]
    t_from = dt.datetime.fromtimestamp(last_t, UTC).date() + dt.timedelta(days=1) if last_arch is None else last_arch[0] + dt.timedelta(days=1)
    if t_from <= until:
        if last_arch is None:
            return f"{coin}: no archive quarter to check the trades against: nothing written"
        check_day = last_arch[0]
        c0 = int(dt.datetime.combine(check_day, dt.time(), UTC).timestamp())
        built, calls = trade_bars(coin, c0, c0 + 86400, log)
        ref = {t: b for t, b in last_arch[1].items() if c0 <= t < c0 + 86400}
        bad = [t for t in set(ref) | set(built) if t not in ref or t not in built or not same(ref[t], built[t])]
        if bad:
            msg.append(f"trades NOT used: {len(bad)} of {len(ref)} hours of {check_day} differ from the archive "
                       f"(first {dt.datetime.fromtimestamp(min(bad), UTC):%H:%M})")
        else:
            tb, more = trade_bars(coin, c0 + 86400, end_t, log); calls += more
            new = [row(t, *tb[t]) for t in sorted(tb)]
            add += new; ranges.append((t_from, until, "Kraken public trades, made into hourly bars (tools/extend_kraken_hourly.py)"))
            msg.append(f"trades {len(new)} hours ({calls} calls; {check_day} rebuilt from trades equals the archive, {len(ref)} hours)")
    if add and not dry_run:
        with path.open("a", encoding="utf-8", newline="") as f:
            csv.writer(f, lineterminator="\n").writerows(add)
        for first, last, src in ranges:
            coverage.record(DATA, path.name, first.isoformat(), last.isoformat(), src)
    return "; ".join(msg) + (f"; first {add[0][0]}, last {add[-1][0]}" if add else "")


def main():
    a = argparse.ArgumentParser()
    yesterday = dt.datetime.now(UTC).date() - dt.timedelta(days=1)
    daily_last = max(next(reversed(list(csv.reader(p.open(encoding="utf-8")))))[0] for p in DATA.glob("kraken_*USD_1d.csv"))
    a.add_argument("--until", default=daily_last, help="the last day to add (at most yesterday, UTC)")
    a.add_argument("--coins", default="", help="comma-separated coins (default: every cached hourly file)")
    a.add_argument("--dry-run", action="store_true")
    args = a.parse_args()
    until = min(dt.date.fromisoformat(args.until), yesterday)
    want = {c.strip().upper() for c in args.coins.split(",") if c.strip()}
    paths = [p for p in sorted(DATA.glob("kraken_*USD_1h.csv")) if not want or p.stem.split("_")[1][:-3] in want]
    log = lambda s: print(s, flush=True)
    first_last = min(dt.datetime.strptime(next(reversed(list(csv.reader(p.open(encoding="utf-8")))))[0][:10], "%Y-%m-%d").date() for p in paths)
    quarters = quarters_after(first_last)
    log(f"until {until}; archive quarters published after {first_last}: {[f'{y}Q{q}' for y, q, *_ in quarters]}")
    for p in paths:
        log(extend(p, until, quarters, args.dry_run, log))


if __name__ == "__main__":
    sys.exit(main())
