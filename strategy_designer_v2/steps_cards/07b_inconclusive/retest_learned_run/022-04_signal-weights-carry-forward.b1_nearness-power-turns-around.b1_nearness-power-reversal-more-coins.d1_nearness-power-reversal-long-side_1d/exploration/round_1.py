def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    fc_col = "debug_info.components.power_reversal.last_history_value"
    rows = []
    coinmean = {}
    H = [1, 3, 5, 10, 20]
    for coin, wins in data["bars"].items():
        allr = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                allr[h].extend(list(c[idx + h] / c[idx] - 1))
        coinmean[coin] = {h: np.mean(allr[h]) if len(allr[h]) else np.nan for h in H}
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            raw = df[fc_col].values if fc_col in df else np.full(len(df), np.nan)
            n = len(c)
            idx = np.arange(0, n - 5, 5)
            for i in idx:
                r = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "f": f[i], "raw": raw[i]}
                for h in H:
                    r["ex%d" % h] = (c[i + h] / c[i] - 1 - coinmean[coin][h]) if i + h < n else np.nan
                # past 60 day return as regime
                r["past60"] = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    pos = d[d["f"] > 0].copy()
    neg = d[d["f"] <= 0]
    def tstat(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["pos_vs_flat_by_h"] = pd.DataFrame({("pos_ex%d" % h): tstat(pos["ex%d" % h]) for h in H} | {("flat_ex%d" % h): tstat(neg["ex%d" % h]) for h in H}).T
    out["pos_by_coin"] = pos.groupby("coin")["ex5"].apply(tstat).unstack()
    out["pos_by_year"] = pos.groupby("year")["ex5"].apply(tstat).unstack()
    pos["fq"] = pd.qcut(pos["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["pos_by_fq"] = pos.groupby("fq")["ex5"].apply(tstat).unstack()
    # branch: which raw component sign drives: excess power sign unknown; use past60 regime
    pos["reg"] = np.where(pos["past60"] > 0, "up60", "down60")
    out["pos_by_past60"] = pos.groupby("reg")["ex5"].apply(tstat).unstack()
    neg2 = neg.copy(); neg2["reg"] = np.where(neg2["past60"] > 0, "up60", "down60")
    out["flat_by_past60"] = neg2.groupby("reg")["ex5"].apply(tstat).unstack()
    out["pos_minus_flat_welch_ex5"] = float(stats.ttest_ind(pos["ex5"].dropna(), neg["ex5"].dropna(), equal_var=False).statistic)
    out["share_pos"] = len(pos) / len(d)
    return out
