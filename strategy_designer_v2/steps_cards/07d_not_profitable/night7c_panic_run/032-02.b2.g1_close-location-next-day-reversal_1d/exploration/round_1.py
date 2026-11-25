def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; book=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            rng=(b.high-b.low)
            b["loc"]=((b.high-b.close)/rng.replace(0,np.nan))
            b["rr"]=(rng/b.close)/((rng/b.close).rolling(20,min_periods=10).mean())
            b["r20"]=b.close/b.close.shift(20)-1
            b["mlow"]=(b.close<=b.close.rolling(30,min_periods=20).min()).astype(int)
            for h in [1,2,3,5]:
                f=b.close.shift(-h)/b.close-1
                g=(np.arange(len(b))%h==0)
                b[f"f{h}"]=np.where(g,f,np.nan)
            b["coin"]=coin; b["w"]=w
            a=b["postRebalance_current_allocation"]
            b["pg"]=a*(b.close.shift(-1)/b.close-1)
            b["fee"]=(b.total_portfolio_value-b.postRebalance_total_value)/b.total_portfolio_value
            b["turn"]=(a-b["previous_allocation"]).abs()
            rows.append(b)
    d=pd.concat(rows,ignore_index=True)
    for h in [1,2,3,5]:
        m=d.groupby("coin")[f"f{h}"].transform("mean")
        d[f"u{h}"]=d[f"f{h}"]-m
    d["locq"]=pd.qcut(d["loc"],10,labels=False)
    out={}
    def tab(gcol):
        r={}
        for h in [1,2,3,5]:
            g=d.groupby(gcol)[f"u{h}"]
            r[f"mean{h}"]=g.mean()*100
            r[f"t{h}"]=g.mean()/(g.std()/np.sqrt(g.count()))
        r["n1"]=d.groupby(gcol)["u1"].count()
        return pd.DataFrame(r)
    out["by_loc_decile"]=tab("locq")
    d["rrq"]=pd.qcut(d["rr"],4,labels=False)
    d["r20s"]=np.sign(d["r20"])
    d["signal"]=(d["loc"]-0.5)*2  # +1 at low
    def slope(sub,h):
        s=sub.dropna(subset=["signal",f"u{h}"])
        if len(s)<30: return (np.nan,np.nan,len(s))
        r=stats.linregress(s["signal"],s[f"u{h}"]); return (r.slope*100,r.slope/r.stderr,len(s))
    res=[]
    for name,col in [("rrq","rrq"),("r20s","r20s"),("mlow","mlow"),("coin","coin")]:
        for k,sub in d.groupby(col):
            for h in [1,3]:
                s,t,n=slope(sub,h); res.append((name,str(k),h,s,t,n))
    out["slope_by_state"]=pd.DataFrame(res,columns=["cond","val","h","slope%","t","n"])
    # side of book
    d["side"]=np.sign(d["postRebalance_current_allocation"])
    out["book_by_side"]=d.groupby("side").agg(pg_mean=("pg","mean"),fee_mean=("fee","mean"),turn=("turn","mean"),n=("pg","count"))
    out["book_totals"]=pd.Series({"pg_mean":d.pg.mean(),"fee_mean":d.fee.mean(),"turn_mean":d.turn.mean(),"absalloc":d.postRebalance_current_allocation.abs().mean()})
    # extreme combos h1
    d["ext"]=np.where(d["loc"]>=0.8,"low_close",np.where(d["loc"]<=0.2,"high_close","mid"))
    out["ext_by_rr"]=d.groupby(["ext","rrq"])["u1"].agg(["mean","count"]).assign(mean=lambda x:x["mean"]*100)
    out["ext_by_r20"]=d.groupby(["ext","r20s"])["u1"].agg(["mean","count"]).assign(mean=lambda x:x["mean"]*100)
    return out
