def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            fwd = c.shift(-H) / c - 1
            d = {}
            for p in [14, 28, 56, 90]:
                hi = c.rolling(p, min_periods=p//2).max(); lo = c.rolling(p, min_periods=p//2).min()
                d["dh%d" % p] = c / hi - 1
                d["rp%d" % p] = (c - lo) / (hi - lo)
            # days since 28-day high
            hi28 = c.rolling(28, min_periods=14).max()
            at = (c >= hi28 - 1e-12)
            last = pd.Series(np.where(at, np.arange(n), np.nan)).ffill()
            d["since"] = np.arange(n) - last
            df = pd.DataFrame(dict(coin=coin, w=w, pos=np.arange(n), fwd=fwd, at=at, **d))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A.pos % H == 0) & A.ex.notna()].copy()
    out = {}
    def st(x):
        return pd.Series({"mean": x.mean(), "n": x.count(), "t": x.mean() / (x.std() / np.sqrt(x.count()))})
    for col in ["dh14", "dh28", "dh56", "dh90", "rp28", "rp90", "since"]:
        g = G.dropna(subset=[col]).copy()
        z = g.groupby("coin")[col].transform(lambda x: (x - x.mean()) / x.std())
        sl = stats.linregress(z, g["ex"])
        g["q"] = g.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        t = g.groupby("q")["ex"].apply(st).unstack()
        t["slope_t"] = sl.slope / sl.stderr
        out["ex5 by quintile " + col] = t.round(4)
    # consistency of rp28 slope by window and coin
    g = G.dropna(subset=["rp28"]).copy()
    def slt(x):
        if len(x) < 10: return np.nan
        s = stats.linregress(x["rp28"], x["ex"]); return s.slope / s.stderr
    out["rp28 slope t by window"] = g.groupby("w").apply(slt).round(2)
    out["rp28 slope t by coin"] = g.groupby("coin").apply(slt).round(2)
    g90 = G.dropna(subset=["rp90"])
    out["rp90 slope t by window"] = g90.groupby("w").apply(lambda x: np.nan if len(x)<10 else (lambda s: s.slope/s.stderr)(stats.linregress(x["rp90"], x["ex"]))).round(2)
    out["at 28d high vs not"] = G.groupby("at")["ex"].apply(st).unstack().round(4)
    out["at 28d high by window"] = G[G["at"]].groupby("w")["ex"].apply(st).unstack().round(4)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t_ in wins.items():
            tt = t_.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr)
    T["days"] = T["duration_minutes"] / 1440
    out["trades by side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "count"), mean=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"), days=("days", "mean")).round(3)
    return out
