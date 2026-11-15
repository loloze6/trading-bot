def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    fc = "forecast"
    # pooled mean daily return per coin
    mu = {}
    for c in bars:
        r = []
        for w, df in bars[c].items():
            r.append(df["close"].pct_change().dropna())
        mu[c] = pd.concat(r).mean()
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df[fc].values
            dist = df["debug_info.components.above_ma.last_history_value"].values if "debug_info.components.above_ma.last_history_value" in df else np.full(len(df), np.nan)
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r60 = np.full(n, np.nan)
            for i in range(60, n):
                r60[i] = cl[i]/cl[i-60]-1
            for h in [5, 10, 20, 40, 60]:
                for i in range(0, n-h, h):
                    rows.append(dict(coin=c, win=w, year=yr[i], h=h, f=f[i], dist=dist[i], r60=r60[i],
                                     ex=cl[i+h]/cl[i]-1-h*mu[c]))
    R = pd.DataFrame(rows)
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan))
    # by horizon: active vs flat
    R["active"] = R["f"] > 0
    g = R.groupby(["h", "active"])["ex"].apply(tt).unstack()
    out["horizon_active_vs_flat"] = g
    # welch diff active minus flat per horizon
    d = []
    for h, s in R.groupby("h"):
        a = s[s.active]["ex"]; b = s[~s.active]["ex"]
        d.append(dict(h=h, diff=a.mean()-b.mean(), t=stats.ttest_ind(a, b, equal_var=False).statistic, med_active=a.median(), share_pos=(a > 0).mean()))
    out["horizon_diff"] = pd.DataFrame(d)
    A = R[(R.h == 20) & R.active].copy()
    out["h20_by_coin"] = A.groupby("coin")["ex"].apply(tt).unstack()
    out["h20_by_year"] = A.groupby("year")["ex"].apply(tt).unstack()
    A["fq"] = pd.qcut(A["f"], 4, labels=False, duplicates="drop")
    out["h20_by_forecast_q"] = A.groupby("fq").agg(fmean=("f", "mean"), n=("ex", "size"), mean=("ex", "mean"), med=("ex", "median"))
    A["dq"] = pd.qcut(A["dist"], 4, labels=False, duplicates="drop")
    out["h20_by_dist_q"] = A.groupby("dq").agg(dmean=("dist", "mean"), n=("ex", "size"), mean=("ex", "mean"), med=("ex", "median"))
    A["mom"] = np.sign(A["r60"])
    out["h20_by_60d_sign"] = A.groupby("mom")["ex"].apply(tt).unstack()
    A60 = R[(R.h == 60) & R.active].copy()
    out["h60_by_coin"] = A60.groupby("coin")["ex"].apply(tt).unstack()
    # skew of active returns
    out["h20_active_skew"] = float(stats.skew(A["ex"].dropna()))
    return out
