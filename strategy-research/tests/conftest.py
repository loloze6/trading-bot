"""
Test-isolation-by-default guard (rider, 2026-07-13/14).

Root cause this closes: sandboxing workflow/run_campaign.py's and
workflow/run_phase1_research.py's own module-level path globals was
previously OPT-IN (the `campaign_root` fixture in
test_k4_routing_registration.py). Any test that forgot to request it ran
against the REAL repository. Exactly this gap produced a real, if inert,
stray write during K2 rider development (protocols/escalation_dotusdt_15m.json
+ an empty runs/run_x_next/ scaffold — both cleaned up, see commit
4ac85c1 and the independent read-only audit this rider's own context
preamble references). This autouse fixture makes isolation the DEFAULT:
every test gets its own throwaway sandbox unless it explicitly opts out.

SURVEY (module-level path globals a test could reach, found by reading
the source, not assumed):

  workflow/run_campaign.py:
    ROOT, QUEUE_PATH, CAMPAIGN_LOG_PATH, CAMPAIGN_SUMMARY_PATH, BASELINE_PATH

  workflow/run_phase1_research.py:
    ROOT, CAMPAIGN_STATE_PATH, _KB_PATH, _POWER_DISCREPANCY_LOG_PATH,
    _DATA_POLICY_PATH

  workflow/setup_run.py:
    ROOT
    (Patching this module's ROOT protects only DIRECT in-process calls,
    e.g. test_run_id_allocation.py's `sr.create_pipeline_state(...)`. The
    subprocess-invocation path used by _route_pivot/_scaffold_next_run
    spawns a fresh Python process that re-imports setup_run.py from disk
    with its own hardcoded ROOT = Path(__file__).parent.parent -- an
    in-process monkeypatch cannot reach that. This is a pre-existing,
    already-documented limitation (test_k4_routing_registration.py's own
    module docstring), not something this rider changes; tests that
    exercise that path already stub setup_run/subprocess.run entirely
    (the campaign_root fixture's own pattern) rather than relying on
    ROOT patching for it.)

  NOT patchable this way, noted for the record:
    run_phase1_research._load_token_budget() reads
    config/campaign_config.yaml via a path hardcoded relative to the
    SOURCE FILE (Path(__file__).parent.parent), never via the ROOT
    global -- it structurally bypasses this guard regardless of what
    ROOT is set to. test_token_budget_weighted.py's own
    test_load_token_budget_reads_campaign_config relies on exactly this
    to read the real file. Out of this rider's scope to change (would be
    a behavior change to shipped code, not a test-isolation fix).

SURVEY (existing test files that intentionally read real repository
content): test_campaign_config_sync.py and test_cost_model_schema.py read
real config/*.yaml files, and test_token_budget_weighted.py,
test_kb_reactivation_gate.py, test_yaml_repair_multiline_continuation.py,
test_power_discrepancy_log.py, and test_k2_verdict_machinery.py read real,
frozen historical run/config artifacts as fixture data. ALL of them do so
via a path constructed independently of the globals this guard patches --
typically each file's own module-level `ROOT = Path(__file__).parent.parent`
(a same-named but entirely separate variable in that test module's own
namespace, never `run_campaign.ROOT`/`run_phase1_research.ROOT`), or a
literal `Path(__file__).parent.parent / "runs" / "run_0NN" / ...`. None of
THOSE touch the patched module attributes for their real-repo reads, so
none of them need the marker.

One test DOES need it, found only by running the full suite (not by
static survey alone): `test_wishlist_predicate.py::
test_er_overlay_predicate_does_not_fire_against_real_kb` calls
`run_campaign.evaluate_wishlist_predicate(...)` directly, with no
tmp_path/monkeypatch of its own -- it is a known-answer test asserting
the mechanical predicate result against the REAL, current
campaign_knowledge_base.yaml/detector_wishlist.yaml (via `ROOT`, which
this guard redirects by default). Marked `@pytest.mark.real_repo_readonly`
at the point of definition. `test_unknown_family_is_missing_field` in the
same file also calls the real function with no sandboxing, but does NOT
need the marker: it queries a family name guaranteed absent from either a
real or an empty wishlist file, so `missing_field` is the correct result
either way -- confirmed by it passing unmarked under this guard.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Parallel runs (pytest-xdist, `-n 8`): every worker process would otherwise let
# numpy/BLAS start one thread per core, so 8 workers x 8 threads fight over 8
# cores (measured 2026-10-03: the slowest tests ran 5-7x slower in parallel than
# alone). One thread per worker. Set before anything imports numpy; only in a
# worker (xdist sets PYTEST_XDIST_WORKER), so a serial run is unchanged; an
# explicit value in the environment still wins.
if os.environ.get("PYTEST_XDIST_WORKER"):
    for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS"):
        os.environ.setdefault(_var, "1")

import pytest
from _net_guard import install_network_block, register_network_marker

# --- CUL-198: cache + network guards for the fast suite -------------------
# Two structural guards (design ruling 198-O1, 2026-09-02) that replace the
# per-file "remember the skipif" convention which let two same-day CI catches
# (2026-09-01) through: an untracked-cache read with no guard, and a live
# PortfolioInfo pinging Binance from a test. Both guards live in uniquely-named
# sibling modules so tests import them without the two-conftest name collision
# (this suite and tools/recorder/tests/ each hold a conftest.py):
#   * tests/_cache_guard.py  -- requires_cache / cache_is_available
#   * tests/_net_guard.py    -- the outbound-network block, wired below and
#     reused verbatim by the recorder subtree's conftest.


# --- D4 regression guard --------------------------------------------------
# The whole point of the D4 fix: no test may write into the shared, tracked
# trading-bot/results/ directory (its trades.json was silently dirtied by the
# suite three times across this arc). This session-finish hook is the standing
# guarantee -- it fails the run if ANY test mutated a tracked file there,
# regardless of which test did it or in what order they ran. See
# trading-bot/tests/conftest.py for the twin guard on the other suite.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_RESULTS_REL = "trading-bot/results"

# --- CUL-221 local_data mutation guard ------------------------------------
# Twin of the D4 guard, one directory over: no test may create or change a file
# under trading-bot/local_data/. The failure it catches is a test that live-
# fetches instead of skipping -- base_fetcher writes the fetched OHLCV/funding/
# fear_greed CSV into local_data, silently, even under the socket block if the
# cache is a wrong-window-but-non-degenerate stub that slips past requires_cache.
# The @requires_cache byte-size floor cannot see window coverage; this session
# snapshot closes that class. The sealed holdout subdir is NEVER enumerated or
# opened (reading it spends it) -- it is skipped by name at the top level.
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


def pytest_sessionstart(session):
    global _local_data_snapshot
    _local_data_snapshot = _snapshot_local_data()


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
    local_dirty = _mutated_local_data_files()
    if local_dirty:
        session.exitstatus = 1
        print(
            f"\nCUL-221 REGRESSION: the test session created/changed file(s) "
            f"under {_LOCAL_DATA_REL} -- a test live-fetched real data instead of "
            f"skipping. Tests must not write market-data caches. Offending "
            f"entries:\n  " + "\n  ".join(local_dirty)
        )


_WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
if str(_WORKFLOW_PATH) not in sys.path:
    sys.path.insert(0, str(_WORKFLOW_PATH))

import run_campaign as _camp  # noqa: E402
import run_phase1_research as _rpr  # noqa: E402
import setup_run as _setup_run  # noqa: E402


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "real_repo_readonly: opt OUT of the autouse sandbox-by-default guard "
        "for this test. Grants READ access to the real repository's own "
        "config/state files BY CONVENTION ONLY -- a test carrying this "
        "marker must not write to the real repo; nothing enforces that "
        "beyond the convention itself, so use it only for genuine "
        "real-config reads, never as a way to skip writing a proper fixture.",
    )
    config.addinivalue_line(
        "markers",
        "slow: tests that take more than a few seconds (e.g. runs the real "
        "backtest engine). Matches trading-bot/pytest.ini's convention; no "
        "default -m filter is configured here, so these still run by default "
        "-- the marker exists for selective inclusion/exclusion, not to hide "
        "them.",
    )
    register_network_marker(config)


@pytest.fixture(autouse=True)
def _block_network(request, monkeypatch):
    """Fail loud on any outbound network connect from a fast-suite test.

    Patches ``socket.socket.connect``/``connect_ex`` for the duration of each
    test (restored by monkeypatch teardown) so an accidental network call --
    e.g. constructing a live PortfolioInfo whose __init__ pings Binance --
    raises on EVERY machine, not only on the network-blocked CI runners.
    Loopback and AF_UNIX stay reachable. Opt out with @pytest.mark.network.
    """
    install_network_block(request, monkeypatch)


@pytest.fixture(autouse=True)
def _sandbox_by_default(request, tmp_path, monkeypatch):
    """
    Redirects every surveyed module-level path global into a per-test
    tmp_path sandbox, unless the test is marked
    @pytest.mark.real_repo_readonly.

    Ordering guarantee (verified, not assumed): pytest runs same-scope
    autouse fixtures before same-scope EXPLICITLY-requested fixtures, and
    all fixtures in one test share the SAME `monkeypatch` instance --
    monkeypatch.setattr always just overwrites the current value while
    remembering only the ORIGINAL (pre-test) one for teardown. So a test
    using its own, more specific sandboxing fixture (e.g. `campaign_root`
    in test_k4_routing_registration.py) has that fixture's own
    monkeypatch.setattr calls run AFTER this one and simply win for the
    rest of the test -- this guard never overrides a test's own explicit
    sandboxing, it only fills the gap when a test provides none.
    """
    # E-030 dispatch bug hunt (2026-08-23): GIT_DIR/GIT_INDEX_FILE/GIT_WORK_TREE
    # leaking from an enclosing `git commit` (the pre-commit hook's own subprocess
    # environment) into a test's `git -C <tmp>`/`cwd=<tmp>` subprocess calls
    # override that targeting -- an explicit GIT_DIR wins over `-C`/`cwd`. Measured
    # live: this exact leak, hit via test_gitsha_dirty.py, set the real repo's own
    # .git/config to `core.bare = true` during an E-030 S2a commit (fixed,
    # f0ff0432), and three more files in THIS suite build throwaway git repos the
    # same unprotected way (test_dual_writer_guards.py, test_holdout_date_gate.py,
    # test_s4_union_merge.py -- one of them runs `git init --bare` on its own
    # fixture, an even closer match to the incident's mechanism). Scrubbed here,
    # once, for every test in this suite -- including real_repo_readonly ones,
    # since an unset GIT_DIR only restores normal directory-based discovery and
    # cannot be the wrong choice for any test.
    for _key in ("GIT_DIR", "GIT_INDEX_FILE", "GIT_WORK_TREE"):
        monkeypatch.delenv(_key, raising=False)

    if request.node.get_closest_marker("real_repo_readonly"):
        return

    sandbox = tmp_path / "_default_test_sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)
    # _save_queue/_materialize_run etc. write into config/ via tempfile.mkstemp(
    # dir=parent) -- which requires the parent directory to already exist (the
    # real repo's config/ always does; a fresh sandbox does not unless created
    # here). Found by the negative-proof test itself (test_sandbox_guard.py).
    (sandbox / "config").mkdir(parents=True, exist_ok=True)

    # campaign_data_policy.yaml is SEEDED, not left absent. _generate_monthly_windows
    # now refuses to emit tiles without knowing where holdout_range starts (deny by
    # default -- a missing policy is not "no holdout to worry about"), so an empty
    # sandbox would make every window-generating test fail for a reason unrelated to
    # what it tests. The seed is a verbatim copy of the real file: the sandbox exists
    # to stop stray WRITES, and a test reading the true seal is the intent, not a
    # leak. Anything the code writes back lands in the sandbox copy as before.
    _real_policy = Path(__file__).parent.parent / "config" / "campaign_data_policy.yaml"
    if _real_policy.exists():
        shutil.copyfile(_real_policy, sandbox / "config" / "campaign_data_policy.yaml")

    monkeypatch.setattr(_camp, "ROOT", sandbox)
    monkeypatch.setattr(_camp, "QUEUE_PATH", sandbox / "config" / "campaign_queue.yaml")
    monkeypatch.setattr(_camp, "CAMPAIGN_LOG_PATH", sandbox / "campaign_log.md")
    monkeypatch.setattr(_camp, "CAMPAIGN_SUMMARY_PATH", sandbox / "campaign_summary.md")
    monkeypatch.setattr(_camp, "BASELINE_PATH", sandbox / "config" / "campaign_baseline_runs.yaml")

    monkeypatch.setattr(_rpr, "ROOT", sandbox)
    monkeypatch.setattr(_rpr, "CAMPAIGN_STATE_PATH", sandbox / "campaign_state.yaml")
    # E-062 S2b-2b: the recompute overlay's one path constant, next to the ledger.
    monkeypatch.setattr(_rpr, "TRIAL_SHARPE_BASIS_OVERLAY_PATH",
                        sandbox / "trial_sharpe_basis_recompute.yaml")
    monkeypatch.setattr(_rpr, "_KB_PATH", sandbox / "campaign_knowledge_base.yaml")
    monkeypatch.setattr(_rpr, "_DATA_POLICY_PATH", sandbox / "config" / "campaign_data_policy.yaml")

    monkeypatch.setattr(_setup_run, "ROOT", sandbox)

    return sandbox
