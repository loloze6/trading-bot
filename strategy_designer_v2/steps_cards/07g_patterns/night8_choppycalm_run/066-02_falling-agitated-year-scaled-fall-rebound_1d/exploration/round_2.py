def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            if len(b)<5: continue
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                "ret":r,"nxt":c.shift(-1)/c-1,"nxt2":(c.shift(-2)/c-1),
                "reg":b["regime"].astype(str),
                "sd30":r.rolling(30,min_periods=20).std(),
                "tr60":c/c.shift(60)-1,
                "cl":(b["close"]-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)})
            d["yr"]=d["ts"].dt.year
            rows.append(d)
    P=pd.concat(rows,ignore_index=True)
    drift=P.groupby("coin")["ret"].mean()
    P["ex"]=P["nxt"]-P["coin"].map(drift)
    P["ex2"]=P["nxt2"]-2*P["coin"].map(drift)
    P["z30"]=P["ret"]/P["sd30"]
    P["day"]=P["ts"].dt.floor("D")
    def ct(df,col):
        df=df.dropna(subset=[col]); n=len(df)
        if n<5: return pd.Series({"n":n,"mean":np.nan,"t":np.nan,"days":0})
        m=df[col].mean(); g=(df[col]-m).groupby(df["day"]).sum()
        se=np.sqrt((g**2).sum())/n
        return pd.Series({"n":n,"mean":m,"t":m/se if se>0 else np.nan,"days":df["day"].nunique()})
    def slope(df,x,y):
        df=df.dropna(subset=[x,y]); n=len(df)
        if n<20: return pd.Series({"n":n,"slope":np.nan,"t":np.nan})
        X=df[x]-df[x].mean(); Y=df[y]
        b=(X*Y).sum()/(X**2).sum(); a=Y.mean()-b*df[x].mean()
        e=Y-a-b*df[x]
        g=(X*e).groupby(df["day"]).sum()
        se=np.sqrt((g**2).sum())/(X**2).sum()
        return pd.Series({"n":n,"slope":b,"t":b/se,"days":df["day"].nunique()})
    out={}
    inn=P[P["reg"]=="unknown"].dropna(subset=["z30"])
    up=inn[inn["ret"]>0]
    out["in up days: mean ex"]=ct(up,"ex")
    out["in up days: slope ex on z30"]=slope(up,"z30","ex")
    out["in up days: by year"]=up.groupby("yr").apply(lambda g:ct(g,"ex"))
    out["in up days: by close loc"]=up.dropna(subset=["cl"]).groupby(pd.cut(up["cl"],[0,0.5,0.8,1.0001],include_lowest=True),observed=True).apply(lambda g:ct(g,"ex"))
    out["in up days: 2-day ex"]=ct(up,"ex2")
    out["in falls: slope ex on z30"]=slope(inn[inn["ret"]<0],"z30","ex")
    o=P[(P["reg"]!="unknown")].dropna(subset=["z30","tr60"])
    fc=o[o["tr60"]<-0.1]
    out["out falling(calm) up: slope"]=slope(fc[fc["ret"]>0],"z30","ex")
    out["out falling(calm) all: slope"]=slope(fc,"z30","ex")
    out["out falling(calm) up by yr"]=fc[fc["ret"]>0].groupby("yr").apply(lambda g:ct(g,"ex"))
    ri=o[o["tr60"]>0.1]
    out["out rising falls: slope"]=slope(ri[ri["ret"]<0],"z30","ex")
    out["out rising falls<=-1 by yr"]=ri[ri["z30"]<=-1].groupby("yr").apply(lambda g:ct(g,"ex"))
    out["out rising falls<=-1 by coin"]=ri[ri["z30"]<=-1].groupby("coin").apply(lambda g:ct(g,"ex"))
    return out
