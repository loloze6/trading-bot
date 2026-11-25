def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "ret1": c.shift(-1) / c - 1,
                "ret3": c.shift(-3) / c - 1,
                "r0": c / c.shift(1) - 1,
                "r5": c / c.shift(5) - 1,
                "clv": (c - l) / rng.replace(0, np.nan),
                "rm": rng / rng.shift(1).rolling(30, min_periods=20).mean(),
                "body": (c - o) / rng.replace(0, np.nan),
                "vol30": (c / c.shift(1) - 1).rolling(30, min_periods=20).std(),
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "pos": np.arange(len(b)),
            })
            d["gain"] = d["alloc"] * d["ret1"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["ret1"].mean()
    D["ex1"] = D["ret1"] - D["coin"].map(mu)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.dayofweek
    D["yr"] = D["ts"].dt.year
    out = {}
    def tday(s, dd):
        x = pd.DataFrame({"v": s, "d": dd}).dropna().groupby("d")["v"].sum()
        n = len(x); 
        return x.mean() / (x.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
    E = D.dropna(subset=["ex1", "clv", "rm"]).copy()
    E["clvq"] = pd.qcut(E["clv"], 5, labels=False)
    E["rmq"] = pd.qcut(E["rm"], 3, labels=["narrow", "mid", "wide"])
    g = E.groupby(["rmq", "clvq"], observed=True)["ex1"]
    out["ex1 mean % by width tercile x clv quintile"] = (g.mean() * 100).unstack().round(3)
    out["count"] = g.count().unstack()
    tt = {}
    for (a, q), s in E.groupby(["rmq", "clvq"], observed=True):
        tt[(a, q)] = tday(s["ex1"], s["day"])
    out["t (day-clustered) by width x clv"] = pd.Series(tt).unstack().round(2)
    # slope of ex1 on signed (0.5-clv)*rm, per year and per coin
    E["sig"] = (0.5 - E["clv"]) * E["rm"]
    res = {}
    for k, s in list(E.groupby("coin")) + list(E.groupby("yr")):
        sl = stats.linregress(s["sig"], s["ex1"])
        res[k] = (sl.slope * 100, sl.slope / sl.stderr, len(s))
    out["slope ex1 on (0.5-clv)*rm by coin/year (slope%, t, n)"] = pd.DataFrame(res, index=["slope%", "t", "n"]).T.round(3)
    # previous-day return terciles and ex1
    E["r0q"] = pd.qcut(E["r0"], 5, labels=False)
    out["ex1 % by today's return quintile"] = (E.groupby("r0q")["ex1"].agg(["mean", "count"]).assign(mean=lambda x: x["mean"] * 100)).round(3)
    E["r5q"] = pd.qcut(E["r5"], 5, labels=False)
    out["ex1 % by 5d return quintile"] = (E.groupby("r5q")["ex1"].agg(["mean", "count"]).assign(mean=lambda x: x["mean"] * 100)).round(3)
    E["bq"] = pd.qcut(E["body"], 5, labels=False)
    out["ex1 % by body/range quintile x width"] = (E.groupby(["rmq", "bq"], observed=True)["ex1"].mean() * 100).unstack().round(3)
    out["ex1 % by weekday"] = (E.groupby("wd")["ex1"].agg(["mean", "count"]).assign(mean=lambda x: x["mean"] * 100)).round(3)
    E["vq"] = E.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["ex1 % by vol tercile x clv quintile"] = (E.groupby(["vq", "clvq"])["ex1"].mean() * 100).unstack().round(3)
    # book: gain by forecast quintile
    F = D.dropna(subset=["gain"])
    out["mean gain % by forecast bucket"] = (F.groupby(pd.qcut(F["fc"].rank(method="first"), 5, labels=False))[["gain", "fc", "alloc"]].mean().assign(gain=lambda x: x["gain"] * 100)).round(3)
    return out
