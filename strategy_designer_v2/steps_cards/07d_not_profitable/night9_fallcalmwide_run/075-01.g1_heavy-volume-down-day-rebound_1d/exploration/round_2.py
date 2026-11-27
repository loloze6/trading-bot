def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]
    recs = []
    for c in bars:
        ws = sorted(bars[c].keys(), key=lambda x:int(x[1:]))
        full = pd.concat([bars[c][w].assign(w=w) for w in ws]).sort_values("timestamp").reset_index(drop=True)
        full["timestamp"] = pd.to_datetime(full["timestamp"])
        cl = full["close"]
        full["r1"] = cl.pct_change()
        full["tr60"] = cl/cl.shift(60)-1
        sd30 = full["r1"].rolling(30).std()
        med = sd30.rolling(365, min_periods=200).median()
        full["agit"] = (sd30 > med).where(med.notna())
        full["vr"] = full["volume"]/full["volume"].shift(1).rolling(20).mean()
        full["nx"] = full.groupby("w")["close"].shift(-1)/cl-1
        full["same_prev_w"] = full["w"].eq(full["w"].shift(1))
        full["down"] = (full["r1"]<0) & full["same_prev_w"]
        full["alloc"] = full["postRebalance_current_allocation"]
        full["coin"] = c
        full["wn"] = full["w"].str[1:].astype(int)
        recs.append(full)
    F = pd.concat(recs)
    F["drift"] = F.groupby("coin")["nx"].transform("mean")
    F["ex"] = F["nx"]-F["drift"]
    F["trend"] = np.where(F["tr60"]>0.1,"rising",np.where(F["tr60"]<-0.1,"falling",np.where(F["tr60"].notna(),"choppy","na")))
    F["day"] = F["timestamp"].dt.floor("D")
    g = F[F["nx"].notna()].copy()
    g["vrq"] = g.groupby("coin")["vr"].transform(lambda s: s.rank(pct=True))
    cost = 0.0022
    def book(mask, name):
        x = g.copy()
        a = x["alloc"].where(mask, 0.0).fillna(0)
        x["a"] = a
        x["prev"] = x.groupby(["coin","w"])["a"].shift(1).fillna(0)
        x["pg"] = x["a"]*x["nx"] - (x["a"]-x["prev"]).abs()*cost/2
        d = x.groupby(["wn","day"])["pg"].mean().sort_index()
        v = (1+d).cumprod(); ddn = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(d))-1
        return pd.Series({"mean":d.mean(),"sharpe":d.mean()/d.std()*np.sqrt(365),"yearly":yr,"maxdd":ddn,"calmar":yr/abs(ddn),"inpos":(x["a"]!=0).mean()})
    m_all = pd.Series(True, index=g.index)
    res = {
        "all (approx)": book(m_all,""),
        "agitated only": book(g["agit"]==True,""),
        "not falling calm": book(~((g["trend"]=="falling")&(g["agit"]==False)),""),
        "vol ratio top half": book(g["vrq"]>0.5,""),
        "vol ratio top third": book(g["vrq"]>2/3,""),
        "agit & vr top half": book((g["agit"]==True)&(g["vrq"]>0.5),""),
    }
    out["book variants (net approx cost)"] = pd.DataFrame(res).T
    # condition alone check: agitated non-down days vs agitated down days
    def summ(x):
        return pd.Series({"n":len(x),"mean_ex":x["ex"].mean(),"t":x["ex"].mean()/(x["ex"].std()/np.sqrt(len(x)))})
    out["agitation x down"] = g.groupby([g["agit"].map({True:"agit",False:"calm"}).fillna("na"), "down"]).apply(summ)
    g["vq"] = pd.cut(g["vrq"],[0,1/3,2/3,1],labels=["lo","mid","hi"])
    out["agit x down x vol"] = g[g["agit"].notna()].groupby([g["agit"].map({True:"agit",False:"calm"}), "down","vq"]).apply(summ)
    # deepest fall w8-w9: where was book losing
    x = g.copy(); x["pg"] = x["alloc"]*x["nx"]
    seg = x[x["wn"].isin([9])]
    out["w9 pg by profile"] = seg.groupby([seg["trend"], seg["agit"].map({True:"agit",False:"calm"}).fillna("na")])["pg"].agg(["sum","count"])
    out["w9 pg by vol tercile on held"] = seg[seg["alloc"]!=0].groupby("vq")["pg"].agg(["sum","mean","count"])
    return out
