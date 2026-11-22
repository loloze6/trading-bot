def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            n = len(b)
            if n < 40: continue
            ret1 = c.pct_change()
            hh20 = h.shift(1).rolling(20).max()
            brk = (c > hh20)
            # failed breakout (back inside range): a breakout in t-3..t-1, close now below that breakout's hh20
            fail_inside = np.zeros(n); fail_low = np.zeros(n)
            for t in range(n):
                for k in (1, 2, 3):
                    s = t - k
                    if s >= 0 and brk.iloc[s]:
                        if c.iloc[t] < hh20.iloc[s]:
                            fail_inside[t] = hh20.iloc[s] / c.iloc[t] - 1
                        if c.iloc[t] < l.iloc[s]:
                            fail_low[t] = l.iloc[s] / c.iloc[t] - 1
                        break
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n),
                "r1": ret1, "r5p": c / c.shift(5) - 1, "r20p": c / c.shift(20) - 1,
                "vol20": ret1.rolling(20).std(),
                "dist_hi": c / h.rolling(20).max() - 1,
                "brk": brk.astype(int), "fail_inside": fail_inside, "fail_low": fail_low,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "fwd5": c.shift(-5) / c - 1, "fwd1": c.shift(-1) / c - 1,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    g = A[(A["pos"] % 5 == 0)].dropna(subset=["fwd5"]).copy()
    st = g.groupby("coin")["fwd5"].agg(["mean", "std"])
    g["un"] = g["fwd5"] - g["coin"].map(st["mean"])
    g["str"] = g["un"] / g["coin"].map(st["std"])
    def summ(gr):
        x = gr["un"]; s = gr["str"]
        return pd.Series({"n": len(x), "mean_un": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "strength": s.mean()})
    out = {}
    # volatility-normalised past returns: within-coin quintiles
    for f in ["r1", "r5p", "r20p", "vol20", "dist_hi"]:
        gg = g.dropna(subset=[f]).copy()
        gg["q"] = gg.groupby("coin")[f].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
        out["by_" + f + "_quintile"] = gg.groupby("q").apply(summ)
    out["breakout_today"] = g.groupby("brk").apply(summ)
    g["fi"] = (g["fail_inside"] > 0).astype(int) + (g["fail_low"] > 0).astype(int)
    out["fail_state_0none_1inside_2belowlow"] = g.groupby("fi").apply(summ)
    out["weekday"] = g.groupby("wd").apply(summ)
    # r5p x vol regime
    gg = g.dropna(subset=["r5p", "vol20"]).copy()
    gg["vq"] = gg.groupby("coin")["vol20"].transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=False))
    gg["rq"] = gg.groupby("coin")["r5p"].transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=False))
    out["vol3_x_r5p3"] = gg.groupby(["vq", "rq"]).apply(summ)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("yr").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    return out
