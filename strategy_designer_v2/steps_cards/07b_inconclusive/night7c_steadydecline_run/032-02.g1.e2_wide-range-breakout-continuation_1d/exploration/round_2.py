def explore(data):
    import numpy as np, pandas as pd
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
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            fc = df["forecast"].values
            for H in (3, 5, 10):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, day=ts.iloc[i].floor("D"),
                                     H=H, ret=c[i+H]/c[i]-1, fc=fc[i], ratio=ratio[i], pe=pe[i], dist=dist[i]))
    R = pd.DataFrame(rows)
    R["mu"] = R.groupby(["coin", "H"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mu"]
    def summ(g):
        x = g["ex"].dropna()
        n = len(x)
        return pd.Series(dict(n=n, mean=x.mean(), t=x.mean()/(x.std(ddof=1)/np.sqrt(n)) if n > 2 else np.nan))
    out = {}
    U = R[(R.pe > 0) & (R.ratio >= 1)].copy()
    U["dq"] = pd.cut(U.dist, [-1e-9, 0.005, 0.02, 0.05, 0.10, 1.0], labels=["<0.5%", "0.5-2%", "2-5%", "5-10%", ">10%"])
    out["wideup_by_dist_bin_H"] = U.groupby(["H", "dq"]).apply(summ)
    U5 = U[U.H == 5]
    near = U5[U5.dist < 0.005]
    out["athigh_by_year"] = near.groupby("year").apply(summ)
    out["athigh_by_coin"] = near.groupby("coin").apply(summ)
    far = U5[U5.dist >= 0.005]
    out["notathigh_by_year"] = far.groupby("year").apply(summ)
    # slope ex on proximity within wideup, H5
    x = 1/(1+U5.dist*100); y = U5.ex
    m = x.notna() & y.notna(); x = x[m]; y = y[m]
    b = np.polyfit(x, y, 1)[0]
    res = y - np.polyval(np.polyfit(x, y, 1), x)
    se = np.sqrt((res**2).sum()/(len(x)-2)/((x-x.mean())**2).sum())
    out["slope_prox_wideup_H5"] = pd.Series(dict(n=len(x), slope=b, t=b/se))
    # at-high, any range, by range tercile among uptrend
    P = R[(R.H == 5) & (R.pe > 0) & (R.dist < 0.005)].copy()
    P["rq"] = pd.qcut(P.ratio.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["uptrend_athigh_by_range_tercile"] = P.groupby("rq").apply(summ)
    return out
