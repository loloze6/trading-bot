def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def tstat(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    for H in [5, 10, 20]:
        rows = []
        for coin, wins in data["bars"].items():
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                allr.extend(list(c[idx + H] / c[idx] - 1))
            m = np.mean(allr)
            for w, df in wins.items():
                c = df["close"].values; f = df["forecast"].values
                idx = np.arange(0, len(c) - H, H)
                for i in idx:
                    rows.append({"coin": coin, "win": w, "f": f[i], "ex": c[i + H] / c[i] - 1 - m,
                                 "fprev": f[i - H] if i >= H else np.nan})
        d = pd.DataFrame(rows)
        pos = d[d["f"] > 0].copy()
        flat = d[d["f"] <= 0]
        out["H%d_pos" % H] = float(tstat(pos["ex"])["t"])
        out["H%d_pos_mean" % H] = float(pos["ex"].mean())
        out["H%d_npos" % H] = int(len(pos))
        out["H%d_pos_minus_flat_welch" % H] = float(stats.ttest_ind(pos["ex"], flat["ex"], equal_var=False).statistic)
        pos["fq"] = pd.qcut(pos["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
        out["H%d_by_fq" % H] = pos.groupby("fq")["ex"].apply(tstat).unstack()
        # rises of the forecast (new cases) vs continuing
        rise = pos[(pos["f"] > pos["fprev"].fillna(0))]
        out["H%d_rising_cases" % H] = tstat(rise["ex"]).to_frame().T
        wm = pos.groupby("win")["ex"].mean()
        out["H%d_share_windows_positive" % H] = float((wm > 0).mean())
        out["H%d_n_windows" % H] = int(len(wm))
    return out
