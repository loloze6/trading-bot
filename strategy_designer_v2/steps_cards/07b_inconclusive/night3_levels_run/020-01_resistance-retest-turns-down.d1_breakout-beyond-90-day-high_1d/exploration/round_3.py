def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    fc = "debug_info.components.breakout_dist.post_pipeline_value"
    raw = "debug_info.components.breakout_dist.last_history_value"
    rows = []
    h = 5
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
            lr = np.log(pd.Series(c)).diff()
            vol20 = lr.rolling(20, min_periods=15).std().values
            vol60 = lr.rolling(60, min_periods=40).std().values
            s = pd.Series(c)
            hi = s.shift(1).rolling(90, min_periods=30).max().values
            # touches: prior closes within 3% below the prior high, excluding the last 5 days
            touches = np.full(len(c), np.nan)
            for i in range(30, len(c)):
                past = c[max(0, i - 90):i - 5]
                if len(past) < 20 or np.isnan(hi[i]):
                    continue
                touches[i] = np.sum(past >= hi[i] * 0.97)
            idx = np.arange(0, len(c) - h, h)
            for i in idx:
                r = c[i + h] / c[i] - 1
                fresh = (i >= 1) and (rv[i - 1] <= 0 if not np.isnan(rv[i - 1]) else False)
                rows.append(dict(coin=coin, f=f[i], raw=rv[i], ex=r - drift, z=(r - drift) / sd,
                                 volratio=vol20[i] / vol60[i] if vol60[i] > 0 else np.nan,
                                 touches=touches[i], fresh=fresh,
                                 prevf=f[i - 1] if i >= 1 else np.nan))
    df = pd.DataFrame(rows)
    g = df[df.f > 0].copy()
    out = {}
    res = []
    for name, sub in [("fresh", g[g.fresh]), ("extended", g[~g.fresh])]:
        sl = stats.linregress(sub.f, sub.ex) if len(sub) > 5 else None
        res.append(dict(grp=name, n=len(sub), mean=sub.ex.mean(), med=sub.ex.median(),
                        t_mean=stats.ttest_1samp(sub.ex, 0).statistic,
                        slope_t=(sl.slope / sl.stderr) if sl else np.nan))
    out["fresh_vs_extended"] = pd.DataFrame(res)
    gv = g.dropna(subset=["volratio"]).copy()
    gv["vq"] = pd.qcut(gv.volratio.rank(method="first"), 3, labels=False)
    r2 = []
    for q, sub in gv.groupby("vq"):
        sl = stats.linregress(sub.f, sub.ex)
        r2.append(dict(vq=q, n=len(sub), vmin=sub.volratio.min(), vmax=sub.volratio.max(),
                       mean=sub.ex.mean(), med=sub.ex.median(), slope_t=sl.slope / sl.stderr))
    out["by_volratio"] = pd.DataFrame(r2)
    gt = g.dropna(subset=["touches"]).copy()
    out["touches_summary"] = pd.Series(dict(n=len(gt), tmed=gt.touches.median(), tmax=gt.touches.max()))
    if len(gt) > 10:
        sl = stats.linregress(gt.touches, gt.ex)
        out["touches_slope"] = pd.Series(dict(slope=sl.slope, t=sl.slope / sl.stderr,
                                              spearman=stats.spearmanr(gt.touches, gt.ex).correlation))
        gt["tq"] = pd.cut(gt.touches, [-1, 0, 3, 10, 200])
        out["by_touches"] = gt.groupby("tq").agg(n=("ex", "size"), mean=("ex", "mean"), med=("ex", "median"))
    return out
