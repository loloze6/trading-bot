def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            f = pd.DataFrame({"coin": coin, "w": w, "r1": c.pct_change(),
                              "wd": ts.dt.weekday, "yr": ts.dt.year,
                              "fc": b["forecast"].astype(float),
                              "run": b.get("debug_info.components.runup.post_pipeline_value", pd.Series(np.nan, index=b.index)).astype(float),
                              "brk": b.get("debug_info.components.break.post_pipeline_value", pd.Series(np.nan, index=b.index)).astype(float),
                              "fwd5": c.shift(-5) / c - 1,
                              "fwd10": c.shift(-10) / c - 1,
                              "ret20": c / c.shift(20) - 1,
                              "cell": np.arange(len(c)) // 5})
            rows.append(f)
    g = pd.concat(rows, ignore_index=True)
    d = g.dropna(subset=["r1"]).copy()
    d["u1"] = d["r1"] - d.groupby("coin")["r1"].transform("mean")
    def tt(s):
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s)))})
    out["daily_by_weekday"] = d.groupby("wd")["u1"].apply(tt).unstack().round(4)
    out["daily_wd_by_coin"] = d.groupby(["coin", "wd"])["u1"].mean().unstack().round(4)
    d["half"] = np.where(d["yr"] <= 2021, "early", "late")
    out["daily_wd_by_half"] = d.groupby(["half", "wd"])["u1"].mean().unstack().round(4)
    out["daily_wd_by_year_mon_tue_minus_rest"] = d.groupby("yr").apply(
        lambda x: x[x.wd.isin([0, 1])]["u1"].mean() - x[~x.wd.isin([0, 1])]["u1"].mean()).round(4)
    # on cases: run-up grading
    grid5 = g.dropna(subset=["fwd5"])
    drift = grid5[grid5.index.isin(grid5.groupby(["coin", "w", "cell"]).head(1).index)].groupby("coin")["fwd5"].mean()
    on = grid5[grid5.fc > 0].groupby(["coin", "w", "cell"]).head(1).dropna(subset=["run", "ret20"]).copy()
    on["unus"] = on["fwd5"] - on["coin"].map(drift)
    on["rq"] = pd.qcut(on["ret20"].rank(method="first"), 3, labels=False)
    out["on_by_ret20_tercile"] = on.groupby("rq").apply(lambda x: pd.concat([tt(x["unus"]), pd.Series({"ret20_med": x["ret20"].median()})])).round(4)
    top, bot = on[on.rq == 2]["unus"], on[on.rq == 0]["unus"]
    out["on_ret20_top_minus_bot"] = pd.Series({"diff": top.mean() - bot.mean(),
        "welch_t": stats.ttest_ind(top, bot, equal_var=False).statistic,
        "rho_ret20": stats.spearmanr(on["ret20"], on["unus"]).correlation}).round(4)
    out["on_ret20_tercile_by_coin"] = on.groupby(["coin", "rq"])["unus"].mean().unstack().round(4)
    on["half"] = np.where(on["yr"] <= 2021, "early", "late")
    out["on_ret20_tercile_by_half"] = on.groupby(["half", "rq"])["unus"].mean().unstack().round(4)
    return out
