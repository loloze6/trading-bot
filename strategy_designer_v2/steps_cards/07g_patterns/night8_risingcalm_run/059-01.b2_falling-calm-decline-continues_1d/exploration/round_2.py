def explore(data):
    import numpy as np, pandas as pd
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd30=r1.rolling(30).std()
            b["s14"]=(c/c.shift(14)-1)/(sd30*np.sqrt(14))
            b["r60"]=c/c.shift(60)-1
            b["sd30"]=sd30
            b["fwd"]=c.shift(-H)/c-1
            b["inprof"]=(b["regime"]=="unknown").astype(int)
            b["fc"]=b["forecast"]
            ts=pd.to_datetime(b["timestamp"])
            b["yr"]=ts.dt.year; b["day"]=ts.dt.floor("D").astype(str)
            b["coin"]=coin; b["w"]=w
            rows.append(b.iloc[::H])
    d=pd.concat(rows).dropna(subset=["fwd"])
    mu=d.groupby("coin")["fwd"].mean()
    d["ex"]=d["fwd"]-d["coin"].map(mu)
    d["volrank"]=d.groupby("coin")["sd30"].rank(pct=True)
    d["agit"]=(d["volrank"]>0.5).astype(int)
    d["trend"]=np.where(d["r60"]>0.1,"rising",np.where(d["r60"]<-0.1,"falling","choppy"))
    d=d.dropna(subset=["s14","r60"])
    def cl(x,col="s14"):
        x=x.dropna(subset=[col,"ex"])
        n=len(x)
        if n<20: return pd.Series({"n":n,"slope":np.nan,"t_cl":np.nan,"days":np.nan,"mean_ex":np.nan})
        X=np.column_stack([np.ones(n),x[col].values]); y=x["ex"].values
        XtXi=np.linalg.inv(X.T@X); bta=XtXi@X.T@y; e=y-X@bta
        g=x["day"].values; S=np.zeros((2,2)); G=0
        for k in pd.unique(g):
            m=g==k; s=X[m].T@e[m]; S+=np.outer(s,s); G+=1
        V=XtXi@S@XtXi*G/(G-1)*(n-1)/(n-2)
        return pd.Series({"n":n,"slope":bta[1],"t_cl":bta[1]/np.sqrt(V[1,1]),"days":G,"mean_ex":y.mean()})
    out={}
    out["calm vs agit: slope ex on s14 (clustered)"]=d.groupby("agit").apply(cl).round(4)
    out["calm by trend"]=d[d.agit==0].groupby("trend").apply(cl).round(4)
    out["calm by year"]=d[d.agit==0].groupby("yr").apply(cl).round(4)
    out["agit by year"]=d[d.agit==1].groupby("yr").apply(cl).round(4)
    out["calm, s14<0 only"]=pd.DataFrame({"v":cl(d[(d.agit==0)&(d.s14<0)])}).round(4)
    out["calm, s14>0 only"]=pd.DataFrame({"v":cl(d[(d.agit==0)&(d.s14>0)])}).round(4)
    out["agit, s14<0 only"]=pd.DataFrame({"v":cl(d[(d.agit==1)&(d.s14<0)])}).round(4)
    out["calm by coin"]=d[d.agit==0].groupby("coin").apply(cl).round(4)
    ip=d[(d.inprof==1)&(d.s14<0)]
    out["in profile: raw s14 vs forecast"]=pd.DataFrame({"raw":cl(ip,"s14"),"fc":cl(ip,"fc")}).round(4)
    # calm: s14 quintiles clustered mean
    c0=d[d.agit==0].copy(); c0["q"]=pd.qcut(c0["s14"],5,labels=False)
    a=c0.groupby("q")["ex"].agg(["mean","count","std"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["calm s14 quintiles"]=a.round(4)
    a1=d[d.agit==1].copy(); a1["q"]=pd.qcut(a1["s14"],5,labels=False)
    b_=a1.groupby("q")["ex"].agg(["mean","count","std"]); b_["t"]=b_["mean"]/(b_["std"]/np.sqrt(b_["count"]))
    out["agit s14 quintiles"]=b_.round(4)
    return out
