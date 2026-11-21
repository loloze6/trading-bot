def explore(data):
    import pandas as pd, numpy as np
    out = {}
    coins = list(data["days"].keys())
    early = {f"w{i}" for i in range(1, 11)}
    cs = []
    pos_rows = []
    for c in coins:
        drift_l = []
        for w, b in data["bars"][c].items():
            cl = b["close"].values
            if len(cl) > 120:
                drift_l.extend(list(cl[120::120] / cl[:-120:120] - 1))
        drift = np.mean(drift_l)
        for w, b in data["bars"][c].items():
            cl = b["close"].values; fc = b["forecast"].fillna(0).values
            al = b["postRebalance_current_allocation"].fillna(0).values
            n = len(cl)
            s = pd.Series(cl)
            lr = np.log(s).diff()
            r24 = s / s.shift(24) - 1
            mad = (s / s.shift(24) - 1).abs().rolling(720, min_periods=300).mean()
            z24 = r24 / mad
            hi = s.rolling(720, min_periods=200).max()
            lo = s.rolling(720, min_periods=200).min()
            pos_rng = (s - lo) / (hi - lo)
            hi_chg = hi / hi.shift(168) - 1
            age = s.rolling(720, min_periods=200).apply(lambda x: len(x) - 1 - np.argmax(x), raw=True)
            r2160 = s / s.shift(1440) - 1
            # position-level: hourly gain of the position, early vs late windows
            g = al[:-1] * (cl[1:] / cl[:-1] - 1)
            pos_rows.append(dict(coin=c, early=w in early, gain=g.sum(), expo=np.mean(np.abs(al)),
                                 coin_ret=np.sum(lr.values[1:][~np.isnan(lr.values[1:])])))
            for g0 in range(0, n - 120, 120):
                idx = np.where(fc[g0:g0 + 120] > 2)[0]
                if len(idx) == 0: continue
                t = g0 + idx[0]
                if t + 120 >= n: continue
                fwd = cl[t + 120] / cl[t] - 1
                r_first24 = cl[t + 24] / cl[t] - 1
                rest = cl[t + 120] / cl[t + 24] - 1
                cs.append(dict(coin=c, early=w in early, unus=fwd - drift, fwd=fwd,
                               z24=z24[t], pos_rng=pos_rng[t], hi_chg=hi_chg[t], age=age[t],
                               r60d=r2160[t], first24=r_first24, rest=rest, alloc=al[t]))
    C = pd.DataFrame(cs)

    def grp(col, q=4, df=None):
        x = (C if df is None else df).dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, duplicates="drop")
        g = x.groupby("b", observed=True)
        res = g.agg(n=("unus", "size"), unus=("unus", "mean"), fwd=("fwd", "mean"),
                    loss10=("fwd", lambda v: (v < -0.1).mean()))
        res["t"] = g["unus"].apply(lambda v: v.mean() / (v.std() / np.sqrt(len(v))))
        res.index = res.index.astype(str)
        return res
    for col in ["z24", "pos_rng", "hi_chg", "age", "r60d"]:
        out["by_" + col] = grp(col)
    out["by_early"] = C.groupby("early").agg(n=("unus", "size"), unus=("unus", "mean"),
                                             fwd=("fwd", "mean"), alloc=("alloc", "mean"))
    out["early_by_hi_chg"] = grp("hi_chg", 3, C[C.early])
    out["early_by_r60d"] = grp("r60d", 3, C[C.early])
    out["early_by_z24"] = grp("z24", 3, C[C.early])
    # after the first 24h: does a falling start keep falling?
    out["rest_by_first24"] = C.dropna(subset=["first24"]).assign(
        b=lambda x: pd.qcut(x["first24"], 5).astype(str)).groupby("b").agg(
        n=("rest", "size"), rest=("rest", "mean"), rest_t=("rest", lambda v: v.mean() / (v.std() / np.sqrt(len(v)))))
    P = pd.DataFrame(pos_rows)
    out["pos_gain_early_late"] = P.groupby("early").agg(gain=("gain", "sum"), expo=("expo", "mean"),
                                                         coin_logret=("coin_ret", "sum"))
    return out
