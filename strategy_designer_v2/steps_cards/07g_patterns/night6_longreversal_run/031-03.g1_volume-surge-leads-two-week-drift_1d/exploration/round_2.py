def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"c":c,"r1":r1,
                "vr":np.log(v.rolling(14).mean()/v.rolling(30).mean()),
                "vr7":np.log(v.rolling(7).mean()/v.rolling(30).mean()),
                "r3":c/c.shift(3)-1,"vol20":r1.rolling(20).std(),
                "day":ts.dt.floor("D"),"yr":ts.dt.year,"wnum":int(w[1:])})
            for h in [1,3,7,14]:
                df["f%d"%h]=c.shift(-h)/c-1
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    out={}
    def clus(s,x,y):
        s=s.dropna(subset=[x,y]).copy()
        s["xz"]=s.groupby("coin")[x].transform(lambda z:(z-z.mean())/z.std())
        s["yz"]=(s[y]-s.groupby("coin")[y].transform("mean"))/s.groupby("coin")[y].transform("std")
        s["p"]=s.xz*s.yz
        d=s.groupby("day").p.sum()
        return d.mean()/d.std()*np.sqrt(len(d)), len(s), len(d), s.p.mean()
    # quintile extremes of vr, day-clustered, 14d grid
    res={}
    for h in [7,14]:
        G=A[(A.pos%h==0)].dropna(subset=["vr","f%d"%h]).copy()
        y="f%d"%h
        G["ex"]=(G[y]-G.groupby("coin")[y].transform("mean"))/G.groupby("coin")[y].transform("std")
        G["q"]=G.groupby("coin").vr.transform(lambda z:pd.qcut(z,5,labels=False))
        for q in [0,4]:
            d=G[G.q==q].groupby("day").ex.sum()
            res["vr h%d q%d"%(h,q)]=[d.mean()/d.std()*np.sqrt(len(d)),len(G[G.q==q]),len(d),G[G.q==q].ex.mean()]
        t,n,nd,cl=clus(G,"vr",y); res["vr slope h%d"%h]=[t,n,nd,cl]
        t,n,nd,cl=clus(G,"vr7",y); res["vr7 slope h%d"%h]=[t,n,nd,cl]
        # split halves of windows
        for lab,sub in [("w1-12",G[G.wnum<=12]),("w13-24",G[G.wnum>12])]:
            t,n,nd,cl=clus(sub,"vr",y); res["vr h%d %s"%(h,lab)]=[t,n,nd,cl]
    out["vr_tests"]=pd.DataFrame(res,index=["t_day","n","days","corr"]).T
    # short reversal: past 1d and 3d return vs next 1,3 days, grid h, day clustered
    res={}
    for x in ["r1","r3"]:
        for h in [1,3,7]:
            G=A[A.pos%h==0]
            t,n,nd,cl=clus(G,x,"f%d"%h); res["%s->f%d"%(x,h)]=[t,n,nd,cl]
    G=A[A.pos%1==0]
    for lab,sub in [("w1-12",G[G.wnum<=12]),("w13-24",G[G.wnum>12])]:
        t,n,nd,cl=clus(sub,"r1","f1"); res["r1->f1 "+lab]=[t,n,nd,cl]
    # r1 scaled by vol20 (surprise)
    A["r1z"]=A.r1/A.vol20
    for h in [1,3]:
        t,n,nd,cl=clus(A[A.pos%h==0],"r1z","f%d"%h); res["r1z->f%d"%h]=[t,n,nd,cl]
    # high-vol regime vs low
    A["vq"]=A.groupby("coin").vol20.transform(lambda z:pd.qcut(z,2,labels=False))
    for q in [0,1]:
        t,n,nd,cl=clus(A[A.vq==q],"r1z","f1"); res["r1z->f1 volhalf%d"%q]=[t,n,nd,cl]
    out["reversal_tests"]=pd.DataFrame(res,index=["t_day","n","days","corr"]).T
    # per coin r1->f1 corr
    out["r1f1_by_coin"]=A.dropna(subset=["r1","f1"]).groupby("coin").apply(lambda s:pd.Series({"corr":s.r1.corr(s.f1),"n":len(s)}))
    out["r1f1_by_year"]=A.dropna(subset=["r1","f1"]).groupby("yr").apply(lambda s:s.groupby("coin").apply(lambda z:z.r1.corr(z.f1)).mean())
    out["vr14_by_coin"]=A[A.pos%14==0].dropna(subset=["vr","f14"]).groupby("coin").apply(lambda s:pd.Series({"corr":s.vr.corr(s.f14),"n":len(s)}))
    return out
