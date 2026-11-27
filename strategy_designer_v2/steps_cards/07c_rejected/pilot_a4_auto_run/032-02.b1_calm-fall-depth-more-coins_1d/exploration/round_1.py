def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    # drift per coin per horizon over all windows (non-overlapping grid)
    H = [1, 3, 5, 10]
    drift = {}
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            depth = (c / c.rolling(30, min_periods=30).max() - 1) * 100
            ret5 = (c / c.shift(5) - 1) * 100
            fc = (df["regime"] == "unknown")
            day = pd.to_datetime(df["timestamp"]).dt.floor("D")
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                for i in idx:
                    rows.append(dict(coin=coin, w=w, h=h, fc=bool(fc.iloc[i]),
                                     depth=depth.iloc[i], r5=ret5.iloc[i],
                                     ex=c.iloc[i + h] / c.iloc[i] - 1 - drift[(coin, h)],
                                     tot=c.iloc[i + h] / c.iloc[i] - 1,
                                     day=day.iloc[i], yr=yr.iloc[i]))
    R = pd.DataFrame(rows).dropna(subset=["depth"])
    def clust_t(sub):
        g = sub.groupby("day")["ex"].sum()
        n = len(sub)
        m = sub["ex"].mean()
        se = np.sqrt((g - g.groupby(level=0).size()*0).pow(2).sum() - 0) if False else None
        dev = (sub["ex"] - m).groupby(sub["day"]).sum()
        se = np.sqrt((dev**2).sum()) / n
        return m, m / se if se > 0 else np.nan, n, sub["day"].nunique()
    def slope(sub):
        x = sub["depth"].values; y = sub["ex"].values
        if len(x) < 10: return np.nan, np.nan
        xm = x - x.mean(); b = (xm * (y - y.mean())).sum() / (xm**2).sum()
        e = y - y.mean() - b * xm
        s = pd.Series(xm * e).groupby(sub["day"].values).sum()
        se = np.sqrt((s**2).sum()) / (xm**2).sum()
        return b, b / se
    t1 = []
    for h in H:
        for fcv in [True, False]:
            sub = R[(R.h == h) & (R.fc == fcv)]
            m, t, n, d = clust_t(sub)
            b, bt = slope(sub)
            t1.append(dict(h=h, falling_calm=fcv, n=n, days=d, mean_ex_long=m, t_long=t,
                           mean_tot=sub["tot"].mean(), slope_ex_per_depthpct=b, slope_t=bt))
    out["by_horizon_profile (slope>0: deeper -> lower)"] = pd.DataFrame(t1)
    # quintiles of depth in falling calm
    t2 = []
    for h in [3, 5, 10]:
        sub = R[(R.h == h) & R.fc].copy()
        sub["q"] = pd.qcut(sub["depth"], 4, labels=False, duplicates="drop")
        for q, g in sub.groupby("q"):
            m, t, n, d = clust_t(g)
            t2.append(dict(h=h, q=q, depth_mean=g.depth.mean(), n=n, mean_ex=m, t=t, mean_tot=g.tot.mean()))
    out["falling_calm depth quartiles"] = pd.DataFrame(t2)
    t3 = []
    for h in [3, 5]:
        for key in ["coin", "yr"]:
            sub = R[(R.h == h) & R.fc]
            for k, g in sub.groupby(key):
                if len(g) < 8: continue
                m, t, n, d = clust_t(g); b, bt = slope(g)
                t3.append(dict(h=h, by=key, k=str(k), n=n, mean_ex=m, t=t, slope_t=bt))
    out["falling_calm by coin/year"] = pd.DataFrame(t3)
    # recent 5-day return grading in falling calm
    t4 = []
    for h in [3, 5]:
        sub = R[(R.h == h) & R.fc].dropna(subset=["r5"]).copy()
        sub["q"] = pd.qcut(sub["r5"], 4, labels=False, duplicates="drop")
        for q, g in sub.groupby("q"):
            m, t, n, d = clust_t(g)
            t4.append(dict(h=h, q=q, r5_mean=g.r5.mean(), n=n, mean_ex=m, t=t))
    out["falling_calm 5d-return quartiles"] = pd.DataFrame(t4)
    return out
