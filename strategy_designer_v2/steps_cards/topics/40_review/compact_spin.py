"""Topic 40, point 8: a block of identical lines in a run's journal (the loop's spin during the account's usage limit,
night 3) becomes its first line, one line saying how many identical lines were removed and between which times, and
its last line. Lines are identical when they are equal apart from their time and running numbers. The full files stay
in git history. Proof: the loop's own readings of the run (failed, unfinished, the turns of every idea) are unchanged.

  python3 topics/40_review/compact_spin.py FILE.jsonl [...]
"""
import json, sys
from pathlib import Path

VOLATILE = {"at", "turn", "spent_before", "spent", "seconds", "log", "usd", "longest_call_seconds"}
MIN_BLOCK = 5


def key(line):
    d = json.loads(line)
    return json.dumps({k: v for k, v in d.items() if k not in VOLATILE}, sort_keys=True)


def compact(path):
    lines = Path(path).read_text().splitlines()
    out, i, removed = [], 0, 0
    while i < len(lines):
        j = i
        while j + 1 < len(lines) and key(lines[j + 1]) == key(lines[i]):
            j += 1
        n = j - i + 1
        if n >= MIN_BLOCK:
            first, last = json.loads(lines[i]), json.loads(lines[j])
            out += [lines[i], json.dumps({"at": first.get("at"), "compacted": {
                "identical_lines_removed": n - 2, "from": first.get("at"), "to": last.get("at"),
                "why": "the loop's spin during the account's usage limit (night 3; fixed in e9df36fe); the full file is in git history (topic 40)"}}),
                    lines[j]]
            removed += n - 2
        else:
            out += lines[i:j + 1]
        i = j + 1
    Path(path).write_text("\n".join(out) + "\n")
    return len(lines), len(out), removed


if __name__ == "__main__":
    for f in sys.argv[1:]:
        print(f, "lines %d -> %d (%d removed)" % compact(f))
