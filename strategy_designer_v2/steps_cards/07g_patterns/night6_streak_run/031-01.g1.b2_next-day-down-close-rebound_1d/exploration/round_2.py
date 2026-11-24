def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    rows = []
    for c, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","open","high","low","close"]].copy().reset_index(drop=True)
            d["coin"]=c; d["win"]=w; d["pos"]=np.arange(len(d))
            r = d["close"].pct_change(); d["r"]=r
            d["vol60"]=r.rolling(60,min_periods=20).std()
            d["z"]=r/d["vol60"]
            d["f1"]=d["close"].shift(-1)/d["close"]-1
            d["f3"]=d["close"].shift(-3)/d["close"]-1
            d["clv"]=(d["close"]-d["low"])/(d["high"]-d["low"])
            # distance of close above the day's low, in usual daily moves
            d["upwick"]=(d["high"]-d["close"])/d["close"]/d["vol60"]
            d["lowdist"]=(d["close"]-d["low"])/d["close"]/d["vol60"]
            d["rng"]=(d["high"]-d["low"])/d["close"]/d["vol60"]
            d["volrank"]=d["vol60"]/d["vol60"].rolling(250,min_periods=60).median()
            d["day"]=pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["yr"]=pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu1=D.groupby("coin")["f1"].mean(); D["x1"]=D["f1"]-D.coin.map(mu1)
    S3=D[D.pos%3==0]; mu3=S3.groupby("coin")["f3"].mean(); D["x3"]=D["f3"]-D.coin.map(mu3)
    def dayt(v, day):
        s=pd.Series(v).groupby(day.values).sum(); K=len(s)
        return s.mean()/ (s.std(ddof=1)/np.sqrt(K)), K
    S=D.dropna(subset=["x1","z","clv","rng","volrank"]).copy()
    # residualised clv signal: regress x1 on z, clv, rng
    X=np.column_stack([np.ones(len(S)),S.z,S.clv-0.5,S.rng,S.volrank])
    b,_,_,_=np.linalg.lstsq(X,S.x1.values,rcond=None)
    res=S.x1.values-X@b; se=np.sqrt(np.diag(np.linalg.inv(X.T@X))*res.var())
    out["OLS x1 ~ z + clv + rng + volrank"]=pd.DataFrame({"coef":b,"t":b/se},index=["c","z","clv-0.5","rng","volrank"]).round(5)
    # clv graded score: (0.5-clv), day-summed t of score*x1
    sc=(0.5-S.clv)*2
    t,K=dayt((sc*S.x1).values,S.day); out["(0.5-clv)*2 x x1: mean, day-t, days"]=pd.Series({"mean":(sc*S.x1).mean(),"t":t,"days":K})
    # clv quintile within up days and within down days
    S["side"]=np.where(S.z<0,"down","up")
    out["clv quintile x side -> x1"]=S.groupby(["side",pd.qcut(S.clv,5,labels=False)])["x1"].agg(["mean","count"]).unstack(0).round(5)
    # by window half / year: clv effect
    S["cq"]=pd.qcut(S.clv,5,labels=False)
    g=S.groupby(["yr","cq"])["x1"].mean().unstack(); out["by year: x1 bottom clv quint minus top"]=(g[0]-g[4]).round(5)
    g=S.groupby(["coin","cq"])["x1"].mean().unstack(); out["by coin: x1 bottom clv quint minus top"]=(g[0]-g[4]).round(5)
    # upper-wick: distance high-close in vol units, quintile
    out["upwick quintile -> x1"]=S.groupby(pd.qcut(S.upwick,5),observed=True)["x1"].agg(["mean","count"]).round(5)
    out["lowdist quintile -> x1"]=S.groupby(pd.qcut(S.lowdist,5),observed=True)["x1"].agg(["mean","count"]).round(5)
    # 3-day horizon for clv
    T=D[D.pos%3==0].dropna(subset=["x3","clv"])
    out["clv quintile -> x3 (nonoverlap)"]=T.groupby(pd.qcut(T.clv,5),observed=True)["x3"].agg(["mean","count"]).round(5)
    # low volrank effect by year
    S["vr"]=pd.qcut(S.volrank,5,labels=False)
    out["by year: x1 lowest volrank quint"]=S[S.vr==0].groupby("yr")["x1"].agg(["mean","count"]).round(5)
    # weekday day-t
    S["wd"]=pd.to_datetime(S.timestamp).dt.weekday
    out["weekday by year x1 (Thu+Fri minus Mon+Wed)"]=S.groupby(["yr"]).apply(lambda g: g[g.wd.isin([3,4])].x1.mean()-g[g.wd.isin([0,2])].x1.mean()).round(5)
    return out
