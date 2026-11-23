def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        # drift per coin: non-overlapping 3-bar returns pooled over windows
        d3 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 3, 3)
            d3 += list(c[idx + 3] / c[idx] - 1)
        drift3 = np.mean(d3) if d3 else 0.0
        d1 = []
        for w, b in wins.items():
            c = b["close"].values
            d1 += list(c[1:] / c[:-1] - 1)
        drift1 = np.mean(d1) if d1 else 0.0
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            vol = r.rolling(20, min_periods=15).std().shift(1)
            f = pd.DataFrame({
                "coin": coin, "win": w, "wd": ts.dt.weekday.values,
                "year": ts.dt.year.values,
                "r1": r.values, "z": (r / vol).values,
                "r2": (b["close"] / b["close"].shift(2) - 1).values,
                "z2": ((b["close"] / b["close"].shift(2) - 1) / (vol * np.sqrt(2))).values,
                "f1": (b["close"].shift(-1) / b["close"] - 1 - drift1).values,
                "f3": (b["close"].shift(-3) / b["close"] - 1 - drift3).values,
                "f3_4": (b["close"].shift(-7) / b["close"].shift(-4) - 1 - drift3).values,
                "vratio": (b["volume"] / b["volume"].rolling(20, min_periods=15).mean().shift(1)).values,
                "vol": vol.values,
                "volrel": (vol / vol.rolling(60, min_periods=30).mean()).values,
                "regime": b["regime"].values,
                "fc": b["forecast"].values,
            })
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    A = A.dropna(subset=["z", "f3"])

    def summ(g, col="f3"):
        x = g[col].dropna()
        n = len(x)
        if n < 3:
            return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})

    out = {}
    # 1. large falls / rises by weekday (each weekday 7 bars apart -> no overlap at 3 days)
    A["zb"] = pd.cut(A["z"], [-np.inf, -2, -1, 1, 2, np.inf], labels=["<-2", "-2..-1", "mid", "1..2", ">2"])
    t1 = A.groupby(["wd", "zb"], observed=True).apply(summ).unstack("zb")
    out["f3 by weekday x z-bucket (mean)"] = t1.xs("mean", axis=1, level=0).round(4)
    out["f3 by weekday x z-bucket (t)"] = t1.xs("t", axis=1, level=0).round(2)
    out["f3 by weekday x z-bucket (n)"] = t1.xs("n", axis=1, level=0)
    # 2. slope of f3 on z by weekday
    sl = []
    for wd, g in A.groupby("wd"):
        res = stats.linregress(g["z"].clip(-6, 6), g["f3"])
        sl.append({"wd": wd, "slope": res.slope, "t": res.slope / res.stderr, "n": len(g)})
    out["slope f3 on z by weekday"] = pd.DataFrame(sl).round(5)
    # 3. Sunday large falls: split by volume ratio and by volrel, and by later horizons
    S = A[(A.wd == 6) & (A.z <= -1.5)].copy()
    S["vq"] = pd.qcut(S["vratio"], 3, labels=["lowvol", "midvol", "highvol"])
    out["Sun falls z<=-1.5 by volume tercile"] = S.groupby("vq", observed=True).apply(summ).round(4)
    S["rq"] = pd.qcut(S["volrel"], 3, labels=["calm", "mid", "turb"])
    out["Sun falls z<=-1.5 by vol60 tercile"] = S.groupby("rq", observed=True).apply(summ).round(4)
    out["Sun falls z<=-1.5 days 4-7"] = summ(S, "f3_4").round(4)
    out["Sun falls z<=-1.5 next day"] = summ(S, "f1").round(4)
    # weekday falls (non-Sunday) by volume tercile
    W = A[(A.wd != 6) & (A.z <= -2)].copy()
    W["vq"] = pd.qcut(W["vratio"], 3, labels=["lowvol", "midvol", "highvol"])
    out["Weekday falls z<=-2 by volume tercile"] = W.groupby("vq", observed=True).apply(summ).round(4)
    W["rq"] = pd.qcut(W["volrel"], 3, labels=["calm", "mid", "turb"])
    out["Weekday falls z<=-2 by vol60 tercile"] = W.groupby("rq", observed=True).apply(summ).round(4)
    # 4. two-day weekend return (Fri close->Sun close)
    S2 = A[(A.wd == 6)].dropna(subset=["z2"]).copy()
    S2["z2b"] = pd.cut(S2["z2"], [-np.inf, -2, -1, 1, 2, np.inf])
    out["Sun: f3 by 2-day weekend z"] = S2.groupby("z2b", observed=True).apply(summ).round(4)
    # 5. by year, Sunday falls
    out["Sun falls z<=-1.5 by year"] = S.groupby("year").apply(summ).round(4)
    # 6. book daily returns
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    bk = D.dropna(subset=["book_return"])
    out["book return by weekday"] = bk.groupby("wd")["book_return"].agg(["mean", "std", "count"]).round(5)
    # 7. trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["ewd"] = pd.to_datetime(T["entry_time"]).dt.weekday
    T["eyear"] = pd.to_datetime(T["entry_time"]).dt.year
    out["trades by entry weekday"] = T.groupby("ewd")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    out["trades by year"] = T.groupby("eyear")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["trades by forecast quartile"] = T.groupby("fq", observed=True)["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"]).round(3)
    return out
