def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy().reset_index(drop=True)
            rng=(d["high"]-d["low"])
            d["clv"]=np.where(rng>0,(d["close"]-d["low"])/rng,np.nan)
            d["r1"]=d["close"].shift(-1)/d["close"]-1
            d["r60"]=d["close"]/d["close"].shift(60)-1
            d["agit"]=(d["regime"]!="chop")
            d["coin"]=coin; d["win"]=w
            d["day"]=pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["pos"]=d["postRebalance_current_allocation"]
            d["absret"]=(d["close"]/d["close"].shift(1)-1).abs()
            rows.append(d[["coin","win","day","clv","r1","r60","agit","forecast","pos","absret"]])
    A=pd.concat(rows,ignore_index=True)
    A["x1"]=A["r1"]-A.groupby("coin")["r1"].transform("mean")
    out={}
    def dayt(s,val):
        g=s.groupby("day")[val].sum(); n=len(s)
        m=s[val].mean()
        dev=(s[val]-m).groupby(s["day"]).sum()
        K=len(dev); se=np.sqrt((dev**2).sum()*K/(K-1))/n
        return pd.Series({"n":n,"days":K,"mean":m,"t":m/se})
    M=A[(A["forecast"]!=0)&A["x1"].notna()].copy()
    M["pm"]=M["pos"]*M["x1"]
    out["main_measure_BC"]=dayt(M,"pm")
    out["main_by_coin"]=M.groupby("coin").apply(lambda s: dayt(s,"pm"))
    Ag=A[A["agit"]&A["clv"].notna()&A["x1"].notna()].copy()
    out["forecast_by_clv_quint"]=Ag.groupby(pd.qcut(Ag["clv"],5,labels=False))[["forecast","pos"]].mean()
    # reversal signal: (0.5-clv) * x1, day clustered
    Ag["rev"]=(0.5-Ag["clv"])*Ag["x1"]
    out["rev_agit"]=dayt(Ag,"rev")
    Ag["trend"]=np.where(Ag["r60"]>0.1,"rising",np.where(Ag["r60"]<-0.1,"falling","choppy"))
    out["rev_agit_by_trend"]=Ag.dropna(subset=["r60"]).groupby("trend").apply(lambda s: dayt(s,"rev"))
    Ca=A[(~A["agit"])&A["clv"].notna()&A["x1"].notna()].copy()
    Ca["rev"]=(0.5-Ca["clv"])*Ca["x1"]
    out["rev_calm"]=dayt(Ca,"rev")
    return out
