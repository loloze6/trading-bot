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


def _tracked_results_status():
    """Return porcelain status lines for tracked files under trading-bot/results/,
    or None if git can't be consulted.

    Untracked ('??') entries are skipped: an untracked file is by definition not a
    mutation of a tracked one.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(_REPO_ROOT), "status", "--porcelain", "--", _RESULTS_REL],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return {
        ln for ln in out.stdout.splitlines() if ln.strip() and not ln.startswith("??")
    }


# Status snapshot taken before any test runs. `None` means git could not be consulted
# at session start, in which case the finish check has no baseline and stands down
# rather than guessing.
_BASELINE = None


def pytest_sessionstart(session):
    """Snapshot the pre-existing status so the finish check measures CHANGE.

    Why a baseline is required (2026-07-26): the original check asked "is any tracked
    file under results/ non-clean?" and treated a yes as proof the session dirtied it.
    That inference only holds while results/ is committed and clean before the run. It
    breaks the moment previously-untracked result files are STAGED for a bulk commit:
    staged additions report as 'A ', which is neither '??' nor caused by any test, so
    the guard failed a run in which all 77 tests passed and nothing was written. The
    defect this guard exists to catch is a WRITE PERFORMED BY THE SESSION, so compare
    against the state at session start rather than against an assumed-clean tree.
    """
    global _BASELINE
    _BASELINE = _tracked_results_status()


def pytest_sessionfinish(session, exitstatus):
    if _BASELINE is None:
        return
    after = _tracked_results_status()
    if after is None:
        return
    # Only entries that APPEARED or CHANGED during the session are attributable to it.
    dirty = sorted(after - _BASELINE)
    if dirty:
        session.exitstatus = 1
        print(
            f"\nD4 REGRESSION: the test session mutated tracked file(s) under "
            f"{_RESULTS_REL}. Tests must write to tmp_path, never the shared "
            f"results dir. Offending entries:\n  " + "\n  ".join(dirty)
        )
