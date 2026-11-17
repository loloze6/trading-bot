def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); n=len(b)
            r7=c/c.shift(7)-1; r30=c/c.shift(30)-1
            yr=pd.to_datetime(b["timestamp"]).dt.year
            fwd=c.shift(-7)/c-1
            for i in range(0,n,7):
                rows.append(dict(coin=coin,w=w,yr=yr[i],reg=b["regime"].iloc[i],fc=b["forecast"].iloc[i],r7=r7[i],r30=r30[i],fwd=fwd[i]))
    d=pd.DataFrame(rows).dropna(subset=["fwd"])
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    def slope(x,y):
        m=x.notna()&y.notna(); x=x[m];y=y[m]
        if len(x)<10: return (np.nan,np.nan,len(x))
        r=stats.linregress(x,y); return (r.slope,r.slope/r.stderr,len(x))
    out={}
    s=d[(d.reg=="mean_reversion")].dropna(subset=["r30","r7"]).copy()
    thr=s.r30.quantile(1/3)
    deep=s[s.r30<=thr]
    out["deep_thr_r30"]=float(thr)
    pc=[]
    for k,g in deep.groupby("coin"):
        a=slope(-g.r7,g.ex); f=slope(g.fc,g.ex); pc.append(dict(coin=k,t_negr7=a[1],t_fc=f[1],n=a[2]))
    out["deep_per_coin"]=pd.DataFrame(pc)
    py=[]
    for k,g in deep.groupby("yr"):
        a=slope(-g.r7,g.ex); py.append(dict(yr=k,t=a[1],n=a[2]))
    out["deep_per_year"]=pd.DataFrame(py)
    deep=deep.copy(); deep["q"]=pd.qcut(deep.r7,4,labels=False)
    out["deep_r7_quart"]=deep.groupby("q").agg(n=("ex","size"),r7=("r7","mean"),ex=("ex","mean"),t=("ex",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))))
    # interaction: x = -r7 * (-r30) across mean_reversion
    s["inter"]=s.r7*s.r30
    a=slope(s.inter,s.ex); out["mr_inter_r7xr30"]=f"slope {a[0]:.4f} t {a[1]:.2f} n {a[2]}"
    # all bars: deep vs rising regime with r7 at 7
    # quintiles of r30 over all bars, -r7 slope
    al=d.dropna(subset=["r30","r7"]).copy(); al["q30"]=pd.qcut(al.r30,5,labels=False)
    qq=[]
    for k,g in al.groupby("q30"):
        a=slope(-g.r7,g.ex); qq.append(dict(q30=k,r30=g.r30.mean(),t=a[1],slope=a[0],n=a[2]))
    out["all_by_r30_quint"]=pd.DataFrame(qq)
    ws=[]
    for k,g in deep.groupby("w"):
        ws.append(dict(w=k,n=len(g)))
    out["deep_windows_count"]=len(ws)
    # deep sides
    sd=[]
    for nm,g in [("bounce",deep[deep.r7>0]),("fall",deep[deep.r7<=0])]:
        a=slope(-g.r7,g.ex); sd.append(dict(side=nm,t=a[1],n=a[2],meanex=g.ex.mean()))
    out["deep_side"]=pd.DataFrame(sd)
    return out
