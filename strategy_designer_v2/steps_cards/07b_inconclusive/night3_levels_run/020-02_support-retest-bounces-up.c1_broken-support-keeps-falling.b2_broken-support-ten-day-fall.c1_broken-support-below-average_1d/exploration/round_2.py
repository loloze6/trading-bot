def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; h = 10
    drift = {}; usual = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            cl = df["close"].values
            for i in range(0, len(cl) - h, h):
                rs.append(cl[i + h] / cl[i] - 1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; f = df["forecast"].values
            raw = df["debug_info.components.support_cluster.last_history_value"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r20 = pd.Series(cl).pct_change(20).values
            for i in range(0, len(cl) - h, h):
                if df["regime"].iloc[i] == "trending" and not np.isnan(raw[i]) and raw[i] > 0:
                    mv = -(cl[i + h] / cl[i] - 1 - drift[c])
                    rows.append(dict(coin=c, year=yr[i], f=f[i], raw=raw[i], r20=r20[i], mv=mv, st=mv / usual[c]))
    d = pd.DataFrame(rows)
    def summ(g):
        n = len(g)
        return pd.Series(dict(n=n, mean=g.mv.mean(), t=g.mv.mean() / (g.mv.std() / np.sqrt(n)) if n > 2 else np.nan, strength=g.st.mean()))
    out = {}
    out["all_active_raw_pos"] = summ(d)
    out["raw_describe"] = d.raw.describe()
    out["spearman_raw_mv_all"] = pd.Series(stats.spearmanr(d.raw, d.mv))
    c2 = d[d.f <= -2]
    out["spearman_raw_mv_cases"] = pd.Series(stats.spearmanr(c2.raw, c2.mv))
    d["rq"] = pd.qcut(d.raw.rank(method="first"), 5, labels=False)
    out["by_raw_q5_all"] = d.groupby("rq").apply(summ)
    out["raw_q5_edges"] = d.groupby("rq").raw.agg(["min", "max"])
    c2 = c2.copy(); med = c2.raw.median(); c2["hi"] = c2.raw > med
    out["cases_rawhalf_by_coin_t"] = c2.groupby(["coin", "hi"]).apply(summ)["t"].unstack()
    out["cases_rawhalf_by_year_mean"] = c2.groupby(["year", "hi"]).apply(summ)["mean"].unstack()
    hi = c2[c2.hi]; lo = c2[~c2.hi]
    out["hi_minus_lo_welch"] = pd.Series(dict(diff=hi.mv.mean() - lo.mv.mean(), t=stats.ttest_ind(hi.mv, lo.mv, equal_var=False).statistic, n_hi=len(hi), n_lo=len(lo)))
    return out
