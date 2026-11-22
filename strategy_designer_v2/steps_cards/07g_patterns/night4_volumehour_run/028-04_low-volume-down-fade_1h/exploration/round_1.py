def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            mabs = r1.abs().shift(1).rolling(720, min_periods=240).mean()
            vr = v / v.shift(1).rolling(720, min_periods=240).mean()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "z": r1 / mabs, "vr": vr,
                               "f2": c.shift(-2)/c-1, "f6": c.shift(-6)/c-1, "f24": c.shift(-24)/c-1,
                               "r24": c/c.shift(24)-1, "vol": mabs,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "pos": np.arange(len(b))})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    g6 = d[d.pos % 6 == 0].copy()
    drift = g6.groupby("coin")["f6"].mean()
    g6["u6"] = g6["f6"] - g6["coin"].map(drift)
    sd6 = g6.groupby("coin")["f6"].std()
    out["drift_sd6"] = pd.DataFrame({"drift": drift, "sd": sd6})
    # move bins x volume bins, signed in move direction (continuation positive)
    g = g6.dropna(subset=["z", "vr", "u6"]).copy()
    g["zb"] = pd.cut(g.z, [-np.inf, -4, -2.5, -1.5, 1.5, 2.5, 4, np.inf])
    g["vb"] = pd.cut(g.vr, [0, 0.667, 1.5, 3, np.inf])
    def agg(x):
        return pd.Series({"n": len(x), "mean_u6_bp": x.u6.mean()*1e4,
                          "t": x.u6.mean()/(x.u6.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["u6_by_move_x_vol"] = g.groupby(["zb", "vb"], observed=True).apply(agg)
    # 24h return regime
    g["r24b"] = pd.qcut(g.r24, 5, labels=False)
    out["u6_by_r24_quint"] = g.groupby("r24b").apply(agg)
    g["volb"] = g.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["u6_by_vol_quint"] = g.groupby("volb").apply(agg)
    out["u6_by_weekday"] = g.groupby("wd").apply(agg)
    # hour: use 1h-grid? use every bar's 1h fwd on grid of 1
    d["f1"] = d.groupby(["coin", "w"])["f2"].transform(lambda s: s) # placeholder
    h = d.copy()
    h["n1"] = h.groupby(["coin","w"])["pos"].transform(lambda s: s)  
    out["u6_by_hour_bucket"] = g.assign(hb=g.hour // 3).groupby("hb").apply(agg)
    # 24h horizon after large moves
    g24 = d[d.pos % 24 == 0].dropna(subset=["z","vr","f24"]).copy()
    dr24 = g24.groupby("coin")["f24"].mean()
    g24["u6"] = g24.f24 - g24.coin.map(dr24)
    g24["zb"] = pd.cut(g24.z, [-np.inf, -2.5, -1.5, 1.5, 2.5, np.inf])
    out["u24_by_move"] = g24.groupby("zb", observed=True).apply(agg)
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, w=w))
    dd = pd.concat(dd).dropna(subset=["book_return", "coin_return"])
    dd["cb"] = pd.qcut(dd.coin_return, 5, labels=False)
    out["book_by_coinday_quint"] = dd.groupby("cb").agg(n=("book_return","size"), book_bp=("book_return", lambda s: s.mean()*1e4), coin_bp=("coin_return", lambda s: s.mean()*1e4))
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades"] = tr.groupby("coin").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), win=("profit_loss_percent", lambda s:(s>0).mean()))
    return out
