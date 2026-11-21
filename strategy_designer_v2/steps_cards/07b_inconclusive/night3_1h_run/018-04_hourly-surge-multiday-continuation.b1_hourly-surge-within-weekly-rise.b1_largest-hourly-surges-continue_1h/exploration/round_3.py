def explore(data):
    import numpy as np, pandas as pd
    H=[120,240]
    rows=[]; prow=[]; drift={}
    for coin,ws in data["bars"].items():
        for h in H:
            rr=[]
            for w,b in ws.items():
                c=b["close"].values; idx=np.arange(0,len(c)-h,h); rr+=list(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=np.mean(rr); drift[(coin,h,'sd')]=np.std(rr)
        for w,b in ws.items():
            c=b["close"].values; f=b["forecast"].fillna(0).values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            s=pd.Series(c)
            r24=s.pct_change(24); ratio=(r24/r24.abs().rolling(720,min_periods=120).mean()).values
            r168=s.pct_change(168).values; r720=s.pct_change(720).values
            n=len(c)
            for st in range(0,n,120):
                e=min(st+120,n); lo=np.inf
                for i in range(st,e):
                    lo=min(lo,f[i])
                    if f[i]>=2 and f[i]-lo>=2:
                        d={"coin":coin,"year":yr[i],"ratio":ratio[i],"r720":r720[i]}
                        for h in H:
                            d["x%d"%h]=(c[i+h]/c[i]-1-drift[(coin,h)]) if i+h<n else np.nan
                            d["tot%d"%h]=(c[i+h]/c[i]-1) if i+h<n else np.nan
                        rows.append(d); break
                # price-only: first bar in cell with ratio>=2 regardless of week
                for i in range(st,e):
                    if np.isfinite(ratio[i]) and ratio[i]>=2:
                        d={"coin":coin,"year":yr[i],"ratio":ratio[i],"wk_up":bool(r168[i]>0) if np.isfinite(r168[i]) else np.nan,"r720":r720[i]}
                        for h in H:
                            d["x%d"%h]=(c[i+h]/c[i]-1-drift[(coin,h)]) if i+h<n else np.nan
                            d["tot%d"%h]=(c[i+h]/c[i]-1) if i+h<n else np.nan
                        prow.append(d); break
    df=pd.DataFrame(rows); pf=pd.DataFrame(prow)
    def summ(g):
        out={}
        for h in H:
            x=g["x%d"%h].dropna(); out["m%d"%h]=x.mean(); out["t%d"%h]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
            out["tot%d"%h]=g["tot%d"%h].mean()
        out["n"]=len(g); return pd.Series(out)
    big=df[df.ratio>=2].copy()
    big["half"]=np.where(big.year<=2021,"2018-21","2022-25")
    big["mo"]=np.where(big.r720>0,"r30d_up","r30d_down")
    small=df[df.ratio<2]
    pf["half"]=np.where(pf.year<=2021,"2018-21","2022-25")
    return {"big_all":summ(big).to_frame().T,"small_all":summ(small).to_frame().T,
            "big_by_half":big.groupby("half").apply(summ),
            "big_by_30d":big.groupby("mo").apply(summ),
            "big_by_coin":big.groupby("coin").apply(summ),
            "price_ratio2_by_week":pf.groupby("wk_up").apply(summ),
            "price_ratio2_by_half":pf.groupby("half").apply(summ)}
