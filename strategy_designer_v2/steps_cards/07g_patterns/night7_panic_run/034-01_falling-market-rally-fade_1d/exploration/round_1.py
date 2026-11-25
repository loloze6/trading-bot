def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b))})
            df["z1"]=r/sd
            df["z3"]=(c/c.shift(3)-1)/(sd*np.sqrt(3))
            df["z10"]=(c/c.shift(10)-1)/(sd*np.sqrt(10))
            df["ret60"]=c/c.shift(60)-1
            df["falling"]=(b["regime"]=="unknown").astype(int)
            df["f1"]=c.shift(-1)/c-1
            df["f3"]=c.shift(-3)/c-1
            df["f5"]=c.shift(-5)/c-1
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            df["clv"]=(b["close"]-b["low"])/rng
            df["rangez"]=(rng/c.shift(1))/sd
            df["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            df["sdlvl"]=sd
            df["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    out={}
    def tab(D,col,key,q=None,bins=None):
        D=D.dropna(subset=[key,col])
        drift=A.loc[A.pos%3==0,"f3"].mean() if col=="f3" else A[col].mean()
        g=pd.qcut(D[key],q,duplicates="drop") if q else pd.cut(D[key],bins)
        res=D.groupby(g,observed=True)[col].agg(lambda x:(x-drift).mean()*100).to_frame("ex%")
        res["t"]=D.groupby(g,observed=True)[col].apply(lambda x:(x-drift).mean()/(x.std()/np.sqrt(len(x))))
        res["n"]=D.groupby(g,observed=True)[col].size()
        return res.round(3)
    G=A[A.pos%3==0]
    bins=[-99,-2,-1,-0.3,0.3,1,2,99]
    out["f3 by z1, falling"]=tab(G[G.falling==1],"f3","z1",bins=bins)
    out["f3 by z1, not falling"]=tab(G[G.falling==0],"f3","z1",bins=bins)
    out["f3 by z10, falling"]=tab(G[G.falling==1],"f3","z10",bins=[-99,-2,-1,0,1,2,99])
    out["f3 by z10, not falling"]=tab(G[G.falling==0],"f3","z10",bins=[-99,-2,-1,0,1,2,99])
    out["f3 by clv all"]=tab(G,"f3","clv",q=5)
    out["f3 by rangez all"]=tab(G,"f3","rangez",q=5)
    out["f3 by ret60 all"]=tab(G,"f3","ret60",bins=[-9,-0.3,-0.1,0.1,0.3,0.6,99])
    out["f1 by weekday"]=tab(A,"f1","wd",bins=[-1,0,1,2,3,4,5,6])
    G2=A[A.pos%5==0]
    out["f5 by z1, all"]=tab(G2,"f5","z1",bins=bins)
    # slopes
    sl={}
    for nm,D in [("fall",G[G.falling==1]),("notfall",G[G.falling==0]),("all",G)]:
        for k in ["z1","z3","z10","clv","rangez"]:
            d=D.dropna(subset=[k,"f3"])
            s=stats.linregress(d[k],d["f3"])
            sl[f"{nm}_{k}"]=(round(s.slope*100,4),round(s.slope/s.stderr,2),len(d))
    out["slopes f3 (%/unit,t,n)"]=pd.DataFrame(sl,index=["slope","t","n"]).T
    # book
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()],ignore_index=True)
    out["trades"]=tr.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median"])
    dy=pd.concat([d.assign(coin=c,w=w) for c,ws in data["days"].items() for w,d in ws.items()])
    bk=dy.groupby(["w","day"])["book_return"].mean()
    out["book by window: mean%, sharpe"]=bk.groupby(level=0).agg(lambda x:x.mean()*100).to_frame("mean%").join(bk.groupby(level=0).agg(lambda x:x.mean()/x.std()*np.sqrt(365) if x.std()>0 else np.nan).rename("sh")).round(3)
    return out
