def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        grid_all = []
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            n = len(b)
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            r1 = c.pct_change()
            past5 = c / c.shift(5) - 1
            past20 = c / c.shift(20) - 1
            vol20 = r1.rolling(20, min_periods=10).std()
            lo60 = c.rolling(60, min_periods=20).min()
            hi60 = c.rolling(60, min_periods=20).max()
            rng = (c - lo60) / (hi60 - lo60)
            rawp = b.get("debug_info.components.high_prox.last_history_value")
            fc = b["debug_info.components.high_prox.post_pipeline_value"]
            pos = b["postRebalance_current_allocation"]
            range_hl = (b["high"] - b["low"]) / c
            ts = pd.to_datetime(b["timestamp"])
            g = pd.DataFrame({"coin": coin, "win": w, "fwd5": fwd5, "past5": past5, "past20": past20,
                              "vol20": vol20, "rng": rng, "rawp": rawp, "fc": fc, "pos": pos,
                              "dayrange": range_hl, "wd": ts.dt.weekday, "year": ts.dt.year})
            grid_all.append(g.iloc[::5])
            d = pd.DataFrame({"coin": coin, "win": w, "fwd1": fwd1, "r1": r1, "wd": ts.dt.weekday,
                              "absr1": r1.abs(), "vol20": vol20, "pos": pos, "year": ts.dt.year})
            daily.append(d)
        G = pd.concat(grid_all)
        G["ex5"] = G["fwd5"] - G["fwd5"].mean()
        G["volrel"] = G["vol20"] / G["vol20"].median()
        rows.append(G)
    G = pd.concat(rows).dropna(subset=["ex5"])
    D = pd.concat(daily)
    D["ex1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    def tab(df, col, q=5):
        x = df.dropna(subset=[col, "ex5"]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        a = x.groupby("q")["ex5"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.round(4)
    out = {}
    out["fc_quint"] = tab(G, "fc")
    out["rawprox_quint"] = tab(G, "rawp")
    out["past5_quint"] = tab(G, "past5")
    out["past20_quint"] = tab(G, "past20")
    out["vol_quint"] = tab(G, "volrel")
    out["range60_quint"] = tab(G, "rng")
    out["dayrange_quint"] = tab(G, "dayrange")
    # interaction: rawp quintile x vol tercile
    x = G.dropna(subset=["rawp", "volrel"]).copy()
    x["pq"] = x.groupby("coin")["rawp"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    x["vq"] = x.groupby("coin")["volrel"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["prox_x_vol"] = x.groupby(["vq", "pq"])["ex5"].agg(["mean", "count"]).round(4)
    out["prox_by_coin_corr"] = G.dropna(subset=["fc"]).groupby("coin").apply(
        lambda s: pd.Series({"r": stats.spearmanr(s["fc"], s["ex5"])[0], "n": len(s)})).round(3)
    out["prox_by_year"] = G.dropna(subset=["fc"]).groupby("year").apply(
        lambda s: pd.Series({"r": stats.spearmanr(s["fc"], s["ex5"])[0], "n": len(s), "ex5": s["ex5"].mean()})).round(3)
    a = D.dropna(subset=["ex1"]).groupby("wd")["ex1"].agg(["mean", "count", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["weekday_next1"] = a.round(5)
    # large-move reversal daily
    y = D.dropna(subset=["ex1", "r1", "vol20"]).copy()
    y["z"] = y["r1"] / y["vol20"]
    y["zq"] = pd.cut(y["z"], [-99, -2, -1, 1, 2, 99])
    a = y.groupby("zq")["ex1"].agg(["mean", "count", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["after_zmove_next1"] = a.round(5)
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d[["book_return", "coin_return"]].copy(); dd["coin"] = coin; dd["win"] = w
            dd["i"] = range(len(dd)); bd.append(dd)
    B = pd.concat(bd)
    bw = B.groupby(["win", "i"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bw.groupby("win").agg(book=("book_return", "sum"), coin=("coin_return", "sum")).round(3)
    lo = bw["book_return"].quantile(0.02); hi = bw["book_return"].quantile(0.98)
    out["book_extremes"] = pd.Series({"q02": lo, "q98": hi,
        "share_gain_top2pct": bw["book_return"][bw["book_return"] >= hi].sum() / bw["book_return"].sum(),
        "share_loss_bot2pct": bw["book_return"][bw["book_return"] <= lo].sum() / bw["book_return"].sum(),
        "corr_book_coin": bw["book_return"].corr(bw["coin_return"])}).round(4)
    return out
