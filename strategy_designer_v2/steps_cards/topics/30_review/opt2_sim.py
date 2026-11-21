"""Option 2 (operator, 2026-11-20): each rise of the forecast is an event holding its own size for N bars. A long book
may not fall below the sum of the rises of the last N bars (capped at the position); a short book may not rise above
minus the sum of the falls. An increase buys target minus position. 0.2 band. Against the block and option 3."""
import json
from pathlib import Path
import pandas as pd
ns = {}; exec(open("/tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/dline/both_sim.py").read().split("res = []")[0], ns)
_l = open("/tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/dline/lots_sim.py").read(); exec(_l[_l.index("def lots"):_l.index("\nres = []")], ns)
rows, horizon, replay, lots = ns["rows"], ns["horizon"], ns["replay"], ns["lots"]
def opt2(tgt, N, band=0.2):
    s = pd.Series(tgt); d = s.diff().fillna(s)
    rises = d.clip(lower=0).rolling(N, min_periods=1).sum().tolist(); falls = (-d).clip(lower=0).rolling(N, min_periods=1).sum().tolist()
    pos, out = 0.0, []
    for i, x in enumerate(tgt):
        new = x
        if pos > 0 and x < pos: new = max(x, min(pos, rises[i]))
        elif pos < 0 and x > pos: new = min(x, max(pos, -falls[i]))
        if abs(new - pos) >= band or (new == 0 and pos != 0): pos = new
        out.append(pos)
    return out
res = []
for r in rows:
    bt = r["backtest"]
    if not str(r.get("step6", "")): continue
    N = horizon(bt); acc = {k: [0.0, 0.0, 0] for k in ("block", "option 3", "option 2")}; g = f = e1 = t1 = 0.0; days = 0.0
    for m in Path(f"04_backtest/d_line_1h_run/backtests/{bt}").glob("*/w*/metrics.json"):
        c = json.load(open(m))["core"]; g += c["gross_pnl"]; f += c["fees_paid"]
        b = pd.read_csv(m.with_name("bars.csv.gz"), usecols=["close", "postRebalance_current_allocation"])
        tgt = b["postRebalance_current_allocation"].fillna(0).tolist(); ret = b["close"].pct_change().shift(-1).fillna(0).values
        p0 = pd.Series(tgt); e1 += (p0.values * ret).sum() * 1000; t1 += p0.diff().fillna(p0).abs().sum(); days += len(tgt) / 24
        for k, p in (("block", replay(tgt, "variant", N)), ("option 3", lots(tgt, N)), ("option 2", opt2(tgt, N))):
            p = pd.Series(p); dd = p.diff().fillna(p)
            acc[k][0] += (p.values * ret).sum() * 1000; acc[k][1] += dd.abs().sum(); acc[k][2] += int((dd.abs() > 1e-12).sum())
    cu = (e1 - g + f) / (t1 * 1000)
    row = {"idea": bt.split(".")[-1][:26], "N": N}
    for k, (e, t, n) in acc.items():
        row[k] = f"{n/days:4.2f}/d {t:5.0f}u {e/t/1000*1e4 if t else 0:5.1f}bps {e - t*1000*cu:+7.0f}"
    res.append(row)
pd.set_option("display.width", 300); pd.set_option("display.max_colwidth", 60)
print(pd.DataFrame(res).to_string(index=False))
