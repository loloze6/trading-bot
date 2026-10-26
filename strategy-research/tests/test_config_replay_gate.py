"""
D-109: orchestrator.config_replay_gate (off by default, no dependency).

With the gate on, when the run's research_brief.yaml carries an exact config
(a constraint starting "Build EXACTLY this strategy config (JSON)"), 1b's
spec_ready config is replayed against it (D-106) before step 2; any forecast,
regime or required_bars difference -- or a replay that cannot run -- pauses the
run (config_replay_mismatch) before any backtest. It does not rely on 1b
declaring the change (CUL-429: run_085 dropped a clip and reported `exact`).
Off: 1b's route is byte-identical.
"""
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402

from _reader_test_helpers import _set_orchestrator  # noqa: E402
from test_e056_1b_block_manifest import CONFIG, GOOD, _authored_1b, _minimal_run  # noqa: E402

CDA = {"config_direct_authoring": {"enabled": True}}
GATE_ON = {**CDA, "config_replay_gate": {"enabled": True}}

# Lane 1's v3 sma50 config (briefs/L1_daily_trend_basket_sma50_v3.md) and run_085's
# authored rewrite of it: id renamed, an identity op added, and the first clip dropped.
LANE1 = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                             "default_regime": "unknown"},
         "strategies": {"regimes": {"unknown": {"components": [{
             "id": "trend", "class": "strategies.strategy_components.MovingAverageDistanceComponent",
             "params": {"period": 50, "average": "sma"}, "weight": 1.0,
             "transforms": [{"op": "scale", "params": {"factor": 5}},
                            {"op": "clip", "params": {"min": 0, "max": 10}},
                            {"op": "vol_target", "params": {"window": 60, "target_annual_vol": 0.4,
                                                            "periods_per_year": 365}},
                            {"op": "clip", "params": {"min": 0, "max": 10}}]}]},
             "trending": None, "mean_reversion": None, "chop": None}}}
RUN_085 = copy.deepcopy(LANE1)
_c = RUN_085["strategies"]["regimes"]["unknown"]["components"][0]
_c["id"] = "sma50_distance"
_c["transforms"] = [{"op": "identity"}, {"op": "scale", "params": {"factor": 5.0}},
                    _c["transforms"][2], {"op": "clip", "params": {"min": 0.0, "max": 10.0}}]
COSMETIC = copy.deepcopy(LANE1)
_k = COSMETIC["strategies"]["regimes"]["unknown"]["components"][0]
_k["id"] = "sma50_distance"
_k["transforms"] = [{"op": "identity"}] + [
    {**t, "params": {p: float(v) for p, v in t["params"].items()}} if t["op"] in ("scale", "clip")
    else t for t in _k["transforms"]]


def _state(run_dir):
    return rpr.load_yaml(run_dir / "pipeline_state.yaml") or {}


def _brief(run_dir, exact, other=("Variants: the base only.",)):
    cons = list(other)
    if exact is not None:
        text = exact if isinstance(exact, str) else json.dumps(exact)
        cons.insert(0, rpr.BRIEF_EXACT_CONFIG_PREFIX + ", nothing added, nothing renamed:\n" + text)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"strategy_domain": "time_series_trend", "constraints": cons})


def _gate_run(run_id, brief_cfg, authored):
    """A run with a research brief and 1b's spec, for a direct call of the gate."""
    run_dir = _minimal_run(rpr.ROOT, run_id)
    _brief(run_dir, brief_cfg)
    if authored is not None:
        rpr.save_yaml(run_dir / "artifacts" / "backtest_spec.yaml",
                      {"status": "spec_ready", "config": authored})
    return run_dir


# --- the flag ---------------------------------------------------------------

def test_flag_off_by_default_and_in_the_shipped_config():
    _set_orchestrator(CDA)
    assert rpr._config_replay_gate_enabled() is False
    shipped = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert shipped["orchestrator"]["config_replay_gate"]["enabled"] is False
    _set_orchestrator(GATE_ON)
    assert rpr._config_replay_gate_enabled() is True


@pytest.mark.parametrize("bad", ["true", 1, None])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**CDA, "config_replay_gate": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._config_replay_gate_enabled()


def test_flag_is_registered_everywhere():
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    [entry] = [f for f in reg["flags"] if f["name"] == "config_replay_gate"]
    assert entry["config_key"] == "orchestrator.config_replay_gate.enabled"
    assert entry["reader"] == "run_phase1_research._config_replay_gate_enabled"
    assert camp._flag_readers()["config_replay_gate"] is rpr._config_replay_gate_enabled
    assert ("config_replay_mismatch", "config_replay_mismatch") in camp._PAUSE_FLAG_TO_REASON


# --- flag off: byte-identical ------------------------------------------------

def test_flag_off_a_differing_config_routes_on_as_before(monkeypatch):
    _set_orchestrator(CDA)
    run_dir = _authored_1b("run_970", GOOD)
    other = copy.deepcopy(CONFIG)
    other["strategies"]["regimes"]["unknown"]["components"][0]["params"]["period"] = 21
    _brief(run_dir, other)
    monkeypatch.setattr(rpr, "_brief_exact_config",
                        lambda p: pytest.fail("flag off must read nothing"))
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert _state(run_dir).get("status") != "paused_for_human"
    assert not (run_dir / "artifacts" / rpr.CONFIG_REPLAY_ARTIFACT).exists()


# --- flag on, through 1b's route ---------------------------------------------

def test_flag_on_same_config_continues_and_records_valid():
    _set_orchestrator(GATE_ON)
    run_dir = _authored_1b("run_971", GOOD)
    _brief(run_dir, CONFIG)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    rec = rpr.load_yaml(run_dir / "artifacts" / rpr.CONFIG_REPLAY_ARTIFACT)
    assert rec["verdict"] == "VALID" and rec["identical_json"] is True


def test_flag_on_forecast_changing_config_pauses_before_step_2(capsys):
    _set_orchestrator(GATE_ON)
    run_dir = _authored_1b("run_972", GOOD)
    other = copy.deepcopy(CONFIG)
    other["strategies"]["regimes"]["unknown"]["components"][0]["params"]["period"] = 21
    _brief(run_dir, other)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"
    state = _state(run_dir)
    assert state["status"] == "paused_for_human"
    assert state["flags"][rpr.CONFIG_REPLAY_FLAG] is True
    assert "replay VOID" in state["last_error"]
    assert camp._classify_human_pause(run_dir, state) == "config_replay_mismatch"
    assert rpr.load_yaml(run_dir / "artifacts" / rpr.CONFIG_REPLAY_ARTIFACT)["verdict"] == "VOID"
    assert "PIPELINE PAUSED (config_replay_mismatch)" in capsys.readouterr().out


def test_flag_on_brief_without_exact_config_continues_and_writes_nothing():
    _set_orchestrator(GATE_ON)
    run_dir = _authored_1b("run_973", GOOD)
    _brief(run_dir, None)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert not (run_dir / "artifacts" / rpr.CONFIG_REPLAY_ARTIFACT).exists()


def test_flag_on_no_research_brief_continues():
    _set_orchestrator(GATE_ON)
    run_dir = _authored_1b("run_974", GOOD)
    assert not (run_dir / "artifacts" / "research_brief.yaml").exists()
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"


# --- the gate itself, on lane 1's configs --------------------------------------

def test_run_085_rewrite_pauses():
    """The case that motivated D-109: 1b dropped the first clip and reported `exact`."""
    run_dir = _gate_run("run_975", LANE1, RUN_085)
    assert rpr._route_config_replay_gate(run_dir) == "human_pause"
    rec = rpr.load_yaml(run_dir / "artifacts" / rpr.CONFIG_REPLAY_ARTIFACT)
    assert rec["verdict"] == "VOID"
    assert sum(s["forecast_or_regime_differences"] for s in rec["series"].values()) > 0


def test_cosmetic_rewrite_continues():
    """Renamed id, a leading identity op, 5.0 for 5: the same forecasts (run_081's case, D-106)."""
    run_dir = _gate_run("run_976", LANE1, COSMETIC)
    assert rpr._route_config_replay_gate(run_dir) == "innovation_expansion"
    rec = rpr.load_yaml(run_dir / "artifacts" / rpr.CONFIG_REPLAY_ARTIFACT)
    assert rec["verdict"] == "VALID" and rec["identical_json"] is False


@pytest.mark.parametrize("brief_cfg,authored,match", [
    ("{not json", LANE1, "does not parse"),
    ("[1, 2]", LANE1, "not a JSON object"),
    (LANE1, None, "backtest_spec.yaml"),
], ids=["bad-json", "not-object", "no-authored"])
def test_fail_closed(brief_cfg, authored, match):
    run_dir = _gate_run("run_977", brief_cfg, authored)
    assert rpr._route_config_replay_gate(run_dir) == "human_pause"
    state = _state(run_dir)
    assert state["flags"][rpr.CONFIG_REPLAY_FLAG] is True
    assert "replay not possible" in state["last_error"] and match in state["last_error"]


def test_series_hash_mismatch_fails_closed(monkeypatch):
    mod = rpr._config_replay_module()
    monkeypatch.setattr(rpr, "_config_replay_module", lambda: mod)
    monkeypatch.setitem(mod.SERIES_SHA256, "series_1.csv", "0" * 64)
    run_dir = _gate_run("run_978", LANE1, LANE1)
    assert rpr._route_config_replay_gate(run_dir) == "human_pause"
    assert "SeriesHashMismatch" in _state(run_dir)["last_error"]


def test_gate_leaves_logging_and_sys_path_as_they_were():
    """Review of PR #394: the replay must not silence logging or grow sys.path in
    the long-lived campaign process."""
    import logging
    before_disable, before_path = logging.root.manager.disable, list(sys.path)
    run_dir = _gate_run("run_979", LANE1, LANE1)
    assert rpr._route_config_replay_gate(run_dir) == "innovation_expansion"
    assert logging.root.manager.disable == before_disable
    assert sys.path == before_path


def test_stale_record_is_removed_when_no_exact_config():
    run_dir = _gate_run("run_980", None, LANE1)
    (run_dir / "artifacts" / rpr.CONFIG_REPLAY_ARTIFACT).write_text("verdict: VOID", encoding="utf-8")
    assert rpr._route_config_replay_gate(run_dir) == "innovation_expansion"
    assert not (run_dir / "artifacts" / rpr.CONFIG_REPLAY_ARTIFACT).exists()
