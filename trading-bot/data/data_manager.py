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
from pathlib import Path

# Fetchers are imported here so callers only need to import data_manager
from data.fetchers.ccxt_fetcher import CcxtFetcher as HistoricalDataFetcher
from data.fetchers.base_fetcher import BaseFetcher

logger = logging.getLogger("trading_bot")

#: `strategy-research/config/campaign_data_policy.yaml:holdout_range`. Read, never
#: assumed — the seal moves with the policy, per the rule
#: `tests/test_no_sealed_date_literals.py` states and follows.
_POLICY_PATH = (Path(__file__).resolve().parents[2]
                / "strategy-research" / "config" / "campaign_data_policy.yaml")


def _holdout_bounds() -> tuple:
    """(first sealed instant, first instant AFTER the seal), from the policy.

    BOTH ends, not just the start. holdout_range is a closed window
    ["2026-01-01", "2026-06-30"] and the policy itself declares data usable
    again afterwards (`era_2026_h2_forward_recorded`, from 2026-07-26). A guard
    keyed on the start alone would refuse every future candle forever, which
    is not a seal but an expiry date on the whole bot.

    The upper end is INCLUSIVE in the policy (the same reading
    `tests/test_no_sealed_date_literals.py` documents), so the returned bound is
    the start of the following day and the comparison against it is strict.

    Deny by default on any failure to read: a reader that cannot locate the seal
    cannot prove it is not serving sealed candles. The yaml import is inside the
    try on purpose — an ImportError is just as much a failure to locate the seal
    as a missing file, and outside it would bypass this refusal.
    """
    try:
        import yaml  # local: this module is imported in contexts without yaml
        with open(_POLICY_PATH, encoding="utf-8") as fh:
            lo, hi = yaml.safe_load(fh)["holdout_range"][:2]
        return pd.Timestamp(lo), pd.Timestamp(hi).normalize() + datetime.timedelta(days=1)
    except Exception as exc:                                  # noqa: BLE001
        raise SealedDataError(
            f"Cannot read holdout_range from {_POLICY_PATH}: {exc}. Refusing to "
            f"return market data — a read that cannot locate the seal cannot "
            f"prove it is not serving sealed candles."
        ) from exc


class SealedDataError(RuntimeError):
    """Requested data reaches into the sealed holdout range."""


def _assert_no_sealed_rows(df: "pd.DataFrame", symbol: str) -> None:
    """Refuse a frame carrying rows at or past the seal.

    Refuses rather than silently dropping them: quietly returning a shorter
    series than was asked for would hand the caller a backtest over a different
    window than it believes it ran, which is the flattering-and-invisible
    failure this project's rules single out. If a run legitimately needs the
    holdout, that is a deliberate, single-use act — pass allow_sealed=True at
    the call site so it appears in the diff.
    """
    if df is None or df.empty or "timestamp" not in df.columns:
        return
    lo, hi = _holdout_bounds()
    sealed = df[(df["timestamp"] >= lo) & (df["timestamp"] < hi)]
    if not sealed.empty:
        raise SealedDataError(
            f"{symbol}: requested window returned {len(sealed)} row(s) INSIDE the "
            f"holdout seal [{lo:%Y-%m-%d}, {hi - datetime.timedelta(days=1):%Y-%m-%d}] — "
            f"first {sealed['timestamp'].min()}, last {sealed['timestamp'].max()}. "
            f"The committed caches still contain sealed rows; reading them spends a "
            f"single-use, terminal holdout. Bound the request outside the sealed "
            f"window, or pass allow_sealed=True if this genuinely is the holdout "
            f"evaluation."
        )


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
#   fetcher         — the BaseFetcher subclass instance that knows how to
#                     retrieve and cache this feed's data
#   column          — the column name that will appear in the enriched
#                     DataFrame (e.g. 'fear_greed', 'funding_rate')
#   window_seconds  — the causality declaration (see AuxFeedCausalityError
#                     below): how far past its own `timestamp` row this feed's
#                     value aggregates. 0 for an instantaneous observation
#                     (funding rate, fear & greed — published AT `timestamp`,
#                     using no data after it); the bar width for a feed that
#                     aggregates a forward window ending at `timestamp +
#                     window_seconds` (e.g. the whale-footprint features,
#                     window_seconds == their own bar_seconds). REQUIRED, no
#                     default — deny by default: a feed that does not declare
#                     its window is a TypeError at registration, not a merge
#                     that trusts it implicitly.
#   agg             — how to reduce multiple readings within one candle window:
#                       'last'  → most recent value (default, good for rates/indices)
#                       'mean'  → average (good for noisy signals)
#                       'sum'   → sum (good for counts/volumes)
#   live_value      — the most recently fetched value, updated by the
#                     background poll thread in live mode; used as the
#                     enrichment value at candle close.
# ===========================================================================

@dataclass
class AuxFeedConfig:
    """Descriptor for one registered auxiliary data feed."""
    fetcher:        BaseFetcher
    column:         str
    window_seconds: float
    agg:            str = "last"          # 'last' | 'mean' | 'sum'
    live_value:     Optional[float] = None  # updated in live mode by poll thread
    required:       bool = False          # see AuxFeedRequiredError


class AuxFeedCausalityError(RuntimeError):
    """
    Raised at the aux-feed merge boundary when a feed's own declared
    aggregation window would extend past the bar it is about to be attached
    to — i.e. the value would encode information the strategy could not yet
    have at that bar's delivery time.

    WHY THIS EXISTS
    ----------------
    `test_aux_feed_causality_canary.py` (dispatch W8) proved empirically that
    the merge/execution path applies NO independent defense against a
    mistimed feed: a feature equal to a bar's literal NEXT return, attached at
    that bar via the same `merge_asof(direction='backward')` every real feed
    uses, produced a ~15x return with nothing anywhere raising. Causality
    rested entirely on each fetcher individually respecting its own window
    boundary — true today for the whale fetcher, but nothing in shared code
    would have caught a future fetcher that got this wrong.

    This is that defense, added at the one shared choke point every feed
    passes through (`DataManager._premerge_aux_feeds`). It is deny-by-default
    (`AuxFeedConfig.window_seconds` has no default — see above) and it TRUSTS
    the declared window rather than inspecting how the value was actually
    computed: it catches a feed that is honest about needing future data
    relative to the bar it is being merged onto (an off-by-one in window
    arithmetic, or a feed built for a coarser bar grid than the one it is
    attached to), not a feed that lies about its own window. See
    `data/ADDING_A_FEED.md` for the declaration this exception enforces.
    """


class AuxFeedVenueError(RuntimeError):
    """
    Raised at `_premerge_aux_feeds`'s no-data branch when a NON-binance-venue
    feed comes back empty (fix/exchange-plumbing-campaign-aux, Ticket 12).

    Binance's degradation contract is unchanged and pre-existing: an empty
    feed there still warns and fills the column with NaN
    (data_manager.py:677-678's documented behavior). That silent-NaN path is
    exactly wrong for any other venue -- a kraken run whose funding feed is
    empty because no kraken funding cache exists yet must not look
    indistinguishable from a kraken run whose funding really is flat, so it
    is refused here instead.

    Scope (read the mechanism, not just the name): this fires only when the
    feed's OWN fetcher declares a non-binance `exchange_id`. A fetcher with no
    `exchange_id` attribute at all (e.g. FearGreedFetcher -- a single global
    index, venue-independent by construction) is exempt by design and keeps
    the binance warn+NaN path regardless of which venue the backtest itself
    is running. Only a feed that HAS adopted `exchange_id` gets this
    protection -- see feed_registry.py's registry comment for what that means
    for a future feed.
    """


class AuxFeedRequiredError(RuntimeError):
    """Raised at `_premerge_aux_feeds`'s no-data branch when a feed registered
    with `required=True` comes back empty -- venue-agnostic, unlike AuxFeedVenueError."""


def _merge_asof_with_causality_guard(
    bars: pd.DataFrame,
    feed_data: pd.DataFrame,
    name: str,
    window_seconds: float,
    interval_seconds: int,
    feed_label: str,
) -> "pd.DataFrame":
    """
    `merge_asof(direction='backward')` the feed's `name` column onto `bars`
    (which must carry a `timestamp` column of bar START times), then refuse
    (raise `AuxFeedCausalityError`) if any matched row's declared source
    window — `[feed_ts, feed_ts + window_seconds)` — ends strictly after the
    bar's own end (`bar_ts + interval_seconds`). Equality is allowed: a feed
    whose window ends exactly when the bar closes is exactly what a
    correctly-bounded same-grid feed (e.g. whale features) looks like.

    `bars` is returned unmodified plus the new column; row order/index is not
    guaranteed to match the input (matches the pre-existing merge_asof calls
    this replaces).
    """
    src = (
        feed_data[["timestamp", name]]
        .sort_values("timestamp")
        .rename(columns={"timestamp": "__src_ts"})
    )
    merged = pd.merge_asof(
        bars.sort_values("timestamp"),
        src,
        left_on="timestamp",
        right_on="__src_ts",
        direction="backward",
    )
    matched = merged["__src_ts"].notna()
    if matched.any():
        window_end = merged.loc[matched, "__src_ts"] + datetime.timedelta(seconds=window_seconds)
        bar_end = merged.loc[matched, "timestamp"] + datetime.timedelta(seconds=interval_seconds)
        violations = window_end > bar_end
        if violations.any():
            bad = merged.loc[matched].loc[violations].iloc[0]
            raise AuxFeedCausalityError(
                f"aux feed '{feed_label}' column '{name}': declared source window "
                f"[{bad['__src_ts']} .. +{window_seconds}s] ends after bar "
                f"{bad['timestamp']} closes (bar_end="
                f"{bad['timestamp'] + datetime.timedelta(seconds=interval_seconds)}) — "
                f"refusing to attach a value the strategy could not yet have. "
                f"{int(violations.sum())} bar(s) affected."
            )
    return merged.drop(columns="__src_ts")


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
                    self.candle_completion_callback(symbol, current)
                except (TypeError, AttributeError, NameError):
                    raise  # structural defect in the callback path — fail loud, don't swallow
                except Exception as e:
                    logger.error(f"Candle callback error for {symbol}: {e}", exc_info=True)

            self.current_candles[symbol] = self._open_candle(symbol, price, volume, timestamp, open, high, low)
            return current
        else:
            # ── Candle update ─────────────────────────────────────────────
            # high/low MUST be forwarded (2026-08-28). They were dropped here
            # while _update_candle declared both parameters, so its
            # `high if high is not None else price` fallback made every row
            # after the first contribute only its CLOSE -- understating an
            # aggregated candle's high and overstating its low. Invisible at
            # one-row-per-candle (that path goes through _open_candle, which
            # always honoured them); it only bit when a candle spans multiple
            # rows, i.e. a derived timeframe such as 4h off a 1h cache.
            self._update_candle(current, price, volume, high, low)
            return None

    def flush_final_candle(self, symbol: str) -> Optional[Candle]:
        """
        Close the still-open final candle at end-of-backtest, mirroring
        _ingest's close sequence exactly (append → callback → pop). Idempotent:
        a second call finds no open candle and declines.

        No-lookahead: by the time this runs the replay loop has already fed
        every row, so the flushed candle exposes only data already seen —
        strictly less than an in-loop close, which opens the next candle on
        a later row.
        """
        current = self.current_candles.get(symbol)
        if current is None:
            logger.warning(f"flush_final_candle: no open candle for {symbol} — declining")
            return None

        self.completed_candles[symbol].append(current)
        if self.candle_completion_callback:
            try:
                self.candle_completion_callback(symbol, current)
            except (TypeError, AttributeError, NameError):
                raise  # structural defect in the callback path — fail loud, don't swallow
            except Exception as e:
                logger.error(f"Candle callback error for {symbol}: {e}", exc_info=True)

        self.current_candles.pop(symbol, None)
        return current

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

        All price/candle timestamps in this codebase are naive datetimes
        that represent UTC instants (never local time). Naive
        datetime.timestamp()/datetime.fromtimestamp() silently interpret
        and re-emit through the LOCAL system timezone instead of UTC —
        a no-op for interval_seconds that are an exact multiple of the
        local UTC offset (e.g. 3600s: any whole-hour offset cancels
        through the floor), but WRONG for any interval_seconds that is
        not (e.g. 86400s/1d on a non-UTC machine), silently shifting
        every aligned start_time to a fixed non-zero hour every day.
        Confirmed root cause of run_059's silent all-bars zero forecast
        at 1d: FundingRateMeanReversionComponent's settlement-boundary
        check (hour % 8 == 0) never matched because daily candles landed
        on hour=01 (or 02 under DST), never hour=00. Explicit UTC
        round-trip below removes the local-timezone dependency entirely;
        1h (and any interval_seconds that already cancelled) is
        unaffected -- see tests/test_funding_rate_component.py.
        """
        ts = int(timestamp.replace(tzinfo=datetime.timezone.utc).timestamp())
        aligned_ts = (ts // self.interval_seconds) * self.interval_seconds
        return datetime.datetime.fromtimestamp(
            aligned_ts, tz=datetime.timezone.utc
        ).replace(tzinfo=None)


# ===========================================================================
# DataManager
#
# Unified live + backtest data manager with pluggable auxiliary feed support.
#
# New in this version
# ────────────────────
# register_feed(name, fetcher, window_seconds, agg)
#     Plug in any BaseFetcher subclass.  The feed's data is automatically:
#       • fetched and cached (same storage pipeline as price data)
#       • pre-merged into historical_data before backtest replay starts,
#         through a causality guard that REFUSES (AuxFeedCausalityError) to
#         attach a value whose declared `window_seconds` would end after the
#         bar it is being merged onto — see data/ADDING_A_FEED.md
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
            name           = 'fear_greed',
            fetcher        = FearGreedFetcher('2024-01-01', '2024-12-31', localStorage=True),
            window_seconds = 0,  # published instantaneously — no forward window
            agg            = 'last',
        )
        dm.register_feed(
            name           = 'funding_rate',
            fetcher        = FundingRateFetcher('2024-01-01', '2024-12-31',
                                         symbols=['BTCUSDT'], localStorage=True),
            window_seconds = 0,  # published instantaneously — no forward window
            agg            = 'last',
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
        window_seconds: float,
        agg: str = "last",
        required: bool = False,
    ) -> None:
        """
        Register an auxiliary data feed.

        Args:
            name:           Column name that will appear in the enriched
                            DataFrame, e.g. 'fear_greed', 'funding_rate',
                            'open_interest'.
            fetcher:        Any BaseFetcher subclass instance.  Must be
                            pre-configured with the correct date range and
                            symbols.
            window_seconds: REQUIRED — the causality declaration consumed by
                            the merge guard (see AuxFeedCausalityError).
                            How far past its own `timestamp` row this feed's
                            value aggregates: 0 for an instantaneous
                            observation (funding rate, fear & greed), or the
                            width of a forward window for a feed that
                            aggregates one (e.g. whale-footprint features,
                            window_seconds == their own bar_seconds). No
                            default — deny by default, per
                            data/ADDING_A_FEED.md.
            agg:            Aggregation function to apply when multiple
                            readings fall within one candle window:
                              'last' — most recent value  (default)
                              'mean' — average
                              'sum'  — sum
            required:       If True, an empty/absent cache for this feed at
                            merge time raises AuxFeedRequiredError on every
                            venue, including binance (see
                            _premerge_aux_feeds). Default False preserves
                            prior behavior: binance warns and fills NaN,
                            non-binance raises AuxFeedVenueError.

        Can be called at any time before initialize() (backtest) or
        initiate_start_thread() (live).
        """
        if agg not in ("last", "mean", "sum"):
            raise ValueError(f"agg must be 'last', 'mean', or 'sum' — got '{agg}'")
        if not isinstance(window_seconds, (int, float)) or isinstance(window_seconds, bool) \
                or window_seconds < 0:
            raise ValueError(
                f"window_seconds must be a non-negative number — got {window_seconds!r}. "
                "This is a required causality declaration, not an optional tuning knob: "
                "see AuxFeedCausalityError / data/ADDING_A_FEED.md."
            )
        self._aux_feeds[name] = AuxFeedConfig(
            fetcher=fetcher, column=name, window_seconds=float(window_seconds), agg=agg,
            required=required,
        )
        logger.info(
            f"DataManager: registered aux feed '{name}' "
            f"(agg={agg}, window_seconds={window_seconds})"
        )

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
                    # at or before its timestamp using merge_asof. `enriched`
                    # here is _enrichment_data, already causality-checked once
                    # by _premerge_aux_feeds; re-checked with the same
                    # declared window for defense-in-depth at this second,
                    # independent merge_asof call site.
                    result = _merge_asof_with_causality_guard(
                        result, enriched, name, feed.window_seconds,
                        self.interval_seconds, feed_label=name,
                    )
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
                # logger.debug(f"_premerge '{name}': feed_data columns={feed_data.columns.tolist()}")
                # logger.debug(f"_premerge '{name}': feed_data head=\n{feed_data.head(3)}")
                # logger.debug(f"_premerge '{name}': price df timestamp range: {df['timestamp'].min()} → {df['timestamp'].max()}")
                # # After
                # if not feed_data.empty and 'timestamp' in feed_data.columns:
                #     logger.debug(f"_premerge '{name}': feed timestamp range: {feed_data['timestamp'].min()} → {feed_data['timestamp'].max()}")
                # else:
                #     logger.debug(f"_premerge '{name}': feed_data is empty after lookup")
            if feed_data.empty or name not in feed_data.columns:
                exchange_id = getattr(feed.fetcher, "exchange_id", "binance")
                if feed.required:
                    raise AuxFeedRequiredError(
                        f"aux feed '{name}' (symbol={symbol}) is required but has no "
                        f"data on exchange '{exchange_id}' — looked for cache file "
                        f"'{feed.fetcher.cache_key(symbol)}'. Ingest '{name}' data for "
                        f"'{exchange_id}', or remove the component(s) that require it."
                    )
                if exchange_id != "binance":
                    raise AuxFeedVenueError(
                        f"aux feed '{name}' (symbol={symbol}) has no data on "
                        f"exchange '{exchange_id}' — looked for cache file "
                        f"'{feed.fetcher.cache_key(symbol)}'. Either ingest "
                        f"'{name}' data for '{exchange_id}', or drop '{name}' "
                        f"from extra_feeds for this run."
                    )
                logger.warning(
                    f"DataManager: no data for aux feed '{name}' "
                    f"(symbol={symbol}) — column will be all-NaN for every bar"
                )
                enriched[name] = np.nan
                continue

            # Apply the registered aggregation function to handle cases where
            # the aux feed has higher resolution than the price data
            # (e.g. funding rate every 8h, price every 1m)
            effective_window_seconds = feed.window_seconds
            if feed.agg != "last":
                feed_data = (
                    feed_data
                    .set_index("timestamp")
                    .resample(f"{self.interval_seconds}s")
                    .agg({name: feed.agg})
                    .reset_index()
                )
                # Resampling buckets raw readings into one row per bar-width
                # bucket, so the resampled row's own window is at least the
                # bucket width regardless of what each raw reading declared —
                # a 'sum'/'mean' over [T, T+interval_seconds) is exactly the
                # forward window whale features already declare on their own
                # grid, so this only ever widens (never narrows) the check.
                effective_window_seconds = max(feed.window_seconds, self.interval_seconds)

            enriched = _merge_asof_with_causality_guard(
                enriched, feed_data, name, effective_window_seconds,
                self.interval_seconds, feed_label=name,
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

    def flush_final_candle(self, symbol: str) -> Optional[Candle]:
        """
        Backtest-only: force-close the final still-open candle through the
        normal completion path so the last fetched bar is processed like any
        other (E-012). RAISES in live mode — a live run must never force-close
        a candle that is still genuinely forming.
        """
        if self.mode == "live":
            raise RuntimeError(
                "flush_final_candle is backtest-only; refusing to flush a "
                "live candle that may still be forming"
            )
        return self.candle_builder.flush_final_candle(symbol)

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
        return self._cursor.get(symbol, 0) < len(self.historical_data[symbol])

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
        n = len(self.historical_data[symbol])
        new_idx = self._cursor.get(symbol, 0) + steps
        if new_idx >= n:
            self._cursor[symbol] = min(new_idx, n)
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

    def fetch_historical_data(self, symbol: str, start_date, end_date, exchange: str = "binance",
                              allow_sealed: bool = False) -> pd.DataFrame:
        """
        Fetch raw OHLCV data for one symbol via CcxtFetcher and return it as
        a flat DataFrame.

        Typical call from BacktestEngine.load_data():
            self.historical_data[symbol] = self.data_manager.fetch_historical_data(
                symbol, start_date, end_date
            )
        followed by self.data_manager.initialize().

        `exchange` selects the CCXT exchange id used for both the remote
        fetch and the local cache filename (see CcxtFetcher.cache_key());
        defaults to "binance" so existing call sites are unaffected unless
        they opt in (e.g. exchange="kraken" to reach kraken_XBTUSD_1h etc.).

        Returns an empty DataFrame on failure.
        """
        logger.debug(f"Fetching OHLCV for {symbol}  {start_date} → {end_date}  (exchange={exchange})")

        data_folder = os.path.dirname(os.path.abspath(__file__))
        project_folder = os.path.dirname(data_folder)
        data_storage_dir = os.path.join(project_folder, "local_data")

        fetcher = HistoricalDataFetcher(
            start_date, end_date, [symbol],
            candle_interval_seconds=self.interval_seconds,
            exchange=exchange,
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

                # Seal guard on the READ path (2026-08-19).
                #
                # The 7 committed Binance caches physically contain sealed 2026
                # rows -- the seal guards added earlier block NEW leaks but never
                # removed the existing ones (BTCUSDT_1h.csv alone carries 4,344
                # rows >= 2026-01-01), and those files are now also on the shared
                # culi.to server. Trimming them is the eventual fix, but it
                # changes their content hash and therefore data_sha256, forcing a
                # rebaseline of the reference run; this guard gets the protection
                # today without that cost.
                #
                # Placed on the RETURNED frame, deliberately, not in
                # BaseFetcher._load_local: that frame feeds _merge_and_store, so
                # clamping there would silently rewrite the caches on the next
                # save -- turning a read guard into an uncontrolled data
                # mutation, which is the separate bug already tracked against
                # this same read path.
                #
                # Expected to be a no-op for every legitimate run: get_data()
                # already bounds by the requested window and every non-holdout
                # window ends <= 2025-12-31, so there is nothing past the seal to
                # drop. It bites only on a request that reaches into the sealed
                # range -- which is exactly the thing to refuse.
                if not allow_sealed:
                    _assert_no_sealed_rows(data[symbol], symbol)
                return data[symbol]
            else:
                logger.warning(f"No OHLCV data available for {symbol}")
                return pd.DataFrame()
        except SealedDataError:
            # MUST propagate. The blanket handler below degrades every failure to
            # an empty DataFrame, which would silently defeat the seal guard
            # entirely — the caller would see "no data" and move on, exactly the
            # quiet outcome the guard exists to prevent. Same convention, and the
            # same reason, as base_fetcher._load_local's tz-aware guard.
            raise
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
