"""Option 3 (operator, 2026-11-20): each purchase (or short sale) is a lot locked N bars; a reduction sells only unlocked
lots, oldest first; an increase buys target minus position. The 0.2 band on each order. Against the block variant."""
import json, sys
from pathlib import Path
import pandas as pd
ns = {}; exec(open("/tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/dline/both_sim.py").read().split("res = []")[0], ns)
rows, horizon, replay = ns["rows"], ns["horizon"], ns["replay"]
def lots(tgt, N, band=0.2):
    L, pos, out = [], 0.0, []          # L: [signed quantity, bar opened]
    for i, x in enumerate(tgt):
        want = x - pos
        if abs(want) >= band or (x == 0 and pos != 0):
            if want * pos >= 0 or pos == 0:                       # growing the position (or opening): a new lot
                if abs(want) > 1e-12: L.append([want, i]); pos += want
            else:                                                  # reducing: unlocked lots first, oldest first
                need = abs(want)
                for lot in L:
                    if need <= 1e-12: break
                    if i - lot[1] >= N and abs(lot[0]) > 1e-12:
                        q = min(abs(lot[0]), need); lot[0] -= q if lot[0] > 0 else -q; need -= q
                        pos -= q if pos > 0 else -q
                L = [l for l in L if abs(l[0]) > 1e-12]
                if abs(pos) < 1e-12 and abs(x) > 1e-12 and need > 1e-12:      # all sold and the target is on the other side
                    L.append([x, i]); pos = x
        out.append(pos)
    return out
res = []
for r in rows:
    bt = r["backtest"]
    if not str(r.get("step6", "")): continue
    N = horizon(bt); acc = {k: [0.0, 0.0, 0] for k in ("block", "lots")}; g = f = e1 = t1 = 0.0; days = 0.0
    for m in Path(f"04_backtest/d_line_1h_run/backtests/{bt}").glob("*/w*/metrics.json"):
        c = json.load(open(m))["core"]; g += c["gross_pnl"]; f += c["fees_paid"]
        b = pd.read_csv(m.with_name("bars.csv.gz"), usecols=["close", "postRebalance_current_allocation"])
        tgt = b["postRebalance_current_allocation"].fillna(0).tolist(); ret = b["close"].pct_change().shift(-1).fillna(0).values
        p0 = pd.Series(tgt); e1 += (p0.values * ret).sum() * 1000; t1 += p0.diff().fillna(p0).abs().sum(); days += len(tgt) / 24
        for k, p in (("block", replay(tgt, "variant", N)), ("lots", lots(tgt, N))):
            p = pd.Series(p); d = p.diff().fillna(p)
            acc[k][0] += (p.values * ret).sum() * 1000; acc[k][1] += d.abs().sum(); acc[k][2] += int((d.abs() > 1e-12).sum())
    cu = (e1 - g + f) / (t1 * 1000)
    row = {"idea": bt.split(".")[-1][:26], "N": N}
    for k, (e, t, n) in acc.items():
        row[k] = f"{n/days:5.2f}/d {t:6.0f}u {e/t/1000*1e4 if t else 0:5.1f}bps net {e - t*1000*cu:+7.0f}"
    res.append(row)
pd.set_option("display.width", 300); pd.set_option("display.max_colwidth", 60)
print(pd.DataFrame(res).to_string(index=False))
