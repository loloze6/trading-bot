def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 10
    rows = []
    for coin, wins in bars.items():
        # drift per horizon over all windows
        for h in (5, 10, 20):
            pass
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            hi60 = pd.Series(c).rolling(60, min_periods=20).max().values
            r28 = pd.Series(c).pct_change(28).values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            f = df["forecast"].values
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], ret=c[i+h]/c[i]-1,
                                     dist=1 - c[i]/hi60[i] if not np.isnan(hi60[i]) else np.nan,
                                     r28=r28[i], year=year[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]

    def slope(g, x="f"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))

    out = {}
    out["by_h"] = d.groupby("h").apply(slope)
    d10 = d[d.h == 10].copy()
    out["by_coin"] = d10.groupby("coin").apply(slope)
    out["by_year"] = d10.groupby("year").apply(slope)
    d10["side"] = np.sign(d10["f"])
    # mean excess in signal direction by side and forecast bucket
    nz = d10[d10.f != 0].copy()
    nz["direx"] = nz["ex"] * np.sign(nz["f"])
    nz["absq"] = pd.qcut(nz["f"].abs(), 4, labels=False)
    out["side"] = nz.groupby("side")["direx"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["absq"] = nz.groupby("absq")["direx"].agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["side_absq"] = nz.groupby(["side", "absq"])["direx"].agg(["count", "mean"])
    # raw 28-day momentum vs distance buckets
    d10["distq"] = pd.qcut(d10["dist"], 4, labels=False, duplicates="drop")
    out["r28_by_dist"] = d10.groupby("distq").apply(lambda g: slope(g, "r28"))
    out["r28_all"] = slope(d10, "r28")
    out["zero_share"] = float((d10.f == 0).mean())
    # by window-group regime: coin's 60-day trend sign proxy -> r28 sign
    d10["up"] = d10["r28"] > 0
    out["f_by_r28sign"] = d10.groupby("up").apply(slope)
    return out
