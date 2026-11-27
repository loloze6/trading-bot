def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).astype(float)
            b["loc"] = np.where(rng > 0, (c - b["low"]) / rng, np.nan)
            b["r1"] = c.pct_change()
            b["r5p"] = c / c.shift(5) - 1
            b["vol20"] = b["r1"].rolling(20).std()
            b["z1"] = b["r1"] / b["vol20"]
            b["z5"] = b["r5p"] / (b["vol20"] * np.sqrt(5))
            b["rngz"] = (rng / c) / ((rng / c).rolling(20).mean())
            for h in (2, 5):
                b[f"f{h}"] = c.shift(-h) / c - 1
            b["inprof"] = b["regime"] != "chop"
            ts = pd.to_datetime(b["timestamp"])
            b["wd"] = ts.dt.weekday
            b["yr"] = ts.dt.year
            b["dkey"] = ts.dt.floor("D")
            b["pos"] = np.arange(len(b))
            b["coin"] = coin; b["win"] = w
            b["volrank"] = b["vol20"].rank(pct=True)
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    def pooled(x, col="u"):
        x = x.dropna(subset=[col])
        if len(x) < 5: return pd.Series({"n": len(x), "days": np.nan, "mean_u": x[col].mean() if len(x) else np.nan, "t_pooled": np.nan})
        m = x[col].mean()
        s = (x[col] - m).groupby(x["dkey"]).sum()
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean_u": m, "t_pooled": m / se if se > 0 else np.nan})
    G = {}
    for h in (2, 5):
        g = d[d["pos"] % h == 0].dropna(subset=[f"f{h}"]).copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["u"] = g[f"f{h}"] - g["coin"].map(drift)
        G[h] = g
    g2 = G[2]; g5 = G[5]
    # Sunday effect robustness
    g2["sun"] = g2["wd"] == 6
    out["h2 sunday vs rest, pooled"] = g2.groupby("sun").apply(pooled)
    out["h2 sunday by year"] = g2[g2["sun"]].groupby("yr").apply(pooled)
    out["h2 sunday by coin"] = g2[g2["sun"]].groupby("coin").apply(pooled)
    # sunday graded by that day's own return?
    s = g2[g2["sun"]].copy()
    s["z1b"] = pd.qcut(s["z1"], 3)
    out["h2 sunday by z1 tercile"] = s.groupby("z1b").apply(pooled)
    # high close in high vol, graded by loc, pooled, and by year
    hv = g2[g2["volrank"] > 0.67].copy()
    hv["locb"] = pd.cut(hv["loc"], [-.01, .25, .5, .75, .9, 1.01])
    out["h2 high-vol by loc, pooled"] = hv.groupby("locb").apply(pooled)
    out["h2 high-vol loc>0.8 by year"] = hv[hv["loc"] > 0.8].groupby("yr").apply(pooled)
    # in-profile, h5, loc grade (no ret5 condition), pooled
    ip = g5[g5["inprof"]].copy()
    ip["locb"] = pd.cut(ip["loc"], [-.01, .5, .8, 1.01])
    out["h5 inprof by loc, pooled"] = ip.groupby("locb").apply(pooled)
    out["h5 inprof loc>0.5 by year"] = ip[ip["loc"] > 0.5].groupby("yr").apply(pooled)
    # big up day continuation h5, pooled by year
    g5["z1b"] = pd.qcut(g5["z1"], 5, labels=False)
    out["h5 top z1 quintile by year"] = g5[g5["z1b"] == 4].groupby("yr").apply(pooled)
    out["h5 z1 quintiles pooled"] = g5.groupby("z1b").apply(pooled)
    # wide range days (rngz) with high close, h5
    g5["rb"] = pd.qcut(g5["rngz"], 3, labels=False)
    out["h5 by rngz tercile x loc>0.8"] = g5.groupby(["rb", g5["loc"] > 0.8]).apply(pooled)
    return out
