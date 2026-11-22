def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            d["z"] = r / sd.shift(1)
            d["r90"] = c / c.shift(90) - 1
            for h in (5, 20):
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["g1"] = d["postRebalance_current_allocation"].astype(float) * (c.shift(-1) / c - 1)
            d["coin"] = coin; d["win"] = w; d["pos"] = np.arange(len(d))
            d["yr"] = pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d[["coin","win","pos","z","r90","f5","f20","g1","regime",
                           "postRebalance_current_allocation","yr"]])
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # book gain per bar by regime and side of position
    A["side"] = np.sign(A["postRebalance_current_allocation"]).map({1: "long", -1: "short", 0: "flat"})
    gg = A.dropna(subset=["g1"]).groupby(["regime","side"])["g1"].agg(["mean","count","std"])
    gg["t"] = gg["mean"] / (gg["std"] / np.sqrt(gg["count"]))
    gg["sum"] = gg["mean"] * gg["count"]
    out["bar gain by regime x side"] = gg.round(5)
    def tab(g, col, keys):
        t = g.groupby(keys, observed=True)[col].agg(["mean","count","std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.round(4)
    for h in (5, 20):
        g = A[A["pos"] % h == 0].dropna(subset=[f"f{h}"]).copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["u"] = g[f"f{h}"] - g["coin"].map(drift)
        g = g.dropna(subset=["z"])
        g["half"] = np.where(g["yr"] <= 2021, "2018-21", "2022-25")
        if h == 20:
            # graded 90-day return -> 20d unusual move (momentum)
            gr = g.dropna(subset=["r90"]).copy()
            gr["q90"] = pd.qcut(gr["r90"], 5, labels=False)
            out["f20 unusual by r90 quintile"] = tab(gr, "u", ["q90"])
            out["f20 unusual by r90 quintile x half"] = tab(gr, "u", ["half","q90"])
            rr = stats.spearmanr(gr["r90"], gr["u"])
            out["spearman r90 vs f20u"] = f"rho={rr[0]:.4f} p={rr[1]:.4g} n={len(gr)}"
            # dips in rising coins
            gd = g[g["regime"] == "trending"].copy()
            gd["zb"] = pd.cut(gd["z"], [-np.inf, -1, 0, np.inf])
            out["trending f20u by z bucket x half"] = tab(gd, "u", ["half","zb"])
            gd2 = g[g["regime"] == "mean_reversion"].copy()
            gd2["zb"] = pd.cut(gd2["z"], [-np.inf, -1, 0, 1, np.inf])
            out["MR f20u by z bucket x half"] = tab(gd2, "u", ["half","zb"])
        else:
            gt = g[g["regime"] == "trending"].copy()
            gt["zb"] = pd.cut(gt["z"], [-np.inf, 0, 1, 2, np.inf])
            out["trending f5u by z x half"] = tab(gt, "u", ["half","zb"])
            gt2 = gt[gt["z"] > 0]
            rr = stats.spearmanr(gt2["z"], gt2["u"])
            out["trending z>0 spearman z vs f5u"] = f"rho={rr[0]:.4f} p={rr[1]:.4g} n={len(gt2)}"
            gm = g[g["regime"] == "mean_reversion"].copy()
            gm["zb"] = pd.cut(gm["z"], [-np.inf, 0, 1, 2, np.inf])
            out["MR f5u by z x half"] = tab(gm, "u", ["half","zb"])
    return out
