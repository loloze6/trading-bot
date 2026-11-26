"""Night 7, the comparison by the rule fixed before the runs (runs/NIGHT7_RUN.md, the control arm): one row per idea
tested within the equal-spend cut (a new-code run counts the ideas whose turn began before 25 USD), both arms, read from
each run's branch: its brief, profile line, steps 5 and 6, cost, and the share its nearest held book explains (the
register's comparison; 0.5 or more = re-finds a portfolio effect). Then the totals by arm.
  python3 topics/44_review/night7_criteria.py"""
import json, re, subprocess, sys
import pandas as pd
import pathlib
HERE=pathlib.Path(__file__).resolve().parent; REPO=str(HERE.parents[3]); SC="strategy_designer_v2/steps_cards"
NAMES=("rangefail","chopreversal","steadydecline","panic"); CUT=25.0
def git(*a): return subprocess.run(["git",*a],cwd=REPO,capture_output=True,text=True).stdout
def show(ref,p): return git("show",f"{ref}:{p}")
def header(t):
    m=re.match(r"\s*---\n(.*?)---\n",t,re.S)
    return {k.strip():v.strip() for k,v in (l.split(":",1) for l in m.group(1).splitlines() if ":" in l)} if m else {}
rows=[]
for control in (False,True):
  for n in NAMES:
    run=f"night7{'c' if control else ''}_{n}_run"; ref=f"origin/night7{'c' if control else ''}-{n}"
    files=git("ls-tree","-r","--name-only",ref,"--",SC).splitlines()
    ideafiles={f.rsplit("/",1)[1][:-3]:f for f in files if f"/{run}/" in f and "/ideas/" in f and f.endswith(".md") and not f.endswith("INDEX.md")}
    loop=[json.loads(l) for l in show(ref,f"{SC}/orchestration/loop/{run}/loop.jsonl").splitlines() if l.strip()]
    turns={t["idea"]:t for t in loop if "turn" in t}
    table={r["idea"]:r for r in json.loads(show(ref,f"{SC}/orchestration/run_idea/{run}/table.json") or "[]")}
    held=set(json.loads(show(ref,f"{SC}/orchestration/ideas_similarities_check/register/held.json"))["keys"])
    for i,t in turns.items():
        if not control and t.get("spent_before",0)>=CUT: continue
        r=table.get(i,{}); bt=r.get("backtest") or ""
        h=header(show(ref,ideafiles[i])) if i in ideafiles else {}
        comp=show(ref,f"{SC}/orchestration/ideas_similarities_check/register/comparisons/{run}__{bt}.json")
        nh=None
        if comp.strip():
            c=json.loads(comp); nh=c.get("nearest_held") or {}
            nh=nh.get("share_explained") if isinstance(nh,dict) else None
        rows.append(dict(arm="control" if control else "new",theme=n,idea=i,brief=i[:3],gen=i.split("_")[0].count("."),
            lines="".join(re.findall(r"\.([a-g])\d",i.split("_")[0])),profile=h.get("profile",""),
            step5=str(r.get("step5",""))[:22],step6=str(r.get("step6",""))[:16],cost=r.get("cost",0.0),nearest_held=nh,
            b=str(r.get("step7",{}).get("7.b",""))[:12], c=str(r.get("step7",{}).get("7.c",""))[:12]))
df=pd.DataFrame(rows); df.to_csv(HERE/"night7_criteria.csv",index=False)
df["confirmed"]=df.step5.fillna("").str.startswith("confirmed"); df["portfolio_effect"]=df.nearest_held>=0.5
print(df.groupby("arm").apply(lambda x: pd.Series({"tested": len(x), "from the theme brief (032)": (x.brief=="032").sum(), "confirmed": x.confirmed.sum(),
    "confirmed, portfolio effect": (x.confirmed&x.portfolio_effect).sum(), "spend": round(x.cost.sum(),1),
    "spend on portfolio effects": round(x.cost[x.portfolio_effect].sum(),1)}), include_groups=False).T.to_string())
