def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            c = d["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20, min_periods=20).std()
            d["z"] = r / sd20
            for h in [1, 2, 3, 5]:
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["ret5"] = c / c.shift(5) - 1
            d["ret5z"] = d["ret5"] / (sd20 * np.sqrt(5))
            d["ret10z"] = (c / c.shift(10) - 1) / (sd20 * np.sqrt(10))
            d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
            d["coin"] = coin; d["win"] = w; d["pos"] = np.arange(len(d))
            ts = pd.to_datetime(d["timestamp"])
            d["day"] = ts.dt.floor("D"); d["yr"] = ts.dt.year
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 2, 3, 5]:
        dr = A[A["pos"] % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(dr)
    def ct(g, col):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series({"n": len(g), "days": 0, "mean": np.nan, "t_day": np.nan})
        m = g[col].mean()
        s = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((s**2).sum()) / len(g)
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean": m, "t_day": m / se})
    out = {}
    for h in [2, 3, 5]:
        G = A[(A["pos"] % h == 0) & A.inprof].dropna(subset=["ret5z", f"u{h}"]).copy()
        G["b"] = pd.cut(G["ret5z"], [-99, -1.5, -0.75, 0, 0.75, 1.5, 99])
        out[f"in prof ret5z bins u{h}"] = G.groupby("b").apply(lambda g: ct(g, f"u{h}")).round(5)
        G["sgn"] = np.sign(G["ret5z"])
        out[f"in prof by sign u{h}"] = G.groupby("sgn").apply(lambda g: ct(g, f"u{h}")).round(5)
        G["mom"] = G[f"u{h}"] * G["sgn"]
        out[f"in prof mom by year u{h}"] = G.groupby("yr").apply(lambda g: ct(g, "mom")).round(5)
        out[f"in prof mom by coin u{h}"] = G.groupby("coin").apply(lambda g: ct(g, "mom")).round(5)
        out[f"in prof corr ret5z,u{h}"] = float(G[["ret5z", f"u{h}"]].corr().iloc[0, 1])
    G = A[(A["pos"] % 3 == 0) & A.inprof].dropna(subset=["ret10z", "u3"]).copy()
    G["b"] = pd.qcut(G["ret10z"], 5, labels=False)
    out["in prof ret10z quintile u3"] = G.groupby("b").apply(lambda g: ct(g, "u3")).round(5)
    return out
