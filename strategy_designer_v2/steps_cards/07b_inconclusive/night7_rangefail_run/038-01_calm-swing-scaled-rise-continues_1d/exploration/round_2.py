def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std()
            x=(c/c.shift(5)-1)/(sd*np.sqrt(5))
            fwd=c.shift(-5)/c-1
            yr=pd.to_datetime(df["timestamp"]).dt.year
            for i in range(0,len(df),5):
                if np.isnan(fwd.iloc[i]) or np.isnan(x.iloc[i]): continue
                rows.append(dict(coin=coin,w=w,x=x.iloc[i],f=fwd.iloc[i],calm=df["regime"].iloc[i]!="chop",
                                 fc=float(df["forecast"].iloc[i]),yr=yr.iloc[i],day=str(df["timestamp"].iloc[i])[:10]))
    d=pd.DataFrame(rows)
    d["ex"]=d["f"]-d.groupby("coin")["f"].transform("mean")
    def clslope(g,xc,yc="ex"):
        g=g.dropna(subset=[xc,yc])
        X=np.column_stack([np.ones(len(g)),g[xc].values]); y=g[yc].values
        if len(g)<10: return pd.Series(dict(n=len(g),slope=np.nan,t_cl=np.nan,mean=np.nan,t_mean=np.nan))
        XtXi=np.linalg.inv(X.T@X); b=XtXi@X.T@y; e=y-X@b
        S=np.zeros((2,2))
        for _,ix in g.reset_index(drop=True).groupby("day").indices.items():
            s=X[ix].T@e[ix]; S+=np.outer(s,s)
        G=g["day"].nunique(); n=len(g)
        S*=G/(G-1)*(n-1)/(n-2)
        V=XtXi@S@XtXi
        dd=g.groupby("day")[yc].sum()
        return pd.Series(dict(n=n,days=G,slope=b[1],t_cl=b[1]/np.sqrt(V[1,1]),mean=g[yc].mean(),
                              t_mean=dd.mean()/(dd.std()/np.sqrt(len(dd)))))
    out={}
    c=d[d.calm]
    out["calm_tested_fc_pos"]=clslope(c[c.fc>0],"fc")
    out["calm_fcpos_rawx_neg_share"]=float((c[c.fc>0].x<0).mean())
    out["calm_rawx_up_on_x"]=clslope(c[c.x>0],"x")
    d["dex"]=np.where(d.x>0,d.ex,-d.ex); d["ax"]=d.x.abs()
    out["calm_both_sides_abs"]=clslope(d[d.calm],"ax","dex")
    out["agit_both_sides_abs"]=clslope(d[~d.calm],"ax","dex")
    out["calm_signed_x_on_ex"]=clslope(d[d.calm],"x","ex")
    out["calm_up_by_year"]=d[d.calm&(d.x>0)].groupby("yr").apply(lambda g: clslope(g,"x"))
    out["calm_signed_by_year"]=d[d.calm].groupby("yr").apply(lambda g: clslope(g,"x","ex"))
    return out
