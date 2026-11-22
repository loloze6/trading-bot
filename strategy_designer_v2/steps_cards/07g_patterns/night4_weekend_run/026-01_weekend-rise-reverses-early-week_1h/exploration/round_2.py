def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; H = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","open","close"]].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); c = b["close"].values; n = len(b)
            r = np.r_[np.nan, c[1:]/c[:-1]-1]   # bar's own return, stamped by bar start
            vol = pd.Series(r).abs().rolling(168, min_periods=100).mean().values  # known at bar close
            H.append(pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year.values,"hour":ts.dt.hour.values,"r":r}))
            for hz in (12,24,48):
                g = np.arange(0, n-hz, hz)
                g = g[g>=hz]
                if len(g)<3: continue
                past = c[g]/c[g-hz]-1; fut = c[g+hz]/c[g]-1
                rows.append(pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year.values[g],"hz":hz,
                                          "past":past,"fut":fut,"vol":vol[g]}))
    D = pd.concat(rows).dropna()
    D["z"] = D["past"]/(D["vol"]*np.sqrt(D["hz"]))
    D["fz"] = D.groupby(["coin","hz"])["fut"].transform(lambda x:(x-x.mean())/x.std())
    D["vq"] = D.groupby(["coin","hz"])["vol"].transform(lambda x: pd.qcut(x,5,labels=False))
    res = {}
    for (hz,v),g in D.groupby(["hz","vq"]):
        s = stats.linregress(g.z,g.fz); rho = stats.spearmanr(g.z,g.fz)
        res[f"h{hz} vq{v}"] = {"slope":s.slope,"t":s.slope/s.stderr,"spearman":rho.correlation,"sp_p":rho.pvalue,"n":len(g)}
    out["reversal slope by horizon and vol quintile"] = pd.DataFrame(res).T
    T = D[(D.hz==24)&(D.vq==4)].copy()
    T["pq"] = pd.qcut(T["z"],5,labels=False)
    # raw signed fut minus coin drift
    drift = D[D.hz==24].groupby("coin")["fut"].mean()
    T["un"] = T["fut"] - T["coin"].map(drift)
    gq = T.groupby("pq").agg(z=("z","mean"),un=("un","mean"),sd=("un","std"),n=("un","count"))
    gq["t"] = gq["un"]/(gq["sd"]/np.sqrt(gq["n"]))
    out["h24 top vol quintile: unusual 24h move by past-move quintile"] = gq
    pc = {}
    for k,g in T.groupby("coin"):
        s = stats.linregress(g.z,g.fz); pc[k]={"slope":s.slope,"t":s.slope/s.stderr,"spear":stats.spearmanr(g.z,g.fz).correlation,"n":len(g)}
    out["h24 top vol: per coin"] = pd.DataFrame(pc).T
    py = {}
    for k,g in T.groupby("year"):
        if len(g)>30:
            s = stats.linregress(g.z,g.fz); py[k]={"slope":s.slope,"t":s.slope/s.stderr,"spear":stats.spearmanr(g.z,g.fz).correlation,"n":len(g)}
    out["h24 top vol: per year"] = pd.DataFrame(py).T
    # trimmed: drop |z|>4
    Tt = T[T.z.abs()<4]; s = stats.linregress(Tt.z,Tt.fz)
    out["h24 top vol trimmed |z|<4"] = f"slope {s.slope:.3f} t {s.slope/s.stderr:.2f} n {len(Tt)}"
    # hour effects: own-bar return by stamp hour, z by coin
    Hh = pd.concat(H).dropna(subset=["r"])
    Hh["rz"] = Hh.groupby("coin")["r"].transform(lambda x:(x-x.mean())/x.std())
    def tt(x): return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"n":len(x)})
    for h in (14,21,22):
        sub = Hh[Hh.hour==h]
        out[f"hour {h} bar z-return per coin"] = sub.groupby("coin")["rz"].apply(tt).unstack()
        out[f"hour {h} bar z-return per year"] = sub.groupby("year")["rz"].apply(tt).unstack()
    Hh["raw_bp"] = Hh["r"]*1e4
    out["hour mean raw return bp, hours 13,14,21,22"] = Hh[Hh.hour.isin([13,14,21,22])].groupby("hour")["raw_bp"].mean()
    return out
