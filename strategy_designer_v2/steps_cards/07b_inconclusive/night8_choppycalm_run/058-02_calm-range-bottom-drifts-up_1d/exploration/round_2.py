def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            b["pos"] = (b["close"] - lo) / (hi - lo) * 2 - 1
            c = b["close"].values
            fr = pd.Series(np.nan, index=b.index); fr.iloc[:len(b)-5] = c[5:] / c[:-5] - 1
            b["fr5"] = fr
            lr = np.log(b["close"]).diff()
            b["tr60"] = b["close"] / b["close"].shift(60) - 1
            sw = lr.rolling(30).std()
            b["agit"] = sw.rolling(365, min_periods=200).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            b["coin"] = coin; b["win"] = w
            b["prof"] = (b["regime"] == "unknown")
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["i"] = np.arange(len(b))
            b["dayid"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b[["coin","win","year","i","pos","prof","forecast","fr5","tr60","agit","dayid"]])
    d = pd.concat(rows, ignore_index=True)
    g = d[d["i"] % 5 == 0].copy()
    dr = g.groupby("coin")["fr5"].mean()
    g["ex5"] = g["fr5"] - g["coin"].map(dr)
    g = g[g.pos.notna() & g.ex5.notna()]
    def sl(x, col="pos"):
        x = x[x[col].notna()]
        if len(x) < 8: return pd.Series({"n": len(x)})
        r = stats.linregress(x[col], x["ex5"])
        return pd.Series({"n": len(x), "slope": r.slope, "t": r.slope / r.stderr})
    out = {}
    p = g[g.prof]
    out["profile slope on pos by year"] = p.groupby("year").apply(sl)
    out["profile slope on pos by coin"] = p.groupby("coin").apply(sl)
    out["profile slope on forecast vs pos"] = pd.DataFrame({"pos": sl(p), "forecast": sl(p, "forecast")})
    # day-clustered t for slope on pos in profile
    X = p["pos"] - p["pos"].mean(); y = p["ex5"]
    b1 = (X * y).sum() / (X ** 2).sum()
    res = y - y.mean() - b1 * X
    sc = (X * res).groupby(p["dayid"].values).sum()
    se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
    out["profile slope clustered"] = pd.Series({"slope": b1, "t_day": b1 / se, "days": len(sc)})
    # choppy agitated vs choppy calm recomputed
    ch = g[(g.tr60.abs() <= 0.10) & g.agit.notna()]
    out["choppy calm (recomputed) vs agitated"] = pd.DataFrame({
        "calm": sl(ch[ch.agit <= 0.5]), "agitated": sl(ch[ch.agit > 0.5])})
    out["all bars slope"] = sl(g)
    out["not profile slope"] = sl(g[~g.prof])
    # upper third graded in profile
    out["profile pos>0 slope"] = sl(p[p.pos > 0])
    out["profile pos<0 slope"] = sl(p[p.pos < 0])
    return out
