def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r30 = c / c.shift(30) - 1
            r7b = c / c.shift(7) - 1
            r1 = c / c.shift(1) - 1
            vol20 = r1.rolling(20).std()
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            fwd3 = c.shift(-3) / c - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n, H):
                rows.append(dict(coin=coin, w=w, i=i, regime=b["regime"].iloc[i],
                                 r30=r30.iloc[i], r7b=r7b.iloc[i], r1=r1.iloc[i],
                                 vol20=vol20.iloc[i], fwd=fwd.iloc[i], fwd1=fwd1.iloc[i], fwd3=fwd3.iloc[i],
                                 rng=rng.iloc[i], clpos=clpos.iloc[i], wd=ts.iloc[i].weekday(),
                                 fc=b["forecast"].iloc[i], day=ts.iloc[i].floor("D")))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].mean()
    df["ex"] = df["fwd"] - df["coin"].map(drift)
    out = {}
    out["regime counts"] = df["regime"].value_counts()

    def tq(g, col, by):
        g = g.dropna(subset=[col, "ex"]).copy()
        g["q"] = pd.qcut(g[col], 5, labels=False, duplicates="drop")
        a = g.groupby("q").agg(n=("ex", "size"), xmean=(col, "mean"), ex=("ex", "mean"), sd=("ex", "std"))
        a["t"] = a["ex"] / (a["sd"] / np.sqrt(a["n"]))
        return a.drop(columns="sd")

    for reg in df["regime"].unique():
        g = df[df.regime == reg]
        out[f"7d ex by r30 quintile, regime {reg}"] = tq(g, "r30", None)
        out[f"7d ex by prior-7d quintile, regime {reg}"] = tq(g, "r7b", None)
    out["7d ex by r30 quintile, all"] = tq(df, "r30", None)
    out["7d ex by prior 7d quintile, all"] = tq(df, "r7b", None)
    out["7d ex by vol20 quintile, all"] = tq(df, "vol20", None)
    out["7d ex by range quintile, all"] = tq(df, "rng", None)
    out["7d ex by close position quintile, all"] = tq(df, "clpos", None)
    # correlations
    cc = {}
    for reg in list(df["regime"].unique()) + ["all"]:
        g = df if reg == "all" else df[df.regime == reg]
        for col in ["r30", "r7b", "r1", "vol20", "rng", "clpos"]:
            gg = g.dropna(subset=[col, "ex"])
            if len(gg) > 10:
                rho, p = stats.spearmanr(gg[col], gg["ex"])
                cc[f"{reg}|{col}"] = (len(gg), round(rho, 4), round(p, 4))
    out["spearman col vs 7d ex"] = pd.DataFrame(cc, index=["n", "rho", "p"]).T
    # by window, r30 slope
    sw = []
    for w, g in df.dropna(subset=["r30", "ex"]).groupby("w"):
        if len(g) > 8:
            rho, p = stats.spearmanr(g["r30"], g["ex"])
            sw.append((w, len(g), rho, g["fwd"].mean()))
    out["by window r30 rho"] = pd.DataFrame(sw, columns=["w", "n", "rho", "meanfwd"]).set_index("w")
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["coin daily return by weekday"] = D.groupby("wd")["coin_return"].agg(["count", "mean", "std"]).assign(t=lambda x: x["mean"]/(x["std"]/np.sqrt(x["count"])))
    out["book daily by window"] = D.groupby("w")["book_return"].agg(["count", "mean", "std"])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; tr.append(t)
    T = pd.concat(tr)
    T["dq"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades by entry forecast quartile"] = T.groupby("dq").agg(n=("net_profit_loss_percent", "size"), fc=("entry_forecast", "mean"), pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), dur_days=("duration_minutes", lambda x: x.mean()/1440))
    out["trades side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
