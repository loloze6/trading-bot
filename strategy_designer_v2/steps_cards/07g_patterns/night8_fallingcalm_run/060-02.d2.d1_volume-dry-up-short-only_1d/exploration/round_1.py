def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            ret60 = c / c.shift(60) - 1
            ret10 = c / c.shift(10) - 1
            ret5p = c / c.shift(5) - 1
            vm = v.rolling(30).mean()
            vr = np.log(vm / vm.shift(30))
            vr10 = np.log(v.rolling(10).mean() / v.rolling(30).mean().shift(10))
            sd30 = r1.rolling(30).std()
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]) / c
            clpos = (c - b["low"]) / (b["high"] - b["low"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "ret60": ret60, "ret10": ret10,
                               "ret5p": ret5p, "vr": vr, "vr10": vr10, "fwd": fwd, "fwd1": fwd1, "r1": r1,
                               "sd30": sd30, "rng": rng, "clpos": clpos,
                               "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.loc[d.pos % H == 0, "fwd"].groupby(d["coin"]).mean()
    d["ufwd"] = d["fwd"] - d["coin"].map(drift)
    g = d[(d.pos % H == 0) & d.fwd.notna()].copy()
    g["trend"] = np.where(g.ret60 > 0.10, "rising", np.where(g.ret60 < -0.10, "falling", "choppy"))
    g = g[g.ret60.notna()]

    def summ(x, col="ufwd"):
        x = x[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    g["vrq"] = g.groupby("trend")["vr"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ufwd5 by trend x vol-ratio quintile"] = g.groupby(["trend", "vrq"]).apply(summ).round(4)
    gf = g[g.trend == "falling"]
    out["falling: ufwd5 by ret10 sign x vr sign"] = gf.groupby([gf.ret10 < 0, gf.vr < 0]).apply(summ).round(4)
    g["sdq"] = g.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["ufwd5 by trend x swing tercile"] = g.groupby(["trend", "sdq"]).apply(summ).round(4)
    g["r5q"] = g.groupby("trend")["ret5p"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ufwd5 by trend x past-5d-return quintile"] = g.groupby(["trend", "r5q"]).apply(summ).round(4)
    g["v10q"] = g.groupby("trend")["vr10"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["ufwd5 by trend x 10d-vs-30d volume quintile"] = g.groupby(["trend", "v10q"]).apply(summ).round(4)
    # daily bars: weekday, 1d after large moves
    dd = d[d.fwd1.notna() & d.ret60.notna()].copy()
    dd["trend"] = np.where(dd.ret60 > 0.10, "rising", np.where(dd.ret60 < -0.10, "falling", "choppy"))
    dd["z"] = dd.r1 / dd.sd30
    dd["zq"] = pd.cut(dd.z, [-99, -2, -1, 0, 1, 2, 99])
    out["next-day ret by trend x today z-move"] = dd.groupby(["trend", "zq"]).apply(lambda x: summ(x, "fwd1")).round(4)
    out["next-day ret by weekday"] = dd.groupby("wd").apply(lambda x: summ(x, "fwd1")).round(4)
    dd["cq"] = pd.cut(dd.clpos, [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["next-day ret by trend x close position"] = dd.groupby(["trend", "cq"]).apply(lambda x: summ(x, "fwd1")).round(4)
    # book
    days = pd.concat([df.assign(coin=c, w=w) for c, ws in data["days"].items() for w, df in ws.items()])
    br = days.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book daily by window: mean, sd, sum"] = br.groupby(level=0).agg(["count", "mean", "std", "sum"]).round(5)
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median", "min", "max"]).round(3)
    return out
