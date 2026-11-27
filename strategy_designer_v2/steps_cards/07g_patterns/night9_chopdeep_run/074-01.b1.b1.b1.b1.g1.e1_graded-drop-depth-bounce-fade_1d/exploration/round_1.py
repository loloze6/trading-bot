def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; o=b["open"]; h=b["high"]; l=b["low"]
            r1 = c.pct_change()
            nxt = c.shift(-1)/c - 1
            nxt3 = c.shift(-3)/c - 1
            rng = (h-l)/c.shift(1)
            width = rng / rng.rolling(20, min_periods=20).mean()
            sd20 = r1.rolling(20, min_periods=20).std()
            z1 = r1/sd20.shift(1)
            ret5 = c.shift(1)/c.shift(6)-1
            z5 = ret5/(sd20.shift(1)*np.sqrt(5))
            clv = (c-l)/(h-l)
            df = pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                "r1":r1,"nxt":nxt,"nxt3":nxt3,"width":width,"z1":z1,"z5":z5,"clv":clv,
                "falling":(b["regime"]!="chop"),"alloc":b["postRebalance_current_allocation"],
                "fc":b["forecast"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["day"]=D["ts"].dt.floor("D")
    D["year"]=D["ts"].dt.year
    D["wd"]=D["ts"].dt.weekday
    drift = D.groupby("coin")["nxt"].mean()
    D["unx"]=D["nxt"]-D["coin"].map(drift)
    def tstat(s, days):
        x = pd.DataFrame({"v":s,"d":days}).dropna()
        if len(x)<5: return (np.nan, len(x), 0)
        g = x.groupby("d")["v"].sum()
        m = x["v"].mean(); n=len(x); nd=len(g)
        se = np.sqrt((g - g.mean()*0 - m*x.groupby("d").size()).pow(2).sum())/n
        return (m, n, nd, m/se if se>0 else np.nan)
    def summ(mask, col="unx"):
        x=D[mask]
        res=tstat(x[col], x["day"])
        return res
    out={}
    # 1 up days by width quintile, falling vs not
    D["wq"]=pd.qcut(D["width"], 5, labels=False)
    tab=[]
    for f in [True, False]:
        for side,sm in [("up",D.r1>0),("down",D.r1<0)]:
            for q in range(5):
                m=(D.falling==f)&sm&(D.wq==q)
                r=summ(m)
                tab.append({"falling":f,"side":side,"wq":q,"mean_unx":r[0],"n":r[1],"days":r[2],"t":r[3] if len(r)>3 else np.nan})
    out["next_unx_by_width"]=pd.DataFrame(tab)
    # 2 by z1 (size of day's move in usual moves) quintile and regime
    D["zq"]=pd.qcut(D["z1"],7,labels=False)
    tab=[]
    for f in [True,False]:
        for q in range(7):
            m=(D.falling==f)&(D.zq==q)
            r=summ(m)
            tab.append({"falling":f,"zq":q,"z_mean":D.loc[m,"z1"].mean(),"mean_unx":r[0],"n":r[1],"t":r[3] if len(r)>3 else np.nan})
    out["next_unx_by_z1"]=pd.DataFrame(tab)
    # 3 close location in day, by regime
    D["cq"]=pd.cut(D["clv"],[-0.01,0.2,0.4,0.6,0.8,1.01],labels=False)
    tab=[]
    for f in [True,False]:
        for q in range(5):
            m=(D.falling==f)&(D.cq==q)
            r=summ(m)
            tab.append({"falling":f,"clv_q":q,"mean_unx":r[0],"n":r[1],"t":r[3] if len(r)>3 else np.nan})
    out["next_unx_by_closeloc"]=pd.DataFrame(tab)
    # 4 weekday by regime
    tab=[]
    for f in [True,False]:
        for q in range(7):
            m=(D.falling==f)&(D.wd==q)
            r=summ(m)
            tab.append({"falling":f,"wd":q,"mean_unx":r[0],"n":r[1],"t":r[3] if len(r)>3 else np.nan})
    out["weekday"]=pd.DataFrame(tab)
    # 5 prior 5d z5 quintile by regime, all days
    D["z5q"]=pd.qcut(D["z5"],5,labels=False)
    tab=[]
    for f in [True,False]:
        for q in range(5):
            m=(D.falling==f)&(D.z5q==q)
            r=summ(m)
            tab.append({"falling":f,"z5q":q,"mean_unx":r[0],"n":r[1],"t":r[3] if len(r)>3 else np.nan})
    out["next_unx_by_z5"]=pd.DataFrame(tab)
    # 6 book: gain by coin, year
    pos = D[D.alloc.abs()>1e-9].copy()
    pos["g"]=pos["alloc"]*pos["nxt"]
    out["book_by_coin"]=pos.groupby("coin")["g"].agg(["count","mean","sum"])
    out["book_by_year"]=pos.groupby("year")["g"].agg(["count","mean","sum"])
    out["falling_share"]=float(D.falling.mean())
    return out
