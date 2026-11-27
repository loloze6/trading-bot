def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            r=np.r_[np.nan, c[1:]/c[:-1]-1]
            fwd1=np.r_[c[1:]/c[:-1]-1, np.nan]
            fwd2=np.r_[c[2:]/c[:-2]-1, [np.nan]*2]
            fwd3=np.r_[c[3:]/c[:-3]-1, [np.nan]*3]
            run=np.zeros(len(c)); k=0
            for i in range(len(c)):
                run[i]=k
                if not np.isnan(r[i]) and r[i]<0: k+=1
                else: k=0
            # run[i] = down days before bar i
            ret20=pd.Series(c).pct_change(20).values
            sd20=pd.Series(r).rolling(20).std().values
            z=ret20/(sd20*np.sqrt(20))
            for i in range(len(c)):
                if not np.isnan(r[i]) and r[i]>0 and run[i]>=1:
                    rows.append(dict(coin=coin,w=w,i=i,run=run[i],z=z[i],reg=b["regime"].iloc[i],
                        fc=b["forecast"].iloc[i],f1=fwd1[i],f2=fwd2[i],f3=fwd3[i],r0=r[i],day=str(b["timestamp"].iloc[i])[:10]))
    d=pd.DataFrame(rows)
    # drift: mean daily return per coin over all bars
    drift={}
    for coin,ws in data["bars"].items():
        rr=[]
        for w,b in ws.items():
            c=b["close"].astype(float).values; rr.append(c[1:]/c[:-1]-1)
        drift[coin]=np.mean(np.concatenate(rr))
    d["dr"]=d.coin.map(drift)
    for h in [1,2,3]:
        d[f"x{h}"]=-(d[f"f{h}"]-h*d.dr)
    def summ(g):
        g=g.dropna(subset=["x1"])
        ds=g.groupby("day")[["x1","x2","x3"]].sum()
        out={"n":len(g),"days":len(ds)}
        for h in [1,2,3]:
            s=ds[f"x{h}"].dropna(); out[f"m{h}"]=g[f"x{h}"].mean(); out[f"t{h}"]=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
        return pd.Series(out)
    res={}
    res["by_regime"]=d.groupby("reg").apply(summ)
    tr=d[d.reg=="trending"]
    res["trend_by_coin"]=tr.groupby("coin").apply(summ)
    res["trend_by_window"]=tr.groupby("w").apply(summ)
    tr=tr.copy(); tr["runb"]=tr.run.clip(upper=4)
    res["trend_by_run"]=tr.groupby("runb").apply(summ)
    tr["zq"]=pd.qcut(tr.z,3,labels=False)
    res["trend_by_zq"]=tr.groupby("zq").apply(summ)
    tr["r0q"]=pd.qcut(tr.r0,3,labels=False)
    res["trend_by_bounce_size"]=tr.groupby("r0q").apply(summ)
    un=d[d.reg=="unknown"].copy(); un["runb"]=un.run.clip(upper=4)
    res["unknown_by_run"]=un.groupby("runb").apply(summ)
    res["trend_fc_nonzero"]=summ(tr[tr.fc<0])
    return res
