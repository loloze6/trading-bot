def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = d["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            z = r / sd.shift(1)
            n = len(d)
            for h in (5, 20):
                fwd = c.shift(-h) / c - 1
                d[f"f{h}"] = fwd
            d["z"] = z
            d["vol"] = sd
            d["r20p"] = c / c.shift(20) - 1
            d["coin"] = coin; d["win"] = w; d["pos"] = np.arange(n)
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.dayofweek
            d["yr"] = pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d[["coin","win","pos","z","vol","r20p","f5","f20","regime","forecast",
                           "postRebalance_current_allocation","wd","yr"]])
    A = pd.concat(rows, ignore_index=True)
    # drift per coin over all windows
    out = {}
    for h in (5, 20):
        g = A[A["pos"] % h == 0].dropna(subset=[f"f{h}"]).copy()
        drift = g.groupby("coin")[f"f{h}"].mean()
        g["u"] = g[f"f{h}"] - g["coin"].map(drift)
        g = g.dropna(subset=["z"])
        g["zb"] = pd.cut(g["z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
        t = g.groupby(["regime", "zb"], observed=True)["u"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        out[f"unusual f{h} by regime x day z"] = t.round(4)
        if h == 20:
            g["vq"] = g.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
            t2 = g.groupby(["regime", "vq"])["u"].agg(["mean", "count", "std"])
            t2["t"] = t2["mean"] / (t2["std"] / np.sqrt(t2["count"]))
            out["unusual f20 by regime x vol tercile"] = t2.round(4)
            g["mq"] = pd.qcut(g["r20p"], 5, labels=False)
            t3 = g.groupby(["regime", "mq"])["u"].agg(["mean", "count", "std"])
            t3["t"] = t3["mean"] / (t3["std"] / np.sqrt(t3["count"]))
            out["unusual f20 by regime x past20 quintile"] = t3.round(4)
            t4 = g.groupby("yr")["u"].agg(["mean", "count"])
            out["f20 unusual by year (all)"] = t4.round(4)
    # daily: next-day return by weekday
    g1 = A.copy()
    # book days
    D = []
    for coin, wins in days.items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; x["win"] = w
            x["wd"] = pd.to_datetime(x["day"]).dt.dayofweek
            x["yr"] = pd.to_datetime(x["day"]).dt.year
            D.append(x)
    D = pd.concat(D, ignore_index=True).dropna(subset=["book_return"])
    out["book & coin daily by weekday"] = D.groupby("wd")[["book_return","coin_return"]].mean().round(5)
    out["book by year"] = D.groupby("yr").agg(book=("book_return","mean"), coin=("coin_return","mean"), n=("book_return","count")).round(5)
    # position sign attribution per bar
    B = A.copy()
    # trades
    T = []
    for coin, wins in trades.items():
        for w, df in wins.items():
            if len(df): x = df.copy(); x["coin"] = coin; T.append(x)
    T = pd.concat(T, ignore_index=True)
    tt = T.groupby(["side","entry_regime"])["net_profit_loss_percent"].agg(["mean","median","count","std"])
    tt["t"] = tt["mean"]/(tt["std"]/np.sqrt(tt["count"]))
    out["trades by side x regime"] = tt.round(3)
    T["fq"] = pd.qcut(T["entry_forecast"].abs().rank(method="first"), 4, labels=False)
    out["trades by |entry forecast| quartile x side"] = T.groupby(["side","fq"])["net_profit_loss_percent"].agg(["mean","count"]).round(3)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean","count"]).round(2)
    return out
