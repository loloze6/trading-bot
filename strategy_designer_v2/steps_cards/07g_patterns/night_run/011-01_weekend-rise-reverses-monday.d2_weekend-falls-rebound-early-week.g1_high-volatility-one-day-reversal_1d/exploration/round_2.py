def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        mu=pd.concat([df["close"].astype(float).pct_change() for df in ws.values()]).mean()
        for w,df in ws.items():
            d=df.copy(); c=d["close"].astype(float); r=c.pct_change()
            d["r"]=r; d["nxt"]=c.shift(-1)/c-1-mu
            d["n2"]=c.shift(-2)/c-1-2*mu
            d["mabs"]=r.abs().shift(1).rolling(60,min_periods=20).mean()
            d["z"]=r/d["mabs"]
            d["volratio"]=r.rolling(20).std()/d["mabs"]
            d["r2"]=c/c.shift(2)-1
            d["z2"]=d["r2"]/(d["mabs"]*np.sqrt(2))
            d["wd"]=pd.to_datetime(d["timestamp"]).dt.dayofweek
            d["coin"]=coin; d["w"]=w
            rows.append(d[["coin","w","r","nxt","n2","z","z2","volratio","wd"]])
    A=pd.concat(rows).dropna(subset=["nxt","z","volratio"])
    def tab(g,col):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    A["vq"]=pd.qcut(A["volratio"],3,labels=False)
    A["side"]=np.where(A["z"]<0,"down","up")
    A["aq"]=A.groupby("side")["z"].transform(lambda s:pd.qcut(s.abs(),3,labels=False))
    out["nxt by side x volratio x |z| tercile"]=A.groupby(["side","vq","aq"]).apply(lambda g:tab(g,"nxt"))
    A["wkend"]=A["wd"].isin([5,6])
    out["nxt by side x weekend (|z| top third within side)"]=A[A["aq"]==2].groupby(["side","wkend"]).apply(lambda g:tab(g,"nxt"))
    S=A[A["wd"]==6].dropna(subset=["z2","n2"]).copy()
    S["q"]=pd.qcut(S["z2"],5,labels=False)
    out["Mon-Tue (2d) ret by Sat+Sun scaled move quintile"]=S.groupby("q").apply(lambda g:tab(g,"n2"))
    T=A[A["wd"]==3].dropna(subset=["z2","n2"]).copy()
    T["q"]=pd.qcut(T["z2"],5,labels=False)
    out["Fri-Sat (2d) ret by Wed+Thu scaled move quintile"]=T.groupby("q").apply(lambda g:tab(g,"n2"))
    out["down side top |z| high vol, by year-window half"]=A[(A["side"]=="down")&(A["vq"]==2)].assign(h=lambda x:x["w"].str[1:].astype(int)>12).groupby("h").apply(lambda g:tab(g,"nxt"))
    return out
