def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            vol=r.rolling(20).std().shift(1)
            z=r/vol
            vr=b["volume"]/b["volume"].rolling(30).mean().shift(1)
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            wick=(np.minimum(b["open"],c)-b["low"])/rng
            uw=(b["high"]-np.maximum(b["open"],c))/rng
            r5=c/c.shift(5)-1
            for h in (1,3,7):
                fwd=c.shift(-h)/c-1
                grid=(np.arange(len(b))%h==0)
                d=pd.DataFrame({"coin":coin,"w":w,"h":h,"z":z,"vr":vr,"wick":wick,"uw":uw,"vol":vol,"r5":r5,
                                "fwd":fwd,"grid":grid,"wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                                "flush":(b["forecast"]>0).values})
                rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D=D[D.grid].dropna(subset=["fwd","z"])
    D["ex"]=D["fwd"]-D.groupby(["coin","h"])["fwd"].transform("mean")
    out={}
    def summ(g):
        return pd.Series({"n":len(g),"mean_ex":g.ex.mean(),"t":g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    D["zb"]=pd.cut(D.z,[-np.inf,-2.5,-1.5,-0.5,0.5,1.5,2.5,np.inf])
    out["fwd_by_zbucket"]=D.groupby(["h","zb"],observed=True).apply(summ).unstack(0)
    falls=D[D.z<=-1].copy()
    falls["vrb"]=pd.cut(falls.vr,[0,1,2,4,np.inf]); falls["wb"]=pd.cut(falls.wick,[-0.01,0.15,0.333,0.6,1.01])
    out["falls_by_volratio"]=falls.groupby(["h","vrb"],observed=True).apply(summ).unstack(0)
    out["falls_by_wick"]=falls.groupby(["h","wb"],observed=True).apply(summ).unstack(0)
    ups=D[D.z>=1].copy(); ups["vrb"]=pd.cut(ups.vr,[0,1,2,4,np.inf]); ups["ub"]=pd.cut(ups.uw,[-0.01,0.15,0.333,0.6,1.01])
    out["ups_by_volratio"]=ups.groupby(["h","vrb"],observed=True).apply(summ).unstack(0)
    out["ups_by_upperwick"]=ups.groupby(["h","ub"],observed=True).apply(summ).unstack(0)
    D["vb"]=D.groupby(["coin","h"])["vol"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["fwd_by_voltercile"]=D.groupby(["h","vb"]).apply(summ).unstack(0)
    D["r5b"]=D.groupby(["coin","h"])["r5"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["fwd_by_r5quintile"]=D.groupby(["h","r5b"]).apply(summ).unstack(0)
    d1=D[D.h==1]
    out["fwd1_by_weekday"]=d1.groupby("wd").apply(summ)
    out["fwd_by_coin_h3_r5q"]=D[D.h==3].groupby(["coin","r5b"]).ex.mean().unstack()
    # book
    bk=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            bk.append(d.assign(coin=coin,w=w))
    B=pd.concat(bk).dropna(subset=["book_return"])
    out["book_by_coin"]=B.groupby("coin").agg(mean=("book_return","mean"),sd=("book_return","std"),n=("book_return","size"),nz=("book_return",lambda s:(s.abs()>1e-9).sum()))
    return out
