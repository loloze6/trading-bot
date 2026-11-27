"""Why confirmed ideas rarely pay, per market profile (the six profiles, and the ideas naming only a trend or only an
agitation): every idea tested in nights 7 to 9 (profiles named since topic 49), read from the committed files.
Per group: tested, confirmed, profitable; for the confirmed: Sharpe, Sharpe minus holding's, Calmar, days in a position,
yearly return, the strategy's daily volatility, the mean gain per day in a position, one trade's swing over its mean
gain, the costs' share of the gross profit; the step 6 measures the confirmed but unprofitable ones fail.
Usage: python3 why_by_profile.py  (from this folder or anywhere)."""
import csv, glob, gzip, json, os, re, statistics as st, collections
from pathlib import Path

SC = Path(__file__).resolve().parents[2]
RUNS = sorted(p.name for p in (SC / "orchestration" / "run_idea").glob("night[789]_*_run") if not p.name.startswith("night7c"))


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(st.median(xs), 2) if xs else None


rows = []
for run in RUNS:
    t = SC / "orchestration" / "run_idea" / run / "table.json"
    if not t.exists():
        continue
    for r in json.loads(t.read_text()):
        if not r.get("step5"):
            continue
        b = r["backtest"]
        plan = (SC / "03_test_plan" / run / "plans" / f"{b}.md")
        plan = plan.read_text() if plan.exists() else ""
        m = re.search(r"^Profile:\s*([a-z ]+?)\s*(\(|$)", plan, re.M)
        prof = m.group(1).strip() if m else "none"
        sd = re.search(r"^Side:\s*(.+)$", plan, re.M)
        side = sd.group(1).lower() if sd else ""
        side = "short" if "short only" in side else "long" if "long only" in side else "both"
        chk_dir = SC / "06_profitability" / run / "checks" / b
        meas = {}
        if (chk_dir / "result.json").exists():
            meas = {x["measure"]: (x.get("value"), x.get("passed")) for x in json.loads((chk_dir / "result.json").read_text())["measures"]}
        chk = (chk_dir / "check.md").read_text() if (chk_dir / "check.md").exists() else ""
        num = lambda pat: (lambda m: float(m.group(1)) if m else None)(re.search(pat, chk))
        rec = SC / "04_backtest" / run / "backtests" / b
        swing = None
        tr = rec / "chart_trades.csv.gz"
        if tr.exists():
            x = [float(a["realized_return"]) for a in csv.DictReader(gzip.open(tr, "rt")) if a.get("realized_return")]
            if len(x) > 20 and st.mean(x) > 0:
                swing = st.pstdev(x) / st.mean(x)
        gross = fees = 0.0
        for f in rec.glob("*/w*/metrics.json"):
            c = json.loads(f.read_text()).get("core", {})
            gross += c.get("gross_pnl") or 0; fees += c.get("fees_paid") or 0
        rows.append(dict(run=run, id=b, profile=prof, side=side,
                         confirmed=str(r["step5"]).startswith("confirmed"),
                         profitable=str(r.get("step6", "")).startswith("profitable"), meas=meas,
                         yearly=num(r"Yearly return \| ([+-]?[0-9.]+) %"), days=num(r"Days in a position \| ([0-9.]+) %"),
                         vol=num(r"Daily standard deviation \| ([0-9.]+) %"), swing=swing,
                         cost=(fees / gross) if gross > 0 else None))

v = lambda r, k: (r["meas"].get(k) or (None,))[0]
fails = lambda r: [k for k, (val, ok) in r["meas"].items() if ok is False]
ORDER = ["rising calm", "rising agitated", "falling calm", "falling agitated", "choppy calm", "choppy agitated",
         "rising", "falling", "choppy", "calm", "agitated", "none"]
g = collections.defaultdict(list)
for r in rows:
    g[r["profile"] if r["profile"] in ORDER else "other"].append(r)
print(f"nights 7 to 9: {len(rows)} ideas tested, {sum(r['confirmed'] for r in rows)} confirmed, "
      f"{sum(r['confirmed'] and r['profitable'] for r in rows)} confirmed and profitable; runs: {len(RUNS)}\n")
print("| profile | tested | confirmed | conf. and profitable | sides of the confirmed (long/short/both) | Sharpe | Sharpe minus holding | Calmar | days in a position % | yearly % | daily volatility % | gain per day in a position % | one trade's swing / its mean gain | costs / gross profit | the unprofitable confirmed fail: Calmar / Sharpe-hold / mean-day |")
print("|" + "---|" * 15)
for k in ORDER + ["other"]:
    L = g.get(k)
    if not L:
        continue
    c = [r for r in L if r["confirmed"]]; cnp = [r for r in c if not r["profitable"]]
    sides = collections.Counter(r["side"] for r in c)
    print(f"| {k} | {len(L)} | {len(c)} | {sum(r['profitable'] for r in c)} | {sides['long']}/{sides['short']}/{sides['both']} | "
          f"{med(v(r,'sharpe_min') for r in c)} | {med(v(r,'sharpe_vs_hold_min') for r in c)} | {med(v(r,'calmar_min') for r in c)} | "
          f"{med(r['days'] for r in c)} | {med(r['yearly'] for r in c)} | {med(r['vol'] for r in c)} | "
          f"{med((v(r,'avg_daily_return_min') or 0)*100 for r in c if v(r,'avg_daily_return_min') is not None)} | "
          f"{med(r['swing'] for r in c)} | {med(r['cost'] for r in c)} | "
          f"{sum('calmar_min' in fails(r) for r in cnp)}/{sum('sharpe_vs_hold_min' in fails(r) for r in cnp)}/"
          f"{sum('avg_daily_return_min' in fails(r) for r in cnp)} of {len(cnp)} |")
