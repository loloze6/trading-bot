def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H) / c - 1,
                "r30": c / c.shift(30) - 1,
                "r60": c / c.shift(60) - 1,
                "vr30": v.rolling(30).mean() / v.shift(30).rolling(30).mean(),
                "vr10": v.rolling(10).mean() / v.shift(10).rolling(30).mean(),
                "sd30": r1.rolling(30).std(),
                "fallcalm": (b["regime"] != "chop").astype(int),
                "yr": ts.dt.year, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
            })
            rows.append(df[df["pos"] % H == 0])
    g = pd.concat(rows).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["sd365"] = np.nan
    def dayt(sub, col="ex"):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return pd.Series({"n": len(s), "days": 0, "mean": np.nan, "t_day": np.nan})
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["day"]).sum()
        J = len(dev); se = np.sqrt((dev**2).sum() * J / (J - 1)) / len(s)
        return pd.Series({"n": len(s), "days": J, "mean": m, "t_day": m / se})
    out = {}
    neg = g[(g.r30 < 0)].dropna(subset=["vr30"]).copy()
    neg["vq"] = pd.qcut(neg["vr30"], 5, labels=False)
    out["falls_by_vr30_quint"] = neg.groupby("vq").apply(dayt)
    out["falls_vr30_cut_edges"] = pd.Series(pd.qcut(neg["vr30"], 5, retbins=True)[1])
    pos = g[(g.r30 >= 0)].dropna(subset=["vr30"]).copy()
    pos["vq"] = pd.qcut(pos["vr30"], 5, labels=False)
    out["rises_by_vr30_quint"] = pos.groupby("vq").apply(dayt)
    allv = g.dropna(subset=["vr30"]).copy()
    allv["vq"] = pd.qcut(allv["vr30"], 5, labels=False)
    out["all_by_vr30_quint"] = allv.groupby("vq").apply(dayt)
    # falls x volume drop
    neg["fq"] = pd.qcut(neg["r30"], 3, labels=False)
    neg["vq3"] = pd.qcut(neg["vr30"], 3, labels=False)
    out["falls_r30t_x_vr30t_mean"] = neg.groupby(["fq", "vq3"])["ex"].mean().unstack()
    out["falls_r30t_x_vr30t_n"] = neg.groupby(["fq", "vq3"])["ex"].count().unstack()
    # graded score: fall depth times thinness
    neg["score"] = (-neg["r30"]) * (-np.log(neg["vr30"]))
    out["corr_ex_logvr30_falls"] = float(np.corrcoef(np.log(neg["vr30"]), neg["ex"])[0, 1])
    out["corr_ex_logvr30_all"] = float(np.corrcoef(np.log(allv["vr30"]), allv["ex"])[0, 1])
    lowv = neg[neg.vq3 == 0]
    out["falls_lowvol_by_win"] = lowv.groupby("win").apply(dayt)
    out["falls_lowvol_by_year"] = lowv.groupby("yr").apply(dayt)
    out["falls_lowvol_by_coin"] = lowv.groupby("coin").apply(dayt)
    neg["trend"] = np.where(neg.r60 > 0.10, "rising", np.where(neg.r60 < -0.10, "falling", "choppy"))
    neg.loc[neg.r60.isna(), "trend"] = "na"
    out["falls_lowvol_by_trend"] = neg[neg.vq3 == 0].groupby("trend").apply(dayt)
    out["falls_lowvol_by_fallcalm"] = neg[neg.vq3 == 0].groupby("fallcalm").apply(dayt)
    out["falls_highvol_by_fallcalm"] = neg[neg.vq3 == 2].groupby("fallcalm").apply(dayt)
    # total move (no drift removed) for low-vol falls
    out["falls_lowvol_total_fwd"] = dayt(lowv, "fwd")
    # short-term volume ratio
    neg["v10q"] = pd.qcut(neg["vr10"], 3, labels=False)
    out["falls_by_vr10_terc"] = neg.groupby("v10q").apply(dayt)
    return out
