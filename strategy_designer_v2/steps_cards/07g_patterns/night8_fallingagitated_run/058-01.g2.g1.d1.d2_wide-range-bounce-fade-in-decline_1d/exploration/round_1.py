def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["r1"]=r; d["r3"]=c/c.shift(3)-1; d["r5"]=c/c.shift(5)-1
            sd=r.rolling(30,min_periods=20).std()
            d["sd"]=sd
            d["rr"]=((b["high"]-b["low"])/c)/sd
            d["clv"]=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            d["z1"]=r/sd; d["z3"]=d["r3"]/(sd*np.sqrt(3))
            d["f1"]=c.shift(-1)/c-1
            d["inFA"]=b["regime"]!="chop"
            d["fc"]=b["forecast"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["f1"].mean()
    D["u"]=D["f1"]-D["coin"].map(drift)
    D["day"]=D["ts"].dt.floor("D")
    def st(g):
        g=g.dropna(subset=["u"])
        if len(g)<10: return pd.Series({"n":len(g),"mean_u":np.nan,"t_day":np.nan})
        s=g.groupby("day")["u"].sum(); G=len(s)
        t=s.sum()/np.sqrt((s**2).sum()*G/(G-1)) if G>1 else np.nan
        return pd.Series({"n":len(g),"days":G,"mean_u":g["u"].mean(),"t_day":t})
    D["sit"]=np.select([(D.r1>0)&(D.r3<0),(D.r1>0)&(D.r3>=0),(D.r1<=0)&(D.r3<0)],["up_r3neg","up_r3pos","dn_r3neg"],"dn_r3pos")
    out={}
    out["drift"]=drift
    out["sit_by_profile"]=D.groupby(["inFA","sit"]).apply(st)
    D["rrq"]=D.groupby(["inFA","sit"])["rr"].transform(lambda x: pd.qcut(x,3,labels=False,duplicates="drop"))
    out["sit_rr_tercile"]=D.groupby(["inFA","sit","rrq"]).apply(st)
    D["z3q"]=D.groupby("inFA")["z3"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["z3_quintile"]=D.groupby(["inFA","z3q"]).apply(st)
    D["z1q"]=D.groupby("inFA")["z1"].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
    out["z1_quintile"]=D.groupby(["inFA","z1q"]).apply(st)
    up=D[D.r1>0].copy()
    up["clvq"]=pd.cut(up["clv"],[-0.01,0.33,0.66,1.01],labels=["lowc","midc","highc"])
    out["up_clv"]=up.groupby(["inFA","clvq"]).apply(st)
    out["weekday_FA"]=D[D.inFA].groupby(D.ts.dt.weekday).apply(st)
    out["share_FA"]=D.inFA.mean()
    act=D[D.fc!=0]
    out["active_by_coin"]=act.groupby("coin").apply(st)
    out["active_by_window"]=act.groupby("w").apply(st)
    return out
