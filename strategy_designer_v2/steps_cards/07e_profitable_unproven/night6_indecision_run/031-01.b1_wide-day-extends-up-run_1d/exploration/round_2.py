def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            lr = np.log(cl).diff()
            vol20 = lr.rolling(20).std()
            r5 = cl / cl.shift(5) - 1
            r5z = np.log(cl / cl.shift(5)) / (vol20 * np.sqrt(5))
            r20 = cl / cl.shift(20) - 1
            rr = (b["high"] - b["low"]) / (b["high"] - b["low"]).rolling(20).mean()
            ts = pd.to_datetime(b["timestamp"])
            for h in [3]:
                fwd = cl.shift(-h) / cl - 1
                idx = np.arange(0, len(b), h)
                recs.append(pd.DataFrame({"coin": c, "w": w, "day": ts.iloc[idx].dt.floor("D").values,
                    "fwd": fwd.iloc[idx].values, "r5": r5.iloc[idx].values, "r5z": r5z.iloc[idx].values,
                    "r20": r20.iloc[idx].values, "rr": rr.iloc[idx].values,
                    "up": (b["regime"].iloc[idx] == "trending").values}))
    R = pd.concat(recs).dropna(subset=["fwd", "r5z", "rr"])
    R["drift"] = R.groupby("coin")["fwd"].transform("mean")
    R["ex"] = R["fwd"] - R["drift"]
    R["year"] = pd.to_datetime(R["day"]).dt.year
    def dayt(df, col="ex"):
        g = df.groupby("day")[col].sum(); n = len(df)
        m = df[col].mean()
        se = np.sqrt((g - g.mean()*0 - df.groupby("day")[col].count()*m).pow(2).sum()) / n
        return pd.Series({"mean ex %": 100*m, "t day": m/se if se > 0 else np.nan, "n": n, "days": g.size})
    def slope_t(df, x):
        d = df.dropna(subset=[x]); X = d[x] - d[x].mean(); y = d["ex"]
        b = (X*y).sum()/(X*X).sum(); e = y - y.mean() - b*X
        g = (X*e).groupby(d["day"]).sum()
        se = np.sqrt((g**2).sum())/(X*X).sum()
        return pd.Series({"slope": b, "t day": b/se, "n": len(d)})
    out["slope on r5z, all bars"] = slope_t(R, "r5z")
    out["slope on r5z, up-run only"] = slope_t(R[R.up], "r5z")
    out["slope on rr, up-run only"] = slope_t(R[R.up], "rr")
    R["zq"] = pd.qcut(R["r5z"], 5, labels=False)
    out["h3 by vol-scaled 5d return quintile (day t)"] = R.groupby("zq").apply(dayt)
    out["slope r5z by coin"] = R.groupby("coin").apply(lambda d: slope_t(d, "r5z"))
    out["slope r5z by year"] = R.groupby("year").apply(lambda d: slope_t(d, "r5z"))
    R["trend20"] = np.where(R["r20"] > 0, "20d up", "20d down")
    out["slope r5z by 20d trend"] = R.groupby("trend20").apply(lambda d: slope_t(d, "r5z"))
    # book day concentration
    rows = []
    for c in days:
        for w, d in days[c].items():
            rows.append(d.assign(coin=c, window=w))
    D = pd.concat(rows)
    bk = D.groupby(["window", "day"])["book_return"].mean().dropna().sort_values(ascending=False)
    out["book days concentration"] = pd.Series({"sum all": bk.sum(), "sum top 1%": bk.head(int(len(bk)*0.01)).sum(),
        "sum top 5%": bk.head(int(len(bk)*0.05)).sum(), "sum without top 1%": bk.iloc[int(len(bk)*0.01):].sum()})
    return out
