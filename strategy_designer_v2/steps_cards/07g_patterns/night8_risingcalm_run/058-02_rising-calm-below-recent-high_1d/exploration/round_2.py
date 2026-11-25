def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=30).std()
            hi5 = c.rolling(5, min_periods=5).max()
            dip = (c - hi5) / hi5 / sd30
            r5s = (c / c.shift(5) - 1) / (sd30 * np.sqrt(5))
            tr60 = c / c.shift(60) - 1
            sd_med = sd30.expanding(min_periods=30).median()
            agit = (sd30 > sd_med).astype(float).where(sd30.notna() & sd_med.notna())
            n = len(b)
            for h in (2, 5):
                f = c.shift(-h) / c - 1
                idx = np.arange(0, n, h)
                rows.append(pd.DataFrame({
                    "h": h, "coin": coin, "win": w,
                    "regime": b["regime"].values[idx],
                    "dip": dip.values[idx], "r5s": r5s.values[idx],
                    "tr60": tr60.values[idx], "agit": agit.values[idx],
                    "f": f.values[idx],
                    "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values[idx]}))
    G = pd.concat(rows, ignore_index=True)
    G = G[G["f"].notna()].copy()
    G["ex"] = G["f"] - G.groupby(["h", "coin"])["f"].transform("mean")
    G["trc"] = pd.cut(G["tr60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    G["prof"] = G["trc"].astype(str) + "_" + G["agit"].map({1.0: "ag", 0.0: "calm"}).astype(str)

    def clus_t(s, xcol, ycol="ex"):
        s = s.dropna(subset=[xcol, ycol])
        if len(s) < 20:
            return (len(s), np.nan, np.nan, np.nan)
        x = s[xcol] - s[xcol].mean(); y = s[ycol]
        beta = (x * (y - y.mean())).sum() / (x ** 2).sum()
        e = (y - y.mean()) - beta * x
        g = (x * e).groupby(s["day"].values).sum()
        se = np.sqrt((g ** 2).sum()) / (x ** 2).sum()
        return (len(s), s["day"].nunique(), beta, beta / se)

    res = {}
    for (h, p), s in G.groupby(["h", "prof"]):
        for xc in ("dip", "r5s"):
            res[(h, p, xc)] = clus_t(s, xc)
    out["clustered slope of ex on dip / r5s by profile"] = pd.DataFrame(res, index=["n", "days", "beta", "t"]).T
    for prof in ("rise_calm", "chop_ag"):
        s = G[(G["h"] == 5) & (G["prof"] == prof)].dropna(subset=["dip"])
        s = s.assign(dq=pd.qcut(s["dip"].rank(method="first"), 3, labels=False))
        a = s.groupby(["win", "dq"])["ex"].mean().unstack()
        out[f"{prof} h5 ex by window x dip tercile (0 deepest)"] = a
        b2 = s.groupby(["coin", "dq"])["ex"].mean().unstack()
        out[f"{prof} h5 ex by coin x dip tercile"] = b2
        out[f"{prof} h5 corr dip vs ex per window sign"] = pd.Series({
            "windows": s["win"].nunique(),
            "share_win_positive_slope": s.groupby("win").apply(
                lambda q: np.sign(np.corrcoef(q["dip"], q["ex"])[0, 1]) if len(q) > 4 else np.nan).gt(0).mean()})
    return out
