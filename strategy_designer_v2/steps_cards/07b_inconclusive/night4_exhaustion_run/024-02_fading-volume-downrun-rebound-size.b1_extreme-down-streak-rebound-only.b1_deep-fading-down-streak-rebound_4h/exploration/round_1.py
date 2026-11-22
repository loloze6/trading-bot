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
        drift[coin]={h:(np.mean(g[h]),np.std(g[h])) for h in H}
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
            n=len(c); r=np.r_[np.nan,c[1:]/c[:-1]-1]
            usual=pd.Series(np.abs(r)).rolling(180,min_periods=45).mean().values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            fc=b["forecast"].fillna(0).values
            L=0
            for t in range(1,n):
                L = L+1 if c[t]<c[t-1] else 0
                if L>=2 and t+18<n and not np.isnan(usual[t]):
                    s=t-L
                    vv=v[s+1:t+1]; x=np.arange(len(vv))
                    slope=np.polyfit(x,vv,1)[0]
                    loss=-(c[t]/c[s]-1)/usual[t]
                    d={"coin":coin,"w":w,"t":t,"cell":t//18,"yr":yr[t],"L":L,"loss":loss,
                       "fade":bool(slope<0),"fc":fc[t],"dfc":fc[t]-fc[t-1]}
                    for h in H:
                        d[f"x{h}"]=c[t+h]/c[t]-1-drift[coin][h][0]
                    rows.append(d)
    df=pd.DataFrame(rows)
    def summ(d,col="x18"):
        x=d[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),
                          "t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out={}
    first=df.sort_values("t").groupby(["coin","w","cell","fade"]).head(1).copy()
    first["lq"]=first.groupby("fade")["loss"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["by_fade_loss_q x18"]=first.groupby(["fade","lq"]).apply(lambda d: pd.concat([summ(d),pd.Series({"loss":d.loss.mean()})])).reset_index()
    out["by_fade_horizon"]=pd.concat({h:first.groupby("fade").apply(lambda d:summ(d,f"x{h}")) for h in H}).reset_index()
    f=first[first.fade]
    out["fade by coin x18"]=f.groupby("coin").apply(summ)
    out["fade by year x18"]=f.groupby("yr").apply(summ)
    out["fade by streak len"]=f.groupby(f.L.clip(upper=6)).apply(summ)
    bets=df[(df.dfc>=2)&(df.fc>0)].sort_values("t").groupby(["coin","w","cell"]).head(1).copy()
    out["bets approx"]=summ(bets).to_frame().T
    bets["fq"]=pd.qcut(bets.fc.rank(method="first"),5,labels=False)
    out["bets by fc quintile"]=bets.groupby("fq").apply(lambda d: pd.concat([summ(d),pd.Series({"fc":d.fc.mean(),"loss":d.loss.mean()})]))
    out["bets by year"]=bets.groupby("yr").apply(summ)
    out["bets by coin"]=bets.groupby("coin").apply(summ)
    return out
