def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "ret5p": c / c.shift(5) - 1,
                "ret20p": c / c.shift(20) - 1,
                "dist30": c / b["high"].astype(float).rolling(30, min_periods=30).max() - 1,
                "vol20": r1.rolling(20, min_periods=20).std(),
                "vr": v.rolling(5).mean() / v.rolling(30, min_periods=30).mean(),
                "regime": b["regime"].values,
                "alloc": b["postRebalance_current_allocation"].astype(float).values,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek.values,
                "fwd1": c.shift(-1) / c - 1,
                "fwd5": c.shift(-5) / c - 1,
                "fwd10": c.shift(-10) / c - 1,
            })
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 5, 10]:
        A[f"m{h}"] = A.groupby("coin")[f"fwd{h}"].transform(lambda s: s[A.loc[s.index, "pos"] % h == 0].mean())
        A[f"x{h}"] = A[f"fwd{h}"] - A[f"m{h}"]
    def quint(feat, h, sub=None):
        d = A[(A.pos % h == 0)].dropna(subset=[feat, f"x{h}"])
        if sub is not None: d = d[sub(d)]
        d = d.copy()
        d["q"] = d.groupby("coin")[feat].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        g = d.groupby("q")[f"x{h}"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        top = d[d.q == 4][f"x{h}"]; bot = d[d.q == 0][f"x{h}"]
        g.loc["top-bot", "mean"] = top.mean() - bot.mean()
        g.loc["top-bot", "t"] = stats.ttest_ind(top, bot, equal_var=False).statistic
        sp = stats.spearmanr(d[feat], d[f"x{h}"])
        g.loc["spearman", "mean"] = sp.correlation; g.loc["spearman", "count"] = len(d)
        return g.drop(columns="std").round(5)
    out["ret5p_vs_x5"] = quint("ret5p", 5)
    out["ret20p_vs_x10"] = quint("ret20p", 10)
    out["dist30_vs_x10"] = quint("dist30", 10)
    out["vol20_vs_x5"] = quint("vol20", 5)
    out["vr_vs_x5"] = quint("vr", 5)
    out["dist30_vs_x5"] = quint("dist30", 5)
    d = A[A.pos % 1 == 0].dropna(subset=["x1"])
    g = d.groupby("wd")["x1"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday_x1"] = g.drop(columns="std").round(5)
    # regime trending vs not, 10d excess
    d = A[A.pos % 10 == 0].dropna(subset=["x10"])
    g = d.groupby("regime")["x10"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["regime_x10"] = g.drop(columns="std").round(5)
    # per coin breakout share and alloc
    out["coin_breakout"] = A.groupby("coin").agg(trend_share=("regime", lambda s: (s == "trending").mean()), mean_alloc=("alloc", "mean")).round(4)
    # book: market vs timing
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.copy(); dd["coin"] = coin; dd["win"] = w; D.append(dd)
    D = pd.concat(D, ignore_index=True)
    br = D.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_daily"] = pd.Series({"mean": br.mean(), "std": br.std(), "sharpe": br.mean() / br.std() * np.sqrt(365), "n": len(br)})
    # window-level book mean
    out["book_by_window"] = D.groupby("win")["book_return"].mean().round(5)
    return out
