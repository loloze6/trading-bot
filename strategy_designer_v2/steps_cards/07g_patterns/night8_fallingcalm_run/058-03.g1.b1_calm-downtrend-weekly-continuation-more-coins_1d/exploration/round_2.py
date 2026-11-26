def explore(data):
    import numpy as np, pandas as pd
    out={}
    # daily rows with profile recomputed from prices (all bars recorded)
    dd=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            b["r1"]=c.pct_change()
            b["r5"]=c/c.shift(5)-1
            b["inp"]=b["regime"]=="unknown"
            v=b["volume"].astype(float)
            b["vr"]=v.rolling(5).mean()/v.rolling(60,min_periods=20).mean()
            b["coin"]=coin; b["w"]=w
            b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["wd"]=b["day"].dt.weekday; b["yr"]=b["day"].dt.year
            b["f5"]=c.shift(-5)/c-1
            b["pos"]=b["postRebalance_current_allocation"].astype(float)
            dd.append(b[["coin","w","day","wd","yr","r1","r5","inp","vr","f5","pos"]])
    D=pd.concat(dd,ignore_index=True).dropna(subset=["r1"])
    D["cx"]=D.r1-D.groupby("coin")["r1"].transform("mean")
    def daycl(df,col,by):
        res={}
        for k,h in df.groupby(by):
            x=h.groupby("day")[col].mean()
            res[k]=dict(days=len(x),mean=x.mean(),t=x.mean()/(x.std(ddof=1)/np.sqrt(len(x))))
        return pd.DataFrame(res).T.round(5)
    out["weekday daycl all"]=daycl(D,"cx","wd")
    out["weekday daycl inprof"]=daycl(D[D.inp],"cx","wd")
    out["weekday daycl outprof"]=daycl(D[~D.inp],"cx","wd")
    S=D[D.wd==5]
    out["saturday by year"]=daycl(S,"cx","yr")
    T=D[D.wd==3]
    out["thursday by year"]=daycl(T,"cx","yr")
    # weekend vs weekday by previous-day size: saturday after big friday?
    # in-profile grid regression of excess f5 on r5 and r5*vr-high
    g=[]
    for (coin,w),h in D.groupby(["coin","w"]):
        h=h.reset_index(drop=True); g.append(h.iloc[::5])
    G=pd.concat(g).dropna(subset=["f5","r5","vr"])
    G["ex"]=G.f5-G.groupby("coin")["f5"].transform("mean")
    H=G[G.inp].copy(); H["vhi"]=(H.vr>H.vr.median()).astype(float)
    X=np.column_stack([np.ones(len(H)),H.r5,H.r5*H.vhi,H.vhi]); y=H.ex.values
    beta=np.linalg.lstsq(X,y,rcond=None)[0]; e=y-X@beta
    XtX=np.linalg.inv(X.T@X); dayid=H.day.values
    S0=np.zeros((4,4))
    for dval in np.unique(dayid):
        m=dayid==dval; s=(X[m]*e[m,None]).sum(0); S0+=np.outer(s,s)
    se=np.sqrt(np.diag(XtX@S0@XtX))
    out["inprof ex~r5+r5*vhi+vhi"]=pd.DataFrame({"b":beta,"t":beta/se},index=["c","r5","r5xvhi","vhi"]).round(4)
    # book's largest days: what came before
    Dp=D.copy()
    days=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; days.append(d)
    B=pd.concat(days); bk=B.groupby("day")["book_return"].mean().dropna()
    q=bk.quantile([0.02,0.98])
    out["book tails"]=pd.Series({"n":len(bk),"q02":q.iloc[0],"q98":q.iloc[1],"top2pct_sum":bk[bk>=q.iloc[1]].sum(),"bot2pct_sum":bk[bk<=q.iloc[0]].sum(),"total":bk.sum()}).round(4)
    # positions: long vs short contributions in profile
    D["gain"]=D.groupby(["coin","w"])["pos"].shift(1)*D.r1
    out["gain by side"]=D.dropna(subset=["gain"]).assign(side=lambda x:np.sign(x.groupby(["coin","w"])["pos"].shift(1).fillna(0))).groupby(np.sign(D.groupby(["coin","w"])["pos"].shift(1)).reindex(D.index)).agg(n=("gain","size"),mean=("gain","mean"),sum=("gain","sum")).round(5)
    return out
