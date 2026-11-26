import pandas as pd, numpy as np

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True).copy()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["loc"] = 2 * (b["close"] - b["low"]) / rng - 1
            b["ret"] = b["close"].pct_change()
            b["next"] = b["close"].shift(-1) / b["close"] - 1
            b["next2"] = b["close"].shift(-2) / b["close"] - 1
            b["ret60"] = b["close"] / b["close"].shift(60) - 1
            b["body"] = (b["close"] - b["open"]) / rng
            b["wick_lo"] = (np.minimum(b["open"], b["close"]) - b["low"]) / rng
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["coin"] = coin; b["win"] = w
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["next"].mean(); sd = d.groupby("coin")["next"].std()
    d["ex"] = d["next"] - d["coin"].map(mu)
    d["z"] = d["ex"] / d["coin"].map(sd)
    d["inprof"] = d["regime"].isin(["mean_reversion", "unknown"])
    d["trend"] = np.where(d["ret60"] < -0.1, "falling", np.where(d["ret60"] > 0.1, "rising", np.where(d["ret60"].notna(), "choppy", "na")))
    def ct(x, col="ex"):
        x = x.dropna(subset=[col])
        if len(x) < 3: return pd.Series({"n": len(x), "days": 0, "mean": np.nan, "t": np.nan})
        g = x.groupby("day")[col].sum(); n = len(g)
        m = x[col].mean()
        se = np.sqrt((g - g.mean()).pow(2).sum() * n / (n - 1)) / len(x) if n > 1 else np.nan
        return pd.Series({"n": len(x), "days": n, "mean": m, "t": m / se})
    out = {}
    d["down"] = d["ret"] < 0
    d["locq"] = pd.cut(d["loc"], [-1.01, -0.33, 0.33, 1.01])
    out["down x loc3 excess (day-clustered)"] = d.groupby(["down", "locq"], observed=True).apply(ct)
    dn = d[d.down]
    out["down days: excess by loc3 x coin"] = dn.groupby(["coin", "locq"], observed=True).apply(ct)
    out["down days: excess by loc3 x year"] = dn.groupby(["yr", "locq"], observed=True).apply(ct)
    out["down days: excess by loc3 x trend"] = dn.groupby(["trend", "locq"], observed=True).apply(ct)
    out["down days: excess by loc3 x inprofile"] = dn.groupby(["inprof", "locq"], observed=True).apply(ct)
    # graded: down days, correlation of loc with next excess
    x = dn.dropna(subset=["ex", "loc"])
    out["down days: corr(loc, next z), spearman"] = float(x["loc"].corr(x["z"], method="spearman"))
    x = dn.dropna(subset=["ex", "wick_lo"])
    out["down days: corr(lower wick share, next z)"] = float(x["wick_lo"].corr(x["z"], method="spearman"))
    # 2-day horizon non-overlapping not needed for 1d; check next2 on grid
    d["pos"] = d.groupby(["coin", "win"]).cumcount()
    g2 = d[(d.pos % 2 == 0) & d.down].copy()
    g2["ex2"] = g2["next2"] - g2["coin"].map(d.groupby("coin")["next2"].mean())
    out["down days 2d excess by loc3 (grid 2)"] = g2.groupby("locq", observed=True).apply(lambda x: ct(x, "ex2"))
    # big down day rebound by trend
    d["r1q"] = d.groupby("coin")["ret"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["lowest return quintile by trend"] = d[d.r1q == 0].groupby("trend").apply(ct)
    out["lowest return quintile by inprofile"] = d[d.r1q == 0].groupby("inprof").apply(ct)
    return out
