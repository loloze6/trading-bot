def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        rets_all = []
        for w, df in wins.items():
            c = df["close"].values
            rets_all.append(c[1:] / c[:-1] - 1)
        drift = np.nanmean(np.concatenate(rets_all)) if rets_all else 0
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            n = len(c)
            r1 = np.full(n, np.nan); r1[1:] = c[1:] / c[:-1] - 1
            for i in range(n):
                if not (f[i] < 0):
                    continue
                # run length before up day i
                k = 0; j = i - 1
                while j >= 1 and r1[j] < 0:
                    k += 1; j -= 1
                d = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "run": k, "bounce": r1[i], "drift": drift}
                for h in (1, 2, 3, 5):
                    if i + h < n:
                        d[f"x{h}"] = -(c[i + h] / c[i] - 1 - h * drift)
                    else:
                        d[f"x{h}"] = np.nan
                rows.append(d)
    t = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for h in (1, 2, 3, 5):
            x = g[f"x{h}"].dropna()
            out[f"m{h}"] = x.mean()
            out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)
    t["runb"] = t["run"].clip(upper=5)
    t["bq"] = pd.qcut(t["bounce"], 4, labels=["b1", "b2", "b3", "b4"])
    return {
        "all": summ(t),
        "by run": t.groupby("runb").apply(summ),
        "by coin": t.groupby("coin").apply(summ),
        "by year": t.groupby("year").apply(summ),
        "by window": t.groupby("win").apply(summ),
        "by bounce quartile": t.groupby("bq").apply(summ),
        "bounce mean by q": t.groupby("bq")["bounce"].mean(),
    }
