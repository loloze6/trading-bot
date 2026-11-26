def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [10, 20]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            fc = df["forecast"].fillna(0).values
            n = len(df)
            ts = df["timestamp"].astype(str).str[:10].values
            for s in range(0, n, 10):
                for i in range(s, min(s + 10, n)):
                    prev = fc[i - 1] if i > 0 else 0.0
                    if fc[i] - prev >= 2 and fc[i] > 0:
                        r = {"coin": c, "win": w, "day": ts[i]}
                        r["ret20"] = cl[i] / cl[i - 20] - 1 if i >= 20 else np.nan
                        r["ret10"] = cl[i] / cl[i - 10] - 1 if i >= 10 else np.nan
                        r["over"] = cl[i] / cl[max(0, i - 60):i].max() - 1 if i >= 20 else np.nan
                        r["pos60"] = ((cl[i] - cl[max(0, i - 60):i].min()) / (cl[max(0, i - 60):i].max() - cl[max(0, i - 60):i].min())) if i >= 20 else np.nan
                        for h in H:
                            r["u%d" % h] = (cl[i + h] / cl[i] - 1 - drift[(c, h)]) if i + h < n else np.nan
                        rows.append(r)
                        break
    d = pd.DataFrame(rows)
    def pooled_t(g, col):
        x = g.dropna(subset=[col])
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean": m, "t_pooled": m / se})
    out = {}
    out["all"] = pd.DataFrame({h: pooled_t(d, "u%d" % h) for h in H}).T
    for v in ["ret20", "ret10", "over"]:
        dd = d.dropna(subset=[v, "u10"])
        sp10 = stats.spearmanr(dd[v], dd["u10"])
        dd2 = d.dropna(subset=[v, "u20"])
        sp20 = stats.spearmanr(dd2[v], dd2["u20"])
        out["spearman_" + v] = pd.DataFrame({"rho": [sp10.statistic, sp20.statistic], "p": [sp10.pvalue, sp20.pvalue]}, index=["u10", "u20"])
        q = pd.qcut(d[v], 2, labels=["lowhalf", "highhalf"])
        out["halves_" + v] = d.groupby(q).apply(lambda g: pooled_t(g, "u10"))
        lo = d.loc[q == "lowhalf", "u10"].dropna(); hi = d.loc[q == "highhalf", "u10"].dropna()
        out["welch_low_minus_high_" + v] = float(stats.ttest_ind(lo, hi, equal_var=False).statistic)
    out["ret20_edges"] = d["ret20"].quantile([0, .5, 1]).to_frame()
    out["leave_coin_out_u10"] = pd.DataFrame({c: pooled_t(d[d.coin != c], "u10") for c in d.coin.unique()}).T
    return out
