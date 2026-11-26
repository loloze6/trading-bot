def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vsr=(c/c.shift(14)-1)/(r.rolling(30).std()*np.sqrt(14))
            reg=b["regime"].astype(str)
            n=len(b)
            for h in (3,7,14):
                fwd=c.shift(-h)/c-1
                for i in range(0,n,h):
                    rows.append(dict(coin=coin,w=w,h=h,i=i,ts=b["timestamp"].iloc[i],fwd=fwd.iloc[i],
                                     vsr=vsr.iloc[i],reg=reg.iloc[i],fc=float(b["forecast"].iloc[i])))
    d=pd.DataFrame(rows).dropna(subset=["fwd"])
    d["drift"]=d.groupby(["coin","h"])["fwd"].transform("mean")
    d["usual"]=d.groupby(["coin","h"])["fwd"].transform("std")
    d["un"]=d["fwd"]-d["drift"]
    d["day"]=pd.to_datetime(d["ts"]).dt.floor("D")
    d["inprof"]=d["reg"].isin(["trending","unknown"])
    def tday(x):
        s=x.groupby("day")["un"].sum(); G=len(s)
        if G<3: return np.nan
        m=x["un"].mean(); dev=x["un"]-m
        sd=dev.groupby(x["day"]).sum()
        se=np.sqrt((sd**2).sum()*G/(G-1))/len(x)
        return m/se
    def summ(g):
        return pd.Series(dict(n=len(g),days=g["day"].nunique(),mean_un=g["un"].mean(),
                              strength=(g["un"]/g["usual"]).mean(),t=tday(g)))
    d["bucket"]=pd.cut(d["vsr"],[-np.inf,-1.5,-1,-0.5,0,0.5,1,1.5,np.inf])
    out={}
    p=d[d.inprof]
    out["inprofile_by_vsr_bucket_h"]=p.groupby(["h","bucket"],observed=True).apply(summ)
    out["outprofile_by_vsr_bucket_h7"]=d[(~d.inprof)&(d.h==7)].groupby("bucket",observed=True).apply(summ)
    tr=d[(d.reg=="trending")&(d.h==7)]
    out["trending_h7_by_coin"]=tr.groupby("coin").apply(summ)
    out["trending_h7_by_window"]=tr.groupby("w").apply(summ)
    tr2=tr.copy(); tr2["fq"]=pd.qcut(tr2["fc"].rank(method="first"),3,labels=["lo","mid","hi"])
    out["trending_h7_by_forecast_tercile"]=tr2.groupby("fq",observed=True).apply(summ)
    out["trending_h7_corr_fc_un"]=float(tr[["fc","un"]].corr().iloc[0,1])
    out["trending_h7_corr_vsr_un"]=float(tr[["vsr","un"]].corr().iloc[0,1])
    out["regime_share"]=d[d.h==1 if False else d.h==7]["reg"].value_counts(normalize=True)
    return out
