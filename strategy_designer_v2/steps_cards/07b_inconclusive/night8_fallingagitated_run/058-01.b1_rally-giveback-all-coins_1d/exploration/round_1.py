def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drift={}
    for coin, ws in data["bars"].items():
        allr={h:[] for h in (1,3,5,10)}
        for w, b in ws.items():
            c=b["close"].values
            for h in allr:
                idx=np.arange(0,len(c)-h,h)
                allr[h]+=list(c[idx+h]/c[idx]-1)
        dr={h:np.mean(v) for h,v in allr.items()}
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; lr=c.pct_change()
            sd=lr.rolling(30,min_periods=20).std()
            r3=c/c.shift(3)-1
            z=r3/sd
            yr=pd.to_datetime(b["timestamp"]).dt.year
            n=len(b)
            for i in range(0,n-5,5):
                if b.loc[i,"regime"]!="unknown": continue
                if not (z[i]>0): continue
                d={"coin":coin,"w":w,"yr":yr[i],"z":z[i],"r3":r3[i],"fc":b.loc[i,"forecast"],"day":str(b.loc[i,"timestamp"])[:10]}
                for h in (1,3,5,10):
                    if i+h<n: d[f"u{h}"]=-(c[i+h]/c[i]-1-dr[h])
                rows.append(d)
    df=pd.DataFrame(rows)
    df["q"]=pd.qcut(df["z"],4,labels=["q1","q2","q3","q4"])
    def summ(g):
        return pd.Series({"n":len(g),"u1":g.u1.mean(),"u3":g.u3.mean(),"u5":g.u5.mean(),"t5":stats.ttest_1samp(g.u5.dropna(),0).statistic if len(g)>2 else np.nan,"u10":g.u10.mean(),"zmean":g.z.mean()})
    out={}
    out["all"]=summ(df).to_frame().T
    out["by_zquart"]=df.groupby("q").apply(summ)
    out["by_year"]=df.groupby("yr").apply(summ)
    out["by_coin"]=df.groupby("coin").apply(summ)
    out["by_window"]=df.groupby("w").apply(summ)
    out["corr_z_u5"]=float(df[["z","u5"]].corr().iloc[0,1])
    out["fc_strong"]=df.assign(s=df.fc<=-2).groupby("s").apply(summ)
    return out
