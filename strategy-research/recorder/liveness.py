"""
Operator liveness check — one command, three independent failure modes.
=======================================================================

    python -m recorder.liveness

Exit 0 = HEALTHY. Any non-zero = the recorder is DOWN or DEGRADED; treat it as
an outage, not as a quiet market.

THE RULE THIS ENFORCES
----------------------
A 0-byte or non-growing shard is a FAILURE, never evidence that the market is
quiet. On this venue that is not a heuristic, it is a guarantee: Kraken emits a
heartbeat ~1/s whenever no other channel update is flowing, so a healthy socket
subscribed to 19 pairs cannot produce a minute of true silence. Silence means
the socket died, or the process did.

Correspondingly this check never trusts file size alone. Size can grow while
coverage is broken (one symbol dropped out of the subscription), and coverage
can be intact while size is flat for a few seconds. So all three of the
following must hold, and the journal is consulted in two of them:

  1. GROWTH   — total bytes across today's shards strictly increases between
                two readings `--window` seconds apart. Zero bytes fails here.
  2. FRESH    — the newest `recv_ts` on disk, and the newest journal record,
                are both recent. Catches a process that is alive, holding its
                files open, and receiving nothing.
  3. COVERAGE — the journal shows an OPEN coverage interval right now (no
                unmatched WS_DISCONNECT / RECORDER_STOP), the most recent
                HEARTBEAT_ROLLUP is recent, it carries a non-zero heartbeat
                count, and it saw all `--expect-symbols` symbols. 19 -> 18 is
                an alert, not a rounding error.

Because check 1 needs two readings, the command sleeps internally for
`--window`. That is the point: it is a single command an operator can run, and
it cannot be satisfied by a stale snapshot.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.journal import (  # type: ignore
        JOURNAL_FILENAME, load_records, parse_iso,
    )
    from recorder.record_kraken_ws import DEFAULT_OUT, SYMBOLS  # type: ignore
else:
    from .journal import JOURNAL_FILENAME, load_records, parse_iso
    from .record_kraken_ws import DEFAULT_OUT, SYMBOLS

_CLOSING = {"WS_DISCONNECT", "RECORDER_STOP"}


def total_bytes(out_dir: Path) -> Tuple[int, int]:
    """(bytes, file count) across today's and yesterday's shards.

    Yesterday is included so a check straddling the UTC rotation boundary does
    not read as a collapse to zero.
    """
    now = datetime.now(timezone.utc)
    days = {now.strftime("%Y-%m-%d"), (now - timedelta(days=1)).strftime("%Y-%m-%d")}
    total = 0
    count = 0
    for p in Path(out_dir).rglob("*.ndjson"):
        if p.name == JOURNAL_FILENAME or p.stem not in days:
            continue
        total += p.stat().st_size
        count += 1
    return total, count


def newest_recv_ts(out_dir: Path) -> Optional[datetime]:
    """Newest `recv_ts` on disk, read from the last line of each shard."""
    newest: Optional[datetime] = None
    for p in Path(out_dir).rglob("*.ndjson"):
        if p.name == JOURNAL_FILENAME or p.stat().st_size == 0:
            continue
        try:
            with open(p, "rb") as fh:
                fh.seek(max(0, p.stat().st_size - 8192))
                tail = fh.read().decode("utf-8", errors="replace")
            line = [ln for ln in tail.splitlines() if ln.strip()][-1]
            key = '"recv_ts":"'
            i = line.find(key)
            if i < 0:
                continue
            j = line.find('"', i + len(key))
            ts = parse_iso(line[i + len(key): j])
        except (OSError, IndexError, ValueError):
            continue
        if newest is None or ts > newest:
            newest = ts
    return newest


def check(
    out_dir: Path,
    window_s: float,
    expect_symbols: int,
    max_staleness_s: float,
) -> Tuple[bool, List[str]]:
    lines: List[str] = []
    ok = True
    journal_path = Path(out_dir) / JOURNAL_FILENAME

    def fail(msg: str) -> None:
        nonlocal ok
        ok = False
        lines.append("FAIL  " + msg)

    def good(msg: str) -> None:
        lines.append("ok    " + msg)

    # ---- 1. GROWTH ----
    b0, n0 = total_bytes(out_dir)
    t0 = datetime.now(timezone.utc)
    lines.append(f"reading 1 @ {t0.isoformat()}  bytes={b0}  shards={n0}")
    time.sleep(window_s)
    b1, n1 = total_bytes(out_dir)
    t1 = datetime.now(timezone.utc)
    lines.append(f"reading 2 @ {t1.isoformat()}  bytes={b1}  shards={n1}")

    if n1 == 0:
        fail("no shard files exist at all")
    elif b1 == 0:
        fail("shards exist but total size is 0 bytes — this is DOWN, not a quiet market")
    elif b1 <= b0:
        fail(f"shards not growing: {b0} -> {b1} over {window_s:.0f}s "
             "— heartbeat guarantees traffic, so flat means dead")
    else:
        rate = (b1 - b0) / max(1e-9, (t1 - t0).total_seconds())
        good(f"growth {b1 - b0} bytes over {(t1 - t0).total_seconds():.1f}s "
             f"({rate / 1024:.1f} KiB/s)")

    # ---- 2. FRESH ----
    newest = newest_recv_ts(out_dir)
    if newest is None:
        fail("no recv_ts found in any shard")
    else:
        age = (datetime.now(timezone.utc) - newest).total_seconds()
        (good if age <= max_staleness_s else fail)(
            f"newest recv_ts {newest.isoformat()} ({age:.1f}s old, "
            f"limit {max_staleness_s:.0f}s)"
        )

    # ---- 3. COVERAGE (journal) ----
    records = load_records(journal_path)
    if not records:
        fail(f"coverage journal missing or empty: {journal_path}")
        return ok, lines

    last = records[-1]
    jage = (datetime.now(timezone.utc) - parse_iso(last["ts"])).total_seconds()
    (good if jage <= max(max_staleness_s, 150.0) else fail)(
        f"journal last record {last['type']} @ {last['ts']} ({jage:.1f}s old)"
    )

    open_syms = set()
    for rec in records:
        if rec.get("type") == "SUBSCRIBE_ACK":
            open_syms.add(rec.get("symbol"))
        elif rec.get("type") in _CLOSING:
            open_syms.clear()
    if not open_syms:
        fail("journal shows NO open coverage interval — last event was a "
             "disconnect or stop; nothing is being captured")
    else:
        (good if len(open_syms) >= expect_symbols else fail)(
            f"open coverage intervals for {len(open_syms)} symbols "
            f"(expected {expect_symbols})"
        )

    rollups = [r for r in records if r.get("type") == "HEARTBEAT_ROLLUP"]
    if not rollups:
        fail("no HEARTBEAT_ROLLUP yet — recorder younger than one rollup "
             "interval (60s), or the rollup task is dead")
    else:
        r = rollups[-1]
        rage = (datetime.now(timezone.utc) - parse_iso(r["ts"])).total_seconds()
        if rage > 150.0:
            fail(f"newest rollup is {rage:.0f}s old (limit 150s) — rollup task dead")
        elif r.get("heartbeats", 0) == 0 and r.get("frames_total", 0) == 0:
            fail("last rollup saw 0 frames AND 0 heartbeats — socket is dead")
        elif r.get("symbols_seen", 0) < expect_symbols:
            fail(f"last rollup saw {r.get('symbols_seen')} symbols, "
                 f"expected {expect_symbols} — a pair has dropped out")
        else:
            good(f"rollup @ {r['ts']}: {r.get('frames_total')} frames, "
                 f"{r.get('heartbeats')} heartbeats, "
                 f"{r.get('symbols_seen')}/{expect_symbols} symbols")

    return ok, lines


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Kraken recorder liveness check")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--window", type=float, default=70.0,
                    help="seconds between the two size readings (default 70)")
    ap.add_argument("--expect-symbols", type=int, default=len(SYMBOLS))
    ap.add_argument("--max-staleness", type=float, default=30.0)
    args = ap.parse_args(argv)

    ok, lines = check(
        Path(args.out), args.window, args.expect_symbols, args.max_staleness
    )
    for line in lines:
        print(line)
    print("HEALTHY" if ok else "UNHEALTHY")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
