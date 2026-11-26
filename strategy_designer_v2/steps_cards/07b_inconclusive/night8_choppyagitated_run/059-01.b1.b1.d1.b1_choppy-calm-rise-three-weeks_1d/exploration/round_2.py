def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    rows = []
    drift = {}
    sd = {}
    for H in [7, 10, 14, 21]:
        for coin, ws in bars.items():
            rets = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rets.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(rets) if rets else np.nan
            sd[(coin, H)] = np.std(rets, ddof=1) if len(rets) > 2 else np.nan
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
                                         f=f[i], ex=r - drift[(coin, H)], r=r, st=(r - drift[(coin, H)]) / sd[(coin, H)]))
    d = pd.DataFrame(rows)

    def mt(g, col="ex"):
        dev = g[col] - g[col].mean()
        s = dev.groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / len(g)
        return g[col].mean() / se if se > 0 else np.nan

    def st(g, x="f", y="ex"):
        X = g[x] - g[x].mean()
        b = (X * g[y]).sum() / (X ** 2).sum()
        a = g[y].mean() - b * g[x].mean()
        e = g[y] - a - b * g[x]
        s = (X * e).groupby(g["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (X ** 2).sum()
        return b, b / se

    res = []
    for H, g in d.groupby("H"):
        b, bt = st(g)
        top = g[g.f >= g.f.median()]
        res.append(dict(H=H, n=len(g), days=g.day.nunique(), mean_ex=g.ex.mean(), mean_t=mt(g),
                        slope=b, slope_t=bt, strength=g.st.mean(),
                        top_half_ex=top.ex.mean(), top_half_t=mt(top), bottom_half_ex=g[g.f < g.f.median()].ex.mean()))
    out["by_horizon"] = pd.DataFrame(res)

    for H in [7, 14]:
        g = d[d.H == H].copy()
        r2 = []
        for y, gy in g.groupby("year"):
            if len(gy) >= 5 and gy.f.std() > 0:
                b, bt = st(gy)
                r2.append(dict(year=y, n=len(gy), ex=gy.ex.mean(), slope=b, slope_t=bt))
        out[f"{H}_by_year"] = pd.DataFrame(r2)
        g["q"] = pd.qcut(g["f"].rank(method="first"), 3, labels=["low", "mid", "high"])
        out[f"{H}_by_forecast_tercile"] = g.groupby("q").agg(n=("ex", "size"), fmean=("f", "mean"), ex=("ex", "mean"), r=("r", "mean"))
        core = g[g.coin.isin(["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"])]
        b, bt = st(core)
        out[f"{H}_core_coins"] = pd.DataFrame([dict(n=len(core), ex=core.ex.mean(), slope=b, slope_t=bt)])
    return out
