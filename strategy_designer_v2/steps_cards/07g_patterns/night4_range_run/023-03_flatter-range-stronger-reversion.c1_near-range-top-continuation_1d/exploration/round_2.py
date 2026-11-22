def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []; rows3 = []; rows1 = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20, min_periods=20).std()
            hi = c.rolling(30, min_periods=30).max(); lo = c.rolling(30, min_periods=30).min()
            rp = (c - (hi + lo) / 2) / ((hi - lo) / 2)
            z10 = (c / c.shift(10) - 1) / (vol * np.sqrt(10))
            z30 = (c / c.shift(30) - 1) / (vol * np.sqrt(30))
            z3 = (c / c.shift(3) - 1) / (vol * np.sqrt(3))
            z1 = r1 / vol
            f10 = c.shift(-10) / c - 1; f3 = c.shift(-3) / c - 1; f1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(d["timestamp"])
            n = len(d)
            for i in range(0, n, 10):
                rows.append(dict(coin=coin, w=w, z10=z10.iloc[i], z30=z30.iloc[i], rp=rp.iloc[i], vol=vol.iloc[i], f=f10.iloc[i], year=ts.iloc[i].year))
            for i in range(0, n, 3):
                rows3.append(dict(coin=coin, z3=z3.iloc[i], f=f3.iloc[i], year=ts.iloc[i].year))
            for i in range(0, n):
                rows1.append(dict(coin=coin, z1=z1.iloc[i], f=f1.iloc[i], wd=ts.iloc[i].weekday(), year=ts.iloc[i].year))
    out = {}
    def prep(rs, col):
        g = pd.DataFrame(rs).dropna(subset=[col, "f"]).copy()
        g["ex"] = g["f"] - g.groupby("coin")["f"].transform("mean")
        g["sd"] = g.groupby("coin")["f"].transform("std")
        g["exs"] = g["ex"] / g["sd"]
        return g
    def reg(g, x):
        if len(g) < 20: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["exs"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))
    g10 = prep(rows, "z10")
    out["10d: exs on z10 pooled"] = reg(g10, "z10").to_frame().T
    out["10d: exs on z10 by year"] = g10.groupby("year").apply(lambda x: reg(x, "z10"))
    out["10d: exs on z10 by coin"] = g10.groupby("coin").apply(lambda x: reg(x, "z10"))
    g10["volq"] = pd.qcut(g10.groupby("coin")["vol"].rank(pct=True), 3, labels=["lo", "mid", "hi"])
    out["10d: exs on z10 by vol tercile"] = g10.groupby("volq").apply(lambda x: reg(x, "z10"))
    gj = g10.dropna(subset=["rp", "z30"])
    X = np.column_stack([np.ones(len(gj)), gj["z10"], gj["rp"], gj["z30"]])
    b, *_ = np.linalg.lstsq(X, gj["exs"].values, rcond=None)
    res = gj["exs"].values - X @ b
    s2 = res @ res / (len(gj) - 4); se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["10d joint: exs on z10, rp, z30"] = pd.DataFrame(dict(coef=b, t=b / se), index=["const", "z10", "rp", "z30"])
    g3 = prep(rows3, "z3")
    out["3d: exs on z3 pooled"] = reg(g3, "z3").to_frame().T
    out["3d: exs on z3 by year"] = g3.groupby("year").apply(lambda x: reg(x, "z3"))
    g1 = prep(rows1, "z1")
    out["1d: exs on z1 pooled"] = reg(g1, "z1").to_frame().T
    w = pd.DataFrame(rows1).dropna(subset=["f"])
    w["ex"] = w["f"] - w.groupby("coin")["f"].transform("mean")
    out["next-day ex return by weekday of signal bar"] = w.groupby("wd")["ex"].agg(n="count", mean="mean", t=lambda a: a.mean() / (a.std() / np.sqrt(len(a))))
    # book: largest days
    dl = []
    for coin, ws in days.items():
        for wn, df in ws.items():
            dd = df[["day", "book_return", "coin_return"]].copy(); dd["w"] = wn; dl.append(dd)
    D = pd.concat(dl).dropna()
    B = D.groupby(["w", "day"]).mean(numeric_only=True).reset_index()
    q = B["book_return"].quantile([0.05, 0.95])
    B["grp"] = np.where(B["book_return"] <= q.iloc[0], "worst5%", np.where(B["book_return"] >= q.iloc[1], "best5%", "rest"))
    out["book extremes"] = B.groupby("grp").agg(n=("book_return", "count"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["book total contribution of extremes"] = B.groupby("grp")["book_return"].sum().to_frame()
    # trades
    T = []
    for coin, ws in data["trades"].items():
        for wn, df in ws.items():
            if len(df): T.append(df.assign(coin=coin))
    T = pd.concat(T)
    T["days"] = T["duration_minutes"] / 1440
    out["trades by side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "count"), net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean"), dur=("days", "median"))
    T["efq"] = pd.qcut(T["entry_forecast"].abs(), 3, labels=["weak", "mid", "strong"], duplicates="drop")
    out["trades by |entry forecast| tercile"] = T.groupby(["side", "efq"]).agg(n=("net_profit_loss_percent", "count"), gross=("profit_loss_percent", "mean"))
    return out
