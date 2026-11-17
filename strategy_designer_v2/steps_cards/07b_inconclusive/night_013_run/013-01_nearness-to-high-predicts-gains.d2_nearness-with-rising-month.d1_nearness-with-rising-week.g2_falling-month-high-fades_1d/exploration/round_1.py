def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].values
            n=len(c)
            ret30=pd.Series(c).pct_change(30).values
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [3,7,14,30]:
                for i in range(0,n-h,h):
                    r=c[i+h]/c[i]-1
                    act = (ret30[i]<0) if not np.isnan(ret30[i]) else (df["regime"].iloc[i]=="mean_reversion")
                    rows.append(dict(coin=coin,w=w,h=h,i=i,fwd=r,act=act,fc=df["forecast"].iloc[i],
                                     yr=yr[i],r30=ret30[i]))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby(["coin","h"])["fwd"].transform("mean")
    a=d[d.act & d.fc.notna()]
    out={}
    def slope(g):
        if len(g)<10 or g.fc.std()==0: return pd.Series(dict(n=len(g),slope=np.nan,t=np.nan))
        s=stats.linregress(g.fc,g.ex)
        return pd.Series(dict(n=len(g),slope=s.slope,t=s.slope/s.stderr))
    out["by_h"]=a.groupby("h").apply(slope)
    a7=a[a.h==7].copy()
    out["by_coin7"]=a7.groupby("coin").apply(slope)
    out["by_year7"]=a7.groupby("yr").apply(slope)
    a7["q"]=pd.qcut(a7.fc.rank(method="first"),5,labels=False)
    out["quint7"]=a7.groupby("q").agg(n=("ex","size"),fc=("fc","mean"),ex=("ex","mean"),sd=("ex","std"))
    a7["r30q"]=pd.qcut(a7.r30.rank(method="first"),3,labels=False)
    out["by_r30tercile7"]=a7.groupby("r30q").apply(slope)
    out["fc_zero_share"]=float((a7.fc==0).mean())
    for h in [14,30]:
        ah=a[a.h==h].copy()
        ah["q"]=pd.qcut(ah.fc.rank(method="first"),3,labels=False)
        out[f"terc_h{h}"]=ah.groupby("q").agg(n=("ex","size"),ex=("ex","mean"))
    return out
