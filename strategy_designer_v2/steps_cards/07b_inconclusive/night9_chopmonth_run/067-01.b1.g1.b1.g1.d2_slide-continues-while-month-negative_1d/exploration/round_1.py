def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    fcol = "debug_info.components.month_fall.last_history_value"
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            r30 = pd.Series(c).pct_change(30).values*100
            r60 = pd.Series(c).pct_change(60).values*100
            lr = np.log(c)
            dr = pd.Series(c).pct_change()
            vol30 = dr.rolling(30).std().values
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ret=c[i+h]/c[i]-1,
                                     fc=df["forecast"].iloc[i], r30=r30[i], r60=r60[i],
                                     vol30=vol30[i], year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    R = pd.DataFrame(rows)
    R["mean_h"] = R.groupby(["coin","h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mean_h"]
    out = {}
    def reg(d, x="fc"):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 8: return pd.Series(dict(n=len(d)))
        s = stats.linregress(d[x], d["ex"])
        return pd.Series(dict(n=len(d), slope=s.slope, t=s.slope/s.stderr, mean_ex=d["ex"].mean(),
                              t_mean=d["ex"].mean()/(d["ex"].std()/np.sqrt(len(d))), mean_ret=d["ret"].mean()))
    S = R[R.fc < 0]
    out["short_by_h"] = pd.DataFrame({h: reg(S[S.h==h]) for h in (5,10,20)}).T
    S10 = S[S.h==10].copy()
    S10["q"] = pd.qcut(S10["fc"], 4, labels=["deepest","q2","q3","shallow"])
    out["short10_by_fc_quartile"] = S10.groupby("q")[["ex","ret","r30"]].agg(["mean","count"])
    out["short10_by_year"] = S10.groupby("year").apply(reg)
    out["short10_by_coin"] = S10.groupby("coin").apply(reg)
    out["short10_by_window"] = S10.groupby("w").apply(reg)
    # agitation proxy: vol30 vs coin median vol30
    R["agit"] = R["vol30"] > R.groupby("coin")["vol30"].transform("median")
    S10 = R[(R.fc<0)&(R.h==10)]
    out["short10_by_agit"] = S10.groupby("agit").apply(reg)
    # whole choppy, both sides, raw r30 as predictor
    C = R[(R.r60.between(-10,10))]
    out["choppy_both_r30_by_h"] = pd.DataFrame({h: reg(C[C.h==h], "r30") for h in (5,10,20)}).T
    C10 = C[C.h==10].copy()
    C10["side"] = np.where(C10.r30<0, "neg", "pos")
    out["choppy10_by_side_r30"] = C10.groupby("side").apply(lambda d: reg(d, "r30"))
    return out
