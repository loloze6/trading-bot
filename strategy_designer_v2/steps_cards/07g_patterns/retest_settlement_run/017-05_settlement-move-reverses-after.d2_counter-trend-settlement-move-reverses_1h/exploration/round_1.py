def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","open","high","low","close","volume","postRebalance_current_allocation"]].copy()
            b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True)
            b = b.reset_index(drop=True)
            c = b["close"]
            b["pos"] = np.arange(len(b))
            b["r1f"] = c.shift(-1)/c - 1
            b["r8f"] = c.shift(-8)/c - 1
            b["r24f"] = c.shift(-24)/c - 1
            b["r1p"] = c/c.shift(1) - 1
            b["r2p"] = c/c.shift(2) - 1
            b["r24p"] = c/c.shift(24) - 1
            b["r168p"] = c/c.shift(168) - 1
            lr = np.log(c).diff()
            b["vol24"] = lr.rolling(24).std()
            b["vol168"] = lr.rolling(168).std()
            b["vrel"] = b["volume"]/b["volume"].rolling(168).median()
            b["closehour"] = (b["timestamp"] + pd.Timedelta(hours=1)).dt.hour
            b["wd"] = b["timestamp"].dt.weekday
            b["year"] = b["timestamp"].dt.year
            b["coin"] = coin; b["win"] = w
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    # drift per coin
    def tt(x):
        x = x.dropna(); n=len(x)
        return pd.Series({"mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan, "n": n})
    # demeaned per coin 1h forward
    B["r1x"] = B["r1f"] - B.groupby("coin")["r1f"].transform("mean")
    out["1h fwd excess by close hour"] = B.groupby("closehour")["r1x"].apply(tt).unstack()
    out["volume rel by close hour"] = B.groupby("closehour")["vrel"].median().to_frame("median vrel")
    # 1h reversal: next 1h vs last 1h, by hour bucket settlement vs other
    B["sgn_r1p"] = np.sign(B["r1p"])
    B["rev1"] = -B["sgn_r1p"]*B["r1x"]
    out["1h reversal (−sign last1h × next1h) by close hour"] = B.groupby("closehour")["rev1"].apply(tt).unstack()
    # 8h grid
    G8 = B[B["pos"] % 8 == 0].copy()
    G8["r8x"] = G8["r8f"] - G8.groupby("coin")["r8f"].transform("mean")
    res = {}
    for col in ["r2p","r24p","r168p"]:
        d = G8[[col,"r8x","coin"]].dropna()
        z = d.groupby("coin")[col].transform(lambda s: (s - s.mean())/s.std())
        sl = stats.linregress(z, d["r8x"])
        res[col] = {"slope_bp_per_sd": sl.slope*1e4, "t": sl.slope/sl.stderr, "n": len(d)}
    out["8h fwd excess slope on past return (z)"] = pd.DataFrame(res).T
    # 24h grid
    G24 = B[B["pos"] % 24 == 0].copy()
    G24["r24x"] = G24["r24f"] - G24.groupby("coin")["r24f"].transform("mean")
    res = {}
    for col in ["r24p","r168p","vol24","vol168","vrel"]:
        d = G24[[col,"r24x","coin"]].dropna()
        z = d.groupby("coin")[col].transform(lambda s: (s - s.mean())/s.std())
        sl = stats.linregress(z, d["r24x"])
        res[col] = {"slope_bp_per_sd": sl.slope*1e4, "t": sl.slope/sl.stderr, "n": len(d)}
    out["24h fwd excess slope on predictor (z)"] = pd.DataFrame(res).T
    # 24h past return × vol tercile
    d = G24[["r24p","r24x","vol168","coin"]].dropna().copy()
    d["vt"] = d.groupby("coin")["vol168"].transform(lambda s: pd.qcut(s,3,labels=False))
    d["s"] = np.sign(d["r24p"])*d["r24x"]
    out["24h continuation (sign past24 × next24) by vol tercile"] = d.groupby("vt")["s"].apply(tt).unstack()
    d = G24[["r168p","r24x","vol168","coin"]].dropna().copy()
    d["vt"] = d.groupby("coin")["vol168"].transform(lambda s: pd.qcut(s,3,labels=False))
    d["s"] = np.sign(d["r168p"])*d["r24x"]
    out["24h after sign 7d return by vol tercile"] = d.groupby("vt")["s"].apply(tt).unstack()
    out["24h fwd excess by weekday"] = G24.groupby("wd")["r24x"].apply(tt).unstack()
    # settlement-hour 2h pre reversal over 8h vs other hours, by close hour (grid aligned per hour)
    B["r8x"] = B["r8f"] - B.groupby("coin")["r8f"].transform("mean")
    B["rev2_8"] = -np.sign(B["r2p"])*B["r8x"]
    sub = B[B["closehour"] % 4 == 0]
    out["8h reversal of 2h pre-move by close hour (0/8/16 settle)"] = sub.groupby("closehour")["rev2_8"].apply(tt).unstack()
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D = pd.concat(D, ignore_index=True)
    D["day"] = pd.to_datetime(D["day"])
    D["year"] = D["day"].dt.year
    out["book daily mean by year (bp)"] = D.groupby("year")["book_return"].apply(tt).unstack()
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"]=coin; T.append(t)
    T = pd.concat(T, ignore_index=True)
    out["trades gross vs net by side"] = T.groupby("side")[["profit_loss_percent","net_profit_loss_percent","duration_minutes"]].agg(["mean","count"])
    out["trades by coin"] = T.groupby("coin")[["profit_loss_percent","net_profit_loss_percent"]].mean()
    return out
