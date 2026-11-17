def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            n=len(b)
            r7=c/c.shift(7)-1; r30=c/c.shift(30)-1
            yr=pd.to_datetime(b["timestamp"]).dt.year
            for h in [3,7,14,30]:
                fwd=c.shift(-h)/c-1
                for i in range(0,n,h):
                    rows.append(dict(coin=coin,w=w,h=h,yr=yr[i],reg=b["regime"].iloc[i],fc=b["forecast"].iloc[i],
                                     r7=r7[i],r30=r30[i],fwd=fwd[i]))
    d=pd.DataFrame(rows).dropna(subset=["fwd"])
    d["ex"]=d["fwd"]-d.groupby(["coin","h"])["fwd"].transform("mean")
    def slope(x,y):
        m=x.notna()&y.notna(); x=x[m];y=y[m]
        if len(x)<10: return (np.nan,np.nan,len(x))
        r=stats.linregress(x,y); return (r.slope,r.slope/r.stderr,len(x))
    out={}
    res=[]
    for h in [3,7,14,30]:
        s=d[d.h==h]
        mr=s[s.reg=="mean_reversion"]; un=s[s.reg!="mean_reversion"]
        a=slope(mr.fc,mr.ex); b_=slope(-mr.r7,mr.ex); c_=slope(-un.r7,un.ex); e=slope(-s.r7,s.ex)
        res.append(dict(h=h,mr_fc_t=a[1],mr_fc_n=a[2],mr_negr7_t=b_[1],un_negr7_t=c_[1],un_n=c_[2],all_negr7_t=e[1]))
    out["horizons"]=pd.DataFrame(res)
    s=d[(d.h==7)&(d.reg=="mean_reversion")].copy()
    pc=[]
    for k,g in s.groupby("coin"):
        a=slope(g.fc,g.ex); pc.append(dict(coin=k,t=a[1],n=a[2],slope=a[0]))
    out["per_coin"]=pd.DataFrame(pc)
    py=[]
    for k,g in s.groupby("yr"):
        a=slope(g.fc,g.ex); py.append(dict(yr=k,t=a[1],n=a[2]))
    out["per_year"]=pd.DataFrame(py)
    s["q"]=pd.qcut(s.r7,5,labels=False,duplicates="drop")
    out["mr_r7_quintile"]=s.groupby("q").agg(n=("ex","size"),r7=("r7","mean"),ex=("ex","mean"),fwd=("fwd","mean"),
        t=("ex",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    s["depth"]=pd.qcut(s.r30,3,labels=["deep","mid","shallow"])
    dd=[]
    for k,g in s.groupby("depth"):
        a=slope(-g.r7,g.ex); dd.append(dict(depth=k,t=a[1],n=a[2],r30=g.r30.mean()))
    out["by_depth"]=pd.DataFrame(dd)
    side=[]
    for nm,g in [("bounce",s[s.r7>0]),("fall",s[s.r7<=0])]:
        a=slope(-g.r7,g.ex); side.append(dict(side=nm,t=a[1],n=a[2],meanex=g.ex.mean()))
    out["side"]=pd.DataFrame(side)
    return out
