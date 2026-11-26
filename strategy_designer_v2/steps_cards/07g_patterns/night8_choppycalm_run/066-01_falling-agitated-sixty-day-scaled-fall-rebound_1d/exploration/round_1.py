def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd60 = r.rolling(60, min_periods=20).std()
            sd10 = r.rolling(10, min_periods=7).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ts": pd.to_datetime(b["timestamp"]),
                "r": r,
                "z60": r / sd60.shift(1),
                "z10": r / sd10.shift(1),
                "loc": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rng": (b["high"] - b["low"]) / c.shift(1) / sd60.shift(1),
                "inprof": (b["regime"] == "unknown"),
                "fc": b["forecast"].astype(float),
                "r1": c.shift(-1) / c - 1,
                "r3": c.shift(-3) / c - 1,
                "r5": c.shift(-5) / c - 1,
                "ret5p": c / c.shift(5) - 1,
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["r"].mean()
    d["x1"] = d["r1"] - d["coin"].map(mu)
    d["wd"] = d["ts"].dt.dayofweek
    d["yr"] = d["ts"].dt.year
    out = {}
    def summ(g, col="x1"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean() if n else np.nan,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    d["zb"] = pd.cut(d["z60"], [-np.inf, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, np.inf])
    out["next day excess by z60 bin x profile"] = d.groupby(["inprof", "zb"], observed=True).apply(summ)
    d["zb10"] = pd.cut(d["z10"], [-np.inf, -2.5, -1.5, -0.75, 0, 0.75, 1.5, 2.5, np.inf])
    out["next day excess by z10 bin, in profile"] = d[d.inprof].groupby("zb10", observed=True).apply(summ)
    # falls in profile: close location
    f = d[(d.inprof) & (d.z60 < -0.75)].copy()
    f["locb"] = pd.cut(f["loc"], [0, 0.25, 0.5, 0.75, 1.0], include_lowest=True)
    out["in-profile falls by close location"] = f.groupby("locb", observed=True).apply(summ)
    # all falls outside profile by close location
    g = d[(~d.inprof) & (d.z60 < -0.75)].copy()
    g["locb"] = pd.cut(g["loc"], [0, 0.25, 0.5, 0.75, 1.0], include_lowest=True)
    out["out-profile falls by close location"] = g.groupby("locb", observed=True).apply(summ)
    # horizon after big falls
    for h in ["r1", "r3", "r5"]:
        d["x" + h] = d[h] - d["coin"].map(mu) * int(h[1:])
    big = d[d.z60 < -1.5]
    out["big falls horizons by profile"] = pd.concat({h: big.groupby("inprof").apply(lambda g: summ(g, "x" + h)) for h in ["r1", "r3", "r5"]}, axis=1)
    # weekday, all bars, next-day excess
    out["weekday all bars"] = d.groupby("wd").apply(summ)
    out["weekday in-profile"] = d[d.inprof].groupby("wd").apply(summ)
    # wide range days
    d["rb"] = pd.qcut(d["rng"], 5, duplicates="drop")
    out["range quintile x profile"] = d.groupby(["inprof", "rb"], observed=True).apply(summ)
    out["share in profile"] = float(d.inprof.mean())
    # book: largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    dd = pd.concat(dd)
    br = dd.groupby("day")["book_return"].mean().dropna()
    s = br.sort_values()
    out["book days"] = pd.Series({"n": len(br), "sum%": 100 * br.sum(),
        "top10 sum%": 100 * s.tail(10).sum(), "bottom10 sum%": 100 * s.head(10).sum(),
        "nonzero days": int((br.abs() > 1e-9).sum())})
    return out
