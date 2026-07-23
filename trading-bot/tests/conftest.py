"""
D4 regression guard for the trading-bot test suite.

Root cause this closes: the backtest path builds its EnhancedPerformanceTracker
via launcher._build_mock_stack without a log_file, so it inherited the
production default (the flat, shared trading-bot/results/trades.json) and the
throttled save_trades() dumped into that tracked file mid-run. The suite dirtied
it three times across this arc. The fix threads an opt-in trades_log_file through
run_backtest -> _build_mock_stack (production default byte-identical); the tests
opt into tmp_path. This hook is the standing guarantee that the defect stays
fixed: it fails the run if ANY test mutated a tracked file under
trading-bot/results/, independent of test order. The strategy-research suite
carries a twin guard (strategy-research/tests/conftest.py).
"""
import subprocess
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
_RESULTS_REL = "trading-bot/results"


def _mutated_tracked_results_files():
    """Return the list of tracked files under trading-bot/results/ that the
    working tree has modified/deleted, or None if git can't be consulted."""
    try:
        out = subprocess.run(
            ["git", "-C", str(_REPO_ROOT), "status", "--porcelain", "--", _RESULTS_REL],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return None
    if out.returncode != 0:
        return None
    # Skip untracked entries ('??'); we assert only on mutations of TRACKED files.
    return [ln for ln in out.stdout.splitlines() if ln.strip() and not ln.startswith("??")]


def pytest_sessionfinish(session, exitstatus):
    dirty = _mutated_tracked_results_files()
    if dirty:
        session.exitstatus = 1
        print(
            f"\nD4 REGRESSION: the test session mutated tracked file(s) under "
            f"{_RESULTS_REL}. Tests must write to tmp_path, never the shared "
            f"results dir. Offending entries:\n  " + "\n  ".join(dirty)
        )
