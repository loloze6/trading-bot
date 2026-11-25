def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20).std()
            hi = c.shift(1).rolling(20).max()
            dist = (c - hi) / hi / vol
            tr60 = (c / c.shift(60) - 1) * 100
            z1 = r1 / vol.shift(1)
            r5 = c / c.shift(5) - 1
            volpct = vol.rolling(60, min_periods=30).rank(pct=True)
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(df)),
                              "dist": dist, "tr60": tr60, "z1": z1, "r5z": r5 / (vol * np.sqrt(5)),
                              "volpct": volpct, "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
                              "alloc": df["postRebalance_current_allocation"].astype(float)})
            for h in (1, 3, 5, 10):
                d[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 5, 10):
        g = A[A.pos % h == 0]
        A[f"drift{h}"] = A.coin.map(g.groupby("coin")[f"f{h}"].mean())
        A[f"x{h}"] = A[f"f{h}"] - A[f"drift{h}"]
    A["prof"] = pd.cut(A.tr60, [-1e9, -10, 10, 1e9], labels=["falling", "choppy", "rising"])
    def summ(df, col):
        s = df[col].dropna()
        n = len(s)
        return pd.Series({"n": n, "mean%": 100 * s.mean() if n else np.nan,
                          "t": s.mean() / (s.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    G3 = A[A.pos % 3 == 0].copy()
    G3["db"] = pd.cut(G3.dist, [-1e9, -8, -4, -2, -0.5, 0, 0.5, 1.5, 1e9])
    out["x3 by profile x dist bucket"] = G3.groupby(["prof", "db"], observed=True).apply(lambda d: summ(d, "x3"))
    res = {}
    for h in (1, 3, 5, 10):
        g = A[(A.pos % h == 0) & (A.prof == "rising")]
        res[f"h{h} above"] = summ(g[g.dist > 0], f"x{h}")
        res[f"h{h} below"] = summ(g[g.dist <= 0], f"x{h}")
    out["rising: above vs below by horizon"] = pd.DataFrame(res).T
    G3["zb"] = pd.cut(G3.z1, [-1e9, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 1e9])
    out["x3 by 1-day move z (all)"] = G3.groupby("zb", observed=True).apply(lambda d: summ(d, "x3"))
    out["x3 by profile x 1-day z"] = G3.groupby(["prof", "zb"], observed=True).apply(lambda d: summ(d, "x3")).unstack()["mean%"]
    G3["vb"] = pd.cut(G3.volpct, [0, .33, .66, 1.0])
    out["rising above-high x3 by vol tercile"] = G3[(G3.prof == "rising") & (G3.dist > 0)].groupby("vb", observed=True).apply(lambda d: summ(d, "x3"))
    out["x3 by profile x vol tercile"] = G3.groupby(["prof", "vb"], observed=True).apply(lambda d: summ(d, "x3"))
    G1 = A.copy()
    out["x1 by weekday"] = G1.groupby("wd").apply(lambda d: summ(d, "x1"))
    G3["r5b"] = pd.cut(G3.r5z, [-1e9, -2, -1, 0, 1, 2, 1e9])
    out["x3 by profile x 5d return z"] = G3.groupby(["prof", "r5b"], observed=True).apply(lambda d: summ(d, "x3")).unstack()["mean%"]
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in trades.items() for t in ws.values()], ignore_index=True)
    if len(T):
        T["fq"] = pd.qcut(T.entry_forecast.rank(method="first"), 4, labels=False)
        out["trades by entry forecast quartile"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"),
            meanpnl=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()),
            dur_d=("duration_minutes", lambda s: s.mean() / 1440))
        out["trades by coin"] = T.groupby("coin").net_profit_loss_percent.agg(["size", "mean"])
    return out
