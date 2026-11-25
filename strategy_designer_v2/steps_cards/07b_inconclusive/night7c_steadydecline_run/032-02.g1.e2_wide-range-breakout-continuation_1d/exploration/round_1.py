def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            rng = pd.Series(h - l)
            ratio = (rng / rng.rolling(28).mean()).values
            pe = pd.Series(c).pct_change(28).values
            hi = pd.Series(c).rolling(28).max().values
            dist = (hi - c) / hi
            n = len(df)
            fc = df["forecast"].values
            for H in (1, 3, 5, 10, 20):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     H=H, ret=c[i+H]/c[i]-1, fc=fc[i], ratio=ratio[i], pe=pe[i], dist=dist[i]))
    R = pd.DataFrame(rows)
    R["mu"] = R.groupby(["coin", "H"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mu"]
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 2 else np.nan))
    act = R[R.fc > 0]
    out = {}
    out["by_H_active"] = act.groupby("H").apply(summ)
    out["by_H_all"] = R.groupby("H").apply(summ)
    a5 = act[act.H == 5].copy()
    out["by_coin"] = a5.groupby("coin").apply(summ)
    out["by_window"] = a5.groupby("win").apply(summ)
    out["by_year"] = a5.groupby("year").apply(summ)
    a5["fq"] = pd.qcut(a5.fc.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by_fc_tercile"] = a5.groupby("fq").apply(summ)
    a5["dq"] = pd.qcut(a5.dist.rank(method="first"), 3, labels=["near", "mid", "far"])
    out["by_dist_tercile"] = a5.groupby("dq").apply(summ)
    a5["rq"] = pd.qcut(a5.ratio.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by_range_tercile"] = a5.groupby("rq").apply(summ)
    a5["pq"] = pd.qcut(a5.pe.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by_pe28_tercile"] = a5.groupby("pq").apply(summ)
    # uptrend + wide range but forecast 0 (far from high)
    r5 = R[(R.H == 5)]
    cond = r5[(r5.pe > 0) & (r5.ratio >= 1)]
    out["regime_fc0_vs_fc>0"] = cond.assign(on=cond.fc > 0).groupby("on").apply(summ)
    # dist at the high exactly
    cond2 = r5[(r5.pe > 0)].copy()
    cond2["wide"] = cond2.ratio >= 1
    cond2["athigh"] = cond2.dist < 0.005
    out["uptrend_wide_x_athigh"] = cond2.groupby(["wide", "athigh"]).apply(summ)
    return out
