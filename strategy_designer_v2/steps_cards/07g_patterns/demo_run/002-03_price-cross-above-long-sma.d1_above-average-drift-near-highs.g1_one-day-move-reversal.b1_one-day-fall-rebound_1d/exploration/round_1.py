def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            v=r.rolling(20,min_periods=15).std()
            d=pd.DataFrame({"coin":c,"win":w,"z":r/v,"r1":r,"vol":v,
                "r5p":cl/cl.shift(5)-1,"r20p":cl/cl.shift(20)-1,
                "f1":cl.shift(-1)/cl-1,"f3":cl.shift(-3)/cl-1,"f5":cl.shift(-5)/cl-1,
                "pos":b["postRebalance_current_allocation"],
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,"i":np.arange(len(b))})
            d["volrank"]=v.rolling(120,min_periods=40).rank(pct=True)
            d["rngz"]=((b["high"]-b["low"])/cl)/((b["high"]-b["low"])/cl).rolling(20).mean()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    cm=D.groupby("coin")["f1"].mean()
    D["x1"]=D["f1"]-D["coin"].map(cm)
    def summ(g,col="x1"):
        x=g[col].dropna(); n=len(x)
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    D["zb"]=pd.cut(D["z"],[-99,-2.5,-1.5,-1,-0.5,0,0.5,1,1.5,2.5,99])
    out["next-day excess by z bin"]=D.groupby("zb").apply(summ)
    F=D[D.z<0].copy()
    F["vt"]=pd.cut(F["volrank"],[0,1/3,2/3,1.01],labels=["lowvol","mid","high"])
    out["falls: slope f1 on -z by vol tercile"]=F.dropna(subset=["vt","x1"]).groupby("vt").apply(
        lambda g: pd.Series({"n":len(g),"corr":np.corrcoef(-g.z,g.x1)[0,1],"meanx":g.x1.mean()}))
    F["tr"]=pd.cut(F["r20p"],[-9,-0.1,0,0.1,99])
    out["falls: by 20d trend"]=F.dropna(subset=["tr"]).groupby("tr").apply(
        lambda g: pd.Series({"n":len(g),"corr":np.corrcoef(-g.z,g.x1)[0,1] if len(g)>5 else np.nan,"meanx":g.x1.mean()}))
    out["by coin falls corr"]=F.dropna(subset=["x1"]).groupby("coin").apply(
        lambda g: pd.Series({"n":len(g),"corr":np.corrcoef(-g.z,g.x1)[0,1],"t":summ(g)["t"]}))
    out["weekday all"]=D.groupby("wd").apply(summ)
    res=[]
    for h in [3,5]:
        G=D[D.i%h==0].dropna(subset=["z","f"+str(h)]).copy()
        G["q"]=pd.qcut(G["z"],5,labels=False)
        for q,g in G.groupby("q"):
            x=g["f"+str(h)]-g["coin"].map(G.groupby("coin")["f"+str(h)].mean())
            res.append({"h":h,"zq":q,"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out["h-day excess by z quintile (nonoverlap)"]=pd.DataFrame(res)
    G=D[D.i%5==0].dropna(subset=["r5p","f5"]).copy()
    G["q"]=G.groupby("coin")["r5p"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["5d fwd by 5d past ret quintile"]=G.groupby("q").apply(lambda g: summ(g.assign(y=g.f5-g.coin.map(G.groupby('coin')['f5'].mean())),"y"))
    D["rq"]=pd.qcut(D["rngz"],5,labels=False)
    out["next-day excess by range/avg range quintile"]=D.groupby("rq").apply(summ)
    dd=[]
    for c,ws in data["days"].items():
        for w,t in ws.items():
            dd.append(t.assign(coin=c,win=w))
    Y=pd.concat(dd)
    bk=Y.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book vs coins"]=pd.Series({"book_mean":bk.book_return.mean(),"coin_mean":bk.coin_return.mean(),
        "corr":bk.corr().iloc[0,1],"book_sd":bk.book_return.std(),"coin_sd":bk.coin_return.std()})
    out["book by window mean*1e4"]=(bk.groupby("win")["book_return"].mean()*1e4).round(1)
    return out
