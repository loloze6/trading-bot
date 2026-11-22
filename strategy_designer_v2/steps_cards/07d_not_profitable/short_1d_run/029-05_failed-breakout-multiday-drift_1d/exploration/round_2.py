def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        g={h:[] for h in (2,8,10)}
        for b in ws.values():
            c=b["close"].values
            for h in g: g[h]+=[c[i+h]/c[i]-1 for i in range(0,len(c)-h,h)]
        dr={h:np.mean(v) for h,v in g.items()}
        for w,b in ws.items():
            c=b["close"].values.astype(float); n=len(c)
            hi=b["high"].values.astype(float)
            ph=pd.Series(c).rolling(20).max().shift(1).values
            seen=set()
            for e in range(4,n):
                ks=[k for k in (e-1,e-2,e-3) if not np.isnan(ph[k]) and c[k]>ph[k]]
                if not ks: continue
                k=ks[0]; ref=ph[k]
                if c[e]>=ref: continue
                if e+10>=n or e//10 in seen: continue
                seen.add(e//10)
                rows.append(dict(coin=coin,depth=(ref-c[e])/ref,
                    ext=(max(c[k:e])-ref)/ref,
                    u02=-(c[e+2]/c[e]-1-dr[2]),
                    u010=-(c[e+10]/c[e]-1-dr[10]),
                    u210=-(c[e+10]/c[e+2]-1-dr[8]),
                    below2=float(c[e+2]<ref)))
    d=pd.DataFrame(rows)
    def s(q):
        o={}
        for col in ["u02","u210","u010"]:
            x=q[col]; o[col]=x.mean(); o["t_"+col]=x.mean()/(x.std()/np.sqrt(len(x)))
        o["n"]=len(q); o["below2"]=q["below2"].mean()
        return pd.Series(o)
    out={"all":s(d).to_frame().T}
    d["dq"]=pd.qcut(d.depth,3,labels=["low","mid","high"])
    out["by_depth"]=d.groupby("dq").apply(s)
    d["eq"]=pd.qcut(d.ext,3,labels=["low","mid","high"])
    out["by_ext"]=d.groupby("eq").apply(s)
    out["by_below2"]=d.groupby("below2").apply(s)
    D=pd.concat([x for ws in data["days"].values() for x in ws.values()])
    B=pd.concat([b.assign(nr=b.close.shift(-1)/b.close-1) for ws in data["bars"].values() for b in ws.values()])
    a=B.postRebalance_current_allocation
    out["book"]=pd.Series({"share_days_short":(a<0).mean(),"mean_alloc_when_short":a[a<0].mean(),
        "gain_per_bar_short":(a*B.nr)[a<0].mean(),"coin_ret_when_short":B.nr[a<0].mean(),"coin_ret_all":B.nr.mean()})
    return out
