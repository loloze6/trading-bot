def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    daily = []
    drift = {}
    for coin, wins in data["bars"].items():
        allg = []
        for w, b in wins.items():
            c = b["close"].values
            n = len(c)
            for i in range(0, n - H, H):
                allg.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(allg) if allg else 0.0
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi = b["high"].astype(float).rolling(30).max()
            lo = b["low"].astype(float).rolling(30).min()
            R30 = c / c.shift(30) - 1
            s = ((c - c.shift(30)).abs() / (hi - lo)).clip(upper=1)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            z1 = r1 / vol20.shift(1)
            R5 = c / c.shift(5) - 1
            R10 = c / c.shift(10) - 1
            pos = (c - lo) / (hi - lo)
            n = len(c)
            for i in range(0, n - H, H):
                f = c.iloc[i + H] / c.iloc[i] - 1
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 fc=b["forecast"].iloc[i], R30=R30.iloc[i], s=s.iloc[i],
                                 z1=z1.iloc[i], vol=vol20.iloc[i], R5=R5.iloc[i], R10=R10.iloc[i],
                                 pos=pos.iloc[i], fwd=f, ex=f - drift[coin],
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
            d = data["days"][coin][w].copy()
            d["coin"] = coin; d["w"] = w
            daily.append(d)
    g = pd.DataFrame(rows)
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    # 1 forecast deciles
    gg = g.dropna(subset=["fc"]).copy()
    gg["fdec"] = pd.qcut(gg["fc"], 10, labels=False, duplicates="drop")
    out["fwd excess by forecast decile"] = gg.groupby("fdec")["ex"].apply(tt).unstack()
    # 2 s bucket x sign(R30): signed excess
    h = g.dropna(subset=["R30", "s"]).copy()
    h["sgn_ex"] = np.sign(h["R30"]) * h["ex"]
    h["sq"] = pd.cut(h["s"], [0, .2, .4, .6, .8, .999, 1.0001], include_lowest=True)
    out["signed excess by share bucket"] = h.groupby("sq")["sgn_ex"].apply(tt).unstack()
    # R30 deciles alone
    h["rdec"] = pd.qcut(h["R30"], 10, labels=False)
    out["excess by R30 decile"] = h.groupby("rdec")["ex"].apply(tt).unstack()
    # position in range decile
    h["pdec"] = pd.qcut(h["pos"], 5, labels=False, duplicates="drop")
    out["excess by range position quintile"] = h.groupby("pdec")["ex"].apply(tt).unstack()
    # 3 large 1-day moves (vol z)
    k = g.dropna(subset=["z1"]).copy()
    k["zb"] = pd.cut(k["z1"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    out["excess by 1-day z bucket"] = k.groupby("zb")["ex"].apply(tt).unstack()
    # R5 deciles
    k2 = g.dropna(subset=["R5"]).copy()
    k2["d5"] = pd.qcut(k2["R5"], 5, labels=False)
    out["excess by 5d return quintile"] = k2.groupby("d5")["ex"].apply(tt).unstack()
    # 4 vol tercile x trend continuation
    v = h.dropna(subset=["vol"]).copy()
    v["vt"] = pd.qcut(v["vol"], 3, labels=["lowvol", "mid", "highvol"])
    out["signed excess (R30 dir) by vol tercile"] = v.groupby("vt")["sgn_ex"].apply(tt).unstack()
    # year
    out["signed excess by year"] = h.groupby("year")["sgn_ex"].apply(tt).unstack()
    # 5 daily book / coin by weekday
    D = pd.concat(daily)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby("day")[["book_return", "coin_return"]].mean()
    bk["wd"] = pd.to_datetime(bk.index).dayofweek
    bk["yr"] = pd.to_datetime(bk.index).year
    out["book/coin by weekday"] = bk.groupby("wd").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    out["book by year"] = bk.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    # 6 book extreme days: preceding coin 10-day mean
    bk2 = bk.dropna().copy()
    q = bk2["book_return"].quantile([0.02, 0.98])
    out["extreme book days count"] = pd.Series(dict(lo=q.iloc[0], hi=q.iloc[1],
        coin_on_big_gain=bk2.loc[bk2.book_return >= q.iloc[1], "coin_return"].mean(),
        coin_on_big_loss=bk2.loc[bk2.book_return <= q.iloc[0], "coin_return"].mean()))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    T["days"] = T["duration_minutes"] / 1440
    T["db"] = pd.cut(T["days"], [0, 5, 10, 20, 40, 1000])
    out["trades by duration"] = T.groupby(["db", "side"])["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
