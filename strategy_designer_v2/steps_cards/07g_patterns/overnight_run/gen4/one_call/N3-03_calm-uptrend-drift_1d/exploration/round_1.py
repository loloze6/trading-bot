def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = np.log(c).diff()
            vol20 = r1.rolling(20).std()
            vrank = vol20.rolling(100, min_periods=50).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            ret20 = c / c.shift(20) - 1
            ret5p = np.log(c / c.shift(5))
            fwd5 = np.log(c.shift(-5) / c)
            fwd1 = r1.shift(-1)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "fwd5": fwd5, "fwd1": fwd1,
                              "r1": r1, "ret5p": ret5p, "ret20": ret20, "vrank": vrank, "vol20": vol20,
                              "fc": b["forecast"].astype(float), "reg": b["regime"].astype(str),
                              "wd": ts.dt.weekday, "yr": ts.dt.year})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["fwd5x"] = D["fwd5"] - D.groupby("coin")["fwd5"].transform("mean")
    G = D[(D["i"] % 5 == 0)].dropna(subset=["fwd5x"])
    def summ(g, col="fwd5x"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan,
                          "hit": (x > 0).mean()})
    out = {}
    G = G.copy()
    G["fcb"] = pd.cut(G["fc"], [-0.01, 0.0001, 0.5, 1.0, 1.5, 100], labels=["0", "0-.5", ".5-1", "1-1.5", ">1.5"])
    out["fwd5x_by_regime_fcbucket"] = G.groupby(["reg", "fcb"], observed=True).apply(summ)
    G["vb"] = pd.cut(G["vrank"], [0, 0.2, 0.5, 0.8, 1.0], include_lowest=True)
    G["r20s"] = np.where(G["ret20"] > 0, "up20", "dn20")
    out["fwd5x_by_volrank_ret20sign"] = G.groupby(["vb", "r20s"], observed=True).apply(summ)
    G["p5q"] = G.groupby("coin")["ret5p"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["fwd5x_by_prior5_quintile"] = G.groupby("p5q").apply(summ)
    out["fwd5x_by_prior5q_volhalf"] = G.groupby([G["vrank"] <= 0.5, "p5q"]).apply(summ)
    out["fwd5x_by_coin_active"] = G[G["fc"] > 0].groupby("coin").apply(summ)
    out["fwd5x_by_year_active"] = G[G["fc"] > 0].groupby("yr").apply(summ)
    # daily: big moves
    D["r1z"] = D["r1"] / D["vol20"].shift(1)
    D["zb"] = pd.cut(D["r1z"], [-99, -2.5, -1.5, 1.5, 2.5, 99])
    out["fwd1_by_prior_day_z"] = D.dropna(subset=["fwd1"]).groupby("zb", observed=True).apply(lambda g: summ(g, "fwd1"))
    D["fwd1x"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    out["fwd1x_by_weekday"] = D.dropna(subset=["fwd1x"]).groupby("wd").apply(lambda g: summ(g, "fwd1x"))
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["db"] = pd.cut(T["dur_d"], [0, 1.5, 3.5, 7.5, 15, 1000])
    out["trades_by_duration"] = T.groupby("db", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median", lambda x: (x > 0).mean(), "sum"])
    T["efb"] = pd.qcut(T["entry_forecast"], 4, duplicates="drop")
    out["trades_by_entry_forecast"] = T.groupby("efb", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median", lambda x: (x > 0).mean()])
    out["trades_overall"] = T["net_profit_loss_percent"].describe()
    # book largest days
    Ds = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; Ds.append(d)
    Ds = pd.concat(Ds, ignore_index=True).dropna(subset=["book_return"])
    inpos = Ds[Ds["book_return"].abs() > 1e-9]
    q = inpos["book_return"].quantile([0.01, 0.05, 0.95, 0.99])
    out["book_ret_tails"] = q
    out["book_share_pnl_top_bottom_5pct"] = pd.Series({
        "sum_all": inpos["book_return"].sum(),
        "sum_top5": inpos[inpos["book_return"] >= q[0.95]]["book_return"].sum(),
        "sum_bot5": inpos[inpos["book_return"] <= q[0.05]]["book_return"].sum(),
        "n_inpos": len(inpos)})
    return out
