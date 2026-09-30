"""
D-051 / D-053 config checks (tools/forecast_rules.py) and their wiring.

Covers:
  1. the on/off class set is read from COMPONENT_CATALOG.md's Kind column, and
     a missing or unreadable catalogue fails loud (never an empty set);
  2. D-051: an on/off class, or a threshold_filter / volume_filter transform,
     on a component in `strategies` is refused; the regime detector is not
     checked;
  3. D-053: a variant's component classes equal the base config's (parameter
     and transform changes pass; add / remove / replace / regime -> null do not);
  4. right after 1b: a refused base config goes back to 1b ONCE with the error,
     the second refusal pauses (forecast_rule_violation), a decide_next
     pass-through config pauses at once; every refusal is recorded;
  5. 5a: checked on the config AFTER the patch (a patch removing the banned
     piece passes), the refusal is a config error for the existing route, and
     run_campaign classifies the new pause.

No LLM, no backtest. tests/conftest.py sandboxes rpr.ROOT.
"""
import asyncio
import copy
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import forecast_rules as fr  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402

SC = "strategies.strategy_components."
ON_OFF = {"SmaTrendLongOnlyComponent", "GatedSmaTrendLongOnlyComponent",
          "FundingRateMeanReversionComponent", "FearGreedContrarianComponent",
          "MacdHistogramCrossoverComponent", "WhaleLargeTradeImbalanceComponent",
          "VolumeExpansionHedgeComponent"}

CONFIG = {
    "regime_detector": {"mode": "threshold_rules",
                        "components": [{"id": "er", "class": SC + "EfficiencyRatioRegimeComponent",
                                        "params": {"period": 24}}],
                        "rules": [], "default_regime": "unknown"},
    "strategies": {"warmup": 51, "regimes": {
        "unknown": {"components": [
            {"id": "rsi", "class": SC + "RSIPullbackComponent", "params": {"period": 14},
             "weight": 1.0, "transforms": [{"op": "identity"}, {"op": "clip",
                                                               "params": {"min": -20, "max": 20}}]},
        ]},
        "trending": None, "mean_reversion": None, "chop": None}},
}
MANIFEST = {
    "block": {"kind": "forecast", "config_paths": ["/strategies/regimes/unknown/components/0"]},
    "scaffolding": ["/strategies/warmup", "/regime_detector"],
    "rationale": "the RSI pullback component is the idea",
}
COMP0 = "/strategies/regimes/unknown/components/0"


def _cfg(**comp_overrides) -> dict:
    cfg = copy.deepcopy(CONFIG)
    cfg["strategies"]["regimes"]["unknown"]["components"][0].update(comp_overrides)
    return cfg


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


# ---------------------------------------------------------------------------
# 1. The catalogue's Kind column
# ---------------------------------------------------------------------------

def test_on_off_classes_are_the_catalogue_on_off_rows():
    assert fr.on_off_classes() == frozenset(ON_OFF)


CATALOG_HEAD = "# c\n<!-- CATALOG:START -->\n| Class | p | o | r | Kind |\n|---|---|---|---|---|\n"


@pytest.mark.parametrize("text,match", [
    (None, "not found"),
    ("# no markers\n| `A` | p | o | r | on/off |\n", "CATALOG:START"),
    (CATALOG_HEAD + "<!-- CATALOG:END -->\n", "no component rows"),
    (CATALOG_HEAD + "| `A` | p | o |\n<!-- CATALOG:END -->\n", "without a Kind"),
    (CATALOG_HEAD + "| `A` | p | o | r | graded |\n<!-- CATALOG:END -->\n", "no row has Kind"),
], ids=["missing", "no_markers", "no_rows", "no_kind_cell", "no_on_off"])
def test_catalogue_problems_fail_loud(tmp_path, text, match):
    path = tmp_path / "COMPONENT_CATALOG.md"
    if text is not None:
        path.write_text(text, encoding="utf-8")
    with pytest.raises(fr.CatalogError, match=match):
        fr.on_off_classes(path)


def test_catalogue_parser_reads_a_minimal_table(tmp_path):
    path = tmp_path / "c.md"
    path.write_text(CATALOG_HEAD + "| `A` | p | o | r | on/off |\n| `B` | p | o | r | graded |\n"
                    "<!-- CATALOG:END -->\n", encoding="utf-8")
    assert fr.on_off_classes(path) == frozenset({"A"})


# ---------------------------------------------------------------------------
# 2. D-051 on one config
# ---------------------------------------------------------------------------

def test_a_graded_config_passes():
    assert fr.strategies_violations(CONFIG, fr.on_off_classes()) == []


@pytest.mark.parametrize("name", sorted(ON_OFF))
def test_every_on_off_class_is_refused_in_strategies(name):
    msgs = fr.strategies_violations(_cfg(**{"class": SC + name}), fr.on_off_classes())
    assert len(msgs) == 1 and msgs[0].startswith("D-051: on/off class " + name)
    assert "strategies.regimes.unknown.components[0]" in msgs[0]


@pytest.mark.parametrize("key,op", [("transforms", "threshold_filter"),
                                    ("transforms", "volume_filter"),
                                    ("history_transforms", "threshold_filter"),
                                    ("history_transforms", "volume_filter")])
def test_dead_zone_ops_are_refused_in_both_pipelines(key, op):
    cfg = _cfg(**{key: [{"op": "identity"}, {"op": op, "params": {"min_abs": 1.0}}]})
    msgs = fr.strategies_violations(cfg, fr.on_off_classes())
    assert msgs == [msgs[0]] and f"dead-zone op '{op}'" in msgs[0]
    assert f"components[0].{key}[1]" in msgs[0]


def test_the_regime_detector_is_not_checked():
    cfg = copy.deepcopy(CONFIG)
    cfg["regime_detector"]["components"].append(
        {"id": "sma_on", "class": SC + "SmaTrendLongOnlyComponent",
         "transforms": [{"op": "threshold_filter"}]})
    assert fr.strategies_violations(cfg, fr.on_off_classes()) == []


def test_malformed_pieces_are_left_to_validate_config():
    cfg = copy.deepcopy(CONFIG)
    cfg["strategies"]["regimes"]["chop"] = {"components": ["not a dict", {"transforms": "x"}]}
    assert fr.strategies_violations(cfg, fr.on_off_classes()) == []
    assert fr.strategies_violations({"strategies": []}, fr.on_off_classes()) == []


# ---------------------------------------------------------------------------
# 3. D-053 between base and variant
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mutate", [
    lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]["params"].update(period=21),
    lambda c: c["strategies"]["regimes"]["unknown"]["components"][0]["transforms"].append(
        {"op": "scale", "params": {"factor": 2}}),
    lambda c: c["regime_detector"]["components"][0]["params"].update(period=48),
    lambda c: c["strategies"]["regimes"]["unknown"]["components"][0].update(weight=0.5),
], ids=["param", "transform", "detector_param", "weight"])
def test_parameter_and_transform_changes_keep_the_classes(mutate):
    var = copy.deepcopy(CONFIG)
    mutate(var)
    assert fr.class_mismatch(CONFIG, var) == []


@pytest.mark.parametrize("mutate,where", [
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"][0].update(
        {"class": SC + "EMASpreadComponent"}), "strategies.regimes.unknown"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"].append(
        {"id": "b", "class": SC + "BuyAndHoldStrategy", "weight": 1.0}), "strategies.regimes.unknown"),
    (lambda c: c["strategies"]["regimes"]["unknown"]["components"].pop(), "strategies.regimes.unknown"),
    (lambda c: c["strategies"]["regimes"].update(unknown=None), "strategies.regimes.unknown"),
    (lambda c: c["strategies"]["regimes"].update(
        chop={"components": [{"id": "x", "class": SC + "RSIPullbackComponent"}]}),
     "strategies.regimes.chop"),
    (lambda c: c["regime_detector"]["components"][0].update(
        {"class": SC + "VarianceRatioComponent"}), "regime_detector.components"),
], ids=["replace", "add", "remove", "regime_to_null", "regime_from_null", "detector_class"])
def test_adding_removing_or_replacing_a_component_is_refused(mutate, where):
    var = copy.deepcopy(CONFIG)
    mutate(var)
    msgs = fr.class_mismatch(CONFIG, var)
    assert len(msgs) == 1 and msgs[0].startswith("D-053:") and where in msgs[0]


# ---------------------------------------------------------------------------
# 4. Right after 1b
# ---------------------------------------------------------------------------

def _authored_1b(run_id: str, config: dict, manifest=MANIFEST, brief: dict | None = None) -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": config,
                                                "config_rationale": ["x"], "component_gap": None})
    rpr.save_yaml(arts / "decision.yaml", {"stage": "strategy_config_authoring",
                                           "status": "spec_ready", "rationale": "x",
                                           "blocking_issues": []})
    if manifest is not None:
        (arts / "block_manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    if brief is not None:
        rpr.save_yaml(arts / "research_brief.yaml", brief)
    return run_dir


def _refusals(run_dir: Path) -> list:
    path = run_dir / "artifacts" / "forecast_rule_refusals.yaml"
    return (rpr.load_yaml(path) or {}).get("refusals", []) if path.exists() else []


ON_OFF_BASE = _cfg(**{"class": SC + "SmaTrendLongOnlyComponent"})


def test_post_1b_clean_base_goes_on_and_records_nothing():
    run_dir = _authored_1b("run_901", CONFIG)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert _refusals(run_dir) == []
    assert "block_manifest_retry" not in rpr.load_yaml(run_dir / "pipeline_state.yaml")


def test_post_1b_refusal_retries_1b_once_then_pauses():
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _authored_1b("run_902", ON_OFF_BASE)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    retry = state["block_manifest_retry"]
    assert retry["attempts"] == 1 and retry["last_check"] == "forecast_rules"
    assert "D-051: on/off class SmaTrendLongOnlyComponent" in retry["last_error"]
    assert state["status"] == "active" and not state["flags"].get("forecast_rule_violation")
    # the retry's handoff carries the error, under its own key
    handoff = {"required_inputs": []}
    rpr._apply_block_manifest_retry_context("strategy_config_authoring", handoff, run_dir)
    ctx = handoff["injected_context"]
    assert "SmaTrendLongOnlyComponent" in ctx["forecast_rule_error"]
    assert "block_manifest_error" not in ctx
    # second refusal: pause, never a raise, never a third 1b pass
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human"
    assert state["flags"]["forecast_rule_violation"] is True
    assert state["block_manifest_retry"]["attempts"] == 1
    # every refusal recorded, append-only
    refusals = _refusals(run_dir)
    assert [(r["stage"], r["variant_id"], r["attempt"]) for r in refusals] == [
        ("strategy_config_authoring", "base", 0), ("strategy_config_authoring", "base", 1)]


def test_post_1b_retry_that_passes_resets_the_counter():
    run_dir = _authored_1b("run_903", ON_OFF_BASE)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    rpr.save_yaml(run_dir / "artifacts" / "backtest_spec.yaml",
                  {"status": "spec_ready", "config": CONFIG, "config_rationale": ["x"],
                   "component_gap": None})
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["block_manifest_retry"]["attempts"] == 0
    assert len(_refusals(run_dir)) == 1


def test_post_1b_pass_through_candidate_pauses_at_once():
    """decide_next hashed the config AFTER its reader patch; 1b must copy it
    verbatim, so a retry of 1b cannot fix it: refused, paused, recorded."""
    brief = {"candidate": {"source": {"expected_config_sha256": "ab" * 32}}}
    run_dir = _authored_1b("run_904", _cfg(transforms=[{"op": "threshold_filter",
                                                        "params": {"min_abs": 5}}]), brief=brief)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["flags"]["forecast_rule_violation"] is True
    assert state["block_manifest_retry"]["attempts"] == 0
    assert "threshold_filter" in _refusals(run_dir)[0]["violations"][0]


def test_post_1b_pass_through_candidate_whose_patch_removed_the_banned_piece_passes():
    brief = {"candidate": {"source": {"expected_config_sha256": "ab" * 32}}}
    run_dir = _authored_1b("run_905", CONFIG, brief=brief)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert _refusals(run_dir) == []


def test_post_1b_manifest_error_keeps_its_own_path_and_carries_the_rule_error():
    run_dir = _authored_1b("run_906", ON_OFF_BASE, manifest=None)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    retry = rpr.load_yaml(run_dir / "pipeline_state.yaml")["block_manifest_retry"]
    assert "is missing" in retry["last_error"] and "also: D-051" in retry["last_error"]
    assert retry["last_check"] == "block_manifest"
    with pytest.raises(RuntimeError, match="still invalid"):
        rpr.determine_post_strategy_config_authoring_route(run_dir)


def test_a_manifest_error_after_a_rules_pause_and_reset_is_labelled_a_manifest_error():
    """Review F1: update_state MERGES block_manifest_retry, so every write sets
    last_check. Sequence: two rule refusals (pause), the RUNBOOK reset
    (attempts 0), then 1b fixes the config but drops the manifest -- the retry
    must carry block_manifest_error, not a D-051 message."""
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _authored_1b("run_907", ON_OFF_BASE)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "human_pause"
    rpr.update_state(path=run_dir, status="active", flags={"forecast_rule_violation": False},
                     block_manifest_retry={"attempts": 0})
    rpr.save_yaml(run_dir / "artifacts" / "backtest_spec.yaml",
                  {"status": "spec_ready", "config": CONFIG, "config_rationale": ["x"],
                   "component_gap": None})
    (run_dir / "artifacts" / "block_manifest.yaml").unlink()
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    retry = rpr.load_yaml(run_dir / "pipeline_state.yaml")["block_manifest_retry"]
    assert retry["last_check"] == "block_manifest" and "is missing" in retry["last_error"]
    handoff = {"required_inputs": []}
    rpr._apply_block_manifest_retry_context("strategy_config_authoring", handoff, run_dir)
    assert "is missing" in handoff["injected_context"]["block_manifest_error"]
    assert "forecast_rule_error" not in handoff["injected_context"]


def test_a_success_reset_clears_last_check():
    run_dir = _authored_1b("run_908", ON_OFF_BASE)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    rpr.save_yaml(run_dir / "artifacts" / "backtest_spec.yaml",
                  {"status": "spec_ready", "config": CONFIG, "config_rationale": ["x"],
                   "component_gap": None})
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["block_manifest_retry"] == {
        "attempts": 0, "last_error": None, "last_check": None}


def test_a_manifest_error_on_the_rules_retry_fails_loud():
    """The D-051 retry spends the one 1b retry the manifest also uses (operator:
    reuse the manifest retry path): a bad manifest on that retry raises."""
    run_dir = _authored_1b("run_909", ON_OFF_BASE)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    rpr.save_yaml(run_dir / "artifacts" / "backtest_spec.yaml",
                  {"status": "spec_ready", "config": CONFIG, "config_rationale": ["x"],
                   "component_gap": None})
    (run_dir / "artifacts" / "block_manifest.yaml").unlink()
    with pytest.raises(RuntimeError, match="still invalid"):
        rpr.determine_post_strategy_config_authoring_route(run_dir)


@pytest.mark.parametrize("content", ["- a list\n", "refusals: not-a-list\n"])
def test_an_unreadable_refusal_record_is_never_overwritten(content):
    """Review F6: a record that is not {refusals: [...]} raises instead of being
    replaced (that would lose earlier refusals)."""
    run_dir = _authored_1b("run_920", ON_OFF_BASE)
    record = run_dir / "artifacts" / "forecast_rule_refusals.yaml"
    record.write_text(content, encoding="utf-8")
    with pytest.raises(RuntimeError, match="refusing to overwrite"):
        rpr.determine_post_strategy_config_authoring_route(run_dir)
    assert record.read_text(encoding="utf-8") == content


def test_run_loop_sends_a_refused_base_back_to_1b_then_pauses(monkeypatch):
    """run_loop really re-enters strategy_config_authoring with the D-051 error
    in its handoff, then pauses (not fails) on a second refusal --
    innovation_expansion is never invoked."""
    import shutil
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _authored_1b("run_921", ON_OFF_BASE)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = "strategy_config_authoring"
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    handoff_name = "hypothesis_to_strategy_config_authoring.yaml"
    (run_dir / "handoffs").mkdir(exist_ok=True)
    shutil.copy(SR_ROOT / "workflow_artifacts" / "templates" / "handoffs" / handoff_name,
                run_dir / "handoffs" / handoff_name)
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text("hypothesis_id: H-1\n",
                                                                encoding="utf-8")
    docs = rpr.ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "COMPONENT_CATALOG.md").write_text("catalogue\n", encoding="utf-8")
    (docs / "STRATEGY_DESIGN_GUIDE.md").write_text("guide\n", encoding="utf-8")
    seen = []

    async def _fake_invoke(stage_name, run_id, retry_context=None):
        handoff = rpr.load_yaml(run_dir / "handoffs" / handoff_name)
        rpr._apply_block_manifest_retry_context(stage_name, handoff, run_dir)
        seen.append((stage_name, (handoff.get("injected_context") or {}).get("forecast_rule_error")))

    monkeypatch.setattr(rpr, "async_invoke_agent", _fake_invoke)
    rpr.run_loop("run_921")
    assert [s for s, _ in seen] == ["strategy_config_authoring", "strategy_config_authoring"]
    assert seen[0][1] is None and "SmaTrendLongOnlyComponent" in seen[1][1]
    final = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert final["status"] == "paused_for_human"
    assert final["pending_stage"] == "strategy_config_authoring"
    assert final["flags"]["forecast_rule_violation"] is True


def test_run_campaign_classifies_the_pause(tmp_path):
    assert camp._classify_human_pause(tmp_path, {"flags": {"forecast_rule_violation": True}}) \
        == "forecast_rule_violation"
    assert ("forecast_rule_violation", "forecast_rule_violation") in camp._PAUSE_FLAG_TO_REASON


# ---------------------------------------------------------------------------
# 5. Step 5a
# ---------------------------------------------------------------------------

def _ok_subprocess(*a, **k):
    class _Ok:
        returncode, stdout, stderr = 0, "", ""
    return _Ok()


def _run_5a(monkeypatch, run_id: str, base: dict, variants: list) -> dict:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": base,
                                                "config_rationale": ["x"], "component_gap": None})
    rpr.save_yaml(arts / "variant_patches.yaml", {"variants": [
        {"variant_id": "base", "patch": [], "rationale": "base"}, *variants]})
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(MANIFEST), encoding="utf-8")
    monkeypatch.setattr(rpr.subprocess, "run", _ok_subprocess)
    asyncio.run(rpr.run_tool_worker("backtest_specification", run_id))
    return rpr.load_yaml(arts / "variants" / "index.yaml")["variants"]


def _design(vid: str, patch: list) -> dict:
    return {"variant_id": vid, "patch": patch, "rationale": vid}


def test_5a_refuses_after_the_patch_and_accepts_a_graded_patch(monkeypatch):
    variants = _run_5a(monkeypatch, "run_910", CONFIG, [
        _design("adds_dead_zone", [{"path": COMP0 + "/transforms/1",
                                    "value": {"op": "threshold_filter", "params": {"min_abs": 5}}}]),
        _design("swaps_class", [{"path": COMP0 + "/class", "value": SC + "EMASpreadComponent"}]),
        _design("swaps_to_on_off", [{"path": COMP0 + "/class",
                                     "value": SC + "MacdHistogramCrossoverComponent"}]),
        _design("slower", [{"path": COMP0 + "/params/period", "value": 21}]),
    ])
    assert variants["base"]["status"] == "validated"
    assert variants["slower"]["status"] == "validated"
    for vid, rule in (("adds_dead_zone", "D-051: dead-zone op"), ("swaps_class", "D-053:"),
                      ("swaps_to_on_off", "D-051: on/off class")):
        assert variants[vid]["status"] == "not_tested", vid
        assert variants[vid]["reason"] == rpr.FORECAST_RULE_REASON
        assert rule in variants[vid]["report"], vid
    assert variants["swaps_to_on_off"]["report"].count("D-053:") == 1  # both rules reported
    refusals = _refusals(rpr.ROOT / "runs" / "run_910")
    assert sorted(r["variant_id"] for r in refusals) == ["adds_dead_zone", "swaps_class",
                                                         "swaps_to_on_off"]
    assert {r["stage"] for r in refusals} == {"backtest_specification"}
    # the existing route counts them as config errors (one Step 2 retry, then pause)
    errors = dict(rpr._variant_config_errors(variants))
    assert set(errors) == {"adds_dead_zone", "swaps_class", "swaps_to_on_off"}
    assert all(d.startswith(rpr.FORECAST_RULE_REASON) for d in errors.values())


def test_5a_a_patch_removing_the_banned_piece_passes_the_rule(monkeypatch):
    """(b): checked on the config after the patch. A base with a dead zone is
    refused; a variant whose patch replaces that transform is not refused by
    D-051 (and keeps the classes, so D-053 passes too)."""
    base = _cfg(transforms=[{"op": "identity"}, {"op": "threshold_filter",
                                                "params": {"min_abs": 5}}])
    variants = _run_5a(monkeypatch, "run_911", base, [
        _design("graded", [{"path": COMP0 + "/transforms/1",
                            "value": {"op": "clip", "params": {"min": -20, "max": 20}}}])])
    assert variants["base"]["status"] == "not_tested"
    assert "D-051: dead-zone op" in variants["base"]["report"]
    assert variants["graded"]["status"] == "validated"
    # a base refusal is 1b's fault: the existing route pauses without a Step 2 retry
    assert [vid for vid, _ in rpr._variant_config_errors(variants)] == ["base"]


def test_5a_fails_loud_when_the_catalogue_is_unreadable(monkeypatch, tmp_path):
    monkeypatch.setattr(fr, "CATALOG_PATH", tmp_path / "missing.md")
    monkeypatch.setattr(fr.on_off_classes, "__defaults__", (tmp_path / "missing.md",))
    with pytest.raises(fr.CatalogError):
        _run_5a(monkeypatch, "run_912", CONFIG, [])
