def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10]
    recs = []; drift = {}
    for coin, wins in bars.items():
        dr = {h: [] for h in H}
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); n = len(c)
            r1 = c.pct_change(); vol = r1.rolling(20, min_periods=20).std()
            z = r1 / vol
            r90 = c / c.shift(90) - 1
            down = (r90 < 0).where(r90.notna(), df["regime"] == "mean_reversion")
            r5p = c / c.shift(5) - 1
            for h in H:
                fwd = c.shift(-h) / c - 1
                dr[h].extend(fwd.iloc[np.arange(0, n - h, h)].dropna().tolist())
            d = pd.DataFrame({"coin": coin, "pos": np.arange(n), "z": z, "down": down, "r90": r90,
                              "r90v": r90 / (vol * np.sqrt(90)), "r5p": r5p,
                              "year": pd.to_datetime(df["timestamp"]).dt.year,
                              "fc": df["forecast"].astype(float)})
            for h in H:
                d[f"f{h}"] = c.shift(-h) / c - 1
            recs.append(d)
        drift[coin] = {h: np.mean(v) for h, v in dr.items()}
    A = pd.concat(recs, ignore_index=True)
    for h in H:
        A[f"u{h}"] = -(A[f"f{h}"] - A["coin"].map(lambda k: drift[k][h]))
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    g5 = A[(A["pos"] % 5 == 0)].copy()
    gd = g5[g5["down"] == True].copy()
    gu = g5[g5["down"] == False].copy()
    bins = [0, 0.5, 1, 1.5, 2, 2.5, 3, np.inf]
    for nm, g in [("down", gd), ("notdown", gu)]:
        gg = g[g["z"] > 0].copy(); gg["zb"] = pd.cut(gg["z"], bins)
        out[f"{nm}_rises_u5_by_z"] = gg.groupby("zb", observed=True).apply(summ)
        out[f"{nm}_rises_u10_by_z"] = gg.groupby("zb", observed=True).apply(lambda x: summ(x, "u10"))
        s = gg[["z", "u5"]].dropna()
        out[f"{nm}_rises_spearman_z_u5"] = float(stats.spearmanr(s["z"], s["u5"])[0])
        out[f"{nm}_rises_pearson_z_u5"] = float(np.corrcoef(s["z"], s["u5"])[0, 1])
    # down vs notdown difference for z>2
    a = gd[gd["z"] > 2]["u5"].dropna(); b = gu[gu["z"] > 2]["u5"].dropna()
    out["z>2_down_minus_notdown_u5"] = pd.Series({"diff%": 100 * (a.mean() - b.mean()),
                                                  "welch_t": stats.ttest_ind(a, b, equal_var=False)[0],
                                                  "n_down": len(a), "n_notdown": len(b)})
    a = gd[gd["z"] > 1]["u5"].dropna(); b = gu[gu["z"] > 1]["u5"].dropna()
    out["z>1_down_minus_notdown_u5"] = pd.Series({"diff%": 100 * (a.mean() - b.mean()),
                                                  "welch_t": stats.ttest_ind(a, b, equal_var=False)[0],
                                                  "n_down": len(a), "n_notdown": len(b)})
    # down-regime all bars by depth of r90 (momentum) 
    gd["r90b"] = pd.qcut(gd["r90"], 4)
    out["down_allbars_u5_by_r90q"] = gd.groupby("r90b", observed=True).apply(summ)
    # rises in down, z>1, by r90 quartile
    gr = gd[gd["z"] > 1].copy(); gr["r90b"] = pd.qcut(gr["r90"], 3)
    out["down_z>1_u5_by_r90tercile"] = gr.groupby("r90b", observed=True).apply(summ)
    # rises z>1 in down: interaction with prior 5d return (bounce after a short sell-off?)
    gr["r5b"] = pd.qcut(gr["r5p"], 3)
    out["down_z>1_u5_by_prior5d_tercile"] = gr.groupby("r5b", observed=True).apply(summ)
    out["down_z>2_u5_by_year"] = gd[gd["z"] > 2].groupby("year").apply(summ)
    return out
