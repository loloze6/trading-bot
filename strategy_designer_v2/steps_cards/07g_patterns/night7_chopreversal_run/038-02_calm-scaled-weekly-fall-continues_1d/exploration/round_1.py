def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            r7 = c / c.shift(7) - 1
            r3 = c / c.shift(3) - 1
            r20 = c / c.shift(20) - 1
            s7 = r7 / (sd30 * np.sqrt(7))
            s3 = r3 / (sd30 * np.sqrt(3))
            s20 = r20 / (sd30 * np.sqrt(20))
            s1 = r1 / sd30
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            agit = (b["regime"] == "chop").astype(int)
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "s1": s1, "s3": s3, "s7": s7,
                               "s20": s20, "f1": f1, "f3": f3, "f5": f5, "agit": agit, "wd": wd, "r1": r1,
                               "sd30": sd30})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin over all windows on 5 grid
    g5 = A[A.pos % 5 == 0].dropna(subset=["f5"]).copy()
    drift = g5.groupby("coin")["f5"].mean()
    g5["u5"] = g5["f5"] - g5["coin"].map(drift)
    def tab(df, key, val):
        g = df.groupby(key)[val]
        t = g.mean() / (g.std() / np.sqrt(g.count()))
        return pd.DataFrame({"mean": g.mean(), "n": g.count(), "t": t})
    for sig in ["s3", "s7", "s20"]:
        d = g5.dropna(subset=[sig]).copy()
        d["q"] = pd.qcut(d[sig], 5, labels=False)
        d["cell"] = d["agit"].astype(str) + "_q" + d["q"].astype(str)
        out[f"u5 by {sig} quintile x agit(1=agitated)"] = tab(d, "cell", "u5")
        sl = {}
        for a in [0, 1]:
            dd = d[d.agit == a]
            res = stats.linregress(dd[sig], dd["u5"])
            sl[f"agit{a}"] = (res.slope, res.slope / res.stderr, len(dd))
        out[f"slope u5 on {sig}: slope,t,n"] = pd.DataFrame(sl, index=["slope", "t", "n"])
    # 1-day scaled moves, next day/3 day, grid 3
    g3 = A[A.pos % 3 == 0].dropna(subset=["f3", "s1"]).copy()
    d3 = g3.groupby("coin")["f3"].mean()
    g3["u3"] = g3["f3"] - g3["coin"].map(d3)
    g3["q"] = pd.qcut(g3["s1"], 5, labels=False)
    g3["cell"] = g3["agit"].astype(str) + "_q" + g3["q"].astype(str)
    out["u3 by 1-day scaled move quintile x agit"] = tab(g3, "cell", "u3")
    # weekday daily returns
    d1 = A.dropna(subset=["f1"]).copy()
    dd1 = d1.groupby("coin")["f1"].mean()
    d1["u1"] = d1["f1"] - d1["coin"].map(dd1)
    d1["nextwd"] = (d1["wd"] + 1) % 7
    out["next-day unusual return by weekday of that day (0=Mon)"] = tab(d1, "nextwd", "u1")
    # vol level
    d = g5.dropna(subset=["sd30"]).copy()
    d["vq"] = d.groupby("coin")["sd30"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["u5 by own-coin sd30 quintile"] = tab(d, "vq", "u5")
    out["u5 by coin x agit"] = tab(g5.assign(k=g5.coin + "_" + g5.agit.astype(str)), "k", "u5")
    # book
    bd = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            bd.append(dy.assign(coin=coin, w=w))
    D = pd.concat(bd, ignore_index=True)
    bk = D.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book mean by window"] = D.groupby("w")["book_return"].agg(["mean", "std", "count"])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t.assign(coin=coin, w=w))
    T = pd.concat(tr, ignore_index=True)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["fq"] = pd.qcut(T["entry_forecast"].abs(), 4, labels=False, duplicates="drop")
    out["trades by |entry_forecast| quartile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["mean", "count", "median"])
    out["trades by duration bucket"] = T.groupby(pd.cut(T.dur_d, [0, 5, 7, 10, 20, 1000]))["net_profit_loss_percent"].agg(["mean", "count"])
    return out
