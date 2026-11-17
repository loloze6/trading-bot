def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df[["timestamp","open","high","low","close","volume","postRebalance_current_allocation"]].copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d=d.sort_values("ts").reset_index(drop=True)
            d["r"]=d["close"].pct_change()
            d["rn1"]=d["close"].shift(-1)/d["close"]-1
            d["rn2"]=d["close"].shift(-2)/d["close"]-1
            d["vol20"]=d["r"].rolling(20,min_periods=10).std()
            d["z"]=d["r"]/d["vol20"].shift(1)
            d["vrel"]=d["volume"]/d["volume"].rolling(30,min_periods=10).median().shift(1)
            d["r7"]=d["close"]/d["close"].shift(7)-1
            d["rng"]=(d["high"]-d["low"])/d["close"]
            d["wd"]=d["ts"].dt.weekday
            d["year"]=d["ts"].dt.year
            d["coin"]=coin; d["win"]=w; d["pos"]=np.arange(len(d))
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    m1=A.groupby("coin")["rn1"].transform("mean")
    A["ex1"]=A["rn1"]-m1
    out={}
    # weekday mean of next-day excess return (day being returned = wd+1)
    g=A.dropna(subset=["ex1"]).groupby("wd")["ex1"]
    out["next-day excess ret by conditioning weekday"]=pd.DataFrame({"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # slope of next-day on z by weekday
    res={}
    for wd,s in A.dropna(subset=["z","ex1"]).groupby("wd"):
        sl=stats.linregress(s["z"].clip(-5,5),s["ex1"])
        res[wd]={"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(s)}
    out["next-day ex on z by weekday"]=pd.DataFrame(res).T
    # z quintile -> next day excess
    B=A.dropna(subset=["z","ex1"]).copy()
    B["zq"]=pd.qcut(B["z"],5,labels=False)
    g=B.groupby("zq")["ex1"]
    out["next-day ex by z quintile"]=pd.DataFrame({"zmean":B.groupby("zq")["z"].mean(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # vol level quintile per coin
    B=A.dropna(subset=["vol20","ex1"]).copy()
    B["vq"]=B.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    g=B.groupby("vq")["ex1"]
    out["next-day ex by vol quintile"]=pd.DataFrame({"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # 7-day return quintile -> next 7 days, nonoverlapping grid
    A["rn7"]=A.groupby(["coin","win"])["close"].shift(-7)/A["close"]-1
    G=A[(A["pos"]%7==0)].dropna(subset=["r7","rn7"]).copy()
    G["ex7"]=G["rn7"]-G.groupby("coin")["rn7"].transform("mean")
    G["q"]=G.groupby("coin")["r7"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    g=G.groupby("q")["ex7"]
    out["next-7d ex by own 7d-return quintile"]=pd.DataFrame({"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # sunday: weekend rise x volume rel
    S=A[(A["wd"]==6)].dropna(subset=["rn2","z","vrel"]).copy()
    S["ex2"]=S["rn2"]-S.groupby("coin")["rn2"].transform("mean")
    S["zq"]=pd.qcut(S["z"],5,labels=False)
    g=S.groupby("zq")["ex2"]
    out["sunday z quintile -> mon-tue ex"]=pd.DataFrame({"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # book daily returns by weekday
    dr=[]
    for coin,ws in data["days"].items():
        for w,df in ws.items():
            x=df.copy(); x["coin"]=coin; x["win"]=w; dr.append(x)
    D=pd.concat(dr,ignore_index=True)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    g=D.dropna(subset=["book_return"]).groupby("wd")["book_return"]
    out["book daily ret by weekday"]=pd.DataFrame({"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    g=D.dropna(subset=["coin_return"]).groupby("wd")["coin_return"]
    out["coin daily ret by weekday"]=pd.DataFrame({"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.count())),"n":g.count()})
    # by year of the sunday reversal
    S["x"]=-S["z"].clip(lower=0)*S["ex2"]
    g=S.groupby("year")["ex2"]
    out["sunday ex2 slope sign by year (corr z,ex2)"]=S.groupby("year").apply(lambda s: pd.Series({"corr":s["z"].corr(s["ex2"]),"n":len(s)}))
    return out
