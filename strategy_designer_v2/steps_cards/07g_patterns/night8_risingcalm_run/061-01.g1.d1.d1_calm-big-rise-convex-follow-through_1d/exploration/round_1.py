def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std().shift(1)
            z = r / sd30
            tr60 = c / c.shift(60) - 1
            tr20 = c / c.shift(20) - 1
            rng = (b["high"] - b["low"]).astype(float)
            clv = ((c - b["low"]) / rng).where(rng > 0)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r": r, "z": z,
                               "sd30": r.rolling(30, min_periods=20).std(), "tr60": tr60, "tr20": tr20,
                               "clv": clv, "wd": ts.dt.weekday, "alloc": b["postRebalance_current_allocation"].astype(float),
                               "regime": b["regime"]})
            for h in (1, 3, 5, 10):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["sdmed"] = D.groupby("coin")["sd30"].transform("median")
    D["agit"] = np.where(D["sd30"] > D["sdmed"], "agit", "calm")
    D["trend"] = pd.cut(D["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    out = {}

    def grid(h):
        g = D[(D["pos"] % h) == 0].dropna(subset=[f"f{h}"]).copy()
        g["ex"] = g[f"f{h}"] - g.groupby("coin")[f"f{h}"].transform("mean")
        return g

    def summ(g, by):
        def f(x):
            n = len(x); m = x.mean(); s = x.std()
            return pd.Series({"n": n, "mean%": 100 * m, "t": m / (s / np.sqrt(n)) if n > 2 and s > 0 else np.nan})
        return g.groupby(by, observed=True)["ex"].apply(f).unstack()

    zb = [-np.inf, -2, -1, -0.5, 0.5, 1, 2, np.inf]
    for h in (1, 5):
        g = grid(h); g["zb"] = pd.cut(g["z"], zb)
        out[f"z bins fwd{h}"] = summ(g, "zb")
        out[f"z bins x agit fwd{h}"] = summ(g, ["agit", "zb"])
    g = grid(5); g["zb"] = pd.cut(g["z"], [-np.inf, -1, 1, np.inf])
    out["z3 x trend fwd5"] = summ(g.dropna(subset=["trend"]), ["trend", "zb"])
    g = grid(1); g["cb"] = pd.cut(g["clv"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    out["close location fwd1"] = summ(g, "cb")
    g = grid(3); g["cb"] = pd.cut(g["clv"], [0, .2, .8, 1.0001], include_lowest=True)
    out["close location x agit fwd3"] = summ(g, ["agit", "cb"])
    g = grid(10); g["t20"] = pd.qcut(g["tr20"], 5)
    out["20d return quintile fwd10"] = summ(g.dropna(subset=["t20"]), "t20")
    g = grid(1)
    out["weekday fwd1"] = summ(g, "wd")
    g = grid(5); g["vq"] = g.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["vol tercile fwd5"] = summ(g.dropna(subset=["vq"]), "vq")
    # book: largest gains/losses by window
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    Dd = pd.concat(dd)
    book = Dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book by window"] = book.groupby("w").agg(["mean", "count"]) * [100, 1, 100, 1]
    out["book days nonzero share"] = float((book["book_return"].abs() > 1e-9).mean())
    return out
