"""Replays option 2 from each bar's recorded target (sizing_target_allocation, written before the hold) and compares
with the position the engine held (postRebalance_current_allocation). A bar where the engine skipped a small trade
(the min_allocation_change band: approved_rebalance false) keeps the previous position. Also counts the target's rises
that come without a rise of the forecast (the sizing alone)."""
import sys, json, pathlib, collections, numpy as np, pandas as pd
ST = pathlib.Path("/home/user/trading-bot/strategy_designer_v2/steps_cards")
for spec in sys.argv[1:]:
    run, pid = spec.split("|")
    rec = ST/"04_backtest"/run/"backtests"/pid
    N = json.loads((rec/"config.json").read_text())["strategies"]["min_holding_bars"]
    bars = held_bars = mism = 0; worst = 0.0; rises = rise_no_fc = 0; ex = None; exs = []
    for f in rec.glob("*/w*/bars.csv.gz"):
        b = pd.read_csv(f, usecols=["forecast", "sizing_target_allocation", "previous_allocation",
                                    "postRebalance_current_allocation", "approved_rebalance"])
        tgt = b["sizing_target_allocation"].fillna(0).to_numpy(float); fc = b["forecast"].fillna(0).to_numpy(float)
        prev = b["previous_allocation"].fillna(0).to_numpy(float); post = b["postRebalance_current_allocation"].fillna(0).to_numpy(float)
        ok = b["approved_rebalance"].astype(str).str.lower().isin(["true", "1", "1.0"]).to_numpy()
        moves = collections.deque(maxlen=N); pt = 0.0
        for t in range(len(b) - 1):          # the last bar: the window's forced close
            m = tgt[t] - pt; moves.append(m); pt = tgt[t]
            if m > 1e-12:
                rises += 1
                if not (abs(fc[t]) > abs(fc[t-1] if t else 0) and np.sign(fc[t]) == np.sign(tgt[t])): rise_no_fc += 1
            want = tgt[t]
            if prev[t] > 0 and want < prev[t]:
                want = max(want, min(prev[t], sum(x for x in moves if x > 0)))
            elif prev[t] < 0 and want > prev[t]:
                want = min(want, max(prev[t], -sum(-x for x in moves if x < 0)))
            if want != tgt[t]: held_bars += 1
            exp = want if ok[t] else prev[t]
            bars += 1; d = abs(exp - post[t])
            if d > 1e-9:
                mism += 1
                exs.append((round(d,4), f.parent.parent.name, f.parent.name, t, round(prev[t],4), round(tgt[t],4), round(want,4), bool(ok[t]), round(post[t],4)))
                if d > worst: worst = d; ex = (f.parent.parent.name, f.parent.name, t, prev[t], tgt[t], want, ok[t], post[t])
    print(f"{pid.split('.')[-1][:42]:42s} N={N:3d} bars={bars} held_by_rule={held_bars} mismatches={mism} worst={worst:.2e} "
          f"target_rises={rises} without_forecast_rise={rise_no_fc}" + (f" e.g. {ex}" if ex else ""))
    exs.sort(reverse=True); print("   largest:", exs[:3]); print("   share >0.01:", sum(e[0]>0.01 for e in exs), "of", len(exs))
