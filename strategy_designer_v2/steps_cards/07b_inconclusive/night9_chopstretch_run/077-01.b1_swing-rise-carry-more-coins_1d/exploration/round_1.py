def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            vsr=(c/c.shift(14)-1)/(r.rolling(30).std()*np.sqrt(14))
            yr=pd.to_datetime(b["timestamp"]).dt.year
            n=len(b)
            for h in (3,7,14):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,i=i,ret=c[i+h]/c[i]-1,vsr=vsr[i],reg=b["regime"][i],yr=yr[i],ts=str(b["timestamp"][i])[:10]))
    d=pd.DataFrame(rows)
    d["drift"]=d.groupby(["coin","h"])["ret"].transform("mean")
    d["un"]=d["ret"]-d["drift"]
    d["inprof"]=d["reg"]!="chop"
    def tclu(g):
        s=g.groupby("ts")["un"].sum(); n=len(g); D=len(s)
        if D<3: return pd.Series(dict(n=n,days=D,mean=g["un"].mean(),t=np.nan))
        m=g["un"].mean(); se=np.sqrt((s-s.mean()*0).pow(2).sum()*0+((g.groupby("ts")["un"].apply(lambda x:(x-m).sum()))**2).sum()*D/(D-1))/n
        return pd.Series(dict(n=n,days=D,mean=m,t=m/se))
    d=d.dropna(subset=["vsr"])
    d["bin"]=pd.cut(d["vsr"],[-99,-3,-2,-1,0,1,2,3,99])
    out={}
    out["inprof_by_bin_h"]=d[d.inprof].groupby(["h","bin"]).apply(tclu)
    out["outprof_by_bin_h7"]=d[(~d.inprof)&(d.h==7)].groupby("bin").apply(tclu)
    a=d[d.inprof&(d.h==7)]
    out["inprof_corr_vsr_un_h7"]=pd.Series({"spearman":a[["vsr","un"]].corr("spearman").iloc[0,1],"n":len(a)})
    out["up_h7_by_coin"]=a[a.vsr>=2].groupby("coin").apply(tclu)
    out["up_h7_by_year"]=a[a.vsr>=2].groupby("yr").apply(tclu)
    out["dn_h7_by_year"]=a[a.vsr<=-2].groupby("yr").apply(tclu)
    out["regcounts"]=d[d.h==7]["reg"].value_counts()
    return out
