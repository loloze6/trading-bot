import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin in bars:
        drift = {}
        frames = []
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r = c.pct_change()
            ma = r.abs().shift(1).rolling(720, min_periods=120).mean()
            z = -r / ma
            vr = v / v.shift(1).rolling(720, min_periods=120).mean()
            ts = pd.to_datetime(df["timestamp"])
            d = pd.DataFrame({"z": z, "vr": vr, "year": ts.dt.year, "w": w,
                              "cell": np.arange(len(df)) // 6})
            for h in [6]:
                d[f"f{h}"] = c.shift(-h) / c - 1
                drift.setdefault(h, []).append((c.iloc[::h].shift(-1) / c.iloc[::h] - 1).dropna())
            d["r7"] = c / c.shift(168) - 1
            d["r3"] = c / c.shift(72) - 1
            d["r30"] = c / c.shift(720) - 1
            frames.append(d)
        D = pd.concat(frames, ignore_index=True)
        D["u6"] = D["f6"] - pd.concat(drift[6]).mean()
        D["coin"] = coin
        rows.append(D)
    D = pd.concat(rows, ignore_index=True)
    D = D[(D["z"] >= 0.5) & (D["vr"] >= 0.667) & (D["vr"] <= 1.5)].copy()
    D = D.drop_duplicates(["coin", "w", "cell"])
    D["zb"] = pd.cut(D["z"], [0.5, 1, 2, 3, 1e9], labels=["0.5-1", "1-2", "2-3", "3+"])
    def st(g, col="u6"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    D["t7"] = np.where(D["r7"] > 0, "up7", "down7")
    D["t3"] = np.where(D["r3"] > 0, "up3", "down3")
    D["t30"] = np.where(D["r30"] > 0, "up30", "down30")
    out["t7 x zb"] = D.groupby(["t7", "zb"], observed=True).apply(st).round(3)
    out["t7 x coin"] = D.groupby(["t7", "coin"]).apply(st).round(3)
    out["t7 x year"] = D.groupby(["t7", "year"]).apply(st).round(3)
    out["t3"] = D.groupby("t3").apply(st).round(3)
    out["t30"] = D.groupby("t30").apply(st).round(3)
    U = D[D["t7"] == "up7"].copy()
    U["r7q"] = pd.qcut(U["r7"], 4, labels=["q1", "q2", "q3", "q4"])
    out["up7 by r7 quartile"] = U.groupby("r7q", observed=True).apply(st).round(3)
    U["zq"] = pd.qcut(U["z"], 4, labels=["q1", "q2", "q3", "q4"])
    out["up7 by fall quartile"] = U.groupby("zq", observed=True).apply(st).round(3)
    return out
