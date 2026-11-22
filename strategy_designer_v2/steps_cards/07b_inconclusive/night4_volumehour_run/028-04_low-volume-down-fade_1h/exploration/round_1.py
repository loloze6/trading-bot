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
            d = pd.DataFrame({"z": z, "vr": vr, "year": ts.dt.year, "hour": ts.dt.hour, "w": w,
                              "cell": np.arange(len(df)) // 6})
            for h in [2, 6, 12, 24]:
                d[f"f{h}"] = c.shift(-h) / c - 1
                drift.setdefault(h, []).append((c.iloc[::h].shift(-1) / c.iloc[::h] - 1).dropna())
            # trailing 7-day return regime
            d["r7"] = c / c.shift(168) - 1
            frames.append(d)
        D = pd.concat(frames, ignore_index=True)
        for h in [2, 6, 12, 24]:
            D[f"u{h}"] = D[f"f{h}"] - pd.concat(drift[h]).mean()
        D["coin"] = coin
        rows.append(D)
    D = pd.concat(rows, ignore_index=True)
    D = D[D["z"] >= 0.5].copy()
    D["vband"] = pd.cut(D["vr"], [0, 0.667, 1.5, 3, 1e9], labels=["low", "mid", "high", "vhigh"])
    D["zb"] = pd.cut(D["z"], [0.5, 1, 2, 3, 1e9], labels=["0.5-1", "1-2", "2-3", "3+"])
    # first per cell per window per coin per vband
    D = D.drop_duplicates(["coin", "w", "cell", "vband"])
    def st(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    tab = []
    for h in [2, 6, 12, 24]:
        s = D.groupby(["vband", "zb"], observed=True).apply(lambda g: st(g, f"u{h}"))
        s["h"] = h
        tab.append(s.reset_index())
    T = pd.concat(tab)
    out["vband x zb x h"] = T[T["h"].isin([6, 24])].round(3)
    M = D[D["vband"] == "mid"]
    out["mid by coin h6"] = M.groupby("coin").apply(lambda g: st(g, "u6")).round(3)
    out["mid by year h6"] = M.groupby("year").apply(lambda g: st(g, "u6")).round(3)
    M = M.copy(); M["r7s"] = np.where(M["r7"] > 0, "up7", "down7")
    out["mid by 7d trend h6/h24"] = pd.concat([M.groupby("r7s").apply(lambda g: st(g, "u6")).add_suffix("_6"),
                                             M.groupby("r7s").apply(lambda g: st(g, "u24")).add_suffix("_24")], axis=1).round(3)
    A = D.copy()
    out["all vol by zb h2"] = A.groupby(["vband", "zb"], observed=True).apply(lambda g: st(g, "u2")).round(3)
    return out
