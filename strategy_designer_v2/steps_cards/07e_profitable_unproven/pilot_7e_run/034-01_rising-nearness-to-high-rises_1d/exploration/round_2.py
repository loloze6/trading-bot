def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True).copy()
            b["coin"] = coin; b["win"] = w
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"].fillna(0)
            b["gain"] = b["pos"] * b["r1"]
            pm = b["close"].shift(1).rolling(20, min_periods=20).max()
            sd = b["close"].pct_change().rolling(20, min_periods=20).std()
            b["dist"] = (b["close"] / pm - 1) / sd
            b["ret60"] = b["close"] / b["close"].shift(60) - 1
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["vol20"] = sd
            b["volrel"] = sd / b["close"].pct_change().rolling(60, min_periods=40).std()
            for h in (5, 10):
                b[f"f{h}"] = b["close"].shift(-h) / b["close"] - 1
            b["pos_in_win"] = np.arange(len(b))
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cm = B.groupby("coin")["r1"].mean()
    B["timing"] = B["gain"] - B["pos"] * B["coin"].map(cm)
    B["date"] = pd.to_datetime(B["timestamp"]).dt.floor("D")
    A = B[B["regime"] == "unknown"].copy()
    for h in (5, 10):
        dm = B[B["pos_in_win"] % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(dm)
    # book gain by dist bucket (all in-profile bars)
    A["dbin"] = pd.cut(A["dist"], [-99, -3, -1.5, -0.5, 0, 0.5, 1.5, 99])
    out["book_by_dist_bin"] = A.groupby("dbin").agg(gain_sum=("gain", "sum"), timing_sum=("timing", "sum"),
                                                     pos=("pos", "mean"), n=("gain", "size"))
    def clus_t(G, col):
        s = G.groupby("date")[col].sum(); n = G.groupby("date")[col].size()
        m = G[col].mean()
        dev = (G[col] - m).groupby(G["date"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(G)
        return m, m / se, G["date"].nunique()
    res = {}
    for h in (5, 10):
        G = A[A["pos_in_win"] % h == 0].dropna(subset=[f"u{h}", "dist"])
        G = G.assign(dbin=pd.cut(G["dist"], [-99, -3, -1.5, -0.5, 0, 0.5, 1.5, 99]))
        for k, g in G.groupby("dbin"):
            if len(g) > 5:
                m, t, nd = clus_t(g, f"u{h}")
                res[(h, str(k))] = {"mean_u": m, "t_day": t, "n": len(g), "days": nd}
    out["u_by_dist_bin"] = pd.DataFrame(res).T
    # above high: graded by distance above? and by 60d trend strength
    G = A[A["pos_in_win"] % 10 == 0].dropna(subset=["u10", "dist", "ret60"])
    up = G[G["dist"] > 0]
    out["above_high_corr_dist_u10"] = pd.Series({"corr": stats.pearsonr(up["dist"], up["u10"])[0],
                                                  "p": stats.pearsonr(up["dist"], up["u10"])[1], "n": len(up)})
    G = G.assign(tq=pd.qcut(G["ret60"], 4, labels=False))
    out["u10_by_ret60_q_and_above"] = G.groupby(["tq", G["dist"] > 0]).agg(ret60=("ret60", "mean"), u10=("u10", "mean"), n=("u10", "size"))
    G = G.dropna(subset=["volrel"]).assign(vq=lambda x: pd.qcut(x["volrel"], 2, labels=False))
    out["u10_by_volrel_and_above"] = G.groupby(["vq", G["dist"] > 0]).agg(volrel=("volrel", "mean"), u10=("u10", "mean"), n=("u10", "size"))
    # book without w10,w11
    D = B.groupby(["win", "date"])["gain"].mean()
    keep = D[~D.index.get_level_values(0).isin(["w10", "w11"])]
    out["book_ex_w10_w11"] = pd.Series({"mean": keep.mean(), "t": keep.mean() / (keep.std() / np.sqrt(len(keep))), "n": len(keep),
                                        "all_mean": D.mean()})
    # by side and dist at short bars
    A["side"] = np.sign(A["pos"])
    out["side_by_dist_sign"] = A.groupby(["side", A["dist"] > 0]).agg(gain_sum=("gain", "sum"), timing_sum=("timing", "sum"), n=("gain", "size"))
    return out
