import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            r30 = pd.Series(c).pct_change(30).values
            r7 = pd.Series(c).pct_change(7).values
            for i in range(n):
                d = {"coin": coin, "win": w, "pos": i, "inprof": df["regime"].iloc[i] == "unknown",
                     "r30": r30[i], "r7": r7[i], "fc": df["forecast"].iloc[i],
                     "year": pd.Timestamp(df["timestamp"].iloc[i]).year}
                for h in (1, 3, 5, 10):
                    d[f"f{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(d)
    X = pd.DataFrame(rows)
    out = {}
    # coin mean daily drift over all windows
    drift = X.groupby("coin")["f1"].mean()
    out["drift_1d_by_coin"] = drift
    out["regime_share"] = X.groupby("coin")["inprof"].mean()
    P = X[X.inprof].copy()
    out["n_prof_by_coin"] = P.groupby("coin").size()
    res = []
    for h in (1, 3, 5, 10):
        g = P[P.pos % h == 0].dropna(subset=[f"f{h}", "r30"]).copy()
        dr = X[X.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g.coin.map(dr)
        t = stats.ttest_1samp(g["ex"], 0)
        sl = stats.linregress(g["r30"], g["ex"])
        res.append({"h": h, "n": len(g), "mean_ex": g.ex.mean(), "t_mean": t.statistic,
                    "slope_on_r30": sl.slope, "t_slope": sl.slope/sl.stderr,
                    "mean_total": g[f"f{h}"].mean()})
    out["prof_by_horizon"] = pd.DataFrame(res)
    # quintiles of r30 inside profile, horizon 5
    for h in (1, 5):
        g = P[P.pos % h == 0].dropna(subset=[f"f{h}", "r30"]).copy()
        dr = X[X.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        g["ex"] = g[f"f{h}"] - g.coin.map(dr)
        g["q"] = pd.qcut(g["r30"], 5, labels=False)
        out[f"quint_r30_h{h}"] = g.groupby("q").agg(n=("ex", "size"), r30=("r30", "mean"),
                                                    ex=("ex", "mean"), sd=("ex", "std"))
        g["q7"] = pd.qcut(g["r7"], 5, labels=False)
        out[f"quint_r7_h{h}"] = g.groupby("q7").agg(n=("ex", "size"), r7=("r7", "mean"),
                                                    ex=("ex", "mean"))
        out[f"coin_h{h}"] = g.groupby("coin").agg(n=("ex", "size"), ex=("ex", "mean"),
                                                  corr=("ex", lambda s: np.corrcoef(s, g.loc[s.index, "r30"])[0, 1]))
        out[f"year_h{h}"] = g.groupby("year").agg(n=("ex", "size"), ex=("ex", "mean"))
    # out of profile comparison h5
    g = X[(~X.inprof) & (X.pos % 5 == 0)].dropna(subset=["f5", "r30"]).copy()
    dr = X[X.pos % 5 == 0].groupby("coin")["f5"].mean()
    g["ex"] = g.f5 - g.coin.map(dr)
    sl = stats.linregress(g["r30"], g["ex"])
    out["outprof_h5_slope"] = pd.Series({"n": len(g), "slope": sl.slope, "t": sl.slope/sl.stderr, "mean_ex": g.ex.mean()})
    return out
