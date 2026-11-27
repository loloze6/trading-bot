def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).astype(float)
            b["loc"] = np.where(rng > 0, (c - b["low"]) / rng, np.nan)
            b["r1"] = c.pct_change()
            b["r5p"] = c / c.shift(5) - 1
            b["r20p"] = c / c.shift(20) - 1
            b["vol20"] = b["r1"].rolling(20).std()
            b["z5"] = b["r5p"] / (b["vol20"] * np.sqrt(5))
            b["z1"] = b["r1"] / b["vol20"]
            for h in (1, 2, 5):
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["inprof"] = b["regime"] != "chop"
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            b["volrank"] = b["vol20"].rank(pct=True)
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    # coin mean drift over all windows
    out = {}
    def grid(df, h):
        return df[df["pos"] % h == 0]
    for h in (2, 5):
        g = grid(d, h).dropna(subset=[f"f{h}"]).copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["u"] = g[f"f{h}"] - g["coin"].map(drift)
        g["locb"] = pd.cut(g["loc"], [-.01, .2, .4, .6, .8, 1.01])
        def summ(x):
            return pd.Series({"n": len(x), "mean_u": x["u"].mean(), "t": x["u"].mean() / (x["u"].std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
        out[f"h{h} by loc x inprof"] = g.groupby(["inprof", "locb"]).apply(summ)
        g["z5b"] = pd.qcut(g["z5"], 5)
        out[f"h{h} by z5 x inprof"] = g.groupby(["inprof", "z5b"]).apply(summ)
        g["z1b"] = pd.qcut(g["z1"], 5)
        out[f"h{h} by z1 all"] = g.groupby("z1b").apply(summ)
        if h == 2:
            out["h2 by weekday"] = g.groupby("wd").apply(summ)
            g["vb"] = pd.qcut(g["volrank"], 3)
            out["h2 by volrank x loc>0.8"] = g.groupby(["vb", g["loc"] > 0.8]).apply(summ)
    # regime counts
    out["regime counts"] = d["regime"].value_counts()
    # book daily returns by weekday and big days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["book by window"] = dd.groupby("win")["book_return"].agg(["mean", "std", "count"])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, x in wins.items():
            if len(x):
                x = x.copy(); x["coin"] = coin; x["win"] = w; tr.append(x)
    tr = pd.concat(tr)
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    tr["fq"] = pd.qcut(tr["entry_forecast"].abs().rank(method="first"), 3, labels=["low", "mid", "high"])
    out["trades by |forecast| third"] = tr.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
