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
            r=np.r_[np.nan,c[1:]/c[:-1]-1]
            absm=pd.Series(np.abs(r)).rolling(180,min_periods=45).mean().values
            ret30=np.full(n,np.nan)
            if n>180: ret30[180:]=c[180:]/c[:-180]-1
            vol6=pd.Series(v).rolling(6).mean().values; vol30=pd.Series(v).rolling(180,min_periods=45).mean().values
            sl=np.zeros(n); start=0
            for i in range(1,n):
                if c[i]<c[i-1]:
                    if not(i>1 and c[i-1]<c[i-2]): start=i-1
                    sl[i]=c[i]/c[start]-1
            ts=pd.to_datetime(b["timestamp"])
            # all down-close bars, one per 36-bar grid cell
            seen=set()
            for i in range(1,n-36):
                if c[i]<c[i-1] and not np.isnan(ret30[i]):
                    cell=i//36
                    if cell in seen: continue
                    seen.add(cell)
                    d={"coin":coin,"year":ts.iloc[i].year,"ret30":ret30[i],
                       "slu":-sl[i]/absm[i] if absm[i]>0 else np.nan,"vr":vol6[i]/vol30[i]}
                    for h in H:
                        d[f"l{h}"]=(c[i+h]/c[i]-1-drift[coin][h][0])  # long side, drift-adjusted
                        d[f"s{h}"]=d[f"l{h}"]/drift[coin][h][1]
                        d[f"tot{h}"]=c[i+h]/c[i]-1
                    rows.append(d)
    D=pd.DataFrame(rows)
    def summ(g):
        out={}
        for h in H:
            x=g[f"s{h}"].dropna()
            out[f"str{h}"]=x.mean(); out[f"t{h}"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        out["n"]=len(g); out["unus36%"]=g["l36"].mean()*100; out["tot36%"]=g["tot36"].mean()*100
        return pd.Series(out)
    res={}
    D["r30d"]=pd.qcut(D["ret30"],10,labels=False)
    res["long_by_ret30_decile_all_downbars"]=D.groupby("r30d").apply(summ).join(D.groupby("r30d")["ret30"].mean())
    neg=D[D["ret30"]<0].copy()
    for h in [18,36]:
        m=neg[["ret30",f"s{h}"]].dropna(); s=stats.linregress(m["ret30"],m[f"s{h}"])
        res[f"neg_month_slope_long_s{h}"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(m)})
    m=D[["ret30","s36"]].dropna(); s=stats.linregress(m["ret30"],m["s36"])
    res["all_month_slope_long_s36"]=pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(m)})
    deep=D[D["ret30"]<D["ret30"].quantile(0.2)]
    res["deep20_by_coin"]=deep.groupby("coin").apply(summ)
    res["deep20_by_year"]=deep.groupby("year").apply(summ)
    deep=deep.copy(); deep["slq"]=pd.qcut(deep["slu"],3,labels=False,duplicates="drop")
    res["deep20_by_streakloss_tercile"]=deep.groupby("slq").apply(summ)
    deep["vrq"]=pd.qcut(deep["vr"],3,labels=False)
    res["deep20_by_volratio_tercile"]=deep.groupby("vrq").apply(summ)
    up=D[D["ret30"]>D["ret30"].quantile(0.8)]
    res["top20_month"]=summ(up)
    return res
