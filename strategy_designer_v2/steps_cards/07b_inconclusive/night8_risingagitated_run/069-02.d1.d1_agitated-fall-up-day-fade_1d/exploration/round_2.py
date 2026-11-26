def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        mu=pd.concat([b["close"].pct_change().dropna() for b in ws.values()]).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            hh=b["high"].rolling(20).max(); sd=r.rolling(20).std()
            x=pd.DataFrame({"timestamp":b["timestamp"],"raw":(c-hh)/hh/sd,"upz":r/sd,
                "f1":c.shift(-1)/c-1,"tr60":c/c.shift(60)-1,"regime":b["regime"],"up":r>0})
            x["mu"]=mu; x["coin"]=coin; x["w"]=w
            rows.append(x)
    d=pd.concat(rows)
    d["day"]=pd.to_datetime(d["timestamp"]).dt.floor("D")
    u=d[d.up & d.f1.notna() & d.raw.notna()].copy()
    u["dep"]=-u.raw; u["s1"]=-(u.f1-u.mu)
    u["inprof"]=u.regime=="mean_reversion"
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x))})
    def cl_slope(z,xc,yc="s1"):
        z=z[[xc,yc,"day"]].dropna()
        X=np.column_stack([np.ones(len(z)),z[xc].values]); y=z[yc].values
        XtX=np.linalg.inv(X.T@X); bta=XtX@X.T@y; e=y-X@bta
        G=z.day.nunique(); M=np.zeros((2,2))
        for _,g in pd.DataFrame({"d":z.day.values,"e":e,"x":z[xc].values}).groupby("d"):
            s=np.array([g.e.sum(),(g.e*g.x).sum()]); M+=np.outer(s,s)
        N=len(z); V=XtX@M@XtX*G/(G-1)*(N-1)/(N-2)
        return pd.Series({"slope":bta[1],"t":bta[1]/np.sqrt(V[1,1]),"n":N,"days":G})
    out={}
    out["all_updays_slope_dep"]=cl_slope(u,"dep")
    out["outside_prof_slope_dep"]=cl_slope(u[~u.inprof],"dep")
    out["inprof_slope_dep"]=cl_slope(u[u.inprof],"dep")
    u["dq"]=pd.qcut(u.dep,5,labels=False)
    out["all_updays_by_dep_quintile(4=deepest)"]=u.groupby("dq")["s1"].apply(tt).unstack()
    u["trend"]=np.where(u.tr60>0.10,"rising",np.where(u.tr60< -0.10,"falling","choppy"))
    u.loc[u.tr60.isna(),"trend"]="na"
    out["slope_by_trend"]=pd.DataFrame({k:cl_slope(g,"dep") for k,g in u.groupby("trend")})
    out["deepest_quintile_by_trend"]=u[u.dq==4].groupby("trend")["s1"].apply(tt).unstack()
    out["deepest_quintile_by_coin"]=u[u.dq==4].groupby("coin")["s1"].apply(tt).unstack()
    out["deepest_quintile_by_year"]=u[u.dq==4].groupby(pd.to_datetime(u[u.dq==4].timestamp).dt.year)["s1"].apply(tt).unstack()
    out["slope_by_year"]=pd.DataFrame({k:cl_slope(g,"dep") for k,g in u.groupby(pd.to_datetime(u.timestamp).dt.year)})
    out["slope_by_coin"]=pd.DataFrame({k:cl_slope(g,"dep") for k,g in u.groupby("coin")})
    out["dep_quintile_inprof_share"]=u.groupby("dq")["inprof"].mean()
    return out
