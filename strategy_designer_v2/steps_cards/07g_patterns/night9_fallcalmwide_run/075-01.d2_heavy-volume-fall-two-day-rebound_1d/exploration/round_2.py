def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vr = v / v.shift(1).rolling(20, min_periods=20).mean()
            sd30 = r1.rolling(30, min_periods=25).std()
            pct = sd30.rolling(365, min_periods=120).apply(lambda a: (a <= a[-1]).mean(), raw=True)
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "vr": vr, "lvr": np.log(vr), "z": r1 / r1.shift(1).rolling(20, min_periods=15).std(),
                "tr60": c / c.shift(60) - 1, "tr20": c / c.shift(20) - 1, "agp": pct,
                "f2": c.shift(-2) / c - 1, "f4": c.shift(-4) / c - 1,
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    res = {}

    def ct(x, day):
        m = pd.DataFrame({"x": x, "d": day}).dropna()
        if len(m) < 10: return (np.nan, np.nan, len(m))
        mu = m["x"].mean(); S = (m["x"] - mu).groupby(m["d"]).sum()
        se = np.sqrt((S ** 2).sum()) / len(m)
        return (mu, mu / se if se > 0 else np.nan, len(m))

    def slope(df, xcol, ycol):
        m = df[[xcol, ycol, "day"]].dropna()
        if len(m) < 30: return (np.nan, np.nan, len(m))
        x = m[xcol] - m[xcol].mean(); y = m[ycol] - m[ycol].mean()
        b = (x * y).sum() / (x * x).sum(); e = y - b * x
        S = (x * e).groupby(m["day"]).sum()
        se = np.sqrt((S ** 2).sum()) / (x * x).sum()
        return (b, b / se, len(m))

    for h, col in [(2, "f2"), (4, "f4")]:
        G = D[D["pos"] % h == 0].copy()
        G["ex"] = G[col] - G.groupby("coin")[col].transform("mean")
        G = G.dropna(subset=["lvr", "ex", "r1", "tr60"])
        G["trend"] = np.where(G["tr60"] > 0.1, "rising", np.where(G["tr60"] < -0.1, "falling", "choppy"))
        G["ag"] = np.where(G["agp"] > 0.5, "agit", np.where(G["agp"].notna(), "calm", "na"))
        G["sgn"] = np.where(G["r1"] < 0, "down", "up")
        out = []
        for k, g in G.groupby(["sgn", "trend", "ag"]):
            b, t, n = slope(g, "lvr", "ex")
            mu, tm, _ = ct(g["ex"], g["day"])
            out.append({"grp": str(k), "slope_logvr%": round(b * 100, 3), "t_slope": round(t, 2), "mean%": round(mu * 100, 3), "t_mean": round(tm, 2), "n": n})
        res[f"h{h} slope of ex on log volratio by sign x trend x agit"] = pd.DataFrame(out)
        out = []
        for k, g in G.groupby(["sgn", "trend"]):
            b, t, n = slope(g, "lvr", "ex")
            out.append({"grp": str(k), "slope%": round(b * 100, 3), "t": round(t, 2), "n": n})
        res[f"h{h} slope by sign x trend"] = pd.DataFrame(out)
        if h == 2:
            R = G[(G.sgn == "down") & (G.trend == "rising")].copy()
            R["vq"] = pd.qcut(R["lvr"], 4, labels=False)
            out = []
            for k, g in R.groupby("vq"):
                mu, t, n = ct(g["ex"], g["day"]); out.append({"vq": k, "mean%": round(mu*100, 3), "t": round(t, 2), "n": n})
            res["rising down days ex2 by volume quartile"] = pd.DataFrame(out)
            out = []
            for k, g in R.assign(year=R.ts.dt.year).groupby("year"):
                b, t, n = slope(g, "lvr", "ex"); out.append({"year": k, "slope%": round(b*100, 3), "t": round(t, 2), "n": n})
            res["rising down days slope by year"] = pd.DataFrame(out)
            out = []
            for k, g in R.groupby("coin"):
                b, t, n = slope(g, "lvr", "ex"); out.append({"coin": k, "slope%": round(b*100, 3), "t": round(t, 2), "n": n})
            res["rising down days slope by coin"] = pd.DataFrame(out)
            # down-day fall size x volume, all trends
            Dn = G[G.sgn == "down"].copy()
            Dn["prod"] = Dn["lvr"] * (-Dn["z"])
            b, t, n = slope(Dn, "lvr", "ex"); res["all down slope lvr"] = f"{b*100:.3f}% t {t:.2f} n {n}"
            b, t, n = slope(Dn.dropna(subset=["z"]), "z", "ex"); res["all down slope z"] = f"{b*100:.3f}% t {t:.2f} n {n}"
            U = G[G.sgn == "up"]
            b, t, n = slope(U, "lvr", "ex"); res["all up slope lvr"] = f"{b*100:.3f}% t {t:.2f} n {n}"
    return res
