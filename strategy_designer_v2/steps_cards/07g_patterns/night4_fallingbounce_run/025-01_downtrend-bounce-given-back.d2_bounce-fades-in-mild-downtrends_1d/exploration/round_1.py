def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vol=r.rolling(20).std()
            z=r/vol
            r90=c/c.shift(90)-1
            r30=c/c.shift(30)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            vq=vol/vol.rolling(120,min_periods=60).median()
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            idx=np.arange(len(b))
            d=pd.DataFrame(dict(coin=coin,w=w,z=z,r90=r90,r30=r30,f5=f5,f1=f1,vq=vq,wd=wd,
                                grid=(idx%5==0),fc=b["forecast"].astype(float),
                                pos=b["postRebalance_current_allocation"].astype(float)))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D[D.grid].groupby("coin")["f5"].mean()
    sd=D[D.grid].groupby("coin")["f5"].std()
    D["u5"]=(D["f5"]-D["coin"].map(drift))/D["coin"].map(sd)
    G=D[D.grid].dropna(subset=["z","u5","r90"])
    out={}
    G["zb"]=pd.cut(G.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    G["reg"]=np.where(G.r90<0,"down90","up90")
    def agg(g):
        return pd.Series(dict(n=len(g),mean_u5=g.u5.mean(),t=g.u5.mean()/(g.u5.std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out["u5 strength by z bucket x regime"]=G.groupby(["reg","zb"]).apply(agg)
    G["r90b"]=pd.qcut(G.r90,5)
    out["u5 by r90 quintile"]=G.groupby("r90b").apply(agg)
    G["r30b"]=pd.qcut(G.r30,5)
    out["u5 by r30 quintile"]=G.dropna(subset=["r30"]).groupby("r30b").apply(agg)
    G["vqb"]=pd.qcut(G.vq,4)
    out["u5 by vol ratio quartile"]=G.dropna(subset=["vq"]).groupby("vqb").apply(agg)
    out["u5 by weekday"]=G.groupby("wd").apply(agg)
    out["u5 by coin x reg"]=G.groupby(["coin","reg"]).apply(agg)
    # corr z with u5 per regime
    for reg in ["down90","up90"]:
        g=G[G.reg==reg]
        s=stats.linregress(g.z,g.u5)
        out[f"slope u5 on z {reg}"]=f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(g)}"
    # 1-day next return after z, all bars (overlap fine for 1d)
    A=D.dropna(subset=["z","f1"])
    A["zb"]=pd.cut(A.z,[-99,-2,-1,1,2,99])
    out["next1d ret by z all bars"]=A.groupby("zb")["f1"].agg(["count","mean"])
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy();x["coin"]=coin;x["w"]=w;dd.append(x)
    DD=pd.concat(dd).dropna(subset=["book_return"])
    out["book mean by window"]=DD.groupby("w")["book_return"].mean().to_frame()
    out["book by coin"]=DD.groupby("coin")["book_return"].agg(["mean","std","count"])
    return out
