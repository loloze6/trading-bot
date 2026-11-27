def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]; o=b["open"]
            r=c.pct_change()
            s30=r.rolling(30,min_periods=20).std()
            rng=(h-l)
            clv=np.where(rng>0,(c-(h+l)/2)/(rng/2),0.0)
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),
                "clv":clv,"width":(rng/c)/s30,"r0":r,"r0z":r/s30,
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,
                "ret20":c/c.shift(20)-1,"s30":s30,
                "inprof":(b["regime"]=="unknown").astype(int),
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "year":pd.to_datetime(b["timestamp"]).dt.year,
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # normal drift per coin over all windows (non-overlapping grid)
    for hz in (1,3):
        g=D[D["pos"]%hz==0]
        drift=g.groupby("coin")[f"f{hz}"].mean()
        D[f"x{hz}"]=D[f"f{hz}"]-D["coin"].map(drift)
    D["volrank"]=D.groupby("coin")["s30"].rank(pct=True)
    D["sig"]=D["clv"]*D["width"]
    def summ(df,col,by):
        out=df.groupby(by)[col].agg(["mean","std","count"])
        out["t"]=out["mean"]/(out["std"]/np.sqrt(out["count"]))
        return out.round(5)
    G1=D[(D["pos"]%1==0)].dropna(subset=["x1","width"])
    G3=D[(D["pos"]%3==0)].dropna(subset=["x3","width"])
    res={}
    G1=G1.assign(clvq=pd.qcut(G1["clv"],5,labels=False),sigq=pd.qcut(G1["sig"],10,labels=False),
                 r0q=pd.qcut(G1["r0z"],10,labels=False),volt=pd.qcut(G1["volrank"],3,labels=False),
                 trend=np.sign(G1["ret20"]).fillna(0))
    G3=G3.assign(clvq=pd.qcut(G3["clv"],5,labels=False),sigq=pd.qcut(G3["sig"],10,labels=False),
                 r0q=pd.qcut(G3["r0z"],10,labels=False),volt=pd.qcut(G3["volrank"],3,labels=False))
    res["1d x by clv quintile, in profile"]=summ(G1,"x1",["inprof","clvq"])
    res["3d x by clv quintile, in profile"]=summ(G3,"x3",["inprof","clvq"])
    res["1d x by sig decile all"]=summ(G1,"x1","sigq")
    res["1d x by day-return decile (z)"]=summ(G1,"x1","r0q")
    res["3d x by day-return decile (z)"]=summ(G3,"x3","r0q")
    res["1d x by weekday"]=summ(G1,"x1","wd")
    res["1d x by vol tercile x r0 sign"]=summ(G1.assign(up=(G1["r0"]>0).astype(int)),"x1",["volt","up"])
    res["1d x by trend20 sign x clv<0"]=summ(G1.assign(lo=(G1["clv"]<0).astype(int)),"x1",["trend","lo"])
    # correlations
    cc={}
    for nm,G,col in (("1d",G1,"x1"),("3d",G3,"x3")):
        for f in ("clv","sig","r0z","width"):
            rr,p=stats.spearmanr(G[f],G[col]); cc[f"{nm}_{f}"]=round(rr,4)
    res["spearman"]=pd.Series(cc)
    res["n bars, share inprof"]=pd.Series({"n":len(G1),"inprof":G1["inprof"].mean()})
    return res
