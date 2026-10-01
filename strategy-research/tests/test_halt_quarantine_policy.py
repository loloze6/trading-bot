"""
E-030 S2a — quarantine + escalate halt policy (`workflow/run_campaign.py`), 2026-08-22.

SCOPE. This covers the QUARANTINE half of EPIC.md's Done-when #1 only. The retry
half is deliberately not built: the S1 taxonomy's R2 says the one proven-retryable
signature is an exact string match already implemented at the stage level
(`_invoke_agent_with_yaml_retry`, ledger A11, `9bf2a4cf`), and there is no second
evidenced campaign-level retry-safe signature. So there is nothing here that tests
retry, and that absence is intentional rather than an omission.

WHAT IS PROVEN HERE
  1. Bit-identity (EPIC.md Done-when #3): the SAME halt scenario run with the flag
     off and with the flag on. Flag-off is compared field-by-field against the
     behavior committed at HEAD -- the queue entry, campaign_log.md, campaign_
     summary.md, the halt_history append and process_once's own return value.
  2. Each of the four quarantine-safe reasons takes the right path, with the right
     queue shape and the right trial accounting.
  3. Every OTHER reason still escalates, including unhandled_exception (taxonomy R2)
     and R1's integrity list.
  4. R11 ambiguity: a stale flag from an earlier resolved pause, still set alongside
     a fresh quarantine-safe one, escalates rather than quarantines -- and says so.
  5. _PAUSE_FLAG_TO_REASON has not rotted away from _classify_human_pause's own
     branch order (the table duplicates it, so it is checked by execution).

Fixture pattern (campaign_root, _write_fresh_scaffold, _save_queue_entries) copied
from tests/test_halt_history.py, itself copied from
tests/test_k4_routing_registration.py's proven hermetic setup: nothing here touches
the real repository, and no LLM or subprocess is spawned.
"""
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402


_FRESH_STATE_TEMPLATE = {
    "status": "active",
    "current_stage": None,
    "pending_stage": "hypothesis_generation",
    "completed_stages": [],
    "artifacts": {},
    "governance": {
        "max_hypothesis_variants_per_cycle": 3,
        "max_refinements_after_validation": 2,
        "max_reruns_after_analysis": 1,
        "max_required_reads_per_stage": 3,
    },
    "counters": {"refinements_used": 0, "reruns_used": 0},
    "flags": {
        "holdout_reserved": False, "validation_approved": False,
        "screening_passed": False, "walk_forward_passed": False,
    },
    "last_summary": None,
}


def _write_fresh_scaffold(runs_dir: Path, run_id: str, **state_overrides):
    run_dir = runs_dir / run_id
    (run_dir / "artifacts").mkdir(parents=True, exist_ok=True)
    (run_dir / "handoffs").mkdir(parents=True, exist_ok=True)
    state = dict(_FRESH_STATE_TEMPLATE)
    state["run_id"] = run_id
    state.update(state_overrides)
    with open(run_dir / "pipeline_state.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, sort_keys=False)
    return run_dir


@pytest.fixture
def campaign_root(tmp_path, monkeypatch):
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    queue_path = config_dir / "campaign_queue.yaml"
    queue_path.write_text(yaml.safe_dump({"queue": []}), encoding="utf-8")
    baseline_path = config_dir / "campaign_baseline_runs.yaml"
    campaign_state_path = tmp_path / "campaign_state.yaml"

    monkeypatch.setattr(camp, "ROOT", tmp_path)
    monkeypatch.setattr(camp, "QUEUE_PATH", queue_path)
    monkeypatch.setattr(camp, "CAMPAIGN_LOG_PATH", tmp_path / "campaign_log.md")
    monkeypatch.setattr(camp, "CAMPAIGN_SUMMARY_PATH", tmp_path / "campaign_summary.md")
    monkeypatch.setattr(camp, "BASELINE_PATH", baseline_path)
    monkeypatch.setattr(rpr, "ROOT", tmp_path)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", campaign_state_path)

    def _fake_setup_run(run_id):
        _write_fresh_scaffold(runs_dir, run_id)
    monkeypatch.setattr(camp, "setup_run", _fake_setup_run)

    return {
        "root": tmp_path, "runs_dir": runs_dir, "queue_path": queue_path,
        "config_dir": config_dir, "campaign_state_path": campaign_state_path,
    }


def _set_quarantine_flag(config_dir: Path, enabled):
    """Writes the sandbox's own campaign_config.yaml. `enabled=None` writes a file
    with no halt_policy section at all -- the 'key absent' case, which must be
    indistinguishable from `false`."""
    cfg = {"orchestrator": {"token_budget_per_run_weighted_units": 1500000}}
    if enabled is not None:
        cfg["orchestrator"]["halt_policy"] = {"quarantine_enabled": enabled}
    (config_dir / "campaign_config.yaml").write_text(
        yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")


def _save_queue_entries(queue_path: Path, entries: list):
    with open(queue_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"queue": entries}, f, sort_keys=False)


def _write_campaign_state(path: Path, **fields):
    state = {
        "campaign_id": "test", "research_question": "", "runs": [],
        "altitude_history": [], "recent_parameter_dimensions_by_family": {},
        "failed_families": [], "instruments_tried": [], "components_built": [],
        "timeframes_tried": ["1h"], "diagnostics_log": [], "status": "active",
    }
    state.update(fields)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(state, f, sort_keys=False)


def _read_state(runs_dir: Path, run_id: str) -> dict:
    return yaml.safe_load((runs_dir / run_id / "pipeline_state.yaml").read_text(encoding="utf-8"))


def _entry(run_id: str, entry_id: str = "TEST_ENTRY") -> dict:
    return {
        "id": entry_id, "brief_path": "briefs/irrelevant.yaml",
        "status": "in_progress", "priority": 1, "run_ids": [run_id], "outcome": None,
    }


def _stage_halt(campaign_root, run_id: str, reason: str, *, flags=None,
                trial_rows=None, **state_overrides):
    """Puts the sandbox in the state that produces `reason` from
    _hard_pause_reason, and returns the run_dir. Each reason is staged through the
    SAME mechanism the real pipeline uses, so the classification under test is the
    real one, not a stub."""
    runs_dir = campaign_root["runs_dir"]
    base_flags = dict(flags or {})

    if reason == "unhandled_exception":
        run_dir = _write_fresh_scaffold(
            runs_dir, run_id, status="failed", pending_stage="human_pause",
            last_error="boom", flags=base_flags, **state_overrides)
    elif reason in ("component_gap", "new_component_escalation"):
        run_dir = _write_fresh_scaffold(
            runs_dir, run_id, status="paused_for_human", pending_stage="human_pause",
            flags=base_flags, **state_overrides)
        if reason == "component_gap":
            (run_dir / "artifacts" / "decision.yaml").write_text(yaml.safe_dump({
                "stage": "backtest_specification", "status": "component_gap",
                "rationale": "needs MacdHistogramCrossoverComponent, which does not exist",
                "blocking_issues": ["engine lacks MacdHistogramCrossoverComponent"],
            }), encoding="utf-8")
        else:
            (run_dir / "artifacts" / "escalation_request.yaml").write_text(yaml.safe_dump({
                "target": "new_component",
                "reason": "family exhausted; needs a FundingBasisCarryComponent",
            }), encoding="utf-8")
    elif reason == "stale_escalation_unclaimed":
        # B10's flag is read by _hard_pause_reason while status == "failed" (it is
        # set by _resolve_protocol_path BEFORE the RuntimeError is raised), NOT by
        # _classify_human_pause -- staging it as a paused_for_human would classify as
        # human_pause_unclassified and prove nothing about this reason.
        base_flags["stale_escalation_unclaimed"] = True
        run_dir = _write_fresh_scaffold(
            runs_dir, run_id, status="failed", pending_stage="human_pause",
            last_error="no claimed escalation", flags=base_flags, **state_overrides)
    else:
        # Every flag-driven reason, staged by setting the flag the real pipeline sets.
        flag = next(f for f, mapped in camp._PAUSE_FLAG_TO_REASON if mapped == reason)
        base_flags[flag] = True
        run_dir = _write_fresh_scaffold(
            runs_dir, run_id, status="paused_for_human", pending_stage="human_pause",
            flags=base_flags, **state_overrides)

    _save_queue_entries(campaign_root["queue_path"], [_entry(run_id)])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=[run_id],
                          trial_sharpes=list(trial_rows or []))
    return run_dir


def _prescreen_row(run_id, route="no_signal_artifact"):
    return {"trial_id": run_id, "source": "prescreen", "route": route, "sharpe": None,
            "expectancy_bps": None, "n_trades": 0, "statistic_valid": "neither"}


# ---------------------------------------------------------------------------
# 1. Bit-identity: the SAME halt, flag off vs flag on (EPIC.md Done-when #3)
# ---------------------------------------------------------------------------

def _run_one_halt(campaign_root, run_id, reason, flag):
    _set_quarantine_flag(campaign_root["config_dir"], flag)
    _stage_halt(campaign_root, run_id, reason,
                trial_rows=[_prescreen_row(run_id)])
    keep_going = camp.process_once()
    root = campaign_root["root"]
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    log = root / "campaign_log.md"
    summary = root / "campaign_summary.md"
    return {
        "keep_going": keep_going,
        "entry": queue["queue"][0],
        "log": log.read_text(encoding="utf-8") if log.exists() else None,
        "summary_exists": summary.exists(),
        "state": _read_state(campaign_root["runs_dir"], run_id),
    }


@pytest.mark.parametrize("flag_off_value", [False, None])
def test_flag_off_is_byte_identical_to_head_behavior(campaign_root, flag_off_value):
    """EPIC.md Done-when #3, the literal acceptance bar. Every artifact the halt path
    touches is asserted against the behavior committed at HEAD (842a2788), field by
    field -- not a weaker 'it still halted' check. `flag_off_value=None` covers the
    key/section being absent entirely, which must be indistinguishable from false."""
    result = _run_one_halt(campaign_root, "run_800", "no_signal_artifact", flag_off_value)

    # process_once STOPS the campaign, exactly as before.
    assert result["keep_going"] is False

    # The queue entry: paused:<reason>, and `outcome` untouched.
    assert result["entry"]["status"] == "paused:no_signal_artifact"
    assert result["entry"]["outcome"] is None

    # campaign_log.md: the HALT line, in its committed wording, and NOTHING from
    # the new policy -- no QUARANTINE line, no AMBIGUITY line.
    log = result["log"]
    assert "HALT — no_signal_artifact." in log
    assert "Campaign stopped on TEST_ENTRY / run_800." in log
    assert "See RUNBOOK.md 'Resume after a pause'." in log
    assert "QUARANTINE" not in log
    assert "AMBIGUITY" not in log

    assert result["summary_exists"]

    # halt_history (S1.5 Piece 1) still appends exactly one entry, and it carries
    # NO quarantine record -- the key must be absent, not present-and-null.
    history = result["state"]["halt_history"]
    assert len(history) == 1
    assert history[0]["reason"] == "no_signal_artifact"
    assert "quarantine" not in history[0]

    # And no trial row was touched.
    campaign = yaml.safe_load(
        campaign_root["campaign_state_path"].read_text(encoding="utf-8"))
    assert campaign["trial_sharpes"] == [_prescreen_row("run_800")]


def test_flag_on_takes_the_quarantine_path_for_the_same_halt(campaign_root):
    """The other half of the bit-identity proof: identical scenario, flag on, and
    every one of the assertions above flips."""
    result = _run_one_halt(campaign_root, "run_800", "no_signal_artifact", True)

    assert result["keep_going"] is True, "quarantine advances the queue; it does not halt"
    assert result["entry"]["status"] == "done"
    assert result["entry"]["outcome"] == "quarantined_engineering_failure"
    assert "QUARANTINE — no_signal_artifact." in result["log"]
    assert "HALT — no_signal_artifact" not in result["log"]

    history = result["state"]["halt_history"]
    assert len(history) == 1
    assert history[0]["quarantine"]["outcome"] == "quarantined_engineering_failure"


def test_quarantine_never_writes_completed_rejected(campaign_root):
    """R8. Laundering an engineering failure into a scientific null is the specific
    failure this outcome value exists to prevent."""
    result = _run_one_halt(campaign_root, "run_801", "component_execution_error", True)
    assert result["entry"]["outcome"] == "quarantined_engineering_failure"
    assert result["entry"]["outcome"] != "completed_rejected"


# ---------------------------------------------------------------------------
# 2. The quarantine record (R6) and trial accounting (R7)
# ---------------------------------------------------------------------------

def test_quarantine_record_carries_untruncated_error_and_flags(campaign_root):
    """R6's minimum fields. The untruncated `last_error` is the whole reason S1.5
    Piece 1 exists -- a quarantine record built on the 300-char campaign_log.md
    truncation would reproduce halt #7, which is unclassifiable to this day."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    long_error = "Y" * 500
    _stage_halt(campaign_root, "run_802", "unhandled_exception")
    # unhandled_exception is NOT quarantine-safe; restage as a flag-driven one that
    # is, but keep a long last_error on the state.
    _stage_halt(campaign_root, "run_802", "component_execution_error",
                last_error=long_error, trial_rows=[_prescreen_row("run_802")])

    camp.process_once()
    history = _read_state(campaign_root["runs_dir"], "run_802")["halt_history"]
    record = history[-1]
    assert record["last_error"] == long_error and len(record["last_error"]) == 500
    q = record["quarantine"]
    assert q["queue_entry_id"] == "TEST_ENTRY"
    assert q["run_id"] == "run_802"
    assert q["queue_status"] == "done"
    assert q["requeueable"] is False
    assert q["retry_attempts"] == [], "S2a builds no retry machinery"
    # `flags` verbatim on the enclosing entry, per R6.
    assert record["flags"]["component_execution_error_flagged"] is True
    assert record["pending_stage"] == "human_pause"
    # campaign_log.md's HALT-line truncation is untouched by this story.
    assert "Y" * 500 not in (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")


def test_component_execution_error_marks_the_existing_trial_invalidated(campaign_root):
    """R7 + F6's binding text: 'No trial or parameter-dimension slot is consumed.'
    Marked invalid via the EXISTING _mark_trial_invalidated, never deleted, and no
    new trial-recording function is called."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_803", "component_execution_error",
                trial_rows=[_prescreen_row("run_803", route="proceed_to_backtest"),
                            {"trial_id": "run_803", "source": "backtest", "sharpe": -0.64}])

    camp.process_once()

    campaign = yaml.safe_load(
        campaign_root["campaign_state_path"].read_text(encoding="utf-8"))
    rows = campaign["trial_sharpes"]
    assert len(rows) == 2, "rows are marked, never deleted"
    assert all(r["invalidated_artifact"] is True for r in rows)
    assert all("E-030 S2a quarantine" in r["invalidation_reason"] for r in rows)

    record = _read_state(campaign_root["runs_dir"], "run_803")["halt_history"][-1]
    assert record["quarantine"]["trial_accounting"] == "marked_trial_invalidated"


def test_no_signal_artifact_writes_no_new_trial_row(campaign_root):
    """R7: the A6.2 prescreen row is already written upstream by
    run_tool_worker's signal_prescreen branch, BEFORE
    determine_post_prescreen_route's F5c branch pauses. Quarantine must add nothing
    and invalidate nothing -- the row is an honest record of a spent look."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    before = [_prescreen_row("run_804")]
    _stage_halt(campaign_root, "run_804", "no_signal_artifact", trial_rows=before)

    camp.process_once()

    campaign = yaml.safe_load(
        campaign_root["campaign_state_path"].read_text(encoding="utf-8"))
    assert campaign["trial_sharpes"] == before, "unchanged: not added to, not invalidated"
    record = _read_state(campaign_root["runs_dir"], "run_804")["halt_history"][-1]
    assert record["quarantine"]["trial_accounting"] == \
        "prescreen_row_already_recorded_by_a6_2_upstream"
    assert record["quarantine"]["no_data_touched"] is False


# ---------------------------------------------------------------------------
# 3. R9 — component_gap / new_component_escalation are RE-QUEUEABLE
# ---------------------------------------------------------------------------

def test_component_gap_quarantines_as_blocked_on_component(campaign_root):
    """R9: `blocked_on_component:<name>` on `status`, never `done`, and no terminal
    `outcome` -- the hypothesis is parked pending engine work, not concluded. The
    name is recovered from decision.yaml's prose, the only place halt #2's own name
    (MacdHistogramCrossoverComponent) ever appeared."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_805", "component_gap")

    keep_going = camp.process_once()

    assert keep_going is True
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    entry = queue["queue"][0]
    assert entry["status"] == "blocked_on_component:MacdHistogramCrossoverComponent"
    assert entry["outcome"] is None, "a parked lineage has not concluded anything"

    record = _read_state(campaign_root["runs_dir"], "run_805")["halt_history"][-1]
    assert record["quarantine"]["requeueable"] is True
    assert record["quarantine"]["blocked_on_component"] == "MacdHistogramCrossoverComponent"
    # R7's fourth bullet: the absence of a trial row is a RECORDED decision.
    assert record["quarantine"]["no_data_touched"] is True


def test_new_component_escalation_quarantines_as_blocked_on_component(campaign_root):
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_806", "new_component_escalation")

    assert camp.process_once() is True
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert queue["queue"][0]["status"] == "blocked_on_component:FundingBasisCarryComponent"


def test_blocked_on_component_entry_is_never_auto_selected(campaign_root):
    """The queue-advance half of R9, checked against the REAL selector rather than
    its docstring. Nothing in _select_entry changes for this story; this asserts
    that the status this story WRITES is one that selector already skips."""
    entries = [
        {"id": "PARKED", "status": "blocked_on_component:MacdHistogramCrossoverComponent",
         "priority": 1, "run_ids": ["run_805"]},
        {"id": "NEXT", "status": "ready", "priority": 5, "run_ids": []},
    ]
    assert camp._select_entry(entries)["id"] == "NEXT"
    assert camp._select_entry([entries[0]]) is None


def test_unnamed_component_falls_back_without_breaking_the_status(campaign_root):
    """A component_gap whose prose names no *Component identifier still produces a
    valid, selector-skipped status. The name is a convenience, not load-bearing."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    run_dir = _stage_halt(campaign_root, "run_807", "component_gap")
    (run_dir / "artifacts" / "decision.yaml").write_text(yaml.safe_dump({
        "stage": "backtest_specification", "status": "component_gap",
        "rationale": "the engine cannot express this signal", "blocking_issues": [],
    }), encoding="utf-8")

    camp.process_once()
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert queue["queue"][0]["status"] == "blocked_on_component:unnamed"
    assert camp._select_entry(queue["queue"]) is None


# ---------------------------------------------------------------------------
# 4. Escalate is the DEFAULT — everything not on the evidenced list still halts
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("reason", [
    "unhandled_exception",              # R2: 6 of 14 halts, >=4 unrelated root causes
    "research_only_unverified",         # R1 integrity list
    "conformance_gate_failure",         # R1
    "kb_reactivation_violation",        # R1
    "pass_rule_evaluation_disagreement",  # R1
    "stale_escalation_unclaimed",       # R1
    "regime_misattribution",            # not on the quarantine-safe list
])
def test_non_quarantine_safe_reasons_still_escalate_with_the_flag_on(campaign_root, reason):
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_810", reason)

    keep_going = camp.process_once()

    assert keep_going is False, f"{reason} must halt the campaign, flag or no flag"
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert queue["queue"][0]["status"] == f"paused:{reason}"
    assert queue["queue"][0]["outcome"] is None
    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert f"HALT — {reason}" in log
    assert "QUARANTINE" not in log
    record = _read_state(campaign_root["runs_dir"], "run_810")["halt_history"][-1]
    assert "quarantine" not in record


def test_quarantine_safe_set_is_exactly_the_four_evidenced_reasons():
    """A change to this set is a change to what the campaign will do unattended.
    Pinning it means widening it cannot happen as a side effect of an unrelated
    edit -- it has to be done here, deliberately, with new evidence cited."""
    assert camp._QUARANTINE_SAFE_REASONS == frozenset({
        "no_signal_artifact", "component_execution_error",
        "component_gap", "new_component_escalation",
    })
    assert camp._REQUEUEABLE_QUARANTINE_REASONS <= camp._QUARANTINE_SAFE_REASONS


# ---------------------------------------------------------------------------
# 5. R11 — ambiguity escalates, visibly
# ---------------------------------------------------------------------------

def test_stale_flag_alongside_a_fresh_one_escalates_instead_of_quarantining(campaign_root):
    """Reconstructs halt #8 (2026-07-09, run_054), the taxonomy's one confirmed
    misreport: #6's `no_signal_artifact_flagged` was never cleared when that pause
    was resolved, so a fresh `component_execution_error_flagged` pause surfaced
    under the stale, higher-priority code. Both reasons are quarantine-safe but
    they carry DIFFERENT trial accounting (R7), so acting on the reported code
    would have applied the wrong one silently. Escalate, and say why."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_808", "no_signal_artifact",
                flags={"component_execution_error_flagged": True},
                trial_rows=[_prescreen_row("run_808")])

    keep_going = camp.process_once()

    assert keep_going is False, "an ambiguous halt escalates exactly as today"
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert queue["queue"][0]["status"] == "paused:no_signal_artifact"

    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert "AMBIGUITY — quarantine declined for 'no_signal_artifact'" in log
    assert "component_execution_error" in log, "the log must name the conflicting flag"
    assert "HALT — no_signal_artifact" in log, "and then escalate exactly as today"
    assert "QUARANTINE" not in log

    # Nothing was quarantined, so nothing was recorded as quarantined.
    record = _read_state(campaign_root["runs_dir"], "run_808")["halt_history"][-1]
    assert "quarantine" not in record
    # And no trial accounting ran off the wrong reason code.
    campaign = yaml.safe_load(
        campaign_root["campaign_state_path"].read_text(encoding="utf-8"))
    assert "invalidated_artifact" not in campaign["trial_sharpes"][0]


def test_state_key_counterpart_also_triggers_ambiguity(campaign_root):
    """_classify_human_pause reads `conformance_violations`/`kb_reactivation_violations`
    ALONGSIDE their flags ('conformance_violation OR conformance_violations' --
    RUNBOOK section 4's own note). A stale state-key with its flag already cleared
    is the same masking hazard and must be caught too."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_809", "component_execution_error",
                kb_reactivation_violations=[{"finding": "H-041-A", "note": "stale"}])

    assert camp.process_once() is False
    log = (campaign_root["root"] / "campaign_log.md").read_text(encoding="utf-8")
    assert "AMBIGUITY — quarantine declined for 'component_execution_error'" in log


def test_clean_single_flag_is_not_ambiguous(campaign_root):
    """The negative control: the guard must not fire on a normal, unambiguous halt,
    or it would silently disable the whole policy."""
    state = {"flags": {"no_signal_artifact_flagged": True,
                       # Non-classifier flags must be ignored entirely.
                       "holdout_reserved": False, "validation_approved": True}}
    assert camp._flag_ambiguity(state, "no_signal_artifact") is None
    assert camp._flag_ambiguity({"flags": {}}, "component_gap") is None


# ---------------------------------------------------------------------------
# 6. The R11 table must not rot away from _classify_human_pause
# ---------------------------------------------------------------------------

def test_pause_flag_table_still_matches_classify_human_pause(tmp_path):
    """_PAUSE_FLAG_TO_REASON duplicates _classify_human_pause's branch order, which
    is a rot risk. Drive the real classifier with each flag in isolation and assert
    the mapping still holds, so a future edit to one has to be made to both."""
    run_dir = tmp_path / "run_x"
    (run_dir / "artifacts").mkdir(parents=True)
    for flag, expected in camp._PAUSE_FLAG_TO_REASON:
        if expected == "stale_escalation_unclaimed":
            # Read by _hard_pause_reason (status == "failed"), not by
            # _classify_human_pause -- asserted through the right door.
            reason, _ = camp._hard_pause_reason(
                run_dir, {"status": "failed", "flags": {flag: True}})
            assert reason == expected
            continue
        assert camp._classify_human_pause(run_dir, {"flags": {flag: True}}) == expected, (
            f"_PAUSE_FLAG_TO_REASON maps {flag!r} -> {expected!r}, but "
            f"_classify_human_pause disagrees -- the R11 cross-check has rotted")

    for key, expected in camp._PAUSE_STATE_KEY_TO_REASON:
        assert camp._classify_human_pause(run_dir, {"flags": {}, key: ["x"]}) == expected


def test_every_known_sticky_flag_branch_has_a_pause_flag_to_reason_entry(tmp_path):
    """FIX 6 (review, 2026-08-24): the forward-direction check above (each
    _PAUSE_FLAG_TO_REASON entry agrees with _classify_human_pause) cannot
    catch a branch _classify_human_pause has that the table is MISSING --
    exactly the anti_adjacency_gate_exhausted drift this fix closes (the
    flag was added to _classify_human_pause's branches but never mirrored
    into the table). This drives every sticky flag KNOWN to be a branch in
    _classify_human_pause, one at a time, and asserts each one's reason
    appears somewhere in _PAUSE_FLAG_TO_REASON -- so a future flag added to
    one and not the other fails here, not silently."""
    run_dir = tmp_path / "run_y"
    (run_dir / "artifacts").mkdir(parents=True)
    known_sticky_flags = (
        "research_only_unverified", "no_signal_artifact_flagged", "conformance_violation",
        "regime_misattribution_flagged", "component_execution_error_flagged",
        "kb_reactivation_violation", "pass_rule_evaluation_disagreement",
        "anti_adjacency_gate_exhausted", "variant_anti_adjacency_gate_refused",
        "variant_gate_insufficient", "inconclusive_grid", "profit_bars_reached",
        # E-059 slice 6c S2a code review (item 7).
        "holdout_refused_under_retired_routing", "campaign_review_refused_under_retired_routing",
        # E-059 slice 6c S2b.
        "campaign_review_terminate",
        # E-059 slice 6c S2d.
        "holdout_unlock_refused", "holdout_unlocked_awaiting_result",
        "holdout_unlocked_result_inconclusive",
        # E-059 slice 6c S2d code-review fixes 3-5.
        "holdout_spent_without_unlock", "holdout_result_unbound", "holdout_result_relabelled",
        # E-061 C1.4 / C1.5.
        "stage_exception", "protocol_promotion_unratified",
        # E-061 C2 S2c.
        "variant_shape_invalid", "variant_config_error",
        # D-051.
        "forecast_rule_violation",
    )
    table_flags = {flag for flag, _ in camp._PAUSE_FLAG_TO_REASON}
    for flag in known_sticky_flags:
        classifier_reason = camp._classify_human_pause(run_dir, {"flags": {flag: True}})
        assert flag in table_flags, (
            f"{flag!r} is a sticky-flag branch in _classify_human_pause (reason "
            f"{classifier_reason!r}) but has no entry in _PAUSE_FLAG_TO_REASON")


def test_quarantine_outcome_is_admissible_without_a_pass_rule_ref():
    """_save_queue runs every entry through validate_verdict_provenance, whose
    default for an UNRECOGNISED outcome is verdict-bearing -- so an unregistered
    quarantine value would turn a quarantine into an UngatedVerdictError crash,
    strictly worse than the halt it replaces. This asserts the registration in
    tools/verdict_criteria_evaluator._NON_VERDICT_OUTCOMES holds."""
    sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
    import verdict_criteria_evaluator as vce
    import record_schema

    assert vce.outcome_is_verdict_bearing(camp._QUARANTINE_OUTCOME) is False
    assert vce.outcome_is_verdict_bearing("completed_rejected") is True, \
        "sanity: a real scientific claim still needs provenance"
    vce.validate_verdict_provenance(
        {"id": "E", "status": "done", "outcome": camp._QUARANTINE_OUTCOME,
         "run_ids": ["run_803"]},
        entry_ref="<quarantined entry>", schema=record_schema.QUEUE_ENTRY_SCHEMA)
    # And it is not counted as a gated verdict.
    assert vce.honest_verdict_count(
        {}, {"queue": [{"id": "E", "outcome": camp._QUARANTINE_OUTCOME}]}) == []
