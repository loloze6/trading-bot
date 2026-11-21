"""tools/derive_kraken_bars.py: longer Kraken bars built from the hourly file, UTC-aligned, coverage recorded."""
import csv, importlib.util, sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("derive_kraken_bars", ROOT / "tools" / "derive_kraken_bars.py")
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
from data import coverage  # noqa: E402


def hour(ts, o, h, l, c, v, n):
    return [ts, str(o), str(h), str(l), str(c), str(v), ts[:14] + "59:59.999", repr(v * c), str(n), "", "", "0"]


ROWS = [
    hour("2024-01-01 02:00:00", 10.0, 11.0, 9.0, 10.5, 1.0, 1),   # block 00:00 (00h and 01h had no trade)
    hour("2024-01-01 03:00:00", 10.5, 12.0, 10.0, 11.0, 2.0, 3),
    hour("2024-01-01 04:00:00", 11.0, 11.5, 8.0, 9.0, 1.5, 2),     # block 04:00
    hour("2024-01-01 07:00:00", 9.0, 9.5, 8.5, 9.2, 0.5, 1),
    hour("2024-01-01 16:00:00", 9.2, 9.3, 9.1, 9.25, 1.0, 1),      # block 16:00 (08:00 and 12:00 empty)
    hour("2024-01-02 00:00:00", 9.25, 9.4, 9.2, 9.3, 1.0, 1),      # next day
]


def test_blocks_are_utc_aligned_and_aggregated():
    out = d.aggregate(ROWS, 4)
    assert [r[0] for r in out] == ["2024-01-01 00:00:00", "2024-01-01 04:00:00", "2024-01-01 16:00:00",
                                   "2024-01-02 00:00:00"]
    first = out[0]
    assert first[1:5] == ["10.0", "12.0", "9.0", "11.0"]           # first open, max high, min low, last close
    assert float(first[5]) == 3.0 and first[8] == "4"               # summed volume and trades
    assert first[6] == "2024-01-01 03:59:59.999"                    # the block's end less a millisecond
    assert float(first[7]) == 3.0 * 11.0                            # volume x close
    assert out[1][1:5] == ["11.0", "11.5", "8.0", "9.2"]


def test_no_row_for_an_empty_block_and_none_past_the_last_covered_day():
    out = d.aggregate(ROWS, 4, last_day=__import__("datetime").date(2024, 1, 1))
    assert [r[0][11:13] for r in out] == ["00", "04", "16"]


def test_a_bar_holds_only_hours_inside_it():
    """No lookahead: every hour feeding a bar starts at or after the bar's start and before its end."""
    for r in d.aggregate(ROWS, 4):
        inside = [h for h in ROWS if r[0] <= h[0] <= r[6]]
        assert float(r[5]) == sum(float(h[5]) for h in inside)


def test_daily_blocks_are_stamped_like_the_daily_files():
    out = d.aggregate(ROWS, 24)
    assert [r[0] for r in out] == ["2024-01-01", "2024-01-02"]
    assert out[0][6] == "2024-01-01 23:59:59.999"
    assert out[0][1:5] == ["10.0", "12.0", "8.0", "9.25"]


def write(path, rows):
    with path.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(d.HEADER)
        w.writerows(rows)


def test_derive_writes_the_file_and_records_coverage_once(tmp_path):
    src = tmp_path / "kraken_XUSD_1h.csv"
    write(src, ROWS)
    coverage.record(tmp_path, src.name, None, "2024-01-01", "test")
    d.derive(src, 4, data_dir=tmp_path)
    d.derive(src, 4, data_dir=tmp_path)                              # a rerun records nothing new
    rows = list(csv.reader((tmp_path / "kraken_XUSD_4h.csv").open()))
    assert rows[0] == d.HEADER and len(rows) == 4                    # the 2024-01-02 block is past the coverage
    entries = coverage.load(tmp_path)["kraken_XUSD_4h.csv"]
    assert len(entries) == 1 and entries[0]["start"] is None and entries[0]["end"] == "2024-01-01"


def test_refuses_a_file_out_of_order(tmp_path):
    src = tmp_path / "kraken_XUSD_1h.csv"
    write(src, [ROWS[1], ROWS[0]])
    with pytest.raises(ValueError):
        d.read(src)


def test_compare_daily_finds_equal_days(tmp_path):
    src = tmp_path / "kraken_XUSD_1h.csv"
    write(src, ROWS)
    coverage.record(tmp_path, src.name, None, "2024-01-02", "test")
    write(tmp_path / "kraken_XUSD_1d.csv", d.aggregate(ROWS, 24))
    tot = d.compare_daily(tmp_path)
    assert tot["days"] == 2 and tot["ohlc_differ"] == tot["volume_differ"] == tot["trades_differ"] == 0
