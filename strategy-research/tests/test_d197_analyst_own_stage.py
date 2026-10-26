"""D-197 (build window run_101, PR-5): the analyst is a stage of its own.

Before: the analyst's two lenses ran inside the specialist_readers stage and the analyst flag
required specialist_readers and reader_findings. Now: STAGE_CONFIGS["analyst"] sits right after
protocol_execution (before specialist_readers when that stage is on, else before
verdict_interpreter), `orchestrator.analyst` depends on folds only, and the five category names
are a constant (tools/reader_categories.py) instead of an import of the report builder.

Pins:
  1. the constant: the same five names in build_reports.REPORT_CATEGORIES' order, split into the
     analyst's two lens categories and the three legacy ones; no build_reports import;
  2. the loaders (load_proposals, decide_next.load_inputs, campaign_memory, fold_confirm) still
     read an old run's five proposal files;
  3. the flag: no dependency on specialist_readers / reader_findings / category_reports;
  4. the stage: runs with those three off; routes protocol_execution -> analyst -> (specialist_readers
     | verdict_interpreter); skips on component errors; refuses to run with its flag off;
  5. all flags on: the analyst's records are byte-identical to what the in-stage path wrote;
  6. an old pipeline_state (no analyst stage) resumes at specialist_readers and completes.

No API key: the SDK `query` is stubbed the way tests/test_e075_pr5_analyst.py stubs it.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import analyst_session as asm  # noqa: E402
import build_reports as br  # noqa: E402
import campaign_memory as cm  # noqa: E402
import decide_next as dn  # noqa: E402
import fold_confirm as fc  # noqa: E402
import reader_categories as rcat  # noqa: E402
import reader_proposals as rp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

import test_e075_pr4_queries as q4  # noqa: E402  (a synthetic run with bars and trades)
import test_e075_pr5_analyst as t75  # noqa: E402  (the stubbed analyst session)
from _reader_test_helpers import (  # noqa: E402,F401
    ALL_ON, REGROUP_ALL_ON, REGROUP_RUN_ID, RUN_ID, _fake_llm, _protocol_result, _seed, _seed_run,
    _set_orchestrator, _stub_tbot_python)
from d178_legacy_fixture import d178_checks_off  # noqa: E402,F401
from test_e033_slice4b_gate_conformance_promotion import _minimal_run_at, _noop_invoke  # noqa: E402

LENS_ORDER = ["trade_efficiency", "forecast"]            # the order the categories are in
NO_READERS = {"specialist_readers", "reader_findings", "category_reports"}


# ---------------------------------------------------------------------------
# 1. the constant
# ---------------------------------------------------------------------------

def test_the_constant_is_the_report_categories_in_the_same_order():
    assert rcat.READER_CATEGORIES == br.REPORT_CATEGORIES      # while build_reports still exists
    assert list(rcat.READER_CATEGORIES) == ["profitability", "trade_efficiency", "forecast_power",
                                            "regime_power", "component_attribution"]
    assert rpr.READER_CATEGORIES is rcat.READER_CATEGORIES
    assert not hasattr(rpr, "_reader_categories")               # replaced by the constant


def test_the_constant_splits_into_the_two_lens_categories_and_the_three_legacy_names():
    lenses = set(asm.LENS_CATEGORY.values())
    assert set(asm.LENS_CATEGORY) == {"forecast", "trade_efficiency"}
    assert lenses == {"forecast_power", "trade_efficiency"}
    assert rcat.ANALYST_LENS_CATEGORIES == [c for c in rcat.READER_CATEGORIES if c in lenses]
    assert [asm.LENS_CATEGORY[lens] for lens in LENS_ORDER] == rcat.ANALYST_LENS_CATEGORIES
    assert rcat.LEGACY_READER_CATEGORIES == [c for c in rcat.READER_CATEGORIES if c not in lenses]
    assert set(rcat.READER_CATEGORIES) == set(rcat.ANALYST_LENS_CATEGORIES) | \
        set(rcat.LEGACY_READER_CATEGORIES)
    assert set(rp.READER_RUBRIC_VERSIONS) == set(rcat.READER_CATEGORIES)


def test_the_constant_module_does_not_import_the_report_builder():
    src = (SR_ROOT / "tools" / "reader_categories.py").read_text(encoding="utf-8")
    assert "import build_reports" not in src and "from build_reports" not in src


# ---------------------------------------------------------------------------
# 2. the loaders still read an old run's five proposal files
# ---------------------------------------------------------------------------

def test_the_loaders_still_read_an_old_runs_five_proposal_files():
    _set_orchestrator(REGROUP_ALL_ON)
    run_dir = _seed(proposals=1)                  # five v2 reader files, one proposal each
    categories = list(rcat.READER_CATEGORIES)
    pdir = run_dir / "artifacts" / "proposals"
    assert sorted(p.name for p in pdir.glob("*.yaml")) == sorted(f"{c}.yaml" for c in categories)
    loaded = rp.load_proposals(pdir, categories)
    assert {c: len(v) for c, v in loaded.items()} == {c: 1 for c in categories}

    block = cm._proposals_block(run_dir, REGROUP_RUN_ID, categories)
    assert [b["category"] for b in block] == categories and {b["count"] for b in block} == {1}

    rpr._run_regroup_record_stage(REGROUP_RUN_ID, run_dir)
    inputs = dn.load_inputs(rpr.ROOT, {"queue": []}, categories=list(rpr.READER_CATEGORIES))
    items = inputs["runs"][REGROUP_RUN_ID]["proposals"]
    assert [i["category"] for i in items] == categories

    for category in categories:                   # fold_confirm: a proposal of any of the five
        pid = f"{category}-{REGROUP_RUN_ID}-1"
        found = fc.source_item(rpr.ROOT, (REGROUP_RUN_ID, category, pid))
        assert found is not None and found["proposal_id"] == pid


# ---------------------------------------------------------------------------
# 3. the flag
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("on", [{"folds"}, {"folds", "specialist_readers"},
                                {"folds", "reader_findings", "category_reports"}])
def test_the_flag_needs_folds_only(monkeypatch, on):
    for name in ("folds", "specialist_readers", "reader_findings", "category_reports",
                 "explore_confirm"):
        monkeypatch.setattr(rpr, f"_{name}_enabled", lambda cfg=None, n=name: n in on)
    assert t75._REAL_ANALYST_ENABLED({"orchestrator": {"analyst": {"enabled": True}}}) is True


def test_the_real_config_flag_reads_with_the_three_off(tmp_path):
    cfg = {"orchestrator": {"folds": {"enabled": True}, "analyst": {"enabled": True},
                            "specialist_readers": {"enabled": False},
                            "reader_findings": {"enabled": False},
                            "category_reports": {"enabled": False}}}
    assert t75._REAL_ANALYST_ENABLED(cfg) is True
    with pytest.raises(ValueError, match="requires orchestrator.folds.enabled=true"):
        t75._REAL_ANALYST_ENABLED({"orchestrator": {"analyst": {"enabled": True}}})


def test_the_registered_flag_and_the_stage():
    assert rpr.STAGE_CONFIGS["analyst"] == {"handoff": "protocol_to_analyst.yaml",
                                            "default_next": "dynamic_routing"}
    assert "analyst" not in rpr._SKILL_MAP
    assert "analyst" in vce._NON_VERDICT_OUTCOMES
    # the specialist_readers entry and the flag-off route are untouched
    assert rpr.STAGE_CONFIGS["specialist_readers"]["handoff"] == "protocol_to_specialist_readers.yaml"
    assert rpr.STAGE_CONFIGS["protocol_execution"]["default_next"] == "verdict_interpreter"
    register = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml")
                              .read_text(encoding="utf-8"))
    (entry,) = [f for f in register["flags"] if f["name"] == "analyst"]
    assert entry["config_key"] == "orchestrator.analyst.enabled"
    assert "Also requires specialist_readers" not in entry["criterion"]


# ---------------------------------------------------------------------------
# helpers for the stage tests
# ---------------------------------------------------------------------------

def _fake_worker(called):
    def worker(lens, run_id, run_dir, stage_attempt=0):
        called.append(lens)
        rpr._write_skipped_reading(asm.LENS_CATEGORY[lens], run_id, run_dir,
                                   {"rule": "output_refused_after_retry", "reason": "stub"})
    return worker


def _loop_run(pending, **seed_kw):
    """A run at `pending` with the files the loop reads at protocol_execution."""
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, pending)
    rpr.save_yaml(run_dir / "handoffs" / "backtest_spec_to_protocol_execution.yaml",
                  {"required_inputs": [], "deliverables": []})
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", _protocol_result())
    return run_dir


def _state(run_dir):
    return rpr.load_yaml(run_dir / "pipeline_state.yaml")


def _proposal_names(run_dir):
    return sorted(p.stem for p in (run_dir / "artifacts" / "proposals").glob("*.yaml"))


# ---------------------------------------------------------------------------
# 4. the stage: with the three flags off, and in the order
# ---------------------------------------------------------------------------

def test_the_analyst_stage_runs_with_the_three_flags_off(monkeypatch):
    """protocol_execution -> analyst -> verdict_interpreter, nothing of the readers touched."""
    _set_orchestrator(None)
    for name in NO_READERS:
        assert getattr(rpr, f"_{name}_enabled")() is False
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    run_dir = _loop_run("protocol_execution")
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    called = []
    monkeypatch.setattr(rpr, "run_analyst_worker", _fake_worker(called))
    monkeypatch.setattr(rpr, "run_reader_worker", lambda *a, **k: pytest.fail("a reader ran"))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=[]))
    # stop at verdict_interpreter without running it: its handoff is absent
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "verdict_interpreter",
                        {**rpr.STAGE_CONFIGS["verdict_interpreter"], "handoff": "missing.yaml"})
    with pytest.raises(FileNotFoundError):
        rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert called == LENS_ORDER
    assert state["completed_stages"][-2:] == ["protocol_execution", "analyst"]
    assert state["pending_stage"] == "verdict_interpreter"
    assert _proposal_names(run_dir) == sorted(rcat.ANALYST_LENS_CATEGORIES)   # the lenses' only
    assert (run_dir / "handoffs" / "protocol_to_analyst.yaml").exists()
    assert not (run_dir / "handoffs" / "protocol_to_specialist_readers.yaml").exists()


def test_with_every_flag_on_the_order_is_analyst_then_the_readers_stage(monkeypatch):
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    _seed_run(pending="protocol_execution", idea_status="refuted")
    rpr.save_yaml(run_dir / "handoffs" / "backtest_spec_to_protocol_execution.yaml",
                  {"required_inputs": [], "deliverables": []})
    stages = []

    async def _record(stage_name, run_id, retry_context=None):
        stages.append(stage_name)
    monkeypatch.setattr(rpr, "async_invoke_agent", _record)
    called, reader_calls = [], []
    monkeypatch.setattr(rpr, "run_analyst_worker", _fake_worker(called))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=reader_calls))
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert stages == ["protocol_execution"]
    assert called == LENS_ORDER and reader_calls == []     # no reader call: the analyst replaces them
    assert state["completed_stages"][-3:] == ["protocol_execution", "analyst", "specialist_readers"]
    assert state["pending_stage"] == "completed_rejected"
    assert _proposal_names(run_dir) == sorted(rcat.READER_CATEGORIES)
    for category in rcat.LEGACY_READER_CATEGORIES:             # the three code-skipped readings
        doc = yaml.safe_load((run_dir / "artifacts" / "proposals" / f"{category}.yaml")
                             .read_text(encoding="utf-8"))
        assert doc["skipped"]["rule"] == asm.REPLACED_RULE


def test_the_analyst_stage_skips_a_run_with_component_errors(monkeypatch):
    _set_orchestrator(None)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    run_dir = _loop_run("analyst")
    rpr.save_yaml(run_dir / "artifacts" / "protocol_result.yaml", _protocol_result(errors_count=2))
    called = []
    monkeypatch.setattr(rpr, "run_analyst_worker", _fake_worker(called))
    rpr._run_analyst_stage(RUN_ID, run_dir)
    assert called == [] and not (run_dir / "artifacts" / "proposals").exists()


def test_a_run_waiting_at_the_analyst_stage_with_its_flag_off_stops_loudly(monkeypatch):
    _set_orchestrator(None)
    run_dir = _loop_run("analyst")
    monkeypatch.setattr(rpr, "run_analyst_worker", lambda *a, **k: pytest.fail("analyst ran"))
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["status"] == "failed" and "analyst is unreached" in state["last_error"]
    assert state["pending_stage"] == "analyst"


def test_the_stage_refuses_to_run_with_its_flag_off(monkeypatch):
    _set_orchestrator(None)
    run_dir = _loop_run("analyst")
    with pytest.raises(RuntimeError, match="analyst reached with orchestrator.analyst.enabled off"):
        rpr._run_analyst_stage(RUN_ID, run_dir)


def test_a_valid_lens_file_already_present_is_not_rerun(monkeypatch):
    _set_orchestrator(None)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    run_dir = _loop_run("analyst")
    rpr._write_skipped_reading("trade_efficiency", RUN_ID, run_dir,
                               {"rule": "output_refused_after_retry", "reason": "stub"})
    called = []
    monkeypatch.setattr(rpr, "run_analyst_worker", _fake_worker(called))
    rpr._run_analyst_stage(RUN_ID, run_dir)
    assert called == ["forecast"]
    assert _proposal_names(run_dir) == sorted(rcat.ANALYST_LENS_CATEGORIES)


def test_an_operator_rerun_gets_the_code_written_reading_for_each_lens(monkeypatch):
    _set_orchestrator(None)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    run_dir = _loop_run("analyst")
    monkeypatch.setattr(rpr, "_refold_readers_off",
                        lambda rd: {"rule": rpr._reader_findings_module().SKIP_OPERATOR_REFOLD,
                                    "reason": "operator re-run"})
    monkeypatch.setattr(rpr, "run_analyst_worker", lambda *a, **k: pytest.fail("analyst ran"))
    rpr._run_analyst_stage(RUN_ID, run_dir)
    for category in rcat.ANALYST_LENS_CATEGORIES:
        doc = yaml.safe_load((run_dir / "artifacts" / "proposals" / f"{category}.yaml")
                             .read_text(encoding="utf-8"))
        assert doc["skipped"]["rule"] == rpr._reader_findings_module().SKIP_OPERATOR_REFOLD


def test_protocol_execution_clears_the_analysts_attempt_when_only_its_flag_is_on(tmp_path):
    arts = tmp_path / "artifacts"
    for rel in ("analyst/forecast.yaml", "analyst_queries/forecast.yaml",
                "proposals/forecast_power.yaml", "proposals/trade_efficiency.yaml",
                "proposals/profitability.yaml"):
        (arts / rel).parent.mkdir(parents=True, exist_ok=True)
        (arts / rel).write_text("x: 1\n", encoding="utf-8")
    rpr._clear_analyst_artifacts(tmp_path)
    assert not (arts / "analyst").exists() and not (arts / "analyst_queries").exists()
    assert sorted(p.name for p in (arts / "proposals").iterdir()) == ["profitability.yaml"]


# ---------------------------------------------------------------------------
# 5. all flags on: the analyst's records are the ones the in-stage path wrote
# ---------------------------------------------------------------------------

@pytest.fixture()
def lens_run(tmp_path, monkeypatch, d178_checks_off):
    """tests/test_e075_pr5_analyst.py's `run` fixture and flags (analyst and folds on, score
    provenance off), plus the protocol_result.yaml the stage's component-error check reads."""
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_folds_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_score_provenance_enabled", lambda *a: False)
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))
    root = tmp_path / "root"
    run_dir = q4.make_run(root / "runs" / t75.RUN_ID)
    arts = run_dir / "artifacts"
    (arts / "pre_registration.yaml").write_text(
        yaml.safe_dump({"machine_constraints": {"protocol": {"fold": "A"}}}), encoding="utf-8")
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump({"status": "active", "audit_log": {}}), encoding="utf-8")
    (arts / "candidate_strategy_config.json").write_text(json.dumps(t75.BASE_CONFIG),
                                                         encoding="utf-8")
    (arts / "protocol_result.yaml").write_text(yaml.safe_dump({"results": []}), encoding="utf-8")
    monkeypatch.setattr(rpr, "ROOT", root)
    monkeypatch.setattr(rpr, "_load_holdout_range", lambda *a: (q4.HOLDOUT, None))
    monkeypatch.setattr(asm, "SR_ROOT", SR_ROOT)
    return run_dir


def _tree(run_dir):
    """{relative path: bytes} of every record the analyst (and the readers stage) writes."""
    arts = run_dir / "artifacts"
    return {p.relative_to(arts).as_posix(): p.read_bytes().replace(b"\r\n", b"\n")
            for sub in ("proposals", "analyst", "analyst_queries")
            for p in sorted((arts / sub).glob("*.yaml"))}


def test_the_analysts_records_are_byte_identical_to_the_in_stage_path(lens_run, tmp_path,
                                                                      monkeypatch):
    _set_orchestrator(None)
    t75._install(monkeypatch, t75._good_claim)
    monkeypatch.setattr(rpr, "_reader_findings_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "run_reader_worker", lambda *a, **k: pytest.fail("a reader ran"))
    other = tmp_path / "other" / t75.RUN_ID                  # the same run, an untouched copy
    shutil.copytree(lens_run, other)

    # before D-197: the lenses ran inside the readers stage's loop (still its fallback path)
    rpr._run_specialist_readers(t75.RUN_ID, lens_run)
    old = _tree(lens_run)
    # now: the analyst stage first, then the readers stage over the same directory
    rpr._run_analyst_stage(t75.RUN_ID, other)
    after_stage = _tree(other)
    rpr._run_specialist_readers(t75.RUN_ID, other)
    new = _tree(other)

    assert sorted(old) == sorted(new)
    assert {"analyst/forecast.yaml", "analyst/trade_efficiency.yaml",
            "proposals/forecast_power.yaml", "proposals/trade_efficiency.yaml",
            "analyst_queries/forecast.yaml", "analyst_queries/trade_efficiency.yaml"} <= set(new)
    for rel in old:
        assert old[rel] == new[rel], rel
    # the analyst stage alone wrote the lenses' files and nothing of the other three categories
    assert sorted(p for p in after_stage if p.startswith("proposals/")) == [
        "proposals/forecast_power.yaml", "proposals/trade_efficiency.yaml"]
    for run in (lens_run, other):
        audit = yaml.safe_load((run / "pipeline_state.yaml").read_text(encoding="utf-8"))["audit_log"]
        assert sorted(audit) == ["specialist_readers_analyst_forecast_attempt_0",
                                 "specialist_readers_analyst_trade_efficiency_attempt_0"]


def test_the_analyst_stage_writes_its_readings_with_the_three_flags_off(lens_run, monkeypatch):
    """The real worker over a stubbed session, no readers-stage flag set."""
    _set_orchestrator(None)
    for name in NO_READERS:
        assert getattr(rpr, f"_{name}_enabled")() is False
    t75._install(monkeypatch, t75._good_claim)
    monkeypatch.setattr(rpr, "run_reader_worker", lambda *a, **k: pytest.fail("a reader ran"))
    rpr._run_analyst_stage(t75.RUN_ID, lens_run)
    tree = _tree(lens_run)
    assert sorted(p for p in tree if p.startswith("proposals/")) == [
        "proposals/forecast_power.yaml", "proposals/trade_efficiency.yaml"]
    record = yaml.safe_load(tree["analyst/trade_efficiency.yaml"])
    assert record["lens"] == "trade_efficiency" and record["category"] == "trade_efficiency"
    assert record["attempts"][-1]["status"] == "accepted"
    assert not (lens_run / "artifacts" / "registry_summary.yaml").exists()  # no readers-stage prelude


# ---------------------------------------------------------------------------
# 6. an old pipeline_state resumes
# ---------------------------------------------------------------------------

def test_an_old_pipeline_state_without_the_analyst_stage_resumes_and_completes(monkeypatch):
    """A run paused inside specialist_readers before D-197 has completed_stages without
    `analyst` and no lens file: the readers stage runs the lenses itself (its fallback), the
    run completes, and `analyst` never appears in its completed stages."""
    _set_orchestrator(ALL_ON)
    monkeypatch.chdir(SR_ROOT)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    run_dir = _seed_run(pending="specialist_readers", idea_status="refuted")
    state = _state(run_dir)
    state["completed_stages"] = ["hypothesis_generation", "protocol_execution"]
    rpr.save_yaml(run_dir / "pipeline_state.yaml", state)
    assert "analyst" not in state["completed_stages"]
    called, reader_calls = [], []
    monkeypatch.setattr(rpr, "run_analyst_worker", _fake_worker(called))
    monkeypatch.setattr(rpr, "_invoke_reader_llm", _fake_llm(calls=reader_calls))
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert sorted(called) == sorted(LENS_ORDER) and reader_calls == []
    assert state["completed_stages"][-1] == "specialist_readers"
    assert "analyst" not in state["completed_stages"]
    assert state["pending_stage"] == "completed_rejected"
    assert _proposal_names(run_dir) == sorted(rcat.READER_CATEGORIES)


def test_an_old_state_paused_after_the_readers_stage_is_untouched(monkeypatch):
    """pending_stage regroup_record (the next stage after specialist_readers): the analyst flag
    plays no part in it."""
    _set_orchestrator(REGROUP_ALL_ON)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    run_dir = _seed(pending="regroup_record")
    monkeypatch.setattr(rpr, "run_analyst_worker", lambda *a, **k: pytest.fail("analyst ran"))
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "holdout_evaluation",
                        {**rpr.STAGE_CONFIGS["holdout_evaluation"], "handoff": "missing.yaml"})
    rpr.run_loop(REGROUP_RUN_ID)
    state = _state(run_dir)
    assert state["completed_stages"][-1] == "regroup_record"
    assert "analyst" not in state["completed_stages"]
