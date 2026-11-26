def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:] / c[:-1] - 1)
        mu = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            r = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sd30 = pd.Series(r).rolling(30, min_periods=20).std().values
            sd7 = pd.Series(r).rolling(7, min_periods=5).std().values
            f = b["forecast"].astype(float).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(c)
            for i in range(n):
                if f[i] < 0 and i + 1 < n:
                    rows.append(dict(coin=coin, win=w, day=ts.iloc[i].normalize(), f=f[i],
                                     sd=sd30[i], sdratio=sd7[i] / sd30[i] if sd30[i] > 0 else np.nan,
                                     up=r[i], r1=c[i + 1] / c[i] - 1 - mu,
                                     r3=c[min(i + 3, n - 1)] / c[i] - 1 - mu * (min(i + 3, n - 1) - i)))
    df = pd.DataFrame(rows)
    # coin-relative vol: sd30 against coin's own median sd30 over its case bars
    df["sdrel"] = df["sd"] / df.groupby("coin")["sd"].transform("median")
    def daysum(g, col="r1"):
        s = (-g[col]).dropna().groupby(g["day"]).mean()
        return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std(ddof=1) / np.sqrt(len(s))), "days": len(s), "cases": len(g)})
    out = {}
    for name, col, k in [("sdrel", "sdrel", 3), ("depth_f", "f", 3), ("sdratio", "sdratio", 3), ("up", "up", 3)]:
        d = df.dropna(subset=[col]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), k, labels=[f"{name}_lo", "mid", f"{name}_hi"])
        out[f"daysum_h1_by_{name}"] = d.groupby("q").apply(daysum)
        out[f"daysum_h3_by_{name}"] = d.groupby("q").apply(lambda g: daysum(g, "r3"))
    # cases per day clustering
    cpd = df.groupby("day").size()
    out["cases_per_day"] = pd.Series({"mean": cpd.mean(), "share_days_ge3": (cpd >= 3).mean(), "share_cases_on_ge3_days": cpd[cpd >= 3].sum() / cpd.sum()})
    # day-mean gain by number of coins in the case that day
    df["ncoin"] = df.groupby("day")["coin"].transform("count")
    df["nc"] = pd.cut(df["ncoin"], [0, 1, 3, 20], labels=["1", "2-3", "4+"])
    out["daysum_h1_by_ncoins_same_day"] = df.groupby("nc").apply(daysum)
    return out
