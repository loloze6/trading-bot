def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            allr.append(pd.Series(b["close"].astype(float).values).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            r = c.pct_change()
            hi20 = h.shift(1).rolling(20).max(); lo20 = l.shift(1).rolling(20).min()
            vol30 = r.rolling(30).std()
            df = pd.DataFrame({
                "coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                "dhi": (c / hi20 - 1) * 100, "dlo": (c / lo20 - 1) * 100,
                "dhiz": (c / hi20 - 1) / vol30,
                "tr60": (c / c.shift(60) - 1) * 100,
                "vr": vol30.rolling(120, min_periods=60).rank(pct=True),
                "pos": np.arange(len(b)), "mu": mu,
            })
            for H in [1, 3, 5, 10]:
                df["x%d" % H] = c.shift(-H) / c - 1 - H * mu
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    D["trend"] = np.where(D["tr60"] > 10, "rising", np.where(D["tr60"] < -10, "falling", np.where(D["tr60"].notna(), "choppy", None)))
    D["yr"] = D["ts"].dt.year

    def tday(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 3: return pd.Series({"n": len(s), "days": 0, "mean": np.nan, "t": np.nan})
        g = s[col].groupby(s["day"]).sum()
        t = g.mean() / (g.std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan
        return pd.Series({"n": len(s), "days": len(g), "mean": s[col].mean(), "t": t})

    out = {}
    # non-overlapping grid per horizon
    res = {}
    for H in [3, 5, 10]:
        G = D[D["pos"] % H == 0]
        for tr in ["rising", "choppy", "falling"]:
            res[("up", tr, H)] = tday(G[(G["dhi"] > 0) & (G["trend"] == tr)], "x%d" % H)
            res[("dn", tr, H)] = tday(G[(G["dlo"] < 0) & (G["trend"] == tr)], "x%d" % H)
    out["breaks nonoverlap by trend & horizon"] = pd.DataFrame(res).T.round(4)
    # rising up-break graded by size (all bars, x5) and nonoverlap
    R = D[(D["dhi"] > 0) & (D["trend"] == "rising")].copy()
    R["q"] = pd.qcut(R["dhiz"], 3, labels=["small", "mid", "large"])
    out["rising up-break x5 by size (all bars)"] = pd.DataFrame({k: tday(g, "x5") for k, g in R.groupby("q")}).T.round(4)
    G5 = R[R["pos"] % 5 == 0]
    out["rising up-break x5 by size (grid)"] = pd.DataFrame({k: tday(g, "x5") for k, g in G5.groupby("q")}).T.round(4)
    # slope of x5 on dhiz, rising, grid
    s = G5.dropna(subset=["x5", "dhiz"])
    sl = np.polyfit(s["dhiz"], s["x5"], 1)[0] if len(s) > 5 else np.nan
    out["slope x5 on dhiz rising grid"] = float(sl)
    # all rising bars graded by distance to high (incl. below)
    RA = D[(D["trend"] == "rising") & (D["pos"] % 5 == 0)].dropna(subset=["dhiz", "x5"]).copy()
    RA["b"] = pd.cut(RA["dhiz"], [-99, -6, -3, -1.5, -0.5, 0, 0.5, 1, 99])
    out["rising: x5 by dist to 20d high (vol units, grid)"] = pd.DataFrame({str(k): tday(g, "x5") for k, g in RA.groupby("b")}).T.round(4)
    # by year, by agitation, by coin
    out["rising up-break x5 by year"] = pd.DataFrame({k: tday(g, "x5") for k, g in R.groupby("yr")}).T.round(4)
    R["ag"] = np.where(R["vr"] > 0.5, "agitated", np.where(R["vr"].notna(), "calm", None))
    out["rising up-break x5 by agitation"] = pd.DataFrame({k: tday(g, "x5") for k, g in R.groupby("ag")}).T.round(4)
    out["rising up-break x5 by coin"] = pd.DataFrame({k: tday(g, "x5") for k, g in R.groupby("coin")}).T.round(4)
    # baseline: rising bars not breaking
    out["rising no-break x5 (grid)"] = tday(D[(D["trend"] == "rising") & (D["dhi"] <= 0) & (D["pos"] % 5 == 0)], "x5").round(4)
    return out
