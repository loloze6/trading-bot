def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); o = b["open"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            z5 = (c / c.shift(5) - 1) / (vol20 * np.sqrt(5))
            z1 = r1 / vol20
            rng = (hi - lo) / c.shift(1)
            rngz = rng / rng.rolling(20, min_periods=15).mean()
            volz = np.log(v / v.rolling(20, min_periods=15).mean())
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                              "fwd": c.shift(-H) / c - 1, "fwd1": c.shift(-1) / c - 1,
                              "z5": z5, "z1": z1, "rngz": rngz, "volz": volz,
                              "wd": ts.dt.dayofweek, "yr": ts.dt.year})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    drift = G.groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    def dayt(g, col="ex"):
        s = g.groupby("day")[col].sum()
        n = g[col].count()
        return pd.Series({"n": n, "days": len(s), "mean_%": 100 * g[col].mean(),
                          "t_day": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out = {}
    # wide range graded, split by day direction
    G["rq"] = pd.qcut(G["rngz"], 5, labels=False)
    G["dir"] = np.where(G["z1"] > 0, "upday", "downday")
    out["range_q_by_daydir"] = G.groupby(["dir", "rq"]).apply(dayt)
    # z5 negative extremes
    G["zq"] = pd.cut(G["z5"], [-9, -2, -1.5, -1, 0, 1, 1.5, 2, 9])
    out["z5_fine_dayt"] = G.groupby("zq").apply(dayt)
    out["z5_lt_-1.5_by_coin"] = G[G["z5"] < -1.5].groupby("coin").apply(dayt)
    # volume
    out["volz_q"] = G.groupby(pd.qcut(G["volz"], 5)).apply(dayt)
    out["volz_q_by_daydir"] = G.groupby(["dir", pd.qcut(G["volz"], 3, labels=False)]).apply(dayt)
    # weekday, daily returns, day-clustered
    A["d1ex"] = A["fwd1"] - A["coin"].map(A.groupby("coin")["fwd1"].mean())
    A["wd_next"] = (A["wd"] + 1) % 7
    W = A.dropna(subset=["d1ex"])
    out["next_day_ret_by_its_weekday"] = W.groupby("wd_next").apply(lambda g: dayt(g, "d1ex"))
    sat = W[W["wd_next"] == 5]
    out["saturday_by_year"] = sat.groupby("yr").apply(lambda g: dayt(g, "d1ex"))
    out["saturday_by_coin"] = sat.groupby("coin").apply(lambda g: dayt(g, "d1ex"))
    # book around its largest days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w; D.append(dd)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk["book_return"].quantile([0.02, 0.98])
    out["book_extremes_coin_ret_%"] = pd.DataFrame({
        "top2%_book": bk[bk["book_return"] >= q[0.98]].mean() * 100,
        "bottom2%_book": bk[bk["book_return"] <= q[0.02]].mean() * 100})
    return out
