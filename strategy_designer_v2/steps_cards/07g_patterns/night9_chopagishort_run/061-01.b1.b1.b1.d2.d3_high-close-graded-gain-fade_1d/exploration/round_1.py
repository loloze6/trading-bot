def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            h = b["high"].values.astype(float)
            l = b["low"].values.astype(float)
            n = len(b)
            rng = np.where(h > l, h - l, np.nan)
            loc = (c - l) / rng
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            ar = pd.Series(np.abs(r1)).rolling(20, min_periods=10).mean().shift(1).values
            r3 = np.r_[[np.nan] * 3, c[3:] / c[:-3] - 1]
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = c[H:] / c[:n - H] - 1
            reg = b["regime"].astype(str).values
            for i in range(0, n, H):
                rows.append(dict(
                    coin=coin, w=w, ts=b["timestamp"].iloc[i],
                    loc=loc[i], r1=r1[i],
                    sc=r1[i] / ar[i] if ar[i] > 0 else np.nan,
                    r3=r3[i] / ar[i] if ar[i] > 0 else np.nan,
                    fwd=fwd[i], inprof=(reg[i] != "chop"), regime=reg[i]))
    d = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].mean()
    d["u"] = d["fwd"] - d["coin"].map(drift)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["year"] = pd.to_datetime(d["ts"]).dt.year
    d["wd"] = pd.to_datetime(d["ts"]).dt.weekday

    def st(g):
        if len(g) < 5:
            return pd.Series(dict(n=len(g), days=np.nan, mean=np.nan, t=np.nan))
        m = g["u"].mean()
        dev = (g["u"] - m).groupby(g["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / len(g)
        return pd.Series(dict(n=len(g), days=G, mean=m, t=m / se if se > 0 else np.nan))

    d["locq"] = pd.cut(d["loc"], [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01],
                       labels=["0-.2", ".2-.4", ".4-.6", ".6-.8", ".8-1"])
    d["up"] = np.where(d["r1"] > 0, "up", "down")
    d["scq"] = pd.cut(d["sc"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    d["r3q"] = pd.cut(d["r3"], [-99, -3, -1, 1, 3, 99])
    ip = d[d.inprof]
    op = d[~d.inprof]
    out = {}
    out["regime counts"] = d["regime"].value_counts()
    out["in profile, by close location and day sign"] = ip.groupby(["locq", "up"], observed=True).apply(st)
    out["out of profile, by close location and day sign"] = op.groupby(["locq", "up"], observed=True).apply(st)
    out["in profile, by day return in usual moves"] = ip.groupby("scq", observed=True).apply(st)
    out["out of profile, by day return in usual moves"] = op.groupby("scq", observed=True).apply(st)
    out["in profile, by 3-day return in usual moves"] = ip.groupby("r3q", observed=True).apply(st)
    out["out of profile, by 3-day return in usual moves"] = op.groupby("r3q", observed=True).apply(st)
    out["in profile, by weekday"] = ip.groupby("wd").apply(st)
    out["in profile, by year"] = ip.groupby("year").apply(st)
    out["in profile, by coin"] = ip.groupby("coin").apply(st)
    return out
