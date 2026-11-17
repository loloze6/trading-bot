import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    hs = [1, 2, 3]
    cmean = {}
    for c, wins in bars.items():
        for h in hs:
            vals = []
            for w, df in wins.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                vals += list(cl[idx + h] / cl[idx] - 1)
            cmean[(c, h)] = np.mean(vals) if vals else np.nan
    rows = []
    for c, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            cl = df["close"].values
            r1 = pd.Series(cl).pct_change()
            z = r1 / r1.rolling(20).std()
            n = len(df)
            for i in range(n):
                rec = {"coin": c, "year": ts[i].year, "wd": ts[i].weekday(), "z": z.iat[i]}
                for h in hs:
                    rec[f"x{h}"] = (cl[i + h] / cl[i] - 1 - cmean[(c, h)]) if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows).dropna(subset=["z"])
    def slope(g, x, y):
        g = g[[x, y]].dropna()
        if len(g) < 30: return (len(g), np.nan, np.nan, np.nan)
        r = stats.linregress(g[x], g[y])
        return (len(g), r.slope, r.slope / r.stderr, g[y].mean())
    out = {}
    sun = d[d.wd == 6]
    out["slope z by weekday h2"] = pd.DataFrame({k: slope(g, "z", "x2") for k, g in d.groupby("wd")}, index=["n","slope","t","mean"]).T
    out["slope z by weekday h3"] = pd.DataFrame({k: slope(g, "z", "x3") for k, g in d.groupby("wd")}, index=["n","slope","t","mean"]).T
    out["sun z by year h2"] = pd.DataFrame({k: slope(g, "z", "x2") for k, g in sun.groupby("year")}, index=["n","slope","t","mean"]).T
    cs = pd.DataFrame({k: slope(g, "z", "x2") for k, g in sun.groupby("coin")}, index=["n","slope","t","mean"]).T
    out["sun z by coin h2"] = cs
    out["share coins neg slope h2"] = float((cs.slope < 0).mean())
    q = sun.dropna(subset=["x2"]).copy()
    q["qq"] = pd.qcut(q.z, 8, labels=False)
    out["sun z octile"] = q.groupby("qq").agg(n=("x2","size"), z=("z","mean"), x1=("x1","mean"), x2=("x2","mean"), x3=("x3","mean"))
    # sunday vs other days difference in slope: interaction
    dd = d.dropna(subset=["x2"]).copy()
    dd["s"] = (dd.wd == 6).astype(float)
    X = np.column_stack([np.ones(len(dd)), dd.z, dd.s, dd.z * dd.s])
    b, *_ = np.linalg.lstsq(X, dd.x2.values, rcond=None)
    res = dd.x2.values - X @ b
    s2 = res @ res / (len(dd) - 4)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["interaction z*sun h2 (coef,t)"] = pd.Series({"coef": b[3], "t": b[3] / se[3]})
    return out
