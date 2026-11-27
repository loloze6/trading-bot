def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    def tstat(x):
        x = pd.Series(x).dropna()
        if len(x) < 3 or x.std() == 0: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].reset_index(drop=True).astype(float)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r = c.pct_change()
            r30 = c / c.shift(30) - 1
            r60 = c / c.shift(60) - 1
            r5 = c / c.shift(5) - 1
            r1 = r
            vr = r.rolling(10).std() / r.rolling(30).std()
            sd30 = r.rolling(30).std()
            rng = (df["high"].values - df["low"].values) / c.values
            for h in (3, 5, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(c) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, fwd=fwd[i], r30=r30[i], r60=r60[i],
                                     r5=r5[i], r1=r1[i], vr=vr[i], sd30=sd30[i], rng=rng[i],
                                     wd=ts[i].weekday(), yr=ts[i].year,
                                     fc=df["forecast"].iloc[i]))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby(["coin", "h"])["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    g["prof"] = np.where(g.r60 > 0.1, "rising", np.where(g.r60 < -0.1, "falling", "choppy"))
    g["z30"] = g.r30 / (g.sd30 * np.sqrt(30))
    g["z5"] = g.r5 / (g.sd30 * np.sqrt(5))
    g["z1"] = g.r1 / g.sd30
    def tab(sub, by):
        t = sub.dropna(subset=[by, "ex"]).groupby(by)["ex"].agg(["count", "mean", tstat])
        return t
    res = []
    for h in (5, 10):
        for prof in ("choppy", "rising", "falling"):
            s = g[(g.h == h) & (g.prof == prof)].dropna(subset=["z30", "ex"])
            if len(s) < 30: continue
            rho, p = stats.spearmanr(s.z30, s.ex)
            s = s.copy(); s["q"] = pd.qcut(s.z30, 5, labels=False)
            m = s.groupby("q")["ex"].mean()
            res.append(dict(h=h, prof=prof, n=len(s), rho_z30=rho, p=p, q0=m[0], q1=m[1], q2=m[2], q3=m[3], q4=m[4]))
    out["z30 vs excess fwd by profile"] = pd.DataFrame(res)
    res = []
    for h in (3, 5, 10):
        for var in ("z1", "z5", "vr", "rng"):
            for prof in ("choppy", "rising", "falling", "all"):
                s = g[g.h == h] if prof == "all" else g[(g.h == h) & (g.prof == prof)]
                s = s.dropna(subset=[var, "ex"])
                if len(s) < 30: continue
                rho, p = stats.spearmanr(s[var], s.ex)
                res.append(dict(h=h, var=var, prof=prof, n=len(s), rho=rho, p=p))
    out["other predictors spearman"] = pd.DataFrame(res).sort_values("p").head(25)
    # choppy z30 by vr half, h=10
    s = g[(g.h == 10) & (g.prof == "choppy")].dropna(subset=["z30", "vr", "ex"]).copy()
    s["vrhi"] = s.vr > 1; s["side"] = np.where(s.z30 > 0, "up", "down")
    out["choppy h10 side x vr"] = s.groupby(["side", "vrhi"])["ex"].agg(["count", "mean", tstat])
    # weekday daily
    dd = []
    for coin, ws in days.items():
        for w, df in ws.items():
            d = df.copy(); d["coin"] = coin
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            d["yr"] = pd.to_datetime(d["day"]).dt.year
            d["next"] = d["coin_return"].shift(-1)
            d["sd30"] = d["coin_return"].rolling(30).std()
            d["z"] = d["coin_return"] / d["sd30"]
            dd.append(d)
    D = pd.concat(dd)
    D["cex"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    out["weekday coin excess"] = D.groupby("wd")["cex"].agg(["count", "mean", tstat])
    D["zq"] = pd.qcut(D.z, 7, labels=False, duplicates="drop")
    out["next day after z bucket"] = D.dropna(subset=["next"]).groupby("zq")["next"].agg(["count", "mean", tstat])
    # book by year, and book's best/worst days context
    bk = D.dropna(subset=["book_return"])
    bd = bk.groupby(["w", "day"] if "w" in bk else ["day"])["book_return"].mean() if False else None
    out["book by year"] = bk.groupby("yr")["book_return"].agg(["count", "mean", tstat])
    out["forecast cases by year h10"] = g[(g.h == 10) & (g.fc < 0)].groupby("yr")["ex"].agg(["count", "mean", tstat])
    return out
