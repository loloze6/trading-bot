def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        r3=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-3,3)
            r3+=list(c[idx+3]/c[idx]-1)
        drift[coin]=np.mean(r3)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            f=b["forecast"].fillna(0).values; c=b["close"].values
            cs=pd.Series(c)
            dr=cs.pct_change()
            sd30=dr.rolling(30,min_periods=20).std().values
            r7=(cs/cs.shift(7)-1).values
            r14=(cs/cs.shift(14)-1).values
            r3b=(cs/cs.shift(3)-1).values
            scal=r7/(sd30*np.sqrt(7))
            ts=pd.to_datetime(b["timestamp"])
            lowest=0.0; cell_done=-1
            for t in range(len(b)):
                if f[t]<=0: lowest=0.0; continue
                lowest=min(lowest,f[t])
                cell=t//3
                if f[t]-lowest>=2 and cell!=cell_done:
                    cell_done=cell; lowest=f[t]
                    rec={"coin":coin,"w":w,"f":f[t],"scal":scal[t],"r7":r7[t],"r3b":r3b[t],"r14":r14[t],"sd30":sd30[t]}
                    for h in [3,5,7]:
                        rec[f"x{h}"]=(c[t+h]/c[t]-1-drift[coin]*h/3) if t+h<len(c) else np.nan
                    rows.append(rec)
    d=pd.DataFrame(rows)
    def summ(g,col):
        s=g[col].dropna()
        return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out={}
    out["n_scal_valid"]=int(d.scal.notna().sum())
    sp={}
    for v in ["f","scal","r7","r3b","r14","sd30"]:
        for h in [3,5,7]:
            dd=d[[v,f"x{h}"]].dropna()
            sp[(v,h)]=stats.spearmanr(dd[v],dd[f"x{h}"])[0]
    out["spearman"]=pd.Series(sp).unstack()
    ds=d.dropna(subset=["scal"]).copy()
    ds["sq"]=pd.qcut(ds.scal.rank(method="first"),4,labels=False)
    out["by_scal_quartile"]=pd.concat({h:ds.groupby("sq").apply(lambda g: summ(g,f"x{h}")) for h in [3,7]},axis=1)
    out["scal_mean_by_q"]=ds.groupby("sq").scal.mean()
    out["share_f_at_20"]=float((d.f>=19.99).mean())
    out["f20_vs_rest_x3"]=pd.DataFrame({"f20":summ(d[d.f>=19.99],"x3"),"rest":summ(d[d.f<19.99],"x3")})
    out["f20_vs_rest_x7"]=pd.DataFrame({"f20":summ(d[d.f>=19.99],"x7"),"rest":summ(d[d.f<19.99],"x7")})
    out["by_coin_x7"]=d.groupby("coin").apply(lambda g: summ(g,"x7"))
    return out
