"""B12's proof (runs/BUILD_B11_B12.md): on night 9's tables, the 7.d calls (the line ran on a backtest), each parent's
count of failed step 6 measures as 7.d's new entry reads it (analyse.failed_of), and what the repairs written by the calls
the new condition skips led to: their children (.dN) and every idea below them, tested in the same run.
Reads files only. Usage (from steps_cards): python3 runs/build_b11_b12/b12_count.py [--nights 9]"""
import argparse, collections, glob, json, sys, yaml
from pathlib import Path
sys.path.insert(0, "07_common/helper")
import analyse as an

a = argparse.ArgumentParser(); a.add_argument("--nights", default="9"); args = a.parse_args()
entry = yaml.safe_load(Path("07d_not_profitable/helper/line.yaml").read_text())["entry"]
ok = lambda r: str(r.get("step5", "")).startswith("confirmed") and str(r.get("step6", "")).startswith("profitable")
calls, kept, skipped = 0, collections.Counter(), collections.Counter()
lead = {"kept": [0, 0, 0, 0.0], "skipped": [0, 0, 0, 0.0]}   # repairs tested, below them tested, profitable, USD (the 7.d call and the ideas it led to)
for n in args.nights.split(","):
    for t in sorted(glob.glob(f"orchestration/run_idea/night{n}_*_run/table.json")):
        run = t.split("/")[2]; rows = [r for r in json.load(open(t)) if r.get("step5")]
        for r in rows:
            ran = "7.d" in r.get("step7", {}) and Path(f"07d_not_profitable/{run}/{r['backtest']}").is_dir()
            if not ran:
                continue
            calls += 1
            failed = an.failed_of(Path(f"06_profitability/{run}/checks"), r["backtest"])
            s5 = str(r["step5"]).split(" (")[0]; s6 = str(r["step6"]).split(" (")[0]
            go = an.entry_met(entry, s5, s6, failed)
            (kept if go else skipped)[failed] += 1
            code = lambda x: x["idea"].split("_")[0]                  # the lineage code: 061-01.b1.d2
            pre = code(r) + ".d"
            kids = [x for x in rows if code(x).startswith(pre) and code(x)[len(pre):].isdigit()]
            below = [x for x in rows if any(code(x).startswith(code(k) + ".") for k in kids)]
            L = lead["kept" if go else "skipped"]
            L[0] += len(kids); L[1] += len(below); L[2] += sum(ok(x) for x in kids + below)
            L[3] += r.get("consumption", {}).get("step7_7.d", {}).get("usd", 0) + sum(x.get("cost", 0) for x in kids + below)
print(f"nights {args.nights}: 7.d calls {calls}")
print("  kept (failed measures: calls):", dict(sorted(kept.items())), "led to [repairs tested, ideas below them tested, profitable, USD]:", lead["kept"][:3] + [round(lead["kept"][3], 1)])
print("  skipped (failed measures: calls):", dict(sorted(skipped.items())), "led to [repairs tested, ideas below them tested, profitable, USD]:", lead["skipped"][:3] + [round(lead["skipped"][3], 1)])
