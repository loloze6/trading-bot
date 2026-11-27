def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].values; h=b["high"].values; l=b["low"].values; o=b["open"].values
            rng=h-l
            cl=np.where(rng>0,(c-l)/np.where(rng>0,rng,1),np.nan)
            n=len(b)
            for H in (1,2,3,5):
                f=np.full(n,np.nan)
                f[:n-H]=c[H:]/c[:n-H]-1
                b[f"f{H}"]=f
            r1=np.full(n,np.nan); r1[1:]=c[1:]/c[:-1]-1
            r5=np.full(n,np.nan); r5[5:]=c[5:]/c[:-5]-1
            r20=np.full(n,np.nan); r20[20:]=c[20:]/c[:-20]-1
            b["cl"]=cl; b["r1"]=r1; b["r5"]=r5; b["r20"]=r20
            b["rngrel"]=rng/c
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(n)
            b["inprof"]=(b["regime"]!="chop").astype(int)
            b["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            b["yr"]=pd.to_datetime(b["timestamp"]).dt.year
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b[["coin","w","pos","cl","r1","r5","r20","rngrel","inprof","wd","yr","day","regime","f1","f2","f3","f5","postRebalance_current_allocation"]])
    A=pd.concat(rows,ignore_index=True)
    # drift per coin per H on grid
    out={}
    def tclust(x,days):
        d=pd.DataFrame({"x":x,"d":days}).dropna()
        if len(d)<5: return np.nan,len(d),0
        s=d.groupby("d")["x"].sum(); G=len(s); n=len(d)
        m=d["x"].mean()
        se=np.sqrt((s-s.index.map(lambda k:0)).pow(2).sum()) # placeholder
        dev=(d["x"]-m); sd=dev.groupby(d["d"]).sum()
        se=np.sqrt((sd**2).sum()*G/(G-1))/n
        return m/se,n,G
    for H in (1,2,3,5):
        g=A[A.pos%H==0].copy()
        dr=g.groupby("coin")[f"f{H}"].mean()
        A[f"u{H}"]=A[f"f{H}"]-A["coin"].map(dr)
    A["clq"]=pd.cut(A.cl,[-0.01,0.2,0.4,0.6,0.8,1.0],labels=["0-.2",".2-.4",".4-.6",".6-.8",".8-1"])
    res=[]
    for H in (1,2,3,5):
        g=A[A.pos%H==0]
        for p in (0,1):
            for q,gg in g[g.inprof==p].groupby("clq",observed=True):
                t,n,G=tclust(gg[f"u{H}"].values,gg["day"].values)
                res.append({"H":H,"inprof":p,"clq":q,"mean_u":gg[f"u{H}"].mean(),"t":t,"n":n})
    out["unusual by CL bin, profile, horizon"]=pd.DataFrame(res)
    # in profile: by prior 1-day return quintile, 2d
    g=A[(A.pos%2==0)&(A.inprof==1)].copy()
    res=[]
    for col in ("r1","r5","r20","rngrel"):
        g["q"]=g.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False) if s.notna().sum()>10 else np.nan)
        for q,gg in g.groupby("q"):
            t,n,G=tclust(gg["u2"].values,gg["day"].values)
            res.append({"var":col,"q":q,"mean_u2":gg["u2"].mean(),"t":t,"n":n})
    out["in profile: u2 by prior var quintile"]=pd.DataFrame(res)
    g2=A[(A.pos%2==0)].copy()
    res=[]
    for col in ("r1","r5"):
        g2["q"]=g2.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
        for q,gg in g2[g2.inprof==0].groupby("q"):
            t,n,G=tclust(gg["u2"].values,gg["day"].values)
            res.append({"var":col,"q":q,"mean_u2":gg["u2"].mean(),"t":t,"n":n})
    out["out of profile: u2 by prior var quintile"]=pd.DataFrame(res)
    res=[]
    g=A[(A.pos%2==0)&(A.inprof==1)]
    for wd,gg in g.groupby("wd"):
        t,n,G=tclust(gg["u2"].values,gg["day"].values)
        res.append({"wd":wd,"mean_u2":gg["u2"].mean(),"t":t,"n":n})
    out["in profile weekday u2"]=pd.DataFrame(res)
    out["share in profile by coin"]=A.groupby("coin")["inprof"].mean()
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd=d.copy(); dd["coin"]=coin; dd["w"]=w; D.append(dd)
    D=pd.concat(D)
    bk=D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book by window"]=bk.groupby(level=0).agg(["mean","std","count","sum"])
    # trades
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            tt=t.copy(); tt["coin"]=coin; tt["w"]=w; T.append(tt)
    T=pd.concat(T)
    out["trades"]=T.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
