def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            d=pd.DataFrame({"coin":coin,"win":w,"wd":ts.dt.weekday.values,"year":ts.dt.year.values,
                            "day":ts.dt.floor("D").values})
            d["pos"]=np.arange(len(b))
            d["r1"]=(c.shift(-1)/c-1).values
            d["r2"]=(c.shift(-2)/c-1).values
            d["r3"]=(c.shift(-3)/c-1).values
            d["up60"]=(c/c.shift(60)-1).values
            d["rise14"]=(c/c.shift(14)-1).values
            d["rise7"]=(c/c.shift(7)-1).values
            d["past1"]=(c/c.shift(1)-1).values
            lr=np.log(c).diff()
            d["vol20"]=lr.rolling(20).std().values
            d["z1"]=d["past1"]/d["vol20"]
            d["z14"]=d["rise14"]/(d["vol20"]*np.sqrt(14))
            d["hi60"]=(c/c.rolling(60).max()-1).values
            d["lo60"]=(c/c.rolling(60).min()-1).values
            d["alloc"]=b["postRebalance_current_allocation"].values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    # coin mean 2-bar return on grid
    g2=D[D.pos%2==0].groupby("coin")["r2"].mean()
    g1=D.groupby("coin")["r1"].mean()
    D["x2"]=D["r2"]-D["coin"].map(g2)
    D["x1"]=D["r1"]-D["coin"].map(g1)
    def ct(sub,col):
        s=sub.dropna(subset=[col]).groupby("day")[col].mean()
        n=len(s)
        if n<3: return pd.Series({"mean":np.nan,"t":np.nan,"days":n})
        return pd.Series({"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(n)),"days":n})
    out={}
    # 2-day excess by weekday x uptrend (one weekday => non-overlapping)
    D["upc"]=np.where(D.up60.isna(),"na",np.where(D.up60>0,"up","down"))
    out["x2 by weekday x up60"]=D.groupby(["wd","upc"]).apply(lambda s:ct(s,"x2")).unstack().round(4)
    out["x1 by weekday"]=D.groupby("wd").apply(lambda s:ct(s,"x1")).round(4)
    # slope of x2 on z14 by weekday in uptrend and downtrend
    res=[]
    for (wd,u),s in D.dropna(subset=["x2","z14"]).groupby(["wd","upc"]):
        if u=="na": continue
        sl=stats.linregress(s.z14,s.x2)
        # day-clustered approx: regress day-means
        res.append({"wd":wd,"up":u,"slope":sl.slope,"t_naive":sl.slope/sl.stderr,"n":len(s)})
    out["slope x2 on z14 by wd/up"]=pd.DataFrame(res).round(4)
    # z14 quintiles across all days, x2, on grid pos%2==0
    G=D[(D.pos%2==0)].dropna(subset=["x2","z14"]).copy()
    G["q"]=pd.qcut(G.z14,5,labels=False)
    out["x2 by z14 quintile x up (grid)"]=G.groupby(["upc","q"]).apply(lambda s:ct(s,"x2")).round(4)
    G1=D.dropna(subset=["x1","z1"]).copy()
    G1["q"]=pd.qcut(G1.z1,7,labels=False)
    out["x1 by past1 z septile"]=G1.groupby("q").apply(lambda s:ct(s,"x1")).round(4)
    Gv=D[(D.pos%2==0)].dropna(subset=["x2","vol20"]).copy()
    Gv["vq"]=Gv.groupby("coin")["vol20"].transform(lambda v:pd.qcut(v,4,labels=False))
    out["x2 by vol quartile (grid)"]=Gv.groupby("vq").apply(lambda s:ct(s,"x2")).round(4)
    Gl=D[(D.pos%2==0)].dropna(subset=["x2","lo60"]).copy()
    Gl["lq"]=pd.qcut(Gl.lo60,5,labels=False)
    out["x2 by dist above 60d low quintile"]=Gl.groupby("lq").apply(lambda s:ct(s,"x2")).round(4)
    # book daily
    dd=[]
    for coin,ws in data["days"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; t["win"]=w; dd.append(t)
    DD=pd.concat(dd)
    DD["day"]=pd.to_datetime(DD["day"],utc=True)
    bk=DD.groupby("day")[["book_return","coin_return"]].mean().dropna()
    bk["wd"]=bk.index.weekday; bk["year"]=bk.index.year
    out["book by weekday"]=bk.groupby("wd")["book_return"].agg(["mean","std","count"])
    out["book by year"]=bk.groupby("year")[["book_return","coin_return"]].mean()
    top=bk["book_return"].abs().sort_values(ascending=False).index[:30]
    out["top30 abs book days: share of gain, sign"]=pd.Series({"sum_top30":bk.loc[top,"book_return"].sum(),"sum_all":bk["book_return"].sum(),"pos_in_top30":(bk.loc[top,"book_return"]>0).sum()})
    return out
