def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna().values)
        mu = np.concatenate(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            o, h, l, c, v = [b[k].astype(float) for k in ["open","high","low","close","volume"]]
            ts = pd.to_datetime(b["timestamp"])
            r = c.pct_change()
            vr = v / v.shift(1).rolling(20).mean()
            rng = (h - l).replace(0, np.nan)
            cl = (c - l) / rng  # 0 at low, 1 at high
            vol20 = r.rolling(20).std()
            r5 = c / c.shift(5) - 1
            r20 = c / c.shift(20) - 1
            df = pd.DataFrame({"coin": coin, "w": w, "r": r, "vr": vr, "cl": cl, "vol20": vol20,
                               "r5": r5, "r20": r20, "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "rng": rng / c, "pos": np.arange(len(b))})
            for k in [1, 2, 3, 5]:
                df[f"f{k}"] = c.shift(-k) / c - 1 - k * mu
            df["mu"] = mu
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["down"] = D["r"] < 0
    out = {}
    def summ(g, col="f1"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    dd = D[D.down].copy()
    dd["clq"] = pd.qcut(dd["cl"], 5, labels=False, duplicates="drop")
    dd["vrq"] = pd.qcut(dd["vr"], 3, labels=False)
    out["down: cl quintile x vr tercile t"] = dd.groupby(["vrq", "clq"]).apply(summ).unstack(0)
    uu = D[D.r > 0].copy()
    uu["clq"] = pd.qcut(uu["cl"], 5, labels=False, duplicates="drop")
    uu["vrq"] = pd.qcut(uu["vr"], 3, labels=False)
    out["up: cl quintile x vr tercile"] = uu.groupby(["vrq", "clq"]).apply(summ).unstack(0)
    D["rq"] = pd.qcut(D["r"], 10, labels=False)
    out["next day by today's return decile"] = D.groupby("rq").apply(summ)
    D["volq"] = D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["next day by vol tercile x down"] = D.groupby(["volq", "down"]).apply(summ)
    D["r5q"] = pd.qcut(D["r5"], 5, labels=False)
    out["5d grid f5 by r5 quintile"] = D[D.pos % 5 == 0].groupby("r5q").apply(lambda g: summ(g, "f5"))
    D["r20q"] = pd.qcut(D["r20"], 5, labels=False)
    out["next day by r20 quintile"] = D.groupby("r20q").apply(summ)
    out["next day by weekday"] = D.groupby("wd").apply(summ)
    top = dd[dd.fc > dd.fc.quantile(0.8)]
    out["top-fifth forecast: horizons (grid)"] = pd.DataFrame({k: summ(top[top.pos % int(k[1:]) == 0], k) for k in ["f1","f2","f3","f5"]}).T
    out["top-fifth by vol tercile"] = top.assign(volq=D.loc[top.index, "volq"]).groupby("volq").apply(summ)
    out["top-fifth by r20 quintile"] = top.assign(q=D.loc[top.index, "r20q"]).groupby("q").apply(summ)
    out["top-fifth by year"] = top.groupby("yr").apply(summ)
    out["top-fifth by coin"] = top.groupby("coin").apply(summ)
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, w=w))
    B = pd.concat(bd, ignore_index=True)
    B["bq"] = pd.qcut(B["book_return"].rank(method="first"), 20, labels=False)
    out["book ret vs coin ret, extreme vigintiles"] = B[B.bq.isin([0, 1, 18, 19])].groupby("bq")[["book_return", "coin_return"]].mean() * 100
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["dq"] = pd.cut(T["days"], [0, 1.5, 3.5, 7.5, 1e9])
    out["trades by duration"] = T.groupby("dq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
