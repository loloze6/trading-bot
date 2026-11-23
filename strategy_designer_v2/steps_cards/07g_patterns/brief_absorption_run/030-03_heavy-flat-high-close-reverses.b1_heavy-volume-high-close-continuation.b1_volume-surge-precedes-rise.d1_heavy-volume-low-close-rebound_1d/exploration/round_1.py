def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 40: continue
            c = b["close"]; h = b["high"]; l = b["low"]; v = b["volume"]
            rng = (h - l).replace(0, np.nan)
            b["clv_low"] = (h - c) / rng
            b["volr"] = v / v.shift(1).rolling(20, min_periods=20).mean()
            b["ret1"] = c / c.shift(1) - 1
            b["past5"] = c / c.shift(5) - 1
            b["past20"] = c / c.shift(20) - 1
            b["vol20"] = b["ret1"].rolling(20, min_periods=15).std()
            b["rngrel"] = (h - l) / c
            b["rngr"] = b["rngrel"] / b["rngrel"].shift(1).rolling(20, min_periods=20).mean()
            b["body"] = (c - b["open"]).abs() / rng
            b["fwd10"] = c.shift(-10) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["fwd3"] = c.shift(-3) / c - 1
            b["coin"] = coin; b["win"] = w
            b["pos"] = np.arange(len(b))
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    G = B[B["pos"] % 10 == 0].dropna(subset=["fwd10"]).copy()
    G["ex10"] = G["fwd10"] - G.groupby("coin")["fwd10"].transform("mean")
    G3 = B[B["pos"] % 3 == 0].dropna(subset=["fwd3"]).copy()
    G3["ex3"] = G3["fwd3"] - G3.groupby("coin")["fwd3"].transform("mean")
    D = B.dropna(subset=["fwd1"]).copy()
    D["ex1"] = D["fwd1"] - D.groupby("coin")["fwd1"].transform("mean")
    out = {}
    def grp(df, col, y, q=5):
        d = df.dropna(subset=[col, y]).copy()
        d["bin"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        r = d.groupby("bin")[y].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["xmean"] = d.groupby("bin")[col].mean()
        return r.round(4)
    def slope(df, x, y):
        d = df.dropna(subset=[x, y])
        s = stats.linregress(d[x], d[y])
        return f"slope {s.slope:.4g} t {s.slope/s.stderr:.2f} n {len(d)}"
    out["10d ex by forecast quintile"] = grp(G, "forecast", "ex10")
    out["10d ex by clv_low quintile"] = grp(G, "clv_low", "ex10")
    out["10d ex by volr quintile"] = grp(G, "volr", "ex10")
    out["10d ex by past5 quintile"] = grp(G, "past5", "ex10")
    out["10d ex by past20 quintile"] = grp(G, "past20", "ex10")
    out["10d ex by vol20 quintile"] = grp(G, "vol20", "ex10")
    out["10d ex by range ratio quintile"] = grp(G, "rngr", "ex10")
    out["3d ex by ret1 quintile"] = grp(G3, "ret1", "ex3")
    out["3d ex by clv_low quintile"] = grp(G3, "clv_low", "ex3")
    out["slopes 10d"] = pd.Series({x: slope(G, x, "ex10") for x in ["forecast","clv_low","volr","past5","past20","vol20","rngr","body","ret1"]})
    out["slopes 3d"] = pd.Series({x: slope(G3, x, "ex3") for x in ["clv_low","volr","past5","past20","vol20","rngr","ret1"]})
    wdr = D.groupby("wd")["ex1"].agg(["mean","count","std"]); wdr["t"] = wdr["mean"]/(wdr["std"]/np.sqrt(wdr["count"]))
    out["next-day ex by weekday of signal day"] = wdr.round(4)
    hv = G[G["vol20"] > G.groupby("coin")["vol20"].transform("median")]
    lv = G[G["vol20"] <= G.groupby("coin")["vol20"].transform("median")]
    out["clv slope in high vol / low vol"] = pd.Series({"high": slope(hv, "clv_low", "ex10"), "low": slope(lv, "clv_low", "ex10"),
        "fc high": slope(hv,"forecast","ex10"), "fc low": slope(lv,"forecast","ex10")})
    out["forecast slope per coin"] = pd.Series({c: slope(g, "forecast", "ex10") for c, g in G.groupby("coin")})
    out["past20 slope per coin"] = pd.Series({c: slope(g, "past20", "ex10") for c, g in G.groupby("coin")})
    out["forecast slope per year"] = pd.Series({y: slope(g, "forecast", "ex10") for y, g in G.groupby("yr")})
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    DD = pd.concat(dd).dropna(subset=["book_return"])
    out["book vs coin daily corr"] = float(DD["book_return"].corr(DD["coin_return"]))
    out["book mean / coin mean daily"] = f"{DD['book_return'].mean():.5f} / {DD['coin_return'].mean():.5f}"
    A = B[["coin","win","postRebalance_current_allocation"]]
    out["mean allocation"] = float(B["postRebalance_current_allocation"].mean())
    out["allocation quantiles"] = B["postRebalance_current_allocation"].quantile([.1,.25,.5,.75,.9]).round(3)
    return out
