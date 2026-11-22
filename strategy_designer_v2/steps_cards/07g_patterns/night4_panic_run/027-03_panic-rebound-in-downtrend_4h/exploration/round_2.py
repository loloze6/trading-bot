def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    rows6, rows18, hr, ev = [], [], [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h=df["high"].astype(float); l=df["low"].astype(float)
            ts = pd.to_datetime(df["timestamp"])
            rng = (h-l)/c
            r6 = c/c.shift(6)-1
            r18 = c/c.shift(18)-1
            r6z = r6/r6.abs().rolling(180, min_periods=60).mean()
            r18z = r18/r18.abs().rolling(180, min_periods=60).mean()
            rr = rng.rolling(6).mean()/rng.rolling(180, min_periods=60).mean()
            n = len(c)
            idx = np.arange(0, n-6, 6)
            rows6.append(pd.DataFrame({"coin":coin,"w":w,"yr":ts.dt.year.values[idx],
                "r6z":r6z.values[idx],"rr":rr.values[idx],
                "fwd":c.values[idx+6]/c.values[idx]-1}))
            idx = np.arange(0, n-18, 18)
            rows18.append(pd.DataFrame({"coin":coin,"w":w,"r6z":r6z.values[idx],"r18z":r18z.values[idx],
                "fwd":c.values[idx+18]/c.values[idx]-1}))
            r1 = (c.shift(-1)/c-1)
            hr.append(pd.DataFrame({"coin":coin,"yr":ts.dt.year,"hour":ts.dt.hour,"wd":ts.dt.weekday,"r":r1}))
    def g(d, by, col="dm"):
        x = d.groupby(by)[col].agg(["mean","std","count"])
        x["t"] = x["mean"]/(x["std"]/np.sqrt(x["count"]))
        return x[["mean","t","count"]].round(4)
    D = pd.concat(rows6).dropna()
    D["dm"] = D["fwd"]-D.groupby("coin")["fwd"].transform("mean")
    D["q"] = pd.qcut(D["r6z"],5,labels=False)
    D["rt"] = pd.qcut(D["rr"],3,labels=False)
    x = D.groupby(["q","rt"])["dm"].agg(["mean","std","count"]); x["t"]=x["mean"]/(x["std"]/np.sqrt(x["count"]))
    out["h6 r6z quint x rr tercile"] = x[["mean","t","count"]].round(4)
    lo = D[D["q"]==0]
    out["h6 bottom r6z by coin"] = g(lo,"coin")
    out["h6 bottom r6z by year"] = g(lo,"yr")
    out["h6 top r6z by coin"] = g(D[D["q"]==4],"coin")
    # graded within falls: deciles of r6z among negatives
    neg = D[D["r6z"]<0].copy(); neg["d"]=pd.qcut(neg["r6z"],5,labels=False)
    y = g(neg,"d"); y["xmed"]=neg.groupby("d")["r6z"].median().round(3)
    out["h6 within falls quintiles"] = y
    out["corr r6z fwd h6 (spearman)"] = float(D[["r6z","dm"]].corr("spearman").iloc[0,1])
    E = pd.concat(rows18).dropna()
    E["dm"] = E["fwd"]-E.groupby("coin")["fwd"].transform("mean")
    for col in ["r6z","r18z"]:
        E["b"] = pd.qcut(E[col],5,labels=False)
        z = g(E,"b"); z["xmed"]=E.groupby("b")[col].median().round(3)
        out[f"h18 by {col}"] = z
    Hh = pd.concat(hr).dropna()
    Hh["dm"] = Hh["r"]-Hh.groupby("coin")["r"].transform("mean")
    for hh in [16,20]:
        s = Hh[Hh["hour"]==hh]
        out[f"hour{hh} by coin"] = g(s,"coin")
        out[f"hour{hh} by year"] = g(s,"yr")
    out["friday by year"] = g(Hh[Hh["wd"]==4],"yr")
    return out
