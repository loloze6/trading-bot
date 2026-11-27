"""Night 9's review (2026-11-27, next steps B10, B11, B12, B2): counts read from the committed run files, nights 7 to 9.
  1. each step 7 line's yield (night 8, night 9) and where the money goes;
  2. discoveries: the status of the test they were found after, and what their briefs gave;
  3. step 5's unclear results by t, and what their follow-ups gave;
  4. repairs (7.d): how far the parent was from step 6's bar, and what the repair gave.
Usage: python3 topics/47_review/night9_review.py (from steps_cards). Reads files only."""
import json, glob, re, collections
from pathlib import Path

def table(run):
    return json.load(open(f"orchestration/run_idea/{run}/table.json"))

def measures(run, backtest):
    p = Path("06_profitability") / run / "checks" / backtest / "result.json"
    return {x["measure"]: (x.get("value"), x.get("passed")) for x in json.loads(p.read_text())["measures"]} if p.exists() else {}

print("1. Lines")
for night in ("night8", "night9"):
    c = collections.defaultdict(lambda: [0, 0, 0, 0.0]); cost = collections.Counter()
    for t in glob.glob(f"orchestration/run_idea/{night}_*_run/table.json"):
        for r in json.load(open(t)):
            if not r.get("step5"): continue
            seg = r["idea"].split("_")[0].split("."); line = "brief" if len(seg) == 1 else seg[-1][0]
            ok5 = str(r["step5"]).startswith("confirmed"); ok6 = str(r.get("step6", "")).startswith("profitable")
            usd = sum(v.get("usd", 0) for v in r.get("consumption", {}).values())
            a = c[line]; a[0] += 1; a[1] += ok5; a[2] += ok5 and ok6; a[3] += usd
            for k, v in r.get("consumption", {}).items(): cost[k] += v.get("usd", 0)
    print(night, {k: f"tested {v[0]}, confirmed {v[1]}, both {v[2]}, {v[3]:.1f} USD" for k, v in c.items()})
    print("  cost by step:", {k: round(v, 1) for k, v in cost.most_common(6)})

print("2. Discoveries: [found, briefs, ideas tested, confirmed, both]")
for night in ("night8", "night9"):
    agg = collections.defaultdict(lambda: [0, 0, 0, 0, 0])
    for f in glob.glob(f"orchestration/loop/{night}_*_run/loop.jsonl"):
        tab = table(f.split("/")[2]); by = {r["backtest"]: r for r in tab}
        for x in (json.loads(l) for l in open(f) if l.strip()):
            if "discovery" not in x: continue
            p = by.get(x["discovery"].split("/")[2], {}); s = str(p.get("step5", "?")).split(" (")[0]
            if s == "confirmed" and str(p.get("step6", "")).startswith("profitable"): s = "confirmed and profitable"
            a = agg[s]; a[0] += 1
            if x.get("brief"):
                n = x["brief"].split("_")[0]; T = [r for r in tab if r.get("step5") and r["idea"].startswith(n + "-")]
                a[1] += 1; a[2] += len(T); a[3] += sum(str(r["step5"]).startswith("confirmed") for r in T)
                a[4] += sum(str(r["step5"]).startswith("confirmed") and str(r.get("step6", "")).startswith("profitable") for r in T)
    print(night, dict(agg))

rows = {}
for t in glob.glob("orchestration/run_idea/night[789]_*_run/table.json"):
    run = t.split("/")[2]
    for r in json.load(open(t)):
        if not r.get("step5"): continue
        m = re.search(r"\(([+-][0-9.]+)\)", str(r["step5"]))
        rows[(run, r["idea"].split("_")[0])] = dict(s=str(r["step5"]).split(" (")[0], t=float(m.group(1)) if m else None,
            p=str(r.get("step6", "")).startswith("profitable"), me=measures(run, r["backtest"]))
print("3. Unclear results by t; their follow-ups [tested, confirmed, both]")
band = lambda t: "below 0" if t < 0 else "0-1" if t < 1 else "1-2" if t < 2 else "2+"
print("  unclear:", collections.Counter(band(v["t"]) for v in rows.values() if v["s"] == "inconclusive" and v["t"] is not None),
      "rejected:", sum(v["s"] == "rejected" for v in rows.values()), "of", len(rows))
ch = collections.defaultdict(lambda: [0, 0, 0])
for (run, i), v in rows.items():
    par = rows.get((run, ".".join(i.split(".")[:-1]))) if "." in i else None
    if par and par["s"] == "inconclusive" and par["t"] is not None:
        a = ch[band(par["t"])]; a[0] += 1; a[1] += v["s"] == "confirmed"; a[2] += v["s"] == "confirmed" and v["p"]
print("  follow-ups by the parent's t:", dict(ch))
print("4. Repairs [repairs, became confirmed and profitable]")
D = []
for (run, i), v in rows.items():
    seg = i.split(".")
    if len(seg) < 2 or seg[-1][0] != "d": continue
    par = rows.get((run, ".".join(seg[:-1])))
    if par and "calmar_min" in par["me"] and "calmar_min" in v["me"]:
        D.append((par["me"]["calmar_min"][0], v["me"]["calmar_min"][0], v["s"] == "confirmed" and v["p"],
                  sum(ok is False for _, ok in par["me"].values())))
d = sorted(c - p for p, c, _, _ in D)
print("  ", len(D), "repairs; Calmar change p25/p50/p75/p90:", [round(d[int(f * (len(d) - 1))], 2) for f in (.25, .5, .75, .9)])
print("  by measures the parent fails:", {n: [sum(x[3] == n for x in D), sum(x[3] == n and x[2] for x in D)] for n in range(1, 6)})
