def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def grid_rows(h):
        rows = []
        for coin, wins in bars.items():
            allr = []
            tmp = []
            for w, df in wins.items():
                c = df["close"].values
                f = df["forecast"].values
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                n = len(c)
                for i in range(0, n - h, h):
                    r = c[i + h] / c[i] - 1
                    allr.append(r)
                    tmp.append((coin, w, yr[i], f[i], r, i))
            m = np.mean(allr) if allr else np.nan
            for t in tmp:
                rows.append(dict(coin=t[0], window=t[1], year=t[2], fc=t[3], r=t[4], ex=t[4] - m, pos=t[5]))
        return pd.DataFrame(rows)
    def summ(g):
        n = len(g)
        mu = g["ex"].mean()
        sd = g["ex"].std(ddof=1)
        return pd.Series(dict(n=n, mean_ex=mu, t=mu / (sd / np.sqrt(n)) if n > 1 and sd > 0 else np.nan,
                              mean_fc=g["fc"].mean()))
    def corr(g):
        if len(g) < 5: return pd.Series(dict(n=len(g), r=np.nan, t=np.nan))
        r = np.corrcoef(g["fc"], g["ex"])[0, 1]
        n = len(g)
        return pd.Series(dict(n=n, r=r, t=r * np.sqrt((n - 2) / (1 - r * r))))
    d = grid_rows(20)
    a = d[d.fc != 0].copy()
    out["check_overall"] = corr(a)
    a["bin"] = pd.cut(a.fc, [-21, -4, -2, -1, 0, 1, 2, 3, 4, 21])
    out["by_fc_bin"] = a.groupby("bin", observed=True).apply(summ)
    a["side"] = np.where(a.fc < 0, "short", "long")
    out["by_side_corr"] = a.groupby("side").apply(corr)
    out["by_side_ex"] = a.groupby("side").apply(summ)
    out["by_coin_corr"] = a.groupby("coin").apply(corr)
    out["by_year_corr"] = a.groupby("year").apply(corr)
    out["by_year_short_ex"] = a[a.fc < 0].groupby("year").apply(summ)
    # inactive grid bars for comparison
    out["flat_grid_ex"] = summ(d[d.fc == 0])
    # other horizons
    hz = {}
    for h in [5, 10, 40, 60]:
        dh = grid_rows(h)
        ah = dh[dh.fc != 0]
        c = corr(ah)
        s = ah[ah.fc <= -2]
        hz[h] = dict(n=c["n"], r=c["r"], t=c["t"], short_n=len(s), short_ex=s["ex"].mean(),
                     long_ex=ah[ah.fc > 0]["ex"].mean(), long_n=(ah.fc > 0).sum())
    out["other_horizons"] = pd.DataFrame(hz).T
    return out
