def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            c = b["close"].values; f = b["forecast"].values
            cols = b.columns
            nh = [x for x in cols if "near_high" in x and "post_pipeline" in x]
            rs = [x for x in cols if "rise" in x and "post_pipeline" in x]
            nhr = [x for x in cols if "near_high" in x and "last_history" in x]
            rsr = [x for x in cols if "rise" in x and "last_history" in x]
            nhv = b[nh[0]].values if nh else np.full(len(c), np.nan)
            rsv = b[rs[0]].values if rs else np.full(len(c), np.nan)
            nhraw = b[nhr[0]].values if nhr else np.full(len(c), np.nan)
            rsraw = b[rsr[0]].values if rsr else np.full(len(c), np.nan)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for h in [1, 5, 10, 20]:
                for i in range(0, len(c) - h, h):
                    recs.append((coin, w, yr[i], h, f[i], nhv[i], rsv[i], nhraw[i], rsraw[i], c[i + h] / c[i] - 1))
    A = pd.DataFrame(recs, columns=["coin", "w", "year", "h", "f", "nh", "rs", "nhraw", "rsraw", "r"])
    A["r_ex"] = A["r"] - A.groupby(["coin", "h"])["r"].transform("mean")
    res = []
    for h in [1, 5, 10, 20]:
        S = A[(A.h == h) & (A.f > 0)]
        v = S["f"] / 10 * S["r_ex"]
        res.append((h, v.mean(), v.mean() / (v.std() / np.sqrt(len(v))), len(v)))
    out["plan_measure_by_h"] = pd.DataFrame(res, columns=["h", "mean", "t", "n"])
    # quartile at h=5 and t top vs bottom
    q = []
    for h in [1, 5, 10]:
        S = A[(A.h == h) & (A.f > 0)].copy()
        S["q"] = pd.qcut(S["f"], 4, labels=False, duplicates="drop")
        top = S[S.q == 3]["r_ex"]; bot = S[S.q == 0]["r_ex"]
        q.append((h, bot.mean(), S[S.q == 1]["r_ex"].mean(), S[S.q == 2]["r_ex"].mean(), top.mean(),
                  stats.ttest_ind(top, bot, equal_var=False).statistic, len(top)))
    out["quartiles_by_h_top_minus_bot_t"] = pd.DataFrame(q, columns=["h", "q0", "q1", "q2", "q3", "t_q3_minus_q0", "n_q3"])
    # components at h=5 among on
    S = A[(A.h == 5) & (A.f > 0)].dropna(subset=["nh", "rs"])
    comp = {}
    for col in ["nh", "rs", "nhraw", "rsraw"]:
        x = S[col]
        comp[col] = (stats.spearmanr(x, S["r_ex"]).correlation, len(S))
    out["comp_spearman_h5"] = pd.DataFrame(comp, index=["rho", "n"]).T
    # top quartile h=5 by coin and year
    S = A[(A.h == 5) & (A.f > 0)].copy()
    S["top"] = S["f"] >= S["f"].quantile(0.75)
    out["h5_excess_top_vs_rest_by_coin"] = S.groupby(["coin", "top"])["r_ex"].mean().unstack()
    out["h5_excess_top_vs_rest_by_year"] = S.groupby(["year", "top"])["r_ex"].mean().unstack()
    # book: days concentration
    rows = []
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            rows.append(d.assign(coin=coin, w=w))
    D = pd.concat(rows).dropna(subset=["book_return"])
    bk = D.groupby(["w", "day"])["book_return"].mean().sort_values(ascending=False)
    out["book_days"] = pd.Series({"mean": bk.mean(), "mean_drop_top1pct": bk.iloc[int(len(bk) * 0.01):].mean(),
                                  "mean_drop_top5pct": bk.iloc[int(len(bk) * 0.05):].mean(), "n": len(bk)})
    # book mean leave-one-coin-out
    out["book_leave_coin_out"] = pd.Series({c: D[D.coin != c].groupby(["w", "day"])["book_return"].mean().mean() for c in D.coin.unique()})
    return out
