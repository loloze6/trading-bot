"""
D-149 standardised forecast rule (tools/forecast_rules.py) and its wiring.

Covers:
  1. a component in `strategies` whose only scale is a bare `scale` op (in
     `transforms` or `history_transforms`) or a `scaling_factor` param is refused;
  2. it passes with a `standardise` op, with a `vol_target` op, or in a regime
     with both `blocks` and `block_standardisation`; a component with no scale
     passes; the regime detector is not checked;
  3. the message is exactly "D-149: <loc> (id 'x') -- " + RULE_SENTENCE, and
     RULE_SENTENCE is byte-for-byte in the design guide and the
     strategy-config-authoring skill;
  4. both doors apply it: right after 1b, and at 5a on the config after the patch.

No LLM, no backtest. tests/conftest.py sandboxes rpr.ROOT.
"""
import copy
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import forecast_rules as fr  # noqa: E402

from test_d051_d053_forecast_rules import (  # noqa: E402
    CONFIG, COMP0, _authored_1b, _cfg, _design, _refusals, _run_5a)
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402

GUIDE = SR_ROOT / "docs" / "STRATEGY_DESIGN_GUIDE.md"
SKILL = SR_ROOT / "workflow_artifacts" / "skills" / "strategy-config-authoring" / "SKILL.md"
EXPECTED_SENTENCE = (
    "Standardised forecast (hard rule). Every component in strategies ends its transforms with "
    "standardise (past values only, target 10, cap 20, window, min_periods), unless its scale is "
    "set by vol_target or the regime is a blocks regime with block_standardisation. A bare scale "
    "or scaling_factor as the only scale is refused after 1b and again at 5a.")
STANDARDISE = {"op": "standardise", "params": {"window": 100, "min_periods": 30}}
SCALE10 = {"op": "scale", "params": {"factor": 10.0}}
LOC = "strategies.regimes.unknown.components[0]"


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _d149(config) -> list:
    return [m for m in fr.strategies_violations(config, fr.on_off_classes()) if m.startswith("D-149:")]


def _scaled(**overrides) -> dict:
    return _cfg(**overrides)


# 1. refused ------------------------------------------------------------------

def test_bare_scale_in_transforms_is_refused():
    assert len(_d149(_scaled(transforms=[{"op": "ratio_to_mean"}, SCALE10]))) == 1


def test_bare_scale_in_history_transforms_is_refused():
    assert len(_d149(_scaled(history_transforms=[SCALE10], transforms=[{"op": "identity"}]))) == 1


def test_scaling_factor_param_only_is_refused():
    assert len(_d149(_scaled(params={"period": 14, "scaling_factor": 0.4}))) == 1


# 2. passes -------------------------------------------------------------------

def test_standardise_passes_alone_and_with_a_scale_after_it():
    assert _d149(_scaled(transforms=[STANDARDISE])) == []
    assert _d149(_scaled(transforms=[STANDARDISE, SCALE10],
                         params={"period": 14, "scaling_factor": 0.4})) == []


def test_vol_target_passes():
    assert _d149(_scaled(transforms=[{"op": "vol_target"}, SCALE10])) == []
    assert _d149(_scaled(transforms=[{"op": "vol_target"}],
                         params={"period": 14, "scaling_factor": 0.4})) == []


def test_blocks_regime_with_block_standardisation_passes():
    cfg = _scaled(transforms=[SCALE10], params={"period": 14, "scaling_factor": 0.4})
    cfg["strategies"]["regimes"]["unknown"]["blocks"] = [{"id": "b"}]
    assert len(_d149(cfg)) == 1  # blocks alone is not enough
    cfg["strategies"]["regimes"]["unknown"]["block_standardisation"] = {"target": 10}
    assert _d149(cfg) == []


def test_a_component_with_no_scale_passes():
    assert _d149(CONFIG) == []
    assert _d149(_scaled(transforms=[{"op": "identity"}])) == []


def test_the_regime_detector_is_not_checked():
    cfg = copy.deepcopy(CONFIG)
    cfg["regime_detector"]["components"][0]["params"]["scaling_factor"] = 2.0
    cfg["regime_detector"]["components"][0]["transforms"] = [SCALE10]
    assert _d149(cfg) == []


def test_malformed_pieces_are_skipped():
    cfg = copy.deepcopy(CONFIG)
    cfg["strategies"]["regimes"]["chop"] = {"components": ["x", {"transforms": "y", "params": "z"}]}
    cfg["strategies"]["regimes"]["trending"] = "not a dict"
    assert _d149(cfg) == []
    assert _d149({"strategies": []}) == []


# 3. the sentence -------------------------------------------------------------

def test_message_is_the_location_and_the_rule_sentence():
    cfg = _scaled(id="x", transforms=[SCALE10])
    assert fr.RULE_SENTENCE == EXPECTED_SENTENCE
    assert _d149(cfg) == [f"D-149: {LOC} (id 'x') -- " + EXPECTED_SENTENCE]


@pytest.mark.parametrize("path", [GUIDE, SKILL], ids=["guide", "skill"])
def test_rule_sentence_is_byte_for_byte_in_the_guide_and_the_skill(path):
    assert path.read_bytes().count(EXPECTED_SENTENCE.encode("utf-8")) == 1


# 4. the two doors ------------------------------------------------------------

def test_post_1b_door_sends_a_bare_scale_config_back_to_1b_with_the_sentence():
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _authored_1b("run_920", _scaled(transforms=[SCALE10]))
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    retry = rpr.load_yaml(run_dir / "pipeline_state.yaml")["block_manifest_retry"]
    assert retry["last_check"] == "forecast_rules"
    assert f"D-149: {LOC} (id 'rsi') -- " + EXPECTED_SENTENCE in retry["last_error"]
    assert [r["variant_id"] for r in _refusals(run_dir)] == ["base"]


def test_5a_door_refuses_a_bare_scale_variant_and_passes_a_standardised_one(monkeypatch):
    variants = _run_5a(monkeypatch, "run_921", CONFIG, [
        _design("bare_scale", [{"path": COMP0 + "/transforms/1", "value": SCALE10}]),
        _design("scaling_factor", [{"path": COMP0 + "/params/scaling_factor", "value": 0.4}]),
        _design("standardised", [{"path": COMP0 + "/transforms/1", "value": STANDARDISE}]),
    ])
    assert variants["base"]["status"] == "validated"
    assert variants["standardised"]["status"] == "validated"
    for vid in ("bare_scale", "scaling_factor"):
        assert variants[vid]["status"] == "not_tested", vid
        assert variants[vid]["reason"] == rpr.FORECAST_RULE_REASON
        assert variants[vid]["report"].endswith(EXPECTED_SENTENCE), vid
    refusals = _refusals(rpr.ROOT / "runs" / "run_921")
    assert sorted(r["variant_id"] for r in refusals) == ["bare_scale", "scaling_factor"]
