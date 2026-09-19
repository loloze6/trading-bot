"""
Tests for data/tick_aggregator.py (E-008 S2).

All trade data here is SYNTHETIC and hand-constructed — no file under
local_data/holdout_sealed/ is read, listed, or referenced anywhere in this
module.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.tick_aggregator import (  # noqa: E402
    OHLCV_COLUMNS,
    SUPPORTED_BUCKET_MINUTES,
    aggregate_trades_to_ohlcv,
    bucket_seconds_from_minutes,
    load_kraken_trades_csv,
)

TOL = 1e-9

# 2021-01-01 00:00:00 UTC, a realistic Kraken-style epoch base.
T0 = 1609459200


def _trades(rows):
    """rows: list of (offset_seconds, price, volume) -> raw Kraken-schema df."""
    return pd.DataFrame(
        {
            "price": [r[1] for r in rows],
            "volume": [r[2] for r in rows],
            "time": [T0 + r[0] for r in rows],
        }
    )


# ---------------------------------------------------------------------------
# Correctness: hand-computed expected OHLCV across 3 hourly buckets
# ---------------------------------------------------------------------------

def test_aggregate_three_hourly_buckets_matches_hand_computed_ohlcv():
    trades = _trades(
        [
            # Bucket 0: [T0, T0+3600)
            (0, 10.0, 1.0),
            (200, 12.0, 2.0),
            (3000, 9.0, 0.5),
            # Bucket 1: [T0+3600, T0+7200)
            (3700, 20.0, 1.0),
            (7199, 25.0, 1.0),
            # Bucket 2: [T0+7200, T0+10800) — single trade
            (8000, 5.0, 10.0),
        ]
    )

    got = aggregate_trades_to_ohlcv(trades, bucket_seconds=3600)

    assert list(got.columns) == OHLCV_COLUMNS
    assert len(got) == 3

    expected = pd.DataFrame(
        {
            "timestamp": [
                pd.Timestamp(T0, unit="s"),
                pd.Timestamp(T0 + 3600, unit="s"),
                pd.Timestamp(T0 + 7200, unit="s"),
            ],
            "open": [10.0, 20.0, 5.0],
            "high": [12.0, 25.0, 5.0],
            "low": [9.0, 20.0, 5.0],
            "close": [9.0, 25.0, 5.0],
            "volume": [3.5, 2.0, 10.0],
        }
    )

    pd.testing.assert_frame_equal(
        got.reset_index(drop=True), expected, check_exact=False, atol=TOL
    )


def test_aggregate_accepts_already_normalized_timestamp_column():
    """A frame that already carries 'timestamp' (not raw 'time') is used
    as-is — the auto-normalize branch only fires when 'timestamp' is
    absent."""
    trades = pd.DataFrame(
        {
            "timestamp": [
                pd.Timestamp(T0, unit="s"),
                pd.Timestamp(T0 + 10, unit="s"),
            ],
            "price": [100.0, 110.0],
            "volume": [1.0, 2.0],
        }
    )
    got = aggregate_trades_to_ohlcv(trades, bucket_seconds=3600)
    assert len(got) == 1
    row = got.iloc[0]
    assert row["open"] == pytest.approx(100.0)
    assert row["close"] == pytest.approx(110.0)
    assert row["high"] == pytest.approx(110.0)
    assert row["low"] == pytest.approx(100.0)
    assert row["volume"] == pytest.approx(3.0)


def test_empty_buckets_are_not_emitted():
    """A gap between two trades leaves the intervening bucket(s) absent from
    the output — no forward-fill happens inside this function."""
    trades = _trades(
        [
            (0, 10.0, 1.0),          # bucket 0
            (5 * 3600 + 1, 99.0, 1.0),  # bucket 5 -- buckets 1-4 have no trades
        ]
    )
    got = aggregate_trades_to_ohlcv(trades, bucket_seconds=3600)
    assert len(got) == 2
    assert list(got["timestamp"]) == [
        pd.Timestamp(T0, unit="s"),
        pd.Timestamp(T0 + 5 * 3600, unit="s"),
    ]


def test_bucket_boundary_is_epoch_aligned_not_data_relative():
    """A trade stream starting mid-bucket must still align to the fixed
    epoch grid (matching CandleBuilder._align), not to its own first
    timestamp (pandas resample's default 'start_day' origin behaviour)."""
    offset_into_bucket = 1234  # arbitrary, non-zero offset from a bucket edge
    trades = _trades([(offset_into_bucket, 42.0, 1.0)])
    got = aggregate_trades_to_ohlcv(trades, bucket_seconds=3600)
    assert len(got) == 1
    expected_bucket_start = (T0 + offset_into_bucket) // 3600 * 3600
    assert got.iloc[0]["timestamp"] == pd.Timestamp(expected_bucket_start, unit="s")


def test_out_of_order_trades_still_resolve_open_close_correctly():
    """Trades arriving out of chronological order within a bucket must not
    corrupt first/last (open/close) — the function sorts before bucketing."""
    trades = pd.DataFrame(
        {
            "price": [30.0, 10.0, 20.0],   # out of order: mid, first, last
            "volume": [1.0, 1.0, 1.0],
            "time": [T0 + 500, T0 + 100, T0 + 900],
        }
    )
    got = aggregate_trades_to_ohlcv(trades, bucket_seconds=3600)
    assert len(got) == 1
    row = got.iloc[0]
    assert row["open"] == pytest.approx(10.0)   # earliest timestamp (t=100)
    assert row["close"] == pytest.approx(20.0)  # latest timestamp (t=900)
    assert row["high"] == pytest.approx(30.0)
    assert row["low"] == pytest.approx(10.0)


# ---------------------------------------------------------------------------
# Minute-based bucket widths (Kraken_batch/master_q4 suffix convention)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("minutes,seconds", sorted(SUPPORTED_BUCKET_MINUTES.items()))
def test_bucket_seconds_from_minutes_matches_convention(minutes, seconds):
    assert bucket_seconds_from_minutes(minutes) == seconds


def test_bucket_seconds_from_minutes_rejects_unmapped_value():
    with pytest.raises(ValueError, match="Unsupported bucket width"):
        bucket_seconds_from_minutes(30)


def test_aggregate_at_4h_bucket_width_via_minute_helper():
    seconds = bucket_seconds_from_minutes(240)  # 4h
    trades = _trades([(0, 1.0, 1.0), (14400, 2.0, 1.0), (14401, 3.0, 1.0)])
    got = aggregate_trades_to_ohlcv(trades, bucket_seconds=seconds)
    # 14400s = exactly 4h -> falls in the SECOND bucket; 14401s also second.
    assert len(got) == 2
    assert got.iloc[0]["close"] == pytest.approx(1.0)
    assert got.iloc[1]["open"] == pytest.approx(2.0)
    assert got.iloc[1]["close"] == pytest.approx(3.0)


# ---------------------------------------------------------------------------
# Degenerate-input guards
# ---------------------------------------------------------------------------

def test_rejects_non_positive_bucket_seconds():
    trades = _trades([(0, 1.0, 1.0)])
    with pytest.raises(ValueError, match="bucket_seconds must be positive"):
        aggregate_trades_to_ohlcv(trades, bucket_seconds=0)
    with pytest.raises(ValueError, match="bucket_seconds must be positive"):
        aggregate_trades_to_ohlcv(trades, bucket_seconds=-3600)


def test_empty_trades_returns_empty_frame_with_correct_columns():
    empty = pd.DataFrame(columns=["price", "volume", "time"])
    got = aggregate_trades_to_ohlcv(empty, bucket_seconds=3600)
    assert got.empty
    assert list(got.columns) == OHLCV_COLUMNS


def test_missing_required_column_raises():
    bad = pd.DataFrame({"price": [1.0], "volume": [1.0]})  # no 'time'/'timestamp'
    with pytest.raises(ValueError, match="missing required column"):
        aggregate_trades_to_ohlcv(bad, bucket_seconds=3600)


def test_tz_aware_timestamp_is_rejected():
    trades = pd.DataFrame(
        {
            "timestamp": pd.to_datetime([T0], unit="s", utc=True),
            "price": [1.0],
            "volume": [1.0],
        }
    )
    with pytest.raises(ValueError, match="tz-aware"):
        aggregate_trades_to_ohlcv(trades, bucket_seconds=3600)


# ---------------------------------------------------------------------------
# CSV loader — synthetic file only, never the real archive
# ---------------------------------------------------------------------------

def test_load_kraken_trades_csv_round_trip(tmp_path):
    path = tmp_path / "synthetic_trades.csv"
    # Headerless: price, volume, time -- hand-built, three trades.
    path.write_text(
        f"{10.5},{0.25},{T0}\n"
        f"{11.0},{1.5},{T0 + 30}\n"
        f"{9.75},{0.1},{T0 + 90}\n"
    )

    df = load_kraken_trades_csv(str(path))

    assert list(df.columns) == ["price", "volume", "timestamp"]
    assert len(df) == 3
    assert df["timestamp"].iloc[0] == pd.Timestamp(T0, unit="s")
    assert df["price"].iloc[1] == pytest.approx(11.0)

    ohlcv = aggregate_trades_to_ohlcv(df, bucket_seconds=3600)
    assert len(ohlcv) == 1
    row = ohlcv.iloc[0]
    assert row["open"] == pytest.approx(10.5)
    assert row["close"] == pytest.approx(9.75)
    assert row["high"] == pytest.approx(11.0)
    assert row["low"] == pytest.approx(9.75)
    assert row["volume"] == pytest.approx(1.85)
