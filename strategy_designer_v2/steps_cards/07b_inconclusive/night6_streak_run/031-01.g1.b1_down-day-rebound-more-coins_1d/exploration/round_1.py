def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    for coin, wins in bars.items():
        # drift per horizon over all windows, non-overlapping
        drift = {}
        for h in H:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.extend(list(c[idx + h] / c[idx] - 1))
            drift[h] = np.nanmean(vals)
        for w, df in wins.items():
            c = df["close"].reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            vol = r1.rolling(60, min_periods=20).std()
            z = r1 / vol
            r60 = c / c.shift(60) - 1
            volrank = vol / vol.rolling(365, min_periods=60).median()
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                for k, i in enumerate(idx):
                    if np.isnan(z.iloc[i]):
                        continue
                    rows.append((coin, w, h, ts.iloc[i].year, ts.iloc[i].normalize(),
                                 z.iloc[i], fwd[k] - drift[h], r60.iloc[i], volrank.iloc[i]))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "year", "day", "z", "u", "r60", "vr"])

    def ct(sub, col="u"):
        g = sub.groupby("day")[col].sum()
        n = len(g)
        if n < 5:
            return np.nan, n
        m = sub[col].mean()
        se = np.sqrt((g - g.mean() * 0 - (sub.groupby("day")[col].count() * m)).pow(2).sum()) / len(sub)
        return m / se if se > 0 else np.nan, n

    def slope_t(sub):
        x = sub["z"].values; y = sub["u"].values
        if len(sub) < 30:
            return np.nan, np.nan, len(sub)
        X = np.c_[np.ones_like(x), x]
        b = np.linalg.lstsq(X, y, rcond=None)[0]
        e = y - X @ b
        XtX = np.linalg.inv(X.T @ X)
        s = pd.DataFrame(X * e[:, None]).groupby(sub["day"].values).sum().values
        V = XtX @ (s.T @ s) @ XtX
        return b[1], b[1] / np.sqrt(V[1, 1]), len(sub)

    out = {}
    # buckets of z for each horizon: mean unusual move and t
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    res = []
    for h in H:
        for b, sub in d[d.h == h].groupby("zb", observed=True):
            t, nd = ct(sub)
            res.append((h, str(b), len(sub), sub["u"].mean() * 100, t))
    out["by_z_bucket_h"] = pd.DataFrame(res, columns=["h", "z", "n", "unusual_%", "t"])
    # slope of u on falls (z<0, using -z) per horizon
    res = []
    for h in H:
        sub = d[(d.h == h) & (d.z < 0)].copy(); sub["z"] = -sub["z"]
        b, t, n = slope_t(sub); res.append(("down", h, b * 100, t, n))
        sub = d[(d.h == h) & (d.z > 0)].copy()
        b, t, n = slope_t(sub); res.append(("up", h, b * 100, t, n))
    out["slope_by_side_h"] = pd.DataFrame(res, columns=["side", "h", "slope_%perz", "t", "n"])
    d3 = d[(d.h == 3) & (d.z < 0)].copy(); d3["z"] = -d3["z"]
    res = []
    for y, sub in d3.groupby("year"):
        b, t, n = slope_t(sub); tm, _ = ct(sub)
        res.append((y, n, sub.u.mean() * 100, tm, b * 100, t))
    out["down_h3_by_year"] = pd.DataFrame(res, columns=["year", "n", "unusual_%", "t_mean", "slope", "t_slope"])
    res = []
    for c_, sub in d3.groupby("coin"):
        b, t, n = slope_t(sub); tm, _ = ct(sub)
        res.append((c_, n, sub.u.mean() * 100, tm, b * 100, t))
    out["down_h3_by_coin"] = pd.DataFrame(res, columns=["coin", "n", "unusual_%", "t_mean", "slope", "t_slope"])
    res = []
    for lab, m in [("r60>0", d3.r60 > 0), ("r60<=0", d3.r60 <= 0), ("vr>1", d3.vr > 1), ("vr<=1", d3.vr <= 1)]:
        sub = d3[m]; b, t, n = slope_t(sub); tm, _ = ct(sub)
        res.append((lab, n, sub.u.mean() * 100, tm, b * 100, t))
    out["down_h3_by_regime"] = pd.DataFrame(res, columns=["regime", "n", "unusual_%", "t_mean", "slope", "t_slope"])
    return out
