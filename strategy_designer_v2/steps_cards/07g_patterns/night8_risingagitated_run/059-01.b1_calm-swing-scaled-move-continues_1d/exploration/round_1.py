def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            ret20 = c / c.shift(20) - 1
            sc = ret20 / (sd20 * np.sqrt(20))
            ret60 = c / c.shift(60) - 1
            ret5p = c / c.shift(5) - 1
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "sc": sc, "ret20": ret20, "ret60": ret60, "ret5p": ret5p, "r1": r1,
                "fwd5": fwd5, "fwd1": fwd1, "rng": rng, "clv": clv,
                "calm": (b["regime"] != "chop").values,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "sd20": sd20,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift5 = A.groupby("coin").apply(lambda d: d[d.pos % 5 == 0]["fwd5"].mean())
    sd5 = A.groupby("coin").apply(lambda d: d[d.pos % 5 == 0]["fwd5"].std())
    A["ex5"] = A["fwd5"] - A["coin"].map(drift5)
    A["z5"] = A["ex5"] / A["coin"].map(sd5)
    G = A[(A.pos % 5 == 0)].dropna(subset=["ex5", "sc"]).copy()
    G["trend"] = np.where(G.ret60 > 0.10, "rising", np.where(G.ret60 < -0.10, "falling", "choppy"))
    G.loc[G.ret60.isna(), "trend"] = "na"
    G["agit"] = np.where(G.calm, "calm", "agit")

    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    # signed continuation by profile: ex5 * sign(sc)
    G["dirret"] = G.ex5 * np.sign(G.sc)
    out["dir_by_profile"] = G.groupby(["trend", "agit"])["dirret"].apply(tt).unstack()
    # slope t by profile
    def slope(d):
        if len(d) < 30: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        s = stats.linregress(d.sc, d.ex5)
        return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})
    out["slope_by_profile"] = G.groupby(["trend", "agit"]).apply(slope)
    G["scq"] = pd.qcut(G.sc, 5, labels=False)
    out["ex5_by_sc_quintile_agit"] = G.groupby(["agit", "scq"])["ex5"].apply(tt).unstack()
    # raw 20d return vs scaled
    G["r20q"] = pd.qcut(G.ret20, 5, labels=False)
    out["ex5_by_ret20_quintile"] = G.groupby("r20q")["ex5"].apply(tt).unstack()
    # short-term: 5-day past return
    G["r5q"] = pd.qcut(G.ret5p, 5, labels=False)
    out["ex5_by_ret5past_quintile"] = G.groupby(["agit", "r5q"])["ex5"].apply(tt).unstack()
    # daily: next-day after large 1d moves scaled by sd20
    A["z1"] = A.r1 / A.sd20
    D = A.dropna(subset=["z1", "fwd1"]).copy()
    D["z1q"] = pd.qcut(D.z1, 10, labels=False)
    D["exf1"] = D.fwd1 - D.coin.map(A.groupby("coin").fwd1.mean())
    out["next1_by_z1_decile"] = D.groupby("z1q")["exf1"].apply(tt).unstack()
    D["clvq"] = pd.qcut(D.clv, 5, labels=False)
    out["next1_by_closeloc_agit"] = D.groupby([np.where(D.calm, "calm", "agit"), "clvq"])["exf1"].apply(tt).unstack()
    out["next1_by_weekday"] = D.groupby("wd")["exf1"].apply(tt).unstack()
    D["rngq"] = D.groupby("coin")["rng"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["next1_by_rangeq"] = D.groupby("rngq")["exf1"].apply(tt).unstack()
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    DD = pd.concat(dd)
    DD["wd"] = pd.to_datetime(DD.day).dt.dayofweek
    out["book_by_window"] = DD.groupby("win")[["book_return", "coin_return"]].mean() * 100
    out["book_by_coin"] = DD.groupby("coin")[["book_return", "coin_return"]].mean() * 100
    out["book_by_weekday"] = DD.groupby("wd")["book_return"].apply(tt).unstack()
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    T["efq"] = pd.qcut(T.entry_forecast.abs(), 4, labels=False, duplicates="drop")
    out["trades_by_abs_entry_fc"] = T.groupby(["side", "efq"])["net_profit_loss_percent"].agg(["count", "mean"])
    return out
