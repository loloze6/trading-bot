def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        # coin mean returns per horizon on grid
        for h in (12,24,36,48):
            vals=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                vals.extend(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=np.mean(vals)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"].values; v=b["volume"].values
            m=(ts.dt.weekday==6)&(ts.dt.hour==23)
            for i in np.where(m)[0]:
                if i<168: continue
                r48=c[i]/c[i-48]-1
                vr=v[i-47:i+1].mean()/max(v[i-167:i-47].mean(),1e-12)
                # vol of 48h returns proxy: std of hourly returns over prior 720
                lo=max(1,i-720)
                hv=np.std(np.diff(np.log(c[lo:i+1])))
                f=b["forecast"].iloc[i]; a=b["postRebalance_current_allocation"].iloc[i]
                d={"coin":coin,"w":w,"year":ts.iloc[i].year,"f":f,"alloc":a,"r48":r48,"vr":vr,"z48":r48/(hv*np.sqrt(48)) if hv>0 else np.nan,"hv":hv}
                for h in (12,24,36,48):
                    d[f"r{h}"]=c[i+h]/c[i]-1 if i+h<len(c) else np.nan
                    d[f"dr{h}"]=drift[(coin,h)]
                rows.append(d)
    df=pd.DataFrame(rows)
    s=np.sign(df["r48"])
    for h in (12,24,36,48):
        df[f"x{h}"]=s*(df[f"r{h}"]-df[f"dr{h}"])
        df[f"t{h}"]=s*df[f"r{h}"]
    df["nz"]=df["f"]!=0
    out={}
    def summ(g):
        res={"n":len(g)}
        for h in (12,24,36,48):
            x=g[f"x{h}"].dropna()
            res[f"x{h}%"]=x.mean()*100; res[f"t{h}"]=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        res["absalloc"]=g["alloc"].abs().mean(); res["absf"]=g["f"].abs().mean()
        return pd.Series(res)
    df["score"]=df["z48"]*df["vr"]
    df["q_score"]=pd.qcut(df["score"].abs(),5,labels=False)
    out["by_absscore_quint"]=df.groupby("q_score").apply(summ)
    df["q_vr"]=pd.qcut(df["vr"],5,labels=False)
    out["by_volratio_quint"]=df.groupby("q_vr").apply(summ)
    df["q_z"]=pd.qcut(df["z48"].abs(),5,labels=False)
    out["by_absmove_quint"]=df.groupby("q_z").apply(summ)
    df["side"]=np.where(df["r48"]>0,"up","down")
    out["by_side_topscoreq"]=df[df.q_score==4].groupby("side").apply(summ)
    out["by_side_all"]=df.groupby("side").apply(summ)
    out["by_coin_top"]=df[df.q_score>=3].groupby("coin").apply(summ)
    out["by_year_top"]=df[df.q_score>=3].groupby("year").apply(summ)
    out["nz_vs_zero"]=df.groupby("nz").apply(summ)
    # alloc distribution among nonzero forecast
    nz=df[df.nz]
    out["alloc_quantiles_nz"]=nz["alloc"].abs().quantile([.1,.25,.5,.75,.9,.99])
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            dd.append(d.assign(coin=coin,w=w))
    D=pd.concat(dd)
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    out["book_by_weekday"]=D.groupby("wd")["book_return"].agg(["mean","std","count"])
    return out
