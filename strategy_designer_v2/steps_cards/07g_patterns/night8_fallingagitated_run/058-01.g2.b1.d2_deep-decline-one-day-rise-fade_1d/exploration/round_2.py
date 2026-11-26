def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd=r1.rolling(30,min_periods=20).std()
            out_={}
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                            "inprof":(b["regime"]!="chop").values,
                            "ts":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            for h in [2,3,5,7]:
                d["z%d"%h]=((c/c.shift(h)-1)/(sd*np.sqrt(h))).values
            d["f3"]=(c.shift(-3)/c-1).values
            d["f5"]=(c.shift(-5)/c-1).values
            d["tr60"]=(c/c.shift(60)-1).values
            d["alloc"]=b["postRebalance_current_allocation"].values
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    def clus_t(x,day):
        s=pd.DataFrame({"x":x-x.mean(),"d":day}).groupby("d")["x"].sum()
        G=len(s); se=np.sqrt((s**2).sum()*G/(G-1))/len(x)
        return x.mean()/se, G
    for H,fc in [(3,"f3"),(5,"f5")]:
        G=D[D.pos%H==0].dropna(subset=[fc]).copy()
        G["u"]=G[fc]-G.groupby("coin")[fc].transform("mean")
        P=G[G.inprof]
        res=[]
        for z in ["z2","z3","z5","z7"]:
            Q=P.dropna(subset=[z])
            # slope of u on z, clustered by day
            X=Q[z].values; y=Q["u"].values
            b1=np.cov(X,y)[0,1]/np.var(X,ddof=1)
            a=y.mean()-b1*X.mean(); e=y-a-b1*X
            xc=X-X.mean()
            s=pd.DataFrame({"g":xc*e,"d":Q["ts"]}).groupby("d")["g"].sum()
            se=np.sqrt((s**2).sum()*len(s)/(len(s)-1))/(xc**2).sum()
            top=Q[Q[z]>Q[z].quantile(0.8)]; tt,gd=clus_t(top["u"].values,top["ts"].values)
            pos=Q[Q[z]>0]; tp,gp=clus_t(pos["u"].values,pos["ts"].values)
            res.append({"H":H,"z":z,"n":len(Q),"slope%":b1*100,"t_slope_clu":b1/se,
                        "top20_u%":top["u"].mean()*100,"top20_t_clu":tt,"top20_days":gd,
                        "z>0_u%":pos["u"].mean()*100,"z>0_t":tp,"z>0_days":gp})
        out["inprof_H%d"%H]=pd.DataFrame(res)
    G=D[D.pos%3==0].dropna(subset=["f3","z3"]).copy()
    G["u"]=G["f3"]-G.groupby("coin")["f3"].transform("mean")
    P=G[G.inprof].copy()
    P["q"]=pd.qcut(P["z3"],5,labels=False)
    out["inprof_z3_by_window_top_minus_bottom"]=P.groupby("w").apply(lambda g: pd.Series({"n":len(g),
        "corr":g[["z3","u"]].corr().iloc[0,1],"top%":g[g.q==4]["u"].mean()*100,"bot%":g[g.q==0]["u"].mean()*100}))
    out["inprof_z3_by_coin"]=P.groupby("coin").apply(lambda g: pd.Series({"n":len(g),
        "corr":g[["z3","u"]].corr().iloc[0,1],"top%":g[g.q==4]["u"].mean()*100}))
    O=G[(~G.inprof)].dropna(subset=["tr60"]).copy()
    O["trend"]=np.where(O.tr60>0.1,"rising",np.where(O.tr60<-0.1,"falling","choppy"))
    O["q"]=O.groupby("trend")["z3"].transform(lambda s: pd.qcut(s,5,labels=False))
    g=O.groupby(["trend","q"])["u"]
    out["outprof_trend_z3q"]=pd.DataFrame({"n":g.size(),"mean%":g.mean()*100,"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # book: tested idea's positions vs z3 at entry
    return out
