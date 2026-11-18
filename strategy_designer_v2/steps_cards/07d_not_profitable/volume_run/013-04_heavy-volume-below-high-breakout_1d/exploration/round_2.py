def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            c = b["close"].values; v = b["volume"].values
            tr = (b["regime"] == "trending").values
            n = len(b)
            vr = pd.Series(v).rolling(10).mean() / pd.Series(v).rolling(90, min_periods=30).mean()
            last_break = -10**9; peak = np.nan
            for t in range(n):
                if tr[t] and (t == 0 or not tr[t-1]):
                    last_break = t; peak = c[t]
                if t - last_break <= 30 and t - last_break >= 0:
                    peak = max(peak, c[t])
                    rows.append(dict(coin=coin, w=w, t=t, k=t - last_break,
                                     fwd1=(c[t+1]/c[t]-1) if t+1 < n else np.nan,
                                     inpos=abs(alloc[t]) > 1e-9,
                                     dd=c[t]/peak - 1,
                                     vr_break=np.nan))
    R = pd.DataFrame(rows)
    # coin mean daily return over all windows
    cm = {}
    for coin, wins in data["bars"].items():
        x = pd.concat([ (b["close"].shift(-1)/b["close"]-1) for b in wins.values()])
        cm[coin] = x.mean()
    R["ex1"] = R["fwd1"] - R["coin"].map(cm)
    R = R.dropna(subset=["ex1"])
    R["kb"] = pd.cut(R["k"], [-1, 0, 2, 5, 10, 20, 30])
    g = R.groupby("kb", observed=True)["ex1"]
    out["daily excess by days since break"] = pd.DataFrame({"mean": g.mean(), "n": g.size(),
        "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    o = R.groupby("inpos")["ex1"]
    out["post-break 30d bars: in vs out"] = pd.DataFrame({"mean": o.mean(), "n": o.size(),
        "t": o.mean() / (o.std() / np.sqrt(o.size()))})
    out["share of post-break 30d bars held"] = R["inpos"].mean()
    # graded by drawdown from post-break peak, out-of-position bars with k>=1
    S = R[(R["k"] >= 1)]
    S = S.assign(ddq=pd.qcut(S["dd"].rank(method="first"), 4, labels=["deep", "q2", "q3", "at peak"]))
    q = S.groupby("ddq", observed=True)["ex1"]
    out["k>=1 daily excess by distance to post-break peak"] = pd.DataFrame({"mean dd": S.groupby("ddq", observed=True)["dd"].mean(),
        "mean ex1": q.mean(), "n": q.size(), "t": q.mean() / (q.std() / np.sqrt(q.size()))})
    # non-overlapping return from day 1 after break to day 30
    rr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].values; tr = (b["regime"] == "trending").values; n = len(c)
            last = -999
            for t in range(1, n):
                if tr[t] and not tr[t-1] and t - last >= 30 and t + 30 < n:
                    last = t
                    rr.append(dict(coin=coin, r0_30=c[t+30]/c[t]-1, r2_30=c[t+30]/c[t+2]-1,
                                   r0_2=c[t+2]/c[t]-1))
    RR = pd.DataFrame(rr)
    m30 = {}
    for coin, wins in data["bars"].items():
        xs = []
        for b in wins.values():
            cc = b["close"].values
            xs += [cc[i+30]/cc[i]-1 for i in range(0, len(cc)-30, 30)]
        m30[coin] = np.mean(xs)
    RR["ex0_30"] = RR["r0_30"] - RR["coin"].map(m30)
    out["break cases"] = pd.Series({"n": len(RR), "mean r0_2": RR["r0_2"].mean(), "mean r2_30": RR["r2_30"].mean(),
        "mean ex0_30": RR["ex0_30"].mean(),
        "t ex0_30": RR["ex0_30"].mean() / (RR["ex0_30"].std() / np.sqrt(len(RR))),
        "share r2_30>0": (RR["r2_30"] > 0).mean()})
    return out
