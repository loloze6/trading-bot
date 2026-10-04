"""
E-056 1b block manifest: stage 1b (strategy_config_authoring) writes
artifacts/block_manifest.yaml; STRATEGY_DESIGN_GUIDE.md's 'Manifest contract' is built.

Covers:
  1. the schema file and tools/block_manifest.py agree (kind enum, keys, and
     accept/reject on shared fixtures); block_registry.schema.json's kind enum
     is the same;
  2. path validation: good, missing and bad pointer; block and scaffolding;
  3. the kind enum and the kind -> config-root rule; overlap rules;
  4. one source of truth: every fixture is accepted/rejected identically by
     the orchestrator's 5a tool stage and by tools/block_registry.py;
  5. skill/handoff text: the manifest instructions live only in the
     config-direct-authoring (flag-on) stage's files;
  6. flag-off byte-identity: no flag-off stage prompt depends on any file this
     ticket changed;
  7. end to end on fixtures: 1b output with manifest -> 5a -> validated grid ->
     regroup_record registers the block.

No LLM, no backtest. tests/conftest.py sandboxes rpr.ROOT.
"""
import asyncio
import hashlib
import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import block_manifest as bm  # noqa: E402
import block_registry as br  # noqa: E402

from test_k3_protocol_pinning import _minimal_run  # noqa: E402
from test_e058_s2a_regroup_record import RUN_ID, ALL_ON, _seed, _memory  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402

SCHEMAS = SR_ROOT / "workflow_artifacts" / "schemas"
SKILL_1B = SR_ROOT / "workflow_artifacts" / "skills" / "strategy-config-authoring" / "SKILL.md"
HANDOFF_1B = SR_ROOT / "workflow_artifacts" / "templates" / "handoffs" / \
    "hypothesis_to_strategy_config_authoring.yaml"
DESIGN_GUIDE = SR_ROOT / "docs" / "STRATEGY_DESIGN_GUIDE.md"

# Ungated base config (STRATEGY_DESIGN_GUIDE.md 'Ungated' pattern) with one real component.
CONFIG = {
    "regime_detector": {"mode": "threshold_rules", "components": [], "rules": [],
                        "default_regime": "unknown"},
    "strategies": {
        "warmup": 51,
        "regimes": {
            "unknown": {"components": [
                {"id": "rsi", "class": "strategies.strategy_components.RSIPullbackComponent",
                 "params": {"period": 14}, "weight": 1.0, "transforms": [{"op": "identity"}]},
            ]},
            "trending": None, "mean_reversion": None, "chop": None,
        },
    },
}
GOOD = {
    "block": {"kind": "forecast", "config_paths": ["/strategies/regimes/unknown/components/0"]},
    "scaffolding": ["/strategies/warmup", "/regime_detector"],
    "rationale": "the RSI pullback component is the idea",
}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _with(**kw) -> dict:
    doc = json.loads(json.dumps(GOOD))
    for k, v in kw.items():
        if k in ("kind", "config_paths"):
            doc["block"][k] = v
        else:
            doc[k] = v
    return doc


def _drop(key: str) -> dict:
    doc = json.loads(json.dumps(GOOD))
    doc.pop(key)
    return doc


# (id, manifest, match) -- rejected by the SHAPE rules the schema also encodes.
SHAPE_BAD = [
    ("not_mapping", ["a"], "expected"),
    ("no_block", _drop("block"), "expected"),
    ("no_scaffolding", _drop("scaffolding"), "missing"),
    ("no_rationale", _drop("rationale"), "missing"),
    ("extra_top_key", _with(symbols=["BTCUSDT"]), "unknown"),
    ("extra_block_key", {**GOOD, "block": {**GOOD["block"], "hypothesis_id": "H-1"}}, "unknown"),
    ("kind_detector", _with(kind="detector"), "block.kind"),
    ("kind_none", _with(kind=None), "block.kind"),
    ("paths_empty", _with(config_paths=[]), "config_paths"),
    ("paths_not_list", _with(config_paths="/strategies"), "config_paths"),
    ("paths_bad_pointer", _with(config_paths=["strategies/regimes/unknown"]), "config_paths"),
    ("paths_duplicate", _with(config_paths=["/strategies/regimes/unknown"] * 2), "config_paths"),
    ("scaffolding_bad_pointer", _with(scaffolding=["warmup"]), "scaffolding"),
    ("scaffolding_not_list", _with(scaffolding="/strategies/warmup"), "scaffolding"),
    ("rationale_empty", _with(rationale="  "), "rationale"),
    ("rationale_not_str", _with(rationale=["x"]), "rationale"),
]
# Rejected only by code (JSON Schema cannot express these): the schema accepts them.
CODE_ONLY_BAD = [
    ("block_overlaps_block", _with(config_paths=["/strategies/regimes/unknown",
                                                 "/strategies/regimes/unknown/components/0"]),
     "overlap"),
    ("block_inside_scaffolding", _with(scaffolding=["/strategies"]), "overlap"),
    ("scaffolding_inside_block", _with(scaffolding=["/strategies/regimes/unknown/components/0/params"]),
     "overlap"),
    ("forecast_without_regimes_path", _with(config_paths=["/strategies/warmup"], scaffolding=[]),
     "at least one"),
    ("regime_without_detector_path", _with(kind="regime"), "at least one"),
    # code-review fix 3: the bare regimes map names no regime (registry regimes=[])
    ("forecast_bare_regimes_map", _with(config_paths=["/strategies/regimes"],
                                        scaffolding=["/strategies/warmup"]), "at least one"),
    # code-review fix 10: scaffolding vs scaffolding
    ("scaffolding_overlaps_scaffolding", _with(scaffolding=["/regime_detector",
                                                            "/regime_detector/rules"]), "overlap"),
]
# Shape-valid, but a pointer does not resolve in CONFIG.
UNRESOLVED = [
    ("block_missing", _with(config_paths=["/strategies/regimes/unknown/components/3"]), "not resolve"),
    ("scaffolding_missing", _with(scaffolding=["/strategies/nope"]), "not resolve"),
]
VALID = [
    ("forecast", GOOD),
    ("forecast_empty_scaffolding", _with(scaffolding=[])),
    ("regime", _with(kind="regime", config_paths=["/regime_detector"], scaffolding=["/strategies"])),
    ("regime_rule_path", _with(kind="regime", config_paths=["/regime_detector/default_regime"],
                               scaffolding=["/strategies/warmup"])),
    ("null_regime_entry", _with(config_paths=["/strategies/regimes/unknown",
                                              "/strategies/regimes/chop"], scaffolding=[])),
]


def _schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def _schema_ok(doc) -> bool:
    import jsonschema
    schema = _schema("block_manifest.schema.json")
    cls = jsonschema.validators.validator_for(schema)
    cls.check_schema(schema)
    return cls(schema).is_valid(doc)


# ---------------------------------------------------------------------------
# 1. Schema <-> code agreement
# ---------------------------------------------------------------------------

def test_schema_constants_match_code():
    schema = _schema("block_manifest.schema.json")
    assert tuple(schema["required"]) == bm.MANIFEST_KEYS
    assert set(schema["properties"]) == set(bm.MANIFEST_KEYS)
    assert schema["additionalProperties"] is False
    block = schema["properties"]["block"]
    assert tuple(block["required"]) == bm.BLOCK_KEYS and block["additionalProperties"] is False
    assert tuple(block["properties"]["kind"]["enum"]) == bm.MANIFEST_KINDS == ("forecast", "regime")
    registry_kind = _schema("block_registry.schema.json")["$defs"]["block"]["properties"]["kind"]["enum"]
    assert tuple(registry_kind) == bm.MANIFEST_KINDS
    assert br.MANIFEST_KINDS is bm.MANIFEST_KINDS and br.MANIFEST_FILENAME == bm.MANIFEST_FILENAME
    assert set(bm.KIND_ASSIGNMENT_KEY) == set(bm.MANIFEST_KINDS)


@pytest.mark.parametrize("name,doc", VALID + [(n, d) for n, d, _ in UNRESOLVED],
                         ids=[n for n, _ in VALID] + [n for n, _, _ in UNRESOLVED])
def test_schema_and_code_accept_the_same_shapes(name, doc):
    assert _schema_ok(doc)
    assert bm.validate_manifest(doc) is doc


@pytest.mark.parametrize("name,doc,match", SHAPE_BAD, ids=[c[0] for c in SHAPE_BAD])
def test_schema_and_code_reject_the_same_shapes(name, doc, match):
    assert not _schema_ok(doc)
    with pytest.raises(bm.BlockManifestError, match=match):
        bm.validate_manifest(doc)


@pytest.mark.parametrize("name,doc,match", CODE_ONLY_BAD, ids=[c[0] for c in CODE_ONLY_BAD])
def test_code_only_rules_are_documented_as_code_only(name, doc, match):
    """The schema's $comment names these rules as code-only; the schema accepts,
    the code rejects."""
    assert _schema_ok(doc)
    with pytest.raises(bm.BlockManifestError, match=match):
        bm.validate_manifest(doc)


# ---------------------------------------------------------------------------
# 2/3. Path validation, kind enum
# ---------------------------------------------------------------------------

def test_good_manifest_resolves():
    assert bm.check_manifest(GOOD, CONFIG) is GOOD
    assert bm.unresolved_paths(CONFIG, GOOD) == []


@pytest.mark.parametrize("name,doc,match", UNRESOLVED, ids=[c[0] for c in UNRESOLVED])
def test_missing_pointer_fails(name, doc, match):
    with pytest.raises(bm.BlockManifestError, match=match):
        bm.check_manifest(doc, CONFIG)


@pytest.mark.parametrize("pointer", ["strategies", "", 3, None])
def test_bad_pointer_fails(pointer):
    with pytest.raises(bm.BlockManifestError, match="config_paths"):
        bm.check_manifest(_with(config_paths=[pointer]), CONFIG)


@pytest.mark.parametrize("kind", ["forecast", "regime"])
def test_kind_enum_accepts_both_kinds(kind):
    paths = {"forecast": ["/strategies/regimes/unknown/components/0"],
             "regime": ["/regime_detector/rules"]}[kind]
    bm.check_manifest(_with(kind=kind, config_paths=paths, scaffolding=[]), CONFIG)


@pytest.mark.parametrize("kind", ["Forecast", "detector", "composite", "", 1, ["forecast"]])
def test_kind_enum_rejects_anything_else(kind):
    with pytest.raises(bm.BlockManifestError, match="block.kind"):
        bm.validate_manifest(_with(kind=kind))


def test_error_class_is_the_callers():
    with pytest.raises(RuntimeError):
        bm.validate_manifest(_with(kind="x"), error_cls=RuntimeError)
    with pytest.raises(br.BlockRegistryError):
        bm.validate_manifest(_with(kind="x"), error_cls=br.BlockRegistryError)


def test_load_manifest_file_is_strict(tmp_path):
    p = tmp_path / "block_manifest.yaml"
    assert bm.load_manifest_file(p) is None
    p.write_text("block: [unclosed\n", encoding="utf-8")
    with pytest.raises(bm.BlockManifestError, match="unparseable"):
        bm.load_manifest_file(p)
    p.write_text(yaml.safe_dump(GOOD), encoding="utf-8")
    assert bm.load_manifest_file(p) == GOOD


@pytest.mark.parametrize("path", [SKILL_1B, DESIGN_GUIDE], ids=["skill_1b", "design_guide"])
def test_documented_examples_are_valid(path):
    """The example manifest in the 1b skill and in the guide's 'Manifest contract' passes the real check
    against the ungated base config."""
    text = path.read_text(encoding="utf-8")
    start = text.index("```yaml\nblock:")
    doc = yaml.safe_load(text[start + len("```yaml\n"):text.index("```", start + 7)])
    bm.check_manifest(doc, CONFIG)


# ---------------------------------------------------------------------------
# 4. One source of truth: the 5a tool stage and the registry agree
# ---------------------------------------------------------------------------

def _ok_subprocess(*a, **k):
    class _Ok:
        returncode, stdout, stderr = 0, "", ""
    return _Ok()


def _stage_5a_accepts(monkeypatch, run_id: str, manifest) -> bool:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": CONFIG,
                                                "config_rationale": ["x"], "component_gap": None})
    rpr.save_yaml(arts / "variant_patches.yaml", {"variants": [
        {"variant_id": "base", "patch": [], "rationale": "base"}]})
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    monkeypatch.setattr(rpr.subprocess, "run", _ok_subprocess)
    try:
        asyncio.run(rpr.run_tool_worker("backtest_specification", run_id))
    except RuntimeError:
        assert not (arts / "variants" / "index.yaml").exists()  # stopped before any variant
        return False
    assert rpr.load_yaml(arts / "variants" / "index.yaml")["variants"]["base"]["status"] == "validated"
    return True


def _registry_accepts(run_id: str, manifest) -> bool:
    run_dir = _minimal_run(rpr.ROOT, run_id + "r")
    arts = run_dir / "artifacts"
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    cfg = arts / "candidate_strategy_config.json"
    cfg.write_text(json.dumps(CONFIG), encoding="utf-8")
    sha = hashlib.sha256(json.dumps(CONFIG, sort_keys=True).encode("utf-8")).hexdigest()
    entry = {"run_id": run_id, "hypothesis_id": "H-1",
             "variants": {"base": {"status": "tested", "config_ref": str(cfg.relative_to(rpr.ROOT)),
                                   "forecast_hash": sha, "symbols": ["BTCUSDT"]}},
             "grid": {"criteria": ["c"], "variants": ["base"],
                      "cells": {"c": {"base": {"result": "PASS", "value": 1.0, "threshold": 0.0}}}}}
    try:
        loaded = br.load_manifest(run_dir)
        block = br.build_block(run_dir, entry, loaded, root=rpr.ROOT)
    except br.BlockRegistryError:
        return False
    assert block["config_fragment"] == {
        p: rpr._json_pointer_module().resolve_json_pointer(CONFIG, p)
        for p in manifest["block"]["config_paths"]}
    # the kind rule and the stored regime_assignment agree (code-review fix 3)
    assert block["regime_assignment"][bm.KIND_ASSIGNMENT_KEY[manifest["block"]["kind"]]]
    return True


_ALL = ([(n, d, True) for n, d in VALID]
        + [(n, d, False) for n, d, _ in SHAPE_BAD + CODE_ONLY_BAD + UNRESOLVED])


@pytest.mark.parametrize("name,doc,expected", _ALL, ids=[c[0] for c in _ALL])
def test_5a_and_registry_agree(monkeypatch, name, doc, expected):
    run_id = f"run_7{_ALL.index((name, doc, expected)):02d}"
    assert _stage_5a_accepts(monkeypatch, run_id, doc) is expected
    assert _registry_accepts(run_id, doc) is expected


def test_5a_still_tests_a_variant_that_changes_scaffolding(monkeypatch):
    """Code-review fix 6: per variant only BLOCK paths must resolve; a variant
    may change (even drop) scaffolding and is still tested."""
    run_dir = _minimal_run(rpr.ROOT, "run_790")
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": CONFIG,
                                                "config_rationale": ["x"], "component_gap": None})
    rpr.save_yaml(arts / "variant_patches.yaml", {"variants": [
        {"variant_id": "base", "patch": [], "rationale": "base"},
        {"variant_id": "design", "patch": [{"path": "/strategies", "value": {
            "regimes": CONFIG["strategies"]["regimes"]}}], "rationale": "drops warmup"}]})
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(GOOD), encoding="utf-8")
    monkeypatch.setattr(rpr.subprocess, "run", _ok_subprocess)
    asyncio.run(rpr.run_tool_worker("backtest_specification", "run_790"))
    variants = rpr.load_yaml(arts / "variants" / "index.yaml")["variants"]
    assert variants["base"]["status"] == "validated"
    assert variants["design"]["status"] == "validated"


def test_per_variant_check_is_block_only():
    no_scaffold = {"strategies": {"regimes": CONFIG["strategies"]["regimes"]}}
    assert rpr._check_manifest_paths(no_scaffold, GOOD) == []
    assert bm.unresolved_paths(no_scaffold, GOOD) == ["/strategies/warmup", "/regime_detector"]


# ---------------------------------------------------------------------------
# Code-review fix 1: the manifest is checked right after 1b, one retry
# ---------------------------------------------------------------------------

def _authored_1b(run_id: str, manifest) -> Path:
    run_dir = _minimal_run(rpr.ROOT, run_id)
    arts = run_dir / "artifacts"
    rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": CONFIG,
                                                "config_rationale": ["x"], "component_gap": None})
    rpr.save_yaml(arts / "decision.yaml", {"stage": "strategy_config_authoring",
                                           "status": "spec_ready", "rationale": "x",
                                           "blocking_issues": []})
    if manifest is not None:
        (arts / "block_manifest.yaml").write_text(yaml.safe_dump(manifest), encoding="utf-8")
    return run_dir


def test_post_1b_route_valid_manifest_goes_to_innovation_expansion():
    run_dir = _authored_1b("run_760", GOOD)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"


@pytest.mark.parametrize("manifest,match", [
    (None, "is missing"),
    (_with(kind="detector"), "block.kind"),
    (_with(config_paths=["/strategies/regimes/unknown/components/3"]), "not resolve"),
], ids=["missing", "malformed", "unresolved"])
def test_post_1b_route_retries_once_then_fails_loud(monkeypatch, manifest, match):
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _authored_1b("run_761", manifest)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    retry = rpr.load_yaml(run_dir / "pipeline_state.yaml")["block_manifest_retry"]
    assert retry["attempts"] == 1 and match in retry["last_error"]
    # the retry's handoff carries the error
    handoff = {"required_inputs": []}
    rpr._apply_block_manifest_retry_context("strategy_config_authoring", handoff, run_dir)
    assert match in handoff["injected_context"]["block_manifest_error"]
    other = {"required_inputs": []}
    rpr._apply_block_manifest_retry_context("innovation_expansion", other, run_dir)
    assert other == {"required_inputs": []}
    # second bad manifest: fail loud, no third pass
    with pytest.raises(RuntimeError, match="still invalid"):
        rpr.determine_post_strategy_config_authoring_route(run_dir)


def test_post_1b_route_retry_then_valid_resets_the_counter():
    run_dir = _authored_1b("run_762", None)
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "strategy_config_authoring"
    (run_dir / "artifacts" / "block_manifest.yaml").write_text(yaml.safe_dump(GOOD), encoding="utf-8")
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    assert rpr.load_yaml(run_dir / "pipeline_state.yaml")["block_manifest_retry"]["attempts"] == 0


def test_retry_context_is_a_no_op_with_the_flag_off():
    _set_orchestrator(None)
    run_dir = _authored_1b("run_763", None)
    rpr.update_state(path=run_dir, block_manifest_retry={"attempts": 1, "last_error": "boom"})
    handoff = {"required_inputs": []}
    rpr._apply_block_manifest_retry_context("strategy_config_authoring", handoff, run_dir)
    assert handoff == {"required_inputs": []}


def test_route_loop_back_to_1b_is_driven_by_run_loop(monkeypatch):
    """run_loop really re-enters strategy_config_authoring with the error in its
    handoff, then stops loud on a second bad manifest -- innovation_expansion is
    never invoked."""
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _authored_1b("run_764", None)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = "strategy_config_authoring"
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    tpl = SR_ROOT / "workflow_artifacts" / "templates" / "handoffs" / HANDOFF_1B.name
    (run_dir / "handoffs").mkdir(exist_ok=True)
    shutil.copy(tpl, run_dir / "handoffs" / HANDOFF_1B.name)
    (run_dir / "artifacts" / "hypothesis_card.yaml").write_text("hypothesis_id: H-1\n", encoding="utf-8")
    docs = rpr.ROOT / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "COMPONENT_CATALOG.md").write_text("catalogue\n", encoding="utf-8")
    (docs / "STRATEGY_DESIGN_GUIDE.md").write_text("guide\n", encoding="utf-8")
    seen = []

    async def _fake_invoke(stage_name, run_id, retry_context=None):
        handoff = rpr.load_yaml(run_dir / "handoffs" / HANDOFF_1B.name)
        rpr._clear_stale_block_manifest(stage_name, run_dir)
        rpr._apply_block_manifest_retry_context(stage_name, handoff, run_dir)
        seen.append((stage_name, (handoff.get("injected_context") or {}).get("block_manifest_error")))

    monkeypatch.setattr(rpr, "async_invoke_agent", _fake_invoke)
    rpr.run_loop("run_764")
    assert [s for s, _ in seen] == ["strategy_config_authoring", "strategy_config_authoring"]
    assert seen[0][1] is None and "is missing" in seen[1][1]
    final = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert final["status"] == "failed" and "still invalid" in final["last_error"]


# ---------------------------------------------------------------------------
# Code-review fix 2: a stale manifest is removed when 1b starts
# ---------------------------------------------------------------------------

def _invoke_1b_capturing(monkeypatch, run_dir: Path, run_id: str) -> list:
    (run_dir / "handoffs").mkdir(exist_ok=True)
    shutil.copy(HANDOFF_1B, run_dir / "handoffs" / HANDOFF_1B.name)
    seen = []

    async def _fake_worker(stage_name, handoff, path, retry_context=None):
        seen.append((path / "artifacts" / "block_manifest.yaml").exists())

    monkeypatch.setattr(rpr, "run_claude_worker", _fake_worker)
    asyncio.run(rpr.async_invoke_agent("strategy_config_authoring", run_id))
    return seen


def test_stale_manifest_is_deleted_when_1b_starts(monkeypatch):
    _set_orchestrator({"config_direct_authoring": {"enabled": True}})
    run_dir = _authored_1b("run_770", GOOD)
    assert _invoke_1b_capturing(monkeypatch, run_dir, "run_770") == [False]
    assert not (run_dir / "artifacts" / "block_manifest.yaml").exists()


def test_stale_manifest_untouched_with_the_flag_off(monkeypatch):
    _set_orchestrator(None)
    run_dir = _authored_1b("run_771", GOOD)
    assert _invoke_1b_capturing(monkeypatch, run_dir, "run_771") == [True]
    rpr._clear_stale_block_manifest("innovation_expansion", run_dir)
    assert (run_dir / "artifacts" / "block_manifest.yaml").exists()


# ---------------------------------------------------------------------------
# Code-review fixes 4, 7, 8, 9: docs, card schema, config text, one registry check
# ---------------------------------------------------------------------------

def test_reader_skills_and_proposal_schema_no_longer_call_7c_unbuilt():
    readers = SR_ROOT / "workflow_artifacts" / "skills" / "readers"
    stale = ("PROPOSED, NOT BUILT", "PROPOSED-NOT-BUILT", "Nothing reads block_manifest",
             "nothing reads block_manifest")
    for skill in readers.glob("*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        assert not any(s in text for s in stale), skill
    schema = (SCHEMAS / "proposal.schema.json").read_text(encoding="utf-8")
    assert not any(s in schema for s in stale)
    assert "the manifest contract is built" in schema


def _card_errors(card: dict) -> list:
    import jsonschema
    import workflow_artifact_validation as wav
    schema = _schema("hypothesis_card.schema.json")
    return [list(e.absolute_path) for e in wav._make_validator(jsonschema, schema).iter_errors(card)]


def test_card_manifest_refs_the_manifest_schema():
    assert _schema("hypothesis_card.schema.json")["properties"]["manifest"]["$ref"] == \
        "block_manifest.schema.json"
    bad = [e for e in _card_errors({"manifest": _with(kind="detector")}) if e[:1] == ["manifest"]]
    assert bad
    assert not [e for e in _card_errors({"manifest": GOOD}) if e[:1] == ["manifest"]]


def test_campaign_config_describes_the_manifest():
    text = (SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8")
    block = text[text.index("  config_direct_authoring:"):text.index("  variant_loop:")]
    assert "block_manifest.yaml" in block and "fails the run loud" in block


def test_registry_resolves_manifest_paths_once():
    assert not hasattr(br, "_resolve_pointer") and not hasattr(br, "_regime_assignment")
    assert _registry_accepts("run_780", GOOD)
    with pytest.raises(br.BlockRegistryError, match="do not resolve in the base config") as exc:
        run_dir = _minimal_run(rpr.ROOT, "run_781r")
        cfg = run_dir / "artifacts" / "candidate_strategy_config.json"
        cfg.write_text(json.dumps(CONFIG), encoding="utf-8")
        sha = hashlib.sha256(json.dumps(CONFIG, sort_keys=True).encode("utf-8")).hexdigest()
        entry = {"run_id": "run_781", "hypothesis_id": "H-1",
                 "variants": {"base": {"status": "tested", "config_ref": str(cfg.relative_to(rpr.ROOT)),
                                       "forecast_hash": sha}},
                 "grid": {"criteria": ["c"], "variants": ["base"],
                          "cells": {"c": {"base": {"result": "PASS"}}}}}
        br.build_block(run_dir, entry, _with(scaffolding=["/nope"]), root=rpr.ROOT)
    assert str(exc.value).count("do not resolve") == 1 and "tested base config" in str(exc.value)


# ---------------------------------------------------------------------------
# 5. Skill / handoff text: manifest instructions only in the flag-on stage
# ---------------------------------------------------------------------------

def test_1b_skill_writes_the_manifest_and_no_longer_forbids_it():
    text = SKILL_1B.read_text(encoding="utf-8")
    assert "Do not attempt to author a `block_manifest.yaml`" not in text
    assert "- `block_manifest.yaml`  (only when status is spec_ready" in text
    assert "Write `block_manifest.yaml` for every spec_ready config" in text
    assert "config-direct-authoring flow only" in text  # the skill's own scope line
    handoff = yaml.safe_load(HANDOFF_1B.read_text(encoding="utf-8"))
    assert any("block_manifest.yaml" in c for c in handoff["constraints"])
    assert not any("Do not attempt to author a block_manifest" in c for c in handoff["constraints"])
    # optional (component_gap writes none): never a required deliverable (ensure_files)
    assert "block_manifest.yaml" not in handoff["deliverables"]


def test_manifest_files_are_read_only_by_the_flag_on_stage():
    """The CONTENT of the 1b skill, its handoff and the design guide enters
    only the strategy_config_authoring prompt (routed to only under
    orchestrator.config_direct_authoring; test_e056_config_direct_authoring.py
    covers the routing) and, since the reader-inputs change, the five reader
    prompts (orchestrator.specialist_readers only; _reader_handoff lists the
    guide so readers stop inventing settings). Other skills -- e.g.
    innovation-expansion -- do NAME the design guide in their own text, but no
    other handoff template lists it as an input and workers run closed-book (tools=[],
    setting_sources=[] -- CUL-336; before it, allowed_tools=[] alone left the
    CLI's default tools on), so they never receive its content (proven
    prompt-by-prompt below)."""
    assert rpr._SKILL_MAP["strategy_config_authoring"] == "strategy-config-authoring"
    assert [s for s, k in rpr._SKILL_MAP.items() if k == "strategy-config-authoring"] == \
        ["strategy_config_authoring"]
    assert [s for s, c in rpr.STAGE_CONFIGS.items() if c["handoff"] == HANDOFF_1B.name] == \
        ["strategy_config_authoring"]
    templates = SR_ROOT / "workflow_artifacts" / "templates" / "handoffs"
    for tpl in templates.glob("*.yaml"):
        if tpl.name == HANDOFF_1B.name:
            continue
        assert "STRATEGY_DESIGN_GUIDE" not in tpl.read_text(encoding="utf-8"), tpl.name
    flag_off_skills = {k for s, k in rpr._SKILL_MAP.items() if s != "strategy_config_authoring"}
    for skill in flag_off_skills:
        text = (SR_ROOT / "workflow_artifacts" / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        assert "block_manifest" not in text, skill


# ---------------------------------------------------------------------------
# 6. Flag-off byte-identity of every flag-off stage prompt (incl. 1b's flag-off
#    counterpart, backtest_specification / backtest-engineering)
# ---------------------------------------------------------------------------

def _handoff(sr: Path, stage: str) -> dict:
    return yaml.safe_load((sr / "workflow_artifacts" / "templates" / "handoffs" /
                           rpr.STAGE_CONFIGS[stage]["handoff"]).read_text(encoding="utf-8"))


def _stub_required_inputs(sr: Path, run_dir: Path) -> None:
    """Every stage's missing required input, stubbed ONCE before any prompt is
    built (a stub made for one stage can be another stage's optional input)."""
    for stage in rpr._SKILL_MAP:
        for req in _handoff(sr, stage).get("required_inputs", []):
            p = run_dir / req["path"]
            if not p.exists():
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(f"stub for {req['path']}\n", encoding="utf-8")


def _prompts(sr: Path, run_dir: Path, stages) -> dict:
    return {stage: rpr._build_stage_prompt(stage, _handoff(sr, stage), run_dir) for stage in stages}


def _reader_prompts(run_dir: Path) -> dict:
    """The five specialist-reader prompts, built exactly as run_reader_worker
    builds them (_reader_handoff + _reader_skill_dir)."""
    out = {}
    for category in rpr._reader_categories():
        handoff = rpr._reader_handoff(category, "run_001", 0)
        for req in handoff["required_inputs"]:
            p = run_dir / req["path"]
            if not p.exists():
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(f"stub for {req['path']}\n", encoding="utf-8")
        out[category] = rpr._build_stage_prompt("specialist_readers", handoff, run_dir,
                                                skill_file_name=rpr._reader_skill_dir(category))
    return out


def test_flag_off_prompts_do_not_depend_on_the_changed_files(tmp_path, monkeypatch):
    sr = tmp_path / "sr"
    shutil.copytree(SR_ROOT / "workflow_artifacts", sr / "workflow_artifacts")
    shutil.copytree(SR_ROOT / "docs", sr / "docs")
    run_dir = sr / "runs" / "run_001"
    (run_dir / "artifacts").mkdir(parents=True)
    monkeypatch.chdir(sr)  # _build_stage_prompt reads the SKILL relative to cwd
    flag_off = [s for s in rpr._SKILL_MAP if s != "strategy_config_authoring"]
    assert "backtest_specification" in flag_off
    _stub_required_inputs(sr, run_dir)
    before = _prompts(sr, run_dir, flag_off)
    readers_before = _reader_prompts(run_dir)
    assert len(readers_before) == 5
    on_before = _prompts(sr, run_dir, ["strategy_config_authoring"])
    changed = [sr / "workflow_artifacts" / "skills" / "strategy-config-authoring" / "SKILL.md",
               sr / "workflow_artifacts" / "templates" / "handoffs" / HANDOFF_1B.name,
               sr / "docs" / "STRATEGY_DESIGN_GUIDE.md",
               sr / "workflow_artifacts" / "schemas" / "block_manifest.schema.json"]
    for p in changed:
        p.write_text("constraints: []\n" if p.suffix == ".yaml" else "BLANKED\n", encoding="utf-8")
    after = _prompts(sr, run_dir, flag_off)
    assert after == before
    # code-review fix 5 pinned the readers as independent of these files; the
    # reader-inputs change makes them read the design guide on purpose
    # (flag-on stage only -- every flag-off prompt above is unchanged).
    assert _reader_prompts(run_dir) != readers_before
    # the harness does see a dependency where there is one
    assert _prompts(sr, run_dir, ["strategy_config_authoring"]) != on_before


# ---------------------------------------------------------------------------
# 7. End to end: 1b output with manifest -> 5a -> validated grid -> block registered
# ---------------------------------------------------------------------------

def test_end_to_end_1b_manifest_to_registered_block(monkeypatch):
    _set_orchestrator({**ALL_ON, "config_direct_authoring": {"enabled": True}})
    run_dir = _seed(idea_status="validated")  # validated grid + ledger rows, no manifest
    arts = run_dir / "artifacts"
    # 1b's outputs (what the skill tells the LLM to write)
    rpr.save_yaml(arts / "backtest_spec.yaml", {"status": "spec_ready", "config": CONFIG,
                                                "config_rationale": ["x"], "component_gap": None})
    rpr.save_yaml(arts / "decision.yaml", {"stage": "strategy_config_authoring",
                                           "status": "spec_ready", "rationale": "x",
                                           "blocking_issues": []})
    (arts / "block_manifest.yaml").write_text(yaml.safe_dump(GOOD), encoding="utf-8")
    assert rpr.determine_post_strategy_config_authoring_route(run_dir) == "innovation_expansion"
    # innovation_expansion's patches, then the 5a tool stage. E-061 C2 S2b
    # (CUL-342, declared): base only -- with the variant loop off only the base
    # is backtested, so a `design` in the index would (correctly) keep this idea
    # from validating and registering (campaign_memory's belt check).
    rpr.save_yaml(arts / "variant_patches.yaml", {"variants": [
        {"variant_id": "base", "patch": [], "rationale": "base"}]})
    monkeypatch.setattr(rpr.subprocess, "run", _ok_subprocess)
    asyncio.run(rpr.run_tool_worker("backtest_specification", RUN_ID))
    base_cfg = json.loads((arts / "candidate_strategy_config.json").read_text(encoding="utf-8"))
    assert base_cfg == CONFIG
    # the backtest's trial row carries the tested config's hash (as _record_backtest_trial does)
    state = rpr.load_yaml(rpr.CAMPAIGN_STATE_PATH)
    for row in state["trial_sharpes"]:
        if row["trial_id"] == RUN_ID and row["source"] == "backtest":
            row["forecast_hash"] = hashlib.sha256(
                json.dumps(base_cfg, sort_keys=True).encode("utf-8")).hexdigest()
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)

    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    doc = yaml.safe_load((rpr.ROOT / "campaign_record" / "block_registry.yaml").read_text(encoding="utf-8"))
    [block] = doc["blocks"]
    assert block["block_id"] == f"H-MEM-1:{RUN_ID}" and block["kind"] == "forecast"
    assert block["config_fragment"] == {
        "/strategies/regimes/unknown/components/0": CONFIG["strategies"]["regimes"]["unknown"]["components"][0]}
    assert block["regime_assignment"] == {"regimes": ["unknown"], "detector_paths": []}
    assert _memory()["runs"][RUN_ID]["registry"] == {"block_ids": [f"H-MEM-1:{RUN_ID}"]}
