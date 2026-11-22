def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            hh = hi.rolling(30).max(); ll = lo.rolling(30).min(); rng = hh - ll
            mid = (hh + ll) / 2
            pos = (c - mid) / rng
            nmr = (c - c.shift(30)).abs() / rng
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60, min_periods=30).std()
            past5 = c / c.shift(5) - 1
            past30 = c / c.shift(30) - 1
            fwd = c.shift(-H) / c - 1
            d = pd.DataFrame({"coin": coin, "w": w, "pos": pos, "nmr": nmr, "vol20": vol20,
                              "volratio": vol20 / vol60, "past5": past5, "past30": past30,
                              "fwd": fwd, "past5z": past5 / (vol20 * np.sqrt(5)),
                              "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                              "fc": b["forecast"], "grid": (np.arange(len(b)) % H == 0),
                              "rng_pct": rng / c})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[A.grid & A.fwd.notna()].copy()
    drift = G.groupby("coin").fwd.mean(); sd = G.groupby("coin").fwd.std()
    G["ex"] = G.fwd - G.coin.map(drift)
    G["z"] = G.ex / G.coin.map(sd)
    def summ(df, key):
        g = df.groupby(key, observed=True)["ex"]
        out = g.agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        out["strength"] = df.groupby(key, observed=True)["z"].mean()
        return out.drop(columns="std").round(4)
    G2 = G.dropna(subset=["pos", "nmr"]).copy()
    G2["posq"] = pd.qcut(G2.pos, 5, labels=False)
    G2["flat"] = np.where(G2.nmr <= 0.3, "flat", "trend")
    res = {}
    res["drift_sd_by_coin"] = pd.DataFrame({"drift": drift, "sd": sd}).round(4)
    res["pos_quintile_x_flat"] = summ(G2, ["flat", "posq"])
    G3 = G.dropna(subset=["past5z"]).copy()
    G3["p5q"] = pd.qcut(G3.past5z, 5, labels=False)
    res["past5z_quintile"] = summ(G3, "p5q")
    G4 = G.dropna(subset=["past30"]).copy()
    G4["p30q"] = pd.qcut(G4.groupby("coin").past30.rank(pct=True), 5, labels=False)
    res["past30_quintile_coinrank"] = summ(G4, "p30q")
    G5 = G.dropna(subset=["vol20"]).copy()
    G5["vq"] = pd.qcut(G5.groupby("coin").vol20.rank(pct=True), 5, labels=False)
    res["vol20_quintile_coinrank"] = summ(G5, "vq")
    G6 = G.dropna(subset=["volratio"]).copy()
    G6["vrq"] = pd.qcut(G6.volratio, 5, labels=False)
    res["volratio_quintile"] = summ(G6, "vrq")
    G7 = G.dropna(subset=["rng_pct", "pos"]).copy()
    G7["rq"] = pd.qcut(G7.groupby("coin").rng_pct.rank(pct=True), 3, labels=False)
    G7["side"] = np.where(G7.pos < 0, "below", "above")
    res["rangewidth_x_side"] = summ(G7, ["rq", "side"])
    # daily returns by weekday (all bars)
    A["r1n"] = A.groupby(["coin", "w"]).apply(lambda x: x.index.to_series()).reset_index(drop=True) if False else np.nan
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["w"] = w
            dd.append(x)
    D = pd.concat(dd, ignore_index=True)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    wdg = D.groupby("wd").coin_return.agg(["count", "mean", "std"])
    wdg["t"] = wdg["mean"] / (wdg["std"] / np.sqrt(wdg["count"]))
    res["coin_return_by_weekday"] = wdg.round(5)
    # book daily
    bk = D.groupby(["w", "day"]).agg(b=("book_return", "mean"), h=("coin_return", "mean")).dropna()
    s = bk.b
    res["book_sharpe_mean"] = pd.Series({"mean": s.mean(), "sharpe": s.mean() / s.std() * np.sqrt(365),
                                         "hold_mean": bk.h.mean(), "corr_book_hold": s.corr(bk.h)}).round(5)
    top = bk.sort_values("b")
    res["book_extremes"] = pd.DataFrame({"worst20_book": [top.b.head(20).mean()], "worst20_hold": [top.h.head(20).mean()],
                                         "best20_book": [top.b.tail(20).mean()], "best20_hold": [top.h.tail(20).mean()]}).round(4)
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T, ignore_index=True)
    T["days"] = T.duration_minutes / 1440
    T["dq"] = pd.qcut(T.days.rank(method="first"), 4, labels=False)
    res["trades_by_duration_q"] = T.groupby("dq").agg(n=("days", "size"), days=("days", "mean"),
                                                     pnl=("net_profit_loss_percent", "mean"),
                                                     win=("net_profit_loss_percent", lambda x: (x > 0).mean())).round(3)
    return res
