def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            if len(b)<30: continue
            rng=(b.high-b.low)
            m20=rng.rolling(20,min_periods=20).mean()
            d=pd.DataFrame({
                "coin":coin,"w":w,
                "day":pd.to_datetime(b.timestamp).dt.floor("D"),
                "wd":pd.to_datetime(b.timestamp).dt.weekday,
                "year":pd.to_datetime(b.timestamp).dt.year,
                "loc":(b.close-b.low)/rng.replace(0,np.nan),
                "width":rng/m20,
                "r0":b.close/b.close.shift(1)-1,
                "r1":b.close.shift(-1)/b.close-1,
                "r2":b.close.shift(-2)/b.close-1,
                "tr60":b.close/b.close.shift(60)-1,
                "inprof":(b.regime!="chop"),
                "pos":b.postRebalance_current_allocation,
            })
            d["vol20"]=d.r0.rolling(20).std()
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["mu"]=D.groupby("coin").r1.transform("mean")
    D["x1"]=D.r1-D.mu
    D["z0"]=D.r0/D.vol20
    def ct(g,col="x1"):
        g=g.dropna(subset=[col])
        if len(g)<10: return pd.Series({"n":len(g),"mean":np.nan,"t":np.nan})
        dev=g[col]-g[col].mean()
        s=dev.groupby(g.day).sum()
        se=np.sqrt((s**2).sum())/len(g)
        return pd.Series({"n":len(g),"days":g.day.nunique(),"mean":g[col].mean(),"t":g[col].mean()/se})
    out={}
    D["locq"]=pd.cut(D["loc"],[-.01,.2,.4,.6,.8,1.01],labels=["0-.2","-.4","-.6","-.8","-1"])
    D["wide"]=np.where(D.width>=1.5,"vwide",np.where(D.width>=1,"wide","narrow"))
    out["inprof_share"]=float(D.inprof.mean())
    out["inprof_loc_wide"]=D[D.inprof].groupby(["wide","locq"],observed=True).apply(ct)
    out["outprof_loc_wide"]=D[~D.inprof].groupby(["wide","locq"],observed=True).apply(ct)
    D["trend"]=np.where(D.tr60>.1,"rising",np.where(D.tr60<-.1,"falling",np.where(D.tr60.notna(),"choppy","na")))
    W=D[(D.width>=1)]
    W["side"]=np.where(W["loc"]<.3,"lowclose",np.where(W["loc"]>.7,"highclose","mid"))
    out["wide_by_trend_side"]=W.groupby(["trend","side"]).apply(ct)
    D["zq"]=pd.cut(D.z0,[-99,-2,-1,0,1,2,99])
    out["after_move_z"]=D.groupby("zq",observed=True).apply(ct)
    out["after_move_z_inprof"]=D[D.inprof].groupby("zq",observed=True).apply(ct)
    out["weekday"]=D.groupby("wd").apply(ct)
    out["year"]=D.groupby("year").apply(ct)
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy();t["coin"]=coin;t["w"]=w;dd.append(t)
    B=pd.concat(dd)
    bk=B.groupby("day").book_return.mean().dropna()
    out["book_days"]=pd.Series({"n":len(bk),"mean":bk.mean(),"sd":bk.std(),"top10_sum":bk.nlargest(10).sum(),"bot10_sum":bk.nsmallest(10).sum(),"total_sum":bk.sum()})
    return out
