def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        per = []
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; hi = b["high"]; lo = b["low"]
            b["r42"] = c / c.shift(42) - 1
            b["r6"] = c / c.shift(6) - 1
            b["dn"] = c < lo.shift(1).rolling(12).min()
            b["up"] = c > hi.shift(1).rolling(12).max()
            rng = (hi.rolling(12).max() - lo.rolling(12).min()) / c
            b["narrow"] = np.log(rng / rng.rolling(120, min_periods=60).mean())
            b["r120"] = c / c.shift(120) - 1
            for H in (6, 18, 36):
                b["f%d" % H] = c.shift(-H) / c - 1
            b["pos"] = np.arange(len(b)); b["win"] = w; b["coin"] = coin
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            per.append(b)
        a = pd.concat(per)
        for H in (6, 18, 36):
            g = a[a["pos"] % H == 0]["f%d" % H].dropna()
            a["adj%d" % H] = a["f%d" % H] - g.mean()
            a["z%d" % H] = a["adj%d" % H] / g.std()
        a["cell"] = a["pos"] // 18
        # coin-standardised past returns
        g18 = a[a["pos"] % 18 == 0]
        a["r42z"] = a["r42"] / g18["r42"].std()
        a["r6z"] = a["r6"] / g18["r6"].std()
        rows.append(a)
    A = pd.concat(rows, ignore_index=True)
    def summ(x, H=18):
        v = x["adj%d" % H].dropna(); n = len(v)
        return pd.Series({"n": n, "mean_adj": v.mean(), "t": v.mean() / (v.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "strength": x["z%d" % H].mean(), "coins_pos": x.groupby("coin")["adj%d" % H].mean().gt(0).sum(),
                          "coins": x["coin"].nunique()})
    # 1. breakdown after falling week, coin-standardised quintiles
    f = A[A["dn"] & (A["r42"] < 0) & A["f18"].notna()].groupby(["coin", "win", "cell"]).head(1).copy()
    f["q"] = pd.qcut(f["r42z"], 5, labels=False)
    out["dnfall_by_r42z_q"] = f.groupby("q").apply(summ)
    out["dnfall_spearman_r42z_vs_adj18"] = pd.Series(stats.spearmanr(f["r42z"], f["adj18"])[:2], index=["rho", "p"])
    d0 = f[f["q"] == 0]
    out["dnfall_q0_by_year"] = d0.groupby("year").apply(summ)
    out["dnfall_q0_horizons"] = pd.DataFrame({H: summ(d0.dropna(subset=["adj%d" % H]), H) for H in (6, 18, 36)}).T
    # 2. all grid bars: deep falling week, graded by r42z, regardless of breakdown
    G = A[(A["pos"] % 18 == 0) & A["f18"].notna()].dropna(subset=["r42z"]).copy()
    G["q"] = pd.qcut(G["r42z"], 10, labels=False)
    out["grid_by_r42z_decile"] = G.groupby("q").apply(summ)
    G["q6"] = pd.qcut(G["r6z"], 5, labels=False)
    out["grid_r6z_q0_by_year"] = G[G["q6"] == 0].groupby("year").apply(summ)
    # 3. narrow range: by year, and controlled by long trend
    x = G.dropna(subset=["narrow", "r120"]).copy()
    x["nq"] = x.groupby("coin")["narrow"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["narrow_q0_by_year"] = x[x["nq"] == 0].groupby("year").apply(summ)
    x["trend"] = np.where(x["r120"] > 0, "up20d", "down20d")
    out["narrow_q_by_trend"] = x.groupby(["trend", "nq"]).apply(summ)
    return out
