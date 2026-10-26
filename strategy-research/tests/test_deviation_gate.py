"""
D-104: orchestrator.deviation_gate (off by default, requires nearest_build).

With the gate on, a spec_ready 1b answer whose artifacts/deviations.yaml lists
any deviation from the brief -- or that has no readable deviations.yaml --
pauses the run (config_deviation) before step 2 and any backtest. Off: 1b's
route is byte-identical. Nearest build's own record stays information only.
"""
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import nearest_build as nb  # noqa: E402

from _reader_test_helpers import _set_orchestrator  # noqa: E402
from test_e068_6_nearest_build import CDA, DEVS, NB_ON, _spec_ready_run  # noqa: E402

GATE_ON = {**NB_ON, "deviation_gate": {"enabled": True}}


def _state(run_dir):
    return rpr.load_yaml(run_dir / "pipeline_state.yaml") or {}


# --- the flag ---------------------------------------------------------------

def test_flag_off_by_default_and_in_the_shipped_config():
    _set_orchestrator(NB_ON)
    assert rpr._deviation_gate_enabled() is False
    shipped = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert shipped["orchestrator"]["deviation_gate"]["enabled"] is False
    _set_orchestrator(GATE_ON)
    assert rpr._deviation_gate_enabled() is True


def test_flag_on_without_nearest_build_raises():
    _set_orchestrator({**CDA, "deviation_gate": {"enabled": True}})
    with pytest.raises(ValueError, match="nearest_build"):
        rpr._deviation_gate_enabled()


@pytest.mark.parametrize("bad", ["true", 1, None])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**NB_ON, "deviation_gate": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._deviation_gate_enabled()


def test_flag_is_registered_everywhere():
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    [entry] = [f for f in reg["flags"] if f["name"] == "deviation_gate"]
    assert entry["config_key"] == "orchestrator.deviation_gate.enabled"
    assert entry["reader"] == "run_phase1_research._deviation_gate_enabled"
    assert camp._flag_readers()["deviation_gate"] is rpr._deviation_gate_enabled
    assert ("config_deviation", "config_deviation") in camp._PAUSE_FLAG_TO_REASON


# --- flag off: byte-identical ------------------------------------------------

def test_flag_off_deviations_route_on_as_before():
    _set_orchestrator(NB_ON)
    run_dir = _spec_ready_run("run_990", deviations=DEVS)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    state = _state(run_dir)
    assert state.get("status") != "paused_for_human"
    assert not (state.get("flags") or {}).get(rpr.CONFIG_DEVIATION_FLAG)
    assert len(nb.load_record(run_dir / "artifacts")["deviations"]) == 2  # nearest build unchanged


# --- flag on ------------------------------------------------------------------

def test_flag_on_deviations_pause_before_step_2(capsys):
    _set_orchestrator(GATE_ON)
    run_dir = _spec_ready_run("run_991", deviations=DEVS)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"
    state = _state(run_dir)
    assert state["status"] == "paused_for_human"
    assert state["flags"][rpr.CONFIG_DEVIATION_FLAG] is True
    assert "2 deviation(s)" in state["last_error"]
    assert camp._classify_human_pause(run_dir, state) == "config_deviation"
    assert "PIPELINE PAUSED (config_deviation)" in capsys.readouterr().out


def test_flag_on_rationale_line_only_deviation_pauses():
    """Review of PR #384: a deviation written only as a `DEVIATION:` rationale line leaves the
    structured `deviations` list empty; the record's status is `approximation`, and the gate pauses."""
    _set_orchestrator(GATE_ON)
    run_dir = _spec_ready_run("run_994", rationale=[
        {"hypothesis_claim": "4-bar hold", "config_choice": "DEVIATION: none, forecast / 10 sizing"}])
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"
    rec = nb.load_record(run_dir / "artifacts")
    assert rec["deviations"] == [] and rec["status"] == nb.STATUS_APPROXIMATION
    assert "1 DEVIATION: line(s)" in _state(run_dir)["last_error"]


def test_flag_on_no_deviation_continues():
    _set_orchestrator(GATE_ON)
    run_dir = _spec_ready_run("run_992")
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert not (_state(run_dir).get("flags") or {}).get(rpr.CONFIG_DEVIATION_FLAG)


def test_flag_on_missing_record_fails_closed(monkeypatch):
    _set_orchestrator(GATE_ON)
    monkeypatch.setattr(rpr, "_record_nearest_build", lambda path: None)
    run_dir = _spec_ready_run("run_993")
    assert not (run_dir / "artifacts" / nb.DEVIATIONS_FILE).exists()
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"
    assert "missing or unreadable" in _state(run_dir)["last_error"]
