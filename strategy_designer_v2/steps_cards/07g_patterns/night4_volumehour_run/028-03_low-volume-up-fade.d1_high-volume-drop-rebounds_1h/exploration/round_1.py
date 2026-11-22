def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            vr = b["volume"] / b["volume"].rolling(720, min_periods=240).mean()
            d = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                              "z": r1 / sd, "vr": vr, "r1": r1,
                              "ts": pd.to_datetime(b["timestamp"]),
                              "alloc": b["postRebalance_current_allocation"].values,
                              "fc": b["forecast"].values})
            d["sd24"] = r1.rolling(24, min_periods=24).std() / sd
            d["ret24"] = c / c.shift(24) - 1
            d["ret24z"] = d["ret24"] / (sd * np.sqrt(24))
            d["ret6z"] = (c / c.shift(6) - 1) / (sd * np.sqrt(6))
            for h in [1, 2, 6, 24]:
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["hour"] = D["ts"].dt.hour
    D["wd"] = D["ts"].dt.weekday

    def tstat(x):
        x = x.dropna()
        n = len(x)
        if n < 3: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(n))})

    zb = pd.cut(D["z"], [-np.inf, -4, -2.5, -1.5, 1.5, 2.5, 4, np.inf])
    vb = pd.cut(D["vr"], [0, 1, 2, 4, np.inf])
    D["zb"] = zb.astype(str); D["vb"] = vb.astype(str)
    for h in [2, 6, 24]:
        g = D[D["pos"] % h == 0].copy()
        drift = g.groupby("coin")[f"f{h}"].transform("mean")
        g["u"] = g[f"f{h}"] - drift
        g["cont"] = np.sign(g["r1"]) * g["u"]
        out[f"h{h} unusual by z bucket x vol bucket"] = g.groupby(["zb", "vb"])["u"].apply(tstat).unstack()
        if h == 6:
            g["r24b"] = pd.qcut(g["ret24z"], 10, labels=False, duplicates="drop")
            out["h6 unusual by 24h return z decile"] = g.groupby("r24b")["u"].apply(tstat).unstack()
        if h == 24:
            g["r24b"] = pd.qcut(g["ret24z"], 10, labels=False, duplicates="drop")
            out["h24 unusual by 24h return z decile"] = g.groupby("r24b")["u"].apply(tstat).unstack()
            g["volb"] = pd.qcut(g["sd24"], 5, labels=False, duplicates="drop")
            out["h24 unusual by 24h vol/30d vol quintile"] = g.groupby("volb")["u"].apply(tstat).unstack()
    g1 = D.copy()
    g1["u"] = g1["f1"] - g1.groupby("coin")["f1"].transform("mean")
    out["h1 unusual by UTC hour"] = g1.groupby("hour")["u"].apply(tstat).unstack()
    # book
    days = pd.concat([df.assign(coin=c, w=w) for c in data["days"] for w, df in data["days"][c].items()])
    days["wd"] = pd.to_datetime(days["day"]).dt.weekday
    out["book vs coin daily by weekday"] = days.groupby("wd").agg(book_bp=("book_return", lambda x: x.mean()*1e4),
                                                               coin_bp=("coin_return", lambda x: x.mean()*1e4), n=("book_return", "count"))
    # position gain before costs by allocation bucket
    D["gain"] = D["alloc"] * D["f1"]
    D["ab"] = pd.cut(D["alloc"], [-0.01, 0.0001, 0.25, 0.5, 1, 3])
    out["gross gain per bar by allocation"] = D.groupby(D["ab"].astype(str))["gain"].apply(tstat).unstack()
    tr = pd.concat([df.assign(coin=c) for c in data["trades"] for df in data["trades"][c].values()])
    tr["fb"] = pd.qcut(tr["entry_forecast"], 5, duplicates="drop").astype(str)
    out["trades by entry forecast quintile"] = tr.groupby("fb").agg(n=("net_profit_loss_percent", "count"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), dur_min=("duration_minutes", "median"))
    return out
