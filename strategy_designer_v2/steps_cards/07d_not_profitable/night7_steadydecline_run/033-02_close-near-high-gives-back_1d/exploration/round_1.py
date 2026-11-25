def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            r=b.close.shift(-1)/b.close-1
            allr.append(r.dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            d=pd.DataFrame()
            d["loc"]=(b.close-b.low)/(b.high-b.low)
            d["rng"]=(b.high-b.low)/b.close
            d["rngrel"]=d.rng/d.rng.rolling(30,min_periods=10).median()
            d["ret1"]=b.close/b.close.shift(1)-1
            d["r5"]=b.close/b.close.shift(5)-1
            d["r20"]=b.close/b.close.shift(20)-1
            d["vol20"]=d.ret1.rolling(20,min_periods=10).std()
            d["fwd"]=b.close.shift(-1)/b.close-1
            d["fwd2"]=b.close.shift(-2)/b.close-1
            d["ex"]=d.fwd-mu
            d["alloc"]=b.postRebalance_current_allocation
            d["gain"]=d.alloc*d.fwd
            d["coin"]=c; d["w"]=w; d["mu"]=mu
            d["wd"]=pd.to_datetime(b.timestamp).dt.weekday
            d["year"]=pd.to_datetime(b.timestamp).dt.year
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["fwd","loc"])
    out={}
    D["q"]=pd.cut(D["loc"],[-.01,.2,.4,.6,.8,1.01],labels=["q1","q2","q3","q4","q5"])
    def agg(g):
        return pd.Series({"n":len(g),"fwd%":g.fwd.mean()*100,"ex%":g.ex.mean()*100,"t_ex":g.ex.mean()/g.ex.std()*np.sqrt(len(g)),"gain%":g.gain.mean()*100,"alloc":g.alloc.mean()})
    out["by_loc_quintile"]=D.groupby("q").apply(agg)
    D["rq"]=pd.qcut(D.rngrel,3,labels=["narrow","mid","wide"])
    out["q5_q1_by_range"]=D[D.q.isin(["q1","q5"])].groupby(["rq","q"]).apply(agg)
    D["tr"]=pd.cut(D.r20,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    out["by_trend20_q"]=D[D.q.isin(["q1","q5"])].groupby(["tr","q"]).apply(agg)
    D["r1s"]=np.where(D.ret1>0,"up","down")
    out["by_dayret_q"]=D[D.q.isin(["q1","q5"])].groupby(["r1s","q"]).apply(agg)
    out["by_year_book"]=D.groupby("year").apply(agg)
    out["by_coin"]=D.groupby("coin").apply(lambda g: pd.Series({"gain%":g.gain.mean()*100,"drift_part%":(g.alloc*g.mu).mean()*100,"slope":np.polyfit(g["loc"],g.ex,1)[0]}))
    out["book_total"]=pd.Series({"gain%":D.gain.mean()*100,"drift_part%":(D.alloc*D.mu).mean()*100,"mean_alloc":D.alloc.mean(),"corr_alloc_loc":D.alloc.corr(D["loc"])})
    out["fwd2_by_q"]=D.groupby("q").fwd2.mean()*100
    return out
