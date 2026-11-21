def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
                "r1": r1,
                "r5p": c / c.shift(5) - 1,
                "r28": c / c.shift(28) - 1,
                "vol30": r1.rolling(30, min_periods=20).std(),
                "near": c / c.rolling(60, min_periods=30).max() - 1,
                "rng": (b["high"].astype(float) - b["low"].astype(float)) / c,
                "fwd5": c.shift(-H) / c - 1,
                "fwd10": c.shift(-10) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "i": np.arange(len(b)),
            })
            df["rngrel"] = df["rng"] / df["rng"].rolling(30, min_periods=20).mean()
            df["volrel"] = df["vol30"] / r1.abs().rolling(10, min_periods=8).mean()
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    g = A[A["i"] % H == 0].copy()
    g = g.dropna(subset=["fwd5"])
    g["drift"] = g.groupby("coin")["fwd5"].transform("mean")
    g["sd"] = g.groupby("coin")["fwd5"].transform("std")
    g["ex"] = (g["fwd5"] - g["drift"]) / g["sd"]
    g["exraw"] = g["fwd5"] - g["drift"]
    out = {}
    def tab(col, q=5):
        d = g.dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = d.groupby("q").agg(n=("ex", "size"), ex_strength=("ex", "mean"), ex_raw=("exraw", "mean"))
        t["t"] = d.groupby("q")["ex"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        top = d[d.q == q - 1].groupby("coin")["ex"].mean() - d[d.q == 0].groupby("coin")["ex"].mean()
        t["coins_top_gt_bottom"] = (top > 0).sum()
        return t
    for col in ["fc", "r1", "r5p", "r28", "vol30", "near", "rngrel", "volrel"]:
        out["q_" + col] = tab(col)
    wd = g.groupby("wd")["ex"].agg(["size", "mean"])
    wd["t"] = g.groupby("wd")["ex"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["weekday_start"] = wd
    yr = g.groupby("yr").apply(lambda d: pd.Series({"n": len(d), "timing": (d.pos * d.exraw).mean(),
                                                   "pos_mean": d.pos.mean()}))
    out["by_year_timing"] = yr
    # book days
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.reset_index(drop=True).copy()
            d["coin"] = coin; d["win"] = w
            d["next5"] = d["coin_return"].shift(-1).rolling(5).sum().shift(-4)
            d["prev5"] = d["coin_return"].rolling(5).sum().shift(1)
            dl.append(d)
    D = pd.concat(dl, ignore_index=True).dropna(subset=["book_return"])
    D["bq"] = D.groupby("coin")["book_return"].transform(lambda s: pd.qcut(s.rank(method="first"), 20, labels=False))
    ext = D[D.bq.isin([0, 19])].groupby("bq").agg(n=("book_return", "size"), book=("book_return", "mean"),
          coin_same=("coin_return", "mean"), coin_prev5=("prev5", "mean"), coin_next5=("next5", "mean"))
    out["book_extreme_days"] = ext
    A2 = A.dropna(subset=["pos"])
    out["pos_share"] = pd.Series({"long": (A2.pos > 0).mean(), "short": (A2.pos < 0).mean(), "flat": (A2.pos == 0).mean(),
                                  "corr_fc_r28": A[["fc", "r28"]].corr().iloc[0, 1],
                                  "corr_fc_vol30": A[["fc", "vol30"]].corr().iloc[0, 1]})
    return out
