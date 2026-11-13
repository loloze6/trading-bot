def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            lc = np.log(b["close"].astype(float))
            b["r1"] = lc.diff()
            b["f1"] = lc.shift(-1) - lc
            b["f12"] = lc.shift(-12) - lc
            b["f24"] = lc.shift(-24) - lc
            b["p12"] = lc - lc.shift(12)
            b["vol24"] = b["r1"].rolling(24).std()
            b["vol24rank"] = b["vol24"].rolling(24*30, min_periods=24*5).rank(pct=True)
            b["rsi"] = 50 - b["debug_info.components.rsi_high.last_history_value"].astype(float)
            b["z"] = b["r1"] / b["r1"].rolling(24*7, min_periods=48).std().shift(1)
            b["coin"] = coin; b["win"] = w
            b["hour"] = b["ts"].dt.hour; b["wd"] = b["ts"].dt.weekday
            b["pos"] = b["postRebalance_current_allocation"].astype(float)
            v = b["postRebalance_total_value"].astype(float)
            b["bookr"] = np.log(v).shift(-1) - np.log(v)
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)

    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_bp": 1e4*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})

    # RSI buckets full range, f12 (t approx: divide by sqrt(12) for overlap)
    d["rsib"] = pd.cut(d["rsi"], [0,20,30,40,50,60,70,80,100])
    t = d.groupby(["rsib"]).apply(lambda g: summ(g, "f12"))
    t["t_adj"] = t["t"]/np.sqrt(12)
    out["f12_by_rsi_pooled"] = t
    t2 = d.groupby(["coin","rsib"]).apply(lambda g: summ(g, "f12"))
    t2["t_adj"] = t2["t"]/np.sqrt(12)
    out["f12_by_rsi_coin"] = t2
    # after large 1h moves
    d["zb"] = pd.cut(d["z"], [-np.inf,-4,-3,-2,2,3,4,np.inf])
    a = d.groupby("zb").apply(lambda g: pd.concat([summ(g,"f1").add_prefix("f1_"), summ(g,"f12").add_prefix("f12_")]))
    out["after_shock_z"] = a
    # by hour
    h = d.groupby("hour").apply(lambda g: summ(g, "f1"))
    out["f1_by_hour"] = h
    out["f1_by_weekday"] = d.groupby("wd").apply(lambda g: summ(g, "f1"))
    # vol regime
    d["vb"] = pd.qcut(d["vol24rank"], 3, labels=["lo","mid","hi"])
    vv = d.groupby(["vb"]).apply(lambda g: summ(g,"f12"))
    vv["t_adj"] = vv["t"]/np.sqrt(12)
    out["f12_by_volrank"] = vv
    # high RSI in vol regimes
    hi = d[d["rsi"]>70]
    hv = hi.groupby("vb").apply(lambda g: summ(g,"f12")); hv["t_adj"]=hv["t"]/np.sqrt(12)
    out["f12_rsi70_by_vol"] = hv
    # book: gross vs net
    tr = []
    for coin, wins in data["trades"].items():
        for w, t_ in wins.items():
            t_ = t_.copy(); t_["coin"]=coin; t_["win"]=w; tr.append(t_)
    tr = pd.concat(tr, ignore_index=True)
    out["trades"] = tr.groupby("coin").agg(n=("side","size"), gross_mean=("profit_loss_percent","mean"),
        net_mean=("net_profit_loss_percent","mean"), win=("net_profit_loss_percent", lambda x:(x>0).mean()),
        dur_med=("duration_minutes","median"))
    out["book_by_window"] = d.groupby(["coin","win"])["bookr"].sum().unstack()
    out["coin_by_window"] = d.groupby(["coin","win"])["r1"].sum().unstack()
    # trend context: high RSI with prior 12h move tercile
    hi = d[d["rsi"]>70].copy()
    out["rsi70_count_share"] = float(len(hi)/len(d))
    return out
