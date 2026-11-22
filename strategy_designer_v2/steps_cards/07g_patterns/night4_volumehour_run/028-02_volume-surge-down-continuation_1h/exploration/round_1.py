def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            z = r / sd
            vr = v / v.rolling(720, min_periods=240).mean()
            r24 = c / c.shift(24) - 1
            z24 = r24 / (sd * np.sqrt(24))
            rv = r.rolling(24).std() / sd
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr, "z24": z24, "rv": rv,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "pos": np.arange(len(b)),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            for h in (1, 6, 24):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    def tt(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan})
    # drift-removed per coin
    for h in (1, 6, 24):
        g = d[d.pos % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(dr)
    g6 = d[d.pos % 6 == 0].dropna(subset=["z", "vr", "u6"]).copy()
    g6["zb"] = pd.cut(g6.z, [-np.inf, -3, -1.5, -0.5, 0.5, 1.5, 3, np.inf])
    g6["vb"] = pd.cut(g6.vr, [0, 1, 2, 4, np.inf])
    out["u6 by z bin x vol bin (mean bp)"] = g6.pivot_table(index="zb", columns="vb", values="u6", aggfunc="mean", observed=True) * 1e4
    out["u6 by z bin x vol bin (n)"] = g6.pivot_table(index="zb", columns="vb", values="u6", aggfunc="count", observed=True)
    out["u6 by z bin"] = g6.groupby("zb", observed=True)["u6"].apply(tt).unstack()
    g24 = d[d.pos % 24 == 0].dropna(subset=["z24", "u24"]).copy()
    g24["zb"] = pd.cut(g24.z24, [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out["u24 by prior 24h z"] = g24.groupby("zb", observed=True)["u24"].apply(tt).unstack()
    g6["zb24"] = pd.cut(g6.z24, [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out["u6 by prior 24h z"] = g6.groupby("zb24", observed=True)["u6"].apply(tt).unstack()
    g6["rvb"] = pd.qcut(g6.rv, 5)
    out["u6 and |f6| by 24h vol ratio quintile"] = g6.groupby("rvb", observed=True).agg(u6_bp=("u6", lambda x: x.mean()*1e4), absf6_bp=("f6", lambda x: x.abs().mean()*1e4), n=("u6", "size"))
    g1 = d.dropna(subset=["u1"])
    out["u1 by hour"] = g1.groupby("hour")["u1"].apply(tt).unstack()
    out["u1 by weekday"] = g1.groupby("wd")["u1"].apply(tt).unstack()
    out["u1 by hour by coin t"] = g1.groupby(["hour", "coin"])["u1"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x)))).unstack()
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd)
    out["book daily mean by window"] = dd.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    t = pd.concat([x.assign(coin=c) for c, ws in data["trades"].items() for x in ws.values()])
    out["trades"] = t.groupby("coin").agg(n=("side", "size"), pl_bp=("profit_loss_percent", "mean"), net_bp=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean()/60))
    return out
