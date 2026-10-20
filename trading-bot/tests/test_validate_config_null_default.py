"""
V18 (D-160): in threshold_rules mode with empty or missing `rules`, every bar resolves to
`default_regime` (or a veto's result); when that regime is null or missing in
`strategies.regimes` and no veto routes to a non-null one, the config forecasts 0.0 on every
bar. A block's source detector is checked against its `source.parts`.

Minimal pins (fuller tests follow): the refusal and its exact line (top level and block
source); an absent mode / rules / default_regime read as the engine reads them; score and
score_product with the same shape accepted; the normal gated shape and the canonical ungated
shape accepted; a veto routing to a non-null regime accepted; V10's case reported once (V10,
not V18).

All data is synthetic.
"""
import copy
import json

import pytest
from tools.validate_config import validate

ER = "strategies.strategy_components.EfficiencyRatioRegimeComponent"
SMA = "strategies.strategy_components.SmaTrendLongOnlyComponent"
TOP = ("VIOLATION V18 regime_detector.default_regime: 'unknown' in mode 'threshold_rules' with "
       "regime_detector.rules empty or missing, so every bar resolves to 'unknown' (or to a veto's result, "
       "and none holds components) -- but strategies.regimes.unknown is null or missing. This "
       "config forecasts 0.0 on every bar; point default_regime at the regime that holds the "
       "components, or move the components to strategies.regimes.unknown.")


def _cfg(**rd_extra):
    """The gap: detector components kept, rules [], default 'unknown', the strategy on
    'trending' only (so strategies.regimes.unknown is null)."""
    rd = {"mode": "threshold_rules", "default_regime": "unknown", "rules": [],
          "components": [{"id": "er", "class": ER, "params": {"period": 20}}]}
    rd.update(rd_extra)
    return {"regime_detector": {k: v for k, v in rd.items() if v is not ...},
            "strategies": {"regimes": {
                "trending": {"components": [{"id": "s", "class": SMA,
                                             "params": {"lookback_L": 50}, "weight": 1.0}]},
                "unknown": None, "mean_reversion": None, "chop": None}}}


def _v18(cfg):
    return [v for v in validate(cfg) if v.startswith("VIOLATION V18 ")]


def test_the_gap_is_refused_with_the_exact_line():
    assert validate(_cfg()) == [TOP]


@pytest.mark.parametrize("extra", [{"mode": ...}, {"rules": ...}, {"default_regime": ...}])
def test_absent_keys_read_as_the_engine_reads_them(extra):
    # mode absent = threshold_rules, rules absent = none, default_regime absent = unknown
    assert _v18(_cfg(**extra)) == [TOP]


def test_a_missing_strategies_key_counts_as_null():
    cfg = _cfg()
    del cfg["strategies"]["regimes"]["unknown"]
    assert _v18(cfg) == [TOP]


@pytest.mark.parametrize("mode", ["score", "score_product"])
def test_score_modes_with_the_same_shape_are_accepted(mode):
    assert _v18(_cfg(mode=mode)) == []


def test_the_normal_gated_shape_is_accepted():
    rules = [{"regime": "trending", "any_of": [[{"id": "er", "op": "gte", "value": 0.4}]]}]
    assert validate(_cfg(rules=rules)) == []


def test_the_canonical_ungated_shape_is_accepted():
    assert validate(_cfg(default_regime="trending")) == []


def test_a_veto_routing_to_a_non_null_regime_is_accepted_and_one_to_a_null_is_not():
    veto = {"id": "er", "rules": [{"op": "gt", "value": 0.5}], "result": "trending"}
    assert validate(_cfg(vetoes=[veto])) == []
    assert _v18(_cfg(vetoes=[dict(veto, result="chop")])) == [TOP]


def test_v10s_case_is_reported_once_by_v10():
    errs = validate(_cfg(components=[]))
    assert [e.split()[1] for e in errs] == ["V10"]


def test_an_explicit_null_or_bad_name_is_v7s_only():
    for bad in (None, "sideways"):
        errs = validate(_cfg(default_regime=bad))
        assert errs and all(e.startswith("VIOLATION V7 ") for e in errs), errs


def _block_cfg(source_detector, parts=None):
    pe = "strategies.strategy_components.PriceEvolutionComponent"
    cfg = _cfg(default_regime="trending")
    cfg["strategies"]["regimes"]["trending"] = {
        "components": [{"id": "b0__x", "class": pe, "params": {"period": 5}, "weight": 1.0,
                        "lookback": 60, "transforms": [{"op": "identity"}]}],
        "blocks": [{"id": "b0", "weight": 1.0, "components": ["b0__x"],
                    "source": {"required_bars": 24, "warmup": 10, "buffer_bars": 124,
                               "regime_detector": source_detector,
                               "parts": parts or {"trending": ["b0__x"]}}}],
        "block_standardisation": {"target": 10.0, "window": 100, "min_periods": 30}}
    return cfg


def test_a_block_source_detector_is_checked_against_its_parts():
    det = copy.deepcopy(_cfg()["regime_detector"])                 # default 'unknown'
    loc = "strategies.regimes.trending.blocks[0].source"
    assert _v18(_block_cfg(det)) == [
        f"VIOLATION V18 {loc}.regime_detector.default_regime: 'unknown' in mode 'threshold_rules' "
        f"with the source detector's rules empty, so every bar resolves to 'unknown' (or to a "
        f"veto's result, and none is in source.parts) -- but {loc}.parts has no 'unknown' entry. "
        f"This block abstains on every bar (contributes 0); point default_regime at a regime of "
        f"source.parts."]
    assert _v18(_block_cfg(det, parts={"unknown": ["b0__x"]})) == []
    assert _v18(_block_cfg(dict(det, mode="score"))) == []


def test_a_block_source_veto_routing_into_parts_is_accepted():
    # ruling (a), for a block: a veto whose result is a regime of source.parts keeps the block
    # contributing, so there is no V18 even though the default 'unknown' is not in parts
    det = copy.deepcopy(_cfg()["regime_detector"])                 # default 'unknown'
    veto = {"id": "er", "rules": [{"op": "gt", "value": 0.5}], "result": "trending"}
    assert _v18(_block_cfg(dict(det, vetoes=[veto]))) == []
    assert len(_v18(_block_cfg(dict(det, vetoes=[dict(veto, result="chop")])))) == 1


def test_a_block_source_with_rules_missing_is_checked_like_empty_rules():
    det = copy.deepcopy(_cfg()["regime_detector"])
    del det["rules"]                                               # missing = no rules
    loc = "strategies.regimes.trending.blocks[0].source"
    (line,) = _v18(_block_cfg(det))
    assert line.startswith(f"VIOLATION V18 {loc}.regime_detector.default_regime: 'unknown' ")
    assert _v18(_block_cfg(det, parts={"unknown": ["b0__x"]})) == []
    # and with a default that is in parts, nothing at all
    assert _v18(_block_cfg(dict(det, default_regime="trending"))) == []


def test_advanced_strategy_construction_refuses_a_v18_config(tmp_path):
    from strategies.main_strategy import AdvancedStrategy
    path = tmp_path / "strategy_config.json"
    path.write_text(json.dumps(_cfg()), encoding="utf-8")
    assert _v18(_cfg())                                            # the fixture is a V18 config
    with pytest.raises(ValueError, match="invalid strategy_config"):
        AdvancedStrategy(config_path=str(path))


def test_advanced_strategy_construction_accepts_the_same_config_pointed_at_the_regime(tmp_path):
    from strategies.main_strategy import AdvancedStrategy
    path = tmp_path / "strategy_config.json"
    path.write_text(json.dumps(_cfg(default_regime="trending")), encoding="utf-8")
    AdvancedStrategy(config_path=str(path))
