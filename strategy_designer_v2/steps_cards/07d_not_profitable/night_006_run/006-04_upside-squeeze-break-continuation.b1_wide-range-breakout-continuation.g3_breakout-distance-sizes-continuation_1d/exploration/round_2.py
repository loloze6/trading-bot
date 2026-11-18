def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = []
    act = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b.close; hi = b.high
            ph = hi.shift(1).rolling(20).max()
            dist = (cl - ph) / ph
            r10 = cl.shift(-10) / cl - 1
            r5 = cl.shift(-5) / cl - 1
            r60 = cl / cl.shift(60) - 1
            # days since last breakout (close above prior 20d high)
            bo = (dist > 0).astype(float)
            last = pd.Series(np.where(bo == 1, np.arange(len(b)), np.nan)).ffill()
            since = np.arange(len(b)) - last
            maxd10 = dist.clip(lower=0).rolling(10).max()
            alloc = b.postRebalance_current_allocation
            act.append(pd.DataFrame({"fc": b.forecast, "alloc": alloc}))
            idx = np.arange(0, len(b), 10)
            rows.append(pd.DataFrame({"dist": dist, "r10": r10, "r5": r5, "r60": r60, "since": since, "maxd10": maxd10, "coin": c}).iloc[idx])
    A = pd.concat(act)
    out["activity"] = pd.Series({"share_fc_pos": (A.fc > 0).mean(), "share_alloc_pos": (A.alloc > 0.001).mean(), "mean_alloc_when_fc_pos": A.loc[A.fc > 0, "alloc"].mean(), "mean_fc_when_pos": A.loc[A.fc > 0, "fc"].mean(), "median_fc_when_pos": A.loc[A.fc > 0, "fc"].median()})
    R = pd.concat(rows).dropna(subset=["r10", "dist", "r60"])
    R["ex10"] = R.r10 - R.coin.map(R.groupby("coin").r10.mean())
    def summ(x):
        return pd.Series({"n": len(x), "ex10": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan})
    R["grp"] = np.select([R.dist > 0, (R.since >= 1) & (R.since <= 10), R.since > 10], ["breakout_now", "broke_1to10d_ago", "older"], "none")
    out["by_since"] = R.groupby("grp")["ex10"].apply(summ).unstack()
    R["tr"] = np.where(R.r60 > 0, "up60", "down60")
    out["since_x_trend"] = R.groupby(["grp", "tr"])["ex10"].apply(summ).unstack()
    S = R[R.maxd10 > 0].copy()
    S["q"] = pd.qcut(S.maxd10, 3, labels=["low", "mid", "high"])
    out["maxd10_tercile"] = S.groupby("q")["ex10"].apply(summ).unstack()
    sl = stats.linregress(S.maxd10, S.ex10)
    out["maxd10_slope"] = pd.Series({"n": len(S), "slope": sl.slope, "t": sl.slope / sl.stderr})
    U = R[R.r60.notna()].copy()
    U["r60q"] = pd.qcut(U.r60, 4, labels=["q1", "q2", "q3", "q4"])
    out["r60_quartile_all"] = U.groupby("r60q")["ex10"].apply(summ).unstack()
    return out
