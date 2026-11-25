def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["loc"] = (h - c) / rng  # 1 = close at low
            d["ret"] = c.pct_change()
            d["rngrel"] = (h - l) / c
            d["rngratio"] = d["rngrel"] / d["rngrel"].rolling(20, min_periods=10).mean().shift(1)
            d["vol20"] = d["ret"].rolling(20, min_periods=10).std()
            d["volratio"] = d["vol20"] / d["vol20"].rolling(60, min_periods=20).mean()
            d["ret20"] = c / c.shift(20) - 1
            d["low30"] = (c <= l.rolling(30, min_periods=20).min()).astype(int)
            for k in [1, 2, 3, 5]:
                d[f"f{k}"] = c.shift(-k) / c - 1
            hk = h.rolling(5, min_periods=5).max(); lk = l.rolling(5, min_periods=5).min()
            d["loc5"] = (hk - c) / (hk - lk).replace(0, np.nan)
            d["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            d["ts"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            d["alloc"] = b["postRebalance_current_allocation"]
            d["gain"] = d["alloc"] * c.pct_change().shift(-1)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in [1, 2, 3, 5]:
        D[f"f{k}d"] = D[f"f{k}"] - D.groupby("coin")[f"f{k}"].transform("mean")
    D["sig"] = 0.5 - (D["loc"] - 0.5) * -1  # not used
    D["side"] = np.sign(D["loc"] - 0.5)
    D["dirret"] = D["side"] * D["f1d"]
    out = {}
    def tab(g, col):
        a = g[col].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std")
    D["locq"] = pd.qcut(D["loc"], 5, labels=False, duplicates="drop")
    out["next1d_by_loc_quintile"] = tab(D.groupby("locq"), "f1d")
    D["rq"] = pd.qcut(D["rngratio"], 4, labels=False)
    out["dirret_by_range_ratio_q"] = tab(D.dropna(subset=["rq"]).groupby("rq"), "dirret")
    D["vq"] = pd.qcut(D["volratio"], 4, labels=False)
    out["dirret_by_volratio_q"] = tab(D.dropna(subset=["vq"]).groupby("vq"), "dirret")
    D["tq"] = pd.qcut(D["ret20"], 4, labels=False)
    out["dirret_by_ret20_q"] = tab(D.dropna(subset=["tq"]).groupby("tq"), "dirret")
    out["dirret_by_low30"] = tab(D.groupby("low30"), "dirret")
    out["next1d_by_low30"] = tab(D.groupby("low30"), "f1d")
    out["dirret_by_weekday"] = tab(D.groupby("wd"), "dirret")
    out["next1d_by_weekday"] = tab(D.groupby("wd"), "f1d")
    # signed, scaled by range: loc deviation x range
    D["ret_z"] = D["ret"] / D["vol20"]
    D["zq"] = pd.cut(D["ret_z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["next1d_by_today_z"] = tab(D.dropna(subset=["zq"]).groupby("zq"), "f1d")
    # multi-day: grid non-overlapping
    for k in [2, 3, 5]:
        G = D[D["pos"] % k == 0].copy()
        G["dr"] = np.sign(G["loc"] - 0.5) * G[f"f{k}d"]
        G["dr5"] = np.sign(G["loc5"] - 0.5) * G[f"f{k}d"]
        out[f"grid{k}_loc1_dirret"] = tab(G.assign(a=1).groupby("a"), "dr")
        G["l5q"] = pd.qcut(G["loc5"], 4, labels=False)
        out[f"grid{k}_by_loc5_q"] = tab(G.dropna(subset=["l5q"]).groupby("l5q"), f"f{k}d")
    out["dirret_by_win"] = tab(D.groupby("win"), "dirret")
    out["dirret_by_coin"] = tab(D.groupby("coin"), "dirret")
    # book days: largest gains/losses context
    out["gain_by_range_ratio_q"] = tab(D.dropna(subset=["rq"]).groupby("rq"), "gain")
    return out
