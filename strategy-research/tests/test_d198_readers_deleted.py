"""D-198 (build window run_101, PR-6): the five readers are deleted.

Pins:
  1. nothing imports the deleted report builder (tools/build_reports.py), and the module is gone;
  2. the five flags (category_reports, specialist_readers, reader_findings, observable_backtest,
     explore_confirm) are absent from config/campaign_config.yaml and the flag register, and from
     the launch pre-flight's flag table;
  3. the stage list has no specialist_readers, and the reader-only functions are gone;
  4. a pipeline_state.yaml pending at the deleted stage resumes into the next live stage;
  5. artifacts/registry_summary.yaml is still written (by regroup_record);
  6. an old run's five proposal files still load (load_proposals, decide_next.load_inputs,
     campaign_memory, fold_confirm);
  7. a leftover `orchestrator.<removed flag>` key in a config does not crash flag reading;
  8. the dependencies that named specialist_readers now name grid_evaluation.

No LLM, no backtest.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import campaign_memory as cm  # noqa: E402
import decide_next as dn  # noqa: E402
import fold_confirm as fc  # noqa: E402
import reader_categories as rcat  # noqa: E402
import reader_proposals as rp  # noqa: E402
import run_campaign as camp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402

from _reader_test_helpers import (  # noqa: E402,F401
    REGROUP_ALL_ON, REGROUP_RUN_ID, _fake_llm, _memory, _seed, _set_orchestrator,
    _stub_tbot_python)

REMOVED_FLAGS = ("category_reports", "specialist_readers", "reader_findings",
                 "observable_backtest", "explore_confirm")
THIS_FILE = Path(__file__).name


# ---------------------------------------------------------------------------
# 1. no build_reports
# ---------------------------------------------------------------------------

def test_the_report_builder_is_gone_and_nothing_imports_it():
    assert not (SR_ROOT / "tools" / "build_reports.py").exists()
    pattern = re.compile(r"^\s*(?:import build_reports\b|from build_reports\b)", re.M)
    offenders = []
    for sub in ("tools", "workflow", "tests", "engineering"):
        for path in (SR_ROOT / sub).rglob("*.py"):
            if path.name == THIS_FILE or "__pycache__" in path.parts:
                continue
            if pattern.search(path.read_text(encoding="utf-8", errors="replace")):
                offenders.append(path.relative_to(SR_ROOT).as_posix())
    assert offenders == []
    with pytest.raises(ModuleNotFoundError):
        __import__("build_reports")


def test_the_reader_skills_schema_and_generated_dictionary_are_gone():
    skills = SR_ROOT / "workflow_artifacts" / "skills"
    assert not (skills / "readers").exists() and not (skills / "readers_v3").exists()
    assert not (SR_ROOT / "workflow_artifacts" / "schemas" / "proposal.schema.json").exists()
    assert not (SR_ROOT / "docs" / "DATA_DICTIONARY_READERS.md").exists()
    assert not (SR_ROOT / "tools" / "data_dictionary.py").exists()
    assert not (SR_ROOT / "campaign_record" / "reader_skips.yaml").exists()


# ---------------------------------------------------------------------------
# 2. the flags
# ---------------------------------------------------------------------------

def test_the_removed_flags_are_absent_from_config_register_and_preflight_table():
    config = yaml.safe_load((SR_ROOT / "config" / "campaign_config.yaml").read_text(encoding="utf-8"))
    for name in REMOVED_FLAGS:
        assert name not in config["orchestrator"], name
    register = yaml.safe_load((SR_ROOT / "config" / "feature_flag_register.yaml")
                              .read_text(encoding="utf-8"))
    registered = {f["name"] for f in register["flags"]}
    assert not registered & set(REMOVED_FLAGS)
    keys = {f.get("config_key") for f in register["flags"]}
    assert not any(f"orchestrator.{n}.enabled" in keys for n in REMOVED_FLAGS)
    assert not set(REMOVED_FLAGS) & set(camp._flag_readers())
    for fn in ("_category_reports_enabled", "_specialist_readers_enabled", "_reader_findings_enabled",
               "_observable_backtest_enabled", "_explore_confirm_enabled"):
        assert not hasattr(rpr, fn), fn


def test_the_flagset_preflight_script_no_longer_expects_the_removed_flags():
    src = (SR_ROOT / "engineering" / "flagset_daily_breadth" / "preflight_check.py").read_text(
        encoding="utf-8")
    for name in REMOVED_FLAGS:
        assert f'"{name}"' not in src, name


# ---------------------------------------------------------------------------
# 3. the stage list and the reader-only functions
# ---------------------------------------------------------------------------

def test_the_stage_list_has_no_specialist_readers():
    assert "specialist_readers" not in rpr.STAGE_CONFIGS
    assert {"analyst", "regroup_record", "verdict_interpreter"} <= set(rpr.STAGE_CONFIGS)
    for name in ("_run_specialist_readers", "_run_specialist_readers_stage", "run_reader_worker",
                 "_reader_handoff", "_reader_handoff_v3", "_stamp_reader_body",
                 "_citation_provenance", "_route_reader_feed_requests",
                 "_write_reader_v3_inputs", "_record_reader_skips", "_prepare_explore_confirm",
                 "_record_confirmations", "_with_data_dictionary"):
        assert not hasattr(rpr, name), name
    # kept: the analyst's checks, the budget check, the route and the merge functions
    for name in ("run_analyst_worker", "_check_reader_budget", "_reader_strictness",
                 "determine_post_specialist_readers_route", "_record_side_finding_merges",
                 "_write_registry_summary", "_write_skipped_reading", "_reading_content_errors"):
        assert hasattr(rpr, name), name


# ---------------------------------------------------------------------------
# 4. an old state pending at the deleted stage resumes
# ---------------------------------------------------------------------------

def _stop_before_holdout(monkeypatch):
    monkeypatch.setitem(rpr.STAGE_CONFIGS, "holdout_evaluation",
                        {**rpr.STAGE_CONFIGS["holdout_evaluation"], "handoff": "missing.yaml"})


def _state(run_dir):
    return rpr.load_yaml(run_dir / "pipeline_state.yaml")


def test_the_resume_mapping_is_analyst_then_regroup_record_then_the_route(tmp_path):
    run_dir = tmp_path / "run"
    proposals = run_dir / "artifacts" / "proposals"
    f = rpr._resume_stage_after_readers_deleted
    assert f(run_dir, True, True) == "analyst"            # a lens reading is missing
    assert f(run_dir, False, True) == "regroup_record"
    assert f(run_dir, False, False) is None               # straight to the route
    assert f(run_dir, True, False) == "analyst"
    proposals.mkdir(parents=True)
    for c in rcat.ANALYST_LENS_CATEGORIES:
        (proposals / f"{c}.yaml").write_text("x: 1\n", encoding="utf-8")
    assert f(run_dir, True, True) == "regroup_record"     # both lens files present
    assert f(run_dir, True, False) is None


def test_a_state_pending_at_the_deleted_stage_resumes_into_regroup_record(monkeypatch):
    _set_orchestrator(REGROUP_ALL_ON)
    run_dir = _seed(idea_status="refuted", pending="specialist_readers")
    _stop_before_holdout(monkeypatch)
    monkeypatch.setattr(rpr, "_invoke_reader_llm", lambda *a, **k: pytest.fail("a model call"))
    rpr.run_loop(REGROUP_RUN_ID)
    state = _state(run_dir)
    assert state["completed_stages"][-1] == "regroup_record"
    assert "specialist_readers" not in state["completed_stages"]
    assert state["pending_stage"] == "completed_rejected"
    assert REGROUP_RUN_ID in _memory()["runs"]


def test_a_state_pending_at_the_deleted_stage_runs_the_analyst_when_a_lens_is_missing(monkeypatch):
    _set_orchestrator(REGROUP_ALL_ON)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    run_dir = _seed(idea_status="refuted", pending="specialist_readers")
    for c in rcat.ANALYST_LENS_CATEGORIES:                # an old state: the lenses never ran
        (run_dir / "artifacts" / "proposals" / f"{c}.yaml").unlink()
    _stop_before_holdout(monkeypatch)
    called = []

    def worker(lens, run_id, run_dir_, stage_attempt=0):
        called.append(lens)
        rpr._write_skipped_reading(rpr._analyst_session_module().LENS_CATEGORY[lens], run_id,
                                   run_dir_, {"rule": "output_refused_after_retry", "reason": "stub"})
    monkeypatch.setattr(rpr, "run_analyst_worker", worker)
    rpr.run_loop(REGROUP_RUN_ID)
    state = _state(run_dir)
    assert sorted(called) == ["forecast", "trade_efficiency"]
    assert state["completed_stages"][-2:] == ["analyst", "regroup_record"]
    assert "specialist_readers" not in state["completed_stages"]
    assert state["pending_stage"] == "completed_rejected"


def test_a_state_pending_at_the_deleted_stage_goes_to_the_route_with_regroup_record_off(monkeypatch):
    _set_orchestrator({"grid_evaluation": {"enabled": True}})
    run_dir = _seed(idea_status="refuted", pending="specialist_readers")
    _stop_before_holdout(monkeypatch)
    seen = []
    real = rpr.determine_post_specialist_readers_route
    monkeypatch.setattr(rpr, "determine_post_specialist_readers_route",
                        lambda *a, **k: (seen.append(a[1]), real(*a, **k))[1])
    rpr.run_loop(REGROUP_RUN_ID)
    assert seen == [REGROUP_RUN_ID]
    state = _state(run_dir)
    assert state["pending_stage"] == "completed_rejected"
    assert "specialist_readers" not in state.get("completed_stages", [])


def test_with_regroup_record_off_and_no_analyst_the_route_is_taken_after_protocol_execution(monkeypatch):
    """The deleted stage's job in the order: nothing between the backtest and the route."""
    _set_orchestrator({"grid_evaluation": {"enabled": True}})
    monkeypatch.chdir(SR_ROOT)
    from test_e033_slice4b_gate_conformance_promotion import _minimal_run_at, _noop_invoke
    from _reader_test_helpers import RUN_ID, _seed_run
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    _seed_run(pending="protocol_execution", idea_status="refuted")
    rpr.save_yaml(run_dir / "handoffs" / "backtest_spec_to_protocol_execution.yaml",
                  {"required_inputs": [], "deliverables": []})
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["completed_stages"][-1] == "protocol_execution"
    assert state["pending_stage"] == "completed_rejected"


def test_a_pause_right_after_the_backtest_resumes_into_the_route_not_the_backtest(monkeypatch):
    """regroup_record off, analyst off, an inconclusive grid: the route pauses in the iteration
    of protocol_execution; pending_stage then names the deleted stage, which a resume maps to
    the route (a re-run of protocol_execution would spend a second backtest)."""
    _set_orchestrator({"grid_evaluation": {"enabled": True}})
    monkeypatch.chdir(SR_ROOT)
    from test_e033_slice4b_gate_conformance_promotion import _minimal_run_at, _noop_invoke
    from _reader_test_helpers import RUN_ID, _seed_run
    run_dir = _minimal_run_at(rpr.ROOT, RUN_ID, "protocol_execution")
    _seed_run(pending="protocol_execution", idea_status="inconclusive")
    rpr.save_yaml(run_dir / "handoffs" / "backtest_spec_to_protocol_execution.yaml",
                  {"required_inputs": [], "deliverables": []})
    monkeypatch.setattr(rpr, "async_invoke_agent", _noop_invoke)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["status"] == "paused_for_human"
    assert state["flags"] == {"inconclusive_grid": True}
    assert state["pending_stage"] == rpr.LEGACY_READERS_STAGE
    assert rpr._resume_stage_after_readers_deleted(run_dir, False, False) is None


# ---------------------------------------------------------------------------
# 5. registry_summary.yaml is still written
# ---------------------------------------------------------------------------

def test_regroup_record_writes_the_registry_summary_before_it_registers_the_run():
    _set_orchestrator(REGROUP_ALL_ON)
    run_dir = _seed(idea_status="refuted", pending="regroup_record")
    path = run_dir / "artifacts" / "registry_summary.yaml"
    assert not path.exists()
    rpr._run_regroup_record_stage(REGROUP_RUN_ID, run_dir)
    summary = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert summary["run_id"] == REGROUP_RUN_ID
    assert summary["this_run"]["idea_status"] == "refuted"
    assert summary["registry"]["n_blocks"] == 0        # written before this run's own block


def test_a_component_error_run_writes_no_registry_summary():
    _set_orchestrator(REGROUP_ALL_ON)
    run_dir = _seed(idea_status="refuted", errors_count=2, pending="regroup_record")
    rpr._run_regroup_record_stage(REGROUP_RUN_ID, run_dir)
    assert not (run_dir / "artifacts" / "registry_summary.yaml").exists()


def test_the_deleted_readers_stage_no_longer_writes_it():
    src = Path(rpr.__file__).read_text(encoding="utf-8")
    assert len(re.findall(r"_write_registry_summary\(", src)) == 2     # the def and the one call


# ---------------------------------------------------------------------------
# 6. an old run's five proposal files still load
# ---------------------------------------------------------------------------

def test_an_old_runs_five_proposal_files_still_load_everywhere():
    _set_orchestrator(REGROUP_ALL_ON)
    run_dir = _seed(proposals=1)                  # five v2 reader files, one proposal each
    categories = list(rcat.READER_CATEGORIES)
    pdir = run_dir / "artifacts" / "proposals"
    loaded = rp.load_proposals(pdir, categories)
    assert {c: len(v) for c, v in loaded.items()} == {c: 1 for c in categories}
    block = cm._proposals_block(run_dir, REGROUP_RUN_ID, categories)
    assert [b["category"] for b in block] == categories
    rpr._run_regroup_record_stage(REGROUP_RUN_ID, run_dir)
    inputs = dn.load_inputs(rpr.ROOT, {"queue": []}, categories=list(rpr.READER_CATEGORIES))
    assert [i["category"] for i in inputs["runs"][REGROUP_RUN_ID]["proposals"]] == categories
    for category in categories:
        pid = f"{category}-{REGROUP_RUN_ID}-1"
        found = fc.source_item(rpr.ROOT, (REGROUP_RUN_ID, category, pid))
        assert found is not None and found["proposal_id"] == pid


def test_an_old_runs_skipped_v3_readings_still_load():
    """The three legacy categories' files of a D-092..D-197 run are code-written `skipped` readings."""
    import reader_findings as rf
    _set_orchestrator(REGROUP_ALL_ON)
    run_dir = _seed(proposals=1)
    pdir = run_dir / "artifacts" / "proposals"
    for category in rcat.LEGACY_READER_CATEGORIES:
        rpr._write_skipped_reading(category, REGROUP_RUN_ID, run_dir,
                                   {"rule": rf.SKIP_REPLACED_BY_ANALYST, "reason": "replaced"})
    loaded = rp.load_proposals(pdir, list(rcat.READER_CATEGORIES))
    for category in rcat.LEGACY_READER_CATEGORIES:
        assert loaded[category] == []
    assert set(rp.load_readings(pdir, list(rcat.READER_CATEGORIES))) == set(rcat.LEGACY_READER_CATEGORIES)


# ---------------------------------------------------------------------------
# 7. a leftover removed-flag key does not crash flag reading
# ---------------------------------------------------------------------------

LEFTOVERS = {name: {"enabled": True} for name in REMOVED_FLAGS}


def test_a_leftover_removed_flag_key_is_ignored_by_every_reader():
    config = {"orchestrator": {**LEFTOVERS, "grid_evaluation": {"enabled": True},
                               "regroup_record": {"enabled": True},
                               "score_provenance": {"enabled": True},
                               "folds": {"enabled": True}, "analyst": {"enabled": True}}}
    assert rpr._grid_route_enabled(config) is True
    assert rpr._regroup_record_enabled(config) is True
    assert rpr._score_provenance_enabled(config) is True
    assert rpr._analyst_enabled(config) is True
    _set_orchestrator(config["orchestrator"])
    values, refusal = camp._flag_preflight()
    assert refusal is None
    assert not set(REMOVED_FLAGS) & set(values)
    assert values["regroup_record"] is True and values["analyst"] is True


def test_a_leftover_key_must_still_be_a_real_boolean():
    """Documented, not weakened: the pre-flight's type check also covers a flag no reader owns."""
    _set_orchestrator({"specialist_readers": {"enabled": "yes"}})
    values, refusal = camp._flag_preflight()
    assert refusal is not None and "specialist_readers" in refusal


# ---------------------------------------------------------------------------
# 8. the dependencies
# ---------------------------------------------------------------------------

def test_regroup_record_needs_the_grid_not_the_deleted_flag():
    with pytest.raises(ValueError, match="orchestrator.grid_evaluation.enabled=true"):
        rpr._regroup_record_enabled({"orchestrator": {"regroup_record": {"enabled": True}}})
    assert rpr._regroup_record_enabled(
        {"orchestrator": {"regroup_record": {"enabled": True},
                          "grid_evaluation": {"enabled": True}}}) is True


def test_score_provenance_has_no_dependency_left():
    assert rpr._score_provenance_enabled({"orchestrator": {"score_provenance": {"enabled": True}}}) is True


def test_the_analyst_no_longer_refuses_explore_confirm():
    cfg = {"orchestrator": {"folds": {"enabled": True}, "analyst": {"enabled": True},
                            "explore_confirm": {"enabled": True}}}
    assert rpr._analyst_enabled(cfg) is True
