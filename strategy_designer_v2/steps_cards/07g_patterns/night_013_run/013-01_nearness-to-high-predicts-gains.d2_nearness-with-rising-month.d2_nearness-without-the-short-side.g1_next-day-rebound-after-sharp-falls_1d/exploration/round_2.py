def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            c = d["close"].astype(float)
            r = c.pct_change()
            d["r"] = r
            d["vol20"] = r.rolling(20).std()
            d["z"] = r / d["vol20"]
            d["vol_rank"] = d["vol20"].rolling(120, min_periods=40).rank(pct=True)
            d["fwd1"] = c.shift(-1)/c - 1
            lv = np.log(d["volume"].astype(float)+1)
            d["vz"] = (lv - lv.rolling(20).mean())/lv.rolling(20).std()
            d["coin"] = coin; d["w"] = w
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            d["alloc"] = d["postRebalance_current_allocation"]
            rows.append(d[["coin","w","r","z","vol_rank","fwd1","vz","wd","year","alloc"]])
    A = pd.concat(rows, ignore_index=True)
    A["ex1"] = A["fwd1"] - A.groupby("coin")["fwd1"].transform("mean")
    out = {}
    D = A[A["z"] < 0].dropna(subset=["z","ex1","vol_rank","vz"]).copy()
    D["f"] = -D["z"]
    # slope of ex1 on fall within vol terciles (fixed cutpoints over all down days)
    D["vq"] = pd.qcut(D["vol_rank"], 3, labels=["low","mid","high"])
    res = {}
    for k, g in D.groupby("vq"):
        s = stats.linregress(g["f"], g["ex1"]); res[k] = (s.slope, s.slope/s.stderr, len(g))
    out["down-day slope by vol tercile"] = pd.DataFrame(res, index=["slope","t","n"]).T
    # interaction regression fall x vol_rank, fall x vz
    def ols(X, y):
        X = np.column_stack([np.ones(len(y))] + X); b, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ b; s2 = e @ e / (len(y)-X.shape[1]); cov = s2*np.linalg.inv(X.T@X)
        return b/np.sqrt(np.diag(cov))
    y = D["ex1"].values
    t = ols([D["f"].values, D["vol_rank"].values, (D["f"]*D["vol_rank"]).values], y)
    out["t: const,fall,volrank,fall*volrank"] = pd.Series(t, index=["c","fall","vr","fall*vr"])
    t = ols([D["f"].values, D["vz"].values, (D["f"]*D["vz"]).values], y)
    out["t: const,fall,vz,fall*vz"] = pd.Series(t, index=["c","fall","vz","fall*vz"])
    # by coin: z<-1 highvol tercile minus lowvol (Welch)
    E = A[A["z"] < -1].dropna(subset=["ex1","vol_rank"]).copy()
    E["vq"] = pd.qcut(E["vol_rank"], 3, labels=["low","mid","high"])
    res = {}
    for coin, g in E.groupby("coin"):
        h = g[g.vq=="high"]["ex1"]; l = g[g.vq=="low"]["ex1"]
        res[coin] = (h.mean(), l.mean(), stats.ttest_ind(h, l, equal_var=False).statistic, len(h), len(l))
    out["z<-1 high minus low vol by coin"] = pd.DataFrame(res, index=["high","low","welch_t","nh","nl"]).T
    # all bars: vol rank tercile graded slope of ex1 on z (both sides)
    B = A.dropna(subset=["z","ex1","vol_rank"]).copy()
    B["vq"] = pd.qcut(B["vol_rank"], 3, labels=["low","mid","high"])
    res = {}
    for k, g in B.groupby("vq"):
        s = stats.linregress(g["z"], g["ex1"]); res[k] = (s.slope, s.slope/s.stderr, len(g))
    out["all-bar slope ex1 on z by vol tercile"] = pd.DataFrame(res, index=["slope","t","n"]).T
    # weekday by coin and by year halves (Fri minus Mon/Wed)
    A["half"] = np.where(A["year"] <= 2021, "2018-21", "2022-25")
    out["weekday x half mean ex1"] = A.dropna(subset=["ex1"]).pivot_table(index="wd", columns="half", values="ex1", aggfunc="mean")
    W = A.dropna(subset=["ex1"])
    out["weekday by coin t"] = W.groupby(["coin","wd"])["ex1"].agg(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))).unstack()
    # book: timing gain split by vol tercile
    B["gain"] = B["alloc"]*B["ex1"]
    out["book timing gain by vol tercile"] = B.groupby("vq")["gain"].agg(["mean","sum","count"])
    return out
