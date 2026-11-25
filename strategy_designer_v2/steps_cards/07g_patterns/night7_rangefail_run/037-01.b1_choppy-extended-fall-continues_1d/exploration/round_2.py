def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            vol20=r.rolling(20).std()
            z=(c/c.shift(5)-1)/(vol20*np.sqrt(5))
            r20=c/c.shift(20)-1; r60=c/c.shift(60)-1
            r1z=r/vol20
            vol30=r.rolling(30).std(); volrel=vol30/vol30.rolling(60,min_periods=30).median()
            f5=c.shift(-5)/c-1; f1=c.shift(-1)/c-1; f2=c.shift(-2)/c-1
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"r20":r20,"r60":r60,"r1z":r1z,
                "volrel":volrel,"f5":f5,"f1":f1,"f2":f2,"day":ts.dt.floor("D"),"yr":ts.dt.year}))
    A=pd.concat(rows)
    A["u1"]=A.f1-A.groupby("coin").f1.transform("mean")
    g2=A[A.pos%2==0].copy(); g2["u2"]=g2.f2-g2.groupby("coin").f2.transform("mean")
    g=A[A.pos%5==0].copy(); g["u5"]=g.f5-g.groupby("coin").f5.transform("mean")
    def ct(df,col):
        x=df[[col,"day"]].dropna(); n=len(x)
        if n<5: return pd.Series({"n":n,"days":x.day.nunique(),"mean%":np.nan,"tcl":np.nan})
        m=x[col].mean(); s=(x[col]-m).groupby(x.day).sum(); D=len(s)
        se=np.sqrt((s**2).sum()*D/(D-1))/n
        return pd.Series({"n":n,"days":D,"mean%":m*100,"tcl":m/se})
    out={}
    A["r1b"]=pd.cut(A.r1z,[-99,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,99])
    out["u1 by 1d z, clustered"]=A.dropna(subset=["r1b"]).groupby("r1b",observed=True).apply(lambda d: ct(d,"u1")).round(3)
    dn=A[A.r1z<=-1.5]
    out["u1 after 1d z<=-1.5 by window"]=dn.groupby("w").apply(lambda d: ct(d,"u1")).round(3)
    A["trend"]=pd.cut(A.r60,[-9,-.1,.1,99],labels=["fall","chop","rise"])
    A["vb"]=np.where(A.volrel>1,"agit","calm")
    out["u1 after 1d z<=-1.5 by trend x agit"]=A[A.r1z<=-1.5].dropna(subset=["trend"]).groupby(["trend","vb"],observed=True).apply(lambda d: ct(d,"u1")).round(3)
    g2["r1b"]=pd.cut(g2.r1z,[-99,-2,-1,0,1,2,99])
    out["u2 (2-day grid) by 1d z"]=g2.dropna(subset=["r1b"]).groupby("r1b",observed=True).apply(lambda d: ct(d,"u2")).round(3)
    sub=A[A.r1z<0].dropna(subset=["u1","r1z"])
    sl=stats.linregress(sub.r1z,sub.u1)
    out["slope u1 on r1z for down days"]=f"slope {sl.slope*100:.3f}%/z, t {sl.slope/sl.stderr:.2f}, n {len(sub)}"
    by=A[A.r1z<=-1.5].groupby("coin").apply(lambda d: ct(d,"u1")).round(3)
    out["u1 after 1d z<=-1.5 by coin"]=by
    ch=g[(g.trend if "trend" in g else pd.cut(g.r60,[-9,-.1,.1,99],labels=["fall","chop","rise"]))=="chop"] if False else g[(g.r60.abs()<=.1)&(g.r20<0)&(g.z<0)]
    out["chop r20neg z<0 u5 clustered"]=ct(ch,"u5").round(3)
    out["same by window"]=ch.groupby("w").apply(lambda d: ct(d,"u5")).round(3)
    return out
