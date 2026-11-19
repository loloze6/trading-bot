def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[]
    hourly=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values.astype(float); v=df["volume"].values.astype(float)
            n=len(c)
            r1=np.r_[np.nan, c[1:]/c[:-1]-1]
            ts=pd.to_datetime(df["timestamp"])
            hourly.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":r1,
                                        "alloc":df["postRebalance_current_allocation"].values}))
            for t in range(0,n-H,H):
                if t<H: continue
                past=c[t]/c[t-H]-1
                seg=r1[t-H+1:t+1]
                eff=abs(np.log(c[t]/c[t-H]))/np.nansum(np.abs(np.log1p(seg)))
                vs=v[t-H+1:t+1]
                top=np.sort(vs)[-3:].sum()/vs.sum() if vs.sum()>0 else np.nan
                vol=np.nanstd(seg)
                fwd=c[t+H]/c[t]-1
                rows.append(dict(coin=coin,w=w,past=past,eff=eff,top=top,vol=vol,fwd=fwd,
                                 fc=df["forecast"].iloc[t]))
    g=pd.DataFrame(rows)
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    g["sfwd"]=np.sign(g["past"])*g["ex"]
    out={}
    def tab(col,q=5,val="ex",sub=None):
        d=g if sub is None else g[sub]
        d=d.copy(); d["q"]=d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),q,labels=False))
        a=d.groupby("q")[val].agg(["mean","std","count"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a
    out["fwd_ex by past72 quintile"]=tab("past")
    out["signed fwd by efficiency quintile"]=tab("eff",val="sfwd")
    out["fwd_ex by eff quintile, falls"]=tab("eff",sub=g.past<0)
    out["fwd_ex by eff quintile, rises"]=tab("eff",sub=g.past>0)
    out["fwd_ex by topshare quintile, rises"]=tab("top",sub=g.past>0)
    out["fwd_ex by topshare quintile, falls"]=tab("top",sub=g.past<0)
    out["fwd_ex by vol quintile"]=tab("vol")
    out["signed fwd by top quintile"]=tab("top",val="sfwd")
    hr=pd.concat(hourly)
    a=hr.groupby("hour")["r"].agg(["mean","std","count"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["ret by hour"]=a
    b=hr.groupby("wd")["r"].agg(["mean","std","count"]); b["t"]=b["mean"]/(b["std"]/np.sqrt(b["count"]))
    out["ret by weekday"]=b
    # book
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    D=pd.concat(dd)
    out["book by coin"]=D.groupby("coin")[["book_return","coin_return"]].mean()
    out["book by window mean"]=D.groupby("w")[["book_return","coin_return"]].mean()
    hr["gain"]=hr.groupby("coin")["alloc"].shift(1)*hr["r"]
    out["mean alloc / gain"]=hr.groupby("coin")[["alloc","gain"]].mean()
    return out
