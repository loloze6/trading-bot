def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "cl": (h - c) / rng,                      # 0 at high, 1 at low
                "r0": c / c.shift(1) - 1,
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c - 1,
                "rng_pct": (h - l) / c,
                "body": (c - o) / rng,
                "inprof": (b["regime"] == "unknown").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            lr = np.log(c).diff()
            d["vol30"] = lr.rolling(30, min_periods=20).std()
            d["volrel"] = d["vol30"] / d["vol30"].rolling(120, min_periods=40).median()
            d["ret60"] = c / c.shift(60) - 1
            d["ret5"] = c / c.shift(5) - 1
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    mu = df.groupby("coin")["r1"].transform("mean")
    df["x1"] = df["r1"] - mu
    df["day"] = df["ts"].dt.floor("D")
    df["wd"] = df["ts"].dt.weekday
    out = {}

    def grp(sub, key):
        g = sub.dropna(subset=["x1", key])
        res = []
        for k, s in g.groupby(key):
            dm = s.groupby("day")["x1"].mean()
            t = dm.mean() / (dm.std(ddof=1) / np.sqrt(len(dm))) if len(dm) > 2 else np.nan
            res.append({key: k, "n_cases": len(s), "n_days": len(dm), "mean_x1_pct": 100 * s["x1"].mean(), "t_day": t})
        return pd.DataFrame(res)

    df["clq"] = pd.qcut(df["cl"], 5, labels=False)
    df["vq"] = df.groupby("coin")["volrel"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    df["agit"] = (df["volrel"] > 1).astype(int)
    df["trend"] = np.select([df["ret60"] > 0.1, df["ret60"] < -0.1], ["rise", "fall"], "chop")
    df.loc[df["ret60"].isna(), "trend"] = np.nan
    out["clq_inprof"] = grp(df[df.inprof == 1], "clq")
    out["clq_outprof"] = grp(df[df.inprof == 0], "clq")
    out["clq_agit"] = grp(df[df.agit == 1], "clq")
    out["clq_calm"] = grp(df[df.agit == 0], "clq")
    # slope of x1 on cl by trend x agit, per-day sum t
    res = []
    for (tr, ag), s in df.dropna(subset=["x1", "cl", "trend"]).groupby(["trend", "agit"]):
        s = s.copy(); s["p"] = (s["cl"] - 0.5) * s["x1"]
        dm = s.groupby("day")["p"].sum()
        res.append({"trend": tr, "agit": ag, "n": len(s), "days": len(dm), "mean_x1_pct": 100*s.x1.mean(),
                    "corr": s[["cl", "x1"]].corr().iloc[0, 1], "t": dm.mean() / (dm.std() / np.sqrt(len(dm)))})
    out["cl_by_trend_agit"] = pd.DataFrame(res)
    df["r0q"] = pd.qcut(df["r0"], 5, labels=False)
    out["r0q_all"] = grp(df, "r0q")
    out["r0q_agit"] = grp(df[df.agit == 1], "r0q")
    df["rngq"] = df.groupby("coin")["rng_pct"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["rngq"] = grp(df, "rngq")
    df["r5q"] = pd.qcut(df["ret5"], 5, labels=False)
    out["r5q"] = grp(df, "r5q")
    out["weekday"] = grp(df, "wd")
    out["vq"] = grp(df, "vq")
    out["trend"] = grp(df.dropna(subset=["trend"]), "trend")
    # book days
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; dd["win"] = w; dl.append(dd)
    D = pd.concat(dl)
    bk = D.groupby("day")[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = D.groupby("win")[["book_return", "coin_return"]].mean() * 100
    out["n_inprof_share"] = float(df.inprof.mean())
    out["alloc_sign_inprof"] = df[df.inprof == 1]["alloc"].apply(np.sign).value_counts()
    return out
