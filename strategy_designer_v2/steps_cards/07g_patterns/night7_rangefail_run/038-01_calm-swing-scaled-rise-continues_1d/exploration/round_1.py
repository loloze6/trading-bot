def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20).std()
            for H in (5,):
                pass
            ret5 = c / c.shift(5) - 1
            z = ret5 / (sd20 * np.sqrt(5))
            ret60 = c / c.shift(60) - 1
            ret1 = r
            z1 = r / sd20
            f5 = c.shift(-5) / c - 1
            f2 = c.shift(-2) / c - 1
            f10 = c.shift(-10) / c - 1
            rng = (b["high"] - b["low"]) / c
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "regime": b["regime"].values, "z": z, "z1": z1, "ret60": ret60,
                "f2": f2, "f5": f5, "f10": f10, "sd20": sd20, "rng": rng,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    for h in (2, 5, 10):
        D[f"x{h}"] = D[f"f{h}"] - D.groupby("coin")[f"f{h}"].transform(lambda s: s.iloc[::1].mean())
    D["calm"] = np.where(D["regime"] == "chop", "agitated", "calm")

    def tday(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5:
            return (np.nan, np.nan, len(s))
        g = s.groupby("day")[col].sum()
        cnt = s.groupby("day")[col].count()
        m = g.sum() / cnt.sum()
        dev = s[col] - m
        gd = dev.groupby(s["day"]).sum()
        se = np.sqrt((gd ** 2).sum()) / cnt.sum()
        return (m, m / se if se > 0 else np.nan, len(s))

    out = {}
    # grid of 5
    G5 = D[D["pos"] % 5 == 0].copy()
    G5["zb"] = pd.cut(G5["z"], [-99, -1.5, -0.75, -0.25, 0.25, 0.75, 1.5, 99])
    res = []
    for (cl, zb), s in G5.groupby(["calm", "zb"], observed=True):
        m, t, n = tday(s, "x5")
        res.append({"profile": cl, "zbin": str(zb), "mean_x5_%": round(100 * m, 3), "t": round(t, 2), "n": n})
    out["fwd5 excess by scaled 5d move & profile"] = pd.DataFrame(res)
    # regression slope by profile, both signs
    res = []
    for cl, s in G5.groupby("calm"):
        s = s.dropna(subset=["z", "x5"])
        sl = stats.linregress(s["z"], s["x5"])
        res.append({"profile": cl, "slope_%perz": round(100 * sl.slope, 3), "t_naive": round(sl.slope / sl.stderr, 2), "n": len(s)})
    out["slope x5 on z"] = pd.DataFrame(res)
    # 1-day scaled move, fwd 2 days, grid 2
    G2 = D[D["pos"] % 2 == 0].copy()
    G2["z1b"] = pd.cut(G2["z1"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    res = []
    for (cl, zb), s in G2.groupby(["calm", "z1b"], observed=True):
        m, t, n = tday(s, "x2")
        res.append({"profile": cl, "z1bin": str(zb), "mean_x2_%": round(100 * m, 3), "t": round(t, 2), "n": n})
    out["fwd2 excess by 1d scaled move"] = pd.DataFrame(res)
    # trend 60 profile x z sign
    G5["trend"] = pd.cut(G5["ret60"], [-99, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    G5["zs"] = np.where(G5["z"] > 0.75, "bigup", np.where(G5["z"] < -0.75, "bigdn", "mid"))
    res = []
    for (tr, zs), s in G5.groupby(["trend", "zs"], observed=True):
        m, t, n = tday(s, "x5")
        res.append({"trend": str(tr), "zs": zs, "mean_x5_%": round(100 * m, 3), "t": round(t, 2), "n": n})
    out["fwd5 by 60d trend & move"] = pd.DataFrame(res)
    # weekday, 1d grid
    D["wd"] = D["ts"].dt.weekday
    D["x1"] = D["ret1"] if False else D.groupby(["coin", "win"])["f2"].transform(lambda s: s)  # placeholder
    D["n1"] = D.groupby(["coin", "win"])["pos"].transform(lambda s: s)  # placeholder
    res = []
    for wd, s in D.groupby("wd"):
        nxt = s["f2"]
    # forward 1 day
    D["f1"] = D.groupby(["coin", "win"])["z"].transform(lambda s: s * 0)
    # vol level: sd20 terciles within coin
    G5["vq"] = G5.groupby("coin")["sd20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    res = []
    for (vq, zs), s in G5.groupby(["vq", "zs"]):
        m, t, n = tday(s, "x5")
        res.append({"volq": vq, "zs": zs, "mean_x5_%": round(100 * m, 3), "t": round(t, 2), "n": n})
    out["fwd5 by vol tercile & move"] = pd.DataFrame(res)
    # by year for calm big up
    G5["year"] = G5["ts"].dt.year
    res = []
    for (y, cl), s in G5[G5["z"] > 0.75].groupby(["year", "calm"]):
        m, t, n = tday(s, "x5")
        res.append({"year": y, "profile": cl, "mean_x5_%": round(100 * m, 3), "t": round(t, 2), "n": n})
    out["big up by year"] = pd.DataFrame(res)
    return out
