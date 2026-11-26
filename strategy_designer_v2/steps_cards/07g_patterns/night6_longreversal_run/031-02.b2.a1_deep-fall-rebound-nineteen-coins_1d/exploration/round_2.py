def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    dl = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            d = df.dropna(subset=["coin_return"]).copy()
            d["coin"] = coin; d["win"] = w
            d["day"] = pd.to_datetime(d["day"])
            dl.append(d[["coin", "win", "day", "coin_return", "book_return"]])
    D = pd.concat(dl)
    D["wd"] = D["day"].dt.weekday
    D["yr"] = D["day"].dt.year
    # day-clustered: mean over coins per day, then t over days
    dm = D.groupby("day").agg(r=("coin_return", "mean"), b=("book_return", "mean")).reset_index()
    dm["wd"] = dm["day"].dt.weekday; dm["yr"] = dm["day"].dt.year
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan))
    out["wd_dayclustered"] = dm.groupby("wd")["r"].apply(tt).unstack()
    # demeaned by day-of-sample overall mean: weekday minus other days, Welch
    res = {}
    for wd in range(7):
        a = dm.loc[dm.wd == wd, "r"]; b = dm.loc[dm.wd != wd, "r"]
        res[wd] = stats.ttest_ind(a, b, equal_var=False).statistic
    out["wd_minus_rest_welch_t"] = pd.Series(res)
    # by year: Wed+Fri+Sat minus other days mean
    dm["grp"] = dm.wd.isin([2, 4, 5])
    yy = dm.groupby(["yr", "grp"])["r"].mean().unstack()
    yy["diff"] = yy[True] - yy[False]
    yy["n_days"] = dm.groupby("yr").size()
    out["wfs_minus_rest_by_year"] = yy
    # per coin, own bars: weekday means (Sat and Thu)
    pc = D.groupby(["coin", "wd"])["coin_return"].mean().unstack()
    out["per_coin_weekday_mean"] = pc
    out["per_coin_share_sat_positive"] = (pc[5] > pc.drop(columns=5).mean(axis=1)).mean()
    # by window halves stability: window number
    D["wn"] = D["win"].str[1:].astype(int)
    dm2 = D.groupby(["day"]).agg(r=("coin_return", "mean"), wn=("wn", "first")).reset_index()
    dm2["wd"] = dm2["day"].dt.weekday
    dm2["half"] = np.where(dm2.wn <= 12, "w1-12", "w13-24")
    out["wd_by_half"] = dm2.groupby(["half", "wd"])["r"].mean().unstack()
    # Book: largest falls context - book drawdown by year
    bb = dm.dropna(subset=["b"])
    out["book_by_year"] = bb.groupby("yr")["b"].agg(["count", "mean", "std", "min", "sum"])
    # inside-regime cases: fall30 contribution vs fall90 at grid h30
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True); c = df["close"].values
            for i in range(0, len(c) - 30, 30):
                if df["forecast"].iloc[i] > 0:
                    rows.append(dict(f90=df["debug_info.components.fall90.post_pipeline_value"].iloc[i],
                                     f30=df["debug_info.components.fall30.post_pipeline_value"].iloc[i],
                                     fr=c[i + 30] / c[i] - 1,
                                     r7=c[i] / c[i - 7] - 1 if i >= 7 else np.nan))
    C = pd.DataFrame(rows)
    out["cases_n"] = len(C)
    out["case_corr_spearman"] = pd.Series(dict(
        f90=stats.spearmanr(C.f90, C.fr, nan_policy="omit").correlation,
        f30=stats.spearmanr(C.f30, C.fr, nan_policy="omit").correlation,
        r7=stats.spearmanr(C.r7, C.fr, nan_policy="omit").correlation))
    C["f30pos"] = C.f30 > 0
    out["cases_by_f30_pos"] = C.groupby("f30pos")["fr"].agg(["count", "mean"])
    return out
