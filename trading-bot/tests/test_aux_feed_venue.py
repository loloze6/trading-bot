"""
Ticket 12 (aux feeds don't follow trading.exchange) — commit C2.

Before this commit, aux feeds constructed inside BacktestEngine.load_data()
(core/backtester.py:121-127) always got FundingRateFetcher's default
exchange_id="binance" — the factory contract (data/feed_registry.py) took no
exchange parameter and the engine had no way to pass one. A kraken run's price
cache was venue-correct (leg-3) but its funding feed silently stayed binance:
the feed's cache_key was also venue-blind (funding_rate_fetcher.py:107-109
returned the same 'BTCUSDT_funding_8h' regardless of exchange_id), so an empty
fetch degraded to a warned, all-NaN column instead of surfacing the mismatch.

This file pins:
  - the venue-qualified funding cache_key (T-06/T-07)
  - the factory contract threading exchange_id through (T-08, T-14, T-15)
  - the engine passing its own exchange into every factory call (T-09)
  - the new fail-loud AuxFeedVenueError for a non-binance empty feed (T-10)
  - the untouched binance warn+NaN degradation, log text corrected (T-11)
"""
import logging
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent      # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.backtester import BacktestEngine                       # noqa: E402
from data.data_manager import AuxFeedVenueError, DataManager     # noqa: E402
from data.feed_registry import FEED_REGISTRY, RESERVED_FEED_REGISTRY  # noqa: E402
from data.fetchers.base_fetcher import BaseFetcher                    # noqa: E402
from data.fetchers.funding_rate_fetcher import FundingRateFetcher     # noqa: E402
from data.fetchers.whale_footprint_fetcher import ReservedDataError   # noqa: E402

TEST_LOGGER = logging.getLogger("test_aux_feed_venue")


# ---------------------------------------------------------------------------
# cache_key venue qualification (T-06, T-07)
# ---------------------------------------------------------------------------

def test_funding_cache_key_binance_stays_unprefixed():
    fetcher = FundingRateFetcher("2022-01-01", "2022-01-02", symbols=["BTCUSDT"],
                                  exchange_id="binance")
    assert fetcher.cache_key("BTCUSDT") == "BTCUSDT_funding_8h"


def test_funding_cache_key_kraken_gets_prefixed():
    fetcher = FundingRateFetcher("2022-01-01", "2022-01-02", symbols=["BTCUSD"],
                                  exchange_id="kraken")
    assert fetcher.cache_key("BTCUSD") == "kraken_BTCUSD_funding_8h"


# ---------------------------------------------------------------------------
# Factory contract (T-08, T-14, T-15)
# ---------------------------------------------------------------------------

def test_funding_rate_factory_threads_exchange_id(tmp_path):
    fetcher = FEED_REGISTRY["funding_rate"](
        ["BTCUSD"], "2022-01-01", "2022-01-02", str(tmp_path), exchange="kraken"
    )
    assert fetcher.exchange_id == "kraken"


def test_all_registry_factories_accept_the_exchange_kwarg(tmp_path):
    """Contract sweep (R2): a factory that hasn't adopted `exchange=` must
    TypeError, never silently ignore it -- this proves every current factory
    (both registries) has adopted it."""
    for factory in FEED_REGISTRY.values():
        factory(["BTCUSD"], "2022-01-01", "2022-01-02", str(tmp_path), exchange="kraken")

    # Whale factories accept the kwarg too, but the reserved-data gate still
    # fires for an undesignated window -- ReservedDataError, not TypeError,
    # proves the kwarg was accepted before the gate ever ran.
    for factory in RESERVED_FEED_REGISTRY.values():
        with pytest.raises(ReservedDataError):
            factory(["BTCUSD"], "2026-07-26", "2026-07-27", str(tmp_path), exchange="kraken")


def test_funding_rate_factory_default_is_binance_positional(tmp_path):
    """Pins the factory default's VALUE (not just its existence): called with
    the historical 4-arg POSITIONAL shape (no exchange), the funding factory
    must still resolve exchange_id="binance" -- the engine passes exchange=
    explicitly (E6), so this default is otherwise a dead branch that a
    default-flip mutation could silently invert."""
    fetcher = FEED_REGISTRY["funding_rate"](["BTCUSDT"], "2022-01-01", "2022-01-02", str(tmp_path))
    assert fetcher.exchange_id == "binance"


# ---------------------------------------------------------------------------
# Engine -> factory threading (T-09)
# ---------------------------------------------------------------------------

class _RecordingDataManager:
    """Stands in for DataManager inside load_data(): serves one bar, records
    register_feed() calls, never touches the network."""

    def __init__(self):
        self.historical_data = {}
        self._aux_feeds = {}

    def fetch_historical_data(self, symbol, start_date, end_date, exchange="binance"):
        return pd.DataFrame({"timestamp": [pd.Timestamp("2022-01-01")], "close": [1.0]})

    def register_feed(self, name, fetcher, window_seconds, agg):
        self._aux_feeds[name] = fetcher

    def initialize(self):
        pass


def test_engine_threads_its_own_exchange_into_every_factory_call():
    captured = {}

    def recording_factory(symbols, start, end, data_dir, exchange="binance"):
        captured["exchange"] = exchange
        return object()

    dm = _RecordingDataManager()
    engine = BacktestEngine(data_manager=dm, logger=TEST_LOGGER, symbols=["BTCUSD"],
                             exchange="kraken")
    engine.load_data(start_date="2022-01-01", end_date="2022-01-02",
                      extra_feeds={"funding_rate": recording_factory})

    assert captured["exchange"] == "kraken"


def test_engine_without_an_exchange_threads_binance_into_factories():
    captured = {}

    def recording_factory(symbols, start, end, data_dir, exchange="binance"):
        captured["exchange"] = exchange
        return object()

    dm = _RecordingDataManager()
    engine = BacktestEngine(data_manager=dm, logger=TEST_LOGGER, symbols=["BTCUSD"])
    engine.load_data(start_date="2022-01-01", end_date="2022-01-02",
                      extra_feeds={"funding_rate": recording_factory})

    assert captured["exchange"] == "binance"


# ---------------------------------------------------------------------------
# Fail-loud vs. warn+NaN at the no-data branch (T-10, T-11)
# ---------------------------------------------------------------------------

class _EmptyFeedFetcher(BaseFetcher):
    """Always reports no data, whatever venue it claims -- drives
    _premerge_aux_feeds straight into the no-data branch under test."""

    def __init__(self, exchange_id):
        super().__init__(
            start_date="2022-01-01", end_date="2022-01-02",
            symbols=["BTCUSD"], interval_seconds=0,
        )
        self.exchange_id = exchange_id

    def get_data(self, symbol=None):
        return pd.DataFrame()

    def cache_key(self, symbol):
        return f"{self.exchange_id}_STUB_funding_8h"

    def _fetch_remote(self, symbol, start, end):
        return pd.DataFrame()


def _price_df():
    return pd.DataFrame({"timestamp": [pd.Timestamp("2022-01-01")], "close": [1.0]})


def test_premerge_raises_aux_feed_venue_error_for_nonbinance_empty_feed():
    dm = DataManager(symbols=["BTCUSD"], interval_seconds=3600, mode="backtest")
    dm.register_feed(name="funding_rate", fetcher=_EmptyFeedFetcher("kraken"),
                      window_seconds=0, agg="last")

    with pytest.raises(AuxFeedVenueError, match="kraken"):
        dm._premerge_aux_feeds("BTCUSD", _price_df())


def test_premerge_binance_empty_feed_still_warns_and_nans(caplog):
    dm = DataManager(symbols=["BTCUSD"], interval_seconds=3600, mode="backtest")
    dm.register_feed(name="funding_rate", fetcher=_EmptyFeedFetcher("binance"),
                      window_seconds=0, agg="last")

    with caplog.at_level(logging.WARNING, logger="trading_bot"):
        enriched = dm._premerge_aux_feeds("BTCUSD", _price_df())

    assert enriched["funding_rate"].isna().all()
    assert "all-NaN for every bar" in caplog.text
