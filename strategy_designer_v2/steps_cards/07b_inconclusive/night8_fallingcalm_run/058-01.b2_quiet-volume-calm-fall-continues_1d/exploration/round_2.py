def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values
            n = len(df)
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    f30 = c[i] / c[i - 30] - 1 if i >= 30 else np.nan
                    rows.append(dict(coin=coin, w=w, h=h, ret=c[i + h] / c[i] - 1,
                                     fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                                     day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year, f30=f30))
    g = pd.DataFrame(rows)
    g["mu"] = g.groupby(["coin", "h"])["ret"].transform("mean")
    g["ex"] = g["ret"] - g["mu"]
    def ct(x, days):
        s = pd.Series(x.values - x.mean(), index=days.values).groupby(level=0).sum()
        k = len(s); se = np.sqrt((s ** 2).sum() * k / (k - 1)) / len(x)
        return x.mean(), x.mean() / se, len(x), k
    out = {}
    res = []
    for h in (5, 10, 20):
        q = g[(g.h == h) & (g.fc < 0)]
        m, t, nn, k = ct((-q.fc / 10) * q.ex, q.day); res.append(("plan_measure", h, m, t, nn, k))
        m, t, nn, k = ct((q.fc / 10) * q.ex, q.day); res.append(("short_gain_measure", h, m, t, nn, k))
        m, t, nn, k = ct(-q.ex, q.day); res.append(("unweighted_short_ex", h, m, t, nn, k))
        tr = g[(g.h == h) & (g.reg == "trending")]
        m, t, nn, k = ct(-tr.ex, tr.day); res.append(("all_trending_short_ex", h, m, t, nn, k))
    out["measures"] = pd.DataFrame(res, columns=["measure", "h", "mean", "t_day", "n", "days"])
    sp = []
    for h in (5, 10, 20):
        q = g[(g.h == h) & (g.fc < 0)]
        r, p = stats.spearmanr(q.fc, q.ex); sp.append((h, "forecast_vs_ex_quiet", r, p, len(q)))
        tr = g[(g.h == h) & (g.reg == "trending")]
        r, p = stats.spearmanr(tr.fc, tr.ex); sp.append((h, "forecast_vs_ex_trending", r, p, len(tr)))
    out["spearman"] = pd.DataFrame(sp, columns=["h", "pair", "rho", "p", "n"])
    q5 = g[(g.h == 5) & (g.fc < 0)]
    out["quiet5_by_window"] = q5.groupby("w")["ex"].agg(["count", "mean"])
    return out
