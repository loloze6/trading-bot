def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 10: continue
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l).replace(0, np.nan)
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "cl": (c - l) / rng,
                "ret1": c.pct_change(),
                "tr60": c / c.shift(60) - 1,
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "agit": (b["regime"] != "chop").astype(int),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            })
            df["vol20"] = df["ret1"].rolling(20, min_periods=10).std()
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(drift)
    A["x1n"] = A["x1"] / A["vol20"]
    A["low"] = 1 - A["cl"]  # 1 at the low
    A["fallz"] = -A["ret1"] / A["vol20"]

    def tday(g, col):
        g = g.dropna(subset=[col]); n = len(g)
        if n < 10: return np.nan, n
        m = g[col].mean()
        d = g.groupby("day")[col].apply(lambda s: (s - m).sum())
        se = np.sqrt((d**2).sum() * len(d) / (len(d) - 1)) / n
        return m / se, n

    def slope(g, xcol, ycol="x1n"):
        g = g.dropna(subset=[xcol, ycol]); n = len(g)
        if n < 30: return pd.Series({"n": n})
        x = g[xcol] - g[xcol].mean(); y = g[ycol] - g[ycol].mean()
        b = (x * y).sum() / (x * x).sum()
        e = y - b * x
        d = (x * e).groupby(g["day"]).sum()
        se = np.sqrt((d**2).sum() * len(d) / (len(d) - 1)) / (x * x).sum()
        return pd.Series({"n": n, "slope": b, "t_day": b / se})

    out = {}
    out["slope_low_by_agit"] = A.groupby("agit").apply(lambda g: slope(g, "low")).round(3)
    out["slope_fallz_by_agit"] = A.groupby("agit").apply(lambda g: slope(g, "fallz")).round(3)
    Ag = A[A.agit == 1]
    out["agit_slope_low_by_year"] = Ag.groupby("yr").apply(lambda g: slope(g, "low")).round(3)
    out["agit_slope_low_by_coin"] = Ag.groupby("coin").apply(lambda g: slope(g, "low")).round(3)
    out["agit_slope_fallz_by_year"] = Ag.groupby("yr").apply(lambda g: slope(g, "fallz")).round(3)
    out["agit_slope_fallz_by_coin"] = Ag.groupby("coin").apply(lambda g: slope(g, "fallz")).round(3)
    # downside only: low close on down days, graded by fall size
    D = Ag[Ag.ret1 < 0].copy()
    D["fq"] = pd.qcut(D["fallz"], 4, labels=False)
    res = []
    for q, g in D.groupby("fq"):
        t, n = tday(g, "x1"); res.append({"fq": q, "n": n, "mean%": 100*g["x1"].mean(), "t_day": t,
                                          "fallz_mean": g["fallz"].mean()})
    out["agit_downdays_by_fallsize"] = pd.DataFrame(res).set_index("fq").round(3)
    # trend within agitated
    Ag2 = Ag.dropna(subset=["tr60"]).copy()
    Ag2["trend"] = np.where(Ag2.tr60 > 0.10, "rising", np.where(Ag2.tr60 < -0.10, "falling", "choppy"))
    out["agit_slope_low_by_trend"] = Ag2.groupby("trend").apply(lambda g: slope(g, "low")).round(3)
    out["agit_slope_fallz_by_trend"] = Ag2.groupby("trend").apply(lambda g: slope(g, "fallz")).round(3)
    # day-2 persistence: return from day1 close to day2 close
    A["x2b"] = (A["f2"] - A["f1"]) / (1 + A["f1"]) - A["coin"].map(drift)
    A["x2bn"] = A["x2b"] / A["vol20"]
    out["agit_slope_low_day2"] = A[A.agit == 1].pipe(lambda g: slope(g, "low", "x2bn")).round(3)
    # combined: low close x fall size
    Ag3 = Ag.copy(); Ag3["combo"] = Ag3["low"] * Ag3["fallz"].clip(lower=0)
    out["agit_slope_combo"] = slope(Ag3, "combo").round(3)
    out["calm_slope_combo"] = slope(A[A.agit == 0].assign(combo=lambda d: d["low"] * d["fallz"].clip(lower=0)), "combo").round(3)
    return out
