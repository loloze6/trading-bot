"""
E-061 C2 S2e -- "distance to profitable" per card I (D-017; C2_S1_FINDINGS.md G9,
G10 and the C2.3 section).

Covers:
  1. block_registry.registry_summary (G9): empty registry, one block, the neighbour
     cases (same classes with a different timeframe category / kind), this run's
     own type present/absent, this run's own blocks excluded, the no-manifest and
     malformed-manifest cases, correlation statuses from residual_ic.yaml, the
     patch-on-a-registered-idea link, grouping past 50 blocks, determinism, and
     that it writes nothing.
  2. The reader handoff lists artifacts/registry_summary.yaml; the readers stage
     writes it before the first reader; the stage is the ONLY caller (AST scan),
     and with orchestrator.specialist_readers off the stage refuses before writing
     anything (flag-off: no new file, no new prompt input).
  3. The five reader SKILLs carry the card-I anchors (G10), name
     registry_summary.yaml as the one extra allowed input, and say -v2.
  4. reader_proposals accepts the -v2 rubric_version (it is free text).
  5. Round-1 review fixes: empty component-class sets are comparable types,
     this_run.idea_status, registry.n_forecast_blocks, the assumed-timeframe relation,
     the capped neighbour list, a malformed registry raising from the stage, and every
     field / relation name a SKILL cites being written by the code.

No LLM, no network, tmp dirs only (tests/conftest.py's autouse sandbox redirects
rpr.ROOT; the real campaign_record/ and runs/ are never touched).
"""
import ast
import copy
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).parent))

import block_registry as br  # noqa: E402
import reader_proposals  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
from build_reports import REPORT_CATEGORIES  # noqa: E402

from test_e046a_slice5b_i_reader_skills import _VALID_EXAMPLES  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import (  # noqa: E402
    ALL_ON, RUN_ID, _fake_llm, _seed_run, _set_orchestrator)

RSI = "strategies.strategy_components.RSIPullbackComponent"
ER = "strategies.strategy_components.EfficiencyRatioRegimeComponent"
MACD = "strategies.strategy_components.MACDComponent"

BASE_CONFIG = {
    "regime_detector": {"components": [{"id": "er", "class": ER, "params": {"period": 24}}]},
    "strategies": {"warmup": 51, "regimes": {"unknown": {"components": [
        {"id": "rsi", "class": RSI, "params": {"period": 14}}]}}},
}
MANIFEST = {"block": {"kind": "forecast", "config_paths": ["/strategies/regimes/unknown/components/0"]},
            "scaffolding": ["/strategies/warmup", "/regime_detector"], "rationale": "the RSI component"}


def _block(block_id, *, classes=(RSI,), kind="forecast", tf_category=None, run=None,
           residual_ic=None, corr=None, symbols=("BTCUSDT",)) -> dict:
    """A registry block with exactly BLOCK_FIELDS (+ the two timeframe fields together)."""
    b = {"block_id": block_id, "hypothesis_id": block_id.split(":")[0], "kind": kind,
         "config_fragment": {"/strategies/regimes/unknown/components/0":
                             {"id": "c0", "class": classes[0], "params": {}}} if len(classes) == 1
         else {"/strategies/regimes/unknown": {"components": [{"id": f"c{i}", "class": c}
                                                                for i, c in enumerate(classes)]}},
         "regime_assignment": {"regimes": ["unknown"], "detector_paths": []},
         "criteria_passed": ["c"], "variants_passed": ["base"], "numbers": {},
         "symbols_tested": list(symbols),
         "correlation_to_composite": None if corr is None else {"value": corr},
         "residual_ic": None if residual_ic is None else {"value": residual_ic},
         "source_config_ref": "runs/x/cfg.json", "source_config_sha256": "0" * 64,
         "validated_by_run": run or block_id.split(":")[1], "registered_at": "2026-09-01T00:00:00+00:00"}
    if tf_category is not None:
        b["timeframe"], b["timeframe_category"] = {"low": "1h", "daily": "1d"}[tf_category], tf_category
    return b


def _doc(*blocks) -> dict:
    return {"schema_version": 1, "revision": len(blocks), "updated_at": None, "blocks": list(blocks)}


def _run(tmp_path, *, manifest=MANIFEST, config=BASE_CONFIG, variant_loop=True, name="run_010") -> Path:
    run_dir = tmp_path / "runs" / name
    arts = run_dir / "artifacts"
    arts.mkdir(parents=True)
    if manifest is not None:
        (arts / "block_manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    if variant_loop:
        (arts / "variants" / "base").mkdir(parents=True)
        (arts / "variants" / "base" / "strategy_config.json").write_text(json.dumps(config),
                                                                         encoding="utf-8")
        (arts / "variants" / "index.yaml").write_text(yaml.safe_dump({"variants": {
            "base": {"status": "validated", "config_path": "artifacts/variants/base/strategy_config.json"},
            "junk": {"status": "not_tested", "config_path": "artifacts/variants/junk/x.json"}}}),
            encoding="utf-8")
    else:
        (arts / "candidate_strategy_config.json").write_text(json.dumps(config), encoding="utf-8")
    return run_dir


def _residual_ic(run_dir: Path, *, category="low", composite_kind="block", corr=None, skipped=None):
    doc = {"timeframe": "1h", "timeframe_category": category}
    if skipped:
        doc.update({"skipped": skipped, "composite": None, "variants": {}})
    else:
        doc.update({"skipped": None, "composite": {"kind": composite_kind},
                    "variants": {vid: {"correlation_to_composite": c} for vid, c in (corr or {}).items()}})
    (run_dir / "artifacts" / "residual_ic.yaml").write_text(yaml.safe_dump(doc), encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. registry_summary
# ---------------------------------------------------------------------------

def test_empty_registry_has_this_runs_type_and_no_neighbours(tmp_path):
    s = br.registry_summary(_doc(), _run(tmp_path))
    assert s["registry"] == {"n_blocks": 0, "revision": 0, "n_forecast_blocks": 0, "grouping": "none"}
    assert s["blocks"] == []
    this = s["this_run"]
    assert this["idea_status"] is None and this["n_neighbour_blocks"] == 0
    assert this["block_type"] == {"kind": "forecast", "component_classes": [RSI],
                                  "timeframe_category": None}
    assert this["reason"] is None
    assert this["type_already_registered"] is False
    assert this["neighbour_block_ids"] == [] and this["patches_registered_block"] is None
    assert this["correlation_to_composite"]["status"] == "no_residual_ic_artifact"


def test_same_block_type_is_present_and_a_neighbour(tmp_path):
    run_dir = _run(tmp_path)
    _residual_ic(run_dir, category="low", composite_kind="none")
    s = br.registry_summary(
        _doc(_block("H-1:run_001", residual_ic=0.02, corr=0.1, tf_category="low")), run_dir)
    row = s["blocks"][0]
    assert row["relation_to_this_run"] == "same_type"
    assert (row["residual_ic"], row["correlation_to_composite"]) == (0.02, 0.1)
    assert row["component_classes"] == [RSI] and row["symbols_tested"] == ["BTCUSDT"]
    assert s["this_run"]["type_already_registered"] is True
    assert s["this_run"]["neighbour_block_ids"] == ["H-1:run_001"]


def test_same_classes_different_timeframe_category_is_a_neighbour_not_the_same_type(tmp_path):
    run_dir = _run(tmp_path)
    _residual_ic(run_dir, category="low", composite_kind="none")
    s = br.registry_summary(_doc(_block("H-1:run_001", tf_category="daily")), run_dir)
    assert s["this_run"]["block_type"]["timeframe_category"] == "low"
    assert s["blocks"][0]["relation_to_this_run"] == "same_classes_different_timeframe_category"
    assert s["this_run"]["type_already_registered"] is False
    assert s["this_run"]["neighbour_block_ids"] == ["H-1:run_001"]


def test_unrecorded_timeframe_category_never_makes_a_block_look_further_away(tmp_path):
    """A block registered without a timeframe (composition_runs was off) still counts as
    the same type -- the lower distance, never the flattering one -- but under its own
    name, so a reader can tell the assumed match from a verified `same_type`."""
    run_dir = _run(tmp_path)
    _residual_ic(run_dir, category="low", composite_kind="none")
    s = br.registry_summary(_doc(_block("H-1:run_001", tf_category=None)), run_dir)
    assert s["blocks"][0]["relation_to_this_run"] == "same_classes_timeframe_unknown"
    assert s["this_run"]["type_already_registered"] is True
    # unknown on THIS run's side is just as unknown: same name
    s = br.registry_summary(_doc(_block("H-1:run_001", tf_category="low")), _run(tmp_path, name="run_011"))
    assert s["blocks"][0]["relation_to_this_run"] == "same_classes_timeframe_unknown"
    # both recorded and equal: verified
    s = br.registry_summary(_doc(_block("H-1:run_001", tf_category="low")), run_dir)
    assert s["blocks"][0]["relation_to_this_run"] == "same_type"


def test_empty_component_class_sets_are_the_same_set():
    """G9: the type is (kind, sorted classes, timeframe category). Two blocks whose config
    paths hold no component mapping (a regime block on /regime_detector/rules) both have the
    EMPTY class set, and the empty set equals itself -- it must not read as 'no relation'."""
    a = {"kind": "regime", "component_classes": [], "timeframe_category": "low"}
    assert br._relation(a, dict(a)) == "same_type"
    assert br._relation(a, {**a, "kind": "forecast"}) == "same_classes_different_kind"
    assert br._relation(a, {**a, "component_classes": [RSI]}) is None
    assert br._relation({**a, "component_classes": [RSI]}, a) is None


def test_empty_class_regime_block_matches_a_registered_twin_end_to_end(tmp_path):
    """The reviewer's repro: a regime block on /regime_detector/rules against a
    byte-identical registered block."""
    cfg = {"regime_detector": {"components": [{"id": "er", "class": ER, "params": {}}],
                               "rules": [{"regime": "trending", "any_of": [{"er": ">0.5"}]}]},
           "strategies": {"warmup": 5, "regimes": {"unknown": {"components": [
               {"id": "r", "class": RSI}]}}}}
    man = {"block": {"kind": "regime", "config_paths": ["/regime_detector/rules"]},
           "scaffolding": ["/strategies", "/regime_detector/components"], "rationale": "x"}
    twin = _block("H-1:run_001", kind="regime")
    twin["config_fragment"] = {"/regime_detector/rules": cfg["regime_detector"]["rules"]}
    s = br.registry_summary(_doc(twin), _run(tmp_path, manifest=man, config=cfg))
    assert s["this_run"]["block_type"]["component_classes"] == []
    assert s["blocks"][0]["component_classes"] == []
    assert s["blocks"][0]["relation_to_this_run"] == "same_classes_timeframe_unknown"
    assert s["this_run"]["type_already_registered"] is True
    assert s["this_run"]["neighbour_block_ids"] == ["H-1:run_001"]


def test_this_runs_idea_status_and_forecast_block_count_are_in_the_summary(tmp_path):
    """regroup_record registers a validated run's block AFTER the readers, so the summary
    carries the run's own status (the SKILLs score a patch on a validated run as 0), and the
    count of forecast blocks the `no_residual_ic_artifact` rule needs."""
    blocks = [_block("H-1:run_001"), _block("H-2:run_002", classes=(ER,), kind="regime"),
              _block("H-3:run_003", classes=(MACD,))]
    s = br.registry_summary(_doc(*blocks), _run(tmp_path, name="run_020"), idea_status="validated")
    assert s["this_run"]["idea_status"] == "validated"
    assert s["registry"]["n_forecast_blocks"] == 2  # the two forecast kinds, not the regime block
    # the count is over EARLIER runs' blocks (this run's own are left out)
    s = br.registry_summary(_doc(_block("H-1:run_010")), _run(tmp_path, name="run_010"))
    assert s["registry"]["n_forecast_blocks"] == 0


def test_same_classes_different_kind(tmp_path):
    s = br.registry_summary(_doc(_block("H-1:run_001", kind="regime")), _run(tmp_path))
    assert s["blocks"][0]["relation_to_this_run"] == "same_classes_different_kind"
    assert s["this_run"]["type_already_registered"] is False


def test_different_component_classes_are_not_neighbours(tmp_path):
    s = br.registry_summary(_doc(_block("H-1:run_001", classes=(MACD,))), _run(tmp_path))
    assert s["blocks"][0]["relation_to_this_run"] is None
    assert s["this_run"]["neighbour_block_ids"] == [] and s["this_run"]["type_already_registered"] is False
    # the block type is the SET of classes: a superset is not the same classes
    s = br.registry_summary(_doc(_block("H-2:run_002", classes=(RSI, MACD))), _run(tmp_path, name="run_011"))
    assert s["blocks"][0]["component_classes"] == sorted([RSI, MACD])
    assert s["blocks"][0]["relation_to_this_run"] is None


def test_blocks_this_run_already_registered_are_left_out(tmp_path):
    run_dir = _run(tmp_path, name="run_010")
    s = br.registry_summary(_doc(_block("H-1:run_010"), _block("H-2:run_001")), run_dir)
    assert [r["block_id"] for r in s["blocks"]] == ["H-2:run_001"]
    assert s["registry"]["n_blocks"] == 1


def test_no_manifest_leaves_the_type_unknown_with_a_reason(tmp_path):
    s = br.registry_summary(_doc(_block("H-1:run_001")), _run(tmp_path, manifest=None))
    this = s["this_run"]
    assert this["block_type"] is None and this["reason"] == "no_block_manifest"
    assert this["type_already_registered"] is None and this["neighbour_block_ids"] == []
    assert s["blocks"][0]["relation_to_this_run"] is None


def test_unreadable_manifest_is_a_reason_not_a_raise(tmp_path):
    """The summary is advisory: a manifest that does not resolve in the base config (5a and
    block_registry.build_block own that check and still raise on it) leaves the type unknown
    with the reason written into the artifact the readers see."""
    bad = copy.deepcopy(MANIFEST)
    bad["block"]["config_paths"] = ["/strategies/regimes/nope/components/0"]
    this = br.registry_summary(_doc(_block("H-1:run_001")), _run(tmp_path, manifest=bad))["this_run"]
    assert this["block_type"] is None and this["type_already_registered"] is None
    assert this["reason"].startswith("block_type_unreadable:") and "do not resolve" in this["reason"]


def test_malformed_registry_still_raises(tmp_path):
    reg = tmp_path / "block_registry.yaml"
    reg.write_text("schema_version: 1\nrevision: 0\nblocks: nope\n", encoding="utf-8")
    with pytest.raises(br.BlockRegistryError):
        br.load_registry(reg)


def test_single_column_run_reads_candidate_strategy_config(tmp_path):
    s = br.registry_summary(_doc(), _run(tmp_path, variant_loop=False))
    assert s["this_run"]["block_type"]["component_classes"] == [RSI]


def test_run_with_no_validated_variant_has_a_reason_not_an_error(tmp_path):
    run_dir = _run(tmp_path)
    idx = run_dir / "artifacts" / "variants" / "index.yaml"
    idx.write_text(yaml.safe_dump({"variants": {"base": {"status": "not_tested"}}}), encoding="utf-8")
    s = br.registry_summary(_doc(), run_dir)
    assert s["this_run"]["block_type"] is None and s["this_run"]["reason"] == "no_validated_variant"


@pytest.mark.parametrize("kwargs,status,max_abs", [
    (dict(composite_kind="block", corr={"base": 0.25, "design": -0.55}), "measured", 0.55),
    (dict(composite_kind="none", corr={"base": None}), "no_composite", None),
    (dict(composite_kind="block", corr={"base": None}), "not_measurable", None),
    (dict(skipped="regime block"), "skipped: regime block", None),
])
def test_correlation_status_and_max_abs_from_residual_ic(tmp_path, kwargs, status, max_abs):
    run_dir = _run(tmp_path)
    _residual_ic(run_dir, **kwargs)
    c = br.registry_summary(_doc(), run_dir)["this_run"]["correlation_to_composite"]
    assert c["status"] == status and c["max_abs"] == max_abs
    if status == "measured":
        assert c["by_variant"] == {"base": 0.25, "design": -0.55}


def test_patch_on_a_registered_idea_is_named(tmp_path):
    run_dir = _run(tmp_path)
    brief = {"candidate": {"source": {"source_run": "run_001", "parent_hypothesis_id": "H-1",
                                      "proposal": {"kind": "patch"}}}}
    (run_dir / "artifacts" / "research_brief.yaml").write_text(yaml.safe_dump(brief), encoding="utf-8")
    s = br.registry_summary(_doc(_block("H-1:run_001"), _block("H-9:run_009", classes=(MACD,))), run_dir)
    assert s["this_run"]["patches_registered_block"] == "H-1:run_001"
    # a new_block proposal, or a patch on an idea nothing registered, names none
    brief["candidate"]["source"]["proposal"]["kind"] = "new_block"
    (run_dir / "artifacts" / "research_brief.yaml").write_text(yaml.safe_dump(brief), encoding="utf-8")
    assert br.registry_summary(_doc(_block("H-1:run_001")), run_dir)["this_run"][
        "patches_registered_block"] is None
    brief["candidate"]["source"].update(proposal={"kind": "patch"}, source_run="run_777",
                                        parent_hypothesis_id="H-777")
    (run_dir / "artifacts" / "research_brief.yaml").write_text(yaml.safe_dump(brief), encoding="utf-8")
    assert br.registry_summary(_doc(_block("H-1:run_001")), run_dir)["this_run"][
        "patches_registered_block"] is None


def test_past_fifty_blocks_the_summary_groups_by_type(tmp_path):
    blocks = [_block(f"H-{i}:run_{i:03d}", corr=0.1 + 0.001 * i, residual_ic=0.01, tf_category="low")
              for i in range(51)]
    blocks += [_block(f"H-m{i}:run_m{i}", classes=(MACD,), symbols=("ETHUSDT",), tf_category="low")
               for i in range(4)]
    run_900 = _run(tmp_path, name="run_900")
    _residual_ic(run_900, category="low", composite_kind="none")
    s = br.registry_summary(_doc(*blocks), run_900)
    assert s["registry"] == {"n_blocks": 55, "revision": 55, "n_forecast_blocks": 55,
                             "grouping": "by_type"}
    assert "blocks" not in s
    # 51 same-type neighbours: the id list is capped, the count is not
    this = s["this_run"]
    assert this["n_neighbour_blocks"] == 51 and len(this["neighbour_block_ids"]) == 5
    assert this["neighbour_block_ids"] == [f"H-{i}:run_{i:03d}" for i in range(5)]
    assert this["type_already_registered"] is True
    by_class = {tuple(g["block_type"]["component_classes"]): g for g in s["groups"]}
    assert by_class[(RSI,)]["n_blocks"] == 51 and by_class[(MACD,)]["n_blocks"] == 4
    assert len(by_class[(RSI,)]["block_ids"]) == 5
    assert by_class[(RSI,)]["relation_to_this_run"] == "same_type"
    assert by_class[(RSI,)]["abs_correlation_to_composite_range"] == [0.1, pytest.approx(0.15)]
    assert by_class[(MACD,)]["symbols_tested"] == ["ETHUSDT"]
    assert by_class[(MACD,)]["relation_to_this_run"] is None
    # exactly 50 still lists every block
    s50 = br.registry_summary(_doc(*blocks[:50]), _run(tmp_path, name="run_901"))
    assert s50["registry"]["grouping"] == "none"
    assert len(s50["this_run"]["neighbour_block_ids"]) == s50["this_run"]["n_neighbour_blocks"] == 50


def test_summary_is_deterministic_and_writes_nothing(tmp_path):
    run_dir = _run(tmp_path)
    reg = tmp_path / "block_registry.yaml"
    reg.write_text(yaml.safe_dump(_doc(_block("H-1:run_001"))), encoding="utf-8")
    before = sorted(str(p) for p in tmp_path.rglob("*")), reg.read_bytes()
    doc = br.load_registry(reg)
    first, second = br.registry_summary(doc, run_dir), br.registry_summary(doc, run_dir)
    assert first == second
    assert (sorted(str(p) for p in tmp_path.rglob("*")), reg.read_bytes()) == before
    yaml.safe_dump(first)  # plain data


# ---------------------------------------------------------------------------
# 2. Wiring: handoff, stage, only caller, flag off
# ---------------------------------------------------------------------------

def test_every_reader_handoff_lists_the_registry_summary_last():
    for cat in REPORT_CATEGORIES:
        req = [r["path"] for r in rpr._reader_handoff(cat, "run_001", 0)["required_inputs"]]
        assert req == [f"artifacts/reports/{cat}.yaml", "artifacts/grid_evaluation.yaml",
                       "artifacts/hypothesis_card.yaml",
                       "artifacts/candidate_strategy_config.json",
                       "../../docs/COMPONENT_CATALOG.md", "../../docs/STRATEGY_DESIGN_GUIDE.md",
                       "artifacts/registry_summary.yaml"]


def test_stage_writes_the_summary_before_the_first_reader(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    (run_dir / "artifacts" / "registry_summary.yaml").unlink()  # the stub _seed_run leaves
    rpr._block_registry_path().parent.mkdir(parents=True, exist_ok=True)
    rpr._block_registry_path().write_text(yaml.safe_dump(_doc(_block("H-1:run_001"))), encoding="utf-8")
    seen = []

    async def _spy(prompt):
        path = run_dir / "artifacts" / "registry_summary.yaml"
        seen.append(path.exists() and "H-1:run_001" in prompt)
        return await _fake_llm()(prompt)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _spy)
    rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert seen == [True] * len(REPORT_CATEGORIES)
    written = yaml.safe_load((run_dir / "artifacts" / "registry_summary.yaml").read_text(encoding="utf-8"))
    assert written["run_id"] == RUN_ID and written["registry"]["n_blocks"] == 1
    # the run's own grid status (the seeded run is refuted) rides along for the SKILLs' row 0
    assert written["this_run"]["idea_status"] == "refuted"
    # no manifest in this seeded run: the type is unknown, with a reason
    assert written["this_run"]["reason"] == "no_block_manifest"


@pytest.mark.parametrize("bad", ["schema_version: 1\nrevision: 0\nblocks: nope\n",
                                 "schema_version: 1\nrevision: 0\nblocks: [oops]\n",
                                 "not: [valid"])
def test_a_malformed_registry_raises_from_the_stage_before_any_reader(monkeypatch, bad):
    """Not only load_registry: the STAGE stops on a registry it cannot read (a summary is
    never guessed), before the first reader is prompted and before anything is written."""
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    (run_dir / "artifacts" / "registry_summary.yaml").unlink()
    rpr._block_registry_path().parent.mkdir(parents=True, exist_ok=True)
    rpr._block_registry_path().write_text(bad, encoding="utf-8")
    prompts = []

    async def _spy(prompt):
        prompts.append(prompt)
        return await _fake_llm()(prompt)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _spy)
    with pytest.raises(br.BlockRegistryError):
        rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert prompts == []
    assert not (run_dir / "artifacts" / "registry_summary.yaml").exists()


def test_flag_off_the_stage_refuses_before_writing_the_summary(monkeypatch):
    _set_orchestrator({})
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    (run_dir / "artifacts" / "registry_summary.yaml").unlink()
    with pytest.raises(RuntimeError, match="specialist_readers"):
        rpr._run_specialist_readers_stage(RUN_ID, run_dir)
    assert not (run_dir / "artifacts" / "registry_summary.yaml").exists()


def _callers(paths, name):
    """[(file name, enclosing function)] of every call of `name` (bare or attribute)."""
    found = []
    for path in paths:
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
        parents = {}
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                parents[child] = node
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                fn = node.func
                called = fn.id if isinstance(fn, ast.Name) else fn.attr if isinstance(fn, ast.Attribute) else None
                if called == name:
                    p = node
                    while p in parents and not isinstance(p, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        p = parents[p]
                    found.append((Path(path).name, getattr(p, "name", "<module>")))
    return found


def test_the_readers_stage_is_the_only_caller():
    sources = sorted((SR_ROOT / "workflow").glob("*.py")) + sorted((SR_ROOT / "tools").glob("*.py"))
    sources = [p for p in sources if p.name != "block_registry.py"] + [SR_ROOT / "tools" / "block_registry.py"]
    assert _callers(sources, "registry_summary") == [("run_phase1_research.py", "_write_registry_summary")]
    assert _callers(sources, "_write_registry_summary") == [
        ("run_phase1_research.py", "_run_specialist_readers_stage")]
    # nothing else names the artifact as a path either
    for p in sources:
        text = p.read_text(encoding="utf-8")
        if p.name not in ("block_registry.py", "run_phase1_research.py"):
            assert "registry_summary.yaml" not in text, p.name


# ---------------------------------------------------------------------------
# 3. The SKILLs
# ---------------------------------------------------------------------------

_SKILLS = SR_ROOT / "workflow_artifacts" / "skills" / "readers"


@pytest.mark.parametrize("cat", REPORT_CATEGORIES)
def test_reader_skill_carries_the_card_i_anchors_and_the_extra_input(cat):
    text = (_SKILLS / f"{cat}-reader" / "SKILL.md").read_text(encoding="utf-8")
    assert f'{cat}-reader-v2' in text and f"{cat}-reader-v1" not in text
    assert "artifacts/registry_summary.yaml" in text
    context_rule = text.split("## Context rule")[1]
    assert "registry_summary.yaml" in context_rule
    scope = text.split("**Scope boundary.**")[1].split("\n## ")[0]
    assert "block_registry.yaml" in scope  # the registry itself stays out of scope
    rows = {int(l.split("|")[1]): l.split(" | ")[2] for l in text.split("## Scoring")[1].splitlines()
            if l.startswith(("| 0 |", "| 1 |", "| 2 |", "| 3 |"))}
    assert set(rows) == {0, 1, 2, 3}
    assert "patches_registered_block" in rows[0] and "same block type as a registered" in rows[0]
    assert "0.6" in rows[1] and "different timeframe category or kind" in rows[1]
    assert "0.3-0.6" in rows[2] and "new_block" in rows[2]
    assert "0.3" in rows[3] and "not in the registry" in rows[3]
    assert "rank-only placeholders" in text
    # the other two score columns keep their own anchors (only distance changed)
    assert "`confidence_real`" in text and "`mechanism_plausibility`" in text


def test_the_five_skills_carry_the_same_distance_rows():
    """Card I is category-independent: the distance column is identical across readers."""
    cols = []
    for cat in REPORT_CATEGORIES:
        text = (_SKILLS / f"{cat}-reader" / "SKILL.md").read_text(encoding="utf-8")
        cols.append([l.split(" | ")[2] for l in text.split("## Scoring")[1].splitlines()
                     if l.startswith(("| Score ", "| 0 |", "| 1 |", "| 2 |", "| 3 |"))])
    assert all(c == cols[0] for c in cols) and len(cols[0]) == 5


def _distance_section(cat: str) -> str:
    text = (_SKILLS / f"{cat}-reader" / "SKILL.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    return text.split("### Distance to profitable")[1].split("\n## ")[0]


def test_the_five_skills_carry_a_byte_identical_distance_section():
    sections = [_distance_section(cat) for cat in REPORT_CATEGORIES]
    assert all(s == sections[0] for s in sections) and len(sections[0]) > 500


def test_skills_state_the_round_1_rules():
    """Row 0 and the precedence rule, patch-only scope, idea_status, n_forecast_blocks."""
    for cat in REPORT_CATEGORIES:
        text = (_SKILLS / f"{cat}-reader" / "SKILL.md").read_text(encoding="utf-8").replace("\r\n", "\n")
        row0 = [l for l in text.split("## Scoring")[1].splitlines() if l.startswith("| 0 |")][0]
        assert "never a `new_block` sketch" in row0
        assert "this_run.idea_status" in row0 and "`validated`" in row0
        row2 = [l for l in text.split("## Scoring")[1].splitlines() if l.startswith("| 2 |")][0]
        row3 = [l for l in text.split("## Scoring")[1].splitlines() if l.startswith("| 3 |")][0]
        assert "`no_residual_ic_artifact` while `registry.n_forecast_blocks` > 0" in row2
        assert "`no_residual_ic_artifact` with `registry.n_forecast_blocks` = 0" in row3
        assert "`no_residual_ic_artifact`" not in row3.replace(
            "`no_residual_ic_artifact` with `registry.n_forecast_blocks` = 0", "")
        section = _distance_section(cat)
        assert "Precedence (a lower score always wins" in section
        assert "Take the LOWEST row" not in section  # replaced by the explicit precedence rule
        assert "never scores 3" in section
        assert "apply to a `patch`" in section and "never to a `new_block` sketch" in section


def _skill_cited_fields(section: str):
    """(this_run.<field> / registry.<field> paths, relation names) a distance section cites."""
    import re
    paths = set(re.findall(r"`((?:this_run|registry)\.[a-z_]+(?:\.[a-z_]+)*)`", section))
    relations = set(re.findall(r"`(same_[a-z_]+)`", section))
    return paths, relations


def test_every_field_and_relation_a_skill_cites_is_written_by_the_code(tmp_path):
    run_dir = _run(tmp_path)
    _residual_ic(run_dir, category="low", composite_kind="block", corr={"base": 0.2})
    s = br.registry_summary(_doc(_block("H-1:run_001", tf_category="low")), run_dir, idea_status="validated")
    written = {"this_run": s["this_run"], "registry": s["registry"]}
    for cat in REPORT_CATEGORIES:
        paths, relations = _skill_cited_fields(_distance_section(cat))
        assert "this_run.idea_status" in paths and "registry.n_forecast_blocks" in paths
        for path in paths:
            node = written
            for part in path.split("."):
                assert isinstance(node, dict) and part in node, (cat, path)
                node = node[part]
        # relation names: exactly the ones the code can emit
        assert relations == set(br.RELATIONS), (cat, relations ^ set(br.RELATIONS))
    # a `blocks[*].relation_to_this_run` row field the SKILLs also cite
    assert "relation_to_this_run" in s["blocks"][0]
    # and the statuses the SKILLs branch on are the statuses the code writes
    text = _distance_section(REPORT_CATEGORIES[0])
    for status in ("measured", "no_composite", "no_residual_ic_artifact", "not_measurable"):
        assert f"`{status}`" in text


@pytest.mark.parametrize("this,other,expected", [
    (("forecast", "low"), ("forecast", "low"), "same_type"),
    (("forecast", "low"), ("forecast", None), "same_classes_timeframe_unknown"),
    (("forecast", "low"), ("forecast", "daily"), "same_classes_different_timeframe_category"),
    (("forecast", "low"), ("regime", None), "same_classes_different_kind"),
    (("forecast", "low"), ("regime", "daily"), "same_classes_different_kind_and_timeframe_category"),
])
def test_every_relation_name_is_reachable(this, other, expected):
    a = {"kind": this[0], "component_classes": [RSI], "timeframe_category": this[1]}
    b = {"kind": other[0], "component_classes": [RSI], "timeframe_category": other[1]}
    assert br._relation(a, b) == expected
    assert expected in br.RELATIONS


# ---------------------------------------------------------------------------
# 4. reader_proposals accepts -v2
# ---------------------------------------------------------------------------

def test_reader_proposals_accepts_v2_rubric_versions(tmp_path):
    out = tmp_path / "proposals"
    out.mkdir()
    for cat, ex in _VALID_EXAMPLES.items():
        p = copy.deepcopy(ex)
        p["proposal_id"] = f"{cat}-run_test-1"
        p["rubric_version"] = f"{cat}-reader-v2"
        (out / f"{cat}.yaml").write_text(yaml.safe_dump([p]), encoding="utf-8")
    loaded = reader_proposals.load_proposals(out, list(REPORT_CATEGORIES))
    assert {c: v[0]["rubric_version"] for c, v in loaded.items()} == {
        c: f"{c}-reader-v2" for c in REPORT_CATEGORIES}
