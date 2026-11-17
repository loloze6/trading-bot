def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    coinmean={}
    for c,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            cl=b["close"].astype(float)
            allr.append((cl.shift(-1)/cl-1).dropna())
        coinmean[c]=pd.concat(allr).mean()
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            cl=b["close"].astype(float).reset_index(drop=True)
            d=pd.DataFrame(index=range(len(cl)))
            d["coin"]=c; d["win"]=w
            d["r0"]=(cl/cl.shift(1)-1).values
            d["r1"]=(cl.shift(-1)/cl-1).values
            d["vol20"]=d["r0"].rolling(20).std()
            d["vol120"]=d["r0"].rolling(120,min_periods=60).std()
            d["pos"]=b["postRebalance_current_allocation"].astype(float).values
            tv=b["total_portfolio_value"].astype(float).values
            pv=b["postRebalance_total_value"].astype(float).values
            d["fee"]=(tv-pv)/tv
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            d["wd"]=ts.dt.weekday.values
            d["year"]=ts.dt.year.values
            v=b["volume"].astype(float).reset_index(drop=True)
            d["relvol"]=(v/v.rolling(30).median()).values
            d["mom20"]=(cl/cl.shift(20)-1).values
            d["cm"]=coinmean[c]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["gain"]=D["pos"]*D["r1"]
    D["timing"]=D["pos"]*(D["r1"]-D["cm"])
    D["mkt"]=D["pos"]*D["cm"]
    def tt(x):
        x=pd.Series(x).dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    out["decomp"]=pd.Series({"gain_mean":D["gain"].mean(),"timing":D["timing"].mean(),"mkt":D["mkt"].mean(),
        "fee_mean":D["fee"].mean(),"mean_pos":D["pos"].mean(),"share_short":(D["pos"]<0).mean(),"mean_abs_pos":D["pos"].abs().mean()})
    E=D.dropna(subset=["r0","r1","vol20"]).copy()
    E["z"]=E["r0"]/E["vol20"]
    E["fade"]=-np.sign(E["r0"])*(E["r1"]-E["cm"])
    E["zb"]=pd.cut(E["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    out["next_by_z"]=E.groupby("zb",observed=True)["r1"].apply(tt).unstack()
    out["fade_by_weekday"]=E.groupby("wd")["fade"].apply(tt).unstack()
    E["vrel"]=E["vol20"]/E["vol120"]
    E["vq"]=pd.qcut(E["vrel"].rank(method="first"),3,labels=False)
    out["fade_by_vol20_over_vol120_q"]=E.dropna(subset=["vrel"]).groupby("vq")["fade"].apply(tt).unstack()
    E["absz"]=E["z"].abs()
    E["aq"]=pd.qcut(E["absz"].rank(method="first"),3,labels=False)
    out["fade_by_absz_q"]=E.groupby("aq")["fade"].apply(tt).unstack()
    R=E.dropna(subset=["relvol"]).copy()
    R["rvq"]=pd.qcut(R["relvol"].rank(method="first"),3,labels=False)
    out["fade_by_relvol_q"]=R.groupby("rvq")["fade"].apply(tt).unstack()
    out["fade_by_mom20sign"]=E.dropna(subset=["mom20"]).groupby(np.sign(E["mom20"].dropna()))["fade"].apply(tt).unstack()
    out["fade_by_year"]=E.groupby("year")["fade"].apply(tt).unstack()
    out["fade_up_vs_down"]=E.groupby(E["r0"]>0)["fade"].apply(tt).unstack()
    # momentum: next-day return (excess) signed by 20d move
    M=E.dropna(subset=["mom20"]).copy()
    M["mom_sig"]=np.sign(M["mom20"])*(M["r1"]-M["cm"])
    M["mq"]=pd.qcut(M["mom20"].abs().rank(method="first"),3,labels=False)
    out["mom20_continuation_by_absq"]=M.groupby("mq")["mom_sig"].apply(tt).unstack()
    out["timing_by_coin"]=D.groupby("coin").agg(timing=("timing","mean"),mkt=("mkt","mean"),fee=("fee","mean"))
    # book daily
    bk=[]
    for c,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd[["day","book_return","coin_return"]].copy(); x["coin"]=c; x["win"]=w; bk.append(x)
    B=pd.concat(bk,ignore_index=True)
    B["day"]=pd.to_datetime(B["day"])
    P=B.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    P["wd"]=P["day"].dt.weekday
    out["book_by_weekday"]=P.groupby("wd")["book_return"].apply(tt).unstack()
    P["cq"]=pd.qcut(P["coin_return"].rank(method="first"),5,labels=False)
    out["book_by_market_day_quintile"]=P.groupby("cq").agg(n=("book_return","size"),book=("book_return","mean"),mkt=("coin_return","mean"))
    P=P.sort_values(["win","day"])
    P["mkt_prev"]=P.groupby("win")["coin_return"].shift(1)
    P["mkt_next"]=P.groupby("win")["coin_return"].shift(-1)
    lo=P["book_return"].quantile(0.02); hi=P["book_return"].quantile(0.98)
    out["around_worst2pct"]=P[P["book_return"]<=lo][["book_return","coin_return","mkt_prev","mkt_next"]].mean()
    out["around_best2pct"]=P[P["book_return"]>=hi][["book_return","coin_return","mkt_prev","mkt_next"]].mean()
    out["book_by_year"]=P.assign(y=P["day"].dt.year).groupby("y")["book_return"].apply(tt).unstack()
    return out
