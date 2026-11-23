def explore(data):
    import pandas as pd, numpy as np
    out = {}
    dd = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["day"] = pd.to_datetime(d["day"])
            d["coin"] = c; d["win"] = w
            d["yr"] = d["day"].dt.year
            d["vol30"] = d["coin_return"].rolling(30).std()
            d["p1"] = d["coin_return"]
            d["p3"] = d["close"]/d["close"].shift(3)-1
            d["p7"] = d["close"]/d["close"].shift(7)-1
            d["n1"] = d["close"].shift(-1)/d["close"]-1
            d["n2"] = d["close"].shift(-2)/d["close"]-1
            d["n3"] = d["close"].shift(-3)/d["close"]-1
            d["wpos"] = np.arange(len(d))
            dd.append(d)
    D = pd.concat(dd, ignore_index=True)
    def tt(s):
        s = s.dropna(); return pd.Series({"mean_pct": s.mean()*100, "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan, "n": len(s)})
    def study(pcol, h, ncol, key, nq=10):
        E = D[D["wpos"] % h == 0].dropna(subset=[pcol, ncol, "vol30"]).copy()
        # drift: coin mean h-day return on the same non-overlapping grid
        E["x"] = E[ncol] - E.groupby("coin")[ncol].transform("mean")
        E["z"] = E[pcol]/(E["vol30"]*np.sqrt(int(pcol[1:])))
        E["q"] = pd.qcut(E["z"], nq, labels=False)
        out[key+"_by_decile"] = E.groupby("q")["x"].apply(tt).unstack().round(3)
        top = E[E["q"] == nq-1]; bot = E[E["q"] == 0]
        out[key+"_top_by_coin"] = top.groupby("coin")["x"].apply(tt).unstack().round(3)
        out[key+"_top_by_year"] = top.groupby("yr")["x"].apply(tt).unstack().round(3)
        out[key+"_bot_by_coin"] = bot.groupby("coin")["x"].apply(tt).unstack().round(3)
        out[key+"_bot_by_year"] = bot.groupby("yr")["x"].apply(tt).unstack().round(3)
        # graded: spearman-like slope of x on z within top half and bottom half
        out[key+"_corr_z_x_pos_half"] = float(E[E["z"]>0][["z","x"]].corr(method="spearman").iloc[0,1])
        out[key+"_corr_z_x_neg_half"] = float(E[E["z"]<0][["z","x"]].corr(method="spearman").iloc[0,1])
    study("p1", 1, "n1", "d1_after_d1")
    study("p3", 2, "n2", "d2_after_d3")
    study("p7", 3, "n3", "d3_after_d7")
    return out
