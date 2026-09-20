"""
Contract tests for performance.signal_statistics.contiguous_segments (CUL-15 D1a,
GH#50 family; relocated from prescreen_signal.py, E-039 step 5, 2026-09-12).

The shared helper partitions a records list into maximal runs of temporally
consecutive bars. Its five-clause contract (C-H1..C-H5) is pre-registered in
docs/analysis-reports/PRESCREEN_GAP_CONTIGUOUS_SEGMENTS.md; these tests pin each
clause, and each is mutation-checked (see the PATCH-1 commit body).
"""

import random
import sys
from pathlib import Path

import pandas as pd
import pytest

TRADING_BOT_ROOT = Path(__file__).parent.parent.parent / "trading-bot"
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))

from performance.signal_statistics import contiguous_segments

_STEP = pd.Timedelta(1, unit="h")
_BASE = pd.Timestamp("2020-01-01 00:00:00")


def _recs(hours):
    """Records carrying only a 'timestamp' at each given hour offset."""
    return [{"timestamp": _BASE + pd.Timedelta(h, unit="h")} for h in hours]


def test_contiguous_segments_none_is_single_span():
    """C-H3: expected_step=None returns one segment spanning every record."""
    recs = _recs(range(10))
    assert contiguous_segments(recs, None) == [(0, 10)]


def test_contiguous_segments_empty_is_empty():
    """C-H1 edge: an empty list has no segments (with or without a step)."""
    assert contiguous_segments([], _STEP) == []
    assert contiguous_segments([], None) == []


def test_contiguous_segments_splits_on_hole():
    """C-H2: one known 1-bar hole splits into exactly two ranges; the
    surrounding contiguous records stay one range each."""
    # hours 0,1,2 then a hole (3 missing) then 4,5 -> boundary between idx2/idx3
    recs = _recs([0, 1, 2, 4, 5])
    assert contiguous_segments(recs, _STEP) == [(0, 3), (3, 5)]


def test_contiguous_segments_cover_is_exact():
    """C-H1: for a randomized gappy list the ranges are contiguous,
    non-overlapping, and sum to len(records)."""
    rng = random.Random(20260903)
    hours, h = [], 0
    for _ in range(200):
        hours.append(h)
        h += rng.choice([1, 1, 1, 2, 5, 30])  # mostly contiguous, occasional holes
    recs = _recs(hours)
    segs = contiguous_segments(recs, _STEP)

    assert segs[0][0] == 0
    assert segs[-1][1] == len(recs)
    for i in range(len(segs) - 1):
        assert segs[i][1] == segs[i + 1][0]  # contiguous: no gap and no overlap
    for s, e in segs:
        assert s < e  # every segment non-empty
    assert sum(e - s for s, e in segs) == len(recs)


def test_contiguous_segments_nonmonotone_is_boundary():
    """C-H2: the test is `!=`, not `>`. A duplicate timestamp (delta 0) and a
    backwards timestamp (delta < 0) each insert a boundary."""
    dup = _recs([0, 1, 1, 2])  # delta idx1->idx2 is 0
    assert contiguous_segments(dup, _STEP) == [(0, 2), (2, 4)]

    back = _recs([0, 1, 0, 1])  # delta idx1->idx2 is -1h
    assert contiguous_segments(back, _STEP) == [(0, 2), (2, 4)]


def test_contiguous_segments_missing_timestamp_raises():
    """C-H5: a record with no 'timestamp' key while expected_step is set raises,
    naming the offending index -- never a silent positional fallback."""
    recs: list = _recs([0, 1])
    recs.append({"forecast": 10.0})  # index 2, no timestamp (deliberately malformed)
    with pytest.raises(KeyError, match="index 2"):
        contiguous_segments(recs, _STEP)


def test_contiguous_segments_missing_timestamp_ok_when_step_none():
    """C-H3/C-H4: with expected_step=None the helper never reads 'timestamp',
    so a timestamp-less record list is fine (one span)."""
    recs = [{"forecast": 1.0}, {"forecast": 2.0}]
    assert contiguous_segments(recs, None) == [(0, 2)]
