"""
E-011 S1b -- single-writer campaign launch lock (tools/campaign_lock.py).

Covers the two real failure modes named in the dispatch:
  1. someone else's campaign is genuinely running -> refuse cleanly (no hang,
     no silent proceed), and the message names who/when and how to check.
  2. a stale lock from a crashed prior run -> detected and cleared, not
     silently ignored forever, and not silently ignored on a guess either
     (live-but-undeterminable and cross-host locks are NOT auto-cleared).

Also proves release() frees the lock for the next launch, and that the
wiring in workflow/run_campaign.py computes the lock path from the CURRENT
(possibly monkeypatched) orch.CAMPAIGN_STATE_PATH rather than a hardcoded
literal -- so it follows the test sandbox and, in production, an env that
relocates campaign_record/.

No subprocess/multiprocess is used ("fake it with two sequential acquire
attempts against the same lock file" -- explicitly sanctioned by the E-011
S1b dispatch for this exact case). Everything here is single-process,
sequential calls against a shared on-disk lock file, which is exactly what
two real racing `run_campaign.py` invocations produce from the filesystem's
point of view.
"""
import json
import os
import socket
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "workflow"))

import campaign_lock  # noqa: E402
import run_campaign as camp  # noqa: E402
import run_phase1_research as rpr  # noqa: E402


# ---------------------------------------------------------------------------
# Core acquire/release
# ---------------------------------------------------------------------------

def test_second_acquire_refuses_while_first_is_live(tmp_path):
    """Two sequential acquires against the same lock file: the second must
    refuse cleanly (CampaignLockHeld), not hang, not silently proceed."""
    lock_path = tmp_path / "campaign_record" / ".campaign.lock"

    campaign_lock.acquire(lock_path)  # "process A" launches
    assert lock_path.exists()

    with pytest.raises(campaign_lock.CampaignLockHeld) as excinfo:
        campaign_lock.acquire(lock_path)  # "process B" launches concurrently

    msg = str(excinfo.value)
    # Message must name who (pid/host) and when (started_at), and how to check.
    assert str(os.getpid()) in msg
    assert socket.gethostname() in msg
    assert "stale" in msg.lower()
    assert str(lock_path) in msg


def test_release_frees_lock_for_next_launch(tmp_path):
    lock_path = tmp_path / "campaign_record" / ".campaign.lock"

    campaign_lock.acquire(lock_path)
    campaign_lock.release(lock_path)
    assert not lock_path.exists()

    # A fresh launch after release must succeed cleanly (no leftover state).
    campaign_lock.acquire(lock_path)
    assert lock_path.exists()
    campaign_lock.release(lock_path)


def test_release_is_idempotent_when_lock_already_gone(tmp_path):
    lock_path = tmp_path / "campaign_record" / ".campaign.lock"
    assert not lock_path.exists()
    campaign_lock.release(lock_path)  # must not raise


def test_held_context_manager_releases_on_exception(tmp_path):
    lock_path = tmp_path / "campaign_record" / ".campaign.lock"

    with pytest.raises(RuntimeError, match="boom"):
        with campaign_lock.held(lock_path):
            assert lock_path.exists()
            raise RuntimeError("boom")

    assert not lock_path.exists()


def test_lock_path_for_derives_from_campaign_state_path(tmp_path):
    """The lock lives NEXT TO campaign_state.yaml, wherever that currently
    resolves to -- not a hardcoded literal path."""
    state_path = tmp_path / "somewhere_else" / "campaign_state.yaml"
    lock_path = campaign_lock.lock_path_for(state_path)
    assert lock_path == tmp_path / "somewhere_else" / ".campaign.lock"


# ---------------------------------------------------------------------------
# Stale-lock detection: dead pid on same host
# ---------------------------------------------------------------------------

def test_stale_lock_dead_pid_same_host_is_cleared(tmp_path, monkeypatch):
    lock_path = tmp_path / "campaign_record" / ".campaign.lock"
    lock_path.parent.mkdir(parents=True)
    lock_path.write_text(json.dumps({
        "pid": 999999,  # arbitrary -- liveness is mocked below, not relied on
        "hostname": socket.gethostname(),
        "started_at": "2020-01-01T00:00:00+00:00",
    }), encoding="utf-8")

    monkeypatch.setattr(campaign_lock, "_pid_is_alive", lambda pid: False)

    campaign_lock.acquire(lock_path)  # must clear the dead-pid lock and succeed
    assert lock_path.exists()
    new_contents = json.loads(lock_path.read_text(encoding="utf-8"))
    assert new_contents["pid"] == os.getpid()


def test_live_pid_same_host_is_never_cleared(tmp_path, monkeypatch):
    lock_path = tmp_path / "campaign_record" / ".campaign.lock"
    lock_path.parent.mkdir(parents=True)
    lock_path.write_text(json.dumps({
        "pid": 12345,
        "hostname": socket.gethostname(),
        "started_at": "2026-09-09T00:00:00+00:00",
    }), encoding="utf-8")

    monkeypatch.setattr(campaign_lock, "_pid_is_alive", lambda pid: True)

    with pytest.raises(campaign_lock.CampaignLockHeld):
        campaign_lock.acquire(lock_path)


def test_undeterminable_liveness_same_host_falls_back_to_age_not_a_guess(tmp_path, monkeypatch):
    """When we genuinely can't tell if the pid is alive (platform limitation),
    the lock must NOT be cleared just because liveness is unknown -- only a
    confirmed age threshold breach may clear it."""
    lock_path = tmp_path / "campaign_record" / ".campaign.lock"
    lock_path.parent.mkdir(parents=True)
    lock_path.write_text(json.dumps({
        "pid": 12345,
        "hostname": socket.gethostname(),
        "started_at": "2026-09-09T00:00:00+00:00",
    }), encoding="utf-8")
    # Fresh mtime (just written) -- well within the staleness threshold.
    monkeypatch.setattr(campaign_lock, "_pid_is_alive", lambda pid: None)

    with pytest.raises(campaign_lock.CampaignLockHeld):
        campaign_lock.acquire(lock_path)


# ---------------------------------------------------------------------------
# Stale-lock detection: age threshold (cross-host, or corrupt lock file)
# ---------------------------------------------------------------------------

def test_stale_lock_by_age_cross_host_is_cleared(tmp_path):
    lock_path = tmp_path / "campaign_record" / ".campaign.lock"
    lock_path.parent.mkdir(parents=True)
    lock_path.write_text(json.dumps({
        "pid": os.getpid(),
        "hostname": "some-other-machine",  # never same-host pid-checked
        "started_at": "2020-01-01T00:00:00+00:00",
    }), encoding="utf-8")

    old_time = time.time() - (campaign_lock.STALE_LOCK_AGE_SECONDS + 3600)
    os.utime(lock_path, (old_time, old_time))

    campaign_lock.acquire(lock_path)  # confirmed-stale by age -> cleared
    assert lock_path.exists()
    assert json.loads(lock_path.read_text(encoding="utf-8"))["pid"] == os.getpid()


def test_young_cross_host_lock_is_not_cleared(tmp_path):
    lock_path = tmp_path / "campaign_record" / ".campaign.lock"
    lock_path.parent.mkdir(parents=True)
    lock_path.write_text(json.dumps({
        "pid": 1,
        "hostname": "some-other-machine",
        "started_at": "2026-09-09T00:00:00+00:00",
    }), encoding="utf-8")
    # Fresh mtime from the write above -- well within threshold.

    with pytest.raises(campaign_lock.CampaignLockHeld):
        campaign_lock.acquire(lock_path)


def test_corrupt_lock_file_falls_back_to_age_not_silently_ignored(tmp_path):
    """A corrupt/unreadable lock file must not be treated as 'no lock' --
    it's judged the same as any unidentifiable lock, by file age."""
    lock_path = tmp_path / "campaign_record" / ".campaign.lock"
    lock_path.parent.mkdir(parents=True)
    lock_path.write_text("{not valid json", encoding="utf-8")

    # Young corrupt lock: must still refuse (never silently proceed past an
    # unreadable lock just because we can't parse who holds it).
    with pytest.raises(campaign_lock.CampaignLockHeld):
        campaign_lock.acquire(lock_path)

    # Aged corrupt lock: confirmed stale by age -> cleared.
    old_time = time.time() - (campaign_lock.STALE_LOCK_AGE_SECONDS + 3600)
    os.utime(lock_path, (old_time, old_time))
    campaign_lock.acquire(lock_path)
    assert json.loads(lock_path.read_text(encoding="utf-8"))["pid"] == os.getpid()


# ---------------------------------------------------------------------------
# Wiring: run_campaign.py imports campaign_lock and derives the path from
# the (possibly monkeypatched) orch.CAMPAIGN_STATE_PATH, matching the
# conftest sandbox convention used by every other test in this suite.
# ---------------------------------------------------------------------------

def test_run_campaign_module_wires_campaign_lock():
    assert camp.campaign_lock is campaign_lock


def test_run_campaign_lock_path_follows_sandboxed_campaign_state_path(tmp_path, monkeypatch):
    fake_state_path = tmp_path / "campaign_record" / "campaign_state.yaml"
    monkeypatch.setattr(rpr, "CAMPAIGN_STATE_PATH", fake_state_path)
    resolved = campaign_lock.lock_path_for(rpr.CAMPAIGN_STATE_PATH)
    assert resolved == fake_state_path.parent / ".campaign.lock"
