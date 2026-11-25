def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            hi = df["high"].astype(float).rolling(20, min_periods=20).max()
            lo = df["low"].astype(float).rolling(20, min_periods=20).min()
            pos = 2 * (c - lo) / (hi - lo) - 1
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            agit = sd30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            ret60 = c / c.shift(60) - 1
            for h in (1, 3, 5, 10, 20):
                fr = c.shift(-h) / c - 1
                idx = np.arange(0, len(df), h)
                for i in idx:
                    if pd.isna(fr.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, win=w, h=h, i=i, fr=fr.iloc[i], fc=df["forecast"].iloc[i],
                                     reg=df["regime"].iloc[i], pos=pos.iloc[i], agit=agit.iloc[i],
                                     ret60=ret60.iloc[i], day=str(df["timestamp"].iloc[i])[:10],
                                     year=str(df["timestamp"].iloc[i])[:4]))
    R = pd.DataFrame(rows)
    R["ex"] = R["fr"] - R.groupby(["coin", "h"])["fr"].transform("mean")
    out = {}

    def slope_t(d, x="fc"):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 20:
            return (np.nan, np.nan, len(d))
        X = d[x].values; y = d["ex"].values
        Xc = X - X.mean()
        b = (Xc * (y - y.mean())).sum() / (Xc ** 2).sum()
        e = y - y.mean() - b * Xc
        g = pd.Series(Xc * e).groupby(d["day"].values).sum()
        se = np.sqrt((g ** 2).sum()) / (Xc ** 2).sum()
        return (b, b / se, len(d))

    act = R[(R.fc != 0) & (R.reg == "unknown")]
    hz = []
    for h in (1, 3, 5, 10, 20):
        d = act[act.h == h]
        b, t, n = slope_t(d)
        bp, tp, _ = slope_t(d, "pos")
        hz.append(dict(h=h, n=n, slope_fc=b, t_fc=t, slope_pos=bp, t_pos=tp))
    out["by_horizon"] = pd.DataFrame(hz)

    d5 = act[act.h == 5].copy()
    # side
    side = []
    for s, dd in [("long", d5[d5.fc > 0]), ("short", d5[d5.fc < 0])]:
        b, t, n = slope_t(dd)
        side.append(dict(side=s, n=n, mean_ex_signed=(np.sign(dd.fc) * dd.ex).mean(),
                         t_mean=stats.ttest_1samp(np.sign(dd.fc) * dd.ex, 0).statistic, slope=b, t=t))
    out["by_side_h5"] = pd.DataFrame(side)
    # quintiles of raw position
    d5["pq"] = pd.qcut(d5["pos"], 5, labels=False, duplicates="drop")
    out["pos_quintile_h5"] = d5.groupby("pq").agg(n=("ex", "size"), pos=("pos", "mean"), ex=("ex", "mean"),
                                                   sd=("ex", "std"))
    # agitation
    d5["agit_c"] = np.where(d5.agit.isna(), "na", np.where(d5.agit > 0.5, "agitated", "calm"))
    ag = []
    for k, dd in d5.groupby("agit_c"):
        b, t, n = slope_t(dd)
        ag.append(dict(agit=k, n=n, slope=b, t=t))
    out["by_agitation_h5"] = pd.DataFrame(ag)
    # windows / years / coins
    for key in ("year", "coin"):
        L = []
        for k, dd in d5.groupby(key):
            b, t, n = slope_t(dd)
            L.append({key: k, "n": n, "slope": b, "t": t})
        out["by_" + key + "_h5"] = pd.DataFrame(L)
    # extreme forecasts
    ex = []
    for lab, dd in [("abs_fc>10", d5[d5.fc.abs() > 10]), ("abs_fc<=10", d5[d5.fc.abs() <= 10]),
                    ("abs_pos>0.6", d5[d5.pos.abs() > 0.6]), ("abs_pos<=0.6", d5[d5.pos.abs() <= 0.6])]:
        ex.append(dict(group=lab, n=len(dd), signed_ex=(np.sign(dd.fc) * dd.ex).mean(),
                       t=stats.ttest_1samp(np.sign(dd.fc) * dd.ex, 0).statistic))
    out["strength_h5"] = pd.DataFrame(ex)
    # Outside profile comparison: rising/falling, using ret60
    allp = R[(R.h == 5)].dropna(subset=["pos", "ret60"]).copy()
    allp["trend"] = np.where(allp.ret60 > .1, "rising", np.where(allp.ret60 < -.1, "falling", "choppy"))
    tr = []
    for k, dd in allp.groupby("trend"):
        b, t, n = slope_t(dd, "pos")
        tr.append(dict(trend=k, n=n, slope_pos=b, t=t))
    out["by_trend_pos_h5_allbars"] = pd.DataFrame(tr)
    return out
