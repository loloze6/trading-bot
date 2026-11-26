def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all windows
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); l = b["low"].astype(float); h = b["high"].astype(float)
            lo20 = l.shift(1).rolling(20).min(); hi20 = h.shift(1).rolling(20).max()
            tr60 = (c/c.shift(60)-1)*100
            d = pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                              "fc":b["forecast"].astype(float),"regime":b["regime"],
                              "depth":(c/lo20-1)*100,"updepth":(c/hi20-1)*100,"tr60":tr60})
            for k in [1,2,3,5]:
                d[f"r{k}"] = c.shift(-k)/c-1 - k*mu
            d["mu"]=mu
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["day"]=D["ts"].dt.floor("D")
    D["year"]=D["ts"].dt.year
    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s)<3: return pd.Series({"n":len(s),"days":0,"mean":np.nan,"t":np.nan})
        m = s[col].mean()
        g = (s[col]-m).groupby(s["day"]).sum()
        Dn=len(g); se=np.sqrt((g**2).sum()*Dn/(Dn-1))/len(s)
        return pd.Series({"n":len(s),"days":Dn,"mean":m,"t":m/se if se>0 else np.nan})
    cases = D[D["fc"]>0]
    out["cases by horizon"] = pd.DataFrame({k:ct(cases,k) for k in ["r1","r2","r3","r5"]}).T
    out["cases by coin r1"] = cases.groupby("coin").apply(lambda s: ct(s,"r1"))
    out["cases by year r1"] = cases.groupby("year").apply(lambda s: ct(s,"r1"))
    cases = cases.copy()
    cases["dq"] = pd.qcut(cases["depth"].rank(method="first"),3,labels=["deep","mid","shallow"])
    out["cases by depth tercile r1"] = cases.groupby("dq").apply(lambda s: pd.concat([ct(s,"r1"),pd.Series({"meandepth":s["depth"].mean()})]))
    # recomputed breaks by trend profile (in-window 60d trend)
    br = D[(D["depth"]<0)&D["tr60"].notna()].copy()
    br["prof"]=np.where(br["tr60"]>10,"rising",np.where(br["tr60"]<-10,"falling","choppy"))
    out["down breaks by trend r1"] = br.groupby("prof").apply(lambda s: ct(s,"r1"))
    out["down breaks by trend r3"] = br.groupby("prof").apply(lambda s: ct(s,"r3"))
    up = D[(D["updepth"]>0)&D["tr60"].notna()].copy()
    up["prof"]=np.where(up["tr60"]>10,"rising",np.where(up["tr60"]<-10,"falling","choppy"))
    out["up breaks by trend r1 (raw, + = continue)"] = up.groupby("prof").apply(lambda s: ct(s,"r1"))
    out["all down breaks any trend r1"] = ct(D[D["depth"]<0],"r1")
    out["regime counts"] = D["regime"].value_counts()
    return out
