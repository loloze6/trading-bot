"""
CUL-380: a malformed reader proposal is dropped and recorded; the run goes on.

run_065 (C4 on Kraken, 2026-10-02) was the first new-pipeline run to reach the
specialist readers. The regime_power reader proposed a new_block whose block
was {kind, config_paths} -- no `rationale`. One retry fixed a first error and
tripped on the next, and the run halted after its backtests, grid and reports,
before regroup_record could record the grid's verdict.

`rationale` stays required: when decide-next picks a new_block, the rationale
becomes the next idea's research goal. What changes: such a proposal is
dropped (recorded in the audit log, raw answer kept) instead of stopping the
run; every reader prompt states the new_block shape; every refusal quotes it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))

import reader_proposals  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
from test_e046a_slice5b_ii_b_readers_stage import ALL_ON, RUN_ID, _fake_llm, _seed_run  # noqa: E402
from test_c5_7b1_model_id_stamp import _set_orchestrator  # noqa: E402

RUN_065 = (Path(__file__).parent / "fixtures" / "run_065_regime_power_reader_no_rationale.txt"
           ).read_text(encoding="utf-8")
CATEGORIES = ("profitability", "trade_efficiency", "forecast_power", "regime_power",
              "component_attribution")


def test_run_065s_answer_is_dropped_with_its_reason_and_the_run_goes_on(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm({"regime_power": RUN_065}, calls))
    result = rpr._run_specialist_readers(RUN_ID, run_dir)  # no raise
    assert result["regime_power"] == []
    assert len([c for c, _ in calls if c == "regime_power"]) == 2
    audit = rpr.load_yaml(run_dir / "pipeline_state.yaml")["audit_log"]
    [drop] = audit["specialist_readers_regime_power_attempt_0_retry1"]["dropped_proposals"]
    assert "rationale" in drop["error"]
    assert (run_dir / "artifacts" / "debug_specialist_readers_regime_power_raw_output.txt").exists()


def test_the_retry_prompt_carries_the_whole_block_shape(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    run_dir = _seed_run()
    calls = []
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm({"regime_power": RUN_065}, calls))
    rpr._run_specialist_readers(RUN_ID, run_dir)
    retry_prompt = [p for c, p in calls if c == "regime_power"][1]
    assert reader_proposals.NEW_BLOCK_SHAPE in retry_prompt


@pytest.mark.parametrize("block", [
    {"kind": "forecast", "config_paths": ["/a"]},                          # no rationale
    {"kind": "other", "config_paths": ["/a"], "rationale": "r"},          # bad kind
    {"kind": "forecast", "config_paths": [], "rationale": "r"},           # empty paths
])
def test_every_new_block_refusal_states_the_whole_shape(tmp_path, block):
    item = {"proposal_id": "regime_power-run_1-1", "kind": "new_block", "block": block,
            "evidence": ["x"], "scores": {"confidence_real": 1, "distance_to_profitable": 1,
                                          "mechanism_plausibility": 1},
            "model_id": "m", "rubric_version": "regime_power-reader-v2"}
    (tmp_path / "regime_power.yaml").write_text(yaml.safe_dump([item]), encoding="utf-8")
    with pytest.raises(reader_proposals.ProposalError) as exc:
        reader_proposals.load_proposals(tmp_path, ["regime_power"])
    assert reader_proposals.NEW_BLOCK_SHAPE in str(exc.value)


@pytest.mark.parametrize("category", CATEGORIES)
def test_every_reader_prompt_states_the_new_block_shape(category):
    text = (SR_ROOT / "workflow_artifacts" / "skills" / "readers" / f"{category}-reader" /
            "SKILL.md").read_text(encoding="utf-8")
    assert "New-block shape (required, CUL-380)" in text
    for key in ("kind: forecast|regime", "config_paths", "scaffolding", "rationale"):
        assert key in text
