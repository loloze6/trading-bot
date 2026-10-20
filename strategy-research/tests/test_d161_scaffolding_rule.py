"""D-161 (vehicle-format V2-1): the scaffolding rule for config vehicles.

A config vehicle is measured against its SOURCE run (config_vehicle.source_fit_errors):
  * a source without block_manifest.yaml is refused (the exact-config route cannot carry it);
  * every scaffolding pointer of the source's manifest keeps the base config's value
    (scaffolding_errors), except a regime gate's three allowances: (a) regime_detector.rules,
    .vetoes, .default_regime; (b) added detector components a rule or veto reads (reading B),
    every source component kept as it is; (c) the regime relabel, exactly one trading regime
    on each side;
  * the source manifest, relabelled by code for (c) (derived_manifest), fits the config by
    block_manifest.check_manifest (Q3, the function D-110's exact-config 1b runs).

Probes on committed sources: the exact config and manifest of
briefs/L1_daily_trend_basket_sma50_v3.md and briefs/rebase_run_095_standardised_host.md
(read with run_phase1_research's own brief parsers), and the detector of
trading-bot/strategy_config.json. The wiring runs with no switch (D-162 deleted
reader_proposals.CONFIG_VEHICLE_ROUTED). No LLM, no backtest, no market data.
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

import block_manifest as bm  # noqa: E402
import config_vehicle as cv  # noqa: E402
import reader_proposals as rp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

from test_e077_pr2_confirm import CAT, _claim, _reading  # noqa: E402

TB_CONFIG = json.loads((SR_ROOT.parent / "trading-bot" / "strategy_config.json")
                       .read_text(encoding="utf-8"))
SC = "strategies.strategy_components."
ER_RULE = {"regime": "trending", "any_of": [[{"id": "er", "op": "gte", "value": 0.3}]]}
KEEP = ("; keep the source's scaffolding unchanged")
SCAFF = ("which the source's block_manifest.yaml lists as scaffolding (not part of the idea)"
         + KEEP)
OLD_MESSAGE = ("vehicle: must be a non-empty list of changes (omit it when the finding needs "
               "no config change)")
NO_MANIFEST = ("v: the source run has no block manifest (artifacts/block_manifest.yaml), so its "
               "scaffolding cannot be told from its idea and the exact-config route (D-110) "
               "cannot carry a config vehicle; write the vehicle as a list of config changes "
               "instead")


def _from_brief(tmp_dir: Path, name: str) -> tuple:
    """(exact config, exact manifest) of a committed brief, read by rpr's own parsers."""
    text = (SR_ROOT / "briefs" / name).read_text(encoding="utf-8").replace("\r\n", "\n")
    assert text.startswith("---\n")
    front = text[4:].split("\n---", 1)[0]
    (tmp_dir / "artifacts").mkdir(parents=True)
    (tmp_dir / "artifacts" / "research_brief.yaml").write_text(front, encoding="utf-8")
    return rpr._brief_exact_config(tmp_dir), rpr._brief_exact_manifest(tmp_dir)


@pytest.fixture(scope="module")
def sma50(tmp_path_factory):
    return _from_brief(tmp_path_factory.mktemp("sma50"), "L1_daily_trend_basket_sma50_v3.md")


@pytest.fixture(scope="module")
def rebase(tmp_path_factory):
    return _from_brief(tmp_path_factory.mktemp("rebase"), "rebase_run_095_standardised_host.md")


def _tb(cid: str) -> dict:
    return copy.deepcopy(next(c for c in TB_CONFIG["regime_detector"]["components"]
                              if c["id"] == cid))


def _veto_gate(base: dict, unread=()) -> dict:
    """The source with trading-bot's `vol` component added and its veto (into chop, null)."""
    cfg = copy.deepcopy(base)
    rd = cfg["regime_detector"]
    rd["components"] = rd["components"] + [_tb(c) for c in unread] + [_tb("vol")]
    rd["vetoes"] = copy.deepcopy(TB_CONFIG["regime_detector"]["vetoes"])
    return cfg


def _relabel_gate(base: dict) -> dict:
    """The source's strategy moved unknown -> trending, traded when trading-bot's `er` says so."""
    cfg = copy.deepcopy(base)
    rd = cfg["regime_detector"]
    rd["components"] = rd["components"] + [_tb("er")]
    rd["rules"] = [copy.deepcopy(ER_RULE)]
    regimes = cfg["strategies"]["regimes"]
    regimes["trending"], regimes["unknown"] = regimes["unknown"], None
    return cfg


def _tb_detector(base: dict) -> dict:
    """A gated source: the base config with trading-bot/strategy_config.json's whole detector."""
    cfg = copy.deepcopy(base)
    cfg["regime_detector"] = copy.deepcopy(TB_CONFIG["regime_detector"])
    return cfg


def _fit(config, base, manifest, combines_as="regime_gate") -> list:
    return cv.source_fit_errors(config, base, manifest, combines_as, "v")


def _full(config, base, manifest, combines_as="regime_gate") -> list:
    """The whole reading-time check: D-159/D-160, then D-161 once those pass."""
    own = cv.config_vehicle_errors({"kind": "config", "config": config}, "v",
                                   combines_as=combines_as)
    return own or _fit(config, base, manifest, combines_as)


# ---------------------------------------------------------------------------
# the sources themselves
# ---------------------------------------------------------------------------

def test_the_committed_sources_are_what_the_probes_assume(sma50, rebase):
    for config, manifest in (sma50, rebase):
        assert cv._trading_regimes(config) == ["unknown"]
        assert config["regime_detector"]["components"] == []
        assert "/regime_detector" in manifest["scaffolding"]
    assert rebase[1]["scaffolding"][1:] == ["/strategies/regimes/trending",
                                            "/strategies/regimes/mean_reversion",
                                            "/strategies/regimes/chop"]
    assert [c["id"] for c in TB_CONFIG["regime_detector"]["components"]] == ["er", "vr", "vol"]
    assert TB_CONFIG["regime_detector"]["vetoes"][0]["id"] == "vol"


@pytest.mark.parametrize("which", ["sma50", "rebase"])
def test_the_source_config_itself_fits_its_source(which, request):
    config, manifest = request.getfixturevalue(which)
    for word in ("forecast_block", "regime_gate", None):
        assert _fit(copy.deepcopy(config), config, manifest, word) == []


# ---------------------------------------------------------------------------
# accepted
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("which", ["sma50", "rebase"])
def test_a_veto_gate_with_an_added_read_component_passes(which, request):
    config, manifest = request.getfixturevalue(which)
    assert _fit(_veto_gate(config), config, manifest) == []


def test_a_veto_gate_passes_the_whole_reading_check(rebase):
    config, manifest = rebase
    assert _full(_veto_gate(config), config, manifest) == []


@pytest.mark.parametrize("which", ["sma50", "rebase"])
def test_a_rules_gate_with_the_relabel_passes_and_its_derived_manifest_resolves(which, request):
    config, manifest = request.getfixturevalue(which)
    gate = _relabel_gate(config)
    assert cv.regime_relabel(config, gate, "regime_gate") == ("unknown", "trending")
    assert _fit(gate, config, manifest) == []
    derived = cv.derived_manifest(manifest, config, gate, "regime_gate")
    import block_manifest as bm
    assert bm.unresolved_paths(gate, derived) == []
    assert bm.unresolved_paths(gate, manifest) == ["/strategies/regimes/unknown/components/0"]


def test_the_relabel_gate_passes_the_whole_reading_check(rebase):
    config, manifest = rebase
    assert _full(_relabel_gate(config), config, manifest) == []


def test_derived_manifest_exact_output(rebase, sma50):
    config, manifest = rebase
    before = copy.deepcopy(manifest)
    derived = cv.derived_manifest(manifest, config, _relabel_gate(config), "regime_gate")
    assert derived == {
        "block": {"kind": "forecast",
                  "config_paths": ["/strategies/regimes/trending/components/0"]},
        "scaffolding": ["/regime_detector", "/strategies/regimes/unknown",
                        "/strategies/regimes/mean_reversion", "/strategies/regimes/chop"],
        "rationale": manifest["rationale"]}
    assert manifest == before                                   # pure
    s_config, s_manifest = sma50
    assert cv.derived_manifest(s_manifest, s_config, _relabel_gate(s_config), "regime_gate") == {
        **s_manifest, "block": {"kind": "forecast",
                                "config_paths": ["/strategies/regimes/trending/components/0"]}}
    # no relabel (not a regime gate, or the same trading regime): the manifest unchanged
    for gate, word in ((_relabel_gate(config), "forecast_block"), (_veto_gate(config), "regime_gate")):
        out = cv.derived_manifest(manifest, config, gate, word)
        assert out == manifest and out is not manifest


def test_rules_edited_with_the_components_kept_passes(rebase):
    config, manifest = rebase
    source = _tb_detector(config)
    gate = copy.deepcopy(source)
    gate["regime_detector"]["rules"][0]["any_of"][0][0]["value"] = 0.35
    del gate["regime_detector"]["vetoes"]
    gate["regime_detector"]["default_regime"] = "unknown"
    assert _full(gate, source, manifest) == []


def test_a_forecast_block_vehicle_changing_only_the_block_passes(rebase, sma50):
    for config, manifest in (rebase, sma50):
        vehicle = copy.deepcopy(config)
        comp = vehicle["strategies"]["regimes"]["unknown"]["components"][0]
        comp["params"]["period"] = 2
        assert _fit(vehicle, config, manifest, "forecast_block") == []
    vehicle = copy.deepcopy(rebase[0])
    vehicle["strategies"]["regimes"]["unknown"]["components"][0]["transforms"][0]["params"][
        "window"] = 90
    assert _full(vehicle, rebase[0], rebase[1], "forecast_block") == []


def test_a_missing_mode_reads_as_threshold_rules(rebase):
    config, manifest = rebase
    vehicle = copy.deepcopy(config)
    del vehicle["regime_detector"]["mode"]
    assert _fit(vehicle, config, manifest, "forecast_block") == []


# ---------------------------------------------------------------------------
# refused
# ---------------------------------------------------------------------------

def test_a_mode_change_is_refused(rebase):
    config, manifest = rebase
    source = _tb_detector(config)
    vehicle = copy.deepcopy(source)
    vehicle["regime_detector"]["mode"] = "score"
    assert _fit(vehicle, source, manifest) == [
        f"v.config: /regime_detector/mode differs from the source run's base config "
        f"(\"threshold_rules\" -> \"score\"): mode change under /regime_detector, {SCAFF}"
        f"{cv.GATE_SUFFIX}"]
    assert _fit(vehicle, source, manifest, "forecast_block") == [
        f"v.config: /regime_detector/mode differs from the source run's base config "
        f"(\"threshold_rules\" -> \"score\"): mode change under /regime_detector, {SCAFF}"]


def test_a_component_class_change_is_refused(rebase):
    config, manifest = rebase
    source = _tb_detector(config)
    vehicle = copy.deepcopy(source)
    vehicle["regime_detector"]["components"][0]["class"] = SC + "VarianceRatioComponent"
    assert _fit(vehicle, source, manifest) == [
        f"v.config: /regime_detector/components/0/class differs from the source run's base "
        f"config (\"{SC}EfficiencyRatioRegimeComponent\" -> \"{SC}VarianceRatioComponent\"): "
        f"detector component change under /regime_detector, {SCAFF}{cv.GATE_SUFFIX}"]


def test_a_component_params_change_is_refused(rebase):
    config, manifest = rebase
    source = _tb_detector(config)
    vehicle = copy.deepcopy(source)
    vehicle["regime_detector"]["components"][0]["params"]["period"] = 30
    assert _fit(vehicle, source, manifest) == [
        f"v.config: /regime_detector/components/0/params/period differs from the source run's "
        f"base config (24 -> 30): detector component change under /regime_detector, {SCAFF}"
        f"{cv.GATE_SUFFIX}"]
    # the whole reading check gets there too (the vehicle is a valid gate otherwise)
    assert _full(vehicle, source, manifest) == _fit(vehicle, source, manifest)


def test_a_component_removal_is_refused_and_long_values_are_cut(rebase):
    config, manifest = rebase
    source = _tb_detector(config)
    vehicle = copy.deepcopy(source)
    del vehicle["regime_detector"]["components"][1]                  # vr
    (err,) = _fit(vehicle, source, manifest)
    assert err.startswith("v.config: /regime_detector/components differs from the source run's "
                          "base config ([{"), err
    assert ", values truncated): detector component removal under /regime_detector, " in err
    assert err.endswith(SCAFF + cv.GATE_SUFFIX)
    shown = err.split(" (", 1)[1].split("): ", 1)[0]
    before, after = shown.replace(", values truncated", "").split(" -> ")
    assert len(before) == len(after) == cv.MAX_VALUE_CHARS and before.endswith("...")


def test_an_added_min_score_is_refused(rebase):
    config, manifest = rebase
    vehicle = _veto_gate(config)
    vehicle["regime_detector"]["min_score"] = 0.5
    assert _fit(vehicle, config, manifest) == [
        f"v.config: /regime_detector/min_score differs from the source run's base config "
        f"((absent) -> 0.5): structure change under /regime_detector, {SCAFF}{cv.GATE_SUFFIX}"]


def test_an_added_component_no_rule_or_veto_reads_is_refused(rebase):
    config, manifest = rebase
    vehicle = _veto_gate(config, unread=("er",))
    (err,) = _fit(vehicle, config, manifest)
    assert err.startswith("v.config: /regime_detector/components differs from the source run's "
                          "base config ([] -> [{"), err
    assert ("): added detector component that no rule or veto reads ['er'] under "
            "/regime_detector, ") in err


def test_a_forecast_block_vehicle_adding_a_gate_is_refused(rebase):
    config, manifest = rebase
    vehicle = _veto_gate(config)
    errs = _fit(vehicle, config, manifest, "forecast_block")
    assert [e.split("): ", 1)[1].split(" under ")[0] for e in errs] == [
        "added detector component ['vol']",
        "gate change, which only combines_as regime_gate (D-160) may make"]
    assert errs[1].startswith("v.config: /regime_detector/vetoes differs from the source run's "
                              "base config ((absent) -> [{")
    assert all(e.endswith(SCAFF) for e in errs)                  # no D-160 suffix


def test_no_manifest_is_refused(rebase):
    config, _manifest = rebase
    assert _fit(_relabel_gate(config), config, None) == [NO_MANIFEST]
    assert _fit(_relabel_gate(config), None, None) == [NO_MANIFEST]   # base never read


def test_a_manifest_that_does_not_resolve_is_refused(sma50, rebase):
    config, manifest = sma50
    moved = copy.deepcopy(config)                 # the strategy moved, but not a regime gate
    regimes = moved["strategies"]["regimes"]
    regimes["trending"], regimes["unknown"] = regimes["unknown"], None
    assert _fit(moved, config, manifest, "forecast_block") == [
        "v.config: the source run's block_manifest.yaml, checked against this config as the "
        "next run's base config: manifest path(s) ['/strategies/regimes/unknown/components/0'] "
        "do not resolve in the base config; keep every block and scaffolding path the source's "
        "manifest lists (D-110 runs this config with that manifest)"]
    # rebase: the null slot it lists as scaffolding is filled, too
    r_config, r_manifest = rebase
    errs = _fit(_relabel_gate(r_config), r_config, r_manifest, "forecast_block")
    assert [e.split("): ", 1)[1].split(" under ")[0] for e in errs[:-1]] == [
        "added detector component ['er']",
        "gate change, which only combines_as regime_gate (D-160) may make",
        "structure change"]
    assert errs[2].startswith("v.config: /strategies/regimes/trending differs from the source "
                              "run's base config (null -> {")
    assert "do not resolve in the base config" in errs[-1]


def test_a_derived_manifest_that_does_not_resolve_names_the_relabel(rebase):
    config, manifest = rebase
    gate = _relabel_gate(config)
    del gate["strategies"]["regimes"]["mean_reversion"]
    errs = _fit(gate, config, manifest)
    assert errs[0].startswith("v.config: /strategies/regimes/mean_reversion differs from the "
                              "source run's base config (null -> (absent)): structure change "
                              "under /strategies/regimes/mean_reversion, "), errs
    assert errs[-1].startswith(
        "v.config: the source run's block_manifest.yaml with regime 'unknown' relabelled "
        "'trending' (D-161), checked against this config as the next run's base config: "
        "manifest path(s) ['/strategies/regimes/mean_reversion'] do not resolve"), errs


def test_more_differences_than_the_cap_are_counted(rebase):
    config, manifest = rebase
    source = _tb_detector(config)
    vehicle = copy.deepcopy(source)
    for c in vehicle["regime_detector"]["components"]:
        c["params"] = {k: v + 1 for k, v in c["params"].items()}
        c["class"] += "X"
    n = sum(len(c["params"]) + 1 for c in vehicle["regime_detector"]["components"])
    assert n > cv.MAX_SCAFFOLDING_DIFFS
    errs = _fit(vehicle, source, manifest)
    assert len(errs) == cv.MAX_SCAFFOLDING_DIFFS + 1
    assert errs[-1] == (f"v.config: and {n - cv.MAX_SCAFFOLDING_DIFFS} more difference(s) "
                        f"under the source's scaffolding (not listed)")


def test_the_relabel_needs_exactly_one_trading_regime_on_each_side(rebase):
    config, _manifest = rebase
    two = _relabel_gate(config)
    two["strategies"]["regimes"]["chop"] = copy.deepcopy(two["strategies"]["regimes"]["trending"])
    assert cv.regime_relabel(config, two, "regime_gate") is None
    assert cv.regime_relabel(config, _relabel_gate(config), "forecast_block") is None
    assert cv.regime_relabel(config, _veto_gate(config), "regime_gate") is None


def test_a_malformed_detector_is_a_refusal_never_a_crash(rebase):
    config, manifest = rebase
    for rd in ([], None, {"components": "er", "rules": {"a": 1}, "vetoes": 5},
               {"components": [1, {"id": ["x"]}], "rules": [{"any_of": [[{"id": 3}]]}]},
               {1: "a", "b": 2}):
        vehicle = dict(copy.deepcopy(config), regime_detector=rd)
        for word in ("regime_gate", "forecast_block"):
            errs = _fit(vehicle, config, manifest, word)
            assert errs and all(isinstance(e, str) for e in errs), (rd, word)
    assert cv._shown(True, {1: "a", "b": 2}) == ("{1: 'a', 'b': 2}", False)


def test_scaffolding_errors_is_pure(rebase):
    config, manifest = rebase
    source = _tb_detector(config)
    vehicle = _veto_gate(source)
    before = (copy.deepcopy(vehicle), copy.deepcopy(source), copy.deepcopy(manifest))
    cv.scaffolding_errors(vehicle, source, manifest, "regime_gate", "v")
    cv.source_fit_errors(vehicle, source, manifest, "regime_gate", "v")
    assert (vehicle, source, manifest) == before


# ---------------------------------------------------------------------------
# review fixes: the ungated twin, added components only after the source's, finer labels,
# truncated pointers, the cycle refusal
# ---------------------------------------------------------------------------

def _with_scaffolding(manifest: dict, pointer: str) -> dict:
    """The manifest with its first scaffolding pointer (/regime_detector) replaced."""
    out = copy.deepcopy(manifest)
    assert out["scaffolding"][0] == "/regime_detector"
    out["scaffolding"][0] = pointer
    return out


@pytest.mark.parametrize("pointer", ["/regime_detector/vetoes", "/regime_detector/rules/0"])
def test_a_scaffolding_pointer_under_the_gate_is_accepted_for_the_twin(rebase, pointer):
    """Probe P1, re-pointed by D-162 (review A): a scaffolding pointer under the gate resolves
    in the gated config but not in its ungated twin (rules [], vetoes dropped). The twin is the
    run's design variant and 5a checks a variant on BLOCK paths only (a variant may change
    scaffolding), so reading time no longer refuses it (D-161 checked the twin in full)."""
    config, manifest = rebase
    source = _tb_detector(config)               # rules and vetoes: the source is gated already
    gate = copy.deepcopy(source)
    assert _fit(gate, source, _with_scaffolding(manifest, pointer)) == []
    assert _full(gate, source, _with_scaffolding(manifest, pointer)) == []
    # an ordinary accepted gate: the same config with the scaffolding /regime_detector
    assert _full(gate, source, manifest) == []
    assert _fit(gate, source, _with_scaffolding(manifest, pointer), "forecast_block") == []


def _with_gate_block_path(manifest: dict, pointer: str) -> dict:
    """The manifest with /regime_detector narrowed to its components (scaffolding) and
    `pointer`, a piece of the gate, added to the BLOCK paths."""
    out = _with_scaffolding(manifest, "/regime_detector/components")
    out["block"]["config_paths"] = out["block"]["config_paths"] + [pointer]
    return bm.validate_manifest(out)


@pytest.mark.parametrize("pointer", ["/regime_detector/vetoes", "/regime_detector/rules/0"])
def test_a_block_path_the_ungated_twin_cannot_resolve_is_refused(rebase, pointer):
    """D-162 (review A): a BLOCK path under the gate resolves in the gated config but not in
    its ungated twin, which 5a would leave untested: refused, by the check decide-next runs
    too (config_vehicle.twin_missing_block_paths)."""
    config, manifest = rebase
    source = _tb_detector(config)
    gate = copy.deepcopy(source)
    m = _with_gate_block_path(manifest, pointer)
    expected = [
        "v.config: the ungated twin (D-052: rules [], vetoes dropped; the run's design variant) "
        f"does not resolve the block path(s) ['{pointer}'] of the source run's "
        "block_manifest.yaml; keep every block path outside the gate, so the twin still holds "
        "the block (5a does not test a variant that loses one)"]
    assert _fit(gate, source, m) == expected
    assert _full(gate, source, m) == expected
    assert cv.twin_missing_block_paths(cv.derived_manifest(m, source, gate, "regime_gate"),
                                       cv.ungated_twin(gate)) == [pointer]
    # not a regime gate: no twin, nothing to refuse
    assert _fit(gate, source, m, "forecast_block") == []


def test_the_twin_is_checked_only_once_the_config_fits(rebase):
    config, manifest = rebase
    gate = _relabel_gate(config)
    del gate["strategies"]["regimes"]["mean_reversion"]
    errs = _fit(gate, config, manifest)
    assert sum("do not resolve" in e for e in errs) == 1
    assert not any("ungated twin" in e for e in errs)


def _er_source(config: dict) -> dict:
    """The source with one detector component (trading-bot's `er`) and a rule reading it."""
    source = copy.deepcopy(config)
    source["regime_detector"]["components"] = [_tb("er")]
    source["regime_detector"]["rules"] = [copy.deepcopy(ER_RULE)]
    return source


def _vol_veto(source: dict, at: int) -> dict:
    gate = copy.deepcopy(source)
    gate["regime_detector"]["components"].insert(at, _tb("vol"))
    gate["regime_detector"]["vetoes"] = copy.deepcopy(TB_CONFIG["regime_detector"]["vetoes"])
    return gate


def test_an_added_read_component_before_the_source_s_is_refused(rebase):
    """Probe P5: `vol` inserted at index 0 moves the source's `er` off
    /regime_detector/components/0, the pointer the manifest lists as scaffolding."""
    config, manifest = rebase
    source = _er_source(config)
    label = "added detector component must follow the source's components"
    m = _with_scaffolding(manifest, "/regime_detector/components/0")
    errs = _fit(_vol_veto(source, 0), source, m)
    assert errs and all(e.startswith("v.config: /regime_detector/components/0/") for e in errs)
    assert all(f"): {label} under /regime_detector/components/0, " in e for e in errs), errs
    assert any(e.startswith('v.config: /regime_detector/components/0/id differs from the source '
                            'run\'s base config ("er" -> "vol"): ') for e in errs), errs
    (err,) = _fit(_vol_veto(source, 0), source, manifest)               # /regime_detector
    assert err.startswith("v.config: /regime_detector/components differs from the source run's "
                          "base config ([{"), err
    assert f"): {label} under /regime_detector, " in err


def test_an_added_read_component_after_the_source_s_passes(rebase):
    config, manifest = rebase
    source = _er_source(config)
    for m in (manifest, _with_scaffolding(manifest, "/regime_detector/components/0")):
        assert _fit(_vol_veto(source, 1), source, m) == []


def test_a_reordered_source_component_is_a_swap_and_a_changed_one_a_change(rebase):
    config, manifest = rebase
    source = _tb_detector(config)
    vehicle = copy.deepcopy(source)
    comps = vehicle["regime_detector"]["components"]
    comps[0], comps[1] = comps[1], comps[0]                                  # er <-> vr
    errs = [e for e in _fit(vehicle, source, manifest) if " more difference(s) " not in e]
    assert errs and all("): detector component swap under /regime_detector, " in e
                        for e in errs), errs
    vehicle = copy.deepcopy(source)
    vehicle["regime_detector"]["components"][2]["params"] = {"x": 1}
    errs = _fit(vehicle, source, manifest)
    assert errs and all("): detector component change under /regime_detector, " in e
                        for e in errs), errs


def test_long_pointers_are_cut_and_said_so(rebase):
    config, manifest = rebase
    vehicle = _veto_gate(config)
    vehicle["regime_detector"]["k" * 100] = 1
    long_p = "/regime_detector/" + "k" * 100
    shown = long_p[:cv.MAX_VALUE_CHARS - 3] + "..."
    (err,) = _fit(vehicle, config, manifest)
    assert err == (f"v.config: {shown} differs from the source run's base config ((absent) -> 1, "
                   f"pointer truncated): structure change under /regime_detector, {SCAFF}"
                   f"{cv.GATE_SUFFIX}")
    (err,) = _fit(vehicle, config, _with_scaffolding(manifest, long_p))
    assert err.startswith(f"v.config: {shown} differs from the source run's base config "
                          f"((absent) -> 1, pointers truncated): structure change under "
                          f"{shown}, "), err


CYCLE = "v.config: the config refers to itself (a YAML alias cycle); write it out in full"


def test_a_config_that_refers_to_itself_is_refused_not_a_crash(rebase):
    """D-161 lead decision: a YAML alias cycle (yaml.safe_load builds one) under a path the
    manifest does not list (/strategies/notes) is a refusal, before any other step."""
    config, _manifest = rebase
    loop = yaml.safe_load("notes: &n {again: *n}\n")["notes"]
    assert loop["again"] is loop
    vehicle = _veto_gate(config)
    vehicle["strategies"]["notes"] = loop
    for word in ("regime_gate", "forecast_block", None):
        assert cv.config_vehicle_errors({"kind": "config", "config": vehicle}, "v",
                                        combines_as=word) == [CYCLE]
    # a shared alias that is not a cycle is no refusal
    shared = {"a": 1}
    assert cv.cycle_error({"x": shared, "y": [shared, shared]}, "v.config") is None
    assert cv.cycle_error(vehicle, "v.config") == CYCLE


# ---------------------------------------------------------------------------
# the wiring (no switch, D-162)
# ---------------------------------------------------------------------------

def _source_run(tmp_path, config, manifest, name="run_x") -> Path:
    run_dir = tmp_path / name
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text(
        json.dumps(config), encoding="utf-8")
    if manifest is not None:
        (run_dir / "artifacts" / "block_manifest.yaml").write_text(
            yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return run_dir


def _doc(config, combines_as="regime_gate") -> dict:
    return _reading(_claim(), vehicle={"kind": "config", "config": config},
                    combines_as=combines_as, fold_observed="A")


@pytest.fixture()
def routed(monkeypatch):
    monkeypatch.setattr(rpr, "_claim_check_kw", lambda: {"folds": True})


def test_on_the_reading_check_accepts_a_gate_that_keeps_the_scaffolding(routed, tmp_path,
                                                                        rebase):
    config, manifest = rebase
    run_dir = _source_run(tmp_path, config, manifest)
    for vehicle in (_relabel_gate(config), _veto_gate(config)):
        rp.check_reading(_doc(vehicle), CAT, "reading", from_model=True, envelope=True)
        assert rpr._reading_content_errors(_doc(vehicle), CAT, run_dir) == []


def test_on_the_reading_check_refuses_a_scaffolding_rewrite(routed, tmp_path, rebase):
    config, manifest = rebase
    source = _tb_detector(config)
    run_dir = _source_run(tmp_path, source, manifest)
    vehicle = copy.deepcopy(source)
    vehicle["regime_detector"]["components"][0]["params"]["period"] = 30
    assert rpr._reading_content_errors(_doc(vehicle), CAT, run_dir) == [
        f"side_findings[0].vehicle.config: /regime_detector/components/0/params/period differs "
        f"from the source run's base config (24 -> 30): detector component change under "
        f"/regime_detector, {SCAFF}{cv.GATE_SUFFIX}"]


def test_on_the_reading_check_refuses_a_source_without_a_manifest(routed, tmp_path, rebase):
    config, _manifest = rebase
    run_dir = _source_run(tmp_path, config, None)
    assert rpr._reading_content_errors(_doc(_relabel_gate(config)), CAT, run_dir) == [
        NO_MANIFEST.replace("v: ", "side_findings[0].vehicle: ", 1)]


def test_on_an_unreadable_manifest_or_base_config_is_a_refusal(routed, tmp_path, rebase):
    config, manifest = rebase
    run_dir = _source_run(tmp_path, config, manifest)
    (run_dir / "artifacts" / "block_manifest.yaml").write_text("block: [", encoding="utf-8")
    (err,) = rpr._reading_content_errors(_doc(_relabel_gate(config)), CAT, run_dir)
    assert err.startswith("side_findings[0].vehicle: the source run's block_manifest.yaml cannot "
                          "be read (block_manifest.yaml: unparseable YAML"), err
    assert str(run_dir) not in err
    run_dir = _source_run(tmp_path, config, manifest, name="run_y")
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text("{", encoding="utf-8")
    (err,) = rpr._reading_content_errors(_doc(_relabel_gate(config)), CAT, run_dir)
    assert err.startswith("side_findings[0].vehicle: the base config "
                          "artifacts/candidate_strategy_config.json cannot be read ("), err


def test_on_the_source_check_runs_only_once_the_config_check_passes(routed, tmp_path, rebase,
                                                                    monkeypatch):
    config, _manifest = rebase
    run_dir = _source_run(tmp_path, config, None)          # no manifest: would be refused
    calls = []
    monkeypatch.setattr(cv, "source_fit_errors", lambda *a: calls.append(a) or [])
    errs = rpr._reading_content_errors(_doc(copy.deepcopy(config)), CAT, run_dir)  # no gate
    assert errs and all("combines_as regime_gate" in e for e in errs), errs
    assert calls == []
    assert rpr._reading_content_errors(_doc(_relabel_gate(config)), CAT, run_dir) == []
    assert len(calls) == 1


def _two_vehicles(config) -> dict:
    """A reading with a config vehicle (side finding 0) and a patch vehicle (side finding 1)."""
    doc = _doc(_veto_gate(config))
    comp = config["strategies"]["regimes"]["unknown"]["components"][0]
    patch = [{"component_id": comp["id"], "field": "params.period",
              "before": comp["params"]["period"], "after": comp["params"]["period"] + 1}]
    doc["side_findings"].append(dict(copy.deepcopy(doc["side_findings"][0]),
                                     proposal_id=f"{CAT}-run_src-2", vehicle=patch,
                                     combines_as="forecast_block"))
    return doc


def test_on_a_config_and_a_patch_vehicle_share_one_base_read(routed, tmp_path, rebase,
                                                              monkeypatch):
    config, manifest = rebase
    run_dir = _source_run(tmp_path, config, manifest)
    reads, read_text = [], Path.read_text

    def counting(self, *a, **kw):
        if self.name == "candidate_strategy_config.json":
            reads.append(self)
        return read_text(self, *a, **kw)

    monkeypatch.setattr(Path, "read_text", counting)
    assert rpr._reading_content_errors(_two_vehicles(config), CAT, run_dir) == []
    assert len(reads) == 1


def test_on_an_unreadable_base_config_both_vehicles_are_refused(routed, tmp_path, rebase):
    """The base config cannot be read (a directory): both side findings are refused with the
    one read's error; the config vehicle's message has the run directory stripped (as the
    manifest error), the patch vehicle's is today's message, unchanged."""
    config, manifest = rebase
    run_dir = _source_run(tmp_path, config, manifest)
    path = run_dir / "artifacts" / "candidate_strategy_config.json"
    path.unlink()
    path.mkdir()
    try:
        path.read_text(encoding="utf-8")
    except OSError as exc:
        raw = str(exc)
    rel = "artifacts/candidate_strategy_config.json"
    errs = rpr._reading_content_errors(_two_vehicles(config), CAT, run_dir)
    assert errs == [
        f"side_findings[0].vehicle: the base config {rel} cannot be read "
        f"({raw.replace(repr(str(path))[1:-1], rel)})",
        f"side_findings[1].vehicle: the base config {rel} cannot be read ({raw})"]
    assert str(run_dir) not in errs[0] and repr(str(run_dir))[1:-1] not in errs[0]
    assert repr(str(path))[1:-1] in raw          # the OSError names the path (the patch keeps it)


def test_on_a_cyclic_config_vehicle_is_a_refusal(routed, tmp_path, rebase):
    config, manifest = rebase
    run_dir = _source_run(tmp_path, config, manifest)
    vehicle = _veto_gate(config)
    vehicle["strategies"]["notes"] = yaml.safe_load("n: &n [*n]\n")["n"]
    assert rpr._reading_content_errors(_doc(vehicle), CAT, run_dir) == [
        CYCLE.replace("v.config", "side_findings[0].vehicle.config")]


def test_a_config_vehicle_is_accepted_by_the_shape_check_with_no_switch(rebase):
    assert not hasattr(rp, "CONFIG_VEHICLE_ROUTED")
    rp.check_reading(_doc(_relabel_gate(rebase[0])), CAT, "reading", from_model=True,
                     envelope=True)
