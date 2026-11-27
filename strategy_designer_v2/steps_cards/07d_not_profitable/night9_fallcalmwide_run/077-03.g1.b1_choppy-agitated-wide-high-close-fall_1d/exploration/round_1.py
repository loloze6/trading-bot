def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            rng = (b.high - b.low)
            cl = (b.close - b.low) / rng.replace(0, np.nan)
            r = b.close.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            width = (rng / b.close) / sd30
            nxt = b.close.shift(-1) / b.close - 1
            ret3 = b.close / b.close.shift(3) - 1
            ret1 = r
            ret20 = b.close / b.close.shift(20) - 1
            d = pd.DataFrame({"coin": coin, "w": w, "ts": b.timestamp, "regime": b.regime,
                              "cl": cl, "width": width, "nxt": nxt, "r1": ret1, "r3": ret3, "r20": ret20,
                              "alloc": b.postRebalance_current_allocation, "fc": b.forecast})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A = A[A.nxt.notna()]
    drift = A.groupby("coin").nxt.mean()
    A["un"] = A.nxt - A.coin.map(drift)
    A["inprof"] = A.regime.isin(["mean_reversion", "unknown"])
    A["day"] = pd.to_datetime(A.ts).dt.floor("D")
    def summ(s, sign=-1):
        x = sign * s
        n = len(x)
        if n < 3: return pd.Series({"n": n})
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)), "hit": (x > 0).mean()})
    out = {}
    out["regime counts"] = A.regime.value_counts()
    hi = A[(A.cl >= 0.75)]
    out["high close short: in vs out profile"] = hi.groupby("inprof").un.apply(lambda s: summ(s, -1)).unstack()
    lo = A[(A.cl <= 0.25)]
    out["low close long: in vs out profile"] = lo.groupby("inprof").un.apply(lambda s: summ(s, 1)).unstack()
    ip = A[A.inprof & (A.cl >= 0.75)].copy()
    ip["wq"] = pd.qcut(ip.width.rank(method="first"), 3, labels=["narrow", "mid", "wide"])
    out["in-prof high close by width tercile"] = ip.groupby("wq").un.apply(lambda s: summ(s, -1)).unstack()
    ip["clb"] = pd.cut(ip.cl, [0.74, 0.85, 0.95, 1.01])
    out["in-prof high close by close loc"] = ip.groupby("clb").un.apply(lambda s: summ(s, -1)).unstack()
    ip["r1s"] = pd.qcut(ip.r1.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["in-prof high close by day return tercile"] = ip.groupby("r1s").un.apply(lambda s: summ(s, -1)).unstack()
    out["in-prof high close day return tercile means"] = ip.groupby("r1s").r1.mean()
    ip["r20s"] = pd.qcut(ip.r20.rank(method="first"), 3, labels=["low", "mid", "high"])
    out["in-prof high close by 20d return tercile"] = ip.groupby("r20s").un.apply(lambda s: summ(s, -1)).unstack()
    ip["year"] = pd.to_datetime(ip.ts).dt.year
    out["in-prof high close by year"] = ip.groupby("year").un.apply(lambda s: summ(s, -1)).unstack()
    out["alloc on active bars"] = A[A.regime == "mean_reversion"].alloc.describe()
    out["width pos in-prof high close"] = ip.width.describe()
    # book drawdown
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    D = pd.concat(dd)
    bk = D.groupby(["w", "day"]).book_return.mean().dropna()
    eq = (1 + bk).cumprod()
    draw = eq / eq.cummax() - 1
    out["book: deepest fall"] = draw.min()
    out["book: total return chain"] = eq.iloc[-1] - 1
    out["book fall by window"] = draw.groupby(level=0).min()
    out["book sum by window"] = bk.groupby(level=0).sum()
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin, w=w))
    T = pd.concat(T)
    out["trades"] = T[["profit_loss_percent", "net_profit_loss_percent", "total_commission"]].describe()
    out["trade duration days"] = (T.duration_minutes / 1440).describe()
    return out
