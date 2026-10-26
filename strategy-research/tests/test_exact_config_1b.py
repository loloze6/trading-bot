"""
D-110: orchestrator.exact_config_1b (off by default, no dependency).

With the flag on, a run whose research_brief.yaml carries an exact config gets
step 1b written by code: the config and the brief's exact block manifest are
copied unchanged, with no model call. A missing or broken manifest, or a broken
config, refuses before anything is written. Step 1a is unchanged, and every
check after 1b runs on what the code wrote. Off: 1b is the model call as before.
"""
import copy
import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import block_manifest as bm  # noqa: E402
import nearest_build as nb  # noqa: E402

from _reader_test_helpers import _set_orchestrator  # noqa: E402
from test_e056_1b_block_manifest import CONFIG, GOOD, HANDOFF_1B, _minimal_run  # noqa: E402

CDA = {"config_direct_authoring": {"enabled": True}}
ON = {**CDA, "exact_config_1b": {"enabled": True}}
NB_ON = {**ON, "claim_tests": {"enabled": True}, "nearest_build": {"enabled": True},
         "deviation_gate": {"enabled": True}}

# Lane 1's v3 configs (briefs/L1_daily_trend_basket_sma{50,100,200}_v3.md) and the
# block manifest shape every accepted lane-1 1b answer wrote (runs 081-086).
def _lane1(period):
    return {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                                "default_regime": "unknown"},
            "strategies": {"regimes": {"unknown": {"components": [{
                "id": "trend", "class": "strategies.strategy_components.MovingAverageDistanceComponent",
                "params": {"period": period, "average": "sma"}, "weight": 1.0,
                "transforms": [{"op": "scale", "params": {"factor": 5}},
                               {"op": "clip", "params": {"min": 0, "max": 10}},
                               {"op": "vol_target", "params": {"window": 60, "target_annual_vol": 0.4,
                                                               "periods_per_year": 365}},
                               {"op": "clip", "params": {"min": 0, "max": 10}}]}]},
                "trending": None, "mean_reversion": None, "chop": None}}}


LANE1_MANIFEST = {"block": {"kind": "forecast",
                            "config_paths": ["/strategies/regimes/unknown/components/0"]},
                  "scaffolding": ["/regime_detector"],
                  "rationale": "the distance-from-SMA component with its transform pipeline is "
                               "the idea; the ungated regime detector is scaffolding"}


def _brief(run_dir, config=CONFIG, manifest=GOOD):
    cons = []
    if config is not None:
        text = config if isinstance(config, str) else json.dumps(config)
        cons.append(rpr.BRIEF_EXACT_CONFIG_PREFIX + ", nothing added:\n" + text)
    if manifest is not None:
        text = manifest if isinstance(manifest, str) else json.dumps(manifest)
        cons.append(rpr.BRIEF_EXACT_MANIFEST_PREFIX + ":\n" + text)
    cons.append("Variants: the base only.")
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"strategy_domain": "time_series_trend", "constraints": cons})


def _run(run_id, **brief_kw):
    run_dir = _minimal_run(rpr.ROOT, run_id)
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text("hypothesis_id: H-1\n",
                                                                 encoding="utf-8")
    if brief_kw.get("no_brief") is not True:
        _brief(run_dir, **{k: v for k, v in brief_kw.items() if k != "no_brief"})
    return run_dir


def _arts(run_dir):
    return run_dir / "artifacts"


# --- the flag ---------------------------------------------------------------

def test_flag_off_by_default_and_in_the_shipped_config():
    _set_orchestrator(CDA)
    assert rpr._exact_config_1b_enabled() is False
    shipped = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    assert shipped["orchestrator"]["exact_config_1b"]["enabled"] is False
    _set_orchestrator(ON)
    assert rpr._exact_config_1b_enabled() is True


@pytest.mark.parametrize("bad", ["true", 1, None])
def test_flag_non_bool_raises(bad):
    _set_orchestrator({**CDA, "exact_config_1b": {"enabled": bad}})
    with pytest.raises(ValueError, match="not a real boolean"):
        rpr._exact_config_1b_enabled()


def test_flag_is_registered_everywhere():
    reg = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml").read_text(encoding="utf-8"))
    [entry] = [f for f in reg["flags"] if f["name"] == "exact_config_1b"]
    assert entry["config_key"] == "orchestrator.exact_config_1b.enabled"
    assert entry["reader"] == "run_phase1_research._exact_config_1b_enabled"
    assert camp._flag_readers()["exact_config_1b"] is rpr._exact_config_1b_enabled


def test_flag_off_mode_reads_nothing_but_the_flag(monkeypatch):
    _set_orchestrator(CDA)
    run_dir = _run("run_960")
    monkeypatch.setattr(rpr, "_brief_exact_config", lambda p: pytest.fail("flag off must read nothing"))
    assert rpr._exact_config_1b_mode(run_dir) is False


# --- the code-written 1b ------------------------------------------------------

def test_writes_the_brief_config_and_manifest_unchanged():
    _set_orchestrator(ON)
    run_dir = _run("run_961")
    rpr._exact_config_1b(run_dir, "run_961")
    spec = rpr.load_yaml(_arts(run_dir) / "backtest_spec.yaml")
    assert spec["status"] == "spec_ready" and spec["hypothesis_id"] == "H-1"
    assert rpr._canonical_json_sha256(spec["config"]) == rpr._canonical_json_sha256(CONFIG)
    manifest = rpr.load_yaml(_arts(run_dir) / bm.MANIFEST_FILENAME)
    assert rpr._canonical_json_sha256(manifest) == rpr._canonical_json_sha256(GOOD)
    decision = rpr.load_yaml(_arts(run_dir) / "decision.yaml")
    assert decision["status"] == "spec_ready" and not decision.get("deviations")
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"


def test_nearest_build_reads_exact_and_the_deviation_gate_passes():
    _set_orchestrator(NB_ON)
    run_dir = _run("run_962")
    rpr._exact_config_1b(run_dir, "run_962")
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert nb.load_record(_arts(run_dir))["status"] == nb.STATUS_EXACT


@pytest.mark.parametrize("period", [50, 100, 200])
def test_lane1_configs_fit_the_lane1_manifest(period):
    """The manifest the v3 briefs will carry fits each lookback's config (D-110)."""
    bm.check_manifest(LANE1_MANIFEST, _lane1(period), error_cls=RuntimeError)
    _set_orchestrator(ON)
    run_dir = _run(f"run_96{period // 50}", config=_lane1(period), manifest=LANE1_MANIFEST)
    rpr._exact_config_1b(run_dir, run_dir.name)
    assert rpr.load_yaml(_arts(run_dir) / "backtest_spec.yaml")["config"] == _lane1(period)


@pytest.mark.parametrize("kw,match", [
    ({"manifest": None}, "no exact block manifest"),
    ({"config": "{not json"}, "does not parse"),
    ({"manifest": "{not json"}, "does not parse"),
    ({"manifest": "[1]"}, "not a JSON object"),
    ({"manifest": {**GOOD, "block": {"kind": "forecast",
                                     "config_paths": ["/strategies/regimes/unknown/components/3"]}}},
     "not resolve"),
], ids=["no-manifest", "bad-config-json", "bad-manifest-json", "manifest-not-object", "manifest-misfit"])
def test_broken_input_refuses_before_writing(kw, match):
    _set_orchestrator(ON)
    run_dir = _run("run_966", **kw)
    with pytest.raises(RuntimeError, match=match):
        rpr._exact_config_1b(run_dir, "run_966")
    for f in ("backtest_spec.yaml", "decision.yaml", bm.MANIFEST_FILENAME):
        assert not (_arts(run_dir) / f).exists()


# --- through run_loop: which 1b runs -------------------------------------------

def _loop(monkeypatch, run_dir):
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = "strategy_config_authoring"
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    tpl = SR_ROOT / "workflow_artifacts" / "templates" / "handoffs" / HANDOFF_1B.name
    (run_dir / "handoffs").mkdir(exist_ok=True)
    shutil.copy(tpl, run_dir / "handoffs" / HANDOFF_1B.name)
    docs = rpr.ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "COMPONENT_CATALOG.md").write_text("catalogue\n", encoding="utf-8")
    (docs / "STRATEGY_DESIGN_GUIDE.md").write_text("guide\n", encoding="utf-8")
    seen = []

    async def _fake_invoke(stage_name, run_id, retry_context=None):
        seen.append(stage_name)

    monkeypatch.setattr(rpr, "async_invoke_agent", _fake_invoke)
    real_route, routes = rpr.determine_post_strategy_config_authoring_route, []

    def _route_then_stop(path, **kw):  # the real route, then stop the loop before step 2
        routes.append(real_route(path, **kw))
        return "human_pause"

    monkeypatch.setattr(rpr, "determine_post_strategy_config_authoring_route", _route_then_stop)
    rpr.run_loop(run_dir.name)
    seen.extend(f"route:{r}" for r in routes)
    return seen


def test_run_loop_flag_on_exact_brief_makes_no_1b_call(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _run("run_967")
    seen = _loop(monkeypatch, run_dir)
    assert seen == ["route:innovation_expansion"]  # no model call; the real route accepts it
    spec = rpr.load_yaml(_arts(run_dir) / "backtest_spec.yaml")
    assert spec["config"] == CONFIG


def test_run_loop_flag_on_without_exact_config_calls_the_model(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _run("run_968", config=None, manifest=None)
    seen = _loop(monkeypatch, run_dir)
    assert seen[0] == "strategy_config_authoring"


def test_run_loop_flag_off_exact_brief_calls_the_model(monkeypatch):
    _set_orchestrator(CDA)
    run_dir = _run("run_969")
    seen = _loop(monkeypatch, run_dir)
    assert seen[0] == "strategy_config_authoring"


def test_run_loop_broken_manifest_fails_before_any_call(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _run("run_970", manifest=None)
    seen = _loop(monkeypatch, run_dir)
    assert seen == []
    final = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert final["status"] == "failed" and "no exact block manifest" in final["last_error"]
    assert not (_arts(run_dir) / "backtest_spec.yaml").exists()


# --- review of PR #396 ------------------------------------------------------------

def test_stale_model_deviations_are_cleared_run_086_shape():
    """run_086's model attempts left deviations.yaml at `approximation`; the
    code-written 1b must not be judged on it."""
    _set_orchestrator(NB_ON)
    run_dir = _run("run_971")
    rpr.save_yaml(_arts(run_dir) / nb.DEVIATIONS_FILE,
                  {"schema_version": 1, "run_id": "run_971", "status": "approximation",
                   "information_only": True, "deviations": [{"clause": "x"}],
                   "config_rationale_lines": []})
    rpr._exact_config_1b(run_dir, "run_971")
    assert not (_arts(run_dir) / nb.DEVIATIONS_FILE).exists()
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert nb.load_record(_arts(run_dir))["status"] == nb.STATUS_EXACT


def test_refusal_leaves_stale_files_untouched():
    _set_orchestrator(NB_ON)
    run_dir = _run("run_972", manifest=None)
    rpr.save_yaml(_arts(run_dir) / nb.DEVIATIONS_FILE, {"status": "approximation"})
    with pytest.raises(RuntimeError):
        rpr._exact_config_1b(run_dir, "run_972")
    assert (_arts(run_dir) / nb.DEVIATIONS_FILE).exists()


def test_run_loop_broken_config_json_fails_with_the_d110_message(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _run("run_973", config="{not json")
    seen = _loop(monkeypatch, run_dir)
    assert seen == []
    final = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert final["status"] == "failed" and "[D-110]" in final["last_error"]
    assert "does not parse" in final["last_error"]


def test_pass_through_candidate_with_exact_config_refuses(monkeypatch):
    _set_orchestrator(ON)
    run_dir = _run("run_974")
    monkeypatch.setattr(rpr, "_is_pass_through_candidate", lambda arts: True)
    with pytest.raises(RuntimeError, match="pass-through"):
        rpr._exact_config_1b(run_dir, "run_974")
    assert not (_arts(run_dir) / "backtest_spec.yaml").exists()
