def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            r30 = c / c.shift(30) - 1
            r7b = c / c.shift(7) - 1
            vol30 = r1.rolling(30).std()
            fwd7 = c.shift(-7) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (df["high"] - df["low"]) / c
            pos_close = (c - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for i in range(0, n, 7):
                rows.append(dict(coin=coin, w=w, i=i, inprof=(df["regime"].iloc[i] == "unknown"),
                                 r30=r30.iloc[i], r7b=r7b.iloc[i], r1=r1.iloc[i], vol30=vol30.iloc[i],
                                 fwd7=fwd7.iloc[i], fwd1=fwd1.iloc[i], rng=rng.iloc[i], pc=pos_close.iloc[i],
                                 wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year,
                                 alloc=df["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd7"].mean()
    sd = g.groupby("coin")["fwd7"].std()
    g["ex"] = g["fwd7"] - g["coin"].map(drift)
    g["z"] = g["ex"] / g["coin"].map(sd)
    g["r30z"] = g["r30"] / (g["vol30"] * np.sqrt(30))
    out = {}
    def tab(sub, key, q=5):
        s = sub.dropna(subset=[key, "z"]).copy()
        s["b"] = pd.qcut(s[key], q, labels=False, duplicates="drop")
        t = s.groupby("b").agg(n=("z", "size"), lo=(key, "min"), hi=(key, "max"),
                               ex_mean=("ex", "mean"), z_mean=("z", "mean"))
        t["t"] = s.groupby("b")["z"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
        return t
    out["all grid: fwd7 excess by r30 quintile"] = tab(g, "r30")
    out["in profile: by r30 quintile"] = tab(g[g.inprof], "r30", 4)
    out["out profile: by r30 quintile"] = tab(g[~g.inprof], "r30")
    out["all: by r30 scaled by vol quintile"] = tab(g, "r30z")
    out["all: by r7b quintile"] = tab(g, "r7b")
    out["all: by r1 quintile"] = tab(g, "r1")
    out["all: by range quintile"] = tab(g, "rng")
    out["all: by close position quintile"] = tab(g, "pc")
    out["all: by vol30 quintile"] = tab(g, "vol30")
    s = g.dropna(subset=["z", "r30"])
    out["corr r30 vs z, all (spearman, n)"] = pd.Series({"rho": stats.spearmanr(s.r30, s.z)[0], "p": stats.spearmanr(s.r30, s.z)[1], "n": len(s)})
    wd = g.dropna(subset=["z"]).groupby("wd")["z"].agg(["size", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["by weekday start"] = wd
    # daily book
    dd = []
    for coin, wins in days.items():
        for w, df in wins.items():
            x = df[["book_return", "coin_return"]].copy(); x["w"] = w; x["coin"] = coin
            x["yr"] = pd.to_datetime(df["day"]).dt.year
            x["wd"] = pd.to_datetime(df["day"]).dt.dayofweek
            dd.append(x)
    d = pd.concat(dd).dropna()
    by = d.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    out["book & coin daily mean by window"] = by
    tr = []
    for coin, wins in trades.items():
        for w, df in wins.items():
            if len(df):
                x = df[["side", "net_profit_loss_percent", "duration_minutes", "entry_forecast"]].copy(); x["coin"] = coin; x["w"] = w
                tr.append(x)
    if tr:
        T = pd.concat(tr)
        out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean", "median"])
        T["fb"] = pd.qcut(T["entry_forecast"], 3, labels=False, duplicates="drop")
        out["trades by entry forecast tercile"] = T.groupby("fb")["net_profit_loss_percent"].agg(["size", "mean", "median"])
    return out
