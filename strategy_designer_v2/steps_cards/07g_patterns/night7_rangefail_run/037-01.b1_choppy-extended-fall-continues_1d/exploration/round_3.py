def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            vol20=r.rolling(20).std()
            z=(c/c.shift(5)-1)/(vol20*np.sqrt(5))
            r20=c/c.shift(20)-1; r60=c/c.shift(60)-1
            vol30=r.rolling(30).std(); volrel=vol30/vol30.rolling(60,min_periods=30).median()
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"r20":r20,"r60":r60,
                "r1z":r/vol20,"volrel":volrel,"f1":c.shift(-1)/c-1,"f2":c.shift(-2)/c-1,"f5":c.shift(-5)/c-1,
                "day":ts.dt.floor("D"),"yr":ts.dt.year}))
    A=pd.concat(rows)
    A["u1"]=A.f1-A.groupby("coin").f1.transform("mean")
    g2=A[A.pos%2==0].copy(); g2["u2"]=g2.f2-g2.groupby("coin").f2.transform("mean")
    g=A[A.pos%5==0].copy(); g["u5"]=g.f5-g.groupby("coin").f5.transform("mean")
    def cslope(df,x,y):
        d=df[[x,y,"day"]].dropna(); n=len(d)
        if n<10: return pd.Series({"n":n,"days":np.nan,"slope%":np.nan,"tcl":np.nan})
        xc=d[x]-d[x].mean(); b=(xc*d[y]).sum()/(xc**2).sum(); a=d[y].mean()-b*d[x].mean()
        e=d[y]-a-b*d[x]; s=(xc*e).groupby(d.day).sum(); D=len(s)
        se=np.sqrt((s**2).sum()*D/(D-1))/(xc**2).sum()
        return pd.Series({"n":n,"days":D,"slope%":b*100,"tcl":b/se})
    out={}
    dn=A[A.r1z<0].copy(); dn["mag"]=-dn.r1z
    dn["vb"]=np.where(dn.volrel>1,"agit","calm")
    dn["trend"]=pd.cut(dn.r60,[-9,-.1,.1,99],labels=["fall","chop","rise"])
    out["u1 on down-day size, all"]=cslope(dn,"mag","u1").round(3)
    out["u1 on down-day size by agit"]=dn.groupby("vb").apply(lambda d: cslope(d,"mag","u1")).round(3)
    out["u1 on down-day size by trend"]=dn.dropna(subset=["trend"]).groupby("trend",observed=True).apply(lambda d: cslope(d,"mag","u1")).round(3)
    out["u1 on down-day size by year"]=dn.groupby("yr").apply(lambda d: cslope(d,"mag","u1")).round(3)
    dn2=g2[g2.r1z<0].copy(); dn2["mag"]=-dn2.r1z
    out["u2 on down-day size (2d grid)"]=cslope(dn2,"mag","u2").round(3)
    up=A[A.r1z>0].copy()
    out["u1 on up-day size"]=cslope(up,"r1z","u1").round(3)
    ch=g[(g.r60.abs()<=.1)&(g.r20<0)&(g.z<0)].copy(); ch["mag"]=-ch.z
    out["theme: u5 on 5d fall size, chop r20<0"]=cslope(ch,"mag","u5").round(3)
    ch2=g[(g.r60.abs()<=.1)&(g.z<0)].copy(); ch2["mag"]=-ch2.z
    out["theme: u5 on 5d fall size, chop any r20"]=cslope(ch2,"mag","u5").round(3)
    return out
