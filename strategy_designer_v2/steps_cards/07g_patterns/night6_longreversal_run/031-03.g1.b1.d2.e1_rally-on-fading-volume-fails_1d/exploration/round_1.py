def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows14 = []; rows3 = []; rows7 = []
    drift = {}
    for coin, ws in bars.items():
        allr = {h: [] for h in (3, 7, 14)}
        for w, b in ws.items():
            c = b["close"].values
            for h in (3, 7, 14):
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(allr[h]) if allr[h] else np.nan for h in allr}
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            f = pd.DataFrame({
                "ret14z": (c / c.shift(14) - 1) / (vol20 * np.sqrt(14)),
                "ret28z": (c / c.shift(28) - 1) / (vol20 * np.sqrt(28)),
                "ret56z": (c / c.shift(56) - 1) / (vol20 * np.sqrt(56)),
                "vr": v.rolling(14).mean() / v.rolling(30).mean() - 1,
                "vol20": vol20,
                "r1z": r1 / vol20.shift(1),
                "r3z": (c / c.shift(3) - 1) / (vol20 * np.sqrt(3)),
                "dist_hi": c / c.rolling(30, min_periods=20).max() - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            for h, store in ((14, rows14), (7, rows7), (3, rows3)):
                idx = np.arange(0, len(c) - h, h)
                fw = c.values[idx + h] / c.values[idx] - 1
                g = f.iloc[idx].copy()
                g["ex"] = fw - drift[coin][h]
                g["usual"] = np.nan
                g["coin"] = coin; g["w"] = w
                store.append(g)
    out = {}
    def tab(df, col, q=5):
        d = df.dropna(subset=[col, "ex"]).copy()
        d["bin"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        r = d.groupby("bin").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"))
        r["t"] = r["mean_ex"] / (r["sd"] / np.sqrt(r["n"]))
        rho = stats.spearmanr(d[col], d["ex"])
        r.loc["spearman"] = [np.nan, np.nan, len(d), rho.correlation, np.nan, rho.correlation * np.sqrt(len(d))]
        return r.round(4)
    d14 = pd.concat(rows14); d7 = pd.concat(rows7); d3 = pd.concat(rows3)
    for col in ["ret14z", "ret28z", "ret56z", "vr", "vol20", "dist_hi"]:
        out["h14 by " + col] = tab(d14, col)
    for col in ["r1z", "r3z", "ret14z", "vol20"]:
        out["h3 by " + col] = tab(d3, col)
    out["h7 by ret28z"] = tab(d7, "ret28z")
    # book
    days = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w; days.append(dd)
    D = pd.concat(days)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday; D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book by year"] = D.groupby("year")[["book_return", "coin_return"]].mean().round(5)
    out["coin ret by weekday"] = D.groupby("wd")["coin_return"].agg(["mean", "std", "size"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["size"]))).round(5)
    return out
