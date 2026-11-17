def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; allret=[]; days=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            r1=pd.Series(c).shift(-1)/c-1
            r2=pd.Series(c).shift(-2)/c-1
            lr=pd.Series(c).pct_change()
            vol20=lr.rolling(20).std()
            mom20=pd.Series(c)/pd.Series(c).shift(20)-1
            mom5=pd.Series(c)/pd.Series(c).shift(5)-1
            g=pd.Series(c)[::2]; allret.append(pd.DataFrame({"coin":coin,"r2":(g.shift(-1)/g-1).values}))
            ts=pd.to_datetime(b["timestamp"])
            m=(b["regime"]=="mean_reversion")
            for i in np.where(m)[0]:
                rows.append(dict(coin=coin,w=w,year=ts[i].year,wd=ts[i].weekday(),fc=b["forecast"].iloc[i],
                    alloc=b["postRebalance_current_allocation"].iloc[i],r1=r1[i],r2=r2[i],
                    sunret=lr[i],vol=vol20[i],mom20=mom20[i],mom5=mom5[i],
                    fee=(b["total_portfolio_value"].iloc[i]-b["postRebalance_total_value"].iloc[i])/b["total_portfolio_value"].iloc[i]))
        for w,d in data["days"][coin].items():
            days.append(d.assign(coin=coin,w=w))
    df=pd.DataFrame(rows); D=pd.concat(days)
    A=pd.concat(allret).dropna(); cm=A.groupby("coin")["r2"].mean()
    df["ex2"]=df["r2"]-df["coin"].map(cm)
    df["gain1"]=df["alloc"]*df["r1"]
    act=df[df.fc>0].dropna(subset=["r1","r2"])
    out={}
    out["weekday of regime bars"]=df["wd"].value_counts()
    def summ(x,col):
        return pd.Series({"n":len(x),"mean_r1":x.r1.mean(),"t_r1":stats.ttest_1samp(x.r1,0).statistic,
            "mean_ex2":x.ex2.mean(),"t_ex2":stats.ttest_1samp(x.ex2,0).statistic,"gain1":x.gain1.mean(),"fee":x.fee.mean(),"alloc":x.alloc.mean()})
    out["active all"]=summ(act,None)
    out["inactive sunday rises"]=summ(df[df.fc<=0].dropna(subset=["r1","r2"]),None)
    act=act.copy()
    act["fcq"]=pd.qcut(act.fc,4,labels=False)
    out["by forecast quartile"]=act.groupby("fcq").apply(lambda x:summ(x,None))
    act["momq"]=pd.qcut(act.mom20,3,labels=False)
    out["by mom20 tercile"]=act.groupby("momq").apply(lambda x:summ(x,None))
    act["m5q"]=pd.qcut(act.mom5,3,labels=False)
    out["by mom5 tercile"]=act.groupby("m5q").apply(lambda x:summ(x,None))
    act["vq"]=pd.qcut(act.vol,3,labels=False)
    out["by vol tercile"]=act.groupby("vq").apply(lambda x:summ(x,None))
    out["by year"]=act.groupby("year").apply(lambda x:summ(x,None))
    br=D.book_return.dropna(); cr=D.coin_return.dropna()
    out["book vs coin daily"]=pd.Series({"book_mean":br.mean(),"book_sd":br.std(),"coin_mean":cr.mean(),"coin_sd":cr.std(),
        "coin_mean_all_r1":df.r1.mean()})
    return out
