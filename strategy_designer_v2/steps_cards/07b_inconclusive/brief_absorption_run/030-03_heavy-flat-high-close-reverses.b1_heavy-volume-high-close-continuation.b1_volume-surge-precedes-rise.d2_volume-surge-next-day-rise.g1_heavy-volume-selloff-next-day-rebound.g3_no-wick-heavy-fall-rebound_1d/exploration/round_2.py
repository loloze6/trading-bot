def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        mu = pd.concat([(b["close"].shift(-1)/b["close"]-1).dropna() for b in wins.values()]).mean()
        for w, b in wins.items():
            b = b.copy()
            b["ex"] = b["close"].shift(-1)/b["close"]-1-mu
            b["ret1"] = b["close"]/b["close"].shift(1)-1
            rng = (b["high"]-b["low"]).replace(0,np.nan)
            b["clh"] = (b["high"]-b["close"])/rng
            b["vr"] = b["volume"]/b["volume"].shift(1).rolling(20).mean()
            lr = np.log(b["close"]).diff(); v20 = lr.rolling(20).std()
            b["volr"] = v20/v20.rolling(60).mean()
            b["raw"] = b["clh"]*b["vr"]*b["volr"]
            b["lhv"] = b.get("debug_info.components.absorb.last_history_value")
            b["coin"]=coin; b["win"]=w
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","win","year","forecast","ex","ret1","clh","vr","volr","raw","lhv"]])
    d = pd.concat(rows).dropna(subset=["ex"])
    a = d[d["forecast"]>0].copy()
    def g(x):
        return pd.Series({"n":len(x),"mean_ex_%":100*x["ex"].mean(),
                          "t":x["ex"].mean()/(x["ex"].std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["lhv_describe_active"] = a["lhv"].astype(float).describe()
    a["rawq"] = pd.qcut(a["raw"], 5)
    out["by_raw_product_q"] = a.groupby("rawq", observed=True).apply(g)
    s = a[a["forecast"]>=19.999].copy()
    s["rawq"] = pd.qcut(s["raw"], 3)
    out["saturated_by_raw_tercile"] = s.groupby("rawq", observed=True).apply(g)
    a["above_med_raw"] = a["raw"] > a["raw"].median()
    out["raw_median_split"] = a.groupby("above_med_raw").apply(g)
    a["mov"] = pd.cut(a["ret1"], [-1,-0.06,-0.03,-0.01,0])
    out["by_day_fall"] = a.groupby("mov", observed=True).apply(g)
    a["spear"] = 0
    out["spearman_raw_ex"] = float(a[["raw","ex"]].corr(method="spearman").iloc[0,1])
    out["spearman_forecast_ex"] = float(a[["forecast","ex"]].corr(method="spearman").iloc[0,1])
    return out
