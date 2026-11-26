def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    rows = []
    drift = {}
    for H in [7, 14, 21, 42]:
        for coin, ws in bars.items():
            rets = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rets.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(rets) if rets else np.nan
        for coin, ws in bars.items():
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                f = df["forecast"].fillna(0).values
                reg = df["regime"].astype(str).values
                ts = pd.to_datetime(df["timestamp"])
                for i in range(0, len(c) - H, H):
                    if f[i] > 0 and reg[i] == "unknown":
                        r = c[i + H] / c[i] - 1
                        rows.append(dict(H=H, coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                         f=f[i], ex=r - drift[(coin, H)], r=r))
    d = pd.DataFrame(rows)

    def clt(g, x, y=None):
        # mean t clustered by day, or slope t
        if y is None:
            dev = g["ex"] - g["ex"].mean()
            s = dev.groupby(g["day"]).sum()
            se = np.sqrt((s ** 2).sum()) / len(g)
            return g["ex"].mean(), g["ex"].mean() / se if se > 0 else np.nan
        X = g[x] - g[x].mean()
        b = (X * g[y]).sum() / (X ** 2).sum()
        a = g[y].mean() - b * g[x].mean()
        e = g[y] - a - b * g[x]
        s = (X * e).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return b, b / se

    res = []
    for H, g in d.groupby("H"):
        m, mt = clt(g, None)
        b, bt = clt(g, "f", "ex")
        res.append(dict(H=H, n=len(g), days=g["day"].nunique(), mean_ex=m, mean_t=mt, slope=b, slope_t=bt))
    out["by_horizon"] = pd.DataFrame(res)

    g21 = d[d.H == 21].copy()
    g21["q"] = pd.qcut(g21["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["21_by_forecast_quartile"] = g21.groupby("q").agg(n=("ex", "size"), fmean=("f", "mean"), ex=("ex", "mean"), r=("r", "mean"))
    g7 = d[d.H == 7].copy()
    g7["q"] = pd.qcut(g7["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["7_by_forecast_quartile"] = g7.groupby("q").agg(n=("ex", "size"), fmean=("f", "mean"), ex=("ex", "mean"), r=("r", "mean"))
    out["21_by_coin"] = g21.groupby("coin").agg(n=("ex", "size"), ex=("ex", "mean"), corr=("f", lambda s: np.corrcoef(s, g21.loc[s.index, "ex"])[0, 1] if len(s) > 2 else np.nan))
    out["21_by_year"] = g21.groupby("year").agg(n=("ex", "size"), ex=("ex", "mean"), r=("r", "mean"))
    out["21_by_window"] = g21.groupby("w").agg(n=("ex", "size"), ex=("ex", "mean"))
    return out
