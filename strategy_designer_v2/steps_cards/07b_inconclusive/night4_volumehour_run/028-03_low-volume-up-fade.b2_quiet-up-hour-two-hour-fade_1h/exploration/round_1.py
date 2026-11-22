import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 2, 4, 6]
    # drift per coin per horizon, non-overlapping grid over all windows
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
    A = pd.concat(rows)
    A = A.dropna(subset=["sc", "vr"])
    def agg(g):
        x = g["un_short"]
        return pd.Series({"n": len(x), "mean_bp": x.mean() * 1e4,
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "strength": (x / g["usual"]).mean()})
    out = {}
    up = A[A.sc > 0].copy()
    up["sc_bin"] = pd.cut(up.sc, [0, 1, 2, 3, 4, 6, 100])
    up["vr_bin"] = pd.cut(up.vr, [0, 0.67, 1.5, 3, 100])
    out["up hours by size x volume, h=2"] = up[up.h == 2].groupby(["vr_bin", "sc_bin"], observed=True).apply(agg)
    big = up[up.sc > 3]
    out["big rises (>3x) by volume x horizon"] = big.groupby(["vr_bin", "h"], observed=True).apply(agg)
    dn = A[A.sc < -3].copy()
    dn["vr_bin"] = pd.cut(dn.vr, [0, 0.67, 1.5, 3, 100])
    out["big falls (<-3x) by volume x horizon (short-signed)"] = dn.groupby(["vr_bin", "h"], observed=True).apply(agg)
    q = A[(A.h == 2) & (A.fc < 0)].copy()
    q["fc_bin"] = pd.cut(-q.fc, [0, 0.5, 2, 5, 10, 21])
    out["forecast<0 cells by |fc|, h=2"] = q.groupby("fc_bin", observed=True).apply(agg)
    out["forecast<0 cells by coin x year, h=2"] = q.groupby(["coin", "year"]).apply(agg)
    return out
