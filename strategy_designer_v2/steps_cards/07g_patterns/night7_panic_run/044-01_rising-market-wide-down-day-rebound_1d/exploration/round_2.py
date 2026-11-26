def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            b["r1"]=r; b["rs"]=((b["high"]-b["low"])/c)/sd
            b["f3"]=c.shift(-3)/c-1; b["f1"]=c.shift(-1)/c-1
            b["pos"]=np.arange(len(b)); b["coin"]=coin; b["w"]=w
            b["rising"]=b["regime"]!="chop"
            b["clv"]=(c-b["low"])/(b["high"]-b["low"])
            ts=pd.to_datetime(b["timestamp"]); b["wd"]=ts.dt.dayofweek; b["year"]=ts.dt.year
            rows.append(b)
    d=pd.concat(rows)
    def summ(sub,col):
        sub=sub.dropna(subset=[col]); n=len(sub)
        if n<10: return pd.Series({"n":n,"mean%":np.nan,"t_day":np.nan,"days":np.nan})
        dev=sub[col]; s=dev.groupby(sub.timestamp.values).sum(); G=len(s)
        se=np.sqrt((s**2).sum()*G/(G-1))/n
        return pd.Series({"n":n,"mean%":100*dev.mean(),"t_day":dev.mean()/se,"days":G})
    out={}
    d1=d[d.f1.notna()].copy()
    d1["ex1"]=d1.f1-d1.coin.map(d1.groupby("coin").f1.mean())
    out["wd_next1_clustered"]=d1.groupby("wd").apply(lambda x:summ(x,"ex1"))
    d1["thufri"]=d1.wd.isin([3,4])
    out["thufri_by_year"]=d1.groupby(["year","thufri"]).apply(lambda x:summ(x,"ex1"))
    out["thufri_by_coin"]=d1.groupby(["coin","thufri"]).apply(lambda x:summ(x,"ex1"))
    out["thufri_by_rising"]=d1.groupby(["rising","thufri"]).apply(lambda x:summ(x,"ex1"))
    g=d[(d.pos%3==0)&d.f3.notna()&d.rs.notna()].copy()
    g["ex"]=g.f3-g.coin.map(g.groupby("coin").f3.mean())
    rd=g[g.rising&(g.r1<0)].copy()
    rd["dec"]=pd.qcut(rd.rs,6,labels=False)
    out["risdown_rs_sextile"]=rd.groupby("dec").apply(lambda x:summ(x,"ex"))
    rd["top"]=rd.rs>=rd.rs.quantile(0.75)
    out["risdown_top_by_year"]=rd.groupby(["year","top"]).apply(lambda x:summ(x,"ex"))
    # close location in rising market
    rr=g[g.rising].copy(); rr["clq"]=pd.qcut(rr.clv,4,labels=False,duplicates="drop")
    out["rising_closeloc"]=rr.groupby("clq").apply(lambda x:summ(x,"ex"))
    # book extreme days
    dl=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; dl.append(t)
    D=pd.concat(dl).dropna(subset=["book_return"])
    q=D.book_return.quantile([0.01,0.99])
    out["book_tails"]=pd.Series({"share_top1pct_of_total":D.book_return[D.book_return>=q[0.99]].sum()/D.book_return.sum(),
        "share_bot1pct_of_total":D.book_return[D.book_return<=q[0.01]].sum()/D.book_return.sum(),
        "n":len(D)})
    return out
