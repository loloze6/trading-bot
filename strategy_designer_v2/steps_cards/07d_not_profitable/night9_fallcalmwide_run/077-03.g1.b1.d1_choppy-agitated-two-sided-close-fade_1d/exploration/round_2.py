def explore(data):
    import pandas as pd, numpy as np
    out = {}
    cr = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["r0"] = b["close"] / b["close"].shift(1) - 1
            b["s"] = np.log(b["close"]).diff().rolling(30).std()
            b["width"] = (b["high"] - b["low"]) / b["close"] / b["s"]
            b["pos"] = (b["close"] - b["low"]) / (b["high"] - b["low"])
            b["r5"] = b["close"] / b["close"].shift(5) - 1
            b["r5s"] = b["r5"] / (b["s"] * np.sqrt(5))
            b["r10"] = b["close"] / b["close"].shift(10) - 1
            b["a"] = b["postRebalance_current_allocation"]
            b["gain"] = b["a"] * b["nxt"]
            b["coin"] = c; b["wn"] = int(w[1:]); b["i"] = np.arange(len(b))
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            cr.append(b)
    X = pd.concat(cr, ignore_index=True)
    drift = X.groupby("coin")["nxt"].mean()
    X["ex"] = X["nxt"] - X["coin"].map(drift)
    X["prof"] = X["regime"] == "unknown"
    X["inpos"] = X["a"].abs() > 1e-9
    # fall period: w15 late to w16; gains by side, coin in w14-w16
    F = X[X["wn"].isin([12, 13, 14, 15, 16]) & X["inpos"]].copy()
    F["side"] = np.sign(F["a"])
    out["fallwins_side"] = F.groupby(["wn", "side"]).agg(n=("gain", "size"), gain=("gain", "sum"), worst=("gain", "min"))
    out["fallwins_coin"] = F.groupby(["wn", "coin"]).agg(n=("gain", "size"), gain=("gain", "sum"), worst=("gain", "min"))
    # worst 15 gains overall: their context (aggregated)
    A = X[X["inpos"] & X["nxt"].notna()].copy()
    A["side"] = np.sign(A["a"])
    A["dir_r5s"] = A["side"] * A["r5s"]  # >0: position with the 5-day move
    A["dir_r0"] = A["side"] * A["r0"]
    worst = A.nsmallest(20, "gain")
    out["worst20_summary"] = pd.Series({"sum_gain": worst["gain"].sum(), "total_gain_all": A["gain"].sum(),
        "share_short": (worst["side"] < 0).mean(), "mean_dir_r5s": worst["dir_r5s"].mean(), "all_mean_dir_r5s": A["dir_r5s"].mean(),
        "share_with5d": (worst["dir_r5s"] > 0).mean(), "all_share_with5d": (A["dir_r5s"] > 0).mean(),
        "mean_width_worst": worst["width"].mean(), "mean_width_all": A["width"].mean()})
    # graded: position aligned against vs with the 5-day move (fade after 5d move same way as signal)
    A["agree5"] = pd.qcut(A["dir_r5s"], 3, labels=["against5d", "mid", "with5d"])
    g = A.groupby(["side", "agree5"])
    out["by_side_agree5"] = g.agg(n=("gain", "size"), dirnxt=("nxt", lambda s: np.nan), gain=("gain", "sum"))
    A["dirnxt"] = A["side"] * A["nxt"]
    out["by_agree5"] = A.groupby("agree5").agg(n=("dirnxt", "size"), mean=("dirnxt", "mean"), sd=("dirnxt", "std"), gain=("gain", "sum"))
    # condition alone: profile bars without position, by r5s tercile, next-day ex return (long direction)
    P = X[X["prof"] & X["nxt"].notna() & X["r5s"].notna()].copy()
    P["r5q"] = pd.qcut(P["r5s"], 3, labels=["r5lo", "r5mid", "r5hi"])
    def tt(s):
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    out["prof_nopos_r5q_ex"] = P[~P["inpos"]].groupby("r5q")["ex"].apply(tt).unstack()
    out["prof_pos_r5q_direx_long"] = P[P["inpos"] & (P["a"] > 0)].groupby("r5q")["ex"].apply(tt).unstack()
    out["prof_pos_r5q_direx_short"] = (-P[P["inpos"] & (P["a"] < 0)].set_index("r5q")["ex"]).groupby(level=0).apply(tt).unstack()
    # close position effect within profile, all bars (graded by pos), next-day ex
    P["posq"] = pd.qcut(P["pos"], 5, labels=False)
    out["prof_all_posq"] = P.groupby("posq")["ex"].apply(tt).unstack()
    # wide days only (top third width) in profile
    W = P[P["width"] >= P["width"].quantile(2/3)]
    out["prof_wide_posq"] = W.groupby(pd.qcut(W["pos"], 5, labels=False))["ex"].apply(tt).unstack()
    # profile share and positions per profile bar
    out["prof_share"] = float(X["prof"].mean()); out["pos_share_in_prof"] = float(X.loc[X["prof"], "inpos"].mean())
    # holding: run lengths
    return out
