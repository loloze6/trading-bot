def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    daily = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            ch20 = pd.Series(c).pct_change(20)
            r1 = pd.Series(c).pct_change()
            vol20 = r1.rolling(20).std()
            f = b["forecast"].values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - 20, 20):
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, ch20=ch20.iloc[i], vol=vol20.iloc[i],
                                 f=f[i], fwd20=c[i+20]/c[i]-1, fwd5=c[min(i+5,n-1)]/c[i]-1))
            for i in range(1, n - 1):
                daily.append(dict(coin=coin, w=w, wd=ts.iloc[i].weekday(), year=ts.iloc[i].year,
                                  r=r1.iloc[i], nxt=c[i+1]/c[i]-1, vol=vol20.iloc[i], ch20=ch20.iloc[i]))
    E = pd.DataFrame(rows).dropna(subset=["ch20"])
    E["ex"] = E["fwd20"] - E.groupby("coin")["fwd20"].transform("mean")
    E["q"] = E.groupby("coin")["ch20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    def agg(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(), "t": stats.ttest_1samp(g["ex"], 0).statistic, "hit": (g["fwd20"] > 0).mean()})
    out["fwd20 excess by ch20 quintile (nonoverlap)"] = E.groupby("q").apply(agg)
    E["vq"] = E.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["fwd20 excess by vol tercile"] = E.groupby("vq").apply(agg)
    out["fwd20 excess q0 by coin"] = E[E.q == 0].groupby("coin").apply(agg)
    out["fwd20 excess q4 by coin"] = E[E.q == 4].groupby("coin").apply(agg)
    out["fwd20 excess q0 by year"] = E[E.q == 0].groupby("year").apply(agg)
    D = pd.DataFrame(daily).dropna()
    D["z"] = D["r"] / D["vol"]
    D["zb"] = pd.cut(D["z"], [-99, -2, -1, 0, 1, 2, 99])
    def ag2(g):
        return pd.Series({"n": len(g), "mean_next": g["nxt"].mean(), "t": stats.ttest_1samp(g["nxt"], 0).statistic})
    out["next-day ret by today z"] = D.groupby("zb").apply(ag2)
    out["next-day ret by weekday"] = D.groupby("wd").apply(ag2)
    # trades
    T = pd.concat([t.assign(coin=c, w=w) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    T["days"] = T["duration_minutes"] / 1440
    T["db"] = pd.cut(T["days"], [0, 1.5, 5, 15, 1000])
    out["trades by duration"] = T.groupby("db").agg(n=("net_profit_loss_percent", "size"), mean=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()), fees=("total_commission", "mean"))
    out["trades by coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), mean=("net_profit_loss_percent", "mean"), sum=("net_profit_loss_percent", "sum"))
    return out
