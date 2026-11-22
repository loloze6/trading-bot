def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[6,18,36]
    rows=[]; drift={}
    for coin,ws in data["bars"].items():
        allr={h:[] for h in H}
        for w,b in ws.items():
            c=b["close"].values.astype(float); n=len(c)
            for h in H:
                idx=np.arange(0,n-h,h); allr[h]+=list(c[idx+h]/c[idx]-1)
        drift[coin]={h:(np.mean(allr[h]),np.std(allr[h])) for h in H}
        for w,b in ws.items():
            c=b["close"].values.astype(float); n=len(c)
            v=b["volume"].values.astype(float)
            f=b["forecast"].values.astype(float)
            r=np.r_[np.nan,c[1:]/c[:-1]-1]
            absm=pd.Series(np.abs(r)).rolling(180,min_periods=45).mean().values
            ret30=np.r_[[np.nan]*180,c[180:]/c[:-180]-1] if n>180 else np.full(n,np.nan)
            vol6=pd.Series(v).rolling(6).mean().values; vol30=pd.Series(v).rolling(180,min_periods=45).mean().values
            # streak loss
            sl=np.zeros(n); start=0; L=np.zeros(n)
            for i in range(1,n):
                if c[i]<c[i-1]:
                    if not(i>1 and c[i-1]<c[i-2]): start=i-1
                    sl[i]=c[i]/c[start]-1; L[i]=i-start
            df=np.r_[0,np.diff(f)]
            seen=set()
            for i in range(n-18):
                if df[i]<=-2:
                    cell=i//18
                    if cell in seen: continue
                    seen.add(cell)
                    d={"coin":coin,"w":w,"year":b["timestamp"].iloc[i].year if hasattr(b["timestamp"].iloc[i],"year") else pd.Timestamp(b["timestamp"].iloc[i]).year,
                       "ret30":ret30[i],"slu":-sl[i]/absm[i] if absm[i]>0 else np.nan,"len":L[i],"vr":vol6[i]/vol30[i]}
                    for h in H:
                        if i+h<n:
                            d[f"u{h}"]=-(c[i+h]/c[i]-1-drift[coin][h][0])
                            d[f"s{h}"]=d[f"u{h}"]/drift[coin][h][1]
                    rows.append(d)
    D=pd.DataFrame(rows)
    def summ(g):
        out={}
        for h in H:
            x=g[f"s{h}"].dropna()
            out[f"str{h}"]=x.mean(); out[f"t{h}"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        out["n"]=len(g); out["u18%"]=g["u18"].mean()*100
        return pd.Series(out)
    res={}
    res["all"]=summ(D)
    D["r30q"]=pd.qcut(D["ret30"],5,labels=False)
    res["by_ret30_quintile"]=D.groupby("r30q").apply(summ).join(D.groupby("r30q")["ret30"].mean())
    D["slq"]=pd.qcut(D["slu"],5,labels=False,duplicates="drop")
    res["by_streakloss_quintile"]=D.groupby("slq").apply(summ).join(D.groupby("slq")["slu"].mean())
    res["by_coin"]=D.groupby("coin").apply(summ)
    res["by_year"]=D.groupby("year").apply(summ)
    D["vrq"]=pd.qcut(D["vr"],3,labels=False)
    res["by_volratio_tercile"]=D.groupby("vrq").apply(summ)
    res["ret30q_x_slq_str18"]=D.pivot_table(index="r30q",columns=pd.qcut(D["slu"],3,labels=False,duplicates="drop"),values="s18",aggfunc="mean")
    res["ret30q_x_slq_n"]=D.pivot_table(index="r30q",columns=pd.qcut(D["slu"],3,labels=False,duplicates="drop"),values="s18",aggfunc="count")
    m=D[["ret30","s18"]].dropna(); sl_=stats.linregress(m["ret30"],m["s18"])
    res["slope_s18_on_ret30"]=pd.Series({"slope":sl_.slope,"t":sl_.slope/sl_.stderr,"n":len(m)})
    m=D[["ret30","s36"]].dropna(); sl_=stats.linregress(m["ret30"],m["s36"])
    res["slope_s36_on_ret30"]=pd.Series({"slope":sl_.slope,"t":sl_.slope/sl_.stderr,"n":len(m)})
    return res
