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
            ts = pd.to_datetime(df["timestamp"])
            ret60 = pd.Series(c).pct_change(60).values
            for i in range(0, n - h, h):
                r = c[i + h] / c[i] - 1
                allr.append(r)
                tmp.append((coin, w, ts.iloc[i].year, ts.iloc[i].normalize(), f[i], r, ret60[i]))
        m = np.mean(allr)
        for t in tmp:
            rows.append(dict(coin=t[0], window=t[1], year=t[2], day=t[3], fc=t[4], r=t[5], ex=t[5] - m, ret60=t[6]))
    d = pd.DataFrame(rows)
    a = d[(d.fc != 0) & d.ret60.notna()].copy()
    def pe(x, y):
        x = np.asarray(x, float); y = np.asarray(y, float); n = len(x)
        if n < 5: return dict(n=n, r=np.nan, t=np.nan)
        r = np.corrcoef(x, y)[0, 1]
        return dict(n=n, r=r, t=r * np.sqrt((n - 2) / (1 - r * r)))
    def sp(x, y):
        n = len(x)
        rho = stats.spearmanr(x, y).correlation
        return dict(n=n, rho=rho, t=rho * np.sqrt((n - 2) / (1 - rho ** 2)))
    s = a[a.fc < 0].copy()
    out["short_ret60_vs_ex_pearson"] = pd.Series(pe(s.ret60, s.ex))
    out["short_ret60_vs_ex_spearman"] = pd.Series(sp(s.ret60, s.ex))
    lo, hi = s.ex.quantile([0.02, 0.98])
    out["short_ret60_vs_ex_winsor"] = pd.Series(pe(s.ret60, s.ex.clip(lo, hi)))
    # combined signal: nearness (negative forecast) times ret60
    a["comb"] = np.where(a.fc < 0, a.fc * a.ret60, 0.0)
    out["comb_all_active"] = pd.Series(pe(a.comb, a.ex))
    s["comb"] = s.fc * s.ret60
    s["cq"] = pd.qcut(s.comb, 3, labels=["strong", "mid", "weak"])
    g = s.groupby("cq", observed=True).ex
    out["short_by_comb_tercile"] = pd.DataFrame(dict(count=g.count(), mean=g.mean(), median=g.median(),
                                                     t=g.mean() / (g.std() / np.sqrt(g.count()))))
    # day-clustered t for short side excess (signed toward short)
    s["dev"] = -s.ex
    dd = s.groupby("day").dev.sum()
    nd = len(dd)
    out["short_side_unusual_move_dayclustered"] = pd.Series(dict(mean=s.dev.mean(), days=nd,
        t=s.dev.mean() / (dd.std(ddof=1) * np.sqrt(nd) / len(s))))
    hs = s[s.ret60 >= s.ret60.median()]
    out["short_highret60_by_year"] = hs.groupby("year").ex.agg(["count", "mean", "median"])
    out["short_highret60_by_coin"] = hs.groupby("coin").ex.agg(["count", "mean", "median"])
    out["short_ret60_quantiles"] = s.ret60.quantile([0.1, 0.33, 0.5, 0.67, 0.9])
    return out
