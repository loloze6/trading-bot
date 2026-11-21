def explore(data):
    import numpy as np, pandas as pd
    H = 120
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            if n < 900: continue
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=500).mean()
            surge = r24 / mabs
            hi = c.rolling(720, min_periods=500).max()
            dist = (hi - c) / c
            r120p = c / c.shift(120) - 1
            r720p = c / c.shift(720) - 1
            vol = np.log(c).diff().rolling(168, min_periods=100).std()
            fwd = c.shift(-H) / c - 1
            fwd24 = c.shift(-24) / c - 1
            g1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "surge": surge, "dist": dist,
                               "r5d": r120p, "r30d": r720p, "vol": vol, "fwd": fwd, "fwd24": fwd24, "g1": g1,
                               "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year})
            df["grid"] = (np.arange(n) % H == 0)
            df["grid24"] = (np.arange(n) % 24 == 0)
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def summ(g):
        x = g["unus"].dropna()
        k = len(x)
        return pd.Series({"n": k, "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(k)) if k > 2 else np.nan,
                          "strength": g.loc[x.index, "str"].mean()})
    G = A[A.grid & A.fwd.notna()].copy()
    drift = G.groupby("coin")["fwd"].mean(); sd = G.groupby("coin")["fwd"].std()
    G["unus"] = G.fwd - G.coin.map(drift); G["str"] = G.unus / G.coin.map(sd)
    Gs = G.dropna(subset=["surge", "dist"]).copy()
    try:
        Gs["surge_q"] = pd.qcut(Gs.surge.rank(method="first"), 10, labels=False)
        out["surge_decile_5d"] = Gs.groupby("surge_q").apply(summ)
        Gs["dist_q"] = pd.qcut(Gs.dist.rank(method="first"), 5, labels=False)
        out["dist_quintile_5d"] = Gs.groupby("dist_q").apply(summ)
        Gs["sup"] = (Gs.surge > 0)
        out["surge_sign_x_dist"] = Gs.groupby(["sup", "dist_q"]).apply(summ)
    except Exception as e: out["err1"] = str(e)
    try:
        G2 = Gs.dropna(subset=["r30d"]).copy()
        G2["r30_q"] = pd.qcut(G2.r30d.rank(method="first"), 5, labels=False)
        out["r30d_quintile_5d"] = G2.groupby("r30_q").apply(summ)
        G2["r5_q"] = pd.qcut(G2.r5d.rank(method="first"), 5, labels=False)
        out["r5d_quintile_5d"] = G2.groupby("r5_q").apply(summ)
        G3 = Gs.dropna(subset=["vol"]).copy()
        G3["vol_rel"] = G3.vol / G3.groupby("coin").vol.transform("median")
        G3["vol_q"] = pd.qcut(G3.vol_rel.rank(method="first"), 5, labels=False)
        out["vol_quintile_5d"] = G3.groupby("vol_q").apply(summ)
        out["by_year_5d"] = G.groupby("year").apply(summ)
    except Exception as e: out["err2"] = str(e)
    try:
        D = A[A.grid24 & A.fwd24.notna()].copy()
        D["u24"] = D.fwd24 - D.coin.map(D.groupby("coin").fwd24.mean())
        out["weekday_24h"] = D.groupby("wd")["u24"].agg(["count", "mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
        A["pos_gain"] = A.alloc * A.g1
        A["inpos"] = A.alloc.abs() > 1e-6
        out["share_in_position"] = float(A.inpos.mean())
        P = A[A.inpos & A.dist.notna()].copy()
        P["dq"] = pd.qcut(P.dist.rank(method="first"), 5, labels=False)
        out["pos_gain_by_dist_q"] = P.groupby("dq")[["pos_gain", "dist"]].agg(["count", "mean"])
        P2 = A[A.inpos & A.r30d.notna()].copy()
        P2["rq"] = pd.qcut(P2.r30d.rank(method="first"), 5, labels=False)
        out["pos_gain_by_r30d_q"] = P2.groupby("rq")[["pos_gain", "r30d"]].agg(["count", "mean"])
    except Exception as e: out["err3"] = str(e)
    try:
        T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)], ignore_index=True)
        T["fq"] = pd.qcut(T.entry_forecast.rank(method="first"), 4, labels=False)
        out["trades_by_entry_fc_q"] = T.groupby("fq")[["entry_forecast", "net_profit_loss_percent", "duration_minutes"]].agg(["count", "mean"])
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    except Exception as e: out["err4"] = str(e)
    try:
        Dy = pd.concat([d.assign(coin=c, win=w) for c, ws in data["days"].items() for w, d in ws.items()], ignore_index=True)
        bk = Dy.groupby("day")[["book_return", "coin_return"]].mean().dropna()
        out["book_vs_coin_corr"] = float(bk.corr().iloc[0, 1])
        bk["cq"] = pd.qcut(bk.coin_return.rank(method="first"), 5, labels=False)
        out["book_by_market_day_q"] = bk.groupby("cq")[["book_return", "coin_return"]].agg(["count", "mean"])
    except Exception as e: out["err5"] = str(e)
    return out
