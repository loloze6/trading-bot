def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            hi5 = c.rolling(5, min_periods=5).max()
            hi10 = c.rolling(10, min_periods=10).max()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "dip": (c - hi5) / hi5 / sd30, "dip10": (c - hi10) / hi10 / sd30,
                               "rawdip": (c - hi5) / hi5,
                               "r5z": (c / c.shift(5) - 1) / (sd30 * np.sqrt(5)),
                               "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1, "f2": c.shift(-2) / c - 1,
                               "day": ts.dt.floor("D").values, "yr": ts.dt.year.values,
                               "inprof": (b["regime"] != "chop").values})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    def prep(H, col):
        g = d[d.pos % H == 0].copy()
        dr = g.groupby("coin")[col].mean()
        g["ex"] = g[col] - g.coin.map(dr)
        return g.dropna(subset=["ex"])
    def clslope(sub, x):
        sub = sub.dropna(subset=[x, "ex"])
        if len(sub) < 30: return [len(sub), np.nan, np.nan, np.nan, np.nan]
        X = sub[x].values; Y = sub["ex"].values
        Xc = X - X.mean(); b = (Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum()
        e = Y - Y.mean() - b * Xc
        s = pd.DataFrame({"day": sub.day.values, "u": Xc * e}).groupby("day")["u"].sum()
        se = np.sqrt((s ** 2).sum()) / (Xc ** 2).sum()
        return [len(sub), sub.day.nunique(), b, b / se, np.corrcoef(X, Y)[0, 1]]
    cols = ["n", "days", "slope", "t_dayclust", "corr"]
    g5 = prep(5, "f5")
    res = {}
    for x in ["dip", "dip10", "rawdip", "r5z"]:
        res[x] = clslope(g5, x)
    out["5d ex on measures, clustered by day"] = pd.DataFrame(res, index=cols).T
    res = {}
    for H, col in [(2, "f2"), (5, "f5"), (10, "f10")]:
        res[f"H{H}"] = clslope(prep(H, col), "dip")
    out["dip slope by horizon"] = pd.DataFrame(res, index=cols).T
    out["dip slope by year"] = pd.DataFrame({y: clslope(s, "dip") for y, s in g5.groupby("yr")}, index=cols).T
    out["dip slope by coin"] = pd.DataFrame({k: clslope(s, "dip") for k, s in g5.groupby("coin")}, index=cols).T
    out["dip slope by window"] = pd.DataFrame({k: clslope(s, "dip") for k, s in g5.groupby("w")}, index=cols).T
    q = g5.dropna(subset=["dip"]).copy()
    q["at_high"] = q.dip == 0
    nz = q[~q.at_high].copy()
    nz["q"] = pd.qcut(nz.dip, 4, labels=False)
    def tday(x):
        s = x.groupby(q.loc[x.index, "day"]).sum() if False else None
        return np.nan
    agg = []
    for k, s in list(nz.groupby("q")) + [("at_high", q[q.at_high])]:
        ds = s.groupby("day")["ex"].sum()
        t = s.ex.mean() * len(s) / np.sqrt(((s.ex - s.ex.mean()).groupby(s.day).sum() ** 2).sum())
        agg.append([k, len(s), s.dip.mean(), s.ex.mean(), t])
    out["ex5 by dip quartile (non-zero) and at high"] = pd.DataFrame(agg, columns=["grp", "n", "mean_dip", "mean_ex", "t_dayclust"])
    # book's largest days
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day", "book_return", "coin_return"]].copy(); days.append(x)
    D = pd.concat(days).dropna()
    D = D[D.book_return != 0]
    out["book nonzero days: share up, mean, n"] = pd.Series({"n": len(D), "share_up": (D.book_return > 0).mean(),
        "mean": D.book_return.mean(), "corr_with_coin": D.book_return.corr(D.coin_return)})
    return out
