def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            c = d["close"].astype(float)
            r1 = c.pct_change()
            d["coin"] = coin; d["win"] = w
            d["i"] = np.arange(len(d))
            d["r1"] = r1
            d["f1"] = c.shift(-1)/c - 1
            d["f20"] = c.shift(-20)/c - 1
            d["vol20"] = r1.rolling(20).std()
            d["vol100"] = r1.rolling(100).std()
            d["vratio"] = d["vol20"]/d["vol100"]
            d["ret20"] = c/c.shift(20) - 1
            d["z1"] = r1/d["vol20"].shift(1)
            d["dist"] = d["debug_info.components.above_ma.last_history_value"].astype(float)
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.dayofweek
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d[["coin","win","i","r1","f1","f20","vol20","vratio","ret20","z1","dist","wd","year","forecast"]])
    A = pd.concat(rows, ignore_index=True)
    A["cm"] = A.groupby("coin")["r1"].transform("mean")
    A["x20"] = A["f20"] - 20*A["cm"]; A["x1"] = A["f1"] - A["cm"]
    A["volq"] = A.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    A["vrq"] = A.groupby("coin")["vratio"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    A["r20q"] = A.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    NO = A[A["i"] % 20 == 0]  # non-overlapping sample
    def summ(s):
        s = s.dropna(); n=len(s)
        return pd.Series({"n":n,"mean":s.mean(),"t":s.mean()/s.std()*np.sqrt(n) if n>2 else np.nan,"pos":(s>0).mean()})
    out = {}
    out["NONOVERLAP volq -> x20"] = NO.groupby("volq")["x20"].apply(summ).unstack()
    out["NONOVERLAP vratio q -> x20"] = NO.groupby("vrq")["x20"].apply(summ).unstack()
    out["NONOVERLAP past20 q -> x20"] = NO.groupby("r20q")["x20"].apply(summ).unstack()
    fb = pd.cut(NO["forecast"],[-0.01,0,5,10,15,20.1],labels=["0","0-5","5-10","10-15","15-20"])
    out["NONOVERLAP forecast -> x20"] = NO.groupby(fb)["x20"].apply(summ).unstack()
    out["lowvol(q0) x20 by coin (overlap mean)"] = A[A.volq==0].groupby("coin")["x20"].mean()
    out["lowvol(q0) minus all x20 by year"] = A[A.volq==0].groupby("year")["x20"].mean() - A.groupby("year")["x20"].mean()
    out["past20 top q x20 by coin"] = A[A.r20q==4].groupby("coin")["x20"].mean() - A[A.r20q==0].groupby("coin")["x20"].mean()
    dn = A[(A.z1<=-1)]
    out["down day z<=-1 -> x1 by coin"] = dn.groupby("coin")["x1"].apply(summ).unstack()
    out["down day z<=-1 -> x1 by year"] = dn.groupby("year")["x1"].mean()
    out["down day z<=-1 x1 by above/below sma"] = dn.groupby(dn["dist"]>0)["x1"].apply(summ).unstack()
    out["weekday x1 by coin (mean*1e3)"] = (A.groupby(["coin","wd"])["x1"].mean()*1e3).unstack()
    # fresh cross: days since close crossed above sma
    def since(g):
        ab = (g["dist"]>0).astype(int)
        grp = (ab != ab.shift()).cumsum()
        return ab.groupby(grp).cumcount()*ab
    A["age"] = A.groupby(["coin","win"], group_keys=False).apply(since)
    ab = pd.cut(A["age"],[-1,0,10,30,90,1e5],labels=["below","1-10","11-30","31-90",">90"])
    sub = A.copy(); sub["ab"]=ab
    NO2 = sub[sub["i"]%20==0]
    out["NONOVERLAP age above sma -> x20"] = NO2.groupby("ab")["x20"].apply(summ).unstack()
    return out
