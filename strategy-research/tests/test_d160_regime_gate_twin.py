"""D-160 (vehicle-format V1d): a config vehicle whose idea combines as a regime gate.

1. The gate form (config_vehicle.gate_form_errors), only with `combines_as: regime_gate`:
   mode threshold_rules, a non-empty regime_detector.rules or vetoes, exactly one non-null
   strategies.regimes entry; else a refusal naming what is missing.
2. The ungated twin (config_vehicle.ungated_twin, D-052): rules [], vetoes dropped,
   default_regime the single non-null regime, everything else kept; pure.
3. The twin is checked like the config (validate_config incl. V18, D-051/D-149); a twin
   failure is a refusal naming the twin.
4. The wiring, with reader_proposals.CONFIG_VEHICLE_ROUTED forced on; off, unchanged (the old
   patch-list refusal).

Minimal pins (fuller tests follow). No LLM, no backtest, no market data.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import config_vehicle as cv  # noqa: E402
import reader_proposals as rp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

from test_d051_d053_forecast_rules import CONFIG, MANIFEST  # noqa: E402
from test_e077_pr2_confirm import CAT, _claim, _reading  # noqa: E402

GATE = {"combines_as": "regime_gate", "fold_observed": "A"}
RULE = {"regime": "trending", "any_of": [[{"id": "er", "op": "gte", "value": 0.4}]]}
VETO = {"id": "er", "transforms": [], "rules": [{"op": "lt", "value": 0.1}], "result": "chop",
        "consecutive_bars": 2}
OLD_MESSAGE = ("vehicle: must be a non-empty list of changes (omit it when the finding needs "
               "no config change)")


def _gated(rules=(RULE,), vetoes=(VETO,)) -> dict:
    """CONFIG's strategy moved to 'trending', traded only when the rule (or no veto) says so."""
    cfg = copy.deepcopy(CONFIG)
    regimes = cfg["strategies"]["regimes"]
    regimes["trending"], regimes["unknown"] = regimes["unknown"], None
    cfg["regime_detector"]["rules"] = copy.deepcopy(list(rules))
    cfg["regime_detector"]["vetoes"] = copy.deepcopy(list(vetoes))
    return cfg


def _vehicle(config) -> dict:
    return {"kind": "config", "config": config}


def _errors(config, combines_as="regime_gate") -> list:
    return cv.config_vehicle_errors(_vehicle(config), "v", combines_as=combines_as)


# ---------------------------------------------------------------------------
# 1. the gate form
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rules,vetoes", [((RULE,), (VETO,)), ((RULE,), ()), ((), (VETO,))])
def test_the_gate_form_passes_with_rules_or_vetoes(rules, vetoes):
    cfg = _gated(rules, vetoes)
    if not rules:   # a vetoes-only gate trades by default and vetoes into a null regime
        cfg["regime_detector"]["default_regime"] = "trending"
    assert _errors(cfg) == []


def test_a_vetoes_only_gate_whose_default_is_null_is_v18s():
    (err,) = _errors(_gated((), (VETO,)))          # every bar 'unknown' or 'chop': both null
    assert err.startswith("v.config: VIOLATION V18 regime_detector.default_regime: 'unknown' ")


def test_no_gate_is_refused():
    cfg = _gated((), ())
    cfg["regime_detector"]["default_regime"] = "trending"   # else V18 (a dead config) too
    assert _errors(cfg) == [
        "v.config.regime_detector: combines_as regime_gate needs the gate, a non-empty "
        "regime_detector.rules or regime_detector.vetoes, and both are empty, missing or not a "
        "list; write the gate, or choose another combines_as"]
    del cfg["regime_detector"]["rules"], cfg["regime_detector"]["vetoes"]
    assert len(_errors(cfg)) == 1


def test_not_exactly_one_trading_regime_is_refused():
    cfg = _gated()
    cfg["strategies"]["regimes"]["unknown"] = copy.deepcopy(cfg["strategies"]["regimes"]["trending"])
    assert _errors(cfg) == [
        "v.config.strategies.regimes: combines_as regime_gate needs exactly one non-null regime "
        "(the regime the gate trades in), and this config has 2 ['unknown', 'trending']; set "
        "every other regime to null"]
    assert cv.gate_form_errors({"regime_detector": {"rules": [RULE]},
                                "strategies": {"regimes": {"trending": None}}}, "c") == [
        "c.strategies.regimes: combines_as regime_gate needs exactly one non-null regime (the "
        "regime the gate trades in), and this config has 0 []; set every other regime to null"]


@pytest.mark.parametrize("mode", ["score", "score_product"])
def test_a_mode_other_than_threshold_rules_is_refused(mode):
    form = cv.gate_form_errors(dict(_gated(), regime_detector=dict(_gated()["regime_detector"],
                                                                     mode=mode)), "c")
    assert form == [f"c.regime_detector.mode={mode!r}: combines_as regime_gate needs mode "
                    f"threshold_rules (the default): its ungated twin (D-052) empties the rules "
                    f"and sets default_regime, which only threshold_rules mode reads"]


@pytest.mark.parametrize("word", ["forecast_block", "execution_rule", "knowledge_only", None])
def test_the_form_applies_to_regime_gate_only(word):
    assert _errors(copy.deepcopy(CONFIG), word) == []          # ungated, several words: no form
    assert _errors(copy.deepcopy(CONFIG))                       # the same config as a gate: refused


def test_a_vetoes_only_gate_with_a_null_default_and_a_veto_into_the_trading_regime_passes():
    # ruling (a): V18 does not fire when a veto's result names a trading regime. Through the
    # whole gate path: form, config checks and twin all pass; the twin trades in 'trending'
    cfg = _gated((), (dict(VETO, result="trending"),))
    assert cfg["strategies"]["regimes"]["unknown"] is None      # default 'unknown' is null
    assert cfg["regime_detector"]["default_regime"] == "unknown"
    assert cv.gate_form_errors(cfg, "c") == []
    assert _errors(cfg) == []
    twin = cv.ungated_twin(cfg)
    assert twin["regime_detector"]["default_regime"] == "trending"
    assert twin["regime_detector"]["rules"] == [] and "vetoes" not in twin["regime_detector"]


def test_the_kill_switch_shape_passes_and_its_twin_keeps_the_default():
    # rules route to a null regime (the 'off' state), default 'unknown' holds the strategy
    cfg = copy.deepcopy(CONFIG)
    cfg["regime_detector"]["rules"] = [dict(RULE, regime="chop")]
    assert cfg["strategies"]["regimes"]["chop"] is None
    assert cfg["regime_detector"]["default_regime"] == "unknown"
    assert _errors(cfg) == []
    twin = cv.ungated_twin(cfg)
    assert twin["regime_detector"]["default_regime"] == "unknown"
    assert twin["regime_detector"]["rules"] == []


_NOT_A_LIST = ("combines_as regime_gate needs the gate, a non-empty regime_detector.rules or "
               "regime_detector.vetoes, and both are empty, missing or not a list; write the gate, "
               "or choose another combines_as")


def test_gate_form_errors_never_raises_on_a_malformed_config():
    # a model-written config: every shape comes back as messages, never an exception
    good = _gated()
    bad_inputs = [None, [], "x", 5,
                  {"regime_detector": None, "strategies": None},
                  {"regime_detector": [], "strategies": {"regimes": []}},
                  dict(good, regime_detector=dict(good["regime_detector"], mode=["score"])),
                  dict(good, regime_detector=dict(good["regime_detector"], mode=None)),
                  dict(good, regime_detector=dict(good["regime_detector"], rules={"a": 1},
                                                  vetoes=None)),
                  dict(good, strategies={"regimes": ["trending"]}),
                  dict(good, strategies={"regimes": None})]
    for cfg in bad_inputs:
        errs = cv.gate_form_errors(cfg, "c")
        assert isinstance(errs, list) and errs and all(isinstance(e, str) for e in errs), cfg
        with pytest.raises(ValueError):                      # the twin refuses, with the same text
            cv.ungated_twin(cfg)


def test_malformed_gate_inputs_name_what_is_wrong():
    good = _gated()
    mode_list = dict(good, regime_detector=dict(good["regime_detector"], mode=["score"]))
    mode_none = dict(good, regime_detector=dict(good["regime_detector"], mode=None))
    for cfg, mode in ((mode_list, ["score"]), (mode_none, None)):
        (err,) = cv.gate_form_errors(cfg, "c")
        assert err.startswith(f"c.regime_detector.mode={mode!r}: combines_as regime_gate needs "
                              f"mode threshold_rules"), err
    rules_dict = dict(good, regime_detector=dict(good["regime_detector"], rules={"a": 1},
                                                 vetoes=None))
    assert cv.gate_form_errors(rules_dict, "c") == [f"c.regime_detector: {_NOT_A_LIST}"]
    # a dict `rules` with real vetoes: the vetoes are the gate
    assert cv.gate_form_errors(
        dict(good, regime_detector=dict(good["regime_detector"], rules={"a": 1})), "c") == []
    regimes_list = dict(good, strategies={"regimes": ["trending"]})
    assert cv.gate_form_errors(regimes_list, "c") == [
        "c.strategies.regimes: combines_as regime_gate needs exactly one non-null regime (the "
        "regime the gate trades in), and this config has 0 []; set every other regime to null"]
    assert cv.gate_form_errors(None, "c") == [
        f"c.regime_detector: {_NOT_A_LIST}",
        "c.strategies.regimes: combines_as regime_gate needs exactly one non-null regime (the "
        "regime the gate trades in), and this config has 0 []; set every other regime to null"]


# ---------------------------------------------------------------------------
# 2. the ungated twin
# ---------------------------------------------------------------------------

def test_the_twin_exact_output_and_the_input_unchanged():
    cfg = _gated()
    before = copy.deepcopy(cfg)
    twin = cv.ungated_twin(cfg)
    expected = copy.deepcopy(before)
    expected["regime_detector"]["rules"] = []
    del expected["regime_detector"]["vetoes"]
    expected["regime_detector"]["default_regime"] = "trending"
    assert twin == expected
    assert twin["regime_detector"]["components"] == before["regime_detector"]["components"]
    assert cfg == before                                        # pure
    twin["strategies"]["regimes"]["trending"]["components"][0]["weight"] = 9.0
    assert cfg == before                                        # a deep copy


def test_the_twin_of_a_config_without_the_gate_form_raises():
    with pytest.raises(ValueError, match=r"^config\.regime_detector: combines_as regime_gate"):
        cv.ungated_twin(_gated((), ()))


# ---------------------------------------------------------------------------
# 3. the twin is validated like the config
# ---------------------------------------------------------------------------

def test_the_twin_is_checked_and_its_failure_names_the_twin(monkeypatch):
    real = cv.ungated_twin

    def bad_twin(config):            # a derivation that points default_regime at a null regime
        twin = real(config)
        twin["regime_detector"]["default_regime"] = "unknown"
        return twin
    monkeypatch.setattr(cv, "ungated_twin", bad_twin)
    (err,) = _errors(_gated())
    assert err.startswith("v.config ungated twin (D-052: rules [], vetoes dropped, default_regime "
                          "'unknown'): VIOLATION V18 regime_detector.default_regime: 'unknown' "), err


def test_the_twin_is_checked_only_once_the_config_and_form_pass(monkeypatch):
    calls = []
    monkeypatch.setattr(cv, "ungated_twin", lambda c: calls.append(1) or c)
    assert _errors(_gated((), ()))                              # the form fails
    cfg = _gated()
    cfg["strategies"]["regimes"]["trending"]["components"][0]["transforms"] = []   # D-149
    assert _errors(cfg)
    assert calls == []
    assert _errors(_gated()) == [] and calls == [1]


# ---------------------------------------------------------------------------
# 4. the wiring, CONFIG_VEHICLE_ROUTED forced on; off unchanged
# ---------------------------------------------------------------------------

def _doc(config) -> dict:
    return _reading(_claim(), vehicle=_vehicle(config), **GATE)


def _source_run(run_dir) -> None:
    """D-161: CONFIG and its MANIFEST as the source run's base config and block manifest."""
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text(
        json.dumps(CONFIG), encoding="utf-8")
    (run_dir / "artifacts" / "block_manifest.yaml").write_text(yaml.safe_dump(MANIFEST),
                                                               encoding="utf-8")


def test_on_the_reading_check_applies_the_gate_form(monkeypatch, tmp_path):
    monkeypatch.setattr(rp, "CONFIG_VEHICLE_ROUTED", True)
    monkeypatch.setattr(rpr, "_claim_check_kw", lambda: {"folds": True})
    _source_run(tmp_path)     # D-161: the vehicle is also checked against its source run
    for cfg in (_gated(), copy.deepcopy(CONFIG)):
        rp.check_reading(_doc(cfg), CAT, "reading", from_model=True, envelope=True)  # shape ok
    assert rpr._reading_content_errors(_doc(_gated()), CAT, tmp_path) == []
    errs = rpr._reading_content_errors(_doc(copy.deepcopy(CONFIG)), CAT, tmp_path)
    assert [e for e in errs if e.startswith(
        "side_findings[0].vehicle.config.regime_detector: combines_as regime_gate needs the "
        "gate")], errs


def test_off_a_regime_gate_config_vehicle_gets_the_old_refusal():
    assert rp.CONFIG_VEHICLE_ROUTED is False
    with pytest.raises(rp.ProposalError) as exc:
        rp.check_reading(_doc(_gated()), CAT, "reading", from_model=True, envelope=True)
    assert str(exc.value) == f"reading.side_findings[0].{OLD_MESSAGE}"
