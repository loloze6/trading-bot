def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].values; v=b["volume"].values; n=len(b)
            wd=ts.dt.weekday.values; hr=ts.dt.hour.values
            alloc=b["postRebalance_current_allocation"].values
            tv=b["postRebalance_total_value"].values
            idx=np.where((wd==6)&(hr==23))[0]
            for t in idx:
                if t-168<0 or t+48>=n: continue
                vwe=v[t-47:t+1].mean(); vwd=v[t-167:t-47].mean()
                r720=c[t]/c[t-720]-1 if t-720>=0 else np.nan
                lr=np.diff(np.log(c[max(0,t-720):t+1]))
                vol720=np.nanstd(lr) if len(lr)>200 else np.nan
                rows.append(dict(coin=coin,w=w,year=ts[t].year,rwe=c[t]/c[t-48]-1,
                    ratio=vwd/vwe if vwe>0 else np.nan,f48=c[t+48]/c[t]-1,
                    fc=b["forecast"].values[t],alloc=alloc[t],r720=r720,vol720=vol720,
                    bookret=tv[t+48]/tv[t-1]-1))
    d=pd.DataFrame(rows)
    g=d.groupby("coin")
    d["z"]=d["rwe"]/g["rwe"].transform("std")
    d["fz"]=(d["f48"]-g["f48"].transform("mean"))/g["f48"].transform("std")
    d["zr"]=d["z"]*d["ratio"]
    d["lr"]=np.log(d["ratio"])
    out={}
    def slope(x,y):
        m=np.isfinite(x)&np.isfinite(y); r=stats.linregress(x[m],y[m]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":m.sum()})
    out["corr_fc_vs_minus_zr"]=float(np.corrcoef(d["fc"],-d["zr"])[0,1])
    out["corr_fc_vs_minus_z"]=float(np.corrcoef(d["fc"],-d["z"])[0,1])
    out["ratio_desc"]=d["ratio"].describe()
    out["fz_on_fc"]=slope(d["fc"].values,d["fz"].values)
    out["fz_on_zr"]=slope(d["zr"].values,d["fz"].values)
    X=np.c_[np.ones(len(d)),d["z"],d["z"]*d["lr"]]
    m=np.isfinite(X).all(1)&np.isfinite(d["fz"].values)
    beta,res,_,_=np.linalg.lstsq(X[m],d["fz"].values[m],rcond=None)
    e=d["fz"].values[m]-X[m]@beta; s2=e@e/(m.sum()-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X[m].T@X[m])))
    out["interaction_z_zlogratio"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["const","z","z*logratio"])
    d["trq"]=pd.qcut(d["r720"],3,labels=["down30d","flat30d","up30d"])
    out["slope_by_30d_trend"]=d.groupby("trq").apply(lambda q:slope(q["z"].values,q["fz"].values))
    d["vq"]=d.groupby("coin")["vol720"].transform(lambda x:pd.qcut(x,3,labels=False))
    out["slope_by_30d_vol"]=d.groupby("vq").apply(lambda q:slope(q["z"].values,q["fz"].values))
    d["rq"]=pd.qcut(d["ratio"],3,labels=["thick","mid","thin"])
    out["thin_slope_by_trend"]=d[d.rq=="thin"].groupby("trq").apply(lambda q:slope(q["z"].values,q["fz"].values))
    d["fq"]=pd.qcut(d["fc"].abs().rank(method="first"),4,labels=False)
    out["by_abs_fc_quartile"]=d.groupby("fq").agg(absfc=("fc",lambda x:x.abs().mean()),absalloc=("alloc",lambda x:x.abs().mean()),
        dirmove_bp=("f48",lambda x:np.nan),n=("f48","size"))
    d["dm"]=np.sign(d["fc"])*(d["f48"]-g["f48"].transform("mean"))
    out["by_abs_fc_quartile"]["dirmove_bp"]=d.groupby("fq")["dm"].mean()*1e4
    out["book_48h_ret_bp_by_year"]=d.groupby("year")["bookret"].mean()*1e4
    return out
