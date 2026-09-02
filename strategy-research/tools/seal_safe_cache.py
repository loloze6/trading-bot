"""Seal-safe cache reads for the research tools (CUL-203).

The trading-bot engine reads OHLCV through `data_manager.fetch_historical_data`,
which carries the read-path seal guards. The research panels/tools instead read
`local_data` caches directly with `pd.read_csv`, bypassing those guards entirely
-- a hole in the same holdout-safety class the engine guard closes (the
`.gitignore` seal-exclusion comment flags exactly this: "no range check exists
anywhere today").

This is the ONE shared loader every tool cache read routes through. It reuses the
engine's single seal definition (`data_manager._holdout_bounds`, via the guards
imported below) -- never a second definition:

  * request-window mode -- an `end` is given (a train/validation clamp): refuse
    BEFORE reading when the requested window reaches the seal
    (`_assert_request_window_unsealed`).
  * content mode -- no window, the whole cache is loaded: the loaded frame must
    carry no rows inside the seal (`_assert_no_sealed_rows`; needs a 'timestamp'
    column, parsed on a throwaway probe so the returned frame is untouched).

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
)

__all__ = ["SealedDataError", "_holdout_bounds", "read_cache_csv"]

# Unbounded-past lower bound for a one-sided (end-only) window: any real start is
# later, so the overlap reduces to "does `end` reach the seal". Not a date literal
# -- the seal itself is derived inside the guard.
_UNBOUNDED_PAST = pd.Timestamp.min


def read_cache_csv(path, *, end=None, allow_sealed=False, **read_csv_kwargs):
    """Read a `local_data` cache CSV with the read-path seal guard applied.

    `end`: the caller's hard upper bound when it has one (a train/validation
    clamp). Given, the request-window guard refuses before reading if `[.., end]`
    reaches the seal. Absent, the loaded frame itself must carry no sealed rows
    (requires a 'timestamp' column). `allow_sealed=True` bypasses both.

    Every other keyword is forwarded to `pd.read_csv` unchanged, and the returned
    frame is exactly that call's result -- a guarded read on non-sealed data is
    byte-identical to the raw read it replaces.
    """
    if not allow_sealed and end is not None:
        _assert_request_window_unsealed(_UNBOUNDED_PAST, end, str(path))
    df = pd.read_csv(path, **read_csv_kwargs)
    if not allow_sealed and end is None and "timestamp" in df.columns:
        # Probe on a throwaway frame with parsed timestamps: the cache stores
        # them as strings, and the engine guard compares against Timestamps. The
        # returned `df` keeps its original (unparsed) columns, untouched.
        _assert_no_sealed_rows(
            pd.DataFrame({"timestamp": pd.to_datetime(df["timestamp"], errors="coerce")}),
            str(path),
        )
    return df
