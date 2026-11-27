def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = (h - l)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret1": c / c.shift(1) - 1,
                "ret5": c / c.shift(5) - 1,
                "trend60": c / c.shift(60) - 1,
                "wide": rng / rng.rolling(20).mean(),
                "loc": (c - l) / rng.replace(0, np.nan),
                "nxt": c.shift(-1) / c - 1,
                "nxt3": c.shift(-3) / c - 1,
                "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["unx"] = d["nxt"] - d["coin"].map(drift)
    d["trend"] = np.where(d["trend60"] < -0.10, "falling", np.where(d["trend60"] > 0.10, "rising", "choppy"))
    d.loc[d["trend60"].isna(), "trend"] = np.nan
    d["updn"] = np.where(d["ret1"] > 0, "up", "down")
    d["wb"] = pd.cut(d["wide"], [0, 1.0, 1.5, 2.2, 99], labels=["n<1", "1-1.5", "1.5-2.2", ">2.2"])
    d["lb"] = pd.cut(d["loc"], [-0.01, 0.25, 0.75, 1.01], labels=["low", "mid", "high"])
    d["r5"] = np.where(d["ret5"] < 0, "r5neg", "r5pos")

    def summ(g):
        g = g.dropna(subset=["unx"])
        s = g.groupby("day")["unx"].sum()
        n = len(g); nd = len(s)
        if nd < 5:
            return pd.Series({"n": n, "days": nd, "mean%": g["unx"].mean() * 100, "t": np.nan})
        se = np.sqrt((s - s.mean() * 0 - g["unx"].mean() * g.groupby("day").size()).pow(2).sum()) / n
        return pd.Series({"n": n, "days": nd, "mean%": g["unx"].mean() * 100, "t": g["unx"].mean() / se if se > 0 else np.nan})

    dd = d.dropna(subset=["trend"])
    out = {}
    out["trend_updn_width"] = dd.groupby(["trend", "updn", "wb"], observed=True).apply(summ).round(3)
    fu = dd[(dd.trend == "falling") & (dd.updn == "up") & (dd.wide >= 1.5)]
    out["fall_wideup_by_loc_r5"] = fu.groupby(["lb", "r5"], observed=True).apply(summ).round(3)
    wd = d[(d.updn == "down") & (d.wide >= 1.5)]
    out["widedown_by_loc_trend"] = wd.dropna(subset=["trend"]).groupby(["trend", "lb"], observed=True).apply(summ).round(3)
    wu = d[(d.updn == "up") & (d.wide >= 1.5)]
    out["wideup_all_by_loc_trend"] = wu.dropna(subset=["trend"]).groupby(["trend", "lb"], observed=True).apply(summ).round(3)
    out["all_by_weekday"] = d.groupby("wd").apply(summ).round(3)
    # big moves scaled
    d["z"] = d["ret1"] / d.groupby(["coin", "win"])["ret1"].transform(lambda x: x.rolling(20).std().shift(1))
    d["zb"] = pd.cut(d["z"], [-99, -3, -2, -1, 1, 2, 3, 99])
    out["by_z_trend"] = d.dropna(subset=["trend"]).groupby(["trend", "zb"], observed=True).apply(summ).round(3)
    out["by_z_all"] = d.groupby("zb", observed=True).apply(summ).round(3)
    return out
