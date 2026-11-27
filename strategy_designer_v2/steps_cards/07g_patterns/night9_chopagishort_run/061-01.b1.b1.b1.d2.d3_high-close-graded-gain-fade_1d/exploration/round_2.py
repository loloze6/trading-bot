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
            r60 = np.full(n, np.nan)
            if n > 60:
                r60[60:] = c[60:] / c[:-60] - 1
            sd30 = pd.Series(r1).rolling(30, min_periods=20).std().values
            sdw = np.nanmedian(sd30) if np.isfinite(sd30).any() else np.nan
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:n - H] = c[H:] / c[:n - H] - 1
            reg = b["regime"].astype(str).values
            for i in range(0, n, H):
                rows.append(dict(coin=coin, w=w, ts=b["timestamp"].iloc[i], loc=loc[i], r1=r1[i],
                                 sc=r1[i] / ar[i] if ar[i] > 0 else np.nan, r60=r60[i],
                                 agi=(sd30[i] > sdw) if np.isfinite(sd30[i]) else np.nan,
                                 fwd=fwd[i], inprof=(reg[i] != "chop")))
    d = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = d.groupby("coin")["fwd"].mean()
    d["u"] = d["fwd"] - d["coin"].map(drift)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["year"] = pd.to_datetime(d["ts"]).dt.year

    def st(g):
        if len(g) < 5:
            return pd.Series(dict(n=len(g), days=np.nan, mean=np.nan, t=np.nan))
        m = g["u"].mean()
        dev = (g["u"] - m).groupby(g["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / len(g)
        return pd.Series(dict(n=len(g), days=G, mean=m, t=m / se if se > 0 else np.nan))

    d["trend"] = pd.cut(d["r60"], [-99, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    d["agit"] = d["agi"].map({True: "agit(win)", False: "calm(win)"})
    hc_up = d[(d["loc"] >= 0.8) & (d["r1"] > 0)]
    hc_dn = d[(d["loc"] >= 0.8) & (d["r1"] <= 0)]
    big_up = d[d["sc"] > 1.5]
    lowmid_dn = d[(d["loc"] < 0.4) & (d["r1"] < 0)]
    out = {}
    out["high close up day, by trend x window-agitation"] = hc_up.groupby(["trend", "agit"], observed=True).apply(st)
    out["high close down day, by trend"] = hc_dn.groupby("trend", observed=True).apply(st)
    out["high close down day, all, by year"] = hc_dn.groupby("year").apply(st)
    out["big up day (>1.5 usual), by trend"] = big_up.groupby("trend", observed=True).apply(st)
    out["big up day, by year"] = big_up.groupby("year").apply(st)
    out["low close down day, by trend"] = lowmid_dn.groupby("trend", observed=True).apply(st)
    out["all, by trend x agitation"] = d.groupby(["trend", "agit"], observed=True).apply(st)
    return out
