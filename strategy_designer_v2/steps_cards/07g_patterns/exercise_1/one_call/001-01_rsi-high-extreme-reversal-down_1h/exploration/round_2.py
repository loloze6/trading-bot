def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            lc = np.log(b["close"].astype(float))
            b["r1"] = lc.diff()
            b["f12"] = lc.shift(-12) - lc
            b["f24"] = lc.shift(-24) - lc
            b["f12x"] = b["f12"] - b["f12"].mean()
            b["f24x"] = b["f24"] - b["f24"].mean()
            b["rsi"] = 50 - b["debug_info.components.rsi_high.last_history_value"].astype(float)
            b["r12p"] = lc - lc.shift(12)
            b["r24p"] = lc - lc.shift(24)
            b["vol24"] = b["r1"].rolling(24).std()
            b["vol_rel"] = b["vol24"] / b["vol24"].rolling(240, min_periods=60).median()
            b["grid"] = (np.arange(len(b)) % 12) == 0
            b["coin"] = coin; b["win"] = w
            b["short"] = b["forecast"].astype(float) < 0
            b["streak_hi"] = (b["rsi"] > 70).astype(int).groupby(((b["rsi"] > 70) != (b["rsi"] > 70).shift()).cumsum()).cumsum()
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["grid"]].copy()
    def agg(x, col="f12x"):
        x = x[col].dropna()
        return pd.Series({"n": len(x), "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    rb = pd.cut(g["rsi"], [0, 25, 30, 35, 40, 45, 55, 60, 65, 70, 75, 100])
    out["RSI band -> fwd12 excess (non-overlap grid)"] = g.groupby(rb).apply(agg)
    out["RSI band -> fwd24 excess (grid)"] = g.groupby(rb).apply(lambda x: agg(x, "f24x"))
    lo = g[g["rsi"] < 30]; hi = g[g["rsi"] > 70]
    out["RSI<30 fwd12 excess by coin x window bp"] = lo.groupby(["win", "coin"])["f12x"].mean().unstack() * 1e4
    out["RSI>70 fwd12 excess by coin x window bp"] = hi.groupby(["win", "coin"])["f12x"].mean().unstack() * 1e4
    g["r24_dec"] = g.groupby("coin")["r24p"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["past24h decile -> fwd24 excess (grid)"] = g.groupby("r24_dec").apply(lambda x: agg(x, "f24x"))
    g["vq"] = pd.qcut(g["vol_rel"], 5, labels=False, duplicates="drop")
    g["dir"] = np.sign(g["r24p"])
    out["rel vol quintile x past24 sign -> fwd12 excess"] = g.groupby(["vq", "dir"]).apply(agg)
    g["vq_abs"] = g.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["abs vol quintile -> fwd12 (grid) by window count of positive"] = g.groupby(["vq_abs"]).apply(agg)
    out["top vol quintile fwd12 excess by window x coin bp"] = g[g["vq_abs"] == 4].groupby(["win", "coin"])["f12x"].mean().unstack() * 1e4
    sb = pd.cut(g["streak_hi"], [-1, 0, 1, 3, 6, 12, 1000])
    out["bars RSI>70 consecutive -> fwd12 excess"] = g.groupby(sb).apply(agg)
    return out
