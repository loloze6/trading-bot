def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    fc = "debug_info.components.breakout_dist.post_pipeline_value"
    raw = "debug_info.components.breakout_dist.last_history_value"
    rows = []
    for h in [5, 10]:
        for coin, ws in bars.items():
            allr = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr += list(c[idx + h] / c[idx] - 1)
            drift = np.mean(allr); sd = np.std(allr)
            for w, b in ws.items():
                c = b["close"].values
                f = b[fc].fillna(b["forecast"]).values
                rv = b[raw].values
                yr = pd.to_datetime(b["timestamp"]).dt.year.values
                hi = pd.Series(c).shift(1).rolling(90, min_periods=90).max().values
                idx = np.arange(0, len(c) - h, h)
                for i in idx:
                    r = c[i + h] / c[i] - 1
                    rows.append(dict(h=h, coin=coin, w=w, yr=yr[i], f=f[i], raw=rv[i],
                                     dist=(c[i] / hi[i] - 1) if not np.isnan(hi[i]) else np.nan,
                                     ex=r - drift, z=(r - drift) / sd))
    df = pd.DataFrame(rows)
    out = {}
    res = []
    for h in [5, 10]:
        g = df[(df.h == h) & (df.f > 0)].dropna(subset=["raw"])
        for name, x in [("raw", g.raw), ("dist", g.dist), ("f", g.f)]:
            gg = g.assign(x=x).dropna(subset=["x"])
            sl = stats.linregress(gg.x, gg.ex)
            lo, hi_ = gg.ex.quantile([0.05, 0.95])
            exw = gg.ex.clip(lo, hi_)
            xl, xh = gg.x.quantile([0.05, 0.95])
            xw = gg.x.clip(xl, xh)
            slw = stats.linregress(xw, exw)
            top = gg.ex.abs().nlargest(5).index
            g2 = gg.drop(top)
            sl2 = stats.linregress(g2.x, g2.ex)
            res.append(dict(h=h, x=name, n=len(gg), xmed=gg.x.median(), xmax=gg.x.max(),
                            t=sl.slope / sl.stderr, t_wins=slw.slope / slw.stderr,
                            t_drop5=sl2.slope / sl2.stderr,
                            spearman=stats.spearmanr(gg.x, gg.ex).correlation,
                            corr_f_raw=np.corrcoef(gg.f, gg.raw)[0, 1]))
    out["slopes"] = pd.DataFrame(res)
    g = df[(df.h == 10) & (df.f > 0)].dropna(subset=["raw"]).copy()
    g["q"] = pd.qcut(g.raw.rank(method="first"), 4, labels=False)
    out["h10_by_rawq"] = g.groupby("q").agg(n=("ex", "size"), rmin=("raw", "min"), rmax=("raw", "max"),
                                            mean=("ex", "mean"), med=("ex", "median"), meanz=("z", "mean"))
    out["h10_by_coin"] = g.groupby("coin").agg(n=("ex", "size"), mean=("ex", "mean"), med=("ex", "median"),
                                               rawmax=("raw", "max"))
    g5 = df[(df.h == 5) & (df.f > 0)].dropna(subset=["raw"]).copy()
    g5["q"] = pd.qcut(g5.raw.rank(method="first"), 4, labels=False)
    out["h5_by_rawq"] = g5.groupby("q").agg(n=("ex", "size"), rmin=("raw", "min"), rmax=("raw", "max"),
                                            mean=("ex", "mean"), med=("ex", "median"), meanz=("z", "mean"))
    # non-breakout distance groups at h5 for the near-high comparison
    a = df[(df.h == 5)].dropna(subset=["dist"]).copy()
    a["dq"] = pd.cut(a.dist, [-1, -0.3, -0.15, -0.05, 0, 0.05, 0.15, 10])
    out["h5_by_dist_all"] = a.groupby("dq").agg(n=("ex", "size"), mean=("ex", "mean"), med=("ex", "median"),
                                                meanz=("z", "mean"))
    return out
