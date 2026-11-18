def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c=b["close"].values;o=b["open"].values;l=b["low"].values;h=b["high"].values;v=b["volume"].values
            n=len(b)
            r1=pd.Series(c).pct_change(); z=r1/r1.rolling(20).std()
            vr=pd.Series(v)/pd.Series(v).shift(1).rolling(20).median()
            rng=h-l
            wick=np.where(rng>0,(np.minimum(o,c)-l)/np.where(rng>0,rng,1),np.nan)
            last=-10
            for t in range(n):
                if not (z.iloc[t]<=-2): continue
                indep = t-last>3
                if indep: last=t
                f1=c[t+1]/c[t]-1 if t+1<n else np.nan
                f3=c[t+3]/c[t]-1 if t+3<n else np.nan
                rows.append(dict(coin=coin,z=z.iloc[t],vr=vr.iloc[t],wick=wick[t],indep=indep,
                    drop=(o[t]-l[t])/o[t],f1=f1,f3=f3,alloc=b["postRebalance_current_allocation"].iloc[t]))
    d=pd.DataFrame(rows)
    out={}
    def s(g):
        r={}
        for k in ("f1","f3"):
            x=g[k].dropna(); r["n"+k]=len(x); r["m"+k]=x.mean(); r["t"+k]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        return pd.Series(r)
    di=d[d.indep]
    vb=di[di.vr>=2]
    out["volburst_by_vr_tercile"]=vb.groupby(pd.qcut(vb.vr,3,labels=False)).apply(s)
    out["volburst_by_z_tercile"]=vb.groupby(pd.qcut(vb.z,3,labels=False)).apply(s)
    out["volburst_by_wick_tercile"]=vb.groupby(pd.qcut(vb.wick,3,labels=False)).apply(s)
    out["all_sharp_by_vr_tercile"]=di.groupby(pd.qcut(di.vr,3,labels=False)).apply(s)
    out["corr_vb"]=vb[["vr","z","wick","drop","f1","f3"]].corr()[["f1","f3"]]
    # holding length of book trades
    tl=[]
    for coin in data["trades"]:
        for w,t in data["trades"][coin].items():
            tl.append(t)
    T=pd.concat(tl)
    out["trade_days_mean"]=float(T.duration_minutes.mean()/1440)
    out["trade_count"]=len(T)
    out["trade_net_mean"]=float(T.net_profit_loss_percent.mean())
    out["trade_gross_mean"]=float(T.profit_loss_percent.mean())
    return out
