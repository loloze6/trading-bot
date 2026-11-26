import numpy as np, pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def explore(data):
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            rng = (b["high"] - b["low"]) / c
            mr30 = rng.rolling(30, min_periods=30).mean()
            r3 = c / c.shift(3) - 1
            r1 = c / c.shift(1) - 1
            vol10 = r1.rolling(10).std(); vol30 = r1.rolling(30).std()
            tr60 = c / c.shift(60) - 1
            f3 = c.shift(-3) / c - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "s3": r3 / mr30, "s1": r1 / mr30, "f3": f3,
                "rising": (b["regime"] != "chop").astype(int),
                "tr60": tr60, "vr": vol10 / vol30,
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "r1": r1,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 3 == 0].copy()
    drift = G.groupby("coin")["f3"].mean()
    G["ex"] = G["f3"] - G["coin"].map(drift)
    G = G.dropna(subset=["ex", "s3"])
    out = {}

    def bucket(df, col, q=5):
        d = df.copy()
        d["b"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        g = d.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"),
                               mean_ex=("ex", "mean"))
        g["t"] = d.groupby("b")["ex"].apply(_t)
        return g

    out["s3 quintiles, rising"] = bucket(G[G.rising == 1], "s3")
    out["s3 quintiles, not rising"] = bucket(G[G.rising == 0], "s3")
    out["s1 quintiles, rising"] = bucket(G[G.rising == 1].dropna(subset=["s1"]), "s1")
    out["s1 quintiles, not rising"] = bucket(G[G.rising == 0].dropna(subset=["s1"]), "s1")
    # trend strength within rising
    R = G[(G.rising == 1)].dropna(subset=["tr60"])
    out["tr60 quintiles, rising"] = bucket(R, "tr60")
    NR = G[(G.rising == 0)].dropna(subset=["tr60"])
    out["tr60 quintiles, not rising"] = bucket(NR, "tr60")
    # vol ratio
    out["vol10/30 quintiles, all"] = bucket(G.dropna(subset=["vr"]), "vr")
    out["vol10/30 quintiles, rising"] = bucket(G[G.rising == 1].dropna(subset=["vr"]), "vr")
    # slope of ex on s3 by regime & sign
    res = []
    for name, d in [("rising s3>0", G[(G.rising == 1) & (G.s3 > 0)]),
                    ("rising s3<0", G[(G.rising == 1) & (G.s3 < 0)]),
                    ("notrising s3>0", G[(G.rising == 0) & (G.s3 > 0)]),
                    ("notrising s3<0", G[(G.rising == 0) & (G.s3 < 0)])]:
        s = stats.linregress(d["s3"], d["ex"])
        res.append({"set": name, "n": len(d), "slope": s.slope, "t": s.slope / s.stderr, "mean_ex": d["ex"].mean()})
    out["slopes"] = pd.DataFrame(res)
    # weekday of daily coin return
    A1 = A.dropna(subset=["r1"])
    wd = A1.groupby("wd")["r1"].agg(["mean", "size"])
    wd["t"] = A1.groupby("wd")["r1"].apply(_t)
    out["weekday coin r1"] = wd
    # book daily by regime and by year
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    by = D.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    out["book vs coin by window"] = by
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T, ignore_index=True)
    T["fb"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    tg = T.groupby("fb").agg(lo=("entry_forecast", "min"), n=("net_profit_loss_percent", "size"),
                             mean_net=("net_profit_loss_percent", "mean"),
                             win=("net_profit_loss_percent", lambda x: (x > 0).mean()),
                             days=("duration_minutes", lambda x: x.mean() / 1440))
    out["trades by entry forecast"] = tg
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["size", "mean"])
    return out
