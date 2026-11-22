def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # coin drift per horizon on non-overlapping grid across all windows
        drift = {}
        for h in (1, 3, 5, 10):
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.append(c[idx + h] / c[idx] - 1)
            v = np.concatenate(vals) if vals else np.array([])
            drift[h] = (np.nanmean(v), np.nanstd(v))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            z = r1 / sd20
            r30 = c / c.shift(30) - 1
            n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            for h in (1, 3, 5, 10):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n - h, h)
                sub = pd.DataFrame({
                    "coin": coin, "win": w, "h": h, "z": z.values[idx],
                    "fwd": fwd.values[idx], "un": fwd.values[idx] - drift[h][0],
                    "str": (fwd.values[idx] - drift[h][0]) / drift[h][1],
                    "regime": df["regime"].values[idx], "r30": r30.values[idx],
                    "sd20": sd20.values[idx], "wd": ts.dt.weekday.values[idx],
                    "year": ts.dt.year.values[idx]})
                rows.append(sub)
    A = pd.concat(rows).dropna(subset=["z", "fwd"])
    A["fall"] = np.where(A["regime"] == "mean_reversion", "fall90", "notfall")
    A["zb"] = pd.cut(A["z"], [-99, -2, -1, 0, 1, 2, 99])
    def agg(g):
        return pd.Series({"n": len(g), "mean_un": g["un"].mean(),
                          "t": g["un"].mean() / (g["un"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "strength": g["str"].mean()})
    out = {}
    for h in (1, 5, 10):
        out[f"h{h} by z bucket x regime"] = A[A.h == h].groupby(["fall", "zb"]).apply(agg)
    B = A[A.h == 5].copy()
    # vol level relative to coin median
    B["volrel"] = B["sd20"] / B.groupby("coin")["sd20"].transform("median")
    B["vb"] = pd.qcut(B["volrel"], 3, labels=["lowvol", "midvol", "highvol"])
    out["h5 by vol level x regime"] = B.groupby(["fall", "vb"]).apply(agg)
    B["r30b"] = pd.qcut(B["r30"], 5)
    out["h5 by 30d return quintile"] = B.groupby("r30b").apply(agg)
    out["h1 by weekday"] = A[A.h == 1].groupby("wd").apply(agg)
    out["h5 by year x regime"] = B.groupby(["year", "fall"]).apply(agg)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            d = df.copy(); d["coin"] = coin; d["win"] = w
            D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book daily by weekday"] = D.groupby("wd")["book_return"].agg(["count", "mean", "std"])
    out["book by coin"] = D.groupby("coin")["book_return"].agg(["count", "mean"])
    return out
