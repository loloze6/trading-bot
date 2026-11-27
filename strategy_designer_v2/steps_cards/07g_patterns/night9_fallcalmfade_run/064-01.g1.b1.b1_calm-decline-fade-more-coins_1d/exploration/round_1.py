def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std()
            zr=r/sd
            tr60=c/c.shift(60)-1
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"zr":zr,"r":r,
                             "tr60":tr60,"regime":b["regime"].values,
                             "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                             "yr":pd.to_datetime(b["timestamp"]).dt.year,
                             "rng":(b["high"]-b["low"])/c,"clpos":(c-b["low"])/(b["high"]-b["low"])})
            for h in [1,2,3,5]:
                df[f"f{h}"]=c.shift(-h)/c-1
            df["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    drift={h:A.groupby("coin")[f"f{h}"].mean() for h in [1,2,3,5]}
    for h in [1,2,3,5]:
        A[f"u{h}"]=A[f"f{h}"]-A["coin"].map(drift[h])
    def tstat(sub,col,h):
        s=sub[sub["pos"]%h==0].dropna(subset=[col])
        g=s.groupby("day")[col].sum()
        n=len(s)
        if n<5: return (n,np.nan,np.nan)
        m=s[col].mean()
        se=g.std(ddof=1)*np.sqrt(len(g))/n
        return (n,m,m/se if se>0 else np.nan)
    out={}
    A["trend"]=pd.cut(A["tr60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    A["zb"]=pd.cut(A["zr"],[-99,-2,-1,-0.3,0.3,1,2,99])
    res=[]
    for tr in ["fall","chop","rise"]:
        for zb in A["zb"].cat.categories:
            s=A[(A.trend==tr)&(A.zb==zb)]
            for h in [1,3,5]:
                n,m,t=tstat(s,f"u{h}",h)
                res.append([tr,str(zb),h,n,m,t])
    out["trend_x_zr_unusual"]=pd.DataFrame(res,columns=["trend","zr","h","n","mean","t"])
    res=[]
    tg=A[A.regime=="trending"]
    for h in [1,2,3,5]:
        n,m,t=tstat(tg,f"u{h}",h); res.append(["trending_all",h,n,m,t])
        for lab,s in [("clpos_hi",tg[tg.clpos>0.7]),("clpos_lo",tg[tg.clpos<=0.7]),("zr>2",tg[tg.zr>2]),("zr1-2",tg[tg.zr<=2])]:
            n,m,t=tstat(s,f"u{h}",h); res.append([lab,h,n,m,t])
    out["trending_cases"]=pd.DataFrame(res,columns=["grp","h","n","mean","t"])
    out["regime_counts"]=A["regime"].value_counts()
    res=[]
    for wd in range(7):
        n,m,t=tstat(A[A.wd==wd],"u1",1); res.append([wd,n,m,t])
    out["weekday_u1"]=pd.DataFrame(res,columns=["wd","n","mean","t"])
    # by year trending cases
    res=[]
    for y,s in tg.groupby("yr"):
        n,m,t=tstat(s,"u1",1); res.append([y,n,m,t])
    out["trending_year"]=pd.DataFrame(res,columns=["yr","n","mean","t"])
    return out
