import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [2, 4, 6]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.append(cl[idx + h] / cl[idx] - 1)
            rs = np.concatenate(rs)
            drift[(c, h)] = (rs.mean(), rs.std())
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            r1 = cl.pct_change()
            mar = r1.abs().rolling(720, min_periods=240).mean()
            vr = df["volume"] / df["volume"].rolling(720, min_periods=240).mean()
            sc = r1 / mar
            yr = pd.to_datetime(df["timestamp"]).dt.year
            fc = df["forecast"]
            for h in H:
                idx = np.arange(0, len(df) - h, h)
                fwd = cl.values[idx + h] / cl.values[idx] - 1
                d, s = drift[(c, h)]
                rows.append(pd.DataFrame({"coin": c, "win": w, "h": h, "year": yr.values[idx],
                    "sc": sc.values[idx], "vr": vr.values[idx], "fc": fc.values[idx],
                    "un_short": -(fwd - d), "usual": s}))
    A = pd.concat(rows).dropna(subset=["sc", "vr"])
    def agg(g):
        x = g["un_short"]
        return pd.Series({"n": len(x), "mean_bp": x.mean() * 1e4,
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "strength": (x / g["usual"]).mean()})
    out = {}
    q = A[(A.vr > 0.67) & (A.vr <= 1.5) & (A.sc > 0)]
    # slope of unusual move on scaled rise, by horizon, for all rises and rises > 2
    res = []
    for h in H:
        for lo in [0, 1, 2, 3]:
            g = q[(q.h == h) & (q.sc > lo)]
            lr = stats.linregress(g.sc, g.un_short)
            res.append({"h": h, "sc_above": lo, "n": len(g), "slope_bp_per_unit": lr.slope * 1e4,
                        "t_slope": lr.slope / lr.stderr, "mean_bp": g.un_short.mean() * 1e4,
                        "t_mean": g.un_short.mean() / (g.un_short.std() / np.sqrt(len(g)))})
    out["quiet rises: slope on scaled rise"] = pd.DataFrame(res)
    big = q[q.sc > 3]
    out["quiet rises >3x by coin x h"] = big.groupby(["coin", "h"]).apply(agg)
    out["quiet rises >3x by year, h=4"] = big[big.h == 4].groupby("year").apply(agg)
    # forecast saturation
    f = A[(A.h == 2) & (A.fc < 0)]
    out["share of short cells at |fc|>=19.9"] = float((f.fc <= -19.9).mean())
    out["quiet rises: sc deciles where fc saturates"] = f.assign(sat=f.fc <= -19.9).groupby("sat").sc.describe()
    return out
