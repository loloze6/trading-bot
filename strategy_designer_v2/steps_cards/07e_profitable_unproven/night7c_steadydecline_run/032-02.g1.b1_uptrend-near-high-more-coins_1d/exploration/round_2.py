def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = pd.Series(b["close"].values); n = len(cl)
            r28 = cl.pct_change(28).values
            r14 = cl.pct_change(14).values
            prox = (cl / cl.rolling(28, min_periods=28).max()).values
            lr = np.log(cl).diff()
            vol = lr.rolling(28, min_periods=20).std().values
            clv = cl.values
            for h in (5, 10):
                for i in range(0, n - h, h):
                    recs.append((c, w, h, i, clv[i + h] / clv[i] - 1, b["regime"].iloc[i] == "trending", r28[i], r14[i], prox[i], vol[i]))
    R = pd.DataFrame(recs, columns=["coin", "win", "h", "i", "ret", "inreg", "r28", "r14", "prox", "vol"])
    R["ex"] = R["ret"] - R.groupby(["coin", "h"])["ret"].transform("mean")
    R["z"] = R["ex"] / R.groupby(["coin", "h"])["ret"].transform("std")
    res = {}
    for h in (5, 10):
        g = R[R.h == h]
        a, b_ = g[g.inreg]["ex"], g[~g.inreg]["ex"]
        res[h] = {"in_minus_out": a.mean() - b_.mean(), "welch_t": stats.ttest_ind(a, b_, equal_var=False)[0], "n_in": len(a), "n_out": len(b_)}
    out["in_vs_out"] = pd.DataFrame(res).T
    # per window in-out at h=5
    g = R[R.h == 5]
    pw = g.groupby(["win", "inreg"])["ex"].mean().unstack()
    pw["diff"] = pw[True] - pw[False]
    out["in_out_by_window_h5"] = pw
    out["in_out_by_coin_h5"] = g.groupby(["coin", "inreg"])["ex"].mean().unstack().assign(diff=lambda x: x[True] - x[False])
    # proximity graded on all bars
    A = R.dropna(subset=["prox", "r28"]).copy()
    A["proxq"] = A.groupby("h")["prox"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["ex_by_prox_all"] = A.groupby(["h", "proxq"])["ex"].agg(["mean", "count"]).unstack()
    out["z_by_prox_all"] = A.groupby(["h", "proxq"])["z"].mean().unstack()
    out["spearman_all"] = A.groupby("h").apply(lambda q: pd.Series({
        "prox": stats.spearmanr(q.prox, q.ex)[0], "r28": stats.spearmanr(q.r28, q.ex)[0],
        "r14": stats.spearmanr(q.r14.fillna(0), q.ex)[0], "r28_over_vol": stats.spearmanr((q.r28 / q.vol).fillna(0), q.ex)[0], "n": len(q)}))
    # t of prox top quintile minus bottom quintile, all bars
    tq = {}
    for h in (5, 10):
        q = A[A.h == h]
        tq[h] = {"top_minus_bot": q[q.proxq == 4].ex.mean() - q[q.proxq == 0].ex.mean(),
                 "t": stats.ttest_ind(q[q.proxq == 4].ex, q[q.proxq == 0].ex, equal_var=False)[0]}
    out["prox_top_bot_all"] = pd.DataFrame(tq).T
    # prox top quintile by window sign, h=5
    q = A[A.h == 5]
    out["prox_q4_minus_q0_by_window_h5"] = q.groupby(["win", "proxq"])["ex"].mean().unstack().pipe(lambda x: x[4] - x[0])
    # trades concentration
    tr = pd.concat([t.assign(coin=c, win=w) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    out["trades_by_coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median", "sum"])
    # book without best days
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            rows.append(d.assign(win=w))
    D = pd.concat(rows).dropna(subset=["book_return"])
    daily = D.groupby(["win", "day"])["book_return"].mean()
    s = daily.sort_values(ascending=False)
    out["book_trim"] = pd.Series({"mean": daily.mean(), "mean_wo_top10": s.iloc[10:].mean(), "mean_wo_top30": s.iloc[30:].mean(),
                                  "share_pos_days": (daily > 0).mean()})
    return out
