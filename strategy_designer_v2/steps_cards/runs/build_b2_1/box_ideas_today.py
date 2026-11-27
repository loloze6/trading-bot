"""B13's proof on today's files: for a few boxes, the untested ideas a new boxed run would take (common/target_box.md),
by run. Reads only.  python3 runs/build_b2_1/box_ideas_today.py"""
import collections, sys
from pathlib import Path
STEPS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(STEPS / "common"))
import target_box as tb
print(f"Ideas with a step 5 answer in some run: {len(tb.answered())}\n")
print("| Box | Ideas taken | From (run: ideas) |\n|---|---|---|")
for p, s in (("falling calm", "long"), ("falling calm", "short"), ("rising agitated", "long"), ("rising agitated", "short")):
    x = tb.box_ideas("a_new_boxed_run", {"profile": p, "side": s})
    c = collections.Counter(r for r, _ in x)
    print(f"| {p}, {s} | {len(x)} | {'; '.join(f'{r}: {n}' for r, n in sorted(c.items()))} |")
