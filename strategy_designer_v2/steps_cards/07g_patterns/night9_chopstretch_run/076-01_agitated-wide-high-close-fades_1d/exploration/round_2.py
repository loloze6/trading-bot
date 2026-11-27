def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            h, l, c, o = b["high"], b["low"], b["close"], b["open"]
            rng = (h - l)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "rm": rng / rng.rolling(20).mean(),
                "cl": (c - l) / rng.replace(0, np.nan),
                "r0": c / c.shift(1) - 1,
                "tr60": c / c.shift(60) - 1,
                "tr30": c / c.shift(30) - 1,
                "nxt": c.shift(-1) / c - 1,
                "agit": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"],
                "alloc": b["postRebalance_current_allocation"],
            })
            df["vol20"] = df["r0"].rolling(20).std()
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["u"] = d["nxt"] - d["coin"].map(drift)
    d["r0z"] = d["r0"] / d["vol20"]

    def tstat(sub, col="u"):
        sub = sub.dropna(subset=[col])
        if len(sub) < 10:
            return pd.Series({"n": len(sub), "days": np.nan, "mean": np.nan, "t": np.nan})
        m = sub[col].mean()
        dev = (sub[col] - m).groupby(sub["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev**2).sum() * D / (D - 1)) / len(sub)
        return pd.Series({"n": len(sub), "days": D, "mean": m, "t": m / se})

    out = {}
    d["trend"] = np.where(d.tr60 > .1, "rising", np.where(d.tr60 < -.1, "falling", "choppy"))
    d.loc[d.tr60.isna(), "trend"] = "na"
    d["trend30"] = np.where(d.tr30 > .1, "rising", np.where(d.tr30 < -.1, "falling", "choppy"))
    d.loc[d.tr30.isna(), "trend30"] = "na"
    # up days in falling agitated: grade by r0z
    fa = d[(d.agit == 1) & (d.trend == "falling")].copy()
    fa["r0b"] = pd.cut(fa.r0z, [-99, -1.5, -0.5, 0, 0.5, 1.5, 99])
    out["fall_agit_r0z"] = fa.groupby("r0b").apply(tstat)
    fa30 = d[(d.agit == 1) & (d.trend30 == "falling")].copy()
    fa30["r0b"] = pd.cut(fa30.r0z, [-99, -1.5, -0.5, 0, 0.5, 1.5, 99])
    out["fall30_agit_r0z"] = fa30.groupby("r0b").apply(tstat)
    # up days in falling agitated by year
    fu = fa[fa.r0z > 0.5]
    out["fall_agit_up_by_year"] = fu.groupby("yr").apply(tstat)
    out["fall_agit_up_by_coin"] = fu.groupby("coin").apply(tstat)
    # regression: u on r0z within falling agitated up days
    x = fu.dropna(subset=["u", "r0z"])
    out["fall_agit_up_corr"] = pd.Series({"corr_r0z_u": x.u.corr(x.r0z), "n": len(x)})
    # very wide high close agit by trend30
    a = d[(d.agit == 1)].copy()
    a["wh"] = (a.rm >= 1.7) & (a.cl >= 0.8)
    out["vwide_high_by_trend30"] = a[a.wh].groupby("trend30").apply(tstat)
    out["vwide_high_by_year"] = a[a.wh].groupby("yr").apply(tstat)
    # wide low close agit by trend30 (held family check)
    a["wl"] = (a.rm >= 1.2) & (a.cl <= 0.2)
    out["wide_low_by_trend30"] = a[a.wl].groupby("trend30").apply(tstat)
    # choppy agitated by cl
    ca = d[(d.agit == 1) & (d.trend30 == "choppy")].copy()
    ca["clb"] = pd.cut(ca.cl, [0, .33, .67, 1.0001], include_lowest=True)
    out["choppy_agit_cl"] = ca.groupby("clb").apply(tstat)
    # book: forecast deciles -> realised
    p = d[d.fc < 0].copy()
    p["fq"] = pd.qcut(p.fc.rank(method="first"), 4, labels=["most_neg", "q2", "q3", "least_neg"])
    out["fc_quart"] = p.groupby("fq").apply(tstat)
    return out
