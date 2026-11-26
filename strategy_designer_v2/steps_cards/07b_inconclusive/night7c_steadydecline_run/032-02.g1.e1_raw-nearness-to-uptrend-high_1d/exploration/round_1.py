def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            hi28 = pd.Series(c).rolling(28, min_periods=28).max().values
            ret28 = np.full(n, np.nan); ret28[28:] = c[28:] / c[:-28] - 1
            ret28_real = ret28.copy()
            trend = np.where(np.isnan(ret28), (df["regime"] == "trending").values, ret28 > 0)
            D = (1 - c / hi28) * 100
            # fallback D from recorded proximity
            prox = df.get("debug_info.components.high_prox.last_history_value")
            if prox is not None:
                p = prox.values.astype(float)
                Drec = np.where((p > 0) & (p <= 1), (1 / p - 1), np.nan)
                D = np.where(np.isnan(D), Drec, D)
            fc = df["forecast"].values.astype(float)
            vol20 = pd.Series(c).pct_change().rolling(20).std().values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (3, 5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=year[i], trend=bool(trend[i]),
                                     fc=fc[i], D=D[i], ret28=ret28_real[i], vol=vol20[i],
                                     fwd=c[i + h] / c[i] - 1))
    R = pd.DataFrame(rows)
    R["ex"] = R["fwd"] - R.groupby(["coin", "h"])["fwd"].transform("mean")
    R["prox"] = 1 / (1 + R["D"])

    def slope_t(d, x, y="ex"):
        d = d[[x, y]].dropna()
        if len(d) < 10 or d[x].std() == 0:
            return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        r = stats.linregress(d[x], d[y])
        return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope / r.stderr})

    out = {}
    T = R[(R.trend) & (R.fc > 0)]
    hs = {}
    for h in (3, 5, 10, 20):
        d = T[T.h == h]
        hs[f"h{h}_fc"] = slope_t(d, "fc")
        hs[f"h{h}_prox"] = slope_t(d, "prox")
        hs[f"h{h}_negD"] = slope_t(d.assign(nD=-d.D), "nD")
    out["by horizon, trending fc>0"] = pd.DataFrame(hs).T
    T5 = T[T.h == 5]
    out["h5 by coin (fc)"] = T5.groupby("coin").apply(lambda d: slope_t(d, "fc"))
    out["h5 by year (fc)"] = T5.groupby("year").apply(lambda d: slope_t(d, "fc"))
    T5q = T5.copy(); T5q["q"] = pd.qcut(T5q.fc, 5, labels=False, duplicates="drop")
    out["h5 fc quintile"] = T5q.groupby("q").agg(n=("ex", "size"), fc=("fc", "mean"), D=("D", "mean"), ex=("ex", "mean"), fwd=("fwd", "mean"))
    T5d = T5.copy(); T5d["qD"] = pd.qcut(T5d.D, 5, labels=False, duplicates="drop")
    out["h5 raw D quintile"] = T5d.groupby("qD").agg(n=("ex", "size"), D=("D", "mean"), ex=("ex", "mean"))
    T10 = T[T.h == 10].copy(); T10["qD"] = pd.qcut(T10.D, 5, labels=False, duplicates="drop")
    out["h10 raw D quintile"] = T10.groupby("qD").agg(n=("ex", "size"), D=("D", "mean"), ex=("ex", "mean"))
    # all bars (not just trending) raw D
    A5 = R[R.h == 5].copy()
    A5["trend"] = A5.trend.astype(str)
    out["h5 all bars by trend, -D slope"] = A5.groupby("trend").apply(lambda d: slope_t(d.assign(nD=-d.D), "nD"))
    # by vol regime within trending
    T5v = T5.copy(); T5v["vq"] = pd.qcut(T5v.vol, 3, labels=False, duplicates="drop")
    out["h5 by vol tercile (fc)"] = T5v.groupby("vq").apply(lambda d: slope_t(d, "fc"))
    T5r = T5.copy(); T5r["rq"] = pd.qcut(T5r.ret28, 3, labels=False, duplicates="drop")
    out["h5 by ret28 tercile (fc)"] = T5r.groupby("rq").apply(lambda d: slope_t(d, "fc"))
    return out
