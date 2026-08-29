"""
E-030 S4 — epic-level bit-identity + the classification's regression fixtures
(`workflow/run_campaign.py`), 2026-08-23.

S4's story text asks for two SEPARATE things and this file keeps them separate:

  PART A — "Bit-identity test". EPIC.md Done-when #3's literal bar: *"a test proves
  output is unchanged when every classified failure is disabled (equivalent to
  today's behavior)."*  S2a and S3 each proved this for THEIR OWN story in
  isolation. Nobody had yet proved it for the epic as one claim.

  PART B — "the classification's regression fixture (one historical halt of each
  class, replayed against the policy)". Three fixtures, each built from the S1
  taxonomy's own per-halt evidence — real run IDs, real queue-entry IDs, real
  `last_error` text, real trial rows — rather than from scenarios invented for test
  convenience. `tests/test_halt_quarantine_policy.py` and
  `tests/test_loop_health_instrument.py` already carry plenty of the invented kind
  and they are the right tool for exercising branch logic; this file's job is the
  evidence-grounded kind, so that a future refactor that silently reclassifies a
  REAL measured halt fails a test that cites the measurement.

---------------------------------------------------------------------------
PART A — what already existed, and the one gap this closes
---------------------------------------------------------------------------

Audited before writing anything, because duplicating existing coverage under a new
name is not progress:

  * `test_halt_history.py` (S1 Piece 1, `994157ec`) — 3 tests proving
    `halt_history` appends untruncated, accumulates, and fires on the
    refinement-brief-conflict path too.
  * `test_halt_quarantine_policy.py::test_flag_off_is_byte_identical_to_head_behavior`
    (S2a, `83f8f1b0`; parametrized `False` / `None`) — flag-off proven field by
    field for ONE reason (`no_signal_artifact`): return value, queue status,
    `outcome`, the `campaign_log.md` HALT wording, absence of QUARANTINE/AMBIGUITY
    lines, summary regenerated, exactly one `halt_history` entry with no
    `quarantine` key, trial rows untouched.
  * `test_loop_health_instrument.py::test_the_repeat_branch_is_unreachable_with_quarantine_disabled`
    (S3, `5053148e`) — the repeat-escalate branch cannot be entered flag-off.

A CORRECTION TO THIS DISPATCH'S OWN PREMISE, stated because it changes what part A
had left to do. `842a2788` is NOT "the last commit before any of E-030's S1.5/S2a/S3
code existed" — `842a2788` **is** S1.5 Piece 2, and S1 Piece 1's `_append_halt_history`
landed one commit earlier (`994157ec`) and is already present there (3 call sites,
verified with `git show 842a2788:strategy-research/workflow/run_campaign.py`). So
`halt_history` is part of the baseline, not a delta against it, and there was never a
"halt_history half" of the epic-level claim left to prove.

WHAT THE DELTA ACTUALLY IS, established by an AST-level diff of `run_campaign.py`
between `842a2788` and this branch's base `55e812c0` rather than by reading:

    functions added : _apply_trial_accounting, _blocked_component_name,
                      _compute_loop_health, _flag_ambiguity, _iter_halt_histories,
                      _pair_halts_with_downtime, _parse_campaign_log_events,
                      _quarantine_enabled, _repeat_quarantine, _run_has_trial_row,
                      _write_loop_health
    functions removed: (none)
    functions changed: _append_halt_history, process_once

`_append_halt_history`'s change is one optional keyword (`quarantine=None`) whose
default adds no key. `process_once`'s change is (a) the whole S2a block, entirely
inside `if reason in _QUARANTINE_SAFE_REASONS and _quarantine_enabled():`, and
(b) four bare `_write_loop_health()` calls. Nothing else moved, nothing was
reordered. Therefore, flag-off, **the entire epic-level delta versus `842a2788` is
the four `_write_loop_health()` calls**, and `campaign_record/loop_health.yaml` is a
file that did not exist at `842a2788` at all. Its APPEARANCE is expected and is not a
bit-identity violation; what would be a violation is any OTHER byte moving with it.
That is exactly the claim `test_flag_off_whole_tree_matches_842a2788_except_loop_health`
pins, across six reasons rather than S2a's one — and it is pinned by comparing the
FULL recursive sandbox tree, so a future write to a file nobody thought to assert on
is caught by construction rather than by remembering to add an assertion.

`test_flag_off_never_invokes_any_s2a_or_s3_machinery` is the companion: it makes the
monkeypatch in the tree test legitimate instead of assumed, by proving from execution
that flag-off reaches NONE of the six S2a/S3 decision functions.

---------------------------------------------------------------------------
PART B — the three regression fixtures
---------------------------------------------------------------------------

  retry-safe      halt #10 (run_054) / #12 (run_058), `unhandled_exception`,
                  `Claude Code returned an error result: success`
  quarantine-safe halt #13 (run_059, FUNDING_MR_DAILY_RETEST), `component_execution_error`
  must-escalate   halt #4 (run_053, P4_ts_trend), `kb_reactivation_violation`

Every real run whose halt these replay (run_053/054/058/059) has SINCE been resumed
to a post-halt state — verified on disk at fixture-construction time: run_053 is
`active`/`completed_reframed`, run_054 `active`/`completed_refined`, run_058 and
run_059 `rejected`/`completed_rejected`, and all four now read `last_error: None`.
The halt-time snapshots the taxonomy documents no longer exist on disk. Per this
dispatch's explicit STOP, the real run directories are NOT mutated to reconstruct
them; each fixture rebuilds the documented halt state inside the hermetic
`campaign_root` sandbox instead, using the taxonomy's own recorded values. Nothing
here reads or writes anything under `runs/`, `config/campaign_queue.yaml`, or
`local_data/`. The real queue entry `P4_ts_trend` is referenced only as a string
inside a throwaway sandbox queue.
"""

import re
import sys
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_phase1_research as rpr  # noqa: E402
import run_campaign as camp  # noqa: E402

from test_halt_quarantine_policy import (  # noqa: E402
    _entry,
    _prescreen_row,
    _read_state,
    _save_queue_entries,
    _set_quarantine_flag,
    _stage_halt,
    _write_fresh_scaffold,
    campaign_root,
)

# `campaign_root` is imported for its fixture effect; naming it keeps linters quiet.
__all__ = ["campaign_root"]


# ---------------------------------------------------------------------------
# Part A helpers
# ---------------------------------------------------------------------------

# Every wall-clock stamp this pipeline writes, in every shape it writes them:
# campaign_log.md's `- 2026-...Z`, campaign_summary.md's `_Regenerated: ...Z_`,
# halt_history's `datetime.now(timezone.utc).isoformat()` (+00:00 form), and
# loop_health.yaml's `computed_at`. Normalised, not stripped, so a stamp
# DISAPPEARING is still caught as a difference.
_ISO_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|\+00:00)?")

# The S2a/S3 DECISION functions — everything reachable only from inside
# `process_once`'s `if reason in _QUARANTINE_SAFE_REASONS and _quarantine_enabled():`
# block.
#
# TWO DELIBERATE OMISSIONS, both measured rather than assumed:
#   `_quarantine_enabled` — it IS the gate, so flag-off must call it. The test is
#     that nothing PAST it is called.
#   `_compute_loop_health` — it IS reached flag-off, via `_write_loop_health`, and
#     that is the one permitted delta (see this module's docstring). It also calls
#     `_repeat_quarantine` itself, read-only, on a synthetic prefix of halt_history
#     to count the R4 population — so the guard below can only be meaningful with
#     `_write_loop_health` neutralised, which is precisely the `842a2788` code path.
#     Its read-only, projection-only nature is pinned elsewhere:
#     `test_loop_health_instrument.py::test_the_file_is_a_projection_and_deleting_it_loses_nothing`
#     plus this file's own whole-tree comparison.
_S2A_DECISION_FUNCTIONS = (
    "_flag_ambiguity",
    "_repeat_quarantine",
    "_blocked_component_name",
    "_apply_trial_accounting",
    "_run_has_trial_row",
)

# One representative per behavioural class the halt path can take, so the tree
# comparison is not a single-scenario claim:
#   the four quarantine-safe reasons (the only ones the flag could ever divert),
#   plus unhandled_exception (R2's escalate-always case, 6 of the 14 halts),
#   plus kb_reactivation_violation (R1's integrity list).
_ALL_HALT_REASONS = [
    "no_signal_artifact",
    "component_execution_error",
    "component_gap",
    "new_component_escalation",
    "unhandled_exception",
    "kb_reactivation_violation",
]


def _build_sandbox(base: Path, monkeypatch) -> dict:
    """A second `campaign_root`, at an explicitly-chosen location.

    The shared `campaign_root` fixture is bound to `tmp_path` and yields exactly one
    sandbox per test; the tree comparison needs two live in the same test so the two
    code paths can be run back to back against identical starting conditions. This
    reproduces that fixture's setup verbatim — same globals, same stubs — differing
    only in taking its root as an argument.
    """
    runs_dir = base / "runs"
    runs_dir.mkdir(parents=True)
    config_dir = base / "config"
    config_dir.mkdir()
    queue_path = config_dir / "campaign_queue.yaml"
    queue_path.write_text(yaml.safe_dump({"queue": []}), encoding="utf-8")
    campaign_state_path = base / "campaign_state.yaml"

    monkeypatch.setattr(camp, "ROOT", base)
    monkeypatch.setattr(camp, "QUEUE_PATH", queue_path)
    monkeypatch.setattr(camp, "CAMPAIGN_LOG_PATH", base / "campaign_log.md")
    monkeypatch.setattr(camp, "CAMPAIGN_SUMMARY_PATH", base / "campaign_summary.md")
    monkeypatch.setattr(camp, "BASELINE_PATH", config_dir / "campaign_baseline_runs.yaml")
    monkeypatch.setattr(rpr, "ROOT", base)
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", campaign_state_path)
    monkeypatch.setattr(camp, "setup_run", lambda run_id: _write_fresh_scaffold(runs_dir, run_id))

    return {
        "root": base,
        "runs_dir": runs_dir,
        "queue_path": queue_path,
        "config_dir": config_dir,
        "campaign_state_path": campaign_state_path,
    }


def _snapshot_tree(root: Path) -> dict:
    """Every file under `root`, wall-clock-normalised. Nothing is filtered by name:
    a file the halt path starts writing that nobody predicted shows up as a new key
    and fails the comparison, which is the point of diffing the tree rather than a
    hand-listed set of artifacts."""
    return {
        p.relative_to(root).as_posix(): _ISO_RE.sub("<TS>", p.read_text(encoding="utf-8"))
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


# ---------------------------------------------------------------------------
# PART A — epic-level bit-identity (EPIC.md Done-when #3)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("reason", _ALL_HALT_REASONS)
def test_flag_off_whole_tree_matches_842a2788_except_loop_health(tmp_path, monkeypatch, reason):
    """The epic-wide claim, as one claim.

    Runs the SAME halt scenario twice into two independent sandboxes:
      A. `_write_loop_health` patched to a no-op. Per the AST diff in this module's
         docstring, that is EXACTLY `842a2788`'s `process_once` when
         `quarantine_enabled` is false — the S2a block is gated off, and the four
         `_write_loop_health()` calls are the only other difference.
      B. the shipped code, unpatched.

    Then compares the FULL recursive file tree. The single permitted difference is
    that B additionally contains `campaign_record/loop_health.yaml`, a file that did
    not exist at `842a2788` in any form. Everything else — `campaign_log.md`,
    `config/campaign_queue.yaml`, `campaign_summary.md`, `campaign_state.yaml`,
    `runs/<id>/pipeline_state.yaml` including its `halt_history` — must be
    byte-identical modulo wall-clock stamps.
    """
    real_write_loop_health = camp._write_loop_health

    baseline = _build_sandbox(tmp_path / "baseline_842a2788", monkeypatch)
    monkeypatch.setattr(camp, "_write_loop_health", lambda: {})
    _set_quarantine_flag(baseline["config_dir"], False)
    _stage_halt(baseline, "run_700", reason, trial_rows=[_prescreen_row("run_700")])
    baseline_keep_going = camp.process_once()
    baseline_tree = _snapshot_tree(baseline["root"])

    head = _build_sandbox(tmp_path / "head", monkeypatch)
    monkeypatch.setattr(camp, "_write_loop_health", real_write_loop_health)
    _set_quarantine_flag(head["config_dir"], False)
    _stage_halt(head, "run_700", reason, trial_rows=[_prescreen_row("run_700")])
    head_keep_going = camp.process_once()
    head_tree = _snapshot_tree(head["root"])

    assert baseline_keep_going is head_keep_going is False

    new_paths = set(head_tree) - set(baseline_tree)
    assert new_paths == {"campaign_record/loop_health.yaml"}, (
        "the ONLY file E-030 may add flag-off is the loop-health projection; "
        f"unexpected new/missing paths for reason={reason}: "
        f"added={sorted(new_paths)} removed={sorted(set(baseline_tree) - set(head_tree))}"
    )

    for path, baseline_text in baseline_tree.items():
        assert head_tree[path] == baseline_text, (
            f"{path} diverged from the 842a2788 code path for reason={reason} — EPIC.md Done-when #3 forbids this"
        )


@pytest.mark.parametrize("reason", _ALL_HALT_REASONS)
def test_flag_off_never_invokes_any_s2a_machinery(campaign_root, monkeypatch, reason):
    """What makes the tree test's no-op patch legitimate rather than assumed.

    With `_write_loop_health` neutralised — i.e. running exactly `842a2788`'s
    `process_once` — every S2a decision function is replaced by one that raises.
    `process_once` must still complete the ordinary escalate halt without touching a
    single one of them, including for the four quarantine-safe reasons, the only ones
    the flag could ever divert. See `_S2A_DECISION_FUNCTIONS` for what is left live
    and why.
    """

    def _forbidden(name):
        def _raise(*args, **kwargs):
            raise AssertionError(
                f"{name} was called with quarantine_enabled off — Done-when #3 says "
                f"flag-off must be equivalent to the pre-E-030 behavior"
            )

        return _raise

    monkeypatch.setattr(camp, "_write_loop_health", lambda: {})
    for name in _S2A_DECISION_FUNCTIONS:
        monkeypatch.setattr(camp, name, _forbidden(name))

    _set_quarantine_flag(campaign_root["config_dir"], False)
    _stage_halt(campaign_root, "run_701", reason)

    assert camp.process_once() is False
    entry = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert entry["status"] == f"paused:{reason}"


# `842a2788`'s own record literal in `_append_halt_history`, read off
# `git show 842a2788:strategy-research/workflow/run_campaign.py`.
_842A2788_HALT_RECORD_KEYS = {
    "timestamp",
    "reason",
    "detail",
    "last_error",
    "pending_stage",
    "flags",
    "completed_stages",
    "counters",
}


def test_append_halt_history_default_record_has_the_842a2788_key_set(campaign_root):
    """`_append_halt_history` is one of only two shared functions whose body changed
    between `842a2788` and this branch's base (the other is `process_once`), and its
    change is a single optional keyword. This pins that the default path still emits
    exactly `842a2788`'s eight-key record — `quarantine` ABSENT, not
    present-and-null, since a null key would change every escalated halt's
    `pipeline_state.yaml` bytes and break Done-when #3 on its own."""
    import inspect

    assert inspect.signature(camp._append_halt_history).parameters["quarantine"].default is None

    run_dir = _write_fresh_scaffold(campaign_root["runs_dir"], "run_702", status="failed", last_error="boom")
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    camp._append_halt_history(run_dir, state, "unhandled_exception", "boom")

    record = _read_state(campaign_root["runs_dir"], "run_702")["halt_history"][-1]
    assert set(record) == _842A2788_HALT_RECORD_KEYS


# ---------------------------------------------------------------------------
# PART B — regression fixtures, one historical halt per class
# ---------------------------------------------------------------------------
#
# Each fixture quotes the S1 taxonomy VERBATIM in its docstring. The taxonomy is the
# only source of truth for what a correct replay outcome is; nothing here classifies
# a halt on its own judgment.
# ---------------------------------------------------------------------------

# --- retry-safe: halts #10 and #12 -----------------------------------------

# `campaign_log.md` lines 57 and 98, verbatim:
#   - 2026-07-09T16:56:17Z HALT — unhandled_exception: Claude Code returned an error
#     result: success. Campaign stopped on P4_ts_trend / run_054. ...
#   - 2026-07-16T14:08:46Z HALT — unhandled_exception: Claude Code returned an error
#     result: success. Campaign stopped on H-041-C-v2 / run_058. ...
_HALT_10_12_ERROR = "Claude Code returned an error result: success"


def test_retry_safe_halt_10_12_is_resolved_before_it_can_become_a_halt(campaign_root, monkeypatch):
    """REGRESSION FIXTURE — class: retry-safe. Halts #10 (run_054) and #12 (run_058).

    Taxonomy #10, verbatim: *"Detail: `Claude Code returned an error result: success`.
    Class: retry-safe — proven, and ALREADY FIXED. `claude_agent_sdk==0.2.82` returns
    `is_error=True` paired with `subtype: "success"`, the SDK falls back to the
    subtype string as the error text. ... Ledger A11 CLOSED, commit `9bf2a4cf`:
    `_invoke_agent_with_yaml_retry` re-invokes the same stage once on an exact string
    match."*  And #12: *"the same SDK defect as #10 ... #10 + #12 = 21.9 h, the
    epic's 'already fixed' figure, reproduced."*

    WHAT "REPLAYING" THIS CLASS MEANS, and why it is not a quarantine/escalate
    assertion. This class is resolved at the STAGE level, before a halt is ever
    logged — S3's own commit message: *"it never reaches campaign_log.md as a HALT
    line at all."*  So the correct outcome to assert is "this never becomes a halt",
    in two halves:

      (a) the stage-level retry still fires on this exact message. Already covered by
          `test_k3_protocol_pinning.py`'s three A11 fixtures
          (`..._recovers_from_sdk_error_result_success`,
          `..._reraises_on_second_sdk_error_result_success`,
          `..._does_not_catch_other_messages`) and NOT duplicated here — this test
          calls the same entry point once, purely to establish the precondition for
          (b) inside this file's own campaign sandbox.

      (b) THE PART THAT WAS MISSING: the campaign layer therefore never classifies
          it. Asserted two ways — the run's state is never left in the shape
          `_hard_pause_reason` halts on, and (the counterfactual that gives the class
          its teeth) had the retry NOT existed, the reason code this would have
          produced is `unhandled_exception`, which is NOT in
          `_QUARANTINE_SAFE_REASONS` and would have escalated for 21.9 h exactly as
          the record shows.
    """
    run_dir = campaign_root["runs_dir"] / "run_054"
    (run_dir / "artifacts").mkdir(parents=True)
    (run_dir / "pipeline_state.yaml").write_text(
        yaml.safe_dump(
            {"run_id": "run_054", "status": "active", "pending_stage": "validation", "flags": {}, "audit_log": {}},
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    deliverable = run_dir / "artifacts" / "decision.yaml"
    deliverable.write_text("status: approve\n", encoding="utf-8")

    calls = {"n": 0}

    async def _sdk_misclassifies_once(stage_name, run_id, retry_context=None):
        calls["n"] += 1
        if calls["n"] == 1:
            raise Exception(_HALT_10_12_ERROR)

    monkeypatch.setattr(rpr, "async_invoke_agent", _sdk_misclassifies_once)
    rpr._invoke_agent_with_yaml_retry("validation", "run_054", run_dir, [deliverable], {})

    # (a) precondition: the stage recovered in-place.
    assert calls["n"] == 2

    # (b) the campaign layer never sees a halt. The state is untouched by the SDK
    # fault: still active, still mid-pipeline, nothing for _hard_pause_reason to fire
    # on.
    state = yaml.safe_load((run_dir / "pipeline_state.yaml").read_text(encoding="utf-8"))
    assert state["status"] == "active"
    assert camp._hard_pause_reason(run_dir, state) is None

    # The counterfactual, which is what makes this a classification fixture rather
    # than a retry test: unresolved, this halt's reason code is `unhandled_exception`
    # — the exact code campaign_log.md recorded twice — and that code escalates.
    would_have_been = camp._hard_pause_reason(
        run_dir, {"status": "failed", "pending_stage": "human_pause", "last_error": _HALT_10_12_ERROR, "flags": {}}
    )
    assert would_have_been == ("unhandled_exception", _HALT_10_12_ERROR)
    assert "unhandled_exception" not in camp._QUARANTINE_SAFE_REASONS, (
        "taxonomy R2: unhandled_exception covers 6 of 14 halts and at least four "
        "unrelated root causes; it must never be quarantine-safe"
    )


# --- quarantine-safe: halt #13 ---------------------------------------------

# `campaign_log.md` line 119, verbatim:
#   - 2026-07-18T05:38:24Z HALT — component_execution_error. Campaign stopped on
#     FUNDING_MR_DAILY_RETEST / run_059. See RUNBOOK.md 'Resume after a pause'.
_HALT_13_ENTRY_ID = "FUNDING_MR_DAILY_RETEST"
_HALT_13_DETAIL = (
    "FundingRateMeanReversionComponent produced avg_forecast=0.0 on all 1,568 "
    "bar-symbol instances at 1d with component_error_count=0"
)
# run_059's two REAL rows in campaign_record/campaign_state.yaml, reproduced with the
# taxonomy-relevant fields. Both exist because the run reached protocol_execution;
# the taxonomy says so explicitly: "run_059 (halts #13/#14) carries both a prescreen
# and a backtest row, so there is generally something to mark."
_RUN_059_TRIAL_ROWS = [
    {
        "trial_id": "run_059",
        "source": "prescreen",
        "route": "proceed_to_backtest",
        "sharpe": None,
        "expectancy_bps": None,
        "n_trades": 0,
        "statistic_valid": "neither",
        "ic_pooled": 0.037802,
        "cost_pass": True,
    },
    {"trial_id": "run_059", "source": "backtest", "sharpe": -0.6375, "n_trades": 0, "statistic_valid": "expectancy"},
]


def test_quarantine_safe_halt_13_quarantines_and_invalidates_run_059s_trials(campaign_root):
    """REGRESSION FIXTURE — class: quarantine-safe. Halt #13
    (2026-07-18T05:38:24Z, `component_execution_error`, run_059,
    queue entry FUNDING_MR_DAILY_RETEST, 10.27 h).

    Taxonomy #13, verbatim: *"What it was: a genuine engine bug, and the most
    expensive kind — silent. `FundingRateMeanReversionComponent` produced
    `avg_forecast=0.0` on all 1,568 bar-symbol instances at 1d with
    `component_error_count=0` — no exception at all. ... Class: quarantine-safe —
    with a mandatory trial-accounting rule. No retry can fix a real engine bug, and
    the queue has no reason to stop. But F6's own text is binding on what quarantine
    must record: 'Fix the component/config, then re-run fresh. No trial or
    parameter-dimension slot is consumed; no family is marked failed.' Any trial row
    already written for such a run must be marked invalid (`_mark_trial_invalidated`
    exists) — not deleted, not counted."*

    Replayed against the live policy with `quarantine_enabled: true`. The asserted
    outcome is the taxonomy's own verdict, not this test's judgment: quarantine (not
    escalate), terminal `done` (not re-queueable — `component_execution_error` is not
    in `_REQUEUEABLE_QUARANTINE_REASONS`), `outcome: quarantined_engineering_failure`
    (R8: never `completed_rejected`), and BOTH of run_059's real trial rows marked
    `invalidated_artifact` rather than removed.
    """
    _set_quarantine_flag(campaign_root["config_dir"], True)
    run_dir = _stage_halt(
        campaign_root,
        "run_059",
        "component_execution_error",
        last_error=_HALT_13_DETAIL,
        trial_rows=_RUN_059_TRIAL_ROWS,
    )
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_059", entry_id=_HALT_13_ENTRY_ID)])

    assert camp.process_once() is True, "quarantine advances the queue; halt #13 cost 10.27h"

    entry = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert entry["id"] == _HALT_13_ENTRY_ID
    assert entry["status"] == "done"
    assert entry["outcome"] == camp._QUARANTINE_OUTCOME == "quarantined_engineering_failure"
    assert entry["outcome"] != "completed_rejected", "R8: never launder an engine bug into a null"

    record = _read_state(campaign_root["runs_dir"], "run_059")["halt_history"][-1]["quarantine"]
    assert record["run_id"] == "run_059"
    assert record["queue_entry_id"] == _HALT_13_ENTRY_ID
    assert record["requeueable"] is False
    assert record["trial_accounting"] == "marked_trial_invalidated"
    assert record["no_data_touched"] is False, (
        "run_059 reached protocol_execution and carries a backtest row — the absence "
        "must be MEASURED (R7's fourth bullet), and here it is not absent"
    )
    assert record["retry_attempts"] == []

    # F6, binding: marked invalid, never deleted, and both rows.
    rows = yaml.safe_load(campaign_root["campaign_state_path"].read_text(encoding="utf-8"))["trial_sharpes"]
    assert len(rows) == 2, "R7: rows are marked, never removed — deletion would shrink N"
    assert all(r["invalidated_artifact"] is True for r in rows)
    assert all("component_execution_error" in r["invalidation_reason"] for r in rows)


# --- must-escalate: halt #4 ------------------------------------------------

# `campaign_log.md` line 34, verbatim:
#   - 2026-07-06T18:23:42Z HALT — kb_reactivation_violation. Campaign stopped on
#     P4_ts_trend / run_053. See RUNBOOK.md 'Resume after a pause'.
_HALT_4_ENTRY_ID = "P4_ts_trend"
# run_053's two `kb_reactivation_violations` records, copied verbatim from that run's
# own pipeline_state.yaml — which, six weeks on, still carries them and still reads
# `flags.kb_reactivation_violation: true`, exactly as the taxonomy reports. Used as
# fixture DATA only; the real run directory is never touched by this test.
_RUN_053_KB_VIOLATIONS = [
    "next_research_question references H-041-A (finding "
    "'funding_rate_mean_reversion_inconclusive'), whose reactivation_condition was "
    "already consumed by run_050 (outcome=no_edge_observed). A genuinely different "
    "formulation is a new hypothesis registration, not a reactivation of this entry.",
    "next_research_question references H-041-C (finding "
    "'fear_greed_contrarian_inconclusive'), whose reactivation_condition was already "
    "consumed by run_048 (outcome=era_conditional_instability). A genuinely different "
    "formulation is a new hypothesis registration, not a reactivation of this entry.",
]


@pytest.mark.parametrize("quarantine_flag", [False, True])
def test_must_escalate_halt_4_escalates_with_the_flag_off_AND_on(campaign_root, quarantine_flag):
    """REGRESSION FIXTURE — class: must-escalate. Halt #4
    (2026-07-06T18:23:42Z, `kb_reactivation_violation`, run_053,
    queue entry P4_ts_trend, 19.04 h).

    Taxonomy #4, verbatim: *"Detail: run_053's state still carries both violation
    records verbatim — the `next_research_question` reactivated H-041-A and H-041-C,
    whose `reactivation_condition`s were already consumed by `run_050` and `run_048`.
    ... Class: must-escalate. By the brief's standing rule and by the RUNBOOK's own
    'remain human-gated' list. Never propose auto-resuming this."*

    Run with `quarantine_enabled` BOTH off and on, asserting the identical escalate
    outcome each time. That parametrization is the point of the fixture: it is the
    strongest available proof that R1's integrity list is never overridden by the
    flag. `kb_reactivation_violation` is simply not in `_QUARANTINE_SAFE_REASONS`, so
    turning quarantine on cannot reach it — but "cannot" is a claim about code
    someone may edit, and this pins it by execution against a halt that really
    happened and really cost 19 hours.
    """
    _set_quarantine_flag(campaign_root["config_dir"], quarantine_flag)
    _stage_halt(
        campaign_root,
        "run_053",
        "kb_reactivation_violation",
        kb_reactivation_violations=list(_RUN_053_KB_VIOLATIONS),
        trial_rows=[_prescreen_row("run_053")],
    )
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_053", entry_id=_HALT_4_ENTRY_ID)])

    assert camp.process_once() is False, "an integrity halt stops the campaign, flag or no flag"

    entry = yaml.safe_load(campaign_root["queue_path"].read_text(encoding="utf-8"))["queue"][0]
    assert entry["status"] == "paused:kb_reactivation_violation"
    assert entry["outcome"] is None

    log = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")
    assert "HALT — kb_reactivation_violation." in log
    assert f"Campaign stopped on {_HALT_4_ENTRY_ID} / run_053." in log
    assert "QUARANTINE" not in log

    entry_record = _read_state(campaign_root["runs_dir"], "run_053")["halt_history"][-1]
    assert entry_record["reason"] == "kb_reactivation_violation"
    assert "quarantine" not in entry_record, "an escalated halt carries no quarantine record"

    # And the trial row is untouched: escalation makes no accounting decision at all.
    rows = yaml.safe_load(campaign_root["campaign_state_path"].read_text(encoding="utf-8"))["trial_sharpes"]
    assert rows == [_prescreen_row("run_053")]


def test_the_three_replayed_classes_cover_the_taxonomys_own_partition():
    """A guard on the fixture set itself. The S1 taxonomy partitions the 14 halts
    into four classes — retry-safe, quarantine-safe, must-escalate and one
    undecidable (#7, 46.85 h, whose cause the record did not keep). S4 asks for one
    replayed fixture per CLASSIFIABLE class, which is three; #7 is deliberately not
    replayed, because there is nothing to replay it against.

    This asserts the three reason codes the fixtures above use still sit on the sides
    of `_QUARANTINE_SAFE_REASONS` the taxonomy put them on, so a change to that set
    that contradicts the measured evidence fails here as well as in
    `test_quarantine_safe_set_is_exactly_the_four_evidenced_reasons`."""
    assert "component_execution_error" in camp._QUARANTINE_SAFE_REASONS  # #13
    assert "kb_reactivation_violation" not in camp._QUARANTINE_SAFE_REASONS  # #4
    assert "unhandled_exception" not in camp._QUARANTINE_SAFE_REASONS  # #10/#12 counterfactual
    assert "component_execution_error" not in camp._REQUEUEABLE_QUARANTINE_REASONS
