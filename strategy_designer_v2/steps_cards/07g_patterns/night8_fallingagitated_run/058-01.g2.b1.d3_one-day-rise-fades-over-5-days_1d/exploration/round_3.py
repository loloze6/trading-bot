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
            pct = sd30.rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            r60 = c / c.shift(60) - 1
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "ts": b["timestamp"].astype(str).str[:10],
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "z1": r1 / sd30, "r60": r60, "pct": pct,
                "fwd": c.shift(-H) / c - 1,
                "fwd2": c.shift(-2) / c - 1,
                "fa": (b["regime"] == "unknown").astype(int),
                "grid": (np.arange(len(b)) % H == 0),
                "grid2": (np.arange(len(b)) % 2 == 0)}))
    d = pd.concat(rows, ignore_index=True)
    d = d.join(d[d.grid].groupby("coin")["fwd"].mean().rename("drift"), on="coin")
    d = d.join(d[d.grid].groupby("coin")["fwd"].std().rename("sd5"), on="coin")
    d = d.join(d[d.grid2].groupby("coin")["fwd2"].mean().rename("drift2"), on="coin")
    d["unus"] = d["fwd"] - d["drift"]
    d["unus2"] = d["fwd2"] - d["drift2"]
    d["str"] = d["unus"] / d["sd5"]
    d["agit"] = np.where(d["pct"] > 0.5, "agit", np.where(d["pct"].notna(), "calm", None))
    d["trend"] = pd.cut(d["r60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])

    def tcl(x, col="unus"):
        x = x.dropna(subset=[col])
        if len(x) < 10: return pd.Series({"n": len(x), "mean": np.nan, "t": np.nan, "days": 0})
        dev = (x[col] - x[col].mean()).groupby(x["ts"]).sum()
        D = len(dev); se = np.sqrt((dev ** 2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "mean": x[col].mean(), "t": x[col].mean() / se, "days": D})

    def slope(x, col="unus"):
        x = x.dropna(subset=[col, "z1"])
        if len(x) < 20: return pd.Series({"n": len(x), "slope": np.nan, "t": np.nan})
        X = x["z1"] - x["z1"].mean(); y = x[col]
        b = (X * y).sum() / (X ** 2).sum()
        e = y - y.mean() - b * X
        s = (X * e).groupby(x["ts"]).sum()
        D = len(s); se = np.sqrt((s ** 2).sum() * D / (D - 1)) / (X ** 2).sum()
        return pd.Series({"n": len(x), "slope": b, "t": b / se})

    g = d[d.grid].dropna(subset=["unus", "z1", "agit"]).copy()
    out = {}
    up = g[g.z1 > 0]
    out["up days slope by agit x trend"] = up.groupby(["agit", "trend"]).apply(slope)
    out["up days calm slope by year"] = up[up.agit == "calm"].groupby("yr").apply(slope)
    out["up days calm slope by coin"] = up[up.agit == "calm"].groupby("coin").apply(slope)
    calm_up = up[(up.agit == "calm") & (up.z1 > 1)]
    out["calm, z1>1: by year"] = calm_up.groupby("yr").apply(tcl)
    out["calm, z1>1: strength"] = tcl(calm_up, "str")
    out["calm, up days by z1 bin"] = up[up.agit == "calm"].assign(b=pd.cut(up["z1"], [0, 0.5, 1, 1.5, 2, 99])).groupby("b").apply(tcl)
    out["agit, up days by z1 bin"] = up[up.agit == "agit"].assign(b=pd.cut(up["z1"], [0, 0.5, 1, 1.5, 2, 99])).groupby("b").apply(tcl)
    dn = g[g.z1 < 0]
    out["down days slope by agit x trend"] = dn.groupby(["agit", "trend"]).apply(slope)
    g2 = d[d.grid2].dropna(subset=["unus2", "z1", "agit"])
    out["2-day: up days slope by agit"] = g2[g2.z1 > 0].groupby("agit").apply(lambda x: slope(x, "unus2"))
    return out
