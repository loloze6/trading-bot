def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            z = r1 / sd20
            vr = b["volume"] / b["volume"].rolling(30).mean()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "ts": ts, "z": z, "vr": vr,
                               "f1": c.shift(-1)/c-1, "f5": c.shift(-5)/c-1,
                               "f2_5": c.shift(-5)/c.shift(-1)-1, "f6_10": c.shift(-10)/c.shift(-5)-1,
                               "f10": c.shift(-10)/c-1,
                               "alloc": b["postRebalance_current_allocation"],
                               "wd": ts.dt.weekday, "year": ts.dt.year,
                               "pos": np.arange(len(b))})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for col in ["f1", "f5", "f2_5", "f6_10", "f10"]:
        A["ex_"+col] = A[col] - A.groupby("coin")[col].transform("mean")
    def summ(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(n)) if n > 2 else np.nan, "n": n})
    out = {}
    A["zq"] = A.groupby("coin").z.transform(lambda x: pd.qcut(x, 5, labels=False))
    A["vq"] = A.groupby("coin").vr.transform(lambda x: pd.qcut(x, 3, labels=False))
    # path after top-z heavy-volume days, on grid 10 for 10-day measures
    sel = A[(A.zq == 4) & (A.vq == 2)]
    g10 = sel[sel.pos % 10 == 0]
    out["path after top z heavy vol (grid10)"] = pd.DataFrame({k: summ(g10["ex_"+k]) for k in ["f1", "f2_5", "f6_10", "f10"]}).T
    out["path after top z heavy vol (all bars, overlapping, ref only)"] = pd.DataFrame({k: summ(sel["ex_"+k]) for k in ["f1", "f2_5", "f6_10"]}).T
    # falls by volume, grid5
    g5 = A[A.pos % 5 == 0]
    out["ex5 bottom z by vol tercile"] = g5[g5.zq == 0].groupby("vq").ex_f5.apply(summ).unstack()
    out["ex5 top z by vol tercile"] = g5[g5.zq == 4].groupby("vq").ex_f5.apply(summ).unstack()
    # weekday: cross-coin mean per date, then t
    D = A.dropna(subset=["ex_f1"]).groupby(["ts"]).agg(ex=("ex_f1", "mean"), wd=("wd", "first"), year=("year", "first"))
    out["weekday ex1 cross-coin daily mean"] = D.groupby("wd").ex.apply(summ).unstack()
    D["half"] = np.where(D.year <= 2021, "early", "late")
    out["weekday ex1 by half"] = D.groupby(["half", "wd"]).ex.mean().unstack()
    out["thu+fri minus rest by coin"] = A.dropna(subset=["ex_f1"]).assign(tf=lambda d: d.wd.isin([3, 4])).groupby("coin").apply(
        lambda d: pd.Series({"diff": d[d.tf].ex_f1.mean() - d[~d.tf].ex_f1.mean(),
                             "t": stats.ttest_ind(d[d.tf].ex_f1, d[~d.tf].ex_f1, equal_var=False).statistic}))
    D["tf"] = D.wd.isin([3, 4])
    out["thu+fri minus rest by year"] = D.groupby("year").apply(
        lambda d: pd.Series({"diff": d[d.tf].ex.mean() - d[~d.tf].ex.mean(),
                             "t": stats.ttest_ind(d[d.tf].ex, d[~d.tf].ex, equal_var=False).statistic}))
    # book: share of book held in-position days after the signal
    A["held"] = A.alloc.fillna(0).abs() > 1e-9
    out["mean alloc and days held per top-z heavy event"] = float(A[(A.zq == 4) & (A.vq == 2)].held.mean())
    return out
