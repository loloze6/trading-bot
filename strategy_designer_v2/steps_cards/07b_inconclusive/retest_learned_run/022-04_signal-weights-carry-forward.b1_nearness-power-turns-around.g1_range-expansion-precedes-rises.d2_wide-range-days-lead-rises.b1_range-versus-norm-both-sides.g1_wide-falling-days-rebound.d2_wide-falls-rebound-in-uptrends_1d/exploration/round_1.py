def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    # normal drift per coin per horizon
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            rng = (df["high"] - df["low"]) / df["close"].shift(1)
            rmult = (rng / rng.shift(1).rolling(30, min_periods=20).mean()).values
            down = (df["close"] < df["close"].shift(1)).values
            ret1 = df["close"].pct_change().values
            ret30 = (df["close"] / df["close"].shift(30) - 1).values
            fc = df["forecast"].values
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=c, w=w, h=h, fc=fc[i], rm=rmult[i], down=down[i],
                                     r1=ret1[i], r30=ret30[i], reg=df["regime"].iloc[i],
                                     ex=cl[i + h] / cl[i] - 1 - drift[(c, h)],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    out = {}
    def reg(sub, x="fc"):
        sub = sub.dropna(subset=[x, "ex"])
        if len(sub) < 10: return (np.nan, np.nan, len(sub))
        r = stats.linregress(sub[x], sub["ex"])
        return (r.slope, r.slope / r.stderr, len(sub))
    # by horizon, forecast>0 cases
    t = []
    for h in H:
        s = d[(d.h == h) & (d.fc > 0)]
        sl, tt, n = reg(s)
        t.append(dict(h=h, slope=sl, t=tt, n=n, mean_ex=s.ex.mean(), t_mean=stats.ttest_1samp(s.ex, 0).statistic))
    out["by_horizon_fc>0"] = pd.DataFrame(t)
    # by horizon, range multiple on down days vs up days
    t = []
    for h in H:
        for dn in [True, False]:
            s = d[(d.h == h) & (d.down == dn)]
            sl, tt, n = reg(s, "rm")
            t.append(dict(h=h, down=dn, slope=sl, t=tt, n=n))
    out["rangemult_slope_down_vs_up"] = pd.DataFrame(t)
    s3 = d[(d.h == 3) & (d.fc > 0)].copy()
    out["by_coin_h3"] = pd.DataFrame({c: reg(g) for c, g in s3.groupby("coin")}, index=["slope", "t", "n"]).T
    out["by_year_h3"] = pd.DataFrame({y: reg(g) for y, g in s3.groupby("year")}, index=["slope", "t", "n"]).T
    out["by_regime_h3"] = pd.DataFrame({r: reg(g) for r, g in s3.groupby("reg")}, index=["slope", "t", "n"]).T
    # quintiles of range multiple among down days, h=3 and h=5
    for h in [3, 5]:
        s = d[(d.h == h) & (d.down)].dropna(subset=["rm"]).copy()
        s["q"] = pd.qcut(s.rm, 5, labels=False)
        g = s.groupby("q").agg(rm=("rm", "mean"), ex=("ex", "mean"), n=("ex", "size"), sd=("ex", "std"))
        g["t"] = g.ex / (g.sd / np.sqrt(g.n))
        out[f"down_rm_quintiles_h{h}"] = g
    # day-return size on down days
    s = d[(d.h == 3) & (d.down)].dropna(subset=["r1"]).copy()
    s["q"] = pd.qcut(s.r1, 5, labels=False)
    g = s.groupby("q").agg(r1=("r1", "mean"), ex=("ex", "mean"), n=("ex", "size"), sd=("ex", "std"))
    g["t"] = g.ex / (g.sd / np.sqrt(g.n)); out["down_dayret_quintiles_h3"] = g
    # regime by r30 sign within top range quintile
    s = d[(d.h == 3) & (d.down)].dropna(subset=["rm", "r30"]).copy()
    s["top"] = s.rm > s.rm.quantile(0.8)
    g = s.groupby(["top", s.r30 > 0]).agg(ex=("ex", "mean"), n=("ex", "size"), sd=("ex", "std"))
    g["t"] = g.ex / (g.sd / np.sqrt(g.n)); out["down_top_rm_by_r30sign_h3"] = g
    return out
