import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "regime": b["regime"].astype(str),
                "r1": c / c.shift(1) - 1, "r3": c / c.shift(3) - 1,
                "vr1": v / v.shift(1).rolling(20).mean(),
                "vr3": v.rolling(3).mean() / v.shift(3).rolling(20).mean(),
                "ret20": c / c.shift(20) - 1,
            })
            for h in [1, 3, 5, 10]:
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["fc"] = D["regime"].isin(["trending", "unknown"])
    out = {}
    out["regime counts"] = D["regime"].value_counts()
    # coin drift per horizon on its grid
    drift = {}
    for h in [1, 3, 5, 10]:
        g = D[D["pos"] % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()

    def summ(sub, h):
        x = sub[f"f{h}"] - sub["coin"].map(drift[h])
        ok = x.notna(); x = x[ok]; days = sub.loc[ok, "day"]
        n = len(x)
        if n < 3: return pd.Series({"n": n})
        m = x.mean()
        S = (x - m).groupby(days).sum()
        se = np.sqrt((S ** 2).sum()) / n
        return pd.Series({"n": n, "days": days.nunique(), "excess%": 100 * m,
                          "total%": 100 * sub.loc[ok, f"f{h}"].mean(), "t_day": m / se if se > 0 else np.nan})

    def label(s):
        lab = pd.Series("down", index=s.index)
        up = s["r1"] > 0
        q = s.loc[up, "vr1"].quantile([1/3, 2/3]).values
        lab[up & (s["vr1"] <= q[0])] = "up_light"
        lab[up & (s["vr1"] > q[0]) & (s["vr1"] <= q[1])] = "up_mid"
        lab[up & (s["vr1"] > q[1])] = "up_heavy"
        return lab

    for h in [1, 3, 5, 10]:
        g = D[(D["pos"] % h == 0)].copy()
        g["lab"] = label(g)
        res = []
        for (fc, lab), s in g.groupby(["fc", "lab"]):
            r = summ(s, h); r["fc"] = fc; r["lab"] = lab; res.append(r)
        out[f"h{h} single-day buckets by falling-calm"] = pd.DataFrame(res)
    # 3-day up on heavy 3d volume, graded, falling calm, h5
    for h in [3, 5, 10]:
        g = D[(D["pos"] % h == 0) & D["fc"]].copy()
        g["ex"] = g[f"f{h}"] - g["coin"].map(drift[h])
        g = g.dropna(subset=["ex", "r3", "vr3", "r1", "vr1"])
        up = g[g["r1"] > 0]
        out[f"h{h} fc up-day spearman vr1 vs excess"] = f"rho={stats.spearmanr(up['vr1'], up['ex'])[0]:.3f} n={len(up)}"
        out[f"h{h} fc spearman r1 vs excess"] = f"rho={stats.spearmanr(g['r1'], g['ex'])[0]:.3f} n={len(g)}"
        out[f"h{h} fc spearman ret20 vs excess"] = f"rho={stats.spearmanr(g['ret20'], g['ex'], nan_policy='omit')[0]:.3f}"
        dn = g[g["r1"] < 0]
        out[f"h{h} fc down-day spearman vr1 vs excess"] = f"rho={stats.spearmanr(dn['vr1'], dn['ex'])[0]:.3f} n={len(dn)}"
        g["r1q"] = pd.qcut(g["r1"], 5, labels=False)
        out[f"h{h} fc by 1-day return quintile"] = g.groupby("r1q").apply(lambda s: summ(s, h))
    g = D[(D["pos"] % 5 == 0) & D["fc"]].copy(); g["lab"] = label(g)
    out["h5 fc by coin x lab"] = g.groupby(["coin", "lab"]).apply(lambda s: summ(s, 5))[["n", "excess%", "t_day"]]
    out["h5 fc by year"] = g.groupby("year").apply(lambda s: summ(s, 5))[["n", "excess%", "t_day"]]
    return out
