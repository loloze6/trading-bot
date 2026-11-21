"""From the recorded bars: the position option 2 holds when an event is a rise of the sized target (today's engine)
against when it is a rise of the forecast, sized at its bar (the operator's decision, 2026-11-20). The trade band and
fills are left out on both sides (the same for both), so only the rule differs. Reports how many bars differ, the
units traded under each, and the book without costs under each (sum of position x next return)."""
import sys, json, pathlib, collections, numpy as np, pandas as pd
ST = pathlib.Path("/home/user/trading-bot/strategy_designer_v2/steps_cards")
def run(tgt, fc, N, mode):
    moves = collections.deque(maxlen=N); pt = pf = 0.0; pos = np.zeros(len(tgt)); prev = 0.0
    for t in range(len(tgt)):
        if mode == "target":
            ev = tgt[t] - pt
        else:
            s = np.sign(fc[t]); base = max(0.0, s * pf) if s else 0.0
            ev = tgt[t] * (s * fc[t] - base) / (s * fc[t]) if s and s * fc[t] > base else 0.0
        moves.append(ev); pt, pf = tgt[t], fc[t]
        want = tgt[t]
        if prev > 0 and want < prev: want = max(want, min(prev, sum(x for x in moves if x > 0)))
        elif prev < 0 and want > prev: want = min(want, max(prev, -sum(-x for x in moves if x < 0)))
        pos[t] = prev = want
    return pos
for spec in sys.argv[1:]:
    run_, pid = spec.split("|"); rec = ST/"04_backtest"/run_/"backtests"/pid
    N = json.loads((rec/"config.json").read_text())["strategies"]["min_holding_bars"]
    diff = n = 0; u = {"target": 0.0, "forecast": 0.0}; g = {"target": 0.0, "forecast": 0.0}; mx = 0.0
    for f in rec.glob("*/w*/bars.csv.gz"):
        b = pd.read_csv(f, usecols=["close", "forecast", "sizing_target_allocation"])
        tgt = b["sizing_target_allocation"].fillna(0).to_numpy(float); fc = b["forecast"].fillna(0).to_numpy(float)
        r = np.append(b["close"].to_numpy()[1:] / b["close"].to_numpy()[:-1] - 1, 0.0)
        p = {m: run(tgt, fc, N, m) for m in ("target", "forecast")}
        d = np.abs(p["target"] - p["forecast"]); diff += (d > 1e-9).sum(); n += len(d); mx = max(mx, d.max())
        for m in p: u[m] += np.abs(np.diff(p[m], prepend=0)).sum(); g[m] += (p[m] * r).sum()
    print(f"{pid.split('.')[-1][:42]:42s} N={N:3d} bars differing {diff/n*100:5.2f} % (largest {mx:.3f}) | units traded "
          f"{u['target']:8.0f} -> {u['forecast']:8.0f} | book without costs {g['target']*1000:8.0f} -> {g['forecast']*1000:8.0f}")
