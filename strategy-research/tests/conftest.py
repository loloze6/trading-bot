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
import sys
from pathlib import Path

import pytest

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
    if request.node.get_closest_marker("real_repo_readonly"):
        return

    sandbox = tmp_path / "_default_test_sandbox"
    sandbox.mkdir(parents=True, exist_ok=True)
    # _save_queue/_materialize_run etc. write into config/ via tempfile.mkstemp(
    # dir=parent) -- which requires the parent directory to already exist (the
    # real repo's config/ always does; a fresh sandbox does not unless created
    # here). Found by the negative-proof test itself (test_sandbox_guard.py).
    (sandbox / "config").mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(_camp, "ROOT", sandbox)
    monkeypatch.setattr(_camp, "QUEUE_PATH", sandbox / "config" / "campaign_queue.yaml")
    monkeypatch.setattr(_camp, "CAMPAIGN_LOG_PATH", sandbox / "campaign_log.md")
    monkeypatch.setattr(_camp, "CAMPAIGN_SUMMARY_PATH", sandbox / "campaign_summary.md")
    monkeypatch.setattr(_camp, "BASELINE_PATH", sandbox / "config" / "campaign_baseline_runs.yaml")

    monkeypatch.setattr(_rpr, "ROOT", sandbox)
    monkeypatch.setattr(_rpr, "CAMPAIGN_STATE_PATH", sandbox / "campaign_state.yaml")
    monkeypatch.setattr(_rpr, "_KB_PATH", sandbox / "campaign_knowledge_base.yaml")
    monkeypatch.setattr(_rpr, "_POWER_DISCREPANCY_LOG_PATH", sandbox / "power_check_discrepancy_log.yaml")
    monkeypatch.setattr(_rpr, "_DATA_POLICY_PATH", sandbox / "config" / "campaign_data_policy.yaml")

    monkeypatch.setattr(_setup_run, "ROOT", sandbox)

    return sandbox
