def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    feats_all = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; rng = (b["high"] - b["low"]) / c
            f = pd.DataFrame({
                "r1": c.pct_change(1), "r3": c.pct_change(3), "r7": c.pct_change(7),
                "r3s": c.pct_change(3) / rng.rolling(30).mean(),
                "dist20hi": c / b["high"].rolling(20).max() - 1,
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "volrel": b["volume"] / b["volume"].rolling(30).mean(),
                "inprof": (b["regime"] == "unknown").astype(int),
                "alloc": b["postRebalance_current_allocation"],
                "pos": np.arange(len(b)),
            })
            for H in [1, 3, 5]:
                f["fwd%d" % H] = c.shift(-H) / c - 1
            f["coin"] = coin; f["w"] = w; f["wn"] = int(w[1:])
            feats_all.append(f)
    d = pd.concat(feats_all, ignore_index=True)
    drift = {}
    for H in [1, 3, 5]:
        for coin in d["coin"].unique():
            q = d[(d["coin"] == coin) & (d["pos"] % H == 0)]
            drift[(coin, H)] = q["fwd%d" % H].mean()
    p = d[d["inprof"] == 1]
    res = []
    for feat in ["r1", "r3", "r3s", "r7", "dist20hi", "clv", "volrel"]:
        for H in [1, 3, 5]:
            for off in range(H):
                g = p[(p["pos"] % H) == off].dropna(subset=[feat, "fwd%d" % H]).copy()
                g["su"] = -(g["fwd%d" % H] - g["coin"].map(lambda k: drift[(k, H)]))
                rr = stats.spearmanr(g[feat], g["su"])
                sl = stats.linregress(g[feat], g["su"])
                res.append({"feat": feat, "H": H, "off": off, "n": len(g),
                            "rho": rr.correlation, "slope_t": sl.slope / sl.stderr})
    R = pd.DataFrame(res)
    out = {"rho_by_offset": R.groupby(["feat", "H"])[["n", "rho", "slope_t"]].mean()}
    # r3 detail H=3, all offsets pooled (overlapping, descriptive), by tercile and window half
    g = p.dropna(subset=["r3", "fwd3"]).copy()
    g["su"] = -(g["fwd3"] - g["coin"].map(lambda k: drift[(k, 3)]))
    g["r3q"] = pd.qcut(g["r3"], 3, labels=False)
    g["half"] = np.where(g["wn"] <= 12, "w1-12", "w13-18")
    out["r3_tercile_by_half"] = g.groupby(["half", "r3q"])["su"].agg(["count", "mean"])
    out["r3_tercile_by_coin"] = g.groupby(["coin", "r3q"])["su"].agg(["count", "mean"])
    # falls only: graded?
    fl = g[g["r3"] < 0]
    sl = stats.linregress(-fl["r3"], fl["su"])
    out["falls_only_slope_t_overlap"] = sl.slope / sl.stderr
    out["falls_only_n"] = len(fl)
    # book: days of largest gains/losses, what preceded
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; dd.append(x)
    D = pd.concat(dd)
    D = D[D["book_return"].abs() > 0]
    out["book_days_n"] = len(D)
    out["book_ret_top_bottom"] = pd.Series({"top5pct_mean": D["book_return"].quantile(0.95),
                                            "bottom5pct": D["book_return"].quantile(0.05),
                                            "mean": D["book_return"].mean()})
    return out
