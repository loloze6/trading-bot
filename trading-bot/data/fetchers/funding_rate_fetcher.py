"""
FundingRateFetcher
==================
Fetches perpetual futures funding rates from Binance via CCXT and stores
them locally as CSV.

Funding rates are published every 8 hours on Binance (00:00, 08:00, 16:00 UTC).
They are a key on-chain / market-structure signal for crypto strategies:
  • Strongly positive rate  → market is paying longs to hold → crowded long
  • Strongly negative rate  → market is paying shorts to hold → crowded short

Output column added to the candle DataFrame:  'funding_rate'  (float, e.g. 0.0001)

During candle-level enrichment in DataManager the rate is forward-filled
(merge_asof) so every candle between two funding events inherits the most
recently published rate.

Usage:
    fetcher = FundingRateFetcher('2024-01-01', '2024-12-31',
                                 symbols=['BTCUSDT'],
                                 localStorage=True)
    data = fetcher.get_data()   # {'BTCUSDT': DataFrame}

    # Register with DataManager:
    data_manager.register_feed(
        name='funding_rate',
        fetcher=FundingRateFetcher(...),
        window_seconds=0,  # published instantaneously — no forward window
        agg='last',
        fill='carry_forward',  # a level: bars without a new print keep the last one (CUL-355)
    )
"""

import datetime
import logging
import time

import pandas as pd

try:
    import ccxt
    _CCXT_AVAILABLE = True
except ImportError:
    _CCXT_AVAILABLE = False

from data.fetchers.base_fetcher import BaseFetcher, _utc_epoch_ms

logger = logging.getLogger("trading_bot")

_FUNDING_INTERVAL_SECONDS = 8 * 3600   # 8 hours in seconds

# Per-exchange settlement cadence, applied at construction only when the caller
# does not pass interval_seconds explicitly. Kraken Futures settles hourly;
# every other venue keeps Binance's 8h default.
_EXCHANGE_FUNDING_INTERVALS = {"krakenfutures": 3600}


class FundingRateFetcher(BaseFetcher):
    """
    Binance perpetual futures funding rates via CCXT.

    CCXT's fetch_funding_rate_history endpoint is used with paginated requests
    similar to the OHLCV fetch in CcxtFetcher.  The exchange must support
    perpetual futures (use exchange_id='binance' and type='future').
    """

    # Allow gaps up to 2× the 8-hour interval before flagging
    # (exchange maintenance windows can delay one publication).
    expected_gap_tolerance: float = 2.0

    def __init__(
        self,
        start_date,
        end_date,
        symbols=None,
        exchange_id: str = "binance",
        localStorage: bool = False,
        data_dir: str = "data",
        interval_seconds: int | None = None,
    ):
        if symbols is None:
            symbols = ["BTCUSDT"]

        if interval_seconds is None:
            interval_seconds = _EXCHANGE_FUNDING_INTERVALS.get(exchange_id, _FUNDING_INTERVAL_SECONDS)

        super().__init__(
            start_date=start_date,
            end_date=end_date,
            symbols=symbols,
            interval_seconds=interval_seconds,
            localStorage=localStorage,
            data_dir=data_dir,
        )

        self.exchange_id = exchange_id
        if _CCXT_AVAILABLE:
            try:
                exchange_class = getattr(ccxt, self.exchange_id)
                # Must use futures market type for funding rates
                self.exchange  = exchange_class({
                    "enableRateLimit": True,
                    "options": {"defaultType": "future"},
                })
                logger.info(f"FundingRateFetcher: initialised {self.exchange_id} (futures)")
            except Exception as e:
                logger.error(f"FundingRateFetcher: failed to initialise exchange: {e}")
                self.exchange = None
        else:
            logger.error("FundingRateFetcher: ccxt not installed")
            self.exchange = None

    # -----------------------------------------------------------------------
    # BaseFetcher interface
    # -----------------------------------------------------------------------

    def cache_key(self, symbol: str) -> str:
        """
        e.g. 'BTCUSDT_funding_8h' (Binance 8h) or
        'krakenfutures_BTCUSD_funding_1h' (Kraken Futures hourly).

        Mirrors CcxtFetcher's binance-unprefixed prefix rule (ccxt_fetcher.py:
        123-124): Binance keeps its historical UN-prefixed key, so every
        existing on-disk cache (local_data/{AVAXUSDT,BTCUSDT,SOLUSDT}_funding_
        8h.csv) continues to load byte-identically with no migration. Only
        non-Binance exchange ids receive the '{exchange_id}_' prefix. The
        '_{hours}h' suffix is derived from interval_seconds, so a Binance 8h
        feed stays '_funding_8h' byte-identically.
        """
        prefix = "" if self.exchange_id == "binance" else f"{self.exchange_id}_"
        hours = self.interval_seconds // 3600
        return f"{prefix}{symbol}_funding_{hours}h"

    def _fetch_remote(
        self,
        symbol: str,
        start: datetime.datetime,
        end: datetime.datetime,
    ) -> pd.DataFrame:
        """
        Fetch funding rate history via CCXT fetch_funding_rate_history.

        Paginates in 1000-record batches the same way CcxtFetcher does for
        OHLCV.  Each record becomes one row with columns:
            timestamp, funding_rate, mark_price (if available)
        """
        if self.exchange is None:
            logger.error("FundingRateFetcher: exchange not initialised")
            return pd.DataFrame()

        # CCXT expects 'BTC/USDT:USDT' format for perpetual futures
        exchange_symbol = self._to_perp_symbol(symbol)

        # start/end are tz-naive UTC instants; naive datetime.timestamp() shifts
        # the epoch by the host UTC offset on a non-UTC host (CUL-248).
        since         = _utc_epoch_ms(start)
        until         = _utc_epoch_ms(end)
        all_records   = []
        current_since = since

        while current_since < until:
            try:
                rates = self.exchange.fetch_funding_rate_history(
                    symbol=exchange_symbol,
                    since=current_since,
                    limit=1000,
                )
                if not rates:
                    break

                for r in rates:
                    all_records.append({
                        "timestamp":    pd.to_datetime(r["timestamp"], unit="ms"),
                        "funding_rate": float(r.get("fundingRate", 0.0)),
                        "mark_price":   float(r.get("markPrice", 0.0)) if r.get("markPrice") else None,
                    })

                last_ts       = rates[-1]["timestamp"]
                current_since = last_ts + self.interval_seconds * 1000
                time.sleep(self.exchange.rateLimit / 1000)

                if last_ts >= until or len(rates) < 100:
                    break

            except Exception as e:
                logger.error(f"FundingRateFetcher: error fetching {symbol}: {e}")
                break

        if not all_records:
            logger.warning(f"FundingRateFetcher: no data returned for {symbol}")
            return pd.DataFrame()

        df = pd.DataFrame(all_records).sort_values("timestamp").reset_index(drop=True)
        logger.info(f"FundingRateFetcher: fetched {len(df)} funding events for {symbol}")
        return df

    # -----------------------------------------------------------------------
    # Helper
    # -----------------------------------------------------------------------

    @staticmethod
    def _to_perp_symbol(symbol: str) -> str:
        """
        Convert 'BTCUSDT' → 'BTC/USDT:USDT' (Binance perpetual futures format).
        If the symbol already contains '/' it is returned unchanged.
        """
        if "/" in symbol:
            return symbol
        for quote in ["USDT", "USD", "BUSD", "USDC"]:
            if symbol.endswith(quote):
                base = symbol[:-len(quote)]
                return f"{base}/{quote}:{quote}"
        return symbol
