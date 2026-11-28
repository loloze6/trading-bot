import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": ts.dt.floor("D"), "year": ts.dt.year,
                "regime": b["regime"].astype(str),
                "r1": c / c.shift(1) - 1, "r3": c / c.shift(3) - 1,
                "vr1": v / v.shift(1).rolling(20).mean(),
                "vr3": v.rolling(3).mean() / v.shift(3).rolling(20).mean(),
            })
            for h in [1, 3, 5, 10]:
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["fc"] = D["regime"].isin(["trending", "unknown"])
    out = {"regime counts": D["regime"].value_counts()}
    drift = {h: D[D["pos"] % h == 0].groupby("coin")[f"f{h}"].mean() for h in [1, 3, 5, 10]}
    out["drift% by coin"] = pd.DataFrame({h: 100 * drift[h] for h in drift})

    def summ(sub, h):
        x = sub[f"f{h}"] - sub["coin"].map(drift[h])
        ok = x.notna(); x = x[ok]; days = sub.loc[ok, "day"]; n = len(x)
        res = {"n": n, "days": days.nunique(), "excess%": np.nan, "total%": np.nan, "t_day": np.nan}
        if n >= 3:
            m = x.mean(); S = (x - m).groupby(days).sum()
            se = np.sqrt((S ** 2).sum()) / n
            res.update({"excess%": 100 * m, "total%": 100 * sub.loc[ok, f"f{h}"].mean(),
                        "t_day": m / se if se > 0 else np.nan})
        return pd.Series(res)

    def tab(g, keys, h):
        res = []
        for k, s in g.groupby(keys):
            r = summ(s, h)
            kk = k if isinstance(k, tuple) else (k,)
            for name, val in zip(keys if isinstance(keys, list) else [keys], kk):
                r[name] = val
            res.append(r)
        return pd.DataFrame(res)

    def label(s):
        lab = pd.Series("down", index=s.index)
        up = s["r1"] > 0
        q = s.loc[up, "vr1"].quantile([1/3, 2/3]).values
        lab[up & (s["vr1"] <= q[0])] = "up_light"
        lab[up & (s["vr1"] > q[0]) & (s["vr1"] <= q[1])] = "up_mid"
        lab[up & (s["vr1"] > q[1])] = "up_heavy"
        return lab

    for h in [1, 3, 5, 10]:
        g = D[D["pos"] % h == 0].copy(); g["lab"] = label(g)
        out[f"h{h} single-day buckets x fc"] = tab(g, ["fc", "lab"], h)
    for h in [3, 5, 10]:
        g = D[(D["pos"] % h == 0) & D["fc"]].copy()
        g["ex"] = g[f"f{h}"] - g["coin"].map(drift[h])
        g = g.dropna(subset=["ex", "r1", "vr1", "r3", "vr3"])
        up = g[g["r1"] > 0]; dn = g[g["r1"] < 0]
        up3 = g[(g["r3"] > 0) & (g["vr3"] > 1)]
        out[f"h{h} fc spearman"] = pd.Series({
            "up vr1 rho": stats.spearmanr(up["vr1"], up["ex"])[0], "n_up": len(up),
            "down vr1 rho": stats.spearmanr(dn["vr1"], dn["ex"])[0], "n_dn": len(dn),
            "all r1 rho": stats.spearmanr(g["r1"], g["ex"])[0],
            "all r3 rho": stats.spearmanr(g["r3"], g["ex"])[0],
            "r3up&vr3>1: r3*vr3 rho": stats.spearmanr(up3["r3"] * up3["vr3"], up3["ex"])[0], "n_up3": len(up3),
            "all vr3 rho": stats.spearmanr(g["vr3"], g["ex"])[0], "n": len(g)})
        g["r1q"] = pd.qcut(g["r1"], 5, labels=False)
        out[f"h{h} fc by 1-day return quintile"] = tab(g, "r1q", h)
        g["r3q"] = pd.qcut(g["r3"], 5, labels=False)
        out[f"h{h} fc by 3-day return quintile"] = tab(g, "r3q", h)
        g["vr3q"] = pd.qcut(g["vr3"], 4, labels=False)
        g["dir3"] = np.where(g["r3"] > 0, "up3", "down3")
        out[f"h{h} fc by 3d dir x 3d volume quartile"] = tab(g, ["dir3", "vr3q"], h)
    g = D[(D["pos"] % 5 == 0) & D["fc"]].copy(); g["lab"] = label(g)
    out["h5 fc coin x lab"] = tab(g, ["coin", "lab"], 5)
    out["h5 fc year x lab"] = tab(g[g["lab"] != "up_mid"], ["year", "lab"], 5)
    return out
