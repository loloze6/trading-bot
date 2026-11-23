def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl)-5, 5)
            allr.append(cl[idx+5]/cl[idx]-1)
        mu5 = np.concatenate(allr).mean() if allr else np.nan
        sd5 = np.concatenate(allr).std(ddof=1)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            s = pd.Series(cl)
            r20 = s.pct_change(20).values
            r60 = s.pct_change(60).values
            hi90 = s.rolling(90, min_periods=30).max().values
            near = cl/hi90
            fc = b["forecast"].fillna(0).values
            a = b["postRebalance_current_allocation"].fillna(0).values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(cl)-5, 5):
                f5 = cl[i+5]/cl[i]-1
                rows.append((c, w, ts[i].year, f5, f5-mu5, (f5-mu5)/sd5, r20[i], r60[i], near[i], fc[i], a[i]))
    df = pd.DataFrame(rows, columns=["coin","w","year","f5","ex5","str5","r20","r60","near","fc","a"])
    d = df.dropna(subset=["r20"]).copy()
    d["q"] = d.groupby("coin")["r20"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    def tt(x): return x.mean()/x.std(ddof=1)*np.sqrt(len(x))
    out["ex5_by_r20_quintile_within_coin"] = d.groupby("q").agg(r20=("r20","mean"), ex5=("ex5","mean"), strength=("str5","mean"), n=("ex5","size"), t=("ex5", tt))
    top_bot = d[d.q==4]["ex5"]; bot = d[d.q==0]["ex5"]
    out["top_minus_bottom_r20"] = pd.Series({"diff": top_bot.mean()-bot.mean(), "welch_t": stats.ttest_ind(top_bot, bot, equal_var=False).statistic})
    # rank corr r20 vs ex5 per coin
    out["spearman_r20_ex5_by_coin"] = d.groupby("coin").apply(lambda g: stats.spearmanr(g["r20"], g["ex5"])[0])
    out["spearman_pooled"] = pd.Series({"r20": stats.spearmanr(d["r20"], d["ex5"])[0], "n": len(d),
        "r60": stats.spearmanr(d.dropna(subset=["r60"])["r60"], d.dropna(subset=["r60"])["ex5"])[0],
        "near": stats.spearmanr(d.dropna(subset=["near"])["near"], d.dropna(subset=["near"])["ex5"])[0]})
    # within r20>0: forecast>0 vs forecast==0
    p = d[d.r20>0]
    g1 = p[p.fc>0]["ex5"]; g0 = p[p.fc<=0]["ex5"]
    out["r20pos_fc_on_vs_off"] = pd.Series({"on_mean": g1.mean(), "on_n": len(g1), "off_mean": g0.mean(), "off_n": len(g0),
        "welch_t": stats.ttest_ind(g1, g0, equal_var=False).statistic})
    # by year, r20 top-vs-bottom
    out["by_year_top_bottom"] = d.groupby("year").apply(lambda g: pd.Series({"top": g[g.q==4]["ex5"].mean(), "bot": g[g.q==0]["ex5"].mean(), "n": len(g)}))
    # r20 graded within r20>0
    p = p.copy(); p["q3"] = pd.qcut(p["r20"].rank(method="first"), 3, labels=False)
    out["r20pos_tercile"] = p.groupby("q3").agg(r20=("r20","mean"), ex5=("ex5","mean"), t=("ex5", tt), n=("ex5","size"))
    return out
