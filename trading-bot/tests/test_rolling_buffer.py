"""Unit tests for RollingBuffer."""

import pytest
import pandas as pd
import numpy as np
from strategies.strategy_base import RollingBuffer


@pytest.mark.unit
class TestRollingBufferBasics:
    def test_empty_buffer_has_zero_size(self):
        buf = RollingBuffer(max_size=10)
        assert buf.size == 0

    def test_add_data_increments_size(self):
        buf = RollingBuffer(max_size=10)
        buf.add_data({"close": 100.0})
        assert buf.size == 1
        buf.add_data({"close": 101.0})
        assert buf.size == 2

    def test_maxsize_enforced(self):
        buf = RollingBuffer(max_size=5)
        for i in range(10):
            buf.add_data({"close": float(i)})
        assert buf.size == 5

    def test_oldest_data_dropped_when_full(self):
        buf = RollingBuffer(max_size=3)
        for i in range(5):
            buf.add_data({"value": float(i)})
        df = buf.get_df()
        # Only the last 3 values should remain: 2, 3, 4
        assert list(df["value"]) == [2.0, 3.0, 4.0]

    def test_get_df_returns_dataframe(self):
        buf = RollingBuffer(max_size=10)
        buf.add_data({"close": 100.0, "volume": 50.0})
        df = buf.get_df()
        assert isinstance(df, pd.DataFrame)
        assert "close" in df.columns
        assert "volume" in df.columns

    def test_get_df_on_empty_buffer_returns_empty_dataframe(self):
        buf = RollingBuffer(max_size=10)
        df = buf.get_df()
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0

    def test_getitem_returns_latest_value(self):
        buf = RollingBuffer(max_size=10)
        buf.add_data({"close": 100.0})
        buf.add_data({"close": 200.0})
        assert buf["close"] == pytest.approx(200.0)


@pytest.mark.unit
class TestRollingBufferIndicators:
    def test_registered_indicator_is_computed(self):
        buf = RollingBuffer(max_size=50)
        buf.register_indicator("mean_close", lambda df: df["close"].mean())
        for i in range(10):
            buf.add_data({"close": float(i + 1)})
        # mean of [1..10] = 5.5
        assert buf["mean_close"] == pytest.approx(5.5)

    def test_indicator_recomputed_on_each_add(self):
        buf = RollingBuffer(max_size=50)
        buf.register_indicator("last_close", lambda df: df["close"].iloc[-1])
        buf.add_data({"close": 100.0})
        assert buf["last_close"] == pytest.approx(100.0)
        buf.add_data({"close": 999.0})
        assert buf["last_close"] == pytest.approx(999.0)

    def test_rolling_std_indicator(self):
        buf = RollingBuffer(max_size=50)
        buf.register_indicator("std5", lambda df: df["close"].rolling(5).std())
        closes = [100.0, 101.0, 99.0, 102.0, 100.5, 100.0]
        for c in closes:
            buf.add_data({"close": c})
        # std of last 5 values should be a float, not NaN
        val = buf["std5"]
        assert not pd.isna(val)
        assert val > 0

    def test_multiple_indicators_independent(self):
        buf = RollingBuffer(max_size=50)
        buf.register_indicator("sum_close", lambda df: df["close"].sum())
        buf.register_indicator("max_close", lambda df: df["close"].max())
        for v in [1.0, 3.0, 2.0]:
            buf.add_data({"close": v})
        assert buf["sum_close"] == pytest.approx(6.0)
        assert buf["max_close"] == pytest.approx(3.0)
