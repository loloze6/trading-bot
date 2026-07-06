"""
F8 (P1a shakedown, 2026-07-04) regression test.

Reproduces the ACTUAL double-collision sequence from this session:
1. run_043 and run_044 are both real, independently-launched runs with progress.
2. run_043's campaign_review reframes. The OLD _next_run_id("run_043") returned
   "run_044" unconditionally (current+1) -- already in use, collision #1.
3. After recovering (content moved to run_045), run_044's OWN campaign_review
   later reframes. The OLD _next_run_id("run_044") returned "run_045" -- by now
   also in use (from the first recovery), collision #2.

The fix must compute the true next-free ID by scanning runs/ + campaign_state.yaml's
runs list, not "current + 1" -- avoiding both collisions on the first try.
"""
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr


def _make_run_with_progress(runs_dir: Path, run_id: str):
    """A run directory with REAL progress (non-fresh pipeline_state.yaml) —
    what a run-ID collision actually destroys."""
    run_dir = runs_dir / run_id
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(yaml.safe_dump({
        "run_id": run_id, "status": "active", "current_stage": "verdict_interpreter",
        "pending_stage": "campaign_review",
        "completed_stages": ["hypothesis_generation", "innovation_expansion",
                              "validation", "backtest_specification",
                              "signal_prescreen", "verdict_interpreter"],
    }), encoding="utf-8")
    (run_dir / "artifacts" / "research_brief.yaml").write_text(
        f"hypothesis_id: REAL_HYPOTHESIS_{run_id.upper()}\n", encoding="utf-8"
    )


@pytest.fixture
def campaign_dir(tmp_path, monkeypatch):
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    monkeypatch.setattr(rpr, "ROOT", tmp_path)
    campaign_state_path = tmp_path / "campaign_state.yaml"
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", campaign_state_path)
    return tmp_path, runs_dir, campaign_state_path


def test_reproduces_real_double_collision_sequence_and_avoids_both(campaign_dir):
    tmp_path, runs_dir, campaign_state_path = campaign_dir

    # Set the scene exactly as it was: run_043 and run_044 both real, both already
    # in campaign_state.runs (run_044 was launched independently, in the same batch).
    _make_run_with_progress(runs_dir, "run_043")
    _make_run_with_progress(runs_dir, "run_044")
    campaign_state_path.write_text(yaml.safe_dump({
        "runs": ["run_039", "run_043", "run_044"],
    }), encoding="utf-8")

    # Collision #1 in the real sequence: run_043 reframes.
    allocated_1 = rpr._next_run_id("run_043")
    assert allocated_1 == "run_045", (
        f"expected the first free slot after 043/044 ('run_045'), got '{allocated_1}' "
        f"-- if this is 'run_044', the collision is NOT fixed"
    )
    assert not (runs_dir / allocated_1).exists(), "allocated ID must not already exist"

    # Simulate that run_045 now exists (as the orchestrator would create it).
    _make_run_with_progress(runs_dir, allocated_1)
    campaign = yaml.safe_load(campaign_state_path.read_text(encoding="utf-8"))
    campaign["runs"].append(allocated_1)
    campaign_state_path.write_text(yaml.safe_dump(campaign), encoding="utf-8")

    # Collision #2 in the real sequence: run_044's OWN reframe, later.
    allocated_2 = rpr._next_run_id("run_044")
    assert allocated_2 == "run_046", (
        f"expected the first free slot after 043/044/045 ('run_046'), got "
        f"'{allocated_2}' -- if this is 'run_045', the second collision is NOT fixed"
    )
    assert not (runs_dir / allocated_2).exists()


def test_setup_run_refuses_to_overwrite_a_run_with_progress(campaign_dir, monkeypatch):
    """The defense-in-depth backstop: even if a caller computed a bad ID, setup_run.py
    itself must refuse to clobber an in-progress run."""
    tmp_path, runs_dir, _ = campaign_dir
    _make_run_with_progress(runs_dir, "run_044")

    setup_run_path = Path(__file__).parent.parent / "workflow" / "setup_run.py"
    sys.path.insert(0, str(setup_run_path.parent))
    import importlib
    import setup_run as sr
    importlib.reload(sr)
    monkeypatch.setattr(sr, "ROOT", tmp_path)

    with pytest.raises(RuntimeError, match="REFUSING TO OVERWRITE"):
        sr.create_pipeline_state(runs_dir / "run_044", "run_044")


def test_safe_write_new_research_brief_refuses_real_content(campaign_dir):
    tmp_path, runs_dir, _ = campaign_dir
    _make_run_with_progress(runs_dir, "run_044")

    with pytest.raises(RuntimeError, match="REFUSING TO OVERWRITE"):
        rpr._safe_write_new_research_brief("run_044", {"hypothesis_id": "SOMETHING_ELSE"})


def test_safe_write_new_research_brief_permits_placeholder_or_absent(campaign_dir):
    tmp_path, runs_dir, _ = campaign_dir
    run_dir = runs_dir / "run_050"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "research_brief.yaml").write_text(
        "# TODO: Paste your research brief configuration here.\n", encoding="utf-8"
    )
    rpr._safe_write_new_research_brief("run_050", {"hypothesis_id": "REAL_ONE"})
    written = yaml.safe_load((run_dir / "artifacts" / "research_brief.yaml").read_text(encoding="utf-8"))
    assert written["hypothesis_id"] == "REAL_ONE"


def test_single_run_no_collision_still_increments_normally(campaign_dir):
    """Non-regression: the common case (no collision) must still behave sensibly."""
    tmp_path, runs_dir, campaign_state_path = campaign_dir
    _make_run_with_progress(runs_dir, "run_010")
    campaign_state_path.write_text(yaml.safe_dump({"runs": ["run_010"]}), encoding="utf-8")
    assert rpr._next_run_id("run_010") == "run_011"
