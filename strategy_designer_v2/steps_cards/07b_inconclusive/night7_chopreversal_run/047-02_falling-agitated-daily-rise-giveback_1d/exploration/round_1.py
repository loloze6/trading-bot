def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    bars=data["bars"]
    # coin mean daily return over all visible windows
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
            n1=c.shift(-1)/c-1
            n2=c.shift(-2)/c.shift(-1)-1
            n3=c.shift(-3)/c-1
            ts=pd.to_datetime(df["timestamp"])
            for i in range(len(df)):
                if df["regime"].iat[i]!="unknown" or pd.isna(r1.iat[i]) or pd.isna(n1.iat[i]): continue
                rows.append(dict(coin=coin,win=w,year=ts.iat[i].year,day=ts.iat[i].normalize(),
                    r1=r1.iat[i],fc=float(df["forecast"].iat[i]) if pd.notna(df["forecast"].iat[i]) else np.nan,
                    ex1=n1.iat[i]-mu,ex2=(n2.iat[i]-mu) if pd.notna(n2.iat[i]) else np.nan,
                    ex3=(n3.iat[i]-3*mu) if pd.notna(n3.iat[i]) else np.nan))
    d=pd.DataFrame(rows)
    out={}
    up=d[d.r1>0].copy(); dn=d[d.r1<0].copy()
    def summ(g,col="ex1"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    up["q"]=pd.qcut(up.r1,5,labels=False)
    out["up_by_rise_quintile_next1"]=up.groupby("q").apply(summ)
    out["up_rise_q_mean_r1%"]=up.groupby("q").r1.mean()*100
    out["up_by_quintile_day2"]=up.groupby("q").apply(lambda g: summ(g,"ex2"))
    dn["q"]=pd.qcut(dn.r1,5,labels=False)
    out["down_by_fall_quintile_next1"]=dn.groupby("q").apply(summ)
    out["up_by_coin"]=up.groupby("coin").apply(summ)
    out["up_by_year"]=up.groupby("year").apply(summ)
    out["up_by_window"]=up.groupby("win").apply(summ)
    out["up_all_next1"]=summ(up); out["up_all_day2"]=summ(up,"ex2"); out["up_all_3d"]=summ(up,"ex3")
    out["down_all_next1"]=summ(dn)
    # correlation of rise size with next-day excess, up days
    out["up_spearman_r1_ex1"]=str(stats.spearmanr(up.r1,up.ex1))
    out["dn_spearman_r1_ex1"]=str(stats.spearmanr(dn.r1,dn.ex1))
    # vs all bars outside profile on up days (control)
    return out
