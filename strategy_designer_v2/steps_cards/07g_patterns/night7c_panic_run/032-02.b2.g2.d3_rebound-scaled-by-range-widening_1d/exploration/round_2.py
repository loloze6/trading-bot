import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, h, l = b["close"], b["high"], b["low"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["ret0"] = c / c.shift(1) - 1
            d["fwd1"] = c.shift(-1) / c - 1
            d["fwd2"] = c.shift(-2) / c - 1
            d["pos2"] = (np.arange(len(b)) % 2 == 0)
            d["loc"] = ((c - l) / (h - l)).where(h > l)
            d["sd30"] = d["ret0"].rolling(30).std().shift(1)
            d["z0"] = d["ret0"] / d["sd30"]
            rng = (h - l) / c
            d["rr"] = rng.rolling(30).mean() / rng.rolling(90).mean()
            d["r30"] = c / c.shift(30) - 1
            d["alloc"] = b["postRebalance_current_allocation"]
            d["gain"] = d["alloc"] * d["fwd1"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin")["fwd1"].mean()
    mu2 = D[D.pos2].groupby("coin")["fwd2"].mean()
    D["x1"] = D["fwd1"] - D["coin"].map(mu1)
    D["x2"] = D["fwd2"] - D["coin"].map(mu2)
    D["day"] = D["ts"].dt.floor("D")
    D["wd"] = D["ts"].dt.weekday
    D["yr"] = D["ts"].dt.year

    def ct(sub, col):
        s = sub.dropna(subset=[col])
        n = len(s)
        if n < 10: return pd.Series({"n": n, "mean%": np.nan, "t": np.nan, "days": 0})
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / n
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / se, "days": g.size})

    def slope_t(sub, xcol, ycol):
        s = sub.dropna(subset=[xcol, ycol])
        x = s[xcol] - s[xcol].mean(); y = s[ycol] - s[ycol].mean()
        bta = (x * y).sum() / (x * x).sum()
        e = y - bta * x
        g = (x * e).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / (x * x).sum()
        return pd.Series({"n": len(s), "slope": bta, "t": bta / se, "days": g.size})

    out = {}
    D["z0c"] = D["z0"].clip(-4, 4)
    D["dz"] = (-D["z0c"]).clip(lower=0)  # size of the fall only
    D["uz"] = D["z0c"].clip(lower=0)
    out["slope x1 on -z0 (falls only, z<0)"] = pd.DataFrame({
        "all": slope_t(D[D.z0 < 0].assign(m=-D.z0c), "m", "x1"),
        "rr>1": slope_t(D[(D.z0 < 0) & (D.rr > 1)].assign(m=-D.z0c), "m", "x1"),
        "rr<=1": slope_t(D[(D.z0 < 0) & (D.rr <= 1)].assign(m=-D.z0c), "m", "x1"),
        "r30<0": slope_t(D[(D.z0 < 0) & (D.r30 < 0)].assign(m=-D.z0c), "m", "x1"),
        "r30>=0": slope_t(D[(D.z0 < 0) & (D.r30 >= 0)].assign(m=-D.z0c), "m", "x1"),
        "up days z>0": slope_t(D[D.z0 > 0].assign(m=D.z0c), "m", "x1"),
    }).T
    D["zb"] = pd.cut(D["z0"], [-99, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 99])
    out["x1 by z0 band"] = D.groupby("zb").apply(lambda s: ct(s, "x1"))
    out["x2 by z0 band (grid 2d)"] = D[D.pos2].groupby("zb").apply(lambda s: ct(s, "x2"))
    big = D[D.z0 <= -1.5]
    out["x1 after z<=-1.5 by year"] = big.groupby("yr").apply(lambda s: ct(s, "x1"))
    out["x1 after z<=-1.5 by coin"] = big.groupby("coin").apply(lambda s: ct(s, "x1"))
    out["x1 after z<=-1.5 by loc half"] = big.groupby(D["loc"] < 0.3).apply(lambda s: ct(s, "x1"))
    out["slope x1 on loc, all bars, by rr"] = pd.DataFrame({
        "all": slope_t(D.assign(m=1 - D["loc"]), "m", "x1"),
        "rr>1": slope_t(D[D.rr > 1].assign(m=1 - D["loc"]), "m", "x1"),
        "rr<=1": slope_t(D[D.rr <= 1].assign(m=1 - D["loc"]), "m", "x1"),
        "loc on z<0": slope_t(D[D.z0 < 0].assign(m=1 - D["loc"]), "m", "x1"),
    }).T
    out["x1 by weekday by year (Thu+Fri)"] = D[D.wd.isin([3, 4])].groupby("yr").apply(lambda s: ct(s, "x1"))
    out["x1 by weekday by year (Mon-Wed)"] = D[D.wd.isin([0, 1, 2])].groupby("yr").apply(lambda s: ct(s, "x1"))
    out["x1 after big falls by weekday"] = D[D.z0 <= -1].groupby("wd").apply(lambda s: ct(s, "x1"))
    out["book gain in position by year"] = D[D.alloc.abs() > 0].groupby("yr").apply(lambda s: ct(s, "gain"))
    out["x1 by window, z<=-1.5"] = big.groupby("win").apply(lambda s: ct(s, "x1"))
    return out
