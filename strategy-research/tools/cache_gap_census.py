"""
Timestamp-continuity census over the local OHLCV caches.

Written for the issue #50 policy decision (docs/analysis-reports/
PRESCREEN_GAP_POLICY_20260829.md). Every number quoted in that document is
reproduced by running this file, so the policy's evidence is re-checkable
rather than asserted.

Reports, per symbol x research window:
  - gap pairs: consecutive rows whose timestamp step != the timeframe step.
    These are the pairs prescreen_signal._extract_forecasts currently scores as
    one-bar returns regardless of their true horizon.
  - the contiguous-run structure, which decides how many bootstrap blocks can
    actually be placed without a block spanning a gap.
  - nominal vs gap-aware n_eff, i.e. how much prescreen_signal.
    _block_adjusted_significance's `n_active_bars // block_size` overstates the
    achievable block count.

Read-only. Never touches the sealed holdout store: it globs an explicit
timeframe suffix inside `local_data/` and does not recurse.

Usage (from strategy-research/):
    ../.venv/bin/python tools/cache_gap_census.py
    ../.venv/bin/python tools/cache_gap_census.py --timeframe 1d --warmup 120

Data-quality audit (a separate mode; the default output above is unchanged
when none of these options is given). Needs the trading-bot venv, because it
imports the data-availability gate's own measurement functions:
    --audit [--audit-timeframes 1m,1h,4h,1d] [--warmup-bars N]
        per cache file (coin x timeframe), in-sample rows only: coverage,
        within-life missing, longest gap, missing by policy era, and the
        per-window view for folds A-D (the gate's own _missing_fraction /
        classification). Prints a short summary.
    --write-census [--census-dir DIR]
        also write campaign_record/data_census/census_<UTC>.yaml (refuses to
        overwrite). Read-only for the pipeline: no stage reads this file.
    --run-dir RUN_DIR
        per variant, write artifacts/variants/<v>/data_census.yaml next to its
        data_availability_gate.yaml (that variant's symbols, exchange,
        timeframe and windows). Refuses to overwrite.
Rows at or after the holdout start (campaign_data_policy.yaml, read in code
only) are dropped right after parsing; the sealed span appears as the single
line `sealed: not audited`.
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import math
import os
import re
import statistics
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

# Research windows (config/folds.yaml, config/campaign_data_policy.yaml). The holdout is deliberately
# absent: it is single-use and reading it is spending it.
WINDOWS = {
    "train": (datetime(2018, 1, 1), datetime(2023, 12, 31, 23, 59, 59)),
    "valid": (datetime(2024, 1, 1), datetime(2025, 12, 31, 23, 59, 59)),
}

_STEPS = {"1m": timedelta(minutes=1), "1h": timedelta(hours=1), "4h": timedelta(hours=4),
          "1d": timedelta(days=1)}

_DEFAULT_DATA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "trading-bot", "local_data",
)


def _load(path: str) -> list[tuple[datetime, float | None]]:
    """Rows as (timestamp, close), sorted. Unparseable timestamps are counted by
    the caller, never silently folded into the series."""
    rows, bad_ts = [], 0
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            raw = (r.get("timestamp") or "").strip()
            try:
                t = datetime.fromisoformat(raw)
            except ValueError:
                bad_ts += 1
                continue
            try:
                c = float(r["close"])
            except (TypeError, ValueError, KeyError):
                c = None
            rows.append((t, c))
    rows.sort(key=lambda x: x[0])
    return rows, bad_ts


def _runs(times: list[datetime], step: timedelta) -> list[int]:
    """Lengths of maximal contiguous runs (consecutive rows exactly `step` apart)."""
    if not times:
        return []
    out, cur = [], 1
    for i in range(len(times) - 1):
        if times[i + 1] - times[i] == step:
            cur += 1
        else:
            out.append(cur)
            cur = 1
    out.append(cur)
    return out


def census(rows, lo, hi, step, warmup, block):
    w = [r for r in rows if lo <= r[0] <= hi]
    times = [t for t, _ in w]
    pairs = max(len(w) - 1, 0)
    gaps = worst = 0
    gap_rets, ok_rets = [], []
    for i in range(pairs):
        delta = times[i + 1] - times[i]
        c0, c1 = w[i][1], w[i + 1][1]
        ret = abs((c1 - c0) / c0 * 10_000.0) if (c0 and c1) else None
        if delta != step:
            gaps += 1
            worst = max(worst, delta.total_seconds() / 3600.0)
            if ret is not None:
                gap_rets.append(ret)
        elif ret is not None:
            ok_rets.append(ret)

    runs = _runs(times, step)
    total = sum(runs)
    # The strategy warms up ONCE over the whole series (it is never reset), so
    # the warmup is charged against the leading run(s); each run then loses its
    # last bar, which has no in-run successor.
    rem, run_recs = warmup + 1, []
    for length in runs:
        take = min(rem, length)
        rem -= take
        run_recs.append(max(length - take - 1, 0))

    nominal = max(total - warmup - 1, 0) // block
    gap_aware = sum(r // block for r in run_recs)
    ratio = (nominal / gap_aware) if gap_aware else float("inf")

    # Admission-gate simulation (policy doc S5). Reported under BOTH sample
    # models, because which one you use changes the answer and the doc
    # originally quoted the wrong one:
    #   no_rewarm -- the model the policy ADOPTS: one global warmup, blocks
    #                merely have to fit inside a contiguous run.
    #   rewarm    -- option 3's model, which the policy REJECTS: every segment
    #                pays the warmup again.
    blocks_no_rewarm = gap_aware
    blocks_rewarm = sum(max(length - warmup - 1, 0) // block for length in runs)

    return {
        "pairs": pairs, "gaps": gaps,
        "pct": (gaps / pairs * 100) if pairs else 0.0,
        "worst_h": worst,
        "med_gap_ret": statistics.median(gap_rets) if gap_rets else None,
        "med_ok_ret": statistics.median(ok_rets) if ok_rets else None,
        "n_runs": len(runs),
        "median_run": statistics.median(runs) if runs else 0,
        "nominal_neff": nominal, "gap_aware_neff": gap_aware,
        "ratio": ratio, "z_inflation": math.sqrt(ratio) if ratio != float("inf") else float("inf"),
        "blocks_no_rewarm": blocks_no_rewarm, "blocks_rewarm": blocks_rewarm,
    }


# ===========================================================================
# Data-quality audit mode (--audit / --write-census / --run-dir)
#
# Everything below is additive: none of it runs, and none of its heavy imports
# (pandas, yaml, the gate, the seal guard) are loaded, unless an audit option is
# given. The per-window numbers are the data-availability gate's own functions,
# imported, never copied (tools/data_availability_gate.py: _measure_end,
# _expected_bar_count, _missing_fraction, _missing_runs, classify_missing_fraction,
# _timeframe_to_seconds, _DEFAULT_GAP_TOLERANCE, layer1_warmup_check).
#
# Seal handling (two layers, both always on):
#   1. every cache read goes through tools/seal_safe_cache.read_cache_csv with
#      `end` = (holdout start - 1ns): the request-window guard, then the content
#      backstop on the kept rows;
#   2. immediately after parsing, every row at or after the holdout start is
#      dropped, before any statistic. The holdout start is read from the policy
#      in code only (tools/holdout_policy), used to filter, and never printed.
# The sealed span appears in any output as the single line `sealed: not audited`.
# ===========================================================================

AUDIT_TIMEFRAMES = ("1m", "1h", "4h", "1d")
CENSUS_NOTE = "read-only for the pipeline: no stage reads this file"
SEALED_LINE = "not audited"
TOOL_REL_PATH = "strategy-research/tools/cache_gap_census.py"

_HERE = os.path.dirname(os.path.abspath(__file__))
_SR = os.path.dirname(_HERE)
DEFAULT_CENSUS_DIR = os.path.join(_SR, "campaign_record", "data_census")

_FORBIDDEN_DIR_PARTS = ("holdout_sealed", "recorded_reserved")
_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]*$")
_FOLD_IDS = ("A", "B", "C", "D")


class AuditRefusal(Exception):
    """The audit refuses (a window reaching the holdout, a forbidden directory,
    an existing output, a read the seal guard stopped). Messages never carry a
    sealed date."""


_DEPS = None


def _deps():
    """Lazy imports, so the default census keeps its stdlib-only import."""
    global _DEPS
    if _DEPS is None:
        if _HERE not in sys.path:  # `python -I` does not put the script dir on sys.path
            sys.path.insert(0, _HERE)
        import numpy as np
        import pandas as pd
        import yaml
        import data_availability_gate as gate  # also puts trading-bot on sys.path
        import holdout_policy as hp
        import research_folds as rf
        import seal_safe_cache as ssc
        import variant_coin as vc
        _DEPS = SimpleNamespace(np=np, pd=pd, yaml=yaml, gate=gate, hp=hp, rf=rf, ssc=ssc, vc=vc)
    return _DEPS


def _num(x):
    """An int when integral, else a float rounded to 6 places (YAML-friendly)."""
    x = float(x)
    if abs(x - round(x)) < 1e-9:
        return int(round(x))
    return round(x, 6)


def _day_str(v):
    if v is None:
        return None
    if isinstance(v, str):
        return v[:10]
    iso = getattr(v, "isoformat", None)
    return iso()[:10] if iso else None


def _parts_lower(path) -> set:
    return {p.lower() for p in Path(os.path.abspath(path)).parts} | \
           {p.lower() for p in Path(os.path.realpath(path)).parts}


def refuse_forbidden_dir(path, what: str, extra=()) -> None:
    """Refuse a path with a holdout_sealed / recorded_reserved component (and,
    for a run dir, a local_data one). Nothing is opened or listed first."""
    hit = _parts_lower(path) & {*_FORBIDDEN_DIR_PARTS, *(e.lower() for e in extra)}
    if hit:
        raise AuditRefusal(f"{what} has a forbidden path component ({sorted(hit)[0]}); refusing")


def cache_key(exchange: str, symbol: str, timeframe: str) -> str:
    """The cache file stem the engine uses for a symbol: mirrors
    trading-bot/data/fetchers/ccxt_fetcher.py CcxtFetcher.cache_key (:101-124,
    the rule itself at :123-124): "{symbol}_{tf}" for binance (the historical,
    un-prefixed name), "{exchange}_{symbol}_{tf}" for every other exchange."""
    for what, v in (("exchange", exchange), ("symbol", symbol), ("timeframe", timeframe)):
        if not (isinstance(v, str) and _SAFE_NAME.match(v) and ".." not in v):
            raise AuditRefusal(f"{what} {v!r} is not a plain name; refusing to build a cache path")
    prefix = "" if exchange == "binance" else f"{exchange}_"
    return f"{prefix}{symbol}_{timeframe}"


# --- policy / seal ----------------------------------------------------------

def _context(policy_path=None, warmup_bars=None) -> SimpleNamespace:
    """The holdout start (as a Timestamp, for filtering only), the eras that END
    BEFORE it (as (era_id, lo, hi) day strings; the holdout era and every later
    one are skipped by era_id and never reported), and the audit options."""
    D = _deps()
    policy = D.hp.load_policy(policy_path)
    hs_str = D.hp.holdout_start_of(policy)
    eras = []
    for era in policy.get("eras") or []:
        if not isinstance(era, dict):
            continue
        rng = era.get("range")
        if not (isinstance(rng, (list, tuple)) and len(rng) == 2):
            continue
        lo, hi = _day_str(rng[0]), _day_str(rng[1])
        if not (era.get("era_id") and lo and hi):
            continue
        if lo >= hs_str or hi >= hs_str:  # reaches or follows the holdout: skipped
            continue
        eras.append((str(era["era_id"]), lo, hi))
    return SimpleNamespace(hs=D.pd.Timestamp(hs_str), eras=eras, warmup_bars=warmup_bars,
                           ignore_limit=None)


def check_windows_clear(windows, ctx, group: str) -> None:
    """Refuse (never clip) a window whose measured span reaches the holdout start."""
    D = _deps()
    for i, w in enumerate(windows, 1):
        test = w.get("test") or {}
        if D.pd.Timestamp(D.gate._measure_end(test["end"])) > ctx.hs:
            raise AuditRefusal(f"{group} window #{i} reaches the holdout start "
                               f"(dates withheld): refusing, not clipping")


def read_in_sample(path, ctx):
    """(DatetimeIndex of unique in-sample timestamps, info). Seal layer 1: the
    shared guarded read. Seal layer 2: rows at or after the holdout start are
    dropped right here, before anything is computed; nothing about them is kept."""
    D = _deps()
    pd = D.pd
    try:
        df = D.ssc.read_cache_csv(path, end=ctx.hs - pd.Timedelta(1, "ns"),
                                  usecols=["timestamp"], dtype=str)
    except D.ssc.SealedDataError:
        raise AuditRefusal(f"the seal guard refused the read of {os.path.basename(path)} "
                           f"(details withheld)") from None
    except ValueError as exc:
        raise AuditRefusal(f"{os.path.basename(path)}: cannot read a 'timestamp' column "
                           f"({type(exc).__name__})") from None
    ts = pd.to_datetime(df["timestamp"], format="ISO8601", errors="coerce")
    del df
    if getattr(ts.dt, "tz", None) is not None:
        ts = ts.dt.tz_convert("UTC").dt.tz_localize(None)
    unparseable = int(ts.isna().sum())
    ts = ts[ts < ctx.hs]  # the clamp: NaT and every sealed or later row are gone
    n_rows = len(ts)
    idx = pd.DatetimeIndex(D.np.unique(ts.to_numpy()))
    return idx, {"duplicate_timestamps": n_rows - len(idx), "unparseable_timestamps": unparseable}


# --- measurements (the gate's own functions) --------------------------------

def _slice(idx, start, end):
    """Rows in [start, end], the filter the gate's functions apply themselves."""
    pd = _deps().pd
    lo = idx.searchsorted(pd.Timestamp(start), side="left")
    hi = idx.searchsorted(pd.Timestamp(end), side="right")
    return idx[lo:hi]


def _measure(idx, start, end, step_s):
    """(expected bars, gate missing_fraction, gate missing runs or None, rows in [start, end])."""
    D = _deps()
    sl = _slice(idx, start, end)
    df = D.pd.DataFrame({"timestamp": sl})
    return (D.gate._expected_bar_count(start, end, step_s),
            D.gate._missing_fraction(df, start, end, step_s),
            D.gate._missing_runs(df, start, end, step_s),
            len(sl))


def _missing_bars(expected, runs):
    return float(expected) if runs is None else float(sum(r["bars"] for r in runs))


def _largest(runs, expected):
    """(count, largest bars, after) of a runs list; None runs = the whole span missing."""
    if runs is None:
        return 1, expected, None
    if not runs:
        return 0, 0, None
    best = max(runs, key=lambda r: r["bars"])
    return len(runs), best["bars"], best["after"]


def _ignore_limit(ctx):
    """The gate's own CUL-374 small-gap limit (DEFAULT_GAP_POLICY ignore_max_bars),
    fetched once and only when a window is actually in the refine band."""
    if ctx.ignore_limit is None:
        ctx.ignore_limit = _deps().gate._engine_ignore_max_bars()
    return ctx.ignore_limit


def _gate_outcome(classification, runs, ctx):
    """check_price_window's own refine -> validate rule (gate :731-744): within
    tolerance AND every missing stretch no longer than the engine's ignore tier."""
    if classification == "refine" and runs and all(r["bars"] <= _ignore_limit(ctx) + 1e-9 for r in runs):
        return "validate"
    return classification


def _window_record(idx, first, win, tf, step_s, ctx):
    D = _deps()
    test = win["test"]
    w_start = D.pd.Timestamp(test["start"]).to_pydatetime()
    w_end = D.gate._measure_end(test["end"])
    expected, frac, runs, nrows = _measure(idx, w_start, w_end, step_s)
    cls = D.gate.classify_missing_fraction(frac)
    n_runs, largest, _after = _largest(runs, expected)
    rec = {"label": win.get("label"), "start": str(test["start"])[:10], "end": str(test["end"])[:10],
           "expected_bars": expected, "rows": nrows, "missing_fraction": float(frac),
           "classification": cls, "gate_outcome": _gate_outcome(cls, runs, ctx),
           "missing_runs": n_runs, "largest_run_bars": _num(largest)}
    if runs is None:
        rec["no_rows_in_window"] = True
    if ctx.warmup_bars is not None:
        n = int(ctx.warmup_bars)
        if first is None:
            avail, ok = 0, n <= 0
        else:
            # layer1_warmup_check (gate :449-480) on this cache's own first bar; the
            # count below is its formula (:473), whole bars between first bar and window start.
            stub = {"venues": {"x": {"spot": {"symbols": {"earliest_ohlcv_utc": {"c": str(first)}}}}}}
            ok = D.gate.layer1_warmup_check(stub, "x", "c", tf, w_start, n)[0]
            avail = max(int((w_start - first.to_pydatetime()).total_seconds() // step_s), 0)
        rec["warmup_bars_available"] = avail
        rec["warmup_rows_present"] = int(idx.searchsorted(D.pd.Timestamp(w_start), side="left"))
        rec["warmup_ok"] = bool(ok)
    return rec


def _window_view(idx, first, windows, tf, step_s, ctx):
    D = _deps()
    recs = [_window_record(idx, first, w, tf, step_s, ctx) for w in windows]
    counts = {k: sum(r["classification"] == k for r in recs) for k in ("validate", "refine", "decline")}
    counts_gate = {k: sum(r["gate_outcome"] == k for r in recs) for k in ("validate", "refine", "decline")}
    n = len(recs)
    covered = counts_gate["validate"]
    min_cov = D.vc.D042_MIN_WINDOW_COVERAGE
    d042 = {"windows_total": n, "windows_validate": covered,
            "fraction": (covered / n) if n else 0.0, "min_window_coverage": min_cov,
            "meets_min_window_coverage": bool(n and covered / n >= min_cov),
            "basis": "gate_outcome == validate; reported as a fact, D-042 is not re-implemented"}
    if ctx.warmup_bars is not None:
        warm = sum(r["gate_outcome"] == "validate" and r["warmup_ok"] for r in recs)
        d042["warmup_bars"] = int(ctx.warmup_bars)
        d042["windows_validate_and_warm"] = warm
        d042["fraction_with_warmup"] = (warm / n) if n else 0.0
        d042["meets_min_window_coverage_with_warmup"] = bool(n and warm / n >= min_cov)
    return {"windows": recs, "counts": counts, "counts_gate_outcome": counts_gate, "d042_reading": d042}


def audit_index(idx, info, tf, ctx, groups):
    """The per-file audit over the in-sample timestamps `idx` (sorted, unique)."""
    D = _deps()
    pd = D.pd
    step_s = D.gate._timeframe_to_seconds(tf)
    first = idx[0] if len(idx) else None
    last = idx[-1] if len(idx) else None
    out = {"coverage": {"first_bar": None if first is None else str(first),
                        "last_in_sample_bar": None if last is None else str(last),
                        "rows": int(len(idx)), **info}}
    if first is None:
        out["within_life"] = None
        out["longest_gap"] = None
        out["by_era"] = {e: "not_listed" for e, _, _ in ctx.eras}
    else:
        expected = D.gate._expected_bar_count(first, last, step_s) + 1
        runs = D.gate._missing_runs(pd.DataFrame({"timestamp": idx}), first, last, step_s) or []
        missing = _missing_bars(expected, runs)
        out["within_life"] = {"expected_bars": expected, "missing_bars": _num(missing),
                              "missing_pct": round(100.0 * missing / expected, 6) if expected else 0.0}
        _n, largest, after = _largest(runs, expected)
        out["longest_gap"] = {"bars": _num(largest), "after": after}
        by_era = {}
        step_td = pd.Timedelta(seconds=step_s)
        for era_id, lo, hi in ctx.eras:
            era_end = pd.Timestamp(D.gate._measure_end(hi))
            s = max(pd.Timestamp(lo), first)
            e = min(era_end, last + step_td)
            n_exp = D.gate._expected_bar_count(s, e, step_s) if (era_end > first and s <= last) else 0
            if n_exp <= 0:
                by_era[era_id] = "not_listed"
                continue
            _, _, eruns, _ = _measure(idx, s, e, step_s)
            miss = _missing_bars(n_exp, eruns)
            by_era[era_id] = {"expected_bars": n_exp, "missing_bars": _num(miss),
                              "missing_pct": round(100.0 * miss / n_exp, 6)}
        out["by_era"] = by_era
    out["views"] = {g: _window_view(idx, first, wins, tf, step_s, ctx) for g, wins in groups.items()}
    return out


def audit_cache_file(path, tf, ctx, groups):
    idx, info = read_in_sample(path, ctx)
    res = audit_index(idx, info, tf, ctx, groups)
    return {"file": os.path.basename(path), **res}


# --- header -----------------------------------------------------------------

def tool_blob_sha() -> str:
    """The git blob sha of this file (git hash-object, which applies the repo's
    line-ending filter; a byte hash of the LF-normalised file as the fallback)."""
    path = os.path.abspath(__file__)
    try:
        r = subprocess.run(["git", "hash-object", path], capture_output=True, text=True,
                           timeout=30, cwd=os.path.dirname(path))
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    data = Path(path).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _header(kind, data_dir, timeframes, now, ctx, **extra):
    D = _deps()
    now = now or datetime.now(timezone.utc)
    return {"kind": kind, "tool": TOOL_REL_PATH, "tool_git_blob_sha": tool_blob_sha(),
            "data_dir": str(data_dir).replace("\\", "/"), "timeframes": list(timeframes),
            "gap_tolerance": D.gate._DEFAULT_GAP_TOLERANCE,
            "warmup_bars": ctx.warmup_bars,
            "utc_run_time": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "note": CENSUS_NOTE, **extra}


def _parse_timeframes(timeframes):
    D = _deps()
    tfs = [t.strip() for t in (timeframes.split(",") if isinstance(timeframes, str) else timeframes) if t.strip()]
    if not tfs:
        raise AuditRefusal("no timeframes given")
    for tf in tfs:
        if not D.gate._timeframe_to_seconds(tf):
            raise AuditRefusal(f"timeframe {tf!r} is not a parseable interval")
    return tfs


# --- Output A: the campaign-level census -----------------------------------

def run_audit(data_dir, timeframes=AUDIT_TIMEFRAMES, *, policy_path=None, folds_doc=None,
              folds_path=None, warmup_bars=None, now=None) -> dict:
    """The census document (header, `sealed`, and per timeframe the per-file audit).
    Globs `*_{tf}.csv` directly inside `data_dir`, non-recursively, as the default census does."""
    D = _deps()
    tfs = _parse_timeframes(timeframes)
    refuse_forbidden_dir(data_dir, "the data dir")
    ctx = _context(policy_path, warmup_bars)
    doc = folds_doc if folds_doc is not None else D.rf.load_folds(folds_path, policy_path=policy_path)
    groups = {fid: D.rf.fold_windows(doc, fid) for fid in _FOLD_IDS if fid in doc["folds"]}
    for fid, wins in groups.items():
        check_windows_clear(wins, ctx, f"fold {fid}")
    sha = {fid: (D.rf.fold_windows_sha256(doc, fid) if wins else None) for fid, wins in groups.items()}
    out_tfs = {}
    for tf in tfs:
        files = sorted(glob.glob(os.path.join(str(data_dir), f"*_{tf}.csv")))
        entry = {}
        for path in files:
            if not os.path.isfile(path):
                continue
            stem = os.path.basename(path)[: -len(f"_{tf}.csv")]
            res = audit_cache_file(path, tf, ctx, groups)
            res["folds"] = res.pop("views")
            entry[stem] = res
        out_tfs[tf] = {"files": entry}
    return {"header": _header("data_census", data_dir, tfs, now, ctx, folds_windows_sha256=sha),
            "sealed": SEALED_LINE, "timeframes": out_tfs}


def census_summary(census: dict) -> str:
    lines = [f"data census | sealed: {census['sealed']}"]
    for tf, body in census["timeframes"].items():
        files = body["files"]
        lines.append("")
        lines.append(f"== {tf} ({len(files)} caches) | fold cells are validate/refine/decline ==")
        if not files:
            lines.append("  no caches matched")
            continue
        lines.append(f"{'coin':22} {'first_bar':19} {'last_in_sample_bar':19} {'miss%':>8} "
                     f"{'longest_gap':32} {'A':>7} {'B':>7} {'C':>7} {'D':>7}")
        for stem, r in files.items():
            cov, wl, lg = r["coverage"], r["within_life"], r["longest_gap"]
            miss = f"{wl['missing_pct']:.3f}" if wl else "-"
            gap = f"{lg['bars']:g} after {lg['after']}" if lg and lg["bars"] else "-"
            cells = []
            for fid in _FOLD_IDS:
                c = r["folds"].get(fid, {}).get("counts")
                cells.append("/".join(str(c[k]) for k in ("validate", "refine", "decline")) if c else "-")
            lines.append(f"{stem:22} {str(cov['first_bar'] or '-'):19} "
                         f"{str(cov['last_in_sample_bar'] or '-'):19} {miss:>8} {gap:32} "
                         + " ".join(f"{c:>7}" for c in cells))
    return "\n".join(lines)


def write_new_yaml(path, doc) -> str:
    """Write `doc` as YAML to a path that must not exist (mode 'x'); refuse otherwise."""
    D = _deps()
    text = D.yaml.safe_dump(doc, sort_keys=False, default_flow_style=False, allow_unicode=True)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "x", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    except FileExistsError:
        raise AuditRefusal(f"{path} already exists; refusing to overwrite") from None
    return str(path)


def write_census(census, census_dir, now=None) -> str:
    stamp = census["header"]["utc_run_time"].replace("-", "").replace(":", "")
    return write_new_yaml(Path(census_dir) / f"census_{stamp}.yaml", census)


# --- Output B: the per-run artifact ----------------------------------------

def _normalise_windows(raw):
    out = []
    for w in raw or []:
        test = w.get("test") if isinstance(w.get("test"), dict) else w
        s, e = _day_str(test.get("start")), _day_str(test.get("end"))
        if s and e:
            out.append({"label": w.get("label"), "test": {"start": s, "end": e}})
    return out


def variant_params(gate_rec: dict, protocol: dict | None):
    """(exchange, timeframe, symbols, windows, source-of-each) for one variant:
    the gate record's own values, falling back to the run protocol only where the
    record lacks them."""
    protocol = protocol or {}
    src = {}
    ex = gate_rec.get("exchange")
    src["exchange"] = "gate_record"
    if not ex:
        ex, src["exchange"] = protocol.get("exchange"), "run_protocol"
    if not ex:
        ex, src["exchange"] = "binance", "default (the gate's own resolve_exchange default)"
    tf = gate_rec.get("timeframe")
    src["timeframe"] = "gate_record"
    if not tf:
        tf, src["timeframe"] = protocol.get("timeframe"), "run_protocol"
    syms = gate_rec.get("symbols")
    src["symbols"] = "gate_record"
    if not syms:
        syms, src["symbols"] = protocol.get("symbols"), "run_protocol"
    seen, wins = set(), []
    for w in gate_rec.get("windows") or []:
        s, e = _day_str(w.get("start")), _day_str(w.get("end"))
        if s and e and (w.get("label"), s, e) not in seen:
            seen.add((w.get("label"), s, e))
            wins.append({"label": w.get("label"), "test": {"start": s, "end": e}})
    src["windows"] = "gate_record"
    if not wins:
        wins, src["windows"] = _normalise_windows(protocol.get("windows")), "run_protocol"
    if not (tf and syms and wins):
        raise AuditRefusal("neither the gate record nor the run protocol gives this variant's "
                           "timeframe, symbols and windows")
    return ex, tf, list(syms), wins, src


def run_census_for_run(run_dir, data_dir, *, policy_path=None, warmup_bars=None, now=None) -> list:
    """Write artifacts/variants/<v>/data_census.yaml next to each variant's
    data_availability_gate.yaml. All-or-nothing on overwrite: every target is checked first."""
    D = _deps()
    refuse_forbidden_dir(run_dir, "the run dir", extra=("local_data",))
    refuse_forbidden_dir(data_dir, "the data dir")
    vdir = Path(run_dir) / "artifacts" / "variants"
    records = sorted(vdir.glob("*/data_availability_gate.yaml"))
    if not records:
        raise AuditRefusal("no artifacts/variants/*/data_availability_gate.yaml under the run dir")
    ctx = _context(policy_path, warmup_bars)
    protocol, plans = None, []
    for rec_path in records:
        gate_rec = D.yaml.safe_load(rec_path.read_text(encoding="utf-8")) or {}
        needs_protocol = not (gate_rec.get("exchange") and gate_rec.get("timeframe")
                              and gate_rec.get("symbols")
                              and any(w.get("start") and w.get("end")
                                      for w in gate_rec.get("windows") or [] if isinstance(w, dict)))
        if needs_protocol and protocol is None:
            pp = vdir / "run_protocol.json"
            if pp.is_file():
                protocol = json.loads(pp.read_text(encoding="utf-8"))
        gate_rec["windows"] = [w for w in gate_rec.get("windows") or [] if isinstance(w, dict)]
        ex, tf, syms, wins, src = variant_params(gate_rec, protocol)
        check_windows_clear(wins, ctx, f"variant {rec_path.parent.name}")
        target = rec_path.parent / "data_census.yaml"
        if target.exists():
            raise AuditRefusal(f"{target} already exists; refusing to overwrite")
        plans.append((rec_path, target, ex, tf, syms, wins, src))
    written = []
    for rec_path, target, ex, tf, syms, wins, src in plans:
        symbols = {}
        for sym in syms:
            path = os.path.join(str(data_dir), cache_key(ex, sym, tf) + ".csv")
            if not os.path.isfile(path):
                symbols[sym] = {"file": os.path.basename(path), "status": "cache_missing"}
                continue
            res = audit_cache_file(path, tf, ctx, {"windows": wins})
            res["window_view"] = res.pop("views")["windows"]
            symbols[sym] = res
        doc = {"header": _header("data_census_run", data_dir, [tf], now, ctx,
                                 variant=rec_path.parent.name,
                                 gate_record="data_availability_gate.yaml",
                                 exchange=ex, timeframe=tf, symbols=list(syms), params_source=src),
               "sealed": SEALED_LINE, "windows": wins, "symbols": symbols}
        written.append(write_new_yaml(target, doc))
    return written


def _audit_main(args) -> int:
    try:
        if args.run_dir:
            if args.audit or args.write_census:
                raise AuditRefusal("--run-dir cannot be combined with --audit / --write-census")
            for p in run_census_for_run(args.run_dir, args.data_dir, warmup_bars=args.warmup_bars):
                print(f"wrote {p}")
            print(f"sealed: {SEALED_LINE}")
            return 0
        if not args.audit:
            raise AuditRefusal("--write-census needs --audit")
        census = run_audit(args.data_dir, args.audit_timeframes, warmup_bars=args.warmup_bars)
        print(census_summary(census))
        if args.write_census:
            print(f"\nwrote {write_census(census, args.census_dir)}")
        return 0
    except AuditRefusal as exc:
        raise SystemExit(f"refused: {exc}") from None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", default=_DEFAULT_DATA)
    ap.add_argument("--timeframe", default="1h", choices=sorted(_STEPS))
    ap.add_argument("--warmup", type=int, default=120,
                    help="bars the strategy needs before is_ready() (default: 120)")
    ap.add_argument("--block", type=int, default=24,
                    help="bootstrap block size (default: 24, matching "
                         "prescreen_signal._BLOCK_SIZE_1H)")
    ap.add_argument("--gate-floor", type=int, action="append", default=None,
                    help="simulate the S5 admission gate at this minimum block "
                         "count; repeatable (default: 8 = _MIN_N_EPISODES, and "
                         "30 = the fork promotion bar)")
    # --- data-quality audit options (a separate mode; see the module docstring)
    ap.add_argument("--audit", action="store_true",
                    help="data-quality audit over the caches (needs the trading-bot venv)")
    ap.add_argument("--audit-timeframes", default=",".join(AUDIT_TIMEFRAMES),
                    help="comma list for --audit (default: %(default)s)")
    ap.add_argument("--warmup-bars", type=int, default=None,
                    help="--audit/--run-dir: also report, per window, the in-sample bars "
                         "available before the window start vs this number (D-169 reading)")
    ap.add_argument("--write-census", action="store_true",
                    help="with --audit: write census_<UTC>.yaml into --census-dir "
                         "(refuses to overwrite)")
    ap.add_argument("--census-dir", default=DEFAULT_CENSUS_DIR)
    ap.add_argument("--run-dir", default=None,
                    help="write artifacts/variants/<v>/data_census.yaml for each variant of "
                         "this run (refuses to overwrite)")
    args = ap.parse_args(argv)
    if args.audit or args.write_census or args.run_dir:
        return _audit_main(args)
    floors = args.gate_floor or [8, 30]

    step = _STEPS[args.timeframe]
    pattern = os.path.join(args.data_dir, f"*_{args.timeframe}.csv")
    files = sorted(glob.glob(pattern))
    if not files:
        raise SystemExit(f"no caches matched {pattern}")

    print(f"{len(files)} {args.timeframe} caches | warmup={args.warmup} block={args.block}\n")
    hdr = (f"{'symbol':22} {'win':6} {'pairs':>7} {'gaps':>6} {'%':>7} {'worst':>7} "
           f"{'runs':>6} {'medrun':>7} {'nom':>6} {'gapaware':>9} {'z infl':>7}")
    print(hdr)
    print("-" * len(hdr))

    out, gappy, combos, bad_total = [], 0, 0, 0
    for path in files:
        sym = os.path.basename(path)[: -len(f"_{args.timeframe}.csv")]
        rows, bad_ts = _load(path)
        bad_total += bad_ts
        for wname, (lo, hi) in WINDOWS.items():
            c = census(rows, lo, hi, step, args.warmup, args.block)
            if c["pairs"] == 0:
                continue
            combos += 1
            gappy += 1 if c["gaps"] else 0
            out.append((c["pct"], sym, wname, c))

    for _, sym, wname, c in sorted(out, reverse=True):
        worst = f"{c['worst_h']:.0f}h" if c["gaps"] else "-"
        print(f"{sym:22} {wname:6} {c['pairs']:7d} {c['gaps']:6d} {c['pct']:6.2f}% "
              f"{worst:>7} {c['n_runs']:6d} {c['median_run']:7.0f} "
              f"{c['nominal_neff']:6d} {c['gap_aware_neff']:9d} {c['z_inflation']:6.2f}x")

    print(f"\n{gappy} of {combos} symbol x window combinations contain at least one gap")

    # --- S5 admission-gate simulation -------------------------------------
    print("\nADMISSION GATE (policy doc S5) -- would it reject anything?")
    print("  A block spanning a gap is the defect, so blocks must fit inside a")
    print("  contiguous run. ADMIT iff placeable blocks >= floor.\n")
    for model, key in (("no-re-warm (ADOPTED)", "blocks_no_rewarm"),
                       ("re-warm    (REJECTED)", "blocks_rewarm")):
        for floor in floors:
            stopped = [(sym, wn) for _, sym, wn, c in out if c[key] < floor]
            verdict = ("admits all %d" % combos) if not stopped else \
                      ("stops %d: %s" % (len(stopped),
                                         ", ".join(f"{s_} {w_}" for s_, w_ in stopped)))
            print(f"  {model}  floor {floor:>3}: {verdict}")
    print("\n  The gate was DROPPED: under the adopted model it rejects nothing at")
    print("  either floor. Raising the floor until it bit would have been the")
    print("  post-hoc threshold-fitting the policy exists to prevent.")
    if bad_total:
        print(f"NOTE: {bad_total} row(s) had an unparseable timestamp and were excluded "
              f"from the series (see issue #50's residual on the lexical window filter).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
