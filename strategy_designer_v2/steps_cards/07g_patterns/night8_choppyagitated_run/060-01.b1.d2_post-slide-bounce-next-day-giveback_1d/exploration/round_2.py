import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            rng = (b["high"] - b["low"]).astype(float)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r": r, "z": r / sd, "sd": sd,
                "tr60": c / c.shift(60) - 1,
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "regime": b["regime"].values,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "clpos": (c - b["low"]) / rng.replace(0, np.nan),
                "rngz": (rng / c) / sd,
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby("coin")["f1"].mean()
    A["d1"] = A["f1"] - A["coin"].map(drift)
    A["d2"] = A["f2"] - 2 * A["coin"].map(drift)
    A["prof"] = np.where(A["regime"] == "chop", "out", "in")

    def ct(s, col):
        s = s.dropna(subset=[col])
        if len(s) < 10:
            return pd.Series({"n": len(s), "days": np.nan, "mean": np.nan, "t_day": np.nan})
        m = s[col].mean()
        gd = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((gd ** 2).sum()) / len(s)
        return pd.Series({"n": len(s), "days": s["day"].nunique(), "mean": m, "t_day": m / se})

    def slope(s, x, y):
        s = s.dropna(subset=[x, y])
        X = s[x] - s[x].mean(); Y = s[y] - s[y].mean()
        b = (X * Y).sum() / (X ** 2).sum()
        e = Y - b * X
        g = (X * e).groupby(s["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / (X ** 2).sum()
        return pd.Series({"n": len(s), "days": s["day"].nunique(), "slope": b, "t": b / se})

    out = {}
    inn = A[A["prof"] == "in"]
    out["in_slope_d1_on_z_all"] = slope(inn, "z", "d1").round(5)
    out["in_slope_d1_on_z_down"] = slope(inn[inn["z"] < 0], "z", "d1").round(5)
    out["in_slope_d1_on_z_up"] = slope(inn[inn["z"] > 0], "z", "d1").round(5)
    out["in_slope_d1_on_clpos"] = slope(inn, "clpos", "d1").round(5)
    # up days by close position
    up = inn[inn["z"] > 0].copy()
    up["cb"] = pd.cut(up["clpos"], [0, 0.5, 0.8, 1.0001], include_lowest=True)
    out["in_up_by_closepos"] = up.groupby("cb", observed=True).apply(lambda s: ct(s, "d1")).round(4)
    out["in_up_slope_d1_on_clpos"] = slope(up, "clpos", "d1").round(5)
    # 2-day grid on up days
    g2 = inn[(inn["pos"] % 2 == 0) & (inn["z"] > 0)].copy()
    g2["zb"] = pd.cut(g2["z"], [0, 0.5, 1, np.inf])
    out["in_up_next2_grid"] = g2.groupby("zb", observed=True).apply(lambda s: ct(s, "d2")).round(4)
    # out of profile by 60d trend (computable part)
    o = A[(A["prof"] == "out") & A["tr60"].notna()].copy()
    o["trend"] = np.where(o["tr60"] > 0.1, "rising", np.where(o["tr60"] < -0.1, "falling", "choppy"))
    o["zb"] = pd.cut(o["z"], [-np.inf, -1, 0, 1, np.inf])
    out["out_by_trend_z"] = o.groupby(["trend", "zb"], observed=True).apply(lambda s: ct(s, "d1")).round(4)
    out["out_slope_by_trend"] = o.groupby("trend").apply(lambda s: slope(s, "z", "d1")).round(5)
    out["out_slope_clpos_by_trend"] = o.groupby("trend").apply(lambda s: slope(s, "clpos", "d1")).round(5)
    # book's largest days context
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    bd = D.groupby("day")["book_return"].mean()
    q = bd.quantile([0.02, 0.98])
    out["book_extreme_days"] = pd.Series({"n_days": len(bd), "top2pct_sum": bd[bd >= q[0.98]].sum(),
                                         "bottom2pct_sum": bd[bd <= q[0.02]].sum(), "total_sum": bd.sum()}).round(5)
    return out
