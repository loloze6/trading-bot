"""
K4 kernel (A1 + A3 + B1) regression tests, 2026-07-13.
See engineering/improvements/done/design_and_docs/K4_routing_registration_design_20260712.md sections 5-8.

Hermeticity note: workflow/setup_run.py's own module-level ROOT is
hardcoded (Path(__file__).parent.parent), independent of any caller's
monkeypatched ROOT, and _route_pivot/_scaffold_next_run scaffold the next
run via a subprocess.run([...setup_run.py...]) call whose spawned process
has that SAME hardcoded, unpatchable ROOT. Neither call site is sandboxable
by monkeypatching ROOT alone (this is also why the pre-existing
dry_run_verify() achieves its "zero footprint" claim via cleanup-after
-- shutil.rmtree in a finally block -- rather than via true isolation).
These tests instead monkeypatch the NAMES actually invoked
(run_campaign.setup_run, run_phase1_research.subprocess.run) to in-tmp_path
fakes that replicate the real functions' on-disk output shape, so nothing
here ever touches the real repository, and no LLM/subprocess is spawned.
"""
import hashlib
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402

assert camp.orch is rpr, "run_campaign.orch must be the same module object as run_phase1_research"


# ---------------------------------------------------------------------------
# Shared fixture: a fully sandboxed campaign root
# ---------------------------------------------------------------------------

_FRESH_STATE_TEMPLATE = {
    "status": "active",
    "current_stage": None,
    "pending_stage": "hypothesis_generation",
    "completed_stages": [],
    "artifacts": {},
    "governance": {
        "max_hypothesis_variants_per_cycle": 3,
        "max_refinements_after_validation": 2,
        "max_reruns_after_analysis": 1,
        "max_required_reads_per_stage": 3,
    },
    "counters": {"refinements_used": 0, "reruns_used": 0},
    "flags": {
        "holdout_reserved": False, "validation_approved": False,
        "screening_passed": False, "walk_forward_passed": False,
    },
    "last_summary": None,
}


def _write_fresh_scaffold(runs_dir: Path, run_id: str):
    run_dir = runs_dir / run_id
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "handoffs").mkdir(parents=True, exist_ok=True)
    state = dict(_FRESH_STATE_TEMPLATE)
    state["run_id"] = run_id
    with open(run_dir / "pipeline_state.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, sort_keys=False)


@pytest.fixture
def campaign_root(tmp_path, monkeypatch):
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    queue_path = config_dir / "campaign_queue.yaml"
    queue_path.write_text(yaml.safe_dump({"queue": []}), encoding="utf-8")
    baseline_path = config_dir / "campaign_baseline_runs.yaml"
    campaign_state_path = tmp_path / "campaign_state.yaml"

    monkeypatch.setattr(camp, "ROOT", tmp_path)
    monkeypatch.setattr(camp, "QUEUE_PATH", queue_path)
    monkeypatch.setattr(camp, "CAMPAIGN_LOG_PATH", tmp_path / "campaign_log.md")
    monkeypatch.setattr(camp, "CAMPAIGN_SUMMARY_PATH", tmp_path / "campaign_summary.md")
    monkeypatch.setattr(camp, "BASELINE_PATH", baseline_path)
    monkeypatch.setattr(rpr, "ROOT", tmp_path)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", campaign_state_path)

    def _fake_setup_run(run_id):
        _write_fresh_scaffold(runs_dir, run_id)
    monkeypatch.setattr(camp, "setup_run", _fake_setup_run)

    class _FakeCompletedProcess:
        returncode = 0

    def _fake_subprocess_run(cmd, *args, **kwargs):
        # cmd = [sys.executable, str(<ROOT>/workflow/setup_run.py), next_run_id]
        next_run_id = cmd[-1]
        _write_fresh_scaffold(runs_dir, next_run_id)
        return _FakeCompletedProcess()
    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)

    return {
        "root": tmp_path, "runs_dir": runs_dir, "queue_path": queue_path,
        "baseline_path": baseline_path, "campaign_state_path": campaign_state_path,
    }


def _save_queue_entries(queue_path: Path, entries: list):
    with open(queue_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"queue": entries}, f, sort_keys=False)


def _write_campaign_state(path: Path, **fields):
    state = {
        "campaign_id": "test", "research_question": "", "runs": [],
        "altitude_history": [], "recent_parameter_dimensions_by_family": {},
        "failed_families": [], "instruments_tried": [], "components_built": [],
        "timeframes_tried": ["1h"], "diagnostics_log": [], "status": "active",
    }
    state.update(fields)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, sort_keys=False)


# ---------------------------------------------------------------------------
# A1 -- persisted continuation intent
# ---------------------------------------------------------------------------

def test_route_refine_persists_continuation_child(campaign_root):
    """_route_refine must write continuation_child/continuation_created_by
    onto ITS OWN run's pipeline_state.yaml before returning, per design
    note section 5."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_100")
    run_dir = runs_dir / "run_100"
    (run_dir / "artifacts" / "proposed_brief.yaml").write_text(
        yaml.safe_dump({"strategy_domain": "test", "timeframe": "1h"}), encoding="utf-8"
    )
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_100"])

    interp = {"proposed_change_dimension": "test_dim", "hypothesis_family": "test_family"}
    next_stage = rpr._route_refine(run_dir, "run_100", interp, {})

    assert next_stage == "completed_refined"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["continuation_child"] == "run_101", state.get("continuation_child")
    assert state["continuation_created_by"] == "_route_refine"
    assert (runs_dir / "run_101").exists(), "child scaffold must exist on disk"


def test_route_pivot_persists_continuation_child(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_200")
    run_dir = runs_dir / "run_200"
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_200"])

    interp = {"hypothesis_family": "exhausted_family"}
    next_stage = rpr._route_pivot(run_dir, "run_200", interp, {})

    assert next_stage == "completed_refined"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["continuation_child"] == "run_201"
    assert state["continuation_created_by"] == "_route_pivot"
    assert (runs_dir / "run_201").exists()


def test_route_escalate_instrument_persists_continuation_child(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_300")
    run_dir = runs_dir / "run_300"

    (root / "protocols").mkdir()
    (root / "protocols" / "baseline_v1.json").write_text(
        '{"symbols": ["BTCUSDT"], "timeframe": "1h", "windows": []}', encoding="utf-8"
    )
    (root / "config").mkdir(exist_ok=True)
    (root / "config" / "coin_universe.yaml").write_text(yaml.safe_dump({
        "escalation_order": {"sequence": [{"category": "majors", "priority": 1}]},
        "categories": {"majors": {"coins": [{"symbol": "ETHUSDT", "data_cached": True}],
                                   "strategy_affinity": []}},
    }), encoding="utf-8")
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_300"])

    next_stage = rpr._route_escalate(run_dir, "run_300", {}, {})

    assert next_stage == "completed_escalated"
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["continuation_child"] == "run_301"
    assert state["continuation_created_by"] == "_route_escalate"
    assert (runs_dir / "run_301").exists()


def test_fresh_process_continuation_across_separate_process_once_calls(campaign_root):
    """The literal A1 acceptance criterion: a refine verdict on fixture run
    N causes the NEXT process_once() invocation (no in-memory state shared
    with the call that produced the verdict) to launch run N+1, leaving the
    queue entry in_progress with the child appended to run_ids -- not
    silently finalized 'done', which is what the pre-K4 dir-diff logic did."""
    runs_dir = campaign_root["runs_dir"]
    queue_path = campaign_root["queue_path"]
    _write_fresh_scaffold(runs_dir, "run_100")
    run_dir = runs_dir / "run_100"
    (run_dir / "artifacts" / "proposed_brief.yaml").write_text(
        yaml.safe_dump({"strategy_domain": "test", "timeframe": "1h"}), encoding="utf-8"
    )
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_100"])

    # Step 1: drive the verdict-stage routing directly (see module docstring
    # for why this replaces invoking orch.run_loop() end-to-end).
    interp = {"proposed_change_dimension": "test_dim", "hypothesis_family": "test_family"}
    next_stage = rpr._route_refine(run_dir, "run_100", interp, {})
    # Simulate run_loop's own step-6 update_state call, which is what
    # actually persists pending_stage after determine_post_verdict_route
    # returns -- the one piece of run_loop's behavior this test doesn't
    # get by calling _route_refine directly.
    rpr.update_state(path=run_dir, pending_stage=next_stage, status="active",
                      completed_stages=["verdict_interpreter"])

    _save_queue_entries(queue_path, [{
        "id": "TEST_ENTRY", "brief_path": "briefs/irrelevant.yaml",
        "status": "in_progress", "priority": 1, "run_ids": ["run_100"], "outcome": None,
    }])

    # Step 2: a SEPARATE process_once() call -- nothing carried over except
    # what's on disk (queue file + run_100's own pipeline_state.yaml).
    keep_going = camp.process_once()

    assert keep_going is True
    queue = camp._load_queue()
    entry = queue["queue"][0]
    assert entry["run_ids"] == ["run_100", "run_101"], entry["run_ids"]
    assert entry["status"] == "in_progress", entry["status"]
    log_text = campaign_root["root"].joinpath("campaign_log.md").read_text(encoding="utf-8")
    assert "CONTINUE TEST_ENTRY" in log_text
    assert "DONE TEST_ENTRY" not in log_text


# ---------------------------------------------------------------------------
# A3 -- reconciler
# ---------------------------------------------------------------------------

def test_reconciler_flags_crash_window_orphan(campaign_root):
    """A run dir materialized but never registered anywhere (the exact
    run_051/run_040 shape) must be flagged."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_400")  # scaffolded...
    _save_queue_entries(campaign_root["queue_path"], [])  # ...never registered
    _write_campaign_state(campaign_root["campaign_state_path"])

    orphans = camp.reconcile_orphans()
    assert "run_400" in orphans
    log_text = campaign_root["root"].joinpath("campaign_log.md").read_text(encoding="utf-8")
    assert "run_400" in log_text and "RECONCILE" in log_text


def test_reconciler_exempts_quarantined_orphan_and_never_selected_or_renumbered(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_500")
    (runs_dir / "run_500" / "ORPHANED_README.md").write_text(
        "quarantined_orphan -- pivot scaffold of an overturned kill, never reuse.",
        encoding="utf-8",
    )
    _save_queue_entries(campaign_root["queue_path"], [])
    _write_campaign_state(campaign_root["campaign_state_path"])

    orphans = camp.reconcile_orphans()
    assert "run_500" in orphans, "still reported"
    # K4 rider (2026-07-13): a quarantined-only orphan set is now the CLEAN
    # case -- reconcile_orphans() always emits exactly one line, but run_500
    # itself must not appear in it (it's covered by the "N known-quarantined"
    # count, not named individually).
    log_text = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert "run_500" not in log_text, "must not appear in the clean-case log line"
    assert "0 unexpected" in log_text

    # Never selected: no queue entry references it, so _select_entry can't return it.
    queue = camp._load_queue()
    assert camp._select_entry(queue["queue"]) is None

    # Never renumbered over: the next allocated id skips past it (it occupies "500").
    next_id = camp._next_new_run_id()
    assert next_id != "run_500"


def test_reconciler_does_not_flag_trial_sharpes_only_id(campaign_root):
    """Regression for the run_041/run_042 case (design note section 4):
    a run_id registered ONLY via campaign_state.trial_sharpes (never
    campaign_state.runs, never any queue run_ids) must NOT be flagged."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_041")
    _save_queue_entries(campaign_root["queue_path"], [])
    _write_campaign_state(
        campaign_root["campaign_state_path"],
        runs=[],
        trial_sharpes=[{"trial_id": "run_041", "source": "prescreen_backfill"}],
    )

    orphans = camp.reconcile_orphans()
    assert "run_041" not in orphans


def _count_reconcile_lines(log_path: Path) -> int:
    if not log_path.exists():
        return 0
    return sum(1 for line in log_path.read_text(encoding="utf-8").splitlines()
               if "RECONCILE:" in line)


def test_reconcile_orphans_emits_exactly_one_line_clean_case(campaign_root):
    """K4 rider (2026-07-13): a clean pass (zero unexpected orphans) must
    still emit exactly one RECONCILE line -- previously it emitted none,
    making a clean pass indistinguishable from reconcile_orphans() never
    having run at all."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_700")
    _save_queue_entries(campaign_root["queue_path"], [{
        "id": "TEST_ENTRY", "brief_path": "briefs/irrelevant.yaml",
        "status": "in_progress", "priority": 1, "run_ids": ["run_700"], "outcome": None,
    }])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_700"])

    orphans = camp.reconcile_orphans()
    assert orphans == [], "run_700 is referenced via campaign_state.runs -- no orphans expected"

    log_path = campaign_root["root"] / "campaign_log.md"
    assert _count_reconcile_lines(log_path) == 1, "exactly one RECONCILE line, never zero"
    log_text = log_path.read_text(encoding="utf-8")
    assert "0 unexpected" in log_text
    assert "1 run dir(s) scanned" in log_text
    assert "1 referenced/grandfathered" in log_text


def test_reconcile_orphans_emits_exactly_one_line_non_clean_case(campaign_root):
    """The non-clean (unexpected-orphan) case must ALSO emit exactly one
    line -- never zero, never two."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(runs_dir, "run_701")  # scaffolded, never registered
    _save_queue_entries(campaign_root["queue_path"], [])
    _write_campaign_state(campaign_root["campaign_state_path"])

    orphans = camp.reconcile_orphans()
    assert orphans == ["run_701"]

    log_path = campaign_root["root"] / "campaign_log.md"
    assert _count_reconcile_lines(log_path) == 1, "exactly one RECONCILE line, never two"
    log_text = log_path.read_text(encoding="utf-8")
    assert "run_701" in log_text
    assert "0 unexpected" not in log_text, "non-clean line's content is unchanged -- no clean-case wording"


# ---------------------------------------------------------------------------
# K4 rider -- dry_run_verify() parity with process_once()'s graceful
# "Queue exhausted" handling on an all-terminal queue
# ---------------------------------------------------------------------------

def test_dry_run_verify_on_all_terminal_queue_returns_cleanly(campaign_root):
    """The real-world trigger for this rider: campaign_queue.yaml with every
    entry done/blocked_on_* (P4_ts_trend done, XS_momentum blocked_on_P2) --
    _select_entry() returns None. Previously raised AssertionError; must now
    log an informative line and return without raising."""
    _save_queue_entries(campaign_root["queue_path"], [
        {"id": "P4_ts_trend", "brief_path": "briefs/irrelevant.yaml", "status": "done",
         "priority": 1, "run_ids": ["run_800"], "outcome": "kill"},
        {"id": "XS_momentum", "brief_path": "briefs/irrelevant2.yaml", "status": "blocked_on_P2",
         "priority": 2, "run_ids": [], "outcome": None},
    ])
    _write_campaign_state(campaign_root["campaign_state_path"])

    camp.dry_run_verify()  # must not raise

    log_text = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert "no ready/in_progress entry" in log_text
    assert "all-terminal" in log_text


# ---------------------------------------------------------------------------
# B1 -- refinement_brief_path
# ---------------------------------------------------------------------------

_MINIMAL_REFINEMENT_BRIEF = {
    "brief_id": "TEST_REFINEMENT_r1",
    "lineage": {"parent_queue_entry": "TEST_ENTRY", "parent_run": "run_600",
                "relation": "refine", "parent_verdict": "refine_pending_test"},
    "source": "user_delivered",
    "status": "ready",
    "hypothesis": {"primary": "test hypothesis text"},
    "gate_definition": {"indicator": "test_indicator", "threshold": 0.3},
    "evaluation": {"pass_rule": "PASS iff test condition holds.",
                   "baseline_comparators": {"x": 1.0}},
}


def _write_refinement_brief(path: Path, overrides: dict | None = None):
    data = yaml.safe_load(yaml.safe_dump(_MINIMAL_REFINEMENT_BRIEF))  # deep copy
    if overrides:
        data.update(overrides)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


def test_refinement_brief_materializes_checksum_identical_and_pre_registration(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_600")
    briefs_dir = root / "briefs"
    briefs_dir.mkdir()
    brief_path = _write_refinement_brief(briefs_dir / "test_refinement.yaml")
    source_checksum = hashlib.sha256(brief_path.read_bytes()).hexdigest()

    _save_queue_entries(campaign_root["queue_path"], [{
        "id": "TEST_ENTRY", "brief_path": "briefs/irrelevant.yaml",
        "status": "in_progress", "priority": 1, "run_ids": ["run_600"], "outcome": None,
        "refinement_brief_path": "briefs/test_refinement.yaml",
    }])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_600"])

    # The materialized child starts fresh at hypothesis_generation (R1: no
    # stage-skip) -- actually executing that stage would need real handoff
    # files and an LLM call, neither of which this fixture is about. Stub
    # run_loop() for this call; the thing under test is the materialization
    # step process_once() performs BEFORE run_loop() is ever invoked.
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(camp.orch, "run_loop", lambda run_id: None)
        keep_going = camp.process_once()
    assert keep_going is True

    queue = camp._load_queue()
    entry = queue["queue"][0]
    assert entry["run_ids"] == ["run_600", "run_601"], entry["run_ids"]
    assert entry["refinement_brief_consumed_for"] == "briefs/test_refinement.yaml"

    child_artifacts = runs_dir / "run_601" / "artifacts"
    verbatim_path = child_artifacts / "user_brief_verbatim.yaml"
    assert verbatim_path.read_bytes() == brief_path.read_bytes()
    assert hashlib.sha256(verbatim_path.read_bytes()).hexdigest() == source_checksum

    pre_reg = yaml.safe_load((child_artifacts / "pre_registration.yaml").read_text(encoding="utf-8"))
    assert pre_reg["lineage"] == _MINIMAL_REFINEMENT_BRIEF["lineage"]
    assert pre_reg["gate_definition"] == _MINIMAL_REFINEMENT_BRIEF["gate_definition"]
    assert pre_reg["pass_rule"] == _MINIMAL_REFINEMENT_BRIEF["evaluation"]["pass_rule"]
    assert pre_reg["user_brief_checksum"] == f"sha256:{source_checksum}"
    # E-039 S4 (2026-09-12): A6.1 holdout-range declaration now registered here,
    # not re-derived mid-pipeline by the validation stage's own skill.
    assert pre_reg["sample_split_design"]["holdout_range"] == list(camp.orch._load_holdout_range())
    assert "A6.1" in pre_reg["sample_split_design"]["holdout_note"]

    # R1: no stage-skip -- child starts at the existing default.
    child_state = yaml.safe_load((runs_dir / "run_601" / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert child_state["pending_stage"] == "hypothesis_generation"


def test_refinement_brief_one_character_corruption_fails_checksum_assertion(campaign_root):
    """A corrupted verbatim copy must NOT match the source's checksum --
    proves the checksum assertion is load-bearing, not a tautology."""
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_600")
    briefs_dir = root / "briefs"
    briefs_dir.mkdir()
    brief_path = _write_refinement_brief(briefs_dir / "test_refinement.yaml")
    brief = rpr.load_yaml(brief_path)

    child_dir = runs_dir / "run_601"
    camp._materialize_refinement_run("run_601", brief, brief_path)
    verbatim_path = child_dir / "artifacts" / "user_brief_verbatim.yaml"

    # Corrupt one byte of the installed copy (simulating a hypothetical
    # transcription bug) and confirm the checksum comparison catches it.
    corrupted = bytearray(verbatim_path.read_bytes())
    corrupted[0] ^= 0xFF
    verbatim_path.write_bytes(bytes(corrupted))

    assert hashlib.sha256(verbatim_path.read_bytes()).hexdigest() != \
        hashlib.sha256(brief_path.read_bytes()).hexdigest()


def test_refinement_brief_idempotency_guard(campaign_root):
    """A second process_once() call with the SAME refinement_brief_path
    unchanged must not scaffold a second child."""
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_600")
    briefs_dir = root / "briefs"
    briefs_dir.mkdir()
    _write_refinement_brief(briefs_dir / "test_refinement.yaml")

    _save_queue_entries(campaign_root["queue_path"], [{
        "id": "TEST_ENTRY", "brief_path": "briefs/irrelevant.yaml",
        "status": "in_progress", "priority": 1, "run_ids": ["run_600"], "outcome": None,
        "refinement_brief_path": "briefs/test_refinement.yaml",
    }])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_600"])

    # Both calls: run_601 (fresh, pending_stage hypothesis_generation) would
    # otherwise have orch.run_loop() try to run a real stage requiring real
    # handoff files and an LLM call -- neither is what these two calls are
    # testing (queue-entry bookkeeping / the idempotency guard), so run_loop
    # is stubbed to a no-op for both.
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(camp.orch, "run_loop", lambda run_id: None)
        camp.process_once()
    queue_after_first = camp._load_queue()
    run_ids_after_first = list(queue_after_first["queue"][0]["run_ids"])
    assert run_ids_after_first == ["run_600", "run_601"]

    # Second call: refinement_brief_consumed_for already matches, so
    # _next_action_for_entry now classifies this entry as "continue".
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(camp.orch, "run_loop", lambda run_id: None)
        camp.process_once()

    queue_after_second = camp._load_queue()
    entry_after_second = queue_after_second["queue"][0]
    assert entry_after_second["run_ids"] == ["run_600", "run_601"], (
        "idempotency guard must prevent a second child from being scaffolded"
    )
    assert not (runs_dir / "run_602").exists()


def test_refinement_brief_conflict_pauses_with_both_children_intact(campaign_root):
    """R2: if the parent run already has an internally-fired continuation
    (continuation_child recorded by _route_refine/_route_pivot/_route_escalate)
    and the operator ALSO sets refinement_brief_path, this is a hard-pause,
    not a silent override -- neither child is discarded, and setup_run is
    never even called for a second child."""
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_600")
    # Simulate internal routing having already fired: an internally-scaffolded
    # child + the continuation_child record on the parent.
    _write_fresh_scaffold(runs_dir, "run_601_internal")
    rpr.update_state(path=runs_dir / "run_600", continuation_child="run_601_internal",
                      continuation_created_by="_route_refine", pending_stage="completed_refined")

    briefs_dir = root / "briefs"
    briefs_dir.mkdir()
    _write_refinement_brief(briefs_dir / "test_refinement.yaml")

    _save_queue_entries(campaign_root["queue_path"], [{
        "id": "TEST_ENTRY", "brief_path": "briefs/irrelevant.yaml",
        "status": "in_progress", "priority": 1, "run_ids": ["run_600"], "outcome": None,
        "refinement_brief_path": "briefs/test_refinement.yaml",
    }])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_600"])

    keep_going = camp.process_once()

    assert keep_going is False, "a conflict must halt the campaign, not proceed"
    queue = camp._load_queue()
    entry = queue["queue"][0]
    assert entry["status"] == "paused:refinement_brief_conflicts_with_existing_continuation"
    # Neither child was touched/created a second time.
    assert (runs_dir / "run_601_internal").exists()
    assert not (runs_dir / "run_601").exists(), "no second child scaffolded for the conflicted entry"
    log_text = root.joinpath("campaign_log.md").read_text(encoding="utf-8")
    assert "briefs/test_refinement.yaml" in log_text, "log must name the refinement_brief_path verbatim"
    assert "run_601_internal" in log_text, "log must name the existing continuation_child verbatim"
