def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30p = r.rolling(30, min_periods=20).std().shift(1)
            sd30 = r.rolling(30, min_periods=20).std()
            z = r / sd30p
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z, "sd30": sd30,
                               "tr60": c / c.shift(60) - 1, "tr20": c / c.shift(20) - 1,
                               "day": ts.dt.floor("D"), "yr": ts.dt.year})
            for h in (3, 5, 10):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["sdmed"] = D.groupby("coin")["sd30"].transform("median")
    D["agit"] = np.where(D["sd30"] > D["sdmed"], "agit", "calm")
    D["trend"] = pd.cut(D["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    out = {}

    def grid(h):
        g = D[(D["pos"] % h) == 0].dropna(subset=[f"f{h}"]).copy()
        g["ex"] = g[f"f{h}"] - g.groupby("coin")[f"f{h}"].transform("mean")
        return g

    def ct(x):
        # clustered by day
        dsum = x.groupby("day")["ex"].sum()
        n = len(x); G = len(dsum); m = x["ex"].mean()
        dev = (x["ex"] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / n if G > 1 else np.nan
        return pd.Series({"n": n, "days": G, "mean%": 100 * m, "t": m / se if se and se > 0 else np.nan})

    zb = [-np.inf, -2, -1, -0.5, 0.5, 1, np.inf]
    for h in (3, 5, 10):
        g = grid(h).dropna(subset=["trend"])
        g["zb"] = pd.cut(g["z"], zb)
        f = g[g["trend"] == "fall"]
        out[f"fall z bins fwd{h}"] = f.groupby("zb", observed=True).apply(ct)
        out[f"fall agit x z fwd{h}"] = f.groupby(["agit", "zb"], observed=True).apply(ct)
    g = grid(5).dropna(subset=["trend"])
    f = g[(g["trend"] == "fall") & (g["z"] <= -1)]
    out["fall z<=-1 fwd5 by year"] = f.groupby("yr").apply(ct)
    out["fall z<=-1 fwd5 by window"] = f.groupby("w").apply(ct)
    out["fall z<=-1 fwd5 by coin"] = f.groupby("coin").apply(ct)
    # graded slope within falling: ex on z
    ff = g[g["trend"] == "fall"].dropna(subset=["z"])
    out["fall slope ex on z (fwd5)"] = float(np.polyfit(ff["z"], ff["ex"], 1)[0])
    out["fall corr z ex (fwd5)"] = float(ff[["z", "ex"]].corr().iloc[0, 1])
    # momentum tr20 by trend, fwd10
    g = grid(10).dropna(subset=["trend", "tr20"])
    g["q"] = g.groupby("trend", observed=True)["tr20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["tr20 tercile x trend fwd10"] = g.groupby(["trend", "q"], observed=True).apply(ct)
    return out
