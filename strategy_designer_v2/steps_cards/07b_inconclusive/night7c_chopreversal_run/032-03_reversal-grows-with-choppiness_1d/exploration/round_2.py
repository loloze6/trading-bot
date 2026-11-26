def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values.astype(float))
            n = len(c)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            mv7 = c / c.shift(7) - 1
            sc = mv7 / (sd30 * np.sqrt(7))
            for H in (7, 14):
                for p in range(0, n - H, H):
                    if p < 30: continue
                    rows.append(dict(H=H, coin=coin, w=w, day=str(b["timestamp"].iloc[p])[:10],
                                     fr=c[p + H] / c[p] - 1, chop=1 - er.iloc[p], sc=sc.iloc[p],
                                     usual=sd30.iloc[p] * np.sqrt(H)))
    d = pd.DataFrame(rows).dropna()
    d["ex"] = d["fr"] - d.groupby(["H", "coin"])["fr"].transform("mean")
    d["exs"] = d["ex"] / d["usual"]
    d["x"] = d["sc"] * d["chop"]  # continuation signal, choppiness-weighted
    out = {}
    def clus(g, x, y="ex"):
        g = g.dropna(subset=[x, y])
        if len(g) < 20: return pd.Series(dict(n=len(g), days=np.nan, slope=np.nan, t=np.nan))
        X = g[x].values - g[x].mean(); Y = g[y].values - g[y].mean()
        bta = (X * Y).sum() / (X * X).sum()
        e = Y - bta * X
        s = pd.Series(X * e).groupby(g["day"].values).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / (X * X).sum()
        return pd.Series(dict(n=len(g), days=G, slope=bta, t=bta / se))
    for H in (7, 14):
        g = d[d.H == H]
        out[f"h{H}_sc"] = clus(g, "sc")
        out[f"h{H}_x"] = clus(g, "x")
        out[f"h{H}_x_scaled_y"] = clus(g, "x", "exs")
        # interaction: sc*chop beyond sc
        r = np.linalg.lstsq(np.column_stack([np.ones(len(g)), g["sc"], g["chop"], g["x"]]), g["ex"], rcond=None)[0]
        out[f"h{H}_interaction_coefs"] = pd.Series(r, index=["c", "sc", "chop", "sc_x_chop"])
        out[f"h{H}_x_by_window"] = g.groupby("w").apply(lambda q: clus(q, "x"))
        out[f"h{H}_x_by_coin"] = g.groupby("coin").apply(lambda q: clus(q, "x"))
        out[f"h{H}_x_by_side"] = g.groupby(np.sign(g["sc"])).apply(lambda q: clus(q, "x"))
        g2 = g.copy(); g2["xq"] = pd.qcut(g2["x"], 5, labels=False)
        out[f"h{H}_x_quintiles"] = g2.groupby("xq").agg(n=("ex", "size"), x=("x", "mean"), ex=("ex", "mean"), exs=("exs", "mean"))
    return out
