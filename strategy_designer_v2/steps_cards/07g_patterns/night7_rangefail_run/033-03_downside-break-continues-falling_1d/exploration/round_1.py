def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            hh = hi.shift(1).rolling(20).max(); ll = lo.shift(1).rolling(20).min()
            pos = (c - ll) / (hh - ll)
            below = (c - ll) / ll * 100
            above = (c - hh) / hh * 100
            vol20 = r1.rolling(20).std()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            z1 = r1 / vol20.shift(1)
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, n, H)
            for i in idx:
                if i + H >= n: continue
                rows.append(dict(coin=coin, w=w, day=ts[i].normalize(), wd=ts[i].dayofweek,
                                 fwd=fwd[i], pos=pos[i], below=below[i], above=above[i], vol20=vol20[i],
                                 r1=r1[i], z1=z1[i], r5=r5[i], r20=r20[i], r60=r60[i],
                                 alloc=b["postRebalance_current_allocation"][i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d["volpct"] = d.groupby("coin")["vol20"].rank(pct=True)
    out = {}
    def bucket(col, q=5):
        x = d.dropna(subset=[col, "ex"]).copy()
        x["b"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = x.groupby("b")["ex"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["colmean"] = x.groupby("b")[col].mean()
        return g.round(4)
    def slope(col):
        x = d.dropna(subset=[col, "ex"])
        rk = x.groupby("coin")[col].rank(pct=True) - 0.5
        r, p = stats.spearmanr(rk, x["ex"])
        # day-pooled t of rank-weighted ex
        v = (rk * x["ex"]).groupby(x["day"]).sum()
        return pd.Series({"spearman": r, "n": len(x), "t_daypooled": v.mean() / (v.std() / np.sqrt(len(v)))})
    for col in ["pos", "r1", "z1", "r5", "r20", "r60", "volpct"]:
        out["q_" + col] = bucket(col)
    out["slopes"] = pd.DataFrame({c: slope(c) for c in ["pos", "r1", "z1", "r5", "r20", "r60", "volpct", "below", "above"]}).T.round(4)
    g = d.groupby("wd")["ex"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday"] = g.round(4)
    # pos by vol regime
    x = d.dropna(subset=["pos", "volpct"]).copy()
    x["hv"] = x["volpct"] > 0.5
    x["pb"] = pd.cut(x["pos"], [-10, 0, 0.33, 0.67, 1, 10])
    out["pos_by_vol"] = x.groupby(["hv", "pb"])["ex"].agg(["mean", "count"]).round(4)
    x["tr"] = pd.cut(x["r60"], [-10, -0.1, 0.1, 10])
    out["pos_by_trend"] = x.dropna(subset=["tr"]).groupby(["tr", "pb"])["ex"].agg(["mean", "count"]).round(4)
    # by coin slope of pos
    out["pos_by_coin"] = d.dropna(subset=["pos"]).groupby("coin").apply(lambda s: pd.Series({"rho": stats.spearmanr(s["pos"], s["ex"])[0], "n": len(s)})).round(3)
    # book: daily returns, largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; dd.append(t)
    dd = pd.concat(dd)
    br = dd.groupby("day")["book_return"].mean().dropna()
    out["book_by_window"] = dd.groupby("w")["book_return"].agg(["mean", "std", "count"]).assign(sh=lambda s: s["mean"] / s["std"] * np.sqrt(365)).round(5)
    out["book_summary"] = pd.Series({"mean": br.mean(), "std": br.std(), "share_top10_days_of_sum": br.nlargest(10).sum() / br.sum(), "share_bottom10": br.nsmallest(10).sum() / br.sum()})
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    out["trades_by_coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count", "median"]).round(3)
    tr["fq"] = pd.qcut(tr["entry_forecast"].abs().rank(method="first"), 4, labels=False)
    out["trades_by_forecast_q"] = tr.groupby("fq")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
