def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            sma = c.rolling(20).mean()
            dist = c / sma - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in [1, 3, 5, 10, 20]:
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(df), h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, year=yr.iloc[i],
                                     fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                                     dist=dist.iloc[i], ret=fwd.iloc[i]))
    R = pd.DataFrame(rows).dropna(subset=["ret"])
    R["mu"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mu"]
    out = {}
    def slope(d, x="fc"):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 15: return (len(d), np.nan, np.nan, np.nan)
        s = stats.linregress(d[x], d["ex"])
        return (len(d), s.slope, s.slope / s.stderr, d["ex"].mean())
    # horizons
    hz = []
    for h in [1, 3, 5, 10, 20]:
        d = R[(R.h == h) & (R.fc > 0)]
        n, b, t, m = slope(d)
        hz.append(dict(h=h, n=n, slope=b, t=t, mean_ex=m, t_mean=m / (d.ex.std() / np.sqrt(n))))
    out["by_horizon_fc>0"] = pd.DataFrame(hz)
    d5 = R[(R.h == 5) & (R.fc > 0)].copy()
    out["by_coin_h5"] = pd.DataFrame({c: slope(g) for c, g in d5.groupby("coin")}, index=["n", "slope", "t", "mean_ex"]).T
    out["by_year_h5"] = pd.DataFrame({y: slope(g) for y, g in d5.groupby("year")}, index=["n", "slope", "t", "mean_ex"]).T
    d5["q"] = pd.qcut(d5["fc"], 4, labels=False, duplicates="drop")
    out["by_fc_quartile_h5"] = d5.groupby("q").agg(n=("ex", "size"), fc=("fc", "mean"), mean_ex=("ex", "mean"), sd=("ex", "std"))
    # raw distance slope in profile vs outside (all positive dist)
    a = R[(R.h == 5) & (R.dist > 0)]
    out["raw_dist_slope_by_regime_h5"] = pd.DataFrame({r: slope(g, "dist") for r, g in a.groupby("reg")}, index=["n", "slope", "t", "mean_ex"]).T
    out["regime_counts"] = R[R.h == 5]["reg"].value_counts()
    return out
