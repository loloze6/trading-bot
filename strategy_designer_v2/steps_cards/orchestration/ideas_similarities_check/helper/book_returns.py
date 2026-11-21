"""A backtest record's book returns per period of a timeframe (definition: common/measures.md, "A paying book, and what
it shares with the books we have"): per coin, its value after the last bar of each UTC period, returns between periods
inside each window; then, each period, the mean of the coins' returns. Holding its coins: the same from the closes.
For the day this is step 6's daily book (06_profitability/helper/check_profitability.py, `load`).

Why this can't leak: it reads a finished record after the fact; it changes no decision.
"""
from pathlib import Path
import pandas as pd

FREQ = {"1h": "h", "4h": "4h", "1d": "D"}          # UTC periods: hours, 4-hour blocks from 00:00, days from 00:00
HOURS = {"1h": 1, "4h": 4, "1d": 24}


def bar_of(record):
    """The record's bar size, from its id (`<idea>_<bar>`)."""
    bar = Path(record).name.rsplit("_", 1)[-1]
    if bar not in FREQ:
        raise ValueError(f"{Path(record).name}: no bar size in its name")
    return bar


def timeframes_from(bar):
    """The timeframes a book of this bar size can be compared on: its own and every larger one."""
    return [t for t in FREQ if HOURS[t] >= HOURS[bar]]


def coin_windows(record):
    """(coin, window number, bars file) for every window that ran."""
    out = []
    for coin in sorted(p for p in Path(record).iterdir() if p.is_dir()):
        for f in sorted(coin.glob("w*/bars.csv.gz"), key=lambda p: int(p.parent.name[1:])):
            out.append((coin.name, int(f.parent.name[1:]), f))
    return out


def period_returns(series, ts, timeframe):
    """Returns between UTC periods from a per-bar series: its value at the last bar of each period."""
    s = pd.Series(series.to_numpy(float), index=pd.to_datetime(ts, utc=True))
    last = s.groupby(s.index.floor(FREQ[timeframe])).last()
    return last.pct_change().dropna()


def book_returns(record, timeframe):
    """DataFrame (window, period, book, hold): the book's and holding's equal-weight returns per period."""
    parts = {}
    files = coin_windows(record)
    if not files:
        raise FileNotFoundError(f"{Path(record).name}: bars not found: rerun step 4 on the plan")
    for coin, w, f in files:
        d = pd.read_csv(f, usecols=["timestamp", "close", "postRebalance_total_value"])
        b = period_returns(d["postRebalance_total_value"], d["timestamp"], timeframe).rename(coin)
        h = period_returns(d["close"], d["timestamp"], timeframe).rename(coin)
        parts.setdefault(w, ([], []))
        parts[w][0].append(b); parts[w][1].append(h)
    rows = []
    for w in sorted(parts):
        book = pd.concat(parts[w][0], axis=1, sort=True).mean(axis=1)
        hold = pd.concat(parts[w][1], axis=1, sort=True).mean(axis=1)
        rows.append(pd.DataFrame({"window": w, "period": book.index, "book": book.to_numpy(), "hold": hold.reindex(book.index).to_numpy()}))
    return pd.concat(rows, ignore_index=True)
