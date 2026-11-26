def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append(pd.Series(b["close"].astype(float).values).pct_change().dropna().values)
        drift=np.concatenate(allr).mean()
        for w,b in ws.items():
            c=pd.Series(b["close"].astype(float).values)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            z1=r/sd
            zs=(z1-z1.rolling(60,min_periods=20).mean())/z1.rolling(60,min_periods=20).std()
            r60=c/c.shift(60)-1
            sdl=r.rolling(90,min_periods=60).std()
            ag=sd/sdl
            r5=c/c.shift(5)-1
            df=pd.DataFrame({"coin":coin,"w":w,"reg":b["regime"].values,"z1":z1,"zs":zs,
                "r60":r60,"ag":ag,"r5":r5,"fc":b["forecast"].astype(float).values,
                "ts":pd.to_datetime(b["timestamp"]).dt.floor("D").values})
            for h in (1,2,3,5):
                df["u%d"%h]=-(c.shift(-h)/c-1-h*drift)
            rows.append(df)
    d=pd.concat(rows)
    def summ(g,col="u1"):
        g=g.dropna(subset=[col]); x=g[col]; n=len(x)
        if n<3: return pd.Series({"n":n,"days":np.nan,"mean":x.mean(),"t_day":np.nan})
        m=x.mean(); dev=g.groupby("ts")[col].apply(lambda s:(s-m).sum()); G=len(dev)
        se=np.sqrt((dev**2).sum()*G/(G-1))/n
        return pd.Series({"n":n,"days":G,"mean":m,"t_day":m/se})
    ip=d[d.reg=="unknown"]
    up=ip[ip.z1>0].copy()
    out={}
    up["fcb"]=pd.cut(up.fc,[-21,-15,-10,-5,-2,0.001])
    out["up in-profile by forecast bucket u1"]=up.groupby("fcb").apply(summ)
    up["zsb"]=pd.cut(up.zs,[-9,0,0.5,1,1.5,2,9])
    out["up in-profile by plan s/10 bucket u1"]=up.groupby("zsb").apply(summ)
    for h in (2,3,5):
        g=up.copy(); g=g[g.groupby(["coin","w"]).cumcount()%h==0]
        out["up in-profile u%d grid"%h]=summ(g,"u%d"%h)
    out["up in-profile by window u1"]=up.groupby("w").apply(summ)
    up["r60b"]=pd.qcut(up.r60,3)
    out["up by 60d return tercile u1"]=up.groupby("r60b").apply(summ)
    up["agb"]=pd.qcut(up.ag,3)
    out["up by 30d/90d swing tercile u1"]=up.groupby("agb").apply(summ)
    up["r5b"]=pd.qcut(up.r5,3)
    out["up by 5d return tercile u1"]=up.groupby("r5b").apply(summ)
    out["share up days next day down"]=float((up.u1>0).mean())
    return out
