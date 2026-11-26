def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # weekday with day-clustered evidence: per day, mean demeaned coin return across coins
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D)
    D["day"] = pd.to_datetime(D["day"])
    D["cu"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    per_day = D.dropna(subset=["cu"]).groupby("day")["cu"].mean()
    wd = per_day.index.weekday
    yr = per_day.index.year
    g = per_day.groupby(wd)
    out["weekday_dayclustered"] = pd.DataFrame({"mean": g.mean(), "days": g.size(),
        "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    out["weekday_by_year"] = per_day.groupby([yr, wd]).mean().unstack()
    # per coin weekday 3 and 5 means
    D["wd"] = D["day"].dt.weekday
    out["weekday_by_coin"] = D.groupby(["coin", "wd"])["cu"].mean().unstack()[[1, 2, 3, 5]]

    # 10-day grid: close location in bar range, and range size, and r1 extremes by vol
    H = 10; rows = []
    for coin, ws in data["bars"].items():
        for w, df in ws.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float); h = d["high"].astype(float); l = d["low"].astype(float)
            r1 = c.pct_change()
            clv = (c - l) / (h - l)
            rng = (h - l) / c
            vol = r1.rolling(20).std()
            clv5 = ((c - l) / (h - l)).rolling(5).mean()
            r5 = c / c.shift(5) - 1
            ts = pd.to_datetime(d["timestamp"])
            for p in range(0, len(c) - H, H):
                rows.append(dict(coin=coin, day=ts.iloc[p].normalize(), year=ts.iloc[p].year,
                    fwd=c.iloc[p+H]/c.iloc[p]-1, clv=clv.iloc[p], clv5=clv5.iloc[p], rng_z=rng.iloc[p]/(vol.iloc[p] if vol.iloc[p] else np.nan),
                    r1z=r1.iloc[p]/vol.iloc[p] if vol.iloc[p] else np.nan, r5=r5.iloc[p]))
    X = pd.DataFrame(rows)
    X["un"] = X["fwd"] - X.groupby("coin")["fwd"].transform("mean")
    def ct(s, days):
        s = s.dropna(); days = days.loc[s.index]; N = len(s); m = s.mean()
        S = (s - m).groupby(days).sum(); G = len(S)
        return m, m / (np.sqrt(G/(G-1)*(S**2).sum())/N), N, G
    for f in ["clv", "clv5", "rng_z", "r1z", "r5"]:
        sub = X.dropna(subset=[f]).copy()
        sub["q"] = sub.groupby("coin")[f].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
        res = []
        for q, gg in sub.groupby("q"):
            m, t, N, G = ct(gg["un"], gg["day"])
            res.append(dict(q=q, feat=gg[f].mean(), unusual=m, t=t, N=N, days=G))
        top = sub[sub.q == 4]; bot = sub[sub.q == 0]
        res.append(dict(q="top-bot", unusual=top["un"].mean() - bot["un"].mean(),
            t=(top["un"].mean()-bot["un"].mean())/np.sqrt(top["un"].var()/len(top)+bot["un"].var()/len(bot))))
        out["q_" + f] = pd.DataFrame(res)
    return out
