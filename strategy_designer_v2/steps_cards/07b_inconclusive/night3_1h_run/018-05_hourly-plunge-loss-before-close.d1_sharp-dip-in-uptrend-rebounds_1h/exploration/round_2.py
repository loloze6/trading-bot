def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    bars=data["bars"]
    rows=[]
    for coin,ws in bars.items():
        allr=[];allr720=[]
        for w,df in ws.items():
            c=df["close"].values
            idx=np.arange(0,len(c)-H,H)
            allr+=list(c[idx+H]/c[idx]-1)
            idx2=np.arange(0,len(c)-720,720)
            allr720+=list(c[idx2+720]/c[idx2]-1)
        drift=np.mean(allr); sd720=np.std(allr720,ddof=1)
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values
            s=pd.Series(c)
            r24=s.pct_change(24)
            ma=r24.abs().rolling(720,min_periods=200).mean()
            fallz=(-r24/ma).values
            r720=s.pct_change(720).values
            f=df["forecast"].fillna(0).values
            ts=pd.to_datetime(df["timestamp"])
            for t in range(0,len(c)-H,H):
                rows.append(dict(coin=coin,year=ts.iloc[t].year,fallz=fallz[t],r720z=r720[t]/sd720,
                                 inpos=f[t]>0,u72=c[t+H]/c[t]-1-drift))
    d=pd.DataFrame(rows).dropna(subset=["fallz","r720z","u72"])
    def summ(g):
        x=g["u72"]; return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out={}
    up=d[d.r720z>0]; dn=d[d.r720z<=0]
    out["grid_by_month_sign"]=pd.DataFrame({"up":summ(up),"down":summ(dn)}).T
    out["up_welch_up_minus_down"]=float(stats.ttest_ind(up.u72,dn.u72,equal_var=False).statistic)
    fb=pd.cut(up.fallz,[-99,-1,-0.5,0,0.5,1,1.5,99])
    out["up_by_fallz_bin"]=up.groupby(fb).apply(summ)
    dfb=pd.cut(dn.fallz,[-99,-1,-0.5,0,0.5,1,1.5,99])
    out["down_by_fallz_bin"]=dn.groupby(dfb).apply(summ)
    upf=up[up.fallz>0].copy()
    upf["q"]=pd.qcut(upf.r720z.rank(method="first"),5,labels=False)
    out["updip_by_r720z_q"]=upf.groupby("q").apply(lambda g: pd.concat([summ(g),pd.Series({"med":g.r720z.median()})]))
    upr=up[up.fallz<=0]
    out["up_dip_vs_up_rise"]=pd.DataFrame({"dip":summ(upf),"rise":summ(upr)}).T
    out["up_dip_minus_rise_t"]=float(stats.ttest_ind(upf.u72,upr.u72,equal_var=False).statistic)
    sp=stats.spearmanr(upf.fallz*upf.r720z,upf.u72)
    out["updip_spearman_prod"]=pd.Series(dict(rho=sp.correlation,p=sp.pvalue,n=len(upf)))
    out["up_by_year"]=up.groupby("year").apply(summ)
    out["up_by_coin"]=up.groupby("coin").apply(summ)
    return out
