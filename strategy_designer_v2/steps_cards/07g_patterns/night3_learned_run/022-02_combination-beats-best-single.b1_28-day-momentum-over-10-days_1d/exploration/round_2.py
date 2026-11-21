def explore(data):
    import numpy as np, pandas as pd
    out = {}
    def tt(s):
        s = s.dropna()
        return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan))
    # per-coin drift over all windows, per horizon
    allr = {}
    for H in [3, 10]:
        rows = []
        for coin, wins in data["bars"].items():
            for w, df in wins.items():
                df = df.sort_values("timestamp").reset_index(drop=True)
                c = df["close"].astype(float); n = len(c)
                r1 = c.pct_change(); r28 = c / c.shift(28) - 1
                r60 = c / c.shift(60) - 1
                hi60 = c.rolling(60, min_periods=30).max(); near = c / hi60 - 1
                lo60 = c.rolling(60, min_periods=30).min(); nearlo = c / lo60 - 1
                vol20 = r1.rolling(20).std()
                r1z = r1 / vol20
                for t in range(0, n - H, H):
                    rows.append(dict(coin=coin, win=w, fwd=c[t + H] / c[t] - 1, r1z=r1z[t], r28=r28[t],
                                     r60=r60[t], near=near[t], nearlo=nearlo[t], vol=vol20[t]))
        g = pd.DataFrame(rows)
        g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
        g["sd"] = g.groupby("coin")["fwd"].transform("std")
        g["z"] = g["ex"] / g["sd"]
        allr[H] = g
    # reversal after large 1-day moves, 3-day horizon, graded by sign*size of 1-day z
    g = allr[3].dropna(subset=["r1z"]).copy()
    g["b"] = pd.cut(g["r1z"], [-99, -2, -1, 0, 1, 2, 99])
    out["h3_by_r1z_bin"] = g.groupby("b")["z"].apply(tt).unstack()
    out["h3_corr_r1z_z_spearman"] = float(g[["r1z", "z"]].corr(method="spearman").iloc[0, 1])
    g10 = allr[10].dropna(subset=["r1z"]).copy()
    g10["b"] = pd.cut(g10["r1z"], [-99, -2, -1, 0, 1, 2, 99])
    out["h10_by_r1z_bin"] = g10.groupby("b")["z"].apply(tt).unstack()
    # nearness to 60-day high, 10 days, deciles pooled per coin
    d = allr[10].dropna(subset=["near"]).copy()
    d["q"] = d.groupby("coin")["near"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["h10_near_q_by_coin_top_minus_bottom"] = d.groupby("coin").apply(
        lambda x: x[x.q == 4]["z"].mean() - x[x.q == 0]["z"].mean())
    out["h10_near_spearman"] = float(d[["near", "z"]].corr(method="spearman").iloc[0, 1])
    d2 = allr[10].dropna(subset=["r60"]).copy()
    d2["q"] = d2.groupby("coin")["r60"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["h10_r60_q"] = d2.groupby("q")["z"].apply(tt).unstack()
    # momentum strength vs 28d return when vol high vs low: sign*z graded by |r28|/vol
    d3 = allr[10].dropna(subset=["r28", "vol"]).copy()
    d3["s28"] = d3["r28"] / (d3["vol"] * np.sqrt(28))
    d3["b"] = pd.cut(d3["s28"], [-99, -1.5, -0.5, 0, 0.5, 1.5, 99])
    out["h10_by_r28_volscaled"] = d3.groupby("b")["z"].apply(tt).unstack()
    # book: long vs short timing decomposition
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            b = data["bars"][coin][w].sort_values("timestamp").reset_index(drop=True)
            x = df.copy().reset_index(drop=True)
            x["alloc_prev"] = b["postRebalance_current_allocation"].astype(float).shift(1).values[:len(x)]
            x["coin"] = coin
            dd.append(x)
    D = pd.concat(dd, ignore_index=True)
    D["mu"] = D.groupby("coin")["coin_return"].transform("mean")
    D["drift_gain"] = D["alloc_prev"] * D["mu"]
    D["side"] = np.sign(D["alloc_prev"])
    out["book_side_decomp"] = D.groupby("side").agg(n=("book_return", "size"), book=("book_return", "mean"),
                                                   drift=("drift_gain", "mean"), coin=("coin_return", "mean"),
                                                   absalloc=("alloc_prev", lambda s: s.abs().mean()))
    # book's worst days: what preceded (coin side, coin return)
    q = D["book_return"].quantile([0.01, 0.99])
    out["worst1pct_side_share"] = D[D.book_return <= q.iloc[0]]["side"].value_counts(normalize=True)
    out["best1pct_side_share"] = D[D.book_return >= q.iloc[1]]["side"].value_counts(normalize=True)
    # trades: short trades by coin
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()], ignore_index=True)
    out["trades_coin_side"] = T.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["size", "mean", "median"])
    return out
