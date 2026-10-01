"""
CUL-356: per-feed publication delay. Fear & greed is stamped with its day at
00:00 UTC and its historical publication time is undocumented, so a reading
stamped day D is usable only from day D+1 (A8.4, runs/run_042's feed
alignment check). The shift lived in the deleted prescreen loader
(bef5f3a4); since then the engine gave the 00:00 bar of day D day D's value.

  * with delay 86400 every bar of day D carries day D-1's value (1h, 4h, 1d);
  * delay 0 is exactly the previous behaviour (funding, whale features);
  * a reading shifted past the last bar is never attached to it;
  * the registry declares a delay for every feed and the backtester passes it;
  * the existing FearGreedContrarianComponent reads the prior day's value.
"""
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.data_manager import DataManager  # noqa: E402
from data.feed_registry import (  # noqa: E402
    FEED_AGG, FEED_DELAY_SECONDS, FEED_FILL, FEED_WINDOW_SECONDS, WHALE_FOOTPRINT_FEEDS,
)
from strategies.strategy_components import FearGreedContrarianComponent  # noqa: E402

SYMBOL = "BTCUSDT"
START = pd.Timestamp("2021-03-01")
DAY = pd.Timedelta(days=1)
VALUES = [20, 40, 60, 80, 30]            # one reading a day from START


class _StubFetcher:
    exchange_id = "binance"

    def __init__(self, df):
        self._df = df

    def get_data(self, symbol=None):
        return self._df

    def cache_key(self, symbol):
        return "stub"


def _fear_greed() -> pd.DataFrame:
    return pd.DataFrame({"timestamp": pd.date_range(START, periods=len(VALUES), freq="D"),
                         "fear_greed": VALUES})


def _bars(interval_seconds: int, days: int = 6) -> pd.DataFrame:
    ts = pd.date_range(START, periods=days * 86400 // interval_seconds, freq=f"{interval_seconds}s")
    return pd.DataFrame({"timestamp": ts, "open": 100.0, "high": 100.0, "low": 100.0,
                         "close": 100.0, "volume": 1.0})


def _enriched(interval_seconds: int, delay_seconds: float, bars=None) -> pd.DataFrame:
    price = _bars(interval_seconds) if bars is None else bars
    dm = DataManager(symbols=[SYMBOL], interval_seconds=interval_seconds, mode="backtest")
    dm.register_feed("fear_greed", _StubFetcher(_fear_greed()), window_seconds=0, agg="last",
                     fill="carry_forward", delay_seconds=delay_seconds)
    dm.historical_data[SYMBOL] = price
    dm.initialize()
    return dm._attach_aux_columns(SYMBOL, price).sort_values("timestamp").reset_index(drop=True)


INTERVALS = [3600, 4 * 3600, 86400]


@pytest.mark.parametrize("interval_seconds", INTERVALS, ids=["1h", "4h", "1d"])
def test_every_bar_of_day_d_carries_day_d_minus_1(interval_seconds):
    out = _enriched(interval_seconds, 86400)
    for _, row in out.iterrows():
        day_index = (row["timestamp"].normalize() - START).days
        if day_index == 0:
            assert pd.isna(row["fear_greed"]), row["timestamp"]      # nothing published yet
        else:
            expected = VALUES[min(day_index - 1, len(VALUES) - 1)]
            assert float(row["fear_greed"]) == expected, (row["timestamp"], row["fear_greed"])


@pytest.mark.parametrize("interval_seconds", INTERVALS, ids=["1h", "4h", "1d"])
def test_the_00_00_bar_no_longer_sees_its_own_day(interval_seconds):
    """The exact CUL-356 exposure: bar D 00:00 used to carry day D's value."""
    before = _enriched(interval_seconds, 0)
    after = _enriched(interval_seconds, 86400)
    d2 = START + 2 * DAY
    b = before[before["timestamp"] == d2]["fear_greed"].iloc[0]
    a = after[after["timestamp"] == d2]["fear_greed"].iloc[0]
    assert (b, a) == (VALUES[2], VALUES[1])


@pytest.mark.parametrize("interval_seconds", INTERVALS, ids=["1h", "4h", "1d"])
def test_delay_zero_is_the_previous_behaviour(interval_seconds):
    price = _bars(interval_seconds)
    dm = DataManager(symbols=[SYMBOL], interval_seconds=interval_seconds, mode="backtest")
    dm.register_feed("fear_greed", _StubFetcher(_fear_greed()), window_seconds=0, agg="last",
                     fill="carry_forward")                        # no delay argument at all
    dm.historical_data[SYMBOL] = price
    dm.initialize()
    default = dm._attach_aux_columns(SYMBOL, price).sort_values("timestamp").reset_index(drop=True)
    pd.testing.assert_frame_equal(default, _enriched(interval_seconds, 0))


def test_a_reading_shifted_past_the_last_bar_is_never_attached():
    """The last bar is day 4 23:00; day 4's reading becomes usable at day 5
    00:00, after that bar -- the bar keeps day 3's value. (Same mechanism that
    keeps a pre-seal reading, shifted onto the first sealed day, off every
    pre-seal bar.)"""
    bars = _bars(3600, days=5)
    out = _enriched(3600, 86400, bars=bars)
    last = out.iloc[-1]
    assert last["timestamp"] == START + 4 * DAY + pd.Timedelta(hours=23)
    assert float(last["fear_greed"]) == VALUES[3]


def test_the_existing_contrarian_component_reads_the_prior_day():
    """DECLARED CHANGE: FearGreedContrarian fires at 00:00 on day D from day
    D-1's value (was day D's)."""
    after = _enriched(3600, 86400).assign(close=100.0)
    before = _enriched(3600, 0).assign(close=100.0)
    d1 = START + DAY                                   # day 1: value 40 (before) vs 20 (after)
    out = {}
    for label, df in (("before", before), ("after", after)):
        comp = FearGreedContrarianComponent(parameters={"fear_threshold": 25.0, "greed_threshold": 75.0})
        comp.update(df[df["timestamp"] <= d1])
        out[label] = comp.raw_value()
    assert out == {"before": 0.0, "after": 10.0}      # 40: no signal; 20 < 25: long (contrarian)


# ---------------------------------------------------------------------------
# Declarations and wiring
# ---------------------------------------------------------------------------

def test_every_feed_declares_a_delay():
    assert set(FEED_DELAY_SECONDS) == set(FEED_WINDOW_SECONDS) == set(FEED_AGG) == set(FEED_FILL)
    assert FEED_DELAY_SECONDS["fear_greed"] == 86400
    assert FEED_DELAY_SECONDS["funding_rate"] == 0
    assert {FEED_DELAY_SECONDS[n] for n in WHALE_FOOTPRINT_FEEDS} == {0}


@pytest.mark.parametrize("bad", [-1, True, "86400", None, float("nan"), float("inf")])
def test_register_feed_validates_the_delay(bad):
    dm = DataManager(symbols=[SYMBOL], interval_seconds=3600, mode="backtest")
    with pytest.raises(ValueError, match="delay_seconds must be"):
        dm.register_feed("x", _StubFetcher(_fear_greed()), window_seconds=0, delay_seconds=bad)


def test_register_feed_default_delay_is_zero():
    dm = DataManager(symbols=[SYMBOL], interval_seconds=3600, mode="backtest")
    dm.register_feed("x", _StubFetcher(_fear_greed()), window_seconds=0)
    assert dm._aux_feeds["x"].delay_seconds == 0.0


def test_backtester_passes_the_declared_delay():
    from tests.test_feed_dependencies import (
        TEST_LOGGER, BacktestEngine, _RecordingDataManager, _StubStrategy,
    )
    dm = _RecordingDataManager()
    engine = BacktestEngine(data_manager=dm, strategy=_StubStrategy({}), logger=TEST_LOGGER,
                            symbols=["BTCUSD"])

    def factory(symbols, start, end, data_dir, exchange="binance"):
        return object()

    engine.load_data(start_date="2022-01-01", end_date="2022-01-02",
                     extra_feeds={"fear_greed": factory, "funding_rate": factory})
    assert dm._delay == {"fear_greed": 86400, "funding_rate": 0}


# ---------------------------------------------------------------------------
# Review additions: finer fetch, the seal boundary (read from the policy at
# runtime -- no sealed date is written here), live mode
# ---------------------------------------------------------------------------

def test_fetch_finer_than_the_bar():
    """4h candles from 1h rows (CUL-250 finer fetch): every 4h candle of day D
    carries day D-1's value, never day D's."""
    rows = _bars(3600)
    dm = DataManager(symbols=[SYMBOL], interval_seconds=4 * 3600, mode="backtest",
                     fetch_interval_seconds=3600)
    dm.register_feed("fear_greed", _StubFetcher(_fear_greed()), window_seconds=0, agg="last",
                     fill="carry_forward", delay_seconds=86400)
    dm.historical_data[SYMBOL] = rows
    dm.initialize()
    enriched = dm._enrichment_data[SYMBOL]
    candles = enriched[enriched["timestamp"].dt.hour % 4 == 0]
    for _, row in candles.iterrows():
        day_index = (row["timestamp"].normalize() - START).days
        if day_index == 0:
            assert pd.isna(row["fear_greed"]), row["timestamp"]
        else:
            assert float(row["fear_greed"]) == VALUES[min(day_index - 1, len(VALUES) - 1)], row["timestamp"]


def test_the_last_pre_seal_day_never_sees_a_shifted_reading():
    """Bars up to the last pre-seal day; readings on the two days before the
    seal. The last pre-seal day's reading is shifted onto the first sealed
    day, so no pre-seal bar carries it -- the last bar keeps the day before's
    value. Dates come from the policy at runtime."""
    from data.data_manager import _holdout_bounds
    seal_start, _ = _holdout_bounds()
    last_day = seal_start - DAY
    feed = pd.DataFrame({"timestamp": [last_day - DAY, last_day], "fear_greed": [11, 22]})
    ts = pd.date_range(last_day - 2 * DAY, periods=72, freq="h")
    assert ts[-1] < seal_start
    price = pd.DataFrame({"timestamp": ts, "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": 1.0})
    dm = DataManager(symbols=[SYMBOL], interval_seconds=3600, mode="backtest")
    dm.register_feed("fear_greed", _StubFetcher(feed), window_seconds=0, agg="last",
                     fill="carry_forward", delay_seconds=86400)
    dm.historical_data[SYMBOL] = price
    dm.initialize()
    out = dm._attach_aux_columns(SYMBOL, price)
    assert (out["fear_greed"] != 22).all()
    assert float(out.sort_values("timestamp")["fear_greed"].iloc[-1]) == 11


@pytest.mark.parametrize("delay,expected", [(0, "today"), (86400, "yesterday")])
def test_live_mode_honours_the_delay(monkeypatch, delay, expected):
    """_aux_feed_poll_loop picks the latest reading known by now - delay."""
    import data.data_manager as dmod
    today = pd.Timestamp.now(tz="UTC").tz_localize(None).normalize()
    values = {"yesterday": 40, "today": 60}
    feed = pd.DataFrame({"timestamp": [today - DAY, today],
                         "fear_greed": [values["yesterday"], values["today"]]})
    dm = DataManager(symbols=[SYMBOL], interval_seconds=3600, mode="backtest")
    dm.register_feed("fear_greed", _StubFetcher(feed), window_seconds=0, delay_seconds=delay)
    cfg = dm._aux_feeds["fear_greed"]
    dm.running = True
    monkeypatch.setattr(dmod.time, "sleep", lambda s: setattr(dm, "running", False))
    dm._aux_feed_poll_loop("fear_greed", cfg)
    assert cfg.live_value == values[expected]
