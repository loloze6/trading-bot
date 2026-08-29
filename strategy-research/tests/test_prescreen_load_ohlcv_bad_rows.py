"""
F5 regression test: _load_ohlcv must NOT silently drop unparseable in-range rows.

A dropped interior bar makes _extract_forecasts' positional next_ret_bps pairing
(prescreen_signal.py:353-354) span two bars, corrupting pooled IC and the route
verdict. The fix counts in-range rows that fail to parse and raises ValueError
naming the file and count, rather than swallowing them.

Fixtures point the module's _LOCAL_DATA constant at tmp_path (monkeypatch) so the
repo's real local_data/ is never touched.
"""

import csv
import re
import sys
from pathlib import Path

import pytest

TOOLS_PATH = Path(__file__).parent.parent / "tools"
TBOT_PATH = Path(__file__).parent.parent.parent / "trading-bot"
sys.path.insert(0, str(TOOLS_PATH))
sys.path.insert(0, str(TBOT_PATH))

import prescreen_signal as ps  # noqa: E402

_HDR = ["timestamp", "open", "high", "low", "close", "volume"]
_START = "2020-01-01"
_END = "2020-02-01"


def _write_csv(path: Path, data_rows: list[list[str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(_HDR)
        w.writerows(data_rows)


def _clean_rows(n: int) -> list[list[str]]:
    out = []
    for i in range(n):
        c = 100.0 + i
        out.append([f"2020-01-01 {i:02d}:00:00", c, c, c, c, 1])
    return out


def test_clean_load_returns_all_rows(monkeypatch, tmp_path):
    """T1: N clean in-range rows -> N rows returned, no raise."""
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    _write_csv(tmp_path / "CLEAN_1h.csv", _clean_rows(6))

    df = ps._load_ohlcv("CLEAN", _START, _END)

    assert len(df) == 6
    assert list(df["close"]) == [100.0, 101.0, 102.0, 103.0, 104.0, 105.0]


def test_one_interior_bad_close_raises(monkeypatch, tmp_path):
    """T2 (sentinel): exactly ONE in-range row with a non-numeric close raises,
    message names the file and the count. Catches an off-by-one threshold."""
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    rows = _clean_rows(6)
    rows[2][4] = "x"  # interior close, in-range
    fname = "DIRTY_1h.csv"
    _write_csv(tmp_path / fname, rows)

    with pytest.raises(ValueError) as exc:
        ps._load_ohlcv("DIRTY", _START, _END)

    msg = str(exc.value)
    assert fname in msg
    # Pin the COUNT itself, not merely the presence of the digit: `fname`
    # contains "1" (via "_1h.csv"), so a bare `"1" in msg` passes even when the
    # counter is wrong. Verified by mutation: `bad_count += 2` left that
    # assertion green.
    assert re.search(r"rows: 1 in ", msg), msg


def test_missing_close_header_raises(monkeypatch, tmp_path):
    """T3: renamed/missing close header (KeyError every row) raises,
    not an empty/short DataFrame."""
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    path = tmp_path / "NOCLOSE_1h.csv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "open", "high", "low", "closing", "volume"])
        for i in range(4):
            c = 100.0 + i
            w.writerow([f"2020-01-01 {i:02d}:00:00", c, c, c, c, 1])

    with pytest.raises(ValueError):
        ps._load_ohlcv("NOCLOSE", _START, _END)


def test_out_of_window_garbage_not_counted(monkeypatch, tmp_path):
    """T4: unparseable rows OUTSIDE [start, end) are not counted, no raise."""
    monkeypatch.setattr(ps, "_LOCAL_DATA", str(tmp_path))
    rows = _clean_rows(3)  # in-range, clean
    rows.append(["2019-06-01 00:00:00", "x", "x", "x", "x", 1])  # before window
    rows.append(["2020-03-01 00:00:00", "y", "y", "y", "y", 1])  # after window
    _write_csv(tmp_path / "MIXED_1h.csv", rows)

    df = ps._load_ohlcv("MIXED", _START, _END)

    assert len(df) == 3
