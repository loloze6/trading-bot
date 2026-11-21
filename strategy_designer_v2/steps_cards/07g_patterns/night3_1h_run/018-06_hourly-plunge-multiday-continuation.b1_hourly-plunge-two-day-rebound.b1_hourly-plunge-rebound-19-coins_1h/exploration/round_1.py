def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [24, 48, 96, 168]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            mad = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            m = r24 / mad
            r720 = c / c.shift(720) - 1
            r168p = c / c.shift(168) - 1
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                fwd = (c.shift(-h) / c - 1).values[idx]
                rows.append(pd.DataFrame({
                    "coin": coin, "win": w, "h": h, "m": m.values[idx],
                    "mad": mad.values[idx], "r720": r720.values[idx], "r168p": r168p.values[idx],
                    "hour": ts.dt.hour.values[idx], "wd": ts.dt.weekday.values[idx],
                    "year": ts.dt.year.values[idx], "fwd": fwd}))
    A = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    g = A.groupby(["coin", "h"])["fwd"]
    A["drift"] = g.transform("mean"); A["usual"] = g.transform("std")
    A["unus"] = A["fwd"] - A["drift"]; A["str"] = A["unus"] / A["usual"]
    A = A.dropna(subset=["m"])
    # vol level tercile per coin
    A["volq"] = A.groupby(["coin", "h"])["mad"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    bins = [-np.inf, -4, -3, -2, -1, 0, 1, 2, 3, 4, np.inf]
    A["mb"] = pd.cut(A["m"], bins)
    def summ(x, col="unus"):
        v = x[col]; return pd.Series({"n": len(v), "mean_pct": 100 * v.mean(),
                                       "t": v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan,
                                       "strength": x["str"].mean()})
    out = {}
    t1 = A.groupby(["h", "mb"], observed=True).apply(summ).reset_index()
    out["unusual by 24h multiple bucket x horizon"] = t1
    D = A[(A.h == 48)]
    dr = D[D.m <= -2]; up = D[D.m >= 2]
    out["drops<=-2, 48h, by vol tercile"] = dr.groupby("volq").apply(summ)
    out["rises>=2, 48h, by vol tercile"] = up.groupby("volq").apply(summ)
    dr = dr.assign(tr=np.sign(dr.r720)); up = up.assign(tr=np.sign(up.r720))
    out["drops<=-2, 48h, by sign of 30d return"] = dr.groupby("tr").apply(summ)
    out["rises>=2, 48h, by sign of 30d return"] = up.groupby("tr").apply(summ)
    out["drops<=-2, 48h, by 4h block of hour"] = dr.groupby(dr.hour // 4).apply(summ)
    out["drops<=-2, 48h, by year"] = dr.groupby("year").apply(summ)
    out["rises>=2, 48h, by year"] = up.groupby("year").apply(summ)
    # all bars 48h by vol tercile, and by 7d past return quintile
    out["all 48h by vol tercile"] = D.groupby("volq").apply(summ)
    D2 = D.dropna(subset=["r168p"]).copy()
    D2["z7"] = D2.groupby("coin")["r168p"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["all 48h by past 7d return quintile (per coin)"] = D2.groupby("z7").apply(summ)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    Dy = pd.concat(dd).dropna(subset=["book_return", "coin_return"])
    out["book vs coin daily, mean & sd"] = pd.DataFrame({"mean": [Dy.book_return.mean(), Dy.coin_return.mean()],
                                                        "sd": [Dy.book_return.std(), Dy.coin_return.std()]}, index=["book", "coin"])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    T = pd.concat(tr)
    T["eh"] = pd.to_datetime(T.entry_time).dt.hour // 4
    T["fb"] = pd.cut(T.entry_forecast, [0, 2, 5, 10, 19.99, 20.01])
    out["trades by entry forecast"] = T.groupby("fb", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by duration days"] = T.groupby(pd.cut(T.duration_minutes / 1440, [0, 2.01, 3, 5, 10, 1000]), observed=True)["net_profit_loss_percent"].agg(["count", "mean"])
    return out
