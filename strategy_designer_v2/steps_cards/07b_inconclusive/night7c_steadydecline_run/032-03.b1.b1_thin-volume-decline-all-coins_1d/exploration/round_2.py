def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for H in [5, 10]:
            g = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    g.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(g) if g else np.nan
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ret28 = pd.Series(c).pct_change(28).values
            rng = ((df["high"] - df["low"]) / df["close"]).values
            rng28 = pd.Series(rng).rolling(28).mean().values
            rngall = pd.Series(rng).expanding(40).mean().values
            dret = pd.Series(c).pct_change()
            maxdrop28 = dret.rolling(28).min().values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").astype("int64").values
            for i in range(0, n, 5):
                f = df["forecast"].iloc[i]
                r = {"coin": coin, "w": w, "day": day[i], "f": f,
                     "trend": df["regime"].iloc[i] == "trending",
                     "ret28": ret28[i], "rngrel": rng28[i] / rngall[i],
                     "maxdrop": maxdrop28[i],
                     "raw": df.get("debug_info.components.rel_volume.last_history_value", pd.Series([np.nan]*n)).iloc[i]}
                for H in [5, 10]:
                    r[f"x{H}"] = (c[i + H] / c[i] - 1 - drift[(coin, H)]) if i + H < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)

    def clslope(sub, x, y):
        s = sub[[x, y, "day"]].dropna()
        if len(s) < 20:
            return pd.Series({"n": len(s), "days": np.nan, "slope": np.nan, "t": np.nan})
        X = s[x] - s[x].mean(); Y = s[y] - s[y].mean()
        b = (X * Y).sum() / (X * X).sum()
        e = Y - b * X
        sc = (X * e).groupby(s["day"]).sum()
        G = len(sc)
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (X * X).sum()
        return pd.Series({"n": len(s), "days": G, "slope": b, "t": b / se})

    def clmean(s, y):
        s = s[[y, "day"]].dropna()
        if len(s) < 5:
            return pd.Series({"n": len(s), "mean": np.nan, "t": np.nan})
        m = s[y].mean()
        dv = (s[y] - m).groupby(s["day"]).sum()
        G = len(dv)
        se = np.sqrt((dv ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean": m, "t": m / se})

    out = {}
    d["down"] = d["ret28"] < 0
    out["x5_down_vs_up"] = d.groupby("down").apply(lambda s: clmean(s, "x5"))
    out["x10_down_vs_up"] = d.groupby("down").apply(lambda s: clmean(s, "x10"))
    dn = d[d["down"]].copy()
    dn["calm"] = dn["rngrel"] < 1.0
    out["x5_down_by_calm"] = dn.groupby("calm").apply(lambda s: clmean(s, "x5"))
    out["x10_down_by_calm"] = dn.groupby("calm").apply(lambda s: clmean(s, "x10"))
    dn["mdq"] = pd.qcut(dn["maxdrop"], 3, labels=False)
    out["x5_down_by_maxdrop_tercile"] = dn.groupby("mdq").apply(lambda s: pd.concat([clmean(s, "x5"), pd.Series({"md": s.maxdrop.mean()})]))
    out["slope_x5_on_ret28_by_calm"] = dn.groupby("calm").apply(lambda s: clslope(s, "ret28", "x5"))
    out["slope_x10_on_ret28_by_calm"] = dn.groupby("calm").apply(lambda s: clslope(s, "ret28", "x10"))
    out["slope_x5_on_f_by_calm"] = dn.groupby("calm").apply(lambda s: clslope(s, "f", "x5"))
    out["slope_x5_on_rngrel_down"] = clslope(dn, "rngrel", "x5")
    out["slope_x10_on_rngrel_down"] = clslope(dn, "rngrel", "x10")
    out["slope_x5_on_maxdrop_down"] = clslope(dn, "maxdrop", "x5")
    out["slope_x10_on_maxdrop_down"] = clslope(dn, "maxdrop", "x10")
    dn["rq"] = pd.qcut(dn["rngrel"], 4, labels=False)
    out["x5_down_by_rngrel_q"] = dn.groupby("rq").apply(lambda s: pd.concat([clmean(s, "x5"), pd.Series({"rr": s.rngrel.mean()})]))
    out["x10_down_by_rngrel_q"] = dn.groupby("rq").apply(lambda s: clmean(s, "x10"))
    dn["year"] = pd.to_datetime(dn["day"]).dt.year
    out["x5_down_calm_by_year"] = dn[dn.calm].groupby("year").apply(lambda s: clmean(s, "x5"))
    out["side_slopes"] = pd.DataFrame({"thin": clslope(dn[dn.f < 0], "f", "x5"), "heavy": clslope(dn[dn.f > 0], "f", "x5")}).T
    return out
