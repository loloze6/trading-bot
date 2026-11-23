def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 5
    rows = []
    for coin, wins in bars.items():
        rr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rr += list(c[idx + H] / c[idx] - 1)
        dr = np.mean(rr)
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values
            n = len(c)
            wret = c[-1] / c[0] - 1
            idx = np.arange(0, n - H, H)
            for i in idx:
                p30 = c[i] / c[i - 30] - 1 if i >= 30 else np.nan
                p60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                hi30 = c[i] / c[max(0, i - 29):i + 1].max() if i >= 29 else np.nan
                r5 = c[i] / c[i - 5] - 1 if i >= 5 else np.nan
                rows.append(dict(coin=coin, w=w, f=f[i], ex=c[i + H] / c[i] - 1 - dr,
                                 p30=p30, p60=p60, hi30=hi30, r5=r5, wup=wret > 0))
    d = pd.DataFrame(rows)
    def wt(g):
        g = g[g.f > 0]
        if len(g) < 5: return pd.Series(dict(n=len(g)))
        x = g.ex.values; ww = g.f.values
        m = np.sum(ww * x) / ww.sum()
        se = np.sqrt(np.sum(ww**2 * (x - m)**2) / ww.sum()**2 * len(x) / (len(x) - 1))
        return pd.Series(dict(n=len(g), wmean=m, wt=m / se, umean=x.mean(),
                              ut=x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))))
    out = {}
    a = d[d.f > 0].ex; b = d[d.f == 0].ex
    from scipy import stats
    out["pos_minus_zero_welch"] = pd.Series(dict(diff=a.mean() - b.mean(), t=stats.ttest_ind(a, b, equal_var=False).statistic, na=len(a), nb=len(b)))
    out["by_window_up_diag"] = d.groupby("wup").apply(wt)
    for col in ["p30", "p60", "hi30", "r5"]:
        dd = d.dropna(subset=[col]).copy()
        dd["q"] = pd.qcut(dd[col], 3, labels=False, duplicates="drop")
        out["by_" + col + "_tercile"] = dd.groupby("q").apply(wt)
    dd = d.dropna(subset=["p30"])
    up = dd[(dd.p30 > 0) & (dd.f > 0)].copy()
    up["fq"] = pd.qcut(up.f, 3, labels=False, duplicates="drop")
    out["p30up_by_f_tercile"] = up.groupby("fq").ex.agg(["count", "mean", "std"])
    out["zero_f_by_p30_sign"] = dd[dd.f == 0].groupby(dd.p30 > 0).ex.agg(["count", "mean"])
    return out
