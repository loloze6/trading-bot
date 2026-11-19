"""
CUL-26, then the local-only backtest read (operator 2026-11-18, data/coverage.py): a backtest read never mutates a
tracked cache and never calls the exchange. A gapped cache inside its coverage is read as it is (the gap included);
days outside the coverage are refused (DataNotFetched), still without a call or a write. (CUL-26's localStorage flag,
which only stopped a gap-fill being written back, is gone with the gap-fill.)

NO NETWORK: `CcxtFetcher._fetch_remote` is monkeypatched to a tripwire that records any call; `fetch_historical_data`
hardcodes the real `local_data` dir, so the fetcher class is swapped for a data_dir-injecting subclass to keep every
read inside tmp_path.
"""
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # trading-bot/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import data.data_manager as dm_module  # noqa: E402
from data.data_manager import DataManager  # noqa: E402
from data.fetchers.ccxt_fetcher import CcxtFetcher  # noqa: E402

H = 3600
T0 = pd.Timestamp("2020-01-01 00:00:00")  # far from any seal
_CLOSE_MS = H * 1000 - 1


def _bars(timestamps) -> pd.DataFrame:
    """A Binance-schema OHLCV frame over the given hourly timestamps."""
    ts = pd.DatetimeIndex(timestamps)
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": 1.0,
            "high": 1.0,
            "low": 1.0,
            "close": 1.0,
            "volume": 1.0,
            "close_time": ts + pd.Timedelta(_CLOSE_MS, unit="ms"),
            "quote_asset_volume": 1.0,
            "number_of_trades": 1,
            "taker_buy_base_asset_volume": float("nan"),
            "taker_buy_quote_asset_volume": float("nan"),
            "ignore": 0,
        }
    )


def _seed_gapped_cache(path: Path) -> None:
    """A cache with an internal gap: hours 0,1,2 then 5,6,7 (3,4 missing)."""
    kept = [T0 + pd.Timedelta(i, unit="h") for i in (0, 1, 2, 5, 6, 7)]
    _bars(kept).to_csv(path, index=False)


def _install_fetcher(monkeypatch, tmp_path, fired):
    """Point fetch_historical_data at tmp_path and mock the remote fetch."""

    class _DirInjectingFetcher(CcxtFetcher):
        def __init__(self, *args, **kwargs):
            kwargs["data_dir"] = str(tmp_path)
            super().__init__(*args, **kwargs)

    def _remote(self, symbol, start, end):
        # Serve the hourly bars in [start .. end] (start is already on the grid);
        # this fills any internal gap so _assert_no_new_gap accepts the merge.
        rng = pd.date_range(start=pd.Timestamp(start), end=pd.Timestamp(end), freq="h")
        fired.append((symbol, str(start), str(end)))
        return _bars(rng)

    monkeypatch.setattr(dm_module, "HistoricalDataFetcher", _DirInjectingFetcher)
    monkeypatch.setattr(CcxtFetcher, "_fetch_remote", _remote)


def test_the_backtest_read_never_fetches_nor_writes(tmp_path, monkeypatch):
    from data import coverage
    cache = tmp_path / "kraken_BTCUSD_1h.csv"
    _seed_gapped_cache(cache)
    coverage.record(tmp_path, cache.name, None, "2020-01-01", "test")
    before = cache.read_bytes()
    fired: list = []
    _install_fetcher(monkeypatch, tmp_path, fired)
    dm = DataManager(symbols=["BTCUSD"], interval_seconds=H, mode="backtest")
    df = dm.fetch_historical_data("BTCUSD", T0, T0 + pd.Timedelta(7, unit="h"), exchange="kraken")
    assert fired == [], "a backtest read called the exchange"
    assert len(df) == 6, "the gapped cache is read as it is"
    assert cache.read_bytes() == before, "a backtest read rewrote the on-disk cache"


def test_the_backtest_read_refuses_days_not_fetched(tmp_path, monkeypatch):
    import pytest
    from data.coverage import DataNotFetched
    cache = tmp_path / "kraken_BTCUSD_1h.csv"
    _seed_gapped_cache(cache)                                  # no coverage recorded: these days were never fetched
    before = cache.read_bytes()
    fired: list = []
    _install_fetcher(monkeypatch, tmp_path, fired)
    dm = DataManager(symbols=["BTCUSD"], interval_seconds=H, mode="backtest")
    with pytest.raises(DataNotFetched):
        dm.fetch_historical_data("BTCUSD", T0, T0 + pd.Timedelta(7, unit="h"), exchange="kraken")
    assert fired == [] and cache.read_bytes() == before
