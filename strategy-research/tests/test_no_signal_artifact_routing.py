"""
F5c (P1a shakedown, 2026-07-04) regression test — orchestrator routing.

determine_post_prescreen_route() must treat route=no_signal_artifact as a dead end
requiring human intervention, NOT hand it to verdict_interpreter like a normal
kill/refine route. No protocol_result.yaml stub, no trial-spending pivot logic —
just a pause, since this is an engineering failure, not a research finding.
"""
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

from run_phase1_research import determine_post_prescreen_route


def _make_run_dir(tmp_path, prescreen_result: dict) -> Path:
    run_dir = tmp_path / "runs" / "run_test"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "prescreen_result.yaml").write_text(
        yaml.safe_dump(prescreen_result), encoding="utf-8"
    )
    pipeline_state = run_dir / "pipeline_state.yaml"
    pipeline_state.write_text(yaml.safe_dump({
        "run_id": "run_test", "status": "running", "current_stage": "signal_prescreen",
        "pending_stage": "signal_prescreen", "completed_stages": [],
    }), encoding="utf-8")
    return run_dir


def test_no_signal_artifact_routes_to_human_pause(tmp_path, monkeypatch):
    import run_phase1_research as rpr
    monkeypatch.setattr(rpr, "ROOT", tmp_path)

    run_dir = _make_run_dir(tmp_path, {
        "route": "no_signal_artifact",
        "route_rationale": "F5c: 10 bar(s) raised a swallowed component exception.",
        "component_error_count": 10,
        "prescreen_kill_reason": "component_error",
    })

    next_stage = determine_post_prescreen_route(run_dir)

    assert next_stage == "human_pause"
    assert not (run_dir / "artifacts" / "protocol_result.yaml").exists(), (
        "no_signal_artifact must not produce a protocol_result stub — nothing for "
        "verdict_interpreter to interpret"
    )
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["status"] == "paused_for_human"
    assert state["flags"]["no_signal_artifact_flagged"] is True


def test_kill_no_ic_still_routes_to_verdict_interpreter_normally(tmp_path, monkeypatch):
    """Non-regression: a genuine kill_no_ic route must behave exactly as before."""
    import run_phase1_research as rpr
    monkeypatch.setattr(rpr, "ROOT", tmp_path)

    run_dir = _make_run_dir(tmp_path, {
        "route": "kill_no_ic",
        "route_rationale": "Active-bar IC=-0.02, p=0.6 >= 0.1.",
        "ic_spearman_pooled": -0.02,
        "cost_check": {"pass": False},
        "component_error_count": 0,
        "prescreen_kill_reason": "no_informational_content_this_venue",
    })

    next_stage = determine_post_prescreen_route(run_dir)

    assert next_stage == "verdict_interpreter"
    assert (run_dir / "artifacts" / "protocol_result.yaml").exists()
