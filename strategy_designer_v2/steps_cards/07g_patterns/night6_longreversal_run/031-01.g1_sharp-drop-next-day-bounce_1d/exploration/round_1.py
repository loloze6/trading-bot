def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "r": r, "z": r / vol, "vol": vol,
                "nxt": c.shift(-1) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "ret60": c / c.shift(60) - 1,
                "ret5": c / c.shift(5) - 1,
                "rng": (b["high"] - b["low"]) / c,
                "clpos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "pos": np.arange(len(b)),
            })
            df["vol60z"] = (df["ret60"] / (vol * np.sqrt(60)))
            df["fwd20"] = c.shift(-20) / c - 1
            df["fwd5"] = c.shift(-5) / c - 1
            df["volrank"] = vol / vol.rolling(365, min_periods=60).median()
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["day"] = d["ts"].dt.floor("D")

    def clt(sub, col="ex"):
        s = sub.dropna(subset=[col])
        g = s.groupby("day")[col].sum()
        n = len(s)
        if n < 5: return (np.nan, np.nan, n)
        m = s[col].mean()
        se = np.sqrt((g - g.mean() * 0 - m * s.groupby("day")[col].count()).pow(2).sum()) / n
        return (m, m / se if se > 0 else np.nan, n)

    def table(key, col="ex"):
        res = []
        for k, sub in d.groupby(key, observed=True):
            m, t, n = clt(sub, col)
            res.append({"grp": str(k), "mean%": m * 100, "t": t, "n": n})
        return pd.DataFrame(res)

    d["zbin"] = pd.cut(d["z"], [-np.inf, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, np.inf])
    out["next-day excess by today's z"] = table("zbin")
    d["vbin"] = pd.qcut(d["volrank"], 4)
    out["next-day excess by vol level (vol/1y median)"] = table("vbin")
    d["wd"] = d["ts"].dt.weekday
    out["next-day excess by weekday of signal bar"] = table("wd")
    d["cbin"] = pd.qcut(d["clpos"], 5)
    out["next-day excess by close position in range"] = table("cbin")
    d["r5bin"] = pd.qcut(d["ret5"] / (d["vol"] * np.sqrt(5)), 5)
    out["next-day excess by 5d return z"] = table("r5bin")
    # brief's own theory: 60d move, next 20d, non-overlapping grid
    g20 = d[d["pos"] % 20 == 0].copy()
    g20["ex20"] = g20["fwd20"] - g20["coin"].map(drift) * 20
    g20["b60"] = pd.qcut(g20["vol60z"], 5)
    res = []
    for k, sub in g20.groupby("b60", observed=True):
        s = sub["ex20"].dropna()
        res.append({"grp": str(k), "mean%": s.mean() * 100, "t": s.mean() / (s.std() / np.sqrt(len(s))), "n": len(s)})
    out["next-20d excess by 60d move z (grid 20)"] = pd.DataFrame(res)
    # down-day size interacting with vol regime
    dn = d[d["z"] < 0].copy()
    res = []
    for k, sub in dn.groupby("vbin", observed=True):
        s = sub.dropna(subset=["ex", "z"])
        sl = stats.linregress(-s["z"], s["ex"])
        res.append({"vol": str(k), "slope%": sl.slope * 100, "t": sl.slope / sl.stderr, "n": len(s)})
    out["down days: slope of next excess on fall size, by vol"] = pd.DataFrame(res)
    # up-day continuation/reversal slope
    up = d[d["z"] > 0].dropna(subset=["ex", "z"])
    sl = stats.linregress(up["z"], up["ex"])
    out["up days: slope next excess on z (%/z, t, n)"] = f"{sl.slope*100:.3f}, {sl.slope/sl.stderr:.2f}, {len(up)}"
    # book: days
    dr = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dr.append(x)
    dd = pd.concat(dr)
    book = dd.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    book["wd"] = pd.to_datetime(book.index.get_level_values("day")).weekday
    out["book daily by weekday"] = book.groupby("wd")["book_return"].agg(["mean", "count"]).assign(mean=lambda x: x["mean"] * 100)
    q = book["book_return"].quantile([0.02, 0.98])
    out["coin ret on book worst 2%/best 2% days, %"] = pd.DataFrame({
        "worst": [book.loc[book.book_return <= q.iloc[0], "coin_return"].mean() * 100],
        "best": [book.loc[book.book_return >= q.iloc[1], "coin_return"].mean() * 100]})
    out["year book mean% "] = book.groupby(pd.to_datetime(book.index.get_level_values("day")).year)["book_return"].mean() * 100
    return out
