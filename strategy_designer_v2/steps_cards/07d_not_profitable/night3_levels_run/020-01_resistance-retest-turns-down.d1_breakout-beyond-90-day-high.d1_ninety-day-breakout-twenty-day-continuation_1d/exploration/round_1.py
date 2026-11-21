import numpy as np, pandas as pd

def explore(data):
    out = {}
    rows = []
    trows = []
    drows = []
    H = 20
    for coin, wins in data["bars"].items():
        # coin's normal 20-day drift over all windows (grid)
        g_all = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                g_all.append(c[i + H] / c[i] - 1)
        drift = np.mean(g_all) if g_all else np.nan
        for w, b in wins.items():
            c = b["close"].astype(float).values
            n = len(c)
            pos = b["postRebalance_current_allocation"].astype(float).fillna(0).values
            fc = b["forecast"].astype(float).fillna(0).values
            s = pd.Series(c)
            ret20 = s.pct_change(20).values
            ret90 = s.pct_change(90).values
            hi90 = s.shift(1).rolling(90, min_periods=90).max().values
            dist = c / hi90 - 1
            # trailing 20d vol
            vol20 = s.pct_change().rolling(20).std().values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, fwd=c[i + H] / c[i] - 1 - drift,
                                 fwdraw=c[i + H] / c[i] - 1,
                                 dist=dist[i], r20=ret20[i], r90=ret90[i], vol=vol20[i],
                                 pos=pos[i], fc=fc[i]))
        for w, d in data["days"][coin].items():
            dd = d.copy()
            dd["coin"] = coin; dd["win"] = w
            drows.append(dd[["coin", "win", "book_return", "coin_return"]])
        for w, t in data["trades"][coin].items():
            if len(t):
                tt = t.copy(); tt["coin"] = coin; tt["win"] = w
                trows.append(tt)
    G = pd.DataFrame(rows)
    out["grid_n"] = len(G)
    out["share_grid_in_position"] = float((G.pos.abs() > 1e-6).mean())
    # graded relation of distance to 90d high and forward drift-adjusted 20d return, all grid
    G2 = G.dropna(subset=["dist"])
    G2["dbin"] = pd.cut(G2["dist"], [-1, -0.5, -0.3, -0.15, -0.05, 0, 0.05, 0.15, 5])
    out["fwd_by_dist"] = G2.groupby("dbin")["fwd"].agg(["count", "mean", "median",
        lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan])
    G2["r90bin"] = pd.qcut(G2["r90"], 6)
    out["fwd_by_r90"] = G2.groupby("r90bin")["fwd"].agg(["count", "mean",
        lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    D = pd.concat(drows)
    D["dayret"] = D["book_return"]
    daily = D.groupby(["win", D.index if False else D.groupby(["coin","win"]).cumcount()])
    # book daily per window: mean over coins per day index
    D["k"] = D.groupby(["coin", "win"]).cumcount()
    B = D.groupby(["win", "k"])[["book_return", "coin_return"]].mean().dropna()
    out["book_mean_daily"] = float(B.book_return.mean())
    out["by_window"] = B.groupby(level=0).agg(book_mean=("book_return", "mean"),
                                              coin_mean=("coin_return", "mean"),
                                              days=("book_return", "size"))
    # deepest falls: chain in window order
    order = sorted(B.index.get_level_values(0).unique(), key=lambda x: int(x[1:]))
    chain = pd.concat([B.loc[w, "book_return"] for w in order])
    eq = (1 + chain).cumprod().values
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1
    out["max_dd"] = float(dd.min())
    winlab = np.concatenate([[w] * len(B.loc[w]) for w in order])
    out["dd_min_by_window"] = pd.Series(dd, index=winlab).groupby(level=0).min().sort_values().head(8)
    T = pd.concat(trows)
    T["side"] = T["side"].astype(str)
    out["trades_n"] = len(T)
    out["trade_pl"] = T["net_profit_loss_percent"].astype(float).describe()
    T["durd"] = T["duration_minutes"].astype(float) / 1440
    out["trade_dur"] = T["durd"].describe()
    T["ef"] = T["entry_forecast"].astype(float)
    T["efbin"] = pd.qcut(T["ef"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["pl_by_entry_fc"] = T.groupby("efbin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["pl_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    # position size when in
    inpos = G[G.pos.abs() > 1e-6]
    out["mean_pos_when_in"] = float(inpos.pos.mean())
    return out
