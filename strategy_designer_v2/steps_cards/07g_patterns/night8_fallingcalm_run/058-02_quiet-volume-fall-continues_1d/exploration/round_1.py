def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r1 = c.pct_change()
            fwd = c.shift(-H) / c - 1
            r30 = c / c.shift(30) - 1
            r60 = c / c.shift(60) - 1
            r5p = c / c.shift(5) - 1
            vol30 = r1.rolling(30).std()
            vrat = v.rolling(30).mean() / v.expanding().mean().shift(30)
            vrat5 = v.rolling(5).mean() / v.rolling(60).mean()
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)), "fwd": fwd,
                "r1": r1, "r5p": r5p, "r30": r30, "r60": r60, "vol30": vol30,
                "vrat": vrat, "vrat5": vrat5, "rng": rng, "clv": clv,
                "fc": b["forecast"].astype(float), "reg": b["regime"].astype(str),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": ts.dt.weekday, "yr": ts.dt.year,
            })
            d["volz"] = d["vol30"] / d["vol30"].rolling(len(d), min_periods=30).median()
            d["s1"] = d["r1"] / d["vol30"].shift(1)
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["fx"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A.pos % H == 0) & A.fx.notna()].copy()

    def summ(g):
        x = g["fx"]
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["regime"] = G.groupby("reg").apply(summ)
    for col in ["r30", "r60", "vrat", "vrat5", "s1", "r5p", "volz", "rng", "clv"]:
        g = G[G[col].notna()].copy()
        g["q"] = pd.qcut(g[col], 5, labels=False, duplicates="drop")
        out["q5 " + col] = g.groupby("q").apply(summ)
    fc = G[G.fc < 0].copy()
    fc["q"] = pd.qcut(fc["vrat"], 3, labels=False, duplicates="drop")
    out["in fc<0 by vrat tercile"] = fc.groupby("q").apply(summ)
    fc["q2"] = pd.qcut(fc["r30"], 3, labels=False, duplicates="drop")
    out["in fc<0 by r30 tercile"] = fc.groupby("q2").apply(summ)
    out["weekday"] = G.groupby("wd").apply(summ)
    out["year"] = G.groupby("yr").apply(summ)
    # trend by 60d within windows
    g = G[G.r60.notna()].copy()
    g["tr"] = np.where(g.r60 > 0.1, "rising", np.where(g.r60 < -0.1, "falling", "choppy"))
    g["ag"] = np.where(g.volz > 1, "agit", "calm")
    out["trend x agit (window-local)"] = g.groupby(["tr", "ag"]).apply(summ)
    # book daily largest days
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.copy(); dd["coin"] = coin; dd["win"] = w; D.append(dd)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    held = D[D.book_return.abs() > 1e-9]
    out["book days held"] = pd.Series({"n": len(held), "mean%": 100*held.book_return.mean(),
                                       "coin mean% those days": 100*held.coin_return.mean(),
                                       "corr": held.book_return.corr(held.coin_return)})
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
