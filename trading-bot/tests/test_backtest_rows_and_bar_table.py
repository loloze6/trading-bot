"""Topic 33 (2026-11-20): the backtest rows read once per window, and the one-bar table from typed arrays, give what
the former per-bar code gave: the same candles, and the same table (values, types, column order)."""
import datetime

import numpy as np
import pandas as pd

from data.data_manager import CandleBuilder


def _frame(n=60):
    rng = np.random.default_rng(3)
    ts = pd.date_range("2020-01-01", periods=n, freq="h")
    close = 100 + rng.standard_normal(n).cumsum()
    df = pd.DataFrame({"timestamp": ts, "open": close + 0.1, "high": close + 1, "low": close - 1, "close": close,
                       "volume": rng.random(n) * 10, "extra": rng.random(n)})
    df.loc[7, "volume"] = np.nan
    return df


def _candles(feed, df):
    cb = CandleBuilder(3600)
    for i in range(len(df)):
        feed(cb, df, i)
    return cb


def test_rows_read_once_give_the_same_candles():
    df = _frame()
    old = _candles(lambda cb, d, i: cb.add_row(d.iloc[i], "X"), df)
    cols = {c: df[c].tolist() for c in ("timestamp", "open", "high", "low", "close", "volume") if c in df.columns}
    rows = [CandleBuilder.row_values(lambda k, i=i: cols[k][i], cols.__contains__) for i in range(len(df))]
    new = _candles(lambda cb, d, i: cb.add_values("X", rows[i]), df)
    assert repr(old.completed_candles["X"]) == repr(new.completed_candles["X"])
    assert repr(old.current_candles["X"]) == repr(new.current_candles["X"])


def _old_history(cb, symbol, count):
    candles = cb.completed_candles.get(symbol, [])[-count:]
    return pd.DataFrame([{"timestamp": c.start_time, "open": c.open, "high": c.high, "low": c.low,
                          "close": c.close, "volume": c.volume} for c in candles])


def test_bar_table_is_the_former_one():
    df = _frame()
    cb = _candles(lambda cb, d, i: cb.add_row(d.iloc[i], "X"), df)
    for count in (1, 2, 30):
        new, old = cb.get_candle_history("X", count), _old_history(cb, "X", count)
        assert new.equals(old) and list(new.columns) == list(old.columns) and (new.dtypes == old.dtypes).all()
        assert new.dtypes["timestamp"] == np.dtype("M8[ns]")


def test_a_value_that_is_not_plain_takes_the_former_table():
    cb = _candles(lambda cb, d, i: cb.add_row(d.iloc[i], "X"), _frame(5))
    cb.completed_candles["X"][-1].volume = 3          # an int: the former construction decides the column's type
    new, old = cb.get_candle_history("X", 2), _old_history(cb, "X", 2)
    assert new.equals(old) and (new.dtypes == old.dtypes).all()
    cb.completed_candles["X"][-1].start_time = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
    new, old = cb.get_candle_history("X", 1), _old_history(cb, "X", 1)
    assert new.equals(old) and (new.dtypes == old.dtypes).all()
