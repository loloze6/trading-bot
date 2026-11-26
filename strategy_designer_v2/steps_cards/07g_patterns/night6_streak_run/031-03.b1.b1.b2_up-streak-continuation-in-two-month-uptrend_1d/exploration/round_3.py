def explore(data):
    import pandas as pd, numpy as np
    allr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); r = c.pct_change()
            sd = r.rolling(60, min_periods=30).std()
            up = (r > 0).astype(int)
            us = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            dfw = pd.DataFrame({"coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]), "r1": r,
                                "z1": r / sd,
                                "z5": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                                "z30": (c / c.shift(30) - 1) / (sd * np.sqrt(30)),
                                "z60": (c / c.shift(60) - 1) / (sd * np.sqrt(60)),
                                "r30": c / c.shift(30) - 1, "r60": c / c.shift(60) - 1,
                                "us": us,
                                "f20": c.shift(-20) / c - 1, "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1,
                                "fc": b["forecast"].astype(float),
                                "pos": b["postRebalance_current_allocation"].astype(float),
                                "i": np.arange(len(b))})
            dfw["gain"] = dfw["pos"] * r.shift(-1)
            allr.append(dfw)
    D = pd.concat(allr, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D"); D["yr"] = D["ts"].dt.year
    def slope(df, x, y):
        d = df.dropna(subset=[x, y])
        if len(d) < 30: return {"slope": np.nan, "n": len(d)}
        X = d[x].clip(d[x].quantile(0.01), d[x].quantile(0.99)); Y = d[y]
        xm = X - X.mean(); b = (xm * (Y - Y.mean())).sum() / (xm ** 2).sum()
        e = (Y - Y.mean()) - b * xm
        s = (xm * e).groupby(d["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (xm ** 2).sum()
        return {"slope": round(b, 5), "t_cl": round(b / se, 2), "n": len(d), "days": s.size}
    out = {}
    for h, col in [(20, "f20"), (10, "f10"), (5, "f5")]:
        G = D[(D.i % h) == 0].copy()
        G["u"] = G[col] - G.groupby("coin")[col].transform("mean")
        res = {}
        for x in ["z1", "z5", "z30", "z60", "us"]:
            res[x] = slope(G, x, "u")
        Gu = G[(G.r30 > 0) & (G.r60 > 0)]
        for x in ["z30", "z60", "us"]:
            res[x + "_bothup"] = slope(Gu, x, "u")
        out[f"fwd{h} unusual slope on predictors, day-clustered"] = pd.DataFrame(res).T
    G = D[(D.i % 20) == 0].copy(); G["u"] = G["f20"] - G.groupby("coin")["f20"].transform("mean")
    yr = {}
    for y, g in G.groupby("yr"):
        yr[y] = slope(g, "z60", "u")
    out["fwd20 slope on z60 by year"] = pd.DataFrame(yr).T
    G5 = D[(D.i % 5) == 0].copy(); G5["u"] = G5["f5"] - G5.groupby("coin")["f5"].transform("mean")
    yr = {}
    for y, g in G5.groupby("yr"):
        yr[y] = slope(g, "z5", "u")
    out["fwd5 slope on z5 by year"] = pd.DataFrame(yr).T
    ip = D[D.pos.abs() > 1e-9]
    out["in-position gain slope on z60 (daily)"] = pd.Series(slope(ip, "z60", "gain"))
    out["in-position gain slope on forecast (daily)"] = pd.Series(slope(ip, "fc", "gain"))
    return out
