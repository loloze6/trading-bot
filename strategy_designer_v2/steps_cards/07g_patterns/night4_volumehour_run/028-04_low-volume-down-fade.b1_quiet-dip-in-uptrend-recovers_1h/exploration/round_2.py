def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = []
    G = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            c = b["close"]
            ts = pd.to_datetime(b["timestamp"])
            b["r1"] = c.pct_change()
            b["hour"] = ts.dt.hour
            b["wd"] = ts.dt.weekday
            b["year"] = ts.dt.year
            b["coin"] = coin
            b["w"] = w
            b["r168"] = c / c.shift(168) - 1
            b["f6"] = c.shift(-6) / c - 1
            b["f24"] = c.shift(-24) / c - 1
            b["pos"] = np.arange(len(b))
            b["day"] = ts.dt.floor("D")
            H.append(b)
    A = pd.concat(H)
    # one return per day: close of bar starting 20 -> close of bar starting 22 (the 21:00-23:00 move)
    A["key"] = A["coin"] + A["w"]
    A = A.sort_values(["key", "timestamp"])
    A["r2fwd"] = A.groupby("key")["close"].shift(-2) / A["close"] - 1
    E = A[A["hour"] == 20].dropna(subset=["r2fwd"])
    allm = A[(A["pos"] % 2 == 0)].dropna(subset=["r2fwd"]).groupby("coin")["r2fwd"].mean()
    E = E.assign(u=E["r2fwd"] - E["coin"].map(allm))
    def summ(df, by, col):
        r = df.groupby(by, observed=True)[col].agg(["mean", "std", "count"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["mean"] = r["mean"] * 100
        return r.drop(columns="std").round(3)
    out["21-23h UTC move minus 2h drift % by coin"] = summ(E, ["coin"], "u")
    out["21-23h move by year"] = summ(E, ["year"], "u")
    out["21-23h move by weekday"] = summ(E, ["wd"], "u")
    # grade: does it scale with the day's move so far (0h->20h close)?
    A["c_open_day"] = A.groupby(["key", "day"])["close"].transform("first")
    E2 = A[A["hour"] == 20].dropna(subset=["r2fwd"]).copy()
    E2["dayret"] = E2["close"] / E2["c_open_day"] - 1
    E2["u"] = E2["r2fwd"] - E2["coin"].map(allm)
    E2["db"] = pd.qcut(E2["dayret"], 5)
    out["21-23h move by day-so-far quintile"] = summ(E2, ["db"], "u")
    # early-hour weakness 0-3 UTC by year
    A["f1"] = A.groupby("key")["close"].shift(-1) / A["close"] - 1
    m1 = A.groupby("coin")["f1"].mean()
    A["u1"] = A["f1"] - A["coin"].map(m1)
    early = A[A["hour"].isin([0, 1, 2])].dropna(subset=["u1"])
    out["hours 0-2 u1 by year"] = summ(early, ["year"], "u1")
    late = A[A["hour"].isin([20, 21])].dropna(subset=["u1"])
    out["hours 20-21 u1 by coin x hour"] = summ(late, ["coin", "hour"], "u1")
    # 7d momentum, 24h horizon, grid 24
    g = A[A["pos"] % 24 == 0].dropna(subset=["f24", "r168"]).copy()
    d24 = g.groupby("coin")["f24"].mean()
    g["u24"] = g["f24"] - g["coin"].map(d24)
    g["tb"] = pd.qcut(g["r168"], 5)
    out["u24 % by 7d return quintile"] = summ(g, ["tb"], "u24")
    out["corr r168 vs u24 by coin"] = g.groupby("coin").apply(lambda x: pd.Series({"r": x["r168"].corr(x["u24"]), "n": len(x)})).round(3)
    out["u24 top quintile r168 by year"] = summ(g[g["r168"] > g["r168"].quantile(0.8)], ["year"], "u24")
    return out
