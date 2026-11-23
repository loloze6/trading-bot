def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def build(H):
        rows = []
        for coin, wins in bars.items():
            g_all = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    g_all.append(c[i+H]/c[i]-1)
            drift = np.mean(g_all); usual = np.std(g_all, ddof=1)
            for w, df in wins.items():
                c = df["close"].values; f = df["forecast"].values
                ts = pd.to_datetime(df["timestamp"]); n = len(c)
                for i in range(0, n - H, H):
                    rows.append({"coin": coin, "window": w, "year": ts.iloc[i].year, "f": f[i],
                                 "ex": c[i+H]/c[i]-1-drift, "str": (c[i+H]/c[i]-1-drift)/usual,
                                 "prior5": c[i]/c[i-5]-1 if i >= 5 else np.nan})
        return pd.DataFrame(rows)
    def slope(g):
        g = g.dropna(subset=["ex"])
        if len(g) < 10: return pd.Series({"n": len(g)})
        s = stats.linregress(g.f, g.ex)
        return pd.Series({"n": len(g), "slope_t": s.slope/s.stderr, "mean_ex%": 100*g.ex.mean(),
                          "mean_strength": g["str"].mean()})
    hz = {}
    for H in [5, 10, 15, 20, 30]:
        d = build(H); p = d[d.f > 0]
        s = slope(p)
        top = p[p.f >= p.f.quantile(0.6)]; bot = d[d.f <= 0]
        s["top40_minus_flat_welch_t"] = stats.ttest_ind(top.ex, bot.ex, equal_var=False).statistic
        s["top40_mean%"] = 100*top.ex.mean(); s["flat_mean%"] = 100*bot.ex.mean()
        s["all_grid_slope_t"] = stats.linregress(d.f, d.ex).slope / stats.linregress(d.f, d.ex).stderr
        hz[H] = s
        if H == 20:
            out["20d by year"] = p.groupby("year").apply(slope)
            out["20d by coin"] = p.groupby("coin").apply(slope)
            p = p.copy(); p["fq"] = pd.qcut(p.f.rank(method="first"), 5, labels=False)
            out["20d by forecast quintile"] = p.groupby("fq").apply(slope)
            pp = p.dropna(subset=["prior5"])
            X = np.column_stack([np.ones(len(pp)), pp.f, pp.prior5])
            b, *_ = np.linalg.lstsq(X, pp.ex, rcond=None)
            res = pp.ex - X @ b; s2 = res.var(ddof=3)
            se = np.sqrt(np.diag(s2*np.linalg.inv(X.T @ X)))
            out["20d ex on f and prior5"] = pd.Series({"t_f": b[1]/se[1], "t_prior5": b[2]/se[2], "n": len(pp)})
        if H == 5:
            pp = p.dropna(subset=["prior5"])
            X = np.column_stack([np.ones(len(pp)), pp.f, pp.prior5])
            b, *_ = np.linalg.lstsq(X, pp.ex, rcond=None)
            res = pp.ex - X @ b; s2 = res.var(ddof=3)
            se = np.sqrt(np.diag(s2*np.linalg.inv(X.T @ X)))
            out["5d ex on f and prior5"] = pd.Series({"t_f": b[1]/se[1], "t_prior5": b[2]/se[2], "n": len(pp)})
    out["horizons, own non-overlapping grid"] = pd.DataFrame(hz).T
    return out
