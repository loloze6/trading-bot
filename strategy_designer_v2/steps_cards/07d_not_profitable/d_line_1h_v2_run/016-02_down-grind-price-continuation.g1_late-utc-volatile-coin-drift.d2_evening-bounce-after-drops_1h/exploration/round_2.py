def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"]
            r1 = cl.pct_change()
            sd = r1.rolling(168, min_periods=84).std()
            z = (cl/cl.shift(24)-1)/(sd*np.sqrt(24))
            d = pd.DataFrame({"coin": c, "win": w, "hour": ts.dt.hour, "z": z, "fc": b["forecast"],
                              "pos": b["postRebalance_current_allocation"]})
            for h in [1, 2, 4, 8, 12, 24]:
                d[f"f{h}"] = cl.shift(-h)/cl - 1
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # coin mean per bar over all windows
    mu = D.groupby("coin")["f1"].mean()
    hs = [1, 2, 4, 8, 12, 24]
    for h in hs:
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(mu)*h
    E = D[(D.hour == 20)].copy()  # bars closing 21:00
    E["grp"] = np.where(E.z >= 0, "nofall", pd.qcut(E.z.where(E.z < 0).rank(method="first"), 4, labels=False).astype("float").astype("Int64").astype(str))
    def tstat(x):
        x = x.dropna(); return x.mean()/x.std()*np.sqrt(len(x)) if len(x) > 2 else np.nan
    res = {}
    for h in hs:
        g = E.groupby("grp")[f"x{h}"]
        res[f"mean_x{h}"] = g.mean()
        res[f"t_x{h}"] = g.apply(tstat)
    res["n"] = E.groupby("grp").size()
    out["21:00 bars: excess by fall quartile (0=deepest)"] = pd.DataFrame(res)
    # same z quartile effect at other hours (fall bars, 2h ahead, every 24th not needed: use hour as grid)
    F = D[D.z < 0].copy()
    F["deep"] = F.groupby(["coin"])["z"].transform(lambda s: s <= s.quantile(0.25))
    out["deepest-quartile falls: excess 2h by hour"] = F[F.deep].groupby("hour").agg(n=("x2", "count"), x2=("x2", "mean"), x24=("x24", "mean"))
    # all bars at hour 20 regardless: unconditional hour effect
    out["all hours: unconditional excess 2h"] = D.groupby("hour")["x2"].agg(["mean", "count"])
    # days: book vs holding
    dd = []
    for c, ws in data["days"].items():
        for w, x in ws.items():
            dd.append(x.assign(coin=c, win=w))
    Dy = pd.concat(dd)
    out["daily"] = pd.Series({"book_mean": Dy.book_return.mean(), "book_sd": Dy.book_return.std(),
                              "coin_mean": Dy.coin_return.mean(), "coin_sd": Dy.coin_return.std()})
    return out
