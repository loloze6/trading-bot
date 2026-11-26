def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            r14 = c / c.shift(14) - 1
            r30 = c / c.shift(30) - 1
            r45 = c / c.shift(45) - 1
            r60 = c / c.shift(60) - 1
            vol30 = r1.rolling(30).std()
            vmed = vol30.expanding(30).median()
            fwd7 = c.shift(-7) / c - 1
            fwd3 = c.shift(-3) / c - 1
            for i in range(0, len(b), 7):
                rows.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), yr=ts.iloc[i].year,
                                 r14=r14.iloc[i], r30=r30.iloc[i], r45=r45.iloc[i], r60=r60.iloc[i],
                                 vol30=vol30.iloc[i], vmed=vmed.iloc[i], fwd7=fwd7.iloc[i], fwd3=fwd3.iloc[i],
                                 reg=b["regime"].iloc[i]))
    g = pd.DataFrame(rows).dropna(subset=["fwd7"])
    g["ex7"] = g["fwd7"] - g.groupby("coin")["fwd7"].transform("mean")
    g["ex3"] = g["fwd3"] - g.groupby("coin")["fwd3"].transform("mean")
    g["sd7"] = g.groupby("coin")["fwd7"].transform("std")
    g = g.dropna(subset=["r60", "r30"])
    g["trend"] = np.where(g.r60 > 0.1, "rising", np.where(g.r60 < -0.1, "falling", "choppy"))
    g["agit"] = np.where(g.vol30 > g.vmed, "agit", "calm")
    out = {}
    def slope(s, x, y="ex7"):
        s = s.dropna(subset=[x, y])
        if len(s) < 15: return pd.Series({"n": len(s)})
        res = stats.linregress(s[x], s[y])
        # day-clustered t of signed move: sign(x)*ex
        z = (np.sign(s[x]) * s[y]).groupby(s["day"]).sum()
        tclu = z.mean() / (z.std() / np.sqrt(len(z)))
        return pd.Series({"n": len(s), "days": len(z), "slope": res.slope, "t_slope": res.slope / res.stderr,
                          "signed_mean": (np.sign(s[x]) * s[y]).mean(), "t_signed_dayclu": tclu})
    ch = g[g.trend == "choppy"]
    out["choppy: slope by lookback (ex7)"] = pd.DataFrame({k: slope(ch, k) for k in ["r14", "r30", "r45"]}).T
    out["choppy: r30 slope ex3"] = slope(ch, "r30", "ex3").to_frame().T
    out["choppy: r30 by agitation"] = pd.DataFrame({k: slope(s, "r30") for k, s in ch.groupby("agit")}).T
    out["choppy: r30 by sign"] = pd.DataFrame({("up" if k > 0 else "down"): slope(s, "r30") for k, s in ch.groupby(np.sign(ch.r30))}).T
    out["choppy: r30 by year"] = pd.DataFrame({k: slope(s, "r30") for k, s in ch.groupby("yr")}).T
    out["choppy: r30 by coin"] = pd.DataFrame({k: slope(s, "r30") for k, s in ch.groupby("coin")}).T
    ch = ch.copy(); ch["q"] = pd.qcut(ch.r30, 4, labels=False)
    o = ch.groupby("q").agg(n=("ex7", "size"), r30=("r30", "mean"), ex7=("ex7", "mean"), sd=("ex7", "std"))
    o["t"] = o.ex7 / (o.sd / np.sqrt(o.n)); out["choppy: ex7 by r30 quartile"] = o
    out["r30 slope by trend"] = pd.DataFrame({k: slope(s, "r30") for k, s in g.groupby("trend")}).T
    # strength in choppy
    ch["str"] = np.sign(ch.r30) * ch.ex7 / ch.sd7
    out["choppy strength mean"] = float(ch["str"].mean())
    # weekday effect by year
    dl = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            x = dy.copy(); x["coin"] = coin
            x["wd"] = pd.to_datetime(x["day"]).dt.weekday; x["yr"] = pd.to_datetime(x["day"]).dt.year
            dl.append(x)
    D = pd.concat(dl).dropna(subset=["coin_return"])
    D["ex"] = D.coin_return - D.groupby("coin")["coin_return"].transform("mean")
    D["frisat"] = D.wd.isin([4, 5]).astype(int)
    o = D.groupby(["yr", "frisat"])["ex"].agg(["count", "mean", "std"]); o["t"] = o["mean"] / (o["std"] / np.sqrt(o["count"]))
    out["fri-sat excess by year"] = o
    return out
