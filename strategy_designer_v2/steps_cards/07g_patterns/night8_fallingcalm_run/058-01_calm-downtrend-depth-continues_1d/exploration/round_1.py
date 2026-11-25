def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H) / c - 1,
                "r30": c / c.shift(30) - 1,
                "r60": c / c.shift(60) - 1,
                "r5": c / c.shift(5) - 1,
                "r1": r1,
                "vol10": r1.rolling(10).std(),
                "vol30": r1.rolling(30).std(),
                "vr": v.rolling(10).mean() / v.rolling(40).mean(),
                "vr30": v.rolling(30).mean() / v.shift(30).rolling(30).mean(),
                "fc": b["forecast"].astype(float),
                "fallcalm": (b["regime"] != "chop").astype(int),
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            })
            df = df[df["pos"] % H == 0]
            rows.append(df)
    g = pd.concat(rows).dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - drift
    def summ(s):
        s = s.dropna()
        n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    out["drift_by_coin"] = g.groupby("coin")["fwd"].agg(["mean", "std", "count"])
    out["ex_by_fallcalm"] = g.groupby("fallcalm")["ex"].apply(summ).unstack()
    g["r30q"] = pd.qcut(g["r30"], 5, labels=False)
    out["ex_by_r30q_all"] = g.groupby("r30q")["ex"].apply(summ).unstack()
    out["ex_by_r30q_fallcalm"] = g[g.fallcalm == 1].groupby(pd.qcut(g.loc[g.fallcalm == 1, "r30"], 3, labels=False))["ex"].apply(summ).unstack()
    g["trend"] = np.where(g.r60 > 0.10, "rising", np.where(g.r60 < -0.10, "falling", "choppy"))
    g.loc[g.r60.isna(), "trend"] = "na"
    out["ex_by_trend"] = g.groupby("trend")["ex"].apply(summ).unstack()
    out["ex_by_trend_r30q"] = g.groupby(["trend", "r30q"])["ex"].mean().unstack()
    g["vrq"] = pd.qcut(g["vr"], 3, labels=False)
    out["ex_by_vrq_fallcalm"] = g[g.fallcalm == 1].groupby("vrq")["ex"].apply(summ).unstack()
    out["ex_by_vrq_all"] = g.groupby("vrq")["ex"].apply(summ).unstack()
    neg = g[g.r30 < 0]
    out["ex_falls_by_vr30q"] = neg.groupby(pd.qcut(neg["vr30"], 3, labels=False))["ex"].apply(summ).unstack()
    g["r5q"] = pd.qcut(g["r5"], 5, labels=False)
    out["ex_by_r5q"] = g.groupby("r5q")["ex"].apply(summ).unstack()
    g["r1q"] = pd.qcut(g["r1"], 5, labels=False)
    out["ex_by_r1q"] = g.groupby("r1q")["ex"].apply(summ).unstack()
    g["volq"] = pd.qcut(g["vol10"] / g["vol30"], 3, labels=False)
    out["ex_by_vol10_30q"] = g.groupby("volq")["ex"].apply(summ).unstack()
    out["ex_by_weekday"] = g.groupby("wd")["ex"].apply(summ).unstack()
    out["ex_by_year"] = g.groupby("yr")["ex"].apply(summ).unstack()
    out["ex_by_window"] = g.groupby("win")["ex"].apply(summ).unstack()
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    D = pd.concat(dd)
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean()
    out["book_by_win"] = D.groupby("win")["book_return"].agg(["mean", "std", "count"])
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
