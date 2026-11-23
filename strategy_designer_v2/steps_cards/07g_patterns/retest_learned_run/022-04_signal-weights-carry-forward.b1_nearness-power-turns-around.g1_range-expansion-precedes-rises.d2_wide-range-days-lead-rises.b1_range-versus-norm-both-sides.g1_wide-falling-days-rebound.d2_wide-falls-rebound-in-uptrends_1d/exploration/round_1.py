def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=3
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]; o=b["open"]
            r1=c.pct_change()
            rng=(h-l)/c.shift(1)
            df=pd.DataFrame({
                "coin":coin,"w":w,
                "r1":r1,
                "r3p":c/c.shift(3)-1,
                "r7":c/c.shift(7)-1,
                "r30":c/c.shift(30)-1,
                "rngm":rng/rng.rolling(30).mean(),
                "vol20":r1.rolling(20).std(),
                "near30":c/h.rolling(30).max()-1,
                "clv":(c-l)/(h-l).replace(0,np.nan),
                "volm":b["volume"]/b["volume"].rolling(30).mean(),
                "fc":b["forecast"],
                "wd":pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "fwd":c.shift(-H)/c-1,
            })
            df["vol20rel"]=df["vol20"]/df["vol20"].rolling(60,min_periods=20).mean()
            df=df.iloc[::H]
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    D=D.dropna(subset=["fwd"])
    drift=D.groupby("coin")["fwd"].mean()
    D["ex"]=D["fwd"]-D["coin"].map(drift)
    out={}
    feats=["r1","r3p","r7","r30","rngm","vol20","vol20rel","near30","clv","volm"]
    summ=[]
    for f in feats:
        d=D.dropna(subset=[f,"ex"]).copy()
        d["z"]=d.groupby("coin")[f].transform(lambda x:(x-x.mean())/x.std())
        d["q"]=d.groupby("coin")[f].transform(lambda x:pd.qcut(x.rank(method="first"),5,labels=False))
        s=stats.linregress(d["z"],d["ex"])
        qm=d.groupby("q")["ex"].mean()
        summ.append({"feat":f,"n":len(d),"slope_per_sd":s.slope,"t":s.slope/s.stderr,
                     **{f"q{int(k)+1}":v for k,v in qm.items()}})
    out["feature_vs_3d_excess"]=pd.DataFrame(summ).set_index("feat")
    # down vs up day by range multiple
    d=D.dropna(subset=["rngm","r1","ex"]).copy()
    d["dn"]=d["r1"]<0
    d["q"]=pd.qcut(d["rngm"],5,labels=False)
    out["ex_by_rangeq_downday"]=d.groupby(["dn","q"])["ex"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    # weekday
    g=D.groupby("wd")["ex"]
    out["weekday"]=pd.DataFrame({"mean":g.mean(),"n":g.count(),"t":g.mean()/g.std()*np.sqrt(g.count())})
    # forecast buckets
    d=D.copy(); d["fb"]=pd.cut(d["fc"],[-0.1,0.001,5,10,15,21])
    g=d.groupby("fb")["ex"]
    out["forecast_bucket"]=pd.DataFrame({"mean":g.mean(),"n":g.count(),"t":g.mean()/g.std()*np.sqrt(g.count())})
    # r1 interaction with r30 sign
    d=D.dropna(subset=["r1","r30","ex"]).copy()
    d["z"]=d.groupby("coin")["r1"].transform(lambda x:(x-x.mean())/x.std())
    res=[]
    for s_,dd in d.groupby(d["r30"]>0):
        s=stats.linregress(dd["z"],dd["ex"]); res.append({"r30pos":s_,"n":len(dd),"slope":s.slope,"t":s.slope/s.stderr})
    out["r1_slope_by_r30sign"]=pd.DataFrame(res)
    # per coin slope of r7 and near30
    res=[]
    for coin,dd in D.dropna(subset=["r7","near30","ex"]).groupby("coin"):
        a=stats.linregress(dd["r7"],dd["ex"]); b2=stats.linregress(dd["near30"],dd["ex"])
        res.append({"coin":coin,"n":len(dd),"t_r7":a.slope/a.stderr,"t_near30":b2.slope/b2.stderr})
    out["per_coin"]=pd.DataFrame(res)
    # book: drift vs timing
    dl=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            dl.append(dd.assign(coin=coin,w=w))
    DD=pd.concat(dl,ignore_index=True)
    out["book_mean_daily"]=DD["book_return"].mean()
    out["coin_mean_daily"]=DD["coin_return"].mean()
    return out
