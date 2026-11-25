def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"];h=b["high"];l=b["low"];o=b["open"]
            rng=(h-l)
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["clv"]=((h-c)/rng.replace(0,np.nan)).values
            d["r1p"]=c.pct_change().values
            d["r3p"]=(c/c.shift(3)-1).values
            d["r7p"]=(c/c.shift(7)-1).values
            d["r30p"]=(c/c.shift(30)-1).values
            d["nr1"]=(c.shift(-1)/c-1).values
            d["nr3"]=(c.shift(-3)/c-1).values
            rr=rng/c
            d["rr"]=rr.values
            d["rrrel"]=(rr/rr.rolling(30,min_periods=10).mean()).values
            d["ratio"]=(rr.rolling(90,min_periods=30).mean()/rr.rolling(30,min_periods=10).mean()).values
            d["low30"]=(c<=c.rolling(30,min_periods=20).min()).astype(float).values
            d["high30"]=(c>=c.rolling(30,min_periods=20).max()).astype(float).values
            d["gap_body"]=((c-o)/o).values
            d["regime"]=b["regime"].values
            d["alloc"]=b["postRebalance_current_allocation"].values
            d["fc"]=b["forecast"].values
            d["pos"]=np.arange(len(b))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["nr1"].mean()
    D["ex1"]=D["nr1"]-D["coin"].map(mu)
    mu3=D[D.pos%3==0].groupby("coin")["nr3"].mean()
    D["ex3"]=D["nr3"]-D["coin"].map(mu3)
    D["day"]=D["ts"].dt.floor("D")
    D["inreg"]=D["regime"].eq("mean_reversion")
    def tday(s,days):
        x=pd.DataFrame({"v":s,"d":days}).dropna()
        if len(x)<10: return np.nan
        m=x.v.mean(); g=(x.v-m).groupby(x.d).sum()
        se=np.sqrt((g**2).sum())/len(x)
        return m/se
    def tab(sub,col,q=5,y="ex1"):
        s=sub.dropna(subset=[col,y]).copy()
        s["b"]=pd.qcut(s[col].rank(method="first"),q,labels=False)
        out=s.groupby("b").apply(lambda g: pd.Series({"mean_x":g[col].mean(),"mean%":g[y].mean()*100,"t":tday(g[y],g["day"]),"n":len(g)}))
        return out
    res={}
    R=D[D.inreg];N=D[~D.inreg]
    res["clv_q in regime"]=tab(R,"clv")
    res["clv_q out regime"]=tab(N,"clv")
    res["r1p_q in regime"]=tab(R,"r1p")
    res["r1p_q out regime"]=tab(N,"r1p")
    res["r7p_q all"]=tab(D,"r7p")
    res["r30p_q all"]=tab(D,"r30p")
    res["rrrel_q all"]=tab(D,"rrrel")
    res["ratio_q all"]=tab(D,"ratio")
    g=D.dropna(subset=["ex1"]).groupby(["low30"]).apply(lambda g: pd.Series({"mean%":g.ex1.mean()*100,"t":tday(g.ex1,g.day),"n":len(g)}))
    res["low30"]=g
    g=D.dropna(subset=["ex1"]).groupby(["high30"]).apply(lambda g: pd.Series({"mean%":g.ex1.mean()*100,"t":tday(g.ex1,g.day),"n":len(g)}))
    res["high30"]=g
    D["wd"]=D.ts.dt.weekday
    res["weekday"]=D.dropna(subset=["ex1"]).groupby("wd").apply(lambda g: pd.Series({"mean%":g.ex1.mean()*100,"t":tday(g.ex1,g.day),"n":len(g)}))
    D["yr"]=D.ts.dt.year
    res["clv slope by year in regime"]=R.assign(yr=R.ts.dt.year).dropna(subset=["clv","ex1"]).groupby("yr").apply(lambda g: pd.Series({"corr":g.clv.corr(g.ex1),"n":len(g)}))
    res["coin in regime clv corr"]=R.dropna(subset=["clv","ex1"]).groupby("coin").apply(lambda g: pd.Series({"corr":g.clv.corr(g.ex1),"n":len(g)}))
    S3=D[D.pos%3==0]
    res["r7p_q 3d nonoverlap"]=tab(S3,"r7p",y="ex3")
    res["clv_q 3d nonoverlap all"]=tab(S3,"clv",y="ex3")
    return res
