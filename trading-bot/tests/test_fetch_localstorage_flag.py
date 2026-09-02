"""
CUL-26 — a pure read must not mutate a tracked cache.

`DataManager.fetch_historical_data(..., localStorage=False)` must suppress the
SAVE side of the read path: a gapped-window read may still reach the (mocked)
remote, but it must NOT write the on-disk cache. The default (localStorage
omitted → True) keeps the historical write-through-on-read behaviour, so the
same gapped read DOES rewrite the cache — the differential proves the new
parameter actually gates persistence, per the reviewed CUL-26 plan.

NO NETWORK: `CcxtFetcher._fetch_remote` is monkeypatched to a fixture-returning
tripwire; a `fired` list records that the mock — never a real socket — is what
served every remote call. `fetch_historical_data` hardcodes the real
`local_data` dir, so the fetcher class is swapped for a data_dir-injecting
subclass to keep every write inside tmp_path.
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


def test_localstorage_false_does_not_write_cache(tmp_path, monkeypatch):
    cache = tmp_path / "kraken_BTCUSD_1h.csv"
    _seed_gapped_cache(cache)
    before = cache.read_bytes()

    fired: list = []
    _install_fetcher(monkeypatch, tmp_path, fired)

    dm = DataManager(symbols=["BTCUSD"], interval_seconds=H, mode="backtest")
    df = dm.fetch_historical_data(
        "BTCUSD",
        T0,
        T0 + pd.Timedelta(7, unit="h"),
        exchange="kraken",
        localStorage=False,
    )

    assert fired, "tripwire: the mocked remote never fired — real network path?"
    assert not df.empty
    assert cache.read_bytes() == before, "localStorage=False rewrote the on-disk cache — the SAVE was not suppressed"


def test_localstorage_default_true_does_write_cache(tmp_path, monkeypatch):
    """Differential control: the default (write-through) path DOES rewrite."""
    cache = tmp_path / "kraken_BTCUSD_1h.csv"
    _seed_gapped_cache(cache)
    before = cache.read_bytes()

    fired: list = []
    _install_fetcher(monkeypatch, tmp_path, fired)

    dm = DataManager(symbols=["BTCUSD"], interval_seconds=H, mode="backtest")
    df = dm.fetch_historical_data(
        "BTCUSD",
        T0,
        T0 + pd.Timedelta(7, unit="h"),
        exchange="kraken",  # localStorage omitted → default True
    )

    assert fired, "tripwire: the mocked remote never fired — real network path?"
    assert not df.empty
    assert cache.read_bytes() != before, "default write-through path did not rewrite the gap-filled cache"
