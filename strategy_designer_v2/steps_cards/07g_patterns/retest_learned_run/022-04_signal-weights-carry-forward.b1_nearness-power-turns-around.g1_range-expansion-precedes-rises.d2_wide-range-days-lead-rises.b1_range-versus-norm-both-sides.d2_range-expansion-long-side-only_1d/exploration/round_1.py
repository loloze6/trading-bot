def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = (h - l) / c
            ratio = rng / rng.rolling(30, min_periods=15).mean()
            ret1 = c.pct_change()
            ret7 = c / c.shift(7) - 1
            clv = (c - l) / (h - l).replace(0, np.nan)
            vol20 = ret1.rolling(20, min_periods=10).std()
            fwd3 = c.shift(-3) / c - 1
            fwd1 = c.shift(-1) / c - 1
            idx = np.arange(0, len(b), 3)
            d = pd.DataFrame({
                "coin": coin, "win": w, "ratio": ratio.iloc[idx].values,
                "ret1": ret1.iloc[idx].values, "ret7": ret7.iloc[idx].values,
                "clv": clv.iloc[idx].values, "vol20": vol20.iloc[idx].values,
                "fwd3": fwd3.iloc[idx].values, "fc": b["forecast"].iloc[idx].values,
                "wd": pd.to_datetime(b["timestamp"].iloc[idx]).dt.weekday.values,
                "yr": pd.to_datetime(b["timestamp"].iloc[idx]).dt.year.values,
            })
            rows.append(d)
    g = pd.concat(rows).dropna(subset=["fwd3"])
    g["ex"] = g["fwd3"] - g.groupby("coin")["fwd3"].transform("mean")

    def summ(grp):
        x = grp["ex"].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    g2 = g.dropna(subset=["ratio"])
    g2["rq"] = pd.qcut(g2["ratio"], 5, labels=False)
    out["by_range_ratio_quintile"] = g2.groupby("rq").apply(summ)
    wide = g2[g2["ratio"] > 1].copy()
    wide["upday"] = np.where(wide["ret1"] > 0, "up", "down")
    out["wide_by_day_sign"] = wide.groupby("upday").apply(summ)
    wide["clvq"] = pd.cut(wide["clv"], [-0.01, 0.33, 0.67, 1.01], labels=["lowclose", "mid", "highclose"])
    out["wide_by_close_location"] = wide.groupby("clvq").apply(summ)
    g3 = g.dropna(subset=["ret1"]).copy()
    g3["r1q"] = pd.qcut(g3["ret1"], 5, labels=False)
    out["all_by_ret1_quintile"] = g3.groupby("r1q").apply(summ)
    g4 = g.dropna(subset=["ret7"]).copy()
    g4["r7q"] = pd.qcut(g4["ret7"], 5, labels=False)
    out["all_by_ret7_quintile"] = g4.groupby("r7q").apply(summ)
    g5 = g.dropna(subset=["vol20"]).copy()
    g5["vq"] = g5.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["all_by_vol_tercile"] = g5.groupby("vq").apply(summ)
    out["by_weekday"] = g.groupby("wd").apply(summ)
    out["by_year"] = g.groupby("yr").apply(summ)
    gc = g.copy(); gc["clvq"] = pd.cut(gc["clv"], [-0.01, 0.33, 0.67, 1.01], labels=["low", "mid", "high"])
    out["all_by_close_location"] = gc.groupby("clvq").apply(summ)
    out["fc_pos_by_coin"] = g[g["fc"] > 0].groupby("coin").apply(summ)
    # book: largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    D = pd.concat(dd)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_vs_coin_corr"] = float(bk.corr().iloc[0, 1])
    q = bk["book_return"]
    out["book_top5pct_share_of_sum"] = float(q[q > q.quantile(0.95)].sum() / q.sum())
    out["book_bottom5pct_share_of_sum"] = float(q[q < q.quantile(0.05)].sum() / q.sum())
    return out
