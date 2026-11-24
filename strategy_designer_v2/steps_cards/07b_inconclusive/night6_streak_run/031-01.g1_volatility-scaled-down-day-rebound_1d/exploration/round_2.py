def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(60, min_periods=20).std()
            z = (r1 / vol).values
            r30 = pd.Series(c).pct_change(30).values
            f = df["forecast"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"])
            day = ts.dt.floor("D").astype("int64").values
            for h in (1, 2, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append((coin, w, h, f[i], z[i], r30[i], day[i], c[i + h] / c[i] - 1))
    D = pd.DataFrame(rows, columns=["coin", "w", "h", "f", "z", "r30", "day", "ret"])
    g = D.groupby(["coin", "h"])["ret"]
    D["u"] = (D["ret"] - g.transform("mean")) / g.transform("std")

    def cl(d):
        d = d.dropna(subset=["f", "u"])
        if len(d) < 30 or d["f"].std() == 0:
            return pd.Series({"n": len(d), "slope": np.nan, "t_cl": np.nan, "days": np.nan})
        x = d["f"].values; y = d["u"].values
        X = np.column_stack([np.ones(len(x)), x])
        XtX = np.linalg.inv(X.T @ X)
        b = XtX @ X.T @ y
        e = y - X @ b
        S = pd.DataFrame(X * e[:, None]).groupby(d["day"].values).sum().values
        G = S.shape[0]; N = len(x)
        V = XtX @ (S.T @ S) @ XtX * (G / (G - 1)) * ((N - 1) / (N - 2))
        return pd.Series({"n": N, "slope": b[1], "t_cl": b[1] / np.sqrt(V[1, 1]), "days": G})

    out = {}
    out["clustered slope by horizon"] = D.groupby("h").apply(cl)
    out["clustered slope by horizon, z>-3 (no extremes)"] = D[~(D.z < -3)].groupby("h").apply(cl)
    d3 = D[D.h == 3].copy()
    d3["trend"] = np.where(d3["r30"] > 0, "up30", "down30")
    out["h3 clustered by trend"] = d3.groupby("trend").apply(cl)
    d1 = D[D.h == 1].copy()
    out["h1 clustered by coin"] = d1.groupby("coin").apply(cl)
    d1["zb"] = pd.cut(d1["z"], [-20, -3, -2, -1, 0, 1, 2, 3, 20])
    out["h1 u by raw z"] = d1.groupby("zb")["u"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["h3 extreme falls z<-3 per coin"] = d3[d3.z < -3].groupby("coin")["u"].agg(["count", "mean"])
    return out
