def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins = list(data["bars"].keys())
    rows = []
    for h in [1,3,7,14]:
        for c in coins:
            for w, b in data["bars"][c].items():
                cl = b["close"].values
                s = b["debug_info.components.rsi_age.last_history_value"].values
                f = b["forecast"].values
                for i in range(0, len(cl)-h, h):
                    rows.append((h, c, w, s[i], f[i], cl[i+h]/cl[i]-1))
    R = pd.DataFrame(rows, columns=["h","coin","w","streak","fc","r"]).dropna()
    R["ex"] = R["r"] - R.groupby(["h","coin"])["r"].transform("mean")
    tab = []
    for (h), g in R.groupby("h"):
        on = g[g.streak > 0]
        sl = stats.linregress(on["streak"], on["ex"])
        sl2 = stats.linregress(g["fc"], g["ex"])
        tab.append((h, len(g), len(on), sl.slope, sl.slope/sl.stderr, sl2.slope/sl2.stderr))
    out["slopes_by_h"] = pd.DataFrame(tab, columns=["h","n","n_on","slope_streak_on","t_streak_on","t_fc_all"])
    R["sb"] = pd.cut(R["streak"], [-1e9,0,5,10,20,40,1e9])
    g7 = R[R.h==7]
    out["h7_by_streak"] = g7.groupby("sb")["ex"].agg(["mean","count", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    g14 = R[R.h==14]
    out["h14_by_streak"] = g14.groupby("sb")["ex"].agg(["mean","count", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # per coin on vs off at h=3,7
    t2 = []
    for (h, c), g in R[R.h.isin([1,3,7])].groupby(["h","coin"]):
        a = g[g.streak>0]["ex"]; bb = g[g.streak<=0]["ex"]
        t2.append((h, c, a.mean(), bb.mean(), len(a), len(bb), stats.ttest_ind(a,bb,equal_var=False).statistic))
    out["on_off_coin"] = pd.DataFrame(t2, columns=["h","coin","on","off","n_on","n_off","t"])
    # below-50 side: does streak depth below predict lower returns (h=7)
    off = g7[g7.streak < 0]
    if len(off) > 10:
        sl = stats.linregress(off["streak"], off["ex"])
        out["h7_below_slope"] = pd.Series({"n": len(off), "slope": sl.slope, "t": sl.slope/sl.stderr})
    # book daily: share of gain in the best 5% of days
    d = []
    for c in coins:
        for w, x in data["days"][c].items():
            d.append(x.assign(coin=c, w=w))
    D = pd.concat(d)
    bk = D.groupby(["w","day"])["book_return"].mean().dropna()
    srt = bk.sort_values(ascending=False)
    k = int(len(srt)*0.05)
    out["book_conc"] = pd.Series({"n_days": len(bk), "mean": bk.mean(), "sum": bk.sum(), "top5pct_sum": srt.head(k).sum(), "bottom5pct_sum": srt.tail(k).sum(), "t_mean": bk.mean()/(bk.std()/np.sqrt(len(bk)))})
    return out
