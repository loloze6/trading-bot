def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20, min_periods=15).std()
            z = r / sd20
            rng = (b["high"] - b["low"]).astype(float)
            cl = (c - b["low"]) / rng.replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "w": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "z": z, "r": r, "sd20": sd20, "cl": cl,
                "r5p": c / c.shift(5) - 1, "r20p": c / c.shift(20) - 1,
                "vr": sd20 / r.rolling(60, min_periods=40).std(),
                "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
                "pos": b["postRebalance_current_allocation"].astype(float),
                "pos_prev": b["previous_allocation"].astype(float),
                "fc": b["forecast"].astype(float), "i": np.arange(len(b))})
            d["wd"] = d["day"].dt.weekday
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["f1"].mean()
    mu3 = D[D.i % 3 == 0].groupby("coin")["f3"].mean()
    mu5 = D[D.i % 5 == 0].groupby("coin")["f5"].mean()
    D["x1"] = D["f1"] - D["coin"].map(mu)
    D["x3"] = D["f3"] - D["coin"].map(mu3)
    D["x5"] = D["f5"] - D["coin"].map(mu5)

    def ct(sub, col):
        s = sub[["day", col]].dropna()
        n = len(s)
        if n < 10: return (n, np.nan, np.nan)
        m = s[col].mean()
        S = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((S ** 2).sum()) / n
        return (n, m, m / se if se > 0 else np.nan)

    def tab(df, key, col="x1", grid=None):
        out = []
        for k, g in df.groupby(key, observed=True):
            if grid: g = g[g.i % grid == 0]
            n, m, t = ct(g, col)
            out.append({"k": str(k), "n": n, "mean%": m * 100 if m == m else m, "t": t})
        return pd.DataFrame(out)

    D["zb"] = pd.cut(D["z"], [-99, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3, 99])
    res = {}
    res["x1_by_z"] = tab(D, "zb")
    res["x3_by_z_grid3"] = tab(D, "zb", "x3", 3)
    res["x5_by_z_grid5"] = tab(D, "zb", "x5", 5)
    dn = D[D.z < -1].copy()
    dn["clb"] = pd.cut(dn["cl"], [0, 0.25, 0.5, 0.75, 1.0001], include_lowest=True)
    res["falls_z<-1_x1_by_closeloc"] = tab(dn, "clb")
    dn["t20"] = pd.cut(dn["r20p"], [-9, -0.15, -0.05, 0.05, 0.15, 99])
    res["falls_x1_by_20d_ret"] = tab(dn, "t20")
    dn["vrb"] = pd.cut(dn["vr"], [0, 0.8, 1.0, 1.25, 99])
    res["falls_x1_by_volratio"] = tab(dn, "vrb")
    dn["p5"] = pd.cut(dn["r5p"] - dn["r"], [-9, -0.1, -0.03, 0.03, 0.1, 99])
    res["falls_x1_by_prior4d"] = tab(dn, "p5")
    res["falls_x1_by_weekday"] = tab(dn, "wd")
    res["all_x1_by_weekday"] = tab(D, "wd")
    res["falls_x1_by_window"] = tab(dn, "w")
    up = D[D.z > 1].copy()
    up["clb"] = pd.cut(up["cl"], [0, 0.25, 0.5, 0.75, 1.0001], include_lowest=True)
    res["ups_z>1_x1_by_closeloc"] = tab(up, "clb")
    # book contribution
    D["g"] = D["pos"] * D["f1"]
    res["book_gain_by_z_sum%"] = D.groupby("zb", observed=True)["g"].agg(["count", "mean", "sum"]).mul([1, 100, 100])
    return res
