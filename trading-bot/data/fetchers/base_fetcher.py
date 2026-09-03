"""
BaseFetcher
===========
Abstract base class for all data fetchers — price and non-price alike.

Every fetcher, regardless of what it fetches (OHLCV, funding rates, fear &
greed index, on-chain metrics…), needs the same operational plumbing:
  • local CSV storage so data is not re-fetched on every run
  • gap detection against an existing local file
  • incremental fetch of only the missing periods
  • deduplication and chronological sorting before saving
  • date-window filtering after merging
  • continuity validation for post-load diagnostics

All of that logic lives here once.  Subclasses only implement:
  • _fetch_remote(symbol, start, end) → pd.DataFrame
    Fetch one contiguous block from whatever remote source they wrap.
    The returned DataFrame MUST have at least a 'timestamp' column.

  • cache_key(symbol) → str
    The stem used for the local CSV filename, e.g. 'BTCUSDT_1m' or
    'fear_greed_daily'.  Keeps each subclass's files in its own namespace.

Optionally subclasses can override:
  • expected_gap_tolerance — multiplier on expected interval before a gap
    is flagged (default 1.5).  Daily macro data might warrant a higher
    value to tolerate weekends.
"""

import os
import datetime
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger("trading_bot")


def _utc_epoch_ms(dt: datetime.datetime) -> int:
    """
    Convert a datetime/Timestamp denoting a UTC instant to epoch-ms, correctly
    for both tz-naive and tz-aware inputs.

    The fetch path normally passes tz-NAIVE values standing for UTC
    (data_manager.py:610): _identify_missing_periods emits plain
    datetime.datetime, and self.start_date/self.end_date are naive. But an
    aware value can also arrive (e.g. the cadence regression test drives an
    aware-UTC start), so both are handled:

      * naive  -> .replace(tzinfo=utc): datetime.datetime.timestamp() on a
        naive value would otherwise interpret it in the host LOCAL zone and
        shift the epoch by the host UTC offset on a non-UTC host (CUL-248,
        the bug this helper closes). Same round-trip data_manager._align uses
        (data_manager.py:634).
      * aware  -> left as-is; its .timestamp() is already the correct instant.
        We deliberately do NOT .replace() an aware value, which would OVERWRITE
        a real offset (e.g. +02:00 mis-read as UTC) and mis-place the epoch.

    An aware value is trusted, not rejected: it is an unambiguous instant, not
    a degenerate input. Only the naive case carried the tz ambiguity CUL-248 fixed.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return int(dt.timestamp() * 1000)


class FetchGapError(RuntimeError):
    """
    Raised at the WRITE boundary when a fetch would introduce a NEW hole into a
    series that was previously continuous across that span.

    Motivating defect (2026-07-23): Kraken's public OHLC endpoint serves a fixed
    rolling ~720-candle window and silently IGNORES `since`. Asking it for
    2026-01-01 onward returns only the last 30 days. `_fetch_remote`'s
    `if not candles: break` then exits cleanly, `_merge_and_store` writes the
    result, and the run logs a successful fetch — leaving a ~173-day hole in the
    middle of the cache with nothing anywhere reporting a problem. A wrong-data
    read that announces itself as success is the worst shape a data defect can
    take: every downstream consumer inherits it and none can detect it.

    The guard is deliberately DIFFERENTIAL. Archive-ingested caches carry real
    natural gaps (INJ ~5.7%, DOGE ~5.1% within-life missing bars are on record),
    so an absolute "no internal gaps" rule would reject every cache the campaign
    already depends on. Only a gap covering time that was NOT already gapped
    fails the write.
    """


class BaseFetcher(ABC):
    """
    Shared plumbing for all data fetchers.

    Subclasses must implement _fetch_remote() and cache_key().
    Everything else — gap detection, local storage, merging, filtering — is
    inherited and works identically for price data, funding rates, or any
    other time-series.
    """

    # Subclasses may raise this to tolerate larger natural gaps
    # (e.g. weekends in macro data).  1.5 = flag gaps > 1.5× expected interval.
    expected_gap_tolerance: float = 1.5

    # When True, a failed OPTIONAL gap-fill (a raising _fetch_remote, or a
    # FetchGapError from _merge_and_store refusing a non-connecting response)
    # falls back to the already-cached rows that cover the window instead of
    # propagating. OFF by default so write/append callers (e.g. the capture
    # tools) keep failing loud; the read-only backtest path opts in via
    # DataManager.fetch_historical_data. See _load_all.
    tolerate_fill_failure: bool = False

    def __init__(
        self,
        start_date,
        end_date,
        symbols: List[str],
        interval_seconds: int,
        localStorage: bool = False,
        data_dir: str = "data",
    ):
        """
        Args:
            start_date:       Start of the desired window (str 'YYYY-MM-DD' or datetime).
            end_date:         End of the desired window (inclusive).
            symbols:          List of identifiers to fetch (e.g. ['BTCUSDT'] or
                              ['fear_greed'] — whatever the subclass understands).
            interval_seconds: Native resolution of this feed in seconds.
                              Used for gap detection arithmetic.
            localStorage:     If True, save fetched data to disk and load from 
                              there on subsequent calls.
            data_dir:         Root directory for all cached CSV files.
        """
        self.start_date      = pd.to_datetime(start_date) if isinstance(start_date, str) else start_date
        self.end_date        = pd.to_datetime(end_date)   if isinstance(end_date,   str) else end_date
        self.symbols         = symbols
        self.interval_seconds = interval_seconds
        self.localStorage    = localStorage
        self.data_dir        = data_dir

        self.data_cache: dict  = {}   # symbol → DataFrame
        self.data_loaded: bool = False

        os.makedirs(self.data_dir, exist_ok=True)

    # -----------------------------------------------------------------------
    # Abstract interface — subclasses must implement these
    # -----------------------------------------------------------------------

    @abstractmethod
    def _fetch_remote(
        self, symbol: str, start: datetime.datetime, end: datetime.datetime
    ) -> pd.DataFrame:
        """
        Fetch one contiguous block of data from the remote source.

        The returned DataFrame must contain at least a 'timestamp' column
        (pd.Timestamp or datetime-compatible).  Additional columns are
        source-specific (e.g. open/high/low/close/volume for price data,
        or 'value'/'funding_rate' for auxiliary feeds).

        Return an empty DataFrame on failure — do not raise.
        """
        ...

    @abstractmethod
    def cache_key(self, symbol: str) -> str:
        """
        Return the CSV filename stem for this symbol.

        Examples:
            CcxtFetcher    → 'BTCUSDT_5m'
            FearGreedFetcher → 'fear_greed_daily'
            FundingRateFetcher → 'BTCUSDT_funding_8h'
        """
        ...

    # -----------------------------------------------------------------------
    # Public API (same for all subclasses)
    # -----------------------------------------------------------------------

    def get_data(self, symbol: str = None):
        """
        Return loaded data, triggering a fetch-and-cache cycle on first call.

        Args:
            symbol: return only this symbol's DataFrame, or None for all.
        """
        if not self.data_loaded:
            self._load_all()
        if symbol:
            return self.data_cache.get(symbol, pd.DataFrame())
        return self.data_cache

    def validate_data_continuity(self, symbol: str) -> Tuple[bool, list]:
        """
        Scan cached data for gaps larger than tolerance × expected interval.

        Returns:
            (is_continuous, gaps) where gaps is a list of (start_ts, end_ts).
        """
        if symbol not in self.data_cache or self.data_cache[symbol].empty:
            return False, []

        data       = self.data_cache[symbol].sort_values("timestamp")
        expected   = np.timedelta64(int(self.interval_seconds), "s")
        timestamps = data["timestamp"].values

        gaps = [
            (timestamps[i - 1], timestamps[i])
            for i in range(1, len(timestamps))
            if timestamps[i] - timestamps[i - 1]
            > expected * self.expected_gap_tolerance
        ]
        return len(gaps) == 0, gaps

    # -----------------------------------------------------------------------
    # Orchestration (identical for every subclass)
    # -----------------------------------------------------------------------

    def _load_all(self):
        """
        For each symbol: load existing local data, detect missing periods,
        fetch them, merge, trim to the requested window, and cache.
        """
        window_end = self._inclusive_end(self.end_date)

        for symbol in self.symbols:
            existing = self._load_local(symbol) if self.localStorage else pd.DataFrame()
            # window_end, not end_date: expanding "through that whole day" ONCE,
            # here, means every period end below is already literal. Deriving it
            # per-period instead is not possible -- a type-1 end computed as
            # `earliest - 1ms` can equal end_date by coincidence, and then no
            # value comparison can tell a derived bound from the caller's.
            missing  = self._identify_missing_periods(existing, self.start_date, window_end)

            if missing:
                logger.info(f"[{self.__class__.__name__}] {len(missing)} missing period(s) for {symbol}")
                try:
                    pieces = [] if existing.empty else [existing]
                    for ps, pe in missing:
                        logger.info(f"  Fetching {symbol}  {ps} → {pe}")
                        chunk = self._trim_to_period(self._fetch_remote(symbol, ps, pe), pe)
                        if not chunk.empty:
                            pieces.append(chunk)
                        else:
                            logger.warning(f"  No data returned for {symbol} {ps} → {pe}")
                    if pieces:
                        self._merge_and_store(symbol, pieces, save=self.localStorage,
                                              existing=existing)
                    else:
                        logger.warning(f"  No valid data assembled for {symbol}")
                        self.data_cache[symbol] = pd.DataFrame()
                except Exception as e:
                    # A gap-fill is an OPTIONAL top-up of already-loaded data. When
                    # it fails -- a raising _fetch_remote (network / rate limit), or
                    # a FetchGapError from _merge_and_store refusing a non-connecting
                    # response -- the read-only backtest path (tolerate_fill_failure)
                    # falls back to the local rows rather than propagating to
                    # fetch_historical_data's blanket handler, which degrades any
                    # exception to an empty frame and turns a recoverable INTERIOR
                    # gap into a hard "No historical data" crash (data_manager.py).
                    #
                    # The fallback is allowed ONLY when the cache, bounded to the
                    # requested window, reaches BOTH boundaries -- its first in-window
                    # row strictly within one interval of start_date and its last
                    # strictly within one interval of window_end. Strict inequalities
                    # keep the two sides symmetric: an off-grid start/end (a request
                    # landing mid-interval) whose first/last bar sits inside the first/
                    # last interval passes, but a whole MISSING boundary bar (first row
                    # at exactly start_date + interval, or last at window_end - interval)
                    # re-raises. With `<=` a missing leading bar would pass silently
                    # while `_inclusive_end`'s 23:59:59.999 already makes the end side
                    # strict -- the asymmetry this avoids. Interior holes (the real
                    # CUL-230 case) are tolerated; a boundary shortfall is NOT, because
                    # returning a
                    # cache that begins or ends inside the requested window would
                    # silently backtest a DIFFERENT window than asked -- launcher.py
                    # rejects only EMPTY frames, so a short window passes as if whole,
                    # trading the loud crash for a quiet wrong answer. Boundary
                    # shortfall therefore re-raises the original exception.
                    #
                    # Three further exclusions always re-raise:
                    #   * Seal guards MUST fail loud. _assert_no_sealed_rows /
                    #     _assert_request_window_unsealed raise SealedDataError
                    #     (data_manager.py); holdout safety depends on that never
                    #     being downgraded to a warning. Imported lazily -- data_manager
                    #     imports this module, so a top-level import would be circular.
                    #   * An empty in-window cache has nothing to fall back to.
                    #   * Write/append callers (capture tools) leave the flag off so
                    #     a non-connecting fetch still fails loud, unchanged.
                    from data.data_manager import SealedDataError
                    in_window = existing[
                        (existing["timestamp"] >= self.start_date) &
                        (existing["timestamp"] <= window_end)
                    ] if not existing.empty else existing
                    one = datetime.timedelta(seconds=int(self.interval_seconds))
                    covers_window = (
                        not in_window.empty
                        and in_window["timestamp"].min() < self.start_date + one
                        and in_window["timestamp"].max() > window_end - one
                    )
                    if (isinstance(e, SealedDataError)
                            or not self.tolerate_fill_failure
                            or not covers_window):
                        raise
                    logger.warning(
                        f"[{self.__class__.__name__}] {symbol}: gap-fill failed "
                        f"({type(e).__name__}: {e}); cache reaches both window "
                        f"boundaries, using it as-is despite the unfilled gap"
                    )
                    self.data_cache[symbol] = existing
            else:
                logger.info(f"[{self.__class__.__name__}] Local data for {symbol} is complete")
                self.data_cache[symbol] = existing

            # Trim to the exact requested window
            if symbol in self.data_cache and not self.data_cache[symbol].empty:
                df = self.data_cache[symbol]
                self.data_cache[symbol] = df[
                    (df["timestamp"] >= self.start_date) &
                    (df["timestamp"] <= window_end)
                ].copy()
                n = len(self.data_cache[symbol])
                logger.info(f"  {symbol}: {n} records after date filter") if n > 0 \
                    else logger.warning(f"  {symbol}: no records after date filter")

        self.data_loaded = True

    # -----------------------------------------------------------------------
    # Window bounds (shared by all subclasses)
    # -----------------------------------------------------------------------

    @staticmethod
    def _inclusive_end(ts) -> pd.Timestamp:
        """
        The last timestamp a window/period end admits.

        A DATE-ONLY end means "through that whole day": end_date='2025-12-31'
        must keep the 23:00 bar. Every caller in this repo passes date-only
        strings (launcher's simulate/analyse/optimise windows, fetch_data.py's
        str(end.date())), and the archive caches all terminate at 23:00, so
        tightening this to midnight would silently drop 23 bars from every
        window in the codebase.

        An end carrying a TIME OF DAY is taken literally. The previous rule --
        `timestamp < end_date + 1 day` -- widened every end by a day, so an end
        of 2025-12-31 23:00 admitted bars through 2026-01-01 22:00: 23 sealed
        holdout bars, past a bound the caller had stated explicitly.

        For date-only ends the two rules select identically (no bar falls in the
        last millisecond of a day), which is why the reference baseline is
        unaffected by this change.
        """
        ts = pd.Timestamp(ts)
        if ts == ts.normalize():
            return ts + datetime.timedelta(days=1) - datetime.timedelta(milliseconds=1)
        return ts

    @staticmethod
    def _trim_to_period(chunk: pd.DataFrame, bound) -> pd.DataFrame:
        """
        Drop rows a fetch returned beyond `bound`, the last timestamp the period
        it was asked for admits. `bound` is already literal -- _load_all expands
        the caller's "through that whole day" once, before periods are computed,
        so nothing here may re-expand it.

        The contract this establishes: a subclass's _fetch_remote MAY return
        more than requested, and the orchestrator is responsible for the bound.
        That is the only workable contract, because paginated endpoints cannot
        honour an arbitrary end -- CcxtFetcher's loop (ccxt_fetcher.py:149-174)
        bounds where a page STARTS, never where the data ENDS, and each page
        carries up to 1000 candles. A fetch of BTCUSDT_1d bounded at 2025-12-31
        wrote daily bars through 2026-03-19, straight across the sealed holdout.
        Bounding a request is not a bound on the response.

        Enforced HERE and not in _merge_and_store deliberately: that method
        concatenates `existing` with the new chunks, so a clamp there would
        delete already-cached rows beyond the current request's end whenever
        anyone fetched a narrower window than the cache holds -- turning a leak
        into data loss. Only freshly fetched rows are this method's business.
        """
        if chunk.empty or "timestamp" not in chunk.columns:
            return chunk
        ts = pd.to_datetime(chunk["timestamp"])
        return chunk[ts <= pd.Timestamp(bound)].copy()

    # -----------------------------------------------------------------------
    # Local storage helpers (shared by all subclasses)
    # -----------------------------------------------------------------------

    def _csv_path(self, symbol: str) -> str:
        """Absolute path to the local CSV for this symbol."""
        return os.path.join(self.data_dir, f"{self.cache_key(symbol)}.csv")

    def _load_local(self, symbol: str) -> pd.DataFrame:
        """
        Load the cached CSV for `symbol`.  Returns an empty DataFrame if the
        file does not exist or cannot be parsed.
        """
        path = self._csv_path(symbol)
        if not os.path.exists(path):
            return pd.DataFrame()
        try:
            df = pd.read_csv(path)
            if "timestamp" not in df.columns:
                logger.warning(f"No 'timestamp' column in {path} — ignoring cache")
                return pd.DataFrame()
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            # close_time is re-parsed for the same reason as timestamp: read_csv
            # infers it as object (string), and concatenating that against a
            # CcxtFetcher chunk's datetime64 close_time in _merge_and_store
            # degrades the merged column to object — to_csv then serialises those
            # rows as '…:59.999000' where a fresh write produces '…:59.999'.
            # Fixed once here so every caller of _merge_and_store gets a
            # consistent dtype, not just ingest's own patched call site (CUL-43).
            # Present only in OHLCV caches; aux feeds carry no close_time column.
            if "close_time" in df.columns:
                df["close_time"] = pd.to_datetime(df["close_time"])
        except Exception as e:
            logger.error(f"Error reading local data {path}: {e}")
            return pd.DataFrame()

        # Convention guard: the whole codebase (this module's own start/end
        # filtering above, fear_greed_fetcher.py, data_manager.py,
        # launcher.py) compares this column against naive datetimes. A
        # tz-aware dtype here means some writer emitted offset-carrying
        # timestamp strings (e.g. parsed elsewhere with utc=True) — that
        # would raise a confusing TypeError deep in an unrelated comparison.
        # Fail loudly at the read boundary instead. Deliberately NOT caught
        # by the try/except above: this must propagate, not degrade to an
        # empty DataFrame like a corrupt/missing file would.
        if isinstance(df["timestamp"].dtype, pd.DatetimeTZDtype):
            raise ValueError(
                f"{path}: 'timestamp' column parsed as tz-aware "
                f"({df['timestamp'].dtype}). The cache convention is "
                f"naive-UTC. Fix the writer that produced this file rather "
                f"than parsing with utc=True here."
            )
        return df

    def _gap_intervals(self, timestamps) -> List[Tuple[pd.Timestamp, pd.Timestamp]]:
        """
        Missing spans in a timestamp series, as inclusive [first_missing,
        last_missing] pairs. A "gap" is any step exceeding
        expected_gap_tolerance x the expected interval — the same criterion
        _identify_missing_periods and validate_data_continuity already use, so
        the guard agrees with the rest of the class rather than inventing a
        second notion of continuity.
        """
        ts = pd.to_datetime(pd.Series(timestamps)).sort_values().reset_index(drop=True)
        if len(ts) < 2:
            return []
        expected = datetime.timedelta(seconds=int(self.interval_seconds))
        threshold = expected * self.expected_gap_tolerance
        spans = []
        deltas = ts.diff()
        for i in range(1, len(ts)):
            if deltas.iloc[i] > threshold:
                spans.append((ts.iloc[i - 1] + expected, ts.iloc[i] - expected))
        return spans

    def _assert_no_new_gap(self, symbol: str, existing: pd.DataFrame,
                           combined: pd.DataFrame) -> None:
        """
        Refuse a write that introduces a hole where the series was previously
        continuous. See FetchGapError for the defect this exists to catch.

        Containment, not equality, is the test: a pre-existing gap that a fetch
        PARTIALLY fills produces a smaller gap nested inside the original. That
        is an improvement and must not be blocked. Only a gap that escapes every
        pre-existing gap's bounds represents time this fetch actually lost.
        """
        if existing is None or existing.empty:
            # Nothing was continuous before, so nothing can be broken. A first
            # fetch of a sparse or late-listed asset legitimately starts partway
            # into the requested window; that is not this guard's business.
            return

        before = self._gap_intervals(existing["timestamp"])
        after = self._gap_intervals(combined["timestamp"])

        new_gaps = [
            (s, e) for (s, e) in after
            if not any(bs <= s and e <= be for (bs, be) in before)
        ]
        if not new_gaps:
            return

        detail = "; ".join(
            f"{s} -> {e} ({int((e - s) / datetime.timedelta(seconds=int(self.interval_seconds))) + 1} bars)"
            for s, e in new_gaps
        )
        raise FetchGapError(
            f"[{self.__class__.__name__}] refusing to write {symbol}: this fetch "
            f"would introduce {len(new_gaps)} new gap(s) into a previously "
            f"continuous series — {detail}. The remote returned data that does "
            f"not connect to what is already cached (a rolling-window endpoint "
            f"that ignores `since` produces exactly this shape). NOTHING was "
            f"written; the existing cache is unchanged."
        )

    def _merge_and_store(self, symbol: str, pieces: list, save: bool = False,
                         existing: pd.DataFrame = None):
        """
        Concatenate DataFrames, deduplicate on timestamp, sort, cache in memory,
        and optionally write to disk.

        Raises FetchGapError — BEFORE touching memory or disk — if the merge
        would introduce a new discontinuity relative to `existing`.
        """
        combined = (
            pd.concat(pieces, ignore_index=True)
            .drop_duplicates(subset=["timestamp"])
            .sort_values("timestamp")
            .reset_index(drop=True)
        )
        # Ordered deliberately ahead of both the in-memory cache assignment and
        # the disk write: a rejected fetch must leave no trace in either.
        self._assert_no_new_gap(symbol, existing, combined)

        self.data_cache[symbol] = combined
        if save:
            path = self._csv_path(symbol)
            combined.to_csv(path, index=False)
            logger.info(f"  Saved {symbol} to {path} ({len(combined)} rows)")

    # -----------------------------------------------------------------------
    # Gap detection (shared by all subclasses)
    # -----------------------------------------------------------------------

    def _identify_missing_periods(
        self,
        existing: pd.DataFrame,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> List[Tuple[datetime.datetime, datetime.datetime]]:
        """
        Compare existing data coverage against [start_date, end_date] and
        return a sorted, merged list of (start, end) periods that need fetching.

        Three gap types detected:
          1. Data needed before the earliest stored timestamp  → prepend
          2. Data needed after  the latest  stored timestamp   → append
          3. Internal gaps > tolerance × expected interval     → inline fill
        """
        if existing.empty:
            return [(start_date, end_date)]

        data       = existing.copy()
        data["timestamp"] = pd.to_datetime(data["timestamp"])
        data       = data.sort_values("timestamp")
        expected   = np.timedelta64(int(self.interval_seconds), "s")
        missing    = []

        # ── Gap type 1: before earliest stored row ─────────────────────────
        earliest = data["timestamp"].min()
        if start_date < earliest:
            missing.append((
                start_date,
                min(pd.Timestamp(earliest).to_pydatetime() - datetime.timedelta(milliseconds=1), end_date)
            ))

        # ── Gap type 2: after latest stored row ────────────────────────────
        # A bar can only exist on the interval grid, so data is missing after
        # `latest` only if at least one whole interval fits before `end_date`.
        # A sub-interval remainder (e.g. the 59m59.999s between a cache's last
        # hourly bar and an inclusive end-of-day bound) is not a gap: treating
        # it as one schedules a phantom top-up fetch on every complete cache —
        # a network call and a file rewrite per run, and the top-up's first
        # page opens past the requested end.
        latest = data["timestamp"].max()
        if end_date >= pd.Timestamp(latest) + expected:
            missing.append((
                max(pd.Timestamp(latest).to_pydatetime() + datetime.timedelta(milliseconds=1), start_date),
                end_date
            ))

        # ── Gap type 3: internal gaps ───────────────────────────────────────
        timestamps = data["timestamp"].sort_values().values
        for i in range(1, len(timestamps)):
            gap = timestamps[i] - timestamps[i - 1]
            if gap > expected * self.expected_gap_tolerance:
                gs = pd.Timestamp(timestamps[i - 1] + expected).to_pydatetime().replace(tzinfo=None)
                ge = pd.Timestamp(timestamps[i] - np.timedelta64(1, "ms")).to_pydatetime().replace(tzinfo=None)
                if gs <= end_date and ge >= start_date:
                    missing.append((max(gs, start_date), min(ge, end_date)))

        if not missing:
            return []

        # Merge overlapping / adjacent periods
        missing.sort()
        merged = [missing[0]]
        for cs, ce in missing[1:]:
            ps, pe = merged[-1]
            if cs <= pe + datetime.timedelta(milliseconds=1):
                merged[-1] = (ps, max(pe, ce))
            else:
                merged.append((cs, ce))
        return merged
