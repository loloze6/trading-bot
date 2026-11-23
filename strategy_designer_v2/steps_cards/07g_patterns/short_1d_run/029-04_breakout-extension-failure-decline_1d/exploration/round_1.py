def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            if n < 30: continue
            r1 = c.pct_change()
            fwd = c.shift(-H) / c - 1
            past5 = c / c.shift(5) - 1
            past20 = c / c.shift(20) - 1
            hh20 = c.rolling(20).max().shift(1)
            dist_hi = c / c.rolling(20).max() - 1
            vol20 = r1.rolling(20).std()
            rng = (hi - lo) / c
            exc = b.get("debug_info.components.fail_exc.last_history_value")
            brk = (c > hh20).astype(float)
            brk_recent = brk.rolling(4).max()
            fail = ((brk_recent > 0) & (c < hh20) & (brk == 0)).astype(float)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "fwd": fwd, "past1": r1, "past5": past5,
                               "past20": past20, "dist_hi": dist_hi, "vol20": vol20, "rng": rng,
                               "brk": brk, "fail": fail,
                               "exc": exc.astype(float) if exc is not None else np.nan,
                               "fc": b["forecast"].astype(float),
                               "yr": ts.dt.year, "wd": ts.dt.weekday})
            df["pos"] = np.arange(n)
            g = df[(df.pos % H == 0) & df.fwd.notna()]
            rows.append(g)
            daily.append(pd.DataFrame({"coin": coin, "r": r1.shift(-1), "past1": r1,
                                       "wd_next": ts.shift(-1).dt.weekday, "vol20": vol20}).dropna())
    G = pd.concat(rows)
    G["drift"] = G.groupby("coin").fwd.transform("mean")
    G["u"] = G.fwd - G.drift
    G["z"] = G.u / G.groupby("coin").fwd.transform("std")
    out = {}
    def tab(col, q=5, sub=None):
        d = (G if sub is None else sub).dropna(subset=[col])
        d = d.copy()
        d["q"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = d.groupby("q").agg(mean_u=("u", "mean"), mean_z=("z", "mean"), n=("u", "size"),
                               t=("u", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))),
                               feat=(col, "mean"))
        return t
    for col in ["past1", "past5", "past20", "dist_hi", "vol20", "rng"]:
        out["q_" + col] = tab(col)
    out["brk_vs_not"] = G.groupby("brk").agg(mean_u=("u", "mean"), n=("u", "size"),
                          t=("u", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    out["fail_vs_not"] = G.groupby("fail").agg(mean_u=("u", "mean"), n=("u", "size"),
                          t=("u", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    ex = G[G.exc > 0]
    if len(ex) > 30:
        ex = ex.copy(); ex["q"] = pd.qcut(ex.exc.rank(method="first"), 3, labels=False)
        out["fail_exc_terc"] = ex.groupby("q").agg(mean_u=("u", "mean"), n=("u", "size"), exc=("exc", "mean"),
                          t=("u", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    out["by_year"] = G.groupby("yr").agg(mean_u=("u", "mean"), n=("u", "size"))
    # slope past5 -> u per coin
    sl = {}
    for coin, d in G.dropna(subset=["past5"]).groupby("coin"):
        s = stats.linregress(d.past5 / d.vol20.fillna(d.vol20.mean()), d.z)
        sl[coin] = {"slope": s.slope, "t": s.slope / s.stderr, "n": len(d)}
    out["past5_slope_by_coin"] = pd.DataFrame(sl).T
    D = pd.concat(daily)
    D["u"] = D.r - D.groupby("coin").r.transform("mean")
    out["weekday_next"] = D.groupby("wd_next").agg(mean_u=("u", "mean"), n=("u", "size"),
                          t=("u", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d[["book_return", "coin_return"]].assign(coin=coin))
    B = pd.concat(bk).dropna()
    B["q"] = pd.qcut(B.book_return.rank(method="first"), 10, labels=False)
    out["book_deciles"] = B.groupby("q").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    return out
