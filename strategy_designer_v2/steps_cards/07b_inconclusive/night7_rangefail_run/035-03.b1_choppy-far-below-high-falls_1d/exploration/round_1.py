def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drift={}
    H=[1,3,5,10,20]
    for coin,ws in data["bars"].items():
        # drift per horizon: non-overlapping grid across windows
        for h in H:
            rs=[]
            for w,b in ws.items():
                c=b["close"].values
                for i in range(0,len(c)-h,h):
                    rs.append(c[i+h]/c[i]-1)
            drift[(coin,h)]=(np.mean(rs),np.std(rs,ddof=1))
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            r=c.pct_change()
            hi=c.shift(1).rolling(20).max()
            sd=r.rolling(20).std()
            depth=(c/hi-1)/sd
            pct=(c/hi-1)
            tr60=(c/c.shift(60)-1)*100
            vol30=r.rolling(30).std()
            ret5p=c/c.shift(5)-1
            f=b["forecast"].values
            n=len(b)
            for g in range(0,n,5):
                for i in range(g,min(g+5,n)):
                    if f[i]<=-2:
                        d=dict(coin=coin,w=w,year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                               fc=f[i],depth=depth.iloc[i],pct=pct.iloc[i],tr60=tr60.iloc[i],
                               vol=sd.iloc[i],ret5p=ret5p.iloc[i],
                               day=str(pd.Timestamp(b["timestamp"].iloc[i]).date()))
                        for h in H:
                            if i+h<n:
                                m,s=drift[(coin,h)]
                                d[f"x{h}"]=-(c.iloc[i+h]/c.iloc[i]-1-m)
                                d[f"t{h}"]=-(c.iloc[i+h]/c.iloc[i]-1)
                        rows.append(d); break
    df=pd.DataFrame(rows)
    def summ(g):
        out={}
        for h in H:
            x=g[f"x{h}"].dropna()
            out[f"x{h}"]=x.mean()
        x=g["x5"].dropna()
        out["n"]=len(x); out["t5"]=x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan
        out["tot5"]=g["t5"].mean()
        return pd.Series(out)
    res={}
    res["all"]=summ(df)
    df["fq"]=pd.qcut(df["fc"].abs(),4,labels=False,duplicates="drop")
    df["dq"]=pd.qcut(df["depth"],4,labels=False,duplicates="drop")
    df["pq"]=pd.qcut(df["pct"],4,labels=False,duplicates="drop")
    df["trq"]=pd.qcut(df["tr60"],4,labels=False,duplicates="drop")
    df["volq"]=pd.qcut(df["vol"],4,labels=False,duplicates="drop")
    df["r5q"]=pd.qcut(df["ret5p"],4,labels=False,duplicates="drop")
    for k in ["fq","dq","pq","trq","volq","r5q","coin","w","year"]:
        res[k]=df.groupby(k).apply(summ)
    res["corr_fc_depth"]=float(df[["fc","depth"]].corr().iloc[0,1])
    res["q_ranges"]=pd.DataFrame({k:df.groupby(k)[v].median() for k,v in [("dq","depth"),("pq","pct"),("trq","tr60"),("volq","vol"),("r5q","ret5p")]})
    return res
