def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            sd365 = sd30.rolling(365, min_periods=120)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "s3": (c / c.shift(3) - 1) / (sd30 * np.sqrt(3)),
                "s7": (c / c.shift(7) - 1) / (sd30 * np.sqrt(7)),
                "s14": (c / c.shift(14) - 1) / (sd30 * np.sqrt(14)),
                "r60": c / c.shift(60) - 1,
                "inprof": (b["regime"] == "unknown"),
                "yr": ts.dt.year, "day": ts.dt.floor("D")})
            for h in (1, 3, 7):
                df["f%d" % h] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def clslope(g, x, y):
        g = g.dropna(subset=[x, y])
        if len(g) < 30: return pd.Series({"n": len(g), "days": g.day.nunique(), "slope": np.nan, "t": np.nan})
        X = g[x].values; Y = g[y].values
        Xc = X - X.mean(); b = (Xc * (Y - Y.mean())).sum() / (Xc ** 2).sum()
        e = Y - Y.mean() - b * Xc
        s = pd.Series(Xc * e).groupby(g["day"].values).sum()
        G = len(s); se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (Xc ** 2).sum()
        return pd.Series({"n": len(g), "days": G, "slope": b, "t": b / se})
    res = {}
    for h in (3, 7):
        G = A[A.pos % h == 0].copy()
        G["ex"] = G["f%d" % h] - G.coin.map(G.groupby("coin")["f%d" % h].mean())
        G["trend"] = np.where(G.r60 > 0.1, "rising", np.where(G.r60 < -0.1, "falling", "choppy"))
        G.loc[G.r60.isna(), "trend"] = np.nan
        for s in ("s3", "s7", "s14"):
            res[("all", h, s)] = clslope(G, s, "ex")
            res[("fallcalm", h, s)] = clslope(G[G.inprof], s, "ex")
            res[("fallcalm_rises", h, s)] = clslope(G[G.inprof & (G[s] > 0)], s, "ex")
            res[("fallcalm_falls", h, s)] = clslope(G[G.inprof & (G[s] < 0)], s, "ex")
            for tr in ("rising", "choppy", "falling"):
                res[(tr, h, s)] = clslope(G[G.trend == tr], s, "ex")
            res[("rising_rises", h, s)] = clslope(G[(G.trend == "rising") & (G[s] > 0)], s, "ex")
            res[("notprof", h, s)] = clslope(G[~G.inprof], s, "ex")
        if h == 3:
            out["fallcalm s7 slope by year"] = G[G.inprof].groupby("yr").apply(lambda g: clslope(g, "s7", "ex"))
            out["rising s7 slope by year"] = G[G.trend == "rising"].groupby("yr").apply(lambda g: clslope(g, "s7", "ex"))
            out["fallcalm s7 slope by coin"] = G[G.inprof].groupby("coin").apply(lambda g: clslope(g, "s7", "ex"))
    out["slopes"] = pd.DataFrame(res).T
    return out
