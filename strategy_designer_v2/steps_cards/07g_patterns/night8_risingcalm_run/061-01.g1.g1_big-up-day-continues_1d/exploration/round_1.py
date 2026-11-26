def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z=r/sd
            fwd=c.shift(-H)/c-1
            fwd1=c.shift(-1)/c-1
            ret60=c/c.shift(60)-1
            rng=(b["high"]-b["low"])/c
            clv=(c-b["low"])/(b["high"]-b["low"])
            vol=b["volume"].astype(float); vz=vol/vol.rolling(30,min_periods=20).mean()
            r5p=c/c.shift(5)-1
            rv=b["sizing_realised_vol"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"fwd":fwd,"fwd1":fwd1,
                            "ret60":ret60,"clv":clv,"vz":vz,"r5p":r5p,"rv":rv,"r":r,"sd":sd,
                            "wd":ts.dt.dayofweek,"alloc":b["postRebalance_current_allocation"],"fc":b["forecast"]})
            rows.append(d)
    A=pd.concat(rows)
    drift=A.loc[A.pos%H==0].groupby("coin")["fwd"].mean()
    A["ex"]=A["fwd"]-A["coin"].map(drift)
    G=A[(A.pos%H==0)].dropna(subset=["z","ex"])
    def tab(g,col):
        o=g.groupby(col)["ex"].agg(["count","mean","std"])
        o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
        return o
    out={}
    G["zb"]=pd.cut(G.z,[-99,-2,-1,-0.5,0,0.5,1,2,99])
    out["ex5 by z"]=tab(G,"zb")
    G["vlev"]=pd.qcut(G.sd,3,labels=["lowvol","mid","hivol"])
    G["zs"]=np.sign(G.z)
    out["ex5 by vol x zsign"]=G.groupby(["vlev","zs"])["ex"].agg(["count","mean"])
    G["tr"]=pd.cut(G.ret60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    G["big"]=pd.cut(G.z,[-99,-1.5,1.5,99],labels=["bigdn","mid","bigup"])
    o=G.groupby(["tr","big"])["ex"].agg(["count","mean","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["ex5 trend x big"]=o
    G["r5b"]=pd.qcut(G.r5p,5)
    out["ex5 by past5 quintile"]=tab(G,"r5b")
    G["clvb"]=pd.qcut(G.clv,4)
    out["ex5 by close location"]=tab(G,"clvb")
    G["vzb"]=pd.qcut(G.vz,4)
    out["ex5 by vol surge"]=tab(G,"vzb")
    D=A.dropna(subset=["fwd1"]).copy()
    D["ex1"]=D.fwd1-D.groupby("coin").fwd1.transform("mean")
    o=D.groupby("wd")["ex1"].agg(["count","mean","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["next day by weekday"]=o
    D["zb"]=pd.cut(D.z,[-99,-2,-1,0,1,2,99])
    o=D.groupby("zb")["ex1"].agg(["count","mean","std"]);o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    out["next day by z"]=o
    out["ex5 by window"]=G.groupby("w")["ex"].mean()
    # book on days: largest gains/losses
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            dd.append(x.assign(coin=coin,w=w))
    Dd=pd.concat(dd)
    bk=Dd.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book vs coin corr"]=float(bk.corr().iloc[0,1])
    q=bk.book_return.quantile([0.05,0.95])
    out["coin ret on worst5% book days"]=float(bk.loc[bk.book_return<q.iloc[0],"coin_return"].mean())
    out["coin ret on best5% book days"]=float(bk.loc[bk.book_return>q.iloc[1],"coin_return"].mean())
    out["mean alloc"]=float(A.alloc.mean())
    return out
