"""
V17 (D-158): validate_config refuses a non-empty `transforms` / `history_transforms` list on a
detector component (`regime_detector.components[j]`, at the top level or in a block's source
detector). The engine never reads them (strategies/regime_engine.py: detector components have no
transforms), so before V17 such a config passed every check while the run measured an unchanged
strategy.

Pins: the refusal and its exact line, at the exact location, once per list, for `transforms` and
`history_transforms`, top level and block source; the same transform on a veto, on a score-mode
regime component and on a strategy component draws no V17 line; an empty list draws none; the
other checks that walk the lists now also see the detector lists (V3 and V16 shown); a config
without the lists is unchanged; AdvancedStrategy construction (which calls validate) refuses such
a config.

All data is synthetic.
"""
import json

import pytest
from strategies.main_strategy import AdvancedStrategy
from tools.validate_config import validate

ER = "strategies.strategy_components.EfficiencyRatioRegimeComponent"
SMA = "strategies.strategy_components.SmaTrendLongOnlyComponent"
IDENT = {"op": "identity"}
MSG = ("detector components take no transforms (the engine ignores them: regime_engine.py); "
       "put the transform on a veto, on a score-mode regime component, or on a strategy component")


def _detector(comp=None, veto=None, score=None):
    """A well-formed threshold_rules detector; each argument is a dict of extra keys put on the
    detector component `er`, the veto on it, and the score-mode regime component."""
    return {
        "mode": "threshold_rules", "default_regime": "unknown", "rules": [],
        "components": [dict({"id": "er", "class": ER, "params": {"period": 20}}, **(comp or {}))],
        "vetoes": [dict({"id": "er", "rules": [{"op": "gt", "value": 0.5}], "result": "chop"},
                        **(veto or {}))],
        "regimes": {"trending": {"components": [
            dict({"id": "er", "class": ER, "params": {"period": 20}}, **(score or {}))]}}}


def _cfg(detector, strat=None):
    return {"regime_detector": detector, "strategies": {"regimes": {
        "unknown": {"components": [dict({"id": "s", "class": SMA, "params": {"lookback_L": 50},
                                         "weight": 1.0}, **(strat or {}))]},
        "trending": None, "mean_reversion": None, "chop": None}}}


def _block_cfg(detector):
    """A well-formed one-block composite whose block source detector is `detector`."""
    pe = "strategies.strategy_components.PriceEvolutionComponent"
    cfg = _cfg(_detector())
    cfg["strategies"]["regimes"]["unknown"] = {
        "components": [{"id": "b0__x", "class": pe, "params": {"period": 5}, "weight": 1.0,
                        "lookback": 60, "transforms": [IDENT]}],
        "blocks": [{"id": "b0", "weight": 1.0, "components": ["b0__x"],
                    "source": {"required_bars": 24, "warmup": 10, "buffer_bars": 124,
                               "regime_detector": detector,
                               "parts": {"unknown": ["b0__x"]}}}],
        "block_standardisation": {"target": 10.0, "window": 100, "min_periods": 30}}
    return cfg


def _v(violations, code):
    return [v for v in violations if v.startswith(f"VIOLATION {code}")]


def test_the_fixtures_validate_clean():
    assert validate(_cfg(_detector())) == []
    assert validate(_block_cfg(_detector())) == []


@pytest.mark.parametrize("key", ["transforms", "history_transforms"])
def test_a_detector_component_list_is_refused_once_at_its_location(key):
    got = validate(_cfg(_detector(comp={key: [IDENT, IDENT]})))
    assert got == [f"VIOLATION V17 regime_detector.components[0].{key}: {MSG}"]


def test_both_lists_on_one_component_give_one_line_each():
    got = validate(_cfg(_detector(comp={"transforms": [IDENT], "history_transforms": [IDENT]})))
    assert got == [
        f"VIOLATION V17 regime_detector.components[0].transforms: {MSG}",
        f"VIOLATION V17 regime_detector.components[0].history_transforms: {MSG}"]


def test_the_location_names_the_component_index():
    det = _detector()
    det["components"].append({"id": "er2", "class": ER, "params": {"period": 10},
                              "transforms": [IDENT]})
    assert _v(validate(_cfg(det)), "V17") == [
        f"VIOLATION V17 regime_detector.components[1].transforms: {MSG}"]


@pytest.mark.parametrize("key", ["transforms", "history_transforms"])
def test_a_block_source_detector_component_list_is_refused_once(key):
    got = validate(_block_cfg(_detector(comp={key: [IDENT]})))
    loc = (f"strategies.regimes.unknown.blocks[0].source.regime_detector.components[0].{key}")
    assert got == [f"VIOLATION V17 {loc}: {MSG}"]


def test_the_same_transform_elsewhere_draws_no_v17_line():
    # veto, score-mode regime component, strategy component (transforms and history_transforms)
    cfg = _cfg(_detector(veto={"transforms": [IDENT]},
                         score={"transforms": [IDENT], "history_transforms": [IDENT]}),
               strat={"transforms": [IDENT], "history_transforms": [IDENT]})
    assert _v(validate(cfg), "V17") == []
    # and in a block source detector: veto and score-mode component
    bcfg = _block_cfg(_detector(veto={"transforms": [IDENT]}, score={"transforms": [IDENT]}))
    assert _v(validate(bcfg), "V17") == []


def test_an_empty_or_absent_list_draws_no_v17_line():
    assert validate(_cfg(_detector(comp={"transforms": [], "history_transforms": []}))) == []
    assert validate(_cfg(_detector(comp={"transforms": None}))) == []


def test_v17_changes_nothing_on_a_config_without_the_lists():
    base = _cfg(_detector(veto={"transforms": [IDENT]}, score={"transforms": [IDENT]}),
                strat={"transforms": [IDENT]})
    assert validate(base) == []


@pytest.mark.parametrize("bad_components", [[None], ["x"], [[]], None])
def test_a_malformed_detector_components_entry_does_not_raise_in_the_list_walk(bad_components):
    from tools.validate_config import _all_transform_lists
    cfg = _cfg(_detector())
    cfg["regime_detector"]["components"] = bad_components
    assert [loc for loc, _ in _all_transform_lists(cfg)
            if loc.startswith("regime_detector.components[")] == []


def test_the_other_walking_checks_now_also_see_the_detector_lists():
    # V3 (op in registry) and V16 (signed_power placement) walk _all_transform_lists, so
    # they now also report on a detector component list; V17 comes in addition
    cfg = _cfg(_detector(comp={"transforms": [{"op": "no_such_op"},
                                              {"op": "signed_power", "params": {"exponent": 2}}]}))
    got = validate(cfg)
    loc = "regime_detector.components[0].transforms"
    assert _v(got, "V3") == [f"VIOLATION V3 {loc}[0].op: 'no_such_op' not in TRANSFORM_OPS_REGISTRY"]
    assert [v.split(":")[0] for v in _v(got, "V16")] == [f"VIOLATION V16 {loc}[1]"]
    assert _v(got, "V17") == [f"VIOLATION V17 {loc}: {MSG}"]


def test_advanced_strategy_construction_refuses_the_config(tmp_path):
    path = tmp_path / "strategy_config.json"
    path.write_text(json.dumps(_cfg(_detector(comp={"transforms": [IDENT]}))), encoding="utf-8")
    with pytest.raises(ValueError, match="invalid strategy_config"):
        AdvancedStrategy(config_path=str(path))


def test_advanced_strategy_construction_accepts_the_same_config_without_the_list(tmp_path):
    path = tmp_path / "strategy_config.json"
    path.write_text(json.dumps(_cfg(_detector())), encoding="utf-8")
    AdvancedStrategy(config_path=str(path))
