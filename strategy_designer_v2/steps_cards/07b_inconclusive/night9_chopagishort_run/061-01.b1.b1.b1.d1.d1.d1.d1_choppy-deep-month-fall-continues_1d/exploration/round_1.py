def explore(data):
    import numpy as np, pandas as pd
    H=5
    rows=[]; drift={}
    for coin,wins in data["bars"].items():
        allr=[]
        for w,df in wins.items():
            c=df["close"].values
            n=len(c)
            for i in range(0,n-H,H):
                allr.append(c[i+H]/c[i]-1)
        drift[coin]=(np.mean(allr) if allr else np.nan, np.std(allr) if allr else np.nan)
        for w,df in wins.items():
            c=df["close"].values; n=len(c)
            d=pd.Series(c)
            r1=d.pct_change()
            for i in range(0,n-H,H):
                if i<60: continue
                r20=c[i]/c[i-20]-1; r60=c[i]/c[i-60]-1
                vol30=r1.iloc[i-29:i+1].std()
                fwd=c[i+H]/c[i]-1
                for h in (1,2,3,10):
                    pass
                f2=c[min(i+2,n-1)]/c[i]-1
                f10=c[i+10]/c[i]-1 if i+10<n else np.nan
                hi,lo=df["high"].values[i],df["low"].values[i]
                cl=(c[i]-lo)/(hi-lo) if hi>lo else np.nan
                rows.append(dict(coin=coin,w=w,year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                    r20=r20,r60=r60,vol30=vol30,fwd=fwd,f2=f2,f10=f10,clpos=cl,
                    alloc=abs(df["postRebalance_current_allocation"].iloc[i]),
                    un=-(fwd-drift[coin][0]),z=-(fwd-drift[coin][0])/drift[coin][1]))
    R=pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g),mean_un=g.un.mean(),t=g.un.mean()/(g.un.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,
                              strength=g.z.mean(),neg_f2=-g.f2.mean(),neg_f10=-g.f10.mean()))
    chop=R[(R.r60>=-0.10)&(R.r60<=0.10)]
    sit=chop[chop.r20<=-0.10].copy()
    out={}
    out["all_grid_chop_by_r20bin"]=chop.groupby(pd.cut(chop.r20,[-1,-0.25,-0.18,-0.14,-0.10,-0.05,0,0.05,0.1,1])).apply(summ)
    sit["vq"]=pd.qcut(sit.vol30,3,labels=["lowvol","midvol","highvol"])
    out["sit_by_vol"]=sit.groupby("vq").apply(summ)
    out["sit_by_r60"]=sit.groupby(pd.cut(sit.r60,[-0.1,-0.05,0,0.05,0.1])).apply(summ)
    out["sit_by_year"]=sit.groupby("year").apply(summ)
    out["sit_by_coin"]=sit.groupby("coin").apply(summ)
    out["sit_by_alloc_half"]=sit.groupby(sit.alloc>sit.alloc.median()).apply(summ)
    out["sit_by_closepos"]=sit.groupby(pd.cut(sit.clpos,[-0.01,0.33,0.66,1.01])).apply(summ)
    fall=R[R.r60<-0.10]; fall=fall[fall.r20<=-0.10]
    out["falling_deep20"]=summ(fall).to_frame().T
    return out
