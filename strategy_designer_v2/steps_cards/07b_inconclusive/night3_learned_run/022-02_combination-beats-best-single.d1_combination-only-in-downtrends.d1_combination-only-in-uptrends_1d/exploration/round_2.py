def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r28 = c / c.shift(28) - 1
            r1 = c / c.shift(1) - 1
            lr = np.log(c).diff()
            vol30 = lr.rolling(30).std()
            hi = c.rolling(60, min_periods=20).max()
            near = c / hi
            r90 = b.get("debug_info.components.ret90.last_history_value", pd.Series([np.nan]*n))
            comb = b.get("debug_info.components.combined.post_pipeline_value", pd.Series([np.nan]*n))
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, reg=b["regime"].iloc[i], r28=r28.iloc[i], rev1=-r1.iloc[i],
                                 vol=-vol30.iloc[i], near=near.iloc[i], r90=r90.iloc[i], comb=comb.iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i],
                                 ret=c.iloc[i+H]/c.iloc[i]-1))
    df = pd.DataFrame(rows)
    df["ex"] = df["ret"] - df.groupby("coin")["ret"].transform("mean")
    t = df[df.reg == "trending"].copy()
    res = {}
    def corrs(g):
        out = {}
        for k in ["r28", "rev1", "vol", "near", "r90", "comb"]:
            gg = g[[k, "ex"]].dropna()
            r = gg[k].corr(gg["ex"]) if len(gg) > 10 else np.nan
            out[k+"_corr"] = r
            out[k+"_t"] = r * np.sqrt((len(gg)-2)/(1-r*r)) if len(gg) > 10 else np.nan
            out[k+"_n"] = len(gg)
        return pd.Series(out)
    res["trend_corrs"] = corrs(t).to_frame().T
    res["nontrend_corrs"] = corrs(df[df.reg != "trending"]).to_frame().T
    t["r90q"] = pd.qcut(t["r90"], 5, labels=False)
    res["trend_corrs_by_r90q"] = t.groupby("r90q").apply(corrs)[["r28_corr","r28_t","rev1_corr","rev1_t","near_corr","near_t","vol_corr","vol_t","comb_corr","comb_t"]]
    t["r28q"] = pd.qcut(t["r28"], 5, labels=False)
    res["ex_by_r28q"] = t.groupby("r28q").agg(ex=("ex","mean"), r28=("r28","mean"), n=("ex","size"))
    t["rq"] = pd.qcut(t["rev1"], 5, labels=False)
    res["ex_by_rev1q"] = t.groupby("rq").agg(ex=("ex","mean"), rev1=("rev1","mean"), n=("ex","size"))
    t["nq"] = pd.qcut(t["near"], 5, labels=False, duplicates="drop")
    res["ex_by_nearq"] = t.groupby("nq").agg(ex=("ex","mean"), near=("near","mean"), n=("ex","size"))
    t["sgn"] = np.sign(t["comb"])
    tt = t.dropna(subset=["comb"])
    x = tt["sgn"] * tt["ex"]
    res["comb_side_excess"] = pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)})
    return res
