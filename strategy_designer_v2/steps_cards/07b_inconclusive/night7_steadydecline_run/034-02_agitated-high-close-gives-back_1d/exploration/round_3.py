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
            d["coin"]=coin
            d["day"]=pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["pos"]=d["postRebalance_current_allocation"]
            rows.append(d[["coin","day","clv","r1","r60","agit","forecast","pos"]])
    A=pd.concat(rows,ignore_index=True)
    A["x1"]=A["r1"]-A.groupby("coin")["r1"].transform("mean")
    A["trend"]=np.where(A["r60"]>0.1,"rising",np.where(A["r60"]<-0.1,"falling",np.where(A["r60"].notna(),"choppy",None)))
    def dayt(s,val):
        n=len(s); m=s[val].mean()
        dev=(s[val]-m).groupby(s["day"]).sum()
        K=len(dev); se=np.sqrt((dev**2).sum()*K/(K-1))/n
        return pd.Series({"n":n,"days":K,"mean%":m*100,"t":m/se})
    out={}
    Ag=A[A["agit"]&A["clv"].notna()&A["x1"].notna()&A["trend"].notna()].copy()
    Ag["shortx"]=-Ag["x1"]*Ag["clv"]   # graded short gain, more the nearer the high
    out["graded_short_by_trend"]=Ag.groupby("trend").apply(lambda s: dayt(s,"shortx"))
    Hi=Ag[Ag["clv"]>0.5].copy(); Hi["sx"]=-Hi["x1"]
    out["high_close_short_by_trend"]=Hi.groupby("trend").apply(lambda s: dayt(s,"sx"))
    M=A[(A["forecast"]!=0)&A["x1"].notna()&A["trend"].notna()].copy()
    M["pm"]=M["pos"]*M["x1"]
    out["main_measure_by_trend"]=M.groupby("trend").apply(lambda s: dayt(s,"pm"))
    out["rawdrift_r1_by_trend_agit%"]=Ag.groupby("trend")["r1"].mean()*100
    return out
