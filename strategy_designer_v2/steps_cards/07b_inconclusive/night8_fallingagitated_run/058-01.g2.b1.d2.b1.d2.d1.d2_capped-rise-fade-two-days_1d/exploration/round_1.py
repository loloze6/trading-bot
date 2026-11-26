import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            inprof = b["regime"].isin(["mean_reversion", "unknown"])
            n = len(b)
            for h in [1, 2, 3, 5, 10]:
                pass
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n), "z": z, "r1": r,
                               "inprof": inprof, "regime": b["regime"],
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            for h in [1, 2, 3, 5, 10]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    # normal drift per horizon: all bars, non-overlap grid
    drift = {}
    for h in [1, 2, 3, 5, 10]:
        g = D[D["pos"] % h == 0]
        drift[h] = g[f"f{h}"].mean()
    out = {}
    out["drift"] = pd.Series(drift)
    out["regime_counts"] = D["regime"].value_counts()
    P = D[D["inprof"] & D["z"].notna()].copy()
    P["zb"] = pd.cut(P["z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3, np.inf])
    # short-direction unusual move, horizon h, on 2-bar grid (h grid)
    tab = {}
    for h in [1, 2, 3, 5, 10]:
        g = P[P["pos"] % h == 0]
        u = -(g[f"f{h}"] - drift[h])
        tab[f"h{h}_mean"] = u.groupby(g["zb"]).mean()
        tab[f"h{h}_t"] = u.groupby(g["zb"]).apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan)
        tab[f"h{h}_n"] = u.groupby(g["zb"]).count()
    out["profile_by_z_short_unusual"] = pd.DataFrame(tab)
    # outside profile, same, for comparison, h2
    O = D[(~D["inprof"]) & D["z"].notna()].copy()
    O["zb"] = pd.cut(O["z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3, np.inf])
    g = O[O["pos"] % 2 == 0]; u = -(g["f2"] - drift[2])
    out["outside_profile_h2"] = pd.DataFrame({"mean": u.groupby(g["zb"]).mean(), "n": u.groupby(g["zb"]).count()})
    # in-range cases (0,1] by coin, year, h2 and h5
    S = P[(P["z"] > 0) & (P["z"] <= 1)]
    g2 = S[S["pos"] % 2 == 0]; u2 = -(g2["f2"] - drift[2])
    out["inrange_h2_by_coin"] = pd.DataFrame({"mean": u2.groupby(g2["coin"]).mean(), "n": u2.groupby(g2["coin"]).count()})
    out["inrange_h2_by_year"] = pd.DataFrame({"mean": u2.groupby(g2["year"]).mean(), "n": u2.groupby(g2["year"]).count()})
    # all up days in profile (z>0), correlation of z with short unusual move per horizon
    U = P[P["z"] > 0]
    cr = {}
    for h in [1, 2, 3, 5, 10]:
        g = U[U["pos"] % h == 0].dropna(subset=[f"f{h}"])
        u = -(g[f"f{h}"] - drift[h]) 
        rr, pp = stats.spearmanr(g["z"], u)
        cr[h] = {"spearman": rr, "p": pp, "n": len(g), "mean": u.mean(),
                 "t": u.mean() / (u.std() / np.sqrt(len(u)))}
    out["updays_corr"] = pd.DataFrame(cr).T
    # multi-day rise (brief's own situation): 3-day and 5-day rise scaled by sd*sqrt(k)
    return out
