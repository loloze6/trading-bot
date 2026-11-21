def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 26
    drift = {}
    for c in bars:
        r = []
        for w, df in bars[c].items():
            cl = df["close"].values
            for i in range(0, len(cl) - H, H):
                r.append(cl[i + H] / cl[i] - 1)
        drift[c] = np.mean(r)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            cl = df["close"].values; fc = df["forecast"].values
            s = pd.Series(cl)
            ma100 = s.rolling(100, min_periods=60).mean().values
            n = len(cl)
            for i in range(0, n - H, H):
                if not (fc[i] < 0):
                    continue
                rr = cl[i + H] / cl[i] - 1
                rec = {"coin": c, "absf": abs(fc[i]), "ex": -(rr - drift[c]), "tot": -rr,
                       "pos_in_window": i / n,
                       "past90": cl[i] / cl[i - 90] - 1 if i >= 90 else np.nan,
                       "past60": cl[i] / cl[i - 60] - 1 if i >= 60 else np.nan,
                       "vs_ma100": cl[i] / ma100[i] - 1 if not np.isnan(ma100[i]) else np.nan}
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="ex"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "share_pos": (x > 0).mean()})
    out = {}
    for v in ["past90", "past60", "vs_ma100"]:
        dd = d.dropna(subset=[v]).copy()
        dd["q"] = pd.qcut(dd[v], 3, labels=False, duplicates="drop")
        out[f"by_{v}_tercile"] = dd.groupby("q").apply(summ)
        out[f"{v}_tercile_means"] = dd.groupby("q")[v].mean()
        out[f"spearman_{v}_vs_ex"] = pd.Series(stats.spearmanr(dd[v], dd["ex"])[:2], index=["rho", "p"])
    out["spearman_absf_ex"] = pd.Series(stats.spearmanr(d["absf"], d["ex"])[:2], index=["rho", "p"])
    out["spearman_absf_tot"] = pd.Series(stats.spearmanr(d["absf"], d["tot"])[:2], index=["rho", "p"])
    # thinness within past60 sign
    dd = d.dropna(subset=["past60"]).copy()
    dd["down60"] = dd["past60"] < 0
    out["absf_spearman_by_down60"] = dd.groupby("down60").apply(lambda g: pd.Series({"n": len(g), "rho": stats.spearmanr(g["absf"], g["ex"])[0], "mean": g["ex"].mean(), "t": g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g)))}))
    return out
