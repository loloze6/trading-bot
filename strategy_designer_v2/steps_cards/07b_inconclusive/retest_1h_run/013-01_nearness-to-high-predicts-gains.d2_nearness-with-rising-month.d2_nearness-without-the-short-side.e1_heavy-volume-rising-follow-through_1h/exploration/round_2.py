def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    col = "debug_info.components.relvol.last_history_value"
    def grid(h):
        rows = []
        for coin, wins in bars.items():
            for w, df in wins.items():
                c = df["close"].values; f = df["forecast"].values; r = df["regime"].values
                v = df["volume"].values
                raw = df[col].values if col in df.columns else np.full(len(df), np.nan)
                ts = pd.to_datetime(df["timestamp"])
                n = len(df)
                for i in range(0, n - h, h):
                    rv = np.nan
                    if i >= 480:
                        rv = v[i-23:i+1].mean() / v[i-479:i+1].mean() - 1
                    rows.append((coin, w, ts.iloc[i].year, f[i], r[i], raw[i], rv, c[i+h]/c[i]-1))
        g = pd.DataFrame(rows, columns=["coin","w","year","f","reg","raw","rv","ret"])
        g["ex"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
        return g
    def slope(d, x="f"):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 10 or d[x].std() == 0:
            return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        res = stats.linregress(d[x], d["ex"])
        return pd.Series({"n": len(d), "slope": res.slope, "t": res.slope/res.stderr})
    g24 = grid(24); tr = g24[g24.reg == "trending"]
    out["24h by coin"] = tr.groupby("coin").apply(slope)
    out["24h by year"] = tr.groupby("year").apply(slope)
    out["24h windows with positive slope share"] = float((tr.groupby("w").apply(slope)["slope"] > 0).mean())
    pos = tr[tr.f > 0].copy(); z = tr[tr.f == 0]
    pos["q"] = pd.qcut(pos["f"].rank(method="first"), 3, labels=["low","mid","high"])
    tab = pos.groupby("q")["ex"].agg(["count","mean","std"])
    tab.loc["zero"] = [len(z), z["ex"].mean(), z["ex"].std()]
    out["24h excess by forecast group"] = tab
    out["24h slope within positives"] = slope(pos)
    out["24h slope on raw relvol, trending"] = slope(tr, "raw")
    out["24h slope on price-recomputed relvol, non-trending"] = slope(g24[g24.reg != "trending"], "rv")
    g72 = grid(72); tr72 = g72[g72.reg == "trending"]
    out["72h slope on raw relvol, trending"] = slope(tr72, "raw")
    out["72h slope on price-recomputed relvol, non-trending"] = slope(g72[g72.reg != "trending"], "rv")
    # raw relvol terciles within trending 72h
    t2 = tr72.dropna(subset=["raw"]).copy()
    t2["q"] = pd.qcut(t2["raw"].rank(method="first"), 5, labels=list("12345"))
    out["72h excess by raw relvol quintile"] = t2.groupby("q")["ex"].agg(["count","mean"])
    return out
