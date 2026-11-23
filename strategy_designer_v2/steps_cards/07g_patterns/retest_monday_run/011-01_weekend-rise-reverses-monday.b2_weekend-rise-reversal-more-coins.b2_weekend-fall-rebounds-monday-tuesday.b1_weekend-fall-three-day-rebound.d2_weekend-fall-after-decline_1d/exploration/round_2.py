def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        g3 = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 3, 3):
                g3.append(c[i + 3] / c[i] - 1)
        g3 = np.array(g3); drift3, sd3 = g3.mean(), g3.std(ddof=1)
        for w, df in wins.items():
            d = df.copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            d["wd"] = ts.dt.weekday.values
            d["wk"] = (ts.dt.floor("D") - pd.to_timedelta(ts.dt.weekday, unit="D")).astype("int64") // 10**9
            c = d["close"]
            d["r1"] = c.pct_change(); d["r20"] = c / c.shift(20) - 1
            d["r7"] = c / c.shift(7) - 1
            d["f3"] = c.shift(-3) / c - 1
            d["ex3"] = d["f3"] - drift3
            d["str3"] = d["ex3"] / sd3
            d["vol20"] = np.log(c).diff().rolling(20).std()
            d["r1z"] = d["r1"] / d["vol20"].shift(1)
            d["coin"] = coin
            rows.append(d[["coin","wd","wk","r1","r7","r20","f3","ex3","str3","vol20","r1z"]])
    A = pd.concat(rows, ignore_index=True)
    A["vr"] = A.groupby("coin")["vol20"].rank(pct=True)
    def summ(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean()/(s.std(ddof=1)/np.sqrt(n)) if n > 2 else np.nan})
    def wkclust(g, col="ex3"):
        m = g.dropna(subset=[col]).groupby("wk")[col].mean()
        return summ(m)
    out = {}
    sun = A[A.wd == 6].dropna(subset=["ex3"]).copy()
    ff = sun[(sun.r1 < 0) & (sun.r20 < 0)]
    rr = sun[sun.r1 > 0]
    out["week-clustered: sun fall&fall / sun rise / sun all"] = pd.DataFrame({"fall&fall": wkclust(ff), "rise": wkclust(rr), "all": wkclust(sun)}).T
    # Sunday 1d return graded, all Sundays, quintiles of r1z (vol-scaled)
    sun["qz"] = pd.qcut(sun["r1z"], 5, labels=False)
    out["sun ex3 by vol-scaled r1 quintile (0 deepest fall)"] = sun.groupby("qz")["ex3"].apply(summ).unstack()
    # slope of str3 on r1z by weekday (all days, all signs)
    sl = {}
    for wd, g in A.dropna(subset=["str3","r1z"]).groupby("wd"):
        r = stats.linregress(g.r1z.values, g.str3.values)
        sl[wd] = {"slope": r.slope, "t": r.slope / r.stderr, "n": len(g)}
    out["slope str3 on r1z by weekday"] = pd.DataFrame(sl).T
    # Sunday rise: by vol tercile and r20 sign
    rr = rr.copy(); rr["qv"] = pd.qcut(rr["vr"], 3, labels=False)
    out["sun rise ex3 by vol tercile"] = rr.groupby("qv")["ex3"].apply(summ).unstack()
    out["sun rise ex3 by r20 sign (1=up)"] = rr.groupby(rr.r20 > 0)["ex3"].apply(summ).unstack()
    # fall&fall: vol tercile x product half
    ff = ff.copy(); ff["qv"] = pd.qcut(ff["vr"], 3, labels=False)
    ff["ph"] = ff.groupby("qv")["r1"].transform(lambda s: (s * 0 + (s.rank(pct=True) <= 0.5)).astype(int))
    out["fall&fall ex3 by vol tercile x deep-r1 half(1=deeper)"] = ff.groupby(["qv","ph"])["ex3"].apply(summ).unstack()
    out["fall&fall strength by vol tercile"] = ff.groupby("qv")["str3"].apply(summ).unstack()
    # high-vol all weekdays: does 1d fall rebound more in high vol on any day?
    A2 = A.dropna(subset=["ex3"]).copy(); A2["qv"] = pd.qcut(A2["vr"], 3, labels=False)
    hv = A2[(A2.qv == 2) & (A2.r1 < 0) & (A2.r20 < 0)]
    out["high-vol fall&fall ex3 by weekday"] = hv.groupby("wd")["ex3"].apply(summ).unstack()
    # book: largest coin-day gains/losses, weekday share
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; bd.append(x)
    D = pd.concat(bd, ignore_index=True).dropna(subset=["book_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    act = D[D.book_return.abs() > 1e-9]
    lo, hi = act.book_return.quantile(0.02), act.book_return.quantile(0.98)
    out["book worst 2% coin-days by weekday"] = act[act.book_return <= lo].groupby("wd").size()
    out["book best 2% coin-days by weekday"] = act[act.book_return >= hi].groupby("wd").size()
    out["book active coin-days by weekday"] = act.groupby("wd").size()
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin))
    T = pd.concat(T, ignore_index=True)
    T["q"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades net pnl% by entry forecast quartile"] = T.groupby("q")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades duration days"] = T["duration_minutes"].describe() / 1440
    return out
