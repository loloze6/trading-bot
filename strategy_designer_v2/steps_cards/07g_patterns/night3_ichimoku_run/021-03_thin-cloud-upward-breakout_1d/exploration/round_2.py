import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values.astype(float); n = len(cl)
            ret1 = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            ts = pd.to_datetime(df["timestamp"])
            for i in range(20, n - 1):
                v = np.nanstd(ret1[i - 19:i + 1])
                r3 = cl[i + 3] / cl[i] - 1 if i + 3 < n else np.nan
                r3s = 1 if (i % 3 == 0) else 0
                rows.append(dict(coin=c, win=w, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                 wd=ts.iloc[i + 1].weekday(), r0=ret1[i], z0=ret1[i] / v,
                                 r1=ret1[i + 1], r3=r3, grid3=r3s, vol=v,
                                 hour=ts.iloc[i].hour))
    d = pd.DataFrame(rows)
    mu = d.groupby("coin")["r1"].transform("mean")
    d["u1"] = d["r1"] - mu
    mu3 = d[d.grid3 == 1].groupby("coin")["r3"].mean()
    d["u3"] = d["r3"] - d["coin"].map(mu3)
    d["q"] = d.groupby("coin")["z0"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    def tt(s):
        s = s.dropna(); return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan))
    out["u1_by_z_decile"] = d.groupby("q")["u1"].apply(tt).unstack().round(5)
    out["u3_by_z_decile_grid3"] = d[d.grid3 == 1].groupby("q")["u3"].apply(tt).unstack().round(5)
    low = d[d.q <= 1]
    out["low20_u1_by_coin"] = low.groupby("coin")["u1"].apply(tt).unstack().round(5)
    out["low20_u1_by_year"] = low.groupby("year")["u1"].apply(tt).unstack().round(5)
    # clustered by day: average over coins each day
    cl_ = low.groupby("day")["u1"].mean()
    out["low20_u1_day_clustered"] = tt(cl_).round(5)
    # within-coin spearman of z0 vs u1 on negative z0 only
    sp = []
    for c, g in d[d.z0 < 0].groupby("coin"):
        g = g.dropna(subset=["z0", "u1"]); r, p = stats.spearmanr(g["z0"], g["u1"]); sp.append(dict(coin=c, rho=r, p=p, n=len(g)))
    out["spearman_negz_by_coin"] = pd.DataFrame(sp).set_index("coin").round(4)
    sp = []
    for c, g in d[d.z0 > 0].groupby("coin"):
        g = g.dropna(subset=["z0", "u1"]); r, p = stats.spearmanr(g["z0"], g["u1"]); sp.append(dict(coin=c, rho=r, p=p, n=len(g)))
    out["spearman_posz_by_coin"] = pd.DataFrame(sp).set_index("coin").round(4)
    # weekday robustness
    sat = d[d.wd == 5]
    out["sat_u1_by_coin"] = sat.groupby("coin")["u1"].apply(tt).unstack().round(5)
    out["sat_u1_by_year"] = sat.groupby("year")["u1"].apply(tt).unstack().round(5)
    out["wd_u1_day_clustered"] = d.groupby(["wd", "day"])["u1"].mean().groupby(level=0).apply(tt).unstack().round(5)
    # interaction: low decile by vol tercile
    d["vt"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["low20_u1_by_voltercile"] = low.assign(vt=d.loc[low.index, "vt"]).groupby("vt")["u1"].apply(tt).unstack().round(5)
    out["hours"] = d["hour"].value_counts().head(3)
    return out
