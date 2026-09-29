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
    assert s["registry"] == {"n_blocks": 0, "revision": 0, "grouping": "none"}
    assert s["blocks"] == []
    this = s["this_run"]
    assert this["block_type"] == {"kind": "forecast", "component_classes": [RSI],
                                  "timeframe_category": None}
    assert this["reason"] is None
    assert this["type_already_registered"] is False
    assert this["neighbour_block_ids"] == [] and this["patches_registered_block"] is None
    assert this["correlation_to_composite"]["status"] == "no_residual_ic_artifact"


def test_same_block_type_is_present_and_a_neighbour(tmp_path):
    s = br.registry_summary(_doc(_block("H-1:run_001", residual_ic=0.02, corr=0.1)), _run(tmp_path))
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
    """A block registered without a timeframe (composition_runs was off) matches this
    run's category: the lower distance, never the flattering one."""
    run_dir = _run(tmp_path)
    _residual_ic(run_dir, category="low", composite_kind="none")
    s = br.registry_summary(_doc(_block("H-1:run_001", tf_category=None)), run_dir)
    assert s["blocks"][0]["relation_to_this_run"] == "same_type"


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


def test_manifest_that_does_not_resolve_raises(tmp_path):
    bad = copy.deepcopy(MANIFEST)
    bad["block"]["config_paths"] = ["/strategies/regimes/nope/components/0"]
    with pytest.raises(br.BlockRegistryError, match="do not resolve"):
        br.registry_summary(_doc(), _run(tmp_path, manifest=bad))


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
    blocks = [_block(f"H-{i}:run_{i:03d}", corr=0.1 + 0.001 * i, residual_ic=0.01) for i in range(51)]
    blocks += [_block(f"H-m{i}:run_m{i}", classes=(MACD,), symbols=("ETHUSDT",)) for i in range(4)]
    s = br.registry_summary(_doc(*blocks), _run(tmp_path, name="run_900"))
    assert s["registry"] == {"n_blocks": 55, "revision": 55, "grouping": "by_type"}
    assert "blocks" not in s
    by_class = {tuple(g["block_type"]["component_classes"]): g for g in s["groups"]}
    assert by_class[(RSI,)]["n_blocks"] == 51 and by_class[(MACD,)]["n_blocks"] == 4
    assert len(by_class[(RSI,)]["block_ids"]) == 5
    assert by_class[(RSI,)]["relation_to_this_run"] == "same_type"
    assert by_class[(RSI,)]["abs_correlation_to_composite_range"] == [0.1, pytest.approx(0.15)]
    assert by_class[(MACD,)]["symbols_tested"] == ["ETHUSDT"]
    assert by_class[(MACD,)]["relation_to_this_run"] is None
    # exactly 50 still lists every block
    assert br.registry_summary(_doc(*blocks[:50]), _run(tmp_path, name="run_901"))["registry"][
        "grouping"] == "none"


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
    # no manifest in this seeded run: the type is unknown, with a reason
    assert written["this_run"]["reason"] == "no_block_manifest"


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
