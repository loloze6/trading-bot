"""
#47: _load_bars must not drop malformed bars.csv rows silently.

A dropped bar silently degrades every field derived from bar POSITION -- MAE/MFE
collapse to 0.0, entry/exit efficiency and post-exit returns to null, exit_reason
to its default. run_protocol.py:387 already warns about exactly that class, but
it is gated on `if bars`, so the ALL-ROWS-FAIL case (a renamed or missing
`timestamp` column makes every row a KeyError) was quieter than the partial one:
empty list, no warning at all.

Not fatal by design, matching the file's documented choice at :387 -- partial
diagnostics beat aborting a completed multi-window protocol run. The defect was
the silence, not the tolerance.
"""

import csv
import sys
from pathlib import Path

_SR = Path(__file__).parent.parent
sys.path.insert(0, str(_SR / "tools"))

import run_protocol as rp  # noqa: E402

_HDR = ["timestamp", "open", "high", "low", "close"]


def _write_bars(run_dir, rows, header=_HDR):
    run_dir.mkdir(parents=True, exist_ok=True)
    with open(run_dir / "bars.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def _clean(n):
    return [
        [f"2024-01-01 {i:02d}:00:00", 100 + i, 101 + i, 99 + i, 100 + i]
        for i in range(n)
    ]


def test_clean_bars_load_silently(tmp_path, capsys):
    _write_bars(tmp_path, _clean(5))
    bars = rp._load_bars(tmp_path)
    assert len(bars) == 5
    assert capsys.readouterr().err == "", "clean input must not warn"


def test_partial_drop_warns_with_the_count(tmp_path, capsys):
    rows = _clean(6)
    rows[2][4] = "x"  # interior close, unparseable
    _write_bars(tmp_path, rows)

    bars = rp._load_bars(tmp_path)
    err = capsys.readouterr().err

    assert len(bars) == 5
    assert "dropped 1 of 6" in err, err
    # Pin the COUNT, not merely that something was printed.
    assert "unreliable" in err


def test_all_rows_failing_warns_even_though_the_list_is_empty(tmp_path, capsys):
    """The half #47 calls nastier: the :387 integrity warning is gated on
    `if bars` and cannot fire here, so this line is the only signal."""
    rows = _clean(4)
    _write_bars(tmp_path, rows, header=["ts", "open", "high", "low", "close"])

    bars = rp._load_bars(tmp_path)
    err = capsys.readouterr().err

    assert bars == []
    assert "ALL of them failed to parse" in err, err
    assert "renamed or missing column" in err


def test_missing_file_is_not_an_error(tmp_path, capsys):
    """Absent bars.csv is a normal state, distinct from a broken one."""
    assert rp._load_bars(tmp_path) == []
    assert capsys.readouterr().err == ""
