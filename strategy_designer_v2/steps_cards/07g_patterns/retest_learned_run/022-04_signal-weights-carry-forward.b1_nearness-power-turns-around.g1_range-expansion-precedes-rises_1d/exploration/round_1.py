def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = (h - l) / c
            b["rr"] = (h - l) / (h - l).rolling(30, min_periods=10).mean()
            b["clv"] = (c - l) / (h - l).replace(0, np.nan)
            b["r1"] = c.pct_change()
            b["r5p"] = c / c.shift(5) - 1
            b["r20p"] = c / c.shift(20) - 1
            b["vol20"] = b["r1"].rolling(20, min_periods=10).std()
            b["volrel"] = b["vol20"] / b["r1"].rolling(60, min_periods=20).std()
            b["fwd5"] = c.shift(-5) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            g = b.iloc[::5].copy()
            g["coin"] = coin; g["win"] = w
            rows.append(g)
    G = pd.concat(rows).dropna(subset=["fwd5"])
    G["drift"] = G.groupby("coin")["fwd5"].transform("mean")
    G["ex"] = G["fwd5"] - G["drift"]
    out = {}
    feats = ["forecast", "rr", "clv", "r1", "r5p", "r20p", "vol20", "volrel"]
    res = []
    for f in feats:
        d = G[[f, "ex"]].dropna()
        s = stats.linregress(d[f], d["ex"])
        res.append({"feat": f, "n": len(d), "slope": s.slope, "t": s.slope / s.stderr,
                    "spearman": stats.spearmanr(d[f], d["ex"])[0]})
    out["single_feature_t"] = pd.DataFrame(res)
    def quint(f, q=5):
        d = G[[f, "ex"]].dropna().copy()
        d["q"] = pd.qcut(d[f], q, labels=False, duplicates="drop")
        a = d.groupby("q")["ex"].agg(["count", "mean", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["fmean"] = d.groupby("q")[f].mean()
        return a
    for f in ["rr", "clv", "r1", "r20p", "volrel"]:
        out["q_" + f] = quint(f)
    # interaction: wide range split by direction of day
    d = G.dropna(subset=["rr", "r1", "clv"]).copy()
    d["rrq"] = pd.qcut(d["rr"], 3, labels=["narrow", "mid", "wide"])
    d["dir"] = np.where(d["r1"] > 0, "up", "down")
    a = d.groupby(["rrq", "dir"])["ex"].agg(["count", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["rr_by_daydir"] = a
    d["clvq"] = pd.qcut(d["clv"], 3, labels=["nearlow", "mid", "nearhigh"])
    a = d.groupby(["rrq", "clvq"])["ex"].agg(["count", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["rr_by_clv"] = a
    d["trend"] = np.where(d["r20p"] > 0, "up20", "down20")
    a = d.dropna(subset=["r20p"]).groupby(["rrq", "trend"])["ex"].agg(["count", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["rr_by_trend20"] = a
    # by coin and year slope t of rr
    def slope_t(x):
        x = x.dropna(subset=["rr", "ex"])
        if len(x) < 20: return np.nan
        s = stats.linregress(x["rr"], x["ex"]); return s.slope / s.stderr
    out["rr_t_by_coin"] = G.groupby("coin").apply(slope_t)
    out["rr_t_by_year"] = G.groupby("year").apply(slope_t)
    # weekday on daily bars (all bars, 1-day fwd)
    allb = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy(); c = b["close"]
            b["fwd1"] = c.shift(-1) / c - 1
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["coin"] = coin
            allb.append(b[["fwd1", "wd", "coin"]])
    A = pd.concat(allb).dropna()
    a = A.groupby("wd")["fwd1"].agg(["count", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
    out["next_day_by_weekday_of_bar"] = a
    # book days: largest gains/losses
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w; D.append(x)
    D = pd.concat(D).dropna(subset=["book_return"])
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean()
    out["book_corr_coin"] = float(bk["book_return"].corr(bk["coin_return"]))
    top = bk["book_return"].quantile([0.01, 0.99])
    out["book_tails_coinret"] = pd.DataFrame({
        "worst1pct_coin_mean": [bk.loc[bk.book_return <= top.iloc[0], "coin_return"].mean()],
        "best1pct_coin_mean": [bk.loc[bk.book_return >= top.iloc[1], "coin_return"].mean()],
        "share_book_from_top1pct": [bk.loc[bk.book_return >= top.iloc[1], "book_return"].sum() / bk["book_return"].sum()]})
    # positions
    P = pd.concat([b.assign(coin=c) for c, ws in data["bars"].items() for b in ws.values()])
    out["alloc_stats"] = P["postRebalance_current_allocation"].describe()
    out["share_short"] = float((P["postRebalance_current_allocation"] < 0).mean())
    return out
