import numpy as np, pandas as pd

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sma=c.rolling(20).mean()
            sd=r.rolling(20).std()
            z=((c-sma)/sma)/sd
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,
                "tr60":c/c.shift(60)-1,"volrel":sd/r.rolling(60).std(),
                "f5":c.shift(-5)/c-1,"choppy":(b["regime"]=="unknown"),
                "yr":ts.dt.year,"day":ts.dt.floor("D")})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    m5=D[D.pos%5==0].groupby("coin")["f5"].mean()
    s5=D[D.pos%5==0].groupby("coin")["f5"].std()
    D["x5"]=D["f5"]-D["coin"].map(m5)
    D["s"]=D["x5"]/D["coin"].map(s5)
    G=D[(D.pos%5==0)&D.x5.notna()&D.z.notna()].copy()
    G["trd"]=np.where(G.tr60>0.1,"rise",np.where(G.tr60<-0.1,"fall",np.where(G.tr60.notna(),"chop","na")))
    def creg(g,xcol="z",ycol="x5"):
        g=g[[xcol,ycol,"day"]].dropna()
        if len(g)<20: return pd.Series({"n":len(g),"days":0,"slope":np.nan,"t":np.nan})
        x=g[xcol]-g[xcol].mean(); y=g[ycol]
        b1=(x*y).sum()/(x*x).sum(); a=y.mean()-b1*g[xcol].mean()
        e=y-a-b1*g[xcol]
        sc=(x*e).groupby(g["day"]).sum()
        v=(sc**2).sum()/((x*x).sum()**2)
        nd=len(sc); v*=nd/(nd-1)
        return pd.Series({"n":len(g),"days":nd,"slope":b1,"t":b1/np.sqrt(v)})
    out={}
    out["slope z all"]=creg(G).round(5)
    out["slope z by trend"]=G.groupby("trd").apply(creg).round(5)
    out["slope z by window"]=G.groupby("w").apply(creg).round(5)
    out["slope z by coin"]=G.groupby("coin").apply(creg).round(5)
    out["slope z by year"]=G.groupby("yr").apply(creg).round(5)
    out["slope z pos side by trend"]=G[G.z>0].groupby("trd").apply(creg).round(5)
    out["slope z neg side by trend"]=G[G.z<0].groupby("trd").apply(creg).round(5)
    G["agit"]=np.where(G.volrel>1,"agit","calm")
    out["slope z by agit"]=G.groupby("agit").apply(creg).round(5)
    out["slope z by trend x agit"]=G.groupby(["trd","agit"]).apply(creg).round(5)
    out["slope volrel by trend (strength)"]=G.groupby("trd").apply(lambda g: creg(g,"volrel","x5")).round(5)
    out["mean strength z sign"]=G.assign(sg=np.sign(G.z)).groupby("sg")["s"].agg(["mean","count"]).round(4)
    return out
