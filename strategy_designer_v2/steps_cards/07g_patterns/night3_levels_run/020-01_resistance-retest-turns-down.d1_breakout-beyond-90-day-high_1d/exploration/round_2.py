import pandas as pd, numpy as np
from scipy import stats

def summ_s(x):
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3:
        return pd.Series({"n": n, "mean": np.nan, "t": np.nan, "share_pos": np.nan, "median": np.nan})
    return pd.Series({"n": n, "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)),
                      "share_pos": (x > 0).mean(), "median": x.median()})

def explore(data):
    days = data["days"]; bars = data["bars"]
    out = {}
    dd = []
    for c in days:
        for w, t in days[c].items():
            t = t.copy(); t["coin"] = c; t["win"] = w
            t["prev_ret"] = t["coin_return"].shift(1)
            dd.append(t)
    dd = pd.concat(dd, ignore_index=True)
    dd["dt"] = pd.to_datetime(dd["day"])
    dd["wd"] = dd["dt"].dt.dayofweek
    dd["year"] = dd["dt"].dt.year
    dd["ex"] = dd["coin_return"] - dd.groupby("coin")["coin_return"].transform("mean")
    dd["sat"] = dd["wd"] == 5
    # Saturday minus other days, by year and by coin
    def satdiff(g):
        a = g.loc[g.sat, "ex"].dropna(); b = g.loc[~g.sat, "ex"].dropna()
        t = stats.ttest_ind(a, b, equal_var=False).statistic
        return pd.Series({"n_sat": len(a), "sat_mean": a.mean(), "other_mean": b.mean(), "t_welch": t,
                          "sat_share_pos": (g.loc[g.sat, "coin_return"] > 0).mean()})
    out["sat_by_year"] = dd.groupby("year").apply(satdiff)
    out["sat_by_coin"] = dd.groupby("coin").apply(satdiff)
    out["sat_overall"] = satdiff(dd).to_frame().T
    # weekday x robust stats
    out["weekday_robust"] = dd.groupby("wd")["ex"].apply(summ_s).unstack()
    # Saturday return graded by Friday's return? (prior-day return quintile, on Saturdays vs others)
    e = dd.dropna(subset=["prev_ret", "ex"]).copy()
    e["q"] = e.groupby("coin")["prev_ret"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["next_day_by_prevret_q"] = e.groupby("q")["ex"].apply(summ_s).unstack()
    out["sat_by_prevret_q"] = e[e.sat].groupby("q")["ex"].apply(summ_s).unstack()
    # Saturday return graded by volatility (30-day std of daily returns)
    dd["vol30"] = dd.groupby(["coin", "win"])["coin_return"].transform(lambda s: s.shift(1).rolling(30, min_periods=15).std())
    f = dd[dd.sat].dropna(subset=["vol30", "ex"]).copy()
    f["vq"] = f.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 3, labels=False))
    f["ex_scaled"] = f["ex"] / f["vol30"]
    out["sat_by_vol_tercile"] = f.groupby("vq")["ex"].apply(summ_s).unstack()
    out["sat_scaled_by_vol_tercile"] = f.groupby("vq")["ex_scaled"].apply(summ_s).unstack()
    # weekend: Sat+Sun combined vs weekday, by year
    dd["wkend"] = dd["wd"].isin([5, 6])
    out["weekend_by_year"] = dd.groupby(["year", "wkend"])["ex"].mean().unstack()
    # nearness to 90d high, graded, on 5-day grid, by coin
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float).values
            n = len(b)
            dist = b["debug_info.components.breakout_dist.last_history_value"].astype(float).values
            for i in range(0, n, 5):
                if i + 5 < n:
                    rows.append(dict(coin=c, fwd=cl[i+5]/cl[i]-1, dist=dist[i]))
    g = pd.DataFrame(rows).dropna()
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["near"] = g["dist"].between(-15, 0)
    out["near_high_by_coin"] = g[g.near].groupby("coin")["ex"].apply(summ_s).unstack()
    sub = g[g["dist"] <= 0]
    sl = stats.linregress(sub["dist"], sub["ex"])
    out["below_high_slope"] = pd.Series({"slope": sl.slope, "t": sl.slope/sl.stderr, "n": len(sub)})
    # book largest days: coin return before/after
    bk = dd.dropna(subset=["book_return"]).copy()
    bk["next_coin"] = bk.groupby(["coin", "win"])["coin_return"].shift(-1)
    bk["bq"] = pd.qcut(bk["book_return"].rank(method="first"), 10, labels=False)
    out["book_decile_next_coin"] = bk.groupby("bq").agg(book=("book_return", "mean"), prev=("prev_ret", "mean"),
                                                        nxt=("next_coin", "mean"), n=("book_return", "count"))
    return out
