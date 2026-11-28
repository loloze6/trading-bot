def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].values
            ret1 = df["close"].pct_change()
            down = (ret1 < 0).astype(float)
            vol = df["volume"]
            df["sh10"] = (vol*down).rolling(10).sum()/vol.rolling(10).sum() - 0.5
            df["cnt10"] = down.rolling(10).mean() - 0.5
            df["r10"] = df["close"]/df["close"].shift(10)-1
            df["relvol"] = vol.rolling(10).mean()/vol.rolling(60, min_periods=20).mean()
            n = len(df)
            for h in (5, 10):
                for i in range(0, n-h, h):
                    rows.append(dict(coin=coin, win=w, h=h,
                        day=str(df["timestamp"].iloc[i])[:10],
                        year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        inprof=df["regime"].iloc[i]=="unknown",
                        sh10=df["sh10"].iloc[i], cnt10=df["cnt10"].iloc[i],
                        r10=df["r10"].iloc[i], relvol=df["relvol"].iloc[i],
                        fc=df["forecast"].iloc[i], fwd=c[i+h]/c[i]-1))
    R = pd.DataFrame(rows)
    R["mu"] = R.groupby(["coin","h"])["fwd"].transform("mean")
    R["un"] = R["fwd"]-R["mu"]
    R["excess"] = R["sh10"]-R["cnt10"]
    def cl_slope(d, x):
        d = d.dropna(subset=[x,"un"])
        if len(d) < 15: return (np.nan, np.nan, len(d))
        X = np.c_[np.ones(len(d)), d[x].values]; y = d["un"].values
        b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X@b
        XtXi = np.linalg.inv(X.T@X); meat = np.zeros((2,2)); g = d["day"].values; G=0
        for k in np.unique(g):
            m = g==k; s = X[m].T@e[m]; meat += np.outer(s,s); G+=1
        V = XtXi@meat@XtXi*G/(G-1)
        return (b[1], b[1]/np.sqrt(V[1,1]), len(d))
    out = {}
    P = R[R.inprof]
    t=[]
    for h in (5,10):
        d=P[P.h==h]
        t.append(dict(h=h, n=len(d), fwd_mean=d.fwd.mean(), fwd_t=d.fwd.mean()/(d.fwd.std()/np.sqrt(len(d))),
                      un_mean=d.un.mean(), coin_mu=d.mu.mean(),
                      short_fc_n=(d.fc<0).sum(), short_fc_fwd=d[d.fc<0].fwd.mean(), short_fc_un=d[d.fc<0].un.mean()))
    out["inprof_overall"]=pd.DataFrame(t)
    t=[]
    for h in (5,10):
        for x in ("sh10","cnt10","excess","r10","relvol"):
            s=cl_slope(P[P.h==h],x); t.append(dict(h=h,x=x,slope=s[0],t=s[1],n=s[2]))
    out["inprof_slopes"]=pd.DataFrame(t)
    P5=P[P.h==5].dropna(subset=["sh10","r10","relvol"]).copy()
    t=[]
    for lab,m in (("r10<0",P5.r10<0),("r10>=0",P5.r10>=0),("relvol>1",P5.relvol>1),("relvol<=1",P5.relvol<=1)):
        s=cl_slope(P5[m],"sh10"); t.append(dict(split=lab,slope=s[0],t=s[1],n=s[2],un=P5[m].un.mean()))
    out["inprof_h5_sh10_splits"]=pd.DataFrame(t)
    P5["q"]=pd.qcut(P5["r10"],4,labels=False)
    out["inprof_h5_by_r10_quartile"]=P5.groupby("q").agg(n=("un","size"),r10=("r10","mean"),un=("un","mean"),fwd=("fwd","mean"))
    return out
