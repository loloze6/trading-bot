def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            r60 = c / c.shift(60) - 1
            trend = np.where(r60.isna(), "na", np.where(r60 > 0.10, "rising", np.where(r60 < -0.10, "falling", "choppy")))
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "z1": r1 / sd, "sd": sd, "trend": trend, "wd": ts.dt.weekday,
                               "z2": (c / c.shift(2) - 1) / (sd * np.sqrt(2))})
            for h in (1, 2, 3):
                df["f%d" % h] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["agit"] = np.where(D["sd"].isna(), "na", np.where(D["sd"] > D.groupby("coin")["sd"].transform("median"), "agitated", "calm"))
    out = {}
    def grid(h):
        g = D[(D["pos"] % h == 0)].dropna(subset=["f%d" % h]).copy()
        drift = D.dropna(subset=["f%d" % h]).groupby("coin")["f%d" % h].mean()
        g["ex"] = g["f%d" % h] - g["coin"].map(drift)
        return g
    def ct(g):
        m = g["ex"].mean()
        s = (g["ex"] - m).groupby(g["day"]).sum()
        G = len(s)
        se = np.sqrt(G / (G - 1) * (s ** 2).sum()) / len(g) if G > 1 else np.nan
        return pd.Series({"n": len(g), "days": G, "mean": m, "t_day": m / se})
    for h in (1, 2, 3):
        g = grid(h).dropna(subset=["z1"])
        g["q"] = pd.qcut(g["z1"], 5, labels=False)
        g["prof"] = g["trend"] + "_" + g["agit"]
        sub = g[g.q == 4]
        out["z1 top quintile -> next %dd excess, by profile" % h] = sub.groupby("prof").apply(ct).round(4)
        fa = g[(g.prof == "falling_agitated") & (g.z1 > 0)].copy()
        if len(fa) > 20:
            fa["t3"] = pd.qcut(fa["z1"], 3, labels=False)
            out["falling agitated, rise days, z1 tercile -> next %dd" % h] = fa.groupby("t3").apply(ct).round(4)
    g = grid(1).copy()
    g["wdn"] = (g["wd"] + 1) % 7
    out["next-day excess by weekday (day-clustered)"] = g.groupby("wdn").apply(ct).round(4)
    g2 = grid(2).dropna(subset=["z2"]); g2["q"] = pd.qcut(g2["z2"], 5, labels=False)
    g2["prof"] = g2["trend"] + "_" + g2["agit"]
    out["z2 top quintile -> next 2d, by profile"] = g2[g2.q == 4].groupby("prof").apply(ct).round(4)
    return out
