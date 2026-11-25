import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    res = {}
    for h in (1, 2, 3):
        rows = []
        for coin, ws in bars.items():
            rs = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            dr = np.mean(rs)
            for w, b in ws.items():
                b = b.reset_index(drop=True)
                c = b["close"]
                r1 = c.pct_change()
                sd = r1.rolling(30, min_periods=20).std().shift(1)
                z = r1 / sd
                inprof = (b["regime"] == "unknown")
                for i in range(0, len(b) - h, h):
                    if not inprof.iloc[i] or not np.isfinite(z.iloc[i]):
                        continue
                    rows.append({"coin": coin, "w": w, "ts": str(pd.Timestamp(b["timestamp"].iloc[i]).date()),
                                 "z": z.iloc[i], "u": -(c.iloc[i + h] / c.iloc[i] - 1 - dr)})
        df = pd.DataFrame(rows)
        up = df[df.z > 0].copy()
        def clt(g):
            dev = g.u - g.u.mean()
            se = np.sqrt((dev.groupby(g.ts).sum() ** 2).sum()) / len(g)
            return g.u.mean() / se if se > 0 else np.nan
        tab = up.groupby(pd.cut(up.z, [0, 0.5, 1, 1.5, 2, 99])).apply(
            lambda g: pd.Series({"n": len(g), "days": g.ts.nunique(), "mean_u": g.u.mean(), "t_day": clt(g)}))
        out[f"h{h} up days by z bucket"] = tab
        sl = stats.linregress(up.z, up.u)
        out[f"h{h} slope u on z (up days)"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(up)})
        big = up[up.z > 1]
        out[f"h{h} z>1 overall"] = pd.Series({"n": len(big), "days": big.ts.nunique(), "mean_u": big.u.mean(), "t_day": clt(big)})
        # z-weighted mean (graded short in proportion to z)
        out[f"h{h} z-weighted mean u, up days"] = float((up.u * up.z).sum() / up.z.sum())
        out[f"h{h} all up days"] = pd.Series({"n": len(up), "mean_u": up.u.mean(), "t_day": clt(up)})
    return out
