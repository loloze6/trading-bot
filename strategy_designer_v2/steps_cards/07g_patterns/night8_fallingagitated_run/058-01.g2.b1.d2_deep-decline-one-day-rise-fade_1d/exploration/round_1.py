def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd=r1.rolling(30,min_periods=20).std()
            z1=r1/sd
            r3p=c/c.shift(3)-1
            z3=r3p/(sd*np.sqrt(3))
            r5p=c/c.shift(5)-1
            z5=r5p/(sd*np.sqrt(5))
            f3=c.shift(-3)/c-1
            f1=c.shift(-1)/c-1
            rng=(b["high"]-b["low"])/c
            clv=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            inprof=(b["regime"]!="chop")
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"z1":z1,"z3":z3,"z5":z5,"f3":f3,"f1":f1,"inprof":inprof,
                            "wd":ts.dt.weekday,"clv":clv,"rngz":rng/sd,"fc":b["forecast"],
                            "alloc":b["postRebalance_current_allocation"],"pos":np.arange(len(b))})
            rows.append(d)
    D=pd.concat(rows)
    G=D[D.pos%3==0].dropna(subset=["f3"]).copy()
    G["drift"]=G.groupby("coin")["f3"].transform("mean")
    G["u3"]=G["f3"]-G["drift"]
    out={}
    def summ(df,col,key):
        g=df.groupby(key)[col]
        return pd.DataFrame({"n":g.size(),"mean%":g.mean()*100,"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    out["share_inprof"]=float(G.inprof.mean())
    for nm in ["z1","z3","z5","clv","rngz"]:
        G[nm+"q"]=G.groupby("inprof")[nm].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
        out[nm+"_quint_u3"]=summ(G.dropna(subset=[nm+"q"]),"u3",["inprof",nm+"q"])
    out["wd_u3"]=summ(G,"u3",["inprof","wd"])
    out["corr_z3_u3_inprof"]=float(G[G.inprof][["z3","u3"]].corr().iloc[0,1])
    return out
