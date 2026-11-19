def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    grid = []
    dd = []
    for coin in data["bars"]:
        cr_all = pd.concat([data["days"][coin][w]["coin_return"] for w in data["days"][coin]]).dropna()
        mu_d = cr_all.mean()
        for w, b in data["bars"][coin].items():
            c = b["close"].values
            v = b["volume"]
            ret72 = b["close"] / b["close"].shift(72) - 1
            top3 = v.rolling(72).apply(lambda x: np.sort(x)[-3:].sum() / x.sum() if x.sum() > 0 else np.nan, raw=True)
            r1 = b["close"].pct_change()
            # grind: share of up hours in last 72
            upsh = (r1 > 0).astype(float).rolling(72).mean()
            for i in range(0, len(b) - 72, 72):
                grid.append(dict(coin=coin, w=w, fwd=c[i+72]/c[i]-1, past=ret72.iloc[i],
                                 top3=top3.iloc[i], upsh=upsh.iloc[i], reg=b["regime"].iloc[i]))
            # daily book decomposition
            d = data["days"][coin][w].copy()
            b2 = b.copy()
            b2["day"] = pd.to_datetime(b2["timestamp"]).dt.floor("D")
            al = b2.groupby("day")["postRebalance_current_allocation"].mean()
            d["day2"] = pd.to_datetime(d["day"]).dt.floor("D") if not np.issubdtype(d["day"].dtype, np.datetime64) else d["day"].dt.floor("D")
            d["alloc"] = d["day2"].map(al)
            d["mu"] = mu_d
            d["coin"] = coin; d["w"] = w
            dd.append(d)
    g = pd.DataFrame(grid).dropna()
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    r = g[g["past"] > 0].copy()
    r["pq"] = pd.qcut(r["past"], 3, labels=False)
    r["cq"] = r.groupby("pq")["top3"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["risen_past_x_conc_mean"] = r.pivot_table(index="pq", columns="cq", values="ex", aggfunc="mean")
    out["risen_past_x_conc_n"] = r.pivot_table(index="pq", columns="cq", values="ex", aggfunc="count")
    tt = []
    for q in range(3):
        s = r[r.pq == q]
        t = stats.ttest_ind(s[s.cq == 2]["ex"], s[s.cq == 0]["ex"], equal_var=False)
        tt.append(dict(pq=q, diff=s[s.cq == 2]["ex"].mean() - s[s.cq == 0]["ex"].mean(), t=t.statistic, n=len(s)))
    out["conc_top_minus_bottom_by_pastq"] = pd.DataFrame(tt)
    # graded continuation over all bars: past return vs ex, by pct of up hours
    r["uq"] = pd.qcut(r["upsh"], 3, labels=False, duplicates="drop")
    out["risen_past_x_upshare"] = r.pivot_table(index="pq", columns="uq", values="ex", aggfunc="mean")
    out["corr_past_ex_all"] = pd.Series({"spearman_all": stats.spearmanr(g["past"], g["ex"])[0],
                                         "spearman_risen": stats.spearmanr(r["past"], r["ex"])[0],
                                         "spearman_conc_risen": stats.spearmanr(r["top3"], r["ex"])[0],
                                         "n_all": len(g), "n_risen": len(r)})
    D = pd.concat(dd).dropna(subset=["book_return"])
    D["drift"] = D["alloc"] * D["mu"]
    out["book_decomp"] = pd.Series({"book_mean": D["book_return"].mean(), "drift_part": D["drift"].mean(),
                                    "timing_and_fees": D["book_return"].mean() - D["drift"].mean(),
                                    "gross_timing_proxy": (D["alloc"] * D["coin_return"]).mean() - D["drift"].mean()})
    D["year"] = pd.to_datetime(D["day2"]).dt.year
    out["book_by_year"] = D.groupby("year")[["book_return", "coin_return"]].mean()
    return out
