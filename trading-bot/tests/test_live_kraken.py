"""live/kraken.py on recorded-shape replies (no network): paging, the forming candle dropped, names, account."""
import datetime
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from live import kraken  # noqa: E402

H = 3_600_000


class FakeCandles:
    """Hourly candles from t0, 5000 of them; answers at most `limit` per call, the forming one included."""

    def __init__(self, t0_ms, n=5000):
        self.rows = [[t0_ms + i * H, 1.0 + i, 2.0 + i, 0.5 + i, 1.5 + i, 10.0] for i in range(n)]
        self.calls = 0

    def fetch_ohlcv(self, symbol, timeframe, since=None, limit=2000):
        self.calls += 1
        lo = since - since % H
        return [r for r in self.rows if r[0] >= lo][:limit]


def test_pages_through_the_2000_limit_and_drops_the_forming_candle():
    t0 = pd.Timestamp("2030-01-01")   # synthetic candles; any date
    ex = FakeCandles(int(t0.value // 1_000_000))
    now = t0 + datetime.timedelta(hours=4500, minutes=17)   # candle 4500 is forming
    df = kraken.fetch_completed_candles(ex, "BTCUSD", 3600, t0, now)
    assert len(df) == 4500 and ex.calls == 3
    assert df["timestamp"].iloc[-1] == t0 + datetime.timedelta(hours=4499)
    assert df["timestamp"].is_monotonic_increasing and df["timestamp"].is_unique
    assert list(df.columns) == kraken.COLUMNS


def test_a_candle_ending_exactly_now_is_complete():
    t0 = pd.Timestamp("2030-01-01")   # synthetic candles; any date
    ex = FakeCandles(int(t0.value // 1_000_000), n=10)
    df = kraken.fetch_completed_candles(ex, "BTCUSD", 3600, t0, t0 + datetime.timedelta(hours=3))
    assert len(df) == 3


def test_symbol_names():
    assert kraken.ccxt_symbol("BTCUSD") == "BTC/USD:USD"
    assert kraken.ccxt_symbol("ETHUSD") == "ETH/USD:USD"
    for bad in ("BTCUSDT", "USD", "BTC"):
        with pytest.raises(ValueError):
            kraken.ccxt_symbol(bad)


class FakeAccount:
    markets = {"BTC/USD:USD": {"id": "PF_XBTUSD", "linear": True}}

    def __init__(self, positions):
        self.positions = positions

    def load_markets(self):
        return self.markets

    def privateGetAccounts(self):
        return {"accounts": {"flex": {"portfolioValue": "1234.5", "balanceValue": "1200"}}}

    def privateGetOpenpositions(self):
        return {"openPositions": self.positions}


def test_account_value_and_signed_position():
    ex = FakeAccount([{"side": "short", "symbol": "PF_XBTUSD", "size": "0.0123"},
                      {"side": "long", "symbol": "PF_ETHUSD", "size": "2"}])
    assert kraken.account_snapshot(ex, "BTCUSD") == {"value": 1234.5, "position": -0.0123}
    assert kraken.account_snapshot(FakeAccount([]), "BTCUSD") == {"value": 1234.5, "position": 0.0}


def test_target_switch():
    real = kraken.make_exchange("real", with_keys=False)
    assert "futures.kraken.com" in real.urls["api"]["public"]
    test = kraken.make_exchange("test", test_host="example.test", with_keys=False)
    assert all("example.test" in v for v in test.urls["api"].values())
    with pytest.raises(ValueError):
        kraken.make_exchange("test", with_keys=False)
    with pytest.raises(ValueError):
        kraken.make_exchange("demo", with_keys=False)
