def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(df)
            s = pd.Series(c)
            dr = s.pct_change()
            vol30 = dr.rolling(30).std().values
            hi14 = s.rolling(14).max().values
            rawc = (c - hi14) / hi14 / vol30
            r60 = s.pct_change(60).values
            for h in [3, 5, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h,
                        year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        fwd=c[i+h]/c[i]-1, f=df["forecast"].iloc[i],
                        reg=df["regime"].iloc[i], rawc=rawc[i], r60=r60[i]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin","h"])["fwd"].transform("mean")
    R["ex"] = R["fwd"] - R["drift"]
    def sl(g, x):
        g = g.dropna(subset=[x,"ex"])
        if len(g) < 15 or g[x].std() == 0: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g.ex); return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope/r.stderr))
    P = R[R.reg == "unknown"].copy()
    NZ = P[P.f != 0]
    out = {}
    out["nonzero_f_by_h"] = NZ.groupby("h").apply(lambda g: sl(g, "f"))
    out["nonzero_raw_by_h"] = NZ.groupby("h").apply(lambda g: sl(g, "rawc"))
    out["all_raw_calm_by_h"] = P.groupby("h").apply(lambda g: sl(g, "rawc"))
    P5 = P[P.h == 5].copy()
    P5["rbin"] = pd.cut(P5.rawc, [-100, -6, -4, -2.5, -1.5, -0.5, -1e-9, 1])
    out["rawbin_h5"] = P5.groupby("rbin")["ex"].agg(["count","mean"])
    P5["zero"] = P5.f == 0
    out["zero_vs_nonzero_h5"] = P5.groupby("zero")["ex"].agg(["count","mean"])
    tz = stats.ttest_ind(P5[P5.zero].ex, P5[~P5.zero].ex, equal_var=False)
    out["zero_minus_nonzero_t"] = tz.statistic
    NZ5 = NZ[NZ.h == 5]
    out["nonzero_f_by_year_h5"] = NZ5.groupby("year").apply(lambda g: sl(g, "f"))
    out["nonzero_f_by_coin_h5"] = NZ5.groupby("coin").apply(lambda g: sl(g, "f"))
    NZ5 = NZ5.copy(); NZ5["trend"] = pd.cut(NZ5.r60, [-np.inf,-0.1,0.1,np.inf], labels=["falling","choppy","rising"])
    out["nonzero_f_by_trend_h5"] = NZ5.groupby("trend").apply(lambda g: sl(g, "f"))
    out["nonzero_meanex_by_trend_h5"] = NZ5.groupby("trend")["ex"].agg(["count","mean"])
    return out
