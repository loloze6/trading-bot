def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    allrows = []
    ev = []
    for coin, wins in data["bars"].items():
        for h in [3, 10, 20]:
            pass
        drifts = {}
        for h in [3, 10, 20]:
            xs = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c)-h, h):
                    xs.append(c[i+h]/c[i]-1)
            drifts[h] = np.mean(xs)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values)
            p30 = c.pct_change(30).values
            hi90 = c.rolling(90, min_periods=60).max().values
            d90 = c.values/hi90 - 1
            vol = c.pct_change().rolling(30).std().values
            f = b["forecast"].fillna(0).values
            raw = b["debug_info.components.res_break.last_history_value"].values
            cv = c.values
            # non-overlapping 10-day grid on all bars
            for i in range(0, len(cv)-10, 10):
                if np.isnan(p30[i]) or np.isnan(d90[i]): continue
                allrows.append({"coin": coin, "p30": p30[i], "d90": d90[i], "vol": vol[i],
                                "x10": cv[i+10]/cv[i]-1-drifts[10]})
            for i in range(1, len(cv)):
                if f[i] > 0 and f[i-1] <= 0 and not np.isnan(d90[i]):
                    r = {"coin": coin, "window": w, "raw": raw[i], "p30": p30[i], "athi": d90[i] >= -1e-9}
                    for h in [3, 10, 20]:
                        if i+h < len(cv):
                            r[f"x{h}"] = cv[i+h]/cv[i]-1-drifts[h]
                    ev.append(r)
    A = pd.DataFrame(allrows)
    A["p30q"] = pd.qcut(A.p30, 5, labels=False)
    A["d90q"] = pd.qcut(A.d90, 5, labels=False)
    g = A.groupby("p30q").x10.agg(["mean", "count", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    g["p30"] = A.groupby("p30q").p30.mean()
    out["all_bars_p30_quintile_x10"] = g
    g = A.groupby("d90q").x10.agg(["mean", "count", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    g["d90"] = A.groupby("d90q").d90.mean()
    out["all_bars_dist_90d_high_quintile_x10"] = g
    sl = {}
    for coin, gg in A.groupby("coin"):
        if len(gg) > 30:
            sl[coin] = {"slope_p30": stats.linregress(gg.p30, gg.x10).slope,
                        "spearman_d90": stats.spearmanr(gg.d90, gg.x10)[0], "n": len(gg)}
    S = pd.DataFrame(sl).T
    out["per_coin_slopes"] = S
    out["per_coin_signs"] = pd.Series({"share_p30_pos": (S.slope_p30 > 0).mean(), "share_d90_pos": (S.spearman_d90 > 0).mean()})
    out["pooled_spearman"] = pd.Series({"p30_rho": stats.spearmanr(A.p30, A.x10)[0], "p30_p": stats.spearmanr(A.p30, A.x10)[1],
                                        "d90_rho": stats.spearmanr(A.d90, A.x10)[0], "d90_p": stats.spearmanr(A.d90, A.x10)[1], "n": len(A)})
    E = pd.DataFrame(ev)
    res = {}
    for k, gg in E.groupby("athi"):
        for h in [3, 10, 20]:
            x = gg[f"x{h}"].dropna()
            res[(k, h)] = {"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)}
    out["events_athi_t"] = pd.DataFrame(res).T
    # within at-high events, raw grading
    H = E[E.athi].copy()
    H["rq"] = pd.qcut(H.raw.rank(method="first"), 3, labels=False)
    out["athi_by_raw_tercile"] = H.groupby("rq").agg(raw=("raw", "mean"), x3=("x3", "mean"), x10=("x10", "mean"), n=("x10", "count"))
    N = E[~E.athi].copy()
    N["rq"] = pd.qcut(N.raw.rank(method="first"), 3, labels=False)
    out["not_athi_by_raw_tercile"] = N.groupby("rq").agg(raw=("raw", "mean"), x3=("x3", "mean"), x10=("x10", "mean"), n=("x10", "count"))
    out["athi_per_coin_x10_pos_share"] = pd.Series({"share": (H.groupby("coin").x10.mean() > 0).mean(), "ncoins": H.coin.nunique()})
    return out
