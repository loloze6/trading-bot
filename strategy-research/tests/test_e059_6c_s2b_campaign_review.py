"""
E-059 S3 / slice 6c S2b -- campaign review under retired verdict routing
(orchestrator.verdict_routing_retired.enabled, off by default). Spec:
engineering/roadmap/E-059/S1_FINDINGS_6C.md §3, §5, guesses 3-6, §8 (S2b) and
its operator decision of 2026-09-25 (guesses 2-13 on the S1 defaults). The
code-review fixes have their own regression file,
tests/test_e059_6c_s2b_review_fixes.py.

All synthetic: no LLM (the worker is stubbed), no backtest, no trial row, no
holdout.
  1. Drift: the terminate pause in every pause list; the reframe brief's
     required keys match run_campaign's parser; the origin is schema-valid;
     the note is a separate file, never in SKILL.md.
  2. Cadence: review_every_n_runs recorded runs without an engineering_fault
     not yet covered by a completed review; never failed_families.
  3. run_loop under the flag: the review runs (the S2a guard lets a triggered
     review through), reads the digest and the note, never
     verdict_interpretation.yaml; each recommendation's effect.
  4. continue / escalate_* never read verdict_interpretation.yaml.
  5. process_once: a reframe becomes one `ready` queue entry and nothing
     else; terminate halts the queue.
  6. Flag off: the campaign_review prompt and the legacy route are unchanged.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest
import yaml

_SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402
import record_schema as rs  # noqa: E402

from test_e058_s2a_regroup_record import RUN_ID, _seed, _set_orchestrator  # noqa: E402
from test_profit_bars_every_backtest import _state  # noqa: E402
from test_halt_quarantine_policy import campaign_root  # noqa: E402,F401  (fixture)
from test_e059_s2a_decide_next import (  # noqa: E402
    _write_flags, _patch, _stage_flag_on_source)
from test_e059_6c_s2a_route_retirement import (  # noqa: E402
    RETIRED_ON, PREREQS, FLAT_ON, _forbid, _graded_run, _run_dirs, _MUST_NOT_RUN)

# The legacy machinery the flag route must never touch. determine_post_
# campaign_review_route itself IS called under the flag (its first line is the
# flag branch), so it is not forbidden here.
_FORBIDDEN = tuple(n for n in _MUST_NOT_RUN if n != "determine_post_campaign_review_route")
_BRIEF = {"strategy_domain": "crypto", "market_universe": "BTCUSDT", "timeframe": "1h",
          "research_goal": "old goal", "venue": "binance", "product": "perp"}
PIN = {"protocol_ref": "protocols/p8.json"}


@pytest.fixture(autouse=True)
def _stub_tbot_python(monkeypatch):
    monkeypatch.setattr(rpr, "_resolve_tbot_python", lambda: Path("stub-python"))


def _mem_entry(run_id: str, idea_status: str = "refuted", fault: str | None = None) -> dict:
    if fault:
        return {"run_id": run_id, "hypothesis_id": None, "legacy": False, "recorded_at": "t",
                "engineering_fault": fault, "engineering_fault_detail": ["x"]}
    return {"run_id": run_id, "hypothesis_id": f"H-{run_id}", "legacy": False, "recorded_at": "t",
            "idea_status": idea_status, "engineering_fault": None, "engineering_fault_detail": []}


def _write_memory(entries: dict) -> Path:
    path = rpr._campaign_memory_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({"schema_version": 1, "legacy_note": "", "runs": entries}),
                    encoding="utf-8")
    return path


def _prior_runs(k: int, faults: int = 2) -> dict:
    """k earlier recorded runs without a fault, plus `faults` fault-only ones."""
    out = {f"run_9{i:02d}": _mem_entry(f"run_9{i:02d}") for i in range(k)}
    out.update({f"run_8{i:02d}": _mem_entry(f"run_8{i:02d}", fault="component_execution_error")
                for i in range(faults)})
    return out


def _pin_source_protocol(run_dir: Path) -> None:
    """The source run's protocol pin (the reframe brief copies it) and the
    protocol file run_loop's pin check needs."""
    pre = rpr.load_yaml(run_dir / "artifacts" / "pre_registration.yaml") or {}
    pre["machine_constraints"] = dict(PIN)
    rpr.save_yaml(run_dir / "artifacts" / "pre_registration.yaml", pre)
    proto = rpr.ROOT / "protocols" / "p8.json"
    proto.parent.mkdir(parents=True, exist_ok=True)
    proto.write_text("{}", encoding="utf-8")


def _review_ready_run(idea_status: str = "refuted", prior: int = 5, kb: bool = True) -> Path:
    """A graded run at regroup_record whose regroup makes it the (prior+1)-th
    recorded run with no completed review yet; its brief, protocol pin and
    (kb=True) the KB on disk."""
    run_dir = _graded_run(idea_status, good=False)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", dict(_BRIEF))
    _pin_source_protocol(run_dir)
    if kb:
        rpr.save_yaml(rpr._KB_PATH, {"findings": []})
    _write_memory(_prior_runs(prior))
    return run_dir


def _stub_review(monkeypatch, review: dict | None, seen: list):
    """Stub the LLM worker: record the handoff it was given (after every
    _apply_* helper) and write campaign_review.yaml."""
    async def _worker(stage_name, handoff, path, retry_context=None):
        seen.append((stage_name, json.loads(json.dumps(handoff))))
        if review is not None:
            rpr.save_yaml(Path(path) / "artifacts" / "campaign_review.yaml", review)
    monkeypatch.setattr(rpr, "run_claude_worker", _worker)


def _no_verdict_interpretation(monkeypatch):
    real = rpr.load_yaml

    def _guarded(path, *a, **k):
        assert Path(path).name != "verdict_interpretation.yaml", "verdict_interpretation.yaml read"
        return real(path, *a, **k)
    monkeypatch.setattr(rpr, "load_yaml", _guarded)


def _mark_triggered(run_dir: Path, since=(RUN_ID,)) -> None:
    rpr.update_state(path=run_dir, **{rpr.CAMPAIGN_REVIEW_TRIGGER_KEY: {
        "rule": "runs_since_last_completed_review", "since_runs": list(since)}})


def _review_log() -> dict:
    path = rpr._review_log_path()
    return rpr.load_yaml(path) if path.exists() else {"completed": []}


# ---------------------------------------------------------------------------
# 1. Drift
# ---------------------------------------------------------------------------

def test_terminate_pause_is_in_every_pause_list():
    flag = rpr.CAMPAIGN_REVIEW_TERMINATE_FLAG
    assert flag == "campaign_review_terminate"
    assert dict(camp._PAUSE_FLAG_TO_REASON)[flag] == flag
    assert camp._classify_human_pause(Path("."), {"flags": {flag: True}}) == flag
    # a stale lower flag from earlier in the run never masks the stop
    assert camp._classify_human_pause(
        Path("."), {"flags": {flag: True, "profit_bars_reached": True,
                              "kb_reactivation_violation": True}}) == flag
    assert flag not in camp._QUARANTINE_SAFE_REASONS
    assert flag not in camp._REQUEUEABLE_QUARANTINE_REASONS
    runbook = (_SR / "docs" / "RUNBOOK.md").read_text(encoding="utf-8")
    assert f"| `{flag}`" in runbook
    assert f"'{flag}': False" in runbook  # section 4's reset list
    rs.validate_queue_entry({"id": "x", "status": f"paused:{flag}"})


def test_reframe_brief_keys_match_the_brief_parser(tmp_path):
    def _write(doc):
        p = tmp_path / "b.md"
        p.write_text("---\n" + yaml.safe_dump(doc) + "---\n", encoding="utf-8")
        return p
    full = {k: "x" for k in rpr.REFRAME_BRIEF_REQUIRED_KEYS}
    assert camp._parse_brief_frontmatter(_write(full)) == full
    for key in rpr.REFRAME_BRIEF_REQUIRED_KEYS:
        with pytest.raises(ValueError, match=f"missing required field '{key}'"):
            camp._parse_brief_frontmatter(_write({k: v for k, v in full.items() if k != key}))


def test_origin_and_state_keys():
    assert rpr.CAMPAIGN_REVIEW_ORIGIN in rs._ORIGIN_VALUES
    rs.validate_queue_entry({"id": "run_1__reframe", "status": "ready", "priority": 999,
                             "source": "agent", "origin": rpr.CAMPAIGN_REVIEW_ORIGIN,
                             "brief_path": "campaign_record/candidate_briefs/run_1__reframe.md",
                             "notes": "n", "run_ids": []})
    keys = {rpr.CAMPAIGN_REVIEW_TRIGGER_KEY, rpr.CAMPAIGN_REVIEW_REFRAME_KEY,
            rpr.CAMPAIGN_REVIEW_TERMINATE_KEY, rpr.CAMPAIGN_REVIEW_TERMINATE_FLAG}
    assert len(keys) == 4
    for doc in ("docs/RUNBOOK.md", "docs/USER_GUIDE.md"):
        text = (_SR / doc).read_text(encoding="utf-8")
        assert rpr.CAMPAIGN_REVIEW_TRIGGER_KEY in text, doc


def test_note_is_a_separate_file_never_in_the_skill():
    note = _SR / "workflow_artifacts" / "skills" / "campaign-review" / "RETIRED_ROUTING.md"
    assert note.is_file()
    assert rpr._RETIRED_REVIEW_GUIDANCE.endswith("skills/campaign-review/RETIRED_ROUTING.md")
    skill = (_SR / "workflow_artifacts" / "skills" / "campaign-review" / "SKILL.md").read_text(
        encoding="utf-8")
    assert "RETIRED_ROUTING" not in skill and "verdict_routing_retired" not in skill
    text = note.read_text(encoding="utf-8")
    for rec in ("continue", "reframe", "escalate_instrument", "escalate_component", "terminate"):
        assert f"`{rec}`" in text
    for key in rpr.REFRAME_BRIEF_REQUIRED_KEYS:
        assert f"`{key}`" in text


# ---------------------------------------------------------------------------
# 2. Cadence
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("prior,n,fires", [(4, 6, False), (5, 6, True), (6, 6, True),
                                           (11, 6, True), (1, 3, False), (2, 3, True)])
def test_trigger_counts_uncovered_recorded_runs_without_a_fault(prior, n, fires):
    runs = _prior_runs(prior, faults=3)
    runs[RUN_ID] = _mem_entry(RUN_ID)
    _write_memory(runs)
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"review_every_n_runs": n, "runs": []})
    trig = rpr._retired_review_trigger(RUN_ID)
    if fires:
        assert trig["rule"] == "runs_since_last_completed_review"
        assert trig["review_every_n_runs"] == n and trig["runs_since_last_review"] == prior + 1
        assert trig["since_runs"] == sorted(r for r, e in runs.items()
                                            if not e.get("engineering_fault"))
        assert trig["memory"] == "campaign_record/campaign_memory.yaml"
    else:
        assert trig is None


def test_trigger_never_reads_failed_families(monkeypatch):
    """S1 measured 9 distinct failed families live: the legacy trigger would fire
    after every run. The flag trigger ignores them."""
    monkeypatch.setattr(rpr, "_should_trigger_campaign_review",
                        lambda *a: (_ for _ in ()).throw(AssertionError("legacy trigger")))
    _write_memory({RUN_ID: _mem_entry(RUN_ID)})
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {
        "review_every_n_runs": 6, "runs": ["a"] * 6,
        "failed_families": [f"family_{i}" for i in range(9)]})
    assert rpr._retired_review_trigger(RUN_ID) is None


@pytest.mark.parametrize("entry", [None, "fault"])
def test_trigger_refuses_a_run_missing_from_the_memory(entry):
    runs = _prior_runs(5)
    if entry == "fault":
        runs[RUN_ID] = _mem_entry(RUN_ID, fault="component_execution_error")
    _write_memory(runs)
    with pytest.raises(ValueError, match="no recorded entry without an engineering_fault"):
        rpr._retired_review_trigger(RUN_ID)


@pytest.mark.parametrize("bad", [0, -6, "6", True, 2.0])
def test_trigger_refuses_a_bad_cadence(bad):
    _write_memory({RUN_ID: _mem_entry(RUN_ID)})
    rpr.save_yaml(rpr.CAMPAIGN_STATE_PATH, {"review_every_n_runs": bad})
    with pytest.raises(ValueError, match="review_every_n_runs"):
        rpr._retired_review_trigger(RUN_ID)


# ---------------------------------------------------------------------------
# 3. run_loop under the flag
# ---------------------------------------------------------------------------

def test_no_review_off_cadence(monkeypatch):
    _set_orchestrator(RETIRED_ON)
    run_dir = _review_ready_run(prior=3)
    seen = []
    _stub_review(monkeypatch, {"recommendation": "continue"}, seen)
    _forbid(monkeypatch, _FORBIDDEN)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert seen == [] and rpr.CAMPAIGN_REVIEW_TRIGGER_KEY not in state
    assert state["pending_stage"] == "completed_refuted" and state["status"] == "completed"


@pytest.mark.parametrize("rec", ["continue", "escalate_instrument", "escalate_component"])
def test_review_runs_on_the_6th_run_and_records_only(monkeypatch, rec):
    _set_orchestrator(RETIRED_ON)
    run_dir = _review_ready_run("refuted")
    dirs_before = _run_dirs()
    review = {"recommendation": rec, "recommendation_rationale": "needs a funding feed",
              # ignored on a continue (guess 4)
              "next_research_question": {**_BRIEF, "research_goal": "new"}}
    seen = []
    _stub_review(monkeypatch, review, seen)
    _forbid(monkeypatch, _FORBIDDEN)
    _no_verdict_interpretation(monkeypatch)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert [s for s, _ in seen] == ["campaign_review"]
    assert state["pending_stage"] == "completed_refuted" and state["status"] == "completed"
    assert state["completed_stages"][-2:] == ["regroup_record", "campaign_review"]
    trigger = state[rpr.CAMPAIGN_REVIEW_TRIGGER_KEY]
    assert trigger["runs_since_last_review"] == 6
    assert trigger["idea_status_terminal"] == "completed_refuted"
    assert not (state.get("flags") or {})
    assert rpr.CAMPAIGN_REVIEW_REFRAME_KEY not in state
    assert "continuation_child" not in state and _run_dirs() == dirs_before
    assert not (rpr.ROOT / "campaign_record" / "candidate_briefs").exists()
    # the review completed: it covers exactly the runs its trigger counted
    (done,) = _review_log()["completed"]
    assert done["run_id"] == RUN_ID and done["recommendation"] == rec
    assert done["covered_runs"] == trigger["since_runs"]
    requests = rpr.ROOT / "campaign_record" / "component_requests.yaml"
    if rec == "escalate_component":
        assert rpr.load_yaml(requests)["requests"] == [
            {"run_id": RUN_ID, "stage": "campaign_review", "variant_id": None,
             "reason": "needs a funding feed"}]
        # once per run: the route re-entered (a resume) appends neither again
        rpr._route_retired_campaign_review(run_dir, RUN_ID)
        assert len(rpr.load_yaml(requests)["requests"]) == 1
        assert len(_review_log()["completed"]) == 1
    else:
        assert not requests.exists()


def test_prompt_contains_the_note_under_the_flag(monkeypatch):
    """The assembled prompt (the real _build_stage_prompt) carries the note."""
    _set_orchestrator(RETIRED_ON)
    run_dir = _review_ready_run()
    _mark_triggered(run_dir)
    note_dst = rpr.ROOT / "workflow_artifacts" / "skills" / "campaign-review" / "RETIRED_ROUTING.md"
    note_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(_SR / "workflow_artifacts" / "skills" / "campaign-review" / "RETIRED_ROUTING.md",
                    note_dst)
    handoff = {"run_id": RUN_ID, "required_inputs": [], "deliverables": ["campaign_review.yaml"]}
    rpr._apply_retired_routing_review_context("campaign_review", handoff, run_dir)
    rpr._apply_retired_routing_review_context("campaign_review", handoff, run_dir)  # idempotent
    assert [r["path"] for r in handoff["required_inputs"]] == [rpr._RETIRED_REVIEW_GUIDANCE]
    monkeypatch.chdir(_SR)  # _build_stage_prompt reads the SKILL relative to cwd
    prompt = rpr._build_stage_prompt("campaign_review", handoff, run_dir)
    assert "Campaign review under retired verdict routing" in prompt
    other = {"run_id": RUN_ID, "required_inputs": []}
    rpr._apply_retired_routing_review_context("hypothesis_generation", other, run_dir)
    assert other == {"run_id": RUN_ID, "required_inputs": []}


def test_reframe_writes_a_brief_and_ends_with_the_idea_status(monkeypatch):
    _set_orchestrator(RETIRED_ON)
    run_dir = _review_ready_run("inconclusive")
    dirs_before = _run_dirs()
    queue_before = camp.QUEUE_PATH.read_bytes() if camp.QUEUE_PATH.exists() else None
    nrq = {"research_goal": "funding carry as cash flow", "timeframe": "1d"}
    _stub_review(monkeypatch, {"recommendation": "reframe", "next_research_question": nrq}, [])
    _forbid(monkeypatch, _FORBIDDEN)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["pending_stage"] == "completed_inconclusive" and state["status"] == "completed"
    rel = state[rpr.CAMPAIGN_REVIEW_REFRAME_KEY]
    assert rel == f"campaign_record/candidate_briefs/{RUN_ID}__reframe.md"
    brief = camp._parse_brief_frontmatter(rpr.ROOT / rel)
    assert brief["research_goal"] == "funding carry as cash flow" and brief["timeframe"] == "1d"
    assert brief["venue"] == "binance" and brief["market_universe"] == "BTCUSDT"  # filled
    assert brief["criteria_from"] == "hypothesis_generation"  # criteria at 1a
    assert brief["machine_constraints"] == PIN  # the source run's pin
    text = (rpr.ROOT / rel).read_text(encoding="utf-8")
    assert "Filled from" in text and "strategy_domain" in text
    # nothing else: no run, no queue write (registration happens at DONE)
    assert _run_dirs() == dirs_before
    assert (camp.QUEUE_PATH.read_bytes() if camp.QUEUE_PATH.exists() else None) == queue_before
    assert "continuation_child" not in state
    assert _review_log()["completed"][0]["recommendation"] == "reframe"


def test_reframe_refusals():
    run_dir = _seed()
    _pin_source_protocol(run_dir)
    rpr.save_yaml(run_dir / "artifacts" / "research_brief.yaml", {"venue": "binance"})
    with pytest.raises(ValueError, match="lacks"):
        rpr._write_reframe_brief(run_dir, RUN_ID, {"research_goal": "g"})
    for owned in ({"candidate": {"x": 1}}, {"criteria_from": "x"},
                  {"machine_constraints": {"protocol_ref": "other.json"}},
                  {"evaluation": {"pass_rule": {"criteria": []}}}):
        with pytest.raises(ValueError, match="the orchestrator writes those"):
            rpr._write_reframe_brief(run_dir, RUN_ID, {**_BRIEF, **owned})
    rel = rpr._write_reframe_brief(run_dir, RUN_ID, dict(_BRIEF))
    assert rpr._write_reframe_brief(run_dir, RUN_ID, dict(_BRIEF)) == rel  # idempotent
    with pytest.raises(RuntimeError, match="never overwritten"):
        rpr._write_reframe_brief(run_dir, RUN_ID, {**_BRIEF, "research_goal": "other"})


def test_reframe_without_a_source_protocol_is_refused():
    run_dir = _seed()
    with pytest.raises(ValueError, match="no protocol to pin"):
        rpr._write_reframe_brief(run_dir, RUN_ID, dict(_BRIEF))


def test_reframe_without_a_question_is_refused():
    run_dir = _seed()
    rpr.save_yaml(run_dir / "artifacts" / "campaign_review.yaml", {"recommendation": "reframe"})
    with pytest.raises(ValueError, match="reframe without a next_research_question"):
        rpr.determine_post_campaign_review_route(run_dir, RUN_ID, routing_retired=True)


def test_reframe_kb_reactivation_violation_pauses_before_any_write(monkeypatch):
    run_dir = _seed()
    _mark_triggered(run_dir)
    rpr.save_yaml(run_dir / "artifacts" / "campaign_review.yaml",
                  {"recommendation": "reframe", "next_research_question": dict(_BRIEF)})
    monkeypatch.setattr(rpr, "_check_kb_reactivation_conformance", lambda nrq, kb: ["closed H-1"])
    assert rpr.determine_post_campaign_review_route(run_dir, RUN_ID, routing_retired=True) == \
        "human_pause"
    state = _state(run_dir)
    assert state["flags"]["kb_reactivation_violation"] is True
    assert rpr.CAMPAIGN_REVIEW_REFRAME_KEY not in state
    assert not (rpr.ROOT / "campaign_record" / "candidate_briefs").exists()
    assert _review_log()["completed"] == []  # not completed: the review stays pending


def test_terminate_stops_then_resume_ends_with_the_idea_status(monkeypatch):
    _set_orchestrator(RETIRED_ON)
    run_dir = _review_ready_run("refuted")
    campaign_before = rpr.load_campaign_state()
    seen = []
    _stub_review(monkeypatch, {"recommendation": "terminate",
                               "recommendation_rationale": "every cell spent",
                               "altitude_justification": "legacy field"}, seen)
    _forbid(monkeypatch, _FORBIDDEN)
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["status"] == "paused_for_human" and state["pending_stage"] == "campaign_review"
    assert state["flags"] == {rpr.CAMPAIGN_REVIEW_TERMINATE_FLAG: True}
    assert camp._hard_pause_reason(run_dir, state) == ("campaign_review_terminate", "")
    decision = rpr.load_yaml(rpr.ROOT / "campaign_decision.yaml")
    (terminate,) = decision["history"]
    assert terminate["event"] == "terminate" and terminate["rationale"] == "every cell spent"
    assert "families_tried" not in terminate and "altitude_justification" not in terminate
    assert terminate["runs_attempted"] == sorted(list(_prior_runs(5)) + [RUN_ID])
    assert terminate["idea_status_counts"] == {"engineering_fault:component_execution_error": 2,
                                               "refuted": 6}
    assert decision["current"]["event"] == "terminate"
    campaign = rpr.load_campaign_state()
    assert campaign.get("status") != "space_empty"
    assert campaign.get("failed_families") == campaign_before.get("failed_families")
    assert _review_log()["completed"] == []  # not complete while stopped
    # the operator resumes: the same review ends the run, no second LLM call
    rpr.update_state(path=run_dir, status="active",
                     flags={rpr.CAMPAIGN_REVIEW_TERMINATE_FLAG: False})
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert len(seen) == 1
    assert state["pending_stage"] == "completed_refuted" and state["status"] == "completed"
    assert len(_review_log()["completed"]) == 1


def test_unknown_recommendation_raises():
    run_dir = _seed()
    rpr.save_yaml(run_dir / "artifacts" / "campaign_review.yaml", {"recommendation": "pivot"})
    with pytest.raises(ValueError, match="Unknown campaign_review recommendation"):
        rpr.determine_post_campaign_review_route(run_dir, RUN_ID, routing_retired=True)


def test_legacy_review_without_the_trigger_is_still_refused(monkeypatch):
    """The S2a guard is relaxed in one place only: a trigger marker lets a
    review through; its absence still pauses before the LLM call."""
    _set_orchestrator(RETIRED_ON)
    run_dir = _seed(pending="campaign_review")
    seen = []
    _stub_review(monkeypatch, {"recommendation": "continue"}, seen)
    rpr.run_loop(RUN_ID)
    assert seen == []
    assert _state(run_dir)["flags"] == {rpr.CAMPAIGN_REVIEW_REFUSED_FLAG: True}


# ---------------------------------------------------------------------------
# 4. continue / escalate_* never read verdict_interpretation.yaml
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rec", ["continue", "escalate_instrument", "escalate_component"])
def test_recorded_only_recommendations_never_load_the_interpretation(monkeypatch, rec):
    run_dir = _seed(idea_status="validated")
    _mark_triggered(run_dir)
    assert not (run_dir / "artifacts" / "verdict_interpretation.yaml").exists()
    rpr.save_yaml(run_dir / "artifacts" / "campaign_review.yaml", {
        "recommendation": rec, "recommendation_rationale": "r",
        "next_research_question": dict(_BRIEF)})
    _forbid(monkeypatch, _FORBIDDEN)
    _no_verdict_interpretation(monkeypatch)
    assert rpr.determine_post_campaign_review_route(run_dir, RUN_ID, routing_retired=True) == \
        "completed_validated"
    assert "continuation_child" not in _state(run_dir)


def test_flag_off_continue_still_reads_the_interpretation(monkeypatch):
    """The legacy branch is untouched: flag off, `continue` loads it as before."""
    run_dir = _seed()
    rpr.save_yaml(run_dir / "artifacts" / "campaign_review.yaml", {"recommendation": "continue"})
    reads = []
    real = rpr.load_yaml

    def _spy(path, *a, **k):
        if Path(path).name == "verdict_interpretation.yaml":
            reads.append(path)
            raise RuntimeError("stop here")
        return real(path, *a, **k)
    monkeypatch.setattr(rpr, "load_yaml", _spy)
    with pytest.raises(RuntimeError, match="stop here"):
        rpr.determine_post_campaign_review_route(run_dir, RUN_ID)
    assert len(reads) == 1


# ---------------------------------------------------------------------------
# 5. process_once
# ---------------------------------------------------------------------------

def _finished_reframe_run(campaign_root):
    run_dir = _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1", conf=3)],
                                    idea_status="refuted")
    _write_flags(campaign_root["root"], **FLAT_ON)
    rel = rpr._write_reframe_brief(run_dir, "run_061", {"research_goal": "a new question"})
    rpr.update_state(path=run_dir, status="completed", pending_stage="completed_refuted",
                     **{rpr.CAMPAIGN_REVIEW_REFRAME_KEY: rel})
    return run_dir, rel


def test_reframe_becomes_one_ready_queue_entry_and_nothing_else(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    monkeypatch.setenv("WORKFLOW_ARTIFACT_VALIDATION", "raise")
    root = campaign_root["root"]
    run_dir, rel = _finished_reframe_run(campaign_root)
    ledger_before = campaign_root["campaign_state_path"].read_bytes()
    dirs_before = {p.name for p in campaign_root["runs_dir"].iterdir()}

    assert camp.process_once() is True
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"]
    assert [e["id"] for e in queue] == ["TEST_ENTRY", "run_061__reframe"]
    done, new = queue
    assert done["status"] == "done" and done["outcome"] == "refuted"
    assert new == {"id": "run_061__reframe", "brief_path": rel, "status": "ready",
                   "priority": 999, "source": "agent",
                   "notes": new["notes"], "run_ids": [], "origin": "campaign_review"}
    rs.validate_queue_entry(new)
    record = rpr.load_yaml(run_dir / "artifacts" / "decision_record.yaml")
    assert record["picked"]["queue_entry_id"] == "run_061__reframe"  # decide-next picks it
    assert "candidate_id" not in record["picked"]  # nothing minted
    assert {p.name for p in campaign_root["runs_dir"].iterdir()} == dirs_before
    assert campaign_root["campaign_state_path"].read_bytes() == ledger_before
    log = (root / "campaign_log.md").read_text(encoding="utf-8")
    assert "REFRAME TEST_ENTRY (run_061): campaign review's brief registered as run_061__reframe" in log


def test_reframe_registration_is_idempotent_on_a_retried_step(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    run_dir, rel = _finished_reframe_run(campaign_root)
    state = _state(run_dir)
    entry = camp._load_queue()["queue"][0]
    assert camp._reframe_registration_blocker("run_061", state, True) is None
    assert camp._register_campaign_review_reframe(entry, "run_061", state) is True
    assert camp._reframe_registration_blocker("run_061", state, True) is None
    assert camp._register_campaign_review_reframe(entry, "run_061", state) is False
    assert [e["id"] for e in camp._load_queue()["queue"]] == ["TEST_ENTRY", "run_061__reframe"]


def test_terminate_halts_the_queue(campaign_root, monkeypatch):
    monkeypatch.setattr(rpr, "run_loop", lambda run_id: None)
    run_dir = _stage_flag_on_source(campaign_root, [_patch("profitability-run_061-1")],
                                    idea_status="refuted")
    _write_flags(campaign_root["root"], **FLAT_ON)
    rpr.update_state(path=run_dir, status="paused_for_human", pending_stage="campaign_review",
                     flags={rpr.CAMPAIGN_REVIEW_TERMINATE_FLAG: True})
    _mark_triggered(run_dir, since=["run_061"])
    assert camp.process_once() is False
    queue = camp._load_queue()["queue"]
    assert [e["id"] for e in queue] == ["TEST_ENTRY"]
    assert queue[0]["status"] == "paused:campaign_review_terminate"
    assert not (run_dir / "artifacts" / "decision_record.yaml").exists()
    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert "HALT — campaign_review_terminate" in log


# ---------------------------------------------------------------------------
# 6. Flag off: byte-identical prompt and legacy route
# ---------------------------------------------------------------------------

def test_flag_off_campaign_review_handoff_and_prompt_unchanged(monkeypatch):
    monkeypatch.chdir(_SR)
    run_dir = _seed()
    template = yaml.safe_load((_SR / "workflow_artifacts" / "templates" / "handoffs" /
                               "campaign_review.yaml").read_text(encoding="utf-8"))
    handoff = {**template, "required_inputs": [], "run_id": RUN_ID}
    reads = []
    real = rpr._verdict_routing_retired_enabled
    monkeypatch.setattr(rpr, "_verdict_routing_retired_enabled",
                        lambda: reads.append(1) or real())
    for cfg in (None, PREREQS, RETIRED_ON):  # no trigger marker: no-op whatever the config
        _set_orchestrator(cfg)
        h = json.loads(json.dumps(handoff))
        rpr._apply_retired_routing_review_context("campaign_review", h, run_dir)
        assert h == handoff
        assert rpr._build_stage_prompt("campaign_review", h, run_dir) == \
            rpr._build_stage_prompt("campaign_review", handoff, run_dir)
    assert reads == []  # no marker: returns before any flag read


@pytest.mark.parametrize("cfg", [None, PREREQS,
                                 {**PREREQS, "verdict_routing_retired": {"enabled": False}}])
def test_flag_off_legacy_route_call_unchanged(monkeypatch, cfg):
    """run_loop's flag-off campaign_review route: the same call as before
    (no keyword), the new trigger never consulted."""
    _set_orchestrator(cfg)
    run_dir = _seed(pending="campaign_review")
    rpr.save_yaml(run_dir / "handoffs" / "campaign_review.yaml",
                  {"required_inputs": [], "deliverables": ["campaign_review.yaml"]})
    rpr.save_yaml(run_dir / "artifacts" / "campaign_review.yaml", {"recommendation": "continue"})
    calls = []

    def _spy(*a, **k):
        calls.append((a, k))
        return "completed_rejected"
    monkeypatch.setattr(rpr, "determine_post_campaign_review_route", _spy)
    monkeypatch.setattr(rpr, "_retired_review_route",
                        lambda *a: (_ for _ in ()).throw(AssertionError("flag route")))
    rpr.run_loop(RUN_ID)
    assert calls == [((run_dir, RUN_ID), {})]
    assert _state(run_dir)["pending_stage"] == "completed_rejected"


def test_flag_off_regroup_route_never_evaluates_the_new_trigger(monkeypatch):
    """Six recorded runs, flag off: the new trigger is never consulted."""
    _set_orchestrator(PREREQS)
    run_dir = _review_ready_run("refuted")
    monkeypatch.setattr(rpr, "_retired_review_trigger",
                        lambda *a: (_ for _ in ()).throw(AssertionError("flag trigger")))
    rpr.run_loop(RUN_ID)
    state = _state(run_dir)
    assert state["pending_stage"] == "completed_rejected"
    assert rpr.CAMPAIGN_REVIEW_TRIGGER_KEY not in state
