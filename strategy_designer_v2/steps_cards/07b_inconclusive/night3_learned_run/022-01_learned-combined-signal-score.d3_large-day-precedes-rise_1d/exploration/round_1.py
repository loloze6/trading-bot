def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [1, 2, 5, 10, 20]
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
                    rows.append((coin, w, int(w[1:]), yr[t], h, f[t], r1[t], c[t + h] / c[t] - 1))
    d = pd.DataFrame(rows, columns=["coin", "w", "wn", "yr", "h", "f", "r1", "fr"])
    d["drift"] = d.groupby(["coin", "h"])["fr"].transform("mean")
    d["ex"] = d["fr"] - d["drift"]
    d = d.dropna(subset=["f", "ex"])

    def tb(g):
        g = g.sort_values("f", kind="stable")
        k = len(g) // 3
        if k < 5:
            return pd.Series({"n": len(g), "diff": np.nan, "t": np.nan, "top": np.nan})
        lo, hi = g["ex"].iloc[:k], g["ex"].iloc[-k:]
        t = stats.ttest_ind(hi, lo, equal_var=False).statistic
        return pd.Series({"n": len(g), "diff": hi.mean() - lo.mean(), "t": t, "top": hi.mean()})

    out = {}
    out["by_horizon"] = d.groupby("h").apply(tb)
    d5 = d[d.h == 5].copy()
    out["h5_by_coin"] = d5.groupby("coin").apply(tb)
    out["h5_by_year"] = d5.groupby("yr").apply(tb)
    d5["sign"] = np.where(d5["r1"] > 0, "up", "down")
    d5["fq"] = pd.qcut(d5["f"].rank(method="first"), 5, labels=False)
    out["h5_quintile_sign_mean_ex"] = d5.pivot_table(index="fq", columns="sign", values="ex", aggfunc="mean")
    out["h5_quintile_sign_n"] = d5.pivot_table(index="fq", columns="sign", values="ex", aggfunc="count")
    out["h5_quintile_f_mean"] = d5.groupby("fq")["f"].mean()
    # signed regression: ex on up part and down part
    for h in [5, 10, 20]:
        g = d[d.h == h].copy()
        x = g["f"] * np.sign(g["r1"])
        up = g[g.r1 > 0]; dn = g[g.r1 <= 0]
        su = stats.linregress(up["f"], up["ex"]); sd = stats.linregress(dn["f"], dn["ex"])
        out[f"slope_h{h}"] = pd.Series({"up_slope": su.slope, "up_t": su.slope / su.stderr, "n_up": len(up),
                                        "down_slope": sd.slope, "down_t": sd.slope / sd.stderr, "n_dn": len(dn)})
    # top third: largest |x| split by sign, vs bottom third
    g = d5.sort_values("f", kind="stable"); k = len(g) // 3
    lo = g.iloc[:k]; hi = g.iloc[-k:]
    res = {}
    for s in ["up", "down"]:
        hs = hi[hi.sign == s]["ex"]
        res[s] = pd.Series({"n": len(hs), "mean": hs.mean(),
                            "t_vs_bottom": stats.ttest_ind(hs, lo["ex"], equal_var=False).statistic})
    out["h5_top_by_sign"] = pd.DataFrame(res)
    # market regime: prior 60-day trend of coin? use window mean ex - not allowed. use sign of 20d past return
    return out
