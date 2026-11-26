def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "inprof": b["regime"].astype(str) != "chop",
                "regime": b["regime"].astype(str),
                "z1": r / sd,
                "z4": (c.shift(1) / c.shift(5) - 1) / sd,
                "z3": (c / c.shift(3) - 1) / sd,
                "rng": (b["high"] - b["low"]) / c / sd,
                "clo": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "usd": sd,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": b["postRebalance_current_allocation"].astype(float),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            })
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["f1"].mean()
    D["u1"] = D["f1"] - D["coin"].map(drift)
    D["u1s"] = D["u1"] / D["usd"]
    out = {}
    out["share in profile"] = float(D["inprof"].mean())
    out["regime counts"] = D["regime"].value_counts()

    def summ(g, col="u1"):
        x = g[col].dropna()
        if len(x) < 5:
            return pd.Series({"n": len(x)})
        dd = g.dropna(subset=[col]).groupby("day")[col].sum()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))),
                          "t_day": dd.mean() / (dd.std() / np.sqrt(len(dd))) if len(dd) > 2 else np.nan})

    P = D[D["inprof"]].copy()
    O = D[~D["inprof"]].copy()
    bins = [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf]
    P["z1b"] = pd.cut(P["z1"], bins)
    O["z1b"] = pd.cut(O["z1"], bins)
    out["in-profile next-day unusual by today z"] = P.groupby("z1b", observed=True).apply(summ)
    out["out-profile next-day unusual by today z"] = O.groupby("z1b", observed=True).apply(summ)
    P["z3b"] = pd.cut(P["z3"], [-np.inf, -3, -1.5, 0, 1.5, 3, np.inf])
    P["u3"] = P["f3"] - P["coin"].map(drift) * 3
    out["in-profile 3-day unusual by 3-day z (overlapping)"] = P.groupby("z3b", observed=True).apply(lambda g: summ(g, "u3"))
    P["rngb"] = pd.qcut(P["rng"], 4, duplicates="drop")
    out["in-profile next-day by range quartile"] = P.groupby("rngb", observed=True).apply(summ)
    P["clob"] = pd.cut(P["clo"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    out["in-profile next-day by close location"] = P.groupby("clob", observed=True).apply(summ)
    out["in-profile next-day by weekday"] = P.groupby("wd").apply(summ)
    out["all bars next-day by weekday"] = D.groupby("wd").apply(summ)
    A = P[P["regime"] == "mean_reversion"].copy()
    A["z4b"] = pd.qcut(A["z4"], 4, duplicates="drop")
    out["active: next-day unusual (long sign) by prior 4d z quartile"] = A.groupby("z4b", observed=True).apply(summ)
    A["z1q"] = pd.qcut(A["z1"], 3)
    out["active: by today z tercile"] = A.groupby("z1q", observed=True).apply(summ)
    out["active by window"] = A.groupby("win").apply(summ)
    # book day returns
    bd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            bd.append(d.assign(coin=coin, win=w))
    BD = pd.concat(bd)
    bk = BD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book daily: mean, sd, n, skew"] = pd.Series({"mean": bk.mean(), "sd": bk.std(), "n": len(bk),
                                                      "skew": stats.skew(bk), "top10 share of sum": bk.nlargest(10).sum() / bk.sum(),
                                                      "worst10 sum": bk.nsmallest(10).sum()})
    out["book by window"] = bk.groupby(level=0).agg(["mean", "sum", "count"])
    return out
