def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin in data["bars"]:
        allr = []
        for w, b in data["bars"][coin].items():
            c = b["close"].values
            allr.append(pd.Series(c[3::3]/c[:-3:3][:len(c[3::3])]-1))
        m3 = pd.concat(allr).mean()
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["wd"] = b["ts"].dt.dayofweek
            b["r1"] = b["close"].shift(-1)/b["close"] - 1
            b["r3"] = b["close"].shift(-3)/b["close"] - 1
            b["ret"] = b["close"].pct_change()
            b["vol20"] = b["ret"].rolling(20).std()
            b["vol60"] = b["ret"].rolling(60).std()
            b["vratio"] = b["vol20"]/b["vol60"]
            b["ret7"] = b["close"]/b["close"].shift(7)-1
            b["z"] = b["ret"]/b["vol20"]
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["r1"]
            b["m3"] = m3; b["coin"]=coin; b["win"]=w
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    S = B[(B["wd"]==6)&(B["forecast"]>0)].dropna(subset=["r3"]).copy()
    S["ex3"] = S["r3"]-S["m3"]
    def tt(x): x=x.dropna(); return x.mean()/(x.std()/np.sqrt(len(x)))
    def agg(g):
        return pd.DataFrame({"n":g["ex3"].count(),"ex3":g["ex3"].mean(),"t_ex3":g["ex3"].apply(tt),
                             "gain1":g["gain"].mean(),"r1":g["r1"].mean()})
    S["vq"] = S.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    out["by_vol20_tercile"] = agg(S.groupby("vq"))
    S["vr"] = pd.qcut(S["vratio"],3,labels=False,duplicates="drop")
    out["by_vol_ratio"] = agg(S.groupby("vr"))
    S["zq"] = pd.qcut(S["z"],3,labels=False,duplicates="drop")
    out["by_raw_z"] = agg(S.groupby("zq"))
    S["r7q"] = pd.qcut(S["ret7"],3,labels=False,duplicates="drop")
    out["by_ret7"] = agg(S.groupby("r7q"))
    # vol x forecast slope
    for q in [0,1,2]:
        s = S[S.vq==q]
        r = stats.linregress(s["forecast"], s["ex3"])
        out[f"slope_vq{q}"] = pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(s)})
    # worst Monday gains
    G = B[B["pos"].abs()>1e-6]
    worst = G.nsmallest(30,"gain")
    worst = worst.merge(S[["coin","win","timestamp","vq"]], on=["coin","win","timestamp"], how="left")
    out["worst30"] = pd.Series({"mean_gain":worst["gain"].mean(),"mean_pos":worst["pos"].mean(),
        "mean_z":worst["z"].mean(),"mean_ret7":worst["ret7"].mean(),"share_hivol":(worst["vq"]==2).mean(),
        "share_lovol":(worst["vq"]==0).mean()})
    out["gain_share_by_vq"] = S.groupby("vq")["gain"].sum()/S["gain"].sum()
    out["pos_by_vq"] = S.groupby("vq")["pos"].mean()
    return out
