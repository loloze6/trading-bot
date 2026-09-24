"""
E-058 S2b code-review fixes (review of 55ee12f1). One regression test per fix;
each one fails on 55ee12f1. Numbering follows the review.
"""
import contextlib
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
import campaign_lock  # noqa: E402
import campaign_memory as cm  # noqa: E402
import grid_kb_writer as kbw  # noqa: E402
import json_pointer as jp  # noqa: E402
import near_miss_scoreboard as nms  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from test_e058_s2a_regroup_record import (  # noqa: E402
    RUN_ID, READERS_ON, ALL_ON, _memory, _memory_path, _stub_tbot_python)  # noqa: F401
from test_e058_s2b_registry_kb_scoreboard import (  # noqa: E402
    _seed_s2b, _registry_path, _kb, LEGACY_KB_ENTRY)
from test_e046a_slice5b_ii_b_readers_stage import _set_orchestrator  # noqa: E402
import test_e058_s2a_regroup_record as s2a  # noqa: E402

_camp = s2a.camp


def _make_fault(run_dir: Path) -> None:
    pr = rpr.load_yaml(run_dir / "artifacts" / "protocol_result.yaml")
    pr["results"] = [{"symbol": "BTCUSDT", "window": "w1", "core": {},
                      "component_errors": {"count": 1, "samples": []}}]
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", pr)


def _write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# 1. Fault path: memory FIRST, then a loud stop on stale records; pause fires
# ---------------------------------------------------------------------------

def test_fault_rerun_writes_fault_entry_first_then_names_stale_records(capsys):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    rpr._run_regroup_record_stage(RUN_ID, run_dir)  # validated pass: block + KB entry
    reg_before, kb_before = _registry_path().read_bytes(), rpr._KB_PATH.read_bytes()
    _make_fault(run_dir)
    rpr.save_yaml(run_dir / "pipeline_state.yaml",
                  {**rpr.load_yaml(run_dir / "pipeline_state.yaml"), "pending_stage": "regroup_record"})
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["status"] == "paused_for_human"
    assert _camp._classify_human_pause(run_dir, state) == "component_execution_error"
    assert _memory()["runs"][RUN_ID]["engineering_fault"] == "component_execution_error"
    out = capsys.readouterr().out
    assert "block_registry.yaml still holds block(s)" in out and "grid entry 'grid_run_980'" in out
    assert "a person decides" in out
    assert _registry_path().read_bytes() == reg_before and rpr._KB_PATH.read_bytes() == kb_before


def test_fault_run_with_malformed_registry_still_records_and_names_the_right_file(capsys):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(errors_count=1)
    _registry_path().parent.mkdir(parents=True, exist_ok=True)
    _registry_path().write_text("blocks: [unclosed\n", encoding="utf-8")
    rpr._run_regroup_record_stage(RUN_ID, run_dir)
    assert _memory()["runs"][RUN_ID]["engineering_fault"] == "component_execution_error"
    out = capsys.readouterr().out
    assert "stale-record check (block_registry.yaml" in out
    assert "fix the memory file" not in out


# ---------------------------------------------------------------------------
# 2. Legacy KB writer: skips grid entries, takes the KB lock, byte-identical
# ---------------------------------------------------------------------------

INTERP = {"hypothesis_id": "H-MEM-1", "run_id": "run_001", "verdict_label": "kill_no_ic"}


def test_legacy_writer_never_merges_into_a_grid_entry():
    grid_entry = {"id": "grid_run_900", "hypothesis_id": "H-MEM-1", "evidence_runs": ["run_900"],
                  "evidence_count": 1, "outcome": "inconclusive", "legacy_schema": False}
    rpr._KB_PATH.write_text(yaml.safe_dump({"findings": [dict(grid_entry)]}, sort_keys=False),
                            encoding="utf-8")
    rpr._write_kb_findings_entry(rpr.ROOT, "run_001", INTERP)
    findings = _kb()["findings"]
    assert findings[0] == grid_entry
    assert findings[1]["id"] == "h_mem_1_auto" and findings[1]["evidence_runs"] == ["run_001"]


def test_legacy_writer_waits_on_the_kb_lock(monkeypatch):
    rpr._KB_PATH.write_text(yaml.safe_dump({"findings": []}), encoding="utf-8")
    before = rpr._KB_PATH.read_bytes()
    monkeypatch.setattr(cm, "MEMORY_LOCK_WAIT_SECONDS", 0.2)
    lock = rpr._KB_PATH.parent / kbw.KB_LOCK_FILENAME
    campaign_lock.acquire(lock)
    try:
        with pytest.raises(cm.CampaignMemoryError, match="still held"):
            rpr._write_kb_findings_entry(rpr.ROOT, "run_001", INTERP)
    finally:
        campaign_lock.release(lock)
    assert rpr._KB_PATH.read_bytes() == before


@pytest.mark.parametrize("existing", [False, True])
def test_legacy_writer_output_byte_identical_without_grid_entries(monkeypatch, existing):
    """Flag-off: on a KB with no grid entry, the lock and the skip change no byte."""
    seed = {"schema_version": "05.A5", "findings": [dict(LEGACY_KB_ENTRY)] if existing else []}

    def _run(lock_on: bool) -> bytes:
        rpr._KB_PATH.write_text(yaml.safe_dump(seed, sort_keys=False), encoding="utf-8")
        if not lock_on:
            monkeypatch.setattr(cm, "_file_lock", lambda *a, **k: contextlib.nullcontext())
        rpr._write_kb_findings_entry(rpr.ROOT, "run_001", INTERP)
        return rpr._KB_PATH.read_bytes()
    locked = _run(True)
    assert not (rpr._KB_PATH.parent / kbw.KB_LOCK_FILENAME).exists()
    unlocked = _run(False)
    assert locked == unlocked
    assert rpr._find_kb_entry(seed["findings"], "H-MEM-1") == (seed["findings"][0] if existing else None)


# ---------------------------------------------------------------------------
# 3. The scoreboard never fails the stage; malformed runs get a marked row
# ---------------------------------------------------------------------------

def test_scoreboard_error_does_not_fail_the_stage(monkeypatch, capsys):
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b(idea_status="refuted", pending="regroup_record")

    def _boom(*a, **k):
        raise RuntimeError("scoreboard exploded")
    monkeypatch.setattr(nms, "build_scoreboard", _boom)
    rpr.run_loop(RUN_ID)
    state = rpr.load_yaml(run_dir / "pipeline_state.yaml")
    assert state["pending_stage"] == "completed_rejected"
    assert RUN_ID in _memory()["runs"]
    assert "near-miss scoreboard NOT rebuilt (RuntimeError: scoreboard exploded)" in capsys.readouterr().out


def test_malformed_unrelated_run_gets_a_marked_row(tmp_path):
    runs = tmp_path / "runs"
    (runs / "run_001" / "artifacts").mkdir(parents=True)
    (runs / "run_001" / "artifacts" / "verdict_interpretation.yaml").write_text("a: [unclosed\n",
                                                                                encoding="utf-8")
    _write(runs / "run_002" / "artifacts" / "grid_evaluation.yaml", {"result": "GRID_EVALUATED"})
    (runs / "run_003").mkdir()
    rows = {r["run_id"]: r for r in nms.build_scoreboard(runs)}
    assert rows["run_001"]["evidence_tier"] == "malformed"
    assert rows["run_001"]["malformed_reason"].startswith(("ScannerError", "ParserError"))
    assert rows["run_002"]["evidence_tier"] == "malformed"
    assert "not a grid_evaluation document" in rows["run_002"]["malformed_reason"]
    assert rows["run_003"]["evidence_tier"] == "thin_no_verdict_file"
    denom = "\n".join(nms._denominator_report(list(rows.values())))
    assert "Malformed run dirs (row marked, not built): 2 of 3" in denom
    assert "Have a verdict_interpretation.yaml: 0 of 3" in denom
    nms.render_markdown(list(rows.values()), [])  # renders


# ---------------------------------------------------------------------------
# 4. Worst failing margin per criterion (unanimity), nearest across criteria
# ---------------------------------------------------------------------------

def test_worst_margin_within_criterion_nearest_across_criteria(tmp_path):
    run_dir = tmp_path / "runs" / "run_100"
    fail = lambda v, t: {"result": "FAIL", "value": v, "threshold": t, "comparator": ">="}  # noqa: E731
    _write(run_dir / "artifacts" / "grid_evaluation.yaml", {
        "result": "GRID_EVALUATED", "criteria": ["a", "b"], "variants": ["base", "asset"],
        "idea_status": "refuted",
        "grid": {"a": {"base": {"result": "FAIL", "per_symbol": {"BTCUSDT": fail(0.9, 1.0),
                                                                  "ETHUSDT": fail(0.5, 1.0)}},
                       "asset": {"result": "PASS", "value": 2.0, "threshold": 1.0}},
                 "b": {"base": fail(0.8, 1.0), "asset": fail(0.7, 1.0)}}})
    row = nms.build_row(run_dir)
    # a: worst = ETHUSDT -0.5 ; b: worst = asset -0.3 ; nearest criterion = b
    assert row["worst_fail_margin_frac"] == pytest.approx(-0.3)
    assert row["worst_fail_criterion_text"].startswith("b @ asset")


# ---------------------------------------------------------------------------
# 5. A verdict file wins: the legacy row is built exactly as before
# ---------------------------------------------------------------------------

def test_run_with_verdict_file_and_grid_keeps_its_legacy_row(tmp_path):
    run_dir = tmp_path / "runs" / "run_100"
    verdict = {"protocol_verdict": "kill", "status": "kill",
               "criteria_summary": [{"criterion": "x", "result": "FAIL", "actual": 0.5, "required": "> 1.0"}]}
    _write(run_dir / "artifacts" / "verdict_interpretation.yaml", verdict)
    legacy_only = nms.build_row(run_dir)
    _write(run_dir / "artifacts" / "grid_evaluation.yaml", {
        "result": "GRID_EVALUATED", "criteria": ["c"], "variants": ["v"], "idea_status": "validated",
        "grid": {"c": {"v": {"result": "PASS", "value": 1, "threshold": 0}}}})
    both = nms.build_row(run_dir)
    assert both == legacy_only
    assert both["evidence_tier"] == "full_protocol" and both["legacy"] is True


# ---------------------------------------------------------------------------
# 6. Base variant = protocol_execution's rule ("base", else sorted()[0])
# ---------------------------------------------------------------------------

def _variant(status):
    return {"status": status, "config_ref": "runs/r/cfg.json", "forecast_hash": "h"}


def test_base_variant_falls_back_like_protocol_execution():
    entry = {"run_id": "r", "variants": {"beta": _variant("tested"), "alpha": _variant("tested"),
                                         "zeta": {"status": "not_tested"}}}
    assert br._base_variant(entry)[0] == "alpha"
    assert jp.base_variant_id(["beta", "alpha"]) == "alpha"
    assert jp.base_variant_id({"base": 1, "alpha": 2}) == "base"


def test_failed_fallback_base_raises_instead_of_picking_another():
    entry = {"run_id": "r", "variants": {"alpha": _variant("failed"), "beta": _variant("tested")}}
    with pytest.raises(br.BlockRegistryError, match="'alpha'"):
        br._base_variant(entry)


# ---------------------------------------------------------------------------
# 7. Ranking: grid rows by idea_status, never below legacy kills
# ---------------------------------------------------------------------------

def test_grid_rows_rank_by_idea_status():
    def r(run_id, tier, margin=None, status="not_recorded", idea="not_recorded"):
        return {"run_id": run_id, "evidence_tier": tier, "worst_fail_margin_frac": margin,
                "status": status, "idea_status": idea, "ic": None}
    rows = [r("legacy_kill_margin", "full_protocol", -0.01, "kill"),
            r("legacy_refine", "full_protocol", None, "refine"),
            r("grid_refuted_nomargin", "grid", None, idea="refuted"),
            r("grid_refuted", "grid", -0.5, idea="refuted"),
            r("grid_inconclusive", "grid", idea="inconclusive"),
            r("grid_validated", "grid", idea="validated"),
            r("thin", "thin_no_verdict_file")]
    nms.rank_rows(rows)
    assert [x["run_id"] for x in rows] == [
        "grid_validated", "grid_inconclusive", "legacy_kill_margin", "grid_refuted",
        "legacy_refine", "grid_refuted_nomargin", "thin"]


# ---------------------------------------------------------------------------
# 8. campaign_review gets the memory only when the file exists
# ---------------------------------------------------------------------------

def test_campaign_review_input_skipped_when_memory_absent(monkeypatch):
    monkeypatch.chdir(SR_ROOT)
    _set_orchestrator(ALL_ON)
    run_dir = _seed_s2b()
    handoff = {"run_id": RUN_ID, "required_inputs": [], "deliverables": ["campaign_review.yaml"]}
    h = json.loads(json.dumps(handoff))
    rpr._apply_regroup_record_context("campaign_review", h, run_dir)
    assert h == handoff
    rpr._build_stage_prompt("campaign_review", h, run_dir)  # no FileNotFoundError


# ---------------------------------------------------------------------------
# 9. Comparator frozen with the run; "==" known; current menu never read
# ---------------------------------------------------------------------------

def test_cell_comparator_wins_and_current_menu_is_not_read(tmp_path):
    runs = tmp_path / "runs"
    _write(tmp_path / "config" / "criterion_menu.yaml",
           {"criteria": [{"id": "m", "source": "window", "metric": "x", "reducer": "median",
                          "comparator": ">=", "threshold": 1.0}]})
    a = runs / "run_a"
    _write(a / "artifacts" / "pre_registration.yaml",
           {"pass_rule": {"criteria": [{"id": "c", "source": "window", "comparator": ">="}]}})
    _write(a / "artifacts" / "grid_evaluation.yaml", {
        "result": "GRID_EVALUATED", "criteria": ["c"], "variants": ["v"], "idea_status": "refuted",
        "grid": {"c": {"v": {"result": "FAIL", "value": 2.0, "threshold": 1.0, "comparator": "<="}}}})
    b = runs / "run_b"  # id-only criterion: only the CURRENT menu knows its comparator
    _write(b / "artifacts" / "pre_registration.yaml",
           {"pass_rule": {"criteria": [{"id": "m", "source": "window"}]}})
    _write(b / "artifacts" / "grid_evaluation.yaml", {
        "result": "GRID_EVALUATED", "criteria": ["m"], "variants": ["v"], "idea_status": "refuted",
        "grid": {"m": {"v": {"result": "FAIL", "value": 0.5, "threshold": 1.0}}}})
    rows = {r["run_id"]: r for r in nms.build_scoreboard(runs)}
    assert rows["run_a"]["worst_fail_margin_frac"] == pytest.approx(-1.0)  # (1.0 - 2.0)/1.0 under "<="
    assert "<=" in rows["run_a"]["worst_fail_criterion_text"]
    assert rows["run_b"]["worst_fail_margin_frac"] is None
    assert rows["run_b"]["worst_fail_margin_source"] == "grid_cell_without_value_or_comparator"
    assert nms._OP_NORM["=="] == "=="


def test_evaluator_stamps_the_comparator_on_the_cell():
    crit = {"id": "c", "metric": "sharpe", "source": "window", "reducer": "median",
            "comparator": ">=", "threshold": 0.0}
    pr = {"results": [{"window": "w1", "core": {"sharpe": 0.5, "trade_count": 10}}]}
    cell = vce._evaluate_grid_cell(crit, pr, [])
    assert cell["result"] == "PASS" and cell["comparator"] == ">="


# ---------------------------------------------------------------------------
# 10. One JSON-pointer implementation for the orchestrator and the registry
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("pointer", ["/l/0", "/l/ 1", "/l/-1", "/l/9", "/d/k", "/d/x", "nope", "/"])
def test_registry_resolves_exactly_what_the_orchestrator_accepts(pointer):
    cfg = {"l": [10, 11], "d": {"k": 1}}
    exists = rpr._json_pointer_exists(cfg, pointer)
    try:
        br._jp.resolve_json_pointer(cfg, pointer)  # what build_block reads fragments with
        resolved = True
    except br._jp.JsonPointerError:
        resolved = False
    assert resolved == exists


def test_split_json_pointer_keeps_patch_application_error():
    with pytest.raises(rpr.PatchApplicationError):
        rpr._split_json_pointer("no-slash")
    assert rpr._split_json_pointer("/a~1b/c~0") == ["a/b", "c~"]
