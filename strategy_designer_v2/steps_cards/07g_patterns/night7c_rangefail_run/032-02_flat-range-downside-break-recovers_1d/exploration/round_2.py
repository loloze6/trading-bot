def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            r = c.pct_change()
            f = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(df)),
                              "day": pd.to_datetime(df["timestamp"]).dt.floor("D"),
                              "year": pd.to_datetime(df["timestamp"]).dt.year})
            hi20 = h.shift(1).rolling(20).max(); lo20 = l.shift(1).rolling(20).min()
            hi60 = h.shift(1).rolling(60, min_periods=40).max(); lo60 = l.shift(1).rolling(60, min_periods=40).min()
            f["above20"] = (c / hi20 - 1)
            f["below20"] = (c / lo20 - 1)
            f["above60"] = (c / hi60 - 1)
            f["below60"] = (c / lo60 - 1)
            f["er60"] = (c - c.shift(60)).abs() / c.diff().abs().rolling(60, min_periods=40).sum()
            f["vol20"] = r.rolling(20).std()
            f["above20n"] = f["above20"] / f["vol20"]
            for H in (5, 10):
                f[f"fwd{H}"] = c.shift(-H) / c - 1
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def clt(s, col="ex"):
        G = s.groupby("day")[col].sum() - s.groupby("day")[col].count() * s[col].mean()
        n = len(G)
        if n < 3: return np.nan
        se = np.sqrt((G**2).sum() * n / (n - 1)) / len(s)
        return s[col].mean() / se
    def summary(H, cond_col, sign, by=None):
        g = A[A["pos"] % H == 0].dropna(subset=[f"fwd{H}"]).copy()
        g["ex"] = g[f"fwd{H}"] - g.groupby("coin")[f"fwd{H}"].transform("mean")
        s = g[(g[cond_col] * sign) > 0].dropna(subset=["ex"])
        if by is None:
            return {"n": len(s), "days": s["day"].nunique(), "mean_ex%": s["ex"].mean() * 100, "t_cl": clt(s)}
        res = []
        for k, ss in s.groupby(by):
            res.append({by: k, "n": len(ss), "mean_ex%": ss["ex"].mean() * 100, "t_cl": clt(ss)})
        return pd.DataFrame(res).round(3)
    tab = []
    for H in (5, 10):
        for cc, sg in (("above20", 1), ("below20", -1), ("above60", 1), ("below60", -1)):
            d = summary(H, cc, sg); d.update({"H": H, "cond": cc}); tab.append(d)
    out["breaks overall"] = pd.DataFrame(tab).round(3)
    out["above20 H10 by coin"] = summary(10, "above20", 1, "coin")
    out["above20 H10 by window"] = summary(10, "above20", 1, "w")
    out["above20 H10 by year"] = summary(10, "above20", 1, "year")
    # graded inside above-20 breaks: terciles of normalised overshoot, and ER60 terciles
    g = A[A["pos"] % 10 == 0].dropna(subset=["fwd10"]).copy()
    g["ex"] = g["fwd10"] - g.groupby("coin")["fwd10"].transform("mean")
    s = g[g["above20"] > 0].dropna(subset=["above20n", "er60"]).copy()
    s["qd"] = pd.qcut(s["above20n"].rank(method="first"), 3, labels=False)
    s["qe"] = pd.qcut(s["er60"].rank(method="first"), 3, labels=False)
    out["above20 H10 by depth tercile"] = s.groupby("qd").apply(lambda x: pd.Series({"n": len(x), "mean_ex%": x["ex"].mean() * 100, "t_cl": clt(x), "med_depth_vol": x["above20n"].median()})).round(3)
    out["above20 H10 by ER60 tercile"] = s.groupby("qe").apply(lambda x: pd.Series({"n": len(x), "mean_ex%": x["ex"].mean() * 100, "t_cl": clt(x), "med_er": x["er60"].median()})).round(3)
    # below-60 breaks in flat vs trending coins (the brief's situation)
    b = g[g["below60"] < 0].dropna(subset=["er60"]).copy()
    b["flat"] = (b["er60"] <= b["er60"].median()).astype(int)
    out["below60 H10 flat(1) vs not"] = b.groupby("flat").apply(lambda x: pd.Series({"n": len(x), "mean_ex%": x["ex"].mean() * 100, "t_cl": clt(x)})).round(3)
    # all bars grid slope of ex on above20n (ranked) for H5
    return out
