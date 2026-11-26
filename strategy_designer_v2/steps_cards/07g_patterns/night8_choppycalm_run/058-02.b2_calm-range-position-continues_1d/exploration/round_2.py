def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; hi = b["high"].rolling(20).max(); lo = b["low"].rolling(20).min()
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)),
                "day": ts.dt.floor("D"), "pos": 2 * (c - lo) / (hi - lo) - 1,
                "fwd": c.shift(-H) / c - 1, "ret60": c / c.shift(60) - 1,
                "vr": r1.rolling(30).std() / r1.rolling(60).std(), "ret20": c / c.shift(20) - 1,
                "inprof": (b["regime"] == "unknown").astype(int), "year": ts.dt.year}))
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.i % H == 0].groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[A.i % H == 0].dropna(subset=["ex", "pos", "ret60", "vr"]).copy()
    G["trend"] = pd.cut(G["ret60"], [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    G["agit"] = np.where(G["vr"] > 1.0, "agit", "calm")
    G["side"] = np.sign(G["pos"])
    def clus(df, col="ex"):
        d = df.groupby("day")[col].agg(["sum", "size"])
        m = df[col].mean()
        dev = df[col] - m
        s = dev.groupby(df["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / len(df)
        return pd.Series({"n": len(df), "days": len(d), "mean%": m * 100, "t_day": m / se if se > 0 else np.nan})
    def cslope(df):
        if len(df) < 30: return pd.Series({"n": len(df), "slope%": np.nan, "t_day": np.nan})
        x = df["pos"] - df["pos"].mean(); y = df["ex"] - df["ex"].mean()
        bta = (x * y).sum() / (x ** 2).sum()
        e = y - bta * x
        s = (x * e).groupby(df["day"]).sum()
        se = np.sqrt((s ** 2).sum()) / (x ** 2).sum()
        return pd.Series({"n": len(df), "days": df["day"].nunique(), "slope%": bta * 100, "t_day": bta / se})
    out = {}
    out["slope trend x agit (clustered)"] = G.groupby(["trend", "agit"]).apply(cslope).round(3)
    out["side mean trend x agit (signed ex: long top/short bottom)"] = G.assign(sx=G["ex"] * G["side"]).groupby(["trend", "agit"]).apply(lambda d: clus(d, "sx")).round(3)
    out["chop agit bottom/top bins"] = G[(G.trend == "chop") & (G.agit == "agit")].assign(pq=pd.cut(G["pos"], [-1.01, -0.5, 0, 0.5, 1.01])).groupby("pq").apply(clus).round(3)
    out["fall calm bins"] = G[(G.trend == "fall") & (G.agit == "calm")].assign(pq=pd.cut(G["pos"], [-1.01, -0.5, 0, 0.5, 1.01])).groupby("pq").apply(clus).round(3)
    out["slope by year all"] = G.groupby("year").apply(cslope).round(3)
    out["slope all"] = cslope(G).round(3)
    out["slope ret20 all"] = cslope(G.assign(pos=G["ret20"]).dropna(subset=["pos"])).round(3)
    return out
