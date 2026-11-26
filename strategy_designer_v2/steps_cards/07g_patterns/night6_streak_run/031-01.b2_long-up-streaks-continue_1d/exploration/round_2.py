def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            up = (r1 > 0).astype(int); dn = (r1 < 0).astype(int)
            us = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            ds = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
            rows.append(pd.DataFrame({
                "coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "r7p": c / c.shift(7) - 1, "r14p": c / c.shift(14) - 1,
                "r30p": c / c.shift(30) - 1, "vol20": r1.rolling(20).std(),
                "us": us, "ds": ds, "fwd3": c.shift(-3) / c - 1,
                "absr1": r1.abs(), "pos": np.arange(len(b))}))
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % 3 == 0].dropna(subset=["fwd3", "vol20"]).copy()
    g["ex"] = g["fwd3"] - g["coin"].map(g.groupby("coin")["fwd3"].mean())
    g["absf"] = g["fwd3"].abs() / (g["vol20"] * np.sqrt(3))
    g["streak"] = np.maximum(g["us"], g["ds"])

    def slope_day(df, x, y):
        df = df.dropna(subset=[x, y])
        X = df[x] - df[x].mean(); Y = df[y] - df[y].mean()
        b = (X * Y).sum() / (X * X).sum()
        e = Y - b * X
        sc = (X * e).groupby(df["ts"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X * X).sum()
        return {"n": len(df), "days": df["ts"].nunique(), "slope": b, "t_day": b / se}

    res = {}
    out = {}
    for x in ["r7p", "r14p", "r30p"]:
        g[x + "z"] = g[x] / (g["vol20"] * np.sqrt(int(x[1:-1])))
        out[x + "z_on_ex"] = slope_day(g, x + "z", "ex")
    out["us_on_ex"] = slope_day(g[g["us"] > 0], "us", "ex")
    out["ds_on_ex"] = slope_day(g[g["ds"] > 0], "ds", "ex")
    out["streak_on_absf"] = slope_day(g, "streak", "absf")
    out["us_on_absf"] = slope_day(g[g["us"] > 0], "us", "absf")
    out["ds_on_absf"] = slope_day(g[g["ds"] > 0], "ds", "absf")
    res["slopes"] = pd.DataFrame(out).T
    a = g[g["streak"] >= 4]["absf"]; bb = g[g["streak"] < 4]["absf"]
    res["absf_streak4_vs_rest"] = pd.Series({"n4": len(a), "m4": a.mean(), "nrest": len(bb),
        "mrest": bb.mean(), "welch_t": stats.ttest_ind(a, bb, equal_var=False).statistic})
    # streak>=4 absf by coin
    res["absf_streak4_by_coin"] = g.groupby(["coin", g["streak"] >= 4])["absf"].mean().unstack()
    # r30z momentum slope by coin and by year
    res["r30z_by_coin"] = pd.DataFrame({k: slope_day(s, "r30pz", "ex") for k, s in g.groupby("coin")}).T
    res["r30z_by_year"] = pd.DataFrame({k: slope_day(s, "r30pz", "ex") for k, s in g.groupby(g["ts"].dt.year)}).T
    # book: days around largest gains / losses
    bd = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            dd = dd.copy(); dd["coin"] = coin; bd.append(dd)
    bd = pd.concat(bd).dropna(subset=["book_return", "coin_return"])
    q = bd["book_return"].quantile([0.02, 0.98])
    res["book_tails"] = pd.DataFrame({
        "worst2%": bd[bd["book_return"] <= q.iloc[0]][["book_return", "coin_return"]].mean(),
        "best2%": bd[bd["book_return"] >= q.iloc[1]][["book_return", "coin_return"]].mean()})
    res["book_coin_corr"] = float(bd["book_return"].corr(bd["coin_return"]))
    return res
