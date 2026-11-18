"""Which dates each local OHLCV file was fetched for: `coverage.yaml` beside the files (operator, 2026-11-18).

Data gathering and backtesting are separate. A data tool fetches from an exchange and writes a file; it records here
the days it asked for. A backtest reads the local files only, never an exchange: it checks that its days (warm-up
included) are inside the file's coverage, and stops otherwise ("not fetched: run the data tool").

Inside a covered range, the exchange gave everything it had: a hole there is the exchange's own (an hour without a
trade) and is read as it is. Outside every covered range, the data was never fetched.

coverage.yaml:
    files:
      kraken_BTCUSD_1d.csv:
        - {start: null, end: "2026-11-17", source: "...", recorded: "2026-11-18"}
`start` and `end` are days, both included. `start: null` means from the exchange's first data for the pair (a file
from Kraken's complete archive: before its first row, the pair did not trade on Kraken). Ranges that touch or overlap
are read as one.

Why this can't leak: it only says which days were fetched; it reads no prices and changes no row.
"""
from __future__ import annotations

import datetime as dt
import os
from pathlib import Path

import yaml

FILE_NAME = "coverage.yaml"
DATA_TOOL = "trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)"


class DataNotFetched(RuntimeError):
    """A backtest asked for days its local file's coverage does not hold."""


def _day(x) -> dt.date:
    return x if isinstance(x, dt.date) and not isinstance(x, dt.datetime) else dt.date.fromisoformat(str(x)[:10])


def path_for(data_dir) -> Path:
    return Path(data_dir) / FILE_NAME


def load(data_dir) -> dict:
    p = path_for(data_dir)
    if not p.exists():
        return {}
    doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return doc.get("files") or {}


def ranges(entries) -> list:
    """The covered ranges, merged: [(start or None, end), ...] as dates, in order."""
    spans = sorted(((None if e.get("start") is None else _day(e["start"]), _day(e["end"])) for e in entries or []),
                   key=lambda s: (s[0] is not None, s[0] or dt.date.min))
    out = []
    for s, e in spans:
        if out and (s is None or out[-1][1] is None or s <= out[-1][1] + dt.timedelta(days=1)):
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out


def missing(data_dir, file_name: str, start, end) -> list:
    """The days of [start, end] (dates or timestamps; both included) outside the file's coverage, as (start, end)
    date pairs. Empty when every day is covered."""
    lo, hi = _day(start), _day(end)
    gaps, cur = [], lo
    for s, e in ranges(load(data_dir).get(file_name)):
        if e < cur:
            continue
        if s is not None and s > cur:
            gaps.append((cur, min(hi, s - dt.timedelta(days=1))))
        cur = max(cur, e + dt.timedelta(days=1))
        if cur > hi:
            break
    if cur <= hi:
        gaps.append((cur, hi))
    return [g for g in gaps if g[0] <= g[1]]


def check(data_dir, file_name: str, start, end) -> None:
    """Raise DataNotFetched when [start, end] is not wholly inside the file's coverage."""
    gaps = missing(data_dir, file_name, start, end)
    if gaps:
        days = "; ".join(f"{a} to {b}" for a, b in gaps)
        raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                             f"local data only; fetch these days first with the data tool, {DATA_TOOL}")


def record(data_dir, file_name: str, start, end, source: str) -> None:
    """Add a fetched range to the file's coverage (start None: from the exchange's first data). Written atomically."""
    files = load(data_dir)
    files.setdefault(file_name, []).append({"start": None if start is None else str(_day(start)),
                                            "end": str(_day(end)), "source": source,
                                            "recorded": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")})
    p = path_for(data_dir)
    text = ("# Which dates each local OHLCV file was fetched for: see trading-bot/data/coverage.py. Written by the "
            "data tools only.\n" + yaml.safe_dump({"files": dict(sorted(files.items()))}, sort_keys=False, width=120))
    tmp = p.with_name(p.name + f".tmp{os.getpid()}")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)
