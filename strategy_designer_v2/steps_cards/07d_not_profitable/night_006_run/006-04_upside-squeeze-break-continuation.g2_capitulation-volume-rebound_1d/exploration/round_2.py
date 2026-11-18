def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; coins = list(bars.keys())
    R = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["f3"] = b["close"].shift(-3)/b["close"]-1
            b["gain"] = b["postRebalance_current_allocation"]*b["ret1"]
            b["sma"] = b["close"]/b["close"].rolling(50).mean()-1
            b["r30"] = b["close"]/b["close"].shift(30)-1
            b["pos"] = np.arange(len(b))
            b["coin"]=c; b["w"]=w; b["wn"]=int(w[1:])
            R.append(b)
    B = pd.concat(R)
    cm3 = B[B["pos"]%3==0].groupby("coin")["f3"].mean()
    B["x3"] = B["f3"]-B["coin"].map(cm3)
    G = B[(B["pos"]%3==0)&(B["regime"]=="mean_reversion")].dropna(subset=["x3","sma"])
    G["smas"] = np.where(G["sma"]>0,"above","below")
    G["fq"] = pd.qcut(G["forecast"],3,labels=False,duplicates="drop")
    def tt(x): return x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan
    out["grid_x3_by_sma_fq"] = G.groupby(["smas","fq"]).agg(n=("x3","size"), fc=("forecast","mean"), x3=("x3","mean"), t=("x3",tt))
    # slope of x3 on forecast within sma states
    sl = {}
    for s, g in G.groupby("smas"):
        r = __import__("scipy").stats.linregress(g["forecast"], g["x3"])
        sl[s] = {"slope": r.slope, "t": r.slope/r.stderr, "n": len(g)}
    out["slope_by_sma"] = pd.DataFrame(sl)
    # graded: x3 by sma quintile
    G["smq"] = pd.qcut(G["sma"],5,labels=False)
    out["grid_x3_by_sma_quint"] = G.groupby("smq").agg(n=("x3","size"), sma=("sma","mean"), x3=("x3","mean"), t=("x3",tt))
    # worst windows: book gain split by sma state
    B["smas"] = np.where(B["sma"]>0,"above","below")
    A = B[B["postRebalance_current_allocation"].abs()>1e-9].dropna(subset=["ret1","sma"])
    worst = [14,2,7,13]
    out["worst_windows_gain_by_sma"] = A[A["wn"].isin(worst)].groupby("smas").agg(n=("gain","size"), gain_sum=("gain","sum"), ret1=("ret1","mean"))
    out["other_windows_gain_by_sma"] = A[~A["wn"].isin(worst)].groupby("smas").agg(n=("gain","size"), gain_sum=("gain","sum"), ret1=("ret1","mean"))
    # 30-day vol state
    B["vol30"] = B.groupby(["coin","w"])["ret1"].transform(lambda x: x.shift(1).rolling(30).std())
    A = B[B["postRebalance_current_allocation"].abs()>1e-9].dropna(subset=["ret1","vol30"])
    A["vq"] = A.groupby("coin")["vol30"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["active_gain_by_vol_tercile"] = A.groupby("vq").agg(n=("gain","size"), gain=("gain","mean"), ret1=("ret1","mean"), t=("gain",tt))
    return out
