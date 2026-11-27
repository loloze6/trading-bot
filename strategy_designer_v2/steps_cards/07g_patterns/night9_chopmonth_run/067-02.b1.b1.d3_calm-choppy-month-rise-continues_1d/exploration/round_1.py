def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ret30 = c / c.shift(30) - 1
            ret7b = c / c.shift(7) - 1
            vol14 = r1.rolling(14).std()
            vol60 = r1.rolling(60).std()
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(b), H):
                if pd.isna(fwd.iloc[i]):
                    continue
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, wd=ts.iloc[i].dayofweek,
                                 day=ts.iloc[i].normalize(), inprof=(b["regime"].iloc[i] == "unknown"),
                                 fc=b["forecast"].iloc[i], ret30=ret30.iloc[i], ret7b=ret7b.iloc[i],
                                 r1=r1.iloc[i], volr=vol14.iloc[i] / vol60.iloc[i] if vol60.iloc[i] else np.nan,
                                 rng=rng.iloc[i], clpos=clpos.iloc[i], fwd=fwd.iloc[i]))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd"].mean()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    out = {}

    def tab(df, col, q=5):
        d = df.dropna(subset=[col, "ex"]).copy()
        d["bin"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        t = d.groupby("bin").agg(n=("ex", "size"), lo=(col, "min"), hi=(col, "max"),
                                 mean_ex=("ex", "mean"), sd=("ex", "std"))
        t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
        return t.drop(columns="sd")

    out["ret30 quintiles in profile"] = tab(g[g.inprof], "ret30")
    out["ret30 quintiles out of profile"] = tab(g[~g.inprof], "ret30")
    out["ret7 past quintiles in profile"] = tab(g[g.inprof], "ret7b")
    out["ret7 past quintiles all"] = tab(g, "ret7b")
    out["1d return quintiles all"] = tab(g, "r1")
    out["vol ratio 14/60 quintiles all"] = tab(g, "volr")
    out["range quintiles all"] = tab(g, "rng")
    out["close position quintiles all"] = tab(g, "clpos")
    out["close position quintiles in profile"] = tab(g[g.inprof], "clpos")

    # signed effect by year in profile
    d = g[g.inprof].dropna(subset=["ret30"])
    d = d.assign(sg=np.sign(d.ret30) * d.ex)
    out["in profile signed ex by year"] = d.groupby("year")["sg"].agg(["size", "mean"])
    out["in profile signed ex by window"] = d.groupby("w")["sg"].agg(["size", "mean"])

    # daily weekday effects from days
    dl = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            x = dd.copy()
            x["coin"] = coin
            x["w"] = w
            dl.append(x)
    D = pd.concat(dl)
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.dayofweek
    D["year"] = D["day"].dt.year
    out["coin return by weekday"] = D.groupby("wd")["coin_return"].agg(
        n="size", mean="mean", t=lambda s: s.mean() / (s.std() / np.sqrt(s.count())))
    out["book return by weekday"] = D.groupby("wd")["book_return"].agg(
        mean="mean", t=lambda s: s.mean() / (s.std() / np.sqrt(s.count())))
    bk = D.groupby(["w", "day"])["book_return"].mean()
    out["book by year"] = D.groupby("year")["book_return"].agg(["size", "mean", "std"])

    # trades
    tl = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                t = t.copy()
                t["coin"] = coin
                tl.append(t)
    T = pd.concat(tl)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["size", "mean", "median", "std"])
    T["absfc"] = T["entry_forecast"].abs()
    T["fcbin"] = pd.qcut(T["absfc"], 4, labels=False, duplicates="drop")
    out["trades by abs entry forecast"] = T.groupby(["side", "fcbin"])["net_profit_loss_percent"].agg(["size", "mean"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean"])
    return out
