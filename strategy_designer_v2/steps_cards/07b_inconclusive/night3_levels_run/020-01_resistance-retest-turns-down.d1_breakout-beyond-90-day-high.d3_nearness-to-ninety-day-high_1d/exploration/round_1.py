def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def grid(h):
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                c = b["close"].values; f = b["forecast"].values
                n = len(c)
                for i in range(0, n - h, h):
                    rows.append((coin, w, int(w[1:]), f[i], c[i+h]/c[i]-1))
        d = pd.DataFrame(rows, columns=["coin","w","wn","f","r"])
        d["ex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
        return d.dropna()
    def slope_t(d):
        if len(d) < 10 or d["f"].std() == 0: return np.nan
        r = stats.linregress(d["f"], d["ex"]); return r.slope / r.stderr
    d = grid(20)
    d["bin"] = pd.qcut(d["f"], 5, labels=False, duplicates="drop")
    out["by_quintile"] = d.groupby("bin").agg(n=("ex","size"), fmin=("f","min"), fmax=("f","max"),
        mean_ex=("ex","mean"), sd=("ex","std"))
    out["by_coin"] = d.groupby("coin").apply(lambda g: pd.Series({"n":len(g),"slope_t":slope_t(g),
        "mean_ex_pos": g.loc[g.f>0,"ex"].mean(), "mean_ex_neg": g.loc[g.f<0,"ex"].mean()}))
    d["wg"] = pd.cut(d["wn"], [0,6,12,18,24], labels=["w1-6","w7-12","w13-18","w19-24"])
    out["by_wgroup"] = d.groupby("wg").apply(lambda g: pd.Series({"n":len(g),"slope_t":slope_t(g),
        "q5_minus_q1": g.loc[g.bin==4,"ex"].mean()-g.loc[g.bin==0,"ex"].mean()}))
    # side split
    pos = d[d.f>0]; neg = d[d.f<0]
    out["sides"] = pd.DataFrame({"n":[len(pos),len(neg)],"slope_t":[slope_t(pos),slope_t(neg)],
        "mean_ex":[pos.ex.mean(),neg.ex.mean()],
        "t_mean":[stats.ttest_1samp(pos.ex,0).statistic, stats.ttest_1samp(neg.ex,0).statistic]},
        index=["f>0","f<0"])
    # spearman and trimmed
    out["spearman"] = pd.Series({"rho": stats.spearmanr(d.f, d.ex).correlation,
        "n": len(d), "slope_t_winsor_ex": slope_t(d.assign(ex=d.ex.clip(d.ex.quantile(.02), d.ex.quantile(.98))))})
    # horizons
    hz = {}
    for h in [5,10,20,40,60]:
        g = grid(h); g["b"] = pd.qcut(g["f"],5,labels=False,duplicates="drop")
        hz[h] = {"n":len(g),"slope_t":slope_t(g),"rho":stats.spearmanr(g.f,g.ex).correlation,
                 "q5_minus_q1":g.loc[g.b==4,"ex"].mean()-g.loc[g.b==0,"ex"].mean(),
                 "t_q5_q1": stats.ttest_ind(g.loc[g.b==4,"ex"],g.loc[g.b==0,"ex"],equal_var=False).statistic}
    out["horizons"] = pd.DataFrame(hz).T
    # variance of ex by quintile vs. forecast's own variance
    out["forecast_desc"] = d["f"].describe()
    return out
