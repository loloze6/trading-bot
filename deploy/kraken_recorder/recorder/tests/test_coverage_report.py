"""
Coverage gap report against synthetic journals with known gaps.

Every fixture here states its answer in advance — "60s uncaptured, cause X" —
because the whole point of the report is that downtime stops being something an
operator reconstructs from file sizes and becomes something the journal says
out loud.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from recorder.coverage_report import (
    Gap,
    covered_spans,
    gaps,
    journal_window,
    main,
    render,
)
from recorder.journal import JOURNAL_FILENAME

T0 = datetime(2026, 7, 27, 12, 0, 0, tzinfo=timezone.utc)


def _at(seconds):
    return T0 + timedelta(seconds=seconds)


def _rec(jseq, seconds, rtype, run_id="run-a", **kw):
    d = {
        "jseq": jseq,
        "run_id": run_id,
        "ts": _at(seconds).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z",
        "mono": float(seconds),
        "type": rtype,
    }
    d.update(kw)
    return d


def _write(tmp_path, records):
    p = tmp_path / JOURNAL_FILENAME
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        for r in records:
            fh.write(json.dumps(r, separators=(",", ":")) + "\n")
    return p


def _one_pair(seconds, rtype, jseq, **kw):
    return _rec(jseq, seconds, rtype, **kw)


# ---------------------------------------------------------------------------
# the headline case: a disconnect gap of known size and cause
# ---------------------------------------------------------------------------


def _disconnect_journal():
    """Captured 0-100 and 200-300 of a 300 s window. Gap: 100 s, ws_disconnect."""
    return [
        _rec(1, 0, "RECORDER_START", prev_clean_shutdown=None),
        _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, 100, "WS_DISCONNECT", code=1006, reason="ConnectionClosed"),
        _rec(4, 200, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(5, 300, "RECORDER_STOP", reason="signal_or_eof"),
    ]


def test_a_known_gap_is_reported_with_start_end_duration_and_cause():
    found, window, covered = gaps(_disconnect_journal())
    assert window == (_at(0), _at(300))
    assert len(found) == 1
    g = found[0]
    assert (g.start, g.end) == (_at(100), _at(200))
    assert g.duration_s == 100.0
    assert g.cause == "ws_disconnect"
    assert "ConnectionClosed" in g.detail


def test_captured_versus_elapsed_percentage(tmp_path):
    records = _disconnect_journal()
    found, window, covered = gaps(records)
    lines = render(tmp_path / JOURNAL_FILENAME, records, found, window, covered, None, None)
    text = "\n".join(lines)
    # 200 s captured of 300 s elapsed.
    assert "66.667%" in text
    assert "33.333%" in text
    assert "0h01m40s" in text  # the 100 s gap


def test_a_fully_covered_journal_reports_no_gaps():
    records = [
        _rec(1, 0, "RECORDER_START"),
        _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, 100, "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(4, 200, "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(5, 300, "RECORDER_STOP"),
    ]
    found, _window, _covered = gaps(records)
    assert found == []


# ---------------------------------------------------------------------------
# cause attribution
# ---------------------------------------------------------------------------


def test_a_guard_abort_gap_names_the_disk_not_a_crash():
    records = [
        _rec(1, 0, "RECORDER_START"),
        _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(
            3,
            60,
            "DISK_GUARD_ABORT",
            free_gb=1.2,
            min_free_gb=5.0,
            reason="free space below configured floor",
            determinable=True,
        ),
    ]
    found, _w, _c = gaps(records, window=(_at(0), _at(120)))
    assert len(found) == 1
    assert found[0].cause == "disk_guard_abort"
    assert "1.2" in found[0].detail and "5.0" in found[0].detail


def test_a_clean_stop_gap_is_labelled_clean_stop():
    records = [
        _rec(1, 0, "RECORDER_START"),
        _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, 60, "RECORDER_STOP", reason="signal_or_eof"),
    ]
    found, _w, _c = gaps(records, window=(_at(0), _at(120)))
    assert [g.cause for g in found] == ["clean_stop"]


def test_a_supervisor_restart_gap_carries_the_dead_processs_exit_code():
    """
    This is why the supervisor writes to the journal at all: without
    RESTART_BOUNDARY the same downtime reports as `crash` at best and `unknown`
    if the successor never starts.
    """
    records = [
        _rec(1, 0, "RECORDER_START"),
        _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, 50, "HEARTBEAT_ROLLUP", heartbeats=50, frames_total=10),
        # process dies here without attesting anything
        _rec(
            4,
            55,
            "RESTART_BOUNDARY",
            run_id="supervisor",
            exit_code=1,
            attempt=2,
            backoff_s=10,
            reason="recorder exited 1",
        ),
        _rec(5, 65, "RECORDER_START", run_id="run-b", prev_clean_shutdown=False),
        _rec(6, 65, "SUBSCRIBE_ACK", run_id="run-b", symbol="BTC/USD", channel="book"),
        _rec(7, 120, "RECORDER_STOP", run_id="run-b"),
    ]
    found, _w, _c = gaps(records)
    assert len(found) == 1
    g = found[0]
    # Closed at the dead run's LAST OWN RECORD (t=50), never at the marker.
    assert (g.start, g.end) == (_at(50), _at(65))
    assert g.cause == "restart"
    assert "exit_code=1" in g.detail


def test_an_unsupervised_crash_gap_is_labelled_crash():
    records = [
        _rec(1, 0, "RECORDER_START"),
        _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, 50, "HEARTBEAT_ROLLUP", heartbeats=50, frames_total=10),
        _rec(4, 90, "RECORDER_START", run_id="run-b", prev_clean_shutdown=False, prev_run_id="run-a"),
        _rec(5, 90, "SUBSCRIBE_ACK", run_id="run-b", symbol="BTC/USD", channel="book"),
        _rec(6, 120, "RECORDER_STOP", run_id="run-b"),
    ]
    found, _w, _c = gaps(records)
    assert [g.cause for g in found] == ["crash"]
    assert (found[0].start, found[0].end) == (_at(50), _at(90))


def test_time_before_the_first_ack_is_not_yet_started():
    records = [
        _rec(1, 0, "RECORDER_START"),
        _rec(2, 30, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, 120, "RECORDER_STOP"),
    ]
    found, _w, _c = gaps(records)
    assert [g.cause for g in found] == ["not_yet_started"]
    assert found[0].duration_s == 30.0


def test_an_unattributable_gap_says_unknown_rather_than_guessing():
    records = [
        _rec(1, 0, "RECORDER_START"),
        _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, 40, "HEARTBEAT_ROLLUP", heartbeats=40),
        _rec(4, 90, "RECORDER_START", run_id="run-b", prev_clean_shutdown=None),
        _rec(5, 90, "SUBSCRIBE_ACK", run_id="run-b", symbol="BTC/USD", channel="book"),
        _rec(6, 100, "RECORDER_STOP", run_id="run-b"),
    ]
    found, _w, _c = gaps(records)
    assert [g.cause for g in found] == ["unknown"]


def test_a_frozen_process_gap_is_labelled_no_attestation_not_invisible():
    """
    THE HEADLINE CASE: a real ~4h06m
    hole under one continuous run_id, no closing record anywhere, used to
    report ~100% captured. It must now be a reported gap with its own cause,
    distinct from ws_disconnect/crash/unknown.
    """
    frozen_for = 600.0  # comfortably past ATTESTATION_TOLERANCE_S (150s)
    records = [
        _rec(1, 0, "RECORDER_START"),
        _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, 60, "HEARTBEAT_ROLLUP", frames_total=5),
        # <-- system suspend here; the process writes nothing at all
        _rec(4, 60 + frozen_for, "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(5, 120 + frozen_for, "RECORDER_STOP"),
    ]
    found, _w, _c = gaps(records)
    assert len(found) == 1
    g = found[0]
    assert (g.start, g.end) == (_at(60), _at(60 + frozen_for))
    assert g.duration_s == frozen_for
    assert g.cause == "no_attestation"
    assert "dead air" in g.detail


def test_a_long_healthy_run_with_realistic_cadence_reports_no_false_gap():
    """Clean run must not report false gaps: two hours of real ~60s-cadence
    heartbeats must read as fully covered end to end."""
    records = [_rec(1, 0, "RECORDER_START"), _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book")]
    jseq = 3
    n_rollups = int(2 * 3600 // 60)
    for i in range(1, n_rollups + 1):
        records.append(_rec(jseq, i * 60, "HEARTBEAT_ROLLUP", frames_total=5))
        jseq += 1
    end_s = n_rollups * 60
    records.append(_rec(jseq, end_s, "RECORDER_STOP"))

    found, _w, _c = gaps(records)
    assert found == []


# ---------------------------------------------------------------------------
# strict (intersection) coverage
# ---------------------------------------------------------------------------


def test_one_pair_dropping_out_makes_the_window_uncaptured():
    """
    19 subscribed and 18 delivering is a partial-coverage defect, not a rounding
    error — the same rule liveness check 3 enforces live. A union would hide it.
    """
    records = [
        _rec(1, 0, "RECORDER_START"),
        _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(3, 0, "SUBSCRIBE_ACK", symbol="ETH/USD", channel="book"),
        _rec(4, 100, "WS_DISCONNECT", reason="drop"),
        # only BTC comes back
        _rec(5, 120, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
        _rec(6, 220, "HEARTBEAT_ROLLUP", frames_total=5),
        _rec(7, 300, "RECORDER_STOP"),
    ]
    found, _w, _c = gaps(records)
    assert [(g.start, g.end) for g in found] == [(_at(100), _at(300))]

    # ...and the per-pair view still shows BTC as covered throughout.
    btc, _w, _c = gaps(records, symbol="BTC/USD")
    assert [(g.start, g.end) for g in btc] == [(_at(100), _at(120))]


def test_covered_spans_of_an_empty_selection_is_no_coverage():
    records = [_rec(1, 0, "RECORDER_START"), _rec(2, 10, "RECORDER_STOP")]
    assert covered_spans(records, symbol="NOPE/USD") == []


def test_journal_window_is_the_records_not_now():
    records = _disconnect_journal()
    assert journal_window(records) == (_at(0), _at(300))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_prints_the_gap_and_exits_zero_by_default(tmp_path, capsys):
    _write(tmp_path, _disconnect_journal())
    assert main(["--out", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "COVERAGE GAP REPORT" in out
    assert "ws_disconnect" in out
    assert "66.667%" in out


def test_cli_fail_on_gap_exits_nonzero(tmp_path):
    _write(tmp_path, _disconnect_journal())
    assert main(["--out", str(tmp_path), "--fail-on-gap"]) == 1


def test_cli_on_a_clean_journal_says_none_and_exits_zero(tmp_path, capsys):
    _write(
        tmp_path,
        [
            _rec(1, 0, "RECORDER_START"),
            _rec(2, 0, "SUBSCRIBE_ACK", symbol="BTC/USD", channel="book"),
            _rec(3, 100, "HEARTBEAT_ROLLUP", frames_total=5),
            _rec(4, 200, "HEARTBEAT_ROLLUP", frames_total=5),
            _rec(5, 300, "RECORDER_STOP"),
        ],
    )
    assert main(["--out", str(tmp_path), "--fail-on-gap"]) == 0
    assert "GAPS: none" in capsys.readouterr().out


def test_a_missing_journal_is_uncaptured_not_clean(tmp_path, capsys):
    """Absence of a journal must never read as 'nothing went wrong'."""
    assert main(["--out", str(tmp_path)]) == 1
    assert "UNCAPTURED" in capsys.readouterr().out
