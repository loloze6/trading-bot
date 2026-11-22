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
            r1 = c.pct_change()
            r30 = c / c.shift(30) - 1
            r5p = c / c.shift(5) - 1
            hi60 = c.rolling(60, min_periods=60).max()
            lo60 = c.rolling(60, min_periods=60).min()
            dist = c / hi60 - 1
            pos60 = (c - lo60) / (hi60 - lo60)
            vol20 = r1.rolling(20, min_periods=20).std()
            vol60 = r1.rolling(60, min_periods=60).std()
            fwd = c.shift(-H) / c - 1
            fc = b["debug_info.components.hpmom.post_pipeline_value"]
            alloc = b["postRebalance_current_allocation"]
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0, n, H):
                if i + H >= n:
                    break
                rows.append(dict(coin=coin, win=w, r30=r30[i], r5p=r5p[i], r1=r1[i], dist=dist[i], pos60=pos60[i],
                                 vratio=vol20[i] / vol60[i] if vol60[i] else np.nan, vol20=vol20[i],
                                 fwd=fwd[i], fc=fc[i], alloc=alloc[i], wd=wd[i], yr=yr[i]))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - drift
    g["exz"] = g["ex"] / g.groupby("coin")["fwd"].transform("std")

    def qtab(col, q=5):
        d = g.dropna(subset=[col, "ex"]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = d.groupby("q")["exz"].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["ex_mean"] = d.groupby("q")["ex"].mean()
        return t.round(4)

    out = {}
    for col in ["fc", "r30", "dist", "pos60", "r5p", "r1", "vol20", "vratio"]:
        out["quintile " + col] = qtab(col)
    # interaction r30 x dist
    d = g.dropna(subset=["r30", "dist", "ex"]).copy()
    d["qr"] = d.groupby("coin")["r30"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d["qd"] = d.groupby("coin")["dist"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["r30 tercile x dist tercile mean exz"] = d.pivot_table(index="qr", columns="qd", values="exz", aggfunc="mean").round(3)
    out["r30 tercile x dist tercile count"] = d.pivot_table(index="qr", columns="qd", values="exz", aggfunc="count")
    # by coin slope t of exz on fc
    res = {}
    for coin, dd in g.dropna(subset=["fc", "ex"]).groupby("coin"):
        s = stats.linregress(dd["fc"], dd["exz"])
        res[coin] = [s.slope, s.slope / s.stderr, len(dd)]
    out["per coin fc slope"] = pd.DataFrame(res, index=["slope", "t", "n"]).T.round(3)
    wdt = g.groupby("wd")["exz"].agg(["mean", "count"]).round(3)
    out["weekday of grid bar"] = wdt
    out["by year exz x sign fc"] = g.assign(s=np.sign(g["fc"]) * g["exz"]).groupby("yr")["s"].agg(["mean", "count"]).round(3)
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day", "book_return", "coin_return"]].copy(); x["coin"] = coin; x["win"] = w
            days.append(x)
    D = pd.concat(days)
    bk = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    bk["wd"] = pd.to_datetime(bk.index.get_level_values("day")).weekday
    out["book by weekday"] = bk.groupby("wd")[["book_return", "coin_return"]].mean().round(5)
    out["book by window"] = bk.groupby(level="win")[["book_return", "coin_return"]].agg(["mean"]).round(5)
    q = bk["book_return"]
    out["book top5pct days: mean coin ret"] = float(bk.loc[q >= q.quantile(0.95), "coin_return"].mean())
    out["book bottom5pct days: mean coin ret"] = float(bk.loc[q <= q.quantile(0.05), "coin_return"].mean())
    out["book share of sum from top5pct days"] = float(q[q >= q.quantile(0.95)].sum() / q.sum())
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tt = t[["side", "net_profit_loss_percent", "duration_minutes"]].copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean", "median", "count"]).round(3)
    out["trades by coin"] = T.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
