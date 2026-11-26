def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            sdmed = sd.expanding(min_periods=40).median()
            agit = sd > sdmed
            z3 = (c / c.shift(3) - 1) / (sd * np.sqrt(3))
            hi20 = c.rolling(20, min_periods=20).max()
            dfh = c / hi20 - 1
            tr60 = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            f5 = c.shift(-5) / c - 1
            f3 = c.shift(-3) / c - 1
            n = len(b)
            for i in range(0, n, 5):
                rows.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), z=z.iloc[i], z3=z3.iloc[i],
                                 f5=f5.iloc[i], f3=f3.iloc[i], dfh=dfh.iloc[i], tr60=tr60.iloc[i],
                                 agit=("agit" if agit.iloc[i] else "calm") if not np.isnan(sdmed.iloc[i]) else np.nan,
                                 yr=ts.iloc[i].year))
    df = pd.DataFrame(rows)
    for col in ("f5", "f3"):
        dr = df.groupby("coin")[col].mean(); us = df.groupby("coin")["f5"].std()
        df["x" + col[1:]] = df[col] - df["coin"].map(dr)
        df["s" + col[1:]] = df["x" + col[1:]] / df["coin"].map(us)
    def clslope(g, x, y="s5"):
        g = g.dropna(subset=[x, y])
        if len(g) < 20: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, days=np.nan))
        X = np.c_[np.ones(len(g)), g[x].values]; Y = g[y].values
        bet = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ bet
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2))
        for _, idx in g.groupby("day").indices.items():
            s = (X[idx] * e[idx, None]).sum(0); meat += np.outer(s, s)
        G = g["day"].nunique(); k = (G / (G - 1)) * ((len(g) - 1) / (len(g) - 2))
        V = XtXi @ meat @ XtXi * k
        return pd.Series(dict(n=len(g), days=G, slope=bet[1], t=bet[1] / np.sqrt(V[1, 1])))
    out = {}
    out["z slope clustered all"] = clslope(df, "z")
    out["z slope by agitation"] = df.groupby("agit").apply(lambda g: clslope(g, "z"))
    out["z slope by year"] = df.groupby("yr").apply(lambda g: clslope(g, "z"))
    out["z slope by coin"] = df.groupby("coin").apply(lambda g: clslope(g, "z"))
    out["z slope, up days only"] = clslope(df[df.z > 0], "z")
    out["z slope, down days only"] = clslope(df[df.z < 0], "z")
    out["z slope 3d horizon"] = clslope(df, "z", "s3")
    out["z3 slope (3-day move)"] = clslope(df, "z3")
    df["athigh"] = np.where(df.dfh >= -0.0001, "at high", np.where(df.dfh > -0.05, "near", "far"))
    out["z slope by dist high"] = df.groupby("athigh").apply(lambda g: clslope(g, "z"))
    df["zb"] = pd.cut(df["z"], [-99, -1, 0, 1, 2, 99])
    out["x5 by agit x zb"] = df.groupby(["agit", "zb"])["x5"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # dfh slope controlling: s5 on dfh
    out["dfh slope"] = clslope(df, "dfh")
    out["dfh slope by agit"] = df.groupby("agit").apply(lambda g: clslope(g, "dfh"))
    return out
