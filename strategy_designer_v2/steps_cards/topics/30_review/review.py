"""Topic 30's review: per idea with a verdict, its origin, verdict, profitability, and its book before and after costs."""
import json, re, sys
from pathlib import Path
import pandas as pd
ROOTS = [Path("/home/user/trading-bot/strategy_designer_v2/steps_cards"), Path(sys.argv[1]) / "strategy_designer_v2/steps_cards"]
def root_of(run):
    for r in ROOTS[::-1]:
        if (r / "orchestration/run_idea" / run / "table.json").exists(): return r
recs = []
runs = sorted({p.parent.name for r in ROOTS for p in r.glob("orchestration/run_idea/*_run/table.json")})
for run in runs:
    R = root_of(run)
    for row in json.load(open(R / "orchestration/run_idea" / run / "table.json")):
        bt = row["backtest"]
        if row.get("step3") != "plan": continue
        g = n = f = t = dur = 0.0
        for m in (R / "04_backtest" / run / "backtests" / bt).glob("*/w*/metrics.json"):
            c = json.load(open(m))["core"]
            g += c.get("gross_pnl") or 0; n += c.get("net_pnl") or 0; f += c.get("fees_paid") or 0
            tc = c.get("trade_count") or 0; t += tc; dur += (c.get("avg_trade_duration_bars") or 0) * tc
        ck = R / "06_profitability" / run / "checks" / bt / "result.json"
        sh = next((x["value"] for x in json.load(open(ck))["measures"] if x["measure"] == "sharpe_min"), None) if ck.exists() else None
        segs = row["idea"].split(".")
        recs.append({"run": run, "bt": bt, "bar": bt.rsplit("_", 1)[-1], "generation": len(segs) - 1,
                     "origin": "brief" if len(segs) == 1 else "step 7 (" + segs[-1][0] + ")",
                     "confirmed": str(row.get("step5", "")).startswith("confirmed"),
                     "profitable": str(row.get("step6", "")).startswith("profitable"),
                     "sharpe": sh, "gross": g, "fees": f, "net": n, "trades": t, "dur_bars": dur / t if t else None})
d = pd.DataFrame(recs)
d.to_csv(Path(sys.argv[1]) / "ideas.csv", index=False)
print(len(d), "planned ideas in", d.run.nunique(), "runs")
