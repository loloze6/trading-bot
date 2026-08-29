"""
E-031 S2 -- the schedulability block (`campaign_record/schedulability.yaml`),
written by `workflow/run_campaign.py`.

WHAT THIS CLOSES (measured, not asserted): E-031/EPIC.md's own reading of
process_once() found all four of E-030's `_write_loop_health()` call sites
sit strictly AFTER `_select_entry()` returns a non-None entry -- the queue-
exhausted `entry is None` branch (the ONE condition that actually stopped
the real campaign, 2026-07-19) has never produced ANY instrument. This is a
DIFFERENT block from loop_health.yaml (that one is about HALTS; this one is
about SCHEDULABILITY -- ready/in_progress/blocked counts, days since the
last completion, and per-blocked-entry dwell time), written unconditionally
near the top of process_once(), before `_select_entry`'s result is even
inspected, so it fires on every path including exhaustion.

WHAT IS PROVEN HERE
  1. Flag-off bit-identity: comparing ACTUAL sandbox contents and
     process_once()'s return value/log line before and after this feature
     existed, not just asserting the code path is skipped (this project's
     standing acceptance bar for every off-by-default flag in this chain).
  2. The block IS written on the exhaustion path specifically -- the exact
     gap E-030's own instrument leaves (test_loop_health_instrument.py never
     exercises this path because loop_health.yaml genuinely never fires on
     it).
  3. It is also written on a normal (non-exhaustion) step, per the epic's
     "on every process_once() step" wording.
  4. The computed shape: counts, days_since_last_completion, and per-
     blocked-entry dwell_days/dwell_basis, including the degenerate (no
     campaign_log.md mention) case reporting None, never a flattering 0.

Fixture pattern (`campaign_root`, `_save_queue_entries`, `_write_fresh_scaffold`)
reused from tests/test_halt_quarantine_policy.py, itself from
test_k4_routing_registration.py's hermetic setup: nothing here touches the
real repository, and no LLM or subprocess is spawned.
"""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(__file__).parent.parent / "workflow"
sys.path.insert(0, str(WORKFLOW_PATH))

import run_campaign as camp  # noqa: E402

from test_halt_quarantine_policy import (  # noqa: E402
    _entry,
    _save_queue_entries,
    _write_campaign_state,
    _write_fresh_scaffold,
    campaign_root,
)

__all__ = ["campaign_root"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _set_flags(config_dir: Path, *, schedulability=None, auto_refill=None):
    """None means the key is omitted entirely (absent-key-and-section case),
    matching every prior story's own `_set_flags`-shaped helper in this test
    suite (e.g. test_variant_anti_adjacency_gate.py)."""
    orchestrator = {"token_budget_per_run_weighted_units": 1500000}
    if schedulability is not None:
        orchestrator["schedulability_block"] = {"enabled": bool(schedulability)}
    if auto_refill is not None:
        orchestrator["auto_refill"] = {"enabled": bool(auto_refill)}
    (config_dir / "campaign_config.yaml").write_text(
        yaml.safe_dump({"orchestrator": orchestrator}, sort_keys=False),
        encoding="utf-8",
    )


def _sched_path(campaign_root) -> Path:
    return campaign_root["root"] / "campaign_record" / "schedulability.yaml"


def _snapshot_tree(root: Path) -> dict:
    """path (relative to root) -> bytes, for every file under root. Used for
    the bit-identity comparison -- the same bar test_variant_selection_
    record.py's own flag-off proof uses ('snapshots every file under
    artifacts/ ... asserts the snapshot is byte-identical')."""
    out = {}
    if not root.exists():
        return out
    for p in root.rglob("*"):
        if p.is_file():
            out[str(p.relative_to(root))] = p.read_bytes()
    return out


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# 1. Flag-off bit-identity
# ---------------------------------------------------------------------------


def test_flag_off_bit_identity_on_exhaustion(campaign_root):
    _set_flags(campaign_root["config_dir"], schedulability=False)
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {**_entry("run_900"), "status": "done", "outcome": "completed_rejected"},
        ],
    )

    before = _snapshot_tree(campaign_root["root"])
    keep_going = camp.process_once()
    after = _snapshot_tree(campaign_root["root"])

    assert keep_going is False
    assert not _sched_path(campaign_root).exists()
    log_lines = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8").splitlines()
    # reconcile_orphans() always logs its own line first, flag-independent --
    # the assertion here is about the SCHEDULABILITY feature, not that line.
    assert any(
        "Queue exhausted — no ready or in_progress entries remain." in ln
        for ln in log_lines
    )
    # Only campaign_log.md may have changed (the one log line _log() always
    # writes, on or off) -- everything else must be untouched.
    diff_paths = {p for p in set(before) | set(after) if before.get(p) != after.get(p)}
    assert diff_paths <= {"campaign_log.md"}, (
        f"flag-off must not write anything besides the ordinary log line; "
        f"changed: {diff_paths}"
    )


def test_flag_off_key_absent_is_also_a_no_op(campaign_root):
    """Absent key/section, not just an explicit false, must behave identically --
    silence is never a green light."""
    _set_flags(campaign_root["config_dir"])  # no schedulability_block key at all
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {**_entry("run_900"), "status": "done", "outcome": "completed_rejected"},
        ],
    )

    assert camp.process_once() is False
    assert not _sched_path(campaign_root).exists()


# ---------------------------------------------------------------------------
# 2. The block IS written on the exhaustion path -- E-030's own measured gap
# ---------------------------------------------------------------------------


def test_written_on_the_exhaustion_path(campaign_root):
    _set_flags(campaign_root["config_dir"], schedulability=True)
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {**_entry("run_900"), "status": "done", "outcome": "completed_rejected"},
            {
                "id": "E2",
                "brief_path": "b.yaml",
                "status": "blocked_on_daily_bar_ingest",
                "priority": 1,
                "run_ids": [],
            },
        ],
    )

    keep_going = camp.process_once()

    assert keep_going is False, "unchanged behavior: exhaustion still returns False"
    assert _sched_path(campaign_root).exists(), (
        "E-031 S2's whole point: this file must exist on the exact path "
        "loop_health.yaml never reaches"
    )
    block = yaml.safe_load(_sched_path(campaign_root).read_text(encoding="utf-8"))
    assert block["counts"] == {
        "total": 2,
        "ready": 0,
        "in_progress": 0,
        "done": 1,
        "blocked": 1,
    }
    log = camp.CAMPAIGN_LOG_PATH.read_text(encoding="utf-8")
    assert "Queue exhausted — no ready or in_progress entries remain." in log


def test_written_on_a_normal_non_exhaustion_step_too(campaign_root):
    """'On every process_once() step', not only when idle -- the DONE branch
    (a healthy step) must refresh the block just as the exhaustion branch
    does."""
    _set_flags(campaign_root["config_dir"], schedulability=False)  # off during setup
    _write_fresh_scaffold(
        campaign_root["runs_dir"],
        "run_912",
        status="completed",
        pending_stage="completed_reframed",
    )
    _save_queue_entries(campaign_root["queue_path"], [_entry("run_912")])
    _write_campaign_state(
        campaign_root["campaign_state_path"], runs=["run_912"], trial_sharpes=[]
    )
    _set_flags(campaign_root["config_dir"], schedulability=True)  # on for the real call

    assert camp.process_once() is True
    assert _sched_path(campaign_root).exists()
    block = yaml.safe_load(_sched_path(campaign_root).read_text(encoding="utf-8"))
    assert block["counts"]["done"] == 1


# ---------------------------------------------------------------------------
# 3. Shape: counts, days_since_last_completion, per-blocked-entry dwell time
# ---------------------------------------------------------------------------


def test_counts_and_blocked_entry_dwell_shape(campaign_root):
    now = datetime.now(timezone.utc)
    five_days_ago = now - timedelta(days=5)

    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {
                "id": "R1",
                "brief_path": "b.yaml",
                "status": "ready",
                "priority": 1,
                "run_ids": [],
            },
            {
                "id": "R2",
                "brief_path": "b.yaml",
                "status": "ready",
                "priority": 2,
                "run_ids": [],
            },
            {**_entry("run_1"), "id": "IP1", "status": "in_progress"},
            {
                "id": "D1",
                "brief_path": "b.yaml",
                "status": "done",
                "priority": 1,
                "run_ids": ["run_0"],
            },
            {
                "id": "BLOCKED_WITH_MENTION",
                "brief_path": "b.yaml",
                "status": "blocked_on_daily_bar_ingest",
                "priority": 1,
                "run_ids": [],
            },
            {
                "id": "BLOCKED_NO_MENTION",
                "brief_path": "b.yaml",
                "status": "paused:some_reason",
                "priority": 1,
                "run_ids": [],
            },
        ],
    )
    camp.CAMPAIGN_LOG_PATH.write_text(
        f"- {_iso(five_days_ago)} STAGE BLOCKED_WITH_MENTION / run_0: something happened\n"
        f"- {_iso(now - timedelta(days=1))} DONE D1 (run_0) -> completed_rejected\n",
        encoding="utf-8",
    )

    block = camp._compute_schedulability()

    assert block["counts"] == {
        "total": 6,
        "ready": 2,
        "in_progress": 1,
        "done": 1,
        "blocked": 2,
    }
    assert block["days_since_last_completion"] == pytest.approx(1.0, abs=0.02)
    assert block["last_completion_basis"] == "last campaign_log.md DONE line"

    by_id = {b["id"]: b for b in block["blocked_entries"]}
    assert set(by_id) == {"BLOCKED_WITH_MENTION", "BLOCKED_NO_MENTION"}

    mentioned = by_id["BLOCKED_WITH_MENTION"]
    assert mentioned["status"] == "blocked_on_daily_bar_ingest"
    # Review fix 4 (2026-08-26): `blocker` now carries the blocker itself, with
    # the `blocked_on_` / `paused:` prefix stripped -- previously it was a
    # verbatim copy of `status` and so carried no information beyond it.
    assert mentioned["blocker"] == "daily_bar_ingest"
    assert mentioned["dwell_days"] == pytest.approx(5.0, abs=0.02)
    assert "last campaign_log.md mention" in mentioned["dwell_basis"]

    unmentioned = by_id["BLOCKED_NO_MENTION"]
    assert unmentioned["dwell_days"] is None, (
        "an unknown dwell time must read as unknown, never as a flattering 0"
    )
    assert "no campaign_log.md mention found" in unmentioned["dwell_basis"]


def test_degenerate_empty_log_reports_none_not_zero(campaign_root):
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {
                "id": "B1",
                "brief_path": "b.yaml",
                "status": "blocked_on_x",
                "priority": 1,
                "run_ids": [],
            },
        ],
    )
    camp.CAMPAIGN_LOG_PATH.write_text("", encoding="utf-8")

    block = camp._compute_schedulability()

    assert block["days_since_last_completion"] is None
    assert (
        block["last_completion_basis"]
        == "no DONE or QUARANTINE line found in campaign_log.md"
    )
    assert block["blocked_entries"][0]["dwell_days"] is None


def test_block_is_a_projection_and_deleting_it_loses_nothing(campaign_root):
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {
                "id": "B1",
                "brief_path": "b.yaml",
                "status": "blocked_on_x",
                "priority": 1,
                "run_ids": [],
            },
        ],
    )
    camp.CAMPAIGN_LOG_PATH.write_text("", encoding="utf-8")

    first = camp._write_schedulability()
    _sched_path(campaign_root).unlink()
    second = camp._write_schedulability()

    volatile = {"computed_at"}
    assert {k: v for k, v in first.items() if k not in volatile} == {
        k: v for k, v in second.items() if k not in volatile
    }


# ---------------------------------------------------------------------------
# Regression tests for the 2026-08-26 code-review findings. The first two are
# the ones that could silently return a WRONG answer to S3's escalate-vs-refill
# consumer rather than merely an untidy one.
# ---------------------------------------------------------------------------


def test_split_child_activity_does_not_reset_the_blocked_parents_dwell(campaign_root):
    """Review fix 1, HIGH. _add_queue_entry_for_split_child mints child ids as
    f"{parent_id}__split_{child_id}", so the parent id is ALWAYS a substring of
    its children's ids. A bare `eid in text` therefore let any activity on a
    split child reset the blocked PARENT's dwell to ~0 -- the flattering
    direction _compute_schedulability's own docstring forbids."""
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {
                "id": "P4_ts_trend",
                "brief_path": "b.yaml",
                "status": "blocked_on_daily_bar_ingest",
                "priority": 1,
                "run_ids": [],
            },
        ],
    )
    # Parent last genuinely mentioned 40 days ago; a SPLIT CHILD launched 5
    # minutes ago. The parent has not moved.
    old = (datetime.now(timezone.utc) - timedelta(days=40)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    recent = (datetime.now(timezone.utc) - timedelta(minutes=5)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    camp.CAMPAIGN_LOG_PATH.write_text(
        "\n".join(
            [
                f"- {old} LAUNCH P4_ts_trend -> run_054",
                f"- {recent} LAUNCH P4_ts_trend__split_run_071 -> run_071",
                "",
            ]
        ),
        encoding="utf-8",
    )

    block = camp._compute_schedulability()
    dwell = block["blocked_entries"][0]["dwell_days"]
    assert dwell > 39, (
        f"dwell_days={dwell}: split-child activity reset the blocked parent's "
        f"dwell -- the longest-blocked entry would read as the freshest"
    )


def test_superseded_is_terminal_not_blocked(campaign_root):
    """Review fix 2. `superseded` is schema-legal and TERMINAL (retired), not
    blocked. Counting it inflated the backlog S3's escalate decision keys on."""
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {
                "id": "S1",
                "brief_path": "b.yaml",
                "status": "superseded",
                "priority": 1,
                "run_ids": [],
            },
            {
                "id": "B1",
                "brief_path": "b.yaml",
                "status": "blocked_on_x",
                "priority": 1,
                "run_ids": [],
            },
        ],
    )
    camp.CAMPAIGN_LOG_PATH.write_text("", encoding="utf-8")

    block = camp._compute_schedulability()
    assert block["counts"]["blocked"] == 1, "superseded must not count as blocked"
    assert [e["id"] for e in block["blocked_entries"]] == ["B1"]


def test_quarantine_counts_as_a_completion(campaign_root):
    """Review fix 5. The quarantine path completes an entry (status=done) but
    logs QUARANTINE, not DONE. Ignoring it made a loop advancing via quarantine
    read as permanently stalled, contradicting counts.done in the same block."""
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {
                "id": "B1",
                "brief_path": "b.yaml",
                "status": "blocked_on_x",
                "priority": 1,
                "run_ids": [],
            },
        ],
    )
    recent = (datetime.now(timezone.utc) - timedelta(days=2)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    camp.CAMPAIGN_LOG_PATH.write_text(
        f"- {recent} QUARANTINE run_059 -> quarantined_engineering_failure" + "\n",
        encoding="utf-8",
    )

    block = camp._compute_schedulability()
    assert block["days_since_last_completion"] is not None
    assert block["days_since_last_completion"] < 3
    assert "QUARANTINE" in block["last_completion_basis"]


def test_blocker_field_strips_the_prefix_it_exists_to_spare_the_consumer(campaign_root):
    """Review fix 4. `blocker` was a verbatim copy of `status`, so the field
    advertised as a blocker string carried no information beyond it."""
    _save_queue_entries(
        campaign_root["queue_path"],
        [
            {
                "id": "B1",
                "brief_path": "b.yaml",
                "status": "blocked_on_daily_bar_ingest",
                "priority": 1,
                "run_ids": [],
            },
            {
                "id": "B2",
                "brief_path": "b.yaml",
                "status": "paused:pending_operator_ratification",
                "priority": 1,
                "run_ids": [],
            },
        ],
    )
    camp.CAMPAIGN_LOG_PATH.write_text("", encoding="utf-8")

    by_id = {e["id"]: e for e in camp._compute_schedulability()["blocked_entries"]}
    assert by_id["B1"]["blocker"] == "daily_bar_ingest"
    assert by_id["B2"]["blocker"] == "pending_operator_ratification"
    assert by_id["B1"]["status"] == "blocked_on_daily_bar_ingest"  # status unchanged
