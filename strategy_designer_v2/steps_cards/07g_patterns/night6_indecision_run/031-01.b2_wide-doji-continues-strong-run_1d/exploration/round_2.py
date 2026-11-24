def explore(data):
    import pandas as pd, numpy as np
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        frames = []
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); o = b["open"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo)
            b["r1"] = c / c.shift(1) - 1
            b["r5"] = c / c.shift(5) - 1
            b["wide"] = rng / rng.rolling(20).mean()
            b["clv"] = (c - lo) / rng.replace(0, np.nan)
            b["body"] = (c - o) / rng.replace(0, np.nan)
            b["vol20"] = b["r1"].rolling(20).std()
            b["z1"] = b["r1"] / b["vol20"]
            b["fwd"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["pos"] = np.arange(len(b))
            b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            frames.append(b[(b["pos"] % H == 0) & b["fwd"].notna()])
        g = pd.concat(frames)
        drift = g["fwd"].mean(); usual = g["fwd"].std()
        rows.append(g.assign(coin=coin, unus=g["fwd"] - drift, strength=(g["fwd"] - drift) / usual))
    G = pd.concat(rows)

    def summ(df):
        if len(df) < 5:
            return pd.Series({"n": len(df)})
        d = df.groupby("day")["unus"].sum(); nd = len(d)
        m = df["unus"].mean()
        se = np.sqrt((d**2).sum() * nd / (nd - 1)) / len(df)
        return pd.Series({"n": len(df), "days": nd, "mean_unus": m, "t": m / se,
                          "strength": df["strength"].mean(), "hit_up": (df["fwd"] > 0).mean()})

    out = {}
    W = G[G["wide"] >= 1.5].copy()
    Wd = W[W["r1"] < 0].copy()
    # grading: wide down days by z of the day's fall
    Wd["zq"] = pd.qcut(Wd["z1"], 3, labels=["deep", "mid", "shallow"])
    out["wide_down_by_fall_size"] = Wd.groupby("zq").apply(summ)
    Wd["wq"] = pd.qcut(Wd["wide"], 3, labels=["w_low", "w_mid", "w_high"])
    out["wide_down_by_width"] = Wd.groupby("wq").apply(summ)
    Wd["clvq"] = pd.cut(Wd["clv"], [-0.01, 0.33, 0.66, 1.01], labels=["close_low", "close_mid", "close_high"])
    out["wide_down_by_close_loc"] = Wd.groupby("clvq").apply(summ)
    out["wide_down_by_prior_run"] = Wd.groupby(np.where(Wd["r5"] > 0, "r5up", "r5down")).apply(summ)
    out["wide_down_by_coin"] = Wd.groupby("coin").apply(summ)
    out["wide_down_by_year"] = Wd.groupby("year").apply(summ)
    # continuous grading across all bars: product of width and signed return z
    G["press"] = -G["z1"] * G["wide"]
    G["pq"] = G.groupby("coin")["press"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["all_by_neg_z_x_width_decile"] = G.groupby("pq").apply(summ)
    # z1 deciles alone for comparison
    G["zq"] = G.groupby("coin")["z1"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["all_by_z1_decile"] = G.groupby("zq").apply(summ)
    # correlation of unusual move with press among wide down days
    out["corr_wide_down_press_unus"] = float(Wd[["unus"]].assign(p=-Wd["z1"] * Wd["wide"]).corr().iloc[0, 1])
    out["wide_down_next1_mean"] = float(Wd["fwd1"].mean())
    return out
