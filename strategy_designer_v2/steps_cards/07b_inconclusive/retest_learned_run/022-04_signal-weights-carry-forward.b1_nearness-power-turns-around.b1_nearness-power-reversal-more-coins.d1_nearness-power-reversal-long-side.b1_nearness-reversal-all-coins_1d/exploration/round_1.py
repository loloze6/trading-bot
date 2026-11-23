def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H_list = [5, 10, 20]
    drift = {}
    for coin, wins in bars.items():
        for H in H_list:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rr += list(c[idx + H] / c[idx] - 1)
            drift[(coin, H)] = (np.mean(rr), np.std(rr, ddof=1))
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for H in H_list:
                idx = np.arange(0, n - H, H)
                for i in idx:
                    # past 30-day return within window
                    past = c[i] / c[i - 30] - 1 if i >= 30 else np.nan
                    rows.append(dict(coin=coin, w=w, H=H, year=ts.iloc[i].year, f=f[i],
                                     ex=c[i + H] / c[i] - 1 - drift[(coin, H)][0],
                                     tot=c[i + H] / c[i] - 1, sd=drift[(coin, H)][1], past=past))
    d = pd.DataFrame(rows)
    out = {}
    def wt(g):
        g = g[g.f > 0]
        if len(g) < 5: return pd.Series(dict(n=len(g)))
        x = g.ex.values; ww = g.f.values
        m = np.sum(ww * x) / ww.sum()
        se = np.sqrt(np.sum(ww**2 * (x - m)**2) / ww.sum()**2 * len(x) / (len(x) - 1))
        return pd.Series(dict(n=len(g), wmean=m, wt=m / se, umean=x.mean(),
                              ut=x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))))
    d5 = d[d.H == 5]
    out["by_horizon"] = d.groupby("H").apply(wt)
    pos = d5[d5.f > 0].copy()
    pos["fq"] = pd.qcut(pos.f, 5, labels=False, duplicates="drop")
    out["by_forecast_quintile"] = pos.groupby("fq").apply(lambda g: pd.Series(dict(
        n=len(g), fmean=g.f.mean(), ex=g.ex.mean(), t=g.ex.mean() / (g.ex.std(ddof=1) / np.sqrt(len(g))))))
    out["zero_vs_pos_5"] = d5.assign(pos=d5.f > 0).groupby("pos").ex.agg(["count", "mean"])
    out["by_coin"] = d5.groupby("coin").apply(wt)
    out["by_year"] = d5.groupby("year").apply(wt)
    d5p = d5.dropna(subset=["past"]).copy()
    d5p["past_up"] = d5p.past > 0
    out["by_past30_sign"] = d5p.groupby("past_up").apply(wt)
    out["by_forecast_quintile_H10"] = (lambda p: p.assign(fq=pd.qcut(p.f, 5, labels=False, duplicates="drop")).groupby("fq").ex.agg(["count", "mean"]))(d[(d.H == 10) & (d.f > 0)])
    # weight concentration
    p = pos.sort_values("f", ascending=False)
    out["share_weight_top10pct"] = float(p.f.iloc[:len(p)//10].sum() / p.f.sum())
    return out
