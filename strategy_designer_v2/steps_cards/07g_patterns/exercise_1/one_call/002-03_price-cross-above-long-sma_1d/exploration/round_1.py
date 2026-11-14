def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            c = d["close"].astype(float)
            r1 = c.pct_change()
            d["coin"] = coin
            d["r1"] = r1
            d["f1"] = c.shift(-1) / c - 1
            d["f5"] = c.shift(-5) / c - 1
            d["f20"] = c.shift(-20) / c - 1
            d["dist"] = d["debug_info.components.above_ma.last_history_value"].astype(float)
            d["vol20"] = r1.rolling(20).std()
            d["ret20"] = c / c.shift(20) - 1
            d["z1"] = r1 / d["vol20"].shift(1)
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.dayofweek
            rows.append(d[["coin","r1","f1","f5","f20","dist","vol20","ret20","z1","wd","forecast","postRebalance_current_allocation"]])
    A = pd.concat(rows, ignore_index=True)
    A["cm"] = A.groupby("coin")["r1"].transform("mean")
    A["x20"] = A["f20"] - 20*A["cm"]
    A["x5"] = A["f5"] - 5*A["cm"]
    A["x1"] = A["f1"] - A["cm"]

    def summ(g, col):
        s = g[col].dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/s.std()*np.sqrt(len(s)) if len(s)>2 else np.nan, "pos": (s>0).mean()})

    out = {}
    A["distq"] = pd.qcut(A["dist"], 10, labels=False, duplicates="drop")
    out["dist decile -> x20"] = A.groupby("distq").apply(lambda g: pd.concat([pd.Series({"dist_mid": g["dist"].median()}), summ(g,"x20")]))
    out["dist decile -> x5"] = A.groupby("distq").apply(lambda g: summ(g,"x5"))
    fb = pd.cut(A["forecast"], [-0.01,0,5,10,15,20.1], labels=["0","0-5","5-10","10-15","15-20"])
    out["forecast bucket -> x20"] = A.groupby(fb).apply(lambda g: summ(g,"x20"))
    zb = pd.cut(A["z1"], [-99,-3,-2,-1,1,2,3,99])
    out["z of day move -> x1"] = A.groupby(zb).apply(lambda g: summ(g,"x1"))
    out["z of day move -> x5"] = A.groupby(zb).apply(lambda g: summ(g,"x5"))
    A["volq"] = A.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["vol quintile -> x20"] = A.groupby("volq").apply(lambda g: summ(g,"x20"))
    out["vol quintile -> x1"] = A.groupby("volq").apply(lambda g: summ(g,"x1"))
    out["weekday -> x1"] = A.groupby("wd").apply(lambda g: summ(g,"x1"))
    r20q = A.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["past20 ret quintile -> x20"] = A.groupby(r20q).apply(lambda g: summ(g,"x20"))
    # interaction dist>0 and vol
    A["above"] = (A["dist"]>0).astype(int)
    out["above x volq -> x20 mean"] = A.groupby(["above","volq"])["x20"].mean().unstack()
    out["coin above vs below x20"] = A.groupby(["coin","above"])["x20"].mean().unstack()
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"]=coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["dur_d"] = T["duration_minutes"]/1440
    out["trades summary"] = pd.Series({"n": len(T), "mean_net": T["net_profit_loss_percent"].mean(), "median_net": T["net_profit_loss_percent"].median(), "win": (T["net_profit_loss_percent"]>0).mean(), "mean_dur_d": T["dur_d"].mean(), "median_dur_d": T["dur_d"].median()})
    T["durb"] = pd.cut(T["dur_d"], [0,1.5,5,20,60,1e4])
    out["trades by duration"] = T.groupby("durb")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
