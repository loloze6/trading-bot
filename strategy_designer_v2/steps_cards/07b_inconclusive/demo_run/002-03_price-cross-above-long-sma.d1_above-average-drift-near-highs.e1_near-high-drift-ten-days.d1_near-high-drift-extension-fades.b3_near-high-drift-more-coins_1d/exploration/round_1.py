def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; n=len(df)
            for h in (5,10,20):
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                        reg=df["regime"].iloc[i],fc=df["forecast"].iloc[i],
                        r20=df.get("debug_info.components.range20.post_pipeline_value",pd.Series([np.nan]*n)).iloc[i],
                        e30=df.get("debug_info.components.ext30.post_pipeline_value",pd.Series([np.nan]*n)).iloc[i],
                        e30raw=df.get("debug_info.components.ext30.last_history_value",pd.Series([np.nan]*n)).iloc[i],
                        ret=c[i+h]/c[i]-1))
    g=pd.DataFrame(rows)
    g["ex"]=g["ret"]-g.groupby(["coin","h"])["ret"].transform("mean")
    def reg(d,x):
        d=d.dropna(subset=[x,"ex"])
        if len(d)<15 or d[x].std()==0: return (len(d),np.nan,np.nan)
        r=stats.linregress(d[x],d["ex"]); return (len(d),r.slope,r.slope/r.stderr)
    out={}
    t=g[g.reg=="trending"]
    res=[]
    for h in (5,10,20):
        d=t[t.h==h]
        for x in ("fc","r20","e30","e30raw"):
            n,s,tt=reg(d,x); res.append(dict(h=h,x=x,n=n,slope=s,t=tt))
    out["by_horizon_var"]=pd.DataFrame(res)
    d10=t[t.h==10].copy()
    out["by_coin"]=pd.DataFrame([dict(coin=k,**dict(zip(["n","slope","t"],reg(v,"fc"))),r20t=reg(v,"r20")[2]) for k,v in d10.groupby("coin")])
    out["by_year"]=pd.DataFrame([dict(year=k,**dict(zip(["n","slope","t"],reg(v,"fc"))),r20t=reg(v,"r20")[2],meanex=v.ex.mean()) for k,v in d10.groupby("year")])
    d10["q"]=pd.qcut(d10["r20"],5,labels=False,duplicates="drop")
    out["r20_quint"]=d10.groupby("q").agg(n=("ex","size"),r20=("r20","mean"),ex=("ex","mean"),ret=("ret","mean"))
    d10["eq"]=pd.qcut(d10["e30raw"],5,labels=False,duplicates="drop")
    out["raw30_quint"]=d10.groupby("eq").agg(n=("ex","size"),raw=("e30raw","mean"),ex=("ex","mean"))
    out["fc_sign"]=d10.groupby(np.sign(d10.fc)).agg(n=("ex","size"),ex=("ex","mean"),sd=("ex","std"))
    nt=g[(g.h==10)]
    out["regime_mean_ex"]=nt.groupby("reg").agg(n=("ex","size"),ex=("ex","mean"),sd=("ex","std"))
    return out
