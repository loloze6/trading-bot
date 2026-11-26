def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    for H in (5,7,10,15):
        rows=[]
        for coin, ws in data["bars"].items():
            allr=[]
            for w,b in ws.items():
                c=b["close"].values; idx=np.arange(0,len(c)-H,H); allr+=list(c[idx+H]/c[idx]-1)
            dr=np.mean(allr); usd=np.std(allr,ddof=1)
            for w,b in ws.items():
                b=b.reset_index(drop=True); c=b["close"]; lr=c.pct_change()
                sd=lr.rolling(30,min_periods=20).std(); r3=c/c.shift(3)-1; z=r3/sd
                yr=pd.to_datetime(b["timestamp"]).dt.year; n=len(b)
                for i in range(0,n-H,H):
                    if b.loc[i,"regime"]!="unknown" or not (z[i]>0): continue
                    u=-(c[i+H]/c[i]-1-dr)
                    rows.append({"coin":coin,"w":w,"yr":yr[i],"z":z[i],"u":u,"s":u/usd,"tot":-(c[i+H]/c[i]-1),
                                 "share":u/r3[i] if r3[i]>0 else np.nan,"day":str(b.loc[i,"timestamp"])[:10]})
        df=pd.DataFrame(rows)
        def ct(g):
            d=g.groupby("day")["u"].sum(); D=len(d); m=g.u.mean()
            se=np.sqrt(((d-g.u.mean()*g.groupby("day").size())**2).sum()*D/(D-1))/len(g)
            return m/se if se>0 else np.nan
        def summ(g):
            return pd.Series({"n":len(g),"days":g.day.nunique(),"u":g.u.mean(),"t_cl":ct(g) if len(g)>3 else np.nan,
                              "strength":g.s.mean(),"tot":g.tot.mean(),"share_med":g.share.median()})
        df["half"]=np.where(df.z>df.z.median(),"top","bot")
        out[f"H{H}_all"]=summ(df).to_frame().T
        out[f"H{H}_half"]=df.groupby("half").apply(summ)
        out[f"H{H}_year"]=df.groupby("yr").apply(summ)
        out[f"H{H}_corr_z_u"]=float(df[["z","u"]].corr().iloc[0,1])
    return out
