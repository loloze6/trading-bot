def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        g5 = []
        tmp = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20, min_periods=15).std()
            z = r1 / sd
            low = c.rolling(90, min_periods=20).min()
            dist = c / low - 1
            f5 = c.shift(-5) / c - 1
            p5 = c / c.shift(5) - 1
            p20 = c / c.shift(20) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "z": z, "sd": sd, "dist": dist,
                               "f5": f5, "p5": p5, "p20": p20,
                               "fc": b["forecast"].astype(float),
                               "fall": (b["regime"] == "mean_reversion").astype(int),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "yr": pd.to_datetime(b["timestamp"]).dt.year})
            df = df.iloc[::5]
            tmp.append(df)
        d = pd.concat(tmp)
        drift = d["f5"].mean()
        d["u5"] = d["f5"] - drift
        d["usd"] = d["f5"].std()
        rows.append(d)
    G = pd.concat(rows).dropna(subset=["u5"])
    def agg(s):
        s = s.dropna()
        n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    G["zb"] = pd.cut(G["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["u5 by z bucket x falling regime"] = G.groupby(["fall", "zb"], observed=True)["u5"].apply(agg).unstack()
    G["fcb"] = pd.cut(G["fc"], [-21, -10, -2, -0.01, 0.01, 21])
    out["u5 by forecast bucket"] = G.groupby("fcb", observed=True)["u5"].apply(agg).unstack()
    G["volq"] = G.groupby("coin")["sd"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["u5 by vol quintile x fall"] = G.groupby(["fall", "volq"])["u5"].apply(agg).unstack()
    G["p20q"] = G.groupby("coin")["p20"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["u5 by past20d quintile x fall"] = G.groupby(["fall", "p20q"])["u5"].apply(agg).unstack()
    G["distq"] = G.groupby("coin")["dist"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["u5 by dist-to-90low quintile x fall"] = G.groupby(["fall", "distq"])["u5"].apply(agg).unstack()
    out["u5 by year x fall"] = G.groupby(["yr", "fall"])["u5"].apply(agg).unstack()
    # daily bars: weekday, next day after big z
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["coin daily ret by weekday"] = D.groupby("wd")["coin_return"].apply(agg).unstack()
    bk = D.groupby(["win", "day"])["book_return"].mean().dropna()
    hold = D.groupby(["win", "day"])["coin_return"].mean().dropna()
    yrs = pd.to_datetime(bk.index.get_level_values(1)).year
    out["book daily by year"] = bk.groupby(yrs).apply(agg).unstack()
    out["hold daily by year"] = hold.groupby(pd.to_datetime(hold.index.get_level_values(1)).year).apply(agg).unstack()
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades by side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        win=("net_profit_loss_percent", lambda s: (s > 0).mean()), dur=("dur_d", "mean"))
    T["efq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades by entry forecast quartile"] = T.groupby("efq").agg(n=("net_profit_loss_percent", "size"),
        ef=("entry_forecast", "mean"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    # book extremes: coin prior context on book's worst/best days
    bkdf = bk.reset_index(); bkdf.columns = ["win", "day", "br"]
    q = bkdf["br"].quantile([0.02, 0.98]).values
    Dm = D.merge(bkdf, on=["win", "day"])
    out["coin ret on book worst2%/best2% days"] = pd.Series({
        "worst_coin_ret": Dm[Dm.br <= q[0]]["coin_return"].mean(),
        "best_coin_ret": Dm[Dm.br >= q[1]]["coin_return"].mean(),
        "n_worst_days": int((bkdf.br <= q[0]).sum())})
    return out
