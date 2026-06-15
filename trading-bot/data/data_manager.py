"""
data_manager.py
===============
Unified data manager for live trading and backtesting, with support for
auxiliary data feeds (funding rates, fear & greed, on-chain metrics, etc.)
that are automatically merged into the candle DataFrame as extra columns.

Architecture overview
─────────────────────
                        ┌─────────────────────────┐
                        │       DataManager        │
                        │  mode = 'live'|'backtest'│
                        └────────────┬────────────┘
                                     │ owns
                          ┌──────────▼──────────┐
                          │    CandleBuilder     │  ← single aggregation engine
                          │  (price ticks only)  │
                          └──────────┬──────────┘
                                     │ on candle close
                          ┌──────────▼──────────┐
                          │  _enrich_and_notify  │  ← merges aux feeds + fires callback
                          └──────────┬──────────┘
                                     │
                          ┌──────────▼──────────┐
                          │   strategy callback   │  ← receives enriched DataFrame
                          └─────────────────────┘

Auxiliary feeds (registered via register_feed())
─────────────────────────────────────────────────
Each feed is a BaseFetcher subclass.  At candle close DataManager looks up
the latest value from each registered feed for that candle's timestamp and
appends it as an extra column to the history DataFrame before the strategy
callback is fired.

In backtest mode the feeds are pre-loaded and pre-merged into the historical
DataFrame using merge_asof (forward-fill on the feed's timestamps) so that
the strategy never sees a future value.  In live mode each feed is polled
on a separate background thread and the latest cached value is used.
"""

from binance.client import Client
from config.settings import API_KEY, API_SECRET, USE_TESTNET
import pandas as pd
import logging
from typing import Callable, Dict, List, Optional
import datetime
import os
import numpy as np
import time

from collections import defaultdict
from dataclasses import dataclass, field
import threading
import queue

# Fetchers are imported here so callers only need to import data_manager
from data.fetchers.ccxt_fetcher import CcxtFetcher as HistoricalDataFetcher
from data.fetchers.base_fetcher import BaseFetcher

logger = logging.getLogger("trading_bot")


# ===========================================================================
# Core data structures  (unchanged)
# ===========================================================================

@dataclass
class PriceTick:
    """
    A single price observation for one symbol.

    In live mode:     created by DataManager._rest_price_fetcher() from a
                      Binance ticker response.
    In backtest mode: created inside CandleBuilder.add_row() from a historical
                      DataFrame row.
    Volume is optional because get_symbol_ticker() does not return it.
    """
    symbol: str
    price: float
    timestamp: datetime.datetime
    volume: Optional[float] = None


@dataclass
class Candle:
    """
    One completed OHLCV bar.

    start_time is always aligned to an interval boundary thanks to
    CandleBuilder._align().  tick_count records how many raw ticks contributed
    (useful for diagnosing sparse backtest data).
    """
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    start_time: datetime.datetime
    end_time: datetime.datetime
    tick_count: int = 0


# ===========================================================================
# AuxFeedConfig
#
# Lightweight descriptor stored by DataManager for each registered auxiliary
# feed.  It carries:
#   fetcher    — the BaseFetcher subclass instance that knows how to
#                retrieve and cache this feed's data
#   column     — the column name that will appear in the enriched DataFrame
#                (e.g. 'fear_greed', 'funding_rate')
#   agg        — how to reduce multiple readings within one candle window:
#                  'last'  → most recent value (default, good for rates/indices)
#                  'mean'  → average (good for noisy signals)
#                  'sum'   → sum (good for counts/volumes)
#   live_value — the most recently fetched value, updated by the background
#                poll thread in live mode; used as the enrichment value at
#                candle close.
# ===========================================================================

@dataclass
class AuxFeedConfig:
    """Descriptor for one registered auxiliary data feed."""
    fetcher:    BaseFetcher
    column:     str
    agg:        str = "last"          # 'last' | 'mean' | 'sum'
    live_value: Optional[float] = None  # updated in live mode by poll thread


# ===========================================================================
# CandleBuilder  (unchanged from previous version — no awareness of aux feeds)
# ===========================================================================

class CandleBuilder:
    """
    Aggregates price ticks into fixed-interval OHLCV candles.

    This class knows nothing about auxiliary feeds — enrichment happens one
    level up in DataManager._enrich_and_notify() after a candle closes.

    Flow diagram
    ────────────
    Live:
        REST poll → PriceTick → add_tick() ──┐
                                              ├─→ _ingest() → Candle (on close)
    Backtest:                                 │               → callback → enrich
        DataFrame row → add_row() ───────────┘
    """

    def __init__(
        self,
        interval_seconds: int,
        candle_completion_callback: Callable[[str, "Candle"], None] = None,
    ):
        self.interval_seconds = interval_seconds
        self.current_candles: Dict[str, Candle] = {}
        self.completed_candles: Dict[str, List[Candle]] = defaultdict(list)
        self.candle_completion_callback = candle_completion_callback

    # ------------------------------------------------------------------
    # Public entry points
    # ------------------------------------------------------------------

    def add_tick(self, tick: PriceTick) -> Optional[Candle]:
        """Live path: ingest a PriceTick, return completed Candle or None."""
        return self._ingest(
            symbol=tick.symbol,
            price=tick.price,
            volume=tick.volume or 0.0,
            timestamp=tick.timestamp,
        )

    def add_row(self, row: pd.Series, symbol: str) -> Optional[Candle]:
        """
        Backtest path: ingest one historical DataFrame row.

        Uses 'close' as the price to avoid look-ahead bias on entries decided
        at bar close.  Converts pd.Timestamp → datetime for timedelta arithmetic.
        """
        timestamp = pd.to_datetime(row["timestamp"])
        if hasattr(timestamp, "to_pydatetime"):
            timestamp = timestamp.to_pydatetime()
        return self._ingest(
            symbol=symbol,
            price=float(row["close"]),
            volume=float(row.get("volume", 0.0)),
            timestamp=timestamp,
            open=float(row["open"])  if "open"  in row.index else None,
            high=float(row["high"])  if "high"  in row.index else None,
            low=float(row["low"])    if "low"   in row.index else None,
        )

    def get_candle_history(self, symbol: str, count: int = 1) -> pd.DataFrame:
        """
        Return the last `count` completed candles as a plain (non-indexed)
        DataFrame.  Extra columns added by DataManager enrichment are NOT
        present here — use DataManager.get_data_history() for enriched data.
        """
        candles = self.completed_candles.get(symbol, [])[-count:]
        
        if not candles:
            return pd.DataFrame()
        return pd.DataFrame([
            {
                "timestamp": c.start_time,
                "open":      c.open,
                "high":      c.high,
                "low":       c.low,
                "close":     c.close,
                "volume":    c.volume,
            }
            for c in candles
        ])

    def get_current_candle(self, symbol: str) -> Optional[Candle]:
        """Return the still-open candle for a symbol, or None."""
        return self.current_candles.get(symbol)

    def reset(self, symbol: str = None):
        """
        Wipe aggregation state.  Called by DataManager.initialize() before
        each backtest run so that candle history does not bleed between runs.
        """
        if symbol:
            self.current_candles.pop(symbol, None)
            self.completed_candles.pop(symbol, None)
        else:
            self.current_candles.clear()
            self.completed_candles.clear()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ingest(
        self,
        symbol: str,
        price: float,
        volume: float,
        timestamp: datetime.datetime,
        open: float = None,
        high: float = None,
        low: float = None,
    ) -> Optional[Candle]:
        """
        Core aggregation logic shared by live and backtest paths.

        1. First tick for a symbol → open a new candle, return None.
        2. Elapsed time >= interval → close candle, fire callback, open next.
        3. Otherwise → update running candle (high/low/close/volume).

        The callback is fired synchronously so the strategy always receives
        a complete, closed bar.
        """
        if symbol not in self.current_candles:
            self.current_candles[symbol] = self._open_candle(symbol, price, volume, timestamp, open, high, low)
            return None

        current = self.current_candles[symbol]

        if (timestamp - current.start_time).total_seconds() >= self.interval_seconds:
            # ── Candle close ──────────────────────────────────────────────
            self.completed_candles[symbol].append(current) #Enrich the local stored candle history with the completed candle before firing the callback, so that the strategy can access it via get_candle_history() in the callback.
            if self.candle_completion_callback:
                try:
                    self.candle_completion_callback(symbol)
                except Exception as e:
                    logger.error(f"Candle callback error for {symbol}: {e}", exc_info=True)

            self.current_candles[symbol] = self._open_candle(symbol, price, volume, timestamp, open, high, low)
            return current
        else:
            # ── Candle update ─────────────────────────────────────────────
            self._update_candle(current, price, volume)
            return None

    def _open_candle(self, symbol, price, volume, timestamp, open=None, high=None, low=None) -> Candle:
        """Open a new candle aligned to the interval boundary."""
        aligned = self._align(timestamp)
        return Candle(
            symbol=symbol, 
            open=open  if open  is not None else price,
            high=high  if high  is not None else price,
            low=low    if low   is not None else price,
            close=price,
            volume=volume,
            start_time=aligned,
            end_time=aligned + datetime.timedelta(seconds=self.interval_seconds),
            tick_count=1,
        )

    @staticmethod
    def _update_candle(candle: Candle, price: float, volume: float, high: float = None, low: float = None):
        """Merge a tick into an open candle in-place."""
        candle.high      = max(candle.high, high if high is not None else price)
        candle.low       = min(candle.low,  low  if low  is not None else price)
        candle.close     = price
        candle.volume   += volume
        candle.tick_count += 1

    def _align(self, timestamp: datetime.datetime) -> datetime.datetime:
        """
        Floor timestamp to the nearest interval boundary using Unix epoch
        integer division.

        Example for interval_seconds=300:  09:03:47 → 09:00:00
        """
        ts = int(timestamp.timestamp())
        return datetime.datetime.fromtimestamp(
            (ts // self.interval_seconds) * self.interval_seconds
        )


# ===========================================================================
# DataManager
#
# Unified live + backtest data manager with pluggable auxiliary feed support.
#
# New in this version
# ────────────────────
# register_feed(name, fetcher, agg)
#     Plug in any BaseFetcher subclass.  The feed's data is automatically:
#       • fetched and cached (same storage pipeline as price data)
#       • pre-merged into historical_data before backtest replay starts
#       • appended as extra columns to every candle history DataFrame
#         returned to the strategy
#     Registering feeds is optional — if none are registered the behaviour is
#     identical to the previous version.
#
# get_data_history(symbol, count)
#     Now returns an enriched DataFrame: OHLCV columns + one column per
#     registered feed.
#
# _enrich_and_notify(symbol, candle)
#     Called by CandleBuilder's callback.  Builds the enriched history
#     DataFrame and fires the strategy callback.  This is the only new
#     code path in the hot loop.
# ===========================================================================

class DataManager:
    """
    Single data manager for live trading and backtesting.

    Auxiliary feed registration example
    ─────────────────────────────────────
        from data.fetchers import FearGreedFetcher, FundingRateFetcher

        dm = DataManager(['BTCUSDT'], interval_seconds=300, mode='backtest')

        dm.register_feed(
            name    = 'fear_greed',
            fetcher = FearGreedFetcher('2024-01-01', '2024-12-31', localStorage=True),
            agg     = 'last',
        )
        dm.register_feed(
            name    = 'funding_rate',
            fetcher = FundingRateFetcher('2024-01-01', '2024-12-31',
                                         symbols=['BTCUSDT'], localStorage=True),
            agg     = 'last',
        )

        # load_data() and initialize() handle pre-merging automatically.
        # The strategy then receives a DataFrame with columns:
        #   timestamp, open, high, low, close, volume, fear_greed, funding_rate

    Live mode aux feeds
    ────────────────────
    Each registered feed's fetcher.get_data() is called once at startup to
    pre-load historical values.  A background thread then polls each feed's
    fetcher at a configurable interval and updates AuxFeedConfig.live_value.
    At candle close the latest cached value is used for enrichment.
    """

    def __init__(
        self,
        symbols: List[str],
        interval_seconds: int,
        mode: str = "live",
        price_fetch_interval: int = 60,
        candle_completion_callback: Callable[[str, Candle], None] = None,
    ):
        """
        Args:
            symbols:                    Trading pairs, e.g. ['BTCUSDT'].
            interval_seconds:           Candle duration in seconds.
            mode:                       'live' or 'backtest'.
            price_fetch_interval:       Seconds between REST price polls (live only).
            candle_completion_callback: Forwarded to CandleBuilder.  Usually set
                                        after TradingBot construction via:
                                        data_manager.candle_builder.candle_completion_callback = ...
        """
        if mode not in ("live", "backtest"):
            raise ValueError(f"mode must be 'live' or 'backtest', got '{mode}'")

        self.symbols              = symbols
        self.interval_seconds     = interval_seconds
        self.mode                 = mode
        self.price_fetch_interval = price_fetch_interval

        # ── Registered auxiliary feeds ─────────────────────────────────────
        # Populated by register_feed().  Keys are the column names that will
        # appear in the enriched candle DataFrame (e.g. 'fear_greed').
        self._aux_feeds: Dict[str, AuxFeedConfig] = {}

        # ── Candle-level enrichment cache ──────────────────────────────────
        # In backtest mode: pre-merged aux columns keyed by symbol.
        #   _enrichment_data[symbol] = DataFrame with columns
        #   [timestamp, col1, col2, …] indexed to the same rows as historical_data.
        # In live mode: managed per-feed via AuxFeedConfig.live_value.
        self._enrichment_data: Dict[str, pd.DataFrame] = {}

        # ── Shared aggregation engine ──────────────────────────────────────
        # CandleBuilder fires _enrich_and_notify() (not the strategy directly).
        # _enrich_and_notify() then adds aux columns and calls the real callback.
        self.candle_builder = CandleBuilder(
            interval_seconds=interval_seconds,
            candle_completion_callback=self._enrich_and_notify,
        )

        # ── Strategy-level callback ────────────────────────────────────────
        # Set externally after TradingBot is constructed.  This is what the
        # strategy ultimately receives (with an enriched DataFrame available
        # via get_candle_history()).
        self._strategy_callback: Optional[Callable[[str, Candle], None]] = (
            candle_completion_callback
        )

        # ── Live-only state ────────────────────────────────────────────────
        if mode == "live":
            self.client      = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)
            self.price_queue: queue.Queue = queue.Queue()
            self.running     = False

        # ── Backtest-only state ────────────────────────────────────────────
        self.historical_data: Dict[str, pd.DataFrame] = {}   # symbol → DataFrame
        self._cursor: Dict[str, int] = {}

    # -----------------------------------------------------------------------
    # Feed registration
    # -----------------------------------------------------------------------

    def register_feed(
        self,
        name: str,
        fetcher: BaseFetcher,
        agg: str = "last",
    ) -> None:
        """
        Register an auxiliary data feed.

        Args:
            name:    Column name that will appear in the enriched DataFrame,
                     e.g. 'fear_greed', 'funding_rate', 'open_interest'.
            fetcher: Any BaseFetcher subclass instance.  Must be pre-configured
                     with the correct date range and symbols.
            agg:     Aggregation function to apply when multiple readings fall
                     within one candle window:
                       'last' — most recent value  (default)
                       'mean' — average
                       'sum'  — sum

        Can be called at any time before initialize() (backtest) or
        initiate_start_thread() (live).
        """
        if agg not in ("last", "mean", "sum"):
            raise ValueError(f"agg must be 'last', 'mean', or 'sum' — got '{agg}'")
        self._aux_feeds[name] = AuxFeedConfig(fetcher=fetcher, column=name, agg=agg)
        logger.info(f"DataManager: registered aux feed '{name}' (agg={agg})")

    # -----------------------------------------------------------------------
    # Enrichment — called at every candle close
    # -----------------------------------------------------------------------

    def _enrich_and_notify(self, symbol: str, candle: Candle) -> None:
        """
        Internal callback wired into CandleBuilder.

        Steps:
        1. Build the base candle history DataFrame from CandleBuilder.
        2. If any aux feeds are registered, join their latest values as extra
           columns (see _attach_aux_columns).
        3. Fire the real strategy callback (_strategy_callback) with the
           enriched DataFrame available via get_data_history().

        This is the only code path that changes in the hot loop compared to the
        previous version.  If no feeds are registered, steps 1→3 degenerate to
        the same behaviour as before.
        """
        if self._strategy_callback:
            try:
                self._strategy_callback(symbol, candle)
            except Exception as e:
                logger.error(f"Strategy callback error for {symbol}: {e}", exc_info=True)

    def _attach_aux_columns(
        self, symbol: str, df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge registered aux feed values into a candle history DataFrame.

        For each registered feed:
          Backtest: use _enrichment_data[symbol] which was pre-merged at
                    initialize() time via merge_asof.  Simply select the rows
                    that overlap with df's timestamp range.
          Live:     use AuxFeedConfig.live_value (the most recently polled value)
                    broadcast as a constant column.

        Returns a new DataFrame with additional columns; the original is not
        mutated.  If a feed has no data for the requested window, the column is
        filled with NaN so the strategy can handle missing data gracefully.
        """
        
        if not self._aux_feeds or df.empty:
            return df

        result = df.copy()

        for name, feed in self._aux_feeds.items():
            if self.mode == "backtest":
                # Pre-merged data is keyed by symbol; may not exist for feeds
                # that are global (e.g. fear_greed uses its own key)
                key = symbol if symbol in self._enrichment_data else name
                enriched = self._enrichment_data.get(key, pd.DataFrame())

                if not enriched.empty and name in enriched.columns:
                    # Forward-fill: each candle gets the latest known value
                    # at or before its timestamp using merge_asof
                    merged = pd.merge_asof(
                        result.sort_values("timestamp"),
                        enriched[["timestamp", name]].sort_values("timestamp"),
                        on="timestamp",
                        direction="backward",   # last known value ≤ candle time
                    )
                    result = merged
                else:
                    result[name] = np.nan

            else:
                # Live mode: broadcast the latest polled value
                result[name] = feed.live_value  # None becomes NaN automatically

        return result

    def get_data_history(self, symbol: str, count: int = 1) -> pd.DataFrame:
        """
        Return the last `count` completed candles enriched with aux feed columns.

        This is the method strategies should call — it returns the full enriched
        DataFrame.  CandleBuilder.get_candle_history() returns OHLCV only and
        should not be called directly by strategies.
        """
        df = self.candle_builder.get_candle_history(symbol, count)
        

        return self._attach_aux_columns(symbol, df)

    # -----------------------------------------------------------------------
    # Backtest aux feed pre-merge
    # -----------------------------------------------------------------------

    def _premerge_aux_feeds(self, symbol: str, df: pd.DataFrame) -> pd.DataFrame:
        """
        Merge all registered aux feeds into a price DataFrame before replay.

        Called by initialize() for each symbol.  Uses pd.merge_asof with
        direction='backward' so each price row gets the most recent aux value
        at or before its timestamp — no look-ahead.

        The merged aux columns are also stored in _enrichment_data[symbol] so
        that _attach_aux_columns() can look them up at candle-close time during
        replay.

        Returns the enriched price DataFrame (aux columns added in-place on a
        copy).
        """
        if not self._aux_feeds:
            return df

        enriched = df.copy().sort_values("timestamp")

        for name, feed in self._aux_feeds.items():
            # Determine which symbol key to use for this feed.
            # Global feeds (e.g. fear_greed) store data under their own name;
            # per-symbol feeds (e.g. funding_rate) store under the trading symbol.
            feed_data = feed.fetcher.get_data(symbol)

            if feed_data.empty:
                all_data  = feed.fetcher.get_data()
                feed_data = (
                    next(iter(all_data.values()), pd.DataFrame())
                    if isinstance(all_data, dict)
                    else all_data
                )
                # Add these:
                logger.debug(f"_premerge '{name}': feed_data columns={feed_data.columns.tolist()}")
                logger.debug(f"_premerge '{name}': feed_data head=\n{feed_data.head(3)}")
                logger.debug(f"_premerge '{name}': price df timestamp range: {df['timestamp'].min()} → {df['timestamp'].max()}")
                # After
                if not feed_data.empty and 'timestamp' in feed_data.columns:
                    logger.debug(f"_premerge '{name}': feed timestamp range: {feed_data['timestamp'].min()} → {feed_data['timestamp'].max()}")
                else:
                    logger.debug(f"_premerge '{name}': feed_data is empty after lookup")
            if feed_data.empty or name not in feed_data.columns:
                logger.warning(
                    f"DataManager: no data for aux feed '{name}' "
                    f"(symbol={symbol}) — column will be NaN"
                )
                enriched[name] = np.nan
                continue

            # Apply the registered aggregation function to handle cases where
            # the aux feed has higher resolution than the price data
            # (e.g. funding rate every 8h, price every 1m)
            if feed.agg != "last":
                feed_data = (
                    feed_data
                    .set_index("timestamp")
                    .resample(f"{self.interval_seconds}s")
                    .agg({name: feed.agg})
                    .reset_index()
                )

            enriched = pd.merge_asof(
                enriched,
                feed_data[["timestamp", name]].sort_values("timestamp"),
                on="timestamp",
                direction="backward",
            )
            logger.info(
                f"DataManager: pre-merged '{name}' into {symbol} "
                f"({feed_data[name].notna().sum()} non-null values)"
            )

        # Store for _attach_aux_columns() to use during replay
        # Keep only timestamp + aux columns (price columns already in historical_data)
        aux_cols = [name for name in self._aux_feeds]
        self._enrichment_data[symbol] = enriched[["timestamp"] + aux_cols].copy()

        return enriched

    # -----------------------------------------------------------------------
    # Shared public interface  (unchanged from previous version)
    # -----------------------------------------------------------------------

    def get_final_candle(self, symbol: str) -> Optional[Candle]:
        """Return the still-open candle at end-of-backtest (or current live candle)."""
        return self.candle_builder.get_current_candle(symbol)

    def process_next_tick(self, symbol: str) -> Optional[Candle]:
        """
        Advance by one tick; return a completed Candle if the interval closed.

        Live:     drains pending ticks from the price queue.
        Backtest: feeds the row at the current cursor into CandleBuilder.
        """
        if self.mode == "live":
            return self._process_live_tick(symbol)
        else:
            return self._process_backtest_tick(symbol)

    def has_more_data(self, symbol: str) -> bool:
        """False when backtest data is exhausted; always True in live mode."""
        if self.mode == "live":
            return True
        if symbol not in self.historical_data:
            return False
        return self._cursor.get(symbol, 0) < len(self.historical_data[symbol]) - 1

    def advance(self, symbol: str, steps: int = 1) -> bool:
        """
        Move the backtest cursor forward.  No-op in live mode.
        Returns False when the end of historical data is reached.
        """
        if self.mode == "live":
            return True
        if symbol not in self.historical_data:
            logger.warning(f"advance: {symbol} not in historical_data")
            return False
        new_idx = self._cursor.get(symbol, 0) + steps
        if new_idx >= len(self.historical_data[symbol]):
            logger.warning(f"DataManager: cursor reached end for {symbol}")
            return False
        self._cursor[symbol] = new_idx
        # logger.debug(f"DataManager: {symbol} cursor → {self._cursor[symbol]}")
        return True

    # -----------------------------------------------------------------------
    # Backtest-specific setup
    # -----------------------------------------------------------------------

    def initialize(self):
        """
        Prepare for a backtest run.

        1. Resets CandleBuilder state (clears candle history from previous run).
        2. Resets all cursors to 0.
        3. Pre-merges any registered aux feeds into each symbol's historical
           DataFrame so that enrichment during replay is a simple dict lookup.

        Must be called after historical_data has been populated and after all
        feeds have been registered via register_feed().
        """
        self.candle_builder.reset()
        self._enrichment_data.clear()

        for symbol, df in self.historical_data.items():
            self._cursor[symbol] = 0

            if self._aux_feeds:
                # Pre-merge aux data; the enriched DataFrame replaces the raw one
                # so that _process_backtest_tick feeds pre-enriched rows to CandleBuilder
                # (price columns are what CandleBuilder uses; aux columns ride along
                # and are picked up by _attach_aux_columns at get_candle_history time)
                if df.empty or 'timestamp' not in df.columns:
                    logger.error(f"No valid price data for {symbol} — skipping aux feed merge")
                    continue  # or return, depending on loop structure
                
                self._premerge_aux_feeds(symbol, df) 
                logger.info(
                    f"DataManager: {symbol} initialised with "
                    f"{len(self._aux_feeds)} aux feed(s) — "
                    f"{len(df)} rows"
                )
            else:
                logger.info(f"DataManager: {symbol} initialised ({len(df)} rows)")

    def fetch_historical_data(self, symbol: str, start_date, end_date) -> pd.DataFrame:
        """
        Fetch raw OHLCV data for one symbol via CcxtFetcher and return it as
        a flat DataFrame.

        Typical call from BacktestEngine.load_data():
            self.historical_data[symbol] = self.data_manager.fetch_historical_data(
                symbol, start_date, end_date
            )
        followed by self.data_manager.initialize().

        Returns an empty DataFrame on failure.
        """
        logger.debug(f"Fetching OHLCV for {symbol}  {start_date} → {end_date}")

        data_folder = os.path.dirname(os.path.abspath(__file__))
        project_folder = os.path.dirname(data_folder)
        data_storage_dir = os.path.join(project_folder, "local_data")

        fetcher = HistoricalDataFetcher(
            start_date, end_date, [symbol],
            candle_interval_seconds=self.interval_seconds,
            exchange="binance",
            localStorage=True,
            data_dir = data_storage_dir
        )
        try:
            data = fetcher.get_data()   # {symbol: DataFrame}
            if symbol in data and not data[symbol].empty:
                is_continuous, gaps = fetcher.validate_data_continuity(symbol)
                logger.debug(f"  Records   : {len(data[symbol])}")
                logger.debug(
                    f"  Date range: {data[symbol]['timestamp'].min()} "
                    f"to {data[symbol]['timestamp'].max()}"
                )
                logger.debug(f"  Continuous: {is_continuous}")
                if not is_continuous:
                    logger.warning(f"  {len(gaps)} gap(s) detected in {symbol} data")
                return data[symbol]
            else:
                logger.warning(f"No OHLCV data available for {symbol}")
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error fetching OHLCV for {symbol}: {e}", stack_info=True, exc_info=True)
            return pd.DataFrame()

    # -----------------------------------------------------------------------
    # Live-mode threading
    # -----------------------------------------------------------------------

    def initiate_start_thread(self) -> Optional[threading.Thread]:
        """
        Start the background REST price-fetcher thread (live mode only).

        Also starts one background poll thread per registered aux feed so that
        live_value is kept up to date between candle closes.
        """
        if self.mode != "live":
            logger.warning("initiate_start_thread called in backtest mode — ignored")
            return None
        self.running = True

        # Price feed thread
        price_thread = threading.Thread(target=self._rest_price_fetcher, daemon=True)
        price_thread.start()

        # One poll thread per aux feed
        for name, feed in self._aux_feeds.items():
            t = threading.Thread(
                target=self._aux_feed_poll_loop,
                args=(name, feed),
                daemon=True,
                name=f"aux_feed_{name}",
            )
            t.start()
            logger.info(f"DataManager: started poll thread for aux feed '{name}'")

        return price_thread

    def _aux_feed_poll_loop(self, name: str, feed: AuxFeedConfig):
        """
        Background thread: periodically refresh one aux feed's live_value.

        Polls once per candle interval (no need to poll faster than the candle
        closes).  On each poll, calls fetcher.get_data() which returns from
        the local cache if the data is still fresh, or re-fetches if needed.
        """
        while self.running:
            try:
                # Refresh feed data (fetcher handles caching internally)
                now = datetime.datetime.utcnow()
                data = feed.fetcher.get_data()

                if isinstance(data, dict):
                    # Global feeds return {key: DataFrame}
                    df = next(iter(data.values()), pd.DataFrame())
                else:
                    df = data

                if not df.empty and feed.column in df.columns:
                    # Forward-fill to now: take the row with the largest
                    # timestamp <= current time
                    df_sorted = df.sort_values("timestamp")
                    past = df_sorted[df_sorted["timestamp"] <= pd.Timestamp(now)]
                    if not past.empty:
                        feed.live_value = float(past[feed.column].iloc[-1])
                        logger.debug(f"Aux feed '{name}': live_value = {feed.live_value}")

            except Exception as e:
                logger.error(f"Aux feed poll error for '{name}': {e}", exc_info=True)

            time.sleep(self.interval_seconds)   # poll once per candle interval

    def _rest_price_fetcher(self):
        """
        Background thread: poll Binance REST at price_fetch_interval seconds
        and push PriceTicks onto price_queue.
        """
        while self.running:
            try:
                for symbol in self.symbols:
                    if not self.running:
                        break
                    price_data = self._get_current_price(symbol)
                    if price_data:
                        tick = PriceTick(
                            symbol=symbol,
                            price=price_data["price"],
                            timestamp=datetime.datetime.now(),
                            volume=price_data.get("volume", 0),
                        )
                        self.price_queue.put(tick)
                    else:
                        logger.warning(f"Failed to fetch price for {symbol}")
                if len(self.symbols) > 1:
                    logger.debug(f"Fetched prices for {len(self.symbols)} symbols")
                time.sleep(self.price_fetch_interval)
            except Exception as e:
                logger.error(f"REST price fetcher error: {e}", exc_info=True)
                time.sleep(1)

    def _get_current_price(self, symbol: str) -> Optional[dict]:
        """Fetch the latest ticker price for one symbol via Binance REST."""
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return {"price": float(ticker["price"]), "volume": 0}
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
            return None

    def live_main_candle_processing_loop(self):
        """
        Drain price_queue and feed ticks into CandleBuilder (live mode).

        The candle_completion_callback (_enrich_and_notify) handles enrichment
        and strategy notification when a candle closes.
        """
        while self.running:
            try:
                processed = 0
                while not self.price_queue.empty():
                    tick = self.price_queue.get_nowait()
                    completed = self.candle_builder.add_tick(tick)
                    if completed:
                        logger.info(
                            f"Candle: {tick.symbol} "
                            f"O:{completed.open} H:{completed.high} "
                            f"L:{completed.low} C:{completed.close}"
                        )
                    processed += 1
                if processed > 0:
                    logger.debug(f"Processed {processed} ticks")
                time.sleep(0.1)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Candle processing loop error: {e}", exc_info=True)

    # -----------------------------------------------------------------------
    # Internal helpers
    # -----------------------------------------------------------------------

    def _process_live_tick(self, symbol: str) -> Optional[Candle]:
        """Drain all queued ticks and return any completed candle for `symbol`."""
        try:
            completed = None
            while not self.price_queue.empty():
                tick    = self.price_queue.get_nowait()
                result  = self.candle_builder.add_tick(tick)
                if result and result.symbol == symbol:
                    completed = result
            return completed
        except queue.Empty:
            return None
        except Exception as e:
            logger.error(f"Live tick error for {symbol}: {e}", exc_info=True)
            return None

    def _process_backtest_tick(self, symbol: str) -> Optional[Candle]:
        """Feed the row at the current cursor to CandleBuilder."""
        if symbol not in self.historical_data:
            return None
        df  = self.historical_data[symbol]
        idx = self._cursor.get(symbol, 0)
        if idx >= len(df):
            return None
        return self.candle_builder.add_row(df.iloc[idx], symbol)

    # -----------------------------------------------------------------------
    # Legacy compatibility shim
    # -----------------------------------------------------------------------

    def get_historical_klines(
        self, symbol: str, interval: str = None, limit: int = 1
    ) -> pd.DataFrame:
        """
        Backward-compatible shim for strategies that called
        HistoricalDataManager.get_historical_klines().

        Backtest: returns raw rows up to the current cursor (not enriched).
        Live:     returns the last `limit` completed enriched candles.
        """
        if self.mode == "backtest" and symbol in self.historical_data:
            idx   = self._cursor.get(symbol, 0)
            start = max(0, idx - limit + 1)
            return self.historical_data[symbol].iloc[start : idx + 1].copy()
        return self.get_data_history(symbol, limit)


# ===========================================================================
# Backward-compatibility re-export
# Code that did:  from data.data_manager import HistoricalDataFetcher
# continues to work unchanged.
# ===========================================================================
__all__ = [
    "PriceTick",
    "Candle",
    "CandleBuilder",
    "DataManager",
    "AuxFeedConfig",
    "HistoricalDataFetcher",   # re-exported from ccxt_fetcher
]
