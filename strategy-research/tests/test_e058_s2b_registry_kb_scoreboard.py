"""
E-058 S2b -- block registry, grid KB writer, grid-aware near-miss scoreboard
and campaign-review's memory input, all from the regroup_record stage under
orchestrator.regroup_record.enabled (off by default). Spec:
engineering/roadmap/E-058/S1_FINDINGS.md guesses 1/2/5/6/7, §4, §6 and the
operator decision of 2026-09-23.

Fixtures reuse the S2a test module's synthetic run (_seed): no LLM, no
backtest. tests/conftest.py sandboxes rpr.ROOT / CAMPAIGN_STATE_PATH / _KB_PATH.
"""
import hashlib
import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import block_registry as br  # noqa: E402
import grid_kb_writer as kbw  # noqa: E402
import near_miss_scoreboard as nms  # noqa: E402
import record_schema  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_e058_s2a_regroup_record import (  # noqa: E402
    RUN_ID, READERS_ON, ALL_ON, _seed, _memory, _memory_path, _loop_from_specialist_readers,
    _stub_tbot_python)  # noqa: F401  (autouse fixture re-exported)
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402

BASE_CONFIG = {
    "regime_detector": {"rules": [{"regime": "trending", "op": "gte", "value": 0.5}]},
    "strategies": {"regimes": {"trending": {"components": [{"class": "Momentum", "params": {"n": 20}}]},
                               "ranging": {"components": []}}},
}
MANIFEST = {"block": {"kind": "forecast",
                      "config_paths": ["/strategies/regimes/trending/components/0"]},
            "scaffolding": ["/regime_detector"], "rationale": "the momentum block"}
LEGACY_KB_ENTRY = {
    "id": "h_mem_1_auto", "hypothesis_id": "H-MEM-1", "evidence_runs": ["run_001"],
    "evidence_count": 1, "outcome": "inconclusive", "verdict_status": "ungated",
    "reactivation_condition": "retest once 2 more years of data exist", "exhausted": False,
}


def _registry_path() -> Path:
    return rpr.ROOT / "campaign_record" / "block_registry.yaml"


def _sha(cfg: dict) -> str:
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode("utf-8")).hexdigest()


def _seed_s2b(run_id=RUN_ID, idea_status="validated", manifest=True, kb=True, **kw) -> Path:
    """_seed plus: a real base config whose sha is the ledger's forecast_hash,
    optionally a block_manifest.yaml and a KB holding a legacy entry with the
    same hypothesis_id."""
    run_dir = _seed(run_id=run_id, idea_status=idea_status, **kw)
    arts = run_dir / "artifacts"
    (arts / "candidate_strategy_config.json").write_text(json.dumps(BASE_CONFIG), encoding="utf-8")
    state = rpr.load_yaml(rpr.CAMPAIGN_STATE_PATH)
    for row in state["trial_sharpes"]:
        if row["trial_id"] == run_id and row["source"] == "backtest":
            row["forecast_hash"] = _sha(BASE_CONFIG)
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)
    if manifest:
        rpr.save_yaml(arts / "block_manifest.yaml", MANIFEST)
    if kb and not rpr._KB_PATH.exists():
        rpr._KB_PATH.write_text(yaml.safe_dump(
            {"schema_version": "05.A5", "findings": [dict(LEGACY_KB_ENTRY)]}, sort_keys=False),
            encoding="utf-8")
    return run_dir


def _kb() -> dict:
    return yaml.safe_load(rpr._KB_PATH.read_text(encoding="utf-8"))


def _registry() -> dict:
    return yaml.safe_load(_registry_path().read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. Flag off: nothing new happens
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status", ["validated", "refuted"])
def test_flag_off_writes_no_registry_kb_or_scoreboard(monkeypatch, idea_status):
    _set_orchestrator(READERS_ON)
    run_dir = _seed_s2b(idea_status=idea_status)
    kb_before = rpr._KB_PATH.read_bytes()
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    state["pending_stage"] = "specialist_readers"
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    _loop_from_specialist_readers(monkeypatch, READERS_ON, idea_status)
    assert rpr._KB_PATH.read_bytes() == kb_before
    assert not _registry_path().exists()
    assert not (rpr.ROOT / "engineering").exists()
    assert not _memory_path().exists()


def test_campaign_review_handoff_and_prompt_identical_flag_off(monkeypatch):
    monkeypatch.chdir(SR_ROOT)  # _build_stage_prompt reads the SKILL relative to cwd
    run_dir = _seed_s2b()
    handoff = {"run_id": RUN_ID, "required_inputs": [], "deliverables": ["campaign_review.yaml"]}
    _set_orchestrator(READERS_ON)
    off = json.loads(json.dumps(handoff))
    rpr._apply_regroup_record_context("campaign_review", off, run_dir)
    assert off == handoff
    assert rpr._build_stage_prompt("campaign_review", off, run_dir) == \
        rpr._build_stage_prompt("campaign_review", handoff, run_dir)

    _set_orchestrator(ALL_ON)
    _memory_path().parent.mkdir(parents=True, exist_ok=True)
    _memory_path().write_text("schema_version: 1\nruns: {}\n", encoding="utf-8")  # review fix 8
    on = json.loads(json.dumps(handoff))
    rpr._apply_regroup_record_context("campaign_review", on, run_dir)
    assert [r["path"] for r in on["required_inputs"]] == ["../../campaign_record/campaign_memory.yaml"]
    assert "idea_status" in on["required_inputs"][0]["reason"]
    rpr._apply_regroup_record_context("campaign_review", on, run_dir)  # idempotent
    assert len(on["required_inputs"]) == 1
    other = json.loads(json.dumps(handoff))
    rpr._apply_regroup_record_context("hypothesis_generation", other, run_dir)
    assert other == handoff


def test_campaign_review_template_does_not_require_memory():
    tpl = yaml.safe_load((SR_ROOT / "workflow_artifacts" / "templates" / "handoffs" /
                          "campaign_review.yaml").read_text(encoding="utf-8"))
    assert not any("campaign_memory" in r["path"] for r in tpl["required_inputs"])


# ---------------------------------------------------------------------------
# 2. Block registry
# ---------------------------------------------------------------------------

def test_validated_without_manifest_is_skipped_loudly(capsys):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(manifest=False)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert _memory()["runs"][RUN_ID]["registry"] == {"skipped": "no_manifest"}
    assert not _registry_path().exists()
    assert "no artifacts/block_manifest.yaml" in capsys.readouterr().out


def test_validated_with_manifest_registers_one_block():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    doc = _registry()
    assert doc["schema_version"] == 1 and doc["revision"] == 1 and doc["updated_at"]
    [block] = doc["blocks"]
    assert set(block) == set(br.BLOCK_FIELDS)
    assert block["block_id"] == f"H-MEM-1:{RUN_ID}"
    assert block["hypothesis_id"] == "H-MEM-1" and block["kind"] == "forecast"
    assert block["config_fragment"] == {
        "/strategies/regimes/trending/components/0": {"class": "Momentum", "params": {"n": 20}}}
    assert block["regime_assignment"] == {"regimes": ["trending"], "detector_paths": []}
    assert block["criteria_passed"] == ["ic_median", "trade_floor"]
    assert block["variants_passed"] == [RUN_ID]
    assert block["numbers"]["ic_median"][RUN_ID] == {"value": 0.031, "threshold": 0.02,
                                                    "n_windows": 2, "n_trades": 40}
    assert block["correlation_to_composite"] is None and block["residual_ic"] is None
    assert block["symbols_tested"] == ["BTCUSDT"]
    assert block["source_config_sha256"] == _sha(BASE_CONFIG)
    assert block["source_config_ref"] == f"runs/{RUN_ID}/artifacts/candidate_strategy_config.json"
    assert block["validated_by_run"] == RUN_ID
    assert _memory()["runs"][RUN_ID]["registry"] == {"block_ids": [f"H-MEM-1:{RUN_ID}"]}


def test_variant_loop_registers_from_the_base_variant_config():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(variant_loop=True)
    base_cfg = run_dir / "artifacts" / "variants" / "base" / "strategy_config.json"
    base_cfg.write_text(json.dumps(BASE_CONFIG), encoding="utf-8")
    state = rpr.load_yaml(rpr.CAMPAIGN_STATE_PATH)
    for row in state["trial_sharpes"]:
        if row["trial_id"] == f"{RUN_ID}:base":
            row["forecast_hash"] = _sha(BASE_CONFIG)
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, state)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    [block] = _registry()["blocks"]
    assert block["source_config_ref"] == f"runs/{RUN_ID}/artifacts/variants/base/strategy_config.json"
    assert block["variants_passed"] == ["base", "design"]
    assert block["symbols_tested"] == ["BTCUSDT", "ETHUSDT"]


def test_regime_block_assignment_from_detector_paths():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    rpr.save_yaml(run_dir / "artifacts" / "block_manifest.yaml",
                  {"block": {"kind": "regime", "config_paths": ["/regime_detector/rules/0"]},
                   "scaffolding": ["/strategies"], "rationale": "the trending gate"})
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    block = _registry()["blocks"][0]
    assert block["kind"] == "regime"
    assert block["regime_assignment"] == {"regimes": [], "detector_paths": ["/regime_detector/rules/0"]}


def test_identical_rerun_is_a_no_op():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    before = _registry_path().read_bytes()
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert _registry_path().read_bytes() == before
    assert _registry()["revision"] == 1


@pytest.mark.parametrize("change", ["manifest", "refuted", "no_manifest"])
def test_rerun_that_would_change_a_block_stops_loudly(change):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    reg_before, mem_before = _registry_path().read_bytes(), _memory_path().read_bytes()
    arts = run_dir / "artifacts"
    if change == "manifest":
        rpr.save_yaml(arts / "block_manifest.yaml",
                      {"block": {"kind": "forecast", "config_paths": ["/strategies/regimes/ranging"]},
                       "scaffolding": [], "rationale": "a different block"})
    elif change == "no_manifest":
        (arts / "block_manifest.yaml").unlink()
    else:
        grid = rpr.load_yaml(arts / "grid_evaluation.yaml")
        grid["grid"]["ic_median"][RUN_ID] = {"result": "FAIL", "value": 0.001, "threshold": 0.02,
                                            "n_windows": 2, "n_trades": 40}
        grid["idea_status"] = "refuted"
        rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
        rpr.save_yaml(arts / "idea_status.yaml", rpr._build_idea_status_artifact(grid, RUN_ID))
    with pytest.raises(br.BlockRegistryError, match="append-only"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert _registry_path().read_bytes() == reg_before
    assert _memory_path().read_bytes() == mem_before  # stopped before the memory was replaced


def test_fault_rerun_of_a_registered_run_is_logged_and_still_pauses(monkeypatch, capsys):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    reg_before = _registry_path().read_bytes()
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml",
                  {**rpr.load_yaml(run_dir / "artifacts" / "protocol_result.yaml"),
                   "results": [{"symbol": "BTCUSDT", "window": "w1", "core": {},
                                "component_errors": {"count": 1, "samples": []}}]})
    checks = rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert checks["component_errors"]
    out = capsys.readouterr().out
    # review fix 1: fault entry written FIRST, then the stale block / KB entry named loudly
    assert "block_registry.yaml still holds block(s)" in out
    assert "campaign_knowledge_base.yaml still holds grid entry 'grid_run_980'" in out
    assert _registry_path().read_bytes() == reg_before
    assert _memory()["runs"][RUN_ID]["engineering_fault"] == "component_execution_error"


@pytest.mark.parametrize("idea_status", ["refuted", "inconclusive"])
def test_no_block_for_refuted_or_inconclusive(idea_status):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(idea_status=idea_status)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert _memory()["runs"][RUN_ID]["registry"] == {"skipped": "not_validated"}
    assert not _registry_path().exists()


def test_fault_run_gets_no_block_and_no_kb_entry():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(errors_count=1)
    kb_before = rpr._KB_PATH.read_bytes()
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    e = _memory()["runs"][RUN_ID]
    assert e["engineering_fault"] == "component_execution_error"
    assert "registry" not in e and "kb_entry_id" not in e
    assert not _registry_path().exists()
    assert rpr._KB_PATH.read_bytes() == kb_before
    assert not (rpr.ROOT / "engineering").exists()


def test_config_changed_after_backtest_refuses_to_register():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    (run_dir / "artifacts" / "candidate_strategy_config.json").write_text(
        json.dumps({**BASE_CONFIG, "extra": 1}), encoding="utf-8")
    with pytest.raises(br.BlockRegistryError, match="forecast_hash"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert not _registry_path().exists() and not _memory_path().exists()


_M = {"scaffolding": [], "rationale": "r"}  # E-056 1b: the full manifest contract


@pytest.mark.parametrize("manifest,match", [
    ({"block": {"kind": "detector", "config_paths": ["/a"]}, **_M}, "block.kind"),
    ({"block": {"kind": "forecast", "config_paths": []}, **_M}, "config_paths"),
    ({"block": {"kind": "forecast", "config_paths": ["strategies"]}, **_M}, "config_paths"),
    ({"block": {"kind": "forecast", "config_paths": ["/strategies/regimes/nope"]}, **_M},
     "not resolve"),
    ({"block": {"kind": "forecast", "config_paths": ["/strategies/regimes/trending"]}}, "missing"),
    (["not", "a", "mapping"], "expected"),
])
def test_malformed_manifest_fails_loud(manifest, match):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    rpr.save_yaml(run_dir / "artifacts" / "block_manifest.yaml", manifest)
    with pytest.raises(br.BlockRegistryError, match=match):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert not _registry_path().exists()


@pytest.mark.parametrize("content,match", [
    ("blocks: [unclosed\n", "unparseable"),
    ("- a\n", "expected a mapping"),
    ("schema_version: 2\nrevision: 0\nblocks: []\n", "schema_version"),
    ("schema_version: 1\nrevision: 0\nblocks: {}\n", "blocks is not a list"),
    ("schema_version: 1\nrevision: -1\nblocks: []\n", "revision"),
    ("schema_version: 1\nrevision: 1\nblocks:\n- {block_id: x}\n", "missing"),
])
def test_malformed_registry_fails_loud_and_is_not_overwritten(content, match):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    _registry_path().parent.mkdir(parents=True, exist_ok=True)
    _registry_path().write_text(content, encoding="utf-8")
    with pytest.raises(br.BlockRegistryError, match=match):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert _registry_path().read_text(encoding="utf-8") == content


def test_second_run_appends_and_bumps_revision():
    _set_orchestrator(ALL_ON)
    rpr._run_regroup_record_stage(RUN_ID, _seed_s2b())
    rpr._run_regroup_record_stage("run_981", _seed_s2b(run_id="run_981"))
    doc = _registry()
    assert [b["validated_by_run"] for b in doc["blocks"]] == [RUN_ID, "run_981"]
    assert doc["revision"] == 2


def test_registry_file_matches_schema():
    jsonschema = pytest.importorskip("jsonschema")
    _set_orchestrator(ALL_ON)
    rpr._run_regroup_record_stage(RUN_ID, _seed_s2b())
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" / "block_registry.schema.json")
                        .read_text(encoding="utf-8"))
    jsonschema.validate(_registry(), schema)
    bad = _registry()
    bad["blocks"][0]["correlation_to_composite"] = 0.3  # slice 7 owns it
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schema)


def test_memory_file_with_s2b_fields_matches_schema():
    jsonschema = pytest.importorskip("jsonschema")
    _set_orchestrator(ALL_ON)
    for i, (status, manifest) in enumerate([("validated", True), ("validated", False),
                                            ("refuted", True), ("inconclusive", False)]):
        run_id = f"run_95{i}"
        rpr._run_regroup_record_stage(run_id, _seed_s2b(run_id=run_id, idea_status=status,
                                                        manifest=manifest))
    schema = json.loads((SR_ROOT / "workflow_artifacts" / "schemas" / "campaign_memory.schema.json")
                        .read_text(encoding="utf-8"))
    doc = _memory()
    jsonschema.validate(doc, schema)
    assert doc["runs"]["run_950"]["registry"] == {"block_ids": ["H-MEM-1:run_950"]}
    assert doc["runs"]["run_951"]["registry"] == {"skipped": "no_manifest"}
    assert doc["runs"]["run_952"]["kb_entry_id"] == "grid_run_952"


# ---------------------------------------------------------------------------
# 3. Grid KB writer
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("idea_status", ["validated", "refuted", "inconclusive"])
def test_kb_entry_shape_and_legacy_entry_untouched(idea_status):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(idea_status=idea_status)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    kb = _kb()
    assert kb["findings"][0] == LEGACY_KB_ENTRY  # same hypothesis_id, never merged or closed
    new = kb["findings"][1]
    expected = {"id": f"grid_{RUN_ID}", "hypothesis_id": "H-MEM-1", "evidence_runs": [RUN_ID],
                "evidence_count": 1, "outcome": idea_status, "legacy_schema": False}
    if idea_status != "inconclusive":
        expected |= {"verdict_status": "gated",
                     "pass_rule_evaluation_ref": f"runs/{RUN_ID}/artifacts/idea_status.yaml"}
    expected["outcome_reason"] = rpr.load_yaml(run_dir / "artifacts" / "idea_status.yaml")["reason"]
    assert new == expected
    vce.validate_verdict_provenance(new, root=rpr.ROOT)  # the ref resolves (PASS/FAIL)
    assert len(kb["findings"]) == 2
    assert _memory()["runs"][RUN_ID]["kb_entry_id"] == f"grid_{RUN_ID}"
    # derived views recomputed, like the legacy writer
    ids = [c["finding_id"] for cells in kb["coverage_matrix"].values() for c in cells]
    assert f"grid_{RUN_ID}" in ids and "h_mem_1_auto" in ids


def test_kb_rerun_replaces_own_entry_only():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(idea_status="refuted")
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    grid = rpr.load_yaml(run_dir / "artifacts" / "grid_evaluation.yaml")
    grid["grid"]["ic_median"][RUN_ID] = {"result": "INCONCLUSIVE", "n_windows": 2, "n_trades": 3}
    grid["idea_status"] = "inconclusive"
    rpr.save_yaml(run_dir / "artifacts" / "grid_evaluation.yaml", grid)
    rpr.save_yaml(run_dir / "artifacts" / "idea_status.yaml", rpr._build_idea_status_artifact(grid, RUN_ID))
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    kb = _kb()
    assert len(kb["findings"]) == 2 and kb["findings"][0] == LEGACY_KB_ENTRY
    assert kb["findings"][1]["outcome"] == "inconclusive"
    assert "pass_rule_evaluation_ref" not in kb["findings"][1]


def test_kb_writer_never_touches_the_legacy_writer_or_f09(monkeypatch):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(idea_status="refuted")

    def _boom(*a, **k):
        raise AssertionError("legacy KB machinery called from regroup_record")
    for name in ("_write_kb_findings_entry", "_find_kb_entry", "_verdict_provenance_stamp",
                 "_auto_generate_findings_carryover"):
        monkeypatch.setattr(rpr, name, _boom)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    legacy = _kb()["findings"][0]
    assert legacy["reactivation_condition"] == LEGACY_KB_ENTRY["reactivation_condition"]
    assert "reactivation_consumed_by" not in legacy


def test_kb_id_held_by_a_foreign_entry_fails_loud():
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    kb = _kb()
    kb["findings"].append({"id": f"grid_{RUN_ID}", "hypothesis_id": "OTHER",
                           "evidence_runs": ["run_001"], "outcome": "inconclusive"})
    rpr._KB_PATH.write_text(yaml.safe_dump(kb, sort_keys=False), encoding="utf-8")
    before = rpr._KB_PATH.read_bytes()
    with pytest.raises(kbw.GridKBError, match="did not write"):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert rpr._KB_PATH.read_bytes() == before


@pytest.mark.parametrize("content,exc,match", [
    ("findings: [unclosed\n", kbw.GridKBError, "unparseable"),
    ("- a\n", kbw.GridKBError, "expected a mapping"),
    ("findings: {a: 1}\n", kbw.GridKBError, "not a list"),
    ("findings:\n- {id: x, outcome: kill_mechanism_falsified}\n", vce.UngatedVerdictError, "kill"),
    ("findings:\n- {id: x, surprise_field: 1}\n", vce.UngatedVerdictError, "unknown field"),
])
def test_malformed_kb_fails_loud_and_is_not_overwritten(content, exc, match):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(kb=False)
    rpr._KB_PATH.write_text(content, encoding="utf-8")
    with pytest.raises(exc, match=match):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert rpr._KB_PATH.read_text(encoding="utf-8") == content


def test_absent_kb_is_skipped_loudly(capsys):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(kb=False)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert not rpr._KB_PATH.exists()
    assert _memory()["runs"][RUN_ID]["kb_entry_id"] is None
    assert "not found" in capsys.readouterr().out


def test_record_schema_accepts_legacy_schema_flag():
    entry = {"id": "grid_run_1", "hypothesis_id": "H", "evidence_runs": ["run_1"],
             "outcome": "inconclusive", "legacy_schema": False}
    assert record_schema.validate_kb_finding(entry) is entry
    with pytest.raises(record_schema.RecordSchemaError, match="boolean"):
        record_schema.validate_kb_finding({**entry, "legacy_schema": "false"})


def test_build_kb_entry_refuses_a_fault_entry():
    with pytest.raises(kbw.GridKBError, match="engineering-fault"):
        kbw.build_kb_entry({"run_id": "run_1", "engineering_fault": "component_execution_error"})


# ---------------------------------------------------------------------------
# 4. Near-miss scoreboard
# ---------------------------------------------------------------------------

def _write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


PRE_REG = {"pass_rule": {"criteria": [
    {"id": "ic_median", "source": "window", "metric": "ic", "reducer": "median",
     "comparator": ">=", "threshold": 0.02},
    {"id": "trade_floor", "source": "pooled", "metric": "n", "comparator": ">=", "threshold": 30}]}}


def test_grid_row_closest_failing_cell_and_legacy_rows(tmp_path):
    runs = tmp_path / "runs"
    grid_dir = runs / "run_100"
    _write(grid_dir / "artifacts" / "pre_registration.yaml", PRE_REG)
    _write(grid_dir / "artifacts" / "hypothesis_card.yaml", {"hypothesis_id": "H-G"})
    _write(grid_dir / "artifacts" / "grid_evaluation.yaml", {
        "result": "GRID_EVALUATED", "criteria": ["ic_median", "trade_floor"],
        "variants": ["base", "asset"], "idea_status": "refuted", "reason": "a cell FAILed",
        "grid": {
            "ic_median": {"base": {"result": "FAIL", "value": 0.001, "threshold": 0.02},
                          "asset": {"result": "FAIL", "per_symbol": {
                              "BTCUSDT": {"result": "PASS", "value": 0.03, "threshold": 0.02},
                              "ETHUSDT": {"result": "FAIL", "value": 0.018, "threshold": 0.02}}}},
            "trade_floor": {"base": {"result": "PASS", "value": 40, "threshold": 30},
                            "asset": {"result": "INCONCLUSIVE", "reason": "floor"}}}})
    _write(runs / "run_050" / "artifacts" / "verdict_interpretation.yaml", {
        "protocol_verdict": "kill", "status": "kill",
        "criteria_summary": [{"criterion": "x", "result": "FAIL", "actual": 0.0, "required": "> 1.0"}]})
    (runs / "run_010").mkdir(parents=True)
    rows = {r["run_id"]: r for r in nms.build_scoreboard(runs)}
    g = rows["run_100"]
    assert g["evidence_tier"] == "grid" and g["legacy"] is False
    assert g["idea_status"] == "refuted" and g["hypothesis_id"] == "H-G"
    # review fix 4: ic_median binds at its WORST failing cell (base), not the nearest
    assert g["worst_fail_margin_frac"] == pytest.approx((0.001 - 0.02) / 0.02)
    assert g["worst_fail_criterion_text"].startswith("ic_median @ base")
    assert g["worst_fail_margin_source"] == "grid"
    assert (g["n_criteria_pass"], g["n_criteria_fail"], g["n_criteria_untested"]) == (1, 2, 1)
    assert g["status"] == "not_recorded" and g["hypothesis_family"] == "not_recorded"
    assert rows["run_050"]["legacy"] is True and rows["run_050"]["evidence_tier"] == "full_protocol"
    assert rows["run_010"]["legacy"] is True and rows["run_010"]["evidence_tier"] == "thin_no_verdict_file"
    assert rows["run_100"]["rank"] == 1  # the nearest miss ranks first
    denom = "\n".join(nms._denominator_report(list(rows.values())))
    assert "Have a verdict_interpretation.yaml: 1 of 3" in denom
    assert "Grid row (grid_evaluation.yaml, no verdict file; legacy: false): 1 of 3" in denom


def test_grid_row_without_comparator_records_no_margin(tmp_path):
    run_dir = tmp_path / "runs" / "run_100"
    _write(run_dir / "artifacts" / "grid_evaluation.yaml", {
        "result": "GRID_EVALUATED", "criteria": ["c"], "variants": ["v"], "idea_status": "refuted",
        "grid": {"c": {"v": {"result": "FAIL", "value": 0.0, "threshold": 1.0}}}})
    row = nms.build_row(run_dir)
    assert row["worst_fail_margin_frac"] is None
    assert row["worst_fail_margin_source"] == "grid_cell_without_value_or_comparator"


def test_malformed_grid_file_fails_loud(tmp_path):
    run_dir = tmp_path / "runs" / "run_100"
    _write(run_dir / "artifacts" / "grid_evaluation.yaml", {"result": "GRID_EVALUATED"})
    with pytest.raises(ValueError, match="not a grid_evaluation"):
        nms.build_row(run_dir)


def test_stage_rebuilds_scoreboard_under_root_only():
    real = SR_ROOT / "engineering" / "roadmap" / "E-018" / "artifacts" / "near_miss_scoreboard.yaml"
    real_before = real.read_bytes() if real.exists() else None
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(idea_status="refuted")
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", PRE_REG)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    out = rpr.ROOT / "engineering" / "roadmap" / "E-018" / "artifacts" / "near_miss_scoreboard.yaml"
    doc = yaml.safe_load(out.read_text(encoding="utf-8"))
    [row] = [r for r in doc["rows"] if r["run_id"] == RUN_ID]
    assert row["evidence_tier"] == "grid" and row["idea_status"] == "refuted"
    assert row["worst_fail_margin_frac"] == pytest.approx((0.001 - 0.02) / 0.02)
    assert (out.parent / "near_miss_scoreboard.md").exists()
    assert (real.read_bytes() if real.exists() else None) == real_before


def test_route_never_reads_the_scoreboard(monkeypatch):
    """Firewall: the route after regroup_record is unchanged with the scoreboard
    module unavailable to it (it is called only from the stage body)."""
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(idea_status="refuted", pending="regroup_record")
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["pending_stage"] == "completed_rejected"
    import inspect
    src = inspect.getsource(rpr.determine_post_specialist_readers_route)
    assert "scoreboard" not in src and "block_registry" not in src and "campaign_memory" not in src


# ---------------------------------------------------------------------------
# 5. No trial rows
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("variant_loop", [False, True])
def test_trial_ledger_byte_identical_with_registry_and_kb(variant_loop):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(idea_status="validated" if not variant_loop else "refuted",
                        variant_loop=variant_loop)
    before = rpr.CAMPAIGN_STATE_PATH.read_bytes()
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert rpr.CAMPAIGN_STATE_PATH.read_bytes() == before
    assert _kb()["findings"][-1]["id"] == f"grid_{RUN_ID}"
