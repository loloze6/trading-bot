"""Quick replay, no backtest: each finished d_line_1h_run book replayed from its recorded bars (close, position) under
(a) today, (b) a holding rule: after a trade, no trade for N bars (N = the plan's horizon), (c) a wider band
(min_allocation_change 0.5). Edge at the bars' closes; cost = units traded x the book's own measured cost per unit.
Approximate: the replay keeps the engine's recorded positions as targets (its sizing and its 0.2 band already in them)."""
import json, re
from pathlib import Path
import pandas as pd
rows = json.load(open("orchestration/run_idea/d_line_1h_run/table.json"))
def horizon(bt):
    t = Path(f"03_test_plan/d_line_1h_run/plans/{bt}.md").read_text()
    m = re.search(r"^horizon:\s*(\d+)", t, re.M | re.I) or re.search(r"Horizon:\s*(\d+)\s*bars", t)
    return int(m.group(1))
def replay(target, rule, N):
    pos, last, out = 0.0, -10**9, []
    for i, x in enumerate(target):
        if rule == "hold":
            if i - last >= N and abs(x - pos) > 1e-12: pos, last = x, i
        elif rule == "band":
            if abs(x - pos) >= 0.5 or (x == 0 and pos != 0 and abs(pos) < 0.5): pos = x
        else: pos = x
        out.append(pos)
    return pd.Series(out)
res = []
for r in rows:
    bt = r["backtest"]
    if not str(r.get("step6", "")): continue
    N = horizon(bt); tot = {k: [0.0, 0.0] for k in ("today", "hold", "band")}; g = f = e0 = 0.0
    for m in Path(f"04_backtest/d_line_1h_run/backtests/{bt}").glob("*/w*/metrics.json"):
        c = json.load(open(m))["core"]; g += c["gross_pnl"]; f += c["fees_paid"]
        b = pd.read_csv(m.with_name("bars.csv.gz"), usecols=["close", "postRebalance_current_allocation"])
        tgt = b["postRebalance_current_allocation"].fillna(0).tolist(); ret = b["close"].pct_change().shift(-1).fillna(0)
        for k in tot:
            p = replay(tgt, k, N); tot[k][0] += (p * ret.values).sum() * 1000; tot[k][1] += p.diff().abs().fillna(p.abs()).sum()
    cost_unit = (tot["today"][0] - g + f) / (tot["today"][1] * 1000)      # the book's own cost per unit traded
    row = {"idea": bt.split(".")[-1][:30], "N": N}
    for k, (edge, turn) in tot.items():
        row[f"{k}: traded"] = round(turn); row[f"{k}: earned bps"] = round(edge / turn / 1000 * 1e4, 1) if turn else None
        row[f"{k}: net"] = round(edge - turn * 1000 * cost_unit)
    res.append(row)
pd.set_option("display.width", 260); pd.set_option("display.max_columns", 20)
print(pd.DataFrame(res).to_string(index=False))
