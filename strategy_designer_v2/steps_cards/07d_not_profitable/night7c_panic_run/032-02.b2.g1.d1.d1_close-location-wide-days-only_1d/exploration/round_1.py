def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            rng=b.high-b.low
            m20=rng.shift(1).rolling(20).mean()
            b["mult"]=rng/m20
            b["cl"]=(2*b.close-b.high-b.low)/rng.replace(0,np.nan)
            b["nxt"]=b.close.shift(-1)/b.close-1
            b["r20"]=b.close/b.close.shift(20)-1
            b["r5"]=b.close/b.close.shift(5)-1
            b["low30"]=(b.close<=b.close.rolling(30).min())
            b["pos"]=b["postRebalance_current_allocation"]
            b["coin"]=coin; b["w"]=w; b["year"]=pd.to_datetime(b.timestamp).dt.year
            b["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            rows.append(b)
    d=pd.concat(rows)
    d["drift"]=d.groupby("coin").nxt.transform("mean")
    d["ex"]=d.nxt-d.drift
    d["wide"]=d.mult>1
    d["side"]=np.sign(-d.cl)
    d["sret"]=d.side*d.nxt
    d["sex"]=d.side*d.ex
    d["posret"]=d.pos*d.nxt
    out={}
    def summ(g):
        return pd.Series({"n":len(g),"side_tot_%":g.sret.mean()*100,"side_ex_%":g.sex.mean()*100,
                          "t":g.sex.mean()/(g.sex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,
                          "posret_bp":g.posret.mean()*1e4})
    x=d.dropna(subset=["nxt","cl","mult"])
    out["wide_vs_not"]=x.groupby("wide").apply(summ)
    xw=x[x.wide]
    out["wide_by_side(1=long)"]=xw.groupby("side").apply(summ)
    xw=xw.copy()
    xw["strength"]=(xw.cl.abs()*xw.mult)
    xw["sq"]=pd.qcut(xw.strength,4,labels=False)
    out["wide_by_strength_q"]=xw.groupby(["sq"]).apply(summ)
    out["wide_by_strength_q_side"]=xw.groupby(["sq","side"]).apply(summ)
    xw["trend"]=np.where(xw.r20>0,"up20","down20")
    out["wide_trend_side"]=xw.groupby(["trend","side"]).apply(summ)
    xn=x[~x.wide].copy(); xn["trend"]=np.where(xn.r20>0,"up20","down20")
    out["narrow_trend_side"]=xn.groupby(["trend","side"]).apply(summ)
    out["wide_year"]=xw.groupby("year").apply(summ)
    out["wide_coin"]=xw.groupby("coin").apply(summ)
    out["wide_low30_side"]=xw.groupby(["low30","side"]).apply(summ)
    # book on days: losses by position side
    x2=d.dropna(subset=["nxt"]).copy()
    x2["held"]=np.sign(x2.pos).fillna(0)
    out["book_by_held"]=x2.groupby("held").agg(n=("posret","size"),mean_bp=("posret",lambda s:s.mean()*1e4),
        coin_bp=("nxt",lambda s:s.mean()*1e4))
    # worst 5% of position days: their side and trend
    x2["trend"]=np.where(x2.r20>0,"up20","down20")
    worst=x2[x2.posret<x2.posret.quantile(0.03)]
    out["worst_days_side_trend"]=worst.groupby(["held","trend"]).size()
    out["all_pos_side_trend"]=x2[x2.held!=0].groupby(["held","trend"]).agg(n=("posret","size"),mean_bp=("posret",lambda s:s.mean()*1e4))
    out["abs_pos_mean"]=x2.pos.abs().mean()
    return out
