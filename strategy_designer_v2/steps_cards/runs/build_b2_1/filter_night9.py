"""B2.1's proof of the filter: night 9's six runs, each with its header's target box (runs/NIGHT9_RUN.md), the tested
ideas the filter would have kept and left out (common/target_box.py, in_box), and the profitable ones left out.
  python3 runs/build_b2_1/filter_night9.py"""
import json, sys
from pathlib import Path
STEPS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(STEPS / "common")); sys.path.insert(0, str(STEPS / "orchestration" / "select_next" / "helper"))
import target_box as tb, select_next
from lib import header_fields

RUNS = [("A", "night9_chopagishort_run", "choppy agitated", "short"), ("B", "night9_chopdeep_run", "choppy", "short"),
        ("C", "night9_chopmonth_run", "choppy", "both"), ("D", "night9_chopstretch_run", "choppy", "both"),
        ("E", "night9_fallcalmfade_run", "falling calm", "short"), ("F", "night9_fallcalmwide_run", "falling calm", "short")]
print("| Session | Run | Box (its header) | Tested | Kept | Left out | of which no profile named | Profitable kept | Profitable left out |")
print("|---|---|---|---|---|---|---|---|---|")
tot = [0] * 6; named_out = []
for s, run, prof, side in RUNS:
    box = {"profile": prof, "side": side}
    files = {f.stem: f for f in select_next.written_in(run)}
    rows = json.loads((STEPS / "orchestration" / "run_idea" / run / "table.json").read_text())
    tested = {r["idea"]: r for r in rows}
    kept, out, noprof, pk, po = 0, 0, 0, 0, []
    for iid, r in tested.items():
        text = files[iid].read_text()
        ok = tb.in_box(text, run, box)
        pay = str(r.get("step5", "")).startswith("confirmed") and str(r.get("step6", "")).startswith("profitable")
        p, sides = tb.idea_profile_side(text, run)
        if ok: kept += 1; pk += pay
        else:
            out += 1; noprof += p is None
            if pay: po.append(f"{iid} (profile {p or 'none'}, sides {'/'.join(sides)})")
    for i, v in enumerate((len(tested), kept, out, noprof, pk, len(po))): tot[i] += v
    print(f"| {s} | {run} | {prof}, {side} | {len(tested)} | {kept} | {out} | {noprof} | {pk} | {len(po)} |")
    named_out += [f"{s}: {x}" for x in po]
print(f"| all | | | {tot[0]} | {tot[1]} | {tot[2]} | {tot[3]} | {tot[4]} | {tot[5]} |")
print("\nProfitable (confirmed and profitable enough) left out:")
for x in named_out: print("-", x)
