def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    allgrid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; v = b["volume"]
            r1 = c.pct_change()
            b["fwd5"] = c.shift(-5) / c - 1
            b["fwd1"] = c.shift(-1) / c - 1
            b["fwd10"] = c.shift(-10) / c - 1
            b["past1"] = r1
            b["past5"] = c / c.shift(5) - 1
            b["past20"] = c / c.shift(20) - 1
            vol20 = r1.rolling(20).std()
            b["vol20"] = vol20
            b["z1"] = r1 / vol20.shift(1)
            b["z5"] = b["past5"] / (vol20 * np.sqrt(5))
            b["z20"] = b["past20"] / (vol20 * np.sqrt(20))
            rng = (b["high"] - b["low"])
            b["clv"] = (c - b["low"]) / rng.replace(0, np.nan)
            b["rngz"] = (rng / c) / ((rng / c).rolling(20).mean().shift(1))
            b["volz"] = v / v.rolling(20).mean().shift(1)
            b["hi20"] = c / b["high"].rolling(20).max() - 1
            b["lo20"] = c / b["low"].rolling(20).min() - 1
            b["volchg"] = vol20 / r1.rolling(60, min_periods=40).std()
            b["dow"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["fc_in"] = (b["regime"] == "unknown")
            b["ratio"] = b.get("debug_info.components.updown_vol.last_history_value")
            b["coin"] = coin; b["win"] = w
            g = b.iloc[::5]
            allgrid.append(g[["coin", "fwd5"]])
            rows.append(g)
    G = pd.concat(rows)
    A = pd.concat(allgrid).dropna()
    drift = A.groupby("coin")["fwd5"].mean()
    G["ex5"] = G["fwd5"] - G["coin"].map(drift)
    F = G[G["fc_in"]].dropna(subset=["ex5"])
    out = {}
    out["share in profile"] = float(G["fc_in"].mean())
    out["cases in profile"] = int(len(F))
    out["mean ex5 in profile, t"] = f"{F.ex5.mean():.4f} t {stats.ttest_1samp(F.ex5,0).statistic:.2f}"
    out["by coin"] = F.groupby("coin")["ex5"].agg(["count", "mean"])
    out["by year"] = F.groupby("year")["ex5"].agg(["count", "mean"])
    res = []
    for f in ["past1", "z1", "past5", "z5", "past20", "z20", "clv", "rngz", "volz", "hi20", "lo20", "vol20", "volchg", "ratio"]:
        d = F[[f, "ex5"]].dropna()
        if len(d) < 30: continue
        rho, p = stats.spearmanr(d[f], d["ex5"])
        q = pd.qcut(d[f].rank(method="first"), 3, labels=False)
        lo = d.ex5[q == 0]; hi = d.ex5[q == 2]
        t = stats.ttest_ind(hi, lo, equal_var=False).statistic
        res.append([f, len(d), rho, p, lo.mean(), d.ex5[q == 1].mean(), hi.mean(), t])
    out["features vs ex5 (falling calm)"] = pd.DataFrame(res, columns=["f", "n", "rho", "p", "low3", "mid3", "high3", "t_hi_lo"])
    out["by weekday"] = F.groupby("dow")["ex5"].agg(["count", "mean"])
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    out["book ret mean/std"] = f"{D.book_return.mean():.5f} / {D.book_return.std():.5f}"
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    if T:
        T = pd.concat(T)
        out["trades"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
