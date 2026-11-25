def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            allr.append(pd.Series(c).pct_change().dropna().values)
        mu = np.concatenate(allr).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            f = df["forecast"].fillna(0).values.astype(float)
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(n):
                r = {"coin": coin, "w": w, "year": ts.iloc[i].year, "i": i, "f": f[i], "mu": mu,
                     "day": ts.iloc[i].normalize()}
                for h in (1, 3, 7):
                    r[f"r{h}"] = c[i+h]/c[i]-1 - h*mu if i+h < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    a = d[d.f != 0].copy()
    a["s"] = np.sign(a.f)
    a["x1"] = a.s * a.r1
    out = {}
    def tday(sub, col):
        g = sub.groupby("day")[col].sum()
        m = sub[col].mean()
        se = np.sqrt((g - g.mean()*0 - sub.groupby("day")[col].count()*m).pow(2).sum())/len(sub)
        return m, m/se if se > 0 else np.nan, len(sub)
    res = {}
    for k, sub in [("all", a)] + [("side " + str(s), a[a.s == s]) for s in (1, -1)]:
        res[k] = tday(sub, "x1")
    for coin, sub in a.groupby("coin"):
        res["coin " + coin] = tday(sub, "x1")
    for y, sub in a.groupby("year"):
        res["year " + str(y)] = tday(sub, "x1")
    a["q"] = pd.qcut(a.f.abs(), 4, labels=False, duplicates="drop")
    for q, sub in a.groupby("q"):
        res["|f| q" + str(q)] = tday(sub, "x1")
    out["signed next-day excess (mean,t,n)"] = pd.DataFrame(res, index=["mean", "t", "n"]).T
    # longer horizons, non-overlapping grid
    hz = {}
    for h in (1, 3, 7):
        sub = a[(a.i % h == 0)].dropna(subset=[f"r{h}"]).copy()
        sub["x"] = sub.s * sub[f"r{h}"]
        sub["xf"] = sub.f/10 * sub[f"r{h}"]
        for side in (0, 1, -1):
            ss = sub if side == 0 else sub[sub.s == side]
            m, t, nn = tday(ss, "x")
            sl = stats.linregress(ss.f/10, ss[f"r{h}"])
            hz[f"h{h} side{side}"] = [m, t, nn, sl.slope, sl.slope/sl.stderr]
    out["horizons signed excess"] = pd.DataFrame(hz, index=["mean", "t", "n", "slope", "slope_t_ols"]).T
    # window-level
    out["by window"] = a.groupby("w").x1.agg(["mean", "count"])
    return out
