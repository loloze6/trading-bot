def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            hi = c.shift(1).rolling(20).max()
            clr = (c / hi - 1) / vol
            r60 = c / c.shift(60) - 1
            r20 = c / c.shift(20) - 1
            ts = pd.to_datetime(d["timestamp"])
            tmp = pd.DataFrame(dict(coin=coin, w=w, pos=np.arange(len(d)), ts=ts, clr=clr, r60=r60, r20=r20,
                                    r1=r / vol, r3=(c / c.shift(3) - 1) / (vol * np.sqrt(3)),
                                    f3=c.shift(-3) / c - 1, f5=c.shift(-5) / c - 1, f10=c.shift(-10) / c - 1,
                                    f20=c.shift(-20) / c - 1, wd=ts.dt.weekday, yr=ts.dt.year,
                                    alloc=d["postRebalance_current_allocation"].astype(float)))
            rows.append(tmp)
    A = pd.concat(rows, ignore_index=True)
    res = {}
    for h in (3, 5, 10, 20):
        g = A[A.pos % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A["coin"].map(dr)
    def clustered(df, col, key):
        # average over coins per date, then t over dates
        m = df.dropna(subset=[col]).groupby([key, "ts"])[col].mean().reset_index()
        out = m.groupby(key)[col].agg(["mean", "count", "std"])
        out["t_dates"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        out["coins_pos_share"] = df.dropna(subset=[col]).groupby([key, "coin"])[col].mean().gt(0).groupby(level=0).mean()
        return out.drop(columns="std")
    # breakout strength, multiple horizons, date-clustered
    for h in (3, 5, 10, 20):
        G = A[A.pos % h == 0].copy()
        G["clrb"] = pd.cut(G["clr"], [-99, -1.5, 0, 0.75, 1.5, 99])
        res[f"x{h}_by_clr_clustered"] = clustered(G, f"x{h}", "clrb")
    G = A[A.pos % 10 == 0].copy()
    # weekday robustness: per year sign of Thursday minus others
    G["thu"] = G.wd == 3
    tt = G.dropna(subset=["x10"]).groupby(["yr", "thu"])["x10"].mean().unstack()
    tt["thu_minus_other"] = tt[True] - tt[False]
    res["thursday_by_year"] = tt
    res["weekday_clustered"] = clustered(G, "x10", "wd")
    # last-day/3-day reversal, date clustered, 3 and 5 day horizons
    for h in (3, 5):
        Gh = A[A.pos % h == 0].copy()
        Gh["r3b"] = pd.qcut(Gh["r3"], 5)
        res[f"x{h}_by_r3_quintile_clustered"] = clustered(Gh, f"x{h}", "r3b")
    # breakout x trend: within breakouts, x10 by r60 tercile
    P = G[G.clr > 0].copy()
    P["r60b"] = pd.qcut(P["r60"], 3)
    res["breakout_x10_by_r60_tercile"] = clustered(P, "x10", "r60b")
    P["clr_hi"] = P.clr > P.clr.median()
    res["breakout_r60pos_x_clrhi"] = P.dropna(subset=["x10"]).groupby([P.r60 > 0, "clr_hi"])["x10"].agg(["mean", "count"])
    # 60-day trend alone, date clustered, 20-day horizon
    G20 = A[A.pos % 20 == 0].copy()
    G20["r60b"] = pd.qcut(G20["r60"], 5)
    res["x20_by_r60_quintile_clustered"] = clustered(G20, "x20", "r60b")
    # book: daily returns, top/bottom 5% days and the coin move before
    D = []
    for coin, wins in days.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            d["coin"] = coin
            d["prev5"] = d["close"] / d["close"].shift(5) - 1
            D.append(d)
    D = pd.concat(D, ignore_index=True).dropna(subset=["book_return"])
    q = D["book_return"].quantile([0.02, 0.98])
    D["tail"] = np.where(D.book_return <= q.iloc[0], "worst2%", np.where(D.book_return >= q.iloc[1], "best2%", "mid"))
    res["book_tails"] = D.groupby("tail").agg(n=("book_return", "size"), book=("book_return", "mean"),
                                              coin=("coin_return", "mean"), prev5=("prev5", "mean"))
    return res
