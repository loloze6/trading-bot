def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            r1 = c.pct_change()
            r60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30).std()
            pc = (c - l) / (h - l).replace(0, np.nan)
            rng = (h - l) / c
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for off in range(7):
                for i in range(off, n, 7):
                    rows.append(dict(coin=coin, w=w, off=off, i=i, day=ts.iloc[i].normalize(),
                                     pc=pc.iloc[i], rng=rng.iloc[i], r1=r1.iloc[i], r60=r60.iloc[i],
                                     rngz=rng.iloc[i] / vol30.iloc[i] if vol30.iloc[i] > 0 else np.nan,
                                     yr=ts.iloc[i].year,
                                     f1=c.shift(-1).iloc[i] / c.iloc[i] - 1,
                                     f3=c.shift(-3).iloc[i] / c.iloc[i] - 1,
                                     f7=c.shift(-7).iloc[i] / c.iloc[i] - 1))
    g = pd.DataFrame(rows)
    out = {}
    def prep(s, col):
        base = s[s.off == 0]
        dr = base.groupby("coin")[col].mean(); sd = base.groupby("coin")[col].std()
        s = s.copy(); s["ex"] = s[col] - s["coin"].map(dr); s["z"] = s["ex"] / s["coin"].map(sd)
        return s
    def cl_slope(s, x):
        s = s.dropna(subset=[x, "z"])
        X = s[x] - s[x].mean(); y = s["z"] - s["z"].mean()
        b = (X * y).sum() / (X ** 2).sum()
        e = y - b * X
        sc = (X * e).groupby(s["day"]).sum()
        se = np.sqrt((sc ** 2).sum()) / (X ** 2).sum()
        return b, b / se, len(s), s["day"].nunique()
    def dayt(s):
        s = s.dropna(subset=["z"])
        dsum = s.groupby("day")["z"].sum()
        m = s["z"].mean(); dev = (s["z"] - m).groupby(s["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return m, m / se, len(s), s["day"].nunique()
    res = {}
    for col in ["f1", "f3", "f7"]:
        s = prep(g, col)
        for off in range(7):
            b, t, n, nd = cl_slope(s[s.off == off], "pc")
            res[(col, off)] = dict(slope=b, t=t, n=n, days=nd)
    out["close position slope on z, by horizon and grid offset (day-clustered)"] = pd.DataFrame(res).T
    s7 = prep(g, "f7"); s0 = s7[s7.off == 0].dropna(subset=["pc", "z"])
    rw = {}
    for w, x in s0.groupby("w"):
        b, t, n, nd = cl_slope(x, "pc"); rw[w] = dict(slope=b, t=t, n=n)
    out["pc slope f7 by window (offset 0)"] = pd.DataFrame(rw).T
    rc = {}
    for c_, x in s0.groupby("coin"):
        b, t, n, nd = cl_slope(x, "pc"); rc[c_] = dict(slope=b, t=t, n=n)
    out["pc slope f7 by coin"] = pd.DataFrame(rc).T
    s0 = s0.copy()
    s0["trend"] = np.where(s0.r60 > 0.10, "rising", np.where(s0.r60 < -0.10, "falling", np.where(s0.r60.notna(), "choppy", "na")))
    rt = {}
    for k, x in s0.groupby("trend"):
        b, t, n, nd = cl_slope(x, "pc"); rt[k] = dict(slope=b, t=t, n=n)
    out["pc slope f7 by 60d trend"] = pd.DataFrame(rt).T
    # quintiles, day-clustered t, pooled offsets for f1
    s1 = prep(g, "f1"); s1 = s1[s1.off == 0].dropna(subset=["pc", "z"]).copy()
    s1["b"] = pd.qcut(s1.pc, 5, labels=False)
    q = {}
    for k, x in s1.groupby("b"):
        m, t, n, nd = dayt(x); q[k] = dict(z=m, t=t, n=n, ex=x.ex.mean())
    out["f1 by pc quintile (offset0, day t)"] = pd.DataFrame(q).T
    # range scaled: wide days
    for col in ["f7"]:
        s = prep(g, col); s = s[s.off == 0]
        b, t, n, nd = cl_slope(s, "rngz"); out["rngz slope f7"] = pd.Series(dict(slope=b, t=t, n=n))
        b, t, n, nd = cl_slope(s, "r1"); out["r1 slope f7"] = pd.Series(dict(slope=b, t=t, n=n))
        s = s.dropna(subset=["pc", "rngz", "z"]).copy(); s["pcr"] = (s.pc - 0.5) * s.rngz
        b, t, n, nd = cl_slope(s, "pcr"); out["(pc-0.5)*rangez slope f7"] = pd.Series(dict(slope=b, t=t, n=n))
    # largest book days
    dd = []
    for coin, wins in days.items():
        for w, df in wins.items():
            x = df[["book_return", "coin_return"]].copy(); x["coin"] = coin; dd.append(x)
    d = pd.concat(dd).dropna(); d = d[d.book_return != 0]
    out["book: largest gains/losses share"] = pd.Series(dict(n_active=len(d), top10_sum=d.book_return.nlargest(10).sum(),
        bot10_sum=d.book_return.nsmallest(10).sum(), total=d.book_return.sum(), corr_coin=d.book_return.corr(d.coin_return)))
    return out
