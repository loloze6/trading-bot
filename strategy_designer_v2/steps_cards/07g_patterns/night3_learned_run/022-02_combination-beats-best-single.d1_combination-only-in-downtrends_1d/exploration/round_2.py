def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    rows = []
    for coin in bars:
        allr5 = []; allr1 = []
        for w, df in bars[coin].items():
            c = df["close"].reset_index(drop=True)
            idx = np.arange(0, len(c) - 5, 5)
            allr5 += list((c.shift(-5) / c - 1).iloc[idx].dropna())
            allr1 += list((c.shift(-1) / c - 1).dropna())
        d5 = np.mean(allr5); d1 = np.mean(allr1); sd5 = np.std(allr5, ddof=1)
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True); c = df["close"]
            f = pd.DataFrame({"coin": coin, "w": w,
                "fwd5": c.shift(-5)/c - 1 - d5, "fwd5raw": c.shift(-5)/c - 1,
                "fwd1": c.shift(-1)/c - 1 - d1,
                "ret90": c/c.shift(90) - 1, "ret28": c/c.shift(28) - 1,
                "fc": df["forecast"], "regime": df["regime"],
                "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(df["timestamp"]).dt.year,
                "grid": (np.arange(len(df)) % 5 == 0)})
            rows.append(f)
    B = pd.concat(rows, ignore_index=True)
    G = B[B["grid"]]
    def summ(g):
        return pd.DataFrame({"mean": g.mean(), "n": g.size(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    res = {}
    dec = G[(G["regime"] == "mean_reversion")].dropna(subset=["fwd5"])
    res["dec_vs_rest_fwd5"] = summ(G.dropna(subset=["fwd5"]).groupby("regime")["fwd5"])
    d2 = dec.dropna(subset=["ret90"]).copy()
    d2["q"] = d2.groupby("coin")["ret90"].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
    res["dec_ret90_quint_fwd5"] = summ(d2.groupby("q")["fwd5"])
    res["dec_ret90_rho"] = pd.Series(stats.spearmanr(d2["ret90"], d2["fwd5"]), index=["rho", "p"])
    a = G.dropna(subset=["ret90", "fwd5"]).copy()
    a["q"] = a.groupby("coin")["ret90"].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
    res["all_ret90_quint_fwd5"] = summ(a.groupby("q")["fwd5"])
    # side of forecast on decline grid
    dd = dec[dec["fc"] != 0].copy(); dd["side"] = np.sign(dd["fc"])
    res["dec_by_fcside_fwd5raw"] = summ(dd.groupby("side")["fwd5raw"])
    # weekday stability: by half of years, and by coin
    W = B.dropna(subset=["fwd1"]).copy()
    W["half"] = np.where(W["yr"] <= 2021, "early", "late")
    res["wd_early"] = summ(W[W.half == "early"].groupby("wd")["fwd1"])
    res["wd_late"] = summ(W[W.half == "late"].groupby("wd")["fwd1"])
    fri = W[W.wd == 4]; mon = W[W.wd == 0]
    res["fri_by_coin"] = summ(fri.groupby("coin")["fwd1"])
    # trades: short by entry_forecast size
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()], ignore_index=True)
    T["af"] = T["entry_forecast"].abs()
    T["q"] = T.groupby("side")["af"].transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=False))
    res["trades_side_fcsize"] = T.groupby(["side", "q"])["profit_loss_percent"].agg(["mean", "count"])
    res["trades_dur_days"] = T.groupby("side")["duration_minutes"].median() / 1440
    return res
