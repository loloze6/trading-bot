def explore(data):
    import numpy as np, pandas as pd
    H=18
    rows=[]; hb=[]
    for coin,ws in data["bars"].items():
        g=[]
        for w,df in ws.items():
            d=df[["timestamp","close","volume"]].copy().reset_index(drop=True)
            c=d.close; r=c.pct_change(); d["r"]=r
            d["usual"]=r.abs().rolling(180,min_periods=45).mean()
            d["fwd"]=c.shift(-H)/c-1
            lv=np.log(d.volume.replace(0,np.nan))
            d["volz"]=lv-lv.rolling(180,min_periods=45).mean()
            d["volz18"]=lv.rolling(18).mean()-lv.rolling(180,min_periods=45).mean()
            d["vol_ratio"]=r.abs().rolling(18).mean()/d.usual
            d["past18"]=(c/c.shift(18)-1)/(d.usual*np.sqrt(18))
            d["past6"]=(c/c.shift(6)-1)/(d.usual*np.sqrt(6))
            ts=pd.to_datetime(d.timestamp)
            d["hour"]=ts.dt.hour; d["wd"]=ts.dt.weekday; d["year"]=ts.dt.year
            d["next"]=r.shift(-1); d["coin"]=coin; d["w"]=w
            hb.append(d[["coin","hour","wd","year","next"]])
            g.append(d.iloc[::H])
        g=pd.concat(g); g["drift"]=g.fwd.mean(); g["sd"]=g.fwd.std(); rows.append(g)
    G=pd.concat(rows).dropna(subset=["fwd"]); G["u"]=G.fwd-G.drift; G["us"]=G.u/G.sd
    def st(x,v="u"):
        return pd.Series({"n":len(x),"m":x[v].mean(),"t":x[v].mean()/(x[v].std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    G["vq"]=G.groupby("coin").volz.transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    G["v18q"]=G.groupby("coin").volz18.transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    G["vrq"]=G.groupby("coin").vol_ratio.transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["volz q by coin (top minus bottom m)"]=G.groupby(["coin","vq"]).apply(st).unstack("vq")["m"].round(4)
    out["volz top q by year"]=G[G.vq==4].groupby("year").apply(st).round(4)
    out["volz18 q"]=G.groupby("v18q").apply(st).round(4)
    out["vol_ratio q x volz q (m)"]=G.groupby(["vrq","vq"]).u.mean().unstack().round(4)
    G["sgn"]=np.sign(G.past6)
    out["volz q x sign past6 (m)"]=G.groupby(["vq","sgn"]).u.mean().unstack().round(4)
    out["volz q x sign past6 (t)"]=G.groupby(["vq","sgn"]).apply(st).t.unstack().round(2)
    # signed continuation strength in high volume
    G["p18q"]=pd.qcut(G.past18,5,labels=False)
    out["past18 q x vq top/other (t)"]=G.assign(hv=(G.vq==4)).groupby(["p18q","hv"]).apply(st).t.unstack().round(2)
    HB=pd.concat(hb).dropna(subset=["next"])
    out["hour16 by coin"]=HB[HB.hour==16].groupby("coin").apply(lambda x: st(x,"next")).round(5)
    out["hour16 by year"]=HB[HB.hour==16].groupby("year").apply(lambda x: st(x,"next")).round(5)
    out["hour20 by year"]=HB[HB.hour==20].groupby("year").apply(lambda x: st(x,"next")).round(5)
    out["friday by year"]=HB[HB.wd==4].groupby("year").apply(lambda x: st(x,"next")).round(5)
    out["friday by hour"]=HB[HB.wd==4].groupby("hour").apply(lambda x: st(x,"next")).round(5)
    out["hour by wd (t)"]=HB.groupby(["wd","hour"]).apply(lambda x: st(x,"next")).t.unstack().round(2)
    return out
