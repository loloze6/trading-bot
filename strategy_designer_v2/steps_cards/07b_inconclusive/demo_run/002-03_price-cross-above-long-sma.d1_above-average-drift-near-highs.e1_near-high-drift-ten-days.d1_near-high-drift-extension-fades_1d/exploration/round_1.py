def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            lo=c.rolling(20).min(); hi=c.rolling(20).max()
            rp=(c-lo)/(hi-lo)
            r30=c/c.shift(30)-1
            yr=pd.to_datetime(b["timestamp"]).dt.year
            for h in (5,10,20):
                fwd=c.shift(-h)/c-1
                for i in range(0,len(b),h):
                    if i+h<len(b):
                        rows.append(dict(coin=coin,w=w,h=h,year=int(yr[i]),reg=b["regime"].iloc[i],
                            fc=float(b["forecast"].iloc[i]) if pd.notna(b["forecast"].iloc[i]) else np.nan,
                            rp=rp[i],r30=r30[i],fwd=fwd[i]))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby(["coin","h"])["fwd"].transform("mean")
    def slope(g,x):
        g=g.dropna(subset=[x,"ex"])
        if len(g)<10 or g[x].std()==0: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        r=stats.linregress(g[x],g["ex"]); return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    out={}
    tr=d[d.reg=="trending"]
    out["fc_slope_by_h"]=tr.groupby("h").apply(lambda g:slope(g,"fc"))
    out["rp_slope_by_h_reg"]=d.groupby(["h","reg"]).apply(lambda g:slope(g,"rp"))
    t10=tr[tr.h==10]
    out["fc10_by_coin"]=t10.groupby("coin").apply(lambda g:slope(g,"fc"))
    out["fc10_by_year"]=t10.groupby("year").apply(lambda g:slope(g,"fc"))
    t10=t10.copy(); t10["q"]=pd.qcut(t10["fc"].rank(method="first"),5,labels=False)
    out["fc10_quint"]=t10.groupby("q").agg(n=("ex","size"),fc=("fc","mean"),ex=("ex","mean"),fwd=("fwd","mean"))
    t10["rq"]=pd.qcut(t10["r30"].rank(method="first"),5,labels=False)
    out["r30_quint_trend"]=t10.groupby("rq").agg(n=("ex","size"),r30=("r30","mean"),ex=("ex","mean"))
    a10=d[d.h==10].copy(); a10["rq"]=pd.qcut(a10["rp"].rank(method="first"),5,labels=False)
    out["rp_quint_all_by_reg"]=a10.dropna(subset=["rp"]).groupby(["reg","rq"]).agg(n=("ex","size"),rp=("rp","mean"),ex=("ex","mean"))
    out["share_trending"]=float((d[d.h==10].reg=="trending").mean())
    return out
