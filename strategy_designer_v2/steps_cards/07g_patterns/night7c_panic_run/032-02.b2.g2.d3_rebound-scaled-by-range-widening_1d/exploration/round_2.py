def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = (h - l) / c
            r1 = c / c.shift(1) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "fwd1": c.shift(-1) / c - 1,
                "fwd3": c.shift(-3) / c - 1,
                "ret1": r1,
                "z1": r1 / r1.rolling(30).std().shift(1),
                "rr20_60": rng.rolling(20).mean() / rng.rolling(60).mean(),
                "rr": rng.rolling(30).mean() / rng.rolling(90).mean(),
                "pos": np.arange(len(b)),
                "gain": b["postRebalance_current_allocation"] * (c.shift(-1) / c - 1),
                "fc": b["forecast"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["fwd1"].mean()
    D["ab"] = D["fwd1"] - D["coin"].map(drift)
    D = D.dropna(subset=["ab"])
    D["wd"] = D["day"].dt.dayofweek
    D["yr"] = D["day"].dt.year

    def dayt(g):
        s = g.groupby("day")["ab"].sum()
        n = len(s)
        return pd.Series({"cases": len(g), "days": n, "mean_ab%": 100*g["ab"].mean(),
                          "t_day": s.mean()/(s.std()/np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    D["z1q"] = pd.qcut(D["z1"], 10, labels=False)
    out["z1_decile"] = D.groupby("z1q").apply(dayt)
    D["z1q"] = pd.qcut(D["z1"], 5, labels=False)
    out["z1_bottom_by_win"] = D[D["z1q"] == 0].groupby("win").apply(dayt)
    out["z1_bottom_by_coin"] = D[D["z1q"] == 0].groupby("coin").apply(dayt)
    out["z1_bottom_by_year"] = D[D["z1q"] == 0].groupby("yr").apply(dayt)
    out["z1_bottom_by_rr"] = D[D["z1q"] == 0].assign(hi=D["rr20_60"] > 1).groupby("hi").apply(dayt)
    D["rrq2"] = pd.qcut(D["rr20_60"], 5, labels=False)
    out["rr20_60_quint"] = D.groupby("rrq2").apply(dayt)
    D["rrq"] = pd.qcut(D["rr"], 5, labels=False)
    out["rr_low_by_win"] = D[D["rrq"] == 0].groupby("win").apply(dayt)
    out["rr_quint_dayt"] = D.groupby("rrq").apply(dayt)
    out["weekday_dayt"] = D.groupby("wd").apply(dayt)
    out["thu_fri_by_year"] = D[D["wd"].isin([3, 4])].groupby("yr").apply(dayt)
    # book's largest gains/losses: what preceded
    G = D.dropna(subset=["gain"])
    G = G[G["gain"] != 0]
    G["gq"] = pd.qcut(G["gain"], 10, labels=False, duplicates="drop")
    out["book_gain_decile_context"] = G.groupby("gq").agg(n=("gain","size"), gain=("gain","mean"),
                                                          z1=("z1","mean"), fc=("fc","mean"), rr=("rr20_60","mean"))
    return out
