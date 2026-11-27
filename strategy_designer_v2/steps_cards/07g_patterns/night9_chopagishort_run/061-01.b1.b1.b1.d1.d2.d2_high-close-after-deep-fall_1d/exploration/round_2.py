def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            cl = (b["close"] - b["low"]) / rng
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            p5 = c / c.shift(5) - 1
            p10 = c / c.shift(10) - 1
            p20 = c / c.shift(20) - 1
            p60 = c / c.shift(60) - 1
            vol20 = r1.rolling(20).std()
            vs = (p20 / (vol20 * np.sqrt(20)))
            fwd5 = c.shift(-5) / c - 1
            fwd2 = c.shift(-2) / c - 1
            fwd10 = c.shift(-10) / c - 1
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, day=ts[i].normalize(), fwd=fwd5[i], fwd2=fwd2[i], fwd10=fwd10[i],
                                 cl=cl[i], p5=p5[i], p10=p10[i], p20=p20[i], p60=p60[i], vs=vs[i],
                                 r1=r1[i], yr=ts[i].year, alloc=b["postRebalance_current_allocation"][i]))
    d = pd.DataFrame(rows)
    for f in ["fwd", "fwd2", "fwd10"]:
        d["u_" + f] = d[f] - d["coin"].map(d.groupby("coin")[f].mean())
    def pooled(g, col="u_fwd"):
        x = g[[col, "day"]].dropna()
        n = len(x)
        if n < 5:
            return pd.Series(dict(n=n, days=np.nan, mean=np.nan, t=np.nan))
        m = x[col].mean()
        s = (x[col] - m).groupby(x["day"]).sum()
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / n
        return pd.Series(dict(n=n, days=D, mean=m, t=m / se))
    out = {}
    out["p20_quint"] = d.groupby(pd.qcut(d["p20"], 5, labels=False)).apply(pooled)
    out["vs_quint"] = d.groupby(pd.qcut(d["vs"], 5, labels=False)).apply(pooled)
    out["vs_quint_by_year_top_bottom"] = d.assign(q=pd.qcut(d["vs"], 5, labels=False)).query("q in [0,4]").groupby(["q", "yr"]).apply(pooled)
    d["trend"] = pd.cut(d["p60"], [-10, -0.1, 0.1, 100], labels=["fall", "chop", "rise"])
    out["vs_quint_by_trend"] = d.assign(q=pd.qcut(d["vs"], 3, labels=False)).groupby(["trend", "q"]).apply(pooled)
    hc = d[d["cl"] >= 0.8]
    out["hc_by_p20_tercile"] = hc.groupby(pd.qcut(hc["p20"], 3, labels=False)).apply(pooled)
    out["hc_by_p20_tercile_fwd2"] = hc.groupby(pd.qcut(hc["p20"], 3, labels=False)).apply(lambda g: pooled(g, "u_fwd2"))
    out["hc_by_p20_tercile_fwd10"] = hc.groupby(pd.qcut(hc["p20"], 3, labels=False)).apply(lambda g: pooled(g, "u_fwd10"))
    hcl = hc[hc["p20"] < hc["p20"].quantile(1/3)]
    out["hc_lowp20_by_year"] = hcl.groupby("yr").apply(pooled)
    out["hc_lowp20_by_trend"] = hcl.groupby("trend").apply(pooled)
    nhc = d[d["cl"] < 0.8]
    out["nonhc_by_p20_tercile"] = nhc.groupby(pd.qcut(nhc["p20"], 3, labels=False)).apply(pooled)
    out["by_r1_quint_pooled"] = d.groupby(pd.qcut(d["r1"], 5, labels=False)).apply(pooled)
    out["by_weekday_pooled"] = d.groupby(pd.to_datetime(d["day"]).dt.dayofweek).apply(pooled)
    out["p10_quint"] = d.groupby(pd.qcut(d["p10"], 5, labels=False)).apply(pooled)
    # book: daily mean across coins, top/bottom days context
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; br.append(x)
    br = pd.concat(br)
    daily = br.groupby(["w", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean")).dropna()
    out["book_corr_with_coins"] = float(daily["book"].corr(daily["coin"]))
    q = daily["book"].quantile([0.02, 0.98])
    out["coins_on_book_worst2pct"] = float(daily.loc[daily["book"] <= q.iloc[0], "coin"].mean())
    out["coins_on_book_best2pct"] = float(daily.loc[daily["book"] >= q.iloc[1], "coin"].mean())
    return out
