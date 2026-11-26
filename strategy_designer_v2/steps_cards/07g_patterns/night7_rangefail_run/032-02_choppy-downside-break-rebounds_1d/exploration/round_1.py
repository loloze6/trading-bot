def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            r5p = c / c.shift(5) - 1
            tr60 = (c / c.shift(60) - 1) * 100
            lo20 = lo.shift(1).rolling(20).min(); hi20 = hi.shift(1).rolling(20).max()
            dlo = c / lo20 - 1; dhi = c / hi20 - 1
            vol30 = r1.rolling(30).std(); vol365med = vol30.rolling(365, min_periods=120).median()
            pos = b["postRebalance_current_allocation"].astype(float)
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            df = pd.DataFrame({"coin": coin, "win": w, "i": np.arange(n), "fwd": fwd, "r1": r1, "r5p": r5p,
                               "tr60": tr60, "dlo": dlo, "dhi": dhi, "agit": vol30 > vol365med,
                               "volz": vol30 / vol365med, "wd": wd, "pos": pos, "fc": b["forecast"].astype(float)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    g = A[(A["i"] % H == 0) & A["fwd"].notna()].copy()
    drift = g.groupby("coin")["fwd"].mean()
    sd = g.groupby("coin")["fwd"].std()
    g["un"] = g["fwd"] - g["coin"].map(drift)
    g["str"] = g["un"] / g["coin"].map(sd)
    g["trend"] = np.where(g["tr60"] > 10, "rising", np.where(g["tr60"] < -10, "falling", "choppy"))
    g.loc[g["tr60"].isna(), "trend"] = "na"
    def summ(x):
        return pd.Series({"n": len(x), "mean_un": x["un"].mean(), "t": x["un"].mean() / (x["un"].std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "strength": x["str"].mean()})
    out = {}
    g["brk"] = np.where(g["dlo"] < 0, "below_low", np.where(g["dhi"] > 0, "above_high", "inside"))
    out["break_by_trend"] = g.groupby(["trend", "brk"]).apply(summ)
    g["r5q"] = g.groupby("coin")["r5p"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["past5d_quintile"] = g.groupby("r5q").apply(summ)
    out["past5d_q_by_trend"] = g.groupby(["trend", "r5q"]).apply(summ)
    g["r1q"] = g.groupby("coin")["r1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["past1d_quintile"] = g.groupby("r1q").apply(summ)
    g["vq"] = g.groupby("coin")["volz"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out["vol_quartile"] = g.groupby("vq").apply(summ)
    out["trend_x_agit"] = g.groupby(["trend", "agit"]).apply(summ)
    out["by_window"] = g.groupby("win").apply(summ)
    # tr60 quintile
    g["tq"] = g.groupby("coin")["tr60"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["tr60_quintile"] = g.groupby("tq").apply(summ)
    # daily weekday effect
    A["un1"] = A["r1"].shift(-1)
    d = A.dropna(subset=["r1"])
    out["weekday_next1d"] = d.groupby("wd")["r1"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # depth among below_low choppy
    bl = g[g["dlo"] < 0]
    out["below_low_depth_q"] = bl.assign(dq=pd.qcut(bl["dlo"], 4, labels=False)).groupby(["dq"]).apply(summ)
    ah = g[g["dhi"] > 0]
    out["above_high_size_q"] = ah.assign(dq=pd.qcut(ah["dhi"], 4, labels=False)).groupby(["dq"]).apply(summ)
    out["coins_book_inpos_share"] = A.groupby("coin")["pos"].apply(lambda s: (s.abs() > 0).mean())
    return out
