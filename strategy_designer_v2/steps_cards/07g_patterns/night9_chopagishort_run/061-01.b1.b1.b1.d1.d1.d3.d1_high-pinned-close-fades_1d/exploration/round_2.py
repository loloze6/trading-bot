def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            clv = (c - b["low"]) / rng
            rngrel = rng / c
            rng_rank = rngrel.rolling(30, min_periods=15).apply(lambda s: (s[:-1] < s[-1]).mean(), raw=True)
            r20 = c.pct_change(20)
            r60 = c.pct_change(60)
            vol30 = c.pct_change().rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                 fwd=c.iloc[i + H] / c.iloc[i] - 1, clv=clv.iloc[i], rngrel=rngrel.iloc[i],
                                 rrank=rng_rank.iloc[i], r20=r20.iloc[i], r60=r60.iloc[i], vol30=vol30.iloc[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d["coin"].map(d.groupby("coin")["fwd"].mean())
    medv = d.groupby("coin")["vol30"].transform("median")
    d["agit"] = np.where(d["vol30"].isna(), "na", np.where(d["vol30"] > medv, "agit", "calm"))
    d["trend"] = pd.cut(d["r60"], [-np.inf, -0.10, 0.10, np.inf], labels=["fall", "chop", "rise"]).astype(str)
    def summ(g, col="ex"):
        g = g.dropna(subset=[col])
        if len(g) < 3:
            return pd.Series({"n": len(g), "mean": g[col].mean() if len(g) else np.nan, "t_day": np.nan, "days": len(g)})
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(g)
        return pd.Series({"n": len(g), "mean": m, "t_day": m / se, "days": D})
    out = {}
    # narrow-range high close continuation
    d["narrow"] = pd.cut(d["rrank"], [-0.01, 0.33, 0.67, 1.01], labels=["narrow", "mid", "wide"]).astype(str)
    d["hi"] = d["clv"] > 0.5
    out["narrow_hi_by_window"] = d[(d.narrow == "narrow") & d.hi].groupby("w").apply(summ)
    out["rrank_x_clv_all"] = d.groupby(["narrow", "hi"]).apply(summ)
    # graded: long signal = clv*(1-rrank) centered
    d["sig"] = (d["clv"] - 0.5) * (1 - d["rrank"])
    d["sigq"] = pd.qcut(d["sig"], 5, labels=False)
    out["sig_quintiles"] = d.groupby("sigq").apply(summ)
    out["narrow_hi_by_profile"] = d[(d.narrow == "narrow") & d.hi].groupby(["trend", "agit"]).apply(summ)
    out["narrow_lo_by_profile"] = d[(d.narrow == "narrow") & ~d.hi].groupby(["trend", "agit"]).apply(summ)
    # r20 momentum by profile and window
    d["r20q"] = pd.qcut(d["r20"], 5, labels=False)
    out["r20q_by_agit"] = d.groupby(["agit", "r20q"]).apply(summ)
    out["r20_top_minus_bottom_by_year"] = d.groupby("year").apply(
        lambda g: pd.Series({"top": g.loc[g.r20q >= 3, "ex"].mean(), "bot": g.loc[g.r20q <= 1, "ex"].mean(), "n": len(g)}))
    # choppy agitated high close at wide days (short-side, thin cell)
    out["chop_agit_clvq"] = d[(d.trend == "chop") & (d.agit == "agit")].groupby(pd.qcut(d["clv"], 3, labels=False)).apply(summ)
    out["profile_counts"] = d.groupby(["trend", "agit"]).size()
    return out
