"""Seal-safe cache reads for the research tools (CUL-203).

The trading-bot engine reads OHLCV through `data_manager.fetch_historical_data`,
which carries the read-path seal guards. The research panels/tools instead read
`local_data` caches directly with `pd.read_csv`, bypassing those guards entirely
-- a hole in the same holdout-safety class the engine guard closes (the
`.gitignore` seal-exclusion comment flags exactly this: "no range check exists
anywhere today").

This is the ONE shared loader every tool cache read routes through. It reuses the
engine's single seal definition (`data_manager._holdout_bounds`, via the guards
imported below) -- never a second definition. Two layers, both always active
(unless `allow_sealed=True`), mirroring `fetch_historical_data`:

  * request-window guard (when `end` is given) -- refuse BEFORE reading if the
    window `[.., end]` reaches the seal (`_assert_request_window_unsealed`). It
    denies (raises), never silently returns, on a bound that is not an unambiguous
    naive date -- tz-aware is normalised, an epoch int or other non-date raises.
  * content backstop (always) -- after reading, inspect the rows the caller will
    KEEP (`<= end`, or the whole frame with no `end`) and refuse any inside the
    seal (`_assert_no_sealed_rows`). A cache without the timestamp column raises
    rather than skipping silently.

`allow_sealed=True` bypasses both -- the same visible escape the engine uses for
the single deliberate holdout evaluation.

Bit-identity: for every train read the returned frame is exactly
`pd.read_csv(path, **kwargs)`. Train windows end <= 2025-12-31 (no seal overlap)
and the panel caches (`kraken_`/`binanceperp_`) physically end 2025-12-31, so
both checks are no-ops -- proven by hash equality in the tests.
"""

import os
import sys

import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_SR = os.path.dirname(_HERE)
_REPO = os.path.dirname(_SR)
_TBOT = os.path.join(_REPO, "trading-bot")
if _TBOT not in sys.path:
    sys.path.insert(0, _TBOT)

from data.data_manager import (  # noqa: E402  (single seal definition; reused, never redefined)
    SealedDataError,
    _assert_no_sealed_rows,
    _assert_request_window_unsealed,
    _holdout_bounds,  # re-exported so tools/tests derive the seal from one place
    _naive_bound,
)

__all__ = ["SealedDataError", "_holdout_bounds", "read_cache_csv"]

# Unbounded-past lower bound for a one-sided (end-only) window: any real start is
# later, so the overlap reduces to "does `end` reach the seal". Not a date literal
# -- the seal itself is derived inside the guard.
_UNBOUNDED_PAST = pd.Timestamp.min


def _assert_returned_frame_unsealed(df, *, end, timestamp_col, name):
    """Content backstop on the rows the caller will KEEP.

    Runs REGARDLESS of `end` (CUL-203 red-team F1(b)), mirroring
    `fetch_historical_data`'s unconditional content check: even if the request-
    window guard were ever fooled, the returned frame is still inspected. With an
    `end` the kept rows are those `<= end` (the caller clamps there), so a cache
    that legitimately extends past `end` is not falsely refused; with no `end` the
    whole frame is kept. Fail loud if the timestamp column is absent — a cache we
    cannot time-check cannot be certified seal-free. Does not mutate `df`.
    """
    if df is None or getattr(df, "empty", True):
        return
    if timestamp_col not in df.columns:
        raise SealedDataError(
            f"{name}: no {timestamp_col!r} column — cannot verify the cache carries no "
            f"sealed rows. Pass timestamp_col= naming the real timestamp column, or fix "
            f"the cache."
        )
    ts = pd.to_datetime(df[timestamp_col], errors="coerce")
    if end is not None:
        ts = ts[ts <= _naive_bound(end, "end", name)]  # kept portion only
    _assert_no_sealed_rows(pd.DataFrame({"timestamp": ts.to_numpy()}), name)


def read_cache_csv(path, *, end=None, timestamp_col="timestamp", allow_sealed=False, **read_csv_kwargs):
    """Read a `local_data` cache CSV with the read-path seal guard applied.

    `end`: the caller's hard upper clamp when it has one (a train/validation
    window). Given, the request-window guard refuses BEFORE reading if `[.., end]`
    reaches the seal — and it denies (raises), never silently returns, on a bound
    that is not an unambiguous naive date (tz-aware is normalised; an epoch int or
    other non-date raises). AFTER reading, the content backstop then inspects the
    rows the caller will keep (`<= end`, or the whole frame with no `end`) and
    refuses any that fall inside the seal — this runs regardless of `end`, so the
    guard cannot fail open. `timestamp_col` names the column to time-check (a cache
    without it raises rather than skipping silently). `allow_sealed=True` bypasses
    both.

    Every other keyword is forwarded to `pd.read_csv` unchanged, and the returned
    frame is exactly that call's result — a guarded read on non-sealed data is
    byte-identical to the raw read it replaces (the content check reads a throwaway
    parse of the timestamp column and never touches `df`).
    """
    if not allow_sealed and end is not None:
        _assert_request_window_unsealed(_UNBOUNDED_PAST, end, str(path))
    df = pd.read_csv(path, **read_csv_kwargs)
    if not allow_sealed:
        _assert_returned_frame_unsealed(df, end=end, timestamp_col=timestamp_col, name=str(path))
    return df
