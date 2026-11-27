def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            v30 = r1.rolling(30).std()
            d = pd.DataFrame({
                "coin": coin, "w": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "r20p": c / c.shift(20) - 1, "r10p": c / c.shift(10) - 1,
                "r60p": c / c.shift(60) - 1,
                "v30": v30, "v30med": v30.expanding(20).median(),
                "f1": c.shift(-1) / c - 1, "f5": c.shift(-5) / c - 1,
            })
            d["r20z"] = d["r20p"] / (d["v30"] * np.sqrt(20))
            d["r1z"] = d["r1"] / d["v30"].shift(1)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["trend"] = np.where(D["r60p"] > 0.10, "rising", np.where(D["r60p"] < -0.10, "falling", np.where(D["r60p"].notna(), "choppy", "na")))
    D["agit"] = np.where(D["v30"] > D["v30med"], "agitated", "calm")
    D["half"] = np.where(D["wn"] <= 12, "w7-12", "w13-18")
    out = {}
    def ct(g, col="u"):
        n = len(g); m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n if G > 1 else np.nan
        return n, G, m, m / se
    def slope(g, x, y="u"):
        g = g.dropna(subset=[x, y])
        xx = g[x] - g[x].mean(); b = (xx * g[y]).sum() / (xx ** 2).sum()
        e = g[y] - g[y].mean() - b * xx
        s = (xx * e).groupby(g["day"]).sum(); G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (xx ** 2).sum()
        return b, b / se, len(g), G
    G5 = D[(D["pos"] % 5 == 0)].dropna(subset=["f5", "r20z"]).copy()
    dr5 = D[D["pos"] % 5 == 0].groupby("coin")["f5"].mean()
    G5["u"] = G5["f5"] - G5["coin"].map(dr5)
    res = []
    for k, g in [("all", G5)] + list(G5.groupby("half")) + list(G5.groupby("trend")) + list(G5.groupby(["trend", "agit"])):
        b, t, n, G = slope(g, "r20z")
        res.append({"group": str(k), "slope_u_on_r20z_%": 100 * b, "t": t, "n": n, "days": G})
    out["r20_momentum_slope"] = pd.DataFrame(res)
    # short side: negative r20z only, by trend/agit and half
    res = []
    neg = G5[G5["r20z"] < 0]
    for k, g in [("all", neg)] + list(neg.groupby("half")) + list(neg.groupby("trend")) + list(neg.groupby(["trend", "agit"])):
        b, t, n, G = slope(g, "r20z")
        n2, G2, m, tm = ct(g)
        res.append({"group": str(k), "slope_%": 100 * b, "t_slope": t, "mean_u_%": 100 * m, "t_mean": tm, "n": n, "days": G})
    out["neg_r20_by_profile"] = pd.DataFrame(res)
    # 1-day fall rebound by profile
    G1 = D.dropna(subset=["f1", "r1z"]).copy()
    dr1 = D.groupby("coin")["f1"].mean()
    G1["u"] = G1["f1"] - G1["coin"].map(dr1)
    res = []
    for k, g in list(G1.groupby(["trend", "agit"])) + list(G1.groupby("half")):
        b, t, n, G = slope(g[g["r1z"] < 0], "r1z")
        res.append({"group": str(k), "slope_u_on_neg_r1z_%": 100 * b, "t": t, "n": n, "days": G})
    out["fall_rebound_by_profile"] = pd.DataFrame(res)
    # weekday by half
    G1["wd"] = G1["ts"].dt.dayofweek
    res = []
    for (h, wd), g in G1.groupby(["half", "wd"]):
        n, G, m, t = ct(g)
        res.append({"half": h, "wd": wd, "mean_u_%": 100 * m, "t": t, "days": G})
    out["weekday_by_half"] = pd.DataFrame(res)
    return out
