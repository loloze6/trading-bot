def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            c=b["close"].astype(float)
            r=c.pct_change()
            v=r.rolling(20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"z":r/v,"r":r,"nxt":c.shift(-1)/c-1,
                "tr60":c/c.shift(60)-1,
                "rp":(c-b["low"].rolling(20).min())/(b["high"].rolling(20).max()-b["low"].rolling(20).min()),
                "inprof":(b["regime"]=="unknown"),
                "pos":b["postRebalance_current_allocation"],
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "rng":(b["high"]-b["low"])/c/v,
                "clv":(c-b["low"])/(b["high"]-b["low"])})
            n=len(c); idx=np.arange(n)
            f5=c.shift(-5)/c-1
            d["f5"]=np.where(idx%5==0,f5,np.nan)
            f3=c.shift(-3)/c-1
            d["f3"]=np.where(idx%3==0,f3,np.nan)
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["ex"]=D["nxt"]-D.groupby("coin")["nxt"].transform("mean")
    D["ex5"]=D["f5"]-D.groupby("coin")["f5"].transform("mean")
    D["ex3"]=D["f3"]-D.groupby("coin")["f3"].transform("mean")
    def st(g,col="ex"):
        x=g[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    D["zq"]=pd.qcut(D["z"],7,labels=False)
    out["z7 x inprof nextday"]=D.groupby(["inprof","zq"]).apply(st).round(3)
    D["trb"]=pd.cut(D["tr60"],[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    out["z7 x trend nextday (out of profile)"]=D[~D.inprof].groupby(["trb","zq"]).apply(st).round(3)
    D["rpq"]=pd.cut(D["rp"],[-.01,.2,.4,.6,.8,1.01],labels=False)
    out["rangepos x trend 5d"]=D.groupby(["trb","rpq"]).apply(lambda g:st(g,"ex5")).round(3)
    out["weekday x inprof nextday"]=D.groupby(["inprof","wd"]).apply(st).round(3)
    D["rngq"]=pd.qcut(D["rng"],5,labels=False)
    out["range/vol q x clv<.3 nextday"]=D[D.clv<0.3].groupby("rngq").apply(st).round(3)
    out["share inprof, held"]=pd.Series({"inprof":D.inprof.mean(),"held":(D.pos.abs()>0).mean()})
    return out
