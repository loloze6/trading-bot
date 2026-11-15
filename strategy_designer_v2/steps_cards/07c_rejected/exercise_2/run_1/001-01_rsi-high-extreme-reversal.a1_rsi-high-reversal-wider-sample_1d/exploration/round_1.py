def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    def rsi(c, n=14):
        d = c.diff()
        up = d.clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
        dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
        return 100 - 100/(1+up/dn)
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].reset_index(drop=True)
            r = rsi(c)
            fc = df["forecast"].reset_index(drop=True)
            yr = pd.to_datetime(df["timestamp"]).dt.year.reset_index(drop=True)
            ret20 = c / c.shift(20) - 1
            for h in [1, 3, 5, 10, 20]:
                idx = np.arange(0, len(c) - h, h)
                fr = (c.shift(-h) / c - 1).iloc[idx]
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "rsi": r.iloc[idx].values,
                                          "fc": fc.iloc[idx].values, "fr": fr.values,
                                          "yr": yr.iloc[idx].values, "r20": ret20.iloc[idx].values}))
    D = pd.concat(rows)
    D["ex"] = D["fr"] - D.groupby(["coin", "h"])["fr"].transform("mean")
    D = D.dropna(subset=["rsi", "ex"])
    D["b"] = pd.cut(D["rsi"], [0, 30, 40, 50, 60, 70, 80, 100])
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["by_h_bucket"] = D.groupby(["h", "b"])["ex"].apply(tt).unstack()
    D5 = D[D.h == 5]
    out["h5_coin_bucket_mean"] = D5.groupby(["coin", "b"])["ex"].mean().unstack()
    ext = D5[D5.fc <= -5]
    out["ext_by_coin"] = ext.groupby("coin")["ex"].apply(tt).unstack()
    out["ext_by_year"] = ext.groupby("yr")["ex"].apply(tt).unstack()
    cor = []
    for h in [1, 3, 5, 10, 20]:
        s = D[D.h == h]
        for coin, g in s.groupby("coin"):
            rho, p = stats.spearmanr(g["rsi"], g["ex"])
            cor.append({"h": h, "coin": coin, "rho": rho, "n": len(g)})
    out["spearman_rsi_ex"] = pd.DataFrame(cor).pivot(index="coin", columns="h", values="rho")
    out["h5_year_bucket_mean"] = D5.groupby(["yr", "b"])["ex"].mean().unstack()
    return out
