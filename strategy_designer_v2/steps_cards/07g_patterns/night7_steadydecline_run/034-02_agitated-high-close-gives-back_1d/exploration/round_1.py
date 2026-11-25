def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 10: continue
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l)
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "cl": np.where(rng > 0, (c - l) / rng.replace(0, np.nan), np.nan),
                "ret1": c.pct_change(),
                "ret5": c / c.shift(5) - 1,
                "rngpct": rng / c,
                "body": (c - o) / rng.replace(0, np.nan),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "agit": (b["regime"] != "chop").astype(int),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            })
            df["gain"] = df["alloc"] * df["f1"]
            # rolling range rank within coin window
            df["rng_rel"] = df["rngpct"] / df["rngpct"].rolling(20, min_periods=10).median()
            df["vol20"] = df["ret1"].rolling(20, min_periods=10).std()
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby("coin")["f1"].mean()
    A["x1"] = A["f1"] - A["coin"].map(drift)
    for hh in [2, 3, 5]:
        A[f"x{hh}"] = A[f"f{hh}"] - A["coin"].map(A[A.pos % hh == 0].groupby("coin")[f"f{hh}"].mean())

    def summ(g, col="x1", grid=1):
        g = g[g.pos % grid == 0].dropna(subset=[col])
        n = len(g)
        if n < 5: return pd.Series({"n": n})
        d = g.groupby("day")[col].apply(lambda s: (s - g[col].mean()).sum())
        se = np.sqrt((d**2).sum()) * np.sqrt(len(d)/(len(d)-1)) / n
        return pd.Series({"n": n, "mean%": 100*g[col].mean(), "t_day": g[col].mean()/se})

    out = {}
    A["clq"] = pd.qcut(A["cl"], 5, labels=False)
    out["cl_quint_by_agit_next1"] = A.groupby(["agit", "clq"]).apply(summ).round(3)
    A["r1q"] = A.groupby("coin")["ret1"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ret1_quint_by_agit_next1"] = A.groupby(["agit", "r1q"]).apply(summ).round(3)
    A["rgq"] = pd.qcut(A["rng_rel"], 5, labels=False)
    out["rangerel_quint_next1"] = A.groupby("rgq").apply(summ).round(3)
    A["r5q"] = A.groupby("coin")["ret5"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ret5_quint_next5"] = A.groupby("r5q").apply(lambda g: summ(g, "x5", 5)).round(3)
    out["ret5_quint_next1"] = A.groupby("r5q").apply(summ).round(3)
    out["weekday_next1"] = A.groupby("wd").apply(summ).round(3)
    out["cl_quint_next3_agit"] = A[A.agit == 1].groupby("clq").apply(lambda g: summ(g, "x3", 3)).round(3)
    # book gains by year/agit/coin
    B = A.dropna(subset=["gain"])
    out["book_gain_by_coin"] = B[B.alloc != 0].groupby("coin")["gain"].agg(["count", "mean"]).assign(mean=lambda d: d["mean"]*100).round(4)
    out["book_gain_by_year"] = B[B.alloc != 0].groupby("yr")["gain"].agg(["count", "mean"]).assign(mean=lambda d: d["mean"]*100).round(4)
    # big ret1 & close location interaction (agitated)
    Ag = A[A.agit == 1].copy()
    Ag["dirn"] = np.sign(Ag["ret1"])
    out["agit_cl_by_daysign"] = Ag.groupby(["dirn", "clq"]).apply(summ).round(3)
    out["corr_x1"] = pd.Series({k: A[[k, "x1"]].dropna().corr().iloc[0, 1] for k in ["cl", "ret1", "ret5", "rng_rel", "body"]}).round(4)
    return out
