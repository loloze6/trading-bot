def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            rng=(b.high-b.low)
            b["loc"]=((b.high-b.close)/rng.replace(0,np.nan))
            rp=rng/b.close
            b["rr"]=rp/rp.rolling(20,min_periods=10).mean()
            b["rr_prev"]=rp/rp.shift(1).rolling(20,min_periods=10).mean()
            b["f1"]=b.close.shift(-1)/b.close-1
            a=b["postRebalance_current_allocation"]
            b["pg"]=a*b["f1"]
            b["fee"]=(b.total_portfolio_value-b.postRebalance_total_value)/b.total_portfolio_value
            b["absalloc"]=a.abs()
            b["coin"]=coin; b["w"]=w; b["yr"]=pd.to_datetime(b.timestamp).dt.year
            rows.append(b)
    d=pd.concat(rows,ignore_index=True)
    d["u1"]=d["f1"]-d.groupby("coin")["f1"].transform("mean")
    d["sig"]=(d["loc"]-0.5)*2
    d["rrq"]=pd.qcut(d["rr_prev"],4,labels=False)
    d["rr5"]=pd.qcut(d["rr_prev"],5,labels=False)
    out={}
    # book by rr quartile
    out["book_by_rrq"]=d.groupby("rrq").agg(pg=("pg","mean"),fee=("fee","mean"),absalloc=("absalloc","mean"),n=("pg","count"))
    # strength by rr quintile: signed move in signal direction, |sig|>=0.6
    e=d[d.sig.abs()>=0.6].copy()
    e["dirmove"]=np.sign(e.sig)*e.u1
    e["tot"]=np.sign(e.sig)*e.f1
    g=e.groupby("rr5")
    out["ext_dirmove_by_rr5"]=pd.DataFrame({"dir_unusual%":g.dirmove.mean()*100,"total%":g.tot.mean()*100,
        "t":g.dirmove.mean()/(g.dirmove.std()/np.sqrt(g.dirmove.count())),"n":g.dirmove.count()})
    # condition alone: wide range days, mid close, long and short
    res=[]
    for k,sub in d.groupby("rr5"):
        s=sub.dropna(subset=["sig","u1"])
        r=stats.linregress(s.sig,s.u1)
        res.append((k,r.slope*100,r.slope/r.stderr,s.u1.mean()*100,len(s)))
    out["slope_by_rr5"]=pd.DataFrame(res,columns=["rr5","slope%","t","mean_u1_all%","n"])
    # side within top rr quintile
    top=e[e.rr5==4]
    out["top_side"]=top.groupby(np.sign(top.sig)).agg(u1=("u1","mean"),f1=("f1","mean"),n=("u1","count"))
    # graded interaction: sig*rr
    s=d.dropna(subset=["sig","u1","rr_prev"])
    x=s.sig*s.rr_prev
    r=stats.linregress(x,s.u1); out["interact"]=pd.Series({"slope%":r.slope*100,"t":r.slope/r.stderr,"n":len(s)})
    # by year in top quintile
    out["top_by_year"]=e[e.rr5==4].groupby("yr").dirmove.agg(["mean","count"]).assign(mean=lambda x:x["mean"]*100)
    # book daily drawdown windows
    dd=[]
    for (c,w),sub in d.groupby(["coin","w"]):
        v=sub.postRebalance_total_value; dd.append((c,w,(v/v.cummax()-1).min()))
    out["dd_by_window"]=pd.DataFrame(dd,columns=["coin","w","mdd"]).groupby("w").mdd.mean()
    return out
