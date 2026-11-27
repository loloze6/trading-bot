def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    H = [1, 3, 5]
    drift = {}
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs)
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            depth = (c / c.rolling(30, min_periods=30).max() - 1) * 100
            uplow30 = (c / c.rolling(30, min_periods=30).min() - 1) * 100
            uplow10 = (c / c.rolling(10, min_periods=10).min() - 1) * 100
            r60 = (c / c.shift(60) - 1) * 100
            fc = (df["regime"] == "unknown")
            ts = pd.to_datetime(df["timestamp"])
            for h in H:
                for i in np.arange(0, len(c) - h, h):
                    if not fc.iloc[i]: continue
                    rows.append(dict(coin=coin, w=w, h=h, depth=depth.iloc[i], ul30=uplow30.iloc[i],
                                     ul10=uplow10.iloc[i], r60=r60.iloc[i],
                                     ex=c.iloc[i + h] / c.iloc[i] - 1 - drift[(coin, h)],
                                     tot=c.iloc[i + h] / c.iloc[i] - 1,
                                     day=ts.iloc[i].floor("D"), wn=int(w[1:])))
    R = pd.DataFrame(rows)
    def ct(sub):
        n = len(sub); m = sub["ex"].mean()
        dev = (sub["ex"] - m).groupby(sub["day"]).sum()
        se = np.sqrt((dev**2).sum()) / n
        return m, m / se if se > 0 else np.nan, n, sub["day"].nunique()
    def slope(sub, col):
        sub = sub.dropna(subset=[col])
        x = sub[col].values; y = sub["ex"].values
        if len(x) < 10: return np.nan, np.nan, len(x)
        xm = x - x.mean(); b = (xm * (y - y.mean())).sum() / (xm**2).sum()
        e = y - y.mean() - b * xm
        s = pd.Series(xm * e).groupby(sub["day"].values).sum()
        se = np.sqrt((s**2).sum()) / (xm**2).sum()
        return b, b / se, len(x)
    t1 = []
    for h in H:
        sub = R[R.h == h]
        for col in ["depth", "ul30", "ul10", "r60"]:
            b, t, n = slope(sub, col)
            t1.append(dict(h=h, x=col, slope=b, t=t, n=n))
    out["slopes in falling calm (ex return on x)"] = pd.DataFrame(t1)
    t2 = []
    for h in [3, 5]:
        sub = R[R.h == h].dropna(subset=["ul30"]).copy()
        sub["q"] = pd.qcut(sub["ul30"], 4, labels=False, duplicates="drop")
        for q, g in sub.groupby("q"):
            m, t, n, d = ct(g)
            t2.append(dict(h=h, q=q, ul30_mean=g.ul30.mean(), n=n, mean_ex=m, t=t, mean_tot=g.tot.mean()))
    out["rise above 30d low quartiles"] = pd.DataFrame(t2)
    t3 = []
    for h in [3, 5]:
        sub = R[R.h == h].dropna(subset=["depth"]).copy()
        sub["half"] = np.where(sub.wn <= 9, "w1-9", "w10-18")
        sub["shallow"] = sub.depth > sub.depth.quantile(0.75)
        for (hf, sh), g in sub.groupby(["half", "shallow"]):
            m, t, n, d = ct(g)
            t3.append(dict(h=h, half=hf, shallow_q=sh, n=n, mean_ex=m, t=t))
        for (cn, sh), g in sub.groupby(["coin", "shallow"]):
            m, t, n, d = ct(g)
            t3.append(dict(h=h, half=cn, shallow_q=sh, n=n, mean_ex=m, t=t))
        b, t, n = slope(sub[sub.depth > sub.depth.median()], "depth")
        t3.append(dict(h=h, half="slope in shallow half", shallow_q=None, n=n, mean_ex=b, t=t))
    out["shallow quartile by half/coin"] = pd.DataFrame(t3)
    return out
