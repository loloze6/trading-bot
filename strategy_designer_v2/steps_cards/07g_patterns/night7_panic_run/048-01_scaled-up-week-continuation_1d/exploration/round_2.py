def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=3
    rows=[]
    for coin, wins in data["bars"].items():
        allg=[]
        for w,b in wins.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H): allg.append(c[i+H]/c[i]-1)
        drift=np.mean(allg); usual=np.std(allg)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd30=r.rolling(30,min_periods=20).std()
            z7=(c/c.shift(7)-1)/(sd30*np.sqrt(7))
            tr60=c/c.shift(60)-1
            volrel=sd30/sd30.rolling(60,min_periods=30).median()
            fwd=c.shift(-H)/c-1
            alloc=b["postRebalance_current_allocation"]
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,len(b)-H,H):
                rows.append(dict(coin=coin,w=w,day=ts[i].normalize(),yr=ts[i].year,z7=z7[i],tr60=tr60[i],volrel=volrel[i],
                                 ex=fwd[i]-drift,s=(fwd[i]-drift)/usual,al=alloc[i]))
    g=pd.DataFrame(rows).dropna(subset=["ex","z7"])
    def cslope(x):
        x=x.dropna(subset=["z7","ex"])
        if len(x)<30: return pd.Series(dict(n=len(x)))
        X=np.column_stack([np.ones(len(x)),x.z7.values]); y=x.ex.values
        bb,_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@bb
        XtXi=np.linalg.inv(X.T@X); meat=np.zeros((2,2))
        for _,idx in x.reset_index(drop=True).groupby("day").groups.items():
            sc=(X[idx]*e[idx][:,None]).sum(0); meat+=np.outer(sc,sc)
        V=XtXi@meat@XtXi; G=x.day.nunique(); V*=G/(G-1)
        return pd.Series(dict(n=len(x),days=G,slope=bb[1],t=bb[1]/np.sqrt(V[1,1])))
    g["trend"]=pd.cut(g.tr60,[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    g["agit"]=np.where(g.volrel>1,"agit","calm")
    g.loc[g.volrel.isna(),"agit"]=np.nan
    g["sgn"]=np.where(g.z7>0,"up","down")
    out={}
    out["slope_all"]=cslope(g)
    out["slope_by_sgn"]=g.groupby("sgn").apply(cslope)
    out["slope_by_agit_sgn"]=g.dropna(subset=["agit"]).groupby(["agit","sgn"]).apply(cslope)
    out["slope_by_trend_sgn"]=g.dropna(subset=["trend"]).groupby(["trend","sgn"]).apply(cslope)
    out["slope_by_trend"]=g.dropna(subset=["trend"]).groupby("trend").apply(cslope)
    out["slope_by_agit"]=g.dropna(subset=["agit"]).groupby("agit").apply(cslope)
    out["slope_by_coin"]=g.groupby("coin").apply(cslope)
    out["slope_by_year"]=g.groupby("yr").apply(cslope)
    # book daily: largest gains/losses context
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    D=pd.concat(dd)
    D["day"]=pd.to_datetime(D["day"])
    B=D.groupby("day").agg(book=("book_return","mean"),coin=("coin_return","mean")).dropna()
    B["q"]=pd.qcut(B.book.rank(method="first"),10,labels=False)
    out["book_deciles_vs_coin"]=B.groupby("q").agg(book=("book","mean"),coin=("coin","mean"),n=("book","size"))
    out["book_by_year"]=B.groupby(B.index.year).agg(mean=("book","mean"),sd=("book","std"),n=("book","size"))
    return out
