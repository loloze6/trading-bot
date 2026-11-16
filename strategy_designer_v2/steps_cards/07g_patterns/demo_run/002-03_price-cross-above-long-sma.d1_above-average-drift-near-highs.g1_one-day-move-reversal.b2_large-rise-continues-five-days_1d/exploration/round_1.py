def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            z = r1 / sd20
            r20 = c / c.shift(20) - 1
            vol_rank = sd20
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            n = len(b)
            idx = np.arange(0, n, 5)
            d = pd.DataFrame({"coin": coin, "w": w, "z": z.values[idx], "r20": r20.values[idx],
                              "sd20": sd20.values[idx], "fwd5": fwd5.values[idx],
                              "fc": b["forecast"].values[idx],
                              "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values[idx],
                              "pos": b["postRebalance_current_allocation"].values[idx]})
            rows.append(d)
    g = pd.concat(rows).dropna(subset=["fwd5", "z"])
    g["ex5"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")
    out = {}
    g["zb"] = pd.cut(g["z"], [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    def summ(x):
        return pd.Series({"n": len(x), "mean_ex5": x["ex5"].mean(),
                          "t": x["ex5"].mean() / (x["ex5"].std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "hit": (x["fwd5"] > 0).mean()})
    out["ex5 by z of 1d move"] = g.groupby("zb").apply(summ)
    g["r20b"] = g.groupby("coin")["r20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex5 by 20d return quintile (per coin)"] = g.groupby("r20b").apply(summ)
    g["volb"] = g.groupby("coin")["sd20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ex5 by vol quintile (per coin)"] = g.groupby("volb").apply(summ)
    neg = g[g["z"] < 0]
    sl = stats.linregress(neg["z"], neg["ex5"])
    out["down days: slope ex5 on z, t, n"] = f"{sl.slope:.5f}, t={sl.slope/sl.stderr:.2f}, n={len(neg)}"
    pos = g[g["z"] > 0]
    sl = stats.linregress(pos["z"], pos["ex5"])
    out["up days: slope ex5 on z, t, n"] = f"{sl.slope:.5f}, t={sl.slope/sl.stderr:.2f}, n={len(pos)}"
    out["ex5 by coin x z sign"] = g.assign(up=g["z"] > 0).groupby(["coin", "up"]).apply(summ)
    # book daily
    br = []
    for coin in days:
        for w, d in days[coin].items():
            dd = d.copy(); dd["coin"] = coin; dd["w"] = w
            br.append(dd)
    D = pd.concat(br)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["coin daily return by weekday"] = D.groupby("wd")["coin_return"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(s.count()))])
    out["book daily by weekday"] = D.groupby("wd")["book_return"].agg(["mean"])
    out["book vs coin by coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean()
    out["book by window"] = D.groupby("w")[["book_return", "coin_return"]].mean()
    return out
