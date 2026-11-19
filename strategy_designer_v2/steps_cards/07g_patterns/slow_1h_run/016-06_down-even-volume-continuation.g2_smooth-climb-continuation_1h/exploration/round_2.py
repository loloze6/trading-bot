def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=72
    rows=[]; hr=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].values.astype(float)
            r=np.r_[np.nan,c[1:]/c[:-1]-1]
            ts=pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"coin":coin,"w":w,"year":ts.dt.year.values,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":r}))
            fc=b.get("debug_info.components.er72.post_pipeline_value")
            n=len(c)
            for t in range(0,n,H):
                if t<H or t+H>=n: continue
                pr=r[t-H+1:t+1]
                if np.isnan(pr).any(): continue
                s=np.abs(pr).sum()
                if s<=0: continue
                rows.append(dict(coin=coin,w=w,wn=int(w[1:]),year=ts.iloc[t].year,past=c[t]/c[t-H]-1,past24=c[t]/c[t-24]-1,fwd=c[t+H]/c[t]-1,
                    er=abs(np.log(c[t]/c[t-H]))/np.abs(np.log1p(pr)).sum(),
                    fc=(fc.iloc[t] if fc is not None else np.nan)))
    g=pd.DataFrame(rows)
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    for f in ["past","er","past24","fc"]:
        g["z_"+f]=g.groupby("coin")[f].transform(lambda x:(x-x.mean())/x.std())
    g["zex"]=g.groupby("coin")["ex"].transform(lambda x:x/x.std())
    def ols(df,f):
        d=df[[f,"zex"]].dropna()
        if len(d)<10: return pd.Series({"slope":np.nan,"t":np.nan,"n":len(d)})
        s=stats.linregress(d[f],d["zex"]); return pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(d)})
    out={}
    up=g[g.past>0]; dn=g[g.past<=0]
    # multivariate on up: er and past
    d=up[["z_er","z_past","zex"]].dropna()
    X=np.c_[np.ones(len(d)),d.z_er,d.z_past]; y=d.zex.values
    b,res,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b; s2=e@e/(len(y)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["up: zex ~ er + past (coef,t)"]=pd.DataFrame({"coef":b,"t":b/se},index=["c","er","past"])
    out["up: raw er vs recorded forecast"]=pd.DataFrame({"raw_er":ols(up,"z_er"),"recorded_fc":ols(up,"z_fc"),"corr_er_fc":pd.Series({"slope":up[["er","fc"]].corr().iloc[0,1]})})
    tab={}
    for coin,sub in up.groupby("coin"): tab[coin]=ols(sub,"z_er")
    tab["first half w1-12"]=ols(up[up.wn<=12],"z_er"); tab["second half w13-24"]=ols(up[up.wn>12],"z_er")
    out["up er slope by coin/half"]=pd.DataFrame(tab).T
    up=up.copy(); up["eq"]=up.groupby("coin")["er"].transform(lambda x:pd.qcut(x,5,labels=False))
    out["up: fwd ex by er quintile"]=up.groupby("eq")["ex"].agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    tab={}
    for coin,sub in dn.groupby("coin"): tab[coin]=ols(sub,"z_past24")
    tab["first half"]=ols(dn[dn.wn<=12],"z_past24"); tab["second half"]=ols(dn[dn.wn>12],"z_past24")
    tab["all-down past72"]=ols(dn,"z_past")
    out["down: past24 slope by coin/half"]=pd.DataFrame(tab).T
    h=pd.concat(hr).dropna()
    h["late"]=h.hour.isin([21,22])
    def tt(x): return x.mean()/x.std()*np.sqrt(len(x))
    out["hours21-22 by coin"]=h[h.late].groupby("coin")["r"].agg(["mean",tt,"count"])
    out["hours21-22 by year"]=h[h.late].groupby("year")["r"].agg(["mean",tt,"count"])
    out["hours21-22 vs rest welch"]=pd.Series(stats.ttest_ind(h[h.late].r,h[~h.late].r,equal_var=False)._asdict())
    out["saturday by coin"]=h[h.wd==5].groupby("coin")["r"].agg(["mean",tt])
    return out
