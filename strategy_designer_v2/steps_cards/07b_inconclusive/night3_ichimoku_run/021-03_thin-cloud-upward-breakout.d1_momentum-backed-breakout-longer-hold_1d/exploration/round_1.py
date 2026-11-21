def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drifts = {}
    for H in [10, 20, 40, 60]:
        for coin, ws in bars.items():
            rets = []
            for w, b in ws.items():
                c = b["close"].values
                for i in range(0, len(c) - H, H):
                    rets.append(c[i + H] / c[i] - 1)
            drifts[(coin, H)] = (np.mean(rets), np.std(rets))
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            r60 = pd.Series(c).pct_change(60).values
            r20 = pd.Series(c).pct_change(20).values
            tr = (b["regime"] == "trending").values
            fc = b["forecast"].fillna(0).values
            for H in [10, 20, 40, 60]:
                seen = set()
                for i in np.where(tr)[0]:
                    if i + H >= n:
                        continue
                    cell = i // H
                    if cell in seen:
                        continue
                    seen.add(cell)
                    d, s = drifts[(coin, H)]
                    rows.append(dict(coin=coin, w=w, H=H, i=i, fc=fc[i], r60=r60[i], r20=r20[i],
                                     year=b["timestamp"].iloc[i].year if hasattr(b["timestamp"].iloc[i], "year") else pd.to_datetime(b["timestamp"].iloc[i]).year,
                                     unus=c[i + H] / c[i] - 1 - d, strength=(c[i + H] / c[i] - 1 - d) / s))
    df = pd.DataFrame(rows)
    out = {}
    def slope(x, y):
        m = x.notna() & y.notna()
        if m.sum() < 5: return (np.nan, np.nan, int(m.sum()))
        r = stats.linregress(x[m], y[m])
        return (r.slope, r.slope / r.stderr, int(m.sum()))
    summ = []
    for H, g in df.groupby("H"):
        pos = g[g.fc > 0]
        zero = g[g.fc <= 0]
        s1 = slope(pos.fc, pos.unus)
        s2 = slope(g.r60, g.unus)
        s3 = slope(g.r60.rank(pct=True), g.unus)
        summ.append(dict(H=H, n_all=len(g), mean_all=g.unus.mean(), t_all=stats.ttest_1samp(g.unus, 0).statistic,
                         med_all=g.unus.median(), n_pos=len(pos), mean_pos=pos.unus.mean(), n_zero=len(zero), mean_zero=zero.unus.mean(),
                         slope_fc=s1[0], t_fc=s1[1], slope_r60=s2[0], t_r60=s2[1], t_r60rank=s3[1]))
    out["by_horizon"] = pd.DataFrame(summ)
    g = df[df.H == 40].copy()
    out["by_coin_40"] = g.groupby("coin").agg(n=("unus", "size"), mean=("unus", "mean"), med=("unus", "median"), frac_pos=("unus", lambda x: (x > 0).mean()))
    out["by_year_40"] = g.groupby("year").agg(n=("unus", "size"), mean=("unus", "mean"), med=("unus", "median"), frac_pos=("unus", lambda x: (x > 0).mean()))
    g["r60q"] = pd.qcut(g.r60, 4, labels=False, duplicates="drop")
    out["by_r60_quartile_40"] = g.groupby("r60q").agg(n=("unus", "size"), r60=("r60", "mean"), mean=("unus", "mean"), med=("unus", "median"), frac_pos=("unus", lambda x: (x > 0).mean()))
    p = g[g.fc > 0].copy()
    p["fcq"] = pd.qcut(p.fc, 4, labels=False, duplicates="drop")
    out["by_fc_quartile_40"] = p.groupby("fcq").agg(n=("unus", "size"), fc=("fc", "mean"), mean=("unus", "mean"), med=("unus", "median"), frac_pos=("unus", lambda x: (x > 0).mean()))
    out["unus_dist_40"] = g.unus.describe()
    out["corr_fc_r60_pos"] = float(p[["fc", "r60"]].corr().iloc[0, 1])
    # trimmed mean / without top 5
    s = g.unus.sort_values()
    out["mean40_drop_top5"] = float(s.iloc[:-5].mean())
    out["t40_drop_top5"] = float(stats.ttest_1samp(s.iloc[:-5], 0).statistic)
    return out
