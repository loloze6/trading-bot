def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    drows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std()
            hi5 = c.rolling(5, min_periods=5).max()
            lo5 = c.rolling(5, min_periods=5).min()
            dip = (c - hi5) / hi5 / sd30
            pop = (c - lo5) / lo5 / sd30
            ret5p = c / c.shift(5) - 1
            tr60 = c / c.shift(60) - 1
            sd_med = sd30.expanding(min_periods=30).median()
            agit = (sd30 > sd_med).astype(float).where(sd30.notna() & sd_med.notna())
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            n = len(b)
            idx = np.arange(0, n, 5)
            g = pd.DataFrame({
                "coin": coin, "win": w,
                "regime": b["regime"].values[idx],
                "dip": dip.values[idx], "pop": pop.values[idx],
                "r5p_s": (ret5p / (sd30 * np.sqrt(5))).values[idx],
                "r1_s": (r1 / sd30).values[idx],
                "tr60": tr60.values[idx], "agit": agit.values[idx],
                "fc": b["forecast"].values[idx],
                "f5": f5.values[idx],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values[idx],
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values[idx],
            })
            rows.append(g)
            dd = pd.DataFrame({"coin": coin, "r1": r1, "f1": f1, "r1s": r1 / sd30,
                               "regime": b["regime"], "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "alloc": b["postRebalance_current_allocation"]})
            drows.append(dd)
    G = pd.concat(rows, ignore_index=True)
    G = G[G["f5"].notna()]
    G["ex5"] = G["f5"] - G.groupby("coin")["f5"].transform("mean")
    D = pd.concat(drows, ignore_index=True)
    D = D[D["f1"].notna()]
    D["ex1"] = D["f1"] - D.groupby("coin")["f1"].transform("mean")

    def summ(df, col, key):
        a = df.groupby(key)[col].agg(["count", "mean", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a

    G["rc"] = np.where(G["regime"] == "unknown", "risingcalm", "other")
    out["by regime ex5"] = summ(G, "ex5", "rc")
    G["dipq"] = G.groupby("rc")["dip"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["ex5 by regime x dip quintile"] = summ(G.dropna(subset=["dipq"]), "ex5", ["rc", "dipq"])
    G["trc"] = pd.cut(G["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    G["prof"] = G["trc"].astype(str) + "_" + G["agit"].map({1.0: "ag", 0.0: "calm"}).astype(str)
    out["ex5 by computed profile"] = summ(G, "ex5", "prof")
    # rank corr dip vs ex5 per profile (dip negative=deeper)
    cr = {}
    for p, s in G.dropna(subset=["dip"]).groupby("prof"):
        if len(s) > 30:
            rr = stats.spearmanr(-s["dip"], s["ex5"])
            cr[p] = (len(s), rr.correlation, rr.pvalue)
    out["spearman depth vs ex5 by profile"] = pd.DataFrame(cr, index=["n", "rho", "p"]).T
    # past 5-day scaled return quintiles -> ex5 overall
    G["r5q"] = pd.qcut(G["r5p_s"].rank(method="first"), 5, labels=False)
    out["ex5 by past5 scaled ret quintile"] = summ(G.dropna(subset=["r5q"]), "ex5", "r5q")
    G["popq"] = pd.qcut(G["pop"].rank(method="first"), 5, labels=False)
    out["ex5 by height above 5d low quintile"] = summ(G.dropna(subset=["popq"]), "ex5", "popq")
    # 1-day scaled move deciles -> next day
    D["r1q"] = pd.qcut(D["r1s"].rank(method="first"), 10, labels=False)
    out["next-day ex by 1d scaled move decile"] = summ(D.dropna(subset=["r1q"]), "ex1", "r1q")
    out["next-day ex by weekday"] = summ(D, "ex1", "wd")
    # book days
    Bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            Bd.append(d.assign(coin=coin, win=w))
    Bd = pd.concat(Bd)
    bk = Bd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk["wd"] = pd.to_datetime(bk.index.get_level_values("day")).weekday
    out["book by window"] = bk.groupby(level="win")[["book_return", "coin_return"]].agg(["mean", "count"])
    top = bk["book_return"].abs().nlargest(20).index
    out["largest 20 abs book days: mean book, coin, share neg"] = pd.Series({
        "mean_book": bk.loc[top, "book_return"].mean(), "mean_coin": bk.loc[top, "coin_return"].mean(),
        "share_neg": (bk.loc[top, "book_return"] < 0).mean()})
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["fcq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades by entry forecast quartile"] = T.groupby("fcq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
