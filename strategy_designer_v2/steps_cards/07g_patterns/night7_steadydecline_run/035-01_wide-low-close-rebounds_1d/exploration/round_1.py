def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            d["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            d["coin"] = coin; d["win"] = w
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            rng = h - l
            d["width"] = rng / rng.shift(1).rolling(14).mean()
            d["clv"] = ((c - l) / rng.replace(0, np.nan))
            d["ret0"] = c / c.shift(1) - 1
            d["r1"] = c.shift(-1) / c - 1
            d["r2"] = c.shift(-2) / c.shift(-1) - 1
            d["r3"] = c.shift(-3) / c - 1
            d["tr60"] = c / c.shift(60) - 1
            d["vol30"] = d["ret0"].rolling(30).std()
            d["fc"] = b["debug_info.components.wide_low_close.post_pipeline_value"]
            d["pos"] = b["postRebalance_current_allocation"]
            d["pos3"] = (np.arange(len(b)) % 3 == 0)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["r1"].transform("mean")
    mu3 = D[D.pos3].groupby("coin")["r3"].mean()
    D["x1"] = D["r1"] - mu1
    D["x2"] = D["r2"] - mu1
    D["x3"] = D["r3"] - D["coin"].map(mu3)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    D["volq"] = D.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    D["trend"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])

    def tab(df, keys, col="x1"):
        df = df.dropna(subset=[col] + keys)
        out = []
        for k, g in df.groupby(keys, observed=True):
            dev = g.groupby("day")[col].sum()
            n = len(g); m = g[col].mean()
            dd = (g[col] - m).groupby(g["day"]).sum()
            se = np.sqrt((dd ** 2).sum()) / n if n > 1 else np.nan
            out.append({"key": str(k), "n": n, "days": g["day"].nunique(), "mean%": 100 * m, "t": m / se if se else np.nan})
        return pd.DataFrame(out)

    D["wq"] = D.groupby("coin")["width"].transform(lambda s: pd.qcut(s, 3, labels=["narrow", "mid", "wide"]))
    D["cq"] = pd.cut(D["clv"], [-0.01, 0.2, 0.8, 1.01], labels=["nearlow", "middle", "nearhigh"])
    D["fq"] = D.groupby("coin")["fc"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    D["r0q"] = D.groupby("coin")["ret0"].transform(lambda s: pd.qcut(s, 5, labels=False))
    res = {}
    res["width x close-loc -> next day"] = tab(D, ["wq", "cq"])
    res["width x close-loc -> day after next"] = tab(D, ["wq", "cq"], "x2")
    res["forecast quintile -> next day"] = tab(D, ["fq"])
    res["past-day return quintile -> next day"] = tab(D, ["r0q"])
    res["past-day ret quintile x width -> next"] = tab(D, ["r0q", "wq"])
    res["trend x close-loc(nearlow, wide) -> next"] = tab(D[(D.wq == "wide")], ["trend", "cq"])
    res["vol tercile x top fc quintile"] = tab(D[D.fq == 4], ["volq"])
    res["weekday -> next day all"] = tab(D, ["wd"])
    res["3-day: width x closeloc (grid)"] = tab(D[D.pos3], ["wq", "cq"], "x3")
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w; bk.append(x)
    B = pd.concat(bk)
    bd = B.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    bd["wd"] = pd.to_datetime(bd.index.get_level_values("day")).dayofweek
    res["book by weekday"] = bd.groupby("wd").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    res["book by window"] = bd.groupby(level="win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), bsd=("book_return", "std"))
    q = bd["book_return"].quantile([0.05, 0.95])
    bd["cls"] = np.where(bd.book_return <= q.iloc[0], "worst5", np.where(bd.book_return >= q.iloc[1], "best5", "mid"))
    res["book extremes: coin ret same day"] = bd.groupby("cls")[["book_return", "coin_return"]].mean()
    return res
