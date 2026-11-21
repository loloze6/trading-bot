def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    recs = []
    exp_rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            n = len(b)
            sma50 = cl.rolling(50, min_periods=20).mean()
            slope = sma50 / sma50.shift(10) - 1
            r60p = cl / cl.shift(60) - 1
            r5p = cl / cl.shift(5) - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            prev = pos.shift(1).fillna(0)
            gain = pos * (cl.shift(-1) / cl - 1)
            exp_rows.append(dict(c=c, w=w, expo=pos.mean(), gain=gain.sum(), coin=cl.iloc[-1] / cl.iloc[0] - 1))
            ent = b.index[(prev <= 1e-9) & (pos > 1e-9)]
            for i in ent:
                j = i + 20
                if j >= n: continue
                fwd = cl[j] / cl[i] - 1
                # failed-break: close below entry within first 5 days, then return from that day to j
                k5 = min(i + 5, j)
                r5f = cl[k5] / cl[i] - 1
                rest = cl[j] / cl[k5] - 1
                recs.append(dict(c=c, w=w, slope=slope[i], r60p=r60p[i], r5p=r5p[i], fwd=fwd,
                                 r5f=r5f, rest=rest, alloc=pos[i]))
    T = pd.DataFrame(recs)
    E = pd.DataFrame(exp_rows)
    out["n_full"] = len(T)
    fallw = ["w12", "w13", "w14"]
    E["fall"] = E["w"].isin(fallw)
    out["exposure_fall_vs_other"] = E.groupby("fall").agg(expo=("expo", "mean"), gain=("gain", "mean"), coin=("coin", "mean"), n=("c", "size"))
    T["fall"] = T["w"].isin(fallw)
    out["entries_fall_vs_other"] = T.groupby("fall").agg(n=("fwd", "size"), fwd=("fwd", "mean"), slope=("slope", "mean"), r60p=("r60p", "mean"))
    for col in ["slope", "r60p", "r5p", "r5f"]:
        q = pd.qcut(T[col], 4, duplicates="drop")
        out["by_" + col] = T.groupby(q, observed=True).agg(n=("fwd", "size"), fwd=("fwd", "mean"), rest=("rest", "mean"), loss10=("fwd", lambda x: (x < -0.1).mean()))
    # after early failure, does it keep falling?
    T["early"] = pd.cut(T["r5f"], [-1, -0.08, -0.03, 0, 0.05, 10])
    g = T.groupby("early", observed=True)["rest"]
    out["rest_after_first5d"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "t": g.apply(lambda x: stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan)})
    out["corr_slope_fwd"] = stats.spearmanr(T["slope"], T["fwd"], nan_policy="omit")[0]
    out["corr_r60_fwd"] = stats.spearmanr(T["r60p"], T["fwd"], nan_policy="omit")[0]
    # slope sign
    T["slope_pos"] = T["slope"] > 0
    g = T.groupby("slope_pos")["fwd"]
    out["by_slope_sign"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "loss10": g.apply(lambda x: (x < -0.1).mean())})
    return out
