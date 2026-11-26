def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 30: continue
            h,l,c,o = b.high,b.low,b.close,b.open
            rng = h-l
            mr = rng.rolling(20).mean()
            mrp = rng.shift(1).rolling(20).mean()
            rr = rng/mr
            cl = (c-l)/rng.replace(0,np.nan)
            d = pd.DataFrame({"coin":coin,"win":w,"day":b.timestamp.astype(str).str[:10],
                "year":pd.to_datetime(b.timestamp).dt.year,
                "rr":rr,"cl":cl,"sev":(h-c)/mrp,"lowext":(c-l)/mrp,
                "body":(c-o)/mrp,
                "r1":c.shift(-1)/c-1,"r2":c.shift(-2)/c-1,"r3":c.shift(-3)/c-1,
                "pos":np.arange(len(b)),"reg":b.regime.astype(str),
                "alloc":b.postRebalance_current_allocation,"fc":b.forecast})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for k in [1,2,3]:
        mu = D[D.pos%k==0].groupby("coin")[f"r{k}"].mean()
        D[f"u{k}"] = D[f"r{k}"]-D.coin.map(mu)
    def ct(sub,col):
        s=sub.dropna(subset=[col])
        if len(s)<5: return pd.Series({"n":len(s),"mean":np.nan,"t":np.nan,"days":0})
        m=s[col].mean(); dev=s.assign(e=s[col]-m).groupby("day").e.sum(); G=len(dev)
        se=np.sqrt((dev**2).sum()*G/(G-1))/len(s)
        return pd.Series({"n":len(s),"mean":m,"t":m/se,"days":G})
    out={}
    out["regime counts"]=D.reg.value_counts()
    WL=D[(D.rr>=1.5)&(D.cl<=0.25)].copy()
    WL["inreg"]=WL.reg=="mean_reversion"
    out["wide-low u1 by in-regime"]=WL.groupby("inreg").apply(lambda s:ct(s,"u1"))
    out["wide-low u2 (pos%2) by in-regime"]=WL[WL.pos%2==0].groupby("inreg").apply(lambda s:ct(s,"u2"))
    out["wide-low u3 (pos%3) by in-regime"]=WL[WL.pos%3==0].groupby("inreg").apply(lambda s:ct(s,"u3"))
    # graded: severity (high-close)/prior mean range, all days
    D["sevb"]=pd.qcut(D.sev,8,duplicates="drop")
    out["u1 by (high-close)/20d range octile, all days"]=D.groupby("sevb",observed=True).apply(lambda s:ct(s,"u1"))
    NR=D[D.reg!="mean_reversion"]
    out["u1 by sev octile, outside regime"]=NR.groupby("sevb",observed=True).apply(lambda s:ct(s,"u1"))
    # mirror: (close-low)/range -> fall?
    D["lob"]=pd.qcut(D.lowext,8,duplicates="drop")
    out["u1 by (close-low)/20d range octile"]=D.groupby("lob",observed=True).apply(lambda s:ct(s,"u1"))
    # body down vs wick: among wide-low days, by body size
    WL["bodyb"]=pd.qcut(WL.body,3,labels=["bigdown","mid","small"])
    out["wide-low u1 by body tercile"]=WL.groupby("bodyb",observed=True).apply(lambda s:ct(s,"u1"))
    # book days: largest gains/losses
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; x["win"]=w; dd.append(x)
    DD=pd.concat(dd)
    bk=DD.groupby(["win","day"]).book_return.mean().dropna()
    out["book daily: n, share nonzero, top10 sum/total"]=pd.Series({"n":len(bk),"nonzero":(bk.abs()>1e-9).mean(),
        "total":bk.sum(),"top10":bk.nlargest(10).sum(),"bottom10":bk.nsmallest(10).sum()})
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    T=pd.concat(tr)
    T["dur_d"]=T.duration_minutes/1440
    out["trades by duration"]=T.groupby(T.dur_d.round()).net_profit_loss_percent.agg(["count","mean","median"])
    return out
