def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); o=b["open"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change(); sd=r.rolling(30,min_periods=20).std()
            df=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),
                "inprof":(b["regime"]=="unknown").values,
                "r20s":(c/c.shift(20)-1)/(sd*np.sqrt(20)),
                "r10s":(c/c.shift(10)-1)/(sd*np.sqrt(10)),
                "ma20gap":(c/c.rolling(20,min_periods=10).mean()-1)/sd,
                "hi20":(c/h.rolling(20,min_periods=10).max()-1)/sd,
                "volr":np.log(v/v.rolling(20,min_periods=10).mean()),
                "upwick":(h-np.maximum(o,c))/(h-l).replace(0,np.nan),
                "rng":(h-l)/c/sd.shift(1),
                "sdratio":sd/r.rolling(90,min_periods=60).std(),
                "upruns":(r>0).astype(int).groupby(((r>0)!=(r>0).shift()).cumsum()).cumsum()*(r>0)})
            for H in [1,3,5,10]:
                df[f"f{H}"]=c.shift(-H)/c-1
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    drift={H:d[f"f{H}"].mean() for H in [1,3,5,10]}
    p=d[d.inprof]
    res=[]
    for var in ["r20s","r10s","ma20gap","hi20","volr","upwick","rng","sdratio","upruns"]:
        for H in [1,3,5,10]:
            s=p[p.pos%H==0].dropna(subset=[var,f"f{H}"])
            if len(s)<20: continue
            x=s[var].clip(s[var].quantile(.01),s[var].quantile(.99)); y=s[f"f{H}"]-drift[H]
            sl=stats.linregress(x,y)
            res.append({"var":var,"H":H,"n":len(s),"t":sl.slope/sl.stderr,"meanex":y.mean()})
    out={"slopes":pd.DataFrame(res)}
    # short-side mean excess by horizon in profile, by coin
    r2=[]
    for coin,g in p.groupby("coin"):
        for H in [1,3,5,10]:
            s=g[g.pos%H==0].dropna(subset=[f"f{H}"]); y=s[f"f{H}"]-drift[H]
            r2.append({"coin":coin,"H":H,"n":len(s),"meanex":y.mean(),"t":y.mean()/y.std()*np.sqrt(len(y)) if len(y)>2 else np.nan})
    out["prof_excess_by_coin"]=pd.DataFrame(r2)
    s=p[p.pos%5==0].dropna(subset=["ma20gap","f5"]).copy()
    s["b"]=pd.qcut(s.ma20gap,4)
    out["f5_by_ma20gap"]=s.groupby("b")["f5"].agg(["count","mean",lambda v: v.mean()/v.std()*np.sqrt(len(v))])
    s=p[p.pos%5==0].dropna(subset=["volr","f5"]).copy()
    s["b"]=pd.qcut(s.volr,4)
    out["f5_by_volr"]=s.groupby("b")["f5"].agg(["count","mean",lambda v: v.mean()/v.std()*np.sqrt(len(v))])
    # book: largest gains/losses
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; dd.append(x)
    dd=pd.concat(dd).dropna(subset=["book_return"])
    act=dd[dd.book_return!=0]
    out["book_active"]=pd.Series({"n":len(act),"mean":act.book_return.mean(),"t":act.book_return.mean()/act.book_return.std()*np.sqrt(len(act)),"share_pos":(act.book_return>0).mean(),"top10share":act.book_return.nlargest(10).sum()/act.book_return.sum() if act.book_return.sum()!=0 else np.nan})
    return out
