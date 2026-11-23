def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            fwd = c.shift(-H) / c - 1
            past1 = r1
            past5 = c / c.shift(5) - 1
            past20 = c / c.shift(20) - 1
            vol20 = r1.rolling(20).std()
            hi30 = c / c.rolling(30).max() - 1
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "win": w, "fwd": fwd, "past1": past1, "past5": past5,
                              "past20": past20, "vol20": vol20, "hi30": hi30,
                              "fc": b["forecast"].astype(float),
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "wd": ts.dt.weekday, "yr": ts.dt.year})
            d = d.iloc[::H]
            rows.append(d)
    df = pd.concat(rows).dropna(subset=["fwd"])
    # excess over coin mean
    df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    df["vstd"] = df["past1"] / df["vol20"]
    out = {}
    def by_q(col, name, q=5):
        s = df.dropna(subset=[col]).copy()
        s["q"] = s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        g = s.groupby("q")["ex"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        out[name] = g.round(5)
        # spearman pooled per coin rank corr
        rc = s.groupby("coin").apply(lambda x: stats.spearmanr(x[col], x["ex"])[0])
        out[name + "_rankcorr_by_coin"] = rc.round(3)
    by_q("fc", "forecast_quint")
    by_q("past1", "past1d_quint")
    by_q("past5", "past5d_quint")
    by_q("past20", "past20d_quint")
    by_q("vol20", "vol20_quint")
    by_q("hi30", "near30dhigh_quint")
    by_q("vstd", "past1d_over_vol_quint")
    g = df.groupby("wd")["ex"].agg(["mean", "count", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["weekday"] = g.round(5)
    # book: biggest gain/loss days
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; dl.append(d)
    dd = pd.concat(dl).dropna(subset=["book_return"])
    out["book_vs_coin_corr"] = float(dd["book_return"].corr(dd["coin_return"]))
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; tl.append(t)
    tr = pd.concat(tl)
    out["trades_by_side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["mean", "count", "median"]).round(3)
    out["trades_dur_days_mean"] = float(tr["duration_minutes"].mean()/1440)
    return out
