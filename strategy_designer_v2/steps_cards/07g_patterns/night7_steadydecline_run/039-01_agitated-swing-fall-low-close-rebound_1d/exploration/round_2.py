def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            cl=(b["high"]-c)/rng
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r":r,"z":r/sd,"cl":cl,"agit":(b["regime"]!="chop"),"f":b["forecast"],
                "n1":c.shift(-1)/c-1,"n2":c.shift(-2)/c-1,"rngz":(b["high"]-b["low"])/c/sd})
            d["g2"]=np.arange(len(d))%2==0
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["x1"]=D["n1"]-D.groupby("coin")["n1"].transform("mean")
    mu2=D[D.g2].groupby("coin")["n2"].mean(); D["x2"]=D["n2"]-D["coin"].map(mu2)
    def dayt(g,col="x1"):
        g=g.dropna(subset=[col]); s=g.groupby("day")[col].sum(); n=len(s)
        return pd.Series({"cases":len(g),"days":n,"mean%":100*g[col].mean(),
            "t_day":s.mean()/(s.std()/np.sqrt(n)) if n>2 else np.nan})
    out={}
    A=D[D.agit]; C=D[~D.agit]
    A_dn=A[A.r<0].copy()
    A_dn["zb"]=pd.cut(A_dn.z,[-99,-2.5,-2,-1.5,-1,-0.5,0])
    out["agit down: z bins, day-clustered next1"]=A_dn.groupby("zb").apply(dayt)
    out["agit down: z bins next2 (grid)"]=A_dn[A_dn.g2].groupby("zb").apply(lambda g:dayt(g,"x2"))
    big=A_dn[A_dn.z<=-1.5].copy(); big["clh"]=np.where(big.cl>0.7,"near low","mid/high")
    out["agit z<=-1.5 by close location"]=big.groupby("clh").apply(dayt)
    sm=A_dn[A_dn.z>-1].copy(); sm["clh"]=np.where(sm.cl>0.7,"near low","mid/high")
    out["agit -1<z<0 by close location"]=sm.groupby("clh").apply(dayt)
    C_dn=C[C.r<0].copy(); C_dn["zb"]=pd.cut(C_dn.z,[-99,-2.5,-2,-1.5,-1,-0.5,0])
    out["calm down: z bins next1"]=C_dn.groupby("zb").apply(dayt)
    A_up=A[A.r>0].copy(); A_up["zb"]=pd.cut(A_up.z,[0,0.5,1,1.5,2,99])
    out["agit up: z bins next1"]=A_up.groupby("zb").apply(dayt)
    A_up["clb"]=pd.cut(A_up.cl,[-0.01,0.2,0.5,1.01])
    out["agit up: close loc next1"]=A_up.groupby("clb").apply(dayt)
    out["agit z<=-2 by coin"]=A_dn[A_dn.z<=-2].groupby("coin").apply(dayt)
    out["agit z<=-1.5 by year"]=A_dn[A_dn.z<=-1.5].assign(y=lambda q:q.day.dt.year).groupby("y").apply(dayt)
    A_dn["rb"]=pd.qcut(A_dn.rngz,4,labels=False)
    out["agit down: range in sd quartile next1"]=A_dn.groupby("rb").apply(dayt)
    D["wd"]=D.day.dt.weekday
    out["weekday by agit next1 day-clustered"]=D.groupby(["agit","wd"]).apply(dayt)
    return out
