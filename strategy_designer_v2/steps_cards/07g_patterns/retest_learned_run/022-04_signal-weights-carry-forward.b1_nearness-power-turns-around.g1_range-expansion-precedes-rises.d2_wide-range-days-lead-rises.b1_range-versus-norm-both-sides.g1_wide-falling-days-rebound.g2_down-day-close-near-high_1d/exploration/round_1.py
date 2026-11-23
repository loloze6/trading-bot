def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if len(b) < 40: continue
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            r1 = c.pct_change()
            rng = (h - l) / c
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": np.arange(len(b)),
                "fwd": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "r1": r1,
                "r3": c / c.shift(3) - 1,
                "r10": c / c.shift(10) - 1,
                "r30": c / c.shift(30) - 1,
                "cloc": ((c - l) / (h - l)).replace([np.inf, -np.inf], np.nan),
                "rng_rel": rng / rng.rolling(20, min_periods=10).mean(),
                "vol20": r1.rolling(20, min_periods=10).std(),
                "vol_rel": r1.rolling(10, min_periods=5).std() / r1.rolling(60, min_periods=20).std(),
                "near_hi20": c / h.rolling(20, min_periods=10).max() - 1,
                "near_lo20": c / l.rolling(20, min_periods=10).min() - 1,
                "body": (c - o) / (h - l),
                "z1": r1 / r1.rolling(30, min_periods=10).std().shift(1),
                "volu_rel": b["volume"].astype(float) / b["volume"].astype(float).rolling(20, min_periods=10).mean(),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(f)
    A = pd.DataFrame(pd.concat(rows, ignore_index=True))
    G = A[(A["pos"] % H == 0)].dropna(subset=["fwd"]).copy()
    st = G.groupby("coin")["fwd"].agg(["mean", "std"])
    G["exc"] = G["fwd"] - G["coin"].map(st["mean"])
    G["s"] = G["exc"] / G["coin"].map(st["std"])
    out = {}
    feats = ["r1", "r3", "r10", "r30", "cloc", "rng_rel", "vol20", "vol_rel", "near_hi20", "near_lo20", "body", "z1", "volu_rel"]
    res = []
    for ft in feats:
        d = G.dropna(subset=[ft, "s"]).copy()
        d["rk"] = d.groupby("coin")[ft].rank(pct=True) - 0.5
        sl = stats.linregress(d["rk"], d["s"])
        q = pd.qcut(d["rk"], 5, labels=False)
        m = d.groupby(q)["s"].mean()
        # per coin sign consistency
        pc = d.groupby("coin").apply(lambda x: np.sign(stats.linregress(x["rk"], x["s"]).slope)).sum()
        res.append([ft, len(d), sl.slope, sl.slope / sl.stderr, m.iloc[0], m.iloc[-1], pc])
    out["feature_rank_vs_strength_all_days"] = pd.DataFrame(res, columns=["feat", "n", "slope", "t", "q1_s", "q5_s", "coin_sign_sum"]).round(4)
    # down vs up days, cloc
    res2 = []
    for side, d0 in [("down", G[G["r1"] < 0]), ("up", G[G["r1"] > 0])]:
        for ft in ["cloc", "rng_rel", "z1", "r10", "near_hi20", "vol_rel"]:
            d = d0.dropna(subset=[ft, "s"]).copy()
            d["rk"] = d.groupby("coin")[ft].rank(pct=True) - 0.5
            sl = stats.linregress(d["rk"], d["s"])
            res2.append([side, ft, len(d), sl.slope, sl.slope / sl.stderr])
    out["by_day_side"] = pd.DataFrame(res2, columns=["side", "feat", "n", "slope", "t"]).round(4)
    # regime: vol tercile x r30 sign
    G["volq"] = G.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    G["tr"] = np.sign(G["r30"])
    out["regime_mean_s"] = G.groupby(["volq", "tr"])["s"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))]).round(4)
    out["weekday_s"] = G.groupby("wd")["s"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))]).round(4)
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["win"] = w; x["coin"] = coin; dd.append(x)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    B = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().reset_index()
    B["yr"] = pd.to_datetime(B["day"]).dt.year
    out["book_by_year"] = B.groupby("yr")[["book_return", "coin_return"]].agg(["mean", "std"]).round(5)
    # position vs forecast quintile on book: gain per bar
    A["g"] = A["alloc"] * A["fwd1"]
    act = A[A["fc"] > 0].copy()
    act["fq"] = pd.qcut(act["fc"], 5, labels=False, duplicates="drop")
    out["fc_quintile_next1"] = act.groupby("fq")[["fc", "fwd1", "g"]].mean().round(5)
    return out
