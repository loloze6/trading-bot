"""Whole-book replay of a one-component hourly book for any standardise window W, from a record's bars:
forecast (std_sim, exact), sized position (the record's own volatility factor: sizing target / (forecast / 10),
carried over bars where the forecast is 0), the corrected holding rule (core/holding_period.py), the trade band
(a trade passes when the signal moved >= 0.2 since the position was last set, or the sized change >= 0.2), and the
record's measured cost per unit traded. A coin's windows are chained by time: a window that starts one bar after
another's end continues its standardise history (as the engine's warm-up would read the same data). Daily returns:
the sum of the bar returns of each UTC day, equal weight over coins; Sharpe x sqrt(365)."""
import sys, json, math, pathlib, numpy as np, pandas as pd
sys.path.insert(0, "/tmp/claude-0/-home-user-trading-bot/9a8c137d-677e-59d2-8d4c-7c621473a28a/scratchpad/wt/trading-bot")
from core.holding_period import HoldingPeriod

def load(rec, comp):
    coins = {}
    for cd in sorted(p for p in rec.iterdir() if p.is_dir()):
        ws = []
        for f in cd.glob("w*/bars.csv.gz"):
            b = pd.read_csv(f, usecols=["timestamp", "close", "forecast", "sizing_target_allocation",
                                        "postRebalance_current_allocation", "postRebalance_total_value",
                                        f"debug_info.components.{comp}.last_history_value"])
            b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True); ws.append(b)
        coins[cd.name] = sorted(ws, key=lambda b: b.timestamp.iloc[0])
    return coins

def cost_per_unit(coins):
    free = real = units = 0.0
    for ws in coins.values():
        for b in ws:
            a = b.postRebalance_current_allocation.fillna(0).to_numpy(); c = b.close.to_numpy(); v = b.postRebalance_total_value.to_numpy()
            units += np.abs(np.diff(a, prepend=0)).sum(); free += (a[:-1] * (c[1:] / c[:-1] - 1)).sum(); real += (v[1:] / v[:-1] - 1).sum()
    return (free - real) / units

def run(coins, comp, W, mp, N, cost, band=0.2, cap=2.0):
    days = []; units = 0.0; gross = 0.0
    for coin, ws in coins.items():
        # chains of windows that follow each other; the forecast per chain, vectorised (rolling mean of |raw| before t)
        chains, cur, prev_end = [], [], None
        for b in ws:
            if prev_end is not None and (b.timestamp.iloc[0] - prev_end) != pd.Timedelta(hours=1):
                chains.append(cur); cur = []
            cur.append(b); prev_end = b.timestamp.iloc[-1]
        chains.append(cur)
        fcs = {}
        for ch in chains:
            raw = pd.Series(np.concatenate([x[f"debug_info.components.{comp}.last_history_value"].to_numpy(float) for x in ch]))
            m = raw.abs().shift(1).rolling(W, min_periods=mp).mean()
            f = np.where(m > 1e-10, np.clip(10 * raw / m, -20, 20), 0.0); f = np.where(np.isfinite(raw) & np.isfinite(m), f, 0.0)
            i = 0
            for x in ch: fcs[id(x)] = f[i:i + len(x)]; i += len(x)
        for b in ws:
            fc = fcs[id(b)]
            fc_rec = b.forecast.fillna(0).to_numpy(float); tg_rec = b.sizing_target_allocation.fillna(0).to_numpy(float)
            k = pd.Series(np.where(np.abs(fc_rec) > 1e-9, tg_rec / np.where(fc_rec == 0, 1, fc_rec / 10), np.nan)).ffill().bfill().fillna(1).to_numpy()
            c = b.close.to_numpy(float); r = np.append(c[1:] / c[:-1] - 1, 0.0)
            hp = HoldingPeriod(N, band); pos = 0.0; held_sig = 0.0; P = np.zeros(len(c))
            for t in range(len(c)):
                tgt = max(-cap, min(cap, fc[t] / 10 * k[t]))
                tgt = hp.apply(coin, fc[t], tgt, pos)
                ch = tgt - pos
                if t == len(c) - 1: tgt, ch = 0.0, -pos              # the window's end closes
                if ch != 0 and (abs(fc[t] / 10 - held_sig) >= band - 1e-6 or abs(ch) >= band - 1e-6 or t == len(c) - 1):
                    units += abs(ch); pos = tgt; held_sig = fc[t] / 10
                P[t] = pos
            dpos = np.abs(np.diff(P, prepend=0))
            bar = P * r - cost * dpos; gross += (P * r).sum()
            d = pd.Series(bar, index=b.timestamp.dt.normalize()).groupby(level=0).sum().rename(coin)
            days.append(d)
    df = pd.concat(days, axis=1).mean(axis=1).sort_index()
    x = df.to_numpy(); sh = x.mean() / x.std(ddof=1) * math.sqrt(365) if x.std() > 0 else 0.0
    curve = np.cumprod(1 + x); years = len(x) / 365; ann = curve[-1] ** (1 / years) - 1
    fall = float(np.max(1 - curve / np.maximum.accumulate(curve))); cal = ann / fall if fall > 0 else float("inf")
    return {"W": W, "sharpe": round(sh, 3), "calmar": round(cal, 3), "units": round(units), "gross": round(gross * 1000), "per_unit_bps": round(gross / units * 1e4, 1) if units else 0}
