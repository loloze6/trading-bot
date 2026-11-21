def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def grid(h):
        rows = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                c = b["close"].values; f = b["forecast"].values
                s = b["debug_info.components.dist_high.last_history_value"].values if "debug_info.components.dist_high.last_history_value" in b else np.full(len(c), np.nan)
                n = len(c)
                for i in range(0, n - h, h):
                    rows.append((coin, w, int(w[1:]), f[i], s[i], c[i+h]/c[i]-1))
        d = pd.DataFrame(rows, columns=["coin","w","wn","f","raw","r"])
        d["ex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
        d["z"] = d["ex"] / d.groupby("coin")["r"].transform("std")
        return d.dropna(subset=["f","r"])
    def slope_t(d, y="ex"):
        if len(d) < 10 or d["f"].std() == 0: return np.nan
        r = stats.linregress(d["f"], d[y]); return r.slope / r.stderr
    for h in [5, 10, 20]:
        d = grid(h)
        d["wg"] = pd.cut(d["wn"], [0,6,12,18,24], labels=["w1-6","w7-12","w13-18","w19-24"])
        out[f"h{h}_by_coin"] = d.groupby("coin").apply(lambda g: pd.Series({"n":len(g),"slope_t":slope_t(g),"slope_t_z":slope_t(g,"z")}))
        out[f"h{h}_by_wgroup"] = d.groupby("wg").apply(lambda g: pd.Series({"n":len(g),"slope_t":slope_t(g),"slope_t_z":slope_t(g,"z")}))
        noz = d[d.coin!="ZECUSD"]
        w = d.assign(ex=d.ex.clip(d.ex.quantile(.02), d.ex.quantile(.98)))
        d["b"] = pd.qcut(d["f"], 5, labels=False, duplicates="drop")
        out[f"h{h}_summary"] = pd.Series({"n":len(d),"slope_t":slope_t(d),"slope_t_z":slope_t(d,"z"),
            "slope_t_noZEC":slope_t(noz),"slope_t_winsor":slope_t(w),
            "slope_t_f_le_2.7":slope_t(d[d.f<=2.7]),
            "mean_ex_q5":d.loc[d.b==4,"ex"].mean(),"t_q5":stats.ttest_1samp(d.loc[d.b==4,"ex"],0).statistic,
            "median_ex_q5":d.loc[d.b==4,"ex"].median(),
            "mean_ex_q1":d.loc[d.b==0,"ex"].mean(),"t_q1":stats.ttest_1samp(d.loc[d.b==0,"ex"],0).statistic,
            "share_f_eq_-5":(d.f<=-4.999).mean()})
        out[f"h{h}_by_quintile"] = d.groupby("b").agg(n=("ex","size"),mean_ex=("ex","mean"),median_ex=("ex","median"),mean_z=("z","mean"))
    # raw distance at 20d: new high vs not
    d = grid(20)
    d["at_high"] = d["raw"] >= 0
    out["h20_newhigh"] = d.groupby("at_high").agg(n=("ex","size"),mean_ex=("ex","mean"),median_ex=("ex","median"))
    return out
