"""
CUL-355: per-feed `fill` -- what a bar with no new aux reading gets.

Since 751d403e (CUL-250) every feed is resampled into bar-width buckets before
the backward as-of join, and an empty bucket became a NaN row that the join
then picked: on 1h bars an 8h funding feed was NaN on 7 bars in 8. The old
carry-forward test used ONE reading, where no bucket is empty, so it passed.

These tests use realistic multi-reading feeds on 1h, 4h and 1d bars:
  * 'carry_forward' (funding_rate, fear_greed): every bar after the first
    reading carries the latest reading made before the bar closes, with no age
    limit -- computed independently from the raw readings;
  * 'none' (whale features): empty buckets stay NaN, exactly as before;
  * the registry declares agg and fill for every feed, and the backtester
    passes them;
  * the existing on/off funding and fear & greed components give the same
    output with and without the fill (they read only the print bars).
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
    FEED_AGG, FEED_FILL, FEED_WINDOW_SECONDS, WHALE_FOOTPRINT_FEEDS,
)
from strategies.strategy_components import (  # noqa: E402
    FearGreedContrarianComponent, FundingRateMeanReversionComponent,
)

SYMBOL = "BTCUSDT"
PRICE_START = pd.Timestamp("2021-03-01")
FEED_START = pd.Timestamp("2021-03-02")
N_DAYS = 8          # bars run 3+ days past the last reading: "forever" is exercised


class _StubFetcher:
    exchange_id = "binance"

    def __init__(self, df):
        self._df = df

    def get_data(self, symbol=None):
        return self._df

    def cache_key(self, symbol):
        return "stub"


def _funding() -> pd.DataFrame:    # 8h prints for 3 days, then nothing
    ts = pd.date_range(FEED_START, periods=9, freq="8h")
    return pd.DataFrame({"timestamp": ts, "funding_rate": [0.0001 * (i + 1) for i in range(9)]})


def _fear_greed() -> pd.DataFrame:  # daily at 00:00 for 3 days
    ts = pd.date_range(FEED_START, periods=3, freq="D")
    return pd.DataFrame({"timestamp": ts, "fear_greed": [20, 40, 60]})


def _enriched(interval_seconds: int, fill: str) -> pd.DataFrame:
    n = N_DAYS * 86400 // interval_seconds
    ts = pd.date_range(PRICE_START, periods=n, freq=f"{interval_seconds}s")
    price = pd.DataFrame({"timestamp": ts, "open": 100.0, "high": 100.0, "low": 100.0,
                          "close": 100.0, "volume": 1.0})
    dm = DataManager(symbols=[SYMBOL], interval_seconds=interval_seconds, mode="backtest")
    dm.register_feed("funding_rate", _StubFetcher(_funding()), window_seconds=0, agg="last", fill=fill)
    dm.register_feed("fear_greed", _StubFetcher(_fear_greed()), window_seconds=0, agg="last", fill=fill)
    dm.historical_data[SYMBOL] = price
    dm.initialize()
    return dm._attach_aux_columns(SYMBOL, price).sort_values("timestamp").reset_index(drop=True)


def _latest_reading_before_close(readings: pd.DataFrame, col: str, bar_start, interval_seconds):
    """Independent expectation: the last raw reading stamped before the bar's
    close (bar_start + interval), or NaN when there is none yet."""
    bar_end = bar_start + pd.Timedelta(seconds=interval_seconds)
    seen = readings[readings["timestamp"] < bar_end]
    return float(seen[col].iloc[-1]) if len(seen) else float("nan")


INTERVALS = [3600, 4 * 3600, 86400]


@pytest.mark.parametrize("interval_seconds", INTERVALS, ids=["1h", "4h", "1d"])
def test_carry_forward_gives_every_bar_the_latest_reading(interval_seconds):
    out = _enriched(interval_seconds, "carry_forward")
    for col, readings in (("funding_rate", _funding()), ("fear_greed", _fear_greed())):
        for _, row in out.iterrows():
            expected = _latest_reading_before_close(readings, col, row["timestamp"], interval_seconds)
            got = row[col]
            if math.isnan(expected):
                assert math.isnan(got), (col, row["timestamp"], got)
            else:
                assert got == pytest.approx(expected), (col, row["timestamp"], got, expected)
        after = out[out["timestamp"] >= FEED_START]
        assert after[col].notna().all(), col


@pytest.mark.parametrize("interval_seconds", INTERVALS, ids=["1h", "4h", "1d"])
def test_carry_forward_has_no_age_limit(interval_seconds):
    """Two days after the last reading the last value is still there
    (operator 2026-09-30: reused forever)."""
    out = _enriched(interval_seconds, "carry_forward")
    last_bar = out.iloc[-1]
    assert last_bar["timestamp"] - _funding()["timestamp"].max() > pd.Timedelta(days=2)
    assert last_bar["funding_rate"] == pytest.approx(_funding()["funding_rate"].iloc[-1])
    assert last_bar["fear_greed"] == _fear_greed()["fear_greed"].iloc[-1]


@pytest.mark.parametrize("interval_seconds", INTERVALS, ids=["1h", "4h", "1d"])
def test_nothing_before_the_first_reading(interval_seconds):
    out = _enriched(interval_seconds, "carry_forward")
    before = out[out["timestamp"] < FEED_START]
    assert before["funding_rate"].isna().all() and before["fear_greed"].isna().all()


def test_fill_none_keeps_empty_bars_empty():
    """Event-feed behaviour, unchanged: between the first and the last reading,
    on 1h bars the 8h feed is set only on the print bars (the measured 7-in-8
    NaN share). After the LAST reading the as-of join already carried the last
    value before CUL-355 and still does -- only the in-between gaps differ."""
    out = _enriched(3600, "none")
    between = out[(out["timestamp"] >= FEED_START) & (out["timestamp"] < _funding()["timestamp"].max())]
    on_print = between["timestamp"].dt.hour % 8 == 0
    assert between.loc[on_print, "funding_rate"].notna().all()
    assert between.loc[~on_print, "funding_rate"].isna().all()


@pytest.mark.parametrize("interval_seconds", INTERVALS, ids=["1h", "4h", "1d"])
def test_fill_changes_only_the_bars_that_were_empty(interval_seconds):
    none = _enriched(interval_seconds, "none")
    carry = _enriched(interval_seconds, "carry_forward")
    for col in ("funding_rate", "fear_greed"):
        was_set = none[col].notna()
        assert (carry.loc[was_set, col] == none.loc[was_set, col]).all(), col


@pytest.mark.parametrize("interval_seconds", INTERVALS, ids=["1h", "4h", "1d"])
def test_the_existing_on_off_components_are_unchanged(interval_seconds):
    """FundingRateMeanReversion reads only settlement bars (hour % 8 == 0) and
    FearGreedContrarian only the 00:00 bar -- the bars a reading lands on -- so
    their outputs are identical with and without the fill."""
    none = _enriched(interval_seconds, "none")
    carry = _enriched(interval_seconds, "carry_forward")
    for make in (lambda: FundingRateMeanReversionComponent(parameters={"threshold": 0.0}),
                 lambda: FearGreedContrarianComponent(parameters={"fear_threshold": 30.0,
                                                                  "greed_threshold": 50.0})):
        a, b = make(), make()
        for i in range(2, len(none) + 1):
            a.update(none.iloc[:i])
            b.update(carry.iloc[:i])
            va, vb = a.raw_value(), b.raw_value()
            assert (math.isnan(va) and math.isnan(vb)) or va == vb, (type(a).__name__, i, va, vb)


# ---------------------------------------------------------------------------
# Declarations and wiring
# ---------------------------------------------------------------------------

def test_every_feed_declares_agg_and_fill():
    assert set(FEED_AGG) == set(FEED_WINDOW_SECONDS) == set(FEED_FILL)
    assert FEED_FILL["funding_rate"] == FEED_FILL["fear_greed"] == "carry_forward"
    assert {FEED_FILL[n] for n in WHALE_FOOTPRINT_FEEDS} == {"none"}
    # agg was hard-coded 'last' for every feed before CUL-355: unchanged
    assert set(FEED_AGG.values()) == {"last"}


def test_register_feed_default_and_validation():
    dm = DataManager(symbols=[SYMBOL], interval_seconds=3600, mode="backtest")
    dm.register_feed("x", _StubFetcher(_funding()), window_seconds=0)
    assert dm._aux_feeds["x"].fill == "none"
    with pytest.raises(ValueError, match="fill must be"):
        dm.register_feed("y", _StubFetcher(_funding()), window_seconds=0, fill="ffill")


def test_backtester_passes_the_declared_agg_and_fill():
    from tests.test_feed_dependencies import (  # the existing recording DataManager stub
        TEST_LOGGER, BacktestEngine, _RecordingDataManager, _StubStrategy,
    )
    dm = _RecordingDataManager()
    engine = BacktestEngine(data_manager=dm, strategy=_StubStrategy({}), logger=TEST_LOGGER,
                            symbols=["BTCUSD"])

    def factory(symbols, start, end, data_dir, exchange="binance"):
        return object()

    engine.load_data(start_date="2022-01-01", end_date="2022-01-02",
                     extra_feeds={"fear_greed": factory, "funding_rate": factory})
    assert dm._agg_fill == {"fear_greed": ("last", "carry_forward"),
                            "funding_rate": ("last", "carry_forward")}


# ---------------------------------------------------------------------------
# Red-team review additions: gaps inside the feed, finer fetch, jitter,
# missing prints, and what the existing components do at a gap
# ---------------------------------------------------------------------------

def _enrichment(feed: pd.DataFrame, col: str, fill: str, interval_seconds: int,
                fetch_interval_seconds=None, days: int = 10) -> pd.DataFrame:
    step = fetch_interval_seconds or interval_seconds
    ts = pd.date_range(PRICE_START, periods=days * 86400 // step, freq=f"{step}s")
    price = pd.DataFrame({"timestamp": ts, "open": 100.0, "high": 100.0, "low": 100.0,
                          "close": 100.0, "volume": 1.0})
    kw = {"fetch_interval_seconds": fetch_interval_seconds} if fetch_interval_seconds else {}
    dm = DataManager(symbols=[SYMBOL], interval_seconds=interval_seconds, mode="backtest", **kw)
    dm.register_feed(col, _StubFetcher(feed), window_seconds=0, agg="last", fill=fill)
    dm.historical_data[SYMBOL] = price
    dm.initialize()
    return dm._enrichment_data[SYMBOL].sort_values("timestamp").reset_index(drop=True)


def _assert_latest_before_close(enriched, feed, col, interval_seconds):
    """At every candle start (on the interval grid), the value is the latest
    reading made before that candle closes; NaN before the first reading."""
    grid = enriched[(enriched["timestamp"] - PRICE_START).dt.total_seconds() % interval_seconds == 0]
    assert len(grid)
    for _, row in grid.iterrows():
        expected = _latest_reading_before_close(feed, col, row["timestamp"], interval_seconds)
        if math.isnan(expected):
            assert pd.isna(row[col]), row["timestamp"]
        else:
            assert float(row[col]) == pytest.approx(expected), (row["timestamp"], row[col], expected)


def _funding_with_gap() -> pd.DataFrame:
    """8h prints with a 3-day hole in the middle (a missing stretch of the
    feed, not its end)."""
    ts = list(pd.date_range(FEED_START, periods=6, freq="8h")) + \
        list(pd.date_range(FEED_START + pd.Timedelta(days=5), periods=6, freq="8h"))
    return pd.DataFrame({"timestamp": ts, "funding_rate": [0.0001 * (i + 1) for i in range(12)]})


@pytest.mark.parametrize("interval_seconds", INTERVALS, ids=["1h", "4h", "1d"])
def test_a_multi_day_gap_inside_the_feed_carries_the_last_value(interval_seconds):
    """No age limit inside the feed either: through a 3-day hole every bar keeps
    the last print before the hole (an ffill(limit=...) would leave NaN)."""
    feed = _funding_with_gap()
    enriched = _enrichment(feed, "funding_rate", "carry_forward", interval_seconds)
    _assert_latest_before_close(enriched, feed, "funding_rate", interval_seconds)
    hole = enriched[(enriched["timestamp"] >= FEED_START + pd.Timedelta(days=2, hours=8))
                    & (enriched["timestamp"] < FEED_START + pd.Timedelta(days=5))]
    assert len(hole) and np.allclose(hole["funding_rate"].to_numpy(dtype=float), 0.0006)


def test_fetch_finer_than_the_bar():
    """CUL-250 finer fetch: 4h candles from 1h rows; every candle carries the
    latest print before it closes, including candles with no print."""
    feed = _funding()
    enriched = _enrichment(feed, "funding_rate", "carry_forward", 4 * 3600, fetch_interval_seconds=3600)
    _assert_latest_before_close(enriched, feed, "funding_rate", 4 * 3600)


@pytest.mark.parametrize("jitter", ["3ms", "17min"])
def test_readings_off_the_grid(jitter):
    feed = _funding()
    feed["timestamp"] = feed["timestamp"] + pd.Timedelta(jitter)
    for interval_seconds in INTERVALS:
        enriched = _enrichment(feed, "funding_rate", "carry_forward", interval_seconds)
        _assert_latest_before_close(enriched, feed, "funding_rate", interval_seconds)


def test_a_nan_print_is_skipped_and_the_previous_value_carried():
    """The resample's 'last' skips a NaN reading, so the bar keeps the
    previous print (the value was never measured, the older one still holds)."""
    feed = _funding()
    feed.loc[3, "funding_rate"] = np.nan                       # the 2021-03-03 00:00 print
    enriched = _enrichment(feed, "funding_rate", "carry_forward", 3600)
    at = enriched[enriched["timestamp"] == pd.Timestamp("2021-03-03 00:00")]
    assert at["funding_rate"].iloc[0] == pytest.approx(0.0003)


def test_declared_change_the_on_off_funding_component_at_a_missing_settlement():
    """DECLARED CHANGE (CUL-355, operator: reuse forever). At a settlement bar
    whose print is missing, FundingRateMeanReversion used to read NaN and
    abstain (CUL-273 propagate_invalid); with carry_forward it reads the last
    print and fires on it. The real Binance cache has 2 such settlements
    before the seal (2022-06, 2023-05); fear & greed has 2 gaps (2018-04,
    2024-10) with the same effect for FearGreedContrarian."""
    feed = _funding().drop(index=3).reset_index(drop=True)     # 2021-03-03 00:00 missing
    bars = {}
    for fill in ("none", "carry_forward"):
        e = _enrichment(feed, "funding_rate", fill, 3600)
        bars[fill] = e.assign(close=100.0)
    t = pd.Timestamp("2021-03-03 00:00")
    out = {}
    for fill, df in bars.items():
        comp = FundingRateMeanReversionComponent(parameters={"threshold": 0.0})
        comp.update(df[df["timestamp"] <= t])
        out[fill] = comp.raw_value()
    assert math.isnan(out["none"])
    assert out["carry_forward"] == -10.0                       # -sign(0.0003) x 10
