def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 2, 3, 5]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            f = df["forecast"].values.astype(float)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for h in H:
                for t in range(0, n - h, h):
                    rows.append((coin, w, yr[t], h, f[t], r1[t], c[t + h] / c[t] - 1))
    d = pd.DataFrame(rows, columns=["coin", "w", "yr", "h", "f", "r1", "fr"])
    d["drift"] = d.groupby(["coin", "h"])["fr"].transform("mean")
    d["sd"] = d.groupby(["coin", "h"])["fr"].transform("std")
    d["ex"] = d["fr"] - d["drift"]
    d = d.dropna(subset=["f", "ex", "r1"])
    d["sign"] = np.where(d["r1"] > 0, "up", "down")

    def tb(g):
        g = g.sort_values("f", kind="stable"); k = len(g) // 3
        if k < 5:
            return pd.Series({"n": len(g), "diff": np.nan, "t": np.nan})
        lo, hi = g["ex"].iloc[:k], g["ex"].iloc[-k:]
        return pd.Series({"n": len(g), "diff": hi.mean() - lo.mean(),
                          "t": stats.ttest_ind(hi, lo, equal_var=False).statistic})
    out = {}
    d5 = d[d.h == 5]
    out["h5_without_ZEC"] = tb(d5[d5.coin != "ZECUSD"])
    # up side only: graded by size of the up move
    up = d5[d5.sign == "up"]
    out["h5_up_by_coin"] = up.groupby("coin").apply(tb)
    out["h5_up_by_year"] = up.groupby("yr").apply(tb)
    out["h5_up_all"] = tb(up)
    dn = d5[d5.sign == "down"]
    out["h5_down_all"] = tb(dn)
    # size per case of top third by horizon (unusual, total, strength)
    sz = {}
    for h in H:
        g = d[d.h == h].sort_values("f", kind="stable"); k = len(g) // 3
        hi = g.iloc[-k:]
        upi = g[g.sign == "up"].sort_values("f", kind="stable"); ku = len(upi) // 3
        hu = upi.iloc[-ku:]
        sz[h] = pd.Series({"top_unusual": hi["ex"].mean(), "top_total": hi["fr"].mean(),
                           "top_strength": (hi["ex"] / hi["sd"]).mean(),
                           "upTop_unusual": hu["ex"].mean(), "upTop_total": hu["fr"].mean(),
                           "upTop_strength": (hu["ex"] / hu["sd"]).mean(), "n_upTop": ku})
    out["size_by_h"] = pd.DataFrame(sz)
    return out
