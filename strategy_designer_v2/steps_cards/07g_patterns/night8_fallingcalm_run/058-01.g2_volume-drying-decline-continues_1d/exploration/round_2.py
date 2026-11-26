def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            f5 = c.shift(-5) / c - 1
            p60 = c / c.shift(60) - 1
            p30 = c / c.shift(30) - 1
            vr = np.log(v.rolling(30).mean() / v.rolling(30).mean().shift(30))
            ts = pd.to_datetime(b["timestamp"])
            trend = np.where(p60 > 0.1, "rising", np.where(p60 < -0.1, "falling", np.where(p60.isna(), "na", "choppy")))
            idx = np.arange(0, len(b), 5)
            rows.append(pd.DataFrame({"coin": coin, "w": w, "f5": f5.iloc[idx].values, "vr": vr.iloc[idx].values,
                "p30": p30.iloc[idx].values, "trend": trend[idx], "yr": ts.iloc[idx].dt.year.values,
                "day": ts.iloc[idx].dt.floor("D").values}))
            pos = b["postRebalance_current_allocation"].astype(float)
            daily.append(pd.DataFrame({"coin": coin, "w": w, "r1n": r1.shift(-1).values, "r1": r1.values,
                "wd": ts.dt.weekday.values, "trend": trend, "yr": ts.dt.year.values, "day": ts.dt.floor("D").values,
                "pos": pos.values, "gain": (pos * r1.shift(-1)).values}))
    G = pd.concat(rows).dropna(subset=["f5"]); D = pd.concat(daily).dropna(subset=["r1n"])
    G["u"] = G["f5"] - G["f5"].mean()
    mu = D["r1n"].mean(); D["un"] = D["r1n"] - mu
    def ct(g, col):
        s = g.groupby("day")[col].sum(); n = g[col].count(); m = g[col].mean()
        G_ = len(s); se = np.sqrt((s - m * g.groupby("day")[col].count()).pow(2).sum() * G_ / (G_ - 1)) / n
        return pd.Series({"n": n, "days": G_, "mean": m, "t_day": m / se})
    out = {}
    D["late"] = D["wd"].isin([3, 4])
    out["late_vs_rest_by_trend"] = D.groupby(["trend", "late"]).apply(lambda g: ct(g, "un"))
    out["late_by_year"] = D[D["late"]].groupby("yr").apply(lambda g: ct(g, "un"))
    out["rest_by_year"] = D[~D["late"]].groupby("yr").apply(lambda g: ct(g, "un"))
    out["late_by_coin"] = D[D["late"]].groupby("coin").apply(lambda g: ct(g, "un"))
    out["wd_falling"] = D[D["trend"] == "falling"].groupby("wd").apply(lambda g: ct(g, "un"))
    # volume shrink continuation by trend, graded
    g = G.dropna(subset=["vr"]).copy()
    res = {}
    for tr in ["rising", "falling", "choppy"]:
        h = g[g["trend"] == tr]
        res[tr] = pd.Series({"n": len(h), "rho_vr_u": stats.spearmanr(h["vr"], h["u"])[0],
                             "rho_p30_u": stats.spearmanr(h["p30"], h["u"])[0] if h["p30"].notna().sum() > 10 else np.nan})
    out["rho_by_trend"] = pd.DataFrame(res).T
    # rising: signed move = u * sign(p30) when vr<0 (shrinking volume continuation of 30d direction)
    g["cont"] = g["u"] * np.sign(g["p30"])
    g["shrink"] = -g["vr"]
    for tr in ["rising", "falling", "choppy"]:
        h = g[(g["trend"] == tr) & (g["vr"] < 0)].dropna(subset=["cont"])
        out["cont_shrink_" + tr] = ct(h, "cont")
        h2 = g[(g["trend"] == tr) & (g["vr"] >= 0)].dropna(subset=["cont"])
        out["cont_grow_" + tr] = ct(h2, "cont")
    # book: short position days, gain vs prior day coin return
    S = D[D["pos"] < 0].copy()
    S["q"] = pd.qcut(S["r1"], 5, labels=False)
    out["short_gain_by_prior_r1"] = S.groupby("q").agg(n=("gain", "count"), r1=("r1", "mean"), gain=("gain", "mean"), nextret=("r1n", "mean"))
    out["short_by_wd"] = S.groupby("wd").agg(n=("gain", "count"), gain=("gain", "mean"), nextret=("r1n", "mean"))
    return out
