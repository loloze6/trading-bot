def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    bars=data["bars"]
    for coin,ws in bars.items():
        allr=[]
        for w,df in ws.items():
            c=df["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu=np.nanmean(np.concatenate(allr))
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r1=c/c.shift(1)-1
            mabs=r1.abs().rolling(60,min_periods=20).mean().shift(1)
            n1=c.shift(-1)/c-1
            n2=c.shift(-2)/c.shift(-1)-1
            ts=pd.to_datetime(df["timestamp"])
            for i in range(len(df)):
                if df["regime"].iat[i]!="unknown" or pd.isna(r1.iat[i]) or pd.isna(n1.iat[i]): continue
                rows.append(dict(coin=coin,win=w,year=ts.iat[i].year,day=ts.iat[i].normalize(),
                    r1=r1.iat[i],z=r1.iat[i]/mabs.iat[i] if pd.notna(mabs.iat[i]) and mabs.iat[i]>0 else np.nan,
                    ex1=n1.iat[i]-mu,ex2=(n2.iat[i]-mu) if pd.notna(n2.iat[i]) else np.nan))
    d=pd.DataFrame(rows)
    out={}
    def summ(g,col="ex1"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def slope_t(g,xcol,ycol="ex1"):
        g=g[[xcol,ycol,"day"]].dropna()
        X=np.column_stack([np.ones(len(g)),g[xcol].values]); y=g[ycol].values
        b=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@b
        XtXi=np.linalg.inv(X.T@X); meat=np.zeros((2,2)); G=0
        for _,idx in g.groupby("day").indices.items():
            s=X[idx].T@e[idx]; meat+=np.outer(s,s); G+=1
        n=len(g); V=XtXi@meat@XtXi*G/(G-1)*(n-1)/(n-2)
        return pd.Series({"n":n,"days":G,"slope":b[1],"t":b[1]/np.sqrt(V[1,1])})
    up=d[d.r1>0].copy(); dn=d[d.r1<0].copy()
    up["qz"]=pd.qcut(up.z,5,labels=False); dn["qz"]=pd.qcut(dn.z,5,labels=False)
    out["up_by_z_quintile_next1"]=up.groupby("qz").apply(summ)
    out["dn_by_z_quintile_next1"]=dn.groupby("qz").apply(summ)
    out["dn_by_z_quintile_day2"]=dn.groupby("qz").apply(lambda g: summ(g,"ex2"))
    out["slope_up_z"]=slope_t(up,"z"); out["slope_up_r1"]=slope_t(up,"r1")
    out["slope_dn_z"]=slope_t(dn,"z"); out["slope_dn_r1"]=slope_t(dn,"r1")
    out["slope_dn_z_ex2"]=slope_t(dn,"z","ex2")
    out["dn_slope_by_coin"]=dn.groupby("coin").apply(lambda g: slope_t(g,"r1"))
    out["dn_slope_by_year"]=dn.groupby("year").apply(lambda g: slope_t(g,"r1"))
    out["up_slope_by_coin"]=up.groupby("coin").apply(lambda g: slope_t(g,"r1"))
    out["up_slope_by_year"]=up.groupby("year").apply(lambda g: slope_t(g,"r1"))
    return out
