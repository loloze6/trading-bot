def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            if len(b) < 40: continue
            c = b["close"]; h = b["high"]; l = b["low"]; v = b["volume"]
            rng = (h - l).replace(0, np.nan)
            b["clv_low"] = (h - c) / rng
            b["volr"] = v / v.shift(1).rolling(20, min_periods=20).mean()
            b["lvolr"] = np.log(b["volr"])
            b["ret1"] = c / c.shift(1) - 1
            b["past5"] = c / c.shift(5) - 1
            b["past20"] = c / c.shift(20) - 1
            b["vol20"] = b["ret1"].rolling(20, min_periods=15).std()
            b["rngrel"] = (h - l) / c
            b["rngr"] = b["rngrel"] / b["rngrel"].shift(1).rolling(20, min_periods=20).mean()
            b["volr5"] = v.rolling(5).mean() / v.shift(5).rolling(20, min_periods=20).mean()
            b["fwd10"] = c.shift(-10) / c - 1
            b["fwd5"] = c.shift(-5) / c - 1
            b["fwd20"] = c.shift(-20) / c - 1
            b["coin"] = coin; b["win"] = w
            b["pos"] = np.arange(len(b))
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    out = {}
    def mk(hz):
        G = B[B["pos"] % hz == 0].dropna(subset=[f"fwd{hz}"]).copy()
        G["ex"] = G[f"fwd{hz}"] - G.groupby("coin")[f"fwd{hz}"].transform("mean")
        G["vu"] = G[f"fwd{hz}"].groupby(G["coin"]).transform("std")
        G["str"] = G["ex"] / G["vu"]
        return G
    G = mk(10)
    def slope(df, x, y="ex"):
        d = df.dropna(subset=[x, y])
        if len(d) < 20: return "n<20"
        s = stats.linregress(d[x], d[y])
        return f"slope {s.slope:.4g} t {s.slope/s.stderr:.2f} n {len(d)}"
    def ols(df, xs, y="ex"):
        d = df.dropna(subset=xs + [y])
        X = np.column_stack([np.ones(len(d))] + [d[x].values for x in xs]); Y = d[y].values
        beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
        res = Y - X @ beta; s2 = res @ res / (len(d) - X.shape[1])
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        return pd.DataFrame({"beta": beta, "t": beta / se}, index=["const"] + xs).round(4).assign(n=len(d))
    out["multi 10d volr clv past20 rngr"] = ols(G, ["volr", "clv_low", "past20", "rngr"])
    out["multi 10d volr ret1 past20"] = ols(G, ["volr", "ret1", "past20"])
    out["multi 10d lvolr"] = ols(G, ["lvolr", "past20"])
    out["volr slope per coin"] = pd.Series({c: slope(g, "volr") for c, g in G.groupby("coin")})
    out["volr slope per year"] = pd.Series({y: slope(g, "volr") for y, g in G.groupby("yr")})
    out["volr slope per window group"] = pd.Series({k: slope(G[G["win"].isin([f"w{i}" for i in range(a, a+6)])], "volr") for k, a in [("w1-6",1),("w7-12",7),("w13-18",13),("w19-24",19)]})
    up = G[G["ret1"] > 0]; dn = G[G["ret1"] <= 0]
    out["volr slope on up / down days"] = pd.Series({"up day": slope(up, "volr"), "down day": slope(dn, "volr")})
    out["volr slope past20 up / down"] = pd.Series({"past20>0": slope(G[G["past20"] > 0], "volr"), "past20<=0": slope(G[G["past20"] <= 0], "volr")})
    out["volr5 slope 10d"] = slope(G, "volr5")
    d = G.dropna(subset=["volr"]).copy()
    d["bin"] = pd.qcut(d["volr"].rank(method="first"), 10, labels=False)
    r = d.groupby("bin").agg(ex=("ex", "mean"), n=("ex", "count"), sd=("ex", "std"), x=("volr", "mean"), strength=("str", "mean"), tot=(f"fwd10", "mean"))
    r["t"] = r["ex"] / (r["sd"] / np.sqrt(r["n"]))
    out["10d ex by volr decile"] = r.round(4)
    for hz in [5, 20]:
        Gh = mk(hz)
        out[f"volr slope {hz}d"] = slope(Gh, "volr")
        out[f"rngr slope {hz}d"] = slope(Gh, "rngr")
    # volr strength in direction: up-day heavy vs down-day heavy
    d["sgn"] = np.sign(d["ret1"])
    d["sv"] = d["sgn"] * d["volr"]
    out["signed volr slope 10d"] = slope(d, "sv")
    # book largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; dd.append(x)
    DD = pd.concat(dd).dropna(subset=["book_return"])
    q = DD["book_return"].quantile([0.02, 0.98])
    out["coin return on book's worst 2% / best 2% days"] = pd.Series({"worst book": DD.loc[DD["book_return"] <= q.iloc[0], "coin_return"].mean(), "best book": DD.loc[DD["book_return"] >= q.iloc[1], "coin_return"].mean(), "worst book mean": DD.loc[DD["book_return"] <= q.iloc[0], "book_return"].mean(), "best book mean": DD.loc[DD["book_return"] >= q.iloc[1], "book_return"].mean()}).round(4)
    return out
