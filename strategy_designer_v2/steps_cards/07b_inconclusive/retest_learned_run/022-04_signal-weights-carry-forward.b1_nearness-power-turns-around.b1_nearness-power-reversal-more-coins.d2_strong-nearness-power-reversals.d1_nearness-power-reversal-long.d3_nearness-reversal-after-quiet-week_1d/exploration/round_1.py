def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    bars = data["bars"]
    rows = []
    allgrid = []
    for coin, wins in bars.items():
        # coin drift: mean 5d return over all grid bars of all windows
        g_all = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                g_all.append(c[i+H]/c[i]-1)
        drift = np.mean(g_all) if g_all else np.nan
        usual = np.std(g_all, ddof=1) if len(g_all) > 1 else np.nan
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for i in range(0, n, H):
                r = {}
                r["coin"] = coin; r["window"] = w; r["year"] = ts.iloc[i].year
                r["f"] = f[i]
                r["fwd5"] = c[i+H]/c[i]-1 if i+H < n else np.nan
                r["fwd2"] = c[i+2]/c[i]-1 if i+2 < n else np.nan
                r["fwd10"] = c[i+10]/c[i]-1 if i+10 < n else np.nan
                r["fwd20"] = c[i+20]/c[i]-1 if i+20 < n else np.nan
                r["prior5"] = c[i]/c[i-5]-1 if i-5 >= 0 else np.nan
                r["prior20"] = c[i]/c[i-20]-1 if i-20 >= 0 else np.nan
                r["drift"] = drift; r["usual"] = usual
                rows.append(r)
    d = pd.DataFrame(rows)
    d["ex5"] = d["fwd5"] - d["drift"]
    pos = d[(d.f > 0) & d.ex5.notna()].copy()
    neg = d[(d.f <= 0) & d.ex5.notna()].copy()
    out = {}
    def tm(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["pos vs zero-forecast ex5"] = pd.DataFrame({"pos": tm(pos.ex5), "zero": tm(neg.ex5)}).T
    # forecast quintiles
    pos["fq"] = pd.qcut(pos.f.rank(method="first"), 5, labels=False)
    out["by forecast quintile"] = pos.groupby("fq").apply(lambda g: pd.concat([tm(g.ex5), pd.Series({"fmean": g.f.mean()})]))
    # slope by coin
    def slope(g):
        g = g.dropna(subset=["ex5"])
        if len(g) < 10: return pd.Series({"n": len(g)})
        s = stats.linregress(g.f, g.ex5)
        return pd.Series({"n": len(g), "slope_t": s.slope/s.stderr, "mean_ex%": 100*g.ex5.mean()})
    out["by coin"] = pos.groupby("coin").apply(slope)
    out["by year"] = pos.groupby("year").apply(slope)
    # prior5 bins
    pp = pos.dropna(subset=["prior5"]).copy()
    pp["pq"] = pd.qcut(pp.prior5.rank(method="first"), 5, labels=False)
    out["by prior5 quintile"] = pp.groupby("pq").apply(lambda g: pd.concat([tm(g.ex5), slope(g)[["slope_t"]], pd.Series({"prior5mean%": 100*g.prior5.mean()})]))
    out["slope within prior<=0 / >0"] = pd.DataFrame({"le0": slope(pp[pp.prior5 <= 0]), "gt0": slope(pp[pp.prior5 > 0])}).T
    # other horizons (excess vs mean of same horizon over all grid bars)
    hz = {}
    for col in ["fwd2", "fwd5", "fwd10", "fwd20"]:
        dm = d.groupby("coin")[col].transform("mean")
        e = d[col] - dm
        sel = (d.f > 0) & e.notna()
        s = stats.linregress(d.f[sel], e[sel])
        hz[col] = {"n": sel.sum(), "mean_ex_pos%": 100*e[sel].mean(), "slope_t": s.slope/s.stderr,
                   "mean_ex_zero%": 100*e[(d.f <= 0) & e.notna()].mean()}
    out["horizons"] = pd.DataFrame(hz).T
    # prior20 effect
    p2 = pos.dropna(subset=["prior20"])
    out["prior20<=0 minus >0"] = pd.Series({"le0": 100*p2[p2.prior20<=0].ex5.mean(), "gt0": 100*p2[p2.prior20>0].ex5.mean(),
        "welch_t": stats.ttest_ind(p2[p2.prior20<=0].ex5, p2[p2.prior20>0].ex5, equal_var=False).statistic,
        "n_le0": (p2.prior20<=0).sum(), "n_gt0": (p2.prior20>0).sum()})
    # whole sample: prior5 reversal regardless of forecast
    a = d.dropna(subset=["ex5","prior5"])
    out["all grid prior5<=0 minus >0"] = pd.Series({"le0": 100*a[a.prior5<=0].ex5.mean(), "gt0": 100*a[a.prior5>0].ex5.mean(),
        "welch_t": stats.ttest_ind(a[a.prior5<=0].ex5, a[a.prior5>0].ex5, equal_var=False).statistic,
        "n": len(a)})
    out["share positive forecast"] = float((d.f > 0).mean())
    return out
