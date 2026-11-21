def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    drift = {}
    usual = {}
    # first pass: grid returns per coin for drift
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                g.append(c[i + H] / c[i] - 1)
        g = np.array(g)
        drift[coin] = g.mean() if len(g) else np.nan
        usual[coin] = g.std() if len(g) else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            n = len(b)
            fwd = c.shift(-H) / c - 1
            r30 = c / c.shift(30) - 1
            r10p = c / c.shift(10) - 1
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            raw = b.get("debug_info.components.break.last_history_value")
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "fwd": fwd, "adj": fwd - drift[coin], "z": (fwd - drift[coin]) / usual[coin],
                "r30": r30, "r10p": r10p, "r1": r1, "vol30": vol30,
                "raw": raw if raw is not None else np.nan,
                "fc": b["forecast"], "regime": b["regime"],
                "alloc": b["postRebalance_current_allocation"],
                "year": ts.dt.year, "wd": ts.dt.weekday,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    grid = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()

    def summ(gr, col="z"):
        s = gr[col]
        return pd.Series({"n": len(s), "mean_adj_pct": gr["adj"].mean() * 100,
                          "mean_z": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})

    out = {}
    # 1. 30-day return deciles (all grid bars) vs next 10 days, drift-adjusted (long direction)
    g1 = grid[grid["r30"].notna()].copy()
    g1["r30q"] = g1.groupby("coin")["r30"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["r30_quintile_next10_long"] = g1.groupby("r30q").apply(summ)
    # 2. negative r30 regime, with vs without a break
    neg = g1[g1["r30"] < 0].copy()
    neg["brk"] = (neg["raw"] > 0).astype(int)
    out["neg30_break_vs_not_long"] = neg.groupby("brk").apply(summ)
    # break cases in any bar (not grid-only): use all bars with raw>0, first per grid cell
    br = A[(A["raw"] > 0) & A["fwd"].notna()].copy()
    br["cell"] = br["pos"] // H
    br = br.groupby(["coin", "win", "cell"]).head(1)
    br["rawq"] = pd.qcut(br["raw"].rank(method="first"), 4, labels=False)
    out["break_raw_quartile_next10_long"] = br.groupby("rawq").apply(summ)
    br["r30q"] = pd.qcut(br["r30"].rank(method="first"), 4, labels=False)
    out["break_r30_quartile_next10_long"] = br.groupby("r30q").apply(summ)
    # 3. after large 1-day moves: 1-day return quintile within coin (grid bars)
    g3 = grid[grid["r1"].notna() & grid["vol30"].notna()].copy()
    g3["s1"] = g3["r1"] / g3["vol30"]
    g3["s1q"] = pd.qcut(g3["s1"].rank(method="first"), 5, labels=False)
    out["r1_scaled_quintile_next10_long"] = g3.groupby("s1q").apply(summ)
    # 4. vol level
    g3["volq"] = g3.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["vol_tercile_next10_long"] = g3.groupby("volq").apply(summ)
    # 10-day past return quintile
    g4 = grid[grid["r10p"].notna()].copy()
    g4["q"] = g4.groupby("coin")["r10p"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["r10past_quintile_next10_long"] = g4.groupby("q").apply(summ)
    # 5. book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["year"] = pd.to_datetime(d["day"]).dt.year
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    day = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"), year=("year", "first"), wd=("wd", "first")).dropna()
    out["book_by_year"] = day.groupby("year").agg(n=("book", "size"), book_mean_bps=("book", lambda x: x.mean() * 1e4), coin_mean_bps=("coin", lambda x: x.mean() * 1e4))
    # position in short vs coin's return while short
    A["next1"] = A.groupby(["coin", "win"])["fwd"].transform(lambda x: x) # placeholder
    pos = A[A["alloc"].notna()].copy()
    out["share_bars_short"] = float((pos["alloc"] < -1e-6).mean())
    out["mean_alloc_when_short"] = float(pos.loc[pos["alloc"] < -1e-6, "alloc"].mean())
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["year"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades_by_year"] = T.groupby("year").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), median_net=("net_profit_loss_percent", "median"), win=("net_profit_loss_percent", lambda x: (x > 0).mean()))
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda x: (x > 0).mean()))
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trade_dur_quant"] = T["dur_d"].describe()
    out["trade_pl_quant"] = T["net_profit_loss_percent"].describe(percentiles=[.05, .25, .5, .75, .95])
    return out
