def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    recs=[]
    for c in data["bars"]:
        allr={}
        for H in [5,10]:
            rr=[]
            for w,b in data["bars"][c].items():
                cl=b["close"].values; g=cl[::H]
                rr+=list(g[1:]/g[:-1]-1)
            allr[H]=np.mean(rr)
        for w,b in data["bars"][c].items():
            cl=b["close"].reset_index(drop=True); lo=b["low"].reset_index(drop=True)
            fc=b["forecast"].reset_index(drop=True).fillna(0)
            n=len(cl)
            if n<30: continue
            ph=cl.shift(1).rolling(20).max(); bo=(cl>ph).values
            run=(cl/cl.shift(20)-1).values
            vol=cl.pct_change().rolling(20).std().values
            f5=(cl.shift(-5)/cl-1).values; f10=(cl.shift(-10)/cl-1).values
            yr=pd.to_datetime(b["timestamp"]).dt.year.reset_index(drop=True)
            for g in range(0,n,5):
                for i in range(g,min(g+5,n)):
                    js=[j for j in range(max(0,i-3),i) if bo[j]]
                    if not js: continue
                    j=js[-1]
                    if cl[i]<lo[j] and not np.isnan(f5[i]):
                        recs.append(dict(coin=c,w=w,year=yr[i],depth=(lo[j]-cl[i])/cl[i],
                            dvol=(lo[j]-cl[i])/cl[i]/vol[i] if vol[i]>0 else np.nan,
                            run=run[j],m5=-(f5[i]-allr[5]),m10=-(f10[i]-allr[10]) if not np.isnan(f10[i]) else np.nan,
                            fc=fc[i],day1=cl[i]/cl[i-1]-1))
                        break
    R=pd.DataFrame(recs)
    def summ(gr,col="m5"):
        return gr[col].agg(n="count",mean="mean",t=lambda x:x.mean()/(x.std(ddof=1)/np.sqrt(x.count())))
    for v in ["depth","dvol","run","day1"]:
        R["q"]=pd.qcut(R[v],5,labels=False,duplicates="drop")
        out["by_"+v]=pd.concat([summ(R.groupby("q")),summ(R.groupby("q"),"m10").add_suffix("10"),R.groupby("q")[v].mean().rename("avg")],axis=1)
    R["fcb"]=pd.cut(R["fc"],[-21,-6,-3,-1,-0.0001,0.1])
    out["by_forecast"]=summ(R.groupby("fcb"))
    out["by_coin"]=summ(R.groupby("coin"))
    out["by_year"]=summ(R.groupby("year"))
    out["spearman"]=pd.Series({v:stats.spearmanr(R[v],R["m5"],nan_policy="omit")[0] for v in ["depth","dvol","run","day1"]})
    # exposure on signal bars
    tot=0;act=0;ab=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            a=b["postRebalance_current_allocation"].fillna(0)
            ab+=list(a[a!=0].abs())
    out["alloc_when_in"]=pd.Series(ab).describe()
    return out
