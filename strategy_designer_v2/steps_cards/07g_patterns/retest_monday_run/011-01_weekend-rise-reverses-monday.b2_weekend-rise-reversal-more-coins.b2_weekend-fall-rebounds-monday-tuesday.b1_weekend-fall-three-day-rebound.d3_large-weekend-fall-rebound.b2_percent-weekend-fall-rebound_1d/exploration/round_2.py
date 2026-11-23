def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float).values
            v = b["volume"].astype(float).values
            ts = pd.to_datetime(b["timestamp"], utc=True)
            n = len(c)
            if n < 40: continue
            r1 = np.full(n, np.nan); r1[1:] = c[1:]/c[:-1]-1
            f3 = np.full(n, np.nan); f3[:-3] = c[3:]/c[:-3]-1
            f1 = np.full(n, np.nan); f1[:-1] = c[1:]/c[:-1]-1
            vrel = (pd.Series(v)/pd.Series(v).rolling(30).mean().shift(1)).values
            mad = pd.Series(np.abs(r1)).rolling(60, min_periods=30).mean().shift(1).values
            for i in range(n):
                rows.append((coin, w, ts.iloc[i].weekday(), ts.iloc[i].year, r1[i], f1[i], f3[i], vrel[i], mad[i], i % 3 == 0))
    df = pd.DataFrame(rows, columns=["coin","w","wd","yr","r1","f1","f3","vrel","mad","grid"])
    drift = df[df.grid].groupby("coin")["f3"].mean()
    df["f3a"] = df["f3"] - df["coin"].map(drift)
    out = {}
    def reg(x, y):
        m = np.isfinite(x) & np.isfinite(y)
        if m.sum() < 30: return (np.nan, np.nan, int(m.sum()))
        r = stats.linregress(x[m], y[m])
        return (r.slope, r.slope/r.stderr, int(m.sum()))
    def tm(x):
        x = x.dropna(); return x.mean()/x.std()*np.sqrt(len(x)) if len(x) > 2 else np.nan
    # Sunday falls: interaction depth x low volume
    sf = df[(df.wd == 6) & (df.r1 < 0)].dropna(subset=["f3a","vrel","mad"]).copy()
    sf["depth"] = -sf.r1
    sf["lowv"] = -np.log(sf.vrel)
    X = np.column_stack([np.ones(len(sf)), sf.depth, sf.lowv, sf.depth*sf.lowv])
    y = sf.f3a.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = res @ res / (len(y)-4)
    se = np.sqrt(np.diag(s2*np.linalg.inv(X.T @ X)))
    out["sun fall OLS: const, depth, lowvol, depth*lowvol"] = pd.DataFrame({"beta": beta, "t": beta/se}, index=["const","depth","lowv","depth_x_lowv"])
    out["sun fall n"] = len(sf)
    # depth/lowvol product as single score
    sf["score"] = sf.depth / sf.vrel
    out["sun fall slope f3a on depth/vrel"] = pd.Series(reg(sf.score.values, sf.f3a.values), index=["slope","t","n"])
    sf["sq"] = pd.qcut(sf.score, 5, labels=False)
    out["sun fall quintiles of depth/vrel"] = sf.groupby("sq")["f3a"].agg(["mean","count", tm])
    # by year for low-volume sunday falls slope
    lo = sf[sf.vrel < sf.vrel.quantile(1/3)]
    out["low-vol sun fall slope by year"] = lo.groupby("yr").apply(lambda g: pd.Series({"n": len(g), "slope_t": reg(-g.depth.values, g.f3a.values)[1], "mean": g.f3a.mean()}))
    # Sunday rises
    sr = df[(df.wd == 6) & (df.r1 > 0)].dropna(subset=["f3a","vrel"]).copy()
    sr["vq"] = pd.qcut(sr.vrel, 3, labels=["lowvol","mid","highvol"])
    out["sun rise by rel volume"] = sr.groupby("vq").apply(lambda g: pd.Series({"n": len(g), "mean_f3a": g.f3a.mean(), "t_mean": tm(g.f3a), "slope_t": reg(g.r1.values, g.f3a.values)[1]}))
    sr["rz"] = sr.r1 / df.loc[sr.index, "mad"]
    sr["zq"] = pd.qcut(sr.rz.dropna(), 4, labels=False)
    out["sun rise by size quartile (vol units)"] = sr.groupby("zq")["f3a"].agg(["mean","count", tm])
    out["sun rise by year"] = sr.groupby("yr")["f3a"].agg(["mean","count", tm])
    # total move for short on sunday rise (raw f3, sign flipped)
    out["sun rise raw f3 mean, short side"] = pd.Series({"mean_minus_f3": -sr.f3.mean(), "t": tm(-sr.f3), "n": sr.f3.count()})
    # Sunday all: f3a vs r1 continuous across both signs, low vol tercile
    sa = df[df.wd == 6].dropna(subset=["f3a","vrel"])
    out["sun all slope by vol tercile"] = sa.groupby(pd.qcut(sa.vrel, 3, labels=["low","mid","high"])).apply(lambda g: pd.Series({"n": len(g), "slope": reg(g.r1.values, g.f3a.values)[0], "t": reg(g.r1.values, g.f3a.values)[1]}))
    # weekday control: same volume split for Wed/Thu falls
    wf = df[(df.wd.isin([1,2,3])) & (df.r1 < 0)].dropna(subset=["f3a","vrel"])
    out["Tue-Thu fall slope by vol tercile"] = wf.groupby(pd.qcut(wf.vrel, 3, labels=["low","mid","high"])).apply(lambda g: pd.Series({"n": len(g), "slope": reg(g.r1.values, g.f3a.values)[0], "t": reg(g.r1.values, g.f3a.values)[1]}))
    return out
