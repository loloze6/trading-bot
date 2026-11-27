def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            r = c.pct_change()
            rng = (h - l) / c.shift(1)
            w20 = rng / rng.rolling(20, min_periods=10).mean()
            clv = (c - l) / (h - l).replace(0, np.nan)
            ret60 = c / c.shift(60) - 1
            ret5 = c / c.shift(5) - 1
            sd20 = r.rolling(20, min_periods=10).std()
            df = pd.DataFrame({"coin": coin, "win": w, "ts": b["timestamp"], "r": r,
                               "nxt": c.shift(-1) / c - 1, "nxt3": c.shift(-3) / c - 1,
                               "w20": w20, "clv": clv, "ret60": ret60, "ret5": ret5, "z": r / sd20,
                               "regime": b["regime"], "pos": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["drift"] = d["coin"].map(d.groupby("coin")["r"].mean())
    d["u1"] = d["nxt"] - d["drift"]
    d["u3"] = d["nxt3"] - 3 * d["drift"]
    d["falling"] = d["regime"].isin(["trending", "unknown"])
    d["trend"] = np.where(d["falling"], "falling", np.where(d["ret60"] > 0.10, "rising",
                          np.where(d["ret60"].notna(), "choppy", "nf_unknown")))
    d = d.dropna(subset=["r", "w20"])

    def ct(s, days):
        x = pd.DataFrame({"v": s - s.mean(), "d": days}).dropna()
        g = x.groupby("d")["v"].sum(); G = len(g)
        if G < 3: return np.nan
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return s.mean() / se

    def summ(sub, col="u1"):
        sub = sub.dropna(subset=[col])
        return pd.Series({"n": len(sub), "days": sub["day"].nunique(), "mean%": 100 * sub[col].mean(),
                          "t_day": ct(sub[col], sub["day"])})

    out = {}
    d["zq"] = pd.cut(d["z"], [-99, -1.5, -0.5, 0, 0.5, 1.5, 99], labels=False)
    out["next1_by_trend_zbin"] = d.groupby(["trend", "zq"]).apply(summ).reset_index()
    fu = d[d["falling"] & (d["r"] > 0)]
    out["falling_up_by_window"] = fu.groupby("win").apply(summ).reset_index()
    fu = fu.assign(wide=fu["w20"] > fu.groupby("coin")["w20"].transform("median"))
    out["falling_up_wide_by_window"] = fu[fu["wide"]].groupby("win").apply(summ).reset_index()
    fd = d[d["falling"] & (d["r"] < 0)]
    fd = fd.assign(wq=pd.qcut(fd["w20"].rank(method="first"), 4, labels=False))
    out["falling_down_widthQ4_u1_u3"] = pd.concat({"u1": fd.groupby("wq").apply(summ),
                                                  "u3": fd.groupby("wq").apply(lambda s: summ(s, "u3"))}, axis=1)
    mid = d[d["falling"] & (d["z"].abs() < 0.5)]
    out["falling_flat_by_window"] = mid.groupby("win").apply(summ).reset_index()
    out["falling_flat_by_ret5sign"] = mid.groupby(mid["ret5"] < 0).apply(summ).reset_index()
    # leave one window out for falling up days
    lo = {}
    for w in fu["win"].unique():
        s = fu[fu["win"] != w]
        lo[w] = ct(s["u1"].dropna(), s.dropna(subset=["u1"])["day"])
    out["falling_up_t_leave_one_window_out"] = pd.Series(lo)
    return out
