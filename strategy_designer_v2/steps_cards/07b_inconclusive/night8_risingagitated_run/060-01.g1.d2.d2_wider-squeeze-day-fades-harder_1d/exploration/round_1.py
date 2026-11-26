def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    drift = {}
    for coin, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            c = b["close"].astype(float).values
            allr.append(c[1:] / c[:-1] - 1)
        drift[coin] = np.concatenate(allr).mean()
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = h - l
            cl = (c - l) / rng.replace(0, np.nan)
            ratio = rng / rng.rolling(20, min_periods=20).mean()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            nxt3 = c.shift(-3) / c - 1
            ret5 = c / c.shift(5) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "regime": b["regime"], "fc": b["forecast"].astype(float),
                               "cl": cl, "ratio": ratio, "u1": -(nxt - drift[coin]),
                               "u2": -(nxt2 - 2 * drift[coin]), "u3": -(nxt3 - 3 * drift[coin]),
                               "ret5": ret5, "dayret": c / c.shift(1) - 1})
            rows.append(df)
    d = pd.concat(rows)
    def summ(g, col="u1"):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series({"n": len(g)})
        s = g.groupby("day")[col].agg(["sum", "count"])
        m = g[col].mean()
        dev = g[col] - m
        ds = dev.groupby(g["day"]).sum()
        G = len(ds)
        se = np.sqrt((ds ** 2).sum() * G / max(G - 1, 1)) / len(g)
        return pd.Series({"n": len(g), "days": G, "mean": m, "t": m / se if se > 0 else np.nan})
    inprof = d[d["regime"].isin(["mean_reversion", "unknown"])].copy()
    cases = d[d["fc"] < 0].copy()
    out = {}
    out["regime counts"] = d["regime"].value_counts()
    out["cases all"] = summ(cases)
    out["cases u2 u3"] = pd.DataFrame({"u2": summ(cases, "u2"), "u3": summ(cases, "u3")})
    out["by coin"] = cases.groupby("coin").apply(summ).round(4)
    out["by year"] = cases.groupby("year").apply(summ).round(4)
    out["by window"] = cases.groupby("win").apply(summ).round(4)
    inprof["clbin"] = pd.cut(inprof["cl"], [-0.01, 0.25, 0.5, 0.75, 0.9, 1.01])
    out["in profile by close location"] = inprof.groupby("clbin").apply(summ).round(4)
    cases["fq"] = pd.qcut(cases["fc"].abs().rank(method="first"), 4, labels=False)
    out["cases by |forecast| quartile"] = cases.groupby("fq").apply(summ).round(4)
    cases["rq"] = pd.qcut(cases["ratio"].rank(method="first"), 4, labels=False)
    out["cases by raw range ratio quartile"] = cases.groupby("rq").apply(summ).round(4)
    cases["clq"] = pd.cut(cases["cl"], [0.5, 0.75, 0.9, 1.01])
    out["cases by close location"] = cases.groupby("clq").apply(summ).round(4)
    cases["dsign"] = np.where(cases["dayret"] > 0, "up day", "down day")
    out["cases by day sign"] = cases.groupby("dsign").apply(summ).round(4)
    cases["r5"] = np.where(cases["ret5"] > 0, "5d up", "5d down")
    out["cases by 5d return sign"] = cases.groupby("r5").apply(summ).round(4)
    out["corr ratio vs u1"] = float(cases[["ratio", "u1"]].corr().iloc[0, 1])
    out["corr cl vs u1"] = float(cases[["cl", "u1"]].corr().iloc[0, 1])
    return out
