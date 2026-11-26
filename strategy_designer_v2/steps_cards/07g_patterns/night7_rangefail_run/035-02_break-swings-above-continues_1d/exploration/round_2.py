def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float)
            r1 = c.pct_change()
            sw = r1.abs().rolling(20).mean()
            hh = hi.shift(1).rolling(20).max()
            dist = (c / hh - 1) / sw
            ts = pd.to_datetime(b["timestamp"])
            grid = np.arange(len(b)) % H == 0
            df = pd.DataFrame(dict(coin=coin, w=w, dist=dist, z1=r1 / sw, r1=r1,
                                   fwd=c.shift(-H) / c - 1, f1=c.shift(-1) / c - 1,
                                   f2=c.shift(-2) / c - 1,
                                   wd=ts.dt.weekday, yr=ts.dt.year, day=ts.dt.floor("D"),
                                   grid=grid, alloc=b["postRebalance_current_allocation"]))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)

    def summ(g, col):
        g = g.dropna(subset=[col])
        x = g[col]; d = g.groupby("day")[col].sum(); D = len(d)
        t = x.sum() / np.sqrt((d**2).sum() * D / max(D - 1, 1)) if D > 1 else np.nan
        return pd.Series(dict(n=len(x), days=D, mean=x.mean(), t_day=t))
    out = {}
    # weekday, excess next-day return over coin mean, day-clustered
    A["ex1"] = A.f1 - A.coin.map(A.groupby("coin").f1.mean())
    out["weekday_next_day_excess"] = A.groupby("wd").apply(lambda g: summ(g, "ex1"))
    out["weekday_x_year_t"] = A.groupby(["yr", "wd"]).apply(lambda g: summ(g, "ex1")).t_day.unstack()
    out["weekday_next_day_excess_by_window_mean"] = A.groupby(["w", "wd"]).ex1.mean().unstack().round(4)
    # big up day, not a breakout, 5-day grid
    G = A[A.grid & A.fwd.notna()].copy()
    G["ex"] = G.fwd - G.coin.map(G.groupby("coin").fwd.mean())
    G = G.dropna(subset=["z1", "dist"])
    G["brk"] = G.dist > 0
    G["zbin"] = pd.cut(G.z1, [-np.inf, -1.5, -0.5, 0.5, 1.5, 3, np.inf])
    out["z1_x_breakout"] = G.groupby(["brk", "zbin"]).apply(lambda g: summ(g, "ex"))
    # breakout by year
    out["breakout_by_year"] = G[G.brk].groupby("yr").apply(lambda g: summ(g, "ex"))
    # 2-day after big up day (all bars, day-clustered, counted at bars 0,2,...)
    A["ex2"] = A.f2 - A.coin.map(A.groupby("coin").f2.mean())
    out["sizes_dist_grid_counts"] = G.groupby(pd.cut(G.dist, [-np.inf, -6, -3, -1, 0, np.inf])).apply(lambda g: summ(g, "ex"))
    # book: largest daily gains share
    Dd = pd.concat([d.assign(coin=c, w=w) for c, ws in data["days"].items() for w, d in ws.items()])
    bk = Dd.groupby(["w", "day"]).book_return.mean().dropna()
    s = bk.sort_values(ascending=False)
    out["book_days"] = pd.Series(dict(n=len(bk), total=bk.sum(), top10=s.head(10).sum(), top30=s.head(30).sum(), worst30=s.tail(30).sum()))
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    out["trades_net_share_long>7d"] = pd.Series(dict(n=len(T), sum_all=T.net_profit_loss_percent.sum(),
        sum_gt7=T[T.duration_minutes > 7*1440].net_profit_loss_percent.sum(),
        median=T.net_profit_loss_percent.median(), winrate=(T.net_profit_loss_percent > 0).mean()))
    return out
