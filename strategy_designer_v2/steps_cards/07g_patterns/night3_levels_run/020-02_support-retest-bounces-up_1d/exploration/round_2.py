def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dl.append(d)
    D = pd.concat(dl, ignore_index=True).dropna(subset=["coin_return"])
    dt = pd.to_datetime(D["day"])
    D["wd"] = dt.dt.dayofweek; D["yr"] = dt.dt.year
    D["sat"] = (D.wd == 5)
    D["frisat"] = D.wd.isin([4, 5])
    out = {}
    # per coin: Saturday mean vs other days
    pc = []
    for coin, s in D.groupby("coin"):
        a = s[s.sat]["coin_return"]; b = s[~s.sat]["coin_return"]
        pc.append({"coin": coin, "sat_mean": a.mean(), "other_mean": b.mean(), "n_sat": len(a),
                   "t_sat_minus_other": stats.ttest_ind(a, b, equal_var=False).statistic,
                   "sat_share_up": (a > 0).mean(), "other_share_up": (b > 0).mean()})
    out["sat_by_coin"] = pd.DataFrame(pc).set_index("coin")
    # per year (pooled coins), Saturday minus other
    py = []
    for yr, s in D.groupby("yr"):
        a = s[s.sat]["coin_return"]; b = s[~s.sat]["coin_return"]
        py.append({"yr": yr, "sat_mean": a.mean(), "other_mean": b.mean(), "n_sat": len(a),
                   "t": stats.ttest_ind(a, b, equal_var=False).statistic})
    out["sat_by_year"] = pd.DataFrame(py).set_index("yr")
    # per window: share of windows where Saturday mean > other mean, averaged over coins (BTC only to keep independent)
    pw = []
    for w, s in D.groupby("win"):
        a = s[s.sat]["coin_return"]; b = s[~s.sat]["coin_return"]
        pw.append(a.mean() - b.mean())
    pw = pd.Series(pw)
    out["sat_minus_other_windows"] = pd.Series({"n_windows": len(pw), "share_pos": (pw > 0).mean(),
                                                 "mean": pw.mean(), "t_over_windows": pw.mean() / (pw.std() / np.sqrt(len(pw)))})
    # cross-coin average per day (to handle correlation): one value per day
    M = D.groupby(["day", "wd"])["coin_return"].mean().reset_index()
    a = M[M.wd == 5]["coin_return"]; b = M[M.wd != 5]["coin_return"]
    out["sat_daily_avg_of_coins"] = pd.Series({"n_sat_days": len(a), "sat_mean": a.mean(), "other_mean": b.mean(),
                                                "t": stats.ttest_ind(a, b, equal_var=False).statistic,
                                                "t_sat_alone": a.mean() / (a.std() / np.sqrt(len(a)))})
    wdm = M.groupby("wd")["coin_return"].agg(["mean", "std", "count"])
    wdm["t"] = wdm["mean"] / (wdm["std"] / np.sqrt(wdm["count"]))
    out["weekday_avg_of_coins"] = wdm
    # graded: Saturday return vs the week's (prior 5 days) return, per coin pooled
    rows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy().reset_index(drop=True)
            d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek
            d["past5"] = d["close"] / d["close"].shift(5) - 1
            d["past5"] = d["past5"].shift(1)
            d["coin"] = coin
            rows.append(d[d.wd == 5].dropna(subset=["coin_return", "past5"]))
    S = pd.concat(rows)
    rho, p = stats.spearmanr(S["past5"], S["coin_return"])
    out["sat_vs_prior_week"] = pd.Series({"n": len(S), "rho": rho, "p": p})
    # range/abs move by weekday
    out["abs_by_wd"] = D.groupby("wd")["coin_return"].apply(lambda x: x.abs().mean())
    # book return by weekday
    bk = D.dropna(subset=["book_return"]).groupby("wd")["book_return"].agg(["mean", "count"])
    out["book_by_wd"] = bk
    return out
