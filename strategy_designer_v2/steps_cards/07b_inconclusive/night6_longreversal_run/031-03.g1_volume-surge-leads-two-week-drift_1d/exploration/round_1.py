def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            v = df["volume"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (7, 14, 28):
                for i in range(0, n - h, h):
                    r60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                    rows.append(dict(coin=coin, win=w, h=h, f=f[i], ret=c[i + h] / c[i] - 1,
                                     year=yr[i], r60=r60,
                                     r14=c[i] / c[i - 14] - 1 if i >= 14 else np.nan))
    d = pd.DataFrame(rows)
    d["dret"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")

    def reg(g):
        g = g.dropna(subset=["f", "dret"])
        if len(g) < 10 or g["f"].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g["f"], g["dret"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))

    out["by_horizon"] = d.groupby("h").apply(reg)
    d14 = d[d.h == 14].copy()
    out["by_coin_h14"] = d14.groupby("coin").apply(reg)
    out["by_year_h14"] = d14.groupby("year").apply(reg)
    d14["side"] = np.sign(d14["f"])
    out["side_h14_mean_dret"] = d14.groupby("side")["dret"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    d14["fq"] = pd.qcut(d14["f"], 5, labels=False, duplicates="drop")
    out["quintile_h14"] = d14.groupby("fq").agg(n=("dret", "size"), fmean=("f", "mean"), dret=("dret", "mean"))
    # condition on prior 60-day move (brief's situation) and prior 14-day return sign
    d14["up60"] = np.sign(d14["r60"])
    out["by_prior60_sign"] = d14.dropna(subset=["r60"]).groupby("up60").apply(reg)
    d14["up14"] = np.sign(d14["r14"])
    out["by_prior14_sign"] = d14.dropna(subset=["r14"]).groupby("up14").apply(reg)
    # volume surge x prior return direction: signed forecast * sign(r14)
    g = d14.dropna(subset=["r14"]).copy()
    g["fx"] = g["f"] * np.sign(g["r14"])
    r = stats.linregress(g["fx"], g["dret"])
    out["f_times_sign_r14_h14"] = pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))
    g = d.dropna(subset=["r60"]).copy()
    g["fx"] = g["f"] * np.sign(g["r14"])
    out["fx14_by_h"] = g.assign(f=g["fx"]).groupby("h").apply(reg)
    # brief's own: 60-day return standardized -> reversal
    for h in (14, 28):
        gg = d[(d.h == h)].dropna(subset=["r60"])
        r = stats.linregress(gg["r60"], gg["dret"])
        out[f"r60_slope_h{h}"] = pd.Series(dict(n=len(gg), slope=r.slope, t=r.slope / r.stderr))
    return out
