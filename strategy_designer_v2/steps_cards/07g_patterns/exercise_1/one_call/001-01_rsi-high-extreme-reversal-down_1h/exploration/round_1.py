def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            lc = np.log(b["close"].astype(float))
            b["r1"] = lc.diff()
            b["f12"] = lc.shift(-12) - lc
            b["f12x"] = b["f12"] - b["f12"].mean()
            b["r1n"] = lc.shift(-1) - lc
            b["raw"] = b["debug_info.components.rsi_high.last_history_value"].astype(float)
            b["r12p"] = lc - lc.shift(12)
            b["vol24"] = b["r1"].rolling(24).std()
            b["coin"] = coin; b["win"] = w
            b["hour"] = b["ts"].dt.hour; b["wd"] = b["ts"].dt.weekday
            b["bv"] = b["postRebalance_total_value"].astype(float)
            b["bret"] = np.log(b["bv"]).diff().shift(-1)
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    def agg(g, col="f12x"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_bp": x.mean()*1e4, "t_naive": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    d["raw_dec"] = d.groupby("coin")["raw"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["raw(50-RSI) decile -> fwd12 excess (t naive /sqrt12 for overlap)"] = d.groupby(["raw_dec"]).apply(agg)
    out["raw decile by coin mean_bp"] = d.groupby(["coin","raw_dec"])["f12x"].mean().unstack(0)*1e4
    d["r12_dec"] = d.groupby("coin")["r12p"].transform(lambda s: pd.qcut(s, 10, labels=False, duplicates="drop"))
    out["past12h ret decile -> fwd12 excess"] = d.groupby("r12_dec").apply(agg)
    d["r1_dec"] = d.groupby("coin")["r1"].transform(lambda s: pd.qcut(s, 20, labels=False, duplicates="drop"))
    out["past1h ret ventile -> next1h (bp)"] = d.groupby("r1_dec").apply(lambda g: agg(g,"r1n"))
    d["vol_q"] = d.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["vol24 quintile -> fwd12 excess"] = d.groupby("vol_q").apply(agg)
    out["vol quintile x short active: book next-bar ret bp"] = d.assign(act=d["forecast"]<0).groupby(["vol_q","act"])["bret"].mean().unstack()*1e4
    out["hour -> next1h ret bp by coin"] = d.groupby(["hour","coin"])["r1n"].mean().unstack()*1e4
    out["weekday -> next1h ret bp"] = d.groupby(["wd","coin"])["r1n"].mean().unstack()*1e4
    out["hour t-stat pooled"] = d.groupby("hour").apply(lambda g: agg(g,"r1n"))["t_naive"]
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"]=coin; tr.append(t)
    t = pd.concat(tr, ignore_index=True)
    t["dur_h"] = t["duration_minutes"]/60
    t["dur_b"] = pd.cut(t["dur_h"], [0,1,2,4,8,16,48,1e9])
    out["trades by duration"] = t.groupby("dur_b").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), win=("profit_loss_percent", lambda x:(x>0).mean()))
    t["ef_b"] = pd.qcut(t["entry_forecast"].abs(), 5, duplicates="drop")
    out["trades by |entry forecast|"] = t.groupby("ef_b").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    out["trades summary"] = t.groupby("coin").agg(n=("side","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), comm=("total_commission","mean"), dur_h=("dur_h","median"))
    return out
