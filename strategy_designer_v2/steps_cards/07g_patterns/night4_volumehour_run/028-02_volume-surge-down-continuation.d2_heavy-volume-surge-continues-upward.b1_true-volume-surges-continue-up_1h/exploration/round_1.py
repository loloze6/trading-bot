def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 4
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std().shift(1)
            vm = v.rolling(720, min_periods=240).mean().shift(1)
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "z": r / sd, "vr": v / vm,
                "r24z": (c / c.shift(24) - 1) / (sd * np.sqrt(24)),
                "volreg": sd / sd.rolling(720, min_periods=240).median(),
                "fwd4": c.shift(-H) / c - 1,
                "fwd12": c.shift(-12) / c - 1,
                "hour": pd.to_datetime(b["timestamp"]).dt.hour,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": b["postRebalance_current_allocation"].astype(float),
                "fc": b["forecast"].astype(float),
            })
            df["onGrid"] = (np.arange(len(df)) % H) == 0
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.onGrid].groupby("coin")["fwd4"].mean()
    A["ex4"] = A["fwd4"] - A["coin"].map(drift)
    G = A[A.onGrid].dropna(subset=["z", "vr", "ex4"]).copy()
    def summ(g, col="ex4"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_bp": x.mean()*1e4,
                          "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    G["zb"] = pd.cut(G.z, [-np.inf, -4, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 4, np.inf])
    G["vb"] = pd.cut(G.vr, [0, 1, 2, 4, np.inf])
    out = {}
    out["by_z"] = G.groupby("zb", observed=True).apply(summ)
    t = G[G.z.abs() > 2.5].copy()
    t["dir_ex"] = np.sign(t.z) * t.ex4
    out["big_moves_dirret_by_vol"] = t.groupby("vb", observed=True).apply(lambda g: summ(g, "dir_ex"))
    out["big_moves_dirret_by_coin_sign"] = t.groupby(["coin", np.sign(t.z)]).apply(lambda g: summ(g, "dir_ex"))
    G["r24b"] = pd.qcut(G.r24z, 5)
    out["by_24h_move"] = G.groupby("r24b", observed=True).apply(summ)
    G["vrb"] = pd.qcut(G.volreg, 4)
    out["by_vol_regime"] = G.groupby("vrb", observed=True).apply(summ)
    out["by_hour"] = G.groupby("hour").apply(summ)
    out["by_weekday"] = G.groupby("wd").apply(summ)
    # book
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            d.append(x.assign(coin=coin, w=w))
    D = pd.concat(d)
    out["book_by_window"] = D.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).mul(1e4).round(1).T
    T = pd.concat([t2.assign(coin=c) for c, ws in data["trades"].items() for t2 in ws.values()])
    out["trades"] = pd.Series({"n": len(T), "gross_mean_pct": T.profit_loss_percent.mean(),
                               "net_mean_pct": T.net_profit_loss_percent.mean(),
                               "dur_h_median": T.duration_minutes.median()/60,
                               "win_share": (T.profit_loss_percent > 0).mean()})
    out["share_time_in_market"] = (A.pos.abs() > 1e-6).mean()
    return out
