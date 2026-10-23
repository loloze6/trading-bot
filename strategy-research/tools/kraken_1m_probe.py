"""
kraken_1m_probe.py -- one-coin, one-day probe of Kraken 1-minute data.

Purpose: before any larger 1-minute data build, measure two candidate sources on
a single in-sample day and say whether they agree:

  * the downloadable OHLCVT archive (no header; columns unix_seconds, open, high,
    low, close, volume, trade_count; minutes with no trades are OMITTED, not
    zero-filled), read from an already-extracted local copy;
  * the public Trades endpoint (GET /0/public/Trades), paged with the response's
    `last` nanosecond cursor via ccxt's implicit raw method (ccxt's fetch_trades
    sends `since` in seconds, so it is NOT used), then aggregated to 1m bars.

Subcommands: archive, trades, compare, sizes. Each writes into a NEW, EMPTY
staging directory outside every git repository and outside any local_data
directory (the CLI refuses otherwise). Every output gets a JSON provenance
sidecar (source, tool blob sha, ccxt version, request count, sha256 and bytes of
every output file). Missing minutes are reported, never treated as failures: the
archive omits no-trade minutes by design.

Why this cannot leak: this is a data-quality measurement, not a signal. No
forecast, feature or decision reads any bar here. Before ANY read or fetch the
tool asserts that the whole requested day lies strictly before the sealed
holdout start, using holdout_policy.load_holdout_range (the policy's one strict
reader); on failure it refuses with a message that names no date. The bounds are
used only to filter and count: the whole-file archive pass drops every row at or
after the holdout start before any statistic is computed, reports only the COUNT
of such rows, and stops (writing nothing) when that count is not zero. The
bounds are never printed, logged or written.

Usage (from the repository root, with the project venv, on this file):
    python -I strategy-research/tools/kraken_1m_probe.py archive --pair XBTUSD \\
        --day YYYY-MM-DD --source <XBTUSD_1.csv> --out <new empty dir>
    python -I strategy-research/tools/kraken_1m_probe.py trades --pair XBTUSD \\
        --day YYYY-MM-DD --out <new empty dir>
    python -I strategy-research/tools/kraken_1m_probe.py compare --pair XBTUSD \\
        --day YYYY-MM-DD --archive-dir <dir> --trades-dir <dir> --out <new dir>
    python -I strategy-research/tools/kraken_1m_probe.py sizes \\
        --source-dir <master_q4 dir> --out <new empty dir>
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:  # -I drops the script dir from sys.path
    sys.path.insert(0, str(_HERE))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import yaml  # noqa: E402

import holdout_policy  # noqa: E402

COLUMNS = ["timestamp", "open", "high", "low", "close", "volume", "trade_count"]
_PRICE_COLS = ["open", "high", "low", "close"]
_COMPARE_FIELDS = ["open", "high", "low", "close", "volume", "trade_count"]
GAP_BINS = (("1", 1, 1), ("2-5", 2, 5), ("6-60", 6, 60), ("61-1440", 61, 1440), (">1440", 1441, None))
_DEFECT_KEYS = ("non_integer_timestamps", "off_grid_timestamps", "non_increasing_steps",
                "duplicate_timestamps", "ohlc_violations", "negative_volume",
                "bad_trade_count", "nan_rows")

MAX_REQUESTS = 400
MIN_CALL_SPACING_S = 1.05
BACKOFF_SECONDS = (2, 4, 8, 16)
TRADES_PAGE_COUNT = 1000
ARCHIVE_URL_NOTE = "local extracted copy of the Kraken OHLCVT archive (origin URL never recorded)"
SHA256SUMS_URL = "https://assets.kraken.com/marketing/institutions/OHLCVT_Full_PARTS_SHA256SUMS.txt"

#: Tests point this at a sandbox policy; None means the real policy file.
POLICY_PATH_OVERRIDE = None


class ProbeRefusal(Exception):
    """A deny-by-default refusal. The message never names a date."""


# --------------------------------------------------------------------------- #
# holdout guard                                                               #
# --------------------------------------------------------------------------- #
def _holdout_start_epoch(policy_path=None) -> int:
    """Epoch seconds (UTC midnight) of the holdout start. Never printed."""
    p = policy_path if policy_path is not None else POLICY_PATH_OVERRIDE
    try:
        start, _ = holdout_policy.load_holdout_range(p)
    except holdout_policy.HoldoutPolicyError as exc:
        # The error text can embed policy values: report only its type.
        raise ProbeRefusal(f"cannot read the holdout policy ({type(exc).__name__}); "
                           f"refusing (fail closed)") from None
    d = date.fromisoformat(start)
    return int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp())


def parse_day(day: str) -> tuple[int, int]:
    """(day_start_epoch, day_end_epoch) of a strict YYYY-MM-DD UTC day."""
    iso = holdout_policy.iso_day(day)
    if iso is None:
        raise ProbeRefusal("--day is not a strict YYYY-MM-DD day")
    d = date.fromisoformat(iso)
    start = int(datetime(d.year, d.month, d.day, tzinfo=timezone.utc).timestamp())
    return start, start + 86400


def assert_day_before_holdout(day: str, policy_path=None) -> tuple[int, int]:
    """Refuse unless the WHOLE day is strictly before the holdout start."""
    d0, d1 = parse_day(day)
    if not d1 <= _holdout_start_epoch(policy_path):
        raise ProbeRefusal("the requested day is not strictly before the sealed holdout "
                           "start; refusing before any read or fetch (dates withheld)")
    return d0, d1


def sealed_row_count(ts_seconds_series, policy_path=None) -> int:
    """Rows at or after the holdout start. Returns a count only; the bounds are
    never returned or logged."""
    start = _holdout_start_epoch(policy_path)
    ts = pd.to_numeric(pd.Series(np.asarray(ts_seconds_series)), errors="coerce")
    return int((ts >= start).sum())


# --------------------------------------------------------------------------- #
# validation                                                                  #
# --------------------------------------------------------------------------- #
def _iso(ts: float) -> str:
    return datetime.fromtimestamp(float(ts), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class MinuteValidator:
    """Streaming validator. update() takes frames with COLUMNS (timestamp in
    unix seconds); report() is identical to validate_minute_frame on the
    concatenation of everything fed in."""

    def __init__(self, interval_seconds: int = 60):
        self.interval = interval_seconds
        self.rows = 0
        self._ts: list[np.ndarray] = []
        self.counts = {"negative_volume": 0, "ohlc_violations": 0, "bad_trade_count": 0,
                       "nan_rows": 0}

    def update(self, df: pd.DataFrame) -> None:
        num = df[COLUMNS].apply(pd.to_numeric, errors="coerce")
        self.rows += len(num)
        nan_mask = num.isna().any(axis=1)
        self.counts["nan_rows"] += int(nan_mask.sum())
        o, h, lo, c = (num[k] for k in _PRICE_COLS)
        bad = ((lo > np.minimum(o, c)) | (h < np.maximum(o, c)) | (lo > h)
               | (num[_PRICE_COLS] <= 0).any(axis=1))
        self.counts["ohlc_violations"] += int(bad.sum())
        self.counts["negative_volume"] += int((num["volume"] < 0).sum())
        tc = num["trade_count"]
        tc_bad = (tc < 1) | ((tc.notna()) & (tc != np.floor(tc)))
        self.counts["bad_trade_count"] += int(tc_bad.sum())
        self._ts.append(num["timestamp"].to_numpy(dtype="float64"))

    def report(self) -> dict:
        ts_all = np.concatenate(self._ts) if self._ts else np.array([], dtype="float64")
        ts = ts_all[~np.isnan(ts_all)]
        interval = self.interval
        rep: dict = {"rows": int(self.rows), "interval_seconds": interval}
        if len(ts):
            rep["first_timestamp"] = _iso(ts.min())
            rep["last_timestamp"] = _iso(ts.max())
        else:
            rep["first_timestamp"] = None
            rep["last_timestamp"] = None
        rep["non_integer_timestamps"] = int((ts != np.floor(ts)).sum())
        rep["off_grid_timestamps"] = int((np.mod(ts, interval) != 0).sum())
        rep["non_increasing_steps"] = int((np.diff(ts) <= 0).sum()) if len(ts) > 1 else 0
        u = np.unique(ts)
        rep["duplicate_timestamps"] = int(len(ts) - len(u))
        rep["ohlc_violations"] = self.counts["ohlc_violations"]
        rep["negative_volume"] = self.counts["negative_volume"]
        rep["bad_trade_count"] = self.counts["bad_trade_count"]
        rep["nan_rows"] = self.counts["nan_rows"]
        # gaps: minutes absent between consecutive distinct timestamps
        hist = {name: 0 for name, _, _ in GAP_BINS}
        missing = 0
        longest = 0
        longest_after = None
        if len(u) > 1:
            steps = np.floor(np.diff(u) / interval).astype("int64") - 1
            idx = np.nonzero(steps > 0)[0]
            for i in idx:
                n = int(steps[i])
                missing += n
                for name, lo_, hi_ in GAP_BINS:
                    if n >= lo_ and (hi_ is None or n <= hi_):
                        hist[name] += 1
                        break
                if n > longest:
                    longest, longest_after = n, _iso(u[i])
        rep["missing_minutes"] = int(missing)
        rep["gap_histogram"] = hist
        rep["longest_gap_minutes"] = int(longest)
        rep["longest_gap_starts_after"] = longest_after
        rep["passed"] = all(rep[k] == 0 for k in _DEFECT_KEYS)
        return rep


def validate_minute_frame(df: pd.DataFrame, *, interval_seconds: int = 60) -> dict:
    """Validation report for one frame (see MinuteValidator)."""
    v = MinuteValidator(interval_seconds)
    v.update(df)
    return v.report()


# --------------------------------------------------------------------------- #
# trades -> candles, comparison                                               #
# --------------------------------------------------------------------------- #
def candles_from_trades(trades) -> pd.DataFrame:
    """1m bars from raw Kraken trade arrays [price, volume, time, side, type,
    misc, trade_id] IN TRADE ORDER (open = first, close = last in that order).
    Minutes with no trades get no row."""
    if len(trades) == 0:
        return pd.DataFrame(columns=COLUMNS).astype(
            {"timestamp": "int64", "trade_count": "int64"})
    price = np.array([float(t[0]) for t in trades], dtype="float64")
    vol = np.array([float(t[1]) for t in trades], dtype="float64")
    minute = (np.floor(np.array([float(t[2]) for t in trades]) / 60.0) * 60).astype("int64")
    df = pd.DataFrame({"timestamp": minute, "price": price, "volume": vol})
    g = df.groupby("timestamp", sort=True)
    out = pd.DataFrame({
        "open": g["price"].first(), "high": g["price"].max(), "low": g["price"].min(),
        "close": g["price"].last(), "volume": g["volume"].sum(),
        "trade_count": g["price"].size().astype("int64"),
    }).reset_index()
    return out[COLUMNS]


def compare_minute_frames(archive_df: pd.DataFrame, trades_df: pd.DataFrame, *,
                          rel_tol: float = 1e-9, abs_tol: float = 1e-12) -> dict:
    """Minute-by-minute comparison of two frames keyed on timestamp (seconds)."""
    a = archive_df.set_index("timestamp")
    b = trades_df.set_index("timestamp")
    only_a = a.index.difference(b.index)
    only_b = b.index.difference(a.index)
    both = a.index.intersection(b.index)
    rep: dict = {
        "minutes_only_in_archive": int(len(only_a)),
        "minutes_only_in_trades": int(len(only_b)),
        "minutes_in_both": int(len(both)),
        "rel_tol": rel_tol,
        "example_minutes_only_in_archive": [_iso(t) for t in list(only_a[:5])],
        "example_minutes_only_in_trades": [_iso(t) for t in list(only_b[:5])],
    }
    mism: dict = {}
    mismatch_mask = pd.Series(False, index=both)
    per_field = {}
    for f in _COMPARE_FIELDS:
        x = a.loc[both, f].astype("float64").to_numpy()
        y = b.loc[both, f].astype("float64").to_numpy()
        bad = ~np.isclose(x, y, rtol=rel_tol, atol=abs_tol)
        mism[f] = int(bad.sum())
        per_field[f] = (x, y, bad)
        mismatch_mask = mismatch_mask | pd.Series(bad, index=both)
    rep["mismatches_by_field"] = mism
    examples = []
    for pos in np.nonzero(mismatch_mask.to_numpy())[0][:5]:
        ex = {"minute": _iso(both[pos]), "fields": {}}
        for f, (x, y, bad) in per_field.items():
            if bad[pos]:
                ex["fields"][f] = {"archive": float(x[pos]), "trades": float(y[pos])}
        examples.append(ex)
    rep["example_mismatches"] = examples
    rep["minutes_with_any_mismatch"] = int(mismatch_mask.sum())
    return rep


# --------------------------------------------------------------------------- #
# provenance, file helpers                                                    #
# --------------------------------------------------------------------------- #
def file_sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _git_blob_sha(path) -> str | None:
    try:
        r = subprocess.run(["git", "hash-object", str(path)], capture_output=True,
                           text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() or None if r.returncode == 0 else None


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _file_facts(path) -> dict:
    p = Path(path)
    return {"path": p.name, "bytes": p.stat().st_size, "sha256": file_sha256(p)}


def write_provenance(sidecar_path, *, source: str, url_or_endpoint: str,
                     local_path: str | None, fetched_or_read_utc: str,
                     output_files, request_count: int | None = None,
                     elapsed_seconds: float | None = None, ccxt_version: str | None = None,
                     rate_limit_ms=None, archive_copy_path=None, extra: dict | None = None,
                     tool_path=None) -> dict:
    """Write the JSON provenance sidecar and return the dict written."""
    tool = Path(tool_path) if tool_path is not None else Path(__file__).resolve()
    doc = {
        "source": source,
        "url_or_endpoint": url_or_endpoint,
        "local_path": local_path,
        "fetched_or_read_utc": fetched_or_read_utc,
        "tool_path": str(tool),
        "tool_git_blob_sha": _git_blob_sha(tool),
        "ccxt_version": ccxt_version,
        "rate_limit_ms": rate_limit_ms,
        "request_count": request_count,
        "elapsed_seconds": elapsed_seconds,
        "output_files": [_file_facts(p) for p in output_files],
    }
    if archive_copy_path is not None:
        ap = Path(archive_copy_path)
        st = ap.stat()
        doc["archive_copy"] = {
            "path": str(ap), "bytes": st.st_size, "sha256": file_sha256(ap),
            "mtime_utc": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
                                 .strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    if extra:
        doc["extra"] = extra
    Path(sidecar_path).write_text(json.dumps(doc, indent=2, sort_keys=False), encoding="utf-8")
    return doc


def _native(o):
    if isinstance(o, dict):
        return {str(k): _native(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_native(v) for v in o]
    if isinstance(o, np.generic):
        return o.item()
    return o


def write_yaml(path, doc) -> None:
    Path(path).write_text(yaml.safe_dump(_native(doc), sort_keys=False), encoding="utf-8")


def write_minute_csv_gz(df: pd.DataFrame, path) -> None:
    """Gzip CSV with header timestamp,open,...,trade_count (ISO UTC timestamps)."""
    out = df[COLUMNS].copy()
    out["timestamp"] = [_iso(t) for t in out["timestamp"]]
    out["trade_count"] = out["trade_count"].astype("int64")
    # mtime=0 and no embedded name: the bytes depend only on the content
    with open(path, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
        gz.write(out.to_csv(index=False, lineterminator="\n").encode("utf-8"))


def read_minute_csv_gz(path) -> pd.DataFrame:
    df = pd.read_csv(path, compression="gzip")
    ts = pd.to_datetime(df["timestamp"], utc=True)
    df["timestamp"] = ts.dt.as_unit("s").astype("int64")
    return df


def check_out_dir(out) -> Path:
    """Refuse an --out inside a git repository or a local_data directory, or one
    that already holds files; create it when absent."""
    p = Path(out).resolve()
    chain = [p, *p.parents]
    for q in chain:
        if (q / ".git").exists():
            raise ProbeRefusal("--out is inside a git repository; refusing")
    if any(part.lower() == "local_data" for part in p.parts):
        raise ProbeRefusal("--out is inside a local_data directory; refusing")
    if p.exists():
        if not p.is_dir() or any(p.iterdir()):
            raise ProbeRefusal("--out already contains files (or is not a directory); refusing")
    else:
        p.mkdir(parents=True)
    return p


# --------------------------------------------------------------------------- #
# archive                                                                     #
# --------------------------------------------------------------------------- #
def run_archive(pair: str, day: str, source, out, *, chunksize: int = 500_000,
                policy_path=None) -> dict:
    d0, d1 = assert_day_before_holdout(day, policy_path)
    source = Path(source)
    outp = check_out_dir(out)
    t0 = time.monotonic()
    start_epoch = _holdout_start_epoch(policy_path)
    whole = MinuteValidator()
    day_parts = []
    sealed = 0
    for chunk in pd.read_csv(source, header=None, names=COLUMNS, chunksize=chunksize):
        ts = pd.to_numeric(chunk["timestamp"], errors="coerce")
        s = int((ts >= start_epoch).sum())
        sealed += s
        keep = chunk[~(ts >= start_epoch)]  # in-sample (and unparseable) rows only
        if len(keep):
            whole.update(keep)
        kts = pd.to_numeric(keep["timestamp"], errors="coerce")
        dm = keep[(kts >= d0) & (kts < d1)]
        if len(dm):
            day_parts.append(dm)
    if sealed:
        # count only; nothing is written (the staging dir stays empty)
        return {"sealed_rows": sealed, "stopped": True}
    day_df = (pd.concat(day_parts, ignore_index=True) if day_parts
              else pd.DataFrame(columns=COLUMNS))
    for c in COLUMNS:
        day_df[c] = pd.to_numeric(day_df[c])
    day_df["timestamp"] = day_df["timestamp"].astype("int64")
    day_df["trade_count"] = day_df["trade_count"].astype("int64")
    csv_path = outp / f"{pair}_1m_{day}_archive.csv.gz"
    write_minute_csv_gz(day_df, csv_path)
    day_rep = validate_minute_frame(day_df)
    day_rep["day_minutes_expected"] = 1440
    day_rep["day_minutes_present"] = int(day_df["timestamp"].nunique())
    day_rep["day_missing_minutes"] = 1440 - day_rep["day_minutes_present"]
    whole_rep = whole.report()
    whole_rep["sealed_rows"] = 0
    day_yaml = outp / f"{pair}_1m_{day}_archive_day_validation.yaml"
    whole_yaml = outp / f"{pair}_1m_whole_file_validation.yaml"
    write_yaml(day_yaml, day_rep)
    write_yaml(whole_yaml, whole_rep)
    write_provenance(
        outp / "provenance_archive.json", source="kraken OHLCVT archive (local extracted copy)",
        url_or_endpoint=ARCHIVE_URL_NOTE, local_path=str(source),
        fetched_or_read_utc=_utcnow(), output_files=[csv_path, day_yaml, whole_yaml],
        elapsed_seconds=round(time.monotonic() - t0, 3), archive_copy_path=source)
    return {"sealed_rows": 0, "stopped": False, "day_report": day_rep,
            "whole_file_report": whole_rep, "out": str(outp)}


# --------------------------------------------------------------------------- #
# trades                                                                      #
# --------------------------------------------------------------------------- #
def _is_rate_error(msg: str) -> bool:
    m = msg.lower()
    return "429" in m or "eapi" in m or "rate limit" in m


def fetch_trades_for_day(exchange, ccxt_pair_id: str, d0: int, d1: int, *, log_path=None,
                         sleep=time.sleep, clock=time.monotonic, max_requests: int = MAX_REQUESTS,
                         network_errors=()) -> dict:
    """Page the raw Trades endpoint from d0 (ns cursor) until a trade's time is
    >= d1. Every attempt counts toward max_requests. Returns trades inside the
    day plus run statistics."""
    since = str(d0 * 1_000_000_000)
    requests = 0
    retries = 0
    errors: list[str] = []
    kept: list = []
    seen_ids: set = set()
    dup_ids = 0
    nonmono_ids = 0
    cursor_not_advancing = 0
    last_id = None
    complete = False
    hit_cap = False
    last_call = None
    t0 = clock()
    log = open(log_path, "a", encoding="utf-8") if log_path else None

    def _log(msg: str) -> None:
        if log:
            log.write(msg + "\n")
            log.flush()

    try:
        while not complete:
            attempt = 0
            while True:
                if requests >= max_requests:
                    hit_cap = True
                    break
                if last_call is not None:
                    wait = MIN_CALL_SPACING_S - (clock() - last_call)
                    if wait > 0:
                        sleep(wait)
                requests += 1
                last_call = clock()
                try:
                    resp = exchange.publicGetTrades(
                        {"pair": ccxt_pair_id, "since": since, "count": TRADES_PAGE_COUNT})
                    break
                except network_errors as exc:
                    msg = f"{type(exc).__name__}: {exc}"
                    errors.append(msg)
                    if attempt >= len(BACKOFF_SECONDS):
                        raise
                    sleep(BACKOFF_SECONDS[attempt])
                    attempt += 1
                    retries += 1
            if hit_cap:
                break
            if requests % 20 == 0:
                _log(f"requests={requests} trades_kept={len(kept)} elapsed_s={clock() - t0:.1f} "
                     f"errors={len(errors)}")
            result = resp["result"]
            new_last = str(result["last"])
            key = next(k for k in result if k != "last")
            page = result[key]
            for t in page:
                tid = t[6] if len(t) > 6 else None
                if tid is not None:
                    if last_id is not None and int(tid) <= last_id:
                        nonmono_ids += 1
                    last_id = int(tid) if last_id is None else max(last_id, int(tid))
                    if tid in seen_ids:
                        dup_ids += 1
                        continue
                    seen_ids.add(tid)
                tt = float(t[2])
                if tt >= d1:
                    complete = True
                    break
                if tt >= d0:
                    kept.append(t)
            if complete:
                break
            if not page or new_last == since:
                cursor_not_advancing += 1
                complete = True  # no more data / stuck cursor: stop, flagged below
                break
            since = new_last
        _log(f"done requests={requests} trades_kept={len(kept)} elapsed_s={clock() - t0:.1f} "
             f"errors={len(errors)} complete={complete} hit_cap={hit_cap}")
    finally:
        if log:
            log.close()
    return {"trades": kept, "requests": requests, "retries": retries, "errors": errors,
            "elapsed_seconds": clock() - t0, "reached_day_end": complete and not cursor_not_advancing,
            "hit_request_cap": hit_cap, "duplicate_trade_ids": dup_ids,
            "non_monotonic_trade_ids": nonmono_ids, "cursor_not_advancing": cursor_not_advancing}


def run_trades(pair: str, day: str, out, *, exchange_factory=None, sleep=time.sleep,
               max_requests: int = MAX_REQUESTS,
               policy_path=None) -> dict:
    import ccxt

    d0, d1 = assert_day_before_holdout(day, policy_path)
    outp = check_out_dir(out)
    exchange = (exchange_factory() if exchange_factory
                else ccxt.kraken({"enableRateLimit": True}))
    t_start = _utcnow()
    log_path = outp / "trades_progress.log"
    stats = fetch_trades_for_day(exchange, pair, d0, d1, log_path=log_path, sleep=sleep,
                                 max_requests=max_requests,
                                 network_errors=(ccxt.NetworkError,))
    trades = stats["trades"]
    raw_path = outp / f"{pair}_trades_{day}.jsonl.gz"
    with open(raw_path, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
        for t in trades:
            gz.write((json.dumps(t, separators=(",", ":")) + "\n").encode("utf-8"))
    bars = candles_from_trades(trades)
    bars_path = outp / f"{pair}_1m_{day}_trades.csv.gz"
    write_minute_csv_gz(bars, bars_path)
    rep = validate_minute_frame(bars)
    rep["day_minutes_expected"] = 1440
    rep["day_minutes_present"] = int(len(bars))
    rep["day_missing_minutes"] = 1440 - rep["day_minutes_present"]
    rep["trades_in_day"] = len(trades)
    rep["fetch_complete"] = bool(stats["reached_day_end"])
    rep["hit_request_cap"] = bool(stats["hit_request_cap"])
    val_path = outp / f"{pair}_1m_{day}_trades_validation.yaml"
    write_yaml(val_path, rep)
    sidecar_extra = {k: stats[k] for k in ("retries", "errors", "duplicate_trade_ids",
                                           "non_monotonic_trade_ids", "cursor_not_advancing",
                                           "hit_request_cap", "reached_day_end")}
    sidecar_extra["errors_429_or_eapi"] = [e for e in stats["errors"] if _is_rate_error(e)]
    write_provenance(
        outp / "provenance_trades.json", source="kraken public REST (ccxt implicit raw method)",
        url_or_endpoint="GET /0/public/Trades via ccxt publicGetTrades",
        local_path=None, fetched_or_read_utc=t_start,
        output_files=[raw_path, bars_path, val_path, log_path],
        request_count=stats["requests"], elapsed_seconds=round(stats["elapsed_seconds"], 3),
        ccxt_version=ccxt.__version__, rate_limit_ms=getattr(exchange, "rateLimit", None),
        extra=sidecar_extra)
    return {"requests": stats["requests"], "elapsed_seconds": stats["elapsed_seconds"],
            "retries": stats["retries"], "errors": stats["errors"], "report": rep,
            "out": str(outp)}


# --------------------------------------------------------------------------- #
# compare, sizes                                                              #
# --------------------------------------------------------------------------- #
def run_compare(pair: str, day: str, archive_dir, trades_dir, out, *, policy_path=None) -> dict:
    assert_day_before_holdout(day, policy_path)
    outp = check_out_dir(out)
    a = read_minute_csv_gz(Path(archive_dir) / f"{pair}_1m_{day}_archive.csv.gz")
    b = read_minute_csv_gz(Path(trades_dir) / f"{pair}_1m_{day}_trades.csv.gz")
    rep = compare_minute_frames(a, b)
    rep["archive_rows"] = int(len(a))
    rep["trades_rows"] = int(len(b))
    path = outp / "compare_report.yaml"
    write_yaml(path, rep)
    write_provenance(outp / "provenance_compare.json", source="derived: archive csv vs trades csv",
                     url_or_endpoint="n/a", local_path=None, fetched_or_read_utc=_utcnow(),
                     output_files=[path])
    return rep


SIZE_PAIRS = ("XBTUSD", "ETHUSD", "XRPUSD", "SOLUSD", "ADAUSD", "SUIUSD", "ZECUSD", "XDGUSD",
              "XMRUSD", "LTCUSD", "ONDOUSD", "NEARUSD", "LINKUSD", "TAOUSD", "AVAXUSD",
              "TRXUSD", "AAVEUSD", "INJUSD", "UNIUSD")


class _CountingSink:
    def __init__(self):
        self.n = 0

    def write(self, b):
        self.n += len(b)
        return len(b)

    def flush(self):
        pass


def byte_line_count(path) -> int:
    """Lines by counting b'\\n' (+1 for an unterminated last line). No parsing."""
    n = 0
    last = b""
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            n += chunk.count(b"\n")
            last = chunk[-1:]
    return n + (1 if last and last != b"\n" else 0)


def gzip_ratio(path) -> dict:
    """Compressed byte count of `path` (level 6) without writing anything."""
    sink = _CountingSink()
    raw = 0
    with gzip.GzipFile(fileobj=sink, mode="wb", compresslevel=6, mtime=0) as gz, \
            open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            raw += len(chunk)
            gz.write(chunk)
    return {"raw_bytes": raw, "gzip_bytes": sink.n,
            "ratio": (raw / sink.n) if sink.n else None}


def run_sizes(source_dir, out, *, pairs=SIZE_PAIRS) -> dict:
    outp = check_out_dir(out)
    src = Path(source_dir)
    t0 = time.monotonic()
    files = {}
    tot_b = tot_l = 0
    for p in pairs:
        f = src / f"{p}_1.csv"  # exact name: never a glob (UNITE/SOLV prefixes)
        if not f.is_file():
            files[p] = {"missing": True}
            continue
        b, n = f.stat().st_size, byte_line_count(f)
        files[p] = {"bytes": b, "lines": n}
        tot_b += b
        tot_l += n
    rep = {"directory": str(src), "files": files,
           "totals": {"files_found": sum(1 for v in files.values() if "bytes" in v),
                      "bytes": tot_b, "lines": tot_l}}
    xbt = src / "XBTUSD_1.csv"
    if xbt.is_file():
        rep["gzip_xbtusd_1"] = gzip_ratio(xbt)
    path = outp / "archive_1m_sizes.yaml"
    write_yaml(path, rep)
    write_provenance(outp / "provenance_sizes.json", source="local archive directory (read-only)",
                     url_or_endpoint=ARCHIVE_URL_NOTE, local_path=str(src),
                     fetched_or_read_utc=_utcnow(), output_files=[path],
                     elapsed_seconds=round(time.monotonic() - t0, 3))
    return rep


# --------------------------------------------------------------------------- #
# CLI                                                                         #
# --------------------------------------------------------------------------- #
def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("archive", "trades", "compare"):
        p = sub.add_parser(name)
        p.add_argument("--pair", required=True)
        p.add_argument("--day", required=True)
        p.add_argument("--out", required=True)
        if name == "trades":
            p.add_argument("--max-requests", type=int, default=MAX_REQUESTS)
        if name == "archive":
            p.add_argument("--source", required=True)
        if name == "compare":
            p.add_argument("--archive-dir", required=True)
            p.add_argument("--trades-dir", required=True)
    p = sub.add_parser("sizes")
    p.add_argument("--source-dir", required=True)
    p.add_argument("--out", required=True)
    return ap


def main(argv=None, *, exchange_factory=None, sleep=time.sleep) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.cmd == "archive":
            res = run_archive(args.pair, args.day, args.source, args.out)
            if res["stopped"]:
                print(f"sealed_rows={res['sealed_rows']} (non-zero): stopped, nothing written")
                return 3
            print(yaml.safe_dump(_native({"day": res["day_report"],
                                          "whole_file": res["whole_file_report"]}),
                                 sort_keys=False))
        elif args.cmd == "trades":
            res = run_trades(args.pair, args.day, args.out, exchange_factory=exchange_factory,
                             sleep=sleep, max_requests=min(args.max_requests, MAX_REQUESTS))
            print(yaml.safe_dump(_native({k: res[k] for k in
                                          ("requests", "elapsed_seconds", "retries", "errors",
                                           "report")}), sort_keys=False))
        elif args.cmd == "compare":
            print(yaml.safe_dump(_native(run_compare(args.pair, args.day, args.archive_dir,
                                                     args.trades_dir, args.out)),
                                 sort_keys=False))
        else:
            print(yaml.safe_dump(_native(run_sizes(args.source_dir, args.out)), sort_keys=False))
    except ProbeRefusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
