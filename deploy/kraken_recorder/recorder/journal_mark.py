"""
Supervisor-side journal writer.
===============================

    python -m recorder.journal_mark restart --out DIR --exit-code 1 --attempt 2 \
        --backoff 10 --reason "recorder exited non-zero"

The supervisor is PowerShell, and the coverage journal is not a log file it may
append to by hand: records carry a `jseq` that must continue across process
restarts, and every record is `fsync`-ed individually because the journal's
whole value is being durable at the instant of the event it describes. Both
properties live in `CoverageJournal`. So the supervisor shells out to this,
rather than the journal acquiring a second, weaker writer.

WHY THE SUPERVISOR WRITES ANYTHING AT ALL
-----------------------------------------
Downtime between two recorder processes would otherwise be attested by nothing.
`coverage_intervals` would still bound it correctly — the successor's
RECORDER_START closes the dead run's intervals at that run's last record — but
only once a successor actually starts. If the recorder is crash-looping, or the
supervisor gives up at its restart cap, the last thing in the journal is a dead
process's rollup and the gap has no attested cause at all.

RESTART_BOUNDARY closes that: it is written between the two processes, it
carries the dead process's exit code, and `coverage_report.py` reads it to
label the gap `restart` with that exit code rather than `unknown`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Optional

if __package__ in (None, ""):  # allow `python journal_mark.py`
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from recorder.journal import CoverageJournal  # type: ignore
    from recorder.record_kraken_ws import DEFAULT_OUT  # type: ignore
else:
    from .journal import CoverageJournal
    from .record_kraken_ws import DEFAULT_OUT


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Append a supervisor record to the coverage journal"
    )
    ap.add_argument("mode", choices=["restart"])
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument(
        "--exit-code",
        type=int,
        required=True,
        help="exit code of the recorder process that just died",
    )
    ap.add_argument(
        "--attempt",
        type=int,
        default=0,
        help="restart attempt number within the supervisor's window",
    )
    ap.add_argument(
        "--backoff",
        type=float,
        default=0.0,
        help="seconds the supervisor will wait before relaunching",
    )
    ap.add_argument("--reason", default="", help="human-readable cause")
    args = ap.parse_args(argv)

    journal = CoverageJournal(Path(args.out))
    try:
        rec = journal.write(
            "RESTART_BOUNDARY",
            exit_code=args.exit_code,
            attempt=args.attempt,
            backoff_s=args.backoff,
            reason=args.reason,
            written_by="supervisor",
        )
    finally:
        journal.close()
    print(
        f"RESTART_BOUNDARY jseq={rec['jseq']} ts={rec['ts']} exit_code={args.exit_code}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
