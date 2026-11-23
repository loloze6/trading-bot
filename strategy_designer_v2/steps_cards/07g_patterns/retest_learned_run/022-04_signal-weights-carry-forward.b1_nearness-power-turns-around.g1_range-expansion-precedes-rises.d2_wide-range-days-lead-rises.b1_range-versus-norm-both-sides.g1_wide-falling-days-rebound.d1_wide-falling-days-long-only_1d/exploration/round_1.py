def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l = b["close"], b["high"], b["low"]
            rng = h - l
            f = pd.DataFrame({"coin": coin, "win": w})
            f["r1"] = c / c.shift(1) - 1
            f["rx"] = rng / rng.rolling(30, min_periods=30).mean() - 1
            f["clv"] = (c - l) / rng.replace(0, np.nan)
            f["r7"] = c / c.shift(7) - 1
            f["r30"] = c / c.shift(30) - 1
            f["vol20"] = f["r1"].rolling(20, min_periods=20).std()
            f["nearhi"] = c / h.rolling(30, min_periods=30).max() - 1
            f["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            f["fwd3"] = c.shift(-3) / c - 1
            f["fwd1"] = c.shift(-1) / c - 1
            f["alloc"] = b["postRebalance_current_allocation"]
            f["fc"] = b["forecast"]
            f["pos"] = np.arange(len(b))
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    g = df[df["pos"] % 3 == 0].dropna(subset=["fwd3"]).copy()
    g["drift"] = g.groupby("coin")["fwd3"].transform("mean")
    g["u"] = g["fwd3"] - g["drift"]
    def tab(col, q=5, sub=None):
        d = (sub if sub is not None else g).dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = d.groupby("q")["u"].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["feat_mean"] = d.groupby("q")[col].mean()
        return r[["feat_mean", "mean", "t", "count"]].round(4)
    out = {}
    for col in ["r1", "rx", "clv", "r7", "r30", "vol20", "nearhi"]:
        out["q5 " + col] = tab(col)
    out["q5 rx on up days"] = tab("rx", sub=g[g["r1"] > 0])
    out["q5 rx on down days"] = tab("rx", sub=g[g["r1"] < 0])
    out["q5 clv on down days"] = tab("clv", sub=g[g["r1"] < 0])
    wd = g.groupby("wd")["u"].agg(["mean", "count", "std"]); wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["weekday"] = wd.round(4)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["win"] = w; x["coin"] = coin; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["year"] = pd.to_datetime(bk["day"]).dt.year
    yr = bk.groupby("year").agg(book_mean=("book_return", "mean"), book_sd=("book_return", "std"), coin_mean=("coin_return", "mean"), n=("book_return", "count"))
    yr["book_sharpe"] = yr.book_mean / yr.book_sd * np.sqrt(365)
    out["book by year"] = yr.round(5)
    wn = bk.groupby("win")["book_return"].agg(["mean", "std", "min", "max", "count"])
    out["book by window"] = wn.round(5)
    return out
