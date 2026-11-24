def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            rng=(b.high-b.low)
            b["rr"]=rng/rng.rolling(20,min_periods=20).mean()
            b["r5"]=b.close/b.close.shift(5)-1
            b["r1"]=b.close/b.close.shift(1)-1
            b["vol20"]=b.r1.rolling(20).std()
            b["fwd"]=b.close.shift(-3)/b.close-1
            b["fwd1"]=b.close.shift(-1)/b.close-1
            b["pos"]=b.postRebalance_current_allocation
            b["gain"]=b.pos*b.fwd1
            ts=pd.to_datetime(b.timestamp)
            b["wd"]=ts.dt.weekday; b["yr"]=ts.dt.year; b["day"]=ts.dt.floor("D")
            b["coin"]=coin; b["win"]=w
            b["wn"]=int(w[1:])
            b["grid"]=(np.arange(len(b))%3==0)
            rows.append(b)
    a=pd.concat(rows)
    mu=a[a.grid].groupby("coin").fwd.mean()
    a["ex"]=a.fwd-a.coin.map(mu)
    mu1=a.groupby("coin").fwd1.mean()
    a["ex1"]=a.fwd1-a.coin.map(mu1)
    def ct(df,col="ex"):
        df=df.dropna(subset=[col])
        m=df[col].mean()
        s=(df[col]-m).groupby(df.day).sum()
        G=len(s)
        se=np.sqrt((s**2).sum()*G/(G-1))/len(df)
        return pd.Series({"mean":round(m,4),"n":len(df),"days":G,"tclu":round(m/se,2)})
    out={}
    g=a[a.grid]
    out["wd 3d clustered"]=g.groupby("wd").apply(ct).unstack() if False else g.groupby("wd").apply(lambda x: ct(x))
    out["wd 1d next-day all bars clustered"]=a.groupby("wd").apply(lambda x: ct(x,"ex1"))
    out["wd next-day by year: Mon"]=a[a.wd==0].groupby("yr").apply(lambda x: ct(x,"ex1"))
    out["wd next-day by year: Sat(next=Sun?)"]=a[a.wd==6].groupby("yr").apply(lambda x: ct(x,"ex1"))
    out["wd next-day by coin"]=a.groupby(["coin","wd"]).ex1.mean().unstack().round(4)
    g=g.dropna(subset=["r5","vol20","rr","ex"]).copy()
    g["sr"]=g.r5/g.vol20
    g["srq"]=pd.qcut(g.sr,5,labels=False)
    g["rrq"]=pd.qcut(g.rr,3,labels=["narrow","midr","wide"])
    out["run strength q x range tercile, clustered"]=g.groupby(["srq","rrq"]).apply(lambda x: ct(x))
    out["run strength top q by window half"]=g[g.srq==4].groupby(g.wn>12).apply(lambda x: ct(x))
    # book days
    dd=pd.concat([df.assign(coin=c) for c,ws in data["days"].items() for w,df in ws.items()])
    br=dd.groupby("day").book_return.mean().dropna()
    out["book by weekday (daily ret mean %)"]=(br.groupby(pd.to_datetime(br.index).weekday).agg(["mean","count"])*[100,1]).round(3)
    # bar-level gain by weekday of position held
    out["position gain by weekday (bp)"]=(a.groupby("wd").gain.mean()*1e4).round(2)
    return out
