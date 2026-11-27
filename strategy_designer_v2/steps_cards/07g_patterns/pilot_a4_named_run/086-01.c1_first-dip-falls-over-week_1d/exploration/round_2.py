def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"];o=b["open"];h=b["high"];l=b["low"]
            r1=c.pct_change()
            up=(r1>0).astype(int)
            streak=up.groupby((up!=up.shift()).cumsum()).cumsum()*up
            f=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "inprof":(b["regime"]!="chop").values,
                "r1":r1,"upstreak":streak,
                "clpos":(c-l)/(h-l).replace(0,np.nan),
                "z1":r1/r1.rolling(30).std(),
                "yr":pd.to_datetime(b["timestamp"]).dt.year})
            for H in (1,2,3,5,7,10,14):
                f[f"fw{H}"]=c.shift(-H)/c-1
            rows.append(f)
    d=pd.concat(rows,ignore_index=True)
    out={}
    def ex(H,off=0):
        drift=d.groupby("coin")[f"fw{H}"].apply(lambda s: s[d.loc[s.index,"pos"]%H==0].mean())
        g=d[((d.pos-off)%H==0)&d.inprof].copy()
        g["ex"]=-(g[f"fw{H}"]-g.coin.map(drift))
        return g.dropna(subset=["ex"])
    def sp(x,feat):
        x=x.dropna(subset=[feat])
        if len(x)<15: return (len(x),np.nan,np.nan)
        rho,_=stats.spearmanr(x[feat],x.ex); n=len(x)
        return (n,rho,rho*np.sqrt((n-2)/(1-rho**2)))
    res=[]
    for feat in ["clpos","r1","upstreak"]:
        for H in (1,2,3,5,7,10,14):
            n,rho,t=sp(ex(H),feat); res.append((feat,H,"off0",n,rho,t))
        for off in range(1,7):
            n,rho,t=sp(ex(7,off),feat); res.append((feat,7,f"off{off}",n,rho,t))
    out["horizon and offset"]=pd.DataFrame(res,columns=["feat","H","grid","n","rho","t"]).round(3)
    # clpos 7d by coin and by year (pooled over all offsets, overlapping -> rho only)
    res=[]
    for off in range(7):
        g=ex(7,off)
        for k,x in g.groupby("coin"):
            n,rho,t=sp(x,"clpos"); res.append(("coin",k,off,n,rho))
        for k,x in g.groupby("yr"):
            n,rho,t=sp(x,"clpos"); res.append(("yr",k,off,n,rho))
    r=pd.DataFrame(res,columns=["by","k","off","n","rho"])
    out["clpos 7d rho by coin/year, mean over offsets"]=r.groupby(["by","k"]).agg(n=("n","mean"),rho=("rho","mean"),pos_share=("rho",lambda s:(s>0).mean())).round(3)
    # clpos terciles 7d, all offsets pooled, on down days vs up days
    allg=pd.concat([ex(7,o) for o in range(7)])
    allg["q"]=pd.qcut(allg.clpos.rank(method="first"),5,labels=False)
    allg["dn"]=allg.r1<0
    out["clpos quintile 7d short ex (pooled offsets)"]=allg.groupby(["dn","q"])["ex"].agg(["count","mean"]).round(4)
    # upstreak 1d by streak length, day-clustered style simple
    g=ex(1); g["s"]=g.upstreak.clip(upper=5)
    out["upstreak 1d"]=g.groupby("s")["ex"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))]).round(4)
    for k,x in g.groupby("coin"):
        out[f"upstreak 1d rho {k}"]=str(sp(x,"upstreak"))
    return out
