def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].values)
            n = len(c)
            hi60 = c.rolling(60, min_periods=20).max()
            dist = (1 - c / hi60) * 100
            r28 = c.pct_change(28) * 100
            prod = r28 * (1 / (1 + dist)) ** 2
            raw = df["debug_info.components.hp_mom.last_history_value"].values
            f = df["forecast"].values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, h=h, f=f[i], raw=raw[i], prod=prod[i],
                                     r28=r28[i], dist=dist[i], year=year[i],
                                     ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")
    d["sgn"] = np.sign(d["r28"])
    d["prod_c"] = d["prod"].clip(d["prod"].quantile(0.01), d["prod"].quantile(0.99))
    d["r28_c"] = d["r28"].clip(d["r28"].quantile(0.01), d["r28"].quantile(0.99))
    # within-coin rank of prod
    d["prod_rank"] = d.groupby(["coin", "h"])["prod"].rank(pct=True) - 0.5

    def slope(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))

    out = {}
    tab = []
    for h in (10, 20):
        g = d[d.h == h]
        for x in ("f", "raw", "prod", "prod_c", "prod_rank", "r28", "r28_c", "sgn"):
            s = slope(g, x); s["h"] = h; s["x"] = x; tab.append(s)
    out["slopes"] = pd.DataFrame(tab)
    d10 = d[d.h == 10]
    out["corr_f_prod"] = float(d10[["f", "prod"]].corr().iloc[0, 1])
    out["corr_raw_prod"] = float(d10[["raw", "prod"]].corr().iloc[0, 1])
    out["prod_c_by_year"] = d10.groupby("year").apply(lambda g: slope(g, "prod_c"))
    out["prod_c_by_coin"] = d10.groupby("coin").apply(lambda g: slope(g, "prod_c"))
    d10 = d10.copy()
    d10["pq"] = pd.qcut(d10["prod"], 5, labels=False)
    out["ex_by_prod_quint"] = d10.groupby("pq")["ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    return out
