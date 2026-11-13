def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allf = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            n = len(c)
            f5 = np.full(n, np.nan); f5[:-5] = c[5:]/c[:-5]-1
            allf.append(f5)
        mu = np.nanmean(np.concatenate(allf))
        for w, b in wins.items():
            c = b["close"].astype(float).values
            n = len(c)
            f5 = np.full(n, np.nan); f5[:-5] = c[5:]/c[:-5]-1
            r20 = np.full(n, np.nan); r20[20:] = c[20:]/c[:-20]-1
            lr = np.diff(np.log(c), prepend=np.nan)
            vol = pd.Series(lr).rolling(20).std().values
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(n), "f5": f5, "ex": f5-mu,
                               "fc": b["forecast"].astype(float).values, "reg": b["regime"].values,
                               "r20": r20, "vol": vol, "year": ts.dt.year.values})
            rows.append(df)
    d = pd.concat(rows)
    d = d[d["f5"].notna()]
    g = d[d["i"] % 5 == 0]
    def tt(x):
        x = x.dropna()
        if len(x) < 3: return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan})
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/x.std(ddof=1)*np.sqrt(len(x))})
    out = {}
    L = g[g["fc"] > 0]
    out["long_all"] = tt(L["ex"])
    out["by_coin"] = L.groupby("coin")["ex"].apply(tt).unstack()
    out["by_year"] = L.groupby("year")["ex"].apply(tt).unstack()
    L = L.copy()
    L["fq"] = pd.qcut(L["fc"].rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["by_fc_quartile"] = L.groupby("fq")["ex"].apply(tt).unstack()
    L["r20q"] = pd.qcut(L["r20"].rank(method="first"), 4, labels=["q1","q2","q3","q4"])
    out["by_r20_quartile"] = L.groupby("r20q")["ex"].apply(tt).unstack()
    # comparison groups
    T = g[g["reg"] == "trending"]
    out["trending_flat_fc0"] = tt(T[T["fc"] <= 0]["ex"])
    nt = g[g["reg"] != "trending"]
    out["nontrend_r20pos"] = tt(nt[nt["r20"] > 0]["ex"])
    out["nontrend_r20neg"] = tt(nt[nt["r20"] <= 0]["ex"])
    out["all_bars"] = tt(g["ex"])
    # market co-movement: BTC 20d return same timestamp
    out["long_std_vs_all_std"] = pd.Series({"long_std": L["f5"].std(), "all_std": g["f5"].std(), "long_hit_pos": (L["f5"]>0).mean(), "all_hit_pos": (g["f5"]>0).mean()})
    return out
