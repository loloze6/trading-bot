def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float); o = b["open"].astype(float)
            rng = (h - l).replace(0, np.nan)
            d = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "cl": (c - l) / rng,
                "r1": c.pct_change(), "r5p": c / c.shift(5) - 1, "r20p": c / c.shift(20) - 1,
                "r60p": c / c.shift(60) - 1,
                "vol20": c.pct_change().rolling(20).std(),
                "rngrel": (h - l) / c,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f5": c.shift(-5) / c - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            d["rngz"] = d["rngrel"] / d["rngrel"].rolling(20).mean()
            d["vol_rank"] = d["vol20"] / d["vol20"].rolling(60, min_periods=30).median()
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    out = {}
    def grid_stats(h, col, bins, label, sub=None):
        G = D[D["pos"] % h == 0].copy() if sub is None else sub[sub["pos"] % h == 0].copy()
        fcol = {1: "f1", 2: "f2", 5: "f5"}[h]
        allg = D[D["pos"] % h == 0]
        drift = allg.groupby("coin")[fcol].mean()
        G = G.dropna(subset=[col, fcol])
        G["u"] = G[fcol] - G["coin"].map(drift)
        G["bin"] = pd.qcut(G[col], bins, duplicates="drop") if not isinstance(bins, list) else pd.cut(G[col], bins)
        res = []
        for k, g in G.groupby("bin", observed=True):
            ds = g.groupby("day")["u"].sum()
            t = ds.mean() / (ds.std(ddof=1) / np.sqrt(len(ds))) * 1 if len(ds) > 2 else np.nan
            # t of mean per case with day clustering
            n = len(g); m = g["u"].mean()
            dev = (g["u"] - m).groupby(g["day"]).sum()
            se = np.sqrt((dev ** 2).sum() * len(dev) / (len(dev) - 1)) / n
            res.append({"bin": str(k), "n": n, "days": g["day"].nunique(), "mean_unusual_%": 100 * m, "t": m / se})
        return pd.DataFrame(res)
    out["cl_vs_f2"] = grid_stats(2, "cl", [-0.01, .25, .5, .75, .9, 1.01], "cl")
    out["cl_vs_f5"] = grid_stats(5, "cl", [-0.01, .25, .5, .75, .9, 1.01], "cl")
    out["r5p_vs_f5"] = grid_stats(5, "r5p", 5, "r5p")
    out["r1_vs_f1"] = grid_stats(1, "r1", 10, "r1")
    out["r20p_vs_f5"] = grid_stats(5, "r20p", 5, "r20p")
    out["vol_rank_vs_f5"] = grid_stats(5, "vol_rank", 4, "vr")
    out["rngz_vs_f2"] = grid_stats(2, "rngz", 5, "rz")
    # falling 60d subset
    fall = D[D["r60p"] < -0.10]
    out["fall_cl_vs_f5"] = grid_stats(5, "cl", [-0.01, .25, .5, .75, 1.01], "cl", fall)
    out["fall_r5p_vs_f5"] = grid_stats(5, "r5p", 4, "r5p", fall)
    out["fall_r1_vs_f2"] = grid_stats(2, "r1", 5, "r1", fall)
    # weekday next-day return
    W = D.dropna(subset=["f1"]).copy()
    W["wd"] = W["ts"].dt.dayofweek
    dr = W.groupby("coin")["f1"].mean()
    W["u"] = W["f1"] - W["coin"].map(dr)
    out["weekday_next1"] = W.groupby("wd")["u"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # book: by window daily mean & in-position
    bd = []
    for coin, ws in days.items():
        for w, dd in ws.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; bd.append(x)
    B = pd.concat(bd)
    bk = B.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    out["book_by_window"] = bk.groupby("w").agg(mean_book=("book_return", "mean"), mean_coin=("coin_return", "mean"), n=("day", "count"))
    # positions: forward 1d gain by position size bins
    P = D[D["alloc"] < 0].dropna(subset=["f1"])
    out["in_pos_count_gain"] = pd.Series({"n_bars": len(P), "mean_gain_%": 100 * (P["alloc"] * P["f1"]).mean(), "mean_f1_%": 100 * P["f1"].mean()})
    return out
