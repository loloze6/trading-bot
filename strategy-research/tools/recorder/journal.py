"""
Coverage journal — the recorder's answer to `FetchGapError`.
============================================================

WHY THIS FILE IS FIRST-CLASS
----------------------------
Kraken WS v2 publishes **no sequence numbers on the book channel** (build spec
§3; the L3 page states outright "no sequencing is required" and the documented
book fields are only `symbol`, `bids`, `asks`, `checksum`, `timestamp`).
Therefore *the market-data stream alone cannot distinguish "no activity" from
"not captured"*. A half-open TCP socket looks exactly like a quiet market: the
process stays alive, the log stays quiet, the shard simply stops growing.

That is the same defect shape as the motivating bug behind
`trading-bot/data/fetchers/base_fetcher.py:42-61` (`FetchGapError`): Kraken's
REST OHLC endpoint silently ignored `since`, `_fetch_remote` exited cleanly,
the write succeeded and the run logged success over a ~173-day hole. Its
docstring's rule is inherited verbatim here:

    "A wrong-data read that announces itself as success is the worst shape a
     data defect can take."

So coverage is not inferred from the data. It is **attested** by this journal,
written separately, `fsync`-ed per record, *before* the corresponding stream
action wherever the ordering is observable.

The second property of `_assert_no_new_gap` (`base_fetcher.py:293-330`) is also
inherited: the guard is **differential**. Only time that is *unattested* is a
defect. Attested-but-quiet is fine.

THE GUARD SITS AT THE READ BOUNDARY
-----------------------------------
`BaseFetcher` guards at the write boundary because it has a merge step. An
event stream has none — every byte is new. So the analogous guard is
`assert_covered()`, which **raises** `CoverageGapError` when a consumer asks
for a window the journal does not attest. It does not warn, and it does not
fill.

JOURNAL RECORD SCHEMA (one JSON object per line)
------------------------------------------------
    jseq     int    monotonically increasing across process restarts; the
                    successor process resumes from the last persisted value
    run_id   str    uuid4 of the writing process; `mono` is only comparable
                    within one run_id
    ts       str    UTC wall clock, RFC3339 with trailing 'Z'
    mono     float  time.monotonic() seconds since process start. Wall clock
                    alone cannot survive an NTP step or a laptop suspend;
                    mono alone cannot survive a restart. Both are recorded.
    type     str    one of RECORD_TYPES below
    ...      any    type-specific fields

RECORD TYPES
------------
    RECORDER_START     process boot; carries prev_jseq/prev_ts/prev_offset of
                       the predecessor process (§5.5: restart is not a
                       gap-eraser) and whether that predecessor shut down clean
    WS_CONNECT         socket open; carries Kraken `connection_id` once the
                       status frame arrives
    STATUS_CHANGE      system=online/maintenance/cancel_only/post_only
    SUBSCRIBE_ACK      per (symbol, channel) — OPENS a coverage interval
    HEARTBEAT_ROLLUP   one per minute: frames seen per symbol + heartbeat
                       count. A minute inside a coverage interval with zero
                       frames but a live heartbeat is COVERED-AND-QUIET.
    CHECKSUM_MISMATCH  book CRC32 disagreement (opens a DEGRADED span)
    WS_DISCONNECT      close code + reason — CLOSES all open intervals
    RECONNECT_ATTEMPT  attempt number + backoff seconds
    RESUBSCRIBE        resubscription issued after a reconnect
    RECORDER_STOP      clean shutdown — CLOSES all open intervals
    DISK_GUARD_ABORT   free-space floor breached; the recorder flushed, attested
                       and stopped. CLOSES all open intervals. This is an
                       ATTESTED stop, not a crash, and it is deliberately a
                       distinct type rather than a RECORDER_STOP with a reason
                       field: the supervisor must not relaunch into a full disk,
                       and a gap report must be able to name the cause without
                       parsing free text. See `disk_guard.py`.
    RESTART_BOUNDARY   written by the SUPERVISOR, between two recorder
                       processes, carrying the dead process's exit code. It
                       marks the downtime as attested rather than leaving it to
                       be inferred from the absence of records, and it closes
                       the dead run's intervals at that run's LAST OWN RECORD
                       (never at the marker), for the same reason
                       RECORDER_START does — see `coverage_intervals`.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

JOURNAL_FILENAME = "_session.ndjson"

RECORD_TYPES = frozenset(
    {
        "RECORDER_START",
        "WS_CONNECT",
        "STATUS_CHANGE",
        "SUBSCRIBE_ACK",
        "HEARTBEAT_ROLLUP",
        "CHECKSUM_MISMATCH",
        "WS_DISCONNECT",
        "RECONNECT_ATTEMPT",
        "RESUBSCRIBE",
        "RECORDER_STOP",
        "DISK_GUARD_ABORT",
        "RESTART_BOUNDARY",
    }
)

#: Record types that open a coverage interval for (symbol, channel).
_OPENING = "SUBSCRIBE_ACK"
#: Record types that close every currently-open coverage interval.
_CLOSING = frozenset({"WS_DISCONNECT", "RECORDER_STOP", "DISK_GUARD_ABORT"})

#: Types written by a DIFFERENT actor than the run whose intervals may still be
#: open — a successor recorder, or the supervisor. Seeing one means the previous
#: run is over; its intervals are closed at ITS last record, not at this one.
_NEW_ACTOR = frozenset({"RECORDER_START", "RESTART_BOUNDARY"})

#: Stop types that were ATTESTED by the stopping process. A journal ending in
#: one of these did not lose its tail to a crash. DISK_GUARD_ABORT belongs here
#: even though it is a failure: the failure is the disk, and the recorder's own
#: shutdown was orderly and recorded.
_ATTESTED_STOP = frozenset({"RECORDER_STOP", "DISK_GUARD_ABORT"})

#: Record types that are POSITIVE EVIDENCE the process was alive and
#: scheduled at that instant, for every (symbol, channel) pair currently open.
#: SUBSCRIBE_ACK attests its own pair; HEARTBEAT_ROLLUP is process-wide (one
#: per ROLLUP_INTERVAL_S, regardless of which pairs it reports on -- see
#: record_kraken_ws.py's `_rollup_loop`) and so renews every pair already open.
#: Nothing else counts: a WS_CONNECT, STATUS_CHANGE or RECONNECT_ATTEMPT proves
#: a socket event happened, not that the minute-cadence rollup loop is still
#: being scheduled by the OS -- and an unscheduled process is exactly the
#: failure mode (a suspended/frozen process, not merely a dead socket) that
#: coverage_intervals must not silently read as covered.
_ATTESTING = frozenset({"SUBSCRIBE_ACK", "HEARTBEAT_ROLLUP"})

#: Kept as a literal (not imported from record_kraken_ws) to avoid a circular
#: import -- record_kraken_ws imports CoverageJournal from this module.
#: test_journal.py::test_attestation_tolerance_matches_the_rollup_cadence
#: asserts this stays in lockstep with record_kraken_ws.ROLLUP_INTERVAL_S.
ROLLUP_INTERVAL_S = 60.0

#: 2.5x the rollup cadence -- the same real-world slack liveness.py already
#: uses ("newest rollup is Xs old (limit 150s)") for the live health check,
#: applied here to historical reconstruction so the two never disagree about
#: how much silence is normal jitter versus a real gap.
ATTESTATION_TOLERANCE_S = ROLLUP_INTERVAL_S * 2.5


class CoverageGapError(RuntimeError):
    """
    Raised at the READ boundary when a consumer requests a window that the
    coverage journal does not fully attest.

    This is the recorder's `FetchGapError` (`base_fetcher.py:42-61`), moved to
    the read side because an event stream has no merge step to guard. The
    contract is deliberately harsh: unattested time is never silently treated
    as "the market was quiet", never warned about, and never filled. A consumer
    that wants partial data must ask for a narrower window explicitly.
    """


def utcnow_iso() -> str:
    """UTC wall clock, RFC3339, microsecond precision, trailing 'Z'."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def parse_iso(ts: str) -> datetime:
    """Inverse of :func:`utcnow_iso`, tolerant of '+00:00' and missing micros."""
    s = ts.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------


class CoverageJournal:
    """
    Append-only, `fsync`-per-record journal writer.

    `fsync` on every record is deliberate and is NOT a candidate for batching.
    The journal's entire value is that it is durable at the instant of the
    event it describes; a journal that loses its tail in the same crash that
    ended the capture attests coverage that never happened — which is the
    announce-success-over-a-hole failure this class exists to prevent. Volume
    is ~20 records/hour plus one rollup/minute, so the cost is irrelevant.
    """

    def __init__(self, out_dir: Path):
        self.path = Path(out_dir) / JOURNAL_FILENAME
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.run_id = str(uuid.uuid4())
        self._t0 = time.monotonic()

        prev = read_tail_state(self.path)
        self._jseq = prev["last_jseq"]
        self._fh = open(self.path, "a", encoding="utf-8", newline="\n")
        self._prev = prev

    # -- lifecycle ---------------------------------------------------------

    def record_start(self, **fields: Any) -> Dict[str, Any]:
        """
        Write RECORDER_START, carrying the predecessor's last journal position.

        §5.5 — restart is not a gap-eraser. An operator-invisible crash-restart
        must surface as a bounded UNCAPTURED interval, not as continuous
        coverage, so the successor records where its predecessor stopped and
        whether that stop was clean.
        """
        return self.write(
            "RECORDER_START",
            prev_jseq=self._prev["last_jseq"],
            prev_ts=self._prev["last_ts"],
            prev_offset=self._prev["offset"],
            prev_run_id=self._prev["last_run_id"],
            prev_clean_shutdown=self._prev["clean_shutdown"],
            prev_torn_tail=self._prev["torn_tail"],
            pid=os.getpid(),
            **fields,
        )

    def write(self, rtype: str, **fields: Any) -> Dict[str, Any]:
        if rtype not in RECORD_TYPES:
            raise ValueError(f"unknown journal record type: {rtype!r}")
        self._jseq += 1
        rec: Dict[str, Any] = {
            "jseq": self._jseq,
            "run_id": self.run_id,
            "ts": utcnow_iso(),
            "mono": round(time.monotonic() - self._t0, 6),
            "type": rtype,
        }
        rec.update(fields)
        self._fh.write(json.dumps(rec, separators=(",", ":"), sort_keys=False) + "\n")
        self._fh.flush()
        os.fsync(self._fh.fileno())
        return rec

    def close(self) -> None:
        try:
            self._fh.flush()
            os.fsync(self._fh.fileno())
        finally:
            self._fh.close()


# ---------------------------------------------------------------------------
# Reader
# ---------------------------------------------------------------------------


def read_tail_state(path: Path) -> Dict[str, Any]:
    """
    Cheaply recover what the previous process left behind.

    `torn_tail` reports a final line that does not parse. `fsync`-per-record
    makes this improbable but not impossible (a kill between `write` and the
    completion of the underlying block write). It is reported rather than
    repaired: a torn tail is evidence about coverage and the consumer must see
    it.
    """
    state = {
        "last_jseq": 0,
        "last_ts": None,
        "last_run_id": None,
        "last_type": None,
        "offset": 0,
        "clean_shutdown": None,
        "torn_tail": False,
    }
    p = Path(path)
    if not p.exists():
        return state
    state["offset"] = p.stat().st_size
    last_type = None
    with open(p, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                state["torn_tail"] = True
                continue
            state["torn_tail"] = False
            state["last_jseq"] = max(state["last_jseq"], int(rec.get("jseq", 0)))
            state["last_ts"] = rec.get("ts", state["last_ts"])
            state["last_run_id"] = rec.get("run_id", state["last_run_id"])
            last_type = rec.get("type")
    state["last_type"] = last_type
    # A guard abort is an attested stop as much as a clean one — the successor
    # must not report it as `prev_clean_shutdown: false`, which means "we lost
    # the tail to a crash". `last_type` is carried alongside so a consumer that
    # needs to tell the two apart still can.
    state["clean_shutdown"] = last_type in _ATTESTED_STOP if last_type else None
    return state


def load_records(path: Path) -> List[Dict[str, Any]]:
    """Parse the journal, skipping (but not hiding) an unparseable final line."""
    p = Path(path)
    if not p.exists():
        return []
    out: List[Dict[str, Any]] = []
    with open(p, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


@dataclass(frozen=True)
class Interval:
    """One attested-covered span for a (symbol, channel) pair."""

    start: datetime
    end: datetime
    closed_by: str  # RECORDER_STOP | WS_DISCONNECT | UNCLEAN_SHUTDOWN | OPEN_TAIL
    run_id: str

    def __contains__(self, t: datetime) -> bool:
        return self.start <= t <= self.end


def coverage_intervals(records: Sequence[Dict[str, Any]]) -> Dict[Tuple[str, str], List[Interval]]:
    """
    Reconstruct, per (symbol, channel), the wall-clock spans the journal
    attests were captured.

    POSITIVE-EVIDENCE, DENY BY DEFAULT
    -----------------------------------
    A span counts as covered only where it is actively attested at the
    expected cadence (`_ATTESTING` / `ATTESTATION_TOLERANCE_S`), not merely
    "opened and never explicitly closed". The original design closed an
    interval only on an explicit CLOSING record, which meant a process that
    stopped being scheduled by the OS entirely (a suspend/freeze -- zero
    HEARTBEAT_ROLLUPs, not just zero network frames) produced no closing
    record and read as continuously covered for as long as the SAME run_id
    eventually resumed and kept writing. A real ~4h06m capture hole was missed
    this way (SESSION_LOG.md 2026-07-27) because the successor records, once
    the process unfroze, belonged to the same run_id and so never tripped
    UNCLEAN_SHUTDOWN. Absence of attestation is now a gap regardless of cause,
    with its own `NO_ATTESTATION` reason distinct from an explicit close.

    Interval semantics:
      * opened by SUBSCRIBE_ACK(symbol, channel); attestation (`covered_since`)
        starts at that same instant;
      * renewed by every subsequent SUBSCRIBE_ACK or HEARTBEAT_ROLLUP while the
        pair stays open -- HEARTBEAT_ROLLUP renews EVERY currently-open pair,
        since one is written per ROLLUP_INTERVAL_S regardless of which pairs
        it reports on;
      * closed by `NO_ATTESTATION` the instant more than ATTESTATION_TOLERANCE_S
        elapses since the last renewal with no new one -- checked against
        every record's timestamp, not just attesting ones, so a stray
        non-attesting record arriving after a long silence is what surfaces
        the gap. The pair stays open (still nominally subscribed) but
        unattested until the next SUBSCRIBE_ACK/HEARTBEAT_ROLLUP reopens it;
      * closed by WS_DISCONNECT, RECORDER_STOP or DISK_GUARD_ABORT;
      * closed by UNCLEAN_SHUTDOWN at the *last record of the dead run* when a
        record from a NEW ACTOR (a successor RECORDER_START, or the
        supervisor's RESTART_BOUNDARY) appears while intervals from an earlier
        run_id are still open. Closing at the new record would silently claim
        coverage across the crash window — the exact failure mode this module
        exists to prevent — so the honest bound is the last thing the dead
        process actually attested;
      * closed by OPEN_TAIL at the last record in the journal when the recorder
        is still running. Coverage is attested only up to the newest record,
        never to "now": a process that died 40 minutes ago and a process that
        is healthy right now have identical journal tails until the next
        rollup lands.

    A pair that is open but currently in a NO_ATTESTATION gap when the journal
    ends emits no OPEN_TAIL interval (there is nothing attested left to flush)
    — the caller sees exactly the last attested instant, same as any other gap.
    """
    open_since: Dict[Tuple[str, str], Tuple[datetime, str]] = {}
    #: Start of the currently-attested run for a key, or None while that key
    #: is open but sitting in an unattested (NO_ATTESTATION) gap.
    covered_since: Dict[Tuple[str, str], Optional[datetime]] = {}
    last_attested: Dict[Tuple[str, str], datetime] = {}
    result: Dict[Tuple[str, str], List[Interval]] = {}
    last_ts: Optional[datetime] = None
    last_run: Optional[str] = None
    tolerance = timedelta(seconds=ATTESTATION_TOLERANCE_S)

    def flush(key: Tuple[str, str], end: datetime, reason: str) -> None:
        start = covered_since.get(key)
        if start is not None and end >= start:
            result.setdefault(key, []).append(
                Interval(start=start, end=end, closed_by=reason, run_id=open_since[key][1])
            )
        covered_since[key] = None

    def close_all(at: datetime, reason: str) -> None:
        for key in list(open_since.keys()):
            flush(key, at, reason)
        open_since.clear()
        covered_since.clear()
        last_attested.clear()

    for rec in records:
        rtype = rec.get("type")
        ts_raw = rec.get("ts")
        if rtype not in RECORD_TYPES or not ts_raw:
            continue
        ts = parse_iso(ts_raw)
        run_id = rec.get("run_id", "")

        if rtype in _NEW_ACTOR and open_since and run_id != last_run:
            close_all(last_ts if last_ts else ts, "UNCLEAN_SHUTDOWN")

        # Cadence check FIRST, using this record's own timestamp, regardless
        # of its type: any record proves the journal has reached `ts` without
        # an intervening attestation, for every key still open.
        for key in list(open_since.keys()):
            if covered_since.get(key) is not None and ts - last_attested[key] > tolerance:
                flush(key, last_attested[key], "NO_ATTESTATION")

        if rtype == _OPENING:
            sym = rec.get("symbol")
            chan = rec.get("channel")
            if sym and chan:
                key = (sym, chan)
                if key not in open_since:
                    open_since[key] = (ts, run_id)
                    covered_since[key] = ts
                last_attested[key] = ts
                if covered_since.get(key) is None:
                    covered_since[key] = ts
        elif rtype == "HEARTBEAT_ROLLUP":
            for key in list(open_since.keys()):
                if covered_since.get(key) is None:
                    covered_since[key] = ts
                last_attested[key] = ts
        elif rtype in _CLOSING:
            close_all(ts, rtype)

        last_ts = ts
        last_run = run_id

    if open_since and last_ts is not None:
        close_all(last_ts, "OPEN_TAIL")

    for key in result:
        result[key] = _merge(result[key])
    return result


def _merge(intervals: List[Interval]) -> List[Interval]:
    """Merge touching/overlapping spans; keeps the later `closed_by`."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda i: (i.start, i.end))
    merged = [ordered[0]]
    for iv in ordered[1:]:
        prev = merged[-1]
        if iv.start <= prev.end:
            merged[-1] = Interval(
                start=prev.start,
                end=max(prev.end, iv.end),
                closed_by=iv.closed_by if iv.end >= prev.end else prev.closed_by,
                run_id=iv.run_id,
            )
        else:
            merged.append(iv)
    return merged


def uncovered(intervals: Iterable[Interval], start: datetime, end: datetime) -> List[Tuple[datetime, datetime]]:
    """Sub-spans of [start, end] that no interval attests. Empty == fully covered."""
    if end < start:
        raise ValueError("end precedes start")
    gaps: List[Tuple[datetime, datetime]] = []
    cursor = start
    for iv in sorted(intervals, key=lambda i: i.start):
        if iv.end < cursor:
            continue
        if iv.start > end:
            break
        if iv.start > cursor:
            gaps.append((cursor, min(iv.start, end)))
        cursor = max(cursor, iv.end)
        if cursor >= end:
            break
    if cursor < end:
        gaps.append((cursor, end))
    return gaps


def assert_covered(
    journal_path: Path,
    symbol: str,
    channel: str,
    start: datetime,
    end: datetime,
) -> None:
    """
    The recorder's `FetchGapError`, at the read boundary.

    Raise `CoverageGapError` unless the journal attests every instant of
    [start, end] for (symbol, channel). Consumers MUST call this before
    treating an absence of frames as an absence of market activity.
    """
    ivs = coverage_intervals(load_records(journal_path)).get((symbol, channel), [])
    gaps = uncovered(ivs, start, end)
    if gaps:
        rendered = ", ".join(f"[{g[0].isoformat()} .. {g[1].isoformat()}]" for g in gaps)
        raise CoverageGapError(
            f"{symbol}/{channel}: journal does not attest "
            f"{len(gaps)} sub-window(s) of the requested range: {rendered}. "
            "Unattested time is UNCAPTURED, not quiet — refusing to serve it."
        )
