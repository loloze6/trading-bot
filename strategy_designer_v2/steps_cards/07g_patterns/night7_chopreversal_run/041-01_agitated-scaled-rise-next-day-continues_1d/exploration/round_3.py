def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "z": r / sd, "sd": sd, "n1": c.shift(-1) / c - 1,
                "n2": c.shift(-2) / c - 1, "pos": np.arange(len(b)),
                "agit": (b["regime"] != "chop").astype(int),
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "r60": c / c.shift(60) - 1,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["x1"] = d["n1"] - d.groupby("coin")["n1"].transform("mean")
    mu2 = d[d.pos % 2 == 0].groupby("coin")["n2"].mean()
    d["x2"] = d["n2"] - d["coin"].map(mu2)
    d["u1"] = d["x1"] / d["sd"]
    d["day"] = d["ts"].dt.floor("D")
    d["trend"] = np.where(d.r60 > 0.1, "rising", np.where(d.r60 < -0.1, "falling", "choppy"))

    def slope(s, xcol, ycol):
        s = s.dropna(subset=[xcol, ycol])
        if len(s) < 30: return (len(s), np.nan, np.nan)
        x = s[xcol] - s[xcol].mean(); y = s[ycol] - s[ycol].mean()
        bta = (x * y).sum() / (x ** 2).sum()
        e = y - bta * x
        g = (x * e).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / (x ** 2).sum()
        return (len(s), bta, bta / se)

    def ct(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 10: return (len(s), np.nan, np.nan, np.nan)
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return (len(s), s["day"].nunique(), m, m / se)

    out = {}
    res = []
    for a in [0, 1]:
        for tr in ["falling", "choppy", "rising"]:
            for side, cond in [("fall", d.z < 0), ("rise", d.z > 0)]:
                s = d[(d.agit == a) & (d.trend == tr) & cond]
                res.append([a, tr, side, "z->u1"] + list(slope(s, "z", "u1")))
                res.append([a, tr, side, "z->x2"] + list(slope(s[s.pos % 2 == 0], "z", "x2")))
    out["slope_trend_side"] = pd.DataFrame(res, columns=["agit", "trend", "side", "reg", "n", "slope", "t"])

    res = []
    s0 = d[(d.agit == 1) & (d.trend == "falling")].copy()
    s0["zb"] = pd.cut(s0["z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    for zb, s in s0.groupby("zb", observed=True):
        res.append([str(zb), "x1"] + list(ct(s, "x1")) + [s["n1"].mean()])
    out["falling_agit_zbins"] = pd.DataFrame(res, columns=["zbin", "h", "n", "days", "mean_x", "t", "total"])

    res = []
    for w, s in d[(d.agit == 1) & (d.trend == "falling") & (d.z < 0)].groupby("win"):
        res.append([w] + list(slope(s, "z", "u1")))
    out["fa_fall_by_window"] = pd.DataFrame(res, columns=["win", "n", "slope", "t"])
    res = []
    for co, s in d[(d.agit == 1) & (d.trend == "falling") & (d.z < 0)].groupby("coin"):
        res.append([co] + list(slope(s, "z", "u1")))
    out["fa_fall_by_coin"] = pd.DataFrame(res, columns=["coin", "n", "slope", "t"])
    return out
