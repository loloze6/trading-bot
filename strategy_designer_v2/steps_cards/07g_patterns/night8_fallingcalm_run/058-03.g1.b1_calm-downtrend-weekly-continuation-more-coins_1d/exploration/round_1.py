def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r5=c/c.shift(5)-1; r20=c/c.shift(20)-1
            vr=v.rolling(5).mean()/v.rolling(60,min_periods=20).mean()
            d1=c.pct_change(); sd=d1.rolling(20).std()
            rng=(b["high"]-b["low"])/c
            f5=c.shift(-5)/c-1
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            for i in range(0,len(b),5):
                rows.append(dict(coin=coin,w=w,i=i,ts=b["timestamp"].iloc[i],inp=b["regime"].iloc[i]=="unknown",
                    r5=r5.iloc[i],r20=r20.iloc[i],vr=vr.iloc[i],sd=sd.iloc[i],rng=rng.iloc[i],f5=f5.iloc[i],wd=wd.iloc[i],
                    d1=d1.iloc[i]))
    g=pd.DataFrame(rows).dropna(subset=["f5"])
    g["drift"]=g.groupby("coin")["f5"].transform("mean"); g["ex"]=g["f5"]-g["drift"]
    g["day"]=pd.to_datetime(g["ts"]).dt.floor("D")
    def tday(s,idx):
        x=s.groupby(g.loc[idx,"day"]).sum(); 
        return x.mean()/ (x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan
    out={}
    def tab(mask,col,q=5,name=None):
        h=g[mask].dropna(subset=[col]).copy()
        h["b"]=pd.qcut(h[col].rank(method="first"),q,labels=False)
        t=h.groupby("b").agg(n=("ex","size"),x=(col,"mean"),ex=("ex","mean"),f5=("f5","mean"))
        t["t"]=[tday(h.loc[h.b==k,"ex"],h.index[h.b==k]) for k in t.index]
        return t.round(4)
    out["inprof r5 quint"]=tab(g.inp,"r5")
    out["outprof r5 quint"]=tab(~g.inp,"r5")
    out["inprof r20 quint"]=tab(g.inp,"r20")
    out["outprof r20 quint"]=tab(~g.inp,"r20")
    out["inprof volratio quint"]=tab(g.inp,"vr")
    out["outprof volratio quint"]=tab(~g.inp,"vr")
    out["inprof sd20 quint"]=tab(g.inp,"sd")
    out["outprof sd20 quint"]=tab(~g.inp,"sd")
    out["all rng quint"]=tab(g.index==g.index,"rng")
    # interaction: in-profile, r5 sign x vol ratio half
    h=g[g.inp].dropna(subset=["r5","vr"]).copy()
    h["vhi"]=h.vr>h.vr.median(); h["dn"]=h.r5<0
    out["inprof dn x volhi"]=h.groupby(["dn","vhi"]).agg(n=("ex","size"),ex=("ex","mean"),r5=("r5","mean")).round(4)
    # weekday daily, all days
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    D=pd.concat(dd); D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    D["cm"]=D.groupby("coin")["coin_return"].transform("mean"); D["cx"]=D.coin_return-D.cm
    out["weekday coin ex"]=D.groupby("wd").agg(n=("cx","size"),cx=("cx","mean"),sd=("cx","std"),book=("book_return","mean")).assign(t=lambda x:x.cx/(x.sd/np.sqrt(x.n))).round(5)
    out["book by window"]=D.groupby("w").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("coin","size")).round(5)
    out["share inprof grid"]=float(g.inp.mean())
    return out
