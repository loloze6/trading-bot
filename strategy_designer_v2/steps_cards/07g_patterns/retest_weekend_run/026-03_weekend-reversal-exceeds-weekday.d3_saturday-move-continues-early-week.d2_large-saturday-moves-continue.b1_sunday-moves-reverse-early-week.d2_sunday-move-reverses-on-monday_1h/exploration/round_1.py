def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; hrs = []; trd = []; held = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","close","postRebalance_current_allocation"]].copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            b["r1"] = b["close"].pct_change()
            b["hour"] = b["ts"].dt.hour
            hrs.append(b[["hour","r1"]].assign(coin=coin))
            held.append(pd.DataFrame({"coin":[coin],"share_bars_held":[(b["postRebalance_current_allocation"].abs()>1e-6).mean()]}))
            b["date"] = b["ts"].dt.floor("D")
            g = b.groupby("date").agg(close=("close","last"), lasthr=("hour","last"),
                                      hv=("r1", "std"))
            g = g[g["lasthr"]==23].copy()
            g = g.asfreq("D") if len(g) else g
            g["ret"] = g["close"].pct_change()
            g["usual"] = g["ret"].abs().rolling(30, min_periods=20).mean().shift(1)
            g["z"] = g["ret"]/g["usual"]
            g["n1"] = g["ret"].shift(-1)
            g["n2"] = g["close"].shift(-2)/g["close"]-1
            g["vol30"] = g["ret"].rolling(30, min_periods=20).std()
            g["wd"] = g.index.dayofweek
            g["year"] = g.index.year
            g["coin"] = coin; g["win"] = w
            rows.append(g.dropna(subset=["z","n1"]))
        for w, t in data["trades"][coin].items():
            if len(t):
                trd.append(t.assign(coin=coin))
    d = pd.concat(rows)
    mu = d.groupby("coin")["n1"].transform("mean")
    d["x1"] = -np.sign(d["z"])*(d["n1"]-mu)
    d["zx1"] = -d["z"]*(d["n1"]-mu)/d["usual"]
    out = {}
    def tt(s):
        s = s.dropna(); return pd.Series({"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))),"n":len(s)})
    out["by_weekday_signed_next_day_reversal"] = d.groupby("wd")["x1"].apply(tt).unstack()
    out["by_weekday_graded_reversal_z_x_next"] = d.groupby("wd")["zx1"].apply(tt).unstack()
    d["zq"] = d.groupby("coin")["z"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["all_days_next_ret_by_z_quintile"] = d.groupby("zq")["n1"].apply(tt).unstack()
    big = d[d["z"].abs()>2]
    out["big_moves_abs_z_gt2_by_weekday"] = big.groupby("wd")["x1"].apply(tt).unstack()
    d["vq"] = d.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out["reversal_by_vol_tercile"] = d.groupby("vq")["x1"].apply(tt).unstack()
    out["reversal_by_coin"] = d.groupby("coin")["x1"].apply(tt).unstack()
    out["reversal_by_year"] = d.groupby("year")["x1"].apply(tt).unstack()
    h = pd.concat(hrs).dropna()
    out["hourly_mean_ret_by_hour"] = h.groupby("hour")["r1"].apply(tt).unstack()
    T = pd.concat(trd)
    T["dur_h"] = T["duration_minutes"]/60
    out["trades"] = pd.Series({"n":len(T),"dur_h_mean":T["dur_h"].mean(),"dur_h_median":T["dur_h"].median(),
        "net_mean":T["net_profit_loss_percent"].mean(),"gross_mean":T["profit_loss_percent"].mean(),
        "win_share":(T["net_profit_loss_percent"]>0).mean(),"share_long":(T["side"]=="LONG").mean()})
    out["trades_by_side"] = T.groupby("side")[["profit_loss_percent","net_profit_loss_percent","dur_h"]].mean()
    out["held_share"] = pd.concat(held).groupby("coin").mean()
    return out
