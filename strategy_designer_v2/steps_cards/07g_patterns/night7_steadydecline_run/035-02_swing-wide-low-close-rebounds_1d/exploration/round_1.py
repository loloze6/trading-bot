def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["fwd"]=c.shift(-1)/c-1
            d["fwd3"]=c.shift(-3)/c-1
            d["r0"]=r
            s20=r.rolling(20).std()
            d["s20"]=s20
            d["rng"]=(b["high"]-b["low"])/c/s20
            hl=(b["high"]-b["low"]).replace(0,np.nan)
            d["low_near"]=(b["high"]-c)/hl
            d["body"]=(c-b["open"])/c/s20
            d["z0"]=r/s20
            d["r5"]=c/c.shift(5)-1
            d["vol_rel"]=s20/r.rolling(60,min_periods=40).std()
            d["volz"]=np.log(b["volume"]/b["volume"].rolling(20).mean())
            d["fc"]=b["forecast"]
            d["alloc"]=b["postRebalance_current_allocation"]
            d["gain"]=d["alloc"]*d["fwd"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["fwd"].transform("mean")
    D["ex"]=D["fwd"]-mu
    D["day"]=D["ts"].dt.floor("D")
    def tday(sub,col="ex"):
        g=sub.groupby("day")[col].sum()
        n=len(g)
        return pd.Series({"mean":sub[col].mean(),"n":len(sub),"days":n,"t":g.mean()/(g.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    def bucket(col,q=5,name=None):
        D["_b"]=D.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),q,labels=False))
        res=D.dropna(subset=["_b","ex"]).groupby("_b").apply(tday)
        out[name or ("q_"+col)]=res
    bucket("fc"); bucket("rng"); bucket("low_near"); bucket("z0"); bucket("body"); bucket("r5"); bucket("vol_rel"); bucket("volz")
    # interaction rng x low_near
    D["rq"]=D.groupby("coin")["rng"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    D["lq"]=D.groupby("coin")["low_near"].transform(lambda x: pd.qcut(x.rank(method="first"),3,labels=False))
    out["rng3_x_low3_mean_ex_bp"]=(D.dropna(subset=["ex"]).groupby(["rq","lq"])["ex"].mean().unstack()*1e4).round(1)
    out["rng3_x_low3_t"]=D.dropna(subset=["ex","rq","lq"]).groupby(["rq","lq"]).apply(lambda s: tday(s)["t"]).unstack().round(2)
    D["wd"]=D["ts"].dt.dayofweek
    out["weekday"]=D.dropna(subset=["ex"]).groupby("wd").apply(tday)
    out["by_coin_fc_top_minus_rest"]=D.dropna(subset=["ex"]).groupby("coin").apply(lambda s: pd.Series({"corr_fc_ex":s["fc"].corr(s["ex"]),"corr_z0_ex":s["z0"].corr(s["ex"]),"n":len(s)}))
    # book daily
    bk=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            x=d[["day","book_return","coin_return"]].copy(); x["w"]=w; x["coin"]=coin; bk.append(x)
    B=pd.concat(bk); Bm=B.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book_by_window"]=Bm.groupby("w").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","count"))
    out["book_corr_coin"]=float(Bm["book_return"].corr(Bm["coin_return"]))
    out["alloc_stats"]=D["alloc"].describe()
    out["corr_alloc_fc"]=float(D["alloc"].corr(D["fc"]))
    return out
