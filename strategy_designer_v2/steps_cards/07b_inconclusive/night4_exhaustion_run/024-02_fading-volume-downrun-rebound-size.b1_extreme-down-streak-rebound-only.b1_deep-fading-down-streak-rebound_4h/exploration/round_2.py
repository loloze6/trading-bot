def explore(data):
    import numpy as np, pandas as pd
    H=[6,12,18]
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        g={h:[] for h in H}
        for w,b in ws.items():
            c=b["close"].values.astype(float)
            for h in H:
                idx=np.arange(0,len(c)-h,h)
                g[h]+=list(c[idx+h]/c[idx]-1)
        drift[coin]={h:np.mean(g[h]) for h in H}
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
            n=len(c); r=np.r_[np.nan,c[1:]/c[:-1]-1]
            usual=pd.Series(np.abs(r)).rolling(180,min_periods=45).mean().values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            L=0
            for t in range(1,n):
                L = L+1 if c[t]<c[t-1] else 0
                if L>=2 and t+18<n and not np.isnan(usual[t]):
                    s=t-L
                    vv=v[s+1:t+1]; x=np.arange(len(vv))
                    slope=np.polyfit(x,vv,1)[0]
                    loss=-(c[t]/c[s]-1)/usual[t]
                    tr=c[t]/c[t-180]-1 if t>=180 else np.nan
                    d={"coin":coin,"w":w,"t":t,"cell":t//18,"yr":yr[t],"L":L,"loss":loss,
                       "fade":bool(slope<0),"tr30":tr}
                    for h in H:
                        d[f"x{h}"]=c[t+h]/c[t]-1-drift[coin][h]
                    rows.append(d)
    df=pd.DataFrame(rows)
    def summ(d,col="x18"):
        x=d[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),
                          "t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    first=df.sort_values("t").groupby(["coin","w","cell","fade"]).head(1).copy()
    first["ld"]=first.groupby("fade")["loss"].transform(lambda s: pd.qcut(s,10,labels=False,duplicates="drop"))
    out["deciles by fade"]=first.groupby(["fade","ld"]).apply(lambda d: pd.concat([summ(d),pd.Series({"loss":d.loss.mean()})])).reset_index()
    f=first[first.fade].copy()
    f["deep"]=f.ld>=8
    out["corr loss vs x18 fade / nonfade"]=pd.Series({"fade":f[["loss","x18"]].corr().iloc[0,1],
        "nonfade":first[~first.fade][["loss","x18"]].corr().iloc[0,1],
        "fade_spearman":f[["loss","x18"]].corr("spearman").iloc[0,1]})
    d=f[f.deep]
    out["deep fade by horizon"]=pd.DataFrame({h:summ(d,f"x{h}") for h in H}).T
    out["deep fade by year"]=d.groupby("yr").apply(summ)
    out["deep fade by coin"]=d.groupby("coin").apply(summ)
    f["trs"]=np.where(f.tr30.isna(),"na",np.where(f.tr30>0,"up30","down30"))
    out["fade deep x trend"]=f.groupby(["trs","deep"]).apply(summ)
    # graded within trend regimes
    out["corr by trend"]=f.groupby("trs").apply(lambda g: pd.Series({"n":len(g),"corr":g[["loss","x18"]].corr().iloc[0,1]}))
    # fade minus nonfade at deep loss
    nd=first[(~first.fade)&(first.ld>=8)]
    from scipy import stats
    tt=stats.ttest_ind(d.x18.dropna(),nd.x18.dropna(),equal_var=False)
    out["deep fade minus deep nonfade"]=pd.Series({"diff%":100*(d.x18.mean()-nd.x18.mean()),"t":tt.statistic,"n_fade":len(d),"n_nonfade":len(nd)})
    return out
