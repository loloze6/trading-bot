def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    coinmean = {}
    for coin, ws in bars.items():
        allr = []
        for w, df in ws.items():
            c = df["close"].astype(float).reset_index(drop=True)
            allr.append(c.pct_change().dropna())
        coinmean[coin] = pd.concat(allr).mean()
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            rise = r / sd
            p5 = (c.shift(1) / c.shift(6) - 1) / (sd.shift(1) * np.sqrt(5))
            f1 = c.shift(-1) / c - 1
            f2 = c.shift(-2) / c - 1
            f3 = c.shift(-3) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "fc": df["forecast"].astype(float),
                              "rise": rise, "p5": p5, "f1": f1, "f2": f2, "f3": f3,
                              "rawrise": r, "day": ts.dt.floor("D"), "year": ts.dt.year})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["m"] = D["coin"].map(coinmean)
    A = D[(D.fc < 0)].dropna(subset=["f1"]).copy()
    A["x1"] = -(A.f1 - A.m)   # short-signed excess
    A["x2"] = -(A.f2 - 2 * A.m)
    A["x3"] = -(A.f3 - 3 * A.m)
    out = {}
    def tday(s, day):
        g = s.groupby(day).sum()
        n = s.notna().sum()
        return s.mean() / (g.std() * np.sqrt(len(g)) / n) if len(g) > 2 else np.nan
    out["n_active"] = len(A)
    summ = {}
    for h in ["x1", "x2", "x3"]:
        s = A[h].dropna()
        summ[h] = {"mean": s.mean(), "t_day": tday(s, A.loc[s.index, "day"]), "n": len(s)}
    out["by_horizon"] = pd.DataFrame(summ).T
    # buckets by rise and by p5
    for var in ["rise", "p5", "fc"]:
        q = pd.qcut(A[var], 4, labels=False, duplicates="drop")
        g = A.groupby(q).agg(mean_var=(var, "mean"), x1=("x1", "mean"), x2=("x2", "mean"), x3=("x3", "mean"), n=("x1", "size"))
        out["quart_" + var] = g
    # correlations
    cr = {}
    for var in ["rise", "p5", "fc"]:
        for h in ["x1", "x2", "x3"]:
            s = A[[var, h]].dropna()
            cr[var + "_" + h] = stats.spearmanr(s[var], s[h])[0]
    out["spearman"] = pd.Series(cr)
    out["by_coin"] = A.groupby("coin").agg(x1=("x1", "mean"), x3=("x3", "mean"), n=("x1", "size"))
    out["by_year"] = A.groupby("year").agg(x1=("x1", "mean"), x3=("x3", "mean"), n=("x1", "size"))
    out["by_window"] = A.groupby("w").agg(x1=("x1", "mean"), n=("x1", "size"))
    return out
