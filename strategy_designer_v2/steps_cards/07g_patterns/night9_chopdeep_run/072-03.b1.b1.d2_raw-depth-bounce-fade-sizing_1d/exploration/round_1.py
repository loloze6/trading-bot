def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float); h = d["high"].astype(float); l = d["low"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20).std()
            hi20 = h.rolling(20).max(); lo20 = l.rolling(20).min()
            depth = (c - hi20) / hi20 / sd20
            height = (c - lo20) / lo20 / sd20
            tr60 = (c / c.shift(60) - 1) * 100
            f1 = c.shift(-1) / c - 1
            f10 = c.shift(-10) / c - 1
            f3 = c.shift(-3) / c - 1
            sd60 = r.rolling(60).std()
            z = r / sd20.shift(1)
            pos = np.arange(len(d))
            ts = pd.to_datetime(d["timestamp"])
            out = pd.DataFrame({"coin": coin, "w": w, "r": r, "z": z, "depth": depth, "height": height,
                                "tr60": tr60, "f1": f1, "f3": f3, "f10": f10, "pos": pos,
                                "wd": ts.dt.dayofweek, "yr": ts.dt.year,
                                "alloc": d["postRebalance_current_allocation"].astype(float),
                                "fc": d["forecast"].astype(float),
                                "volr": sd20 / sd60,
                                "g10": (pos % 10 == 0), "g3": (pos % 3 == 0)})
            rows.append(out)
    A = pd.concat(rows, ignore_index=True)
    A["prof"] = np.where(A.tr60 > 10, "rising", np.where(A.tr60 < -10, "falling", np.where(A.tr60.notna(), "choppy", None)))
    # drift per coin
    dr1 = A.groupby("coin").f1.mean(); dr10 = A[A.g10].groupby("coin").f10.mean(); dr3 = A[A.g3].groupby("coin").f3.mean()
    A["u1"] = A.f1 - A.coin.map(dr1); A["u10"] = A.f10 - A.coin.map(dr10); A["u3"] = A.f3 - A.coin.map(dr3)
    def summ(g, col):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean%": 100 * x.mean() if n else np.nan,
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    res = {}
    # 1 depth bins in choppy, next day, by up/down
    C = A[A.prof == "choppy"].copy()
    C["dbin"] = pd.cut(C.depth, [-100, -6, -4, -2.5, -1, 1e-9], labels=["<-6", "-6..-4", "-4..-2.5", "-2.5..-1", "-1..0"])
    C["up"] = C.r > 0
    res["choppy depth x up, next1d unusual"] = C.groupby(["up", "dbin"]).apply(lambda g: summ(g, "u1")).unstack(0) if False else C.groupby(["up", "dbin"]).apply(lambda g: summ(g, "u1"))
    res["choppy depth x up, next10d unusual (grid)"] = C[C.g10].groupby(["up", "dbin"]).apply(lambda g: summ(g, "u10"))
    # 2 all profiles depth bins 10d
    A["dbin"] = pd.cut(A.depth, [-100, -6, -4, -2.5, -1, 1e-9], labels=["<-6", "-6..-4", "-4..-2.5", "-2.5..-1", "-1..0"])
    res["profile x depth, 10d unusual grid"] = A[A.g10].groupby(["prof", "dbin"]).apply(lambda g: summ(g, "u10"))
    # 3 big moves next-day by profile
    A["zbin"] = pd.cut(A.z, [-100, -2, -1, 1, 2, 100], labels=["<-2", "-2..-1", "mid", "1..2", ">2"])
    res["z of day x profile, next1d unusual"] = A.groupby(["prof", "zbin"]).apply(lambda g: summ(g, "u1"))
    res["z of day x profile, next3d unusual grid"] = A[A.g3].groupby(["prof", "zbin"]).apply(lambda g: summ(g, "u3"))
    # 4 weekday
    res["weekday next1d unusual"] = A.groupby("wd").apply(lambda g: summ(g, "u1"))
    # 5 vol ratio
    A["vbin"] = pd.qcut(A.volr, 4, labels=["q1", "q2", "q3", "q4"])
    res["volratio x profile, 10d unusual grid"] = A[A.g10].groupby(["prof", "vbin"]).apply(lambda g: summ(g, "u10"))
    # 6 book
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; D.append(x)
    D = pd.concat(D, ignore_index=True)
    D["yr"] = pd.to_datetime(D.day).dt.year
    res["book ret by year"] = D.groupby("yr").book_return.agg(["count", "mean", "std"])
    res["book ret by coin"] = D.groupby("coin").book_return.agg(["count", "mean"])
    # 7 trades
    T = []
    for coin, wins in data["trades"].items():
        for w, tt in wins.items():
            if len(tt): x = tt.copy(); x["coin"] = coin; T.append(x)
    T = pd.concat(T, ignore_index=True)
    T["efq"] = pd.qcut(T.entry_forecast.abs().rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    res["trades by |entry fc| quartile"] = T.groupby("efq").agg(n=("net_profit_loss_percent", "size"),
        mean=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"))
    res["trade count side"] = T.side.value_counts()
    return res
