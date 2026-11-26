def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            f=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),
                "z0":r/sd,"width":(b["high"]-b["low"])/c/sd,
                "loc":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "tr60":c/c.shift(60)-1,"sd":sd,"nxt":c.shift(-1)/c-1,
                "reg":b["regime"].astype(str)})
            rows.append(f)
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["nxt"].mean(); d["ex"]=d["nxt"]-d["coin"].map(mu)
    d["day"]=d["ts"].dt.floor("D"); d["yr"]=d["ts"].dt.year
    d["fc_prof"]=d["reg"].isin(["unknown","mean_reversion"])
    d=d.dropna(subset=["z0","ex"])
    def summ(g,col="ex"):
        if len(g)<15: return pd.Series({"n":len(g)})
        s=g.groupby("day")[col].sum(); nd=len(s)
        return pd.Series({"n":len(g),"days":nd,"mean%":100*g[col].mean(),
                          "t_day":s.mean()/(s.std(ddof=1)/np.sqrt(nd))})
    out={}
    out["regime counts"]=d["reg"].value_counts()
    d["zb"]=pd.cut(d["z0"],[-100,-1.5,-0.5,0.5,1.5,100])
    out["falling calm profile: own move z"]=d[d.fc_prof].groupby("zb").apply(summ)
    out["outside profile: own move z"]=d[~d.fc_prof].groupby("zb").apply(summ)
    fc=d[d.fc_prof]
    def slope(g):
        if len(g)<30: return pd.Series({"n":len(g)})
        x=g["z0"].clip(-4,4); y=g["ex"]
        s=stats.linregress(x,y)
        return pd.Series({"n":len(g),"slope%":100*s.slope,"t":s.slope/s.stderr})
    out["falling calm slope ex on z by year"]=fc.groupby("yr").apply(slope)
    out["falling calm slope ex on z all"]=slope(fc)
    out["outside slope"]=slope(d[~d.fc_prof])
    up=fc[fc.z0>0]
    up["lb"]=pd.cut(up["loc"],[-0.01,0.5,0.75,1.01])
    out["falling calm up days by close loc"]=up.groupby("lb").apply(summ)
    up["wb"]=pd.cut(up["width"],[0,1.5,2.5,100])
    out["falling calm up days by width"]=up.groupby("wb").apply(summ)
    out["falling calm up days z>0.5 by coin"]=fc[fc.z0>0.5].groupby("coin").apply(summ)
    out["falling calm up days z>0.5 by window"]=fc[fc.z0>0.5].groupby("w").apply(summ)["mean%"]
    return out
