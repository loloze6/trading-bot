def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    coinmean = {}
    for coin, ws in bars.items():
        g = []
        for w, b in ws.items():
            c = b["close"].values
            for i in range(0, len(c) - 10, 10):
                g.append(c[i + 10] / c[i] - 1)
        coinmean[coin] = np.mean(g) if g else np.nan
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            sma = c.rolling(20).mean()
            dist = (c / sma - 1) * 100
            r60 = (c / c.shift(60) - 1) * 100
            r1 = c.pct_change()
            vol10 = r1.rolling(10).std()
            vol30 = r1.rolling(30).std()
            r5 = c / c.shift(5) - 1
            n = len(b)
            for h in (1, 3, 10):
                b["f%d" % h] = c.shift(-h) / c - 1
            b["pos"] = np.arange(n)
            b["dist"] = dist; b["r60"] = r60; b["r1"] = r1; b["r5"] = r5
            b["vr"] = vol10 / vol30
            b["coin"] = coin; b["win"] = w
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["ex10"] = b["f10"] - coinmean[coin]
            rows.append(b)
    D = pd.concat(rows, ignore_index=True)
    D["grp"] = np.where(D["regime"] == "unknown", "rising_calm",
               np.where(D["r60"] > 10, "rising_agit",
               np.where(D["r60"] < -10, "falling", np.where(D["r60"].notna(), "choppy", "na"))))
    G = D[(D["pos"] % 10 == 0)].dropna(subset=["ex10", "dist"])
    out = {}
    def slope(df, x, y):
        df = df.dropna(subset=[x, y])
        if len(df) < 10: return (np.nan, np.nan, len(df))
        r = stats.linregress(df[x], df[y]); return (r.slope, r.slope / r.stderr, len(df))
    res = []
    for k, df in G.groupby("grp"):
        s, t, n = slope(df, "dist", "ex10")
        res.append([k, s, t, n, df["ex10"].mean(), df["ex10"].mean() / df["ex10"].std() * np.sqrt(len(df))])
    s, t, n = slope(G, "dist", "ex10")
    res.append(["all", s, t, n, G["ex10"].mean(), np.nan])
    out["slope_ex10_on_dist_by_group"] = pd.DataFrame(res, columns=["grp", "slope", "t", "n", "mean_ex10", "t_mean"])
    # dist quintile by group
    G2 = G.copy(); G2["dq"] = pd.qcut(G2["dist"], 5, labels=False)
    out["ex10_by_distq_grp"] = G2.pivot_table(index="dq", columns="grp", values="ex10", aggfunc="mean")
    out["n_by_distq_grp"] = G2.pivot_table(index="dq", columns="grp", values="ex10", aggfunc="count")
    # big 1-day moves -> next 3 days, 3-day grid
    G3 = D[(D["pos"] % 3 == 0)].dropna(subset=["r1", "f3"]).copy()
    G3["z"] = G3["r1"] / G3.groupby("coin")["r1"].transform("std")
    G3["zq"] = pd.qcut(G3["z"], 5, labels=False)
    out["f3_by_r1quint"] = G3.groupby("zq")["f3"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    G3["vq"] = pd.qcut(G3["vr"], 4, labels=False)
    out["f3_by_volratio_q"] = G3.groupby("vq")["f3"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # 5-day return quintile -> 10-day, by group
    G2["r5q"] = pd.qcut(G2["r5"], 5, labels=False)
    out["ex10_by_r5q_grp"] = G2.pivot_table(index="r5q", columns="grp", values="ex10", aggfunc="mean")
    # weekday 1d returns
    G1 = D.dropna(subset=["f1"])
    out["f1_by_weekday"] = G1.groupby("wd")["f1"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # book
    dd = []
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    DD = pd.concat(dd)
    bk = DD.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_by_window"] = bk.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    q = bk["book_return"].quantile([0.02, 0.98])
    out["coin_ret_on_book_extremes"] = pd.Series({"book_low2pct_coin": bk.loc[bk.book_return <= q.iloc[0], "coin_return"].mean(),
        "book_high2pct_coin": bk.loc[bk.book_return >= q.iloc[1], "coin_return"].mean(),
        "share_gain_top5pct_days": bk.book_return[bk.book_return >= bk.book_return.quantile(.95)].sum() / bk.book_return.sum()})
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    T["dur_d"] = T["duration_minutes"] / 1440
    T["dq"] = pd.qcut(T["dur_d"], 4, labels=False, duplicates="drop")
    out["trades_by_duration_q"] = T.groupby("dq").agg(n=("net_profit_loss_percent", "count"), dur=("dur_d", "mean"), pnl=("net_profit_loss_percent", "mean"))
    T["eq"] = pd.qcut(T["entry_forecast"], 3, labels=False, duplicates="drop")
    out["trades_by_entryfc"] = T.groupby("eq").agg(n=("net_profit_loss_percent", "count"), fc=("entry_forecast", "mean"), pnl=("net_profit_loss_percent", "mean"))
    return out
