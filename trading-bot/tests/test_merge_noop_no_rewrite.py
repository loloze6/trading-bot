"""
A merge that adds no rows does not rewrite the cache (run_096, 2026-10-15).

Defect: BaseFetcher._load_all re-requests every missing period on every read,
including periods the source can never fill -- fear_greed before its
2018-02-01 start, and its 2018-04-14..16 hole. The fetch returns nothing,
`combined` is the cache exactly as loaded, and _merge_and_store's unconditional
`to_csv` re-opened the shared cache for writing anyway. run_096 (fold C,
2018-01..2021-08) read that range in every protocol subprocess; its composite
subprocess died on the needless open with
    PermissionError: [Errno 13] Permission denied: '...fear_greed_daily.csv'
while another handle held the file without write-sharing.

Fix: _merge_and_store skips the write when the merged frame equals `existing`.
The in-memory frame is assigned before the check, so the rows a run sees are
unchanged; only the needless open goes away.

No network: _fetch_remote is stubbed to the real API's answer for a
pre-inception window (no rows). Temp dirs only.
"""
import os
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.fetchers.fear_greed_fetcher import FearGreedFetcher  # noqa: E402

# Fold C's window with a warm-up reaching back before the index's first day.
WINDOW_START = pd.Timestamp("2017-09-01")
WINDOW_END = pd.Timestamp("2021-08-31")


def _cache(days=1340, start="2018-02-01", hole=("2018-04-14", "2018-04-16")):
    """fear_greed-shaped cache: starts 2018-02-01, runs past the window end,
    and carries the real 2018-04-14..16 hole, so the window above has a prefix
    AND an interior missing period -- both unfillable."""
    ts = pd.date_range(start, periods=days, freq="D")
    ts = ts[(ts < pd.Timestamp(hole[0])) | (ts > pd.Timestamp(hole[1]))]
    return pd.DataFrame({
        "timestamp": ts,
        "fear_greed": [(i * 7) % 101 for i in range(len(ts))],
        "classification": ["Fear" if i % 2 else "Greed" for i in range(len(ts))],
    })


def _write_cache(tmp_path, df) -> Path:
    path = tmp_path / "fear_greed_daily.csv"
    df.to_csv(path, index=False)
    return path


def _fetcher(tmp_path, remote=None):
    f = FearGreedFetcher(start_date=WINDOW_START, end_date=WINDOW_END,
                         localStorage=True, data_dir=str(tmp_path))
    calls = []

    def fake_remote(symbol, start, end):
        calls.append((start, end))
        return remote(start, end) if remote else pd.DataFrame()

    f._fetch_remote = fake_remote
    return f, calls


def test_unfillable_missing_periods_leave_cache_untouched(tmp_path):
    """The run_096 shape: prefix before 2018-02-01 + the April hole, the remote
    returns nothing. The cache file keeps its bytes AND its mtime."""
    path = _write_cache(tmp_path, _cache())
    raw_before = path.read_bytes()
    mtime_before = path.stat().st_mtime_ns

    f, calls = _fetcher(tmp_path)
    got = f.get_data("fear_greed")

    assert len(calls) == 2, calls  # prefix + April hole: the read did try to fill
    assert path.read_bytes() == raw_before
    assert path.stat().st_mtime_ns == mtime_before, "cache was rewritten by a no-op merge"
    # The rows this read returns are the cache's, bounded to the window.
    expected = pd.read_csv(path, parse_dates=["timestamp"])
    expected = expected[expected["timestamp"] <= WINDOW_END].reset_index(drop=True)
    pd.testing.assert_frame_equal(got.reset_index(drop=True), expected)


@pytest.mark.skipif(sys.platform != "win32", reason="Windows share-mode semantics")
def test_noop_read_succeeds_while_another_handle_denies_write_sharing(tmp_path):
    """The failure itself: a handle opened WITHOUT FILE_SHARE_WRITE (what a
    scanner/indexer/viewer may hold) makes any open-for-write raise
    [Errno 13]. Before the fix the no-op merge opened the file for writing and
    crashed exactly like run_096; now the read never opens it for writing."""
    import ctypes
    from ctypes import wintypes

    path = _write_cache(tmp_path, _cache())
    raw_before = path.read_bytes()

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.CreateFileW.restype = wintypes.HANDLE
    k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD,
                                wintypes.HANDLE]
    GENERIC_READ, FILE_SHARE_READ, OPEN_EXISTING = 0x80000000, 0x1, 3
    handle = k32.CreateFileW(str(path), GENERIC_READ, FILE_SHARE_READ, None,
                             OPEN_EXISTING, 0, None)
    assert handle not in (None, wintypes.HANDLE(-1).value), ctypes.get_last_error()
    try:
        # Premise: the hold really blocks a writer, with run_096's exact error.
        with pytest.raises(PermissionError) as exc:
            _cache().to_csv(path, index=False)
        assert exc.value.errno == 13

        f, _ = _fetcher(tmp_path)
        got = f.get_data("fear_greed")  # pre-fix: PermissionError [Errno 13]
        assert not got.empty
    finally:
        k32.CloseHandle(handle)
    assert path.read_bytes() == raw_before


def test_rows_added_are_still_written(tmp_path):
    """The skip is only for a no-op: a fetch that fills the hole is persisted."""
    path = _write_cache(tmp_path, _cache())

    def remote(start, end):
        if start <= pd.Timestamp("2018-04-14") <= end:
            ts = pd.date_range("2018-04-14", "2018-04-16", freq="D")
            return pd.DataFrame({"timestamp": ts, "fear_greed": 50,
                                 "classification": "Neutral"})
        return pd.DataFrame()

    f, _ = _fetcher(tmp_path, remote)
    f.get_data("fear_greed")

    on_disk = pd.read_csv(path, parse_dates=["timestamp"])
    assert pd.Timestamp("2018-04-15") in set(on_disk["timestamp"])
    assert len(on_disk) == len(_cache()) + 3


def test_merge_that_normalises_the_cache_is_still_written(tmp_path):
    """A cache whose rows the merge reorders/deduplicates is not a no-op: the
    write happens exactly as before the fix (the merged frame differs from
    `existing`), so on-disk normalisation behaviour is unchanged."""
    df = _cache()
    messy = pd.concat([df.iloc[::-1], df.iloc[:3]], ignore_index=True)  # reversed + dupes
    path = _write_cache(tmp_path, messy)
    mtime_before = path.stat().st_mtime_ns
    os.utime(path, ns=(mtime_before - 10**9, mtime_before - 10**9))
    mtime_before = path.stat().st_mtime_ns

    f, _ = _fetcher(tmp_path)
    f.get_data("fear_greed")

    assert path.stat().st_mtime_ns != mtime_before
    on_disk = pd.read_csv(path, parse_dates=["timestamp"])
    pd.testing.assert_frame_equal(on_disk, df.reset_index(drop=True))
