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
        for symbol in self.symbols:
            existing = self._load_local(symbol) if self.localStorage else pd.DataFrame()
            missing  = self._identify_missing_periods(existing, self.start_date, self.end_date)

            if missing:
                logger.info(f"[{self.__class__.__name__}] {len(missing)} missing period(s) for {symbol}")
                pieces = [] if existing.empty else [existing]
                for ps, pe in missing:
                    logger.info(f"  Fetching {symbol}  {ps} → {pe}")
                    chunk = self._fetch_remote(symbol, ps, pe)
                    if not chunk.empty:
                        pieces.append(chunk)
                    else:
                        logger.warning(f"  No data returned for {symbol} {ps} → {pe}")
                if pieces:
                    self._merge_and_store(symbol, pieces, save=self.localStorage)
                else:
                    logger.warning(f"  No valid data assembled for {symbol}")
                    self.data_cache[symbol] = pd.DataFrame()
            else:
                logger.info(f"[{self.__class__.__name__}] Local data for {symbol} is complete")
                self.data_cache[symbol] = existing

            # Trim to the exact requested window
            if symbol in self.data_cache and not self.data_cache[symbol].empty:
                df = self.data_cache[symbol]
                self.data_cache[symbol] = df[
                    (df["timestamp"] >= self.start_date) &
                    (df["timestamp"] < self.end_date + datetime.timedelta(days=1))
                ].copy()
                n = len(self.data_cache[symbol])
                logger.info(f"  {symbol}: {n} records after date filter") if n > 0 \
                    else logger.warning(f"  {symbol}: no records after date filter")

        self.data_loaded = True

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

    def _merge_and_store(self, symbol: str, pieces: list, save: bool = False):
        """
        Concatenate DataFrames, deduplicate on timestamp, sort, cache in memory,
        and optionally write to disk.
        """
        combined = (
            pd.concat(pieces, ignore_index=True)
            .drop_duplicates(subset=["timestamp"])
            .sort_values("timestamp")
            .reset_index(drop=True)
        )
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
        latest = data["timestamp"].max()
        if end_date > latest:
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
