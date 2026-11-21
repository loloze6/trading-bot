def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            f=pd.DataFrame({"coin":coin,"w":w})
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
            f["reg"]=b["regime"]
            f["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            f["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            f=f.iloc[::5]
            rows.append(f)
    d=pd.concat(rows,ignore_index=True)
    d=d.dropna(subset=["fwd5"])
    drift=d.groupby("coin")["fwd5"].transform("mean")
    sd=d.groupby("coin")["fwd5"].transform("std")
    d["ab"]=(d["fwd5"]-drift)/sd
    d["abr"]=d["fwd5"]-drift
    out={}
    res=[]
    for feat in ["mom28","ret1","ret5","near","vol30","rng","fc"]:
        for sub,mask in [("all",d.index==d.index),("trend",d["reg"]=="trending"),("notrend",d["reg"]!="trending")]:
            x=d.loc[mask,[feat,"ab","coin"]].dropna()
            z=x.groupby("coin")[feat].transform(lambda s:(s-s.mean())/s.std() if s.std()>0 else s*0)
            if len(x)<30: continue
            r=stats.linregress(z,x["ab"])
            res.append([feat,sub,len(x),round(r.slope,4),round(r.slope/r.stderr,2)])
    out["slopes_strength_per_sd"]=pd.DataFrame(res,columns=["feat","sub","n","slope","t"])
    t=d[(d.reg=="trending")&(d.fc!=0)].copy()
    t["q"]=pd.qcut(t["fc"].rank(method="first"),5,labels=False)
    out["trend_fc_quintile"]=t.groupby("q").agg(n=("abr","size"),fc=("fc","mean"),abr=("abr","mean"),t=("ab",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    out["by_weekday"]=d.groupby("wd").agg(n=("ab","size"),abr=("abr","mean"),t=("ab",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    out["by_year"]=d.groupby("yr").agg(n=("ab","size"),abr=("abr","mean"))
    d["vq"]=d.groupby("coin")["vol30"].transform(lambda s:pd.qcut(s.rank(method="first"),3,labels=False))
    out["by_vol_tercile"]=d.groupby("vq").agg(n=("ab","size"),abr=("abr","mean"),t=("ab",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    d["r5q"]=d.groupby("coin")["ret5"].transform(lambda s:pd.qcut(s.rank(method="first"),5,labels=False))
    out["by_ret5_quintile"]=d.groupby("r5q").agg(n=("ab","size"),abr=("abr","mean"),t=("ab",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    d["side"]=np.sign(d["alloc"])
    out["by_position_side"]=d.groupby("side").agg(n=("ab","size"),abr=("abr","mean"),t=("ab",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    tr=pd.concat([x.assign(coin=c) for c,ws in data["trades"].items() for x in ws.values()])
    out["trades"]=tr.groupby("side").agg(n=("side","size"),pl=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_d=("duration_minutes",lambda s:s.mean()/1440))
    return out
