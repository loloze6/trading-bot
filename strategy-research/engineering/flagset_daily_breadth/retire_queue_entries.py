"""Retire held queue entries the RUNBOOK's way (RUNBOOK 'Approval mode' step 3: "To reject an entry
instead, set it `superseded` by hand (it then never runs, and its brief is no longer held)").

Text-level edit of config/campaign_queue.yaml: only the entry's `status:` line changes (comments,
notes and every other line stay). Run with NO campaign running.

Usage, from strategy-research/:
    ../venv/Scripts/python.exe engineering/flagset_daily_breadth/retire_queue_entries.py <entry_id> [<entry_id> ...]            # plan only
    ../venv/Scripts/python.exe engineering/flagset_daily_breadth/retire_queue_entries.py --write <entry_id> [<entry_id> ...]   # applies it

An entry is retired only if its status is `blocked_on_operator_approval` or starts with `paused:`;
any other status, or an unknown id, stops the script before anything is written.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

QUEUE = Path("config") / "campaign_queue.yaml"


def main() -> None:
    args = sys.argv[1:]
    write = "--write" in args
    ids = [a for a in args if a != "--write"]
    if not ids:
        raise SystemExit(__doc__)
    text = QUEUE.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    starts = [i for i, ln in enumerate(lines) if ln.startswith("- id: ")]
    plan = []
    for entry_id in ids:
        hit = [i for i in starts if lines[i] == f"- id: {entry_id}"]
        if len(hit) != 1:
            raise SystemExit(f"{QUEUE}: expected exactly one entry '{entry_id}', found {len(hit)}")
        end = next((s for s in starts if s > hit[0]), len(lines))
        sl = [k for k in range(hit[0], end) if re.fullmatch(r"  status: \S+", lines[k])]
        if len(sl) != 1:
            raise SystemExit(f"{QUEUE}: entry '{entry_id}' has {len(sl)} status lines")
        status = lines[sl[0]].split(": ", 1)[1]
        if status != "blocked_on_operator_approval" and not status.startswith("paused:"):
            raise SystemExit(f"{QUEUE}:{sl[0] + 1}: '{entry_id}' is '{status}', not held or paused "
                             "-- stopping, nothing written")
        plan.append((entry_id, sl[0], status))
    for entry_id, k, status in plan:
        print(f"{QUEUE}:{k + 1}  {entry_id}  status: {status} -> superseded")
        lines[k] = "  status: superseded"
    if not write:
        print("\n(dry: nothing written; add --write to apply)")
        return
    QUEUE.write_bytes(nl.join(lines).encode("utf-8"))
    print(f"\nwritten: {len(plan)} entries superseded")


if __name__ == "__main__":
    main()
