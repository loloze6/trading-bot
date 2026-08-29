"""
Coverage-journal gap reconstruction.

The property under test is the one the whole recorder rests on: given a
journal, a consumer can say exactly which wall-clock intervals were captured,
and asking for anything else RAISES rather than returning a quiet-looking
empty result.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from recorder.journal import (
    ATTESTATION_TOLERANCE_S,
    CoverageGapError,
    CoverageJournal,
    Interval,
    ROLLUP_INTERVAL_S,
    assert_covered,
    coverage_intervals,
    load_records,
    parse_iso,
    read_tail_state,
    uncovered,
)

T0 = datetime(2026, 7, 26, 12, 0, 0, tzinfo=timezone.utc)


def _rec(jseq, ts, rtype, run_id="run-a", **kw):
    d = {
        "jseq": jseq,
        "run_id": run_id,
        "ts": ts.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z",
        "mono": float(jseq),
        "type": rtype,
    }
    d.update(kw)
    return d


def _mins(n):
    return T0 + timedelta(minutes=n)


# ---------------------------------------------------------------------------
# interval reconstruction
# ---------------------------------------------------------------------------


def test_ack_then_stop_yields_one_closed_interval():
    recs = [
        _rec(1, _mins(0), "RECORDER_START"),
        _rec(2, _mins(1), "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, _mins(3), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(4, _mins(5), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(5, _mins(7), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(6, _mins(9), "RECORDER_STOP"),
    ]
    ivs = coverage_intervals(recs)[("BTC/USD", "book")]
    assert len(ivs) == 1
    assert ivs[0].start == _mins(1)
    assert ivs[0].end == _mins(9)
    assert ivs[0].closed_by == "RECORDER_STOP"


def test_disconnect_reconnect_leaves_a_hole_between_intervals():
    recs = [
        _rec(1, _mins(0), "RECORDER_START"),
        _rec(2, _mins(1), "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, _mins(2), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(4, _mins(3), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(5, _mins(4), "WS_DISCONNECT", reason="heartbeat_timeout"),
        _rec(6, _mins(6), "RECONNECT_ATTEMPT", attempt=1),
        _rec(7, _mins(7), "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(8, _mins(8), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(9, _mins(9), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(10, _mins(10), "RECORDER_STOP"),
    ]
    ivs = coverage_intervals(recs)[("BTC/USD", "book")]
    assert [(i.start, i.end) for i in ivs] == [
        (_mins(1), _mins(4)),
        (_mins(7), _mins(10)),
    ]
    gaps = uncovered(ivs, _mins(0), _mins(10))
    assert gaps == [(_mins(0), _mins(1)), (_mins(4), _mins(7))]


def test_unclean_restart_closes_at_last_dead_record_not_at_new_start():
    """
    The crash window must NOT be claimed as covered.

    A process that died at minute 5 and was restarted at minute 30 leaves 25
    unattested minutes. Closing the stale interval at the new RECORDER_START
    would silently swallow them — the announce-success-over-a-hole failure the
    journal exists to prevent.
    """
    recs = [
        _rec(1, _mins(0), "RECORDER_START", run_id="run-a"),
        _rec(2, _mins(1), "SUBSCRIBE_ACK", run_id="run-a", symbol="BTC/USD", channel="book"),
        _rec(3, _mins(2), "HEARTBEAT_ROLLUP", run_id="run-a", frames_total=99),
        _rec(4, _mins(3), "HEARTBEAT_ROLLUP", run_id="run-a", frames_total=99),
        _rec(5, _mins(4), "HEARTBEAT_ROLLUP", run_id="run-a", frames_total=99),
        _rec(6, _mins(5), "HEARTBEAT_ROLLUP", run_id="run-a", frames_total=99),
        # <-- process killed here; no WS_DISCONNECT, no RECORDER_STOP
        _rec(7, _mins(30), "RECORDER_START", run_id="run-b", prev_clean_shutdown=False),
        _rec(8, _mins(31), "SUBSCRIBE_ACK", run_id="run-b", symbol="BTC/USD", channel="book"),
        _rec(9, _mins(33), "HEARTBEAT_ROLLUP", run_id="run-b", frames_total=99),
        _rec(10, _mins(35), "HEARTBEAT_ROLLUP", run_id="run-b", frames_total=99),
        _rec(11, _mins(37), "HEARTBEAT_ROLLUP", run_id="run-b", frames_total=99),
        _rec(12, _mins(39), "HEARTBEAT_ROLLUP", run_id="run-b", frames_total=99),
        _rec(13, _mins(40), "RECORDER_STOP", run_id="run-b"),
    ]
    ivs = coverage_intervals(recs)[("BTC/USD", "book")]
    assert [(i.start, i.end) for i in ivs] == [
        (_mins(1), _mins(5)),
        (_mins(31), _mins(40)),
    ]
    assert ivs[0].closed_by == "UNCLEAN_SHUTDOWN"
    assert uncovered(ivs, _mins(1), _mins(40)) == [(_mins(5), _mins(31))]


def test_still_running_interval_is_attested_only_to_the_last_record():
    recs = [
        _rec(1, _mins(0), "RECORDER_START"),
        _rec(2, _mins(1), "SUBSCRIBE_ACK", symbol="ETH/USD", channel="trade"),
        _rec(3, _mins(3), "HEARTBEAT_ROLLUP", frames_total=12),
    ]
    ivs = coverage_intervals(recs)[("ETH/USD", "trade")]
    assert ivs[0].end == _mins(3)
    assert ivs[0].closed_by == "OPEN_TAIL"


def test_symbols_and_channels_are_tracked_independently():
    recs = [
        _rec(1, _mins(0), "RECORDER_START"),
        _rec(2, _mins(1), "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, _mins(2), "SUBSCRIBE_ACK", symbol="BTC/USD", channel="trade"),
        _rec(4, _mins(3), "SUBSCRIBE_ACK", symbol="ETH/USD", channel="book"),
        _rec(5, _mins(8), "RECORDER_STOP"),
    ]
    cov = coverage_intervals(recs)
    assert set(cov) == {("BTC/USD", "book"), ("BTC/USD", "trade"), ("ETH/USD", "book")}
    assert cov[("ETH/USD", "book")][0].start == _mins(3)


def test_quiet_minute_inside_an_interval_is_still_covered():
    """Zero frames + live heartbeat == covered-and-quiet, not a gap."""
    recs = [
        _rec(1, _mins(0), "RECORDER_START"),
        _rec(2, _mins(0), "SUBSCRIBE_ACK", symbol="INJ/USD", channel="trade"),
        _rec(3, _mins(1), "HEARTBEAT_ROLLUP", heartbeats=60, frames_total=0),
        _rec(4, _mins(2), "HEARTBEAT_ROLLUP", heartbeats=60, frames_total=0),
        _rec(5, _mins(3), "RECORDER_STOP"),
    ]
    ivs = coverage_intervals(recs)[("INJ/USD", "trade")]
    assert uncovered(ivs, _mins(0), _mins(3)) == []


# ---------------------------------------------------------------------------
# positive-evidence attestation
# ---------------------------------------------------------------------------


def test_attestation_tolerance_matches_the_rollup_cadence():
    """journal.py hardcodes ROLLUP_INTERVAL_S (to avoid importing
    record_kraken_ws, which imports CoverageJournal from this module — a
    cycle). This is the tripwire that catches the two drifting apart."""
    from recorder.record_kraken_ws import ROLLUP_INTERVAL_S as PRODUCTION_ROLLUP_INTERVAL_S

    assert ROLLUP_INTERVAL_S == PRODUCTION_ROLLUP_INTERVAL_S
    assert ATTESTATION_TOLERANCE_S == ROLLUP_INTERVAL_S * 2.5


def test_frozen_process_produces_a_no_attestation_gap():
    """
    THE HEADLINE REGRESSION CASE.

    A real ~4h06m capture hole was missed by the original model: the SAME
    process (same run_id) simply stopped being scheduled by the OS (system
    suspend, not a network disconnect) for hours, wrote nothing at all —
    zero HEARTBEAT_ROLLUP, zero anything — and then resumed writing under
    the identical run_id once the machine woke. No WS_DISCONNECT, no
    RECORDER_STOP, no RESTART_BOUNDARY, no new RECORDER_START: every
    condition the original model required to close an interval was absent,
    so it read as continuously covered. This must now report a gap.
    """
    frozen_for = ATTESTATION_TOLERANCE_S * 3  # comfortably past the tolerance
    recs = [
        _rec(1, _mins(0), "RECORDER_START"),
        _rec(2, _mins(0), "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, T0 + timedelta(seconds=60), "HEARTBEAT_ROLLUP", frames_total=5),
        # <-- process frozen here (system suspend): nothing scheduled, nothing
        # written, for far longer than any normal rollup gap.
        _rec(4, T0 + timedelta(seconds=60 + frozen_for), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(5, T0 + timedelta(seconds=120 + frozen_for), "RECORDER_STOP"),
    ]
    ivs = coverage_intervals(recs)[("BTC/USD", "book")]
    last_attested = T0 + timedelta(seconds=60)
    resumed = T0 + timedelta(seconds=60 + frozen_for)
    assert [(i.start, i.end, i.closed_by) for i in ivs] == [
        (_mins(0), last_attested, "NO_ATTESTATION"),
        (resumed, T0 + timedelta(seconds=120 + frozen_for), "RECORDER_STOP"),
    ]
    gap = uncovered(ivs, _mins(0), T0 + timedelta(seconds=120 + frozen_for))
    assert gap == [(last_attested, resumed)]
    assert (resumed - last_attested).total_seconds() == frozen_for


def test_a_long_healthy_run_with_realistic_cadence_reports_no_gap():
    """Clean run must not report false gaps: two hours of real ~60s-cadence
    heartbeats (the actual production interval), never exceeding tolerance,
    must read as fully covered end to end."""
    recs = [
        _rec(1, T0, "RECORDER_START"),
        _rec(2, T0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
    ]
    jseq = 3
    n_rollups = int(2 * 3600 // ROLLUP_INTERVAL_S)
    for i in range(1, n_rollups + 1):
        recs.append(_rec(jseq, T0 + timedelta(seconds=i * ROLLUP_INTERVAL_S), "HEARTBEAT_ROLLUP", frames_total=5))
        jseq += 1
    end = T0 + timedelta(seconds=n_rollups * ROLLUP_INTERVAL_S)
    recs.append(_rec(jseq, end, "RECORDER_STOP"))

    ivs = coverage_intervals(recs)[("BTC/USD", "book")]
    assert len(ivs) == 1
    assert ivs[0].start == T0
    assert ivs[0].end == end
    assert uncovered(ivs, T0, end) == []


# ---------------------------------------------------------------------------
# uncovered() edge cases
# ---------------------------------------------------------------------------


def test_uncovered_with_no_intervals_is_the_whole_window():
    assert uncovered([], _mins(0), _mins(5)) == [(_mins(0), _mins(5))]


def test_uncovered_trims_a_request_that_overruns_coverage_on_both_sides():
    ivs = [Interval(_mins(10), _mins(20), "RECORDER_STOP", "r")]
    assert uncovered(ivs, _mins(5), _mins(25)) == [
        (_mins(5), _mins(10)),
        (_mins(20), _mins(25)),
    ]


def test_uncovered_rejects_inverted_window():
    with pytest.raises(ValueError):
        uncovered([], _mins(5), _mins(1))


# ---------------------------------------------------------------------------
# the read-boundary guard
# ---------------------------------------------------------------------------


def test_assert_covered_raises_on_a_gap_and_passes_inside_coverage(tmp_path):
    path = tmp_path / "_session.ndjson"
    recs = [
        _rec(1, _mins(0), "RECORDER_START"),
        _rec(2, _mins(1), "SUBSCRIBE_ACK", symbol="SOL/USD", channel="book"),
        _rec(3, _mins(2), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(4, _mins(3), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(5, _mins(4), "WS_DISCONNECT", reason="heartbeat_timeout"),
        _rec(6, _mins(7), "SUBSCRIBE_ACK", symbol="SOL/USD", channel="book"),
        _rec(7, _mins(8), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(8, _mins(9), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(9, _mins(10), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(10, _mins(11), "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(11, _mins(12), "RECORDER_STOP"),
    ]
    path.write_text("".join(json.dumps(r) + "\n" for r in recs), encoding="utf-8")

    assert_covered(path, "SOL/USD", "book", _mins(2), _mins(3))  # inside

    with pytest.raises(CoverageGapError) as exc:
        assert_covered(path, "SOL/USD", "book", _mins(2), _mins(9))
    assert "UNCAPTURED" in str(exc.value)

    # a symbol that was never subscribed is entirely unattested, not empty
    with pytest.raises(CoverageGapError):
        assert_covered(path, "DOGE/USD", "book", _mins(2), _mins(3))


# ---------------------------------------------------------------------------
# writer durability / restart continuity
# ---------------------------------------------------------------------------


def test_jseq_continues_across_process_restart(tmp_path):
    j1 = CoverageJournal(tmp_path)
    j1.record_start()
    j1.write("SUBSCRIBE_ACK", symbol="BTC/USD", channel="book")
    last = j1.write("RECORDER_STOP", reason="test")
    j1.close()

    j2 = CoverageJournal(tmp_path)
    start = j2.record_start()
    j2.close()

    assert start["jseq"] == last["jseq"] + 1
    assert start["prev_jseq"] == last["jseq"]
    assert start["prev_clean_shutdown"] is True
    assert start["run_id"] != last["run_id"]


def test_restart_after_crash_reports_unclean_predecessor(tmp_path):
    j1 = CoverageJournal(tmp_path)
    j1.record_start()
    j1.write("SUBSCRIBE_ACK", symbol="BTC/USD", channel="book")
    j1.close()  # no RECORDER_STOP == crash

    j2 = CoverageJournal(tmp_path)
    start = j2.record_start()
    j2.close()
    assert start["prev_clean_shutdown"] is False
    assert start["prev_offset"] > 0


def test_torn_final_line_is_reported_not_hidden(tmp_path):
    j = CoverageJournal(tmp_path)
    j.record_start()
    j.close()
    with open(j.path, "a", encoding="utf-8") as fh:
        fh.write('{"jseq":99,"type":"HEARTBE')  # killed mid-write

    state = read_tail_state(j.path)
    assert state["torn_tail"] is True
    assert state["last_jseq"] == 1
    assert len(load_records(j.path)) == 1  # the torn line is skipped, not parsed


def test_unknown_record_type_is_rejected_at_write_time(tmp_path):
    j = CoverageJournal(tmp_path)
    with pytest.raises(ValueError):
        j.write("TOTALLY_MADE_UP")
    j.close()


def test_every_record_carries_wall_clock_and_monotonic(tmp_path):
    j = CoverageJournal(tmp_path)
    r = j.record_start()
    j.close()
    assert parse_iso(r["ts"]).tzinfo is not None
    assert isinstance(r["mono"], float)
    assert r["run_id"]
