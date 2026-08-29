"""
Coverage gap report — downtime made visible instead of inferred.
================================================================

    python -m recorder.coverage_report

`journal.assert_covered` answers "is THIS window captured?" for one consumer
asking about one span. It is the read-boundary guard and it raises. This module
answers the operator's question instead: *over the whole life of this capture,
which intervals were NOT captured, for how long, and why?*

Without it, downtime is invisible. A recorder that died at 03:00 and was
restarted at 07:00 leaves a journal that says so precisely — and nobody reads
raw NDJSON. The alternative in practice is reconstructing the outage from shard
file sizes weeks later, which is guesswork about the one property
(`book` history) that can never be re-fetched.

WHAT COUNTS AS CAPTURED — THE STRICT READING
--------------------------------------------
An instant counts as captured only when EVERY (symbol, channel) pair the
journal has ever attested is covered at that instant. It is an intersection,
not a union.

This is deliberate and it is the same rule `liveness.py` check 3 enforces
live: 19 pairs subscribed and 18 delivering is a partial-coverage defect, not a
rounding error, and a report that averaged it away would hide exactly the
failure the subscription-ack accounting exists to surface. A per-pair view is
available with `--symbol`/`--channel`.

CAUSE ATTRIBUTION — ATTESTED FIRST, INFERRED ONLY AS A LAST RESORT
------------------------------------------------------------------
Each gap is labelled with what the journal actually says, in this order:

  disk_guard_abort  the gap opens at a DISK_GUARD_ABORT — the free-space floor
                    stopped the capture, attested (`disk_guard.py`)
  clean_stop        opens at a RECORDER_STOP — an operator stopped it
  ws_disconnect     opens at a WS_DISCONNECT the recorder never recovered from
                    inside this window
  restart           a supervisor RESTART_BOUNDARY sits inside the gap; it
                    carries the dead process's exit code
  crash             no closing record at all, and the next RECORDER_START
                    reports `prev_clean_shutdown: false` — the process died
                    without attesting anything
  no_attestation    the gap starts exactly at the journal's last
                    SUBSCRIBE_ACK/HEARTBEAT_ROLLUP before a silence exceeding
                    `journal.ATTESTATION_TOLERANCE_S`, with no explicit close,
                    no supervisor restart and no successor crash marker — the
                    SAME run_id simply stopped being scheduled by the OS
                    (suspend/freeze) and later resumed. This is what a real
                    ~4h06m capture hole looked like before this cause existed
                    (SESSION_LOG.md 2026-07-27): zero closing record, so the
                    old model read it as continuously covered.
  not_yet_started   before the first SUBSCRIBE_ACK in the window
  unknown           none of the above. Reported as unknown; never guessed at,
                    and never quietly folded into one of the others.

`unknown` is a real answer here, not a failure of the report. A gap whose cause
cannot be named from the journal is exactly the thing an operator needs to see.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

if __package__ in (None, ""):  # allow `python coverage_report.py`
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.journal import (  # type: ignore
        JOURNAL_FILENAME,
        coverage_intervals,
        load_records,
        parse_iso,
    )
    from recorder.record_kraken_ws import DEFAULT_OUT  # type: ignore
else:
    from .journal import (
        JOURNAL_FILENAME,
        coverage_intervals,
        load_records,
        parse_iso,
    )
    from .record_kraken_ws import DEFAULT_OUT

Span = Tuple[datetime, datetime]

#: Positive-evidence record types — mirrors journal._ATTESTING. Kept as its
#: own copy (not imported) because that name is module-private to journal.py;
#: test_coverage_report.py checks the two stay in lockstep.
_ATTESTING = frozenset({"SUBSCRIBE_ACK", "HEARTBEAT_ROLLUP"})

CAUSE_BY_CLOSING_TYPE = {
    "DISK_GUARD_ABORT": "disk_guard_abort",
    "RECORDER_STOP": "clean_stop",
    "WS_DISCONNECT": "ws_disconnect",
}


@dataclass(frozen=True)
class Gap:
    start: datetime
    end: datetime
    cause: str
    detail: str

    @property
    def duration_s(self) -> float:
        return (self.end - self.start).total_seconds()


def _merge(spans: Sequence[Span]) -> List[Span]:
    if not spans:
        return []
    out: List[Span] = []
    for s, e in sorted(spans):
        if out and s <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out


def _intersect(a: Sequence[Span], b: Sequence[Span]) -> List[Span]:
    out: List[Span] = []
    i = j = 0
    while i < len(a) and j < len(b):
        lo = max(a[i][0], b[j][0])
        hi = min(a[i][1], b[j][1])
        if lo < hi:
            out.append((lo, hi))
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return out


def covered_spans(
    records: Sequence[Dict[str, Any]],
    symbol: Optional[str] = None,
    channel: Optional[str] = None,
) -> List[Span]:
    """
    Spans in which every selected (symbol, channel) pair is attested — see
    WHAT COUNTS AS CAPTURED. With no filter this is the intersection across all
    pairs the journal mentions; an empty selection yields no coverage at all,
    which is the deny-by-default answer, not an error.
    """
    by_key = coverage_intervals(records)
    keys = [
        k
        for k in by_key
        if (symbol is None or k[0] == symbol) and (channel is None or k[1] == channel)
    ]
    if not keys:
        return []
    acc = _merge([(iv.start, iv.end) for iv in by_key[keys[0]]])
    for key in keys[1:]:
        acc = _intersect(acc, _merge([(iv.start, iv.end) for iv in by_key[key]]))
        if not acc:
            break
    return acc


def journal_window(records: Sequence[Dict[str, Any]]) -> Optional[Span]:
    """[first record, last record]. Coverage is never claimed beyond the newest
    record — a process that died 40 minutes ago and one that is healthy right
    now have identical tails until the next rollup lands."""
    stamps = [parse_iso(r["ts"]) for r in records if r.get("ts")]
    if not stamps:
        return None
    return min(stamps), max(stamps)


def _closing_before(
    records: Sequence[Dict[str, Any]], at: datetime
) -> Optional[Dict[str, Any]]:
    """The newest interval-closing record at or before `at`."""
    best = None
    for rec in records:
        ts_raw = rec.get("ts")
        if not ts_raw or rec.get("type") not in CAUSE_BY_CLOSING_TYPE:
            continue
        ts = parse_iso(ts_raw)
        if ts <= at and (best is None or ts >= parse_iso(best["ts"])):
            best = rec
    return best


def _attestation_before(
    records: Sequence[Dict[str, Any]], at: datetime
) -> Optional[Dict[str, Any]]:
    """The newest SUBSCRIBE_ACK/HEARTBEAT_ROLLUP record at or before `at`."""
    best = None
    for rec in records:
        ts_raw = rec.get("ts")
        if not ts_raw or rec.get("type") not in _ATTESTING:
            continue
        ts = parse_iso(ts_raw)
        if ts <= at and (best is None or ts >= parse_iso(best["ts"])):
            best = rec
    return best


def _attribute(
    records: Sequence[Dict[str, Any]],
    gap: Span,
    first_ack: Optional[datetime],
) -> Tuple[str, str]:
    start, end = gap
    if first_ack is not None and end <= first_ack:
        return "not_yet_started", "before the first SUBSCRIBE_ACK in this journal"

    closing = _closing_before(records, start)
    # Tolerance: a closing record and the interval end it produces are the same
    # instant by construction, so an exact match is expected; anything older
    # belongs to an earlier gap and must not be borrowed for this one.
    if closing is not None and parse_iso(closing["ts"]) == start:
        cause = CAUSE_BY_CLOSING_TYPE[closing["type"]]
        if cause == "disk_guard_abort":
            detail = (
                f"free_gb={closing.get('free_gb')} floor_gb={closing.get('min_free_gb')} "
                f"({closing.get('reason')})"
            )
        elif cause == "ws_disconnect":
            detail = f"reason={closing.get('reason')!r} code={closing.get('code')!r}"
        else:
            detail = f"reason={closing.get('reason')!r}"
        return cause, detail

    inside = [
        r
        for r in records
        if r.get("type") == "RESTART_BOUNDARY"
        and r.get("ts")
        and start <= parse_iso(r["ts"]) <= end
    ]
    if inside:
        r = inside[0]
        return "restart", (
            f"supervisor relaunch #{r.get('attempt')} after exit_code="
            f"{r.get('exit_code')}; {r.get('reason')}"
        )

    later_starts = [
        r
        for r in records
        if r.get("type") == "RECORDER_START"
        and r.get("ts")
        and parse_iso(r["ts"]) >= end
    ]
    if later_starts and later_starts[0].get("prev_clean_shutdown") is False:
        return "crash", (
            "successor RECORDER_START reports prev_clean_shutdown=false "
            f"(prev_run_id={later_starts[0].get('prev_run_id')})"
        )

    # A gap bounded by ANY run transition (a RECORDER_START at or after `end`,
    # regardless of what prev_clean_shutdown says) is restart/crash territory,
    # already checked above and not resolved — it must fall through to
    # `unknown` rather than being reattributed below. Without this gate, a
    # gap that happens to start exactly on the dead run's last
    # SUBSCRIBE_ACK/HEARTBEAT_ROLLUP (common — those are the most frequent
    # record types) would be misread as a same-run cadence violation when it
    # is really an unattributable predecessor/successor boundary.
    if not later_starts:
        # By construction of journal.coverage_intervals, a gap that is NOT
        # bounded by a run transition and does not match an explicit closing
        # record opens at exactly one place: a NO_ATTESTATION split, i.e. the
        # journal's last SUBSCRIBE_ACK/HEARTBEAT_ROLLUP before a silence. This
        # is what a real ~4h06m capture hole looked like before this cause
        # existed: no closing record, so it read as continuously covered.
        last_attestation = _attestation_before(records, start)
        if last_attestation is not None and parse_iso(last_attestation["ts"]) == start:
            return "no_attestation", (
                f"last positive attestation ({last_attestation['type']}) at "
                f"{start.isoformat()}; no SUBSCRIBE_ACK/HEARTBEAT_ROLLUP until "
                f"{end.isoformat()} ({(end - start).total_seconds():.0f}s of dead "
                "air — an OS-level process freeze/suspend signature, not a "
                "network disconnect the process could attest to"
            )

    return "unknown", "no closing record and no successor attestation"


def gaps(
    records: Sequence[Dict[str, Any]],
    window: Optional[Span] = None,
    symbol: Optional[str] = None,
    channel: Optional[str] = None,
) -> Tuple[List[Gap], Span, List[Span]]:
    """(gaps, window, covered spans clipped to the window)."""
    win = window or journal_window(records)
    if win is None:
        raise ValueError("journal has no timestamped records — nothing to report")
    w0, w1 = win
    if w1 < w0:
        raise ValueError("window end precedes window start")

    covered = [
        (max(s, w0), min(e, w1))
        for s, e in covered_spans(records, symbol=symbol, channel=channel)
        if e > w0 and s < w1
    ]
    covered = _merge(covered)

    acks = [
        parse_iso(r["ts"])
        for r in records
        if r.get("type") == "SUBSCRIBE_ACK" and r.get("ts")
    ]
    first_ack = min(acks) if acks else None

    raw: List[Span] = []
    cursor = w0
    for s, e in covered:
        if s > cursor:
            raw.append((cursor, s))
        cursor = max(cursor, e)
    if cursor < w1:
        raw.append((cursor, w1))

    out = []
    for g in raw:
        cause, detail = _attribute(records, g, first_ack)
        out.append(Gap(start=g[0], end=g[1], cause=cause, detail=detail))
    return out, (w0, w1), covered


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------


def _dur(seconds: float) -> str:
    s = int(round(seconds))
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h:d}h{m:02d}m{sec:02d}s"


def render(
    journal_path: Path,
    records: Sequence[Dict[str, Any]],
    found: Sequence[Gap],
    window: Span,
    covered: Sequence[Span],
    symbol: Optional[str],
    channel: Optional[str],
) -> List[str]:
    w0, w1 = window
    elapsed = (w1 - w0).total_seconds()
    captured = sum((e - s).total_seconds() for s, e in covered)
    uncaptured = sum(g.duration_s for g in found)
    keys = coverage_intervals(records)
    selected = [
        k
        for k in keys
        if (symbol is None or k[0] == symbol) and (channel is None or k[1] == channel)
    ]

    lines = [
        "COVERAGE GAP REPORT",
        f"  journal   : {journal_path}",
        f"  records   : {len(records)}",
        f"  window    : {w0.isoformat()} .. {w1.isoformat()}  ({_dur(elapsed)})",
        f"  streams   : {len(selected)} (symbol, channel) pair(s); an instant counts as "
        "CAPTURED only when ALL of them are attested",
    ]
    if symbol or channel:
        lines.append(f"  filter    : symbol={symbol!r} channel={channel!r}")
    lines.append("")

    if not found:
        lines.append("GAPS: none — every instant of the window is attested.")
    else:
        lines.append(f"GAPS ({len(found)}):")
        lines.append(f"  {'#':>3}  {'start':<32} {'end':<32} {'duration':>12}  cause")
        for i, g in enumerate(found, 1):
            lines.append(
                f"  {i:>3}  {g.start.isoformat():<32} {g.end.isoformat():<32} "
                f"{_dur(g.duration_s):>12}  {g.cause}"
            )
            if g.detail:
                lines.append(f"       {g.detail}")

    pct = (captured / elapsed * 100.0) if elapsed > 0 else 0.0
    lines.append("")
    lines.append(
        f"CAPTURED   {_dur(captured)} of {_dur(elapsed)} elapsed  ({pct:.3f}%)"
    )
    lines.append(
        f"UNCAPTURED {_dur(uncaptured)} across {len(found)} gap(s)  "
        f"({100.0 - pct:.3f}%)"
    )
    return lines


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Report every interval the coverage journal does NOT attest"
    )
    ap.add_argument(
        "--out",
        default=str(DEFAULT_OUT),
        help="recorder output directory (holds the coverage journal)",
    )
    ap.add_argument(
        "--journal", default=None, help="path to the journal directly (overrides --out)"
    )
    ap.add_argument(
        "--start",
        default=None,
        help="window start, ISO8601 (default: first journal record)",
    )
    ap.add_argument(
        "--end",
        default=None,
        help="window end, ISO8601 (default: newest journal record)",
    )
    ap.add_argument("--symbol", default=None, help="restrict to one venue symbol")
    ap.add_argument("--channel", default=None, help="restrict to one channel")
    ap.add_argument(
        "--fail-on-gap",
        action="store_true",
        help="exit 1 if any gap is found (for unattended checks)",
    )
    args = ap.parse_args(argv)

    journal_path = (
        Path(args.journal) if args.journal else Path(args.out) / JOURNAL_FILENAME
    )
    records = load_records(journal_path)
    if not records:
        print(f"COVERAGE GAP REPORT: journal missing or empty: {journal_path}")
        print("No coverage is attested. Absence of a journal is UNCAPTURED, not quiet.")
        return 1

    window = None
    if args.start or args.end:
        auto = journal_window(records)
        w0 = parse_iso(args.start) if args.start else (auto[0] if auto else None)
        w1 = parse_iso(args.end) if args.end else (auto[1] if auto else None)
        window = (w0, w1)

    found, win, covered = gaps(
        records, window=window, symbol=args.symbol, channel=args.channel
    )
    for line in render(
        journal_path, records, found, win, covered, args.symbol, args.channel
    ):
        print(line)
    return 1 if (found and args.fail_on_gap) else 0


if __name__ == "__main__":
    raise SystemExit(main())
