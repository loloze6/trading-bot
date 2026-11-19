"""Change 1's proof: line records and rankings under today's success rule (confirmed or profitable) and the new one
(profitable only), every run (the local tree, plus intraday_1h_run from the run session's branch)."""
import json, sys, collections
from pathlib import Path
sys.path.insert(0, "/home/user/trading-bot/strategy_designer_v2/steps_cards/orchestration/select_next/helper")
import select_next as SN
from lib import header_fields
LOCAL = SN.STEPS
ARCH = Path("/tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/r30/strategy_designer_v2/steps_cards")

def analyses(root, rule, runs=None):
    out = {}
    for plan in sorted(root.glob("03_test_plan/*_run/plans/*.md")):
        if plan.name in ("INDEX.md", "COMPONENT_WISHLIST.md"): continue
        run, rid = plan.parents[1].name, plan.stem
        if runs and run not in runs: continue
        idea = header_fields(plan.read_text()).get("idea") or SN.BAR.sub("", rid)
        line, cf, _, _ = SN.id_parts(idea)
        if line is None: continue
        v = root / "05_verification" / run / "verdicts" / rid / "result.json"
        c = root / "06_profitability" / run / "checks" / rid / "result.json"
        if not v.exists(): continue
        conf = json.loads(v.read_text()).get("status") == "confirmed"
        prof = c.exists() and json.loads(c.read_text()).get("status") == "profitable enough"
        ok = (conf or prof) if rule == "old" else prof
        k = (run, line, cf); out[k] = out.get(k, False) or ok
    return out

def recs(rule):
    a = analyses(LOCAL, rule); a.update(analyses(ARCH, rule, {"intraday_1h_run"}))
    o = {}
    for (_, line, _), ok in a.items():
        s, n = o.get(line, (0, 0)); o[line] = (s + ok, n + 1)
    return {l: (s, n, (s + 1) / (n + 2)) for l, (s, n) in o.items()}

R = {r: recs(r) for r in ("old", "new")}
print("| Line | Analyses | Successes today | Record today | Successes new | Record new |")
print("|---|---|---|---|---|---|")
for l in sorted(set(R["old"]) | set(R["new"])):
    so, n, ro = R["old"][l]; sn, _, rn = R["new"][l]
    print(f"| {l} | {n} | {so} | {ro:.3f} | {sn} | {rn:.3f} |")

for run, root in (("slow_1h_run", LOCAL), ("intraday_1h_run", ARCH)):
    for rule in ("old", "new"):
        SN.records = lambda root=None, _r=R[rule]: _r
        rows = [r for r in SN.rank(run, root) if r["status"] == "candidate"]
        top = collections.Counter(r["line"] for r in rows[:20])
        print(f"\n{run}, rule {rule}: {len(rows)} candidates; the next 20 by line: {dict(top)}")
        for r in rows[:3]: print(f"   {r['line']} score {r['score']} gen {r['generation']} {r['idea'][-55:]}")

print("\nEvery local run: candidates, the first candidate under each rule, and the next 10's lines")
for run in sorted(p.name for p in LOCAL.glob("02_ideation/*_run")):
    res = {}
    for rule in ("old", "new"):
        SN.records = lambda root=None, _r=R[rule]: _r
        rows = [r for r in SN.rank(run, LOCAL) if r["status"] == "candidate"]
        res[rule] = rows
    if not res["old"]: continue
    same = res["old"][0]["idea"] == res["new"][0]["idea"]
    lo = dict(collections.Counter(r["line"] for r in res["old"][:10])); ln = dict(collections.Counter(r["line"] for r in res["new"][:10]))
    print(f"{run:18s} {len(res['old']):3d} candidates | first {'same' if same else 'changes'} | next 10 today {lo} | new {ln}")
