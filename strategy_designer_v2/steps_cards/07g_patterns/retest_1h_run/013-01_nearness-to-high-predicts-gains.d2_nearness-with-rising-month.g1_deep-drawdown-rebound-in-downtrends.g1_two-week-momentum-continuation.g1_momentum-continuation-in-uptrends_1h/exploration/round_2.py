def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    hr=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float).reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            v=b["volume"].astype(float).reset_index(drop=True)
            lr=np.log(c).diff()
            hr.append(pd.DataFrame(dict(coin=coin,w=w,ts=ts,h=ts.dt.hour,wd=ts.dt.weekday,yr=ts.dt.year,
                nxt=c.shift(-1)/c-1,r24=c/c.shift(24)-1,r336=c/c.shift(336)-1,
                vol=lr.rolling(336,min_periods=168).std(),
                vrel=v.rolling(24).sum()/v.rolling(336,min_periods=168).sum()*14)))
    H=pd.concat(hr).dropna(subset=["nxt"])
    H["dn"]=H["nxt"]-H.groupby("coin")["nxt"].transform("mean")
    # cross-coin averaged per timestamp to remove correlation
    T=H.groupby("ts").agg(dn=("dn","mean"),h=("h","first"),wd=("wd","first"),yr=("yr","first"))
    def tt(g):
        return pd.Series(dict(mean=g.mean(),n=g.count(),t=g.mean()/(g.std()/np.sqrt(g.count()))))
    out["hour, coin-avg per timestamp"]=T.groupby("h")["dn"].apply(tt).unstack().round(5)
    out["weekday, coin-avg per timestamp"]=T.groupby("wd")["dn"].apply(tt).unstack().round(5)
    T["seg"]=np.select([T.h.isin([20,21]),T.h.isin([0,1,2]),T.h==13],["h20-21","h0-2","h13"],"other")
    p=T[T.seg!="other"].groupby(["yr","seg"])["dn"].mean().unstack()*1e4
    out["segments by year (bp)"]=p.round(2)
    q=H.assign(seg=np.select([H.h.isin([20,21]),H.h.isin([0,1,2]),H.h==13],["h20-21","h0-2","h13"],"other"))
    out["segments by coin (bp)"]=(q[q.seg!="other"].groupby(["coin","seg"])["dn"].mean().unstack()*1e4).round(2)
    # graded: h20-21 return vs prior 24h return quintile and vol quintile
    s=H[H.h.isin([20,21])].dropna(subset=["r24","vol"]).copy()
    s["q24"]=s.groupby("coin")["r24"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    s["qv"]=s.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["h20-21 by prior-1d return quintile"]=s.groupby("q24")["dn"].apply(tt).unstack().round(5)
    out["h20-21 by 14d vol quintile"]=s.groupby("qv")["dn"].apply(tt).unstack().round(5)
    s=H[H.h.isin([0,1,2])].dropna(subset=["r24","vol"]).copy()
    s["q24"]=s.groupby("coin")["r24"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["h0-2 by prior-1d return quintile"]=s.groupby("q24")["dn"].apply(tt).unstack().round(5)
    # weekly grid: rel volume within trending vs not, using 168 grid
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float).reset_index(drop=True); v=b["volume"].astype(float).reset_index(drop=True)
            vrel=v.rolling(24).sum()/v.rolling(336,min_periods=168).sum()*14
            r1440=c/c.shift(1440)-1; reg=b["regime"].reset_index(drop=True)
            vr7=v.rolling(168).sum()/v.rolling(1440,min_periods=336).sum()*1440/168
            for pp in range(0,len(c)-168,168):
                rows.append(dict(coin=coin,yr=pd.to_datetime(b["timestamp"].iloc[pp]).year,reg=reg[pp],vrel=vrel[pp],vr7=vr7[pp],fwd=c[pp+168]/c[pp]-1))
    d=pd.DataFrame(rows); d["dfwd"]=d.fwd-d.groupby("coin").fwd.transform("mean")
    for col in ["vrel","vr7"]:
        x=d.dropna(subset=[col]).copy()
        x["q"]=x.groupby("coin")[col].transform(lambda z: pd.qcut(z.rank(method="first"),5,labels=False))
        out[f"7d fwd by {col} quintile x regime"]=x.groupby(["reg","q"])["dfwd"].apply(tt).unstack().round(4)
        out[f"spearman {col} per coin"]=x.groupby("coin").apply(lambda g: stats.spearmanr(g[col],g.dfwd)[0]).round(3)
    return out
