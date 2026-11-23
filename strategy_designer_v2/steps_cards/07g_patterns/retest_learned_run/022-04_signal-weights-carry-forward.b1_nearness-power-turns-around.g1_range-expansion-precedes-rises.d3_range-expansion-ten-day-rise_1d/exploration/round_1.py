def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l) / c
            rr = (h - l) / (h - l).rolling(30, min_periods=20).mean()
            r1 = c.pct_change()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            vol20 = r1.rolling(20, min_periods=15).std()
            hi30 = c / c.rolling(30, min_periods=20).max() - 1
            up = (c - l) / (h - l).replace(0, np.nan)  # close location in bar
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "rr": rr, "r1": r1, "r5": r5,
                               "r20": r20, "vol20": vol20, "hi30": hi30, "up": up, "fwd": fwd, "fwd1": fwd1,
                               "wd": ts.dt.weekday, "yr": ts.dt.year, "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
        for w, d in data["days"][coin].items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w
            daily.append(dd)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A.pos % H == 0) & A.fwd.notna()].copy()
    drift = G.groupby("coin")["fwd"].mean()
    usual = G.groupby("coin")["fwd"].std()
    G["ex"] = G.fwd - G.coin.map(drift)
    G["str"] = G.ex / G.coin.map(usual)
    # per-coin quintile ranks to avoid coin mixing
    def q(col):
        return G.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False) if s.notna().sum() > 10 else s * np.nan)
    def summ(key):
        g = G.groupby(key)["ex"]
        out = pd.DataFrame({"n": g.count(), "mean_ex%": g.mean() * 100, "t": g.mean() / (g.std() / np.sqrt(g.count())),
                            "strength": G.groupby(key)["str"].mean()})
        return out.round(3)
    res = {}
    for col in ["rr", "r1", "r5", "r20", "vol20", "hi30", "up"]:
        G["q_" + col] = q(col)
    G["reg"] = np.where(G.r20 > 0, "up20", "down20")
    for col in ["rr", "r1", "r5", "r20", "vol20", "hi30", "up"]:
        res["10d ex by q_" + col] = summ("q_" + col)
    res["10d ex by up20 x q_rr"] = summ(["reg", "q_rr"])
    res["10d ex by up20 x q_vol20"] = summ(["reg", "q_vol20"])
    res["10d ex by up20 x q_hi30"] = summ(["reg", "q_hi30"])
    res["10d ex by coin x reg"] = summ(["coin", "reg"])
    res["10d ex by year x reg"] = summ(["yr", "reg"])
    # correlations (spearman) of features with ex, pooled
    cors = {}
    for col in ["rr", "r1", "r5", "r20", "vol20", "hi30", "up"]:
        s = G[[col, "ex"]].dropna()
        rho, p = stats.spearmanr(s[col], s.ex)
        cors[col] = (round(rho, 4), round(p, 4), len(s))
    res["spearman feature vs 10d ex (all grid cases)"] = pd.DataFrame(cors, index=["rho", "p", "n"]).T
    # daily: book & coin by weekday
    D = pd.concat(daily, ignore_index=True)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    g = D.groupby("wd")
    res["daily by weekday"] = pd.DataFrame({"n": g.book_return.count(), "book%": g.book_return.mean() * 100,
                                            "coin%": g.coin_return.mean() * 100,
                                            "t_coin": g.coin_return.mean() / (g.coin_return.std() / np.sqrt(g.coin_return.count()))}).round(3)
    # 1-day next return after large days (all bars), by r1 decile pooled per coin
    A["q_r1"] = A.groupby("coin")["r1"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    A["ex1"] = A.fwd1 - A.coin.map(A.groupby("coin").fwd1.mean())
    g = A.dropna(subset=["ex1", "q_r1"]).groupby("q_r1")["ex1"]
    res["next-day ex by r1 decile"] = pd.DataFrame({"n": g.count(), "mean%": g.mean() * 100,
                                                    "t": g.mean() / (g.std() / np.sqrt(g.count()))}).round(3)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["q_fc"] = pd.qcut(T.entry_forecast.rank(method="first"), 4, labels=False)
    g = T.groupby("q_fc")["net_profit_loss_percent"]
    res["trades by entry forecast quartile"] = pd.DataFrame({"n": g.count(), "mean_net": g.mean(), "win": T.groupby("q_fc").net_profit_loss_percent.apply(lambda s: (s > 0).mean()),
                                                             "fc_mean": T.groupby("q_fc").entry_forecast.mean(),
                                                             "dur_days": T.groupby("q_fc").duration_minutes.mean() / 1440}).round(3)
    return res
