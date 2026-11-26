def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:] / c[:-1] - 1)
        cm = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            nxt = c.shift(-1) / c - 1
            r1 = c / c.shift(1) - 1
            down = (r1 < 0).astype(int)
            streak = down.groupby((down == 0).cumsum()).cumsum()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "prof": (b["regime"] == "unknown"),
                "fc": b["forecast"].astype(float),
                "ex": nxt - cm, "r1": r1,
                "r3": c / c.shift(3) - 1, "r5": c / c.shift(5) - 1,
                "r10": c / c.shift(10) - 1, "streak": streak,
                "vol": r1.rolling(30).std(),
            })
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["ex"])

    def tclust(x):
        dev = x["ex"] - x["ex"].mean()
        s = dev.groupby(x["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / len(x)
        return pd.Series({"n": len(x), "days": x["day"].nunique(),
                          "mean_ex%": 100 * x["ex"].mean(),
                          "t": x["ex"].mean() / se if se > 0 else np.nan})

    out = {}
    P = D[D.prof]
    out["profile all days vs down days vs up days"] = pd.concat({
        "all": tclust(P), "down": tclust(P[P.r1 < 0]), "up": tclust(P[P.r1 >= 0]),
        "nonprofile_down": tclust(D[(~D.prof) & (D.r1 < 0)])}, axis=1).T
    Pd = P[P.r1 < 0]
    out["profile down days by streak"] = Pd.groupby(Pd.streak.clip(upper=5)).apply(tclust)
    for col in ["r1", "r3", "r5", "r10"]:
        x = P.dropna(subset=[col]).copy()
        x["z"] = x[col] / x["vol"]
        x = x.dropna(subset=["z"])
        x["q"] = pd.qcut(x["z"], 5, labels=False, duplicates="drop")
        out[f"profile all days by {col}/vol quintile"] = x.groupby("q").apply(tclust)
    # down days in profile by 5d depth quintile
    x = Pd.dropna(subset=["r5", "vol"]).copy()
    x["q"] = pd.qcut(x["r5"] / x["vol"], 5, labels=False)
    out["profile down days by r5/vol quintile"] = x.groupby("q").apply(tclust)
    out["profile down days by coin"] = Pd.groupby("coin").apply(tclust)
    out["profile down days by window"] = Pd.groupby("win").apply(tclust)
    # regressions in profile, day-clustered slope t
    def slope(x, col):
        x = x.dropna(subset=[col])
        xv = x[col] - x[col].mean(); yv = x["ex"] - x["ex"].mean()
        b = (xv * yv).sum() / (xv ** 2).sum()
        res = yv - b * xv
        s = (xv * res).groupby(x["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (xv ** 2).sum()
        return pd.Series({"slope": b, "t": b / se, "n": len(x)})
    P2 = P.copy()
    for col in ["r1", "r3", "r5", "r10"]:
        P2[col + "z"] = P2[col] / P2["vol"]
    out["profile slopes of ex on past return/vol (neg slope = rebound)"] = pd.DataFrame(
        {c: slope(P2, c + "z") for c in ["r1", "r3", "r5", "r10"]}).T
    return out
