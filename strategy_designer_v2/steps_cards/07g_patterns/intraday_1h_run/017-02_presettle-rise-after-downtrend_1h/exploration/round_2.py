def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            d = df[["timestamp","close","volume"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"])
            d["r1"] = d["close"].shift(-1)/d["close"] - 1
            d["r2"] = d["close"].shift(-2)/d["close"] - 1
            d["p1"] = d["close"]/d["close"].shift(1) - 1
            d["p24"] = d["close"]/d["close"].shift(24) - 1
            d["p72"] = d["close"]/d["close"].shift(72) - 1
            d["vol720"] = d["p1"].rolling(720).std()
            d["vol24"] = d["p1"].rolling(24).std()
            d["f24"] = d["close"].shift(-24)/d["close"] - 1
            d["pos"] = np.arange(len(d))
            d["coin"] = c; d["win"] = w
            d["hour"] = d["timestamp"].dt.hour
            d["year"] = d["timestamp"].dt.year
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["r1x"] = A["r1"] - A.groupby("coin")["r1"].transform("mean")
    A["r2x"] = A["r2"] - A.groupby("coin")["r2"].transform("mean")
    A["held"] = (A["hour"]+1) % 24
    out = {}
    def tt(s):
        s = s.dropna(); return pd.Series({"n":len(s),"mean_bp":s.mean()*1e4,"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    # 2-hour block bars stamped 20 -> holds 21,22 ; grid: one per day per coin, independent
    B = A[A["hour"]==20].copy()
    out["2h return after 20:00 bar (holds 21-22) by coin"] = B.groupby("coin")["r2x"].apply(tt).unstack()
    out["same by year"] = B.groupby("year")["r2x"].apply(tt).unstack()
    wm = B.groupby(["coin","win"])["r2x"].mean()
    out["share of coin-windows positive (21-22)"] = pd.Series({"share":(wm>0).mean(),"n":len(wm)})
    # graded: within 20:00 bars, regress on 24h z
    B["z24"] = B["p24"]/(B["vol720"]*np.sqrt(24))
    res={}
    for c,g in B.dropna(subset=["z24","r2x"]).groupby("coin"):
        s=stats.linregress(g["z24"],g["r2x"]); res[c]=pd.Series({"slope_bp":s.slope*1e4,"t":s.slope/s.stderr,"n":len(g)})
    out["21-22 return on 24h z per coin"]=pd.DataFrame(res).T
    # hour 14 held (bar stamped 13) per coin and year
    C = A[A["hour"]==13]
    out["held-hour 14 by coin"] = C.groupby("coin")["r1x"].apply(tt).unstack()
    out["held-hour 14 by year"] = C.groupby("year")["r1x"].apply(tt).unstack()
    # held 1-3 (bar stamped 0, r over 3 bars)
    A["r3"] = A.groupby(["coin","win"])["close"].shift(-3)/A["close"]-1
    A["r3x"] = A["r3"] - A.groupby("coin")["r3"].transform("mean")
    E = A[A["hour"]==0]
    out["held 01-03 (3h) by coin"] = E.groupby("coin")["r3x"].apply(tt).unstack()
    # 1-bar reversal graded, per coin
    A["z1"] = A["p1"]/A["vol720"]
    res={}
    for c,g in A.dropna(subset=["z1","r1x"]).groupby("coin"):
        g = g[g["z1"].abs()<6]
        s=stats.linregress(g["z1"],g["r1x"]); res[c]=pd.Series({"slope_bp":s.slope*1e4,"t":s.slope/s.stderr,"n":len(g)})
    out["next-hour return on last-hour z per coin"]=pd.DataFrame(res).T
    # 1-bar reversal by vol level
    A["vq"] = A.groupby("coin")["vol24"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    res={}
    for q,g in A.dropna(subset=["z1","r1x","vq"]).groupby("vq"):
        g=g[g["z1"].abs()<6]; s=stats.linregress(g["z1"],g["r1x"]); res[q]=pd.Series({"slope_bp":s.slope*1e4,"t":s.slope/s.stderr,"n":len(g)})
    out["1h reversal slope by 24h-vol quintile"]=pd.DataFrame(res).T
    # 24h reversal on 24h z, per coin, non-overlapping
    G = A[A["pos"]%24==0].copy()
    G["f24x"] = G["f24"] - G.groupby("coin")["f24"].transform("mean")
    G["z24"] = G["p24"]/(G["vol720"]*np.sqrt(24))
    res={}
    for c,g in G.dropna(subset=["z24","f24x"]).groupby("coin"):
        s=stats.linregress(g["z24"],g["f24x"]); res[c]=pd.Series({"slope_bp":s.slope*1e4,"t":s.slope/s.stderr,"n":len(g)})
    out["24h return on 24h z per coin"]=pd.DataFrame(res).T
    return out
