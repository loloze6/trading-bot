def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    rows = []
    for c, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","open","high","low","close","forecast","postRebalance_current_allocation"]].copy().reset_index(drop=True)
            d["coin"]=c; d["win"]=w; d["pos"]=np.arange(len(d))
            r = d["close"].pct_change()
            d["r"]=r
            d["vol60"]=r.rolling(60,min_periods=20).std()
            d["z"]=r/d["vol60"]
            for h in [1,2,3,5]:
                d[f"f{h}"]=d["close"].shift(-h)/d["close"]-1
            s = np.sign(r).fillna(0)
            grp=(s!=s.shift()).cumsum()
            d["streak"]=s*s.groupby(grp).cumcount().add(1)
            d["r5"]=d["close"]/d["close"].shift(5)-1
            d["z5"]=d["r5"]/(d["vol60"]*np.sqrt(5))
            d["volrank"]=d["vol60"]/d["vol60"].rolling(250,min_periods=60).median()
            d["rng"]=(d["high"]-d["low"])/d["close"]/d["vol60"]
            d["clv"]=(d["close"]-d["low"])/(d["high"]-d["low"])
            d["wd"]=pd.to_datetime(d["timestamp"]).dt.weekday
            d["yr"]=pd.to_datetime(d["timestamp"]).dt.year
            d["gain"]=d["postRebalance_current_allocation"]*d["f1"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu={h:{c:D[D.coin==c][f"f{h}"][D[D.coin==c].pos%h==0].mean() for c in D.coin.unique()} for h in [1,2,3,5]}
    for h in [1,2,3,5]:
        D[f"x{h}"]=D[f"f{h}"]-D.coin.map(mu[h])
    def tab(key, col, h=1, q=None):
        S=D[D.pos%h==0].dropna(subset=[col,f"x{h}"])
        g = pd.qcut(S[col],q,duplicates="drop") if q else S[col]
        a=S.groupby(g,observed=True)[f"x{h}"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        out[key]=a.drop(columns="std").round(5)
    for h in [1,2,3,5]: tab(f"z decile -> excess h{h}d","z",h,10)
    D["streakc"]=D["streak"].clip(-6,6)
    tab("streak -> x1","streakc",1); tab("streak -> x3","streakc",3)
    tab("z5 quintile -> x5","z5",5,5)
    tab("weekday -> x1","wd",1)
    tab("volrank quintile -> x1","volrank",1,5)
    tab("range/vol quintile -> x1","rng",1,5)
    tab("close-location quintile -> x1","clv",1,5)
    # down-day scaled fall effect by vol regime
    S=D.dropna(subset=["z","x1","volrank"]); S=S[S.z<0]
    S["vq"]=pd.qcut(S.volrank,3,labels=["lowvol","mid","hivol"])
    out["down days: corr(-z,x1) by vol tercile"]=S.groupby("vq",observed=True).apply(lambda g: pd.Series({"rho":stats.spearmanr(-g.z,g.x1)[0],"n":len(g),"slope":np.polyfit(-g.z,g.x1,1)[0]}))
    S["cq"]=pd.qcut(S.clv,3,labels=["closeLow","mid","closeHigh"])
    out["down days: z tercile x close-loc -> x1"]=S.groupby([pd.qcut(-S.z,3,labels=["small","mid","big"]),"cq"],observed=True)["x1"].agg(["mean","count"]).round(5)
    out["down days by year: mean x1 for z<-1.5"]=S[S.z<-1.5].groupby("yr")["x1"].agg(["mean","count"]).round(5)
    out["by coin: z decile1 x1"]=D[D.z<D.z.quantile(0.1)].groupby("coin")["x1"].agg(["mean","count"]).round(5)
    # book gains extremes: what preceded
    G=D.dropna(subset=["gain"]); G=G[G.postRebalance_current_allocation!=0]
    G["gq"]=pd.qcut(G.gain,10,labels=False)
    out["held bars: gain decile vs z, volrank, streak"]=G.groupby("gq")[["gain","z","volrank","streak","clv"]].mean().round(4)
    return out
