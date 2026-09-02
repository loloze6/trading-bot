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

# --- CUL-221 local_data mutation guard ------------------------------------
# Twin of the strategy-research suite's CUL-221 guard, applied to this suite's
# own runs (strategy-research/tests/conftest.py holds the original). No test may
# create or change a file under trading-bot/local_data/: the failure it catches
# is a test that live-fetches real market data instead of skipping when its
# cache is absent -- base_fetcher writes the fetched OHLCV/funding/fear_greed CSV
# into local_data silently, invisible to `git status` because the caches are
# gitignored, and the stray 2024 rows then poison downstream cache-gated tests.
# The @requires_cache byte-size floor cannot see window coverage; this session
# snapshot closes that class. The sealed holdout subdir is NEVER enumerated or
# opened (reading it spends it) -- it is skipped by name at the top level.
# Duplicated (~40 lines) rather than shared: importing across the two test trees
# would couple them, and the house pattern is disjoint per-suite conftests.
_LOCAL_DATA_REL = "trading-bot/local_data"
_HOLDOUT_DIRNAME = "holdout_sealed"
_local_data_snapshot = None


def _snapshot_local_data():
    """Top-level {name: (size, mtime_ns)} of trading-bot/local_data/, with the
    sealed holdout subdir EXCLUDED -- never descended, never opened. Returns None
    if the dir can't be read (guard then no-ops rather than false-failing)."""
    root = _REPO_ROOT / _LOCAL_DATA_REL
    snap = {}
    try:
        for entry in root.iterdir():
            if entry.name == _HOLDOUT_DIRNAME:
                continue  # sealed store: never enumerate or open it
            if entry.is_file():
                st = entry.stat()
                snap[entry.name] = (st.st_size, st.st_mtime_ns)
    except OSError:
        return None
    return snap


def _mutated_local_data_files():
    """Files under trading-bot/local_data/ created or changed since session start
    (top level, holdout excluded), or None if either snapshot was unavailable."""
    before = _local_data_snapshot
    after = _snapshot_local_data()
    if before is None or after is None:
        return None
    changed = [f"CREATED {n}" for n in after if n not in before]
    changed += [f"CHANGED {n}" for n, sig in after.items() if n in before and before[n] != sig]
    return changed


def _tracked_results_status():
    """Return porcelain status lines for tracked files under trading-bot/results/,
    or None if git can't be consulted.

    Untracked ('??') entries are skipped: an untracked file is by definition not a
    mutation of a tracked one.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(_REPO_ROOT), "status", "--porcelain", "--", _RESULTS_REL],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return {ln for ln in out.stdout.splitlines() if ln.strip() and not ln.startswith("??")}


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
    global _BASELINE, _local_data_snapshot
    _BASELINE = _tracked_results_status()
    _local_data_snapshot = _snapshot_local_data()


def pytest_sessionfinish(session, exitstatus):
    if _BASELINE is not None:
        after = _tracked_results_status()
        if after is not None:
            # Only entries that APPEARED or CHANGED during the session are attributable to it.
            dirty = sorted(after - _BASELINE)
            if dirty:
                session.exitstatus = 1
                print(
                    f"\nD4 REGRESSION: the test session mutated tracked file(s) under "
                    f"{_RESULTS_REL}. Tests must write to tmp_path, never the shared "
                    f"results dir. Offending entries:\n  " + "\n  ".join(dirty)
                )

    local_dirty = _mutated_local_data_files()
    if local_dirty:
        session.exitstatus = 1
        print(
            f"\nCUL-221 REGRESSION: the test session created/changed file(s) "
            f"under {_LOCAL_DATA_REL} -- a test live-fetched real market data "
            f"instead of skipping. Tests must not write market-data caches. "
            f"Offending entries:\n  " + "\n  ".join(local_dirty)
        )
