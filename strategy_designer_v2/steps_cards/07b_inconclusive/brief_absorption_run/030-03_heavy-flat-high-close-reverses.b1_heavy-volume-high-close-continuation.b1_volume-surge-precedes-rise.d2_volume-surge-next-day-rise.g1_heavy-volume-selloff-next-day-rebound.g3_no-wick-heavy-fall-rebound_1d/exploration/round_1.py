def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            r = b["close"].shift(-1) / b["close"] - 1
            allr.append(r.dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.copy()
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["ex"] = b["nxt"] - mu
            b["ret1"] = b["close"] / b["close"].shift(1) - 1
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["cl_from_high"] = (b["high"] - b["close"]) / rng
            b["vr"] = b["volume"] / b["volume"].shift(1).rolling(20).mean()
            lr = np.log(b["close"]).diff()
            v20 = lr.rolling(20).std()
            b["volr"] = v20 / v20.rolling(60).mean()
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","win","year","forecast","nxt","ex","ret1","cl_from_high","vr","volr"]])
    d = pd.concat(rows).dropna(subset=["nxt"])
    a = d[d["forecast"] > 0].copy()
    out = {}
    out["forecast_describe"] = a["forecast"].describe()
    out["share_forecast_eq_max"] = float((a["forecast"] >= a["forecast"].max() - 1e-9).mean())
    out["forecast_max"] = float(a["forecast"].max())
    out["median_forecast"] = float(a["forecast"].median())
    def g(x):
        return pd.Series({"n": len(x), "mean_ex_%": 100*x["ex"].mean(),
                          "t": x["ex"].mean()/(x["ex"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    a["fbin"] = pd.cut(a["forecast"], [0,5,10,15,19.999,20.001])
    out["by_forecast_bin"] = a.groupby("fbin", observed=True).apply(g)
    out["by_coin"] = a.groupby("coin").apply(g)
    out["by_year"] = a.groupby("year").apply(g)
    a["clbin"] = pd.cut(a["cl_from_high"], [-0.01,0.25,0.5,0.75,0.9,1.01])
    out["by_close_from_high"] = a.groupby("clbin", observed=True).apply(g)
    a["vrbin"] = pd.qcut(a["vr"], 4)
    out["by_volratio_q"] = a.groupby("vrbin", observed=True).apply(g)
    a["volrbin"] = pd.qcut(a["volr"], 4)
    out["by_volatility_ratio_q"] = a.groupby("volrbin", observed=True).apply(g)
    # control: down days ordinary volume, by close position
    c = d[(d["ret1"] < 0) & (d["vr"] < 1)].copy()
    c["clbin"] = pd.cut(c["cl_from_high"], [-0.01,0.25,0.5,0.75,0.9,1.01])
    out["control_lowvol_down_by_close"] = c.groupby("clbin", observed=True).apply(g)
    out["all_down_heavy_ex"] = g(d[(d["ret1"]<0)&(d["vr"]>=1)])
    return out
