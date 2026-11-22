def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 18, 18)
            rs.extend(c[idx + 18] / c[idx] - 1)
        m18 = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            rng = (df["high"] - df["low"]) / c
            ratio = rng.rolling(6).mean() / rng.rolling(180, min_periods=30).mean()
            r6 = c / c.shift(6) - 1
            fallz = r6 / r6.abs().rolling(180, min_periods=30).mean()
            r30 = c / c.shift(180) - 1
            r30z = r30 / (c / c.shift(180) - 1).abs().rolling(180, min_periods=30).mean()
            f = df["forecast"].fillna(0).values
            n = len(df)
            for start in range(0, n, 18):
                end = min(start + 18, n)
                sel = np.where(f[start:end] >= 2)[0]
                if len(sel) == 0:
                    continue
                t = start + sel[0]
                if t + 18 >= n:
                    continue
                rows.append(dict(coin=coin, year=pd.Timestamp(df["timestamp"].iloc[t]).year,
                                 ratio=ratio.iloc[t], fallz=fallz.iloc[t], r30=r30.iloc[t],
                                 x18=c.iloc[t + 18] / c.iloc[t] - 1 - m18))
    d = pd.DataFrame(rows).dropna()

    def summ(g):
        v = g["x18"]
        return pd.Series({"n": len(v), "mean": v.mean(),
                          "t": v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan})
    out = {}
    d["r30_q"] = pd.qcut(d["r30"], 4, labels=False)
    out["by_r30_q"] = d.groupby("r30_q").apply(summ).join(d.groupby("r30_q")["r30"].median())
    d["up"] = d["r30"] > 0
    d["ratio_hi"] = d["ratio"] > d["ratio"].median()
    out["by_up_ratio_hi"] = d.groupby(["up", "ratio_hi"]).apply(summ)
    d["fall_deep"] = d["fallz"] < d["fallz"].median()
    out["by_up_fall_deep"] = d.groupby(["up", "fall_deep"]).apply(summ)
    # joint regression, standardised regressors
    X = d[["ratio", "fallz", "r30"]]
    X = (X - X.mean()) / X.std()
    X = np.column_stack([np.ones(len(X)), X.values])
    y = d["x18"].values
    b, res, rk, sv = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    s2 = e @ e / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["ols_x18"] = pd.DataFrame({"coef": b, "t": b / se}, index=["const", "ratio", "fallz", "r30"])
    out["ols_ratio_only"] = pd.Series(dict(zip(["slope", "t"], [stats.linregress(d["ratio"], d["x18"]).slope,
                                       stats.linregress(d["ratio"], d["x18"]).slope / stats.linregress(d["ratio"], d["x18"]).stderr])))
    out["by_coin_up"] = d.groupby(["coin", "up"]).apply(summ)
    return out
