"""
Free-space guard: breach stops and attests, headroom runs, unknown is a breach.

The property under test is the one that makes a guard worth having: it must be
impossible for the recorder to keep writing into a volume it cannot prove has
room, and impossible for the resulting stop to be mistaken afterwards for a
crash or for a clean operator stop.
"""

from __future__ import annotations

import asyncio

import pytest

from recorder.disk_guard import (
    DEFAULT_MIN_FREE_GB,
    EXIT_DISK_GUARD_ABORT,
    GB,
    DiskGuard,
    probe_free_bytes,
)
from recorder.journal import (
    JOURNAL_FILENAME,
    coverage_intervals,
    load_records,
    read_tail_state,
)
from recorder.record_kraken_ws import Recorder


def _probe(value):
    return lambda _path: value


def _recorder(tmp_path, free, min_free_gb=5.0):
    return Recorder(
        out_dir=tmp_path,
        symbols=["BTC/USD"],
        compress=False,
        min_free_gb=min_free_gb,
        disk_probe=_probe(free),
    )


# ---------------------------------------------------------------------------
# the guard itself
# ---------------------------------------------------------------------------


def test_headroom_is_ok(tmp_path):
    g = DiskGuard(tmp_path, min_free_gb=5.0, probe=_probe(20 * GB))
    r = g.check()
    assert r.ok
    assert r.free_gb == pytest.approx(20.0)
    assert r.min_free_gb == pytest.approx(5.0)


def test_below_floor_is_a_breach(tmp_path):
    r = DiskGuard(tmp_path, min_free_gb=5.0, probe=_probe(4 * GB)).check()
    assert not r.ok
    assert "below configured floor" in r.reason


def test_exactly_at_the_floor_is_not_a_breach(tmp_path):
    """The floor is the minimum acceptable, not the first rejected value."""
    r = DiskGuard(tmp_path, min_free_gb=5.0, probe=_probe(5 * GB)).check()
    assert r.ok


def test_undeterminable_free_space_is_a_breach(tmp_path):
    """
    Deny by default. An unmeasurable disk is the state in which continuing to
    write is least defensible, so it is treated exactly as a full one.
    """
    r = DiskGuard(tmp_path, min_free_gb=5.0, probe=_probe(None)).check()
    assert not r.ok
    assert r.free_bytes is None
    assert r.as_journal_fields()["determinable"] is False


def test_probe_returns_none_rather_than_raising_on_a_bad_path(tmp_path):
    assert probe_free_bytes(tmp_path / "no" / "such" / "volume") is None


def test_a_zero_or_negative_floor_is_refused(tmp_path):
    for bad in (0.0, -1.0):
        with pytest.raises(ValueError):
            DiskGuard(tmp_path, min_free_gb=bad)


def test_units_are_decimal_gb_not_gib(tmp_path):
    """A 5 GB floor must not silently become 5.37 GB. See disk_guard UNITS."""
    assert DiskGuard(tmp_path, min_free_gb=5.0).min_free_bytes == 5_000_000_000


# ---------------------------------------------------------------------------
# the recorder's use of it
# ---------------------------------------------------------------------------


def test_breach_flushes_attests_and_requests_stop(tmp_path):
    rec = _recorder(tmp_path, free=1 * GB)
    rec.writer.write_frame("book_d10", "BTCUSD", '{"channel":"book"}')

    assert rec.check_disk() is False
    assert rec._guard_abort is True
    assert rec._stop.is_set()

    records = load_records(tmp_path / JOURNAL_FILENAME)
    aborts = [r for r in records if r["type"] == "DISK_GUARD_ABORT"]
    assert len(aborts) == 1
    assert aborts[0]["free_bytes"] == 1 * GB
    assert aborts[0]["min_free_bytes"] == 5 * GB
    assert aborts[0]["determinable"] is True
    # The frame was on disk BEFORE the attestation — the journal never claims
    # coverage for data it has not made durable.
    assert (tmp_path / "book_d10" / "BTCUSD").exists()

    rec.writer.close()
    rec.journal.close()


def test_no_breach_writes_no_record(tmp_path):
    rec = _recorder(tmp_path, free=500 * GB)
    assert rec.check_disk() is True
    assert rec._guard_abort is False
    assert not rec._stop.is_set()
    assert [r for r in load_records(tmp_path / JOURNAL_FILENAME)
            if r["type"] == "DISK_GUARD_ABORT"] == []
    rec.writer.close()
    rec.journal.close()


def test_undeterminable_stops_the_recorder_too(tmp_path):
    rec = _recorder(tmp_path, free=None)
    assert rec.check_disk() is False
    abort = [r for r in load_records(tmp_path / JOURNAL_FILENAME)
             if r["type"] == "DISK_GUARD_ABORT"][0]
    assert abort["determinable"] is False
    assert abort["free_bytes"] is None
    rec.writer.close()
    rec.journal.close()


def test_run_aborts_before_opening_a_socket_and_exits_nonzero(tmp_path):
    """
    A boot under the floor must never reach the websocket, and must never reach
    the startup compaction sweep either — compaction writes a `.part` the size
    of an hour of capture, which is the last thing a full volume needs.
    """
    rec = _recorder(tmp_path, free=0)
    assert asyncio.run(rec.run()) == EXIT_DISK_GUARD_ABORT

    records = load_records(tmp_path / JOURNAL_FILENAME)
    types = [r["type"] for r in records]
    assert "DISK_GUARD_ABORT" in types
    assert "WS_CONNECT" not in types
    # No RECORDER_STOP on top of it: a journal ending in a clean-stop record is
    # exactly what the supervisor reads as "the operator meant this".
    assert types[-1] == "DISK_GUARD_ABORT"


def test_the_guard_never_re_arms(tmp_path):
    """
    "There was room again a minute later" is not a reason to resume writing to
    a volume that already crossed the floor once.
    """
    rec = _recorder(tmp_path, free=0)
    assert rec.check_disk() is False
    rec.guard._probe = _probe(500 * GB)
    assert rec.check_disk() is False
    assert len([r for r in load_records(tmp_path / JOURNAL_FILENAME)
                if r["type"] == "DISK_GUARD_ABORT"]) == 1
    rec.writer.close()
    rec.journal.close()


# ---------------------------------------------------------------------------
# how the abort reads back out of the journal
# ---------------------------------------------------------------------------


def test_guard_abort_closes_open_coverage_intervals(tmp_path):
    rec = _recorder(tmp_path, free=0)
    rec.journal.record_start()
    rec.journal.write("SUBSCRIBE_ACK", symbol="BTC/USD", channel="book")
    rec.check_disk()
    rec.journal.close()

    ivs = coverage_intervals(load_records(tmp_path / JOURNAL_FILENAME))
    assert ivs[("BTC/USD", "book")][0].closed_by == "DISK_GUARD_ABORT"
    rec.writer.close()


def test_guard_abort_is_an_attested_shutdown_not_a_crash(tmp_path):
    rec = _recorder(tmp_path, free=0)
    rec.check_disk()
    rec.journal.close()

    state = read_tail_state(tmp_path / JOURNAL_FILENAME)
    assert state["last_type"] == "DISK_GUARD_ABORT"
    # `prev_clean_shutdown: false` means "we lost the tail to a crash". A guard
    # abort lost nothing, and reporting it as a crash would mislabel the gap.
    assert state["clean_shutdown"] is True
    rec.writer.close()


def test_the_default_floor_is_the_documented_one():
    assert DEFAULT_MIN_FREE_GB == 5.0
    assert EXIT_DISK_GUARD_ABORT == 3
