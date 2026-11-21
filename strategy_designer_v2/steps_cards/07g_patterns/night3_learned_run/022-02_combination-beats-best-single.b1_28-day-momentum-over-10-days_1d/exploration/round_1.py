def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            r28 = c / c.shift(28) - 1
            r5 = c / c.shift(5) - 1
            vol20 = r1.rolling(20).std()
            hi60 = c.rolling(60, min_periods=30).max()
            near = c / hi60 - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            wd = pd.to_datetime(df["timestamp"]).dt.weekday
            for t in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, t=t, year=yr[t], wd=wd[t],
                                 fwd=c[t + H] / c[t] - 1, fc=df["forecast"].iloc[t],
                                 r28=r28[t], r5=r5[t], r1=r1[t], vol=vol20[t], near=near[t],
                                 alloc=df["postRebalance_current_allocation"].iloc[t]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["z"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")
    out = {}

    def binned(col, q=5):
        d = g.dropna(subset=[col, "z"]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        r = d.groupby("b").agg(n=("z", "size"), mean_ex=("ex", "mean"), mean_z=("z", "mean"),
                               t=("z", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
        return r

    for col in ["fc", "r28", "r5", "r1", "vol", "near"]:
        out["quintile_" + col] = binned(col)
    # slope per regime of vol: momentum strength by vol tercile
    d = g.dropna(subset=["r28", "vol", "z"]).copy()
    d["vt"] = d.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["s"] = np.sign(d["r28"]) * d["z"]
    out["mom_sign_z_by_voltercile"] = d.groupby("vt")["s"].agg(["size", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    out["mom_sign_z_by_year"] = d.groupby("year")["s"].agg(["size", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    out["mom_sign_z_by_coin"] = d.groupby("coin")["s"].agg(["size", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    d["side"] = np.where(d["r28"] > 0, "up", "down")
    out["mom_by_side"] = d.groupby("side")["s"].agg(["size", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            b = data["bars"][coin][w].sort_values("timestamp")
            a = b["postRebalance_current_allocation"].astype(float).values
            x = df.copy()
            x["coin"] = coin; x["win"] = w
            x["alloc_prev"] = pd.Series(a[:len(x)]).shift(1).values if len(a) >= len(x) else np.nan
            x["vol"] = x["coin_return"].rolling(20).std()
            x["year"] = pd.to_datetime(x["day"]).dt.year
            dd.append(x)
    D = pd.concat(dd, ignore_index=True)
    D["side"] = np.sign(D["alloc_prev"])
    out["book_by_side"] = D.groupby("side")["book_return"].agg(["size", "mean", "std"])
    out["book_by_year"] = D.groupby("year")["book_return"].agg(["size", "mean", "std"])
    D["vt"] = D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["book_by_voltercile"] = D.groupby("vt")["book_return"].agg(["size", "mean", "std"])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()], ignore_index=True)
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["size", "mean", "median", "std"])
    T["af"] = pd.qcut(T["entry_forecast"].abs().rank(method="first"), 4, labels=False)
    out["trades_by_absfc_q"] = T.groupby("af")["net_profit_loss_percent"].agg(["size", "mean", "median"])
    out["n_cases"] = len(g)
    return out
