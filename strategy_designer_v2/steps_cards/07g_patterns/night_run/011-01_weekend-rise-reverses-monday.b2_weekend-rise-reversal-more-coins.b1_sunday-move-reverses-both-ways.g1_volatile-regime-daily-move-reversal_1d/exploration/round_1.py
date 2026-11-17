def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
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
            b=b.copy()
            cl=b["close"].astype(float)
            d=pd.DataFrame({"coin":c,"win":w})
            d=pd.DataFrame(index=b.index)
            d["coin"]=c; d["win"]=w
            d["r0"]=cl/cl.shift(1)-1
            d["r1"]=cl.shift(-1)/cl-1
            d["r3"]=cl.shift(-3)/cl-1
            d["vol20"]=d["r0"].rolling(20).std()
            d["absn"]=d["r0"].abs()/d["vol20"]
            d["pos"]=b["postRebalance_current_allocation"].astype(float)
            d["fee"]=(b["total_portfolio_value"].astype(float)-b["postRebalance_total_value"].astype(float))/b["total_portfolio_value"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            d["wd"]=ts.dt.weekday.values
            d["year"]=ts.dt.year.values
            v=b["volume"].astype(float)
            d["relvol"]=v/v.rolling(30).median()
            d["mom20"]=cl/cl.shift(20)-1
            d["cm"]=coinmean[c]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["gain"]=D["pos"]*D["r1"]
    D["timing"]=D["pos"]*(D["r1"]-D["cm"])
    D["mkt"]=D["pos"]*D["cm"]
    out={}
    out["decomp"]=pd.Series({"gain_mean":D["gain"].mean(),"timing":D["timing"].mean(),"mkt":D["mkt"].mean(),"fee_mean":D["fee"].mean(),"mean_pos":D["pos"].mean(),"share_short":(D["pos"]<0).mean(),"mean_abs_pos":D["pos"].abs().mean()})
    # reversal: next-day signed return vs today sign, by z-bucket
    E=D.dropna(subset=["r0","r1","vol20"]).copy()
    E["z"]=E["r0"]/E["vol20"]
    E["zb"]=pd.cut(E["z"],[-99,-2,-1,-0.3,0.3,1,2,99])
    out["next_by_z"]=E.groupby("zb").agg(n=("r1","size"),r1=("r1","mean"),r3=("r3","mean"))
    E["fade"]=-np.sign(E["r0"])*E["r1"]
    def tt(x): x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out["fade_by_weekday"]=E.groupby("wd")["fade"].apply(tt).unstack()
    E["vq"]=E.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["fade_by_volq"]=E.groupby("vq")["fade"].apply(tt).unstack()
    E["big"]=E["absn"]>1.5
    out["fade_big_by_volq"]=E[E["big"]].groupby("vq")["fade"].apply(tt).unstack()
    E["rvq"]=pd.qcut(E["relvol"].rank(method="first"),3,labels=False)
    out["fade_by_relvol"]=E.dropna(subset=["relvol"]).groupby("rvq")["fade"].apply(tt).unstack()
    E["momsign"]=np.sign(E["mom20"])
    out["fade_by_mom20sign"]=E.groupby("momsign")["fade"].apply(tt).unstack()
    out["fade_by_year"]=E.groupby("year")["fade"].apply(tt).unstack()
    # up vs down day fade
    E["up"]=E["r0"]>0
    out["fade_up_vs_down"]=E.groupby("up")["fade"].apply(tt).unstack()
    out["timing_by_coin"]=D.groupby("coin").agg(timing=("timing","mean"),mkt=("mkt","mean"),fee=("fee","mean"))
    # momentum continuation: next 1d return by mom20 tercile
    E["mq"]=pd.qcut(E["mom20"].rank(method="first"),3,labels=False)
    out["r1_by_mom20q"]=E.dropna(subset=["mom20"]).groupby("mq")["r1"].apply(tt).unstack()
    return out
