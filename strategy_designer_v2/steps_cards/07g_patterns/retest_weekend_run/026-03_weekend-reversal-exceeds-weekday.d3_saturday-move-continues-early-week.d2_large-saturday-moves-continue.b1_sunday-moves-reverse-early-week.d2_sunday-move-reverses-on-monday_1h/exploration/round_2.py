def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; hrs = []; bk = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","close","postRebalance_current_allocation"]].copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            b["r1"] = b["close"].pct_change()
            b["hour"] = b["ts"].dt.hour
            b["wd"] = b["ts"].dt.dayofweek
            b["year"] = b["ts"].dt.year
            b["r24p"] = b["close"]/b["close"].shift(24)-1
            b["sd720"] = b["r1"].rolling(720, min_periods=500).std()
            b["z24"] = b["r24p"]/(b["sd720"]*np.sqrt(24))
            hrs.append(b[["hour","wd","year","r1","z24","sd720"]].assign(coin=coin))
            a = b["postRebalance_current_allocation"]
            g = a*(b["close"].shift(-1)/b["close"]-1)
            bk.append(pd.DataFrame({"gain":g,"side":np.sign(a)}).assign(coin=coin))
            b["date"] = b["ts"].dt.floor("D")
            dd = b.groupby("date").agg(close=("close","last"), lasthr=("hour","last"))
            dd = dd[dd["lasthr"]==23].asfreq("D")
            dd["ret"] = dd["close"].pct_change()
            dd["usual"] = dd["ret"].abs().rolling(30, min_periods=20).mean().shift(1)
            dd["z"] = dd["ret"]/dd["usual"]
            dd["n1"] = dd["ret"].shift(-1)
            dd["vol30"] = dd["ret"].rolling(30, min_periods=20).std()
            dd["wd"] = dd.index.dayofweek; dd["year"] = dd.index.year; dd["coin"] = coin
            rows.append(dd.dropna(subset=["z","n1","vol30"]))
    d = pd.concat(rows)
    mu = d.groupby("coin")["n1"].transform("mean")
    d["ex"] = d["n1"]-mu
    def tt(s):
        s = s.dropna(); return pd.Series({"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))),"n":len(s)})
    out = {}
    d["side"] = np.where(d["z"]<0,"down","up")
    d["x"] = -np.sign(d["z"])*d["ex"]
    out["reversal_by_weekday_and_side"] = d.groupby(["wd","side"])["x"].apply(tt).unstack()
    d["zq"] = d.groupby("coin")["z"].transform(lambda s: pd.qcut(s,10,labels=False,duplicates="drop"))
    out["next_day_excess_by_z_decile"] = d.groupby("zq")["ex"].apply(tt).unstack()
    d["vq"] = d.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    dn = d[d["z"]<0]
    out["down_days_graded_negz_x_ex_by_vol"] = dn.assign(g=-dn["z"]*dn["ex"]).groupby("vq")["g"].apply(tt).unstack()
    out["down_days_excess_by_vol_and_zq"] = dn.groupby(["vq", pd.qcut(dn["z"],3,labels=False)])["ex"].mean().unstack()
    out["down_days_reversal_by_year"] = dn.groupby("year")["ex"].apply(tt).unstack()
    h = pd.concat(hrs).dropna(subset=["r1"])
    h["e"] = h["r1"]-h.groupby("coin")["r1"].transform("mean")
    h2122 = h[h["hour"].isin([21,22])]
    out["h21_22_excess_by_year"] = h2122.groupby("year")["e"].apply(tt).unstack()
    out["h21_22_excess_by_weekday"] = h2122.groupby("wd")["e"].apply(tt).unstack()
    out["h21_22_excess_by_coin"] = h2122.groupby("coin")["e"].apply(tt).unstack()
    h03 = h[h["hour"].isin([2,3])]
    out["h2_3_excess_by_year"] = h03.groupby("year")["e"].apply(tt).unstack()
    B = pd.concat(bk).dropna()
    B = B[B["side"]!=0]
    out["book_bar_gain_by_side"] = B.groupby("side")["gain"].agg(["mean","count","sum"])
    return out
