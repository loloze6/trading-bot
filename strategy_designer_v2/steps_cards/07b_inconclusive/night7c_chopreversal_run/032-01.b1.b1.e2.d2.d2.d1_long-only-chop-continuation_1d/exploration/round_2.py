def explore(data):
    import numpy as np, pandas as pd
    H=7
    grid=[]; rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            vol30=r.rolling(30).std()
            r60=c/c.shift(60)-1
            r30=c/c.shift(30)-1
            ts=pd.to_datetime(b["timestamp"])
            n=len(b)
            for i in range(0,n-H,H):
                ret=c.iloc[i+H]/c.iloc[i]-1
                f=b["forecast"].iloc[i]
                rec=dict(coin=coin,w=w,year=ts.iloc[i].year,f=f,ret=ret,vol=vol30.iloc[i],
                         r60=r60.iloc[i],r30=r30.iloc[i],day=str(ts.iloc[i])[:10])
                grid.append(rec)
    g=pd.DataFrame(grid)
    cm=g.groupby("coin").ret.mean()
    g["u"]=g.ret-g.coin.map(cm)
    # coin-year mean of all grid cases (market's own move in that year)
    cy=g.groupby(["coin","year"]).ret.mean()
    g["cyr"]=[cy[(a,b)] for a,b in zip(g.coin,g.year)]
    g["ex_cy"]=g.ret-g.cyr
    def ct(df,col):
        x=df.dropna(subset=[col])
        if len(x)<3: return pd.Series(dict(n=len(x),days=0,mean=np.nan,t=np.nan))
        s=x.groupby("day")[col].sum(); D=len(s)
        m=x[col].mean(); N=len(x)
        se=np.sqrt((s-s.mean()*0).pow(2).sum()*0+((x.groupby("day")[col].sum()-x.groupby("day")[col].count()*m)**2).sum()*D/(D-1))/N
        return pd.Series(dict(n=N,days=D,mean=m,t=m/se))
    a=g[g.f>0].copy()
    out={}
    out["active_u_clustered"]=ct(a,"u")
    out["active_ex_coinyear_clustered"]=ct(a,"ex_cy")
    out["all_u_by_year"]=g.groupby("year").apply(lambda x: ct(x,"u"))
    out["active_u_by_year"]=a.groupby("year").apply(lambda x: ct(x,"u"))
    out["active_excy_by_year"]=a.groupby("year").apply(lambda x: ct(x,"ex_cy"))
    a["r60q"]=pd.qcut(a.r60,3,labels=False)
    out["active_u_by_r60"]=a.groupby("r60q").apply(lambda x: ct(x,"u"))
    out["active_r60_cut_means"]=a.groupby("r60q").r60.mean()
    a["fq"]=pd.qcut(a.f,3,labels=False)
    out["f_tercile_excy"]=a.groupby("fq").apply(lambda x: ct(x,"ex_cy"))
    a["vq"]=pd.qcut(a.vol,3,labels=False)
    out["vol_tercile_excy"]=a.groupby("vq").apply(lambda x: ct(x,"ex_cy"))
    out["r60sign_u"]=a.groupby(a.r60>0).apply(lambda x: ct(x,"u"))
    # inactive bars with positive 7d and 30d in coin's same year for comparison
    out["inactive_u"]=ct(g[g.f<=0],"u")
    return out
