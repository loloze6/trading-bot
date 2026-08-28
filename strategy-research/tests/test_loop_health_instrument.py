"""
E-030 S3 — the loop-health instrument + R4 repeat-escalation (`workflow/run_campaign.py`),
2026-08-22.

SCOPE, STATED FIRST BECAUSE THE EPIC'S OWN WORDING IS WIDER THAN WHAT EXISTS.
EPIC.md Done-when #2 says the block is "consumed by run_campaign.py itself to decide
retry-vs-escalate at the next halt". There is no retry to decide between: S2b is
unbuilt (taxonomy R2 — the single evidenced retry-safe signature is an exact string
match already handled at the STAGE level in `_invoke_agent_with_yaml_retry`, ledger
A11). The auto-action that DOES exist is S2a's quarantine, so the decision wired up
and tested here is **quarantine-vs-escalate**, via taxonomy R4 extended from retry to
quarantine. Nothing in this file tests retry, and that absence is deliberate.

WHAT IS PROVEN HERE
  1. The re-implemented pairing algorithm reproduces `measure_halt_cost.py` EXACTLY
     against the real, tracked `campaign_record/campaign_log.md` — 17 halts, 129.8 h,
     median 1.81 h, and the taxonomy's own reason-code tally. A known-answer test
     against the S1 artifact, not a self-consistent one. (Rebaselined 2026-08-28
     from 14/127.0/1.98 by RE-RUNNING measure_halt_cost.py and regenerating
     measured_halt_cost.txt, so both sides stay independently derived.)
  2. The emitted block's shape: the mandated keys, TWO cause buckets (never three),
     null rather than a flattering 0.0 on a degenerate denominator, and the two
     different denominators disclosed rather than silently conflated.
  3. `_write_loop_health` fires on every `process_once()` outcome — halt, quarantine
     and DONE — and is a pure re-derivation (deleting the file loses nothing).
  4. R4: the repeat check fires EXACTLY on the evidenced scenario (two consecutive
     `component_execution_error` halts on the same run — halts #13/#14 on run_059)
     and on nothing else. Four negative controls, one per way "in a row" can fail.
  5. Ordering: the repeat check runs AFTER R11's ambiguity check and never overrides
     it.
  6. Gating: `orchestrator.halt_policy.quarantine_enabled` gates BOTH, and with it
     off the repeat branch is structurally unreachable.

Fixture pattern (`campaign_root`, `_write_fresh_scaffold`, `_stage_halt`) reused from
tests/test_halt_quarantine_policy.py, itself from test_k4_routing_registration.py's
hermetic setup: nothing here touches the real repository except the one explicitly
read-only known-answer test in section 1, which passes an independently-constructed
path and never goes through the patched globals.
"""
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_campaign as camp  # noqa: E402

from test_halt_quarantine_policy import (  # noqa: E402
    _prescreen_row, _read_state, _set_quarantine_flag, _stage_halt, campaign_root,
)

# `campaign_root` is imported for its fixture effect; naming it keeps linters quiet.
__all__ = ["campaign_root"]

REPO_STRATEGY_RESEARCH = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# 1. Known-answer: the re-implementation reproduces the S1 artifact exactly
# ---------------------------------------------------------------------------

def test_pairing_reproduces_measured_halt_cost_txt():
    """`artifacts/measure_halt_cost.py` is a flat script and cannot be imported, so
    its algorithm was re-implemented as `_pair_halts_with_downtime`. A
    re-implementation that quietly disagrees with the artifact it is meant to be
    cross-checkable against is worse than no instrument, so this asserts the
    artifact's own published numbers, verbatim:

        halts                    : 17
        total recorded downtime  : 129.8 h
        median halt downtime     : 1.81 h

    REBASELINED 2026-08-28 (was 14 / 127.0 h / 1.98 h, measured 2026-08-23).
    NOT a silent re-pin: `measure_halt_cost.py` was re-run against the current
    log and `measured_halt_cost.txt` regenerated from that run, so the two
    sides of this cross-check were re-derived independently and still agree.
    The original 14 rows are byte-identical; the three additions are this
    session's own halts while getting run_060 through the pipeline --
    unhandled_exception (0.77 h), stale_escalation_unclaimed (0.12 h) and
    conformance_gate_failure (1.99 h) on 2026-08-27. The median moved only
    because the count went even->odd.

    Read-only, and via an INDEPENDENTLY constructed path (the conftest autouse guard
    redirects `camp.CAMPAIGN_LOG_PATH` to a sandbox by default — that redirection is
    correct and is not bypassed here; the path is simply passed in)."""
    log_path = REPO_STRATEGY_RESEARCH / "campaign_record" / "campaign_log.md"
    assert log_path.exists(), "the campaign's primary record is tracked; it should be here"

    events = camp._parse_campaign_log_events(log_path)
    halts = camp._pair_halts_with_downtime(events)

    assert len(halts) == 17
    known = sorted(h["downtime_hours"] for h in halts if h["downtime_hours"] is not None)
    assert len(known) == 17, "every halt in the record has a successor event"
    assert round(sum(known), 1) == 129.8
    assert round(known[len(known) // 2], 2) == 1.81

    # And the reason-code tally the taxonomy reconciles against ("unhandled_exception 7,
    # component_execution_error 3, no_signal_artifact 2, kb_reactivation_violation 2,
    # component_gap 1, stale_escalation_unclaimed 1, conformance_gate_failure 1 --
    # 17 of 17"). The last three are 2026-08-27 additions from the run_060 session;
    # stale_escalation_unclaimed and conformance_gate_failure are NEW reason codes,
    # both raised by gates doing their job rather than by defects in the loop.
    tally = {}
    for h in halts:
        tally[h["reason"]] = tally.get(h["reason"], 0) + 1
    assert tally == {
        "unhandled_exception": 7, "component_execution_error": 3,
        "no_signal_artifact": 2, "kb_reactivation_violation": 2, "component_gap": 1,
        "stale_escalation_unclaimed": 1, "conformance_gate_failure": 1,
    }


def test_dry_run_lines_are_excluded(tmp_path):
    """`dry_run_verify()` writes HALT-shaped lines with zero campaign meaning.
    Counting them would inflate the halt count with rehearsals — which is exactly
    why measure_halt_cost.py skips them, and why this does too."""
    log = tmp_path / "log.md"
    log.write_text(
        "- 2026-07-06T14:00:00Z LAUNCH E1 -> run_001\n"
        "- 2026-07-06T15:00:00Z [DRY RUN] HALT — no_signal_artifact. Campaign stopped.\n"
        "- 2026-07-06T16:00:00Z HALT — component_gap. Campaign stopped on E1 / run_001.\n"
        "- 2026-07-06T18:00:00Z RESUME E1 / run_001\n"
        "not a log line at all\n",
        encoding="utf-8")
    halts = camp._pair_halts_with_downtime(camp._parse_campaign_log_events(log))
    assert [h["reason"] for h in halts] == ["component_gap"]
    assert halts[0]["downtime_hours"] == pytest.approx(2.0)


def test_final_halt_downtime_is_null_not_zero(tmp_path):
    """A halt with no successor event has UNKNOWN downtime. Reporting 0.0 would
    understate the total in the flattering direction — the direction this repo's own
    'fail loud, not flattering' rule exists to forbid."""
    log = tmp_path / "log.md"
    log.write_text(
        "- 2026-07-06T14:00:00Z LAUNCH E1 -> run_001\n"
        "- 2026-07-06T16:00:00Z HALT — unhandled_exception: boom. Campaign stopped.\n",
        encoding="utf-8")
    halts = camp._pair_halts_with_downtime(camp._parse_campaign_log_events(log))
    assert len(halts) == 1
    assert halts[0]["downtime_hours"] is None


# ---------------------------------------------------------------------------
# 2. The emitted block's shape
# ---------------------------------------------------------------------------

def _seed_log(campaign_root, lines: str):
    camp.CAMPAIGN_LOG_PATH.write_text(lines, encoding="utf-8")


def test_block_carries_every_mandated_key(campaign_root):
    _set_quarantine_flag(campaign_root["config_dir"], False)
    _seed_log(campaign_root,
              "- 2026-07-06T14:00:00Z LAUNCH E1 -> run_900\n"
              "- 2026-07-06T15:00:00Z HALT — component_gap. Campaign stopped.\n"
              "- 2026-07-06T17:00:00Z RESUME E1 / run_900\n"
              "- 2026-07-06T18:00:00Z HALT — unhandled_exception: boom. Campaign stopped.\n"
              "- 2026-07-06T19:00:00Z RESUME E1 / run_900\n")

    block = camp._compute_loop_health()

    assert set(block) >= {"computed_at", "span_hours", "halts", "cause_breakdown",
                          "outcomes", "policy"}
    assert set(block["halts"]) >= {"total", "downtime_hours", "downtime_share_pct",
                                   "median_downtime_hours"}
    assert block["halts"]["total"] == 2
    assert block["halts"]["downtime_hours"] == pytest.approx(3.0)
    assert block["halts"]["median_downtime_hours"] == pytest.approx(2.0)
    # span runs first-event -> NOW, so it strictly exceeds the halted hours.
    assert block["span_hours"] > block["halts"]["downtime_hours"]
    assert 0 < block["halts"]["downtime_share_pct"] < 100


def test_cause_breakdown_has_exactly_two_buckets(campaign_root):
    """TWO buckets, not three. A `retry_safe` bucket is not observable from this
    layer: the one evidenced retry-safe signature is resolved inside
    `_invoke_agent_with_yaml_retry` before `_hard_pause_reason` is ever consulted, so
    it never reaches campaign_log.md as a HALT line. A permanently-empty third bucket
    would read as 'retry never helps', the opposite of what the record shows."""
    _set_quarantine_flag(campaign_root["config_dir"], False)
    _seed_log(campaign_root,
              "- 2026-07-06T14:00:00Z LAUNCH E1 -> run_900\n"
              "- 2026-07-06T15:00:00Z HALT — component_execution_error: bug. Campaign stopped.\n"
              "- 2026-07-06T16:00:00Z RESUME E1\n"
              "- 2026-07-06T17:00:00Z HALT — component_execution_error: bug. Campaign stopped.\n"
              "- 2026-07-06T18:00:00Z RESUME E1\n"
              "- 2026-07-06T19:00:00Z HALT — kb_reactivation_violation. Campaign stopped.\n"
              "- 2026-07-06T20:00:00Z RESUME E1\n")

    breakdown = camp._compute_loop_health()["cause_breakdown"]

    assert set(breakdown) == {"quarantine_safe", "escalate"}
    assert "retry_safe" not in breakdown
    assert breakdown["quarantine_safe"]["component_execution_error"] == {
        "count": 2, "downtime_hours": pytest.approx(2.0)}
    assert breakdown["escalate"]["kb_reactivation_violation"]["count"] == 1
    # Bucket membership is _QUARANTINE_SAFE_REASONS, not a second hand-kept list.
    assert set(breakdown["quarantine_safe"]) <= camp._QUARANTINE_SAFE_REASONS
    assert not set(breakdown["escalate"]) & camp._QUARANTINE_SAFE_REASONS


def test_degenerate_inputs_report_null_not_a_flattering_zero(campaign_root):
    """An empty log must not produce '0.0% of the span was halted'. This file is read
    when the loop is UNHEALTHY; a silent zero is the worst possible default."""
    _set_quarantine_flag(campaign_root["config_dir"], False)
    _seed_log(campaign_root, "")

    block = camp._compute_loop_health()

    assert block["span_hours"] is None
    assert block["halts"]["total"] == 0
    assert block["halts"]["downtime_share_pct"] is None
    assert block["halts"]["median_downtime_hours"] is None


def test_outcomes_split_comes_from_halt_history_and_discloses_its_denominator(campaign_root):
    """A quarantined halt writes a QUARANTINE line, NOT a HALT line, so it can never
    appear in `halts.total`. The outcome split is therefore derived from halt_history,
    which spans both — and the block says so instead of leaving a reader to discover
    that two numbers they expect to reconcile do not."""
    _set_quarantine_flag(campaign_root["config_dir"], False)
    _seed_log(campaign_root,
              "- 2026-07-06T14:00:00Z LAUNCH E1 -> run_900\n"
              "- 2026-07-06T15:00:00Z HALT — unhandled_exception: boom. Campaign stopped.\n"
              "- 2026-07-06T16:00:00Z RESUME E1\n")
    runs_dir = campaign_root["runs_dir"]
    (runs_dir / "run_900" / "artifacts").mkdir(parents=True)
    (runs_dir / "run_900" / "pipeline_state.yaml").write_text(yaml.safe_dump({
        "run_id": "run_900",
        "halt_history": [
            {"reason": "component_execution_error", "quarantine": {"policy": "x"}},
            {"reason": "unhandled_exception"},
            {"reason": "no_signal_artifact", "quarantine": {"policy": "x"}},
        ],
    }), encoding="utf-8")

    block = camp._compute_loop_health()

    assert block["outcomes"]["auto_recovered"] == 2
    assert block["outcomes"]["escalated"] == 1
    assert block["outcomes"]["halt_history_records"] == 3
    assert block["halts"]["total"] == 1, "log-derived; the two quarantines are not here"
    # The disclosure is load-bearing, not decoration: a reader who assumes these two
    # reconcile will conclude halts went missing. Both notes must say they don't.
    assert "does not equal halts.total" in block["outcomes"]["denominator_note"].lower()
    assert "not counted here" in block["halts"]["denominator_note"].lower()


def test_instrument_counts_the_r4_population_with_the_decision_s_own_predicate(campaign_root):
    """The instrument and the decision must not drift, so both run through
    `_repeat_quarantine`. Two consecutive quarantined `component_execution_error`
    entries (halts #13/#14's shape) is ONE repeat pair; the third, different reason
    adds none."""
    _set_quarantine_flag(campaign_root["config_dir"], False)
    _seed_log(campaign_root, "")
    runs_dir = campaign_root["runs_dir"]
    (runs_dir / "run_059" / "artifacts").mkdir(parents=True)
    (runs_dir / "run_059" / "pipeline_state.yaml").write_text(yaml.safe_dump({
        "run_id": "run_059",
        "halt_history": [
            {"reason": "component_execution_error", "quarantine": {"policy": "x"}},
            {"reason": "component_execution_error", "quarantine": {"policy": "x"}},
            {"reason": "no_signal_artifact", "quarantine": {"policy": "x"}},
        ],
    }), encoding="utf-8")

    assert camp._compute_loop_health()["outcomes"]["repeat_quarantine_escalations"] == 1


def test_policy_block_states_retry_is_unbuilt(campaign_root):
    """The instrument must not let a reader infer a retry-vs-escalate decision exists.
    S2b is unbuilt and the emitted file says so in its own words."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _seed_log(campaign_root, "")
    policy = camp._compute_loop_health()["policy"]
    assert policy["retry_enabled"] is False
    assert policy["quarantine_enabled"] is True
    assert sorted(policy["quarantine_safe_reasons"]) == sorted(camp._QUARANTINE_SAFE_REASONS)


# ---------------------------------------------------------------------------
# 3. Wiring: written on every process_once() outcome, and purely re-derived
# ---------------------------------------------------------------------------

def _loop_health_path(campaign_root) -> Path:
    return campaign_root["root"] / "campaign_record" / "loop_health.yaml"


def test_written_on_the_escalate_halt_path(campaign_root):
    _set_quarantine_flag(campaign_root["config_dir"], False)
    _stage_halt(campaign_root, "run_910", "unhandled_exception")

    assert camp.process_once() is False

    block = yaml.safe_load(_loop_health_path(campaign_root).read_text(encoding="utf-8"))
    # The halt that JUST happened is in the numbers — not one step stale. This is why
    # the call sits at the END of each branch rather than beside _regenerate_summary.
    assert block["halts"]["total"] == 1
    assert block["cause_breakdown"]["escalate"]["unhandled_exception"]["count"] == 1
    assert block["outcomes"]["escalated"] == 1


def test_written_on_the_quarantine_path(campaign_root):
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_911", "component_execution_error",
                trial_rows=[_prescreen_row("run_911")])

    assert camp.process_once() is True

    block = yaml.safe_load(_loop_health_path(campaign_root).read_text(encoding="utf-8"))
    assert block["halts"]["total"] == 0, "a quarantine writes QUARANTINE, not HALT"
    assert block["outcomes"]["auto_recovered"] == 1
    assert block["outcomes"]["escalated"] == 0


def test_written_on_the_done_path(campaign_root):
    """The DONE branch is one of `_regenerate_summary`'s own call sites, so the
    instrument fires there too — a healthy step refreshes the block just as a halt
    does, or `computed_at` would only ever advance on bad news."""
    _set_quarantine_flag(campaign_root["config_dir"], False)
    from test_halt_quarantine_policy import (_entry, _save_queue_entries,
                                             _write_campaign_state, _write_fresh_scaffold)
    # `completed_reframed` (not `completed_rejected`) so _save_queue's provenance gate
    # is satisfied without inventing a pass_rule_evaluation_ref: a lineage marker
    # asserts nothing about the hypothesis. The DONE branch is identical either way.
    _write_fresh_scaffold(campaign_root["runs_dir"], "run_912",
                          status="completed", pending_stage="completed_reframed")
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_912")])
    _write_campaign_state(campaign_root["campaign_state_path"], runs=["run_912"],
                          trial_sharpes=[])

    assert camp.process_once() is True

    assert _loop_health_path(campaign_root).exists()
    log = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")
    assert "DONE TEST_ENTRY" in log


def test_the_file_is_a_projection_and_deleting_it_loses_nothing(campaign_root):
    """Re-derived from primary records on every call, never accumulated — the same
    posture as campaign_summary.md. Delete it and the next step reproduces it byte
    for byte apart from the wall-clock stamps."""
    _set_quarantine_flag(campaign_root["config_dir"], False)
    _seed_log(campaign_root,
              "- 2026-07-06T14:00:00Z LAUNCH E1 -> run_900\n"
              "- 2026-07-06T15:00:00Z HALT — component_gap. Campaign stopped.\n"
              "- 2026-07-06T17:00:00Z RESUME E1\n")

    first = camp._write_loop_health()
    _loop_health_path(campaign_root).unlink()
    second = camp._write_loop_health()

    volatile = {"computed_at", "span_hours"}
    assert {k: v for k, v in first.items() if k not in volatile} == \
           {k: v for k, v in second.items() if k not in volatile}


# ---------------------------------------------------------------------------
# 4. R4 — the one new decision. Fires on the evidenced scenario, nothing else.
# ---------------------------------------------------------------------------
#
# ADJACENCY SEMANTICS, chosen and stated so the tests below mean something:
# only `halt_history[-1]` — the IMMEDIATELY preceding halt on the same run — is
# consulted, and it must carry BOTH the same reason code AND a `quarantine` key.
# Any other halt in between breaks the chain (the intervening halt is itself
# evidence the situation changed), and a previous same-reason halt that ESCALATED
# does not count (a human already looked at that one; R4's target is the loop
# silently auto-actioning the same fault twice).

def _prior_halt(reason, quarantined=True, ts="2026-07-18T05:38:24+00:00"):
    record = {"timestamp": ts, "reason": reason, "detail": "", "last_error": None,
              "pending_stage": "human_pause", "flags": {}, "completed_stages": [],
              "counters": {}}
    if quarantined:
        record["quarantine"] = {"policy": "E-030 S2a quarantine", "run_id": "run_059"}
    return record


def test_repeat_of_a_quarantined_reason_escalates(campaign_root):
    """THE EVIDENCED SCENARIO. Halts #13 and #14: both `component_execution_error`,
    both on run_059, back to back. #13 was a real engine bug fixed by a human at the
    confirmed site; #14 then needed a state-only human intervention (no commit exists
    in its window) after which the run reached terminal in 2m17s. Quarantining the
    same reason a second time in a row is not recovery — it is laundering a repeating
    fault into an outcome nobody looks at."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_059", "component_execution_error",
                halt_history=[_prior_halt("component_execution_error")],
                trial_rows=[_prescreen_row("run_059")])

    keep_going = camp.process_once()

    assert keep_going is False, "R4: escalate, exactly as an unclassified halt would"
    queue = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))
    assert queue["queue"][0]["status"] == "paused:component_execution_error"
    assert queue["queue"][0]["outcome"] is None

    log = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")
    assert "REPEAT-ESCALATE — quarantine declined for 'component_execution_error'" in log
    assert "R4" in log and "#13/#14" in log, "the log line must name the rule and its evidence"
    assert "HALT — component_execution_error" in log, "and then escalate exactly as today"
    assert "QUARANTINE — " not in log

    # Nothing was quarantined, so nothing was recorded as quarantined...
    history = _read_state(campaign_root["runs_dir"], "run_059")["halt_history"]
    assert len(history) == 2, "the prior record survives; the new one is appended"
    assert "quarantine" not in history[-1]
    # ...and no trial accounting ran off the declined action.
    campaign = yaml.safe_load(
        campaign_root["campaign_state_path"].read_text(encoding="utf-8"))
    assert "invalidated_artifact" not in campaign["trial_sharpes"][0]


def test_first_occurrence_still_quarantines(campaign_root):
    """(a) Only one occurrence so far. The whole point of quarantine is that the
    FIRST one is handled automatically; a check that fired here would delete S2a."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_920", "component_execution_error",
                trial_rows=[_prescreen_row("run_920")])

    assert camp.process_once() is True
    log = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")
    assert "QUARANTINE — component_execution_error" in log
    assert "REPEAT-ESCALATE" not in log


def test_two_different_quarantine_safe_reasons_still_quarantine(campaign_root):
    """(b) DIFFERENT reasons back to back is not R4's situation — R4 is 'same reason
    code twice in a row', and two distinct engineering faults on one run are two
    faults, each of which quarantine handles correctly on its own evidence."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_921", "component_execution_error",
                halt_history=[_prior_halt("no_signal_artifact")],
                trial_rows=[_prescreen_row("run_921")])

    assert camp.process_once() is True
    log = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")
    assert "QUARANTINE — component_execution_error" in log
    assert "REPEAT-ESCALATE" not in log


def test_an_intervening_different_halt_breaks_the_chain(campaign_root):
    """(c) Two same-reason halts with something else in between are not 'in a row'.
    The intervening halt is itself evidence the run's situation changed, so the
    second occurrence is treated as a fresh first — chosen semantics, tested here so
    a future edit to `_repeat_quarantine` cannot change it silently."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_922", "component_execution_error",
                halt_history=[
                    _prior_halt("component_execution_error"),
                    _prior_halt("unhandled_exception", quarantined=False),
                ],
                trial_rows=[_prescreen_row("run_922")])

    assert camp.process_once() is True
    log = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")
    assert "QUARANTINE — component_execution_error" in log
    assert "REPEAT-ESCALATE" not in log


def test_a_previous_same_reason_halt_that_escalated_does_not_count(campaign_root):
    """(d) The `quarantine` key is REQUIRED, not just the reason match. A previous
    same-reason halt that escalated means a human already looked at it and resumed;
    R4's target is the LOOP auto-actioning the same fault twice unattended. Stated
    and pinned because it is the semantics most likely to be 'fixed' by mistake."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_923", "component_execution_error",
                halt_history=[_prior_halt("component_execution_error", quarantined=False)],
                trial_rows=[_prescreen_row("run_923")])

    assert camp.process_once() is True
    assert "REPEAT-ESCALATE" not in camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")


def test_repeat_predicate_in_isolation():
    """The unit-level truth table, independent of process_once's plumbing."""
    same = _prior_halt("component_execution_error")
    assert camp._repeat_quarantine({"halt_history": [same]},
                                   "component_execution_error") is same
    assert camp._repeat_quarantine({}, "component_execution_error") is None
    assert camp._repeat_quarantine({"halt_history": []}, "component_execution_error") is None
    assert camp._repeat_quarantine({"halt_history": [same]}, "no_signal_artifact") is None
    assert camp._repeat_quarantine(
        {"halt_history": [_prior_halt("component_execution_error", quarantined=False)]},
        "component_execution_error") is None
    # A malformed history entry must not raise inside the halt path.
    assert camp._repeat_quarantine({"halt_history": ["not a dict"]},
                                   "component_execution_error") is None


# ---------------------------------------------------------------------------
# 5. Ordering against R11, and the gate
# ---------------------------------------------------------------------------

def test_ambiguity_wins_over_the_repeat_check(campaign_root):
    """Order matters in BOTH directions. An ambiguous halt already escalates for a
    prior and different reason (R11, halt #8's stale-flag fingerprint); if the repeat
    check ran first it would have to duplicate that decision, and a NON-repeating
    ambiguous halt would take the 'clean' path and lose R11's explanation. So R11
    runs first and its line is what appears — the repeat check must not override it."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_930", "no_signal_artifact",
                flags={"component_execution_error_flagged": True},
                halt_history=[_prior_halt("no_signal_artifact")],
                trial_rows=[_prescreen_row("run_930")])

    assert camp.process_once() is False
    log = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")
    assert "AMBIGUITY — quarantine declined for 'no_signal_artifact'" in log
    assert "REPEAT-ESCALATE" not in log, "R11 owns this escalation, not R4"
    assert "HALT — no_signal_artifact" in log


@pytest.mark.parametrize("flag_off_value", [False, None])
def test_the_repeat_branch_is_unreachable_with_quarantine_disabled(campaign_root,
                                                                   flag_off_value):
    """THE GATE DECISION, pinned. `orchestrator.halt_policy.quarantine_enabled` gates
    this check too — no third flag. With quarantine off nothing is ever quarantined,
    so no halt_history entry ever carries a `quarantine` key, so 'cap repeat
    quarantines' is structurally unreachable: a separate toggle would be dead
    configuration the first time anyone read it closely (the `rebalance_threshold`
    trap this repo's own root CLAUDE.md names as a real mistake not to repeat).

    Staged with a quarantine record already present — the only way such a record can
    exist is the flag having been ON earlier — to prove the check does not fire even
    then. Flipping the flag off is a deliberate 'stop auto-actioning' instruction and
    the escalate path is already what it asks for."""
    _set_quarantine_flag(campaign_root["config_dir"], flag_off_value)
    _stage_halt(campaign_root, "run_931", "component_execution_error",
                halt_history=[_prior_halt("component_execution_error")],
                trial_rows=[_prescreen_row("run_931")])

    assert camp.process_once() is False
    log = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")
    assert "REPEAT-ESCALATE" not in log
    assert "QUARANTINE — " not in log
    assert "HALT — component_execution_error" in log
    block = yaml.safe_load(_loop_health_path(campaign_root).read_text(encoding="utf-8"))
    assert block["policy"]["quarantine_enabled"] is False


def test_non_quarantine_safe_reasons_never_reach_the_repeat_check(campaign_root):
    """`unhandled_exception` escalates on R2 grounds long before R4 is consulted, even
    with a matching quarantined predecessor on the record. The repeat check narrows
    quarantine; it must never widen the set of things that halt."""
    _set_quarantine_flag(campaign_root["config_dir"], True)
    _stage_halt(campaign_root, "run_932", "unhandled_exception",
                halt_history=[_prior_halt("unhandled_exception")])

    assert camp.process_once() is False
    log = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")
    assert "REPEAT-ESCALATE" not in log
    assert "HALT — unhandled_exception" in log
