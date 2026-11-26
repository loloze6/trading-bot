def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for H in [1, 3, 5, 10, 20]:
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
            rng118 = pd.Series(rng).rolling(118).mean().values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").astype("int64").values
            for i in range(0, n, 5):
                if df["regime"].iloc[i] != "trending":
                    continue
                f = df["forecast"].iloc[i]
                if pd.isna(f) or f == 0:
                    continue
                r = {"coin": coin, "w": w, "day": day[i], "f": f,
                     "ret28": ret28[i], "rngrel": rng28[i] / rng118[i] if rng118[i] == rng118[i] else np.nan,
                     "year": pd.to_datetime(df["timestamp"].iloc[i]).year}
                for H in [1, 3, 5, 10, 20]:
                    r[f"x{H}"] = (c[i + H] / c[i] - 1 - drift[(coin, H)]) if i + H < n else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)

    def clslope(sub, x, y):
        s = sub[[x, y, "day"]].dropna()
        if len(s) < 20:
            return pd.Series({"n": len(s), "slope": np.nan, "t": np.nan})
        X = s[x] - s[x].mean(); Y = s[y] - s[y].mean()
        b = (X * Y).sum() / (X * X).sum()
        e = Y - b * X
        sc = (X * e).groupby(s["day"]).sum()
        G = len(sc)
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (X * X).sum()
        return pd.Series({"n": len(s), "days": G, "slope": b, "t": b / se})

    def clmean(s, y):
        s = s[[y, "day"]].dropna()
        m = s[y].mean()
        dv = (s[y] - m).groupby(s["day"]).sum()
        G = len(dv)
        se = np.sqrt((dv ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"n": len(s), "mean": m, "t": m / se})

    out = {}
    out["slope_by_horizon"] = pd.DataFrame({H: clslope(d, "f", f"x{H}") for H in [1, 3, 5, 10, 20]}).T
    d["fq"] = pd.qcut(d["f"], 5, labels=False)
    out["x5_by_fq"] = d.groupby("fq").apply(lambda s: pd.concat([clmean(s, "x5"), pd.Series({"fmean": s.f.mean()})]))
    out["x10_by_fq"] = d.groupby("fq").apply(lambda s: clmean(s, "x10"))
    d["dq"] = pd.qcut(d["ret28"], 4, labels=False)
    out["x5_by_depth_q"] = d.groupby("dq").apply(lambda s: pd.concat([clmean(s, "x5"), pd.Series({"r28": s.ret28.mean()})]))
    out["slope_f_by_depth_q"] = d.groupby("dq").apply(lambda s: clslope(s, "f", "x5"))
    out["slope_on_ret28"] = pd.DataFrame({H: clslope(d, "ret28", f"x{H}") for H in [5, 10, 20]}).T
    d["calm"] = d["rngrel"] < d["rngrel"].median()
    out["slope_f_by_calm"] = d.groupby("calm").apply(lambda s: clslope(s, "f", "x5"))
    out["slope_r28_by_calm"] = d.groupby("calm").apply(lambda s: clslope(s, "ret28", "x5"))
    out["slope_f_by_year"] = d.groupby("year").apply(lambda s: clslope(s, "f", "x5"))
    out["slope_f_by_coin"] = d.groupby("coin").apply(lambda s: clslope(s, "f", "x5"))
    out["slope_f_by_window"] = d.groupby("w").apply(lambda s: clslope(s, "f", "x5"))
    return out
