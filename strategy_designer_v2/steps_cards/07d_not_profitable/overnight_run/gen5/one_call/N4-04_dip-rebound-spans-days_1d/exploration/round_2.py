def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(b)
            fc = b["forecast"].fillna(0).values
            r = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            vol = pd.Series(r).rolling(20, min_periods=10).std().values
            dd20 = cl / pd.Series(cl).rolling(20, min_periods=5).max().values - 1
            last = -10
            for t in range(n - 3):
                if fc[t] > 0 and t - last > 3:
                    last = t
                    rows.append({"coin": c, "win": w, "fc": fc[t], "r0": r[t], "vol": vol[t],
                                 "dd20": dd20[t],
                                 "r1": cl[t+1]/cl[t]-1, "r23": cl[t+3]/cl[t+1]-1, "r3": cl[t+3]/cl[t]-1,
                                 "fc1": fc[t+1]})
    E = pd.DataFrame(rows)
    def summ(g):
        return pd.Series({"n": len(g), "r1": g.r1.mean(), "r23": g.r23.mean(), "r3": g.r3.mean(),
                          "t_r1": stats.ttest_1samp(g.r1, 0).statistic if len(g) > 2 else np.nan,
                          "t_r23": stats.ttest_1samp(g.r23, 0).statistic if len(g) > 2 else np.nan,
                          "t_r3": stats.ttest_1samp(g.r3, 0).statistic if len(g) > 2 else np.nan})
    E["fbin"] = pd.cut(E.fc, [0, 1, 5, 10, 19.9, 20.1])
    out["fwd_by_fc"] = E.groupby("fbin", observed=True).apply(summ)
    E["volq"] = E.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["calm", "mid", "wild"]))
    out["fwd_by_vol"] = E.groupby("volq", observed=True).apply(summ)
    E["day1"] = np.where(E.r1 > 0, "day1_up", "day1_down")
    out["fwd_by_day1"] = E.groupby("day1").apply(summ)
    E["ddq"] = pd.cut(E.dd20, [-1, -0.15, -0.08, -0.03, 0.01])
    out["fwd_by_dd20"] = E.groupby("ddq", observed=True).apply(summ)
    E["period"] = np.where(E.win.str[1:].astype(int) <= 10, "w1-w10", "w11-w24")
    out["fwd_by_period"] = E.groupby("period").apply(summ)
    # book: position size vs day returns
    D = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            pv = b["postRebalance_total_value"]
            d = pd.DataFrame({"ret": pv.pct_change(), "pos": b["postRebalance_current_allocation"].shift(1),
                              "cr": b["close"].pct_change()})
            d["coin"] = c; d["win"] = w; D.append(d)
    D = pd.concat(D).dropna()
    D = D[D.pos.abs() > 0.01]
    D["psz"] = pd.cut(D.pos, [0, 0.5, 1.5, 3])
    out["book_by_pos"] = D.groupby("psz", observed=True).agg(n=("ret", "size"), mean=("ret", "mean"), sd=("ret", "std"),
        worst=("ret", "min"), sum=("ret", "sum"), coin_mean=("cr", "mean"))
    return out
