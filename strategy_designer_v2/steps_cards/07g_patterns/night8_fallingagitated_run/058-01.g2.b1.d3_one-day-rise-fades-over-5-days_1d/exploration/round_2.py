def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            sd365 = sd30.rolling(365, min_periods=60)
            pct = sd30.rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            r60 = c / c.shift(60) - 1
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "ts": b["timestamp"].astype(str).str[:10],
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "z1": r1 / sd30, "r60": r60, "pct": pct, "fwd": fwd, "fwd1": fwd1,
                "fa": (b["regime"] == "unknown").astype(int),
                "grid": (np.arange(len(b)) % H == 0)}))
    d = pd.concat(rows, ignore_index=True)
    d = d.join(d[d.grid].groupby("coin")["fwd"].mean().rename("drift"), on="coin")
    d["unus"] = d["fwd"] - d["drift"]
    sd5 = d[d.grid].groupby("coin")["fwd"].std().rename("sd5")
    d = d.join(sd5, on="coin")
    d["str"] = d["unus"] / d["sd5"]
    g = d[d.grid].dropna(subset=["unus", "z1"]).copy()

    def tcl(x, col="unus"):
        if len(x) < 10: return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan, "days": 0})
        dev = (x[col] - x[col].mean()).groupby(x["ts"]).sum()
        D = len(dev); se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "mean": x[col].mean(), "t": x[col].mean() / se, "days": D})

    def slope(x):
        # clustered slope of unus on z1
        if len(x) < 20: return pd.Series({"n": len(x), "slope": np.nan, "t": np.nan})
        X = x["z1"] - x["z1"].mean(); y = x["unus"]
        b = (X * y).sum() / (X ** 2).sum()
        e = y - y.mean() - b * X
        s = (X * e).groupby(x["ts"]).sum()
        D = len(s); se = np.sqrt((s ** 2).sum() * D / (D - 1)) / (X ** 2).sum()
        return pd.Series({"n": len(x), "slope": b, "t": b / se})

    out = {}
    nf = g[g.fa == 0].copy()
    up = nf[nf.z1 > 0].copy()
    out["notFA up days: slope unus on z1 (clustered)"] = slope(up)
    out["notFA up z1>1: by window"] = up[up.z1 > 1].groupby("win").apply(tcl)
    out["notFA up z1>1: by year"] = up[up.z1 > 1].groupby("yr").apply(tcl)
    up["agit"] = np.where(up["pct"] > 0.5, "agit", "calm")
    up["trend"] = pd.cut(up["r60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    out["notFA up z1>1: by trend x agitation"] = up[up.z1 > 1].groupby(["trend", "agit"]).apply(tcl)
    out["notFA up days: slope by agitation"] = up.groupby("agit").apply(slope)
    out["notFA up z1>1: by coin"] = up[up.z1 > 1].groupby("coin").apply(tcl)
    out["notFA up z1>1 strength"] = tcl(up[up.z1 > 1], "str")
    # weekday, clustered by day, all bars
    dd = d.dropna(subset=["fwd1"]).copy()
    dd["unus"] = dd["fwd1"] - dd.groupby("coin")["fwd1"].transform("mean")
    out["next-day by weekday, all, clustered"] = dd.groupby("wd").apply(tcl)
    out["next-day by weekday, FA, clustered"] = dd[dd.fa == 1].groupby("wd").apply(tcl)
    out["next-day Tue FA by year"] = dd[(dd.fa == 1) & (dd.wd == 1)].groupby("yr").apply(tcl)
    return out
