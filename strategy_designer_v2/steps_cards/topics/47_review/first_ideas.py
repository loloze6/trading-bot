"""Topic 47, 1g (the operator, 2026-11-24: "why do first ideas fail?"). Every step 5 verdict of every run (in sample;
the unseen periods' verdicts left out), with its idea's generation: 0 = written by step 2 from the brief, 1+ = written by
a step 7 line from a tested parent (the id's last segment: a not observable, b inconclusive, c rejected, d confirmed not
paying, e paying not confirmed, g patterns). Per group: the verdicts by status, the main measure's t (its sign: + is the
idea's own direction), the cases; for the follow-ups, the parent's status. Writes first_ideas.csv.
  python3 topics/47_review/first_ideas.py"""
import json, pathlib, re
import numpy as np, pandas as pd

STEPS = pathlib.Path(__file__).resolve().parents[2]
SEG = re.compile(r"\.([a-g])(\d+)(?=[._]|$)")
rows = []
for f in STEPS.glob("05_verification/*_run/verdicts/*/result.json"):
    run, rid = f.parts[-4], f.parts[-2]
    try:
        d = json.loads(f.read_text())
    except (OSError, ValueError):
        continue
    code = re.sub(r"_(1h|4h|1d)$", "", rid)
    segs = SEG.findall(code)
    mm = d.get("main_measure") or {}; st = mm.get("statistic")
    rows.append({"run": run, "id": rid, "bar": rid.rsplit("_", 1)[-1], "generation": len(segs),
                 "line": segs[-1][0] if segs else "-", "status": d.get("status"),
                 "t": st.get("value") if isinstance(st, dict) else np.nan,
                 "cases": (d.get("counts") or {}).get("cases", np.nan),
                 "parent": rid[: rid.rfind(".")] if segs else None})
v = pd.DataFrame(rows)
status_of = {}
for r in v.itertuples():
    status_of[(r.run, re.sub(r"_(1h|4h|1d)$", "", r.id))] = r.status
def parent_status(r):
    if r.parent is None: return None
    pc = r.parent.split("_", 1)[0] if False else re.sub(r"_.*$", "", r.parent.split(".")[0]) + "".join(f".{a}{b}" for a, b in SEG.findall(r.parent))
    for (run, code), s in status_of.items():
        if run == r.run and re.sub(r"_.*?(?=\.|$)", "", code, count=1) == pc:
            return s
    return "unknown"
v["kind"] = np.where(v.generation == 0, "first idea", "follow-up")
v.to_csv(pathlib.Path(__file__).with_name("first_ideas.csv"), index=False, float_format="%.4g")
pd.set_option("display.width", 200)
print(f"verdicts: {len(v)} in {v.run.nunique()} runs")
tab = pd.crosstab(v.kind, v.status, margins=True); print("\nby status:"); print(tab.to_string())
print("\nshare by status (rows sum to 1):"); print(pd.crosstab(v.kind, v.status, normalize="index").round(2).to_string())
g = v.groupby("kind")
print("\nthe main measure's t (+ = the idea's own direction):")
print(g.t.describe(percentiles=[.25, .5, .75]).round(2).to_string())
print("share with t below 0 (the effect the other way):", g.t.apply(lambda s: (s < 0).mean()).round(2).to_dict())
print("share with 0 <= t < 2 (the right way, not sure enough):", g.t.apply(lambda s: ((s >= 0) & (s < 2)).mean()).round(2).to_dict())
print("cases, median:", g.cases.median().to_dict())
print("\nby bar:"); print(pd.crosstab([v.kind, v.bar], v.status == "confirmed", normalize="index").round(2).to_string())
f = v[v.kind == "follow-up"]
print("\nfollow-ups by step 7's line (the parent's verdict that wrote them): share confirmed")
print(f.groupby("line").agg(n=("status", "size"), confirmed=("status", lambda s: (s == "confirmed").mean())).round(2).to_string())
