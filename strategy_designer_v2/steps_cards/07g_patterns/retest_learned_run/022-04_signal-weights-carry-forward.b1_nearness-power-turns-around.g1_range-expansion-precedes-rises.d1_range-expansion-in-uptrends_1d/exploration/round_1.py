def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = (h - l) / c
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "r1": c / c.shift(1) - 1,
                "ret5p": c / c.shift(5) - 1,
                "ret20": c / c.shift(20) - 1,
                "rr": (h - l) / (h - l).rolling(30, min_periods=20).mean(),
                "vol20": (c / c.shift(1) - 1).rolling(20).std(),
                "nearhi": c / h.rolling(30, min_periods=20).max() - 1,
                "clpos": (c - l) / (h - l).replace(0, np.nan),
                "fwd": c.shift(-H) / c - 1,
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            f["pos"] = np.arange(len(f))
            rows.append(f)
    d = pd.concat(rows, ignore_index=True)
    g = d[(d["pos"] % H == 0)].dropna(subset=["fwd"]).copy()
    drift = g.groupby("coin")["fwd"].mean()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    sd = g.groupby("coin")["fwd"].std()
    g["exz"] = g["ex"] / g["coin"].map(sd)
    out = {}
    def reg(df, x):
        df = df.dropna(subset=[x, "exz"])
        z = df.groupby("coin")[x].transform(lambda s: (s - s.mean()) / s.std())
        r = stats.linregress(z, df["exz"])
        return r.slope, r.slope / r.stderr, len(df)
    feats = ["r1", "ret5p", "ret20", "rr", "vol20", "nearhi", "clpos"]
    res = []
    for x in feats:
        for name, sub in [("all", g), ("up20", g[g.ret20 > 0]), ("dn20", g[g.ret20 <= 0])]:
            s, t, n = reg(sub, x)
            res.append({"feat": x, "set": name, "slope_z": s, "t": t, "n": n})
    out["slopes_std_ex5_on_feature"] = pd.DataFrame(res)
    # quintiles of key features, mean excess 5d %
    q = []
    for x in feats:
        sub = g.dropna(subset=[x]).copy()
        sub["q"] = sub.groupby("coin")[x].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        m = sub.groupby("q")["ex"].agg(["mean", "count"])
        q.append(pd.Series(m["mean"].values * 100, index=[f"q{i}" for i in m.index], name=x))
    out["quintile_mean_ex5_pct"] = pd.DataFrame(q)
    # range expansion by close direction
    sub = g.dropna(subset=["rr", "r1"]).copy()
    sub["rrhi"] = sub.groupby("coin")["rr"].transform(lambda s: s > s.median())
    out["rr_by_daydir"] = sub.groupby([sub["rrhi"], sub["r1"] > 0, sub["ret20"] > 0])["ex"].agg(lambda s: f"{s.mean()*100:.2f}% t={s.mean()/s.std()*np.sqrt(len(s)):.2f} n={len(s)}")
    out["weekday_ex5"] = g.groupby("wd")["ex"].agg(["mean", "count"])
    out["year_ex5_up20_vs_dn20"] = g.groupby(["yr", g.ret20 > 0])["ex"].mean().unstack()
    out["coin_ex5_up20_minus_dn20"] = g.groupby(["coin", g.ret20 > 0])["ex"].mean().unstack()
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window_mean_pct"] = bk.groupby("win").mean().mul(100).round(3)
    big = bk["book_return"]
    out["book_tail_share"] = pd.Series({
        "sum_all": big.sum(), "sum_top20": big.nlargest(20).sum(), "sum_bot20": big.nsmallest(20).sum(),
        "coin_on_top20": bk.loc[big.nlargest(20).index, "coin_return"].mean(),
        "coin_on_bot20": bk.loc[big.nsmallest(20).index, "coin_return"].mean()})
    return out
