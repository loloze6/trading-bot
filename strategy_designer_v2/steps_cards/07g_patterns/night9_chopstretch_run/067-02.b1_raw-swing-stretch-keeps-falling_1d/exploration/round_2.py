def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            d["z"] = (c / c.rolling(20).mean() - 1) / sd
            d["ret60"] = c / c.shift(60) - 1
            d["sd30"] = r1.rolling(30).std()
            d["s20"] = (c / c.shift(20) - 1) / (sd * np.sqrt(20))
            d["f10"] = c.shift(-10) / c - 1
            d["f5"] = c.shift(-5) / c - 1
            d["r1"] = r1
            d["f1"] = c.shift(-1) / c - 1
            d["pos"] = np.arange(len(d))
            d["coin"] = coin; d["w"] = w
            d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["choppy"] = (d["regime"] == "unknown").astype(int)
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # agitation: 30d sd vs its past-365 median, per coin within window (approx: within window only)
    A["agit"] = A.groupby(["coin", "w"])["sd30"].transform(lambda s: (s > s.rolling(365, min_periods=60).median()).astype(float).where(s.rolling(365, min_periods=60).median().notna()))
    out = {}
    def clust(df, col):
        s = df.dropna(subset=[col])
        if len(s) < 5: return pd.Series({"n": len(s), "days": 0, "mean": np.nan, "t_day": np.nan})
        m = s[col].mean()
        g = (s[col] - m).groupby(s["day"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean": m, "t_day": m / se})
    for h, col in ((10, "f10"), (5, "f5")):
        g = A[(A["pos"] % h == 0) & A[col].notna()].copy()
        dr = g.groupby("coin")[col].mean()
        g["x"] = g[col] - g["coin"].map(dr)
        g["zq"] = pd.cut(g["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
        out[f"x{h} choppy by agit x z"] = g[g["choppy"] == 1].groupby(["agit", "zq"]).apply(lambda q: clust(q, "x")).round(4)
        if h == 10:
            gc = g[(g["choppy"] == 1) & (g["z"] < 0)]
            out["x10 choppy z<0 by window"] = gc.groupby("w").apply(lambda q: pd.Series({"n": len(q), "mean": q["x"].mean()})).round(4)
            gs = g[(g["choppy"] == 1)].copy()
            gs["sq"] = pd.cut(gs["s20"], [-np.inf, -1, -0.3, 0.3, 1, np.inf])
            out["x10 choppy by s20 x agit"] = gs.groupby(["agit", "sq"]).apply(lambda q: clust(q, "x")).round(4)
            # correlation in choppy of x with s20 (full, both sides)
            q = gs.dropna(subset=["s20", "x"])
            out["corr x10 s20 choppy"] = float(np.corrcoef(q["s20"], q["x"])[0, 1])
            out["corr x10 z choppy"] = float(np.corrcoef(q["z"], q["x"])[0, 1])
            # trending: z>2 split by rising/falling
            gt = g[g["choppy"] == 0].copy()
            gt["tr"] = np.where(gt["ret60"] > 0.1, "rising", np.where(gt["ret60"] < -0.1, "falling", "other"))
            out["x10 trending by trend x z"] = gt.groupby(["tr", "zq"]).apply(lambda q: clust(q, "x")).round(4)
    # weekday by year
    dr1 = A.groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(dr1)
    A["nwd"] = (A["wd"] + 1) % 7
    out["x1 next-day Fri/Sat vs other by year"] = A.dropna(subset=["x1"]).assign(fs=A["nwd"].isin([4, 5]).astype(int)).groupby(["year", "fs"])["x1"].mean().unstack().round(4)
    out["x1 by next weekday clustered"] = A.groupby("nwd").apply(lambda q: clust(q, "x1")).round(4)
    return out
