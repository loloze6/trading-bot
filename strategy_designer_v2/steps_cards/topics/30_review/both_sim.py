"""Replay of d_line_1h_run's books (recorded positions as targets) under: today, the hold as built, the variant.
Per book: trades per day (a change of position; a window's last bar not counted, as step 6), units traded, earned per
unit at the bars' closes, net after the book's own measured cost per unit."""
import json, re
from pathlib import Path
import pandas as pd
rows = json.load(open("orchestration/run_idea/d_line_1h_run/table.json"))
def horizon(bt):
    t = Path(f"03_test_plan/d_line_1h_run/plans/{bt}.md").read_text()
    m = re.search(r"^horizon:\s*(\d+)", t, re.M | re.I) or re.search(r"Horizon:\s*(\d+)\s*bars", t)
    return int(m.group(1))
def replay(tgt, rule, N):
    pos, last, out = 0.0, None, []
    for i, x in enumerate(tgt):
        held = rule != "today" and last is not None and i - last < N
        if not held:
            if abs(x - pos) > 1e-12:
                pos = x
                last = i if (rule == "built" or (rule == "variant" and pos != 0)) else None
            elif rule == "variant" and pos != 0:
                last = i              # the forecast asks the held position again: the hold is renewed
        out.append(pos)
    return out
res = []
for r in rows:
    bt = r["backtest"]
    if not str(r.get("step6", "")): continue
    N = horizon(bt); acc = {k: [0.0, 0.0, 0] for k in ("today", "built", "variant")}; g = f = 0.0; days = 0.0
    for m in Path(f"04_backtest/d_line_1h_run/backtests/{bt}").glob("*/w*/metrics.json"):
        c = json.load(open(m))["core"]; g += c["gross_pnl"]; f += c["fees_paid"]
        b = pd.read_csv(m.with_name("bars.csv.gz"), usecols=["close", "postRebalance_current_allocation"])
        tgt = b["postRebalance_current_allocation"].fillna(0).tolist(); ret = b["close"].pct_change().shift(-1).fillna(0).values
        days += len(tgt) / 24
        for k in acc:
            p = pd.Series(replay(tgt, k, N)); d = p.diff().fillna(p)
            acc[k][0] += (p.values * ret).sum() * 1000; acc[k][1] += d.abs().sum(); acc[k][2] += int((d.abs() > 1e-12).sum())
    cu = (acc["today"][0] - g + f) / (acc["today"][1] * 1000)
    row = {"idea": bt.split(".")[-1][:28], "N": N}
    for k, (e, t, n) in acc.items():
        row[f"{k} trades/day"] = round(n / days, 3); row[f"{k} units"] = round(t); row[f"{k} bps"] = round(e / t / 1000 * 1e4, 1) if t else None
        row[f"{k} net"] = round(e - t * 1000 * cu)
    res.append(row)
d = pd.DataFrame(res)
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 30)
for k in ("today", "built", "variant"):
    print(f"\n== {k}"); print(d[["idea", "N", f"{k} trades/day", f"{k} units", f"{k} bps", f"{k} net"]].to_string(index=False))
