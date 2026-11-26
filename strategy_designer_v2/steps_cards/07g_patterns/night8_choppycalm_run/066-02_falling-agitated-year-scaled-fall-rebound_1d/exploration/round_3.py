def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            if len(b)<5: continue
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                "ret":r,"nxt":c.shift(-1)/c-1,"nxt2":c.shift(-2)/c-1,
                "reg":b["regime"].astype(str),
                "sd30":r.rolling(30,min_periods=20).std(),
                "tr60":c/c.shift(60)-1,
                "cl":(b["close"]-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)})
            d["yr"]=d["ts"].dt.year
            rows.append(d)
    P=pd.concat(rows,ignore_index=True)
    drift=P.groupby("coin")["ret"].mean()
    sdall=P.groupby("coin")["ret"].std()
    P["ex"]=P["nxt"]-P["coin"].map(drift)
    P["ex2"]=P["nxt2"]-2*P["coin"].map(drift)
    P["z30"]=P["ret"]/P["sd30"]
    P["zall"]=P["ret"]/P["coin"].map(sdall)
    P["relvol"]=P["sd30"]/P["coin"].map(sdall)
    P["day"]=P["ts"].dt.floor("D")
    def ct(df,col):
        df=df.dropna(subset=[col]); n=len(df)
        if n<5: return pd.Series({"n":n,"mean":np.nan,"t":np.nan,"days":0})
        m=df[col].mean(); g=(df[col]-m).groupby(df["day"]).sum()
        se=np.sqrt((g**2).sum())/n
        return pd.Series({"n":n,"mean":m,"t":m/se if se>0 else np.nan,"days":df["day"].nunique()})
    def slope(df,x,y):
        df=df.dropna(subset=[x,y]); n=len(df)
        if n<20: return pd.Series({"n":n,"slope":np.nan,"t":np.nan,"days":0})
        X=df[x]-df[x].mean(); Y=df[y]
        b=(X*Y).sum()/(X**2).sum(); a=Y.mean()-b*df[x].mean()
        e=Y-a-b*df[x]
        g=(X*e).groupby(df["day"]).sum()
        se=np.sqrt((g**2).sum())/(X**2).sum()
        return pd.Series({"n":n,"slope":b,"t":b/se,"days":df["day"].nunique()})
    out={}
    o=P[P["reg"]!="unknown"].dropna(subset=["z30","tr60"])
    ri=o[o["tr60"]>0.1].copy()
    rf=ri[ri["ret"]<0].copy()
    rf["b"]=pd.cut(rf["z30"],[-99,-2,-1.5,-1,-0.5,0])
    out["rising falls: ex by z30 bin"]=rf.groupby("b",observed=True).apply(lambda g:ct(g,"ex"))
    out["rising falls: 2-day ex by z30 bin"]=rf.groupby("b",observed=True).apply(lambda g:ct(g,"ex2"))
    rf["vol"]=np.where(rf["relvol"]>rf["relvol"].median(),"hi","lo")
    out["rising falls<=-1 by relvol"]=rf[rf["z30"]<=-1].groupby("vol").apply(lambda g:ct(g,"ex"))
    out["rising falls slope z30 by relvol"]=rf.groupby("vol").apply(lambda g:slope(g,"z30","ex"))
    out["rising falls slope zall"]=slope(rf,"zall","ex")
    out["rising falls<=-1 by close loc"]=rf[rf["z30"]<=-1].dropna(subset=["cl"]).groupby(pd.cut(rf["cl"],[0,0.33,0.66,1.0001],include_lowest=True),observed=True).apply(lambda g:ct(g,"ex"))
    inn=P[P["reg"]=="unknown"].dropna(subset=["z30"])
    up=inn[inn["ret"]>0].copy()
    up["b"]=pd.cut(up["z30"],[0,0.5,1,2,99])
    out["in up days by z30 bin"]=up.groupby("b",observed=True).apply(lambda g:ct(g,"ex"))
    out["in up days by coin"]=up.groupby("coin").apply(lambda g:ct(g,"ex"))
    return out
