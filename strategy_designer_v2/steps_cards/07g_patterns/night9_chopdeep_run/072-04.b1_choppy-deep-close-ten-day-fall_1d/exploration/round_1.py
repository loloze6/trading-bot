def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std()
            hi=c.rolling(20).max()
            depth=(c/hi-1)/sd
            ch=(b["regime"]=="unknown")
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"depth":depth,"choppy":ch,
                            "r0":r,"z0":r/sd.shift(1),
                            "rng":(b["high"]-b["low"])/c/sd,
                            "clv":(c-b["low"])/(b["high"]-b["low"]),
                            "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                            "alloc":b["postRebalance_current_allocation"]})
            for h in (1,3,10):
                d[f"f{h}"]=c.shift(-h)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in (1,3,10):
        g=D[D.pos%h==0]
        drift=g.groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"]=D[f"f{h}"]-D.coin.map(drift)
        D[f"g{h}"]=(D.pos%h==0)
    def summ(df,h,by):
        s=df[df[f"g{h}"]].dropna(subset=[f"x{h}"])
        o=s.groupby(by)[f"x{h}"].agg(["mean","count","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        return o.drop(columns="std").round(4)
    D["dq"]=pd.qcut(D.depth,5,labels=False)
    D["zq"]=pd.cut(D.z0,[-99,-2,-1,0,1,2,99])
    D["rq"]=pd.qcut(D.rng,5,labels=False)
    D["up"]=D.r0>0
    out={}
    out["depth_q x choppy, 10d"]=summ(D,10,["choppy","dq"])
    out["depth_q x choppy, 1d"]=summ(D,1,["choppy","dq"])
    out["depth_q x up, choppy, 1d"]=summ(D[D.choppy],1,["up","dq"])
    out["z0 x choppy, 1d"]=summ(D,1,["choppy","zq"])
    out["z0 x choppy, 3d"]=summ(D,3,["choppy","zq"])
    out["range_q x up, 1d"]=summ(D,1,["up","rq"])
    out["weekday, 1d"]=summ(D,1,["wd"])
    out["weekday x choppy, 1d"]=summ(D,1,["choppy","wd"])
    out["depth range"]=D.groupby("dq").depth.agg(["min","max"]).round(2)
    # book
    dr=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy();x["coin"]=coin;x["w"]=w;dr.append(x)
    Y=pd.concat(dr)
    bk=Y.groupby(["w","day"]).book_return.mean().reset_index()
    bk["wd"]=pd.to_datetime(bk.day).dt.weekday
    out["book by window"]=bk.groupby("w").book_return.agg(["mean","count"]).round(5)
    return out
