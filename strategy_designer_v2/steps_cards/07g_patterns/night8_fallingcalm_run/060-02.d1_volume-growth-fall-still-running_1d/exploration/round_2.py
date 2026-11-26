def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=pd.Series(b["close"].values.astype(float)); v=pd.Series(b["volume"].values.astype(float)); n=len(b)
            m1=v.rolling(30).mean(); m0=v.shift(30).rolling(30).mean()
            lvr=np.log(m1/m0)
            r1=c.pct_change(); r60=c.pct_change(60); r20=c.pct_change(20)
            dr=c.pct_change()
            sd30=dr.rolling(30).std()
            rng=(b["high"]-b["low"])/b["close"]
            clpos=(b["close"]-b["low"])/(b["high"]-b["low"])
            vr1=np.log(v/v.rolling(30).mean().shift(1))
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,n-H,H):
                rows.append(dict(coin=coin,w=w,fwd=c[i+H]/c[i]-1,reg=b["regime"].iloc[i],
                    lvr=lvr.iloc[i],r1=r1.iloc[i],r60=r60.iloc[i],r20=r20.iloc[i],sd30=sd30.iloc[i],
                    r1z=r1.iloc[i]/sd30.iloc[i] if sd30.iloc[i]>0 else np.nan,
                    rng=rng.iloc[i],clpos=clpos.iloc[i],vr1=vr1.iloc[i],yr=ts.iloc[i].year))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    d["usual"]=d.groupby("coin")["fwd"].transform("std")
    d["trend"]=np.where(d.r60>0.10,"rising",np.where(d.r60< -0.10,"falling",np.where(d.r60.notna(),"choppy",None)))
    sdmed=d.groupby("coin")["sd30"].transform("median")
    d["agit"]=np.where(d.sd30>sdmed,"agit","calm")
    out={}
    def slope(g,xc):
        g=g[[xc,"ex"]].dropna(); g=g[np.isfinite(g[xc])]
        if len(g)<20: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        r=stats.linregress(g[xc],g["ex"]); return pd.Series(dict(n=len(g),slope=r.slope,t=r.slope/r.stderr))
    nf=d[d.reg=="chop"]
    out["nonfall_lvr_by_trend"]=nf.groupby("trend").apply(lambda g: slope(g,"lvr"))
    out["nonfall_lvr_by_agit"]=nf.groupby("agit").apply(lambda g: slope(g,"lvr"))
    out["nonfall_lvr_by_year"]=nf.groupby("yr").apply(lambda g: slope(g,"lvr"))
    out["nonfall_lvr_by_coin"]=nf.groupby("coin").apply(lambda g: slope(g,"lvr"))
    nf2=nf.dropna(subset=["lvr"]).copy(); nf2["q"]=pd.qcut(nf2.lvr,5,labels=False)
    out["nonfall_lvr_quint"]=nf2.groupby("q").agg(n=("ex","size"),lvr=("lvr","mean"),ex=("ex","mean"),sd=("ex","std"))
    out["nonfall_r1z_by_trend"]=nf.groupby("trend").apply(lambda g: slope(g,"r1z"))
    out["nonfall_r1z_by_agit"]=nf.groupby("agit").apply(lambda g: slope(g,"r1z"))
    out["nonfall_r1z_by_year"]=nf.groupby("yr").apply(lambda g: slope(g,"r1z"))
    out["nonfall_r1z_by_coin"]=nf.groupby("coin").apply(lambda g: slope(g,"r1z"))
    nf3=nf.dropna(subset=["r1z"]).copy(); nf3["q"]=pd.qcut(nf3.r1z,5,labels=False)
    out["nonfall_r1z_quint"]=nf3.groupby("q").agg(n=("ex","size"),r1z=("r1z","mean"),ex=("ex","mean"))
    out["all_r1z_by_trend"]=d.groupby("trend").apply(lambda g: slope(g,"r1z"))
    out["all_lvr_by_trend_agit"]=d.groupby(["trend","agit"]).apply(lambda g: slope(g,"lvr"))
    out["all_vr1_by_trend"]=d.groupby("trend").apply(lambda g: slope(g,"vr1"))
    out["all_clpos_by_trend"]=d.groupby("trend").apply(lambda g: slope(g,"clpos"))
    # strength per case of nonfall lvr (short on growth)
    g=nf.dropna(subset=["lvr"])
    out["nonfall_lvr_sign_strength"]=pd.Series(dict(n=len(g),unusual=(-np.sign(g.lvr)*g.ex).mean(),strength=(-np.sign(g.lvr)*g.ex/g.usual).mean()))
    g=nf.dropna(subset=["r1z"])
    out["nonfall_r1_sign_strength"]=pd.Series(dict(n=len(g),unusual=(np.sign(g.r1z)*g.ex).mean(),strength=(np.sign(g.r1z)*g.ex/g.usual).mean()))
    return out
