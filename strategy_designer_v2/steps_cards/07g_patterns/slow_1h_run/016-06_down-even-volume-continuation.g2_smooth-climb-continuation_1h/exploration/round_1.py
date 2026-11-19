def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[]; hr=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
            r=np.r_[np.nan,c[1:]/c[:-1]-1]
            ts=pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":r}))
            n=len(c)
            for t in range(0,n,H):
                if t<H or t+H>=n: continue
                pr=r[t-H+1:t+1]; pv=v[t-H+1:t+1]
                if np.isnan(pr).any(): continue
                s=np.abs(pr).sum()
                if s<=0: continue
                vs=pv.sum()
                rows.append(dict(coin=coin,w=w,past=c[t]/c[t-H]-1,fwd=c[t+H]/c[t]-1,
                    er=abs(c[t]/c[t-H]-1)/s if False else abs(np.log(c[t]/c[t-H]))/np.abs(np.log1p(pr)).sum(),
                    jump=np.abs(pr).max()/s, top3=np.sort(np.abs(pr))[-3:].sum()/s,
                    vtop3=(np.sort(pv)[-3:].sum()/vs) if vs>0 else np.nan,
                    vol=pr.std(), past24=c[t]/c[t-24]-1,
                    vrel=pv[-24:].mean()/pv.mean() if vs>0 else np.nan))
    g=pd.DataFrame(rows)
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    # per-coin z of features
    for f in ["past","er","jump","top3","vtop3","vol","past24","vrel"]:
        g["z_"+f]=g.groupby("coin")[f].transform(lambda x:(x-x.mean())/x.std())
    g["zex"]=g.groupby("coin")["ex"].transform(lambda x:x/x.std())
    def ols(df,f):
        d=df[[f,"zex"]].dropna()
        s=stats.linregress(d[f],d["zex"]); return pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(d)})
    out={}
    tab={}
    for name,sub in [("all",g),("up",g[g.past>0]),("down",g[g.past<=0])]:
        for f in ["z_past","z_er","z_jump","z_top3","z_vtop3","z_vol","z_past24","z_vrel"]:
            tab[(name,f)]=ols(sub,f)
    out["pooled slopes zex on z-feature"]=pd.DataFrame(tab).T
    # signed past by coin
    pc={}
    for coin,sub in g.groupby("coin"):
        pc[coin]=pd.Series({"t_past":ols(sub,"z_past")["t"],"t_vol":ols(sub,"z_vol")["t"],"t_past24":ols(sub,"z_past24")["t"],"n":len(sub)})
    out["by coin t"]=pd.DataFrame(pc).T
    g["pq"]=g.groupby("coin")["past"].transform(lambda x:pd.qcut(x,5,labels=False))
    out["fwd ex by past quintile"]=g.groupby("pq")["ex"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    g["vq"]=g.groupby("coin")["vol"].transform(lambda x:pd.qcut(x,5,labels=False))
    out["fwd ex by vol quintile"]=g.groupby("vq")["ex"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    h=pd.concat(hr).dropna()
    out["hour"]=h.groupby("hour")["r"].agg(["mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["weekday"]=h.groupby("wd")["r"].agg(["mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    # book daily
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    D=pd.concat(dd); D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    bk=D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    bk["wd"]=pd.to_datetime(bk["day"]).dt.weekday
    out["book by weekday"]=bk.groupby("wd")[["book_return","coin_return"]].mean()
    out["book by window"]=bk.groupby("w")[["book_return","coin_return"]].mean()
    return out
