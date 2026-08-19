"""The read path must refuse sealed rows (E-015-adjacent, 2026-08-19).

The 7 committed Binance caches physically contain sealed 2026 rows: the seal
guards added earlier block NEW leaks but never removed the existing ones
(BTCUSDT_1h.csv alone carries 4,344 rows >= 2026-01-01), and those files now
also sit on the shared culi.to server. Trimming them is the eventual fix, but
it changes their content hash and therefore data_sha256, forcing a rebaseline
of the reference run. This guard buys the protection today without that cost.

REFUSES rather than silently dropping: quietly returning a shorter series than
was requested hands the caller a backtest over a different window than it
believes it ran.
"""
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from data.data_manager import (  # noqa: E402
    SealedDataError,
    _assert_no_sealed_rows,
    _holdout_start,
)


def _frame(*stamps):
    return pd.DataFrame({"timestamp": [pd.Timestamp(s) for s in stamps],
                         "close": [1.0] * len(stamps)})


def test_seal_is_read_from_policy_not_hardcoded(tmp_path, monkeypatch):
    """A hardcoded boundary would keep passing while ignoring a policy change --
    the 'correct-looking banner over a stale check' shape already flagged
    against holdout_date_gate.sh's PATTERN."""
    import data.data_manager as dm
    policy = tmp_path / "p.yaml"
    policy.write_text("holdout_range: ['2025-06-01', '2025-12-31']\n", encoding="utf-8")
    monkeypatch.setattr(dm, "_POLICY_PATH", policy)
    assert dm._holdout_start() == pd.Timestamp("2025-06-01")


def test_unreadable_policy_refuses_rather_than_defaulting(tmp_path, monkeypatch):
    import data.data_manager as dm
    monkeypatch.setattr(dm, "_POLICY_PATH", tmp_path / "nope.yaml")
    with pytest.raises(SealedDataError, match="Cannot read holdout_range"):
        dm._holdout_start()


def test_a_frame_reaching_into_the_seal_is_refused():
    seal = _holdout_start()
    df = _frame("2025-12-31 22:00", "2025-12-31 23:00", seal)
    with pytest.raises(SealedDataError, match="holdout seal"):
        _assert_no_sealed_rows(df, "BTCUSDT")


def test_the_first_sealed_timestamp_itself_is_refused():
    """Boundary: the seal date is the FIRST sealed instant, not the last legal
    one. An off-by-one here reads exactly the bar the seal exists to protect --
    the same defect fixed the same day in measure_bar_sigma."""
    with pytest.raises(SealedDataError):
        _assert_no_sealed_rows(_frame(_holdout_start()), "BTCUSDT")


def test_a_wholly_pre_seal_frame_passes_untouched():
    """Control, and the bit-identity claim in miniature: every legitimate window
    ends <= the day before the seal, so the guard must be a no-op for them."""
    df = _frame("2024-04-01", "2025-06-15", "2025-12-31 23:00")
    _assert_no_sealed_rows(df, "BTCUSDT")          # must not raise


def test_empty_and_columnless_frames_are_tolerated():
    """A failed fetch returns an empty frame; that is #4's problem to report,
    not this guard's -- it must not mask it with a confusing seal error."""
    _assert_no_sealed_rows(pd.DataFrame(), "BTCUSDT")
    _assert_no_sealed_rows(None, "BTCUSDT")
    _assert_no_sealed_rows(pd.DataFrame({"close": [1.0]}), "BTCUSDT")
