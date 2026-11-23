def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        coin_rows = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, hi, lo = b["close"], b["high"], b["low"]
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "win": w})
            df["fwd"] = c.shift(-H) / c - 1
            df["r1"] = r1
            df["r5"] = c / c.shift(5) - 1
            df["r20"] = c / c.shift(20) - 1
            df["vol20"] = r1.rolling(20).std()
            df["volratio"] = r1.rolling(5).std() / r1.rolling(60, min_periods=30).std()
            ph20 = hi.shift(1).rolling(20).max()
            df["dist_hi20"] = c / ph20 - 1
            pl20 = lo.shift(1).rolling(20).min()
            df["dist_lo20"] = c / pl20 - 1
            bo = (c > ph20)
            # failed breakout broad: a breakout close within last 3 days (not today), today close back below that day's broken level
            lvl = ph20.where(bo)
            last_lvl = lvl.shift(1).rolling(3, min_periods=1).max()
            df["fail_broad"] = (last_lvl.notna()) & (c < last_lvl)
            df["fail_depth"] = np.where(df["fail_broad"], 1 - c / last_lvl, np.nan)
            df["bo"] = bo
            df["range"] = (hi - lo) / c
            df["clv"] = (c - lo) / (hi - lo).replace(0, np.nan)
            df["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            df["fc"] = b["forecast"]
            df["alloc"] = b["postRebalance_current_allocation"]
            df["grid"] = (np.arange(len(b)) % H == 0)
            coin_rows.append(df)
        cd = pd.concat(coin_rows)
        g = cd[cd["grid"] & cd["fwd"].notna()]
        mu = g["fwd"].mean()
        cd["ex"] = cd["fwd"] - mu
        cd["usual"] = g["fwd"].std()
        rows.append(cd)
    A = pd.concat(rows)
    G = A[A["grid"] & A["fwd"].notna()].copy()
    G["z"] = G["ex"] / G["usual"]
    def summ(gr):
        x = gr["ex"]
        n = len(x)
        return pd.Series({"n": n, "mean_ex": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan, "mean_z": gr["z"].mean()})
    out = {}
    for f in ["r1", "r5", "r20", "vol20", "volratio", "dist_hi20", "dist_lo20", "range", "clv"]:
        G["q"] = G.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["by_" + f + "_quintile"] = G.groupby("q").apply(summ)
    out["by_weekday"] = G.groupby("wd").apply(summ)
    out["breakout_today"] = G.groupby("bo").apply(summ)
    out["fail_broad"] = G.groupby("fail_broad").apply(summ)
    fb = G[G["fail_broad"]]
    out["fail_broad_depth_spearman"] = str(stats.spearmanr(fb["fail_depth"], fb["ex"])) + " n=%d" % len(fb)
    # all bars (overlapping) fail broad by coin, for info only
    out["fail_broad_by_coin"] = G[G["fail_broad"]].groupby("coin").apply(summ)
    # spearman of features with z, pooled grid
    sp = {}
    for f in ["r1", "r5", "r20", "vol20", "volratio", "dist_hi20", "dist_lo20", "range", "clv"]:
        s = G[[f, "z"]].dropna()
        rr, p = stats.spearmanr(s[f], s["z"])
        sp[f] = (rr, p, len(s))
    out["spearman_feature_vs_z"] = pd.DataFrame(sp, index=["rho", "p", "n"]).T
    # book: days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["mean", "count"]).iloc[:40]
    out["book_corr_coin"] = float(bk.corr().iloc[0, 1])
    act = A[A["alloc"].abs() > 1e-6]
    out["active_bars_share"] = float(len(act) / len(A))
    return out
