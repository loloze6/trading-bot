def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 10
    # coin mean 10-day returns & std over all windows (non-overlapping grid)
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            for i in range(0, n - H, H):
                r = c[i+H]/c[i]-1
                # past returns
                p10 = c[i]/c[i-10]-1 if i>=10 else np.nan
                p30 = c[i]/c[i-30]-1 if i>=30 else np.nan
                p90 = c[i]/c[i-90]-1 if i>=90 else np.nan
                lr = np.diff(np.log(c[max(0,i-20):i+1]))
                vol20 = lr.std() if len(lr)>=10 else np.nan
                hi = b["high"].values[max(0,i-90):i+1].max()
                lo = b["low"].values[max(0,i-90):i+1].min()
                pos = (c[i]-lo)/(hi-lo) if hi>lo else np.nan
                rows.append(dict(coin=coin, w=w, r=r, f=b["forecast"].iloc[i],
                                 reg=b["regime"].iloc[i], p10=p10, p30=p30, p90=p90,
                                 vol20=vol20, pos=pos,
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek))
    g = pd.DataFrame(rows)
    g["mu"] = g.groupby("coin")["r"].transform("mean")
    g["sd"] = g.groupby("coin")["r"].transform("std")
    g["ex"] = (g["r"]-g["mu"])/g["sd"]
    def tab(col, q=5):
        d = g.dropna(subset=[col]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        t = d.groupby("b")["ex"].agg(["mean","count","std"])
        t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
        t["raw_r"] = d.groupby("b")["r"].mean()
        return t
    for col in ["p10","p30","p90","vol20","pos"]:
        out["ex10_by_"+col+"_quintile"] = tab(col)
    out["ex10_by_weekday"] = g.groupby("wd")["ex"].agg(["mean","count"])
    out["ex10_by_regime"] = g.groupby("reg")["ex"].agg(["mean","count"])
    # book by regime
    br = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            nxt = b["close"].shift(-1)/b["close"]-1
            pos = b["postRebalance_current_allocation"]
            br.append(pd.DataFrame({"coin":coin,"reg":b["regime"],"gain":pos*nxt,"pos":pos,
                                    "side":np.sign(pos)}))
    br = pd.concat(br).dropna()
    t = br.groupby(["reg","side"])["gain"].agg(["mean","count","sum"])
    out["bar_gain_by_regime_side"] = t
    out["bar_gain_by_coin_side"] = br.groupby(["coin","side"])["gain"].agg(["mean","count"])
    # trades
    tr = pd.concat([df.assign(coin=c) for c, ws in data["trades"].items() for df in ws.values() if len(df)])
    out["trades_by_side"] = tr.groupby(["side","entry_regime"])["net_profit_loss_percent"].agg(["mean","median","count"])
    return out
