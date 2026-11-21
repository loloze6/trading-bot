def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            d = df[["timestamp","close","volume","postRebalance_current_allocation"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"])
            d["r1"] = d["close"].shift(-1)/d["close"] - 1   # next bar return
            d["p1"] = d["close"]/d["close"].shift(1) - 1
            d["p72"] = d["close"]/d["close"].shift(72) - 1
            d["p24"] = d["close"]/d["close"].shift(24) - 1
            d["vol24"] = d["p1"].rolling(24).std()
            d["vol720"] = d["p1"].rolling(720).std()
            d["f24"] = d["close"].shift(-24)/d["close"] - 1
            d["f4"] = d["close"].shift(-4)/d["close"] - 1
            d["pos"] = np.arange(len(d))
            d["coin"] = c; d["win"] = w
            d["hour"] = d["timestamp"].dt.hour  # bar start; r1 is return over next bar (start hour+1)
            d["wd"] = d["timestamp"].dt.weekday
            d["lvol"] = np.log(d["volume"].replace(0, np.nan))
            d["lvol_rel"] = d["lvol"] - d["lvol"].rolling(168).mean()
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # coin-demeaned next-bar return
    A["r1x"] = A["r1"] - A.groupby("coin")["r1"].transform("mean")
    out = {}
    def tt(s):
        s = s.dropna(); return pd.Series({"n":len(s),"mean_bp":s.mean()*1e4,"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    # hour of the held bar = hour+1 mod 24
    A["held_hour"] = (A["hour"]+1)%24
    out["next-bar excess return by held hour"] = A.groupby("held_hour")["r1x"].apply(tt).unstack()
    out["rel log volume by bar hour"] = A.groupby("hour")["lvol_rel"].mean()
    out["next-bar excess by weekday"] = A.groupby("wd")["r1x"].apply(tt).unstack()
    # reversal after large 1h moves: z of last bar
    A["z1"] = A["p1"]/A["vol720"]
    A["z1b"] = pd.cut(A["z1"], [-np.inf,-3,-2,-1,0,1,2,3,np.inf])
    out["next-bar excess by last-bar z"] = A.groupby("z1b", observed=True)["r1x"].apply(tt).unstack()
    # 24h grid: f24 vs p72 / p24 quintiles, non-overlapping
    G = A[A["pos"]%24==0].copy()
    G["f24x"] = G["f24"] - G.groupby("coin")["f24"].transform("mean")
    G["z72"] = G["p72"]/(G["vol720"]*np.sqrt(72))
    G["z24"] = G["p24"]/(G["vol720"]*np.sqrt(24))
    G["q72"] = pd.qcut(G["z72"], 5, labels=False, duplicates="drop")
    G["q24"] = pd.qcut(G["z24"], 5, labels=False, duplicates="drop")
    out["next 24h excess by 3d-z quintile"] = G.groupby("q72")["f24x"].apply(tt).unstack()
    out["next 24h excess by 1d-z quintile"] = G.groupby("q24")["f24x"].apply(tt).unstack()
    # by vol level
    G["vq"] = G.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["next 24h excess by 24h-vol quintile"] = G.groupby("vq")["f24x"].apply(tt).unstack()
    # 4h grid: graded fall effect by hour block pre-settle vs others
    H = A[A["pos"]%4==0].copy()
    H["f4x"] = H["f4"] - H.groupby("coin")["f4"].transform("mean")
    H["z72"] = H["p72"]/(H["vol720"]*np.sqrt(72))
    res = {}
    for c, g in H.dropna(subset=["f4x","z72"]).groupby("coin"):
        s = stats.linregress(g["z72"], g["f4x"]); res[c] = pd.Series({"slope_bp":s.slope*1e4,"t":s.slope/s.stderr,"n":len(g)})
    out["4h excess on 3d z, per coin"] = pd.DataFrame(res).T
    # book
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"]=c; d["win"]=w; D.append(d)
    D = pd.concat(D)
    bd = D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book daily: mean, sd, corr with coins"] = pd.Series({"book_mean":bd["book_return"].mean(),"coin_mean":bd["coin_return"].mean(),"corr":bd.corr().iloc[0,1],"n":len(bd)})
    # trades
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades by coin"] = T.groupby("coin").agg(n=("profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), fee=("total_commission","mean"))
    return out
