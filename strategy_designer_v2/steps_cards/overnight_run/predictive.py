"""Orchestrator tool: for each idea taken through steps 3 to 5, the strongest t in the step 7 findings it rested on,
against the t (or z) step 5 measured on the same data, and on unseen coins when tested there."""
import glob, json, re
from pathlib import Path
SC = Path(__file__).resolve().parents[1]
rows = []
for lin in sorted(SC.glob("overnight_run/gen*/handoff/LINEAGE.md")):
    for nid, src in re.findall(r"- `(N\d-\d+_[^`]+)` <- `([^`]+)`", lin.read_text()):
        idea = next(iter(glob.glob(str(SC / f"07?_*/**/ideas/{src}.md"), recursive=True)), None)
        if not idea:
            continue
        res = json.loads((Path(idea).parents[1] / "result.json").read_text())
        g = next(x for i, x in enumerate(res["ideas"]) if res["idea_ids"][i] == src)
        ts = [abs(float(t)) for r in g["refs"] for t in re.findall(r"\b[tz]\s*[=≈]?\s*([−+-]?\d+\.\d+)", res["findings"][r].replace("−", "-"))]
        def stat(vdir, rid):
            f = SC / vdir / rid / "result.json"
            if not f.exists():
                return None, None
            o = json.loads(f.read_text())
            st = (o.get("main_measure") or {}).get("statistic") or {}
            return o["status"], st.get("value")
        rid = nid + "_1d"
        s5, t5 = None, None
        for vd in ("05_verification/overnight_run/verdicts_used", "05_verification/overnight_run/verdicts"):
            s5, t5 = stat(vd, rid)
            if s5:
                break
        so, to = stat("05_verification/overnight_run/verdicts_oos", rid + "_oos")
        rows.append((nid, nid[:2], max(ts) if ts else None, s5, t5, so, to))
for r in rows:
    f = lambda x: f"{x:+.2f}" if isinstance(x, (int, float)) else str(x)
    print(f"{r[0][:34]:34} step 7 strongest t {f(r[2]):>6} | step 5: {str(r[3])[:12]:12} {f(r[4]):>6} | unseen: {str(r[5])[:12]:12} {f(r[6])}")
