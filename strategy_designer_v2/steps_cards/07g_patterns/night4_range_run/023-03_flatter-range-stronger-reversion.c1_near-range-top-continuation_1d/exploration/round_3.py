def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows1 = []; rows10 = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=20).std()
            z1 = r1 / vol
            z10 = (c / c.shift(10) - 1) / (vol * np.sqrt(10))
            z10x = (c.shift(1) / c.shift(10) - 1) / (vol * np.sqrt(9))
            f1 = c.shift(-1) / c - 1
            f10 = c.shift(-10) / c - 1
            f10s = c.shift(-10) / c.shift(-1) - 1
            ts = pd.to_datetime(d["timestamp"])
            for i in range(len(d)):
                rows1.append(dict(coin=coin, z1=z1.iloc[i], vol=vol.iloc[i], f=f1.iloc[i], wd=ts.iloc[i].weekday(), year=ts.iloc[i].year))
            for i in range(0, len(d), 10):
                rows10.append(dict(coin=coin, z10=z10.iloc[i], z10x=z10x.iloc[i], z1=z1.iloc[i], f=f10.iloc[i], fs=f10s.iloc[i], year=ts.iloc[i].year))
    out = {}
    g = pd.DataFrame(rows1).dropna(subset=["z1", "f"]).copy()
    g["ex"] = g["f"] - g.groupby("coin")["f"].transform("mean")
    g["exs"] = g["ex"] / g.groupby("coin")["f"].transform("std")
    def tt(a): return pd.Series(dict(n=len(a), mean=a.mean(), t=a.mean() / (a.std() / np.sqrt(len(a)))))
    g["zq"] = pd.qcut(g["z1"], 5, labels=False)
    out["1d: next-day ex by z1 quintile"] = g.groupby("zq")["ex"].apply(tt).unstack()
    def reg(x, col):
        r = stats.linregress(x[col], x["exs"]); return pd.Series(dict(n=len(x), slope=r.slope, t=r.slope / r.stderr))
    out["1d: exs on z1 by year"] = g.groupby("year").apply(lambda x: reg(x, "z1"))
    out["1d: exs on z1 by coin"] = g.groupby("coin").apply(lambda x: reg(x, "z1"))
    g["volq"] = pd.qcut(g.groupby("coin")["vol"].rank(pct=True), 3, labels=["lo", "mid", "hi"])
    out["1d: exs on z1 by vol tercile"] = g.groupby("volq").apply(lambda x: reg(x, "z1"))
    out["weekday next-day ex by year (Thu+Fri minus Mon+Wed)"] = g.groupby("year").apply(lambda x: pd.Series(dict(
        diff=x.loc[x.wd.isin([3, 4]), "ex"].mean() - x.loc[x.wd.isin([0, 2]), "ex"].mean(),
        t=stats.ttest_ind(x.loc[x.wd.isin([3, 4]), "ex"], x.loc[x.wd.isin([0, 2]), "ex"], equal_var=False).statistic)))
    h = pd.DataFrame(rows10).dropna(subset=["z10", "z10x", "z1", "f", "fs"]).copy()
    for col in ["f", "fs"]:
        h[col + "e"] = (h[col] - h.groupby("coin")[col].transform("mean")) / h.groupby("coin")[col].transform("std")
    X = np.column_stack([np.ones(len(h)), h["z10x"], h["z1"]])
    res = {}
    for col in ["fe", "fse"]:
        b, *_ = np.linalg.lstsq(X, h[col].values, rcond=None)
        e = h[col].values - X @ b; s2 = e @ e / (len(h) - 3)
        se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
        res[col + "_coef"] = b; res[col + "_t"] = b / se
    out["10d: ex on past 9d (excl last day) and last-day z"] = pd.DataFrame(res, index=["const", "z9_excl_last", "z1_last"])
    h["zq"] = pd.qcut(h["z10"], 5, labels=False)
    h["exr"] = h["f"] - h.groupby("coin")["f"].transform("mean")
    out["10d: ex by z10 quintile"] = h.groupby("zq")["exr"].apply(tt).unstack()
    return out
