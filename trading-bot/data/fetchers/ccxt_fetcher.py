"""
CcxtFetcher
===========
Fetches OHLCV price data from any CCXT-compatible exchange (defaulting to
Binance) and stores it locally as CSV.

This is a direct extraction of the old HistoricalDataFetcher network logic.
The gap-detection, storage, and merge logic it previously owned now lives in
BaseFetcher and is inherited here for free.

Subclass responsibilities implemented here:
  • _fetch_remote(symbol, start, end) → paginated CCXT fetch_ohlcv calls
  • cache_key(symbol)                 → e.g. 'BTCUSDT_5m'

Usage (unchanged from old HistoricalDataFetcher):
    fetcher = CcxtFetcher(start, end, ['BTCUSDT'],
                          candle_interval_seconds=300,
                          exchange='binance',
                          localStorage=True)
    data = fetcher.get_data()  # {symbol: DataFrame}
"""

import datetime
import logging
import time

import ccxt
import numpy as np
import pandas as pd

from data.fetchers.base_fetcher import BaseFetcher

logger = logging.getLogger("trading_bot")


class CcxtFetcher(BaseFetcher):
    """
    OHLCV fetcher backed by CCXT.

    Handles:
      • Binance compact symbol → CCXT 'BASE/QUOTE' normalisation
      • Paginated fetch_ohlcv loops (most exchanges cap at 1000 rows/call)
      • Exchange rate-limit compliance via ccxt's built-in rateLimit value
      • Extra Binance-compatible columns (close_time, quote_asset_volume…)
        kept for format compatibility with the rest of the codebase
    """

    def __init__(
        self,
        start_date,
        end_date,
        symbols=None,
        candle_interval_seconds: int = 60,
        exchange: str = "binance",
        localStorage: bool = False,
        data_dir: str = "data",
    ):
        """
        Args:
            candle_interval_seconds: Desired candle resolution in seconds.
                                     Snapped to the nearest CCXT timeframe
                                     (1m, 5m, 15m, 30m, 1h, 4h, 1d) for the
                                     API call.  DataManager re-aggregates if the
                                     stored resolution is finer than the target.
            exchange:                Any CCXT-supported exchange id string.
            localStorage:            Cache fetched data to ./data/ as CSV.
        """
        if symbols is None:
            symbols = ["BTCUSDT"]

        # Snap to nearest CCXT timeframe string before calling super().__init__
        # so that interval_seconds stored on the base class reflects the actual
        # candle size being fetched (used for gap arithmetic).
        self.ccxt_timeframe = self._seconds_to_ccxt_timeframe(candle_interval_seconds)

        super().__init__(
            start_date=start_date,
            end_date=end_date,
            symbols=symbols,
            interval_seconds=candle_interval_seconds,
            localStorage=localStorage,
            data_dir=data_dir,
        )

        self.exchange_id = exchange
        try:
            exchange_class = getattr(ccxt, self.exchange_id)
            self.exchange = exchange_class(
                {
                    "enableRateLimit": True,
                    "options": {"defaultType": "spot"},
                }
            )
            logger.info(f"CcxtFetcher: initialised {self.exchange_id}")
        except Exception as e:
            logger.error(f"CcxtFetcher: failed to initialise {self.exchange_id}: {e}")
            self.exchange = None

    # -----------------------------------------------------------------------
    # BaseFetcher interface
    # -----------------------------------------------------------------------

    def cache_key(self, symbol: str) -> str:
        """
        e.g. 'BTCUSDT_5m' (Binance) or 'kraken_XBTUSD_1h' (Kraken).

        The key is exchange-qualified so caches from different venues can never
        collide among CcxtFetcher-derived caches (e.g. a Kraken instance fetching
        'BTCUSDT' must not overwrite / silently read Binance's 'BTCUSDT_1h.csv').
        This guarantee is scoped to CcxtFetcher; it does not automatically
        extend to other BaseFetcher subclasses in the same flat data_dir
        namespace. FundingRateFetcher.cache_key() (funding_rate_fetcher.py:
        117-118) independently mirrors this same prefix rule as of
        fix/exchange-plumbing-campaign-aux, but that is a deliberate parallel
        construction, not an inherited guarantee from this class.

        Backward-compatibility (decision (a) of the exchange-qualification
        dispatch): Binance keeps its historical UN-prefixed key, so every
        existing on-disk cache file (local_data/BTCUSDT_1h.csv, ...) continues
        to load byte-identically with no migration. Only non-Binance exchanges
        receive the '{exchange_id}_' prefix. self.exchange_id is always set by
        __init__ before any cache_key() call (which only happens later via
        get_data()/_load_all()).
        """
        prefix = "" if self.exchange_id == "binance" else f"{self.exchange_id}_"
        return f"{prefix}{symbol}_{self.ccxt_timeframe}"

    def _fetch_remote(
        self,
        symbol: str,
        start: datetime.datetime,
        end: datetime.datetime,
    ) -> pd.DataFrame:
        """
        Fetch OHLCV data via paginated CCXT fetch_ohlcv calls.

        Pagination: most exchanges return at most 1000 candles per call.
        We advance `current_since` by one timeframe after each batch until
        `until` is reached or fewer than 100 candles are returned (indicating
        we're at the edge of available data).

        Symbol normalisation: CCXT requires 'BTC/USDT'; Binance uses 'BTCUSDT'.
        We detect compact symbols and insert the '/' separator.
        """
        if self.exchange is None:
            logger.error("CcxtFetcher: exchange not initialised")
            return pd.DataFrame()

        since = int(start.timestamp() * 1000)  # ms epoch
        until = int(end.timestamp() * 1000)
        all_candles = []
        current_since = since

        while current_since < until:
            try:
                # Normalise 'BTCUSDT' → 'BTC/USDT' for CCXT
                exchange_symbol = symbol
                if "/" not in symbol and len(symbol) > 3:
                    for quote in ["USDT", "USD", "BUSD", "USDC", "ETH", "BTC"]:
                        if symbol.endswith(quote):
                            exchange_symbol = f"{symbol[: -len(quote)]}/{quote}"
                            break

                candles = self.exchange.fetch_ohlcv(
                    symbol=exchange_symbol,
                    timeframe=self.ccxt_timeframe,
                    since=current_since,
                    limit=1000,
                )
                if not candles:
                    break

                all_candles.extend(candles)
                last_ts = candles[-1][0]
                current_since = last_ts + self._timeframe_to_ms(self.ccxt_timeframe)
                time.sleep(self.exchange.rateLimit / 1000)  # respect rate limit

                if last_ts >= until or len(candles) < 100:
                    break  # reached end of window or end of available data

            except Exception as e:
                logger.error(f"CcxtFetcher: error fetching {symbol}: {e}")
                break

        if not all_candles:
            logger.warning(f"CcxtFetcher: no data returned for {symbol}")
            return pd.DataFrame()

        df = pd.DataFrame(
            all_candles,
            columns=["timestamp", "open", "high", "low", "close", "volume"],
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        # Extra columns kept for Binance format compatibility
        ms = self._timeframe_to_ms(self.ccxt_timeframe)
        df["close_time"] = df["timestamp"] + datetime.timedelta(milliseconds=ms - 1)
        df["quote_asset_volume"] = df["volume"] * df["close"]  # estimated
        df["number_of_trades"] = np.nan
        df["taker_buy_base_asset_volume"] = np.nan
        df["taker_buy_quote_asset_volume"] = np.nan
        df["ignore"] = 0
        print(
            f"CcxtFetcher: fetched {len(df)} candles for {symbol} from {self.exchange_id}, example row:\n{df.iloc[0:5].to_dict()}"
        )
        return df

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    @staticmethod
    def _seconds_to_ccxt_timeframe(seconds: int) -> str:
        """
        Map seconds to the nearest CCXT timeframe string.

        E.g. 240 s → '5m'.  The DataManager's CandleBuilder will then
        re-aggregate the stored 5-minute candles to the exact 4-minute target
        during replay.
        """
        intervals = {
            60: "1m",
            300: "5m",
            900: "15m",
            1800: "30m",
            3600: "1h",
            14400: "4h",
            86400: "1d",
        }
        return intervals[min(intervals, key=lambda x: abs(x - seconds))]

    @staticmethod
    def _timeframe_to_ms(timeframe: str) -> int:
        """Convert a CCXT timeframe string to milliseconds."""
        amount = int("".join(filter(str.isdigit, timeframe)))
        unit = "".join(filter(str.isalpha, timeframe))
        return amount * {"m": 60_000, "h": 3_600_000, "d": 86_400_000, "w": 604_800_000}.get(unit, 3_600_000)

    # -----------------------------------------------------------------------
    # Kept for backward compatibility with callers that used the old class name
    # -----------------------------------------------------------------------

    def validate_data_continuity(self, symbol: str):
        """Delegates to BaseFetcher.validate_data_continuity()."""
        return super().validate_data_continuity(symbol)


# ---------------------------------------------------------------------------
# Backward-compatibility alias
# Code that still imports HistoricalDataFetcher continues to work unchanged.
# ---------------------------------------------------------------------------
HistoricalDataFetcher = CcxtFetcher
