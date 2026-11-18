def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        dmap = data["days"][coin]
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            sd20 = r1.rolling(20).std(); z = r1/sd20
            vr = b["volume"]/b["volume"].rolling(30).mean()
            v = b["postRebalance_total_value"]
            gain = b["postRebalance_current_allocation"]*(c.shift(-1)/c-1)
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr, "s": z.clip(lower=0)*vr,
                               "f1": c.shift(-1)/c-1, "f2_6": c.shift(-6)/c.shift(-1)-1,
                               "f5": c.shift(-5)/c-1,
                               "gain0": gain, "gain1_4": gain.shift(-1).rolling(4).sum().shift(-3),
                               "alloc1": b["postRebalance_current_allocation"].shift(-1),
                               "alloc3": b["postRebalance_current_allocation"].shift(-3),
                               "pos": np.arange(len(b))})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for col in ["f1", "f2_6", "f5"]:
        A["ex_"+col] = A[col]-A.groupby("coin")[col].transform("mean")
    def summ(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(n)) if n > 2 else np.nan, "n": n})
    out = {}
    g = A[(A.pos % 5 == 0)].dropna(subset=["s", "ex_f2_6"])
    up = g[g.z > 0].copy()
    up["sq"] = up.groupby("coin").s.transform(lambda x: pd.qcut(x, 5, labels=False))
    out["delayed ex(day2-6) by own-coin z*vr quintile, up days"] = up.groupby("sq").ex_f2_6.apply(summ).unstack()
    out["next-day ex by z*vr quintile, up days"] = up.groupby("sq").ex_f1.apply(summ).unstack()
    out["spearman s vs ex day2-6 (up days)"] = str(stats.spearmanr(up.s, up.ex_f2_6))
    out["spearman s vs ex day1 (up days)"] = str(stats.spearmanr(up.s, up.ex_f1))
    out["delayed ex by coin, top quintile"] = up[up.sq == 4].groupby("coin").ex_f2_6.apply(summ).unstack()
    A["sq"] = A[A.z > 0].groupby("coin").s.transform(lambda x: pd.qcut(x, 5, labels=False))
    top = A[A.sq == 4]
    out["book on top events: alloc after 1 and 3 bars, gain day0 vs days1-4"] = pd.Series({
        "alloc_next": top.alloc1.abs().mean(), "alloc_3later": top.alloc3.abs().mean(),
        "gain_day0": top.gain0.mean(), "gain_days1_4": top.gain1_4.mean()})
    return out
