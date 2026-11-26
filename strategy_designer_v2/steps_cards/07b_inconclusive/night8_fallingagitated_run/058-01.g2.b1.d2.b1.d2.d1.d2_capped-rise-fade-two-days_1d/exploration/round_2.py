import pandas as pd, numpy as np
from scipy import stats

def tclust(u, day):
    s = (u - u.mean()).groupby(day).sum()
    n = len(u)
    se = np.sqrt((s**2).sum()) / n
    return u.mean() / se if se > 0 else np.nan, s.shape[0]

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": r / sd,
                               "inprof": b["regime"].isin(["mean_reversion", "unknown"]),
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            for k in [3, 5]:
                df[f"z{k}"] = (c / c.shift(k) - 1) / (sd * np.sqrt(k))
            for h in [1, 2, 3, 5]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = {h: D[D["pos"] % h == 0][f"f{h}"].mean() for h in [1, 2, 3, 5]}
    P = D[D["inprof"]].copy()
    out = {}
    # 1-day horizon, capped in-range rise
    S = P[(P["z"] > 0) & (P["z"] <= 1)].dropna(subset=["f1"])
    u = -(S["f1"] - drift[1]); tot = -S["f1"]
    t, nd = tclust(u, S["day"])
    out["h1_inrange_summary"] = pd.Series({"mean_unusual": u.mean(), "t_clust": t, "days": nd, "n": len(u),
                                           "mean_total": tot.mean(),
                                           "spearman_z": stats.spearmanr(S["z"], u)[0]})
    out["h1_inrange_by_year"] = pd.DataFrame({"mean": u.groupby(S["year"]).mean(), "n": u.groupby(S["year"]).count()})
    out["h1_inrange_by_coin"] = pd.DataFrame({"mean": u.groupby(S["coin"]).mean(), "n": u.groupby(S["coin"]).count()})
    out["h1_inrange_by_win"] = pd.DataFrame({"mean": u.groupby(S["win"]).mean(), "n": u.groupby(S["win"]).count()})
    # all up days in profile, h1, by z tercile
    U = P[P["z"] > 0].dropna(subset=["f1"]).copy()
    U["q"] = pd.qcut(U["z"], 4, labels=False)
    uu = -(U["f1"] - drift[1])
    out["h1_updays_by_quartile"] = pd.DataFrame({"mean": uu.groupby(U["q"]).mean(), "z_mean": U["z"].groupby(U["q"]).mean(), "n": uu.groupby(U["q"]).count()})
    # multi-day rise (brief's situation)
    res = {}
    for k in [3, 5]:
        M = P[P[f"z{k}"] > 0]
        for h in [1, 2, 3, 5]:
            g = M[M["pos"] % h == 0].dropna(subset=[f"f{h}"])
            v = -(g[f"f{h}"] - drift[h])
            tt, nd = tclust(v, g["day"])
            res[f"rise{k}_h{h}"] = {"mean": v.mean(), "t_clust": tt, "days": nd, "n": len(v),
                                   "spearman": stats.spearmanr(g[f"z{k}"], v)[0],
                                   "total": (-g[f"f{h}"]).mean()}
    out["multiday"] = pd.DataFrame(res).T
    return out
