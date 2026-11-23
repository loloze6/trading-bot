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
            r2 = np.full(n, np.nan); r2[2:] = c[2:]/c[:-2]-1
            f1 = np.full(n, np.nan); f1[:-1] = c[1:]/c[:-1]-1
            f3 = np.full(n, np.nan); f3[:-3] = c[3:]/c[:-3]-1
            s = pd.Series(r1)
            vol20 = s.rolling(20).std().values
            vrel = (pd.Series(v)/pd.Series(v).rolling(30).mean().shift(1)).values
            r7 = np.full(n, np.nan); r7[7:] = c[7:]/c[:-7]-1
            # grid positions for drift
            grid = np.arange(0, n-3, 3)
            for i in range(n):
                rows.append((coin, w, ts.iloc[i].weekday(), ts.iloc[i].year, r1[i], r2[i], r7[i], f1[i], f3[i], vol20[i], vrel[i], i % 3 == 0))
    df = pd.DataFrame(rows, columns=["coin","w","wd","yr","r1","r2","r7","f1","f3","vol20","vrel","grid"])
    drift = df[df.grid].groupby("coin")["f3"].mean()
    df["f3a"] = df["f3"] - df["coin"].map(drift)
    d1 = df.groupby("coin")["f1"].mean()
    df["f1a"] = df["f1"] - df["coin"].map(d1)
    out = {}
    def reg(x, y):
        m = np.isfinite(x) & np.isfinite(y)
        if m.sum() < 30: return (np.nan, np.nan, int(m.sum()))
        r = stats.linregress(x[m], y[m])
        return (r.slope, r.slope/r.stderr, int(m.sum()))
    # slope of 3-day fwd on the day's own return, by weekday, falls and rises separately (z by vol20)
    res = []
    for wd in range(7):
        g = df[df.wd == wd]
        for side, gg in (("fall", g[g.r1 < 0]), ("rise", g[g.r1 > 0])):
            s_, t_, n_ = reg(gg["r1"].values, gg["f3a"].values)
            res.append((wd, side, s_, t_, n_, gg["f3a"].mean(), gg["f3a"].mean()/gg["f3a"].std()*np.sqrt(len(gg.dropna(subset=["f3a"])))))
    out["slope f3a on own r1 by weekday(0=Mon)"] = pd.DataFrame(res, columns=["wd","side","slope","t","n","mean_f3a","t_mean"])
    # next-day return by weekday
    out["next-day adj ret by weekday of bar"] = df.groupby("wd")["f1a"].agg(["mean","count", lambda x: x.mean()/x.std()*np.sqrt(x.count())])
    # Sunday fall: volume interaction
    sun = df[(df.wd == 6) & (df.r1 < 0)].dropna(subset=["f3a","vrel"]).copy()
    sun["vq"] = pd.qcut(sun["vrel"], 3, labels=["lowvol","mid","highvol"])
    out["sun fall by rel volume"] = sun.groupby("vq").apply(lambda g: pd.Series({"n": len(g), "mean_f3a": g.f3a.mean(), "slope_t": reg(g.r1.values, g.f3a.values)[1], "slope": reg(g.r1.values, g.f3a.values)[0]}))
    # Sunday fall: vol regime
    sun2 = df[(df.wd == 6) & (df.r1 < 0)].dropna(subset=["f3a","vol20"]).copy()
    sun2["volq"] = pd.qcut(sun2["vol20"], 3, labels=["lowvol","mid","highvol"])
    out["sun fall by vol20"] = sun2.groupby("volq").apply(lambda g: pd.Series({"n": len(g), "mean_f3a": g.f3a.mean(), "slope_t": reg(g.r1.values, g.f3a.values)[1]}))
    # Sunday fall by prior 7-day trend
    sun3 = df[(df.wd == 6) & (df.r1 < 0)].dropna(subset=["f3a","r7"]).copy()
    sun3["tq"] = pd.qcut(sun3["r7"], 3, labels=["down7","mid","up7"])
    out["sun fall by r7"] = sun3.groupby("tq").apply(lambda g: pd.Series({"n": len(g), "mean_f3a": g.f3a.mean(), "slope_t": reg(g.r1.values, g.f3a.values)[1]}))
    # weekend 2-day (Fri close->Sun close) return
    sw = df[df.wd == 6]
    out["sun 2day r2 slope (all)"] = pd.Series(reg(sw.r2.values, sw.f3a.values), index=["slope","t","n"])
    # year breakdown of Sunday fall cases
    sf = df[(df.wd == 6) & (df.r1 < 0)]
    out["sun fall by year"] = sf.groupby("yr").apply(lambda g: pd.Series({"n": g.f3a.count(), "mean_f3a": g.f3a.mean(), "slope_t": reg(g.r1.values, g.f3a.values)[1]}))
    # book: daily returns by weekday, top/bottom days
    dd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd)
    D["day"] = pd.to_datetime(D["day"], utc=True)
    bk = D.groupby(["w","day"])["book_return"].mean().dropna().reset_index()
    bk["wd"] = bk["day"].dt.weekday
    out["book daily ret by weekday"] = bk.groupby("wd")["book_return"].agg(["mean","std","count"])
    q = bk["book_return"].quantile([0.02, 0.98])
    bk["tail"] = np.where(bk.book_return <= q.iloc[0], "worst2%", np.where(bk.book_return >= q.iloc[1], "best2%", "mid"))
    out["book tails by weekday"] = pd.crosstab(bk["wd"], bk["tail"])
    return out
