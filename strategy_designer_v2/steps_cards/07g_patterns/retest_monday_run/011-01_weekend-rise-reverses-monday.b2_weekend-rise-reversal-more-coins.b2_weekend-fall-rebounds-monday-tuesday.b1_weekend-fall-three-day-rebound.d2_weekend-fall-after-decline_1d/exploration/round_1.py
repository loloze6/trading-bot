def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # coin drift / usual move on non-overlapping 3-bar grid pooled over windows
        g3 = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 3, 3):
                g3.append(c[i + 3] / c[i] - 1)
        g3 = np.array(g3)
        drift3, sd3 = g3.mean(), g3.std(ddof=1)
        for w, df in wins.items():
            d = df.copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            d["wd"] = ts.dt.weekday.values
            d["year"] = ts.dt.year.values
            c = d["close"]
            d["r1"] = c.pct_change()
            d["r2"] = c / c.shift(2) - 1
            d["r20"] = c / c.shift(20) - 1
            d["f1"] = c.shift(-1) / c - 1
            d["f2"] = c.shift(-2) / c - 1
            d["f3"] = c.shift(-3) / c - 1
            d["f5"] = c.shift(-5) / c - 1
            d["ex3"] = d["f3"] - drift3
            d["str3"] = d["ex3"] / sd3
            lr = np.log(c).diff()
            d["vol20"] = lr.rolling(20).std()
            d["volrel"] = d["volume"] / d["volume"].shift(1).rolling(28).mean()
            d["wkendvol"] = (d["volume"] + d["volume"].shift(1)) / 2 / d["volume"].shift(2).rolling(28).mean()
            d["fc"] = d["forecast"]
            d["coin"] = coin
            d["win"] = w
            d["drift3"] = drift3
            rows.append(d[["coin","win","wd","year","r1","r2","r20","f1","f2","f3","f5","ex3","str3","vol20","volrel","wkendvol","fc","drift3"]])
    A = pd.concat(rows, ignore_index=True)
    A["vol20rank"] = A.groupby("coin")["vol20"].rank(pct=True)

    def summ(s):
        s = s.dropna()
        n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean() / (s.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    # A: by weekday, 1d fall & 20d fall
    ff = A[(A.r1 < 0) & (A.r20 < 0)]
    out["fall&20dfall ex3 by weekday"] = ff.groupby("wd")["ex3"].apply(summ).unstack()
    out["1d fall, 20d rise ex3 by weekday"] = A[(A.r1 < 0) & (A.r20 > 0)].groupby("wd")["ex3"].apply(summ).unstack()
    out["1d rise ex3 by weekday"] = A[(A.r1 > 0)].groupby("wd")["ex3"].apply(summ).unstack()
    # slope of ex3 on product, by weekday
    sl = {}
    for wd, g in ff.dropna(subset=["ex3"]).groupby("wd"):
        x = (g.r1 * g.r20).values
        r = stats.linregress(x, g.ex3.values)
        sl[wd] = {"slope": r.slope, "t": r.slope / r.stderr, "n": len(g)}
    out["slope ex3 on r1*r20 by weekday"] = pd.DataFrame(sl).T
    # Sunday fall&fall: horizons
    sun = ff[ff.wd == 6].copy()
    hz = {}
    for h in ["f1", "f2", "f3", "f5"]:
        hz[h] = summ(sun[h] - 0)
    out["sunday fall&fall raw fwd returns by horizon"] = pd.DataFrame(hz).T
    # Sunday quintiles of product
    sun["prod"] = sun.r1 * sun.r20
    sun["q"] = pd.qcut(sun["prod"], 5, labels=False)
    out["sunday ex3 by product quintile (0 small)"] = sun.groupby("q")["ex3"].apply(summ).unstack()
    sun["q20"] = pd.qcut(sun["r20"], 5, labels=False)
    out["sunday ex3 by r20 quintile (0 deepest)"] = sun.groupby("q20")["ex3"].apply(summ).unstack()
    sun["q1"] = pd.qcut(sun["r1"], 5, labels=False)
    out["sunday ex3 by r1 quintile (0 deepest)"] = sun.groupby("q1")["ex3"].apply(summ).unstack()
    sun["qv"] = pd.qcut(sun["wkendvol"], 3, labels=False)
    out["sunday ex3 by weekend volume tercile (0 thin)"] = sun.groupby("qv")["ex3"].apply(summ).unstack()
    sun["qvol"] = pd.qcut(sun["vol20rank"], 3, labels=False)
    out["sunday ex3 by vol20 tercile"] = sun.groupby("qvol")["ex3"].apply(summ).unstack()
    out["sunday ex3 by year"] = sun.groupby("year")["ex3"].apply(summ).unstack()
    # 2-day weekend fall (Sat+Sun) on Sunday vs 2-day fall other days
    ff2 = A[(A.r2 < 0) & (A.r20 < 0)]
    out["2d fall&20d fall ex3 by weekday"] = ff2.groupby("wd")["ex3"].apply(summ).unstack()
    # book daily
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy()
            x["coin"] = coin; x["win"] = w
            bd.append(x)
    D = pd.concat(bd, ignore_index=True)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book ret by year (coin-day mean)"] = D.groupby("year")["book_return"].agg(["mean", "std", "count"])
    out["book ret by weekday"] = D.groupby("wd")["book_return"].agg(["mean", "std"])
    out["coin ret by weekday (all)"] = D.groupby("wd")["coin_return"].apply(summ).unstack()
    return out
