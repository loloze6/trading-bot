def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    fc = "debug_info.components.breakout_dist.post_pipeline_value"
    raw = "debug_info.components.breakout_dist.last_history_value"
    out = {}
    rows = []
    for h in [1, 5, 10, 20]:
        for coin, ws in bars.items():
            # drift
            allr = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr += list(c[idx + h] / c[idx] - 1)
            drift = np.mean(allr); sd = np.std(allr)
            for w, b in ws.items():
                c = b["close"].values
                f = b[fc].fillna(b["forecast"]).values if fc in b else b["forecast"].values
                rv = b[raw].values if raw in b else np.full(len(c), np.nan)
                yr = pd.to_datetime(b["timestamp"]).dt.year.values
                # prior 20-day return for regime
                idx = np.arange(0, len(c) - h, h)
                for i in idx:
                    r = c[i + h] / c[i] - 1
                    p20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                    rows.append(dict(h=h, coin=coin, w=w, yr=yr[i], f=f[i], raw=rv[i],
                                     ex=r - drift, z=(r - drift) / sd, p20=p20))
    df = pd.DataFrame(rows)
    res = []
    for h, g in df.groupby("h"):
        br = g[g.f > 0]; nb = g[g.f <= 0]
        sl = stats.linregress(br.f, br.ex)
        t_slope = sl.slope / sl.stderr
        res.append(dict(h=h, n_br=len(br), mean_br=br.ex.mean(),
                        t_br=stats.ttest_1samp(br.ex, 0).statistic,
                        mean_nb=nb.ex.mean(), welch_br_nb=stats.ttest_ind(br.ex, nb.ex, equal_var=False).statistic,
                        slope_t=t_slope, med_ex=br.ex.median(), share_pos=(br.ex > 0).mean()))
    out["by_horizon"] = pd.DataFrame(res)
    g5 = df[(df.h == 5) & (df.f > 0)].copy()
    g5["fq"] = pd.qcut(g5.f.rank(method="first"), 4, labels=False)
    out["h5_by_fquart"] = g5.groupby("fq").agg(n=("ex", "size"), fmin=("f", "min"), fmax=("f", "max"),
                                               mean=("ex", "mean"), med=("ex", "median"), sd=("ex", "std"))
    out["h5_by_coin"] = g5.groupby("coin").agg(n=("ex", "size"), mean=("ex", "mean"), med=("ex", "median"),
                                              corr_f=("ex", lambda s: np.corrcoef(s, g5.loc[s.index, "f"])[0, 1]))
    out["h5_by_year"] = g5.groupby("yr").agg(n=("ex", "size"), mean=("ex", "mean"), med=("ex", "median"))
    g10 = df[(df.h == 10) & (df.f > 0)].copy()
    out["h10_by_year"] = g10.groupby("yr").agg(n=("ex", "size"), mean=("ex", "mean"), med=("ex", "median"))
    # rank correlation & z-scored slope
    rows2 = []
    for h, g in df[df.f > 0].groupby("h"):
        sp = stats.spearmanr(g.f, g.ex)
        sl = stats.linregress(g.f, g.z)
        gr = g.dropna(subset=["raw"])
        slr = stats.linregress(gr.raw, gr.ex) if len(gr) > 5 else None
        rows2.append(dict(h=h, spearman=sp.correlation, sp_p=sp.pvalue, slope_t_z=sl.slope / sl.stderr,
                          slope_t_raw=(slr.slope / slr.stderr) if slr else np.nan, n_raw=len(gr)))
    out["robust_slopes"] = pd.DataFrame(rows2)
    # regime: prior 20d return
    g5b = g5.dropna(subset=["p20"]).copy()
    g5b["pq"] = pd.qcut(g5b.p20.rank(method="first"), 3, labels=False)
    out["h5_by_prior20"] = g5b.groupby("pq").agg(n=("ex", "size"), pmin=("p20", "min"), pmax=("p20", "max"),
                                                 mean=("ex", "mean"), med=("ex", "median"))
    return out
