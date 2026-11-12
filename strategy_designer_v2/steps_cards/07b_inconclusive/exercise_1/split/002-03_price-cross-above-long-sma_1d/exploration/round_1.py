def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        rets = []
        for w, df in wins.items():
            r = df["close"].pct_change().dropna()
            rets.append(r)
        mu = pd.concat(rets).mean()
        for w, df in wins.items():
            d = df[["timestamp","close","forecast","postRebalance_current_allocation"]].copy().reset_index(drop=True)
            d["fwd"] = d["close"].shift(-20)/d["close"] - 1
            d["exc"] = d["fwd"] - 20*mu
            d["coin"] = coin; d["win"] = w
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            d["i"] = np.arange(len(d))
            d["dist"] = df["debug_info.components.above_ma.last_history_value"].values
            rows.append(d)
    a = pd.concat(rows).dropna(subset=["fwd"])
    a["alloc"] = a["postRebalance_current_allocation"]
    a["contrib"] = a["alloc"]*a["exc"]
    a["blk"] = a["i"]//20
    def t(x):
        x = x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std(ddof=1)*np.sqrt(len(x)) if len(x)>1 else np.nan})
    blocks = a.groupby(["coin","win","blk"]).agg(c=("contrib","sum"),alloc=("alloc","mean"),year=("year","first"),exc=("exc","mean")).reset_index()
    nb = blocks[blocks["alloc"]!=0]
    out = {}
    out["blocks_by_coin"] = nb.groupby("coin")["c"].apply(t).unstack()
    out["blocks_by_year"] = nb.groupby("year")["c"].apply(t).unstack()
    out["exc_on_vs_off"] = a.groupby(a["forecast"]>0)["exc"].apply(t).unstack()
    on = a[a["forecast"]>0].copy()
    on["fq"] = pd.qcut(on["forecast"].rank(method="first"),5,labels=False)
    g = on.groupby("fq")
    out["by_forecast_quintile"] = pd.DataFrame({"fc_mean":g["forecast"].mean(),"alloc_mean":g["alloc"].mean(),"exc_mean":g["exc"].mean(),"exc_median":g["exc"].median(),"hit":g["exc"].apply(lambda x:(x>0).mean()),"n":g.size()})
    on["dq"] = pd.qcut(on["dist"].rank(method="first"),5,labels=False)
    g = on.groupby("dq")
    out["by_raw_distance_quintile"] = pd.DataFrame({"dist_mean":g["dist"].mean(),"exc_mean":g["exc"].mean(),"exc_median":g["exc"].median(),"hit":g["exc"].apply(lambda x:(x>0).mean()),"n":g.size()})
    out["on_exc_by_coin"] = on.groupby("coin")["exc"].agg(["mean","median",lambda x:(x>0).mean(),"size"])
    out["on_exc_by_year"] = on.groupby("year")["exc"].agg(["mean","median",lambda x:(x>0).mean(),"size"])
    out["contrib_dist"] = nb["c"].describe(percentiles=[.05,.25,.5,.75,.95])
    top = nb["c"].sort_values(ascending=False)
    out["share_top10_blocks_of_sum"] = float(top.head(10).sum()/top.sum())
    return out
