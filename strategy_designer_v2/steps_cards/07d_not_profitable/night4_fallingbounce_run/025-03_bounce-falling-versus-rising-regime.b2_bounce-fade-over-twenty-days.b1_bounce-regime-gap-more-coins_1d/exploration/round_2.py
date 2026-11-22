def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    cases = []
    allfwd = []
    B = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True).copy()
            c = b["close"]
            b["fwd20"] = c.shift(-20)/c - 1
            b["r20"] = c/c.shift(20) - 1
            b["r60"] = c/c.shift(60) - 1
            b["r5"] = c/c.shift(5) - 1
            b["ret_next"] = c.shift(-1)/c - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["ret_next"]
            b["coin"]=coin; b["window"]=w
            b["cell"] = b.index//20
            grid = b.iloc[::20]
            allfwd.append(grid["fwd20"].dropna())
            sig = b[b["forecast"].abs() >= 2]
            first = sig.groupby("cell").head(1)
            cases.append(first)
            B.append(b[["coin","window","pos","gain","ret_next","r20","r5","regime"]])
    drift = pd.concat(allfwd).mean()
    out["drift20"] = round(drift,4)
    C = pd.concat(cases).dropna(subset=["fwd20"])
    C["side"] = np.where(C["forecast"]>0,"long","short")
    C["unusual_dir"] = np.sign(C["forecast"])*(C["fwd20"]-drift)
    def summ(g):
        x = g["unusual_dir"]
        return pd.Series({"n":len(x),"mean_dir":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                          "mean_fwd20":g["fwd20"].mean()})
    out["by_side"] = C.groupby("side").apply(summ).round(4)
    for v in ["r20","r60"]:
        sub = C.dropna(subset=[v]).copy()
        sub["q"] = sub.groupby("side")[v].transform(lambda s: pd.qcut(s,4,labels=False,duplicates="drop"))
        out["by_side_"+v+"_quartile"] = sub.groupby(["side","q"]).apply(lambda g: pd.concat([summ(g), pd.Series({"mean_"+v:g[v].mean()})])).round(4)
    C["fq"] = C.groupby("side")["forecast"].transform(lambda s: pd.qcut(s.abs(),3,labels=False,duplicates="drop"))
    out["by_side_forecast_tercile"] = C.groupby(["side","fq"]).apply(summ).round(4)
    # book drawdown composition: worst book days
    Bb = pd.concat(B).dropna(subset=["gain"])
    Bb["side"] = np.where(Bb["pos"]>0,"long",np.where(Bb["pos"]<0,"short","flat"))
    thr = Bb["gain"].quantile(0.02)
    worst = Bb[Bb["gain"]<=thr]
    out["worst2pct_bars_by_side"] = worst.groupby("side").agg(n=("gain","size"),sum_gain=("gain","sum"),
        mean_coin_ret=("ret_next","mean"),mean_r20=("r20","mean"),mean_r5=("r5","mean")).round(4)
    # short-held bars gain graded by r20 of coin at bar
    s = Bb[Bb["side"]=="short"].dropna(subset=["r20"]).copy()
    s["q"] = pd.qcut(s["r20"],5,labels=False)
    out["short_bars_gain_by_r20_quintile"] = s.groupby("q").agg(n=("gain","size"),mean_gain=("gain","mean"),
        mean_r20=("r20","mean"),mean_coin_next=("ret_next","mean")).round(5)
    return out
