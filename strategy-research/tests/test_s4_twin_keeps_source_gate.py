"""S4 (operator rulings 2026-10-20, D-160 note): the ungated twin keeps the SOURCE's own gate.

config_vehicle.ungated_twin(config, source): a copy of the gated config whose
regime_detector.rules and .vetoes are the source run's own (relabelled when the gate moved the
trading regime), default_regime the regime holding the strategy, detector components kept as
the gated config has them -- so the twin differs from the gated config only by the gate the
config adds. A source with no rules and no vetoes of its own gives the D-052 twin exactly
(rules [], vetoes dropped), byte for byte.

Pinned: synthetic sources with their own rules and vetoes, only vetoes, only rules (with and
without the relabel); the relabel mapping; validation (validate_config incl. V18, D-051/D-149)
and the block-path check; the committed sources (sma50_v3, rebase_run_095, the D-160/D-162 test
config) unchanged; trading-bot/strategy_config.json as a source keeps its own gate; the source
passed at reading time, at decide-next and at step 2. No LLM, no backtest, no market data.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import config_vehicle as cv  # noqa: E402
import json_pointer as jp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

import test_d162_config_vehicle_routing as d162  # noqa: E402
from test_d051_d053_forecast_rules import CONFIG, MANIFEST  # noqa: E402
from test_d160_regime_gate_twin import _gated  # noqa: E402
from test_d161_scaffolding_rule import (  # noqa: E402
    TB_CONFIG, _doc, _from_brief, _relabel_gate, _source_run, _tb, _veto_gate)
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
from test_e077_pr2_confirm import CAT  # noqa: E402

VC = cv._validate_config_module(cv.TBOT_ROOT)
# the source's own gate: a rule routing to its trading regime ('unknown', taking priority), a
# kill switch into a null regime, and a veto into a null regime ('trending')
OWN_RULES = [{"regime": "unknown", "any_of": [[{"id": "er", "op": "gte", "value": 0.6}]]},
             {"regime": "chop", "any_of": [[{"id": "er", "op": "lte", "value": 0.15}]]}]
OWN_VETOES = [dict(copy.deepcopy(TB_CONFIG["regime_detector"]["vetoes"][0]), result="trending")]
# the gate the vehicle adds: a rule reading a component the source does not have (into a null
# regime; with the relabel, into the vehicle's trading regime, whose default is then null)
NEW_RULE = {"regime": "chop", "any_of": [[{"id": "vr", "op": "lte", "value": 0.9}]]}
NEW_RULE_RELABEL = {"regime": "trending", "any_of": [[{"id": "vr", "op": "gte", "value": 1.1}]]}
NEW_VETO = {"id": "vr", "transforms": [{"op": "identity"}], "rules": [{"op": "gte", "value": 1.5}],
            "consecutive_bars": 1, "result": "chop"}
SWAP = {"unknown": "trending", "trending": "unknown"}
OWN = [(True, True), (False, True), (True, False)]
OWN_IDS = ["rules_and_vetoes", "vetoes_only", "rules_only"]


def _source(rules=True, vetoes=True) -> dict:
    """CONFIG (trading regime 'unknown') with trading-bot's er and vol detector components and
    its own rules and/or vetoes (CONFIG itself has rules [] and no vetoes key)."""
    cfg = copy.deepcopy(CONFIG)
    rd = cfg["regime_detector"]
    rd["components"] = [_tb("er"), _tb("vol")]
    if rules:
        rd["rules"] = copy.deepcopy(OWN_RULES)
    if vetoes:
        rd["vetoes"] = copy.deepcopy(OWN_VETOES)
    return cfg


def _gate(source: dict, relabel=False, add="rule") -> dict:
    """The vehicle: the source plus a gate (NEW_RULE after the source's rules, or NEW_VETO after
    its vetoes) reading trading-bot's `vr`, added after the source's components. With
    `relabel`, the strategy moved unknown -> trending, the source's rules and vetoes written in
    the vehicle's regime names, the added rule routing to 'trending', default_regime left
    'unknown' (null now: V9 forbids a trading default beside non-empty rules)."""
    v = copy.deepcopy(source)
    rd = v["regime_detector"]
    rd["components"].append(_tb("vr"))
    if relabel:
        regimes = v["strategies"]["regimes"]
        regimes["trending"], regimes["unknown"] = regimes["unknown"], None
        for r in rd.get("rules") or []:
            r["regime"] = SWAP.get(r["regime"], r["regime"])
        for x in rd.get("vetoes") or []:
            x["result"] = SWAP.get(x["result"], x["result"])
    if add == "rule":
        rd["rules"] = list(rd.get("rules") or []) + [
            copy.deepcopy(NEW_RULE_RELABEL if relabel else NEW_RULE)]
    else:
        rd["vetoes"] = list(rd.get("vetoes") or []) + [copy.deepcopy(NEW_VETO)]
    return v


def _without_the_gate(vehicle: dict, add="rule") -> dict:
    """The vehicle with only the added gate removed and default_regime the strategy's regime:
    what the twin must be (an empty vetoes list dropped, as the twin has no veto at all rather
    than an empty one)."""
    out = copy.deepcopy(vehicle)
    rd = out["regime_detector"]
    key = "rules" if add == "rule" else "vetoes"
    rd[key] = rd[key][:-1]
    if key == "vetoes" and not rd["vetoes"]:
        del rd["vetoes"]
    rd["default_regime"] = cv._trading_regimes(vehicle)[0]
    return out


# ---------------------------------------------------------------------------
# the recipe
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("relabel", [False, True], ids=["same_regime", "relabel"])
@pytest.mark.parametrize("rules,vetoes", OWN, ids=OWN_IDS)
def test_the_twin_keeps_the_source_s_own_gate_and_drops_only_the_added_one(rules, vetoes,
                                                                          relabel):
    source = _source(rules, vetoes)
    vehicle = _gate(source, relabel)
    before = (copy.deepcopy(source), copy.deepcopy(vehicle))
    twin = cv.ungated_twin(vehicle, source)
    expected = _without_the_gate(vehicle)
    assert twin == expected
    assert json.dumps(twin) == json.dumps(expected)               # key order too
    rd = twin["regime_detector"]
    assert rd["default_regime"] == cv._trading_regimes(vehicle)[0] == (
        "trending" if relabel else "unknown")
    assert rd["components"] == vehicle["regime_detector"]["components"]   # vr kept, unread
    assert ("vetoes" in rd) is vetoes and (rd["rules"] != []) is rules
    assert (source, vehicle) == before                            # pure
    twin["regime_detector"]["components"][0]["params"]["period"] = 99
    assert (source, vehicle) == before                            # deep copies
    # the D-052 twin drops the source's own gate too (the confound S4 removes)
    old = cv.ungated_twin(vehicle)
    assert old["regime_detector"]["rules"] == [] and "vetoes" not in old["regime_detector"]
    assert old != twin


@pytest.mark.parametrize("rules,vetoes", [(True, False), (True, True)], ids=["rules_only",
                                                                              "rules_and_vetoes"])
def test_an_added_veto_is_dropped_and_the_source_s_vetoes_kept(rules, vetoes):
    source = _source(rules, vetoes)
    vehicle = _gate(source, add="veto")
    twin = cv.ungated_twin(vehicle, source)
    assert twin == _without_the_gate(vehicle, add="veto")
    assert twin["regime_detector"].get("vetoes", []) == source["regime_detector"].get("vetoes", [])


def test_the_relabel_mapping_swaps_the_two_trading_regimes_in_rules_and_vetoes():
    source = _source()
    vehicle = _gate(source, relabel=True)
    assert cv.regime_relabel(source, vehicle, "regime_gate") == ("unknown", "trending")
    rd = cv.ungated_twin(vehicle, source)["regime_detector"]
    # the source's rule to its trading regime routes to the vehicle's; the kill switch into
    # 'chop' is untouched; the veto into the source's null 'trending' goes to the vehicle's
    # null 'unknown'
    assert [r["regime"] for r in rd["rules"]] == ["trending", "chop"]
    assert [v["result"] for v in rd["vetoes"]] == ["unknown"]
    assert vehicle["strategies"]["regimes"]["unknown"] is None
    # what each rule reads is unchanged
    assert [r["any_of"] for r in rd["rules"]] == [r["any_of"] for r in OWN_RULES]
    # _own_gate on its own: malformed entries kept as they are, nothing else renamed
    odd = {"regime_detector": {"rules": [5, {"regime": ["unknown"]}, {"regime": "unknown"}],
                               "vetoes": [{"result": "trending", "id": "unknown"}]}}
    assert cv._own_gate(odd, "rules", ("unknown", "trending")) == [
        5, {"regime": ["unknown"]}, {"regime": "trending"}]
    assert cv._own_gate(odd, "vetoes", ("unknown", "trending")) == [
        {"result": "unknown", "id": "unknown"}]


@pytest.mark.parametrize("own", [None, [], "x", {"a": 1}], ids=["missing", "empty", "str", "dict"])
def test_a_source_with_no_gate_of_its_own_gives_the_d052_twin(own):
    source = copy.deepcopy(CONFIG)
    for key in ("rules", "vetoes"):
        if own is None:
            source["regime_detector"].pop(key, None)
        else:
            source["regime_detector"][key] = copy.deepcopy(own)
    gate = _gated()
    assert json.dumps(cv.ungated_twin(gate, source)) == json.dumps(cv.ungated_twin(gate))
    assert cv.twin_recipe(cv.ungated_twin(gate, source)) == cv.D052_RECIPE
    for not_a_config in (None, [], "x"):
        assert json.dumps(cv.ungated_twin(gate, not_a_config)) == json.dumps(cv.ungated_twin(gate))


# ---------------------------------------------------------------------------
# validation: validate_config incl. V18, D-051/D-149, the block paths
# ---------------------------------------------------------------------------

VALID = [(True, True, False), (False, True, False), (True, False, False), (False, True, True)]
VALID_IDS = ["rules_and_vetoes", "vetoes_only", "rules_only", "vetoes_only-relabel"]


@pytest.mark.parametrize("rules,vetoes,relabel", VALID, ids=VALID_IDS)
def test_the_twin_validates_and_resolves_the_block_paths(rules, vetoes, relabel):
    source = _source(rules, vetoes)
    assert VC.validate(source) == []
    vehicle = _gate(source, relabel)
    assert VC.validate(vehicle) == []
    twin = cv.ungated_twin(vehicle, source)
    assert VC.validate(twin) == []
    vehicle_doc = {"kind": "config", "config": vehicle}
    assert cv.config_vehicle_errors(vehicle_doc, "v", combines_as="regime_gate",
                                    source=source) == []
    assert cv.source_fit_errors(vehicle, source, MANIFEST, "regime_gate", "v") == []
    derived = cv.derived_manifest(MANIFEST, source, vehicle, "regime_gate")
    assert cv.twin_missing_block_paths(derived, twin) == []


V9_LINE = ("VIOLATION V9 regime_detector.default_regime: 'trending' is forbidden in mode "
           "'threshold_rules' while regime_detector.rules is non-empty.")


@pytest.mark.parametrize("vetoes", [True, False], ids=["rules_and_vetoes", "rules_only"])
def test_open_point_v9_refuses_the_twin_of_own_rules_with_a_non_unknown_strategy_regime(vetoes):
    """Pinned as built, reported to the operator: with the source's own rules kept (non-empty)
    and default_regime the strategy's regime, validate_config's V9 (no trading default beside
    non-empty rules: a gate bypass) refuses the twin whenever that regime is not 'unknown' --
    here the relabel moved it to 'trending' -- so the vehicle is refused, naming the twin. The
    vehicle itself validates; the D-052 twin (rules []) did not hit V9."""
    source = _source(rules=True, vetoes=vetoes)
    vehicle = _gate(source, relabel=True)
    assert VC.validate(vehicle) == []
    twin = cv.ungated_twin(vehicle, source)
    (line,) = VC.validate(twin)
    assert line.startswith(V9_LINE), line
    (err,) = cv.config_vehicle_errors({"kind": "config", "config": vehicle}, "v",
                                      combines_as="regime_gate", source=source)
    assert err.startswith("v.config ungated twin (D-052, S4: rules and vetoes the source's own, "
                          "default_regime 'trending'): " + V9_LINE), err
    assert VC.validate(cv.ungated_twin(vehicle)) == []


def test_v18_does_not_fire_on_a_twin_whose_source_rules_are_non_empty():
    """V18 is the empty-rules case only: the twin of a source with its own rules is not it,
    even pointed at a null default; the same twin with its rules emptied is."""
    source = _source(rules=True, vetoes=False)
    twin = cv.ungated_twin(_gate(source), source)
    assert twin["regime_detector"]["rules"] == OWN_RULES
    assert not [ln for ln in VC.validate(twin) if ln.startswith("VIOLATION V18")]
    dead = copy.deepcopy(twin)
    dead["regime_detector"]["default_regime"] = "chop"               # null in strategies
    assert not [ln for ln in VC.validate(dead) if ln.startswith("VIOLATION V18")]
    dead["regime_detector"]["rules"] = []
    assert [ln for ln in VC.validate(dead) if ln.startswith("VIOLATION V18")]


def test_a_twin_failure_names_the_s4_recipe(monkeypatch):
    source = _source()
    real = cv.ungated_twin

    def bad_twin(config, source=None):     # a derivation pointing default_regime at a null regime
        twin = real(config, source)
        twin["regime_detector"]["default_regime"] = "chop"
        twin["regime_detector"]["rules"] = []
        return twin
    monkeypatch.setattr(cv, "ungated_twin", bad_twin)
    # rules [] but vetoes kept: not the D-052 words
    (err,) = cv.config_vehicle_errors({"kind": "config", "config": _gate(source)}, "v",
                                      combines_as="regime_gate", source=source)
    assert err.startswith("v.config ungated twin (D-052, S4: rules and vetoes the source's own, "
                          "default_regime 'chop'): VIOLATION V18 "), err


def test_a_block_path_under_the_source_s_own_gate_resolves_in_the_twin():
    """A block path under the source's own vetoes: the S4 twin keeps it; the D-052 twin lost
    it (a refusal before S4). A block path under the ADDED gate is still refused."""
    source = _source()
    vehicle = _gate(source)
    m = {"block": {"kind": "forecast", "config_paths": [
        "/strategies/regimes/unknown/components/0", "/regime_detector/vetoes/0"]},
        "scaffolding": ["/strategies/warmup", "/regime_detector/components"],
        "rationale": "the gated block"}
    assert cv.source_fit_errors(vehicle, source, m, "regime_gate", "v") == []
    assert cv.twin_missing_block_paths(m, cv.ungated_twin(vehicle)) == ["/regime_detector/vetoes/0"]
    added = dict(m, block={"kind": "forecast", "config_paths": [
        "/strategies/regimes/unknown/components/0", "/regime_detector/rules/2"]})
    assert cv.source_fit_errors(vehicle, source, added, "regime_gate", "v") == [
        "v.config: the ungated twin (D-052, S4: rules and vetoes the source's own; the run's "
        "design variant) does not resolve the block path(s) ['/regime_detector/rules/2'] of the "
        "source run's block_manifest.yaml; keep every block path outside the gate, so the twin "
        "still holds the block (5a does not test a variant that loses one)"]


# ---------------------------------------------------------------------------
# the existing sources: byte-identical twins
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def briefs(tmp_path_factory):
    return {name: _from_brief(tmp_path_factory.mktemp(name), f"{name}.md")
            for name in ("L1_daily_trend_basket_sma50_v3", "rebase_run_095_standardised_host")}


def test_the_committed_sources_give_byte_identical_twins(briefs):
    for config, _manifest in briefs.values():
        assert not config["regime_detector"].get("rules") and "vetoes" not in config[
            "regime_detector"]
        for gate in (_veto_gate(config), _relabel_gate(config)):
            assert json.dumps(cv.ungated_twin(gate, config)) == json.dumps(cv.ungated_twin(gate))
    for gate in (_gated(), _gated((), (dict(_gated()["regime_detector"]["vetoes"][0],
                                            result="trending"),))):
        assert json.dumps(cv.ungated_twin(gate, CONFIG)) == json.dumps(cv.ungated_twin(gate))


def test_trading_bot_s_config_as_a_source_keeps_its_own_gate():
    """trading-bot/strategy_config.json has its own rules (to trending, mean_reversion, chop)
    and a veto (to chop), one trading regime (mean_reversion), default 'unknown' (null). As a
    source, its twin keeps both; default_regime is the strategy's regime (the ruling), not the
    source's own 'unknown' -- so V9 refuses that twin (the open point above)."""
    source = copy.deepcopy(TB_CONFIG)
    assert cv._trading_regimes(source) == ["mean_reversion"]
    vehicle = copy.deepcopy(source)
    vehicle["regime_detector"]["rules"].append(
        {"regime": "chop", "any_of": [[{"id": "vr", "op": "gte", "value": 1.5}]]})
    assert VC.validate(vehicle) == []
    twin = cv.ungated_twin(vehicle, source)
    rd, src = twin["regime_detector"], source["regime_detector"]
    assert rd["rules"] == src["rules"] and rd["vetoes"] == src["vetoes"]
    assert rd["components"] == src["components"]
    assert rd["default_regime"] == "mean_reversion" != src["default_regime"]
    (line,) = VC.validate(twin)
    assert line.startswith(V9_LINE.replace("'trending'", "'mean_reversion'")), line


# ---------------------------------------------------------------------------
# the callers pass the source
# ---------------------------------------------------------------------------

@pytest.fixture()
def routed(monkeypatch):
    monkeypatch.setattr(rpr, "_claim_check_kw", lambda: {"folds": True})


def test_reading_time_passes_this_run_s_base_config_as_the_source(routed, tmp_path, monkeypatch):
    source = _source()
    run_dir = _source_run(tmp_path, source, MANIFEST)
    seen, real = [], cv.ungated_twin
    monkeypatch.setattr(cv, "ungated_twin",
                        lambda config, source=None: seen.append(source) or real(config, source))
    assert rpr._reading_content_errors(_doc(_gate(source)), CAT, run_dir) == []
    assert seen == [source, source]                     # step 4 (validated) and step 5 (block paths)


def test_reading_time_refuses_an_unreadable_source_before_the_twin(routed, tmp_path, monkeypatch):
    source = _source()
    run_dir = _source_run(tmp_path, source, MANIFEST)
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{", encoding="utf-8")
    calls = []
    monkeypatch.setattr(cv, "config_vehicle_errors", lambda *a, **k: calls.append(1) or [])
    (err,) = rpr._reading_content_errors(_doc(_gate(source)), CAT, run_dir)
    assert err.startswith("side_findings[0].vehicle: the base config "
                          "artifacts/candidate_strategy_config.json cannot be read ("), err
    assert calls == []
    # not a regime gate: the config check runs first, as before
    rpr._reading_content_errors(_doc(_gate(source), "forecast_block"), CAT, run_dir)
    assert calls == [1]


def test_decide_next_passes_the_source_s_base_config():
    source = _source()
    vehicle = _gate(source)
    m = {"block": {"kind": "forecast", "config_paths": [
        "/strategies/regimes/unknown/components/0", "/regime_detector/vetoes/0"]},
        "scaffolding": ["/strategies/warmup"], "rationale": "the gated block"}
    p = d162._side(d162._vehicle(vehicle))
    src = {**d162._src(p, manifest=m), "base_config": copy.deepcopy(source)}
    assert d162._reasons(d162._cand(p, src)) == [d162.ELIGIBLE]
    # the same candidate from a source without its own vetoes: the twin loses the block path
    plain = {**d162._src(p, manifest=m), "base_config": _source(vetoes=False)}
    assert d162._reasons(d162._cand(p, plain)) == [
        "manifest_unresolved: the ungated twin (D-052, the run's design variant) does not "
        "resolve the block path(s) ['/regime_detector/vetoes/0']"]


@pytest.mark.parametrize("rules,vetoes,relabel", [(True, True, False), (False, True, True)],
                         ids=["rules_and_vetoes", "vetoes_only-relabel"])
def test_step_2_reads_the_source_from_the_brief_and_writes_the_s4_twin(rules, vetoes, relabel):
    _set_orchestrator(d162.LOOP_ON)
    source = _source(rules, vetoes)
    gate = _gate(source, relabel)
    p = d162._side(d162._vehicle(gate))
    src = {**d162._src(p), "base_config": copy.deepcopy(source)}
    front = d162._front(p, src)
    run_dir = d162._1b_run("run_991", front, source=source)
    rpr._exact_config_1b(run_dir, "run_991")
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "variant_patches.yaml", {"base_config_ref": "x", "variants": d162.STEP2})
    assert rpr._brief_source_base_config(run_dir) == source
    rpr._set_ungated_twin_variant(run_dir, "run_991")
    entry = rpr.load_yaml(arts / "variant_patches.yaml")["variants"][1]
    assert entry["variant_id"] == rpr.UNGATED_TWIN_VARIANT_ID
    twin = jp.apply_json_pointer_patch(gate, entry["patch"])
    assert twin == cv.ungated_twin(gate, source) == _without_the_gate(gate)
    assert "the source run's own" in entry["rationale"]
    derived = rpr.load_yaml(arts / "block_manifest.yaml")
    assert jp.manifest_missing_paths(twin, derived) == []


def test_step_2_without_the_source_config_on_disk_raises():
    _set_orchestrator(d162.LOOP_ON)
    gate = _gate(_source())
    p = d162._side(d162._vehicle(gate))
    src = {**d162._src(p), "base_config": _source()}
    front = d162._front(p, src)
    run_dir = d162._1b_run("run_992", front)
    rpr._exact_config_1b(run_dir, "run_992")
    (rpr.ROOT / front["candidate"]["source"]["base_config_ref"]).unlink()
    rpr.save_yaml(run_dir / "artifacts" / "variant_patches.yaml",
                  {"base_config_ref": "x", "variants": d162.STEP2})
    with pytest.raises(RuntimeError, match=r"^\[S4\] ungated twin: the source run's base config "
                                           r"runs/run_070/\S+ cannot be read"):
        rpr._set_ungated_twin_variant(run_dir, "run_992")
    brief = rpr.load_yaml(run_dir / "artifacts" / "research_brief.yaml")
    del brief["candidate"]["source"]["base_config_ref"]
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", brief)
    with pytest.raises(RuntimeError, match=r"no candidate\.source\.base_config_ref"):
        rpr._set_ungated_twin_variant(run_dir, "run_992")
