def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l).rolling(30).mean().shift(1)
            mv = (c - c.shift(1)) / rng
            vol30 = c.pct_change().rolling(30).std().shift(1)
            z = c.pct_change() / vol30
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "mv": mv, "z": z,
                "r0": c.pct_change(),
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c.shift(-1) - 1,
                "r3_5": c.shift(-5) / c.shift(-2) - 1,
                "tr60": c / c.shift(60) - 1,
                "inprof": (b["regime"] == "unknown"),
                "clv": ((c - l) / (h - l)).where(h > l),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["r1"].mean()
    D["x1"] = D["r1"] - D["coin"].map(drift)
    D["x2"] = D["r2"] - D["coin"].map(drift)
    D["x35"] = D["r3_5"] - 3 * D["coin"].map(drift)
    D = D.dropna(subset=["mv", "x1"])

    def tday(s, sub):
        g = sub.assign(v=s).groupby("day")["v"]
        ds = g.sum(); n = g.count()
        m = ds.sum() / n.sum()
        dev = (sub.assign(v=s - m).groupby("day")["v"].sum())
        se = np.sqrt((dev**2).sum()) / n.sum()
        return m, m / se if se > 0 else np.nan, len(ds)

    def table(sub, key, ycol="x1"):
        out = []
        for k, g in sub.groupby(key, observed=True):
            m, t, nd = tday(g[ycol], g)
            out.append({"grp": str(k), "n": len(g), "days": nd, "mean%": 100 * m, "t": t})
        return pd.DataFrame(out)

    D["trend"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 99], labels=["fall", "chop", "rise"])
    D["mvq"] = pd.qcut(D["mv"], 10, labels=False)
    res = {}
    P = D[D["inprof"]]
    res["inprof_mv_decile_next"] = table(P, "mvq")
    res["all_mv_decile_next"] = table(D, "mvq")
    res["inprof_mv_decile_day2"] = table(P, "mvq", "x2")
    res["inprof_mv_decile_d3to5"] = table(P, "mvq", "x35")
    res["notprof_by_trend_mvq_ext"] = table(D[~D["inprof"] & D["mvq"].isin([0, 9])].assign(k=lambda x: x["trend"].astype(str) + "_" + x["mvq"].astype(str)), "k")
    res["inprof_clv_q_next"] = table(P.assign(q=pd.qcut(P["clv"], 5, labels=False)), "q")
    res["all_clv_q_next"] = table(D.assign(q=pd.qcut(D["clv"], 5, labels=False)), "q")
    res["all_weekday_next"] = table(D, "wd")
    res["inprof_weekday_next"] = table(P, "wd")
    res["all_year_next_top_decile"] = table(D[D["mvq"] == 9], "year")
    res["all_year_next_bot_decile"] = table(D[D["mvq"] == 0], "year")
    res["share_inprof"] = float(D["inprof"].mean())
    # book days: largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin, win=w))
    DD = pd.concat(dd).dropna(subset=["book_return"])
    bk = DD.groupby("day")[["book_return", "coin_return"]].mean()
    bk["q"] = pd.qcut(bk["book_return"].rank(method="first"), 20, labels=False)
    res["book_by_vigintile"] = bk.groupby("q").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    return res
