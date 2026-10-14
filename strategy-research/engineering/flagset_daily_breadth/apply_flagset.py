"""The daily-breadth loop's flag set (D-130): ONE exact edit of campaign_config.yaml and
feature_flag_register.yaml, applied by the operator in the operator's checkout.

Usage, from the checkout's strategy-research/:
    ../venv/Scripts/python.exe engineering/flagset_daily_breadth/apply_flagset.py            # prints the plan, writes nothing
    ../venv/Scripts/python.exe engineering/flagset_daily_breadth/apply_flagset.py --write    # applies it

Every change states the value it expects to find; any other value stops the script before
anything is written. Both files are computed first and written together. Comments and every
other line stay as they are (line endings are kept).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CONFIG = Path("config") / "campaign_config.yaml"
REGISTER = Path("config") / "feature_flag_register.yaml"

# (flag key under `orchestrator:`, expected current, new) -- and why, in one line
ENABLED_CHANGES = [
    ("variant_loop", False, True),
    ("composition_runs", False, True),
    ("analyst", False, True),
    ("brief_criteria", False, True),
    ("deviation_gate", True, False),
]
REGISTER_STATE = {  # flag name -> (expected state, new state)
    "variant_loop": ("off_incomplete", '"on"'),
    "composition_runs": ("off_incomplete", '"on"'),
    "analyst": ("off_incomplete", '"on"'),
    "brief_criteria": ("off_incomplete", '"on"'),
    "deviation_gate": ('"on"', "off_incomplete"),
    # already enabled: true in the operator's campaign_config.yaml, still off_incomplete here
    # (tests/test_feature_flag_register.py fails on that drift)
    "folds": ("off_incomplete", '"on"'),
}
LANE1_PREFIX = ("lane 1 (2026-10-11): off for the daily basket run -- a multi-coin variant is "
                "refused in per-coin mode (tools/variant_coin.py). ")
BLOCKED_ON_NEW = {
    "folds": 'blocked_on: "c4/flag-set (runtime, uncommitted): switched on by the operator for the '
             'lane-1 runs and kept on for the daily breadth loop (D-123: a child run\'s fold is '
             'drawn at random among the folds its source is not on)"',
    "analyst": 'blocked_on: "c4/flag-set (runtime, uncommitted): switched on by the operator '
               '2026-10-14 as the idea source of the daily breadth loop; D-092..D-098 settings and '
               'caps unchanged (folds, specialist_readers, reader_findings on; explore_confirm off)"',
    "brief_criteria": 'blocked_on: "c4/flag-set (runtime, uncommitted): switched on by the operator '
                      '2026-10-14 for the daily breadth loop (D-121: decide-next fold children copy '
                      'their source run\'s criteria)"',
}


def _nl(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def edit_config(text: str, log: list) -> str:
    nl = _nl(text)
    lines = text.split(nl)
    for key, old, new in ENABLED_CHANGES:
        idx = [i for i, ln in enumerate(lines) if ln == f"  {key}:"]
        if len(idx) != 1:
            raise SystemExit(f"{CONFIG}: expected exactly one '  {key}:' line, found {len(idx)}")
        j = next(k for k in range(idx[0] + 1, idx[0] + 4) if lines[k].startswith("    enabled:"))
        want = f"    enabled: {str(old).lower()}"
        if lines[j] != want:
            raise SystemExit(f"{CONFIG}:{j + 1}: {key} reads {lines[j].strip()!r}, expected {want.strip()!r}"
                             " -- stopping, nothing written")
        lines[j] = f"    enabled: {str(new).lower()}"
        log.append(f"{CONFIG}:{j + 1}  orchestrator.{key}.enabled  {str(old).lower()} -> {str(new).lower()}")
    return nl.join(lines)


def edit_register(text: str, log: list) -> str:
    nl = _nl(text)
    lines = text.split(nl)
    for name, (old, new) in REGISTER_STATE.items():
        idx = [i for i, ln in enumerate(lines) if ln == f"  - name: {name}"]
        if len(idx) != 1:
            raise SystemExit(f"{REGISTER}: expected exactly one entry named {name}, found {len(idx)}")
        i0 = idx[0]
        s = next(k for k in range(i0, i0 + 10) if lines[k].startswith("    state:"))
        b = next(k for k in range(i0, i0 + 10) if lines[k].startswith("    blocked_on:"))
        if lines[s] != f"    state: {old}":
            raise SystemExit(f"{REGISTER}:{s + 1}: {name} state reads {lines[s].strip()!r}, expected "
                             f"'state: {old}' -- stopping, nothing written")
        lines[s] = f"    state: {new}"
        log.append(f"{REGISTER}:{s + 1}  {name}  state: {old} -> {new}")
        if name in BLOCKED_ON_NEW:
            lines[b] = f"    {BLOCKED_ON_NEW[name]}"
            log.append(f"{REGISTER}:{b + 1}  {name}  blocked_on rewritten")
        elif name in ("variant_loop", "composition_runs"):
            m = re.match(r'(    blocked_on: ")' + re.escape(LANE1_PREFIX) + r"(.*)$", lines[b])
            if not m:
                raise SystemExit(f"{REGISTER}:{b + 1}: {name} blocked_on lacks the lane-1 prefix "
                                 "-- stopping, nothing written")
            lines[b] = m.group(1) + m.group(2)
            log.append(f"{REGISTER}:{b + 1}  {name}  blocked_on: lane-1 prefix removed (master's text)")
    return nl.join(lines)


def main() -> None:
    write = "--write" in sys.argv[1:]
    log: list = []
    new = {}
    for path, fn in ((CONFIG, edit_config), (REGISTER, edit_register)):
        raw = path.read_bytes().decode("utf-8")
        new[path] = fn(raw, log)
    print("\n".join(log))
    if not write:
        print("\n(dry: nothing written; add --write to apply)")
        return
    for path, text in new.items():
        path.write_bytes(text.encode("utf-8"))
    print("\nwritten: both files")


if __name__ == "__main__":
    main()
