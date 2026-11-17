import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    hs = [1, 2, 3, 5]
    # coin mean non-overlapping returns per h
    cmean = {}
    for c, wins in bars.items():
        for h in hs:
            vals = []
            for w, df in wins.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                vals += list(cl[idx + h] / cl[idx] - 1)
            cmean[(c, h)] = np.mean(vals) if vals else np.nan
    for c, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            cl = df["close"].values
            r1 = pd.Series(cl).pct_change()
            vol = r1.rolling(20).std()
            z = r1 / vol
            vlr = df["volume"] / df["volume"].rolling(20).mean()
            n = len(df)
            for i in range(n):
                rec = {"coin": c, "win": int(w[1:]), "year": ts[i].year, "wd": ts[i].weekday(),
                       "reg": df["regime"].iat[i], "z": z.iat[i], "fc": df["forecast"].iat[i],
                       "vlr": vlr.iat[i]}
                for h in hs:
                    rec[f"x{h}"] = (cl[i + h] / cl[i] - 1 - cmean[(c, h)]) if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    def slope(g, xcol, ycol):
        g = g[[xcol, ycol]].dropna()
        if len(g) < 30: return (len(g), np.nan, np.nan, np.nan)
        r = stats.linregress(g[xcol], g[ycol])
        return (len(g), r.slope, r.slope / r.stderr, g[ycol].mean())
    act = d[(d.reg == "mean_reversion")]
    out["regime weekday"] = act.wd.value_counts()
    cases = act[act.fc > 0]
    # by horizon, slope of excess on -z (fall size), sunday falls
    res = {}
    for h in hs:
        res[f"fall fc h{h}"] = slope(cases, "fc", f"x{h}")
        g = act[act.z < 0].assign(f=-act.z)
        res[f"fall -z h{h}"] = slope(g, "f", f"x{h}")
        g2 = act[act.z > 0]
        res[f"rise z h{h}"] = slope(g2, "z", f"x{h}")
        g3 = act.dropna(subset=["z"])
        res[f"all sun z h{h}"] = slope(g3, "z", f"x{h}")
        g4 = d[(d.reg != "mean_reversion")].dropna(subset=["z"])
        res[f"all other days z h{h}"] = slope(g4, "z", f"x{h}")
    out["slopes (n,slope,t,mean)"] = pd.DataFrame(res, index=["n", "slope", "t", "mean"]).T
    # by year, sunday falls, h2
    out["by year fall h2"] = pd.DataFrame({y: slope(g, "fc", "x2") for y, g in cases.groupby("year")}, index=["n","slope","t","mean"]).T
    out["by coin fall h2"] = pd.DataFrame({y: slope(g, "fc", "x2") for y, g in cases.groupby("coin")}, index=["n","slope","t","mean"]).T
    # quintiles of fc
    q = cases.dropna(subset=["x2"]).copy()
    q["qq"] = pd.qcut(q.fc, 5, labels=False)
    out["fc quintile h2"] = q.groupby("qq").agg(n=("x2","size"), fc=("fc","mean"), mean=("x2","mean"), x1=("x1","mean"), x5=("x5","mean"))
    # volume interaction
    v = cases.dropna(subset=["x2","vlr"]).copy()
    v["vq"] = pd.qcut(v.vlr, 3, labels=False)
    out["by vol tercile h2"] = pd.DataFrame({k: slope(g, "fc", "x2") for k, g in v.groupby("vq")}, index=["n","slope","t","mean"]).T
    return out
