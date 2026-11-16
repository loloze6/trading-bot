def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    days = data["days"]; bars = data["bars"]
    out = {}
    dd = []
    for c in days:
        for w, x in days[c].items():
            x = x.copy(); x["coin"] = c; x["w"] = w
            x["prev_ret"] = x["coin_return"].shift(1)
            x["prev5"] = x["close"].shift(1) / x["close"].shift(6) - 1
            dd.append(x)
    dd = pd.concat(dd, ignore_index=True)
    dd["day"] = pd.to_datetime(dd["day"])
    dd["wd"] = dd["day"].dt.weekday
    dd["yr"] = dd["day"].dt.year
    tt = lambda s: s.mean() / s.std() * np.sqrt(s.count())
    # cross-coin average per day, then weekday t (removes same-day correlation)
    m = dd.groupby(["day", "w"]).agg(cr=("coin_return", "mean"), br=("book_return", "mean")).reset_index()
    m["wd"] = m["day"].dt.weekday; m["yr"] = m["day"].dt.year
    out["day-avg coin ret by weekday"] = m.groupby("wd")["cr"].agg(["count", "mean", tt])
    out["day-avg book ret by weekday"] = m.groupby("wd")["br"].agg(["count", "mean", tt])
    # Saturday minus other days, per coin
    def satdiff(x):
        a = x.loc[x.wd == 5, "coin_return"].dropna(); b = x.loc[x.wd != 5, "coin_return"].dropna()
        return pd.Series(dict(sat=a.mean(), other=b.mean(), t=stats.ttest_ind(a, b, equal_var=False).statistic, n=len(a)))
    out["sat vs other by coin"] = dd.groupby("coin").apply(satdiff)
    out["sat vs other by year"] = dd.groupby("yr").apply(satdiff)
    fri = dd.copy(); fri["wd"] = fri["wd"].replace({4: 5})
    out["fri+sat vs other by year"] = fri.groupby("yr").apply(satdiff)
    # share of windows where saturday avg > other avg
    pw = m.groupby("w").apply(lambda x: x.loc[x.wd == 5, "cr"].mean() - x.loc[x.wd != 5, "cr"].mean())
    out["sat minus other, per window: share>0, mean, t"] = pd.Series(dict(share=(pw > 0).mean(), mean=pw.mean(), t=tt(pw), n=pw.count()))
    # weekend return as fraction of book: position on Friday close
    # next-day return after large daily moves, by coin-standardised prev ret
    dd["z"] = dd.groupby("coin")["prev_ret"].transform(lambda s: (s - s.mean()) / s.std())
    e = dd.dropna(subset=["z", "coin_return"]).copy()
    e["q"] = pd.cut(e["z"], [-99, -2, -1, 0, 1, 2, 99])
    e["dm"] = e["coin_return"] - e.groupby("coin")["coin_return"].transform("mean")
    out["next-day ret by prev-day z"] = e.groupby("q")["dm"].agg(["count", "mean", tt])
    # weekday of prev big moves
    # book's largest gain/loss days: coin returns before and after
    m = m.sort_values(["w", "day"])
    m["cr_prev5"] = m.groupby("w")["cr"].transform(lambda s: s.shift(1).rolling(5).sum())
    m["cr_next5"] = m.groupby("w")["cr"].transform(lambda s: s[::-1].shift(1).rolling(5).sum()[::-1])
    m["bq"] = pd.qcut(m["br"].rank(method="first"), 10, labels=False)
    out["book decile: coin prev5/next5"] = m.groupby("bq")[["br", "cr_prev5", "cr_next5"]].mean()
    return out
