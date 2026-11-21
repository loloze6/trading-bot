def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; hi=b["high"].values; lo=b["low"].values
            pa=b["previous_allocation"].fillna(0).values; a=b["postRebalance_current_allocation"].fillna(0).values
            n=len(b)
            r42=pd.Series(cl).pct_change(42).values
            rng=pd.Series((hi-lo)/cl)
            vr=(rng.rolling(42).mean()/rng.rolling(360).mean()).values
            for t in range(n-18):
                if pa[t]<=1e-9 and a[t]>1e-9:
                    rows.append(dict(coin=c,wn=int(w[1:]),fwd=cl[t+18]/cl[t]-1,r42=r42[t],vr=vr[t],alloc=a[t],
                                     maxdd=lo[t+1:t+19].min()/cl[t]-1))
    cs=pd.DataFrame(rows).dropna()
    cs["fall"]=cs.wn.between(5,10)
    cs["vrq"]=pd.qcut(cs.vr,4,labels=False); cs["r42q"]=pd.qcut(cs.r42,2,labels=False)
    def agg(x):
        return pd.Series({"n":len(x),"fwd":x.fwd.mean(),"t":x.fwd.mean()/x.fwd.std()*np.sqrt(len(x)),"worst_path":x.maxdd.mean(),"wfwd":(x.fwd*x.alloc).sum()/x.alloc.sum(),"alloc":x.alloc.mean()})
    out["vrq_by_fall"]=cs.groupby(["fall","vrq"]).apply(agg).round(4)
    out["vrq_x_r42half"]=cs.groupby(["vrq","r42q"]).apply(agg).round(4)
    out["vrq_by_coin"]=cs.groupby(["coin","vrq"]).fwd.mean().unstack().round(4)
    cs["half"]=np.where(cs.wn<=12,"w1-12","w13-24")
    out["vrq_by_half"]=cs.groupby(["half","vrq"]).apply(agg).round(4)
    # vr as continuous: per-decile
    cs["vrd"]=pd.qcut(cs.vr,8,labels=False)
    out["vr_octile"]=cs.groupby("vrd").apply(lambda x: pd.Series({"vr_mid":x.vr.median(),"n":len(x),"fwd":x.fwd.mean(),"worst":x.maxdd.mean()})).round(4)
    return out
