def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20, min_periods=15).std()
            rng = (b["high"] - b["low"]).astype(float)
            cl = (c - b["low"]) / rng.replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "w": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "z": r / sd20, "cl": cl,
                "z3": (c / c.shift(3) - 1) / (sd20 * np.sqrt(3)),
                "z5": (c / c.shift(5) - 1) / (sd20 * np.sqrt(5)),
                "r60": c / c.shift(60) - 1,
                "vr": sd20 / r.rolling(60, min_periods=40).std(),
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1,
                "i": np.arange(len(b))})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["f1"].mean()
    mu2 = D[D.i % 2 == 0].groupby("coin")["f2"].mean()
    D["x1"] = D["f1"] - D["coin"].map(mu)
    D["x2"] = D["f2"] - D["coin"].map(mu2)
    lo, hi = D["x1"].quantile([0.01, 0.99])
    D["x1w"] = D["x1"].clip(lo, hi)

    def slope(df, xcol, ycol):
        s = df[[xcol, ycol, "day"]].dropna()
        n = len(s)
        if n < 30: return pd.Series({"n": n, "slope%": np.nan, "t": np.nan})
        x = s[xcol] - s[xcol].mean(); y = s[ycol] - s[ycol].mean()
        bta = (x * y).sum() / (x * x).sum()
        e = y - bta * x
        S = (x * e).groupby(s["day"]).sum()
        se = np.sqrt((S ** 2).sum()) / (x * x).sum()
        return pd.Series({"n": n, "days": s["day"].nunique(), "slope%": bta * 100, "t": bta / se})

    res = {}
    F = D.copy()
    F["fall"] = (-F["z"]).clip(lower=0)
    F["fall_low"] = F["fall"] * (1 - F["cl"])
    F["fall5"] = (-F["z5"]).clip(lower=0)
    F["fall3"] = (-F["z3"]).clip(lower=0)
    F["rise"] = F["z"].clip(lower=0)
    F["rise_high"] = F["rise"] * F["cl"]
    out = {}
    for xc in ["fall", "fall_low", "fall3", "fall5", "rise", "rise_high"]:
        out[xc + "_x1"] = slope(F, xc, "x1")
        out[xc + "_x1win"] = slope(F, xc, "x1w")
        out[xc + "_x2grid"] = slope(F[F.i % 2 == 0], xc, "x2")
    res["slopes_all_bars"] = pd.DataFrame(out).T
    # within falls only: does close location add, does 5d fall add
    dn = F[F.z < 0]
    o2 = {}
    for xc in ["fall", "fall_low", "fall5", "cl"]:
        o2[xc] = slope(dn, xc, "x1")
        o2[xc + "_win"] = slope(dn, xc, "x1w")
    res["slopes_down_days"] = pd.DataFrame(o2).T
    # profile split for fall5 and fall
    F["trend"] = pd.cut(F["r60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    F["agit"] = np.where(F["vr"] > 1, "agitated", "calm")
    o3 = {}
    for (tr), g in F.groupby("trend", observed=True):
        for xc in ["fall", "fall5"]:
            o3[f"{tr}_{xc}"] = slope(g, xc, "x1w")
    for ag, g in F.groupby("agit"):
        for xc in ["fall", "fall5"]:
            o3[f"{ag}_{xc}"] = slope(g, xc, "x1w")
    res["slopes_by_profile"] = pd.DataFrame(o3).T
    o4 = {}
    for coin, g in F.groupby("coin"):
        o4[coin] = slope(g, "fall5", "x1w")
    res["fall5_by_coin"] = pd.DataFrame(o4).T
    o5 = {}
    for wd in range(7):
        pass
    D["wd"] = D["day"].dt.weekday
    res["small_up_x1_by_cl"] = D[(D.z > 0) & (D.z < 1)].assign(
        clb=pd.cut(D["cl"], [0, 0.5, 0.75, 1.0001], include_lowest=True)).groupby("clb", observed=True)["x1w"].agg(["count", "mean"])
    return res
