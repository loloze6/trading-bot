def explore(data):
    import numpy as np, pandas as pd
    out = {}
    D = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            D.append(pd.DataFrame({"coin": c, "cr": d["coin_return"].values}))
    D = pd.concat(D)
    mu = D.groupby("coin")["cr"].mean()
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(b)
            r = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            sd30 = pd.Series(r).rolling(30, min_periods=25).std().values
            sdall = np.nanstd(r)
            mad = pd.Series(np.abs(r)).rolling(30, min_periods=20).mean().values
            run = np.zeros(n, int)
            for i in range(1, n):
                run[i] = run[i-1] + 1 if r[i] < 0 else 0
            for i in range(30, n - 1):
                tr60 = cl[i] / cl[i-60] - 1 if i >= 60 else np.nan
                tr30 = cl[i] / cl[i-30] - 1
                brk = (r[i] > 0) and run[i-1] >= 2 and (i - 1 - run[i-1] >= 0)
                depth = np.nan
                if brk:
                    depth = -(cl[i-1] / cl[i-1-run[i-1]] - 1) / mad[i]
                rows.append(dict(coin=c, wn=int(w[1:]), i=i, brk=brk, k=run[i-1] if brk else 0, depth=depth,
                                 tr60=tr60, tr30=tr30, agit=sd30[i] > sdall,
                                 unus=-(r[i+1] - mu[c]), alloc=b["postRebalance_current_allocation"].iloc[i],
                                 bk=b["postRebalance_total_value"].iloc[i+1] / b["postRebalance_total_value"].iloc[i] - 1))
    A = pd.DataFrame(rows)
    def g(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean_short": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    A["t30"] = pd.cut(A["tr30"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    A["t60"] = pd.cut(A["tr60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    out["t30_brk_vs_nonbrk"] = A.groupby(["t30", "brk"])["unus"].apply(g).unstack()
    out["t60_brk_vs_nonbrk"] = A.groupby(["t60", "brk"])["unus"].apply(g).unstack()
    out["t30_agit_brk"] = A[A.brk].groupby(["t30", "agit"])["unus"].apply(g).unstack()
    out["t30_agit_nonbrk"] = A[~A.brk].groupby(["t30", "agit"])["unus"].apply(g).unstack()
    F = A[A.brk & (A.t30 == "fall")].copy()
    F["dq"] = pd.qcut(F["depth"], 3, labels=["shallow", "mid", "deep"])
    out["fall30_brk_by_depth"] = F.groupby("dq")["unus"].apply(g).unstack()
    F["held"] = F.alloc < 0
    out["fall30_brk_held"] = F.groupby("held")["unus"].apply(g).unstack()
    out["fall30_brk_by_window"] = F.groupby("wn")["unus"].agg(["size", "mean"])
    # book loss days: which held bars lose
    Hd = A[A.alloc < 0]
    out["held_bars_by_t30"] = Hd.groupby("t30")["bk"].agg(["size", "mean", "sum"])
    out["held_bars_by_brk"] = Hd.groupby("brk")["bk"].agg(["size", "mean", "sum"])
    return out
