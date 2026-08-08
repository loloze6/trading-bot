"""
Unit tests for tests/_cache_guard.py's `cache_skip_reason` predicate.

FAST (carries no slow marker): every case builds its own synthetic caches
under `tmp_path`, so this file has no dependency on local_data, no network,
and no engine import -- it tests the predicate, not the backtest. Runs
identically with or without real caches present, including inside a
socket-blocked, cache-less clone.

Reason assertions check filename + failure-mode SUBSTRING, not the full
string, so the tests don't couple to exact wording -- only to the D2
7-mode family being distinguishable and naming the offending file.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "tests") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "tests"))

from _cache_guard import cache_skip_reason  # noqa: E402

NEEDED = ("a.csv", "b.csv", "c.csv")


def _write(path: Path, lines: list[str], trailing_newline: bool = True) -> None:
    content = "\n".join(lines)
    if trailing_newline:
        content += "\n"
    path.write_text(content)


def _healthy(path: Path, first_ts: str, last_ts: str) -> None:
    _write(path, ["timestamp,value", f"{first_ts},1", f"{last_ts},2"])


def test_u1_healthy_trio_returns_none(tmp_path):
    for name in NEEDED:
        _healthy(tmp_path / name, "2024-01-01", "2024-01-10")
    assert cache_skip_reason(tmp_path, NEEDED, "2024-01-05", "2024-01-06") is None


def test_u2_one_file_absent(tmp_path):
    _healthy(tmp_path / "a.csv", "2024-01-01", "2024-01-10")
    _healthy(tmp_path / "b.csv", "2024-01-01", "2024-01-10")
    # c.csv deliberately not created
    reason = cache_skip_reason(tmp_path, NEEDED, "2024-01-05", "2024-01-06")
    assert reason is not None
    assert "c.csv" in reason
    assert "not present" in reason


def test_u3_1h_zero_byte_file(tmp_path):
    (tmp_path / "a.csv").write_bytes(b"")
    _healthy(tmp_path / "b.csv", "2024-01-01", "2024-01-10")
    _healthy(tmp_path / "c.csv", "2024-01-01", "2024-01-10")
    reason = cache_skip_reason(tmp_path, NEEDED, "2024-01-05", "2024-01-06")
    assert reason is not None
    assert "a.csv" in reason
    assert "empty file" in reason


def test_u4_1h_header_only(tmp_path):
    _write(tmp_path / "a.csv", ["timestamp,value"])
    _healthy(tmp_path / "b.csv", "2024-01-01", "2024-01-10")
    _healthy(tmp_path / "c.csv", "2024-01-01", "2024-01-10")
    reason = cache_skip_reason(tmp_path, NEEDED, "2024-01-05", "2024-01-06")
    assert reason is not None
    assert "a.csv" in reason
    assert "no data rows" in reason


def test_u5_all_three_zero_byte(tmp_path):
    for name in NEEDED:
        (tmp_path / name).write_bytes(b"")
    reason = cache_skip_reason(tmp_path, NEEDED, "2024-01-05", "2024-01-06")
    assert reason is not None
    assert "a.csv" in reason
    assert "empty file" in reason


def test_u6_1h_2018_only_vs_2024_window(tmp_path):
    _healthy(tmp_path / "a.csv", "2018-01-01", "2018-06-01")
    _healthy(tmp_path / "b.csv", "2024-01-01", "2024-01-10")
    _healthy(tmp_path / "c.csv", "2024-01-01", "2024-01-10")
    reason = cache_skip_reason(tmp_path, NEEDED, "2024-01-05", "2024-01-06")
    assert reason is not None
    assert "a.csv" in reason
    assert "does not cover" in reason


def test_u7_covers_start_but_ends_before_window_end(tmp_path):
    _healthy(tmp_path / "a.csv", "2024-01-01", "2024-01-05")  # ends before window_end
    _healthy(tmp_path / "b.csv", "2024-01-01", "2024-01-10")
    _healthy(tmp_path / "c.csv", "2024-01-01", "2024-01-10")
    reason = cache_skip_reason(tmp_path, NEEDED, "2024-01-05", "2024-01-06")
    assert reason is not None
    assert "a.csv" in reason
    assert "does not cover" in reason


def test_u8_final_row_truncated_mid_write(tmp_path):
    # Last line's timestamp field itself is cut off mid-write -- no trailing
    # newline, no comma -- so field 0 fails datetime.fromisoformat.
    _write(
        tmp_path / "a.csv",
        ["timestamp,value", "2024-01-01,1", "2024-01-1"],
        trailing_newline=False,
    )
    _healthy(tmp_path / "b.csv", "2024-01-01", "2024-01-10")
    _healthy(tmp_path / "c.csv", "2024-01-01", "2024-01-10")
    reason = cache_skip_reason(tmp_path, NEEDED, "2024-01-05", "2024-01-06")
    assert reason is not None
    assert "a.csv" in reason
    assert "unparseable final row" in reason


def test_u9_funding_header_only_others_healthy(tmp_path):
    _healthy(tmp_path / "a.csv", "2024-01-01", "2024-01-10")
    _write(tmp_path / "b_funding.csv", ["timestamp,funding_rate"])
    _healthy(tmp_path / "c.csv", "2024-01-01", "2024-01-10")
    needed = ("a.csv", "b_funding.csv", "c.csv")
    reason = cache_skip_reason(tmp_path, needed, "2024-01-05", "2024-01-06")
    assert reason is not None
    assert "b_funding.csv" in reason
    assert "no data rows" in reason


def test_u10_fear_greed_wrong_window(tmp_path):
    _healthy(tmp_path / "a.csv", "2024-01-01", "2024-01-10")
    _healthy(tmp_path / "b.csv", "2024-01-01", "2024-01-10")
    _healthy(tmp_path / "c_fear_greed.csv", "2018-01-01", "2018-06-01")
    needed = ("a.csv", "b.csv", "c_fear_greed.csv")
    reason = cache_skip_reason(tmp_path, needed, "2024-01-05", "2024-01-06")
    assert reason is not None
    assert "c_fear_greed.csv" in reason
    assert "does not cover" in reason


def test_u11_span_exactly_equals_window_boundary(tmp_path):
    # Pins inclusive boundary semantics: first_ts == window_start and
    # last_ts == window_end must count as coverage, not a near-miss.
    for name in NEEDED:
        _healthy(tmp_path / name, "2024-01-05", "2024-01-06")
    assert cache_skip_reason(tmp_path, NEEDED, "2024-01-05", "2024-01-06") is None
