def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days, bars, trades = data["days"], data["bars"], data["trades"]
    coins = list(bars.keys())
    # book daily returns across coins
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            b = bars[c][w]
            b = b.assign(day=pd.to_datetime(b["timestamp"]).dt.floor("D"))
            pos = b.groupby("day")["postRebalance_current_allocation"].apply(lambda s: s.abs().max())
            dd["inpos"] = pd.to_datetime(dd["day"]).map(pos).fillna(0).values > 1e-9
            rows.append(dd)
    D = pd.concat(rows)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    # coin mean daily return over all windows
    cm = D.groupby("coin")["coin_return"].mean()
    out["coin_mean_daily"] = cm
    # per coin book contribution
    pc = D.groupby("coin").agg(book_mean=("book_return", "mean"), share_inpos=("inpos", "mean"))
    pc["book_sum"] = D.groupby("coin")["book_return"].sum()
    out["per_coin"] = pc
    pw = D.groupby("w").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"))
    pw["book_sum_over_coins"] = D.groupby("w")["book_return"].sum() / len(coins)
    out["per_window"] = pw
    out["per_year"] = D.groupby("year").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), inpos=("inpos", "mean"))
    # market rise share: allocation held x coin mean daily return
    mk = []
    for c in coins:
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].fillna(0).values
            r = b["close"].pct_change().shift(-1).values
            mk.append(pd.DataFrame({"c": c, "a": a, "r": r}))
    M = pd.concat(mk).dropna()
    M["drift"] = M["c"].map(cm)
    out["gain_split_per_bar_per_coin"] = pd.Series({
        "total_mean": (M.a * M.r).mean(), "market_part": (M.a * M.drift).mean(),
        "timing_part": (M.a * (M.r - M.drift)).mean(), "mean_alloc": M.a.mean()})
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in coins for t in trades[c].values() if len(t)])
    pl = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(T), "win_share": (pl > 0).mean(), "sum": pl.sum(),
                               "top5_sum": pl.head(5).sum(), "top10_sum": pl.head(10).sum(),
                               "median": pl.median(), "mean": pl.mean()})
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "sum", "mean"])
    # breakout cases recomputed: forward returns at several horizons, by run-up bucket
    cs = []
    for c in coins:
        for w, b in bars[c].items():
            cl = b["close"].reset_index(drop=True)
            prevmax = cl.shift(1).rolling(60).max()
            brk = cl > prevmax
            R = cl.shift(1) / cl.shift(61) - 1
            r60 = cl / cl.shift(60) - 1
            m = r60.abs().rolling(120, min_periods=60).mean().shift(1)
            exc = (cl / prevmax - 1)
            n = len(cl)
            for h in [5, 10, 20, 40]:
                fwd = cl.shift(-h) / cl - 1
                grid = np.arange(n) // h
                df = pd.DataFrame({"brk": brk, "R": R, "Rm": R / m, "exc": exc, "fwd": fwd, "g": grid})
                df = df[df.brk & df.fwd.notna() & df.R.notna()]
                df = df.groupby("g").head(1)
                df = df.assign(coin=c, w=w, h=h)
                cs.append(df)
    C = pd.concat(cs)
    # coin drift per horizon: non-overlapping
    drift = {}
    for c in coins:
        for h in [5, 10, 20, 40]:
            v = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                v += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(v)
    C["ex"] = C["fwd"] - [drift[(a, b)] for a, b in zip(C.coin, C.h)]
    C["rb"] = pd.cut(C["Rm"], [-np.inf, 0.5, 1.0, 1.5, np.inf], labels=["<0.5", "0.5-1", "1-1.5", ">1.5"])
    g = C.groupby(["h", "rb"], observed=True)["ex"]
    tab = g.agg(["count", "mean"])
    tab["t"] = g.mean() / (g.std() / np.sqrt(g.count()))
    out["breakout_excess_by_runup"] = tab
    g2 = C.groupby("h")["ex"]
    out["all_breakouts_excess"] = pd.DataFrame({"n": g2.count(), "mean": g2.mean(), "t": g2.mean() / (g2.std() / np.sqrt(g2.count()))})
    C["eb"] = pd.qcut(C["exc"], 3, labels=["small", "mid", "large"])
    g3 = C[C.h == 20].groupby("eb", observed=True)["ex"]
    out["h20_excess_by_overshoot"] = pd.DataFrame({"n": g3.count(), "mean": g3.mean(), "t": g3.mean() / (g3.std() / np.sqrt(g3.count()))})
    g4 = C[C.h == 20].groupby("coin")["ex"]
    out["h20_by_coin"] = pd.DataFrame({"n": g4.count(), "mean": g4.mean()})
    return out
