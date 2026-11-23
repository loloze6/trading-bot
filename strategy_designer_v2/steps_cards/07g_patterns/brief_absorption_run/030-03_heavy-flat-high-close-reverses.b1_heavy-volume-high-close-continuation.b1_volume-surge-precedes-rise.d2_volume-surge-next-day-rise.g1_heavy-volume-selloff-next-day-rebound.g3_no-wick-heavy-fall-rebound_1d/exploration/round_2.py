def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            v = b["volume"].astype(float)
            d = pd.DataFrame({"ret1": c / c.shift(1) - 1})
            d["ret3p"] = c / c.shift(3) - 1
            d["ret5p"] = c / c.shift(5) - 1
            d["ret10p"] = c / c.shift(10) - 1
            d["vr"] = v / v.shift(1).rolling(20, min_periods=20).mean()
            rng = (h - l).replace(0, np.nan)
            d["fall_left"] = (h - c) / rng
            r = c.pct_change()
            d["vol20"] = r.rolling(20, min_periods=20).std()
            d["n1"] = c.shift(-1) / c - 1
            d["n3"] = c.shift(-3) / c - 1
            d["pos"] = np.arange(len(b))
            d["fc"] = b["forecast"].astype(float)
            d["year"] = pd.to_datetime(b["timestamp"]).dt.year
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu = D.groupby("coin")["n1"].transform("mean")
    D["x1"] = D["n1"] - mu
    D["x3"] = D["n3"] - 3 * mu
    D["z3"] = D["ret3p"] / (D["vol20"] * np.sqrt(3))
    D["z1"] = D["ret1"] / D["vol20"]
    def summ(g, col="x1"):
        s = g[col].dropna(); n = len(s)
        return pd.Series({"n": n, "mean%": s.mean() * 100 if n else np.nan,
                          "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    dh = D[(D.ret1 < 0) & (D.vr >= 1)].copy()
    dh["r1t"] = pd.qcut(dh["ret1"], 3, labels=False)
    dh["flt"] = pd.qcut(dh["fall_left"], 3, labels=False)
    out["downheavy_ret1tercile_x_fallleft_tercile"] = dh.groupby(["r1t", "flt"]).apply(summ)
    # all days: prior 3d move scaled by vol, quintiles, heavy vs not
    a = D.dropna(subset=["z3", "vr"]).copy()
    a["z3q"] = pd.qcut(a["z3"], 5, labels=False)
    a["heavy"] = a.vr >= 1
    out["all_next1_by_z3q_x_heavy"] = a.groupby(["z3q", "heavy"]).apply(summ)
    # non-overlapping 3-day grid: z3 quintile on 3-day excess
    g3 = a[a.pos % 3 == 0].copy()
    g3["z3q"] = pd.qcut(g3["z3"], 5, labels=False)
    out["grid3_next3_by_z3q_x_heavy"] = g3.groupby(["z3q", "heavy"]).apply(lambda g: summ(g, "x3"))
    # bottom z3 quintile & heavy: by coin and by year
    sel = a[(a.z3q == 0) & a.heavy]
    out["lowz3_heavy_by_coin"] = sel.groupby("coin").apply(summ)
    out["lowz3_heavy_by_year"] = sel.groupby("year").apply(summ)
    # prior 5d and 10d on heavy days
    for col in ["ret5p", "ret10p"]:
        b2 = D[D.vr >= 1].dropna(subset=[col, "vol20"]).copy()
        b2["q"] = pd.qcut(b2[col] / b2["vol20"], 5, labels=False)
        out[f"heavy_next1_by_{col}_vol_q"] = b2.groupby("q").apply(summ)
    # volume ratio grading within bottom z3 quintile
    s2 = a[a.z3q == 0].copy()
    s2["vq"] = pd.qcut(s2["vr"], 4, labels=False)
    out["lowz3_next1_by_vr_quartile"] = s2.groupby("vq").apply(summ)
    # forecast quintile grading
    f = D[D.fc > 0].copy()
    f["fq"] = pd.qcut(f["fc"].rank(method="first"), 5, labels=False)
    out["signal_next1_by_forecast_q"] = f.groupby("fq").apply(summ)
    return out
