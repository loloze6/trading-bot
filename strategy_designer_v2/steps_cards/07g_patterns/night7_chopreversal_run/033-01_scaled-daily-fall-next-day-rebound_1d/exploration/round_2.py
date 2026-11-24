def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"], utc=True),
                "r": r, "z": r / sd30.shift(1), "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "vrel": np.log(v / v.rolling(30, min_periods=10).median().shift(1)),
                "sdpct": sd30.rolling(365, min_periods=120).rank(pct=True),
                "tr60": c / c.shift(60) - 1})
            df["pos"] = np.arange(len(df)); rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["x1"] = D["f1"] - D["coin"].map(D.groupby("coin")["f1"].mean())
    D["day"] = D["ts"].dt.floor("D")

    def clus(s, col="x1"):
        s = s.dropna(subset=[col])
        if len(s) < 10: return pd.Series({"n": len(s), "days": 0, "mean%": np.nan, "t_day": np.nan})
        m = s[col].mean(); gs = (s[col] - m).groupby(s["day"]).sum(); G = len(gs)
        se = np.sqrt((gs**2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean%": 100*m, "t_day": m/se})

    def slope(s, xcol, ycol="x1"):
        s = s.dropna(subset=[xcol, ycol])
        x = s[xcol] - s[xcol].mean(); y = s[ycol]
        b = (x*y).sum() / (x*x).sum(); e = y - y.mean() - b*x
        gs = (x*e).groupby(s["day"]).sum(); G = len(gs)
        se = np.sqrt((gs**2).sum()*G/(G-1)) / (x*x).sum()
        return pd.Series({"n": len(s), "days": G, "slope": b, "t_day": b/se})

    out = {}
    dn = D[D["z"] < 0].copy()
    dn["fall"] = -dn["z"]
    dn["fallxvol"] = dn["fall"] * dn["vrel"].clip(-2, 2)
    dn["fallvol_pos"] = dn["fall"] * np.exp(dn["vrel"].clip(-2, 2))
    out["slopes on down days"] = pd.DataFrame({k: slope(dn, k) for k in ["fall", "vrel", "fallxvol", "fallvol_pos"]}).T
    # volume tertiles x fall
    dn["vt"] = pd.qcut(dn["vrel"], 3, labels=["lowV", "midV", "highV"])
    dn["fb"] = pd.cut(dn["fall"], [0, 1, 2, np.inf], labels=["0-1", "1-2", ">2"])
    out["down: volume tertile x fall"] = dn.groupby(["vt", "fb"], observed=True).apply(clus)
    # slope of fall within agitation
    dn["ag"] = np.where(dn["sdpct"] > 0.5, "agitated", np.where(dn["sdpct"].notna(), "calm", None))
    out["slope of fall by agitation"] = dn.dropna(subset=["ag"]).groupby("ag").apply(lambda s: slope(s, "fall"))
    # up days: next day by volume
    up = D[D["z"] > 0].copy(); up["vt"] = pd.qcut(up["vrel"], 3, labels=["lowV", "midV", "highV"])
    out["up days by volume tertile"] = up.groupby("vt", observed=True).apply(clus)
    out["volume alone, all days, slope"] = slope(D, "vrel")
    # 2-day horizon, grid, high-volume falls
    g2 = D[D["pos"] % 2 == 0].copy(); g2["x2"] = g2["f2"] - g2["coin"].map(g2.groupby("coin")["f2"].mean())
    g2d = g2[g2["z"] < -1]
    g2d = g2d.assign(vt=pd.cut(g2d["vrel"], [-np.inf, 0, 0.5, np.inf], labels=["v<med", "v 1-1.6x", "v>1.6x"]))
    out["2d excess, z<-1, by volume"] = g2d.groupby("vt", observed=True).apply(lambda s: clus(s, "x2"))
    # high-volume large falls by window (stability)
    hv = dn[(dn["fall"] > 1) & (dn["vt"] == "highV")]
    out["highV fall>1 by window"] = hv.groupby("win").apply(clus)
    out["highV fall>1 by coin"] = hv.groupby("coin").apply(clus)
    # book: share of position held after small falls
    D["fcb"] = pd.cut(D["z"], [-np.inf, -1, -0.5, 0, np.inf], labels=["z<-1", "-1..-0.5", "-0.5..0", "up"])
    D["gain"] = D["alloc"] * D["f1"]
    out["book: allocation and gain by z"] = D.groupby("fcb", observed=True).agg(
        mean_alloc=("alloc", "mean"), sum_gain=("gain", "sum"), n=("gain", "size"))
    return out
