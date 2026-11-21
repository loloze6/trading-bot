def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 26
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"]; lo = b["low"]
            n = len(b)
            hh52 = hi.rolling(52).max(); ll52 = lo.rolling(52).min()
            mid52 = (hh52 + ll52) / 2
            hh26 = hi.rolling(26).max(); ll26 = lo.rolling(26).min()
            mid26 = (hh26 + ll26) / 2
            pos52 = (b["close"] - mid52) / b["close"]
            pos26 = (b["close"] - mid26) / b["close"]
            r26p = b["close"] / b["close"].shift(26) - 1
            rv = np.log(b["close"]).diff().rolling(20).std()
            fc = b["forecast"].fillna(0)
            alloc = b["postRebalance_current_allocation"].fillna(0)
            cross = (fc > 0) & (fc.shift(1).fillna(0) <= 0)
            for i in range(0, n - H, H):
                rows.append({"coin": c, "w": w, "fr": cl[i + H] / cl[i] - 1, "pos52": pos52.iloc[i], "pos26": pos26.iloc[i],
                             "r26p": r26p.iloc[i], "rv": rv.iloc[i], "inv": abs(alloc.iloc[i]) > 1e-6})
            # cross cases: path after cross
            for i in np.where(cross.values)[0]:
                rec = {"coin": c, "w": w, "kind": "cross"}
                for k in [5, 13, 26, 39]:
                    rec["f%d" % k] = cl[i + k] / cl[i] - 1 if i + k < n else np.nan
                rec["r26p"] = r26p.iloc[i]; rec["pos52"] = pos52.iloc[i]; rec["rv"] = rv.iloc[i]
                rows.append(rec)
    R = pd.DataFrame(rows)
    G = R[R.get("kind").isna()].copy() if "kind" in R else R.copy()
    drift = G.groupby("coin")["fr"].transform("mean")
    G["un"] = G["fr"] - drift
    res = {}
    for f in ["pos52", "pos26", "r26p", "rv"]:
        s = G.dropna(subset=[f, "un"])
        g = pd.qcut(s[f].rank(method="first"), 5, labels=False)
        m = s.groupby(g)["un"].agg(["mean", "count"])
        hi_ = s.un[g == 4]; lo_ = s.un[g == 0]
        res[f] = dict(zip(["q%d" % k for k in range(5)], m["mean"].round(4))) | {"n": len(s), "t_hi_lo": stats.ttest_ind(hi_, lo_, equal_var=False)[0], "rho": stats.spearmanr(s[f], s.un)[0]}
    out["grid_unusual_by_quintile"] = pd.DataFrame(res).T.round(4)
    # above vs below midpoint
    s = G.dropna(subset=["pos52"])
    out["above_vs_below_mid52"] = pd.DataFrame({"above": s[s.pos52 > 0].un.describe(), "below": s[s.pos52 <= 0].un.describe()}).round(4)
    out["invested_vs_not_grid"] = G.groupby("inv")["un"].agg(["mean", "count"]).round(4)
    C = R[R.get("kind") == "cross"].copy()
    out["cross_path"] = C[["f5", "f13", "f26", "f39"]].agg(["mean", "median", "count"]).round(4)
    for f in ["r26p", "pos52", "rv"]:
        s = C.dropna(subset=[f, "f26"])
        g = pd.qcut(s[f].rank(method="first"), 3, labels=["lo", "mid", "hi"])
        out["cross_f26_by_" + f] = s.groupby(g)["f26"].agg(["mean", "median", "count"]).round(4)
    # drawdown composition: worst 5% book days, by coin, and invested state
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            rows.append(d.assign(coin=c, w=w))
    D = pd.concat(rows).dropna(subset=["book_return"])
    out["book_mean_by_coin"] = D.groupby("coin")["book_return"].agg(["mean", "std"]).round(5)
    q = D.book_return.quantile(0.02)
    out["worst2pct_days_by_coin"] = D[D.book_return < q].groupby("coin").size()
    return out
