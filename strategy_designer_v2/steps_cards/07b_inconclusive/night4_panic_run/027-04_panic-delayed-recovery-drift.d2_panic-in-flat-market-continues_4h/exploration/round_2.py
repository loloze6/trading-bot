import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    h = 78
    drift = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            cl = df["close"].values
            idx = np.arange(0, len(cl) - h, h)
            rs.append(cl[idx + h] / cl[idx] - 1)
        drift[c] = np.concatenate(rs).mean()
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            f = df["forecast"].values; cl = df["close"].values
            hi = df["high"].values; lo = df["low"].values
            n = len(df)
            for s in range(0, n, 78):
                e = min(s + 78, n)
                q = np.where(f[s:e] <= -10)[0]
                if len(q) == 0: continue
                t = s + q[0]
                if t + h >= n: continue
                ret = cl[t + h] / cl[t] - 1
                r = {"coin": c, "u78": -(ret - drift[c]),
                     "fall": cl[t-6]/cl[t-12]-1 if t >= 12 else np.nan,
                     "bounce1d": cl[t]/cl[t-6]-1 if t >= 6 else np.nan,
                     "p30": cl[t-12]/cl[t-192]-1 if t >= 192 else np.nan,
                     "p10": cl[t-12]/cl[t-72]-1 if t >= 72 else np.nan,
                     "u_first2d": -(cl[t+12]/cl[t]-1), "u_last11d": -(cl[t+h]/cl[t+12]-1)}
                rows.append(r)
    d = pd.DataFrame(rows)
    def agg(g, col="u78"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean()})
    out = {}
    for col in ["fall", "bounce1d", "p30", "p10"]:
        dd = d.dropna(subset=[col]).copy()
        dd["q"] = pd.qcut(dd[col], 4, duplicates="drop")
        out["by_" + col] = dd.groupby("q").apply(agg)
        out["corr_" + col] = pd.Series({"spearman": stats.spearmanr(dd[col], dd["u78"])[0], "n": len(dd)})
    out["split_time"] = pd.DataFrame({k: agg(d, k) for k in ["u_first2d", "u_last11d"]}).T
    return out
