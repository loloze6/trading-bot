def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    rows = []
    # pooled per-coin 30d swing distribution (approximate agitation proxy)
    sdall = {}
    for coin in bars:
        v = []
        for w, df in bars[coin].items():
            c = df["close"].astype(float).reset_index(drop=True)
            v.append(c.pct_change().rolling(30, min_periods=30).std())
        sdall[coin] = pd.concat(v).dropna()
    for coin in bars:
        med = sdall[coin].median()
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=30).std()
            r5s = (c / c.shift(5) - 1) / sd
            r60 = c / c.shift(60) - 1
            lo20 = c.rolling(20, min_periods=20).min(); hi20 = c.rolling(20, min_periods=20).max()
            pos = (c - lo20) / (hi20 - lo20)
            ts = pd.to_datetime(df["timestamp"])
            for h in (5, 10):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(df), h)
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "r5s": r5s.values[idx],
                    "r1z": (r1 / sd).values[idx], "r60": r60.values[idx], "agit": (sd > med).astype(float).where(sd.notna()).values[idx],
                    "pos": pos.values[idx], "fwd": fwd.values[idx], "day": ts.dt.floor("D").values[idx],
                    "yr": ts.dt.year.values[idx]}))
    g = pd.concat(rows).dropna(subset=["fwd"])
    g = g.join(g.groupby(["coin", "h"])["fwd"].mean().rename("drift"), on=["coin", "h"])
    g["unu"] = g["fwd"] - g["drift"]
    def ct(x):
        d = x.groupby("day")["unu"].sum(); n = len(x); D = len(d)
        m = x["unu"].mean()
        dev = x.assign(e=x["unu"] - m).groupby("day")["e"].sum()
        se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / n
        return pd.Series({"n": n, "days": D, "mean%": 100 * m, "t_day": m / se if se > 0 else np.nan})
    s = g.dropna(subset=["r5s"]).copy()
    s["r5bin"] = pd.cut(s["r5s"], [-99, -4, -3, -2, -1, 1, 2, 3, 4, 99])
    out["r5s bins, day-clustered"] = s.groupby(["h", "r5bin"], observed=True).apply(ct)
    s10 = s[s.h == 10]
    deep = s10[s10.r5s <= -3]
    out["deep fall h10 by window"] = deep.groupby("w").apply(ct)
    out["deep fall h10 by coin"] = deep.groupby("coin").apply(ct)
    out["deep fall h10 by agit"] = deep.groupby("agit").apply(ct)
    s10 = s10.assign(trend=pd.cut(s10["r60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"]))
    out["r5s<=-2 h10 by trend x agit"] = s10[s10.r5s <= -2].groupby(["trend", "agit"], observed=True).apply(ct)
    out["r5s>=2 h10 by trend x agit"] = s10[s10.r5s >= 2].groupby(["trend", "agit"], observed=True).apply(ct)
    # graded continuation: sign(r5s)*unu by |r5s| bins
    s["cont"] = np.sign(s["r5s"]) * s["unu"]
    s["ab"] = pd.cut(s["r5s"].abs(), [0, 1, 2, 3, 99])
    out["continuation |r5s|, h10 by agit"] = s[s.h == 10].assign(unu=lambda d: d["cont"]).groupby(["agit", "ab"], observed=True).apply(ct)
    # position in 20-day range
    p = g[g.h == 10].dropna(subset=["pos"]).copy()
    p["pb"] = pd.cut(p["pos"], [-0.01, 0.1, 0.33, 0.67, 0.9, 1.01])
    out["20d range position h10 by agit"] = p.groupby(["agit", "pb"], observed=True).apply(ct)
    return out
