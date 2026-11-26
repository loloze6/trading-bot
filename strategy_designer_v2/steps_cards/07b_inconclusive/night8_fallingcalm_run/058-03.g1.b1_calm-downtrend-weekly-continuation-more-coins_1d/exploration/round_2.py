import pandas as pd, numpy as np

def explore(data):
    rows=[]
    allmeans={}
    for H in (3,5,10):
        for coin,ws in data["bars"].items():
            allr=[]
            for w,df in ws.items():
                c=df["close"].values
                for i in range(0,len(c)-H,H):
                    allr.append(c[i+H]/c[i]-1)
            allmeans[(coin,H)]=np.mean(allr) if allr else np.nan
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"]
            r1=c.pct_change()
            vol=r1.rolling(60,min_periods=20).std()
            past=c/c.shift(5)-1
            ts=pd.to_datetime(df["timestamp"])
            for H in (3,5,10):
                fwd=c.shift(-H)/c-1
                for i in range(0,len(df)-H,H):
                    if pd.isna(past.iat[i]) or past.iat[i]==0: continue
                    rows.append(dict(H=H,coin=coin,inprof=df["regime"].iat[i]=="unknown",
                        day=ts.iat[i].normalize(),year=ts.iat[i].year,f=df["forecast"].iat[i]/10,
                        past=past.iat[i],pastz=past.iat[i]/(vol.iat[i]*np.sqrt(5)) if vol.iat[i]>0 else np.nan,
                        fwd=fwd.iat[i]-allmeans[(coin,H)]))
    d=pd.DataFrame(rows).dropna(subset=["fwd","pastz"])
    def slope(g,x):
        g=g.dropna(subset=[x,"fwd"])
        if len(g)<15: return pd.Series(dict(n=len(g)))
        X=np.c_[np.ones(len(g)),g[x].values]; y=g.fwd.values
        b=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@b
        XtXi=np.linalg.inv(X.T@X)
        sc=pd.DataFrame(X*e[:,None]).groupby(g.day.values).sum().values
        G=len(sc); V=XtXi@(sc.T@sc)@XtXi*G/max(G-1,1)
        return pd.Series(dict(n=len(g),days=G,slope=b[1],t=b[1]/np.sqrt(V[1,1]),corr=np.corrcoef(g[x],g.fwd)[0,1]))
    out={}
    res=[]
    for (H,ip),g in d.groupby(["H","inprof"]):
        for x in ("past","pastz","f"):
            if x=="f" and not ip: continue
            s=slope(g,x); s["H"]=H; s["inprof"]=ip; s["x"]=x; res.append(s)
    out["slopes"]=pd.DataFrame(res)
    g=d[(d.H==5)&d.inprof].copy()
    g["fz"]=pd.qcut(g.f,5,labels=False)
    out["fwd_by_forecast_quintile"]=g.groupby("fz").agg(n=("fwd","size"),f=("f","mean"),past=("past","mean"),fwd=("fwd","mean"))
    out["corr_f_past"]=float(np.corrcoef(g.f,g.past)[0,1])
    g2=d[(d.H==5)&~d.inprof].copy()
    g2["pq"]=pd.qcut(g2.past,5,labels=False)
    out["outside_fwd_by_past_quintile"]=g2.groupby("pq").agg(n=("fwd","size"),past=("past","mean"),fwd=("fwd","mean"))
    g["pq"]=pd.qcut(g.past,5,labels=False)
    out["inprof_year_extremes"]=g[g.pq.isin([0,4])].groupby(["year","pq"]).agg(n=("fwd","size"),fwd=("fwd","mean"))
    return out
