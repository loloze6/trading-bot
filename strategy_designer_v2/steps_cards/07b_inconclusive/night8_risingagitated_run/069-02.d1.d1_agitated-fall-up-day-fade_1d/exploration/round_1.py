def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append(b["close"].pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            hh=b["high"].rolling(20).max()
            sd=r.rolling(20).std()
            raw=(c-hh)/hh/sd
            for h in (1,2,3):
                b[f"f{h}"]=c.shift(-h)/c-1
            b["raw"]=raw; b["upret"]=r/sd; b["mu"]=mu
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(len(b))
            b["inprof"]=b["regime"].isin(["mean_reversion"])
            b["up"]=r>0
            rows.append(b[["timestamp","forecast","raw","upret","f1","f2","f3","mu","coin","w","pos","inprof","up","regime"]])
    d=pd.concat(rows)
    d["day"]=pd.to_datetime(d["timestamp"]).dt.floor("D")
    cs=d[(d.forecast<0)&d.f1.notna()].copy()
    cs["dep"]=-cs.forecast
    cs["s1"]=-(cs.f1-cs.mu)
    cs["s2"]=-(cs.f2-2*cs.mu); cs["s3"]=-(cs.f3-3*cs.mu)
    out={}
    out["n"]=pd.Series({"cases":len(cs),"days":cs.day.nunique(),"corr_dep_raw":cs[["dep","raw"]].corr().iloc[0,1]})
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    cs["q_dep"]=pd.qcut(cs.dep,4,labels=False,duplicates="drop")
    cs["q_raw"]=pd.qcut(-cs.raw,4,labels=False,duplicates="drop")
    cs["q_up"]=pd.qcut(cs.upret,4,labels=False,duplicates="drop")
    out["by_dep_q"]=cs.groupby("q_dep")["s1"].apply(tt).unstack()
    out["by_rawdepth_q (3=deepest)"]=cs.groupby("q_raw")["s1"].apply(tt).unstack()
    out["by_upday_size_q (3=biggest)"]=cs.groupby("q_up")["s1"].apply(tt).unstack()
    out["by_coin"]=cs.groupby("coin")["s1"].apply(tt).unstack()
    out["by_window"]=cs.groupby("w")["s1"].apply(tt).unstack()
    out["by_year"]=cs.groupby(pd.to_datetime(cs.timestamp).dt.year)["s1"].apply(tt).unstack()
    out["horizons"]=pd.DataFrame({h:tt(cs[h]) for h in ["s1","s2","s3"]})
    sl={}
    for x in ["dep","raw","upret"]:
        z=cs[[x,"s1"]].dropna(); res=stats.linregress(z[x],z.s1); sl[x]=pd.Series({"slope":res.slope,"t":res.slope/res.stderr,"n":len(z)})
    out["slopes_s1 (short gain on x)"]=pd.DataFrame(sl)
    # up days outside profile
    o=d[(d.up)&(~d.inprof)&d.f1.notna()&d.raw.notna()].copy()
    o["s1"]=-(o.f1-o.mu); o["q_raw"]=pd.qcut(-o.raw,4,labels=False)
    out["outside_profile_updays_by_rawdepth"]=o.groupby("q_raw")["s1"].apply(tt).unstack()
    out["regimes"]=d.regime.value_counts()
    return out
