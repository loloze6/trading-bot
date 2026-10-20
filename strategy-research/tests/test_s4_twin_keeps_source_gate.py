"""S4 (operator rulings 2026-10-20, D-160 note): the ungated twin keeps the SOURCE's own gate.

config_vehicle.ungated_twin(config, source): a copy of the gated config whose
regime_detector.rules, .vetoes and .default_regime are the source run's own (relabelled through
D-161's swap when the gate moved the trading regime; a missing default read as 'unknown'),
detector components kept as the gated config has them -- so the twin differs from the gated
config only by the gate the config adds. A source with no rules and no vetoes of its own gives
the D-052 twin exactly (rules [], vetoes dropped, default_regime the trading regime), byte for
byte. The caveat (the limit on D-160): a source with its own rules whose default, relabelled,
is a trading regime refuses the gate form (its twin would fail V9; V9 unchanged). The pin: the
brief carries candidate.source.base_config_sha256 and step 2 derives the twin only from a
source config that matches it.

Pinned: synthetic sources with their own rules and vetoes, only vetoes, only rules (with and
without the relabel); the relabel mapping; validation (validate_config incl. V18, D-051/D-149)
and the block-path check; the caveat refusal; the committed sources (sma50_v3, rebase_run_095,
the D-160/D-162 test config) unchanged; trading-bot/strategy_config.json as a source accepted,
its twin exactly its own gate; the source passed at reading time, at decide-next and at step 2;
the pin. No LLM, no backtest, no market data.
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
import decide_next as dn  # noqa: E402
import json_pointer as jp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

import test_d162_config_vehicle_routing as d162  # noqa: E402
import test_e068_9_one_proposal_start_config as e068_9  # noqa: E402
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
    """The vehicle with only the added gate removed and default_regime the source's own
    ('unknown', CONFIG's) relabelled -- 'trending' when the gate moved the strategy there:
    what the twin must be (an empty vetoes list dropped, as the twin has no veto at all rather
    than an empty one)."""
    out = copy.deepcopy(vehicle)
    rd = out["regime_detector"]
    key = "rules" if add == "rule" else "vetoes"
    rd[key] = rd[key][:-1]
    if key == "vetoes" and not rd["vetoes"]:
        del rd["vetoes"]
    moved = cv._trading_regimes(vehicle) == ["trending"]
    rd["default_regime"] = SWAP["unknown"] if moved else "unknown"
    return out


# ---------------------------------------------------------------------------
# the recipe
# ---------------------------------------------------------------------------

# every source x relabel case but the caveat (own rules, relabelled default 'trending'), which
# is refused: test_the_caveat_*
RECIPE = [pytest.param(r, v, rel, id=f"{i}-{'relabel' if rel else 'same_regime'}")
          for (r, v), i in zip(OWN, OWN_IDS) for rel in (False, True) if not (r and rel)]


@pytest.mark.parametrize("rules,vetoes,relabel", RECIPE)
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
    # the source's own default ('unknown'), relabelled: here also the strategy's regime
    relabel_pair = cv.regime_relabel(source, vehicle, "regime_gate")
    assert rd["default_regime"] == cv._own_default(source, relabel_pair) == (
        "trending" if relabel else "unknown") == cv._trading_regimes(vehicle)[0]
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
    relabel = cv.regime_relabel(source, vehicle, "regime_gate")
    assert relabel == ("unknown", "trending")
    # (this source has its own rules, so its twin is the caveat's refusal; the mapping is
    # _own_gate's / _own_default's, which ungated_twin applies to every source)
    rd = {"rules": cv._own_gate(source, "rules", relabel),
          "vetoes": cv._own_gate(source, "vetoes", relabel)}
    # the source's rule to its trading regime routes to the vehicle's; the kill switch into
    # 'chop' is untouched; the veto into the source's null 'trending' goes to the vehicle's
    # null 'unknown'
    assert [r["regime"] for r in rd["rules"]] == ["trending", "chop"]
    assert [v["result"] for v in rd["vetoes"]] == ["unknown"]
    # the default: the same swap; a missing key (or detector) read as 'unknown'; a regime the
    # swap does not name kept; no relabel, kept as it is
    assert cv._own_default(source, relabel) == "trending"
    assert cv._own_default({"regime_detector": {}}, relabel) == "trending"
    assert cv._own_default({}, relabel) == "trending"
    assert cv._own_default({"regime_detector": {"default_regime": "trending"}},
                           relabel) == "unknown"
    assert cv._own_default({"regime_detector": {"default_regime": "chop"}}, relabel) == "chop"
    assert cv._own_default({"regime_detector": {"default_regime": "chop"}}, None) == "chop"
    assert cv._own_default({"regime_detector": {"default_regime": None}}, relabel) is None
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


CAVEAT = ("v.config: combines_as regime_gate cannot be used on this source: it has its own "
          "regime rules and its default regime 'unknown', relabelled 'trending' by this gate "
          "(D-161), is a trading regime (a source trading in its default regime with its own "
          "rules); its ungated twin (S4: the source's own rules, vetoes and default_regime) "
          "would set default_regime 'trending' with non-empty rules, which validate_config V9 "
          "refuses. Keep the source's gate, or use another combines_as")


def _would_be_twin(vehicle: dict, source: dict) -> dict:
    """The twin the caveat refuses, built by hand: the S4 recipe applied with no refusal."""
    relabel = cv.regime_relabel(source, vehicle, "regime_gate")
    out = copy.deepcopy(vehicle)
    rd = out["regime_detector"]
    rd["rules"] = cv._own_gate(source, "rules", relabel)
    vetoes = cv._own_gate(source, "vetoes", relabel)
    if vetoes:
        rd["vetoes"] = vetoes
    else:
        rd.pop("vetoes", None)
    rd["default_regime"] = cv._own_default(source, relabel)
    return out


@pytest.mark.parametrize("vetoes", [True, False], ids=["rules_and_vetoes", "rules_only"])
def test_the_caveat_a_source_trading_in_unknown_with_its_own_rules_refuses_the_gate_form(
        vetoes, routed, tmp_path):
    """Ruling item 2: the source trades in 'unknown' (its default) with its own rules; the gate
    relabels the strategy to 'trending', so the source's default relabelled is 'trending'
    beside non-empty rules -- a twin V9 refuses. The gate form is refused at reading time with
    the message naming that source shape; the vehicle itself validates; V9 is unchanged (it
    still refuses the would-be twin, and nothing else)."""
    source = _source(rules=True, vetoes=vetoes)
    vehicle = _gate(source, relabel=True)
    assert VC.validate(source) == [] and VC.validate(vehicle) == []
    assert cv.source_gate_errors(vehicle, source, "v.config") == [CAVEAT]
    assert cv.config_vehicle_errors({"kind": "config", "config": vehicle}, "v",
                                    combines_as="regime_gate", source=source) == [CAVEAT]
    with pytest.raises(ValueError) as exc:
        cv.ungated_twin(vehicle, source)
    assert str(exc.value) == CAVEAT.replace("v.config: ", "config: ", 1)
    (line,) = VC.validate(_would_be_twin(vehicle, source))           # V9 unchanged
    assert line.startswith(V9_LINE), line
    # not a regime gate: no gate form, no caveat (no twin)
    assert not any("cannot be used on this source" in e for e in cv.config_vehicle_errors(
        {"kind": "config", "config": vehicle}, "v", combines_as="forecast_block", source=source))
    # no source (a caller without one): the D-052 twin, no caveat
    assert cv.source_gate_errors(vehicle, None, "v.config") == []
    # at reading time, from this run's base config
    run_dir = _source_run(tmp_path, source, MANIFEST)
    assert rpr._reading_content_errors(_doc(vehicle), CAT, run_dir) == [
        CAVEAT.replace("v.config", "side_findings[0].vehicle.config", 1)]


def test_the_caveat_condition_is_v9_s_on_the_would_be_twin():
    """The condition: the source's rules a non-empty list AND its default, relabelled, one of
    V9's trading regimes -- exactly when V9 refuses the would-be twin (whose mode is
    threshold_rules, the gate form). Each shape below: the caveat fires iff V9 refuses."""
    def case(src_trading, src_default, veh_trading, rules=True):
        src = _source(rules=rules, vetoes=False)
        regimes = src["strategies"]["regimes"]
        block = regimes["unknown"]
        for r in regimes:
            regimes[r] = block if r == src_trading else None
        if src_default is None:
            src["regime_detector"].pop("default_regime", None)
        else:
            src["regime_detector"]["default_regime"] = src_default
        veh = copy.deepcopy(src)
        veh["regime_detector"]["components"].append(_tb("vr"))
        veh["regime_detector"]["vetoes"] = [copy.deepcopy(NEW_VETO)]
        vreg = veh["strategies"]["regimes"]
        for r in vreg:
            vreg[r] = block if r == veh_trading else None
        # (the vehicle's own rules and default do not matter: the twin replaces both)
        refused = bool(cv.source_gate_errors(veh, src, "v.config"))
        v9 = any(ln.startswith("VIOLATION V9") for ln in VC.validate(_would_be_twin(veh, src)))
        return refused, v9

    shapes = {
        "unknown_default_unknown_relabel_trending": ("unknown", "unknown", "trending"),
        "unknown_default_absent_relabel_chop": ("unknown", None, "chop"),
        "unknown_default_unknown_no_relabel": ("unknown", "unknown", "unknown"),
        # the strategy moved INTO 'unknown': the source default 'unknown' becomes the source's
        # trading regime 'trending' (null in the vehicle) -- V9 refuses that twin too
        "trending_default_unknown_relabel_unknown": ("trending", "unknown", "unknown"),
        "mean_reversion_default_unknown_no_relabel": ("mean_reversion", "unknown",
                                                       "mean_reversion"),
        "mean_reversion_default_unknown_relabel_chop": ("mean_reversion", "unknown", "chop"),
    }
    seen = {name: case(*args) for name, args in shapes.items()}
    assert seen == {
        "unknown_default_unknown_relabel_trending": (True, True),
        "unknown_default_absent_relabel_chop": (True, True),
        "unknown_default_unknown_no_relabel": (False, False),
        "trending_default_unknown_relabel_unknown": (True, True),
        "mean_reversion_default_unknown_no_relabel": (False, False),
        "mean_reversion_default_unknown_relabel_chop": (False, False),
    }
    # no rules of its own: never the caveat (V9 needs non-empty rules), whatever the default
    assert case("unknown", "unknown", "trending", rules=False) == (False, False)
    # the message for a source whose own default already is a trading regime (no relabel)
    src = _source(rules=True, vetoes=False)
    src["regime_detector"]["default_regime"] = "chop"
    (msg,) = cv.source_gate_errors(_gate(src), src, "w")
    assert msg.startswith("w: combines_as regime_gate cannot be used on this source: it has its "
                          "own regime rules and its default regime 'chop' is a trading regime "
                          "(a source trading in its default regime with its own rules); its "
                          "ungated twin (S4: the source's own rules, vetoes and default_regime) "
                          "would set default_regime 'chop' with non-empty rules"), msg


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
    assert err.startswith("v.config ungated twin (D-052, S4: rules, vetoes and default_regime "
                          "the source's own, default_regime 'chop'): VIOLATION V18 "), err
    assert cv.S4_RECIPE == "D-052, S4: rules, vetoes and default_regime the source's own"


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
        "v.config: the ungated twin (D-052, S4: rules, vetoes and default_regime the source's "
        "own; the run's design variant) does not resolve the block path(s) ['/regime_detector/rules/2'] of the "
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
    """Ruling item 1: for every existing source (no rules, no vetoes of its own, trading in
    its default 'unknown'), the S4 twin -- default_regime the source's 'unknown' relabelled --
    is today's D-052 twin byte for byte (rules [], vetoes dropped, default_regime the trading
    regime): 'unknown' with no relabel, 'trending' when the gate moved the strategy there."""
    for config, _manifest in briefs.values():
        assert not config["regime_detector"].get("rules") and "vetoes" not in config[
            "regime_detector"]
        assert config["regime_detector"]["default_regime"] == "unknown"
        assert cv._trading_regimes(config) == ["unknown"]
        for gate in (_veto_gate(config), _relabel_gate(config)):
            twin = cv.ungated_twin(gate, config)
            assert json.dumps(twin) == json.dumps(cv.ungated_twin(gate))
            assert twin["regime_detector"]["default_regime"] == cv._trading_regimes(gate)[0]
    for gate in (_gated(), _gated((), (dict(_gated()["regime_detector"]["vetoes"][0],
                                            result="trending"),))):
        assert json.dumps(cv.ungated_twin(gate, CONFIG)) == json.dumps(cv.ungated_twin(gate))


def test_trading_bot_s_config_as_a_source_is_accepted_and_its_twin_is_its_own_gate():
    """trading-bot/strategy_config.json has its own rules (to trending, mean_reversion, chop)
    and a veto (to chop), one trading regime (mean_reversion), default 'unknown' (null), and no
    relabel here. Its default stays 'unknown' (not a V9 trading regime): no caveat, and the
    twin of a gate that adds one rule is exactly the source -- its own gate, its own default."""
    source = copy.deepcopy(TB_CONFIG)
    assert cv._trading_regimes(source) == ["mean_reversion"]
    assert source["regime_detector"]["default_regime"] == "unknown"
    vehicle = copy.deepcopy(source)
    vehicle["regime_detector"]["rules"].append(
        {"regime": "chop", "any_of": [[{"id": "vr", "op": "gte", "value": 1.5}]]})
    assert VC.validate(vehicle) == []
    assert cv.regime_relabel(source, vehicle, "regime_gate") is None
    assert cv.source_gate_errors(vehicle, source, "v.config") == []
    twin = cv.ungated_twin(vehicle, source)
    assert twin == source and json.dumps(twin) == json.dumps(source)
    assert VC.validate(twin) == []
    # accepted whole at reading time: the same detector over CONFIG's strategy (D-051/D-149
    # clean; trading-bot's own strategy block uses a dead-zone op D-051 refuses on any vehicle)
    source = copy.deepcopy(CONFIG)
    source["regime_detector"] = copy.deepcopy(TB_CONFIG["regime_detector"])
    regimes = source["strategies"]["regimes"]
    regimes["mean_reversion"], regimes["unknown"] = regimes["unknown"], None
    vehicle = copy.deepcopy(source)
    vehicle["regime_detector"]["rules"].append(
        {"regime": "chop", "any_of": [[{"id": "vr", "op": "gte", "value": 1.5}]]})
    assert cv.config_vehicle_errors({"kind": "config", "config": vehicle}, "v",
                                    combines_as="regime_gate", source=source) == []
    assert json.dumps(cv.ungated_twin(vehicle, source)) == json.dumps(source)


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


# ---------------------------------------------------------------------------
# the source pin (ruling item 3): candidate.source.base_config_sha256
# ---------------------------------------------------------------------------

def test_the_brief_pins_the_source_config_beside_its_ref_on_the_config_vehicle_path_only():
    source = _source()
    p = d162._side(d162._vehicle(_gate(source)))
    src = {**d162._src(p), "base_config": copy.deepcopy(source)}
    brief_source = d162._front(p, src)["candidate"]["source"]
    assert brief_source["base_config_sha256"] == dn.config_sha256(source)
    keys = list(brief_source)
    assert keys.index("base_config_sha256") == keys.index("base_config_ref") + 1   # beside it
    # additive: a side finding with no config vehicle (its start config is the source's) has none
    other = e068_9._brief_front(e068_9._side())["candidate"]["source"]
    assert "base_config_ref" in other and "base_config_sha256" not in other


def _pinned_step_2_run(run_id: str, source: dict) -> tuple:
    """A step-2 run of `source` + an added rule, its brief pinning `source`, 1b done and step 2's
    variant_patches.yaml written; (run_dir, gate, the brief's source block)."""
    _set_orchestrator(d162.LOOP_ON)
    gate = _gate(source)
    p = d162._side(d162._vehicle(gate))
    src = {**d162._src(p), "base_config": copy.deepcopy(source)}
    front = d162._front(p, src)
    run_dir = d162._1b_run(run_id, front, source=source)
    rpr._exact_config_1b(run_dir, run_id)
    rpr.save_yaml(run_dir / "artifacts" / "variant_patches.yaml",
                  {"base_config_ref": "x", "variants": d162.STEP2})
    return run_dir, gate, front["candidate"]["source"]


def test_step_2_derives_the_twin_when_the_source_config_matches_the_pin():
    source = _source()
    run_dir, gate, pin = _pinned_step_2_run("run_993", source)
    assert pin["base_config_sha256"] == dn.config_sha256(source)
    assert rpr._brief_source_base_config(run_dir) == source
    rpr._set_ungated_twin_variant(run_dir, "run_993")
    entry = rpr.load_yaml(run_dir / "artifacts" / "variant_patches.yaml")["variants"][1]
    assert jp.apply_json_pointer_patch(gate, entry["patch"]) == cv.ungated_twin(gate, source)


def test_step_2_refuses_a_source_config_that_does_not_match_the_pin():
    source = _source()
    run_dir, _gate_cfg, pin = _pinned_step_2_run("run_994", source)
    changed = copy.deepcopy(source)
    changed["regime_detector"]["rules"][0]["any_of"][0][0]["value"] = 0.7   # a different gate
    path = rpr.ROOT / pin["base_config_ref"]
    path.write_text(json.dumps(changed), encoding="utf-8")
    vp = run_dir / "artifacts" / "variant_patches.yaml"
    before = vp.read_bytes()
    got, want = dn.config_sha256(changed), pin["base_config_sha256"]
    msg = (f"[S4] ungated twin refused: the source base config at {pin['base_config_ref']} does "
           f"not match the brief's base_config_sha256 ({got} != {want}); the twin takes the "
           f"source's own rules, vetoes and default_regime, so it is derived only from the "
           f"source config decide-next pinned; restore that file, or write the brief again "
           f"with decide-next")
    with pytest.raises(RuntimeError) as exc:
        rpr._set_ungated_twin_variant(run_dir, "run_994")
    assert str(exc.value) == msg
    assert vp.read_bytes() == before                                   # nothing written
    # the same file content written differently (key order, spacing): the canonical sha matches
    path.write_text(json.dumps(source, indent=3, sort_keys=True), encoding="utf-8")
    rpr._set_ungated_twin_variant(run_dir, "run_994")
    assert vp.read_bytes() != before


def test_step_2_refuses_a_brief_without_the_pin():
    source = _source()
    run_dir, _gate_cfg, pin = _pinned_step_2_run("run_995", source)
    brief_path = run_dir / "artifacts" / "research_brief.yaml"
    brief = rpr.load_yaml(brief_path)
    del brief["candidate"]["source"]["base_config_sha256"]        # a brief from before the pin
    rpr.save_yaml(brief_path, brief)
    vp = run_dir / "artifacts" / "variant_patches.yaml"
    before = vp.read_bytes()
    with pytest.raises(RuntimeError) as exc:
        rpr._set_ungated_twin_variant(run_dir, "run_995")
    assert str(exc.value) == (
        f"[S4] ungated twin refused: the brief has no candidate.source.base_config_sha256 beside "
        f"base_config_ref {pin['base_config_ref']} (a brief written before the source pin); the "
        f"twin takes the source's own rules, vetoes and default_regime, and is never derived "
        f"from an unpinned source config; write the brief again with decide-next")
    assert vp.read_bytes() == before                                   # nothing written
