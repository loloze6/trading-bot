def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 2, 2)
            g.extend(list(c[idx + 2] / c[idx] - 1))
        drift[coin] = np.mean(g)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values
            n = len(c)
            r14 = pd.Series(c).pct_change(14).values
            r2 = np.full(n, np.nan)
            r2[:-2] = c[2:] / c[:-2] - 1
            fc = df.get("debug_info.components.near_high.post_pipeline_value")
            lh = df.get("debug_info.components.near_high.last_history_value")
            for i in range(n):
                if np.isnan(r2[i]) or np.isnan(r14[i]):
                    continue
                rows.append(dict(coin=coin, window=w, year=ts[i].year, wd=ts[i].weekday(),
                                 day=ts[i].normalize(), r14=r14[i], ex=r2[i] - drift[coin],
                                 trend=df["regime"].iloc[i] == "trending",
                                 f=fc.iloc[i] if fc is not None else np.nan,
                                 raw=lh.iloc[i] if lh is not None else np.nan))
    d = pd.DataFrame(rows)

    def ct(x, days):
        x = np.asarray(x); m = x.mean()
        s = pd.Series(x - m).groupby(np.asarray(days)).sum().values
        G = len(s)
        se = np.sqrt(G / (G - 1) * (s ** 2).sum()) / len(x)
        return m, m / se, len(x), G

    def summ(sub):
        if len(sub) < 10: return pd.Series(dict(mean=np.nan, t=np.nan, n=len(sub), days=0))
        m, t, n, G = ct(sub["ex"], sub["day"])
        return pd.Series(dict(mean=m, t=t, n=n, days=G))

    cases = d[(d.wd == 4) & d.trend & d.f.notna()].copy()
    cases["fq"] = pd.qcut(cases.f, 5, labels=False)
    cases["rq"] = pd.qcut(cases.r14, 5, labels=False)
    out = {}
    out["cases by forecast quintile"] = cases.groupby("fq").apply(summ).join(cases.groupby("fq").f.mean())
    out["cases by 14d return quintile"] = cases.groupby("rq").apply(summ).join(cases.groupby("rq").r14.mean())
    out["cases by coin"] = cases.groupby("coin").apply(summ)
    out["cases by year"] = cases.groupby("year").apply(summ)
    fr = d[d.wd == 4].copy()
    fr["up"] = fr.r14 > 0
    out["all Fridays by rise"] = fr.groupby("up").apply(summ)
    fr["rq"] = pd.qcut(fr.r14, 10, labels=False)
    out["all Fridays by 14d return decile"] = fr.groupby("rq").apply(summ).join(fr.groupby("rq").r14.mean())
    d["up"] = d.r14 > 0
    out["2-bar excess by weekday and rise"] = d.groupby(["wd", "up"]).apply(summ)
    sl = stats.linregress(cases.r14, cases.ex)
    out["slope ex on r14 in cases"] = pd.Series(dict(slope=sl.slope, t=sl.slope / sl.stderr))
    sl2 = stats.linregress(fr.r14, fr.ex)
    out["slope ex on r14 all Fridays"] = pd.Series(dict(slope=sl2.slope, t=sl2.slope / sl2.stderr))
    out["corr f r14 in cases"] = float(np.corrcoef(cases.f, cases.r14)[0, 1])
    return out
