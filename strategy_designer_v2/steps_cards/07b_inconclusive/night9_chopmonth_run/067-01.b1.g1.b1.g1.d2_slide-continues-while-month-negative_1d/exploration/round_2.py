def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            s = pd.Series(c)
            r30 = s.pct_change(30).values*100
            r60 = s.pct_change(60).values*100
            dr = s.pct_change()
            vol30 = dr.rolling(30).std().values
            reg_ = df["regime"].values
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, ret=c[i+h]/c[i]-1,
                                     fc=df["forecast"].iloc[i], r30=r30[i], r60=r60[i],
                                     vol30=vol30[i], regime=reg_[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    R = pd.DataFrame(rows)
    R["mean_h"] = R.groupby(["coin","h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mean_h"]
    R["agit"] = R["vol30"] > R.groupby("coin")["vol30"].transform("median")
    def reg(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 8: return pd.Series(dict(n=len(d)))
        s = stats.linregress(d[x], d["ex"])
        return pd.Series(dict(n=len(d), slope=s.slope, t=s.slope/s.stderr, mean_ex=d["ex"].mean(),
                              t_mean=d["ex"].mean()/(d["ex"].std()/np.sqrt(len(d))), mean_ret=d["ret"].mean()))
    out = {}
    # in the chop regime (recorded), r30<0: raw r30 as predictor
    S = R[(R.regime=="chop")]
    out["chop_raw_r30_by_h"] = pd.DataFrame({h: reg(S[S.h==h], "r30") for h in (5,10,20)}).T
    out["chop_fc_by_h"] = pd.DataFrame({h: reg(S[S.h==h], "fc") for h in (5,10,20)}).T
    S10 = S[S.h==10].copy()
    out["chop10_raw_r30_by_agit"] = S10.groupby("agit").apply(lambda d: reg(d, "r30"))
    out["chop10_raw_r30_by_year"] = S10.groupby("year").apply(lambda d: reg(d, "r30"))
    S10["q"] = pd.qcut(S10["r30"], 4, labels=["deepest","q2","q3","shallow"])
    out["chop10_by_r30_quartile"] = S10.groupby("q")[["ex","ret","r30"]].agg(["mean","count"])
    out["corr_fc_r30"] = float(S10[["fc","r30"]].dropna().corr().iloc[0,1])
    big = ["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]
    S10["grp"] = np.where(S10.coin.isin(big), "core6", "others")
    out["chop10_raw_r30_by_coingroup"] = S10.groupby("grp").apply(lambda d: reg(d, "r30"))
    return out
