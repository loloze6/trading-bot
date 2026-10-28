"""D-202 -- `run_campaign.py retry-analyst --run <run_id>`: the analyst's second pass on a
finished run, after the operator rejected its first reading by hand.

Pins:
  1. the command: archives the analyst's artifacts to artifacts/retry_<n>/ (copies), clears the
     live ones the stage would validate instead of re-run, puts the run back at pending_stage
     `analyst` (status active, last_error cleared) and its entry at `in_progress` with a note,
     logs RETRY-ANALYST; <n> = 1 + the retry folders already there;
  2. its refusals (each changes nothing): entry not done, run not completed, a refold, no
     proposals/, a flag off, over budget, an unknown run, the campaign lock held;
  3. the proposal ids continue after the archived ones (analyst_session.archived_proposal_count,
     check_answer's first_proposal_n) and are unchanged for a run with no retry folder;
  4. the three claims the command rests on, run for real: run_loop re-enters a completed run from
     the reset pending_stage and runs analyst -> regroup_record -> route; regroup_record replaces
     the run's memory entry; the DONE branch decides again and mints no colliding id.

All synthetic and under the per-test sandbox: no model call, no backtest, no real run folder.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

SR_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR_ROOT / "workflow"))
sys.path.insert(0, str(SR_ROOT / "tools"))
sys.path.insert(0, str(SR_ROOT / "tests"))

import analyst_session as asm  # noqa: E402
import campaign_lock  # noqa: E402
import record_schema as rs  # noqa: E402
import run_campaign as camp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402

from d178_legacy_fixture import d178_checks_off  # noqa: E402,F401  (D-178, as test_e075_pr5)
import test_e075_pr4_queries as q4  # noqa: E402
import test_e075_pr5_analyst as t75  # noqa: E402
from _reader_test_helpers import (  # noqa: E402,F401
    REGROUP_RUN_ID, _memory, _set_orchestrator, reader_docs)
from test_e059_6c_s2a_route_retirement import (  # noqa: E402
    FLAT_ON, RETIRED_ON, _graded_run)
from test_e059_s2a_decide_next import (  # noqa: E402
    _memory_entry, _patch, _stage_flag_on_source, _write_flags)
from test_halt_quarantine_policy import (  # noqa: E402
    _entry, _save_queue_entries, _write_fresh_scaffold,
    campaign_root,  # noqa: F401  (fixture)
)
from test_profit_bars_every_backtest import _write_bars  # noqa: E402

RUN = "run_900"
LENSES = ("trade_efficiency", "forecast_power")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _read(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _queue(cr) -> list:
    return _read(cr["queue_path"])["queue"]


def _reading(category: str, run_id: str, n_findings: int, first: int = 1) -> dict:
    rid = f"{category}-{run_id}"
    return {"schema_version": 3, "reading_id": rid, "model_id": "m", "rubric_version": "r",
            "explanation": "x", "evidence": ["q1:a=1"],
            "side_findings": [{"proposal_id": f"{rid}-{first + i}"} for i in range(n_findings)]}


def _finished_run(cr, run_id=RUN, **state) -> Path:
    """A completed run with the analyst's artifacts on disk and a done queue entry."""
    run_dir = _write_fresh_scaffold(
        cr["runs_dir"], run_id, status="completed", pending_stage="completed_refuted",
        completed_stages=["protocol_execution", "analyst", "regroup_record"],
        last_error="old error", **state)
    arts = run_dir / "artifacts"
    (arts / "analyst").mkdir()
    (arts / "analyst" / "trade_efficiency.yaml").write_text("record: te\n", encoding="utf-8")
    (arts / "analyst_queries").mkdir()
    (arts / "analyst_queries" / "trade_efficiency.yaml").write_text("log: te\n", encoding="utf-8")
    (arts / "proposals").mkdir()
    for category, n in (("trade_efficiency", 1), ("forecast_power", 0)):
        (arts / "proposals" / f"{category}.yaml").write_text(
            yaml.safe_dump(_reading(category, run_id, n)), encoding="utf-8")
    (arts / "decision_record.yaml").write_text("picked: first\n", encoding="utf-8")
    (arts / "idea_status.yaml").write_text("idea_status: refuted\n", encoding="utf-8")
    entry = {**_entry(run_id, "E900"), "status": "done", "outcome": "refuted",
             "pass_rule_evaluation_ref": f"runs/{run_id}/artifacts/idea_status.yaml",
             "notes": "first note."}
    _save_queue_entries(cr["queue_path"], [entry])
    return run_dir


@pytest.fixture
def flags_on(monkeypatch):
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    monkeypatch.setattr(rpr, "_regroup_record_enabled", lambda *a: True)


def _snapshot(cr, run_dir: Path) -> tuple:
    return (cr["queue_path"].read_bytes(), (run_dir / "pipeline_state.yaml").read_bytes(),
            sorted(str(p.relative_to(run_dir)) for p in run_dir.rglob("*")))


# ---------------------------------------------------------------------------
# 1. the command
# ---------------------------------------------------------------------------

def test_retry_archives_clears_and_resets(campaign_root, flags_on):
    run_dir = _finished_run(campaign_root)
    arts = run_dir / "artifacts"
    before = {name: (arts / name).read_bytes() for name in
              ("analyst/trade_efficiency.yaml", "analyst_queries/trade_efficiency.yaml",
               "proposals/trade_efficiency.yaml", "proposals/forecast_power.yaml",
               "decision_record.yaml")}

    assert camp._retry_analyst(RUN) is True

    # the archive: byte-for-byte copies of all four items
    for name, content in before.items():
        assert (arts / "retry_1" / name).read_bytes() == content, name
    # the live per-attempt files the stage would validate instead of re-run are gone;
    # nothing else was touched (the decision record is overwritten by the next decide call)
    assert not (arts / "analyst").exists() and not (arts / "analyst_queries").exists()
    assert sorted(p.name for p in (arts / "proposals").glob("*")) == []
    assert (arts / "decision_record.yaml").read_bytes() == before["decision_record.yaml"]
    assert (arts / "idea_status.yaml").exists()
    # the run
    state = _read(run_dir / "pipeline_state.yaml")
    assert state["status"] == "active" and state["pending_stage"] == "analyst"
    assert state["last_error"] is None
    assert state["completed_stages"] == ["protocol_execution", "analyst", "regroup_record"]
    # the entry
    (entry,) = _queue(campaign_root)
    assert entry["status"] == "in_progress" and entry["outcome"] is None
    assert entry["run_ids"] == [RUN] and entry["priority"] == 1
    assert entry["notes"].startswith("first note.") and "RETRY-ANALYST" in entry["notes"]
    assert "artifacts/retry_1/" in entry["notes"] and "was refuted" in entry["notes"]
    vce.validate_verdict_provenance(entry, root=campaign_root["root"],
                                    schema=rs.QUEUE_ENTRY_SCHEMA)
    assert camp._select_entry(_queue(campaign_root))["id"] == "E900"
    # the log, and the lock is released
    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert f"RETRY-ANALYST E900 / {RUN}" in log
    assert not campaign_lock.lock_path_for(rpr.CAMPAIGN_STATE_PATH).exists()


def test_a_second_retry_numbers_its_folder_after_the_first_and_leaves_it_alone(
        campaign_root, flags_on):
    run_dir = _finished_run(campaign_root)
    assert camp._retry_analyst(RUN) is True
    first = {p: p.read_bytes() for p in (run_dir / "artifacts" / "retry_1").rglob("*")
             if p.is_file()}
    # the second pass finishes: the analyst wrote new readings, the run is completed again
    arts = run_dir / "artifacts"
    (arts / "analyst").mkdir()
    (arts / "analyst" / "trade_efficiency.yaml").write_text("record: second\n", encoding="utf-8")
    (arts / "proposals" / "trade_efficiency.yaml").write_text(
        yaml.safe_dump(_reading("trade_efficiency", RUN, 1, first=2)), encoding="utf-8")
    rpr.update_state(path=run_dir, status="completed", pending_stage="completed_refuted")
    queue = _queue(campaign_root)
    queue[0].update(status="done", outcome="refuted")
    _save_queue_entries(campaign_root["queue_path"], queue)

    assert camp._retry_analyst(RUN) is True
    assert (arts / "retry_2" / "analyst" / "trade_efficiency.yaml").read_text(
        encoding="utf-8") == "record: second\n"
    assert {p: p.read_bytes() for p in (arts / "retry_1").rglob("*") if p.is_file()} == first
    assert sorted(p.name for p in arts.glob("retry_*")) == ["retry_1", "retry_2"]


# ---------------------------------------------------------------------------
# 2. refusals: each changes nothing
# ---------------------------------------------------------------------------

def _refuse_not_done(cr, run_dir):
    q = _queue(cr)
    q[0]["status"] = "in_progress"
    _save_queue_entries(cr["queue_path"], q)


def _refuse_not_last(cr, run_dir):
    q = _queue(cr)
    q[0]["run_ids"] = [RUN, "run_901"]
    _save_queue_entries(cr["queue_path"], q)


def _refuse_not_completed(cr, run_dir):
    rpr.update_state(path=run_dir, status="paused_for_human")


def _refuse_refold(cr, run_dir):
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml",
                  {"refold": {"source_run": "run_001", "fold": "B"}})


def _refuse_no_proposals(cr, run_dir):
    import shutil
    shutil.rmtree(run_dir / "artifacts" / "proposals")


def _refuse_over_budget(cr, run_dir):
    rpr.update_state(path=run_dir, audit_log={
        "analyst_attempt_0": {"tokens": {"input": 10 ** 9, "output": 0}}})


@pytest.mark.parametrize("damage,needle", [
    (_refuse_not_done, "not 'done'"),
    (_refuse_not_last, "not the last run"),
    (_refuse_not_completed, "not 'completed'"),
    (_refuse_refold, "operator re-run"),
    (_refuse_no_proposals, "no artifacts/proposals/"),
    (_refuse_over_budget, "over its weighted token budget"),
])
def test_retry_refusals_change_nothing(campaign_root, flags_on, capsys, damage, needle):
    run_dir = _finished_run(campaign_root)
    damage(campaign_root, run_dir)
    before = _snapshot(campaign_root, run_dir)
    assert camp._retry_analyst(RUN) is False
    assert needle in capsys.readouterr().out
    assert _snapshot(campaign_root, run_dir) == before
    assert not list((run_dir / "artifacts").glob("retry_*"))
    assert not campaign_lock.lock_path_for(rpr.CAMPAIGN_STATE_PATH).exists()


def test_the_over_budget_fixture_really_is_over_budget(campaign_root):
    run_dir = _finished_run(campaign_root)
    _refuse_over_budget(campaign_root, run_dir)
    used, _ = rpr._compute_weighted_budget_usage(_read(run_dir / "pipeline_state.yaml")["audit_log"])
    assert used > rpr._load_token_budget()


@pytest.mark.parametrize("off", ["analyst", "regroup_record"])
def test_retry_refused_with_a_flag_off(campaign_root, monkeypatch, capsys, off):
    run_dir = _finished_run(campaign_root)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: off != "analyst")
    monkeypatch.setattr(rpr, "_regroup_record_enabled", lambda *a: off != "regroup_record")
    before = _snapshot(campaign_root, run_dir)
    assert camp._retry_analyst(RUN) is False
    assert "must both be on" in capsys.readouterr().out
    assert _snapshot(campaign_root, run_dir) == before


def test_retry_refused_for_an_unknown_run(campaign_root, flags_on, capsys):
    _finished_run(campaign_root)
    assert camp._retry_analyst("run_404") is False
    assert "no queue entry holds 'run_404'" in capsys.readouterr().out


def test_retry_refused_while_the_campaign_lock_is_held(campaign_root, flags_on):
    run_dir = _finished_run(campaign_root)
    before = _snapshot(campaign_root, run_dir)
    lock = campaign_lock.lock_path_for(rpr.CAMPAIGN_STATE_PATH)
    campaign_lock.acquire(lock)
    try:
        assert camp._retry_analyst(RUN) is False
        assert lock.exists()          # never released on someone else's behalf
    finally:
        campaign_lock.release(lock)
    assert _snapshot(campaign_root, run_dir) == before


def test_a_failed_archive_leaves_nothing_changed(campaign_root, flags_on, monkeypatch):
    run_dir = _finished_run(campaign_root)
    before = _snapshot(campaign_root, run_dir)

    def boom(*a, **k):
        raise OSError("disk full")
    monkeypatch.setattr(camp.shutil, "copytree", boom)
    assert camp._retry_analyst(RUN) is False
    assert _snapshot(campaign_root, run_dir) == before


def test_cli_exposes_retry_analyst():
    src = (SR_ROOT / "workflow" / "run_campaign.py").read_text(encoding="utf-8")
    assert 'subparsers.add_parser("retry-analyst"' in src
    assert 'args.command == "retry-analyst"' in src and "_retry_analyst_from_cli(args.run)" in src


# ---------------------------------------------------------------------------
# 3. proposal ids continue after the archived ones
# ---------------------------------------------------------------------------

def test_archived_proposal_count_reads_every_retry_folder(tmp_path):
    arts = tmp_path / "artifacts"
    for k, (te, fp) in enumerate([(2, 0), (1, 3)], start=1):
        (arts / f"retry_{k}" / "proposals").mkdir(parents=True)
        for category, n in (("trade_efficiency", te), ("forecast_power", fp)):
            (arts / f"retry_{k}" / "proposals" / f"{category}.yaml").write_text(
                yaml.safe_dump(_reading(category, "run_1", n)), encoding="utf-8")
    (arts / "proposals").mkdir()      # the live folder is not an archive
    (arts / "proposals" / "trade_efficiency.yaml").write_text(
        yaml.safe_dump(_reading("trade_efficiency", "run_1", 5)), encoding="utf-8")
    assert asm.archived_proposal_count(tmp_path, "trade_efficiency") == 3
    assert asm.archived_proposal_count(tmp_path, "forecast_power") == 3


def test_archived_proposal_count_is_zero_without_a_retry_folder(tmp_path):
    (tmp_path / "artifacts" / "proposals").mkdir(parents=True)
    assert asm.archived_proposal_count(tmp_path, "trade_efficiency") == 0
    assert asm.archived_proposal_count(tmp_path / "absent", "trade_efficiency") == 0


def _check(**kw):
    return asm.check_answer(t75._claim_answer(), lens="trade_efficiency", run_id=t75.RUN_ID,
                            entries=t75._entries_for_claim(), claim_check=lambda c: t75._Res(),
                            holdout_start=q4.HOLDOUT, fold="A", model_id="m", **kw)


def test_the_proposal_id_is_one_by_default_and_continues_on_request(d178_checks_off):
    reading, _rec, errors = _check()
    assert errors == []
    assert reading["side_findings"][0]["proposal_id"] == f"trade_efficiency-{t75.RUN_ID}-1"
    reading, _rec, errors = _check(first_proposal_n=3)
    assert errors == []
    assert reading["side_findings"][0]["proposal_id"] == f"trade_efficiency-{t75.RUN_ID}-3"
    assert reading["reading_id"] == f"trade_efficiency-{t75.RUN_ID}"      # the reading keeps its id


# ---------------------------------------------------------------------------
# 4. the three claims, for real
# ---------------------------------------------------------------------------

pytestmark_loop = pytest.mark.usefixtures("reader_docs")


def _fake_worker(called):
    def worker(lens, run_id, run_dir, stage_attempt=0):
        called.append((lens, stage_attempt))
        rpr._write_skipped_reading(asm.LENS_CATEGORY[lens], run_id, run_dir,
                                   {"rule": "output_refused_after_retry", "reason": "stub"})
    return worker


@pytestmark_loop
def test_run_loop_reenters_a_completed_run_and_runs_analyst_regroup_record_and_the_route(
        campaign_root, monkeypatch):
    """Claims 1 and 2: run_loop leaves a completed run only through pending_stage; reset to
    `analyst` it runs both lenses again (the archive is not what the stage sees), then
    regroup_record replaces the run's memory entry, then the route ends the run again."""
    _write_bars()
    _set_orchestrator(RETIRED_ON)
    monkeypatch.setattr(rpr, "_analyst_enabled", lambda *a: True)
    called: list = []
    monkeypatch.setattr(rpr, "run_analyst_worker", _fake_worker(called))
    run_dir = _graded_run("refuted", good=False)            # at regroup_record
    arts = run_dir / "artifacts"
    rpr.run_loop(REGROUP_RUN_ID)
    first_state = _read(run_dir / "pipeline_state.yaml")
    assert first_state["status"] == "completed" and first_state["pending_stage"] == "completed_refuted"
    assert called == []                                         # the seeded lens files stood
    # a finished run's queue entry, its analyst records, and the analyst stage counted once
    rpr.update_state(path=run_dir, stage_attempts={"analyst": 1})
    (arts / "analyst").mkdir(exist_ok=True)
    (arts / "analyst" / "trade_efficiency.yaml").write_text("record: first\n", encoding="utf-8")
    _save_queue_entries(camp.QUEUE_PATH, [
        {**_entry(REGROUP_RUN_ID, "E980"), "status": "done", "outcome": "refuted",
         "pass_rule_evaluation_ref": f"runs/{REGROUP_RUN_ID}/artifacts/idea_status.yaml"}])
    with monkeypatch.context() as m:
        m.setattr(rpr, "_regroup_record_enabled", lambda *a: True)
        assert camp._retry_analyst(REGROUP_RUN_ID) is True
    assert (arts / "retry_1" / "analyst" / "trade_efficiency.yaml").exists()
    assert _read(run_dir / "pipeline_state.yaml")["pending_stage"] == "analyst"

    memory_before = _memory()["runs"][REGROUP_RUN_ID]
    rpr.run_loop(REGROUP_RUN_ID)

    state = _read(run_dir / "pipeline_state.yaml")
    assert called == [("trade_efficiency", 1), ("forecast", 1)]     # both lenses ran, attempt 1
    assert state["completed_stages"][-2:] == ["analyst", "regroup_record"]
    assert state["status"] == "completed" and state["pending_stage"] == "completed_refuted"
    assert state["last_error"] is None
    assert state["stage_attempts"]["analyst"] == 2
    # the two lenses were re-written by the second pass (stub: code-written skipped readings),
    # not left as the first pass wrote them
    for category in LENSES:
        now = (arts / "proposals" / f"{category}.yaml").read_bytes()
        assert now != (arts / "retry_1" / "proposals" / f"{category}.yaml").read_bytes()
        assert "output_refused_after_retry" in now.decode("utf-8")
    # regroup_record replaced the run's memory entry (same key, recorded again)
    assert list(_memory()["runs"]) == [REGROUP_RUN_ID]
    assert _memory()["runs"][REGROUP_RUN_ID]["recorded_at"] != memory_before["recorded_at"] \
        or _memory()["runs"][REGROUP_RUN_ID] != first_memory
    # and nothing of the first pass was touched
    assert (arts / "retry_1" / "analyst" / "trade_efficiency.yaml").read_text(
        encoding="utf-8") == "record: first\n"


def _stub_second_pass(cr, run_dir, ids, extra=None):
    """A run_loop stand-in for the second analyst pass: new readings numbered `ids`, the memory
    entry re-recorded with them, the run completed again."""
    def run_loop(run_id):
        arts = run_dir / "artifacts"
        arts.joinpath("proposals", "profitability.yaml").write_text(
            yaml.safe_dump([_patch(pid, conf=3) for pid in ids]), encoding="utf-8")
        mem_path = cr["root"] / "campaign_record" / "campaign_memory.yaml"
        mem = _read(mem_path)
        mem["runs"][run_id] = _memory_entry(run_id, proposal_ids=ids)
        mem_path.write_text(yaml.safe_dump(mem), encoding="utf-8")
        rpr.update_state(path=run_dir, status="completed", pending_stage="completed_refuted")
    return run_loop


def _first_pass_then_retry(campaign_root, monkeypatch):
    """run_061 done and decided (minting profitability-run_061-1), that entry rejected by hand,
    then retry-analyst. Returns (run_dir, the minted entry's id)."""
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    root = campaign_root["root"]
    run_dir = _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1", conf=3)])
    _write_flags(root, **FLAT_ON)
    rpr.update_state(path=run_dir, status="completed", pending_stage="completed_refuted")
    assert camp.process_once() is True
    queue = _queue(campaign_root)
    done, minted = queue
    assert done["status"] == "done" and minted["id"] == "profitability-run_061-1"
    minted["status"] = "superseded"                       # the operator's rejection, by hand
    _save_queue_entries(campaign_root["queue_path"], queue)
    with monkeypatch.context() as m:
        m.setattr(rpr, "_analyst_enabled", lambda *a: True)
        m.setattr(rpr, "_regroup_record_enabled", lambda *a: True)
        assert camp._retry_analyst("run_061") is True
    return run_dir, minted["id"]


def test_the_done_branch_decides_again_and_the_continued_ids_do_not_collide(
        campaign_root, monkeypatch):
    """Claim 3: after the retried run completes again, process_once's DONE branch runs
    decide-next on the new readings. The retried analyst numbers its proposal -2 (it counts the
    archived one), so the new entry and brief never collide with the superseded -1."""
    run_dir, old_id = _first_pass_then_retry(campaign_root, monkeypatch)
    arts = run_dir / "artifacts"
    old_record = (arts / "decision_record.yaml").read_bytes()
    (entry, superseded) = _queue(campaign_root)
    assert entry["status"] == "in_progress" and superseded["status"] == "superseded"

    # what the next --once does: the entry is selected, run_loop runs the second pass
    n = 1 + asm.archived_proposal_count(run_dir, "profitability")      # the archive's count
    assert n == 2
    monkeypatch.setattr(rpr, "run_loop", _stub_second_pass(
        campaign_root, run_dir, [f"profitability-run_061-{n}"]))
    assert camp.process_once() is True

    queue = _queue(campaign_root)
    done, superseded, new = queue
    assert done["status"] == "done" and done["outcome"] == "refuted"
    assert done["pass_rule_evaluation_ref"] == "runs/run_061/artifacts/idea_status.yaml"
    vce.validate_verdict_provenance(done, root=campaign_root["root"], schema=rs.QUEUE_ENTRY_SCHEMA)
    assert superseded["id"] == old_id and superseded["status"] == "superseded"
    assert new["id"] == "profitability-run_061-2" and new["status"] == "ready"
    new_record = (arts / "decision_record.yaml").read_bytes()
    assert new_record != old_record                                    # decided again
    assert (arts / "retry_1" / "decision_record.yaml").read_bytes() == old_record
    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert "DECIDE after TEST_ENTRY (run_061): picked profitability-run_061-2" in log


def test_without_the_continued_numbering_decide_next_picks_nothing(campaign_root, monkeypatch):
    """The reason for the numbering: a second pass that wrote -1 again proposes the id the
    superseded entry already holds, so decide-next finds no eligible candidate and stops."""
    run_dir, old_id = _first_pass_then_retry(campaign_root, monkeypatch)
    monkeypatch.setattr(rpr, "run_loop", _stub_second_pass(
        campaign_root, run_dir, ["profitability-run_061-1"]))
    assert camp.process_once() is False
    assert [e["id"] for e in _queue(campaign_root)] == ["TEST_ENTRY", old_id]
    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert "DECIDE stop after TEST_ENTRY (run_061): no_eligible_candidate" in log
