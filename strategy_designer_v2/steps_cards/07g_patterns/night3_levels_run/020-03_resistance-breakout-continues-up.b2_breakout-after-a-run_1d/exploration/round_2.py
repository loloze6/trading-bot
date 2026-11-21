def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = [5, 10, 20]
    recs = {h: [] for h in H}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            base = pd.DataFrame({
                "coin": coin, "w": w,
                "fc": b["forecast"].astype(float),
                "brk": b.get("debug_info.components.break.post_pipeline_value", pd.Series(np.nan, index=b.index)).astype(float),
                "run": b.get("debug_info.components.runup.post_pipeline_value", pd.Series(np.nan, index=b.index)).astype(float),
                "dist30l": c / c.rolling(30).min() - 1,
                "dist90l": c / c.rolling(90, min_periods=30).min() - 1,
                "ret60": c / c.shift(60) - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            for h in H:
                f = base.copy()
                f["fwd"] = c.shift(-h) / c - 1
                f["cell"] = np.arange(len(f)) // h
                f["pos"] = np.arange(len(f)) % h
                recs[h].append(f)
    res_on = {}
    res_grid = {}
    for h in H:
        g = pd.concat(recs[h], ignore_index=True)
        grid = g[g["pos"] == 0].dropna(subset=["fwd"]).copy()
        drift = grid.groupby("coin")["fwd"].mean()
        usual = grid.groupby("coin")["fwd"].std()
        g["unus"] = g["fwd"] - g["coin"].map(drift)
        g["str"] = g["unus"] / g["coin"].map(usual)
        grid["unus"] = grid["fwd"] - grid["coin"].map(drift)
        grid["str"] = grid["unus"] / grid["coin"].map(usual)
        on = g[(g["fc"] > 0)].dropna(subset=["fwd"]).groupby(["coin", "w", "cell"]).head(1)
        res_on[h] = {"n": len(on), "unus": on["unus"].mean(), "t": on["unus"].mean() / (on["unus"].std() / np.sqrt(len(on))),
                     "strength": on["str"].mean(), "total": on["fwd"].mean()}
        # component grading among on cases
        if h == 5:
            oc = on.dropna(subset=["brk", "run"])
            out["on5_spearman"] = pd.Series({
                "rho_brk": stats.spearmanr(oc["brk"], oc["unus"]).correlation,
                "rho_run": stats.spearmanr(oc["run"], oc["unus"]).correlation,
                "rho_fc": stats.spearmanr(oc["fc"], oc["unus"]).correlation,
                "rho_dist90l": stats.spearmanr(oc["dist90l"], oc["unus"], nan_policy="omit").correlation,
                "n": len(oc)}).round(3)
            oc = oc.copy()
            oc["rq"] = pd.qcut(oc["run"].rank(method="first"), 3, labels=False)
            out["on5_by_run_tercile"] = oc.groupby("rq")["unus"].agg(["size", "mean"]).round(4)
            oc["bq"] = pd.qcut(oc["brk"].rank(method="first"), 3, labels=False)
            out["on5_by_brk_tercile"] = oc.groupby("bq")["unus"].agg(["size", "mean"]).round(4)
        for col in ["dist30l", "dist90l", "ret60"]:
            d = grid.dropna(subset=[col]).copy()
            d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
            top, bot = d[d.q == 4]["unus"], d[d.q == 0]["unus"]
            res_grid[(col, h)] = {"n_top": len(top), "top": top.mean(), "bot": bot.mean(),
                                  "t_topbot": stats.ttest_ind(top, bot, equal_var=False).statistic,
                                  "rho": stats.spearmanr(d[col], d["unus"]).correlation}
        if h == 5:
            grid["half"] = np.where(grid["yr"] <= 2021, "early", "late")
            out["weekday_by_half"] = grid.groupby(["half", "wd"])["unus"].mean().unstack().round(4)
            grid["monTue"] = grid["wd"].isin([0, 1])
            out["montue_by_coin"] = grid.groupby(["coin", "monTue"])["unus"].mean().unstack().round(4)
    out["on_by_horizon"] = pd.DataFrame(res_on).T.round(4)
    out["grid_features"] = pd.DataFrame(res_grid).T.round(4)
    return out
