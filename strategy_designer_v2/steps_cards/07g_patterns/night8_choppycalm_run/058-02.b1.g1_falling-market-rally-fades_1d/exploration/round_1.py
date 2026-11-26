def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd20 = r.rolling(20).std()
            z = r / sd20
            ret60 = c / c.shift(60) - 1
            hi20 = b["high"].astype(float).rolling(20).max()
            lo20 = b["low"].astype(float).rolling(20).min()
            pos = (c - lo20) / (hi20 - lo20)
            vol30 = r.rolling(30).std()
            vrank = vol30.rolling(90, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            n1 = c.shift(-1) / c - 1
            n3 = c.shift(-3) / c - 1
            n5 = c.shift(-5) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "z": z, "ret60": ret60,
                               "pos": pos, "n1": n1, "n3": n3, "n5": n5, "vrank": vrank,
                               "wd": ts.dt.weekday, "regime": b["regime"],
                               "br": b["postRebalance_total_value"].astype(float).pct_change().shift(-1),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "ret5": c / c.shift(5) - 1, "sd20": sd20})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    # demean by coin mean
    for h in ["n1", "n3", "n5"]:
        d[h + "u"] = d[h] - d.groupby("coin")[h].transform("mean")
    d["trend"] = np.where(d.ret60 > 0.10, "rising", np.where(d.ret60 < -0.10, "falling", "choppy"))
    d.loc[d.ret60.isna(), "trend"] = np.nan
    d["agit"] = np.where(d.vrank > 0.5, "agit", "calm")
    d.loc[d.vrank.isna(), "agit"] = np.nan

    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    # 1. scaled 1-day move quintile -> next day, by trend
    e = d.dropna(subset=["z", "trend", "n1u"]).copy()
    e["zq"] = pd.cut(e.z, [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    out["z bucket x trend next1 unusual"] = e.groupby(["trend", "zq"], observed=True).apply(lambda g: summ(g, "n1u")).round(3)

    # 2. range position, 3-day grid, by trend
    g3 = d[d.i % 3 == 0].dropna(subset=["pos", "trend", "n3u"]).copy()
    g3["pq"] = pd.cut(g3.pos, [-0.01, 0.2, 0.4, 0.6, 0.8, 1.01])
    out["range pos x trend next3 unusual"] = g3.groupby(["trend", "pq"], observed=True).apply(lambda g: summ(g, "n3u")).round(3)
    g3b = g3.dropna(subset=["agit"])
    out["range pos x agit (choppy) next3"] = g3b[g3b.trend == "choppy"].groupby(["agit", "pq"], observed=True).apply(lambda g: summ(g, "n3u")).round(3)

    # 3. weekday next1
    e1 = d.dropna(subset=["n1u"])
    out["weekday next1 unusual"] = e1.groupby("wd").apply(lambda g: summ(g, "n1u")).round(3)

    # 4. 5-day return scaled, 5-day grid, by trend
    g5 = d[d.i % 5 == 0].dropna(subset=["ret5", "sd20", "trend", "n5u"]).copy()
    g5["z5"] = g5.ret5 / (g5.sd20 * np.sqrt(5))
    g5["zq"] = pd.cut(g5.z5, [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    out["5d scaled x trend next5 unusual"] = g5.groupby(["trend", "zq"], observed=True).apply(lambda g: summ(g, "n5u")).round(3)

    # 5. book: largest gains/losses bars, what z precedes
    bk = d.dropna(subset=["br"])
    bk = bk[bk.alloc.abs() > 0]
    q = bk.br.quantile([0.05, 0.95])
    out["book worst5% mean z, ret5, n"] = pd.Series({"worst_z": bk[bk.br <= q[0.05]].z.mean(), "worst_ret5": bk[bk.br <= q[0.05]].ret5.mean(),
                                                    "best_z": bk[bk.br >= q[0.95]].z.mean(), "best_ret5": bk[bk.br >= q[0.95]].ret5.mean(), "n": len(bk)}).round(4)
    # vol level next1 by trend
    e2 = d.dropna(subset=["agit", "trend", "n1u"])
    out["trend x agit next1 unusual"] = e2.groupby(["trend", "agit"]).apply(lambda g: summ(g, "n1u")).round(3)
    return out
