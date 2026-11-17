def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            c = d["close"].astype(float)
            r = c.pct_change()
            d["r"] = r
            d["vol20"] = r.rolling(20).std()
            d["z"] = r / d["vol20"]
            d["vol_rank"] = d["vol20"].rolling(120, min_periods=40).rank(pct=True)
            d["fwd1"] = c.shift(-1)/c - 1
            d["fwd3"] = c.shift(-3)/c - 1
            d["ret20"] = c/c.shift(20) - 1
            d["nearhigh"] = c / c.rolling(20).max() - 1
            d["vz"] = np.log(d["volume"].astype(float)+1)
            d["vz"] = (d["vz"] - d["vz"].rolling(20).mean())/d["vz"].rolling(20).std()
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["w"] = w
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d[["coin","w","pos","r","z","vol20","vol_rank","fwd1","fwd3","ret20","nearhigh","vz","wd","year","forecast","postRebalance_current_allocation"]])
    A = pd.concat(rows, ignore_index=True)
    cm = A.groupby("coin")["fwd1"].transform("mean")
    A["ex1"] = A["fwd1"] - cm
    cm3 = A[A.pos%3==0].groupby("coin")["fwd3"].mean()
    A["ex3"] = A["fwd3"] - A["coin"].map(cm3)
    out = {}
    def tab(g, col="ex1", sub=None):
        S = A if sub is None else sub
        x = S.dropna(subset=[col]).groupby(g)[col]
        t = x.agg(["mean","std","count"])
        t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
        return t[["mean","count","t"]]
    A["zb"] = pd.cut(A["z"], [-np.inf,-2.5,-1.5,-1,-0.5,0,0.5,1,1.5,2.5,np.inf])
    out["z bucket -> next1 excess"] = tab("zb")
    A3 = A[A.pos%3==0]
    out["z bucket -> next3 excess (nonoverlap)"] = tab("zb","ex3",A3)
    # by coin, down bars slope
    res = {}
    for coin, g in A[A["z"]<0].dropna(subset=["z","ex1"]).groupby("coin"):
        s = stats.linregress(-g["z"], g["ex1"]); res[coin] = (s.slope, s.slope/s.stderr, len(g))
    out["downday slope by coin"] = pd.DataFrame(res, index=["slope","t","n"]).T
    res = {}
    for coin, g in A[A["z"]>0].dropna(subset=["z","ex1"]).groupby("coin"):
        s = stats.linregress(g["z"], g["ex1"]); res[coin] = (s.slope, s.slope/s.stderr, len(g))
    out["upday slope by coin (z>0)"] = pd.DataFrame(res, index=["slope","t","n"]).T
    # vol regime interaction on down days
    D = A[A["z"]<-1]
    D = D.assign(vq=pd.qcut(D["vol_rank"], 3, labels=["lowvol","mid","highvol"]))
    out["z<-1 by vol tercile"] = tab("vq", sub=D)
    D = D.assign(tr=pd.qcut(D["ret20"], 3, labels=["down20","mid","up20"]))
    out["z<-1 by 20d trend"] = tab("tr", sub=D)
    D = D.assign(vb=pd.qcut(D["vz"], 3, labels=["lowvolu","mid","highvolu"]))
    out["z<-1 by volume z"] = tab("vb", sub=D)
    out["all bars by weekday"] = tab("wd")
    out["z<-1 by year"] = tab("year", sub=D)
    A["vq"] = pd.qcut(A["vol_rank"], 5, labels=False)
    out["all by vol quintile"] = tab("vq")
    A["nh"] = pd.qcut(A["nearhigh"], 5, labels=False)
    out["all by nearness to 20d high quintile"] = tab("nh")
    return out
