def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = {"1d":6, "2d":12, "3d":18, "5d":30}
    rows = []; hr = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); hi = df["high"].astype(float); lo = df["low"].astype(float)
            r6 = c / c.shift(6) - 1
            mabs = r6.abs().rolling(180, min_periods=90).mean()
            z6 = r6 / mabs
            rng = (hi - lo) / c
            rr = rng.rolling(6).mean() / rng.rolling(180, min_periods=90).mean()
            r180 = c / c.shift(180) - 1
            ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year
            n = len(df)
            for hn, h in H.items():
                f = (c.shift(-h) / c - 1).values
                for i in np.arange(0, n - h, h):
                    rows.append((coin, w, int(w[1:]), yr.iat[i], hn, z6.iat[i], rr.iat[i], r180.iat[i], f[i]))
            nr = (c.shift(-1) / c - 1).values
            for i in range(n - 1):
                hr.append((coin, yr.iat[i], ts.iat[i].hour, ts.iat[i].dayofweek, nr[i]))
    D = pd.DataFrame(rows, columns=["coin","w","wn","yr","h","z6","rr","r180","f"])
    D["ex"] = D["f"] - D.groupby(["coin","h"])["f"].transform("mean")
    D = D.dropna()
    D["score"] = (-D["z6"]).clip(lower=0) * D["rr"]
    out = {}
    def st(x):
        return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "n": len(x)})
    # graded: fall x range score buckets
    res = []
    for hn in H:
        s = D[D.h == hn]
        b = pd.cut(s["score"], [-0.01, 0, 0.5, 1, 1.5, 2.5, 100], labels=["0","0-.5",".5-1","1-1.5","1.5-2.5",">2.5"])
        g = s.groupby(b, observed=True)["ex"].apply(st).unstack(); g["h"] = hn
        res.append(g.reset_index())
    out["score buckets"] = pd.concat(res).round(4)
    s = D[(D.h == "3d") & (D.z6 < -1) & (D.rr > 1.3)]
    out["3d fall-wide by coin"] = s.groupby("coin")["ex"].apply(st).unstack().round(4)
    out["3d fall-wide by year"] = s.groupby("yr")["ex"].apply(st).unstack().round(4)
    s["prior"] = np.where(s.r180 > 0, "up30d", "down30d")
    out["3d fall-wide by prior trend"] = s.groupby("prior")["ex"].apply(st).unstack().round(4)
    s2 = D[(D.h == "1d") & (D.z6 < -1) & (D.rr > 1.3)]
    out["1d fall-wide by coin"] = s2.groupby("coin")["ex"].apply(st).unstack().round(4)
    Hr = pd.DataFrame(hr, columns=["coin","yr","hour","wd","r"]).dropna()
    Hr["ex"] = Hr["r"] - Hr.groupby("coin")["r"].transform("mean")
    x = Hr[Hr.hour == 16]
    out["16h bar by coin"] = x.groupby("coin")["ex"].apply(st).unstack().round(5)
    out["16h bar by year"] = x.groupby("yr")["ex"].apply(st).unstack().round(5)
    x = Hr[Hr.hour == 20]
    out["20h bar by year"] = x.groupby("yr")["ex"].apply(st).unstack().round(5)
    x = Hr[Hr.wd == 4]
    out["friday by year"] = x.groupby("yr")["ex"].apply(st).unstack().round(5)
    return out
