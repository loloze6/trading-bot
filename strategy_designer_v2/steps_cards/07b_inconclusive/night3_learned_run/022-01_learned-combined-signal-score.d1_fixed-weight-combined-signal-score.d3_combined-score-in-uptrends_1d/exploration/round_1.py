def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float)
            r=c.pct_change()
            f5=c.shift(-5)/c-1
            sig=pd.DataFrame({
                "mom28":c/c.shift(28)-1,
                "rev1":-r,
                "near90":c/c.rolling(90,min_periods=30).max(),
                "negvol30":-r.rolling(30).std(),
            })
            g=df.index[df.index%5==0]
            d=pd.DataFrame({"coin":coin,"win":w,"year":pd.to_datetime(df.loc[g,"timestamp"]).dt.year.values,
                            "fc":df.loc[g,"forecast"].values,"regime":df.loc[g,"regime"].values,
                            "f5":f5.loc[g].values})
            for k in sig: d[k]=sig.loc[g,k].values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D=D.dropna(subset=["f5"])
    D["drift"]=D.groupby("coin")["f5"].transform("mean")
    D["ex"]=D["f5"]-D["drift"]
    T=D[(D.regime=="trending")&(D.fc!=0)].copy()
    def slope(x):
        if len(x)<20: return pd.Series({"n":len(x),"slope_t":np.nan,"mean_ex_signed":np.nan})
        s=stats.linregress(x["fc"],x["ex"])
        return pd.Series({"n":len(x),"slope_t":s.slope/s.stderr,"mean_ex_signed":(np.sign(x.fc)*x.ex).mean()})
    out={}
    out["by_coin"]=T.groupby("coin").apply(slope)
    out["by_year"]=T.groupby("year").apply(slope)
    T["side"]=np.where(T.fc>0,"long","short")
    out["by_side"]=T.groupby("side").apply(lambda x:pd.Series({"n":len(x),"mean_ex":x.ex.mean(),"t":stats.ttest_1samp(x.ex,0)[1] if False else x.ex.mean()/(x.ex.std()/np.sqrt(len(x)))}))
    T["q"]=pd.qcut(T.fc,5,labels=False)
    out["by_fc_quintile"]=T.groupby("q").agg(n=("ex","size"),fc=("fc","mean"),mean_ex=("ex","mean"),sd=("ex","std"))
    # single signals in trending and non-trending
    res=[]
    for reg,sub in [("trending",D[D.regime=="trending"]),("other",D[D.regime!="trending"]),("all",D)]:
        for k in ["mom28","rev1","near90","negvol30"]:
            s=sub.dropna(subset=[k])
            # within-coin z of signal
            z=s.groupby("coin")[k].transform(lambda v:(v-v.mean())/v.std())
            lr=stats.linregress(z,s["ex"])
            res.append({"regime":reg,"signal":k,"n":len(s),"slope_bps_per_sd":lr.slope*1e4,"t":lr.slope/lr.stderr,"spearman":stats.spearmanr(z,s.ex)[0]})
    out["single_signals"]=pd.DataFrame(res)
    # mom28 strength within trending: quintiles of mom28
    tr=D[D.regime=="trending"].dropna(subset=["mom28"]).copy()
    tr["mq"]=tr.groupby("coin")["mom28"].transform(lambda v:pd.qcut(v,5,labels=False))
    out["trend_mom28_quint"]=tr.groupby("mq").agg(n=("ex","size"),mom=("mom28","mean"),mean_ex=("ex","mean"),sd=("ex","std"))
    out["counts"]=pd.Series({"grid":len(D),"trending":int((D.regime=="trending").sum()),"active":len(T)})
    return out
