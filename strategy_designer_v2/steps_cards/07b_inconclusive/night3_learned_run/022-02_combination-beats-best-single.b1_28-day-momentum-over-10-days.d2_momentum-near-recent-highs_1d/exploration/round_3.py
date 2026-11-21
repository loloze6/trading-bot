def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].values)
            n = len(c)
            hi60 = c.rolling(60, min_periods=20).max()
            dist = (1 - c / hi60) * 100
            r28 = c.pct_change(28) * 100
            prod = r28 * (1 / (1 + dist)) ** 2
            raw = df["debug_info.components.hp_mom.last_history_value"].values
            f = df["forecast"].values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            h = 10
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, f=f[i], raw=raw[i], prod=prod[i], r28=r28[i],
                                 dist=dist[i], year=year[i], pos=i, ret=c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby("coin")["ret"].transform("mean")
    d["early"] = d["prod"].isna()

    def slope(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))

    out = {}
    tab = []
    for sub, g in (("late", d[~d.early]), ("early", d[d.early]), ("all", d)):
        for x in ("f", "raw", "r28"):
            s = slope(g, x); s["sub"] = sub; s["x"] = x; tab.append(s)
    out["slopes_by_subset"] = pd.DataFrame(tab)
    late = d[~d.early].copy()
    out["corr_f_raw_late"] = float(late[["f", "raw"]].corr().iloc[0, 1])
    late["rq"] = pd.qcut(late["raw"], 5, labels=False, duplicates="drop")
    out["ex_by_raw_quint_late"] = late.groupby("rq")["ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    late["fq"] = pd.qcut(late["f"], 5, labels=False, duplicates="drop")
    out["ex_by_f_quint_late"] = late.groupby("fq")["ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # nearness split: r28 slope near vs far from high
    late["near"] = late["dist"] <= late["dist"].median()
    out["r28_near_far"] = late.groupby("near").apply(lambda g: slope(g, "r28"))
    # residual raw after r28: does proximity add?
    g = late.dropna(subset=["raw", "r28", "ex"])
    X = np.column_stack([np.ones(len(g)), g["r28"], g["raw"]])
    b, *_ = np.linalg.lstsq(X, g["ex"].values, rcond=None)
    res = g["ex"].values - X @ b
    s2 = res @ res / (len(g) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["joint_r28_raw_t"] = pd.Series({"t_r28": b[1] / se[1], "t_raw": b[2] / se[2], "n": len(g)})
    late["half"] = np.where(late["year"] <= 2021, "y2018_21", "y2022_25")
    out["raw_by_half"] = late.groupby("half").apply(lambda g: slope(g, "raw"))
    return out
