def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; h = b["high"]; l = b["low"]
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            b["fromlow"] = (c - l.rolling(20).min()) / l.rolling(20).min() / sd
            b["fromlow10"] = (c - l.rolling(10).min()) / l.rolling(10).min() / sd
            b["z5"] = (c / c.shift(5) - 1) / (sd * np.sqrt(5))
            b["z10"] = (c / c.shift(10) - 1) / (sd * np.sqrt(10))
            for k in [1, 3, 5]:
                b["f%d" % k] = c.shift(-k) / c - 1
            b["fc"] = (b["regime"] == "unknown")
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    res = []
    for k in [1, 3, 5]:
        g = d[d["pos"] % k == 0].dropna(subset=["f%d" % k])
        m = g.groupby("coin")["f%d" % k].mean()
        for off in range(k):
            s = d[(d["pos"] % k == off) & d["fc"]].dropna(subset=["f%d" % k]).copy()
            s["ex"] = s["f%d" % k] - s["coin"].map(m)
            for col in ["fromlow", "fromlow10", "z5", "z10"]:
                ss = s.dropna(subset=[col])
                sl = stats.linregress(ss[col], ss["ex"])
                # top third minus bottom third
                lo = ss[col].quantile(1/3); hi = ss[col].quantile(2/3)
                diff = ss[ss[col] >= hi]["ex"].mean() - ss[ss[col] <= lo]["ex"].mean()
                res.append(dict(h=k, off=off, col=col, n=len(ss), slope_t=sl.slope / sl.stderr,
                                top_minus_bottom=diff))
    out["slopes by horizon and grid offset"] = pd.DataFrame(res)
    # robustness of fromlow at h=3 offset 0: by coin, by year, outside profile
    g = d[d["pos"] % 3 == 0].dropna(subset=["f3"])
    m = g.groupby("coin")["f3"].mean()
    g = g.assign(ex=g["f3"] - g["coin"].map(m)).dropna(subset=["fromlow"])
    def st(x):
        if len(x) < 8: return pd.Series(dict(n=len(x), slope_t=np.nan, corr=np.nan))
        sl = stats.linregress(x["fromlow"], x["ex"])
        return pd.Series(dict(n=len(x), slope_t=sl.slope / sl.stderr, corr=sl.rvalue))
    out["fromlow h3 in profile by coin"] = g[g["fc"]].groupby("coin").apply(st)
    out["fromlow h3 in profile by year"] = g[g["fc"]].groupby("yr").apply(st)
    out["fromlow h3 outside profile"] = st(g[~g["fc"]])
    # day-clustered t: long share-weighted: sign by fromlow standardized
    s = g[g["fc"]].copy()
    s["zf"] = (s["fromlow"] - s["fromlow"].mean()) / s["fromlow"].std()
    s["prod"] = s["zf"] * s["ex"]
    pd_ = s.groupby("day")["prod"].sum()
    out["fromlow h3 day-clustered t of zf*ex"] = float(pd_.mean() / (pd_.std() / np.sqrt(len(pd_))))
    out["n days"] = len(pd_)
    out["corr fromlow vs z5 in profile"] = float(s[["fromlow", "z5"]].corr().iloc[0, 1])
    return out
