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
            z5 = r5 / (sd20 * np.sqrt(5))
            z20 = r20 / (sd20 * np.sqrt(20))
            f5 = c.shift(-5) / c - 1
            f10 = c.shift(-10) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                                      "year": ts.dt.year, "regime": b["regime"], "z5": z5, "z20": z20,
                                      "r20": r20, "r60": r60, "f5": f5, "f10": f10}))
    d = pd.concat(rows, ignore_index=True)

    def ct(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 5: return pd.Series({"n": len(x), "days": 0, "mean": np.nan, "t": np.nan})
        m = x[col].mean()
        s = (x[col] - m).groupby(x["day"]).sum()
        D = len(s)
        se = np.sqrt((s**2).sum() * D / max(D - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "days": D, "mean": m, "t": m / se if se > 0 else np.nan})

    def slope(x, xc, yc):
        x = x.dropna(subset=[xc, yc])
        if len(x) < 10: return pd.Series({"n": len(x), "slope": np.nan, "t": np.nan})
        X = x[xc] - x[xc].mean(); y = x[yc]
        b = (X * y).sum() / (X**2).sum()
        e = y - y.mean() - b * X
        s = (X * e).groupby(x["day"]).sum(); D = len(s)
        se = np.sqrt((s**2).sum() * D / max(D - 1, 1)) / (X**2).sum()
        return pd.Series({"n": len(x), "slope": b, "t": b / se})

    out = {}
    for h, col, dc in [(5, "f5", "u5"), (10, "f10", "u10")]:
        g = d[d.pos % h == 0].copy()
        g[dc] = g[col] - g["coin"].map(g.groupby("coin")[col].mean())
        g["prof"] = np.where(g.regime == "chop", "outside_choppy", "choppy")
        g["trend"] = pd.cut(g["r60"], [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])
        # choppy profile: graded by z20
        ch = g[g.prof == "choppy"].copy()
        ch["z20b"] = pd.cut(ch["z20"], [-np.inf, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, np.inf])
        out[f"{dc} choppy-profile by z20 bin"] = ch.groupby("z20b", observed=True).apply(lambda x: ct(x, dc)).round(4)
        out[f"{dc} choppy-profile slope on z20 / r20"] = pd.DataFrame({"z20": slope(ch, "z20", dc), "r20": slope(ch, "r20", dc)}).T.round(4)
        out[f"{dc} choppy r20<0 by window"] = ch[ch.r20 < 0].groupby("w").apply(lambda x: ct(x, dc)).round(4)
        # outside choppy (known trend): z5 grading by trend side
        tr = g[g.trend.notna()].copy()
        tr["z5b"] = pd.cut(tr["z5"], [-np.inf, -1, 0, 1, 2, np.inf])
        out[f"{dc} by r60 trend x z5 bin"] = tr.groupby(["trend", "z5b"], observed=True).apply(lambda x: ct(x, dc)).round(4)
        oc = g[g.prof == "outside_choppy"]
        out[f"{dc} outside-choppy slope on z5"] = slope(oc, "z5", dc).round(5)
        out[f"{dc} outside-choppy z5>1 by year"] = oc[oc.z5 > 1].groupby("year").apply(lambda x: ct(x, dc)).round(4)
    return out
