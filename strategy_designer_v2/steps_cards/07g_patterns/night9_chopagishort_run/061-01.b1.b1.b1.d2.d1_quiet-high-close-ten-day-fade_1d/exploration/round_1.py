def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = (h - l).replace(0, np.nan)
            loc = (c - l) / rng
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            z = r1 / sd20
            tr60 = c / c.shift(60) - 1
            vr = b["volume"] / b["volume"].rolling(20).mean()
            rngz = (rng / c) / ((rng / c).rolling(20).mean())
            r5 = c / c.shift(5) - 1
            ts = pd.to_datetime(b["timestamp"])
            for hz in (2, 10):
                fwd = c.shift(-hz) / c - 1
                idx = np.arange(0, len(b), hz)
                for i in idx:
                    if np.isnan(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, hz=hz, loc=loc.iloc[i], z=z.iloc[i],
                                     tr60=tr60.iloc[i], vr=vr.iloc[i], rngz=rngz.iloc[i],
                                     r5=r5.iloc[i] / (sd20.iloc[i] * np.sqrt(5)) if sd20.iloc[i] > 0 else np.nan,
                                     inprof=b["regime"].iloc[i] != "chop",
                                     wd=ts.iloc[i].weekday(), year=ts.iloc[i].year,
                                     fwd=fwd.iloc[i]))
    S = pd.DataFrame(rows)
    S["drift"] = S.groupby(["coin", "hz"])["fwd"].transform("mean")
    S["ex"] = S["fwd"] - S["drift"]

    def summ(g):
        n = len(g); m = g["ex"].mean(); s = g["ex"].std()
        return pd.Series({"n": n, "mean_ex": m, "t": m / (s / np.sqrt(n)) if n > 2 and s > 0 else np.nan})

    out = {}
    for hz in (2, 10):
        T = S[S.hz == hz].copy()
        T["locq"] = pd.cut(T["loc"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
        out[f"h{hz} inprof x loc"] = T.groupby(["inprof", "locq"]).apply(summ)
        T["zq"] = pd.cut(T["z"], [-99, -2, -1, 0, 1, 2, 99])
        out[f"h{hz} inprof x z"] = T.groupby(["inprof", "zq"]).apply(summ)
        T["trq"] = pd.cut(T["tr60"], [-9, -.3, -.1, .1, .3, 99])
        out[f"h{hz} tr60 x highloc"] = T[T["loc"] >= .75].groupby("trq").apply(summ)
        T["vrq"] = pd.qcut(T["vr"], 5, duplicates="drop")
        out[f"h{hz} volume ratio"] = T.groupby("vrq").apply(summ)
        T["r5q"] = pd.cut(T["r5"], [-99, -2, -1, 0, 1, 2, 99])
        out[f"h{hz} inprof x r5z"] = T.groupby(["inprof", "r5q"]).apply(summ)
    T1 = S[S.hz == 2]
    out["h2 weekday"] = T1.groupby("wd").apply(summ)
    out["h10 inprof by year (highloc quiet up)"] = S[(S.hz == 10) & S.inprof & (S["loc"] >= .75) & (S.z > 0) & (S.z <= 1)].groupby("year").apply(summ)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D)
    book = D.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book by window"] = book.groupby(level=0).agg(["count", "mean", "std", "sum"])
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    tr = pd.concat(tr)
    tr["ewd"] = pd.to_datetime(tr["entry_time"]).dt.weekday
    out["trades by entry weekday"] = tr.groupby("ewd")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades summary"] = tr["net_profit_loss_percent"].describe()
    return out
