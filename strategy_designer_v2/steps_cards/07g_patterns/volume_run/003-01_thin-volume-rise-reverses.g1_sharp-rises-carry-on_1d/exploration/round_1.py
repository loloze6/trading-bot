def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; v=b["volume"]
            r1=c.pct_change()
            vol=r1.rolling(20,min_periods=15).std()
            z=r1/vol
            vr=v/v.rolling(20,min_periods=15).mean()
            r5p=c/c.shift(5)-1
            z5=r5p/(vol*np.sqrt(5))
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            volrank=vol/vol.expanding().median()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"z":z,"vr":vr,"z5":z5,
                            "f5":f5,"f1":f1,"volrank":volrank,"wd":ts.dt.dayofweek,"yr":ts.dt.year,
                            "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"]})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[D.pos%5==0].dropna(subset=["f5","z"]).copy()
    G["ex"]=G["f5"]-G.groupby("coin")["f5"].transform("mean")
    def summ(g,col="ex"):
        x=g[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    G["zb"]=pd.cut(G.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    out["ex5 by z bucket"]=G.groupby("zb").apply(summ)
    G["vrb"]=pd.qcut(G.vr,3,labels=["thin","mid","heavy"])
    G["zs"]=pd.cut(G.z,[-99,-1,1,99],labels=["bigdown","small","bigup"])
    out["ex5 by bigmove x volume"]=G.groupby(["zs","vrb"]).apply(summ)
    G["z5b"]=pd.qcut(G.z5,5)
    out["ex5 by 5d z quintile"]=G.groupby("z5b").apply(summ)
    G["vlb"]=pd.qcut(G.volrank,3,labels=["lowvol","midvol","highvol"])
    out["ex5 by vol level"]=G.groupby("vlb").apply(summ)
    out["ex5 by coin"]=G.groupby("coin").apply(summ)
    out["corr z ex by coin t"]=G.groupby("coin").apply(lambda g: pd.Series({"slope_t":stats.linregress(g.z,g.ex).rvalue*np.sqrt((len(g)-2)/(1-stats.linregress(g.z,g.ex).rvalue**2)),"n":len(g)}))
    # 1-day
    D1=D.dropna(subset=["f1","z"]).copy()
    D1["ex1"]=D1.f1-D1.groupby("coin")["f1"].transform("mean")
    out["ex1 by weekday"]=D1.groupby("wd").apply(lambda g: summ(g,"ex1"))
    D1["zb"]=pd.cut(D1.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    out["ex1 by z bucket"]=D1.groupby("zb").apply(lambda g: summ(g,"ex1"))
    # book
    br=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; br.append(d)
    B=pd.concat(br,ignore_index=True)
    out["book by coin"]=B.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    # market vs timing: alloc on bar t times coin mean daily return
    mu=D.groupby("coin")["f1"].mean()
    D["mkt"]=D["alloc"]*D["coin"].map(mu)
    D["gain"]=D["alloc"]*D["f1"]
    out["gain decomposition"]=D.groupby("coin").agg(gain=("gain","mean"),mkt=("mkt","mean"),avg_alloc=("alloc","mean"),share_in=("alloc",lambda a:(a.abs()>0.01).mean()))
    out["gain by fc bucket"]=D.assign(fb=pd.cut(D.fc,[-1,0.01,5,10,20.1])).groupby("fb").apply(lambda g: pd.Series({"n":len(g),"gain":g.gain.mean(),"f1":g.f1.mean(),"alloc":g.alloc.mean()}))
    return out
