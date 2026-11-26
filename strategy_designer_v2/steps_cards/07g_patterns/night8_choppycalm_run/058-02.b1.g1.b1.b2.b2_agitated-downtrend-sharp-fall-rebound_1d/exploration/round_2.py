def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            allr.append(b["close"].astype(float).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=20).std()
            rng = (b["high"] - b["low"]).astype(float)
            clv = (c - b["low"]) / rng.replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            ar = rng / c.shift(1) / sd
            df = pd.DataFrame({"coin": coin, "w": w, "day": ts.dt.floor("D"), "yr": ts.dt.year,
                               "z": r / sd, "clv": clv, "ar": ar, "x1": c.shift(-1) / c - 1 - mu,
                               "x2": c.shift(-2) / c - 1 - 2 * mu,
                               "fa": (b["regime"] == "unknown").astype(int),
                               "tr60": c / c.shift(60) - 1})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)

    def slope_t(sub, xcol, ycol="x1"):
        s = sub.dropna(subset=[xcol, ycol])
        if len(s) < 30: return pd.Series({"n": len(s), "slope": np.nan, "t_day": np.nan})
        x = s[xcol].values - s[xcol].mean(); y = s[ycol].values - s[ycol].mean()
        bta = (x * y).sum() / (x * x).sum()
        e = y - bta * x
        g = pd.Series(x * e).groupby(s["day"].values).sum()
        se = np.sqrt((g ** 2).sum()) / (x * x).sum()
        return pd.Series({"n": len(s), "slope": bta, "t_day": bta / se})

    res = {}
    fa = d[d.fa == 1]; out = d[d.fa == 0]
    up = fa[fa.z > 0]
    res["FA_up_days_x1_on_z"] = slope_t(up, "z").to_frame().T
    res["FA_up_days_x1_on_clv"] = slope_t(up, "clv").to_frame().T
    res["FA_all_x1_on_clv"] = slope_t(fa, "clv").to_frame().T
    res["OUT_all_x1_on_clv"] = slope_t(out, "clv").to_frame().T
    res["FA_up_by_window"] = up.groupby("w").apply(lambda g: slope_t(g, "z")).reset_index()
    res["FA_up_mean_by_window"] = up.groupby("w")["x1"].agg(["count", "mean"]).reset_index()
    out = out.copy()
    out["trb"] = pd.cut(out["tr60"], [-9, -0.1, 0.1, 99]).astype(str)
    res["OUT_clv_slope_by_trend"] = out.groupby("trb").apply(lambda g: slope_t(g, "clv")).reset_index()
    res["OUT_clv_slope_by_window"] = out.groupby("w").apply(lambda g: slope_t(g, "clv")).reset_index()
    ri = out[out.trb == "(0.1, 99.0]"]
    res["RISING_x1_on_z_up"] = slope_t(ri[ri.z > 0], "z").to_frame().T
    res["RISING_x1_on_z_down"] = slope_t(ri[ri.z < 0], "z").to_frame().T
    res["FA_x2_on_clv"] = slope_t(fa, "clv", "x2").to_frame().T
    return res
