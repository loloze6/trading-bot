"""
E-061 C2 S2a -- a crashed variant can never validate an idea (D-015; C2_S1_FINDINGS.md
C2.4, guesses G11 and G15). The joined-up case lives in test_e061_end_to_end_wiring.py
(test_c2_4_one_crashed_variant_never_validates).

Covers, one block per consumer of "grid column = tested variant":
  1. The grid (tools/verdict_criteria_evaluator.py::evaluate_grid): a failed
     variant is an INCONCLUSIVE not_graded column, no grader runs for it; FAIL on
     another variant still refutes (D-014); failed_variants None / {} is
     byte-identical to the call without it; malformed input raises.
  2. The variant loop (run_phase1_research.run_tool_worker, protocol_execution):
     a crashed variant reaches the grid as a failed column; the idea is
     inconclusive where the survivors alone would validate; trial rows unchanged.
  3. Branch 3 (_profit_bars_backtest_candidates): a failed column is NOT_TESTED,
     never graded -- even with a stale passing protocol_result.yaml on disk.
  4. Campaign memory (tools/campaign_memory.py): the failed column is `failed`
     (never `tested`), its cells keep `not_graded`, schema-valid; a corrupt
     failed_variants raises. decide_next / novelty read that status.
  5. Block registry (tools/block_registry.py::build_block): refuses a validated
     entry whose grid holds a non-tested column.
"""
import asyncio
import copy
import json
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import run_phase1_research as rpr  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402
import campaign_memory as cm  # noqa: E402
import block_registry as br  # noqa: E402
import decide_next as dn  # noqa: E402
import novelty as nov  # noqa: E402

from test_grid_evaluation import (  # noqa: E402
    _protocol_result, _windows_for_reducer, _menu_shaped_pre_reg)
from test_e033_slice4a_variant_loop import (  # noqa: E402
    _set_flag, _write_three_variant_index, _summary_for)
from test_k3_protocol_pinning import _minimal_run, _write_protocol  # noqa: E402
from test_profit_bars_every_backtest import (  # noqa: E402
    FULL_ON, VARIANT_LOOP_ON, RUN_ID, _variant_run, _write_bars, _grid, _memory,
    _set_orchestrator, _SCHEMA)

CRASH = "backtest_failed: run_protocol.py non-zero exit (1)"
PASS_CRIT = {"id": "c1", "metric": "net_return_pct", "source": "window", "reducer": "median",
             "comparator": ">", "threshold": 0.0, "floor": {"min_windows": 1}}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _good():
    return _protocol_result(_windows_for_reducer([1.0, 2.0, 3.0]))


def _bad():
    return _protocol_result(_windows_for_reducer([-1.0, -2.0, -3.0]))


# ---------------------------------------------------------------------------
# 1. The grid
# ---------------------------------------------------------------------------

def test_two_passing_survivors_and_one_crashed_variant_is_inconclusive():
    pre = _menu_shaped_pre_reg([PASS_CRIT])
    survivors = vce.evaluate_grid({"base": _good(), "design": _good()}, pre, {}, {})
    assert survivors["idea_status"] == "validated"  # the survivors alone would validate
    res = vce.evaluate_grid({"base": _good(), "design": _good()}, pre, {}, {},
                            failed_variants={"asset": CRASH})
    assert res["idea_status"] == "inconclusive"
    assert res["variants"] == ["base", "design", "asset"]
    assert res["failed_variants"] == {"asset": CRASH}
    assert res["grid"]["c1"]["asset"] == {"result": "INCONCLUSIVE", "not_graded": True,
                                          "reason": CRASH}
    assert res["grid"]["c1"]["base"] == survivors["grid"]["c1"]["base"]
    assert "['asset']" in res["reason"] and "D-015" in res["reason"]


def test_a_genuine_fail_on_a_survivor_still_refutes():
    """D-014: FAIL dominates the crashed column's INCONCLUSIVE."""
    pre = _menu_shaped_pre_reg([PASS_CRIT])
    res = vce.evaluate_grid({"base": _bad()}, pre, {}, {}, failed_variants={"asset": CRASH})
    assert res["idea_status"] == "refuted"
    assert res["grid"]["c1"]["asset"]["not_graded"] is True


def test_no_grader_runs_for_a_failed_column(monkeypatch):
    graded, profit = [], []
    real = vce._evaluate_grid_cell

    def _spy(crit, pr, eras, composition_runs=False):
        graded.append(id(pr))
        return real(crit, pr, eras, composition_runs=composition_runs)
    monkeypatch.setattr(vce, "_evaluate_grid_cell", _spy)
    pre = _menu_shaped_pre_reg([PASS_CRIT, {"id": "profit_bars", "source": "profit_bars",
                                            "reducer": "all_pass"}])

    def _grader(vid):
        profit.append(vid)
        return {"result": "PASS", "bars": [{"name": "sharpe_min", "result": "PASS"}],
                "reasons": []}
    res = vce.evaluate_grid({"base": _good()}, pre, {}, {}, composition_runs=True,
                            profit_bars_grader=_grader, failed_variants={"asset": CRASH})
    assert len(graded) == 1 and profit == ["base"]
    assert all(res["grid"][c]["asset"]["not_graded"] for c in ("c1", "profit_bars"))
    assert res["idea_status"] == "inconclusive"


@pytest.mark.parametrize("failed", [None, {}])
def test_no_failed_variant_is_byte_identical(failed):
    pre = _menu_shaped_pre_reg([PASS_CRIT])
    today = vce.evaluate_grid({"base": _good(), "design": _bad()}, pre, {}, {})
    got = vce.evaluate_grid({"base": _good(), "design": _bad()}, pre, {}, {},
                            failed_variants=failed)
    assert yaml.safe_dump(got) == yaml.safe_dump(today)
    assert "failed_variants" not in got


@pytest.mark.parametrize("failed,exc,match", [
    ({"base": CRASH}, ValueError, "both graded"),
    ({"asset": ""}, ValueError, "non-empty strings"),
    ({"asset": None}, ValueError, "non-empty strings"),
    (["asset"], TypeError, "dict"),
])
def test_malformed_failed_variants_raise(failed, exc, match):
    with pytest.raises(exc, match=match):
        vce.evaluate_grid({"base": _good()}, _menu_shaped_pre_reg([PASS_CRIT]), {}, {},
                          failed_variants=failed)


# ---------------------------------------------------------------------------
# 2. The variant loop
# ---------------------------------------------------------------------------

def _loop_with_crash(monkeypatch, run_id: str, crash: str | None):
    _set_flag(rpr.ROOT, {"config_direct_authoring": {"enabled": True},
                         "variant_loop": {"enabled": True},
                         "grid_evaluation": {"enabled": True}})
    _write_protocol(rpr.ROOT, f"{run_id}.json")
    run_dir = _minimal_run(rpr.ROOT, run_id)
    (run_dir / "artifacts" / "validation_protocol.yaml").write_text("{}", encoding="utf-8")
    rpr._ensure_protocol_ref_pinned(run_dir, run_id, {"protocol_ref": f"protocols/{run_id}.json"})
    _write_three_variant_index(run_dir)
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml",
                  _menu_shaped_pre_reg([{**PASS_CRIT, "metric": "sharpe"}]))

    def _run(cmd, *a, **k):
        vid = Path(cmd[2]).parent.name
        out = Path(cmd[cmd.index("--out-dir") + 1])
        out.mkdir(parents=True, exist_ok=True)
        if vid == crash:
            class _Fail:
                returncode, stdout, stderr = 1, "", "boom"
            return _Fail()
        summary = _summary_for(vid)
        summary["results"] = _windows_for_reducer([1.0, 2.0, 3.0])
        for r in summary["results"]:
            r["core"]["sharpe"] = 1.0
        (out / "protocol_summary.json").write_text(json.dumps(summary), encoding="utf-8")

        class _Ok:
            returncode, stdout, stderr = 0, "", ""
        return _Ok()
    monkeypatch.setattr(rpr.subprocess, "run", _run)
    asyncio.run(rpr.run_tool_worker("protocol_execution", run_id))
    return run_dir


def test_variant_loop_passes_the_crashed_variant_to_the_grid(monkeypatch):
    run_dir = _loop_with_crash(monkeypatch, "run_941", crash="design_v2")
    grid = rpr.load_yaml(run_dir / "artifacts" / "grid_evaluation.yaml")
    assert grid["failed_variants"] == {"design_v2": CRASH}
    assert grid["variants"] == ["asset_v2", "base", "design_v2"]
    assert grid["idea_status"] == "inconclusive"
    assert rpr.load_yaml(run_dir / "artifacts" / "idea_status.yaml")["idea_status"] == "inconclusive"
    rows = sorted((t["trial_id"], t["source"]) for t in rpr.load_campaign_state()["trial_sharpes"])
    assert rows == [("run_941:asset_v2", "backtest"), ("run_941:base", "backtest"),
                    ("run_941:design_v2", "backtest_failed")]


def test_variant_loop_without_a_crash_validates_and_writes_no_failed_key(monkeypatch):
    run_dir = _loop_with_crash(monkeypatch, "run_942", crash=None)
    grid = rpr.load_yaml(run_dir / "artifacts" / "grid_evaluation.yaml")
    assert "failed_variants" not in grid and grid["idea_status"] == "validated"


# ---------------------------------------------------------------------------
# 3. Branch 3 and 4. memory
# ---------------------------------------------------------------------------

def _crashed_column_run(stale_good: bool) -> Path:
    """`base` graded (all PASS), `broken` crashed: a failed_variants column, with a
    stale passing protocol_result.yaml left on disk when stale_good."""
    run_dir = _variant_run({"base": True}, stale={"good": True} if stale_good else None)
    arts = run_dir / "artifacts"
    grid = _grid(["base"], "validated")
    for row in grid["grid"].values():
        row["broken"] = vce._not_graded_cell(CRASH)
    grid.update(variants=["base", "broken"], failed_variants={"broken": CRASH},
                idea_status="inconclusive", reason="crashed column")
    rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
    rpr.save_yaml(arts / "idea_status.yaml", rpr._build_idea_status_artifact(grid, RUN_ID))
    return run_dir


def test_branch3_failed_column_is_not_tested_even_with_a_stale_passing_result():
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _crashed_column_run(stale_good=True)
    assert (run_dir / "artifacts" / "variants" / "broken" / "protocol_result.yaml").exists()
    cands = rpr._profit_bars_backtest_candidates(run_dir, RUN_ID)
    assert cands["broken"]["result"] == "NOT_TESTED" and CRASH in cands["broken"]["reason"]
    assert cands["base"]["result"] is None  # gradeable
    ev = rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    assert ev["variants"]["broken"]["result"] == "NOT_TESTED" and ev["variants"]["broken"]["bars"] == []
    assert "broken" not in ev["passing"]


def test_branch3_refuses_a_failed_variant_outside_the_columns():
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    run_dir = _crashed_column_run(stale_good=False)
    path = run_dir / "artifacts" / "grid_evaluation.yaml"
    grid = rpr.load_yaml(path)
    grid["failed_variants"] = {"ghost": CRASH}
    rpr.save_yaml(path, grid)
    with pytest.raises(ValueError, match="failed_variants"):
        rpr._profit_bars_backtest_candidates(run_dir, RUN_ID)


def test_memory_marks_the_crashed_column_failed_and_keeps_not_graded():
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _crashed_column_run(stale_good=True)
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    rpr._run_regroup_record_stage(RUN_ID, run_dir, profit_bars_evaluated=True)
    doc = _memory()
    e = doc["runs"][RUN_ID]
    assert e["idea_status"] == "inconclusive"
    assert e["variants"]["broken"]["status"] == "failed"
    assert e["variants"]["broken"]["reason"] == CRASH
    assert e["variants"]["broken"]["trial_id"] == f"{RUN_ID}:broken"  # its backtest_failed row
    assert e["variants"]["base"]["status"] == "tested"
    cell = e["grid"]["cells"]["ic_median"]["broken"]
    assert cell == {"result": "INCONCLUSIVE", "reason": CRASH, "not_graded": True}
    assert e["grid"]["counts"]["INCONCLUSIVE"] == 2
    assert e["profit_bars"]["variants"]["broken"]["result"] == "NOT_TESTED"
    assert e["registry"] == {"skipped": cm.REGISTRY_SKIPPED_NOT_VALIDATED}
    jsonschema.Draft202012Validator(_SCHEMA).validate(doc)
    # the downstream readers of that status: novelty never sees it as tested
    assert [(r, v) for r, v, _e, _v in nov._tested_variants(doc)] == [(RUN_ID, "base")]


def test_decide_next_sees_a_crashed_base_as_not_tested():
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    _write_bars()
    run_dir = _variant_run({"design": True})
    arts = run_dir / "artifacts"
    index = rpr.load_yaml(arts / "variants" / "index.yaml")
    index["variants"]["base"] = {"status": "validated",
                                 "config_path": "artifacts/variants/base/strategy_config.json"}
    rpr.save_yaml(arts / "variants" / "index.yaml", index)
    grid = _grid(["design"], "validated")
    for row in grid["grid"].values():
        row["base"] = vce._not_graded_cell(CRASH)
    grid.update(variants=["design", "base"], failed_variants={"base": CRASH},
                idea_status="inconclusive", reason="crashed base")
    rpr.save_yaml(arts / "grid_evaluation.yaml", grid)
    rpr.save_yaml(arts / "idea_status.yaml", rpr._build_idea_status_artifact(grid, RUN_ID))
    rpr._evaluate_profit_bars_every_backtest(run_dir, RUN_ID)
    rpr._run_regroup_record_stage(RUN_ID, run_dir, profit_bars_evaluated=True)
    e = _memory()["runs"][RUN_ID]
    vid, base = dn._base_variant(e)
    assert vid == "base" and base["status"] == "failed"  # -> source_base_variant_not_tested


@pytest.mark.parametrize("mutate,match", [
    (lambda g: g.update(failed_variants={"ghost": CRASH}), "must be a grid column"),
    (lambda g: g.update(failed_variants=[]), "non-empty mapping"),
    (lambda g: g["grid"]["ic_median"].update(broken={"result": "PASS"}), "not_graded"),
])
def test_memory_refuses_a_corrupt_failed_variants(mutate, match):
    _set_orchestrator({**FULL_ON, **VARIANT_LOOP_ON})
    run_dir = _crashed_column_run(stale_good=False)
    path = run_dir / "artifacts" / "grid_evaluation.yaml"
    grid = rpr.load_yaml(path)
    mutate(grid)
    rpr.save_yaml(path, grid)
    with pytest.raises(cm.CampaignMemoryError, match=match):
        rpr._run_regroup_record_stage(RUN_ID, run_dir)


# ---------------------------------------------------------------------------
# 5. Block registry
# ---------------------------------------------------------------------------

def test_block_registry_refuses_a_validated_entry_with_a_non_tested_column(tmp_path):
    entry = {"run_id": RUN_ID, "hypothesis_id": "H", "legacy": False,
             "idea_status": "validated", "engineering_fault": None,
             "grid": {"criteria": ["c1"], "variants": ["base", "asset"],
                      "cells": {"c1": {"base": {"result": "PASS"},
                                       "asset": {"result": "PASS"}}}},
             "variants": {"base": {"status": "tested"}, "asset": {"status": "failed"}}}
    with pytest.raises(br.BlockRegistryError, match="D-015"):
        br.build_block(tmp_path, copy.deepcopy(entry), {"block": {}}, root=tmp_path)
