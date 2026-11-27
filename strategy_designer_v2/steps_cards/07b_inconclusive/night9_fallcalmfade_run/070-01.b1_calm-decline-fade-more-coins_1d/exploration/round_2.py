def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        rets_all = []
        for w, df in wins.items():
            c = df["close"].values
            rets_all.append(c[1:] / c[:-1] - 1)
        drift = np.nanmean(np.concatenate(rets_all))
        sd1 = np.nanstd(np.concatenate(rets_all), ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            n = len(c)
            r1 = np.full(n, np.nan); r1[1:] = c[1:] / c[:-1] - 1
            for i in range(n):
                if not (f[i] < 0) or i + 1 >= n:
                    continue
                k = 0; j = i - 1
                while j >= 1 and r1[j] < 0:
                    k += 1; j -= 1
                runret = c[i - 1] / c[i - 1 - k] - 1 if k > 0 and i - 1 - k >= 0 else np.nan
                ret20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                rows.append({"coin": coin, "win": w, "day": pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                             "year": pd.Timestamp(df["timestamp"].iloc[i]).year, "run": k,
                             "runret": runret, "ret20": ret20,
                             "x1": -(c[i + 1] / c[i] - 1 - drift),
                             "x1n": -(c[i + 1] / c[i] - 1 - drift) / sd1})
    t = pd.DataFrame(rows)
    def dayt(g, col="x1"):
        s = g.groupby("day")[col].sum()
        cnt = g.groupby("day")[col].count()
        m = s.sum() / cnt.sum()
        dev = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / cnt.sum()
        return pd.Series({"mean": m, "t_day": m / se if se > 0 else np.nan, "n": len(g), "days": g["day"].nunique()})
    t["runb"] = pd.cut(t["run"], [-1, 1, 2, 3, 4, 30], labels=["<=1", "2", "3", "4", "5+"])
    t["long"] = np.where(t["run"] >= 3, "3+", "1-2")
    t["rrq"] = pd.qcut(t["runret"], 4, labels=["deep", "q2", "q3", "shallow"])
    out = {
        "all, day t": dayt(t),
        "all, strength": dayt(t, "x1n"),
        "by run, day t": t.groupby("runb").apply(dayt),
        "by year x long": t.groupby(["year", "long"]).apply(dayt),
        "by run-depth quartile": t.groupby("rrq").apply(dayt),
        "runret mean by q": t.groupby("rrq")["runret"].mean(),
        "corr run vs x1": t[["run", "x1"]].corr().iloc[0, 1],
        "corr runret vs x1": t[["runret", "x1"]].dropna().corr().iloc[0, 1],
        "run>=3 by coin": t[t.run >= 3].groupby("coin").apply(dayt),
    }
    return out
