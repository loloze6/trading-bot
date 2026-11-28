def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    col = "debug_info.components.down_vol_share.last_history_value"
    rows = []
    coinmean = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            c = df["close"].values
            ret1 = df["close"].pct_change()
            down = (ret1 < 0).astype(float)
            vol = df["volume"]
            for p in (5, 10, 20):
                df[f"sh{p}"] = (vol*down).rolling(p).sum()/vol.rolling(p).sum() - 0.5
            df["r10"] = df["close"]/df["close"].shift(10)-1
            n = len(df)
            for h in (1, 3, 5, 10, 20):
                for i in range(0, n-h, h):
                    rows.append(dict(coin=coin, win=w, h=h, i=i,
                        day=str(df["timestamp"].iloc[i])[:10],
                        year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        inprof=df["regime"].iloc[i]=="unknown",
                        sh=df[col].iloc[i] if col in df else np.nan,
                        sh5=df["sh5"].iloc[i], sh10=df["sh10"].iloc[i], sh20=df["sh20"].iloc[i],
                        r10=df["r10"].iloc[i],
                        fc=df["forecast"].iloc[i],
                        fwd=c[i+h]/c[i]-1))
    R = pd.DataFrame(rows)
    R["mu"] = R.groupby(["coin","h"])["fwd"].transform("mean")
    R["un"] = R["fwd"]-R["mu"]
    def cl_slope(d, x):
        d = d.dropna(subset=[x,"un"])
        if len(d) < 15: return (np.nan, np.nan, len(d))
        X = np.c_[np.ones(len(d)), d[x].values]; y = d["un"].values
        b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X@b
        XtXi = np.linalg.inv(X.T@X); meat = np.zeros((2,2))
        g = d["day"].values; G = 0
        for k in np.unique(g):
            m = g==k; s = X[m].T@e[m]; meat += np.outer(s,s); G += 1
        V = XtXi@meat@XtXi*G/(G-1)
        return (b[1], b[1]/np.sqrt(V[1,1]), len(d))
    out = {}
    P = R[R.inprof]
    t = []
    for h in (1,3,5,10,20):
        for x in ("sh","sh5","sh10","sh20","r10"):
            s = cl_slope(P[P.h==h], x); t.append(dict(h=h, x=x, slope=s[0], t=s[1], n=s[2]))
    out["inprof_slopes_by_h_and_measure"] = pd.DataFrame(t)
    t = []
    for h in (1,5,10):
        s = cl_slope(R[(R.h==h)&(~R.inprof)], "sh10"); t.append(dict(h=h, slope=s[0], t=s[1], n=s[2]))
    out["outprof_slopes_sh10"] = pd.DataFrame(t)
    P5 = P[P.h==5].dropna(subset=["sh10"]).copy()
    P5["q"] = pd.qcut(P5["sh10"], 5, labels=False, duplicates="drop")
    out["inprof_h5_by_quintile"] = P5.groupby("q").agg(n=("un","size"), sh=("sh10","mean"), un=("un","mean"), fwd=("fwd","mean"), up_share=("fwd", lambda v:(v>0).mean()))
    P10 = P[P.h==10].dropna(subset=["sh10"]).copy()
    P10["q"] = pd.qcut(P10["sh10"], 5, labels=False, duplicates="drop")
    out["inprof_h10_by_quintile"] = P10.groupby("q").agg(n=("un","size"), sh=("sh10","mean"), un=("un","mean"))
    t=[]
    for k, d in P[P.h==5].groupby("coin"):
        s=cl_slope(d,"sh10"); t.append(dict(coin=k,slope=s[0],t=s[1],n=s[2],un_mean=d.un.mean()))
    out["inprof_h5_by_coin"]=pd.DataFrame(t)
    t=[]
    for k, d in P[P.h==5].groupby("year"):
        s=cl_slope(d,"sh10"); t.append(dict(year=k,slope=s[0],t=s[1],n=s[2],un_mean=d.un.mean()))
    out["inprof_h5_by_year"]=pd.DataFrame(t)
    out["inprof_share"] = R[R.h==1].groupby("coin")["inprof"].mean()
    return out
