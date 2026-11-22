def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    hourrows = []
    dayrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            mv = v.rolling(720, min_periods=240).mean()
            z = r / sd; rv = v / mv
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            # past 24h realised vol rel to 30d
            vol24 = r.rolling(24).std() / sd
            ret24 = c / c.shift(24) - 1
            ret24z = ret24 / (sd * np.sqrt(24))
            for h in (1, 2, 4, 6, 24):
                idx = np.arange(0, n - h, h)
                f = c.values[idx + h] / c.values[idx] - 1
                d = pd.DataFrame({"coin": coin, "w": w, "h": h, "z": z.values[idx], "rv": rv.values[idx],
                                  "vol24": vol24.values[idx], "ret24z": ret24z.values[idx],
                                  "hour": ts.dt.hour.values[idx], "wd": ts.dt.weekday.values[idx], "f": f})
                rows.append(d)
    A = pd.concat(rows).dropna()
    out = {}
    # drift per coin/h
    drift = A.groupby(["coin", "h"])["f"].transform("mean")
    A["u"] = A["f"] - drift
    A["su"] = np.sign(A["z"]) * A["u"]
    A["zb"] = pd.cut(A["z"].abs(), [0, 1, 2, 3, 5, 100], labels=["<1", "1-2", "2-3", "3-5", ">5"])
    A["rvb"] = pd.cut(A["rv"], [0, 1, 2, 4, 1000], labels=["<1", "1-2", "2-4", ">4"])
    def agg(g, col="su"):
        x = g[col]
        return pd.Series({"n": len(x), "mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    for h in (2, 6, 24):
        S = A[(A.h == h)]
        out[f"signed cont h{h} by |z| x relvol"] = S.groupby(["zb", "rvb"], observed=True).apply(agg).query("n>=30")
    # direction split for large moves
    S = A[(A.h == 6) & (A.z.abs() > 2)].copy()
    S["dir"] = np.where(S.z > 0, "up", "down")
    out["h6 |z|>2 by dir x relvol (signed cont)"] = S.groupby(["coin", "dir", "rvb"], observed=True).apply(agg).query("n>=20")
    # hour of day, h=1 raw return
    H = A[A.h == 1]
    out["h1 by hour (unusual)"] = H.groupby("hour").apply(lambda g: agg(g, "u"))
    out["h1 by hour by coin t"] = H.groupby(["hour", "coin"]).apply(lambda g: agg(g, "u"))["t"].unstack()
    D = A[A.h == 24]
    out["h24 by weekday (unusual)"] = D.groupby(["wd"]).apply(lambda g: agg(g, "u"))
    D = D.copy()
    D["volq"] = D.groupby("coin")["vol24"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["h24 by vol24 quintile (unusual)"] = D.groupby(["coin", "volq"]).apply(lambda g: agg(g, "u"))
    D["rq"] = D.groupby("coin")["ret24z"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["h24 by past-24h return quintile (unusual)"] = D.groupby(["coin", "rq"]).apply(lambda g: agg(g, "u"))
    return out
