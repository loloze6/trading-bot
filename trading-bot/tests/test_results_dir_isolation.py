"""
D4 positive proof: EnhancedPerformanceTracker's opt-in log_file seam actually
redirects the trades dump away from the shared trading-bot/results/trades.json,
and using it leaves that shared, tracked file byte-for-byte untouched.

This is the fast, order-independent counterpart to the session-finish guard in
conftest.py. The guard fails the run if the shared file is dirtied by anyone;
this test proves the mechanism the fix relies on to keep it clean.
"""

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from performance.metrics import EnhancedPerformanceTracker  # noqa: E402

SHARED_TRADES = PROJECT_ROOT / "results" / "trades.json"


def test_log_file_override_writes_to_tmp_and_leaves_shared_untouched(tmp_path):
    before = SHARED_TRADES.read_bytes() if SHARED_TRADES.exists() else None

    target = tmp_path / "interim_trades.json"
    tracker = EnhancedPerformanceTracker(log_file=str(target))
    # The tracker must resolve the absolute tmp path verbatim, not fold it under
    # the project's results dir.
    assert Path(tracker.log_file) == target

    tracker.save_trades()  # would hit the shared file if the override were ignored
    assert target.exists(), "override path was not written"

    after = SHARED_TRADES.read_bytes() if SHARED_TRADES.exists() else None
    assert after == before, (
        "shared trading-bot/results/trades.json was mutated despite a log_file "
        "override (D4 regression)"
    )


def test_default_still_targets_shared_results_path():
    """The production default is unchanged: absent an override, the tracker still
    resolves to the flat results/trades.json. Guards against silently altering
    the live/default behaviour while fixing the test-isolation defect. This
    constructs the tracker but never calls save_trades(), so it writes nothing."""
    tracker = EnhancedPerformanceTracker()
    assert Path(tracker.log_file) == SHARED_TRADES
