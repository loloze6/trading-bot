"""Replay of d_line_1h_run's 7 books: the block variant against tranches (each bar's target held N bars, 1/N each:
the position is the mean of the last N targets), with and without the 0.2 band. Same cost per unit as each book's own."""
import json, re, sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/dline")
ns = {}; exec(open("/tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/dline/both_sim.py").read().split("res = []")[0], ns)
rows, horizon, replay = ns["rows"], ns["horizon"], ns["replay"]
def tranches(tgt, N, band):
    s = pd.Series(tgt).rolling(N, min_periods=1).sum() / N
    if not band: return s.tolist()
    pos, out = 0.0, []
    for x in s:
        if abs(x - pos) >= 0.2 or (x == 0 and pos != 0): pos = x
        out.append(pos)
    return out
res = []
for r in rows:
    bt = r["backtest"]
    if not str(r.get("step6", "")): continue
    N = horizon(bt); acc = {k: [0.0, 0.0, 0, 0.0] for k in ("block variant", "tranches", "tranches + band")}; g = f = 0.0; e1 = t1 = 0.0; days = 0
    for m in Path(f"04_backtest/d_line_1h_run/backtests/{bt}").glob("*/w*/metrics.json"):
        c = json.load(open(m))["core"]; g += c["gross_pnl"]; f += c["fees_paid"]
        b = pd.read_csv(m.with_name("bars.csv.gz"), usecols=["close", "postRebalance_current_allocation"])
        tgt = b["postRebalance_current_allocation"].fillna(0).tolist(); ret = b["close"].pct_change().shift(-1).fillna(0).values
        p0 = pd.Series(tgt); e1 += (p0.values * ret).sum() * 1000; t1 += p0.diff().fillna(p0).abs().sum(); days += len(tgt) / 24
        for k, p in (("block variant", replay(tgt, "variant", N)), ("tranches", tranches(tgt, N, False)), ("tranches + band", tranches(tgt, N, True))):
            p = pd.Series(p); d = p.diff().fillna(p)
            acc[k][0] += (p.values * ret).sum() * 1000; acc[k][1] += d.abs().sum(); acc[k][2] += int((d.abs() > 1e-12).sum()); acc[k][3] += p.abs().sum()
    cu = (e1 - g + f) / (t1 * 1000)
    row = {"idea": bt.split(".")[-1][:26], "N": N}
    for k, (e, t, n, expo) in acc.items():
        row[k] = f"{n/days:5.2f}/d {t:6.0f}u {e/t/1000*1e4 if t else 0:5.1f}bps net {e - t*1000*cu:+7.0f}"
    res.append(row)
pd.set_option("display.width", 320); pd.set_option("display.max_colwidth", 60)
print("per book: trades per day / units traded / earned per unit / net after costs")
print(pd.DataFrame(res).to_string(index=False))
