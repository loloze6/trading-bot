def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- daily coin returns: weekday effect, clustered by day, by year, by coin
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dl.append(d)
    D = pd.concat(dl).dropna(subset=["coin_return"])
    D["day"] = pd.to_datetime(D["day"])
    D["wd"] = D["day"].dt.weekday
    D["yr"] = D["day"].dt.year
    D["cun"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    dd = D.groupby(["day"]).agg(cun=("cun", "sum"), n=("cun", "size"), wd=("wd", "first"), yr=("yr", "first")).reset_index()
    res = []
    for k, s in dd.groupby("wd"):
        sub = D[D.wd == k]
        res.append(dict(wd=k, days=len(s), mean=sub["cun"].mean(),
                        t_day=s["cun"].mean() / (s["cun"].std(ddof=1) / np.sqrt(len(s)))))
    out["wd_clustered"] = pd.DataFrame(res).set_index("wd")
    # Saturday and Thursday by year and coin
    for k, nm in [(5, "sat"), (3, "thu")]:
        s = D[D.wd == k]
        o = D[D.wd != k]
        by = pd.DataFrame({"mean_k": s.groupby("yr")["cun"].mean(), "mean_other": o.groupby("yr")["cun"].mean(),
                           "n": s.groupby("yr").size()})
        out[nm + "_by_year"] = by
        out[nm + "_by_coin"] = pd.DataFrame({"mean_k": s.groupby("coin")["cun"].mean(),
                                             "t": s.groupby("coin")["cun"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x)))),
                                             "n": s.groupby("coin").size()})
    # Saturday graded by Friday's return? (weekend reversal / continuation)
    D = D.sort_values(["coin", "w", "day"])
    D["prev"] = D.groupby(["coin", "w"])["coin_return"].shift(1)
    D["prev_wd"] = D.groupby(["coin", "w"])["wd"].shift(1)
    sat = D[(D.wd == 5) & (D.prev_wd == 4)].dropna(subset=["prev"])
    sat["q"] = pd.qcut(sat["prev"].rank(method="first"), 5, labels=False)
    out["sat_by_fri_ret_q"] = sat.groupby("q").agg(n=("cun", "size"), fri=("prev", "mean"), sat_un=("cun", "mean"))
    allp = D.dropna(subset=["prev"]).copy()
    allp["q"] = allp.groupby("coin")["prev"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["next_day_by_prev_q"] = allp.groupby("q").agg(n=("cun", "size"), prev=("prev", "mean"), next_un=("cun", "mean"))

    # ---- 10-day grid: distance to 30-day high, clustered by day, by year halves and coin
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            dh = c / c.rolling(30, min_periods=30).max() - 1
            dh60 = c / c.rolling(60, min_periods=60).max() - 1
            p10 = c / c.shift(10) - 1
            for i in range(0, len(c) - H, H):
                rows.append(dict(coin=coin, ts=pd.Timestamp(b["timestamp"].iloc[i]), fwd=c.iloc[i + H] / c.iloc[i] - 1,
                                 dh=dh.iloc[i], dh60=dh60.iloc[i], p10=p10.iloc[i]))
    g = pd.DataFrame(rows)
    g["un"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["str"] = g["un"] / g.groupby("coin")["fwd"].transform("std")
    g["day"] = g["ts"].dt.floor("D"); g["yr"] = g["ts"].dt.year
    for col in ["dh", "dh60"]:
        d = g.dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        d["top"] = (d["q"] == 4).astype(int)
        # day-clustered t of top-minus-rest via per-day sums of (un*(top) - ) : simpler: top cases clustered
        tp = d[d.top == 1].groupby("day")["un"].sum()
        out[col + "_top_clustered"] = pd.DataFrame({"mean_un": [d[d.top == 1]["un"].mean()], "days": [len(tp)],
                                                    "t_day": [tp.mean() / (tp.std() / np.sqrt(len(tp)))],
                                                    "strength": [d[d.top == 1]["str"].mean()]})
        out[col + "_top_by_year"] = d.groupby("yr").apply(lambda s: pd.Series({
            "top": s[s.top == 1]["un"].mean(), "rest": s[s.top == 0]["un"].mean(), "n_top": (s.top == 1).sum()}))
        out[col + "_top_by_coin"] = d.groupby("coin").apply(lambda s: pd.Series({
            "top": s[s.top == 1]["un"].mean(), "rest": s[s.top == 0]["un"].mean(), "n_top": (s.top == 1).sum()}))
        out[col + "_q"] = d.groupby("q").agg(n=("un", "size"), mean_un=("un", "mean"), feat=(col, "mean"))
    # ---- book: around largest days
    bk = D.groupby("day")["book_return"].mean().dropna()
    out["book_top_days"] = pd.DataFrame({"n_active": [(bk.abs() > 1e-9).sum()],
                                          "share_gain_top5": [bk.nlargest(5).sum() / bk.sum()]})
    return out
