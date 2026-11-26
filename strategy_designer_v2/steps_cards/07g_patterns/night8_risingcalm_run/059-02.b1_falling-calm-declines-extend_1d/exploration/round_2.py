def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            sd30=r.rolling(30,min_periods=20).std()
            hi14=c.rolling(14).max()
            df=pd.DataFrame({"coin":coin,"win":w,"fc":b["forecast"],"reg":b["regime"],
                "depth":(c-hi14)/hi14/sd30,"ret60":(c/c.shift(60)-1)*100,
                "ret14z":(c/c.shift(14)-1)/sd30,
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "yr":pd.to_datetime(b["timestamp"]).dt.year,"f5":c.shift(-5)/c-1})
            df["grid"]=(np.arange(len(df))%5==0)
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    drift=A[A.grid].groupby("coin")["f5"].mean()
    A["u5"]=A["f5"]-A["coin"].map(drift)
    G=A[A.grid].dropna(subset=["u5"])
    def slope_t(g,x):
        g=g.dropna(subset=[x,"u5"])
        X=g[x]-g[x].mean(); y=g["u5"]-g["u5"].mean()
        b=(X*y).sum()/(X*X).sum(); e=y-b*X
        s=(X*e).groupby(g["day"]).sum()
        se=np.sqrt((s**2).sum())/(X*X).sum()
        return pd.Series({"n":len(g),"days":g["day"].nunique(),"slope":b,"t":b/se})
    out={}
    U=G[G.reg=="unknown"]
    out["FC slope: depth raw"]=slope_t(U,"depth").round(4)
    out["FC slope: forecast"]=slope_t(U[U.fc<0],"fc").round(4)
    out["FC slope: ret14z"]=slope_t(U,"ret14z").round(4)
    U2=U.copy(); U2["deep"]=U2["depth"]<U2["depth"].median()
    out["FC deep half by year"]=U2.groupby(["yr","deep"])["u5"].agg(["size","mean"]).round(4)
    out["FC deep half by coin"]=U2.groupby(["coin","deep"])["u5"].agg(["size","mean"]).round(4)
    out["corr depth vs fc (FC)"]=float(U[["depth","fc"]].corr().iloc[0,1])
    C=G[G.reg=="chop"].copy()
    C["tr"]=np.where(C.ret60>10,"rising",np.where(C.ret60<-10,"falling","choppy"))
    C.loc[C.ret60.isna(),"tr"]="na"
    out["chop by trend: depth slope"]=C.groupby("tr").apply(lambda g: slope_t(g,"depth")).round(4)
    out["chop by trend: ret14z slope"]=C.groupby("tr").apply(lambda g: slope_t(g,"ret14z")).round(4)
    out["all: ret14z slope"]=slope_t(G,"ret14z").round(4)
    return out
