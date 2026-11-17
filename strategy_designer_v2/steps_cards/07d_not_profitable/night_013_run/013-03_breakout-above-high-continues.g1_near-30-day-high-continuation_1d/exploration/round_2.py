def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    S = []
    D = []
    for coin, wins in data["bars"].items():
        allc = []
        for w, b in wins.items():
            c = b["close"].values
            r10 = pd.Series(c).shift(-10).values / c - 1
            allc.append(r10[::10])
        mu10 = np.nanmean(np.concatenate(allc))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r10 = c.shift(-10) / c - 1
            r60 = c / c.shift(60) - 1
            dh = b["debug_info.components.dist_high.last_history_value"]
            g = pd.DataFrame({"dh": dh, "r10": r10 - mu10, "raw10": r10, "r60": r60,
                              "fc": b["forecast"], "pos": b["postRebalance_current_allocation"],
                              "coin": coin}).iloc[::10]
            S.append(g)
            ret1 = c.shift(-1) / c - 1
            D.append(pd.DataFrame({"gain": b["postRebalance_current_allocation"] * ret1,
                                   "pos": b["postRebalance_current_allocation"], "r60": r60, "dh": dh}))
    S = pd.concat(S).dropna(subset=["dh", "r10"])
    S["dhbin"] = pd.qcut(S.dh, 6)
    out["fwd10_by_dist"] = S.groupby("dhbin", observed=True).agg(n=("r10", "size"),
        excess10=("r10", "mean"), raw10=("raw10", "mean"), up_share=("raw10", lambda s: (s > 0).mean()),
        fc=("fc", "mean"))
    S2 = S.dropna(subset=["r60"])
    S2["trend"] = np.where(S2.r60 > 0, "r60_up", "r60_down")
    out["fwd10_by_dist_trend"] = S2.groupby(["trend", pd.qcut(S2.dh, 3)], observed=True).agg(
        n=("r10", "size"), excess10=("r10", "mean"), raw10=("raw10", "mean"))
    # slope t within trend states
    res = {}
    for k, g in S2.groupby("trend"):
        sl = stats.linregress(g.dh, g.r10)
        res[k] = {"n": len(g), "slope": sl.slope, "t": sl.slope / sl.stderr}
    out["slope_by_trend"] = pd.DataFrame(res).T
    D = pd.concat(D).dropna()
    D["side"] = np.where(D.pos > 0.01, "long", np.where(D.pos < -0.01, "short", "flat"))
    out["gain_by_side"] = D.groupby("side").agg(n=("gain", "size"), mean_gain=("gain", "mean"),
        sum_gain=("gain", "sum"), mean_abs_pos=("pos", lambda s: s.abs().mean()))
    D["trend"] = np.where(D.r60 > 0, "r60_up", "r60_down")
    out["gain_side_trend"] = D.groupby(["side", "trend"]).agg(n=("gain", "size"),
        mean_gain=("gain", "mean"), sum_gain=("gain", "sum"))
    return out
