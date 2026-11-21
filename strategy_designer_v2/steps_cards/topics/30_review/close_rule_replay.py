"""Replay a held record from its recorded forecast and sized target (core/holding_period.py and the band as coded),
with or without one rule: a trade to a target of 0 (closing the position) always passes the band. Cost per unit
measured from the record; daily returns = the sum of bar returns per UTC day, equal weight over coins."""
import sys, json, math, pathlib, numpy as np, pandas as pd
sys.path.insert(0, "/home/user/trading-bot/trading-bot")
from core.holding_period import HoldingPeriod
def run(rec, close_rule, band=0.2):
    s = json.loads((rec/"config.json").read_text())["strategies"]; N = s["min_holding_bars"]
    days = []; units = free = real = 0.0; u_rec = 0.0
    for cd in sorted(p for p in rec.iterdir() if p.is_dir()):
        parts = []
        for f in cd.glob("w*/bars.csv.gz"):
            b = pd.read_csv(f, usecols=["timestamp", "close", "forecast", "sizing_target_allocation", "postRebalance_current_allocation", "postRebalance_total_value"])
            a = b.postRebalance_current_allocation.fillna(0).to_numpy(); c = b.close.to_numpy(); v = b.postRebalance_total_value.to_numpy()
            u_rec += np.abs(np.diff(a, prepend=0)).sum(); free += (a[:-1] * (c[1:] / c[:-1] - 1)).sum(); real += (v[1:] / v[:-1] - 1).sum()
            fc = b.forecast.to_numpy(float); tg = b.sizing_target_allocation.fillna(0).to_numpy(float)
            r = np.append(c[1:] / c[:-1] - 1, 0.0)
            hp = HoldingPeriod(N, band); pos = 0.0; held = 0.0; P = np.zeros(len(c))
            for t in range(len(c)):
                nan = not math.isfinite(fc[t]); tgt = pos if nan else tg[t]
                want = hp.apply(cd.name, None if nan else fc[t], tgt, pos)
                if t == len(c) - 1: want = 0.0
                ch = want - pos; sig = 0.0 if nan else fc[t] / 10
                passes = abs(sig - held) >= band - 1e-6 or abs(ch) >= band - 1e-6 or t == len(c) - 1 or (close_rule and want == 0.0)
                if ch != 0 and not nan and passes:
                    units += abs(ch); pos = want; held = sig
                P[t] = pos
            parts.append(pd.Series(P * r, index=pd.to_datetime(b.timestamp, utc=True).dt.normalize()) - 0)
            parts[-1] = (parts[-1], np.abs(np.diff(P, prepend=0)))
        days.append((cd.name, parts))
    cost = (free - real) / u_rec
    cols = []
    for coin, parts in days:
        ser = pd.concat([s - cost * pd.Series(d, index=s.index) for s, d in parts])
        cols.append(ser.groupby(level=0).sum().rename(coin))
    x = pd.concat(cols, axis=1).mean(axis=1).sort_index().to_numpy()
    sh = x.mean() / x.std(ddof=1) * math.sqrt(365); curve = np.cumprod(1 + x); ann = curve[-1] ** (365 / len(x)) - 1
    fall = float(np.max(1 - curve / np.maximum.accumulate(curve)))
    return round(sh, 3), round(ann / fall, 3), round(units)
if __name__ == "__main__":
    for p in sys.argv[1:]:
        rec = pathlib.Path(p)
        print(rec.name.split(".")[-1][:44], "| today's band:", run(rec, False), "| close to 0 always passes:", run(rec, True), "(Sharpe, Calmar, units)")
