def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=20
    rows=[]; drift={}; usual={}
    for coin,wins in data["bars"].items():
        nr=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            nr+=list(c[idx+H]/c[idx]-1)
        drift[coin]=np.mean(nr); usual[coin]=np.std(nr)
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(c)
            r1=pd.Series(c).pct_change()
            z=(r1/r1.rolling(20).std().shift(1)).values
            for start in range(0,n,H):
                cell=range(start,min(start+H,n))
                for t in cell:
                    if abs(f[t])>=2:
                        out={"coin":coin,"w":w,"year":yr[t],"f":f[t],"side":"up" if f[t]>0 else "down","z":z[t]}
                        for h in (3,5,10,20,40):
                            out["r%d"%h]=c[t+h]/c[t]-1 if t+h<n else np.nan
                        rows.append(out); break
    d=pd.DataFrame(rows)
    d["u20"]=d["r20"]-d["coin"].map(drift)
    res={}
    def welch(g,col):
        a=g.loc[g.side=="up",col].dropna(); bb=g.loc[g.side=="down",col].dropna()
        if len(a)<3 or len(bb)<3: return pd.Series({"n_up":len(a),"n_dn":len(bb)})
        return pd.Series({"n_up":len(a),"n_dn":len(bb),"mean_up":a.mean(),"mean_dn":bb.mean(),"diff":a.mean()-bb.mean(),"t":stats.ttest_ind(a,bb,equal_var=False)[0]})
    res["overall_u20"]=welch(d,"u20").to_frame().T
    res["by_horizon_raw"]=pd.DataFrame({h:welch(d,"r%d"%h) for h in (3,5,10,20,40)}).T
    res["by_coin"]=d.groupby("coin").apply(lambda g:welch(g,"u20"))
    res["by_year"]=d.groupby("year").apply(lambda g:welch(g,"u20"))
    d["fq"]=d.groupby("side")["f"].transform(lambda s:pd.qcut(s.abs().rank(method="first"),4,labels=False))
    res["by_fsize_q"]=d.groupby("fq").apply(lambda g:welch(g,"u20"))
    # one-sample per side, raw signed returns
    out={}
    for s in ("up","down"):
        for h in (5,10,20):
            x=d.loc[d.side==s,"r%d"%h].dropna()
            out[(s,h)]={"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))}
    res["side_raw_mean"]=pd.DataFrame(out).T
    res["drift20"]=pd.Series(drift)
    res["n_cases"]=len(d)
    return res
