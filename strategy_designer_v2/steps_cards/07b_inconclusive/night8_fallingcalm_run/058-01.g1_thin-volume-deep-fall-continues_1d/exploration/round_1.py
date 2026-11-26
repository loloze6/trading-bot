def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            v = df["volume"].astype(float)
            vnear = v.rolling(30).mean()
            vfar = v.shift(30).rolling(30).mean()
            vf = (vfar / vnear).values
            r30 = (df["close"] / df["close"].shift(30) - 1).values
            n = len(df)
            for h in (1, 3, 5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, f=df["forecast"].iloc[i],
                                     ret=c[i+h]/c[i]-1, vf=vf[i], r30=r30[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    R = pd.DataFrame(rows)
    R["mu"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mu"]
    R["sg"] = -R["ex"]  # short gain vs holding
    A = R[R.f < 0].copy()
    out = {}
    def slope(d):
        if len(d) < 8 or d.f.std() == 0: return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan, mean_sg=np.nan, t_sg=np.nan))
        s = stats.linregress(d.f, d.ex)
        return pd.Series(dict(n=len(d), slope=s.slope, t=s.slope/s.stderr, mean_sg=d.sg.mean(),
                              t_sg=d.sg.mean()/(d.sg.std()/np.sqrt(len(d)))))
    out["by_horizon"] = A.groupby("h").apply(slope)
    A5 = A[A.h == 5].copy()
    out["by_coin_h5"] = A5.groupby("coin").apply(slope)
    out["by_window_h5"] = A5.groupby("win").apply(slope)
    out["by_year_h5"] = A5.groupby("year").apply(slope)
    A5["fq"] = pd.qcut(A5.f, 4, labels=["q1_strongest", "q2", "q3", "q4_weakest"])
    out["by_fq_h5"] = A5.groupby("fq").apply(slope)
    A5["vthin"] = np.where(A5.vf > 1, "thinning", "swelling")
    out["by_volume_h5"] = A5.groupby("vthin").apply(slope)
    B = A5.dropna(subset=["vf", "r30"])
    if len(B) > 10:
        X = np.column_stack([np.ones(len(B)), B.r30, B.vf])
        beta, *_ = np.linalg.lstsq(X, B.ex.values, rcond=None)
        res = B.ex.values - X @ beta
        cov = np.linalg.inv(X.T @ X) * res.var(ddof=3)
        out["ex_on_r30_vf"] = pd.Series(dict(n=len(B), b_r30=beta[1], t_r30=beta[1]/np.sqrt(cov[1,1]),
                                             b_vf=beta[2], t_vf=beta[2]/np.sqrt(cov[2,2])))
    # all profile cells: does continuation depend on r30 everywhere?
    G = R[(R.h == 5)].dropna(subset=["r30"])
    G = G.assign(active=np.where(G.f < 0, "active", "inactive"))
    out["r30_slope_active_vs_not"] = G.groupby("active").apply(lambda d: pd.Series(dict(
        n=len(d), slope=stats.linregress(d.r30, d.ex).slope,
        t=stats.linregress(d.r30, d.ex).slope/stats.linregress(d.r30, d.ex).stderr)))
    return out
