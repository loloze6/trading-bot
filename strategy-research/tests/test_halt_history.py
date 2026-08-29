"""
E-030 S1 durable-halt-record fix (`tasks/todo.md`, Piece 1), 2026-08-22.

`pipeline_state.yaml`'s `last_error` is written in full at halt time
(`run_loop`'s except-block, `last_error=str(e)`, untruncated) but two things
destroy it before it's ever recoverable: `_hard_pause_reason` truncates it to
300 chars for the `campaign_log.md` HALT line, and RUNBOOK.md section 4's own
documented resume procedure has the operator null the field on every resume.
Together these meant halt #7 in `E-030/artifacts/s1_halt_taxonomy.md`
(46.85h, the single largest halt in the campaign's recorded history) left no
recoverable cause anywhere on disk.

`_append_halt_history` (`workflow/run_campaign.py`) closes this by appending
a full-fidelity snapshot to a new `halt_history` list on `pipeline_state.yaml`
itself -- modeled on `completed_stages`/`audit_log`, the two fields on that
same file that already accumulate across a run's life instead of being
overwritten -- at the moment the halt is detected, before any resume step
can touch `last_error`/`flags`.

Fixture pattern (campaign_root, _write_fresh_scaffold, _save_queue_entries)
copied from tests/test_k4_routing_registration.py's proven hermetic setup:
monkeypatches ROOT/QUEUE_PATH/etc. so nothing here touches the real
repository, and no LLM/subprocess is spawned. `pending_stage` is always set
to a TERMINAL_PREFIXES-matching value ("human_pause") so `run_loop` breaks
immediately without attempting to process a real stage.
"""

import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402


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
        "holdout_reserved": False,
        "validation_approved": False,
        "screening_passed": False,
        "walk_forward_passed": False,
    },
    "last_summary": None,
}


def _write_fresh_scaffold(runs_dir: Path, run_id: str, **state_overrides):
    run_dir = runs_dir / run_id
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "handoffs").mkdir(parents=True, exist_ok=True)
    state = dict(_FRESH_STATE_TEMPLATE)
    state["run_id"] = run_id
    state.update(state_overrides)
    with open(run_dir / "pipeline_state.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, sort_keys=False)
    return run_dir


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
        next_run_id = cmd[-1]
        _write_fresh_scaffold(runs_dir, next_run_id)
        return _FakeCompletedProcess()

    monkeypatch.setattr(rpr.subprocess, "run", _fake_subprocess_run)

    return {
        "root": tmp_path,
        "runs_dir": runs_dir,
        "queue_path": queue_path,
        "baseline_path": baseline_path,
        "campaign_state_path": campaign_state_path,
    }


def _save_queue_entries(queue_path: Path, entries: list):
    with open(queue_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"queue": entries}, f, sort_keys=False)


def _write_campaign_state(path: Path, **fields):
    state = {
        "campaign_id": "test",
        "research_question": "",
        "runs": [],
        "altitude_history": [],
        "recent_parameter_dimensions_by_family": {},
        "failed_families": [],
        "instruments_tried": [],
        "components_built": [],
        "timeframes_tried": ["1h"],
        "diagnostics_log": [],
        "status": "active",
    }
    state.update(fields)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, sort_keys=False)


def _read_state(runs_dir: Path, run_id: str) -> dict:
    return yaml.safe_load((runs_dir / run_id / "pipeline_state.yaml").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------


def test_hard_pause_appends_untruncated_last_error_to_halt_history(campaign_root):
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]

    long_error = "X" * 500  # over the 300-char campaign_log.md truncation
    _write_fresh_scaffold(
        runs_dir,
        "run_700",
        status="failed",
        pending_stage="human_pause",
        last_error=long_error,
    )
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {
                "id": "TEST_ENTRY",
                "brief_path": "briefs/irrelevant.yaml",
                "status": "in_progress",
                "priority": 1,
                "run_ids": ["run_700"],
                "outcome": None,
            }
        ],
    )
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_700"])

    keep_going = camp.process_once()

    assert keep_going is False
    state = _read_state(runs_dir, "run_700")
    history = state.get("halt_history")
    assert history is not None and len(history) == 1
    entry = history[0]
    assert entry["reason"] == "unhandled_exception"
    assert entry["last_error"] == long_error, "halt_history must carry the FULL, untruncated last_error"
    assert len(entry["last_error"]) == 500

    log_text = (root / "campaign_log.md").read_text(encoding="utf-8")
    # The campaign_log.md HALT line is still truncated to 300 chars, unchanged --
    # this fix adds a durable record, it does not touch campaign_log.md's format.
    assert "X" * 500 not in log_text, "campaign_log.md's HALT line must remain truncated, unchanged by this fix"
    assert "X" * 300 in log_text


def test_halt_history_accumulates_across_repeated_halts_same_run(campaign_root):
    """Models run_053's real 4-halt history (S1 taxonomy #1/#2/#4/#5) --
    halt_history must APPEND, mirroring completed_stages/audit_log's existing
    accumulate-don't-overwrite convention on the same file, not overwrite the
    prior entry the way `last_error` itself is overwritten on each halt."""
    runs_dir = campaign_root["runs_dir"]
    _write_fresh_scaffold(
        runs_dir,
        "run_701",
        status="failed",
        pending_stage="human_pause",
        last_error="first failure",
    )
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {
                "id": "TEST_ENTRY",
                "brief_path": "briefs/irrelevant.yaml",
                "status": "in_progress",
                "priority": 1,
                "run_ids": ["run_701"],
                "outcome": None,
            }
        ],
    )
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_701"])

    camp.process_once()
    state = _read_state(runs_dir, "run_701")
    assert len(state["halt_history"]) == 1

    # Simulate the operator's documented RUNBOOK section 4 resume-reset (nulls
    # last_error/status) followed by a SECOND, different halt on the same run --
    # the accumulated first entry must survive the reset that clears the
    # CURRENT-state fields.
    rpr.update_state(path=runs_dir / "run_701", status="failed", last_error="second, different failure")
    queue = camp._load_queue()
    queue["queue"][0]["status"] = "in_progress"
    _save_queue_entries(campaign_root["queue_path"], queue["queue"])

    camp.process_once()
    state = _read_state(runs_dir, "run_701")
    history = state["halt_history"]
    assert len(history) == 2, "second halt must APPEND, not overwrite, the first entry"
    assert history[0]["last_error"] == "first failure"
    assert history[1]["last_error"] == "second, different failure"


def test_refinement_brief_conflict_appends_to_halt_history_on_parent(campaign_root):
    """The refinement_brief_conflicts_with_existing_continuation pause (the
    OTHER HALT site in process_once(), separate from _hard_pause_reason) must
    also append -- durability shouldn't depend on which of the two HALT sites
    fired."""
    runs_dir = campaign_root["runs_dir"]
    root = campaign_root["root"]
    _write_fresh_scaffold(runs_dir, "run_702", pending_stage="completed_refined")
    _write_fresh_scaffold(runs_dir, "run_703_internal")
    rpr.update_state(
        path=runs_dir / "run_702",
        continuation_child="run_703_internal",
        continuation_created_by="_route_refine",
        pending_stage="completed_refined",
    )

    briefs_dir = root / "briefs"
    briefs_dir.mkdir()
    briefs_dir.joinpath("test_refinement.yaml").write_text(
        yaml.safe_dump(
            {
                "hypothesis_id": "test_hyp",
                "new_research_question": "q",
                "parameter_dimension": {"name": "d", "value": "v"},
                "rationale": "r",
                "expected_impact": "i",
            }
        ),
        encoding="utf-8",
    )

    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {
                "id": "TEST_ENTRY",
                "brief_path": "briefs/irrelevant.yaml",
                "status": "in_progress",
                "priority": 1,
                "run_ids": ["run_702"],
                "outcome": None,
                "refinement_brief_path": "briefs/test_refinement.yaml",
            }
        ],
    )
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_702"])

    keep_going = camp.process_once()

    assert keep_going is False
    state = _read_state(runs_dir, "run_702")
    history = state.get("halt_history")
    assert history is not None and len(history) == 1
    assert history[0]["reason"] == "refinement_brief_conflicts_with_existing_continuation"
    assert "run_703_internal" in history[0]["detail"]
