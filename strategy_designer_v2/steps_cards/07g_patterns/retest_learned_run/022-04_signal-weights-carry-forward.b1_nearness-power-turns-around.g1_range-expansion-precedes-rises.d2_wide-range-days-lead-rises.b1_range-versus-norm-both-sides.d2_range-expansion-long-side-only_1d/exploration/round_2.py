def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l = b["close"], b["high"], b["low"]
            rng = (h - l) / c
            ratio = rng / rng.rolling(30, min_periods=15).mean()
            ret1 = c.pct_change()
            ret7 = c / c.shift(7) - 1
            ret14 = c / c.shift(14) - 1
            vol30 = ret1.rolling(30, min_periods=15).std()
            fwd3 = c.shift(-3) / c - 1
            idx = np.arange(0, len(b), 3)
            d = pd.DataFrame({
                "coin": coin, "win": w, "ratio": ratio.iloc[idx].values,
                "ret1": ret1.iloc[idx].values, "ret7": ret7.iloc[idx].values,
                "ret14": ret14.iloc[idx].values, "vol30": vol30.iloc[idx].values,
                "fwd3": fwd3.iloc[idx].values, "fc": b["forecast"].iloc[idx].values,
                "yr": pd.to_datetime(b["timestamp"].iloc[idx]).dt.year.values,
            })
            rows.append(d)
    g = pd.concat(rows).dropna(subset=["fwd3"])
    g["ex"] = g["fwd3"] - g.groupby("coin")["fwd3"].transform("mean")
    g["z1"] = g["ret1"] / g["vol30"]
    g["z7"] = g["ret7"] / (g["vol30"] * np.sqrt(7))

    def summ(grp):
        x = grp["ex"].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    gg = g.dropna(subset=["ratio", "z1"]).copy()
    gg["side"] = np.where(gg["ret1"] < 0, "down", "up")
    gg["rb"] = pd.cut(gg["ratio"], [0, 0.7, 1.0, 1.3, 1.7, 100], labels=["<0.7", "0.7-1", "1-1.3", "1.3-1.7", ">1.7"])
    out["ratio_bin_x_daysign"] = gg.groupby(["side", "rb"]).apply(summ)
    # graded signal: down-day size times range ratio
    dn = gg[gg["ret1"] < 0].copy()
    dn["s"] = -dn["z1"] * dn["ratio"]
    dn["sq"] = pd.qcut(dn["s"], 4, labels=False)
    out["down_days_by_sizexwidth_quartile"] = dn.groupby("sq").apply(summ)
    out["corr_s_ex_down"] = float(dn[["s", "ex"]].corr().iloc[0, 1])
    # down-day z1 quartiles all days
    dn["zq"] = pd.qcut(-dn["z1"], 4, labels=False)
    out["down_days_by_size_quartile"] = dn.groupby("zq").apply(summ)
    wd = gg[(gg["ret1"] < 0) & (gg["ratio"] > 1)]
    out["wide_down_by_coin"] = wd.groupby("coin").apply(summ)
    out["wide_down_by_year"] = wd.groupby("yr").apply(summ)
    # momentum graded
    g7 = g.dropna(subset=["z7"]).copy()
    g7["q"] = pd.qcut(g7["z7"], 10, labels=False)
    out["ret7z_deciles"] = g7.groupby("q").apply(summ)
    out["corr_z7_ex"] = float(g7[["z7", "ex"]].corr().iloc[0, 1])
    g14 = g.dropna(subset=["ret14"]).copy()
    g14["q"] = pd.qcut(g14["ret14"], 5, labels=False)
    out["ret14_quintiles"] = g14.groupby("q").apply(summ)
    g7h = g7[g7["z7"] > g7["z7"].quantile(0.8)]
    out["top_ret7_by_year"] = g7h.groupby("yr").apply(summ)
    return out
