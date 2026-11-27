def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].values; o=b["open"].values; h=b["high"].values; l=b["low"].values
            r=pd.Series(c).pct_change().values
            nxt=np.r_[c[1:]/c[:-1]-1,np.nan]
            nxt2=np.r_[c[2:]/c[:-2]-1,np.nan,np.nan]
            run=np.zeros(len(c),int); k=0
            for i in range(len(c)):
                if i>0 and r[i]<0: k+=1
                else: k=0
                run[i]=k
            prevrun=np.r_[0,run[:-1]]
            sd20=pd.Series(r).rolling(20).std().values
            ret20=np.r_[[np.nan]*20,c[20:]/c[:-20]-1] if len(c)>20 else np.full(len(c),np.nan)
            z20=ret20/(sd20*np.sqrt(20))
            ret60=np.r_[[np.nan]*60,c[60:]/c[:-60]-1] if len(c)>60 else np.full(len(c),np.nan)
            rng=(h-l)/c
            clpos=(c-l)/np.where(h>l,h-l,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame(dict(coin=coin,w=w,r=r,nxt=nxt,nxt2=nxt2,prevrun=prevrun,z20=z20,ret60=ret60,
                sd20=sd20,rng=rng,clpos=clpos,reg=b["regime"].values,wd=ts.dt.weekday.values,yr=ts.dt.year.values,
                alloc=b["postRebalance_current_allocation"].values,fc=b["forecast"].values,day=ts.dt.floor("D").values))
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    mu=d.groupby("coin")["nxt"].mean(); d["ex"]=d["nxt"]-d["coin"].map(mu)
    d["sdz"]=d["r"]/d["sd20"]
    d["fc_prof"]=d["reg"].isin(["trending","unknown"])
    def summ(g,col="ex"):
        x=g[col].dropna(); 
        if len(x)<3: return pd.Series(dict(n=len(x),mean=np.nan,t=np.nan))
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x)))))
    out={}
    out["regime counts"]=d["reg"].value_counts()
    brk=d[(d.r>0)&(d.prevrun>=1)].copy()
    brk["rb"]=brk.prevrun.clip(upper=5)
    out["break by run, all"]=brk.groupby("rb").apply(summ)
    out["break by run, fallcalm"]=brk[brk.fc_prof].groupby("rb").apply(summ)
    out["break by run, ret60<-10%"]=brk[brk.ret60<-0.1].groupby("rb").apply(summ)
    brk["zq"]=pd.qcut(brk.z20,5,labels=False,duplicates="drop")
    out["break by z20 quint"]=brk.groupby("zq").apply(summ)
    d["sdzq"]=pd.qcut(d.sdz,10,labels=False,duplicates="drop")
    out["next ex by today sd-scaled ret decile"]=d.groupby("sdzq").apply(summ)
    d["zq"]=pd.qcut(d.z20,10,labels=False,duplicates="drop")
    out["next ex by z20 decile"]=d.groupby("zq").apply(summ)
    d["vq"]=pd.qcut(d.rng/d.sd20,5,labels=False,duplicates="drop")
    out["next ex by range/sd quint"]=d.groupby("vq").apply(summ)
    d["cq"]=pd.qcut(d.clpos,5,labels=False,duplicates="drop")
    out["next ex by close pos quint"]=d.groupby("cq").apply(summ)
    out["next ex by weekday"]=d.groupby("wd").apply(summ)
    out["next ex by run length (down days so far)"]=d.assign(rl=np.where(d.r<0,d.prevrun+1,0).clip(max=6)).groupby("rl").apply(summ)
    d["t60"]=pd.cut(d.ret60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    out["next ex by 60d trend x dir"]=d.groupby(["t60",d.r>0]).apply(summ)
    dd=data["days"]; br=[]
    for coin,ws in dd.items():
        for w,x in ws.items(): br.append(x.assign(coin=coin))
    br=pd.concat(br); out["book days nonzero"]=pd.Series(dict(n=(br.book_return.abs()>1e-9).sum(),mean=br.book_return[br.book_return.abs()>1e-9].mean()))
    tr=[]
    for coin,ws in data["trades"].items():
        for w,x in ws.items():
            if len(x): tr.append(x.assign(coin=coin))
    tr=pd.concat(tr); out["trades by coin"]=tr.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","sum"])
    return out
