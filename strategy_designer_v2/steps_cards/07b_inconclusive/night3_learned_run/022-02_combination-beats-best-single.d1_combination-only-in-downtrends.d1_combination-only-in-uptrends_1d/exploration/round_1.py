def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, wn=int(w[1:]), year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 reg=b["regime"].iloc[i],
                                 comb=b.get("debug_info.components.combined.post_pipeline_value", pd.Series([np.nan]*n)).iloc[i],
                                 best=b.get("debug_info.components.best.post_pipeline_value", pd.Series([np.nan]*n)).iloc[i],
                                 r90=b.get("debug_info.components.ret90.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                                 fc=b["forecast"].iloc[i],
                                 ret=c[i+H]/c[i]-1))
    df = pd.DataFrame(rows)
    df["mu"] = df.groupby("coin")["ret"].transform("mean")
    df["ex"] = df["ret"] - df["mu"]
    t = df[(df.reg == "trending")].dropna(subset=["comb", "best", "ex"]).copy()
    t["sc"] = t["comb"] / t["comb"].std()
    t["sb"] = t["best"] / t["best"].std()
    t["dc"] = t["sc"] * t["ex"]
    t["db"] = t["sb"] * t["ex"]
    t["d"] = t["dc"] - t["db"]
    def agg(g):
        out = {}
        for k in ["d", "dc", "db"]:
            x = g[k]
            out[k+"_mean"] = x.mean()
            out[k+"_t"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        out["corr_comb"] = g["sc"].corr(g["ex"])
        out["corr_best"] = g["sb"].corr(g["ex"])
        out["corr_cb"] = g["sc"].corr(g["sb"])
        return pd.Series(out)
    res = {}
    res["all"] = agg(t).to_frame().T
    res["by_coin"] = t.groupby("coin").apply(agg)
    res["by_year"] = t.groupby("year").apply(agg)
    t["r90q"] = pd.qcut(t["r90"], 5, labels=False)
    res["by_r90q"] = t.groupby("r90q").apply(agg)
    res["r90q_mean"] = t.groupby("r90q")["r90"].mean()
    t["side"] = np.sign(t["comb"])
    res["by_comb_side"] = t.groupby("side").apply(agg)
    t["cq"] = pd.qcut(t["comb"], 5, labels=False)
    res["ex_by_comb_q"] = t.groupby("cq").agg(ex=("ex", "mean"), n=("ex", "size"), comb=("comb", "mean"))
    t["bq"] = pd.qcut(t["best"], 5, labels=False)
    res["ex_by_best_q"] = t.groupby("bq").agg(ex=("ex", "mean"), n=("ex", "size"), best=("best", "mean"))
    # ret90 alone as a predictor in trending
    res["ex_by_r90q"] = t.groupby("r90q").agg(ex=("ex", "mean"), ret=("ret", "mean"), n=("ex", "size"))
    # non trending: ex and ret
    nt = df[df.reg != "trending"]
    res["nontrend"] = pd.Series({"n": len(nt), "ex": nt.ex.mean(), "ret": nt.ret.mean(), "n_tr": len(t), "ex_tr": t.ex.mean()})
    return res
