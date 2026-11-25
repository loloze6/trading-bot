def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r": r, "z": r / sd,
                "z_prev": (r / sd).shift(1),
                "fwd1": r.shift(-1),
                "fwd3": c.shift(-3) / c - 1,
                "ret60": c / c.shift(60) - 1,
                "ret5": c / c.shift(5) - 1,
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rng": (b["high"] - b["low"]) / c.shift(1) / sd,
                "vrel": b["volume"] / b["volume"].rolling(30, min_periods=20).mean(),
                "sdrel": sd / sd.rolling(90, min_periods=40).median(),
                "pos": np.arange(len(b)),
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["fwd1"].mean()
    d["ex1"] = d["fwd1"] - d["coin"].map(mu)
    mu3 = d[d["pos"] % 3 == 0].groupby("coin")["fwd3"].mean()
    d["ex3"] = d["fwd3"] - d["coin"].map(mu3)
    d["wd"] = d["ts"].dt.dayofweek
    d["yr"] = d["ts"].dt.year

    def stat(g, col="ex1"):
        x = g[col].dropna()
        n = len(x)
        if n < 3:
            return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n))})

    zb = pd.cut(d["z"], [-np.inf, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 3, np.inf])
    out = {}
    out["ex1 by z bin"] = d.groupby(zb).apply(stat)
    d3 = d[d["pos"] % 3 == 0]
    out["ex3 by z bin (grid)"] = d3.groupby(pd.cut(d3["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])).apply(lambda g: stat(g, "ex3"))
    dn = d[d["z"] < -1]
    out["z<-1 ex1 by trend"] = dn.groupby(pd.cut(dn["ret60"], [-np.inf, -0.1, 0.1, np.inf])).apply(stat)
    out["z<-1 ex1 by sdrel"] = dn.groupby(pd.cut(dn["sdrel"], [0, 0.8, 1.0, 1.25, np.inf])).apply(stat)
    out["z<-1 ex1 by clv"] = dn.groupby(pd.cut(dn["clv"], [-0.01, 0.15, 0.35, 0.6, 1.01])).apply(stat)
    out["z<-1 ex1 by vrel"] = dn.groupby(pd.cut(dn["vrel"], [0, 1, 1.5, 2.5, np.inf])).apply(stat)
    out["z<-1 ex1 by ret5"] = dn.groupby(pd.cut(dn["ret5"], [-np.inf, -0.15, -0.07, 0, np.inf])).apply(stat)
    out["z<-1 ex1 by weekday"] = dn.groupby("wd").apply(stat)
    out["z<-1 ex1 by year"] = dn.groupby("yr").apply(stat)
    out["z<-1 ex1 by coin"] = dn.groupby("coin").apply(stat)
    up = d[d["z"] > 1]
    out["z>1 ex1 by trend"] = up.groupby(pd.cut(up["ret60"], [-np.inf, -0.1, 0.1, np.inf])).apply(stat)
    out["z>1 ex1 by clv"] = up.groupby(pd.cut(up["clv"], [-0.01, 0.4, 0.65, 0.85, 1.01])).apply(stat)
    out["all ex1 by weekday"] = d.groupby("wd").apply(stat)
    out["all ex1 by clv"] = d.groupby(pd.cut(d["clv"], [-0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 1.01])).apply(stat)
    out["all ex1 by rng (range/sd)"] = d.groupby(pd.cut(d["rng"], [0, 1, 1.5, 2, 3, np.inf])).apply(stat)
    out["two-day: z_prev<-1 & z by sign"] = d[d["z_prev"] < -1].groupby(np.sign(d["z"])).apply(stat)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["win"] = w; t["coin"] = coin; dd.append(t)
    dd = pd.concat(dd)
    bk = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.02, 0.98])
    out["book worst2%/best2% mean coin_ret%"] = pd.DataFrame({
        "worst": [100 * bk[bk.book_return <= q.iloc[0]].coin_return.mean(), (bk.book_return <= q.iloc[0]).sum()],
        "best": [100 * bk[bk.book_return >= q.iloc[1]].coin_return.mean(), (bk.book_return >= q.iloc[1]).sum()]},
        index=["coin_ret%", "n"])
    return out
