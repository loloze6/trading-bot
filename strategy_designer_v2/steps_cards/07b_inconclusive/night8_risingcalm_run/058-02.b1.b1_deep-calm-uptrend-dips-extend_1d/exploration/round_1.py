def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10]
    for coin, wd in bars.items():
        for w, df in wd.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std()
            hi5 = c.rolling(5, min_periods=5).max()
            depth = (c - hi5) / hi5 / sd30
            ret60 = c / c.shift(60) - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in H:
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(df), h):
                    if pd.isna(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, i=i, year=int(yr.iloc[i]),
                                     day=str(df["timestamp"].iloc[i])[:10],
                                     fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                                     depth=depth.iloc[i], ret60=ret60.iloc[i], fwd=fwd.iloc[i]))
    R = pd.DataFrame(rows)
    R["mean_h"] = R.groupby(["coin", "h"])["fwd"].transform("mean")
    R["ex"] = R["fwd"] - R["mean_h"]

    def tday(sub, col):
        g = sub.groupby("day")[col].sum()
        n = len(sub)
        m = sub[col].mean()
        # clustered se
        dev = (sub[col] - m).groupby(sub["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return m, (m / se if se > 0 else np.nan), n, sub["day"].nunique()

    out = {}
    # 1. main measure by horizon, in profile
    res = []
    for h in H:
        s = R[(R.h == h) & (R.reg == "unknown") & (R.fc < 0)].copy()
        s["prod"] = (s.fc / 10) * s.ex
        m, t, n, d = tday(s, "prod")
        m2, t2, _, _ = tday(s, "ex")
        res.append(dict(h=h, prod_mean=m, prod_t=t, ex_mean=m2, ex_t=t2, n=n, days=d))
    out["profile_by_horizon"] = pd.DataFrame(res)
    # 2. h=5 profile, by depth tercile and by forecast==0 vs <0
    s5 = R[(R.h == 5) & (R.reg == "unknown")].copy()
    s5["grp"] = np.where(s5.fc < 0, "fc<0", "fc=0")
    out["prof_h5_fc0_vs_neg"] = s5.groupby("grp")["ex"].agg(["mean", "count"])
    neg = s5[s5.fc < 0].copy()
    neg["q"] = pd.qcut(neg.fc.rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["prof_h5_terciles"] = neg.groupby("q")["ex"].agg(["mean", "std", "count"])
    neg["prod"] = (neg.fc / 10) * neg.ex
    out["prof_h5_by_coin"] = neg.groupby("coin").apply(lambda x: pd.Series(dict(prod=x["prod"].mean(), ex=x.ex.mean(), n=len(x))))
    out["prof_h5_by_year"] = neg.groupby("year").apply(lambda x: pd.Series(dict(prod=x["prod"].mean(), ex=x.ex.mean(), n=len(x))))
    out["prof_h5_by_window"] = neg.groupby("w").apply(lambda x: pd.Series(dict(prod=x["prod"].mean(), ex=x.ex.mean(), n=len(x))))
    # 3. depth from prices vs excess, everywhere, by context
    res = []
    for h in H:
        s = R[(R.h == h) & R.depth.notna()].copy()
        s["ctx"] = np.where(s.reg == "unknown", "risingcalm",
                   np.where(s.ret60 > 0.10, "rising_other",
                   np.where(s.ret60 < -0.10, "falling", np.where(s.ret60.notna(), "choppy", "na"))))
        for ctx, x in s.groupby("ctx"):
            x = x[x.depth < 0]
            if len(x) < 30: continue
            rho, p = stats.spearmanr(x.depth, x.ex)
            x = x.copy(); x["prod"] = -x.depth / 3 * x.ex
            m, t, n, d = tday(x, "prod")
            res.append(dict(h=h, ctx=ctx, spearman_depth_ex=rho, prod_mean=m, prod_t=t, ex_mean=x.ex.mean(), n=n, days=d))
    out["depth_by_context"] = pd.DataFrame(res)
    return out
