import pandas as pd, numpy as np
from scipy import stats

def ct(d, col):
    d = d.dropna(subset=[col])
    if len(d) < 3:
        return pd.Series({"n": len(d), "days": d["day"].nunique() if len(d) else 0, "mean": d[col].mean() if len(d) else np.nan, "t": np.nan})
    m = d[col].mean()
    s = (d[col]-m).groupby(d["day"]).sum()
    D = len(s)
    se = np.sqrt((s**2).sum()*D/(D-1))/len(d)
    return pd.Series({"n": len(d), "days": D, "mean": m, "t": m/se if se > 0 else np.nan})

def explore(data):
    G = []; Dl = []
    for coin, wins in data["bars"].items():
        g7, d1 = [], []
        for w, b in wins.items():
            c = b["close"].values
            g7 += [c[i+7]/c[i]-1 for i in range(0, len(c)-7, 7)]
            d1 += list(pd.Series(c).pct_change().dropna())
        m7, m1 = np.mean(g7), np.mean(d1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change(); sd = r1.rolling(30).std()
            z7 = (c/c.shift(7)-1)/(sd*np.sqrt(7))
            r60 = c/c.shift(60)-1
            f7 = c.shift(-7)/c-1; f1 = c.shift(-1)/c-1; f3 = c.shift(-3)/c-1
            ts = pd.to_datetime(b["timestamp"]); day = ts.dt.floor("D")
            inp = b["regime"] == "unknown"
            rng = (b["high"]-b["low"])/c/sd
            for i in range(0, len(b)-7, 7):
                G.append(dict(day=day[i], inp=inp[i], z=z7[i], r60=r60[i], fx=f7[i]-m7, coin=coin))
            for i in range(0, len(b)-3, 3):
                Dl.append(dict(day=day[i], wd=ts[i].weekday(), r1z=r1[i]/sd[i] if sd[i] > 0 else np.nan,
                               rng=rng[i], f3x=f3[i]-3*m1, inp=inp[i]))
    G = pd.DataFrame(G); D = pd.DataFrame(Dl)
    out = {}
    gc = G[(G.r60.abs() <= 0.1)].dropna(subset=["z", "fx"]).copy()
    gc["zq"] = pd.qcut(gc.z, 4, labels=False)
    out["choppy_trend_z_quartile_f7"] = gc.groupby("zq").apply(lambda d: ct(d, "fx"))
    gn = gc[gc.z < 0]
    out["choppy_falls_spearman"] = pd.Series({"rho": stats.spearmanr(gn.z, gn.fx)[0], "n": len(gn)})
    gi = G[G.inp & (G.z < 0)].dropna(subset=["z", "fx"])
    out["inprof_falls_spearman"] = pd.Series({"rho": stats.spearmanr(gi.z, gi.fx)[0] if len(gi) > 5 else np.nan, "n": len(gi)})
    Dd = D.dropna(subset=["rng", "f3x"]).copy()
    Dd["rq"] = pd.qcut(Dd.rng, 5, labels=False)
    out["range_q_f3_clustered"] = Dd.groupby("rq").apply(lambda d: ct(d, "f3x"))
    Dd2 = D.dropna(subset=["r1z", "f3x"]).copy()
    Dd2["q"] = pd.qcut(Dd2.r1z, 5, labels=False)
    out["r1z_q_f3_clustered"] = Dd2.groupby("q").apply(lambda d: ct(d, "f3x"))
    out["wide_range_by_dir"] = Dd[Dd.rq == 4].dropna(subset=["r1z"]).groupby(Dd["r1z"] > 0).apply(lambda d: ct(d, "f3x"))
    return out
