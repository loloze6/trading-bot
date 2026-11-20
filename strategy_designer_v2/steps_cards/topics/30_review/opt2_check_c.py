"""Check C on held records. (1) Positions on the other side of the forecast with no bet of the position's side within
its last N bars (a hold past its bets: a defect; within its bets it is the definition). (2) The engine's position
against core/holding_period.py replayed from the recorded forecast and target, the trade decided by the engine's own
recorded approval (approved_rebalance), the window's last bar left out."""
import sys, json, pathlib, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/trading-bot/trading-bot")
from core.holding_period import HoldingPeriod
ST = pathlib.Path("/home/user/trading-bot/strategy_designer_v2/steps_cards")
for run in sys.argv[1:]:
    for rec in sorted((ST/"04_backtest"/run/"backtests").iterdir()):
        if not (rec/"config.json").exists(): continue
        s = json.loads((rec/"config.json").read_text())["strategies"]; N = s["min_holding_bars"]; band = s.get("min_allocation_change") or 0.2
        n = against = past = bad = 0; worst = 0.0; ex = None
        for f in rec.glob("*/w*/bars.csv.gz"):
            b = pd.read_csv(f, usecols=["forecast", "sizing_target_allocation", "previous_allocation", "postRebalance_current_allocation", "approved_rebalance"])
            fc = b.forecast.to_numpy(float); tg = b.sizing_target_allocation.fillna(0).to_numpy(float)
            prev = b.previous_allocation.fillna(0).to_numpy(float); post = b.postRebalance_current_allocation.fillna(0).to_numpy(float)
            ok = b.approved_rebalance.astype(str).str.lower().isin(["true", "1", "1.0"]).to_numpy()
            hp = HoldingPeriod(N, band); last_bet = {1: -10**9, -1: -10**9}
            for t in range(len(b) - 1):
                nan = not np.isfinite(fc[t]); tgt = prev[t] if nan else tg[t]
                bet = hp._bets.get("X")
                want = hp.apply("X", None if nan else fc[t], tgt, prev[t])
                b_now = hp._bets["X"][-1]
                if b_now > 0: last_bet[1] = t
                if b_now < 0: last_bet[-1] = t
                side = int(np.sign(post[t]))
                if side and np.sign(tg[t]) == -side and abs(tg[t]) > 1e-9:
                    against += 1
                    if t - last_bet[side] >= N: past += 1
                exp = want if ok[t] else prev[t]
                d = abs(exp - post[t]); n += 1
                if d > 0.01:
                    bad += 1
                    if d > worst: worst = d; ex = (f.parent.parent.name, f.parent.name, t, round(prev[t], 3), round(tg[t], 3), round(want, 3), bool(ok[t]), round(post[t], 3))
        if n:
            print(f"{run[:18]:18s} {rec.name.split('.')[-1][:40]:40s} against {against:6d}, of which past its bets {past:4d} | engine vs module: {bad} bars differ >0.01 ({bad/n*100:.3f} %)" + (f" e.g. {ex}" if ex else ""))
