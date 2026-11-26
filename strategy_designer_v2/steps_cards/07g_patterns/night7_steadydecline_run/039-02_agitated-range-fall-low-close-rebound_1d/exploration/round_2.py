def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            allr.append(b["close"].pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l = b["close"], b["high"], b["low"]
            rng = (h - l)
            mr = rng.shift(1).rolling(30, min_periods=20).mean()
            r1 = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": b["timestamp"],
                "r1": r1,
                "fall_rng": (-(c - c.shift(1)) / mr),
                "loc": ((h - c) / rng.replace(0, np.nan)),
                "rng_rel": rng / mr,
                "agit": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
                "nx1": c.shift(-1) / c - 1,
                "nx2": c.shift(-2) / c.shift(-1) - 1,
                "nx3": c.shift(-3) / c - 1,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
            })
            d["ex1"] = d["nx1"] - mu
            d["ex2"] = d["nx2"] - mu
            d["ex3"] = d["nx3"] - 3 * mu
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            d["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def ct(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 5:
            return pd.Series({"n": len(x), "days": np.nan, "mean%": np.nan, "t": np.nan})
        m = x[col].mean()
        g = (x[col] - m).groupby(x["ts"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(x)
        return pd.Series({"n": len(x), "days": x["ts"].nunique(), "mean%": 100 * m, "t": m / se if se > 0 else np.nan})

    def q(s, k):
        return pd.qcut(s.rank(method="first"), k, labels=False)

    out = {}
    def safe(name, f):
        try:
            out[name] = f()
        except Exception as e:
            out[name] = "err: " + str(e)[:80]

    dn = D[(D["r1"] < 0) & D["fall_rng"].notna()].copy()
    dn["fallq"] = q(dn["fall_rng"], 4)
    dn["locq"] = pd.cut(dn["loc"], [-0.01, 0.5, 0.8, 1.01], labels=["mid/high", "nearlow", "atlow"])
    safe("down: agit x fallq(0 small..3 big) x loc, ex1", lambda: dn.groupby(["agit", "fallq", "locq"]).apply(lambda x: ct(x, "ex1")).round(3))
    safe("down big fall (q3): agit x loc, ex2 (day after next)", lambda: dn[dn["fallq"] == 3].groupby(["agit", "locq"]).apply(lambda x: ct(x, "ex2")).round(3))
    up = D[(D["r1"] > 0) & D["fall_rng"].notna()].copy()
    up["riseq"] = q(-up["fall_rng"], 4)
    up["locq"] = pd.cut(up["loc"], [-0.01, 0.2, 0.5, 1.01], labels=["athigh", "nearhigh", "mid/low"])
    safe("up: agit x riseq(0 small..3 big) x loc, ex1", lambda: up.groupby(["agit", "riseq", "locq"]).apply(lambda x: ct(x, "ex1")).round(3))
    sig = D[D["fc"] > 0].copy()
    safe("signal: ex1 ex2 ex3", lambda: pd.DataFrame({k: ct(sig, k) for k in ["ex1", "ex2", "ex3"]}).round(3))
    sig["fcq"] = q(sig["fc"], 4)
    safe("signal by fc quartile ex1", lambda: sig.groupby("fcq").apply(lambda x: ct(x, "ex1")).round(3))
    safe("signal by year ex1", lambda: sig.groupby("yr").apply(lambda x: ct(x, "ex1")).round(3))
    safe("signal by coin ex1", lambda: sig.groupby("coin").apply(lambda x: ct(x, "ex1")).round(3))
    sig["r20q"] = q(sig["r20"].fillna(0), 3)
    safe("signal by 20d return tercile ex1", lambda: sig.groupby("r20q").apply(lambda x: ct(x, "ex1")).round(3))
    safe("weekday x agit ex1", lambda: D.groupby(["agit", "wd"]).apply(lambda x: ct(x, "ex1")).round(3))
    D2 = D.dropna(subset=["r5"]).copy()
    D2["r5q"] = D2.groupby("coin")["r5"].transform(lambda s: q(s, 5))
    safe("5d return quintile x agit, ex1", lambda: D2.groupby(["agit", "r5q"]).apply(lambda x: ct(x, "ex1")).round(3))
    safe("5d return quintile x agit, ex3", lambda: D2.groupby(["agit", "r5q"]).apply(lambda x: ct(x, "ex3")).round(3))
    D3 = D.dropna(subset=["rng_rel"]).copy()
    D3["rq"] = D3.groupby("coin")["rng_rel"].transform(lambda s: q(s, 4))
    safe("day range rel quartile x agit, ex1", lambda: D3.groupby(["agit", "rq"]).apply(lambda x: ct(x, "ex1")).round(3))
    # book daily returns: largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    B = pd.concat(dd, ignore_index=True)
    bk = B.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    def bstats():
        top = bk["book_return"].sort_values()
        n = len(top); k = max(1, n // 20)
        tot = bk["book_return"].sum()
        return pd.Series({"days": n, "mean%": 100 * bk["book_return"].mean(),
                          "share of sum from best 5% days": top.iloc[-k:].sum() / tot,
                          "share of sum from worst 5% days": top.iloc[:k].sum() / tot,
                          "coin ret% on best5% book days": 100 * bk.loc[top.index[-k:], "coin_return"].mean(),
                          "coin ret% on worst5% book days": 100 * bk.loc[top.index[:k], "coin_return"].mean()}).round(4)
    safe("book extremes", bstats)
    safe("book by window", lambda: bk.groupby(level=0)["book_return"].agg(["count", "mean", "std"]).assign(sh=lambda x: x["mean"] / x["std"] * np.sqrt(365)).round(4))
    return out
