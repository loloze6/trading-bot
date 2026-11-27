def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values
            n=len(b); rng=h-l
            cl=np.where(rng>0,(c-l)/np.where(rng>0,rng,1),np.nan)
            agit=(b["regime"]!="chop").values
            ts=pd.to_datetime(b["timestamp"])
            rr=rng/c
            rr20=pd.Series(rr).rolling(20).mean().values
            r60=np.r_[[np.nan]*60,c[60:]/c[:-60]-1] if n>60 else np.full(n,np.nan)
            for t in range(n):
                f1=c[t+1]/c[t]-1 if t+1<n else np.nan
                f2=c[t+2]/c[t]-1 if t+2<n else np.nan
                f6=c[t+6]/c[t]-1 if t+6<n else np.nan
                rows.append(dict(coin=coin,w=w,pos=t,cl=cl[t],agit=agit[t],f1=f1,f2=f2,f6=f6,
                    day=ts.iloc[t].normalize(),yr=ts.iloc[t].year,wrel=rr[t]/rr20[t] if rr20[t]>0 else np.nan,r60=r60[t]))
    d=pd.DataFrame(rows)
    for col in ["f1","f2","f6"]:
        h=int(col[1:])
        g=d[d.pos%h==0]
        d["u"+col]=d[col]-d.coin.map(g.groupby("coin")[col].mean())
    def clu(sub,col):
        x=sub.dropna(subset=[col]); v=x[col]
        if len(v)<5: return dict(mean=np.nan,t=np.nan,n=len(v),days=0)
        m=v.mean(); s=(v-m).groupby(x.day).sum(); se=np.sqrt((s**2).sum())/len(v)
        return dict(mean=m,t=m/se,n=len(v),days=x.day.nunique())
    def slope(sub,xc,col):
        x=sub.dropna(subset=[xc,col]); xx=x[xc]-x[xc].mean(); beta=(xx*x[col]).sum()/(xx*xx).sum()
        e=(x[col]-x[col].mean()-beta*xx)*xx; s=e.groupby(x.day).sum(); se=np.sqrt((s**2).sum())/(xx*xx).sum()
        return dict(beta=beta,t=beta/se,n=len(x),days=x.day.nunique())
    a=d[d.agit].copy()
    a["tr"]=pd.cut(a.r60,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    a["wq"]=a.groupby("coin").wrel.transform(lambda s:pd.qcut(s,3,labels=False,duplicates="drop"))
    a["sc"]=a.cl*a.wrel  # not used
    out={}
    R=[]
    for tr in ["fall","chop","rise"]:
        for wq in [0,1,2]:
            sub=a[(a.tr==tr)&(a.wq==wq)]
            r=slope(sub,"cl","uf1"); r.update(tr=tr,wq=wq); R.append(r)
    out["next-day slope of u1 on cl, agit, trend x width"]=pd.DataFrame(R)
    R=[]
    for tr in ["fall","chop","rise"]:
        sub=a[(a.tr==tr)&(a.cl>=0.8)&(a.wq==2)]
        r=clu(sub,"uf1"); r.update(tr=tr,grp="wide hi"); R.append(r)
        sub=a[(a.tr==tr)&(a.cl>=0.8)]
        r=clu(sub,"uf1"); r.update(tr=tr,grp="all hi"); R.append(r)
    out["next-day unusual after high close, agit"]=pd.DataFrame(R)
    # graded: next-day unusual by cl*width signal: (0.5-cl)*wrel
    a["sig"]=(0.5-a.cl)*a.wrel
    R=[]
    for nm,sub in [("all agit",a),("calm",d[~d.agit].assign(sig=lambda x:(0.5-x.cl)*x.wrel))]:
        r=slope(sub,"sig","uf1"); r.update(grp=nm); R.append(r)
    for yr,sub in a.groupby("yr"):
        r=slope(sub,"sig","uf1"); r.update(grp=str(yr)); R.append(r)
    out["slope u1 on (0.5-cl)*width"]=pd.DataFrame(R)
    # wide-day 6-day drift, non-overlapping grid 6
    g=a[a.pos%6==0]
    R=[]
    for wq in [0,1,2]:
        r=clu(g[g.wq==wq],"uf6"); r.update(wq=wq); R.append(r)
    out["u6 by width tercile agit grid6"]=pd.DataFrame(R)
    out["slope u6 on wrel agit grid6"]=pd.Series(slope(g,"wrel","uf6"))
    out["u2 slope on sig agit grid2"]=pd.Series(slope(a[a.pos%2==0],"sig","uf2"))
    return out
