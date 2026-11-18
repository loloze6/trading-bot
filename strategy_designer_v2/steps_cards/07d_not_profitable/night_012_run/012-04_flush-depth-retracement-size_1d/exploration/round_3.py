def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    allrows=[]; rows=[]
    for coin in bars:
        for w, b in bars[coin].items():
            b=b.reset_index(drop=True)
            c=b["close"].values;o=b["open"].values;l=b["low"].values;h=b["high"].values;v=b["volume"].values
            n=len(b)
            for t in range(0,n-3,3):
                allrows.append(dict(coin=coin,f3=c[t+3]/c[t]-1))
            r1=pd.Series(c).pct_change(); z=r1/r1.rolling(20).std()
            vr=pd.Series(v)/pd.Series(v).shift(1).rolling(20).median()
            rng=h-l
            wick=np.where(rng>0,(np.minimum(o,c)-l)/np.where(rng>0,rng,1),np.nan)
            sdd=pd.Series((o-l)/o).rolling(60,min_periods=20).mean()
            last={k:-10 for k in ("z2","z15")}
            for t in range(n):
                for k,th in (("z2",-2),("z15",-1.5)):
                    if z.iloc[t]<=th and vr.iloc[t]>=2 and t-last[k]>3:
                        last[k]=t
                        rows.append(dict(set=k,coin=coin,w=w,vr=vr.iloc[t],wick=wick[t],
                          drop=(o[t]-l[t])/o[t],dropn=((o[t]-l[t])/o[t])/sdd.iloc[t] if sdd.iloc[t]>0 else np.nan,
                          f1=c[t+1]/c[t]-1 if t+1<n else np.nan,
                          f3=c[t+3]/c[t]-1 if t+3<n else np.nan))
    A=pd.DataFrame(allrows); mm=A.groupby("coin").f3.mean()
    d=pd.DataFrame(rows); d["x3"]=d.f3-d.coin.map(mm)
    out={}
    def s(g):
        r={}
        for k in ("f1","x3"):
            x=g[k].dropna(); r["n"+k]=len(x); r["m"+k]=x.mean(); r["t"+k]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        return pd.Series(r)
    for k in ("z2","z15"):
        g=d[d.set==k]
        out[k+"_all"]=s(g).to_frame().T
        out[k+"_by_dropn_tercile"]=g.groupby(pd.qcut(g.dropn,3,labels=False)).apply(s)
        out[k+"_by_wick_half"]=g.groupby(g.wick>=0.3).apply(s)
        gg=g.dropna(subset=["dropn","x3"])
        sl=stats.linregress(gg.dropn,gg.x3); out[k+"_slope_t_x3_on_dropn"]=float(sl.slope/sl.stderr)
        g1=g.dropna(subset=["dropn","f1"]); sl=stats.linregress(g1.dropn,g1.f1); out[k+"_slope_t_f1_on_dropn"]=float(sl.slope/sl.stderr)
        out[k+"_cases_per_bar"]=len(g)/17504
    return out
