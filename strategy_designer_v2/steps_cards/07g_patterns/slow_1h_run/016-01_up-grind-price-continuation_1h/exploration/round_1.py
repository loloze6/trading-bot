def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[]
    hr=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            ts=pd.to_datetime(b["timestamp"])
            hh=pd.DataFrame({"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":np.r_[c[1:]/c[:-1]-1,np.nan],"coin":coin})
            hr.append(hh)
            n=len(c)
            for t in range(H,n-H,H):
                past=c[t]/c[t-H]-1; fwd=c[t+H]/c[t]-1
                rr=r[t-H+1:t+1]; vv=v[t-H+1:t+1]
                lr=np.log1p(rr)
                net=lr.sum()
                if net>0:
                    top=np.sort(lr)[-3:].sum(); share=1-top/net
                elif net<0:
                    top=np.sort(lr)[:3].sum(); share=1-top/net
                else: share=np.nan
                vsh=np.sort(vv)[-3:].sum()/vv.sum() if vv.sum()>0 else np.nan
                vol=np.nanstd(rr)
                eff=abs(net)/np.abs(lr).sum()
                rows.append(dict(coin=coin,w=w,past=past,fwd=fwd,share=share,vsh=vsh,vol=vol,eff=eff,
                                 up=np.mean(rr>0),fc=b["forecast"].values[t]))
    d=pd.DataFrame(rows).dropna(subset=["fwd","past"])
    out={}
    out["n"]=len(d)
    d["pq"]=d.groupby("coin")["past"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["fwd by past quintile"]=d.groupby("pq")["fwd"].agg(["mean","count",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    for col in ["vol","eff","vsh","up"]:
        d["q"]=d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
        out["fwd by "+col+" quintile"]=d.groupby("q")["fwd"].agg(["mean","count",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    for sgn,name in [(1,"up"),(-1,"down")]:
        s=d[np.sign(d.past)==sgn].copy()
        s["q"]=pd.qcut(s["share"].rank(method="first"),3,labels=False)
        out["fwd by share tercile "+name]=s.groupby("q")[["fwd","past"]].mean().assign(n=s.groupby("q").size())
        s["vq"]=pd.qcut(s["vsh"].rank(method="first"),3,labels=False)
        out["fwd by volconc tercile "+name]=s.groupby("vq")[["fwd","past"]].mean().assign(n=s.groupby("vq").size())
    # slopes per coin: fwd on past
    sl=[]
    for coin,g in d.groupby("coin"):
        res=stats.linregress(g.past,g.fwd); sl.append([coin,res.slope,res.slope/res.stderr,len(g)])
    out["fwd~past per coin"]=pd.DataFrame(sl,columns=["coin","slope","t","n"])
    h=pd.concat(hr).dropna()
    out["by hour"]=h.groupby("hour")["r"].agg(["mean",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["by weekday"]=h.groupby("wd")["r"].agg(["mean",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    return out
