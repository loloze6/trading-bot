import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    rows = []
    for coin, wins in bars.items():
        allr = {}
        for h in (10, 30):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            allr[h] = (np.mean(rs), np.std(rs, ddof=1))
        for w, df in wins.items():
            c = df["close"].values; n = len(c)
            ts = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            reg = df["regime"].values
            for i in range(n):
                d = dict(coin=coin, pos=i, day=ts[i], regime=reg[i])
                for h in (10, 30):
                    d[f"u{h}"] = (c[i + h] / c[i] - 1 - allr[h][0]) / allr[h][1] if i + h < n else np.nan
                for p in (10, 30, 60, 90):
                    d[f"p{p}"] = c[i] / c[i - p] - 1 if i >= p else np.nan
                rows.append(d)
    X = pd.DataFrame(rows)
    for p in (10, 30, 60, 90):
        X[f"z{p}"] = X.groupby("coin")[f"p{p}"].transform(lambda s: (s - s.mean()) / s.std())

    def slope(sub, x, h):
        s = sub[(sub["pos"] % h == 0)].dropna(subset=[x, f"u{h}"])
        if len(s) < 20:
            return pd.Series(dict(n=len(s)))
        xv = s[x] - s[x].mean(); y = s[f"u{h}"]
        b = (xv * y).sum() / (xv ** 2).sum()
        e = y - y.mean() - b * xv
        sc = (xv * e).groupby(s["day"]).sum()
        G = len(sc)
        se = np.sqrt((sc ** 2).sum() * G / (G - 1)) / (xv ** 2).sum()
        return pd.Series(dict(n=len(s), days=G, slope=b, t_day=b / se))

    res = {}
    for p in (10, 30, 60, 90):
        for h in (10, 30):
            res[(f"z{p}", h, "all")] = slope(X, f"z{p}", h)
            res[(f"z{p}", h, "notregime")] = slope(X[X["regime"] != "mean_reversion"], f"z{p}", h)
    out["slopes_std_future_on_past"] = pd.DataFrame(res).T
    # sign split: does momentum come from up or down side
    res2 = {}
    for p in (30, 90):
        for h in (10, 30):
            res2[(f"z{p}", h, "up")] = slope(X[X[f"z{p}"] > 0], f"z{p}", h)
            res2[(f"z{p}", h, "down")] = slope(X[X[f"z{p}"] <= 0], f"z{p}", h)
    out["slopes_by_side"] = pd.DataFrame(res2).T
    # weekday of coin daily returns (all windows)
    D = pd.concat([df.assign(coin=c) for c, ws in days.items() for w, df in ws.items()])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    g = D.groupby("wd")["coin_return"]
    out["weekday_coin_ret"] = pd.DataFrame(dict(mean=g.mean(), n=g.count(),
                                                t=g.mean() / (g.std() / np.sqrt(g.count()))))
    # book: largest daily gains/losses, coin's 30d prior return around them
    B = D.dropna(subset=["book_return"])
    B = B[B["book_return"] != 0]
    out["book_active_days"] = len(B)
    q = B["book_return"].quantile([0.02, 0.98])
    out["book_tail_share_of_sum"] = pd.Series(dict(
        top2pct=B.loc[B["book_return"] >= q.iloc[1], "book_return"].sum() / B["book_return"].sum(),
        bottom2pct=B.loc[B["book_return"] <= q.iloc[0], "book_return"].sum() / B["book_return"].sum()))
    # trades
    T = pd.concat([df.assign(coin=c) for c, ws in trades.items() for w, df in ws.items() if len(df)])
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades_summary"] = pd.Series(dict(n=len(T), mean_net=T["net_profit_loss_percent"].mean(),
        median_net=T["net_profit_loss_percent"].median(), win=(T["net_profit_loss_percent"] > 0).mean(),
        mean_dur=T["dur_d"].mean()))
    T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades_by_year"] = T.groupby("yr")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"])
    return out
