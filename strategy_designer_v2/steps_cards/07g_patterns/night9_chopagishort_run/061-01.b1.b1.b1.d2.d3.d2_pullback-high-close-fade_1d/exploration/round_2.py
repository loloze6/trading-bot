def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            n = len(b)
            if n < 10: continue
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            rng = np.where(h - l > 0, h - l, np.nan)
            cl = (c - l) / rng
            r1 = pd.Series(c).pct_change().values
            mabs = pd.Series(np.abs(r1)).rolling(20, min_periods=10).mean().values
            r3p = (pd.Series(c).shift(1) / pd.Series(c).shift(4) - 1).values
            tr60 = (pd.Series(c) / pd.Series(c).shift(60) - 1).values
            for i in range(0, n - 5, 5):
                ts = pd.Timestamp(b["timestamp"].iloc[i])
                rows.append(dict(coin=coin, w=w, i=i, day=ts.normalize(), cl=cl[i], r1=r1[i],
                                 z=r1[i] / mabs[i] if mabs[i] > 0 else np.nan,
                                 prior3=r3p[i], tr60=tr60[i],
                                 inprof=b["regime"].iloc[i] != "chop",
                                 fwd=c[i + 5] / c[i] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")

    def ct(s, x):
        # day-clustered t
        g = s.groupby("day")[x].sum()
        dev = s[x] - s[x].mean()
        gd = dev.groupby(s["day"]).sum()
        G = len(gd)
        se = np.sqrt((gd ** 2).sum() * G / (G - 1)) / len(s) if G > 1 else np.nan
        return pd.Series(dict(mean=s[x].mean(), n=len(s), days=G, t=s[x].mean() / se if se else np.nan))

    ip = d[d.inprof]
    out["inprof all: excess by closeloc thirds (clustered)"] = ip.groupby(pd.cut(ip.cl, [-0.01, 0.33, 0.67, 1.01])).apply(lambda s: ct(s, "ex")).round(4)
    hc = ip[ip.cl >= 0.67]
    out["inprof cl>=0.67 by up/down day"] = hc.groupby(hc.r1 > 0).apply(lambda s: ct(s, "ex")).round(4)
    out["inprof cl>=0.67 by z sign/size"] = hc.groupby(pd.cut(hc.z, [-99, 0, 0.7, 99])).apply(lambda s: ct(s, "ex")).round(4)
    out["inprof cl>=0.67 by coin"] = hc.groupby("coin")["ex"].agg(["mean", "count"]).round(4)
    out["inprof corr cl vs ex (spearman)"] = float(ip[["cl", "ex"]].corr(method="spearman").iloc[0, 1])
    # out of profile: large up days continuation by 60-day trend (where computable)
    op = d[~d.inprof & d.tr60.notna()].copy()
    op["trend"] = np.where(op.tr60 > 0.10, "rising", np.where(op.tr60 < -0.10, "falling", "choppy"))
    big = op[op.z > 1]
    out["outprof z>1 by trend (clustered)"] = big.groupby("trend").apply(lambda s: ct(s, "ex")).round(4)
    out["outprof z by bucket, choppy only"] = op[op.trend == "choppy"].groupby(pd.cut(op[op.trend == "choppy"].z, [-99, -1, -0.3, 0.3, 1, 2, 99])).apply(lambda s: ct(s, "ex")).round(4)
    out["outprof z bucket, all trends"] = op.groupby(pd.cut(op.z, [-99, -1, -0.3, 0.3, 1, 2, 99])).apply(lambda s: ct(s, "ex")).round(4)
    out["all z>2 by coin"] = d[d.z > 2].groupby("coin")["ex"].agg(["mean", "count"]).round(4)
    return out
