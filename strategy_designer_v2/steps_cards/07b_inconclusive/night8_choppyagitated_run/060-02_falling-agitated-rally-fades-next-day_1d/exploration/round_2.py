def explore(data):
    import pandas as pd, numpy as np
    bars=data["bars"]
    mu={}
    for c,ws in bars.items():
        mu[c]=pd.concat([b["close"].pct_change().dropna() for b in ws.values()]).mean()
    rows=[]
    for c,ws in bars.items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            sd=r.rolling(30).std()
            d=pd.DataFrame({"timestamp":b["timestamp"],"sc":r/sd,"r0":r,
                "f1":cl.shift(-1)/cl-1,"f3":cl.shift(-3)/cl-1,
                "tr60":cl/cl.shift(60)-1,"tr10":cl.shift(1)/cl.shift(11)-1,
                "wick":(b["high"]-b["close"])/(b["high"]-b["low"]).replace(0,np.nan),
                "rng":(b["high"]-b["low"])/cl.shift(1)/sd,
                "prof":b["regime"]=="unknown","fc":b["forecast"]})
            d["coin"]=c
            d["x1"]=-(d["f1"]-mu[c]); d["x3"]=-(d["f3"]-3*mu[c])
            rows.append(d[d["prof"]&(d["fc"]<0)])
    cs=pd.concat(rows,ignore_index=True).dropna(subset=["x1","sc"])
    def ct(s,ts):
        g=pd.DataFrame({"v":s,"t":ts}).dropna().groupby("t")["v"].sum()
        n=s.dropna().shape[0]; m=s.dropna().mean()
        se=g.std(ddof=1)*np.sqrt(len(g))/n
        return m, m/se, n
    def slope(x,y,ts):
        df=pd.DataFrame({"x":x,"y":y,"t":ts}).dropna()
        X=np.c_[np.ones(len(df)),df["x"]]; beta=np.linalg.lstsq(X,df["y"],rcond=None)[0]
        e=df["y"]-X@beta; XtXi=np.linalg.inv(X.T@X)
        S=np.zeros((2,2))
        for _,g in df.assign(e=e).groupby("t"):
            Xg=np.c_[np.ones(len(g)),g["x"]]; u=Xg.T@g["e"].values; S+=np.outer(u,u)
        V=XtXi@S@XtXi
        return beta[1], beta[1]/np.sqrt(V[1,1]), len(df)
    out={}
    tab=[]
    for name,x in [("sc",cs["sc"]),("raw r0",cs["r0"]),("wick share",cs["wick"]),("range/sd",cs["rng"]),
                   ("tr60",cs["tr60"]),("tr10 before",cs["tr10"]),("sc low 80%",cs["sc"].where(cs["sc"]<cs["sc"].quantile(0.8)))]:
        for h in ("x1","x3"):
            s,t,n=slope(x,cs[h],cs["timestamp"]); tab.append([name,h,s,t,n])
    out["slopes"]=pd.DataFrame(tab,columns=["x","y","slope","t","n"])
    for col,k in [("wick",4),("tr60",4),("tr10",4)]:
        q=pd.qcut(cs[col],k,labels=False); tab=[]
        for i,g in cs.groupby(q):
            m,t,n=ct(g["x1"],g["timestamp"]); m3,t3,_=ct(g["x3"],g["timestamp"])
            tab.append([i,g[col].mean(),g["sc"].mean(),m,t,m3,t3,n])
        out[f"by {col} quartile"]=pd.DataFrame(tab,columns=["q",col,"sc","m1","t1","m3","t3","n"])
    top=cs[cs["sc"]>=cs["sc"].quantile(0.8)]
    tab=[]
    for col in ("wick","tr10"):
        q=pd.qcut(top[col],2,labels=False)
        for i,g in top.groupby(q):
            m,t,n=ct(g["x1"],g["timestamp"]); tab.append([col,i,g[col].mean(),m,t,n])
    out["top sc quintile split"]=pd.DataFrame(tab,columns=["by","half","val","m1","t1","n"])
    return out
