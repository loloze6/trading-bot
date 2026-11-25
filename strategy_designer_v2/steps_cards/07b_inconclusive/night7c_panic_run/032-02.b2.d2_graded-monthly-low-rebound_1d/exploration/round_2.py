def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    coinmean = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values.astype(float)
            allr.append(c[1:] / c[:-1] - 1)
        coinmean[coin] = np.concatenate(allr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            hi = df["high"].values.astype(float); lo = df["low"].values.astype(float)
            n = len(df)
            rng = (hi - lo) / c
            mr30 = pd.Series(rng).rolling(30).mean().values
            r1 = np.full(n, np.nan); r1[1:] = c[1:] / c[:-1] - 1
            r5 = np.full(n, np.nan); r5[5:] = c[5:] / c[:-5] - 1
            ret30 = np.full(n, np.nan); ret30[30:] = c[30:] / c[:-30] - 1
            ts = pd.to_datetime(df["timestamp"])
            f = df["forecast"].values
            dep = df.get("debug_info.components.depth.last_history_value")
            rw = df.get("debug_info.components.range_width.last_history_value")
            for t in range(n):
                if not (f[t] > 0):
                    continue
                rows.append(dict(coin=coin, win=w, year=ts[t].year, day=ts[t].normalize(), f=f[t],
                                 depth=float(dep.iloc[t]) if dep is not None else np.nan,
                                 rw=float(rw.iloc[t]) if rw is not None else np.nan,
                                 r1d=r1[t], r5d=r5[t], ret30=ret30[t],
                                 rngday=rng[t] / mr30[t] if mr30[t] > 0 else np.nan,
                                 x1=(c[t + 1] / c[t] - 1 - coinmean[coin]) if t + 1 < n else np.nan))
    d = pd.DataFrame(rows).dropna(subset=["x1"])

    def pooled(g):
        g = g.dropna(subset=["x1"])
        m = g.x1.mean()
        s = (g.x1 - m).groupby(g.day).sum()
        D = len(s)
        if D < 3:
            return pd.Series(dict(n=len(g), days=D, mean=m, t=np.nan))
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / len(g)
        return pd.Series(dict(n=len(g), days=D, mean=m, t=m / se))

    out = {}
    out["all_pooled"] = pooled(d).to_frame().T
    for col in ["rw", "depth", "r1d", "r5d", "rngday", "ret30"]:
        q = pd.qcut(d[col].rank(method="first"), 3, labels=False)
        out[f"tercile_{col}"] = d.groupby(q).apply(pooled)
        out[f"tercile_{col}_range"] = d.groupby(q)[col].agg(["min", "max"])
    out["year_pooled"] = d.groupby("year").apply(pooled)
    out["corr_with_x1"] = d[["f", "rw", "depth", "r1d", "r5d", "rngday", "ret30"]].corrwith(d.x1, method="spearman").to_frame("spearman")
    d["rwhi"] = d.rw > d.rw.median(); d["dephi"] = d.depth > d.depth.median()
    out["depth_x_rw"] = d.groupby(["dephi", "rwhi"]).apply(pooled)
    out["year_rw_mean"] = d.groupby("year")[["rw", "depth", "r1d"]].mean()
    return out
