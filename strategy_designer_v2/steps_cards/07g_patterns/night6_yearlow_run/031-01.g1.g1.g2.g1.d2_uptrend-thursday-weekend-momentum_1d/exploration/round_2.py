def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            d=pd.DataFrame({"coin":coin,"win":w,"wd":ts.dt.weekday.values,"year":ts.dt.year.values,
                            "day":ts.dt.floor("D").values})
            d["pos"]=np.arange(len(b))
            d["r1"]=(c.shift(-1)/c-1).values
            d["r2"]=(c.shift(-2)/c-1).values
            d["up60"]=(c/c.shift(60)-1).values
            d["rise14"]=(c/c.shift(14)-1).values
            d["rise7"]=(c/c.shift(7)-1).values
            d["past1"]=(c/c.shift(1)-1).values
            lr=np.log(c).diff()
            d["vol20"]=lr.rolling(20).std().values
            d["z1"]=d["past1"]/d["vol20"]
            d["z14"]=d["rise14"]/(d["vol20"]*np.sqrt(14))
            d["z7"]=d["rise7"]/(d["vol20"]*np.sqrt(7))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    g2=D[D.pos%2==0].groupby("coin")["r2"].mean()
    g1=D.groupby("coin")["r1"].mean()
    D["x2"]=D["r2"]-D["coin"].map(g2)
    D["x1"]=D["r1"]-D["coin"].map(g1)
    D["upc"]=np.where(D.up60.isna(),"na",np.where(D.up60>0,"up","down"))
    def cslope(s,x,y):
        s=s.dropna(subset=[x,y])
        X=np.column_stack([np.ones(len(s)),s[x].values]); Y=s[y].values
        if len(s)<30: return pd.Series({"slope":np.nan,"t":np.nan,"n":len(s),"days":0})
        XtX=np.linalg.inv(X.T@X); b=XtX@X.T@Y; e=Y-X@b
        sc=pd.DataFrame(X*e[:,None]).groupby(s["day"].values).sum().values
        G=len(sc); N=len(s)
        V=XtX@(sc.T@sc)@XtX*G/(G-1)*(N-1)/(N-2)
        return pd.Series({"slope":b[1],"t":b[1]/np.sqrt(V[1,1]),"n":N,"days":G})
    out={}
    out["clustered slope x2~z14 by wd (all regimes)"]=D.groupby("wd").apply(lambda s:cslope(s,"z14","x2")).round(4)
    out["clustered slope x2~z14 by wd x up"]=D[D.upc!="na"].groupby(["upc","wd"]).apply(lambda s:cslope(s,"z14","x2")).round(4)
    out["clustered slope x1~z14 by wd (next day)"]=D.groupby("wd").apply(lambda s:cslope(s,"z14","x1")).round(4)
    out["clustered slope x1~z7 by wd"]=D.groupby("wd").apply(lambda s:cslope(s,"z7","x1")).round(4)
    out["clustered slope x1~z1 by wd"]=D.groupby("wd").apply(lambda s:cslope(s,"z1","x1")).round(4)
    D["abs_z1"]=D["z1"].abs()
    out["clustered slope x1~|z1| all"]=cslope(D,"abs_z1","x1").round(5).to_frame().T
    # Wed-Fri pooled momentum stability by year, x1 on z14, days wd in 2,3,4
    M=D[D.wd.isin([2,3,4])]
    out["x1~z14 Wed-Fri by year"]=M.groupby("year").apply(lambda s:cslope(s,"z14","x1")).round(4)
    out["x1~z14 Sat-Tue by year"]=D[~D.wd.isin([2,3,4])].groupby("year").apply(lambda s:cslope(s,"z14","x1")).round(4)
    out["x1~z14 Wed-Fri by coin"]=M.groupby("coin").apply(lambda s:cslope(s,"z14","x1")).round(4)
    return out
