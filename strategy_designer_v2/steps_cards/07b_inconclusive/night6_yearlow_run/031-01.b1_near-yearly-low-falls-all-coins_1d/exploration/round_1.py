def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            prox = df.get("debug_info.components.low_prox.last_history_value")
            r20b = pd.Series(c).pct_change(20).values
            for h in (5, 10, 20, 40):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, ts=df["timestamp"].iloc[i],
                                     fc=df["forecast"].iloc[i],
                                     prox=(prox.iloc[i] if prox is not None else np.nan),
                                     past20=r20b[i],
                                     ret=c[i + h] / c[i] - 1))
    g = pd.DataFrame(rows)
    g["year"] = pd.to_datetime(g["ts"]).dt.year
    g["ex"] = g["ret"] - g.groupby(["coin", "h"])["ret"].transform("mean")
    g["dnum"] = pd.to_datetime(g["ts"]).astype("int64") // 86400_000_000_000

    def ct(d, x="fc", y="ex"):
        d = d.dropna(subset=[x, y])
        if len(d) < 20 or d[x].std() == 0:
            return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan))
        X = np.column_stack([np.ones(len(d)), d[x].values]); Y = d[y].values
        b = np.linalg.lstsq(X, Y, rcond=None)[0]; e = Y - X @ b
        XtXi = np.linalg.inv(X.T @ X)
        meat = np.zeros((2, 2)); G = 0
        for _, idx in d.groupby("dnum").indices.items():
            s = X[idx].T @ e[idx]; meat += np.outer(s, s); G += 1
        V = XtXi @ meat @ XtXi * G / (G - 1)
        return pd.Series(dict(n=len(d), slope=b[1], t=b[1] / np.sqrt(V[1, 1])))

    out = {}
    out["by horizon (slope of excess on forecast; + = idea)"] = g.groupby("h").apply(ct)
    g20 = g[g.h == 20].copy()
    out["h20 by coin"] = g20.groupby("coin").apply(ct)
    out["h20 by year"] = g20.groupby("year").apply(ct)
    g20["pq"] = pd.qcut(g20["prox"].rank(method="first"), 5, labels=False)
    out["h20 by raw proximity quintile: mean excess, mean ret, n"] = g20.groupby("pq").agg(
        prox=("prox", "mean"), ex=("ex", "mean"), ret=("ret", "mean"), n=("ex", "size"),
        tex=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    g20["mom"] = np.where(g20["past20"] < 0, "past20 down", "past20 up")
    out["h20 by past 20d sign"] = g20.groupby("mom").apply(ct)
    out["h20 by past20 sign x prox quintile mean ex"] = g20.groupby(["mom", "pq"])["ex"].agg(["mean", "size"])
    # proximity slope directly (raw), per horizon
    out["raw prox slope by horizon"] = g.groupby("h").apply(lambda d: ct(d, x="prox"))
    return out
