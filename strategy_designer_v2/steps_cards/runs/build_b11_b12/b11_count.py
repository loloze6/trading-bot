"""B11's proof, part 1 (runs/BUILD_B11_B12.md): step 5's new rule (make_verdict.effect_check, common/verdicts.md) applied
to each stored result of night 9's tested ideas, as make_verdict applies it after measure(bars). Reads files only; writes
nothing in the repository. Usage (from steps_cards): python3 runs/build_b11_b12/b11_count.py [--nights 7,8,9]"""
import argparse, collections, glob, json, sys
from pathlib import Path
sys.path.insert(0, "05_verification/helper"); sys.path.insert(0, "common")
import make_verdict as mv
from lib import step5_answer

a = argparse.ArgumentParser(); a.add_argument("--nights", default="9"); a.add_argument("--list", action="store_true")
args = a.parse_args()
change, rows, band = collections.Counter(), [], collections.Counter()
for n in args.nights.split(","):
    for t in sorted(glob.glob(f"orchestration/run_idea/night{n}_*_run/table.json")):
        run = t.split("/")[2]
        for r in json.load(open(t)):
            if not r.get("step5"):
                continue
            rid = r["backtest"]
            f = Path(f"05_verification/{run}/verdicts/{rid}/result.json")
            if not f.exists():
                change[("no result.json", "-")] += 1
                continue
            res = json.loads(f.read_text())
            plan = Path(f"03_test_plan/{run}/plans/{rid}.md").read_text()
            old = res["status"]
            ec = mv.effect_check(res, plan)
            new = "no effect" if ec and ec["no_effect"] else old
            change[(old, new)] += 1
            st = (res.get("main_measure") or {}).get("statistic") or {}
            raw = st.get("value")
            if old == "inconclusive" and isinstance(raw, (int, float)):
                band["raw t below 1" if raw < 1 else "raw t 1 or more"] += 1
            rows.append((run, rid, old, new, raw, mv.idea_direction(plan), ec))
print(f"nights {args.nights}: {len(rows)} tested ideas")
for (o, nw), k in sorted(change.items()):
    print(f"  {o} -> {nw}: {k}")
print("  inconclusive by the raw t (night9_review's reading):", dict(band))
d = [x for x in rows if x[5] == -1]
print(f"  plans whose confirm rule is t <= -2 (the idea's direction negative): {len(d)}; their answers:",
      dict(collections.Counter((x[2], x[3]) for x in d)))
for x in rows:
    if x[2] == "inconclusive" and x[3] == "inconclusive" and isinstance(x[4], (int, float)) and x[4] < 1:
        print("  unclear, raw t below 1, stays unclear:", x[1], f"raw t {x[4]:+.2f}", x[6]["why"])
if args.list:
    for x in rows:
        if x[2] != x[3]:
            print("  changed:", x[0], x[1], x[2], "->", x[3], x[6]["why"])
