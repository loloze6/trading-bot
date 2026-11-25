import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                                      "year": ts.dt.year, "regime": b["regime"],
                                      "z5": r5 / (sd20 * np.sqrt(5)), "z20": r20 / (sd20 * np.sqrt(20)),
                                      "z10": (c / c.shift(10) - 1) / (sd20 * np.sqrt(10)),
                                      "r60": r60, "f5": c.shift(-5) / c - 1, "f10": c.shift(-10) / c - 1}))
    d = pd.concat(rows, ignore_index=True)

    def ct(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 5: return pd.Series({"n": len(x), "days": 0, "mean": np.nan, "t": np.nan})
        m = x[col].mean(); s = (x[col] - m).groupby(x["day"]).sum(); D = len(s)
        se = np.sqrt((s**2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean": m, "t": m / se if se > 0 else np.nan})

    def slope(x, xc, yc):
        x = x.dropna(subset=[xc, yc])
        if len(x) < 10: return pd.Series({"n": len(x), "slope": np.nan, "t": np.nan})
        X = x[xc] - x[xc].mean(); y = x[yc]
        b = (X * y).sum() / (X**2).sum(); e = y - y.mean() - b * X
        s = (X * e).groupby(x["day"]).sum(); D = len(s)
        se = np.sqrt((s**2).sum() * D / max(D - 1, 1)) / (X**2).sum()
        return pd.Series({"n": len(x), "slope": b, "t": b / se})

    out = {}
    for h, col, dc in [(5, "f5", "u5"), (10, "f10", "u10")]:
        g = d[d.pos % h == 0].copy()
        g[dc] = g[col] - g["coin"].map(g.groupby("coin")[col].mean())
        g["trend"] = pd.cut(g["r60"], [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])
        ch = g[g.trend == "choppy"]
        out[f"{dc} choppy slopes"] = pd.DataFrame({k: slope(ch, k, dc) for k in ["z5", "z10", "z20"]}).T.round(4)
        out[f"{dc} choppy z20<0 slope (falls only)"] = slope(ch[ch.z20 < 0], "z20", dc).round(4)
        out[f"{dc} choppy z20 slope by year"] = ch.groupby("year").apply(lambda x: slope(x, "z20", dc)).round(4)
        out[f"{dc} choppy z20<0 by year"] = ch[ch.z20 < 0].groupby("year").apply(lambda x: ct(x, dc)).round(4)
        ri = g[g.trend == "rising"]
        out[f"{dc} rising slopes"] = pd.DataFrame({k: slope(ri, k, dc) for k in ["z5", "z10", "z20"]}).T.round(4)
        out[f"{dc} rising z5 slope by year"] = ri.groupby("year").apply(lambda x: slope(x, "z5", dc)).round(4)
        fa = g[g.trend == "falling"]
        out[f"{dc} falling slopes"] = pd.DataFrame({k: slope(fa, k, dc) for k in ["z5", "z10", "z20"]}).T.round(4)
    return out
