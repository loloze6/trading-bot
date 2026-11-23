def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 6
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]) / c
            b["rr"] = rng / rng.rolling(30, min_periods=20).mean()
            b["ret30"] = c / c.shift(30) - 1
            b["ret1"] = c / c.shift(1) - 1
            b["ret7"] = c / c.shift(7) - 1
            b["vol30"] = b["ret1"].rolling(30, min_periods=20).std()
            b["vol_rel"] = b["vol30"] / b["ret1"].rolling(120, min_periods=60).std()
            hh = b["high"].rolling(30, min_periods=20).max()
            b["near_hi"] = c / hh - 1
            b["clv"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["fwd"] = c.shift(-H) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            g = b.iloc[::H].copy()
            g["coin"] = coin; g["win"] = w
            g["wd"] = pd.to_datetime(g["timestamp"]).dt.weekday
            g["year"] = pd.to_datetime(g["timestamp"]).dt.year
            rows.append(g)
    G = pd.concat(rows, ignore_index=True)
    G = G.dropna(subset=["fwd"])
    drift = G.groupby("coin")["fwd"].transform("mean")
    G["ex"] = G["fwd"] - drift
    G["sd"] = G.groupby("coin")["fwd"].transform("std")
    G["z"] = G["ex"] / G["sd"]

    def summ(df, col):
        out = df.groupby(col, observed=True)["z"].agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        out["ex_mean"] = df.groupby(col, observed=True)["ex"].mean()
        return out.round(4)

    res = {}
    up = G[G["ret30"] > 0].copy(); dn = G[G["ret30"] <= 0].copy()
    for name, df in [("up", up), ("dn", dn)]:
        df["q"] = pd.qcut(df["rr"], 5, labels=False, duplicates="drop")
        res[f"rangeratio_q_{name}"] = summ(df, "q")
    for col in ["ret1", "ret7", "ret30", "vol_rel", "near_hi", "clv"]:
        G["q"] = pd.qcut(G[col], 5, labels=False, duplicates="drop")
        res[f"{col}_q"] = summ(G, "q")
    res["weekday"] = summ(G, "wd")
    res["year"] = summ(G, "year")
    G["fpos"] = np.where(G["forecast"] > 0, "pos", "flat")
    res["forecast_side"] = summ(G, "fpos")
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    dd = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    res["book_days"] = pd.Series({"n": len(dd), "mean": dd.book_return.mean(),
        "corr_coin": dd.book_return.corr(dd.coin_return),
        "top5pct_share_of_sum": dd.book_return.nlargest(int(len(dd)*0.05)).sum()/dd.book_return.sum()})
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["fq"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    res["trades_by_entryforecast"] = T.groupby("fq")[["net_profit_loss_percent", "dur_d", "entry_forecast"]].agg(["mean", "count"]).round(3)
    res["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"]).round(3)
    return res
