def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    h = 20
    rows = []
    for coin, wins in bars.items():
        allr = []; tmp = []
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values
            n = len(c)
            ret60 = pd.Series(c).pct_change(60).values
            raw = df.get("debug_info.components.dist_low.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            past20 = pd.Series(c).pct_change(20).values
            for i in range(0, n - h, h):
                r = c[i + h] / c[i] - 1
                allr.append(r)
                tmp.append((coin, w, f[i], r, ret60[i], raw[i], past20[i]))
        m = np.mean(allr)
        for t in tmp:
            rows.append(dict(coin=t[0], window=t[1], fc=t[2], r=t[3], ex=t[3] - m,
                             ret60=t[4], dist=t[5], p20=t[6]))
    d = pd.DataFrame(rows)
    a = d[d.fc != 0].copy()
    def sp(g):
        if len(g) < 5: return pd.Series(dict(n=len(g), rho=np.nan, t=np.nan))
        rho = stats.spearmanr(g.fc, g.ex).correlation; n = len(g)
        return pd.Series(dict(n=n, rho=rho, t=rho * np.sqrt((n - 2) / (1 - rho ** 2))))
    def pe(g):
        if len(g) < 5: return pd.Series(dict(n=len(g), r=np.nan, t=np.nan))
        r = np.corrcoef(g.fc, g.ex)[0, 1]; n = len(g)
        return pd.Series(dict(n=n, r=r, t=r * np.sqrt((n - 2) / (1 - r * r))))
    out["spearman_all"] = sp(a)
    lo, hi = a.ex.quantile([0.02, 0.98])
    aw = a.assign(ex=a.ex.clip(lo, hi))
    out["pearson_winsor2pct"] = pe(aw)
    out["short_spearman"] = sp(a[a.fc < 0])
    out["short_pearson_winsor"] = pe(aw[aw.fc < 0])
    out["largest_abs_ex_by_bin"] = a.assign(bin=pd.cut(a.fc, [-21, -2, -1, 0, 2, 4, 21])).groupby("bin", observed=True).ex.agg(["max", "min", "median", "mean", "count"])
    s = a[a.fc < 0].copy()
    s["r60q"] = pd.qcut(s.ret60, 3, labels=["low60", "mid60", "high60"])
    out["short_by_ret60_tercile"] = s.groupby("r60q", observed=True).ex.agg(["count", "mean", "median"])
    out["short_by_ret60_spearman"] = s.groupby("r60q", observed=True).apply(sp)
    s["p20q"] = pd.qcut(s.p20, 2, labels=["p20_low", "p20_high"])
    out["short_by_past20"] = s.groupby("p20q", observed=True).ex.agg(["count", "mean", "median"])
    # raw distance from low (percent) on active bars
    a["distq"] = pd.qcut(a.dist, 5)
    out["by_raw_dist_quintile"] = a.groupby("distq", observed=True).ex.agg(["count", "mean", "median"])
    out["short_median_ex_by_coin"] = s.groupby("coin").ex.agg(["count", "mean", "median"])
    return out
