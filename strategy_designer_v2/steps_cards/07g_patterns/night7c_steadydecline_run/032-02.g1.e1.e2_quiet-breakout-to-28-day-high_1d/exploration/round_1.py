def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            n = len(b)
            fwd = c.shift(-H) / c - 1
            hi28 = c.rolling(28, min_periods=10).max()
            dh = c / hi28 - 1
            lo28 = c.rolling(28, min_periods=10).min()
            dl = c / lo28 - 1
            ret28 = c / c.shift(28) - 1
            ret5 = c / c.shift(5) - 1
            ret1 = r
            s20 = r.rolling(20).std(); s60 = r.rolling(60).std()
            vr = s20 / s60
            rng = (b["high"] - b["low"]) / c
            rngr = rng.rolling(5).mean() / rng.rolling(60).mean()
            volr = b["volume"].rolling(5).mean() / b["volume"].rolling(60).mean()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame(dict(coin=coin, w=w, pos=np.arange(n), fwd=fwd, dh=dh, dl=dl,
                ret28=ret28, ret5=ret5, ret1=ret1, vr=vr, s20=s20, rngr=rngr, volr=volr,
                wd=ts.dt.weekday, yr=ts.dt.year, reg=b["regime"], fc=b["forecast"],
                alloc=b["postRebalance_current_allocation"]))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A.pos % H == 0) & A.ex.notna()].copy()
    out = {}
    def by(col, q=5):
        g = G.dropna(subset=[col]).copy()
        g["b"] = g.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = g.groupby("b")["ex"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        sl = stats.linregress(g.groupby("coin")[col].transform(lambda x: (x - x.mean()) / x.std()), g["ex"])
        t["slope_t_all"] = sl.slope / sl.stderr
        return t.round(4)
    for col in ["dh", "dl", "ret28", "ret5", "ret1", "vr", "s20", "rngr", "volr"]:
        out["ex5 by quintile of " + col] = by(col)
    wd = G.groupby("wd")["ex"].agg(["mean", "count", "std"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["ex5 by weekday"] = wd.round(4)
    # calm decline per brief: ret28 bottom third and range ratio low
    g = G.dropna(subset=["ret28", "rngr"]).copy()
    g["fall"] = g.groupby("coin")["ret28"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    g["calm"] = g.groupby("coin")["rngr"].transform(lambda x: pd.qcut(x.rank(method="first"), 2, labels=False))
    t = g.groupby(["fall", "calm"])["ex"].agg(["mean", "count", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["ex5 by ret28 tercile x range-ratio half"] = t.round(4)
    # ret28 quintile by window consistency for extreme
    g2 = G.dropna(subset=["ret28"]).copy()
    g2["q"] = g2.groupby("coin")["ret28"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["ret28 top-minus-bottom quintile by window"] = (g2[g2.q == 4].groupby("w")["ex"].mean() - g2[g2.q == 0].groupby("w")["ex"].mean()).round(4)
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w; D.append(dd)
    D = pd.concat(D)
    out["book daily mean/std by coin"] = D.groupby("coin")["book_return"].agg(["mean", "std", "count"]).round(5)
    tr = []
    for coin, wins in data["trades"].items():
        for w, t_ in wins.items():
            tt = t_.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr)
    T["efq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades net pnl by entry forecast quartile"] = T.groupby(["side", "efq"])["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
