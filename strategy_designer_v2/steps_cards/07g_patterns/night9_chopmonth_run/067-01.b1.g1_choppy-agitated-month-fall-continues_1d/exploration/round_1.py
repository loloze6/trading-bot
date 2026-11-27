def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            r30 = c / c.shift(30) - 1
            r60 = c / c.shift(60) - 1
            r7p = c / c.shift(7) - 1
            vol30 = r1.rolling(30).std()
            fwd7 = c.shift(-7) / c - 1
            fwd1 = c.shift(-1) / c - 1
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0, len(b), 7):
                rows.append(dict(coin=coin, w=w, reg=b["regime"].iloc[i], r1=r1.iloc[i], r7p=r7p.iloc[i],
                                 r30=r30.iloc[i], r60=r60.iloc[i], vol30=vol30.iloc[i], fwd7=fwd7.iloc[i],
                                 fwd1=fwd1.iloc[i], wd=wd.iloc[i], yr=yr.iloc[i], alloc=b["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows).dropna(subset=["fwd7"])
    drift = g.groupby("coin")["fwd7"].transform("mean")
    g["ex7"] = g["fwd7"] - drift
    def summ(df, key):
        o = df.groupby(key)["ex7"].agg(["count", "mean", "std"])
        o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
        return o
    out = {}
    out["regime counts/ex7"] = summ(g, "reg")
    d = g.dropna(subset=["r30"]).copy()
    d["q30"] = pd.qcut(d["r30"], 5, labels=False)
    out["ex7 by r30 quintile, all"] = summ(d, "q30")
    out["ex7 by r30 quintile, unknown (chop-agit)"] = summ(d[d.reg == "unknown"], "q30")
    dd = d.dropna(subset=["r60"]).copy()
    dd["trend"] = np.where(dd.r60 > 0.1, "rising", np.where(dd.r60 < -0.1, "falling", "choppy"))
    dd["vq"] = dd.groupby("coin")["vol30"].transform(lambda s: (s > s.median()).astype(int))
    dd["prof"] = dd["trend"] + "_" + dd["vq"].astype(str)
    out["ex7 by approx profile"] = summ(dd, "prof")
    dd["sgn30"] = np.sign(dd.r30)
    out["ex7 by profile x sign r30"] = summ(dd, ["prof", "sgn30"])
    # slope ex7 on r30 by trend
    sl = {}
    for k, s in dd.groupby("prof"):
        if len(s) > 20:
            res = stats.linregress(s.r30, s.ex7)
            sl[k] = pd.Series({"n": len(s), "slope": res.slope, "t": res.slope / res.stderr})
    out["slope ex7~r30 by profile"] = pd.DataFrame(sl).T
    e = g.dropna(subset=["r7p"]).copy()
    e["q7"] = pd.qcut(e["r7p"], 5, labels=False)
    out["ex7 by past-7d quintile"] = summ(e, "q7")
    f = g.dropna(subset=["vol30"]).copy()
    f["vz"] = f.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["ex7 by vol tercile"] = summ(f, "vz")
    out["ex7 by year"] = summ(g, "yr")
    # book days
    dl = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            x = dy.copy(); x["coin"] = coin; x["w"] = w
            x["wd"] = pd.to_datetime(x["day"]).dt.weekday
            dl.append(x)
    D = pd.concat(dl).dropna(subset=["coin_return"])
    o = D.groupby("wd")["coin_return"].agg(["count", "mean", "std"])
    o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
    out["coin daily return by weekday"] = o
    D["big"] = pd.qcut(D.groupby(["coin","w"])["coin_return"].shift(0), 10, labels=False)
    D["next"] = D.groupby(["coin","w"])["coin_return"].shift(-1)
    o = D.groupby("big")["next"].agg(["count", "mean", "std"])
    o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
    out["next-day return by today decile"] = o
    return out
