def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].values; h=b["high"].values; l=b["low"].values
            rng=h-l; n=len(b)
            cl=np.where(rng>0,(c-l)/np.where(rng>0,rng,1),np.nan)
            for H in (1,2,3,5):
                f=np.full(n,np.nan); f[:n-H]=c[H:]/c[:n-H]-1; b[f"f{H}"]=f
            r60=np.full(n,np.nan); r60[60:]=c[60:]/c[:-60]-1
            lr=np.full(n,np.nan); lr[1:]=np.log(c[1:]/c[:-1])
            v30=pd.Series(lr).rolling(30).std().values
            v60m=pd.Series(v30).rolling(60,min_periods=30).median().values
            agi=(v30>v60m).astype(float); agi[np.isnan(v60m)]=np.nan
            b["cl"]=cl; b["r60"]=r60; b["agi"]=agi
            b["coin"]=coin; b["w"]=w; b["pos"]=np.arange(n)
            b["inprof"]=(b["regime"]!="chop").astype(int)
            ts=pd.to_datetime(b["timestamp"]); b["yr"]=ts.dt.year; b["day"]=ts.dt.floor("D")
            rows.append(b)
    A=pd.concat(rows,ignore_index=True)
    for H in (1,2,3,5):
        dr=A[A.pos%H==0].groupby("coin")[f"f{H}"].mean()
        A[f"u{H}"]=A[f"f{H}"]-A.coin.map(dr)
    def slope(q,H):
        x=q.cl; y=q[f"u{H}"]; ok=x.notna()&y.notna(); x=x[ok]; y=y[ok]; d=q.day[ok]
        if len(x)<15: return np.nan,np.nan,len(x)
        xc=x-x.mean(); b1=(xc*(y-y.mean())).sum()/(xc**2).sum()
        e=y-y.mean()-b1*xc; sc=(xc*e).groupby(d).sum()
        se=np.sqrt((sc**2).sum())/(xc**2).sum()
        return b1,b1/se,len(x)
    out={}
    res=[]
    for H in (1,2,3,5):
        g=A[(A.pos%H==0)&(A.inprof==1)]
        b1,t,n=slope(g,H); res.append({"H":H,"slope":b1,"t":t,"n":n})
    out["recorded profile: slope u on CL, all in-profile bars"]=pd.DataFrame(res)
    g=A[(A.pos%5==0)&(A.inprof==1)&(A.cl>=0.8)]
    out["inprof hi 5d: by window"]=g.groupby("w")["u5"].agg(["count","mean"])
    out["inprof hi 5d: by coin"]=g.groupby("coin")["u5"].agg(["count","mean"])
    g["trend"]=np.where(A.loc[g.index,"r60"]>0.1,"r",np.where(A.loc[g.index,"r60"]<-0.1,"f","c"))
    # own agitated profiles, 1d slope by year and leave-one-window-out
    A["trend"]=np.where(A.r60>0.10,"rising",np.where(A.r60<-0.10,"falling",np.where(A.r60.notna(),"choppy",None)))
    res=[]
    for tr in ("choppy","falling","rising"):
        q=A[(A.trend==tr)&(A.agi==1)]
        for yr,s in q.groupby("yr"):
            b1,t,n=slope(s,1); res.append({"trend":tr,"yr":yr,"slope":b1,"t":t,"n":n})
    out["agitated 1d slope by trend, year"]=pd.DataFrame(res)
    res=[]
    for tr in ("choppy","falling"):
        q=A[(A.trend==tr)&(A.agi==1)]
        for w in sorted(q.w.unique()):
            b1,t,n=slope(q[q.w!=w],1); res.append({"trend":tr,"left_out":w,"slope":b1,"t":t,"n":n})
    out["agitated 1d slope leave one window out"]=pd.DataFrame(res).groupby("trend")[["slope","t"]].agg(["min","max"])
    q=A[(A.trend.isin(["choppy","falling"]))&(A.agi==1)].copy()
    q["clq"]=pd.cut(q.cl,[-0.01,0.2,0.4,0.6,0.8,1.0])
    out["choppy+falling agitated: u1 by CL bin"]=q.groupby("clq",observed=True)["u1"].agg(["count","mean"])
    return out
