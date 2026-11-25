def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            d = pd.DataFrame()
            d["coin"] = coin; d["win"] = w
            ts = pd.to_datetime(b["timestamp"])
            d["day"] = ts.dt.floor("D").values
            d["wd"] = ts.dt.weekday.values
            d["year"] = ts.dt.year.values
            c, h, l, o = b["close"], b["high"], b["low"], b["open"]
            rng = h - l
            d["clv"] = ((h - c) / rng.replace(0, np.nan)).values  # 1 = close at low
            d["rmult"] = (rng / rng.shift(1).rolling(20).mean()).values
            d["r1"] = (c / c.shift(1) - 1).values
            d["r5"] = (c / c.shift(5) - 1).values
            d["r20"] = (c / c.shift(20) - 1).values
            d["r60"] = (c / c.shift(60) - 1).values
            d["vol20"] = (np.log(c).diff().rolling(20).std()).values
            d["vol60"] = (np.log(c).diff().rolling(60).std()).values
            d["low30"] = (c <= l.rolling(30).min()).astype(float).values
            d["dist30"] = (c / c.rolling(30).max() - 1).values
            d["gap"] = (o / c.shift(1) - 1).values
            d["body"] = ((c - o) / rng.replace(0, np.nan)).values
            d["fc"] = b["forecast"].values
            d["alloc"] = b["postRebalance_current_allocation"].values
            d["fwd1"] = (c.shift(-1) / c - 1).values
            d["fwd3"] = (c.shift(-3) / c - 1).values
            d["pos"] = np.arange(len(b))
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["fwd1"].mean()
    D["ex1"] = D["fwd1"] - D["coin"].map(drift)
    drift3 = D[D.pos % 3 == 0].groupby("coin")["fwd3"].mean()
    D["ex3"] = D["fwd3"] - D["coin"].map(drift3)

    def tq(col, q=5, y="ex1", sub=None):
        X = D if sub is None else sub
        X = X.dropna(subset=[col, y]).copy()
        X["g"] = X.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        out = []
        for g, G in X.groupby("g"):
            dm = G.groupby("day")[y].mean()
            out.append({"q": g, "n": len(G), "days": len(dm), "mean%": 100*dm.mean(),
                        "t": dm.mean()/(dm.std(ddof=1)/np.sqrt(len(dm)))})
        return pd.DataFrame(out).round(3)

    def hl(col, q=5, y="ex1", sub=None):
        X = D if sub is None else sub
        X = X.dropna(subset=[col, y]).copy()
        X["g"] = X.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        a = X[X.g == q-1].groupby("day")[y].mean(); bb = X[X.g == 0].groupby("day")[y].mean()
        t = stats.ttest_ind(a, bb, equal_var=False).statistic
        return 100*(a.mean()-bb.mean()), t
    res = {}
    res["fc_q5"] = tq("fc")
    res["clv_q5"] = tq("clv")
    res["rmult_q5"] = tq("rmult")
    res["r1_q5"] = tq("r1")
    summ = []
    for col in ["fc","clv","rmult","r1","r5","r20","r60","vol20","vol60","dist30","gap","body"]:
        for y in ["ex1","ex3"]:
            sub = None if y == "ex1" else D[D.pos % 3 == 0]
            m, t = hl(col, 5, y, sub)
            summ.append({"col": col, "y": y, "top-bot%": round(m,3), "t": round(t,2)})
    res["summary_top_minus_bottom"] = pd.DataFrame(summ)
    res["r20_q5_ex3"] = tq("r20", 5, "ex3", D[D.pos % 3 == 0])
    res["r5_q5_ex3"] = tq("r5", 5, "ex3", D[D.pos % 3 == 0])
    # brief's condition
    dec = D[(D.r20 < 0)]
    dec = dec.assign(hv=dec.groupby("coin")["vol20"].transform(lambda s: s > s.median()))
    g = dec[dec.hv]
    a = g[g.low30 == 1].groupby("day")["ex1"].mean(); bb = g[g.low30 == 0].groupby("day")["ex1"].mean()
    res["brief_low30_in_volatile_decline_ex1"] = pd.DataFrame({"n_days":[len(a),len(bb)], "mean%":[100*a.mean(),100*bb.mean()],
        "welch_t":[stats.ttest_ind(a,bb,equal_var=False).statistic, np.nan]}, index=["low30","other"]).round(3)
    wd = D.groupby(["wd"]).apply(lambda G: pd.Series({"mean%":100*G.groupby("day")["ex1"].mean().mean(),
        "t": (lambda s: s.mean()/(s.std()/np.sqrt(len(s))))(G.groupby("day")["ex1"].mean())}))
    res["weekday_ex1"] = wd.round(3)
    res["year_fc_corr"] = D.dropna(subset=["fc","ex1"]).groupby("year").apply(lambda G: G["fc"].corr(G["ex1"], method="spearman")).round(3)
    res["coin_fc_corr"] = D.dropna(subset=["fc","ex1"]).groupby("coin").apply(lambda G: G["fc"].corr(G["ex1"], method="spearman")).round(3)
    res["alloc_mean"] = float(D["alloc"].mean())
    return res
