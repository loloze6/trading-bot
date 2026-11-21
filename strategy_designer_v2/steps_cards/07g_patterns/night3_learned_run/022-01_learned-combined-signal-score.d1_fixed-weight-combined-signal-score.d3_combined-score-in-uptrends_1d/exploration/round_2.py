def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            f=pd.DataFrame(index=b.index)
            f["coin"]=coin; f["w"]=w
            f["fwd5"]=c.shift(-5)/c-1
            f["mom28"]=c/c.shift(28)-1
            f["ret1"]=c/c.shift(1)-1
            f["ret5"]=c/c.shift(5)-1
            f["near"]=c/c.rolling(90,min_periods=20).max()-1
            f["vol30"]=c.pct_change().rolling(30,min_periods=15).std()
            f["rng"]=(b["high"]-b["low"])/c
            f["fc"]=b["forecast"].astype(float)
            f["alloc"]=b["postRebalance_current_allocation"].astype(float)
            f["reg"]=b["regime"].astype(str)
            ts=pd.to_datetime(b["timestamp"])
            f["wd"]=ts.dt.weekday
            f["yr"]=ts.dt.year
            f=f.iloc[::5]
            rows.append(f)
    d=pd.concat(rows,ignore_index=True)
    d=d.dropna(subset=["fwd5"])
    drift=d.groupby("coin")["fwd5"].transform("mean")
    sd=d.groupby("coin")["fwd5"].transform("std")
    d["ab"]=(d["fwd5"]-drift)/sd
    d["abr"]=d["fwd5"]-drift
    tst=lambda s:s.mean()/s.std()*np.sqrt(len(s)) if len(s)>2 else np.nan
    out={}
    res=[]
    for feat in ["mom28","ret1","ret5","near","vol30","rng","fc"]:
        for sub,mask in [("all",np.ones(len(d),bool)),("trend",(d["reg"]=="trending").values),("notrend",(d["reg"]!="trending").values)]:
            x=d.loc[mask,[feat,"ab","coin"]].dropna()
            if len(x)<30 or x[feat].std()==0: continue
            z=x.groupby("coin")[feat].transform(lambda s:(s-s.mean())/s.std() if s.std()>0 else s*0)
            r=stats.linregress(z,x["ab"])
            res.append([feat,sub,len(x),round(r.slope,4),round(r.slope/r.stderr,2)])
    out["slopes_strength_per_sd"]=pd.DataFrame(res,columns=["feat","sub","n","slope","t"])
    t=d[(d.reg=="trending")&(d.fc!=0)].copy()
    t["q"]=pd.qcut(t["fc"].rank(method="first"),5,labels=False)
    out["trend_fc_quintile"]=t.groupby("q").agg(n=("abr","size"),fc=("fc","mean"),abr=("abr","mean"),fwd=("fwd5","mean"),t=("ab",tst))
    # per coin sign of fc slope in trend
    pc=[]
    for coin,g in t.groupby("coin"):
        r=stats.linregress(g["fc"],g["ab"]); pc.append([coin,len(g),round(r.slope/r.stderr,2)])
    out["fc_t_by_coin"]=pd.DataFrame(pc,columns=["coin","n","t"])
    out["by_weekday"]=d.groupby("wd").agg(n=("ab","size"),abr=("abr","mean"),t=("ab",tst))
    out["by_year"]=d.groupby("yr").agg(n=("ab","size"),abr=("abr","mean"),t=("ab",tst))
    d["vq"]=d.groupby("coin")["vol30"].transform(lambda s:pd.qcut(s.rank(method="first"),3,labels=False))
    out["by_vol_tercile"]=d.groupby("vq").agg(n=("ab","size"),abr=("abr","mean"),t=("ab",tst))
    d["r5q"]=d.groupby("coin")["ret5"].transform(lambda s:pd.qcut(s.rank(method="first"),5,labels=False))
    out["by_ret5_quintile"]=d.groupby("r5q").agg(n=("ab","size"),abr=("abr","mean"),t=("ab",tst))
    d["m28q"]=d.groupby("coin")["mom28"].transform(lambda s:pd.qcut(s.rank(method="first"),5,labels=False))
    out["by_mom28_quintile"]=d.groupby("m28q").agg(n=("ab","size"),m=("mom28","mean"),abr=("abr","mean"),t=("ab",tst))
    d["nq"]=d.groupby("coin")["near"].transform(lambda s:pd.qcut(s.rank(method="first"),5,labels=False))
    out["by_near_quintile"]=d.groupby("nq").agg(n=("ab","size"),abr=("abr","mean"),t=("ab",tst))
    d["side"]=np.sign(d["alloc"])
    out["by_position_side"]=d.groupby("side").agg(n=("ab","size"),abr=("abr","mean"),t=("ab",tst))
    tr=pd.concat([x.assign(coin=c) for c,ws in data["trades"].items() for x in ws.values() if len(x)])
    out["trades"]=tr.groupby("side").agg(n=("side","size"),pl=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_d=("duration_minutes",lambda s:s.mean()/1440))
    dy=pd.concat([x.assign(coin=c) for c,ws in data["days"].items() for x in ws.values()])
    dy=dy.dropna(subset=["book_return","coin_return"])
    dy["wd"]=pd.to_datetime(dy["day"]).dt.weekday
    out["book_by_weekday"]=dy.groupby("wd").agg(n=("book_return","size"),book=("book_return","mean"),coin=("coin_return","mean"))
    return out
