def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 30: continue
            o,h,l,c = b.open,b.high,b.low,b.close
            rng = (h-l)
            mr = rng.rolling(20).mean()
            rr = rng/mr  # day range over 20d mean incl day
            cl = (c-l)/rng.replace(0,np.nan)
            lr = np.log(c).diff()
            vol = lr.rolling(20).std()
            vr = vol/vol.rolling(60).mean()
            r1 = c.shift(-1)/c-1
            r3 = c.shift(-3)/c-1
            r5p = c/c.shift(5)-1
            ret0 = c/c.shift(1)-1
            z0 = ret0/vol
            d = pd.DataFrame({"coin":coin,"win":w,"day":b.timestamp.astype(str).str[:10],
                "wd":pd.to_datetime(b.timestamp).dt.dayofweek,"year":pd.to_datetime(b.timestamp).dt.year,
                "rr":rr,"cl":cl,"vr":vr,"r1":r1,"r3":r3,"r5p":r5p,"z0":z0,"pos":np.arange(len(b)),
                "alloc":b.postRebalance_current_allocation})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    mu1 = D.groupby("coin").r1.mean(); mu3 = D[D.pos%3==0].groupby("coin").r3.mean()
    D["u1"] = D.r1 - D.coin.map(mu1); D["u3"] = D.r3 - D.coin.map(mu3)
    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s)<5: return pd.Series({"n":len(s),"mean":np.nan,"t":np.nan,"days":0})
        g = s.groupby("day")[col].sum(); m = s[col].mean()
        G=len(g); dev = s.assign(e=s[col]-m).groupby("day").e.sum()
        se = np.sqrt((dev**2).sum()*G/(G-1))/len(s)
        return pd.Series({"n":len(s),"mean":m,"t":m/se,"days":G})
    out = {}
    D["rrb"] = pd.cut(D.rr,[0,0.8,1.2,1.5,2,10])
    D["clb"] = pd.cut(D.cl,[-0.01,0.25,0.5,0.75,1.01])
    out["u1 by range x closeloc (all)"] = D.groupby(["rrb","clb"],observed=True).apply(lambda s: ct(s,"u1"))
    W = D[(D.rr>=1.5)]
    W = W.assign(vhi=W.vr>=1)
    out["wide days u1 by closeloc x volhi"] = W.groupby(["clb","vhi"],observed=True).apply(lambda s: ct(s,"u1"))
    out["wide days u3 by closeloc x volhi"] = W.groupby(["clb","vhi"],observed=True).apply(lambda s: ct(s,"u3"))
    WL = W[W.cl<=0.25]
    WL = WL.assign(prun=pd.qcut(WL.r5p,3,labels=["down","mid","up"]))
    out["wide low u1 by prior5d tercile"] = WL.groupby("prun",observed=True).apply(lambda s: ct(s,"u1"))
    out["wide low u1 by weekday"] = WL.groupby("wd").apply(lambda s: ct(s,"u1"))
    out["wide low u1 by year"] = WL.groupby("year").apply(lambda s: ct(s,"u1"))
    out["wide low u1 by coin"] = WL.groupby("coin").apply(lambda s: ct(s,"u1"))
    D["zb"] = pd.cut(D.z0,[-20,-2.5,-1.5,-0.5,0.5,1.5,2.5,20])
    out["u1 by today's z-return (all days)"] = D.groupby("zb",observed=True).apply(lambda s: ct(s,"u1"))
    D["vb"] = pd.cut(D.vr,[0,0.8,1,1.2,1.5,10])
    out["u1 after z<-1.5 by volratio"] = D[D.z0<-1.5].groupby("vb",observed=True).apply(lambda s: ct(s,"u1"))
    out["u1 by weekday all"] = D.groupby("wd").apply(lambda s: ct(s,"u1"))
    return out
