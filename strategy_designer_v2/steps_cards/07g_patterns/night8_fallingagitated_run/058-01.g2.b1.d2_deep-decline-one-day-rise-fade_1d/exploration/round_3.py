def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd=r1.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                            "inprof":(b["regime"]!="chop").values,
                            "ts":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            for h in [3,5]:
                d["z%d"%h]=((c/c.shift(h)-1)/(sd*np.sqrt(h))).values
            d["f3"]=(c.shift(-3)/c-1).values
            d["f5"]=(c.shift(-5)/c-1).values
            d["tr60"]=(c/c.shift(60)-1).values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    def clus_t(x,day):
        s=pd.DataFrame({"x":x-x.mean(),"d":day}).groupby("d")["x"].sum()
        G=len(s); se=np.sqrt((s**2).sum()*G/(G-1))/len(x)
        return x.mean()/se, G
    def slope(Q,z,u="u"):
        X=Q[z].values; y=Q[u].values
        b1=np.cov(X,y)[0,1]/np.var(X,ddof=1)
        a=y.mean()-b1*X.mean(); e=y-a-b1*X; xc=X-X.mean()
        s=pd.DataFrame({"g":xc*e,"d":Q["ts"].values}).groupby("d")["g"].sum()
        se=np.sqrt((s**2).sum()*len(s)/(len(s)-1))/(xc**2).sum()
        return b1, b1/se, len(s)
    res=[]; byw=[]
    for H,fc in [(3,"f3"),(5,"f5")]:
        G=D[D.pos%H==0].dropna(subset=[fc,"tr60","z3","z5"]).copy()
        G["u"]=G[fc]-G.groupby("coin")[fc].transform("mean")
        G["trend"]=np.where(G.tr60>0.1,"rising",np.where(G.tr60<-0.1,"falling","choppy"))
        G["set"]=np.where(G.inprof,"falling_agit",G["trend"]+"_calm/other")
        for st,Q in G.groupby("set"):
            for z in ["z3","z5"]:
                b1,t,nd=slope(Q,z)
                lo=Q[Q[z]<Q[z].quantile(0.2)]; hi=Q[Q[z]>Q[z].quantile(0.8)]
                tl,_=clus_t(lo["u"].values,lo["ts"].values); th,_=clus_t(hi["u"].values,hi["ts"].values)
                tu,_=clus_t(Q["f"+str(H)].values if False else Q[fc].values,Q["ts"].values)
                res.append({"H":H,"set":st,"z":z,"n":len(Q),"days":nd,"slope%":b1*100,"t_clu":t,
                            "low20_u%":lo["u"].mean()*100,"low_t":tl,"hi20_u%":hi["u"].mean()*100,"hi_t":th,
                            "raw_mean%":Q[fc].mean()*100,"raw_t":tu})
        F=G[G.set=="falling_calm/other"]
        for w,Q in F.groupby("w"):
            if len(Q)>=8:
                byw.append({"H":H,"w":w,"n":len(Q),"corr_z3":Q[["z3","u"]].corr().iloc[0,1],
                            "corr_z5":Q[["z5","u"]].corr().iloc[0,1]})
    out["slopes_by_set"]=pd.DataFrame(res)
    out["falling_calm_by_window"]=pd.DataFrame(byw)
    return out
