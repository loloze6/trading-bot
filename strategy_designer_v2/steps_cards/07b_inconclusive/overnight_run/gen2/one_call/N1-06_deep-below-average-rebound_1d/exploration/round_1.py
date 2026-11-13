def explore(data):
    import pandas as pd, numpy as np
    H=10
    rows=[]
    bars=data["bars"]
    for coin in bars:
        for w,df in bars[coin].items():
            df=df.reset_index(drop=True)
            c=df["close"].values; n=len(c)
            fc=df["forecast"].values
            col="debug_info.components.below_sma200.last_history_value"
            dist=df[col].values if col in df.columns else np.full(n,np.nan)
            vol=df["volume"].values
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0,n-H,H):
                r=c[i+H]/c[i]-1
                p10=c[i]/c[i-10]-1 if i>=10 else np.nan
                p1=c[i]/c[i-1]-1 if i>=1 else np.nan
                v20=vol[max(0,i-20):i].mean() if i>=5 else np.nan
                rv=np.std(np.diff(np.log(c[max(0,i-20):i+1]))) if i>=10 else np.nan
                rows.append(dict(coin=coin,w=w,yr=yr[i],f=fc[i],dist=dist[i],r=r,p10=p10,p1=p1,
                                 vr=(vol[i]/v20) if (v20 and v20==v20) else np.nan,rv=rv,ts=str(df["timestamp"].iloc[i])))
    d=pd.DataFrame(rows)
    d["hold"]=d.groupby("coin")["r"].transform("mean")
    d["ex"]=d["r"]-d["hold"]
    def summ(g):
        x=g["ex"].dropna()
        return pd.Series(dict(n=len(x),mean=x.mean(),med=x.median(),hit=(x>0).mean(),sd=x.std(),
                              t=x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan))
    out={}
    d["fb"]=pd.cut(d["f"],[-0.01,0,1,5,10,15,20.01])
    out["by_fbucket"]=d.groupby("fb").apply(summ)
    s=d[d.f>=5].copy()
    out["deep_by_coin"]=s.groupby("coin").apply(summ)
    out["deep_by_window"]=s.groupby("w").apply(summ)
    out["deep_by_year"]=s.groupby("yr").apply(summ)
    s["p10b"]=pd.qcut(s["p10"],3,labels=["fell_most","mid","fell_least"])
    out["deep_by_prior10"]=s.groupby("p10b").apply(summ)
    s["p1b"]=np.where(s["p1"]>0,"up_day","down_day")
    out["deep_by_lastday"]=s.groupby("p1b").apply(summ)
    s["vrb"]=pd.qcut(s["vr"],3,labels=["lowvol","mid","highvol"])
    out["deep_by_volratio"]=s.groupby("vrb").apply(summ)
    s["rvb"]=pd.qcut(s["rv"],3,labels=["calm","mid","wild"])
    out["deep_by_realvol"]=s.groupby("rvb").apply(summ)
    if s["dist"].notna().sum()>10:
        s["db"]=pd.qcut(s["dist"],3,labels=["deepest","mid","shallowest"])
        out["deep_by_rawdist"]=s.groupby("db").apply(summ)
    btc=d[d.coin=="BTCUSD"].drop_duplicates("ts").set_index("ts")["r"]
    d["btc"]=d["ts"].map(btc)
    s2=d[(d.f>=5)&(d.coin!="BTCUSD")].dropna(subset=["btc"])
    x=s2.r-s2.btc
    out["deep_alt_minus_btc"]=pd.Series(dict(n=len(s2),mean=x.mean(),t=x.mean()/x.std()*np.sqrt(len(x)),
                                             corr_with_btc=np.corrcoef(s2.r,s2.btc)[0,1],btc_mean=s2.btc.mean()))
    out["distinct_dates_deep"]=d[d.f>=5]["ts"].nunique()
    return out
