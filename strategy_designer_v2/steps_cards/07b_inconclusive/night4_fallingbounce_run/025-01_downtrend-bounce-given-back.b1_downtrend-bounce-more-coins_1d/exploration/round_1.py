def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    recs = []      # bar-level rows with features and forward returns
    drift = {}     # coin -> {h: mean non-overlapping h-return}
    for coin, wins in bars.items():
        dr = {h: [] for h in H}
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=20).std()
            z = r1 / vol
            r90 = c / c.shift(90) - 1
            down = r90 < 0
            down = down.where(r90.notna(), df["regime"] == "mean_reversion")
            fc = df["forecast"].astype(float)
            for h in H:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n - h, h)
                dr[h].extend(fwd.iloc[idx].dropna().tolist())
            year = pd.to_datetime(df["timestamp"]).dt.year
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n), "z": z, "down": down,
                              "fc": fc, "year": year, "r90": r90})
            for h in H:
                d[f"f{h}"] = c.shift(-h) / c - 1
            recs.append(d)
        drift[coin] = {h: np.mean(v) if v else np.nan for h, v in dr.items()}
    A = pd.concat(recs, ignore_index=True)
    for h in H:
        A[f"u{h}"] = -(A[f"f{h}"] - A["coin"].map(lambda k: drift[k][h]))  # short-direction unusual
    # cases: first bar per 5-grid cell with forecast <= -2
    A["cell"] = A["pos"] // 5
    cs = A[(A["fc"] <= -2) & A["f5"].notna()].groupby(["coin", "win", "cell"]).head(1)
    out = {}
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["cases_overall_by_h"] = pd.DataFrame({f"h{h}": summ(cs, f"u{h}") for h in H}).T
    # baseline: all down-regime bars on 5-grid (no bounce condition)
    g5 = A[(A["pos"] % 5 == 0)]
    out["baseline_grid_down_vs_up_u5"] = pd.DataFrame({"down": summ(g5[g5["down"] == True]),
                                                       "notdown": summ(g5[g5["down"] == False])}).T
    # down-regime grid bars by z bin (any day, incl falls)
    gd = g5[g5["down"] == True].copy()
    gd["zbin"] = pd.cut(gd["z"], [-np.inf, -2, -1, 0, 1, 2, 3, np.inf])
    out["down_grid_u5_by_z"] = gd.groupby("zbin", observed=True).apply(summ)
    gu = g5[g5["down"] == False].copy()
    gu["zbin"] = pd.cut(gu["z"], [-np.inf, -2, -1, 0, 1, 2, 3, np.inf])
    out["notdown_grid_u5_by_z"] = gu.groupby("zbin", observed=True).apply(summ)
    cs = cs.copy()
    cs["fbin"] = pd.qcut(cs["fc"].abs(), 4, duplicates="drop")
    out["cases_by_forecast_quartile"] = cs.groupby("fbin", observed=True).apply(summ)
    cs["zbin"] = pd.cut(cs["z"], [-np.inf, 0, 1, 2, 3, np.inf])
    out["cases_by_z"] = cs.groupby("zbin", observed=True).apply(summ)
    out["cases_by_year"] = cs.groupby("year").apply(summ)
    out["cases_by_coin"] = cs.groupby("coin").apply(summ)
    cs["r90bin"] = pd.qcut(cs["r90"], 4, duplicates="drop")
    out["cases_by_r90_quartile"] = cs.groupby("r90bin", observed=True).apply(summ)
    # total move (raw) in cases
    out["cases_raw_f5_mean%"] = 100 * cs["f5"].mean()
    out["corr_absfc_u5"] = float(np.corrcoef(cs["fc"].abs(), cs["u5"])[0, 1])
    return out
