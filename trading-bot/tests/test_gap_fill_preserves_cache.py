"""
A gap-fill (a data tool's fetch of the periods missing from a file) and the backtest's local-only read
(CUL-230, 2026-09-02; restated 2026-11-19).

The backtest never calls the exchange (DataManager.fetch_historical_data, operator 2026-11-18): it reads the file
inside its coverage, interior holes included, so the CUL-230 crash (a failed top-up of an interior hole throwing away a
cache that covered the window) cannot happen there. The fallback that once tolerated a failed top-up on that path
(`tolerate_fill_failure`) had no caller left and was removed (2026-11-19). A data tool's fetch that fails fails loud.

Fixtures only — no live calls. `_fetch_remote` is stubbed per test.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import data.fetchers.ccxt_fetcher as ccxt_fetcher  # noqa: E402
from data.data_manager import DataManager, SealedDataError  # noqa: E402
from data.fetchers.base_fetcher import BaseFetcher  # noqa: E402

HOUR = 3600


def _bars(start: str, periods: int) -> pd.DataFrame:
    """OHLCV-shaped frame; only `timestamp` drives gap detection."""
    ts = pd.date_range(start=start, periods=periods, freq="1h")
    return pd.DataFrame({
        "timestamp": ts,
        "open": 1.0, "high": 1.0, "low": 1.0, "close": 1.0, "volume": 1.0,
    })


def _cache_with_interior_gap() -> pd.DataFrame:
    """44 hourly bars spanning the FULL 2020-06-01..2020-06-02 window (reaches
    both boundaries: 06-01 00:00 and 06-02 23:00) with one 5h interior hole
    (drops 10:00..13:00 on 06-01). This is the CUL-230 shape."""
    return pd.concat(
        [_bars("2020-06-01 00:00", 10), _bars("2020-06-01 14:00", 34)],
        ignore_index=True,
    )


class _CacheFetcher(BaseFetcher):
    """Concrete BaseFetcher whose `_fetch_remote` is injected per test."""

    def __init__(self, tmp_dir, start, end, remote):
        self._remote = remote
        super().__init__(
            start_date=start, end_date=end, symbols=["BTCUSD"],
            interval_seconds=HOUR, localStorage=True, data_dir=str(tmp_dir),
        )

    def _fetch_remote(self, symbol, start, end):
        return self._remote(symbol, start, end)

    def cache_key(self, symbol):
        return symbol


def _write_cache(tmp_dir, symbol, df):
    df.to_csv(Path(tmp_dir) / f"{symbol}.csv", index=False)


def _raise(exc):
    def _remote(symbol, start, end):
        raise exc
    return _remote


# ---------------------------------------------------------------------------
# A failed fetch fails loud
# ---------------------------------------------------------------------------

def test_no_cached_rows_failure_still_surfaces(tmp_path):
    # no cache file on disk -> existing is empty -> nothing to fall back to
    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02",
                      _raise(RuntimeError("simulated network failure")))
    with pytest.raises(RuntimeError):
        f.get_data("BTCUSD")


def test_seal_guard_from_fetch_still_propagates(tmp_path):
    """A seal guard fails loud even when the cache covers the window."""
    _write_cache(tmp_path, "BTCUSD", _cache_with_interior_gap())
    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02",
                      _raise(SealedDataError("holdout window touched")))
    with pytest.raises(SealedDataError):
        f.get_data("BTCUSD")


def test_a_failed_fill_reraises_even_when_the_cache_covers_the_window(tmp_path):
    """A data tool's failed fetch re-raises; the cached rows are not returned in its place."""
    _write_cache(tmp_path, "BTCUSD", _cache_with_interior_gap())
    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02",
                      _raise(RuntimeError("simulated network failure")))
    with pytest.raises(RuntimeError):
        f.get_data("BTCUSD")


# ---------------------------------------------------------------------------
# A successful fill still fills and writes (no regression on the happy path)
# ---------------------------------------------------------------------------

def test_successful_fill_still_merges(tmp_path):
    _write_cache(tmp_path, "BTCUSD", _cache_with_interior_gap())

    def remote(symbol, start, end):
        return _bars("2020-06-01 10:00", 4)           # exactly the 5h hole's bars

    f = _CacheFetcher(tmp_path, "2020-06-01", "2020-06-02", remote)
    got = f.get_data("BTCUSD")

    assert len(got) == 48                             # 44 cached + 4 filled
    assert pd.Timestamp("2020-06-01 11:00") in set(got["timestamp"])
    assert len(pd.read_csv(Path(tmp_path) / "BTCUSD.csv")) == 48


# ---------------------------------------------------------------------------
# End-to-end: the backtest's local-only read keeps an interior-gap cache (the CUL-230 shape)
# ---------------------------------------------------------------------------

def test_the_local_only_read_returns_the_window_with_its_interior_hole(tmp_path, monkeypatch):
    """The literal crash path, under the local-only backtest read (2026-11-18): an interior-gap cache inside its
    coverage returns the full cached window through DataManager.fetch_historical_data, with no exchange call at all
    (the remote raises if it is ever called), not the empty frame launcher.py turns into 'No historical data'."""
    # CcxtFetcher (exchange=binance) resolves the cache slot to "<symbol>_<tf>".
    _write_cache(tmp_path, "BTCUSD_1h", _cache_with_interior_gap())
    from data import coverage
    coverage.record(tmp_path, "BTCUSD_1h.csv", None, "2020-06-02", "test")

    orig_init = ccxt_fetcher.CcxtFetcher.__init__

    def patched_init(self, *args, **kwargs):
        kwargs["data_dir"] = str(tmp_path)
        orig_init(self, *args, **kwargs)
        self.exchange = None

    monkeypatch.setattr(ccxt_fetcher.CcxtFetcher, "__init__", patched_init)
    monkeypatch.setattr(
        ccxt_fetcher.CcxtFetcher, "_fetch_remote",
        lambda self, symbol, start, end: (_ for _ in ()).throw(RuntimeError("network down")),
    )

    manager = DataManager(["BTCUSD"], interval_seconds=HOUR, mode="backtest")
    df = manager.fetch_historical_data("BTCUSD", "2020-06-01", "2020-06-02")

    assert len(df) == 44
    assert df["timestamp"].min() == pd.Timestamp("2020-06-01 00:00")
    assert df["timestamp"].max() == pd.Timestamp("2020-06-02 23:00")
